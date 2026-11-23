"""
Conversations API Router
Handles conversation lifecycle, history loading, renaming, and cascading deletion.
"""

from typing import Optional
from fastapi import APIRouter, Query, status
import logging

from ..schemas.conversation import (
    ConversationCreateRequest,
    ConversationCreateResponse,
    ConversationRenameRequest,
    ConversationRenameResponse,
    ConversationDeleteResponse,
    ConversationListResponse,
    ConversationDetailResponse,
)
from ..services.conversation_service import conversation_service

logger = logging.getLogger("sahyogsetu.api.conversations")

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])

@router.get("", response_model=ConversationListResponse)
async def list_conversations(
    limit: int = Query(50, ge=1, le=100, description="Max conversation threads to return"),
    user_id: Optional[str] = Query(None, description="Optional user filter")
):
    """Retrieves conversation thread summaries from SQLite database."""
    convs = conversation_service.list_all(limit=limit, user_id=user_id)
    return {
        "conversations": convs,
        "source": "live_backend",
        "total": len(convs),
    }

@router.post("", response_model=ConversationCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(req: ConversationCreateRequest):
    """Initializes a new conversation session."""
    title = req.initialTitle or req.title or "New Legal Query"
    res = conversation_service.create(
        title=title,
        jurisdiction=req.jurisdiction,
        language=req.language,
        user_id=req.user_id,
    )
    return {
        "conversation_id": res["conversation_id"],
        "id": res["conversation_id"],
        "conversationId": res["conversation_id"],
        "title": res["title"],
        "createdAt": res["created_at"],
        "created_at": res["created_at"],
        "source": "live_backend",
    }

@router.get("/{conv_id}", response_model=ConversationDetailResponse)
async def get_conversation(conv_id: str):
    """Retrieves conversation details and its chronological messages."""
    return conversation_service.get_with_messages(conv_id)

@router.get("/{conv_id}/messages")
async def get_conversation_messages(conv_id: str):
    """Retrieves full message history of a conversation."""
    msgs = conversation_service.get_messages(conv_id)
    return {
        "conversationId": conv_id,
        "conversation_id": conv_id,
        "messages": msgs,
    }

@router.patch("/{conv_id}/title", response_model=ConversationRenameResponse)
@router.patch("/{conv_id}", response_model=ConversationRenameResponse)
async def rename_conversation(conv_id: str, req: ConversationRenameRequest):
    """Renames an existing conversation."""
    new_title = req.get_title()
    res = conversation_service.rename(conv_id, new_title)
    return res

@router.delete("/{conv_id}", response_model=ConversationDeleteResponse)
async def delete_conversation(conv_id: str):
    """Deletes a conversation and all its associated messages."""
    return conversation_service.delete(conv_id)
