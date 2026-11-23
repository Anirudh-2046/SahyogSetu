"""
Feedback Business Logic Service
Handles user evaluation, helpfulness feedback recording, and validation.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import logging

from ..database import (
    save_feedback as db_save_feedback,
    get_feedback_by_id as db_get_feedback_by_id,
    get_conversation_by_id,
)
from ..exceptions import ValidationException

logger = logging.getLogger("sahyogsetu.services.feedback")

class FeedbackService:
    """Processes citizen feedback on legal responses and recommendations."""

    def submit(
        self,
        message_id: str,
        rating: str,
        feedback_text: Optional[str] = None,
        conversation_id: Optional[str] = None,
        feedback_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Validates and records user feedback."""
        clean_mid = (message_id or "").strip()
        if not clean_mid:
            raise ValidationException("message_id is required for feedback submission.")

        clean_rating = (rating or "").strip().lower()
        if not clean_rating:
            raise ValidationException("rating is required for feedback submission.")

        fid = feedback_id or f"fb_{int(datetime.now().timestamp() * 1000)}"
        clean_text = (feedback_text or "").strip()

        # If conversation_id is provided, verify it exists so FK constraint succeeds
        clean_cid = conversation_id.strip() if conversation_id and conversation_id.strip() else None
        if clean_cid:
            conv = get_conversation_by_id(clean_cid)
            if not conv:
                logger.warning("Conversation %s not found for feedback; detaching conversation_id", clean_cid)
                clean_cid = None

        db_save_feedback(
            feedback_id=fid,
            message_id=clean_mid,
            rating=clean_rating,
            feedback_text=clean_text,
            conv_id=clean_cid,
        )

        logger.info("Feedback %s recorded for message %s with rating '%s'", fid, clean_mid, clean_rating)
        return {
            "success": True,
            "feedbackId": fid,
            "feedback_id": fid,
            "message": "Feedback recorded successfully",
        }

    def get_by_id(self, feedback_id: str) -> Optional[Dict[str, Any]]:
        return db_get_feedback_by_id(feedback_id)

feedback_service = FeedbackService()
