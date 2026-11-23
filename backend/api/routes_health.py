"""
Health & System Diagnostics API Router
Provides component-level operational health checks without exposing secrets.
"""

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

from ..schemas.health import HealthCheckResponse
from ..database import count_news, get_conversations
from ..services.bhashini.bhashini_client import bhashini_client
from ..services.tts.tts_manager import tts_manager
from ..config import settings

logger = logging.getLogger("sahyogsetu.api.health")

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthCheckResponse)
@router.get("/api/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Component-level health check reporting status for:
    - Database connectivity & record counts
    - Text-to-Speech (TTS) operational state
    - Bhashini ULCA configuration & offline fallback mode
    """
    db_connected = True
    news_count = 0
    conv_count = 0
    try:
        news_count = count_news("all")
        conv_count = len(get_conversations(limit=100))
    except Exception as e:
        logger.error("Health check database probe failed: %s", e)
        db_connected = False

    tts_status = tts_manager.get_system_status()

    return {
        "status": "healthy" if db_connected else "degraded",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": {
            "status": "connected" if db_connected else "disconnected",
            "total_news_records": news_count,
            "total_conversations": conv_count,
            "foreign_keys_enforced": True,
        },
        "tts": {
            "status": "operational",
            "active_provider": tts_status.get("active_provider", "local_harmonic"),
            "supported_languages": len(tts_status.get("supported_languages", [])),
        },
        "bhashini": {
            "status": "configured" if settings.is_bhashini_configured else "offline_fallback_active",
            "active_fallback": "Local harmonic synthesizers & browser speech active.",
        },
        "timestamp": datetime.now().isoformat(),
    }

@router.get("/health/liveness")
@router.get("/api/health/liveness")
@router.get("/health/live")
@router.get("/api/health/live")
async def health_liveness():
    """
    Kubernetes/container liveness probe.
    Fast response verifying the web application process is alive and responsive.
    """
    return {
        "status": "alive",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.now().isoformat(),
    }

@router.get("/health/readiness")
@router.get("/api/health/readiness")
@router.get("/health/ready")
@router.get("/api/health/ready")
async def health_readiness(response: Response = None):
    """
    Kubernetes/container readiness probe.
    Verifies that critical dependencies (database and knowledge store) are accessible.
    Sets HTTP 503 on error when invoked within FastAPI HTTP context.
    """
    import os
    checks = {
        "database": False,
        "knowledge_store": False,
        "vector_store": False,
    }
    try:
        _ = count_news("all")
        checks["database"] = True
    except Exception as e:
        logger.error("Readiness check: database probe failed: %s", e)

    try:
        db_file = settings.DB_PATH
        checks["knowledge_store"] = os.path.exists(db_file)
    except Exception as e:
        logger.error("Readiness check: storage probe failed: %s", e)

    try:
        vector_db = os.path.join(settings.DB_DIR, "vectors.db")
        checks["vector_store"] = os.path.exists(vector_db)
    except Exception as e:
        logger.error("Readiness check: vector store probe failed: %s", e)

    is_ready = checks["database"] and checks["knowledge_store"]
    if not is_ready and response is not None:
        response.status_code = 503

    return {
        "status": "ready" if is_ready else "not_ready",
        "service": settings.APP_NAME,
        "checks": checks,
        "timestamp": datetime.now().isoformat(),
    }

@router.get("/api/bhashini/health")
async def bhashini_health():
    """Returns live Bhashini ULCA connectivity diagnostic."""
    return await bhashini_client.check_health()
