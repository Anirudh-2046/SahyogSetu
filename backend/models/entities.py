"""
Database Entity Models
Typed dataclass representations for SQLite table rows.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class ConversationModel:
    conversation_id: str
    title: str
    jurisdiction: str = "all"
    language: str = "en"
    user_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    is_bookmarked: bool = False

@dataclass
class MessageModel:
    message_id: str
    conversation_id: str
    role: str
    content: str
    language: str = "en"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class FeedbackModel:
    feedback_id: str
    message_id: str
    rating: str
    feedback_text: Optional[str] = None
    conversation_id: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class UploadedDocumentModel:
    id: str
    filename: str
    file_size: int
    extracted_text: Optional[str] = None
    jurisdiction: str = "central"
    language: str = "en"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
