"""
Language and Provider Capabilities Specification
Defines verified capability matrix for:
- English (en)
- Hindi (hi)
- Punjabi (pa)
- Dogri (doi)
- Haryanvi (bgc)
Strictly avoids faking dialect support or claiming live model availability without verification.
"""

from typing import Dict, Any, List

LANGUAGE_CAPABILITY_MATRIX: Dict[str, Dict[str, Any]] = {
    "en": {
        "code": "en",
        "name": "English",
        "native_name": "English",
        "script": "Latin",
        "nmt_supported": True,
        "asr_supported": True,
        "tts_supported": True,
        "primary_provider": "Google Speech / Bhashini NMT",
        "fallback_provider": "SahyogSetu Local Synthesizer / Web Speech",
        "status": "SUPPORTED_AND_VALIDATED",
        "notes": "Full support across NMT, ASR, and TTS.",
        "bhashini_code": "en",
        "browser_speech_code": "en-IN",
    },
    "hi": {
        "code": "hi",
        "name": "Hindi",
        "native_name": "हिन्दी",
        "script": "Devanagari",
        "nmt_supported": True,
        "asr_supported": True,
        "tts_supported": True,
        "primary_provider": "Bhashini ULCA / Google Speech",
        "fallback_provider": "SahyogSetu Local Synthesizer / Web Speech",
        "status": "SUPPORTED_WITH_LIMITATIONS",
        "notes": "Native Devanagari Hindi support across NMT, ASR, and TTS with local offline fallback.",
        "bhashini_code": "hi",
        "browser_speech_code": "hi-IN",
    },
    "pa": {
        "code": "pa",
        "name": "Punjabi",
        "native_name": "ਪੰਜਾਬੀ",
        "script": "Gurmukhi",
        "nmt_supported": True,
        "asr_supported": True,
        "tts_supported": True,
        "primary_provider": "Bhashini ULCA (Gurmukhi) / Google Speech",
        "fallback_provider": "SahyogSetu Local Synthesizer / Web Speech",
        "status": "SUPPORTED_WITH_LIMITATIONS",
        "notes": "Native Gurmukhi Punjabi neural voice and language model support with offline synthesizers.",
        "bhashini_code": "pa",
        "browser_speech_code": "pa-Guru-IN",
    },
    "doi": {
        "code": "doi",
        "name": "Dogri",
        "native_name": "डोगरी",
        "script": "Devanagari",
        "nmt_supported": True,
        "asr_supported": True,
        "tts_supported": True,
        "primary_provider": "Bhashini ULCA (MeitY)",
        "fallback_provider": "Explicit Hindi Alternative",
        "status": "FALLBACK_AVAILABLE",
        "notes": (
            "Supported natively via Bhashini ULCA pipeline tasks. "
            "When credentials are not configured, transparently offers explicitly labelled Hindi audio alternative."
        ),
        "bhashini_code": "doi",
        "browser_speech_code": None,  # Not supported in standard Web Speech browsers
    },
    "bgc": {
        "code": "bgc",
        "name": "Haryanvi",
        "native_name": "बागड़ी / हरियाणवी",
        "script": "Devanagari",
        "nmt_supported": False,
        "asr_supported": False,
        "tts_supported": False,
        "primary_provider": "Explicit Hindi Alternative",
        "fallback_provider": "English Alternative",
        "status": "FALLBACK_AVAILABLE",
        "notes": (
            "No validated Haryanvi neural voice or acoustic model exists in standard Indian providers. "
            "Preserves Haryanvi text while requiring explicit user consent to listen to a Hindi audio alternative."
        ),
        "bhashini_code": None,
        "browser_speech_code": None,
    },
}

class LanguageCapabilitiesService:
    """Provides configuration-driven language capability inspection."""

    @classmethod
    def get_matrix(cls) -> List[Dict[str, Any]]:
        return list(LANGUAGE_CAPABILITY_MATRIX.values())

    @classmethod
    def get_for_language(cls, lang_code: str) -> Dict[str, Any]:
        return LANGUAGE_CAPABILITY_MATRIX.get(lang_code.lower(), LANGUAGE_CAPABILITY_MATRIX["en"])

    @classmethod
    def is_task_supported(cls, lang_code: str, task: str) -> bool:
        meta = cls.get_for_language(lang_code)
        key = f"{task}_supported"
        return bool(meta.get(key, False))

language_capabilities = LanguageCapabilitiesService()
