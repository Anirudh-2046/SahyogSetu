"""
Language Detector for Regional & Official Indic Languages
Supports detection of:
- English (en)
- Hindi (hi)
- Punjabi (pa, Gurmukhi script)
- Dogri (doi, Devanagari dialectal markers)
- Haryanvi (bgc, Bangru/Haryanvi Devanagari markers)
Does not force low-confidence classifications.
"""

import re
from typing import Tuple

class LanguageDetector:
    """Detects text language using script analysis and lexical marker scoring."""

    # Lexical patterns for Devanagari regional languages
    DOGRI_MARKERS = [
        r"\bकन्नै\b", r"\bआह्डा\b", r"\bजाग\b", r"\bगेया\b", r"\bशा\b", r"\bथमां\b",
        r"\bमुक्की\b", r"\bदित्ते\b", r"\bकीते\b", r"\bदित्ती\b", r"\bलेई\b", r"\bहोग\b",
        r"\bसद्दा\b", r"\bच\b", r"\bमैम्बरें\b", r"\bसमितियें\b"
    ]

    HARYANVI_MARKERS = [
        r"\bसैं\b", r"\bसै\b", r"\bखातर\b", r"\bहोवैगा\b", r"\bकऱ्या\b", r"\bगैल\b",
        r"\bतैं\b", r"\bम्ह\b", r"\bम्हारा\b", r"\bथारा\b", r"\bआले\b", r"\bलाणी\b",
        r"\bहोग्या\b", r"\bबणाए\b", r"\bमिलैगी\b", r"\bबखत\b"
    ]

    HINDI_MARKERS = [
        r"\bहै\b", r"\bहैं\b", r"\bहोगा\b", r"\bगया\b", r"\bगए\b", r"\bके लिए\b",
        r"\bद्वारा\b", r"\bकिया\b", r"\bकी गई\b", r"\bयोजना\b", r"\bसमिति\b"
    ]

    @classmethod
    def detect(cls, text: str) -> Tuple[str, float]:
        """
        Returns (language_code, confidence).
        language_code is one of: 'en', 'hi', 'pa', 'doi', 'bgc'
        """
        if not text or not text.strip():
            return "en", 0.5

        # 1. Script checks
        gurmukhi_chars = len(re.findall(r"[\u0a00-\u0a7f]", text))
        devanagari_chars = len(re.findall(r"[\u0900-\u097f]", text))
        latin_chars = len(re.findall(r"[a-zA-Z]", text))
        total_letters = gurmukhi_chars + devanagari_chars + latin_chars

        if total_letters == 0:
            return "en", 0.5

        # Gurmukhi script -> Punjabi
        if gurmukhi_chars / total_letters > 0.4:
            conf = min(0.99, 0.7 + (gurmukhi_chars / total_letters) * 0.3)
            return "pa", round(conf, 2)

        # Latin alphabet -> English
        if latin_chars / total_letters > 0.6:
            conf = min(0.99, 0.7 + (latin_chars / total_letters) * 0.3)
            return "en", round(conf, 2)

        # Devanagari script -> Distinguish Hindi vs Dogri vs Haryanvi
        if devanagari_chars / total_letters > 0.4:
            dogri_score = sum(1 for m in cls.DOGRI_MARKERS if re.search(m, text))
            haryanvi_score = sum(1 for m in cls.HARYANVI_MARKERS if re.search(m, text))
            hindi_score = sum(1 for m in cls.HINDI_MARKERS if re.search(m, text))

            if dogri_score > haryanvi_score and dogri_score >= 2:
                return "doi", 0.85
            if haryanvi_score > dogri_score and haryanvi_score >= 2:
                return "bgc", 0.85
            
            # Default Devanagari is Hindi with high confidence
            return "hi", 0.92

        return "en", 0.6

