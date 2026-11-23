"""
SahyogSetu Backend API Application
FastAPI entrypoint providing modular REST endpoints for:
1. Legal RAG Chatbot (source-grounded retrieval, citation validation, multi-jurisdiction)
2. Conversation History & Message Persistence (SQLite with referential integrity)
3. Document Analysis & Upload (PDF/text extraction & statutory clause extraction)
4. Citizen Feedback & Helpful Evaluations
5. Official Government News Aggregation & Multilingual NLP
6. Multilingual Text-to-Speech (TTS) & Dialect Ethics
7. Automatic Speech Recognition (ASR) & Machine Translation (NMT)
8. Bhashini Integration & Health Monitoring
9. Quantitative Retrieval Evaluation (Precision@K, Recall@K, MRR)
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from .config import settings
from .exceptions import SahyogSetuException, sahyogsetu_exception_handler
from .database import init_db
from .security.logging_middleware import RequestTracingMiddleware
from .security.rate_limiter import RateLimitMiddleware
from .api import (
    health_router,
    chat_router,
    conversations_router,
    feedback_router,
    documents_router,
    news_router,
    tts_router,
    voice_router,
    evaluation_router,
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("sahyogsetu.main")

def create_app() -> FastAPI:
    """Initializes and configures the FastAPI application with routers and middleware."""
    app = FastAPI(
        title=settings.APP_NAME,
        description="Official, source-backed legal assistance, news aggregation, and Indian-language AI services for cooperative societies.",
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # 0. Request Tracing & Correlation ID Middleware
    app.add_middleware(RequestTracingMiddleware)

    # 1. Sliding-Window Rate Limiting Middleware
    if settings.RATE_LIMIT_ENABLED:
        app.add_middleware(RateLimitMiddleware, enabled=True)

    # 2. CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 3. Exception Handlers
    app.add_exception_handler(SahyogSetuException, sahyogsetu_exception_handler)

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error("Unhandled exception processing request to %s: %s", request.url.path, exc, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "code": 500,
                "message": "The legal service encountered an internal issue. Statutory knowledge remains safely accessible.",
                "request_id": getattr(request.state, "request_id", None),
            },
        )

    # 3. Mount Modular API Routers
    app.include_router(health_router)
    app.include_router(chat_router)
    app.include_router(conversations_router)
    app.include_router(feedback_router)
    app.include_router(documents_router)
    app.include_router(news_router)
    app.include_router(tts_router)
    app.include_router(voice_router)
    app.include_router(evaluation_router)

    # 4. Lifecycle Event: Database Initialization & Safe Migration
    @app.on_event("startup")
    async def on_startup():
        logger.info("Validating SahyogSetu environment configuration...")
        env_report = settings.validate_environment()
        if not env_report["valid"]:
            logger.error("Environment configuration errors: %s", env_report["errors"])
            if settings.APP_ENV == "production":
                raise RuntimeError(f"Production environment validation failed: {env_report['errors']}")
        if env_report["warnings"]:
            logger.warning("Environment configuration warnings: %s", env_report["warnings"])

        logger.info("Initializing SahyogSetu database and verifying tables...")
        init_db()
        logger.info("SahyogSetu Backend API (%s) initialized successfully in %s mode.", settings.APP_VERSION, settings.APP_ENV)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
