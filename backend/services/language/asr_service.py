"""
Multilingual Automatic Speech Recognition (ASR) Service
Implements Phase 5.4: Speech-to-Text with:
1. Strict Payload Validation: validates base64 encoding, mime/format, minimum bytes, and maximum file size (10 MB).
2. Live Bhashini ASR Integration: routes to MeitY ULCA ASR when credentials are configured.
3. Honest Confidence Reporting: returns confidence score ONLY when reported by provider; never invents synthetic numbers.
4. Transparent Fallback Identification: explicitly distinguishes Bhashini ULCA from Browser Web Speech fallback.
5. Dialect Ethics: clearly reports unsupported status for Dogri/Haryanvi when native models are absent.
"""

import base64
import logging
from typing import Dict, Any, Optional

from .bhashini_client import bhashini_client
from .language_capabilities import LANGUAGE_CAPABILITY_MATRIX
from .exceptions import AudioValidationException

logger = logging.getLogger("sahyogsetu.language.asr")

MAX_AUDIO_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
MIN_AUDIO_BYTES = 100                     # Minimum meaningful audio header length
SUPPORTED_FORMATS = {"wav", "mp3", "webm", "ogg", "flac"}

class ASRService:
    """Manages audio transcription with strict validation and honest provider reporting."""

    def __init__(self):
        self.bhashini = bhashini_client

    def validate_audio_payload(self, audio_bytes: bytes, audio_format: str) -> None:
        """Validates audio stream format, byte size, and non-emptiness."""
        if not audio_bytes or len(audio_bytes) < MIN_AUDIO_BYTES:
            raise AudioValidationException("Audio stream is empty, corrupted, or below minimum size threshold.")

        if len(audio_bytes) > MAX_AUDIO_SIZE_BYTES:
            raise AudioValidationException(f"Audio payload ({len(audio_bytes)} bytes) exceeds maximum limit of 10 MB.")

        fmt = audio_format.lower().strip()
        if fmt not in SUPPORTED_FORMATS:
            raise AudioValidationException(f"Audio format '{audio_format}' not supported. Expected one of: {list(SUPPORTED_FORMATS)}")

    def get_capabilities(self, language: str = "hi") -> Dict[str, Any]:
        """Returns honest capability disclosure for the specified language."""
        lang = language.lower().strip()
        meta = LANGUAGE_CAPABILITY_MATRIX.get(lang, LANGUAGE_CAPABILITY_MATRIX["en"])
        bhashini_ok = self.bhashini.is_configured()

        return {
            "language": lang,
            "language_name": meta["name"],
            "is_native_supported": meta["asr_supported"] and (bhashini_ok if lang == "doi" else True),
            "provider": "Bhashini ULCA ASR" if bhashini_ok and meta.get("bhashini_code") else "Browser Web Speech Engine",
            "disclaimer": meta.get("notes"),
            "bhashini_configured": bhashini_ok,
            "supported_formats": list(SUPPORTED_FORMATS),
            "max_file_size_bytes": MAX_AUDIO_SIZE_BYTES,
            "max_duration_seconds": 60,
        }

    async def transcribe(
        self,
        audio_base64: str,
        language: str = "hi",
        audio_format: str = "wav",
    ) -> Dict[str, Any]:
        """
        Transcribes speech audio bytes into text.
        Returns recognized transcript, genuine confidence, provider, and status.
        """
        # 1. Decode Base64 Payload
        try:
            audio_bytes = base64.b64decode(audio_base64)
        except Exception as e:
            return {
                "status": "error",
                "error_code": "invalid_base64",
                "message": f"Malformed base64 audio payload: {e}",
                "transcript": "",
                "language": language,
                "provider": "Validation Gateway",
                "confidence": None,
                "requires_user_review": True,
            }

        # 2. Validate Payload
        try:
            self.validate_audio_payload(audio_bytes, audio_format)
        except AudioValidationException as ave:
            return {
                "status": "error",
                "error_code": "validation_failed",
                "message": ave.reason,
                "transcript": "",
                "language": language,
                "provider": "Validation Gateway",
                "confidence": None,
                "requires_user_review": True,
            }

        target_lang = language.lower().strip()
        meta = LANGUAGE_CAPABILITY_MATRIX.get(target_lang)

        # 3. Dialect Ethics Gate for Unsupported Regional Languages
        if target_lang == "bgc":
            return {
                "status": "fallback_client_speech",
                "transcript": "",
                "language": "bgc",
                "provider": "Hindi Phonetic Fallback / Browser Web Speech",
                "confidence": None,
                "message": (
                    "Native Haryanvi speech acoustic model is unavailable. "
                    "Using Hindi acoustic model as phonetic fallback. Please review transcription before submitting."
                ),
                "requires_user_review": True,
            }

        # 4. Attempt Remote Bhashini ASR if configured
        if self.bhashini.is_configured():
            try:
                res = await self.bhashini.transcribe(audio_bytes, target_lang, audio_format)
                if res and res.get("transcript"):
                    return {
                        "status": "success",
                        "transcript": res["transcript"],
                        "language": target_lang,
                        "provider": "Bhashini ULCA ASR",
                        "confidence": res.get("confidence"),  # Genuine confidence only
                        "requires_user_review": True,
                    }
            except Exception as e:
                logger.warning("Bhashini ASR call failed: %s; routing to client speech fallback.", e)

        # 5. Honest Client Speech Fallback Notice
        cap = self.get_capabilities(target_lang)
        return {
            "status": "fallback_client_speech",
            "transcript": "",
            "language": target_lang,
            "provider": "Browser Web Speech Engine",
            "confidence": None,
            "message": cap.get("disclaimer") or "Audio payload received. Using client-side speech recognition.",
            "requires_user_review": True,
        }

asr_service = ASRService()
