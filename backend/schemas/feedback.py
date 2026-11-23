"""
Feedback Schemas
Validation for user helpfulness ratings and feedback comments.
"""

from typing import Optional
from pydantic import BaseModel, Field

class FeedbackSubmitRequest(BaseModel):
    messageId: Optional[str] = Field(None, max_length=100, description="CamelCase message identifier")
    message_id: Optional[str] = Field(None, max_length=100, description="Snake_case message identifier")
    rating: str = Field(..., max_length=50, description="Rating: helpful, not_helpful, thumbs_up, thumbs_down, 1-5")
    comments: Optional[str] = Field(None, max_length=1000, description="User comments")
    comment: Optional[str] = Field(None, max_length=1000, description="Alternative singular comment key")
    feedback_text: Optional[str] = Field(None, max_length=1000, description="Standard database feedback text key")
    conversationId: Optional[str] = Field(None, max_length=100, description="CamelCase conversation identifier")
    conversation_id: Optional[str] = Field(None, max_length=100, description="Snake_case conversation identifier")

    def get_message_id(self) -> str:
        mid = self.messageId or self.message_id
        if not mid or not mid.strip():
            raise ValueError("message_id is required for feedback submission.")
        return mid.strip()

    def get_conversation_id(self) -> Optional[str]:
        cid = self.conversationId or self.conversation_id
        return cid.strip() if cid and cid.strip() else None

    def get_feedback_text(self) -> str:
        return (self.feedback_text or self.comments or self.comment or "").strip()

class FeedbackSubmitResponse(BaseModel):
    success: bool = True
    feedbackId: str
    feedback_id: str
    message: str = "Feedback recorded successfully"
