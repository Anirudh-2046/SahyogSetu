"""API Route Modules for SahyogSetu."""
from .routes_conversations import router as conversations_router
from .routes_chat import router as chat_router
from .routes_feedback import router as feedback_router
from .routes_documents import router as documents_router
from .routes_health import router as health_router
from .routes_news import router as news_router
from .routes_tts import router as tts_router
from .routes_voice import router as voice_router
from .routes_evaluation import router as evaluation_router

__all__ = [
    "conversations_router",
    "chat_router",
    "feedback_router",
    "documents_router",
    "health_router",
    "news_router",
    "tts_router",
    "voice_router",
    "evaluation_router",
]
