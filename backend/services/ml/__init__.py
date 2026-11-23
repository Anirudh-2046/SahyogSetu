"""
AI/ML Classification and Evaluation Services for SahyogSetu
Implements Phase 6:
- Language identification (en, hi, pa, doi, bgc)
- News category classification (10 cooperative classes)
- Query intent detection (9 user intents)
- Quantitative held-out evaluation metrics (Precision, Recall, F1, MRR)
"""

from .language_identifier import language_identifier
from .news_classifier import ml_news_classifier
from .intent_detector import intent_detector
from .evaluation import ml_evaluator

__all__ = [
    "language_identifier",
    "ml_news_classifier",
    "intent_detector",
    "ml_evaluator",
]
