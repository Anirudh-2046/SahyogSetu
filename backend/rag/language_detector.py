"""
Multilingual Query Language & Script Detector for SahyogSetu
Identifies script, natural language, and Romanized Indian-language queries (Hinglish/Pinglish).
Preserves the original query text and normalizes whitespace and punctuation.
"""

import re
import unicodedata
from typing import Dict, Any, Optional

ROMANIZED_HINDI_PATTERNS = [
    r"\b(kya|hai|hain|kaise|kitna|kitne|chahiye|hoga|karein|kare|sahkari|samiti|yojana|panjikaran)\b",
    r"\b(kisan|krishi|rin|byaj|chhoot|vivad|chunav|kendra|sarkar)\b",
]

ROMANIZED_PUNJABI_PATTERNS = [
    r"\b(kiven|kida|kine|chahide|hovega|kariye|sabha|sahkari|vich|layi|dian|nu)\b",
    r"\b(fasal|bima|arzi|farad|jambandi|chona|jhangra)\b",
]

class LanguageDetector:
    """Detects query language, script, and Romanized transliterations."""

    @classmethod
    def detect(cls, query: str, interface_language: str = "en") -> Dict[str, Any]:
        """
        Analyzes query string to identify script, primary language, and Romanized characteristics.
        """
        if not query or not query.strip():
            return {
                "detected_language": interface_language or "en",
                "script": "Latin",
                "is_romanized": False,
                "confidence": 0.5,
                "normalized_query": "",
            }

        normalized = unicodedata.normalize("NFC", query).strip()
        # Remove extra whitespace
        normalized = re.sub(r"\s+", " ", normalized)

        # 1. Check Native Scripts
        gurmukhi_chars = len(re.findall(r"[\u0A00-\u0A7F]", normalized))
        devanagari_chars = len(re.findall(r"[\u0900-\u097F]", normalized))
        arabic_chars = len(re.findall(r"[\u0600-\u06FF]", normalized))
        latin_chars = len(re.findall(r"[A-Za-z]", normalized))

        total_script_chars = gurmukhi_chars + devanagari_chars + arabic_chars + latin_chars

        if gurmukhi_chars > 2 and (gurmukhi_chars / max(total_script_chars, 1)) > 0.3:
            return {
                "detected_language": "pa",
                "script": "Gurmukhi",
                "is_romanized": False,
                "confidence": 0.95,
                "normalized_query": normalized,
            }

        if devanagari_chars > 2 and (devanagari_chars / max(total_script_chars, 1)) > 0.3:
            # Devanagari script is shared by Hindi, Dogri, and Haryanvi.
            # Respect user's explicitly selected language (doi or bgc) rather than forcing to Hindi.
            devanagari_lang = interface_language.lower() if interface_language.lower() in ["doi", "bgc"] else "hi"
            return {
                "detected_language": devanagari_lang,
                "script": "Devanagari",
                "is_romanized": False,
                "confidence": 0.95,
                "normalized_query": normalized,
            }

        if arabic_chars > 2:
            return {
                "detected_language": "ur",
                "script": "Arabic/Nastaliq",
                "is_romanized": False,
                "confidence": 0.90,
                "normalized_query": normalized,
            }

        # 2. Latin Script Analysis: Check for Romanized Indic words
        q_lower = normalized.lower()
        is_hin_romanized = any(re.search(p, q_lower) for p in ROMANIZED_HINDI_PATTERNS)
        is_pan_romanized = any(re.search(p, q_lower) for p in ROMANIZED_PUNJABI_PATTERNS)

        if is_pan_romanized:
            return {
                "detected_language": "pa",
                "script": "Latin",
                "is_romanized": True,
                "confidence": 0.85,
                "normalized_query": normalized,
            }

        if is_hin_romanized:
            return {
                "detected_language": "hi",
                "script": "Latin",
                "is_romanized": True,
                "confidence": 0.85,
                "normalized_query": normalized,
            }

        # 3. Fallback to English or user selected language
        if latin_chars > 0:
            return {
                "detected_language": "en",
                "script": "Latin",
                "is_romanized": False,
                "confidence": 0.80,
                "normalized_query": normalized,
            }

        return {
            "detected_language": interface_language or "en",
            "script": "Unknown",
            "is_romanized": False,
            "confidence": 0.50,
            "normalized_query": normalized,
        }

    @classmethod
    def resolve_priority_language(cls, user_selected_language: Optional[str], query: str) -> str:
        """
        Enforces strict language-selection priority:
        1. Explicit user-selected response language ('hi', 'pa', 'en', 'doi', 'bgc')
        2. Detected query language if user language is not selected or empty or 'auto'
        3. Configured default language ('en')
        """
        valid_langs = {"en", "hi", "pa", "doi", "bgc"}
        if user_selected_language:
            cleaned = user_selected_language.lower().strip()
            if cleaned in valid_langs:
                return cleaned

        # Priority 2: Detected query language
        det = cls.detect(query, interface_language="en")
        detected = det.get("detected_language", "").lower().strip()
        if detected in valid_langs:
            return detected

        # Priority 3: Configured default
        return "en"

    @classmethod
    def validate_language_consistency(cls, text: str, target_language: str) -> Dict[str, Any]:
        """
        Validates whether user-facing text matches the expected target language script.
        Ignores URLs, Markdown markup, protected statutory identifiers, and numbers.
        """
        tgt = target_language.lower().strip()
        if not text or not text.strip():
            return {"is_consistent": True, "score": 1.0, "reason": "empty_text"}

        # Strip URLs and Markdown links
        clean = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
        clean = re.sub(r"https?://\S+", "", clean)
        # Strip digits, punctuation, and markdown formatting symbols
        clean = re.sub(r"[\d\s\.,;:!\?\"'\(\)\[\]\{\}\*#\-_/\\|`~]", "", clean)

        if not clean:
            return {"is_consistent": True, "score": 1.0, "reason": "non_alphabetic"}

        total_chars = len(clean)
        devanagari_chars = len(re.findall(r"[\u0900-\u097F]", clean))
        gurmukhi_chars = len(re.findall(r"[\u0A00-\u0A7F]", clean))
        latin_chars = len(re.findall(r"[A-Za-z]", clean))

        if tgt in ["hi", "bgc", "doi"]:
            # Devanagari script is expected for Hindi, Haryanvi, Dogri
            # Allow some English statutory act names / acronyms, but require >= 50% Devanagari
            ratio = devanagari_chars / total_chars
            is_consistent = ratio >= 0.45 or (total_chars < 30 and devanagari_chars > 0)
            return {
                "is_consistent": is_consistent,
                "score": round(ratio, 4),
                "script": "Devanagari",
                "dominant_script": "Devanagari" if ratio >= 0.45 else "Latin",
                "details": f"{devanagari_chars}/{total_chars} Devanagari chars ({ratio:.1%})",
            }

        elif tgt == "pa":
            # Gurmukhi script is expected for Punjabi
            ratio = gurmukhi_chars / total_chars
            is_consistent = ratio >= 0.45 or (total_chars < 30 and gurmukhi_chars > 0)
            return {
                "is_consistent": is_consistent,
                "score": round(ratio, 4),
                "script": "Gurmukhi",
                "dominant_script": "Gurmukhi" if ratio >= 0.45 else "Latin",
                "details": f"{gurmukhi_chars}/{total_chars} Gurmukhi chars ({ratio:.1%})",
            }

        elif tgt == "en":
            ratio = latin_chars / total_chars
            is_consistent = ratio >= 0.70
            return {
                "is_consistent": is_consistent,
                "score": round(ratio, 4),
                "script": "Latin",
                "dominant_script": "Latin",
                "details": f"{latin_chars}/{total_chars} Latin chars ({ratio:.1%})",
            }

        return {"is_consistent": True, "score": 1.0, "reason": "unconstrained_lang"}

language_detector = LanguageDetector()
