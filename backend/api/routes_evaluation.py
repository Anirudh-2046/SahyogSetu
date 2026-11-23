"""
Quantitative RAG Evaluation API Router
Computes precision, recall, and reciprocal rank metrics against held-out benchmark questions.
"""

from fastapi import APIRouter
import logging

from ..services.sources.source_resolver import source_resolver
from ..services.ml.evaluation import ml_evaluator, HELD_OUT_EVALUATION_DATASET
from ..rag.evaluation import rag_evaluator

logger = logging.getLogger("sahyogsetu.api.evaluation")

router = APIRouter(prefix="/api/evaluation", tags=["Evaluation"])

@router.get("/rag")
async def evaluate_rag_retrieval():
    """
    Evaluates retrieval performance across held-out cooperative queries.
    Returns comparative evaluation across semantic, keyword, hybrid, and reranked models.
    """
    detailed_eval = rag_evaluator.evaluate_all()
    return detailed_eval
