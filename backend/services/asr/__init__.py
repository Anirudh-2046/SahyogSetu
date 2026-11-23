"""
Automatic Speech Recognition (ASR) Service for SahyogSetu
Implements Phase 5B:
- Audio capture and transcription
- Multi-provider routing (Bhashini ASR, Web Speech fallback)
- Language disclosure & transcription review
"""

from .asr_service import asr_service

__all__ = ["asr_service"]
