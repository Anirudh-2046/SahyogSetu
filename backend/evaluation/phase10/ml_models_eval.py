"""
SahyogSetu Phase 10: AI/ML Models Independent Evaluation
Implements Phase 10.8:
- Evaluates:
  1. Intent Classifier (intent_model.joblib)
  2. Language Identifier (language_model.joblib)
  3. News Sector Classifier (news_model.joblib)
  4. Legal Reranker comparative performance
- Computes:
  - Accuracy, Macro Precision, Macro Recall, Macro F1
  - Per-class precision, recall, and F1
  - Full confusion matrices
- Saves results to backend/evaluation/phase10/ml_models_eval_results.json
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
import joblib
import numpy as np

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Need custom transformers in sys.modules so joblib can unpickle
from backend.ml import transformers

MODELS_DIR = PROJECT_ROOT / "backend" / "ml" / "models"
DATASETS_DIR = PROJECT_ROOT / "backend" / "ml" / "datasets"
GOLD_PATH = Path(__file__).resolve().parent / "gold_benchmark_dataset.json"
OUTPUT_ML_RESULTS_PATH = Path(__file__).resolve().parent / "ml_models_eval_results.json"


def evaluate_classifier(model, X_test: List[str], y_test: List[str], label_names: List[str]) -> Dict[str, Any]:
    """Computes comprehensive classification metrics and confusion matrix."""
    y_pred = model.predict(X_test)
    
    total = len(y_test)
    correct = sum(1 for yt, yp in zip(y_test, y_pred) if yt == yp)
    accuracy = correct / max(1, total)

    # Confusion matrix
    label_to_idx = {lbl: i for i, lbl in enumerate(label_names)}
    n_labels = len(label_names)
    cm = [[0 for _ in range(n_labels)] for _ in range(n_labels)]

    for yt, yp in zip(y_test, y_pred):
        if yt in label_to_idx and yp in label_to_idx:
            cm[label_to_idx[yt]][label_to_idx[yp]] += 1

    # Per-class precision, recall, f1
    per_class = {}
    precisions = []
    recalls = []
    f1s = []

    for i, lbl in enumerate(label_names):
        tp = cm[i][i]
        fp = sum(cm[r][i] for r in range(n_labels) if r != i)
        fn = sum(cm[i][c] for c in range(n_labels) if c != i)

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

        per_class[lbl] = {
            "support": sum(cm[i]),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
        }
        precisions.append(prec)
        recalls.append(rec)
        f1s.append(f1)

    macro_f1 = sum(f1s) / max(1, len(f1s))
    macro_prec = sum(precisions) / max(1, len(precisions))
    macro_rec = sum(recalls) / max(1, len(recalls))

    return {
        "sample_size": total,
        "accuracy": round(accuracy, 4),
        "macro_precision": round(macro_prec, 4),
        "macro_recall": round(macro_rec, 4),
        "macro_f1": round(macro_f1, 4),
        "per_class": per_class,
        "labels": label_names,
        "confusion_matrix": cm,
    }


def run_ml_evaluations():
    print("=" * 80)
    print("SAHYOGSETU PHASE 10: AI/ML MODEL EVALUATION")
    print("=" * 80)

    results = {}

    # -------------------------------------------------------------------------
    # 1. Intent Classifier Evaluation
    # -------------------------------------------------------------------------
    print("\n[1] Evaluating Intent Classifier (intent_model.joblib)...")
    intent_model_path = MODELS_DIR / "intent_model.joblib"
    intent_model = joblib.load(intent_model_path)
    
    # Load 243 dataset and hold-out 37 test queries
    with open(DATASETS_DIR / "intent_dataset.json", "r", encoding="utf-8") as f:
        intent_data = json.load(f)
    
    # Test split (last 37 samples)
    X_intent = [item["query"] for item in intent_data[206:]]
    y_intent = [item["intent"] for item in intent_data[206:]]
    intent_labels = list(sorted(set(item["intent"] for item in intent_data)))

    intent_metrics = evaluate_classifier(intent_model, X_intent, y_intent, intent_labels)
    results["intent_classifier"] = intent_metrics
    print(f"  Accuracy: {intent_metrics['accuracy'] * 100:.2f}% | Macro F1: {intent_metrics['macro_f1']:.4f} (N={intent_metrics['sample_size']})")

    # -------------------------------------------------------------------------
    # 2. Language Identifier Evaluation
    # -------------------------------------------------------------------------
    print("\n[2] Evaluating Language Identifier (language_model.joblib)...")
    lang_model_path = MODELS_DIR / "language_model.joblib"
    lang_model = joblib.load(lang_model_path)

    with open(DATASETS_DIR / "language_dataset.json", "r", encoding="utf-8") as f:
        lang_data = json.load(f)

    # Test split (last 19 samples)
    X_lang = [item["text"] for item in lang_data[106:]]
    y_lang = [item["language"] for item in lang_data[106:]]
    lang_labels = ["en", "hi", "pa", "doi", "bgc"]

    lang_metrics = evaluate_classifier(lang_model, X_lang, y_lang, lang_labels)
    results["language_identifier"] = lang_metrics
    print(f"  Accuracy: {lang_metrics['accuracy'] * 100:.2f}% | Macro F1: {lang_metrics['macro_f1']:.4f} (N={lang_metrics['sample_size']})")

    # -------------------------------------------------------------------------
    # 3. News Sector Classifier Evaluation
    # -------------------------------------------------------------------------
    print("\n[3] Evaluating News Sector Classifier (news_model.joblib)...")
    news_model_path = MODELS_DIR / "news_model.joblib"
    news_model = joblib.load(news_model_path)

    with open(DATASETS_DIR / "news_dataset.json", "r", encoding="utf-8") as f:
        news_data = json.load(f)

    # Test split (last 12 samples)
    X_news = [item["text"] for item in news_data[68:]]
    y_news = [item["category"] for item in news_data[68:]]
    news_labels = list(sorted(set(item["category"] for item in news_data)))

    news_metrics = evaluate_classifier(news_model, X_news, y_news, news_labels)
    results["news_classifier"] = news_metrics
    print(f"  Accuracy: {news_metrics['accuracy'] * 100:.2f}% | Macro F1: {news_metrics['macro_f1']:.4f} (N={news_metrics['sample_size']})")

    # -------------------------------------------------------------------------
    # 4. Reranker Comparative Summary (from retrieval_eval_results.json)
    # -------------------------------------------------------------------------
    retrieval_res_file = Path(__file__).resolve().parent / "retrieval_eval_results.json"
    if retrieval_res_file.exists():
        with open(retrieval_res_file, "r", encoding="utf-8") as f:
            retrieval_res = json.load(f)
        results["reranker_comparison"] = retrieval_res.get("paradigms", {})

    with open(OUTPUT_ML_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\nResults successfully saved to:", OUTPUT_ML_RESULTS_PATH)
    return results


if __name__ == "__main__":
    run_ml_evaluations()
