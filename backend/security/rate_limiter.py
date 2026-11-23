"""
SahyogSetu In-Memory Sliding-Window Rate Limiter
Prevents API exhaustion, brute-force requests, and compute starvation.
Requires zero external infrastructure (Redis-free, thread-safe, sliding-window).
"""

import time
import threading
from typing import Dict, List, Tuple
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

# Tiered rate limits (requests per 60-second window per client IP)
ROUTE_LIMITS: Dict[str, int] = {
    "/api/chat": 30,
    "/chat": 30,
    "/api/tts": 25,
    "/api/asr": 20,
    "/api/translate": 40,
    "/api/documents/analyze": 10,
    "/api/documents/ingest": 5,
    "/api/documents/reindex": 5,
    "/api/news/collect": 5,
    "/api/news/refresh": 5,
    "/api/feedback": 30,
    "default": 120,
}

WINDOW_SECONDS = 60


class SlidingWindowRateLimiter:
    """Thread-safe in-memory sliding window request tracker."""

    def __init__(self):
        self._lock = threading.Lock()
        # client_ip -> {route_prefix -> [timestamps]}
        self._store: Dict[str, Dict[str, List[float]]] = {}
        self._last_clean = time.time()

    def _get_route_limit(self, path: str) -> Tuple[str, int]:
        for prefix, limit in ROUTE_LIMITS.items():
            if prefix != "default" and path.startswith(prefix):
                return prefix, limit
        return "default", ROUTE_LIMITS["default"]

    def is_allowed(self, client_ip: str, path: str) -> Tuple[bool, int, int]:
        """
        Checks if client IP is within rate limits.
        Returns (is_allowed: bool, remaining: int, retry_after_seconds: int).
        """
        prefix, limit = self._get_route_limit(path)
        now = time.time()

        with self._lock:
            # Periodic cleanup of expired clients every 2 minutes
            if now - self._last_clean > 120:
                self._cleanup(now)
                self._last_clean = now

            if client_ip not in self._store:
                self._store[client_ip] = {}
            if prefix not in self._store[client_ip]:
                self._store[client_ip][prefix] = []

            # Prune timestamps older than window
            window_start = now - WINDOW_SECONDS
            timestamps = [t for t in self._store[client_ip][prefix] if t > window_start]
            self._store[client_ip][prefix] = timestamps

            if len(timestamps) >= limit:
                oldest = timestamps[0]
                retry_after = max(1, int(WINDOW_SECONDS - (now - oldest)))
                return False, 0, retry_after

            # Record this request
            timestamps.append(now)
            remaining = limit - len(timestamps)
            return True, remaining, 0

    def _cleanup(self, now: float):
        """Removes expired IPs and route buckets."""
        window_start = now - WINDOW_SECONDS
        dead_ips = []
        for ip, routes in self._store.items():
            dead_routes = []
            for r, ts in routes.items():
                routes[r] = [t for t in ts if t > window_start]
                if not routes[r]:
                    dead_routes.append(r)
            for dr in dead_routes:
                del routes[dr]
            if not routes:
                dead_ips.append(ip)
        for dip in dead_ips:
            del self._store[dip]


rate_limiter = SlidingWindowRateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """FastAPI/Starlette middleware enforcing rate limits with citizen-friendly responses."""

    def __init__(self, app, enabled: bool = True):
        super().__init__(app)
        self.enabled = enabled

    async def dispatch(self, request: Request, call_next):
        if not self.enabled:
            return await call_next(request)

        # Skip rate-limiting for static assets and documentation
        path = request.url.path
        if path in ("/docs", "/redoc", "/openapi.json", "/favicon.ico"):
            return await call_next(request)

        # Determine client IP (respecting forward proxies if present)
        client_ip = (
            request.headers.get("x-forwarded-for", "").split(",")[0].strip()
            or request.client.host if request.client else "127.0.0.1"
        )

        allowed, remaining, retry_after = rate_limiter.is_allowed(client_ip, path)
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "status": "error",
                    "code": 429,
                    "message": "Too many requests. Please wait a moment before trying again.",
                    "retry_after_seconds": retry_after,
                },
                headers={"Retry-After": str(retry_after)},
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
