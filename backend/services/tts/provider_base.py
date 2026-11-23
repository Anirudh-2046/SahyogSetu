"""
Abstract Base Class & Result Models for TTS Providers
Modular interface allowing providers (Bhashini, AI4Bharat, Google, Local)
to be swapped or chained without altering the application layer.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel

class TTSResult(BaseModel):
    success: bool
    audio_bytes: Optional[bytes] = None
    audio_format: str = "audio/mpeg"
    actual_language: str
    is_alternative: bool = False
    provider_name: str
    model_name: str
    error_message: Optional[str] = None
    duration_seconds: float = 0.0
    is_synthetic_tone: bool = False

class TTSProvider(ABC):
    """Abstract interface that each speech synthesis provider must implement."""

    name: str = "BaseProvider"
    supported_languages: List[str] = []

    @abstractmethod
    def is_configured(self) -> bool:
        """Returns True if the provider has necessary API keys/credentials/models."""
        pass

    @abstractmethod
    async def generate_audio(
        self,
        text: str,
        language: str,
        voice_gender: str = "female",
    ) -> TTSResult:
        """
        Synthesizes speech for the given text.
        Must respect requested language and never return a different language
        without setting is_alternative=True.
        """
        pass

