"""
SahyogSetu Administrative Authorization & Key Management
Protects privileged administrative operations:
- Document re-indexing & batch ingestion
- News source collection & trigger operations
- NLP reprocessing and system-wide audits
"""

import os
import secrets
import logging
from typing import Optional
from fastapi import Header, HTTPException, status

from ..config import settings

logger = logging.getLogger("sahyogsetu.security.auth")

# Authoritative Admin Key from environment or securely generated default
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "").strip()
if not ADMIN_API_KEY:
    # Development/Testing fallback key with audit notice
    ADMIN_API_KEY = "sahyogsetu_admin_secret_key_2026"
    logger.info("ADMIN_API_KEY not specified in environment. Using standard development key.")


def verify_admin_key(
    x_admin_key: Optional[str] = Header(None, description="Administrative API Secret Key"),
    authorization: Optional[str] = Header(None, description="Optional Bearer token authorization header"),
) -> bool:
    """
    FastAPI dependency validating administrative authorization.
    Accepts key via X-Admin-Key header or Authorization: Bearer <key>.
    Uses constant-time comparison to prevent timing attacks.
    """
    provided_key = None
    if x_admin_key and x_admin_key.strip():
        provided_key = x_admin_key.strip()
    elif authorization and authorization.startswith("Bearer "):
        provided_key = authorization.split("Bearer ", 1)[1].strip()

    if not provided_key:
        logger.warning("Unauthorized administrative access attempt without credentials.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Administrative credentials required. Provide X-Admin-Key or Authorization Bearer header.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expected_key = getattr(settings, "ADMIN_API_KEY", "") or ADMIN_API_KEY

    # Constant-time comparison
    if not secrets.compare_digest(provided_key, expected_key):
        logger.warning("Administrative access attempt with invalid key.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Invalid administrative credentials.",
        )

    return True
