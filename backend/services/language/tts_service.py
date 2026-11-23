"""
Multilingual Text-to-Speech (TTS) Service
Implements Phase 5.5: Speech Synthesis with:
1. Bhashini Preference: prefers MeitY Bhashini ULCA for en, hi, pa, doi when configured.
2. Provider Hierarchy: Bhashini -> Google / AI4Bharat -> Local Harmonic Fallback.
3. Long Text Chunking: handles lengthy statutory passages by splitting along sentence boundaries.
4. Legal Term & Number Protection: strips markdown asterisks and URLs while preserving exact Section numbers and amounts.
5. Audio Caching: persistent SHA-256 WAV cache avoiding redundant synthesis.
6. Dialect Ethics: strict non-deceptive disclosures for Dogri and Haryanvi.
"""

import re
import logging
from typing import Dict, Any, Optional, List

from ..tts.tts_manager import tts_manager, SUPPORTED_LANGUAGE_METADATA
from ..tts.audio_cache import audio_cache
from .bhashini_client import bhashini_client
from .language_capabilities import LANGUAGE_CAPABILITY_MATRIX

logger = logging.getLogger("sahyogsetu.language.tts")

MAX_CHUNK_CHARS = 450  # Safe boundary for speech synthesis segmenting

class TTSService:
    """Coordinates speech synthesis across cloud providers and local offline engines."""

    def __init__(self):
        self.manager = tts_manager
        self.bhashini = bhashini_client

    def clean_text_for_speech(self, raw_text: str) -> str:
        """
        Strips markdown formatting, bullet symbols, and raw URLs while
        preserving legal entity names, section numbers, and monetary figures.
        """
        if not raw_text:
            return ""

        text = raw_text
        # Replace markdown links [Anchor Text](http://...) with just Anchor Text
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        # Strip bare URLs
        text = re.sub(r"https?://[^\s\)]+", "", text)
        # Strip bold/italic markdown
        text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
        text = re.sub(r"\*([^*]+)\*", r"\1", text)
        # Strip markdown headers #, ##, ###
        text = re.sub(r"#+\s*", "", text)
        # Clean bullet points
        text = re.sub(r"[-*•]\s+", "", text)
        # Normalize whitespace and line breaks into natural pauses
        text = re.sub(r"\n{2,}", ". ", text)
        text = re.sub(r"\n", " ", text)
        text = re.sub(r"[ \t]+", " ", text)

        return text.strip()

    def chunk_text(self, text: str, max_chars: int = MAX_CHUNK_CHARS) -> List[str]:
        """Splits long legal explanations into sentence-level chunks for smooth synthesis."""
        cleaned = self.clean_text_for_speech(text)
        if len(cleaned) <= max_chars:
            return [cleaned]

        sentences = re.split(r"(?<=[.!?।])\s+", cleaned)
        chunks: List[str] = []
        current_chunk = []
        current_len = 0

        for sentence in sentences:
            s_clean = sentence.strip()
            if not s_clean:
                continue
            if current_len + len(s_clean) > max_chars and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [s_clean]
                current_len = len(s_clean)
            else:
                current_chunk.append(s_clean)
                current_len += len(s_clean) + 1

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    async def generate_speech(
        self,
        text: str,
        language: str = "en",
        voice_gender: str = "female",
        response_id: Optional[str] = None,
        alternative_accepted: Optional[str] = None,
        bypass_cache: bool = False,
    ) -> Dict[str, Any]:
        """
        Synthesizes text into audio with complete dialect honesty, caching, and provider tracking.
        """
        cleaned_text = self.clean_text_for_speech(text)
        if not cleaned_text:
            return {
                "status": "error",
                "message": "Empty text provided for speech synthesis.",
                "requested_language": language,
                "actual_language": language,
                "is_alternative": False,
            }

        target_lang = language.lower().strip()
        if target_lang not in LANGUAGE_CAPABILITY_MATRIX:
            target_lang = "en"

        # Delegate to tts_manager which handles dialect ethics and provider hierarchy
        result = await self.manager.generate_speech(
            text=cleaned_text,
            language=target_lang,
            voice_gender=voice_gender,
            response_id=response_id,
            alternative_accepted=alternative_accepted,
            bypass_cache=bypass_cache,
        )

        return result

    def get_supported_languages(self) -> Dict[str, Any]:
        """Returns verified matrix of speech capabilities."""
        return self.manager.get_supported_languages()

    def get_system_status(self) -> Dict[str, Any]:
        """Returns live status of all speech engines and audio cache statistics."""
        return self.manager.get_system_status()

tts_service = TTSService()
