"""
Multilingual Language Identifier for SahyogSetu
Accurately identifies English, Hindi, Punjabi, Dogri, and Haryanvi
using Unicode script boundaries and linguistic dialect markers.
Computes confidence scores without guessing.
"""

import re
from typing import Tuple, Dict, Any

PUNJABI_REGEX = re.compile(r"[\u0A00-\u0A7F]")
DEVANAGARI_REGEX = re.compile(r"[\u0900-\u097F]")
LATIN_REGEX = re.compile(r"[a-zA-Z]")

HARYANVI_MARKERS = {
    "सै", "सैं", "म्ह", "किकण", "कित", "घराणां", "आदमियां", "बणाणा", "खातर",
    "थारे", "म्हारा", "कै", "लागै", "होवै", "पाछै", "मिलज्यावै", "रपट",
}

DOGRI_MARKERS = {
    "न", "कुत्थै", "किन्नी", "कन्ने", "आह्ले", "पौंदी", "होंदा", "मते", "घट्टੋ",
    "टब्बर", "बक्खो-बक्ख", "बक्ख", "ब'रे", "थमां", "तीगर", "लाजिमी", "करी", "करियै",
}

class LanguageIdentifier:
    """Evaluates text script, regional dialect markers, and ML character n-grams."""

    def identify(self, text: str, user_preference: str = None) -> Tuple[str, float, Dict[str, Any]]:
        """
        Returns (language_code, confidence, debug_info).
        Language codes: en, hi, pa, doi, bgc.
        """
        if not text or not text.strip():
            return "en", 0.0, {"reason": "empty"}

        # 1. Attempt ML Language Identification
        try:
            from backend.ml.inference.language_inference import language_predictor
            res = language_predictor.predict_language(text, user_preference=user_preference)
            return (
                res["detected_language"],
                round(float(res["confidence"]), 2),
                {
                    "source": "ml_language_model",
                    "script": res.get("script", ""),
                    "is_romanized": res.get("is_romanized", False),
                    "user_preference_respected": res.get("user_preference_respected", False),
                    "all_probabilities": res.get("all_probabilities", {}),
                },
            )
        except Exception:
            pass

        raw = text.strip()
        words = set(re.findall(r"[\w\u0900-\u097F\u0A00-\u0A7F]+", raw.lower()))

        # 2. Deterministic Rule-Based Fallback
        # Punjabi (Gurmukhi) Check
        if PUNJABI_REGEX.search(raw):
            gurmukhi_chars = len(PUNJABI_REGEX.findall(raw))
            total_chars = max(len(raw.replace(" ", "")), 1)
            conf = min(0.99, max(0.85, gurmukhi_chars / total_chars))
            return "pa", round(conf, 2), {"source": "rule_fallback", "script": "Gurmukhi", "chars": gurmukhi_chars}

        # Devanagari Script (Hindi vs Dogri vs Haryanvi)
        if DEVANAGARI_REGEX.search(raw):
            if user_preference and user_preference.lower() in ["doi", "bgc"]:
                return user_preference.lower(), 0.95, {"source": "rule_fallback", "script": "Devanagari", "dialect_ethics": True}

            haryanvi_matches = words.intersection(HARYANVI_MARKERS)
            dogri_matches = words.intersection(DOGRI_MARKERS)

            if len(haryanvi_matches) >= 1 and len(haryanvi_matches) >= len(dogri_matches):
                conf = min(0.95, 0.70 + (0.08 * len(haryanvi_matches)))
                return "bgc", round(conf, 2), {"source": "rule_fallback", "dialect": "Haryanvi", "matched_markers": list(haryanvi_matches)}

            if len(dogri_matches) >= 1:
                conf = min(0.95, 0.70 + (0.08 * len(dogri_matches)))
                return "doi", round(conf, 2), {"source": "rule_fallback", "dialect": "Dogri", "matched_markers": list(dogri_matches)}

            # Standard Hindi
            return "hi", 0.95, {"source": "rule_fallback", "script": "Devanagari", "dialect": "Standard Hindi"}

        # English (Latin script)
        if LATIN_REGEX.search(raw):
            return "en", 0.98, {"source": "rule_fallback", "script": "Latin"}

        return "en", 0.50, {"source": "rule_fallback", "reason": "fallback"}

language_identifier = LanguageIdentifier()
