"""
Voice Recognition (ASR) & Translation API Router
Provides speech-to-text, capability inspection, and entity-preserving language translation.
"""

from fastapi import APIRouter, Query, HTTPException
import logging

from ..services.language import (
    language_service,
    ASRTranscribeRequest,
    ASRTranscribeResponse,
    ASRCapabilitiesResponse,
    TranslationRequest,
    TranslationResponse,
)

logger = logging.getLogger("sahyogsetu.api.voice")

router = APIRouter(tags=["Voice & Translation"])

@router.post("/api/asr/transcribe", response_model=ASRTranscribeResponse)
async def transcribe_speech(req: ASRTranscribeRequest):
    """
    Transcribes audio bytes using Bhashini ASR when configured,
    or returns honest language capability guidance for user review.
    """
    res = await language_service.transcribe_speech(
        audio_base64=req.audio_base64,
        language=req.language,
        audio_format=req.audio_format,
    )
    return res

@router.get("/api/asr/capabilities", response_model=ASRCapabilitiesResponse)
async def get_asr_capabilities(language: str = Query("hi")):
    """Returns honest disclosure of speech recognition capabilities per language."""
    return language_service.asr.get_capabilities(language)

@router.post("/api/translate", response_model=TranslationResponse)
async def translate_text(req: TranslationRequest):
    """
    Translates text between languages using Bhashini NMT with strict legal entity protection.
    Never alters statutory Act names, section numbers, amounts, or URLs.
    """
    return await language_service.translate_text(
        text=req.text,
        source_language=req.source_language,
        target_language=req.target_language,
        preserve_legal_entities=True,
    )
