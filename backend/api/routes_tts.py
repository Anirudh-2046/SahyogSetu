"""
Text-to-Speech (TTS) API Router
Provides multilingual voice synthesis with dialect honesty and local audio caching.
"""

from fastapi import APIRouter, HTTPException, Response
import logging

from ..schemas.voice import TTSGenerateRequest
from ..services.language import language_service
from ..services.tts.audio_cache import audio_cache

logger = logging.getLogger("sahyogsetu.api.tts")

router = APIRouter(prefix="/api/tts", tags=["TTS"])

@router.post("/generate")
@router.post("/synthesize")
async def generate_speech(req: TTSGenerateRequest):
    """Synthesizes speech in requested language with dialect ethics and caching."""
    res = await language_service.generate_speech(
        text=req.text,
        language=req.language,
        voice_gender=req.voice_gender,
        response_id=req.response_id,
        alternative_accepted=req.alternative_accepted,
        bypass_cache=req.bypass_cache,
    )
    return res

@router.get("/audio/{audio_id}")
async def get_audio_stream(audio_id: str):
    """Streams the synthesized audio file from cache."""
    cached = audio_cache.get_audio(audio_id)
    if not cached:
        raise HTTPException(status_code=404, detail="Audio file expired or not found")
    audio_bytes, mime_type = cached
    return Response(
        content=audio_bytes,
        media_type=mime_type,
        headers={
            "Accept-Ranges": "bytes",
            "Content-Length": str(len(audio_bytes)),
            "Cache-Control": "public, max-age=86400",
        },
    )

@router.get("/languages")
async def get_tts_languages():
    """Returns matrix of supported TTS languages and capabilities."""
    return language_service.tts.get_supported_languages()

@router.get("/status")
async def get_tts_status():
    """Returns TTS provider operational status and cache metrics."""
    return language_service.get_system_status()
