"""
Voice & Speech Processing Schemas
"""

from typing import Optional
from pydantic import BaseModel, Field

class ASRTranscribeRequest(BaseModel):
    audio_base64: str = Field(..., max_length=15_000_000, description="Base64 encoded audio bytes")
    language: str = Field("hi", max_length=10, description="Spoken language code")
    audio_format: str = Field("wav", max_length=10, description="Audio container/format: wav, mp3, webm")

class TTSGenerateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, description="Text to synthesize")
    language: str = Field("en", max_length=10, description="Target language code")
    voice_gender: str = Field("female", max_length=10, description="Voice gender: female or male")
    response_id: Optional[str] = Field(None, max_length=100, description="Optional associated response ID")
    alternative_accepted: Optional[str] = Field(None, max_length=50, description="Alternative dialect accepted")
    bypass_cache: bool = Field(False, description="Whether to bypass local audio cache")

class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Source text to translate")
    source_language: str = Field("en", max_length=10, description="Source language code")
    target_language: str = Field("hi", max_length=10, description="Target language code")
