"""
Language Service Data Schemas
Pydantic contracts for NMT, ASR, TTS, and language capabilities.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Translation (NMT)
# ---------------------------------------------------------------------------
class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Source text to translate")
    source_language: str = Field("en", description="ISO 639-1/3 source language code")
    target_language: str = Field("hi", description="ISO 639-1/3 target language code")
    preserve_legal_entities: bool = Field(True, description="Whether to protect statutory sections, amounts, and URLs")

class TranslationResponse(BaseModel):
    original_text: str
    source_language: str
    target_language: str
    translated_text: str
    provider: str
    protected_entities_count: int = 0
    is_fallback: bool = False
    status: str = "success"

# ---------------------------------------------------------------------------
# Automatic Speech Recognition (ASR)
# ---------------------------------------------------------------------------
class ASRTranscribeRequest(BaseModel):
    audio_base64: str = Field(..., description="Base64 encoded audio bytes")
    language: str = Field("hi", description="Spoken language code: en, hi, pa, doi, bgc")
    audio_format: str = Field("wav", description="Audio format: wav, mp3, webm, ogg")

class ASRTranscribeResponse(BaseModel):
    status: str = Field("success", description="success, error, or fallback_client_speech")
    transcript: str = Field("", description="Recognized speech text")
    language: str = Field("hi", description="Language code")
    provider: str = Field("Bhashini ULCA ASR", description="Speech provider name")
    confidence: Optional[float] = Field(None, description="Recognition confidence if reported by provider")
    requires_user_review: bool = Field(True, description="Always true for citizen legal transparency")
    error_code: Optional[str] = None
    message: Optional[str] = None

class ASRCapabilitiesResponse(BaseModel):
    language: str
    is_native_supported: bool
    provider: str
    disclaimer: Optional[str] = None
    bhashini_configured: bool = False
    supported_formats: List[str] = ["wav", "mp3", "webm", "ogg"]
    max_duration_seconds: int = 60
    max_file_size_bytes: int = 10 * 1024 * 1024

# ---------------------------------------------------------------------------
# Text-to-Speech (TTS)
# ---------------------------------------------------------------------------
class TTSGenerateRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to synthesize")
    language: str = Field("en", description="Target language code: en, hi, pa, doi, bgc")
    voice_gender: str = Field("female", description="female or male")
    response_id: Optional[str] = Field(None, description="Optional associated response ID")
    alternative_accepted: Optional[str] = Field(None, description="Alternative dialect accepted")
    bypass_cache: bool = Field(False, description="Whether to bypass local audio cache")

class TTSGenerateResponse(BaseModel):
    status: str = Field("success", description="success, error, alternative_offered, unavailable")
    audio_url: Optional[str] = None
    audio_format: Optional[str] = None
    requested_language: str
    actual_language: str
    is_alternative: bool = False
    provider: Optional[str] = None
    model: Optional[str] = None
    audio_id: Optional[str] = None
    cached: bool = False
    message: Optional[str] = None
    suggested_alternatives: Optional[List[Dict[str, str]]] = None

# ---------------------------------------------------------------------------
# Capabilities Matrix
# ---------------------------------------------------------------------------
class LanguageCapabilityItem(BaseModel):
    code: str
    name: str
    native_name: str
    script: str
    nmt_supported: bool
    asr_supported: bool
    tts_supported: bool
    primary_provider: str
    fallback_provider: str
    status: str
    notes: str
    bhashini_available: bool = False

class LanguageCapabilitiesResponse(BaseModel):
    supported_languages: List[LanguageCapabilityItem]
    total_count: int
    bhashini_configured: bool
    engine_status: str = "operational"
