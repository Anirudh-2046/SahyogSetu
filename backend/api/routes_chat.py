"""
Chat API Router
Executes source-grounded legal and scheme retrieval.
Guarantees that every answer provides direct official URLs and page-level evidence.
Persists messages to database when a conversation thread is active.
"""

from fastapi import APIRouter
import logging

from ..schemas.chat import ChatQueryRequest, ChatQueryResponse
from ..services.conversation_service import conversation_service
from ..services.sources.source_resolver import source_resolver
from ..exceptions import EntityNotFoundException
from ..security.input_sanitizer import sanitize_user_query

logger = logging.getLogger("sahyogsetu.api.chat")

router = APIRouter(tags=["Chat"])

@router.post("/api/chat", response_model=ChatQueryResponse)
@router.post("/chat", response_model=ChatQueryResponse)
async def handle_chat_query(req: ChatQueryRequest):
    """
    Executes source-grounded legal retrieval for cooperative societies.
    Persists query and answer if conversationId is specified.
    """
    conv_id = req.get_conversation_id()
    attached = req.get_attached_doc()

    # Sanitize citizen query to neutralize adversarial injection attempts
    clean_query, had_injection = sanitize_user_query(req.query)
    if had_injection:
        logger.warning("Neutralized potential prompt injection attempt in conversation %s", conv_id)

    # If conversation_id is provided, ensure thread exists or auto-create
    if conv_id:
        try:
            conversation_service.get_by_id(conv_id)
        except EntityNotFoundException:
            # Auto-create conversation thread
            title = clean_query[:50] + ("..." if len(clean_query) > 50 else "")
            conversation_service.create(
                title=title,
                jurisdiction=req.jurisdiction,
                language=req.language,
                conv_id=conv_id,
            )

    # 1. Execute full source resolution workflow
    result = source_resolver.resolve_query(
        query=clean_query,
        language=req.language,
        jurisdiction=req.jurisdiction,
        attached_doc=attached,
    )

    # 2. Persist messages if conversation_id is active
    if conv_id:
        conversation_service.add_message(
            conv_id=conv_id,
            role="user",
            content=clean_query,
            language=req.language,
            metadata=attached,
        )
        conversation_service.add_message(
            conv_id=conv_id,
            role="assistant",
            content=result.get("summary", ""),
            language=req.language,
            metadata=result,
            msg_id=result.get("id"),
        )

    resolved_conv_id = conv_id or f"conv_{result.get('id', 'temp')}"
    return {
        "conversationId": resolved_conv_id,
        "conversation_id": resolved_conv_id,
        "response": result,
        "source": "live_backend",
    }
