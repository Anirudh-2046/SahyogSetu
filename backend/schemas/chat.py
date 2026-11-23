"""
Chat Request & Response Schemas
Validation schemas for the legal assistant query and response contracts.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class ChatQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="User legal or procedural question")
    language: Optional[str] = Field("en", max_length=10, description="User interface language code")
    jurisdiction: str = Field("all", max_length=50, description="Selected jurisdiction filter")
    conversation_id: Optional[str] = Field(None, max_length=100, description="Optional conversation ID for persistence")
    conversationId: Optional[str] = Field(None, max_length=100, description="CamelCase alias for conversation_id")
    attached_doc: Optional[Dict[str, Any]] = Field(None, description="Optional uploaded document attachment")
    attachedDoc: Optional[Dict[str, Any]] = Field(None, description="CamelCase alias for attached_doc")

    def get_conversation_id(self) -> Optional[str]:
        return self.conversation_id or self.conversationId

    def get_attached_doc(self) -> Optional[Dict[str, Any]]:
        return self.attached_doc or self.attachedDoc

class ChatQueryResponse(BaseModel):
    conversationId: str
    conversation_id: str
    response: Dict[str, Any]
    source: str = "live_backend"
