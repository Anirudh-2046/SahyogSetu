"""
ASR Service Implementation
Handles speech audio transcription requests, language verification,
error classification, and user-review enforcement.
"""

import logging
from typing import Dict, Any, Optional
from ..bhashini.bhashini_client import bhashini_client

logger = logging.getLogger("sahyogsetu.asr.service")

LANGUAGE_ASR_METADATA = {
    "en": {"supported": True, "provider": "Bhashini / Web Speech", "native": True},
    "hi": {"supported": True, "provider": "Bhashini / Web Speech", "native": True},
    "pa": {"supported": True, "provider": "Bhashini / Web Speech", "native": True},
    "doi": {"supported": False, "provider": "Bhashini ULCA (Requires Credentials)", "native": True, "notice": "Dogri ASR requires active Bhashini model credentials. Typing is recommended."},
    "bgc": {"supported": False, "provider": "Hindi Phonetic Fallback", "native": False, "notice": "Native Haryanvi acoustic model is unavailable across standard providers. Hindi acoustic model used as phonetic fallback."},
}

class ASRService:
    """Manages audio transcription pipeline with honest language capability disclosure."""

    def get_capabilities(self, language: str) -> Dict[str, Any]:
        meta = LANGUAGE_ASR_METADATA.get(language, LANGUAGE_ASR_METADATA["en"])
        return {
            "language": language,
            "is_native_supported": meta["supported"],
            "provider": meta["provider"],
            "disclaimer": meta.get("notice"),
            "bhashini_configured": bhashini_client.is_configured(),
        }

    async def transcribe_audio(
        self,
        audio_bytes: bytes,
        language: str = "hi",
        audio_format: str = "wav",
    ) -> Dict[str, Any]:
        """Transcribes incoming audio bytes via Bhashini or indicates client review requirement."""
        if not audio_bytes or len(audio_bytes) < 100:
            return {
                "status": "error",
                "error_code": "no-speech",
                "message": "Empty or corrupted audio stream received.",
                "transcript": "",
            }

        target_lang = language.lower()

        # Attempt Bhashini ASR if configured
        if bhashini_client.is_configured():
            transcript = await bhashini_client.transcribe(audio_bytes, target_lang)
            if transcript:
                return {
                    "status": "success",
                    "transcript": transcript.strip(),
                    "language": target_lang,
                    "provider": "Bhashini ULCA ASR",
                    "requires_user_review": True,
                }

        # If Bhashini unconfigured or failed, return explicit notice for client Web Speech or manual review
        cap = self.get_capabilities(target_lang)
        return {
            "status": "fallback_client_speech",
            "transcript": "",
            "message": cap.get("disclaimer") or "Audio received. Using browser speech recognition or text composer.",
            "language": target_lang,
            "provider": "Browser Web Speech Engine",
            "requires_user_review": True,
        }

asr_service = ASRService()
