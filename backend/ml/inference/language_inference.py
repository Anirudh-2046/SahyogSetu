"""
Language Inference Engine for SahyogSetu
Loads language_model.joblib and identifies languages: en, hi, pa, doi, bgc.
Strictly enforces Dialect Ethics:
- If text is written in Devanagari and user explicitly chose Dogri (doi) or Haryanvi (bgc),
  never override user preference to Hindi (hi).
- Detects Romanized Indic queries (Hinglish/Pinglish).
"""

import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Dict, Any, List, Optional

import joblib
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "language_model.joblib"

GURMUKHI_REGEX = re.compile(r"[\u0A00-\u0A7F]")
DEVANAGARI_REGEX = re.compile(r"[\u0900-\u097F]")
LATIN_REGEX = re.compile(r"[a-zA-Z]")

ROMANIZED_HINDI_PATTERNS = [
    r"\b(kya|hai|hain|kaise|kitna|kitne|chahiye|hoga|karein|kare|sahkari|samiti|yojana|panjikaran)\b",
    r"\b(kisan|krishi|rin|byaj|chhoot|vivad|chunav|kendra|sarkar)\b",
]

ROMANIZED_PUNJABI_PATTERNS = [
    r"\b(kiven|kida|kine|chahide|hovega|kariye|sabha|sahkari|vich|layi|dian|nu)\b",
    r"\b(fasal|bima|arzi|farad|jambandi|chona|jhangra)\b",
]

class LanguagePredictor:
    """Classifies user text into supported languages with script and dialect awareness."""

    def __init__(self, model_path: Optional[Path] = None):
        self.model_path = model_path or MODEL_PATH
        self.pipeline = None
        self._load_model()

    def _load_model(self):
        if self.model_path.exists():
            try:
                self.pipeline = joblib.load(self.model_path)
            except Exception as e:
                print(f"[LanguagePredictor] Warning: Failed to load model from {self.model_path}: {e}")
                self.pipeline = None
        else:
            print(f"[LanguagePredictor] Model path does not exist: {self.model_path}")

    def predict_language(
        self,
        text: str,
        user_preference: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Identifies language code (en, hi, pa, doi, bgc).
        Respects dialect ethics for Dogri and Haryanvi when user preference is explicitly set.
        """
        if not text or not text.strip():
            return {
                "detected_language": user_preference or "en",
                "script": "Latin",
                "is_romanized": False,
                "confidence": 0.50,
                "all_probabilities": {},
            }

        norm_text = unicodedata.normalize("NFC", text).strip()
        user_pref = (user_preference or "en").lower()

        # 1. Script Analysis
        is_gurmukhi = bool(GURMUKHI_REGEX.search(norm_text))
        is_devanagari = bool(DEVANAGARI_REGEX.search(norm_text))
        is_latin = bool(LATIN_REGEX.search(norm_text))

        script = "Latin"
        if is_gurmukhi:
            script = "Gurmukhi"
        elif is_devanagari:
            script = "Devanagari"

        # Check Romanized Indic
        t_lower = norm_text.lower()
        is_hin_romanized = any(re.search(p, t_lower) for p in ROMANIZED_HINDI_PATTERNS)
        is_pan_romanized = any(re.search(p, t_lower) for p in ROMANIZED_PUNJABI_PATTERNS)
        is_romanized = is_hin_romanized or is_pan_romanized

        # 2. Run ML Pipeline if available
        if self.pipeline is not None:
            probs = self.pipeline.predict_proba([norm_text])[0]
            classes = self.pipeline.classes_
            prob_dict = {cls: round(float(p), 4) for cls, p in zip(classes, probs)}
            best_idx = int(np.argmax(probs))
            ml_pred = classes[best_idx]
            ml_conf = float(probs[best_idx])
        else:
            ml_pred = "en"
            ml_conf = 0.50
            prob_dict = {}

        # 3. Dialect Ethics and Script Consistency Enforcement
        effective_lang = ml_pred
        confidence = ml_conf

        if is_gurmukhi:
            effective_lang = "pa"
            confidence = max(ml_conf, 0.98)

        elif is_devanagari:
            # Devanagari script is shared by Hindi, Dogri, and Haryanvi
            if user_pref in ["doi", "bgc"]:
                # NEVER force user preference to Hindi if user explicitly chose Dogri/Haryanvi
                effective_lang = user_pref
                confidence = max(ml_conf, 0.95)
            elif ml_pred in ["doi", "bgc", "hi"]:
                effective_lang = ml_pred
            else:
                effective_lang = "hi"

        elif is_latin and is_romanized:
            # Prefer ML prediction when available and confident
            if ml_pred in ["hi", "pa"] and ml_conf >= 0.35:
                effective_lang = str(ml_pred)
                confidence = max(ml_conf, 0.85)
            elif is_pan_romanized and not is_hin_romanized:
                effective_lang = "pa"
                confidence = 0.88
            elif is_hin_romanized:
                effective_lang = "hi"
                confidence = 0.88

        return {
            "detected_language": effective_lang,
            "script": script,
            "is_romanized": is_romanized,
            "confidence": round(confidence, 4),
            "ml_predicted_language": ml_pred,
            "user_preference_respected": user_pref == effective_lang,
            "all_probabilities": prob_dict,
        }

language_predictor = LanguagePredictor()
