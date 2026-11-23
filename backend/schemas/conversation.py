"""
Conversation & Message Pydantic Schemas
Defines request and response validation contracts for conversation threads.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ConversationCreateRequest(BaseModel):
    initialTitle: Optional[str] = Field(None, max_length=200, description="Initial conversation title")
    title: Optional[str] = Field(None, max_length=200, description="Alternative title key")
    language: str = Field("en", max_length=10, description="Interface language code (en, hi, pa, doi, bgc)")
    jurisdiction: str = Field("all", max_length=50, description="Applicable jurisdiction (central, punjab, haryana, jk, all)")
    user_id: Optional[str] = Field(None, max_length=100, description="Optional user identifier for multi-user setups")

class ConversationRenameRequest(BaseModel):
    title: Optional[str] = Field(None, max_length=200, description="New conversation title")
    newTitle: Optional[str] = Field(None, max_length=200, description="Alternative key for new title")

    def get_title(self) -> str:
        t = self.title or self.newTitle
        if not t or not t.strip():
            raise ValueError("Conversation title cannot be empty.")
        return t.strip()

class MessageResponse(BaseModel):
    message_id: str = Field(..., description="Unique message ID")
    id: str = Field(..., description="Alias for message_id")
    conversation_id: str = Field(..., description="ID of parent conversation")
    conversationId: str = Field(..., description="Alias for conversation_id")
    role: str = Field(..., description="Sender role: user, assistant, system")
    sender: str = Field(..., description="Alias for role")
    content: str = Field(..., description="Message text content")
    text: str = Field(..., description="Alias for content")
    language: str = Field("en", description="Message language")
    created_at: str = Field(..., description="ISO creation timestamp")
    timestamp: str = Field(..., description="Alias for created_at")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Structured message metadata / citations")
    payload: Optional[Dict[str, Any]] = Field(None, description="Alias for metadata")

class ConversationSummary(BaseModel):
    conversation_id: str = Field(..., description="Unique conversation ID")
    id: str = Field(..., description="Alias for conversation_id")
    conversationId: str = Field(..., description="Alias for conversation_id")
    title: str = Field(..., description="Conversation title")
    user_id: Optional[str] = Field(None, description="User ID if set")
    jurisdiction: str = Field("all", description="Jurisdiction")
    language: str = Field("en", description="Interface language")
    created_at: str = Field(..., description="ISO creation timestamp")
    createdAt: str = Field(..., description="Alias for created_at")
    updated_at: str = Field(..., description="ISO update timestamp")
    updatedAt: str = Field(..., description="Alias for updated_at")
    message_count: int = Field(0, description="Number of messages in thread")
    messageCount: int = Field(0, description="Alias for message_count")
    is_bookmarked: bool = Field(False, description="Whether pinned/bookmarked")
    isBookmarked: bool = Field(False, description="Alias for is_bookmarked")

class ConversationDetailResponse(ConversationSummary):
    messages: List[MessageResponse] = Field(default_factory=list, description="Messages in thread")

class ConversationListResponse(BaseModel):
    conversations: List[ConversationSummary] = Field(default_factory=list)
    source: str = "live_backend"
    total: int = 0

class ConversationCreateResponse(BaseModel):
    conversation_id: str
    id: str
    conversationId: str
    title: str
    createdAt: str
    created_at: str
    source: str = "live_backend"

class ConversationRenameResponse(BaseModel):
    success: bool = True
    conversationId: str
    conversation_id: str
    title: str

class ConversationDeleteResponse(BaseModel):
    success: bool = True
    conversationId: str
    conversation_id: str
    message: str = "Conversation deleted successfully"
