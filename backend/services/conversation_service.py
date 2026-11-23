"""
Conversation Business Logic Service
Coordinates conversation lifecycle, message threading, validation, and persistence.
Separates business logic from FastAPI route handlers.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from ..database import (
    create_conversation as db_create_conversation,
    get_conversations as db_get_conversations,
    get_conversation_by_id as db_get_conversation_by_id,
    rename_conversation as db_rename_conversation,
    delete_conversation as db_delete_conversation,
    save_message as db_save_message,
    get_messages_for_conversation as db_get_messages_for_conversation,
)
from ..exceptions import EntityNotFoundException, ValidationException

logger = logging.getLogger("sahyogsetu.services.conversation")

class ConversationService:
    """Manages conversations and messages with domain validation and referential integrity."""

    def create(
        self,
        title: Optional[str] = None,
        jurisdiction: str = "all",
        language: str = "en",
        user_id: Optional[str] = None,
        conv_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Creates a new conversation session."""
        cid = conv_id or f"conv_{int(datetime.now().timestamp() * 1000)}"
        clean_title = (title or "").strip() or "New Legal Query"
        clean_jur = (jurisdiction or "all").strip().lower()
        clean_lang = (language or "en").strip().lower()

        logger.info("Creating conversation %s: title='%s', jur='%s', lang='%s'", cid, clean_title, clean_jur, clean_lang)
        return db_create_conversation(
            conv_id=cid,
            title=clean_title,
            jurisdiction=clean_jur,
            language=clean_lang,
            user_id=user_id,
        )

    def list_all(self, limit: int = 50, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves conversation thread summaries."""
        if limit < 1:
            limit = 50
        elif limit > 100:
            limit = 100
        return db_get_conversations(limit=limit, user_id=user_id)

    def get_by_id(self, conv_id: str) -> Dict[str, Any]:
        """Retrieves conversation summary or raises EntityNotFoundException."""
        conv = db_get_conversation_by_id(conv_id)
        if not conv:
            raise EntityNotFoundException("Conversation", conv_id)
        return conv

    def get_with_messages(self, conv_id: str) -> Dict[str, Any]:
        """Retrieves conversation summary along with its chronological messages."""
        conv = self.get_by_id(conv_id)
        messages = db_get_messages_for_conversation(conv_id)
        conv["messages"] = messages
        conv["message_count"] = len(messages)
        conv["messageCount"] = len(messages)
        return conv

    def rename(self, conv_id: str, new_title: str) -> Dict[str, Any]:
        """Renames an existing conversation or raises EntityNotFoundException."""
        clean_title = (new_title or "").strip()
        if not clean_title:
            raise ValidationException("Conversation title cannot be empty.")

        # Ensure conversation exists
        self.get_by_id(conv_id)

        ok = db_rename_conversation(conv_id, clean_title)
        if not ok:
            raise EntityNotFoundException("Conversation", conv_id)

        logger.info("Renamed conversation %s to '%s'", conv_id, clean_title)
        return {
            "success": True,
            "conversation_id": conv_id,
            "conversationId": conv_id,
            "title": clean_title,
        }

    def delete(self, conv_id: str) -> Dict[str, Any]:
        """Deletes conversation and cascades deletion to messages and feedback."""
        # Ensure conversation exists
        self.get_by_id(conv_id)

        ok = db_delete_conversation(conv_id)
        if not ok:
            raise EntityNotFoundException("Conversation", conv_id)

        logger.info("Deleted conversation %s and all associated messages", conv_id)
        return {
            "success": True,
            "conversation_id": conv_id,
            "conversationId": conv_id,
            "message": "Conversation deleted successfully",
        }

    def add_message(
        self,
        conv_id: str,
        role: str,
        content: str,
        language: str = "en",
        metadata: Optional[Dict[str, Any]] = None,
        msg_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Appends a validated message to a conversation."""
        # Ensure conversation exists
        self.get_by_id(conv_id)

        clean_role = (role or "").strip().lower()
        if clean_role not in ("user", "assistant", "system"):
            clean_role = "user"

        clean_content = content if content is not None else ""
        mid = msg_id or f"msg_{int(datetime.now().timestamp() * 1000)}"

        db_save_message(
            msg_id=mid,
            conv_id=conv_id,
            role=clean_role,
            content=clean_content,
            language=language or "en",
            metadata=metadata,
        )

        return {
            "message_id": mid,
            "id": mid,
            "conversation_id": conv_id,
            "conversationId": conv_id,
            "role": clean_role,
            "sender": clean_role,
            "content": clean_content,
            "text": clean_content,
            "language": language or "en",
            "metadata": metadata,
            "payload": metadata,
            "created_at": datetime.now().isoformat(),
            "timestamp": datetime.now().isoformat(),
        }

    def get_messages(self, conv_id: str) -> List[Dict[str, Any]]:
        """Retrieves messages for a conversation, validating conversation existence."""
        self.get_by_id(conv_id)
        return db_get_messages_for_conversation(conv_id)

conversation_service = ConversationService()
