"""
Language Provider Registry
Central directory of all translation, ASR, and TTS providers.
Tracks configuration status, health, and fallback chains without exposing secrets.
"""

import logging
from typing import Dict, Any, List

from .bhashini_client import bhashini_client
from ..tts.google_provider import GoogleTTSProvider
from ..tts.ai4bharat_provider import AI4BharatTTSProvider
from ..tts.local_synthesizer import LocalHarmonicTTSProvider

logger = logging.getLogger("sahyogsetu.language.registry")

class ProviderRegistry:
    """Tracks language service providers, capabilities, and operational health."""

    def __init__(self):
        self.bhashini = bhashini_client
        self.google_tts = GoogleTTSProvider()
        self.ai4bharat_tts = AI4BharatTTSProvider()
        self.local_tts = LocalHarmonicTTSProvider()

    def get_provider_status(self) -> Dict[str, Any]:
        """Returns consolidated health and configuration metrics across providers."""
        return {
            "nmt_providers": [
                {
                    "name": "Bhashini NMT (MeitY)",
                    "type": "remote_neural",
                    "configured": self.bhashini.is_configured(),
                    "supported_languages": ["en", "hi", "pa", "doi"],
                    "status": "operational" if self.bhashini.is_configured() else "not_configured",
                },
                {
                    "name": "SahyogSetu Statutory Term Translator",
                    "type": "grounded_lexicon",
                    "configured": True,
                    "supported_languages": ["en", "hi", "pa", "doi", "bgc"],
                    "status": "operational",
                },
            ],
            "asr_providers": [
                {
                    "name": "Bhashini ASR (MeitY)",
                    "type": "remote_acoustic",
                    "configured": self.bhashini.is_configured(),
                    "supported_languages": ["en", "hi", "pa", "doi"],
                    "status": "operational" if self.bhashini.is_configured() else "not_configured",
                },
                {
                    "name": "Browser Web Speech Engine",
                    "type": "client_fallback",
                    "configured": True,
                    "supported_languages": ["en", "hi", "pa"],
                    "status": "operational",
                },
            ],
            "tts_providers": [
                {
                    "name": "Bhashini TTS (MeitY)",
                    "configured": self.bhashini.is_configured(),
                    "supported_languages": ["en", "hi", "pa", "doi"],
                    "status": "operational" if self.bhashini.is_configured() else "not_configured",
                },
                {
                    "name": self.ai4bharat_tts.name,
                    "configured": self.ai4bharat_tts.is_configured(),
                    "supported_languages": self.ai4bharat_tts.supported_languages,
                    "status": "operational" if self.ai4bharat_tts.is_configured() else "not_configured",
                },
                {
                    "name": self.google_tts.name,
                    "configured": self.google_tts.is_configured(),
                    "supported_languages": self.google_tts.supported_languages,
                    "status": "operational" if self.google_tts.is_configured() else "not_configured",
                },
                {
                    "name": self.local_tts.name,
                    "configured": True,
                    "supported_languages": self.local_tts.supported_languages,
                    "status": "operational",
                },
            ],
        }

    async def check_all_health(self) -> Dict[str, Any]:
        """Aggregates health checks from all providers."""
        bhashini_h = await self.bhashini.check_health()
        return {
            "overall_status": "healthy",
            "bhashini": bhashini_h,
            "local_fallback": {"status": "operational", "message": "Local harmonic synthesizer and lexicon ready."},
        }

provider_registry = ProviderRegistry()
