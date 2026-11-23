"""
Unified Multilingual Language Service for SahyogSetu
Orchestrates:
1. Neural Machine Translation (NMT) via translation_service
2. Automatic Speech Recognition (ASR) via asr_service
3. Text-to-Speech (TTS) via tts_service
4. Provider discovery and status via provider_registry
5. Language capability matrix via language_capabilities
"""

import logging
from typing import Dict, Any, Optional

from .translation_service import translation_service
from .asr_service import asr_service
from .tts_service import tts_service
from .provider_registry import provider_registry
from .language_capabilities import language_capabilities
from .bhashini_client import bhashini_client

logger = logging.getLogger("sahyogsetu.language.service")

class LanguageService:
    """Unified entrypoint for all natural language processing and speech services."""

    def __init__(self):
        self.translation = translation_service
        self.asr = asr_service
        self.tts = tts_service
        self.registry = provider_registry
        self.capabilities = language_capabilities
        self.bhashini = bhashini_client

    async def translate_text(
        self,
        text: str,
        source_language: str = "en",
        target_language: str = "hi",
        preserve_legal_entities: bool = True,
    ) -> Dict[str, Any]:
        """Translates text with legal entity preservation and caching."""
        return await self.translation.translate(
            text=text,
            source_language=source_language,
            target_language=target_language,
            preserve_legal_entities=preserve_legal_entities,
        )

    def translate_text_sync(
        self,
        text: str,
        source_language: str = "en",
        target_language: str = "hi",
        preserve_legal_entities: bool = True,
    ) -> Dict[str, Any]:
        """Synchronous translation path using grounded statutory terms."""
        return self.translation.translate_sync(
            text=text,
            source_language=source_language,
            target_language=target_language,
            preserve_legal_entities=preserve_legal_entities,
        )

    async def transcribe_speech(
        self,
        audio_base64: str,
        language: str = "hi",
        audio_format: str = "wav",
    ) -> Dict[str, Any]:
        """Transcribes incoming speech audio bytes."""
        return await self.asr.transcribe(
            audio_base64=audio_base64,
            language=language,
            audio_format=audio_format,
        )

    async def generate_speech(
        self,
        text: str,
        language: str = "en",
        voice_gender: str = "female",
        response_id: Optional[str] = None,
        alternative_accepted: Optional[str] = None,
        bypass_cache: bool = False,
    ) -> Dict[str, Any]:
        """Synthesizes text into audio with dialect ethics and caching."""
        return await self.tts.generate_speech(
            text=text,
            language=language,
            voice_gender=voice_gender,
            response_id=response_id,
            alternative_accepted=alternative_accepted,
            bypass_cache=bypass_cache,
        )

    def get_language_matrix(self) -> Dict[str, Any]:
        """Returns consolidated language capability matrix."""
        return {
            "supported_languages": self.capabilities.get_matrix(),
            "total_count": len(self.capabilities.get_matrix()),
            "bhashini_configured": self.bhashini.is_configured(),
            "engine_status": "operational",
        }

    def get_system_status(self) -> Dict[str, Any]:
        """Returns live status of all language providers and cache metrics."""
        providers = self.registry.get_provider_status()
        tts_status = self.tts.get_system_status()
        return {
            "bhashini_client": self.bhashini.get_status(),
            "providers": providers,
            "cache_stats": tts_status.get("cache_stats", {}),
            "status": "operational",
        }

language_service = LanguageService()
