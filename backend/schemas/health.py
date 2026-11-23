"""
Health & Diagnostic Schemas
"""

from typing import Dict, Any
from pydantic import BaseModel, Field

class ComponentStatus(BaseModel):
    status: str
    details: Dict[str, Any] = Field(default_factory=dict)

class HealthCheckResponse(BaseModel):
    status: str = "healthy"
    service: str = "SahyogSetu Backend API"
    version: str = "2.0.0"
    database: Dict[str, Any] = Field(default_factory=dict)
    tts: Dict[str, Any] = Field(default_factory=dict)
    bhashini: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str
