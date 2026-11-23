"""
SahyogSetu Phase 10: Master Independent Evaluation Orchestrator
Executes and synthesizes all evaluation benchmarks:
1. Legal RAG Retrieval Evaluation (retrieval_eval.py)
2. Legal Answer Quality & Claim-Level Groundedness (answer_quality_eval.py)
3. Jurisdiction Isolation & Cross-State Leakage (jurisdiction_eval.py)
4. Multilingual & Speech Capabilities (multilingual_eval.py)
5. AI/ML Models Independent Evaluation (ml_models_eval.py)
6. News Ingestion & Document Provenance Pipeline (news_pipeline_eval.py)
7. Security & Abuse Regression (security_regression_eval.py)
8. Performance, Latency & Resource Benchmarks (performance_eval.py)

Consolidates all metrics into:
backend/evaluation/phase10/final_evaluation_summary.json
"""

import json
import sys
import os
import time
from pathlib import Path
from typing import Dict, Any

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

EVAL_DIR = Path(__file__).resolve().parent
SUMMARY_FILE = EVAL_DIR / "final_evaluation_summary.json"

from backend.evaluation.phase10.retrieval_eval import evaluate_retrieval
from backend.evaluation.phase10.answer_quality_eval import run_answer_evaluation
from backend.evaluation.phase10.jurisdiction_eval import run_jurisdiction_benchmark
from backend.evaluation.phase10.multilingual_eval import run_multilingual_benchmark
from backend.evaluation.phase10.ml_models_eval import run_ml_evaluations
from backend.evaluation.phase10.news_pipeline_eval import evaluate_news_pipeline
from backend.evaluation.phase10.security_regression_eval import run_security_regression
from backend.evaluation.phase10.performance_eval import run_performance_benchmarks


def run_all():
    print("=" * 80)
    print("SAHYOGSETU PHASE 10: MASTER EVALUATION & QUALITY ASSURANCE SUITE")
    print("=" * 80)
    start_time = time.time()

    summary: Dict[str, Any] = {
        "evaluation_phase": "Phase 10 — Independent Evaluation & Quality Assurance",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "gold_benchmark_size": 220,
    }

    print("\n>>> Stage 1/8: Legal RAG Retrieval Benchmark...")
    summary["retrieval"] = evaluate_retrieval()

    print("\n>>> Stage 2/8: Legal Answer Quality & Claim-Level Groundedness...")
    summary["answer_quality"] = run_answer_evaluation()

    print("\n>>> Stage 3/8: Jurisdiction Boundary & Cross-State Leakage...")
    summary["jurisdiction_isolation"] = run_jurisdiction_benchmark()

    print("\n>>> Stage 4/8: Multilingual Language & Speech Capabilities...")
    summary["multilingual"] = run_multilingual_benchmark()

    print("\n>>> Stage 5/8: AI/ML Models Independent Evaluation...")
    summary["ml_models"] = run_ml_evaluations()

    print("\n>>> Stage 6/8: News Ingestion & Document Provenance Pipeline...")
    summary["news_pipeline"] = evaluate_news_pipeline()

    print("\n>>> Stage 7/8: Security & Abuse Regression Suite...")
    summary["security_regression"] = run_security_regression()

    print("\n>>> Stage 8/8: Performance Latency & System Resource Benchmarks...")
    summary["performance"] = run_performance_benchmarks()

    elapsed = round(time.time() - start_time, 2)
    summary["total_evaluation_runtime_seconds"] = elapsed

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 80)
    print(f"MASTER EVALUATION COMPLETE in {elapsed}s")
    print(f"Consolidated metrics saved to: {SUMMARY_FILE}")
    print("=" * 80)
    return summary


if __name__ == "__main__":
    run_all()
