"""
Feedback API Router
Receives and records citizen helpfulness ratings and comments.
"""

from fastapi import APIRouter
import logging

from ..schemas.feedback import FeedbackSubmitRequest, FeedbackSubmitResponse
from ..services.feedback_service import feedback_service

logger = logging.getLogger("sahyogsetu.api.feedback")

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])

@router.post("", response_model=FeedbackSubmitResponse)
async def submit_feedback(req: FeedbackSubmitRequest):
    """Records user feedback and evaluation metrics in SQLite."""
    res = feedback_service.submit(
        message_id=req.get_message_id(),
        rating=req.rating,
        feedback_text=req.get_feedback_text(),
        conversation_id=req.get_conversation_id(),
    )
    return res
