"""
SahyogSetu Structured Request Tracing & Privacy-Safe Logging Middleware
Assigns X-Request-ID to all incoming calls.
Logs performance latency and response codes while strictly scrubbing secrets and PII.
"""

import time
import uuid
import re
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("sahyogsetu.access")

# Regular expressions for scrubbing sensitive patterns
SECRET_TOKEN_REGEX = re.compile(r"(?:Bearer\s+[A-Za-z0-9_\-\.]{15,}|sk-[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_\-]{30,})", re.IGNORECASE)
AADHAAR_REGEX = re.compile(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}\b")
OTP_REGEX = re.compile(r"\b(?:otp|pin)[:=\s]+[0-9]{4,6}\b", re.IGNORECASE)


def scrub_sensitive_string(text: str) -> str:
    """Masks secrets, tokens, Aadhaar numbers, and OTPs in log strings."""
    if not text:
        return ""
    text = SECRET_TOKEN_REGEX.sub("[TOKEN_REDACTED]", text)
    text = AADHAAR_REGEX.sub("[AADHAAR_REDACTED]", text)
    text = OTP_REGEX.sub("[OTP_REDACTED]", text)
    return text


class RequestTracingMiddleware(BaseHTTPMiddleware):
    """Assigns unique correlation ID and logs structured request latency without PII."""

    async def dispatch(self, request: Request, call_next):
        # 1. Resolve or generate correlation Request ID
        request_id = request.headers.get("x-request-id") or f"req_{uuid.uuid4().hex[:12]}"
        start_time = time.time()

        # 2. Attach request_id to request state for handler access
        request.state.request_id = request_id

        # 3. Process request
        response = await call_next(request)

        # 4. Compute latency
        duration_ms = round((time.time() - start_time) * 1000, 2)
        response.headers["X-Request-ID"] = request_id

        # 5. Privacy-safe structured log
        client_ip = (
            request.headers.get("x-forwarded-for", "").split(",")[0].strip()
            or request.client.host if request.client else "127.0.0.1"
        )
        safe_path = scrub_sensitive_string(request.url.path)
        safe_query = scrub_sensitive_string(request.url.query)
        full_endpoint = f"{safe_path}?{safe_query}" if safe_query else safe_path

        log_msg = f"{request.method} {full_endpoint} -> {response.status_code} ({duration_ms}ms) [client={client_ip}] [id={request_id}]"

        if response.status_code >= 500:
            logger.error(log_msg)
        elif response.status_code >= 400:
            logger.warning(log_msg)
        else:
            logger.info(log_msg)

        return response
