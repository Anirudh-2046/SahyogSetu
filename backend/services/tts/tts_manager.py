"""
SahyogSetu Multilingual TTS Manager
Coordinates speech synthesis with:
1. Script and language verification
2. Strict non-deceptive dialect handling for Dogri (doi) and Haryanvi (bgc)
3. Fallback hierarchy
4. SHA-256 caching and temporary storage
5. Provider fault isolation
"""

import re
import logging
from typing import Dict, Any, Optional, List

from .provider_base import TTSResult
from .bhashini_provider import BhashiniTTSProvider
from .ai4bharat_provider import AI4BharatTTSProvider
from .google_provider import GoogleTTSProvider
from .local_synthesizer import LocalHarmonicTTSProvider
from .audio_cache import audio_cache

logger = logging.getLogger("sahyogsetu.tts.manager")

SUPPORTED_LANGUAGE_METADATA = {
    "en": {
        "name": "English",
        "native_name": "English",
        "script": "Latin",
        "has_native_voice": True,
        "primary_provider": "Google Speech Engine",
        "fallback_provider": "SahyogSetu Local Synthesizer",
        "status": "fully_supported",
        "notes": "Natural Indian English neural voice.",
    },
    "hi": {
        "name": "Hindi",
        "native_name": "हिन्दी",
        "script": "Devanagari",
        "has_native_voice": True,
        "primary_provider": "Google Speech Engine / Bhashini",
        "fallback_provider": "SahyogSetu Local Synthesizer",
        "status": "fully_supported",
        "notes": "Standard Hindi neural voice with high intelligibility.",
    },
    "pa": {
        "name": "Punjabi",
        "native_name": "ਪੰਜਾਬੀ",
        "script": "Gurmukhi",
        "has_native_voice": True,
        "primary_provider": "Google Speech Engine (Gurmukhi) / Bhashini",
        "fallback_provider": "SahyogSetu Local Synthesizer",
        "status": "fully_supported",
        "notes": "Native Gurmukhi Punjabi neural voice.",
    },
    "doi": {
        "name": "Dogri",
        "native_name": "डोगरी",
        "script": "Devanagari",
        "has_native_voice": True,
        "primary_provider": "Bhashini / AI4Bharat Indic-TTS",
        "fallback_provider": "Explicit Hindi Audio Alternative",
        "status": "credential_dependent",
        "notes": "Supported natively via Bhashini & AI4Bharat. When unconfigured, offers explicitly labelled Hindi audio.",
    },
    "bgc": {
        "name": "Haryanvi",
        "native_name": "बागड़ी / हरियाणवी",
        "script": "Devanagari",
        "has_native_voice": False,
        "primary_provider": "Explicit Hindi Alternative",
        "fallback_provider": "English Alternative",
        "status": "alternative_required",
        "notes": "No validated Haryanvi neural voice model exists in standard providers. Offers explicitly labelled Hindi audio alternative while retaining Haryanvi text.",
    },
}

class TTSManager:
    """Central orchestrator for multilingual speech generation in SahyogSetu."""

    def __init__(self):
        self.bhashini = BhashiniTTSProvider()
        self.ai4bharat = AI4BharatTTSProvider()
        self.google = GoogleTTSProvider()
        self.local = LocalHarmonicTTSProvider()

    def get_supported_languages(self) -> Dict[str, Any]:
        """Returns verified language matrix with provider capabilities."""
        languages = []
        for code, meta in SUPPORTED_LANGUAGE_METADATA.items():
            languages.append({
                "code": code,
                **meta,
                "bhashini_available": self.bhashini.is_configured(),
                "ai4bharat_available": self.ai4bharat.is_configured(),
                "google_available": self.google.is_configured(),
            })
        return {
            "supported_languages": languages,
            "total_count": len(languages),
            "engine_status": "operational",
        }

    def get_system_status(self) -> Dict[str, Any]:
        """Returns health status of all speech providers and cache metrics."""
        return {
            "providers": [
                {
                    "name": self.bhashini.name,
                    "configured": self.bhashini.is_configured(),
                    "supported_languages": self.bhashini.supported_languages,
                },
                {
                    "name": self.ai4bharat.name,
                    "configured": self.ai4bharat.is_configured(),
                    "supported_languages": self.ai4bharat.supported_languages,
                },
                {
                    "name": self.google.name,
                    "configured": self.google.is_configured(),
                    "supported_languages": self.google.supported_languages,
                },
                {
                    "name": self.local.name,
                    "configured": self.local.is_configured(),
                    "supported_languages": self.local.supported_languages,
                },
            ],
            "cache_stats": audio_cache.get_stats(),
        }

    @staticmethod
    def clean_text_for_speech(raw_text: str) -> str:
        """Strips markdown asterisks, hashes, and links to ensure natural speech cadence."""
        if not raw_text:
            return ""
        text = re.sub(r"\*\*([^*]+)\*\*", r"\1", raw_text)
        text = re.sub(r"\*([^*]+)\*", r"\1", text)
        text = re.sub(r"#+\s*", "", text)
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        text = re.sub(r"[-*•]\s+", "", text)
        text = re.sub(r"\n{2,}", ". ", text)
        text = re.sub(r"\n", " ", text)
        text = re.sub(r"[ \t]+", " ", text)
        return text.strip()

    async def generate_speech(
        self,
        text: str,
        language: str,
        voice_gender: str = "female",
        response_id: Optional[str] = None,
        alternative_accepted: Optional[str] = None,
        bypass_cache: bool = False,
    ) -> Dict[str, Any]:
        """
        Main entrypoint for speech generation with strict adherence to language ethics:
        - Never silently converts Dogri or Haryanvi into unlabelled Hindi.
        - Preserves user choice and transparency.
        - Applies SHA-256 caching (with bypass option for regeneration).
        """
        cleaned_text = self.clean_text_for_speech(text)
        if not cleaned_text:
            return {
                "status": "error",
                "message": "Empty or whitespace-only text provided for speech synthesis.",
            }

        target_lang = language.lower().strip()
        if target_lang not in SUPPORTED_LANGUAGE_METADATA:
            target_lang = "en"

        # ---------------------------------------------------------------------
        # 1. SPECIAL DIALECT HANDLING: HARYANVI (bgc)
        # ---------------------------------------------------------------------
        if target_lang == "bgc":
            if alternative_accepted in ["hi", "en"]:
                actual_voice_lang = alternative_accepted
                is_alternative = True
                notice = (
                    f"Playing an explicitly labelled { 'Hindi' if actual_voice_lang == 'hi' else 'English' } "
                    f"audio alternative because a dedicated Haryanvi voice model is unavailable."
                )
            else:
                return {
                    "status": "alternative_offered",
                    "requested_language": "bgc",
                    "message": (
                        "Dedicated Haryanvi neural voice model is currently unavailable across standard Indian speech providers. "
                        "You can listen to an explicitly labelled Hindi audio alternative while retaining your Haryanvi text."
                    ),
                    "suggested_alternatives": [
                        {"code": "hi", "label": "Listen in Hindi", "native_label": "हिन्दी में सुनें"},
                        {"code": "en", "label": "Listen in English", "native_label": "Listen in English"},
                    ],
                }
        # ---------------------------------------------------------------------
        # 2. SPECIAL DIALECT HANDLING: DOGRI (doi)
        # ---------------------------------------------------------------------
        elif target_lang == "doi":
            # Attempt native Dogri via Bhashini or AI4Bharat first
            native_dogri_available = self.bhashini.is_configured() or self.ai4bharat.is_configured()
            if native_dogri_available:
                actual_voice_lang = "doi"
                is_alternative = False
                notice = "Playing with native Dogri speech synthesis."
            elif alternative_accepted in ["hi", "en"]:
                actual_voice_lang = alternative_accepted
                is_alternative = True
                notice = f"Playing { 'Hindi' if actual_voice_lang == 'hi' else 'English' } audio alternative for Dogri response."
            else:
                return {
                    "status": "unavailable",
                    "requested_language": "doi",
                    "message": (
                        "Native Dogri voice synthesis requires active Bhashini credentials (BHASHINI_API_KEY) "
                        "or offline Indic-TTS engine. Audio is currently unavailable in native Dogri. "
                        "You can listen in Hindi or English instead."
                    ),
                    "suggested_alternatives": [
                        {"code": "hi", "label": "Listen in Hindi", "native_label": "हिन्दी में सुनें"},
                        {"code": "en", "label": "Listen in English", "native_label": "Listen in English"},
                    ],
                }
        # ---------------------------------------------------------------------
        # 3. STANDARD LANGUAGES: EN, HI, PA
        # ---------------------------------------------------------------------
        else:
            actual_voice_lang = target_lang
            is_alternative = False
            notice = f"Playing in native {SUPPORTED_LANGUAGE_METADATA[actual_voice_lang]['name']}."

        # ---------------------------------------------------------------------
        # 4. CACHE LOOKUP
        # ---------------------------------------------------------------------
        audio_id = audio_cache.compute_audio_id(cleaned_text, actual_voice_lang, voice_gender)
        if not bypass_cache:
            cached = audio_cache.get_audio(audio_id)
            if cached:
                audio_bytes, mime = cached
                meta = audio_cache.meta_index.get(audio_id, {})
                return {
                    "status": "success",
                    "audio_url": f"/api/tts/audio/{audio_id}",
                    "audio_format": mime,
                    "requested_language": target_lang,
                    "actual_language": actual_voice_lang,
                    "is_alternative": is_alternative,
                    "provider": meta.get("provider", "Audio Cache"),
                    "model": meta.get("model", "cached-audio"),
                    "is_synthetic_tone": meta.get("is_synthetic_tone", False),
                    "audio_id": audio_id,
                    "cached": True,
                    "message": notice,
                }

        # ---------------------------------------------------------------------
        # 5. PROVIDER SELECTION & SYNTHESIS
        # ---------------------------------------------------------------------
        result: Optional[TTSResult] = None

        # Priority 1: Bhashini for Dogri
        if actual_voice_lang == "doi" and self.bhashini.is_configured():
            result = await self.bhashini.generate_audio(cleaned_text, "doi", voice_gender)

        # Priority 2: AI4Bharat for Dogri if Bhashini failed or unconfigured
        if actual_voice_lang == "doi" and (not result or not result.success) and self.ai4bharat.is_configured():
            result = await self.ai4bharat.generate_audio(cleaned_text, "doi", voice_gender)

        # Priority 3: Google for en, hi, pa
        if actual_voice_lang in ["en", "hi", "pa"]:
            result = await self.google.generate_audio(cleaned_text, actual_voice_lang, voice_gender)

        # Fallback to local synthesizer if online providers failed or offline
        if not result or not result.success:
            logger.info("Cloud provider unavailable for %s; using local diagnostic harmonic fallback.", actual_voice_lang)
            result = await self.local.generate_audio(cleaned_text, actual_voice_lang, voice_gender)

        if result and result.success and result.audio_bytes:
            audio_cache.save_audio(
                audio_id=audio_id,
                audio_bytes=result.audio_bytes,
                audio_format=result.audio_format,
                metadata={
                    "language": actual_voice_lang,
                    "provider": result.provider_name,
                    "model": result.model_name,
                    "is_synthetic_tone": result.is_synthetic_tone,
                    "response_id": response_id,
                },
            )
            return {
                "status": "success",
                "audio_url": f"/api/tts/audio/{audio_id}",
                "audio_format": result.audio_format,
                "requested_language": target_lang,
                "actual_language": actual_voice_lang,
                "is_alternative": is_alternative,
                "provider": result.provider_name,
                "model": result.model_name,
                "is_synthetic_tone": result.is_synthetic_tone,
                "audio_id": audio_id,
                "cached": False,
                "message": notice,
            }

        return {
            "status": "error",
            "message": result.error_message if result else "Audio synthesis failed across all providers.",
        }

tts_manager = TTSManager()
