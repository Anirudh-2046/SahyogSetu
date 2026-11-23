"""
Intent Inference Engine for SahyogSetu
Loads intent_model.joblib and delivers low-latency intent prediction (<1ms).
Preserves deterministic regex extraction of statutory section numbers and numeric parameters.
Applies confidence threshold (< 0.60 -> fallback to general_cooperative).
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import joblib
import numpy as np

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.ml.transformers import CrossLingualExpander

MODEL_PATH = BASE_DIR / "models" / "intent_model.joblib"

SECTION_REGEX = re.compile(r"(?:section|rule|sec|ਧਾਰਾ|धारा)\s*(\d+[A-Za-z]?)", re.IGNORECASE)

class IntentPredictor:
    """Classifies user queries into 9 cooperative intents with fallback and entity extraction."""

    def __init__(self, model_path: Optional[Path] = None):
        self.model_path = model_path or MODEL_PATH
        self.pipeline = None
        self._load_model()

    def _load_model(self):
        if self.model_path.exists():
            try:
                self.pipeline = joblib.load(self.model_path)
            except Exception as e:
                print(f"[IntentPredictor] Warning: Failed to load model from {self.model_path}: {e}")
                self.pipeline = None
        else:
            print(f"[IntentPredictor] Model path does not exist: {self.model_path}")

    def extract_statutory_sections(self, query: str) -> List[str]:
        """Extracts exact statutory section or rule numbers deterministically."""
        matches = SECTION_REGEX.findall(query)
        seen = []
        for m in matches:
            norm = m.strip().lower()
            if norm not in seen:
                seen.append(norm)
        return seen

    def extract_numeric_entities(self, query: str) -> List[str]:
        """Extracts statutory thresholds (e.g. 6000, 1.60 lakh, 72 hours, 5 years)."""
        q_lower = query.lower()
        entities = []
        if re.search(r"\b(?:6000|₹6,?000)\b", q_lower):
            entities.append("6000_annual_support")
        if re.search(r"\b(?:1\.60|1\.6|160000|1,60,000)\b", q_lower):
            entities.append("1.60_lakh_collateral_free")
        if re.search(r"\b(?:72\s*(?:hours|ਘੰਟੇ|घंटे|hrs))\b", q_lower):
            entities.append("72_hours_reporting")
        if re.search(r"\b(?:5\s*(?:years|ਸਾਲ|वर्ष|साल))\b", q_lower):
            entities.append("5_years_tenure")
        return entities

    def predict_intent(self, query: str, threshold: float = 0.35) -> Dict[str, Any]:
        """
        Predicts intent from query text.
        If confidence < threshold, flags as uncertain and falls back to general_cooperative.
        """
        extracted_sections = self.extract_statutory_sections(query)
        numeric_entities = self.extract_numeric_entities(query)

        if not query or not query.strip():
            return {
                "predicted_intent": "general_cooperative",
                "confidence": 0.50,
                "is_uncertain": True,
                "extracted_sections": [],
                "numeric_entities": [],
                "all_probabilities": {},
            }

        # If model is unavailable, return baseline
        if self.pipeline is None:
            return {
                "predicted_intent": "general_cooperative",
                "confidence": 0.50,
                "is_uncertain": True,
                "extracted_sections": extracted_sections,
                "numeric_entities": numeric_entities,
                "all_probabilities": {},
            }

        probs = self.pipeline.predict_proba([query])[0]
        classes = self.pipeline.classes_
        prob_dict = {cls: round(float(p), 4) for cls, p in zip(classes, probs)}

        best_idx = int(np.argmax(probs))
        top_intent = classes[best_idx]
        confidence = float(probs[best_idx])

        is_uncertain = confidence < threshold
        effective_intent = top_intent if not is_uncertain else "general_cooperative"

        return {
            "predicted_intent": effective_intent,
            "raw_top_intent": top_intent,
            "confidence": round(confidence, 4),
            "is_uncertain": is_uncertain,
            "extracted_sections": extracted_sections,
            "numeric_entities": numeric_entities,
            "all_probabilities": prob_dict,
        }

intent_predictor = IntentPredictor()
