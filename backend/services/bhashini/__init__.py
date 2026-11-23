"""
Bhashini Unified Client for SahyogSetu
Implements Phase 5:
- Translation (NMT)
- Automatic Speech Recognition (ASR)
- Text-to-Speech (TTS)
With health checks, timeout isolation, credential management, and verified offline fallbacks.
"""

from .bhashini_client import bhashini_client

__all__ = ["bhashini_client"]
