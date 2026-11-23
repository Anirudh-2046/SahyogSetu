"""
Google Cloud / gTTS Speech Provider
Provides verified neural voice output for:
- English (en / en-IN)
- Hindi (hi / hi-IN)
- Punjabi (pa / pa-Guru-IN)
Note: Does NOT support Dogri (doi) or Haryanvi (bgc).
"""

import io
import asyncio
import logging
from typing import List
from gtts import gTTS

from .provider_base import TTSProvider, TTSResult

logger = logging.getLogger("sahyogsetu.tts.google")

class GoogleTTSProvider(TTSProvider):
    name = "Google Speech Engine"
    supported_languages: List[str] = ["en", "hi", "pa"]

    def is_configured(self) -> bool:
        # Standard gTTS relies on public endpoints; always ready
        return True

    async def generate_audio(
        self,
        text: str,
        language: str,
        voice_gender: str = "female",
    ) -> TTSResult:
        if language not in self.supported_languages:
            return TTSResult(
                success=False,
                actual_language=language,
                provider_name=self.name,
                model_name="gtts-neural",
                error_message=f"Google Speech does not support '{language}'. Commercial voices exist only for en, hi, pa.",
            )

        def _synthesize():
            speech_text = text.strip()
            # If text is lengthy, truncate at sentence boundary within 600 chars for responsive synthesis
            if len(speech_text) > 600:
                cutoff = speech_text[:600]
                last_punct = max(
                    cutoff.rfind(". "),
                    cutoff.rfind("। "),
                    cutoff.rfind("? "),
                    cutoff.rfind("! "),
                    cutoff.rfind("\n"),
                )
                if last_punct > 150:
                    speech_text = speech_text[:last_punct + 1]
                else:
                    speech_text = cutoff.rsplit(" ", 1)[0] + "."

            tts = gTTS(text=speech_text, lang=language, tld="com", slow=False)
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            return buf.read()

        try:
            # 10.0 second timeout to accommodate complete natural speech synthesis over WAN
            audio_bytes = await asyncio.wait_for(asyncio.to_thread(_synthesize), timeout=10.0)
            return TTSResult(
                success=True,
                audio_bytes=audio_bytes,
                audio_format="audio/mpeg",
                actual_language=language,
                is_alternative=False,
                provider_name=self.name,
                model_name=f"google-{language}-in",
                is_synthetic_tone=False,
            )
        except Exception as e:
            logger.warning("Google TTS unavailable or timed out (%s): %s", type(e).__name__, e)
            return TTSResult(
                success=False,
                actual_language=language,
                provider_name=self.name,
                model_name="gtts-neural",
                error_message=str(e),
                is_synthetic_tone=False,
            )

