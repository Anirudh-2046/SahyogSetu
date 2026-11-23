"""
Local Offline Synthesizer & Harmonic Fallback Generator
Generates valid PCM WAV audio streams using standard library 'wave' and 'struct'.
Ensures audio can always be produced for testing, offline verification, or complete cloud fallback.
"""

import io
import math
import wave
import struct
import logging
from typing import List

from .provider_base import TTSProvider, TTSResult

logger = logging.getLogger("sahyogsetu.tts.local")

class LocalHarmonicTTSProvider(TTSProvider):
    name = "SahyogSetu Local Synthesizer (Offline Fallback)"
    supported_languages: List[str] = ["en", "hi", "pa", "doi", "bgc"]

    def is_configured(self) -> bool:
        return True

    async def generate_audio(
        self,
        text: str,
        language: str,
        voice_gender: str = "female",
    ) -> TTSResult:
        """Generates standard playable 16-bit PCM WAV audio."""
        sample_rate = 16000
        words = text.split()
        num_words = max(len(words), 3)
        # Approximate duration: ~0.35s per word, bounded between 2.0s and 15.0s
        duration_sec = min(max(num_words * 0.35, 2.0), 15.0)
        total_samples = int(sample_rate * duration_sec)

        # Tone pitch: female ~240Hz, male ~150Hz with natural inflection modulation
        base_freq = 240.0 if voice_gender == "female" else 150.0

        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(sample_rate)

            samples = []
            for i in range(total_samples):
                t = i / sample_rate
                # Harmonic overtone synthesis + soft envelope
                envelope = min(t / 0.1, 1.0) * min((duration_sec - t) / 0.1, 1.0)
                freq_mod = base_freq + 20.0 * math.sin(2 * math.pi * 1.5 * t)
                val = 0.5 * math.sin(2 * math.pi * freq_mod * t) + 0.25 * math.sin(2 * math.pi * (freq_mod * 2) * t)
                sample_val = int(val * 16000 * max(0.0, envelope))
                samples.append(struct.pack("<h", max(-32768, min(32767, sample_val))))

            wf.writeframes(b"".join(samples))

        buf.seek(0)
        audio_bytes = buf.read()

        return TTSResult(
            success=True,
            audio_bytes=audio_bytes,
            audio_format="audio/wav",
            actual_language=language,
            is_alternative=False,
            provider_name=self.name,
            model_name="local-harmonic-diagnostic-tone",
            duration_seconds=round(duration_sec, 2),
            is_synthetic_tone=True,
        )

