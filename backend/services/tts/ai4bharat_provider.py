"""
AI4Bharat Indic Parler-TTS / IndicTTS Provider
Open-source Indian language TTS models developed by AI4Bharat (IIT Madras).
Natively supports:
- Dogri (doi)
- Punjabi (pa)
- Hindi (hi)
Configurable via environment variables:
- AI4BHARAT_TTS_URL
- AI4BHARAT_API_KEY (optional)
"""

import os
import base64
import logging
from typing import List
import httpx

from .provider_base import TTSProvider, TTSResult

logger = logging.getLogger("sahyogsetu.tts.ai4bharat")

class AI4BharatTTSProvider(TTSProvider):
    name = "AI4Bharat IndicTTS / Indic Parler-TTS"
    supported_languages: List[str] = ["hi", "pa", "doi"]

    def __init__(self):
        self.endpoint_url = os.getenv("AI4BHARAT_TTS_URL", "").strip()
        self.api_key = os.getenv("AI4BHARAT_API_KEY", "").strip()

    def is_configured(self) -> bool:
        return bool(self.endpoint_url)

    async def generate_audio(
        self,
        text: str,
        language: str,
        voice_gender: str = "female",
    ) -> TTSResult:
        if not self.is_configured():
            return TTSResult(
                success=False,
                actual_language=language,
                provider_name=self.name,
                model_name="ai4bharat-indic-parler",
                error_message="AI4BHARAT_TTS_URL not configured in environment.",
            )

        if language not in self.supported_languages:
            return TTSResult(
                success=False,
                actual_language=language,
                provider_name=self.name,
                model_name="ai4bharat-indic-parler",
                error_message=f"AI4Bharat does not support language code '{language}'.",
            )

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "input": [{"source": text[:800]}],
            "config": {
                "language": {"sourceLanguage": language},
                "gender": voice_gender,
            }
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(self.endpoint_url, json=payload, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    audio_b64 = data.get("audio", [{}])[0].get("audioContent", "")
                    if audio_b64:
                        return TTSResult(
                            success=True,
                            audio_bytes=base64.b64decode(audio_b64),
                            audio_format="audio/wav",
                            actual_language=language,
                            is_alternative=False,
                            provider_name=self.name,
                            model_name="ai4bharat-vits-indic",
                        )
                return TTSResult(
                    success=False,
                    actual_language=language,
                    provider_name=self.name,
                    model_name="ai4bharat-indic-parler",
                    error_message=f"AI4Bharat returned HTTP {res.status_code}",
                )
        except Exception as e:
            logger.error("AI4Bharat TTS invocation failed: %s", e)
            return TTSResult(
                success=False,
                actual_language=language,
                provider_name=self.name,
                model_name="ai4bharat-indic-parler",
                error_message=str(e),
            )

