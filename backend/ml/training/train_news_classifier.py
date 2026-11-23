"""
Training Script for SahyogSetu Government News Classifier
Trains TF-IDF + LogisticRegression with NewsExpander on news_dataset.json.
Produces:
- backend/ml/models/news_model.joblib
- backend/ml/models/news_metrics.json
"""

import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion, Pipeline

from backend.ml.transformers import NewsExpander

DATASET_PATH = BASE_DIR / "datasets" / "news_dataset.json"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
MODEL_OUT_PATH = MODELS_DIR / "news_model.joblib"
METRICS_OUT_PATH = MODELS_DIR / "news_metrics.json"

def train():
    print(f"Loading news dataset from: {DATASET_PATH}")
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [item["text"] for item in data]
    labels = [item["category"] for item in data]

    print(f"Total samples: {len(texts)} across {len(set(labels))} sectors")

    # 1. Stratified 70/15/15 Split
    X_train, X_temp, y_train, y_temp = train_test_split(
        texts, labels, test_size=0.30, random_state=42, stratify=labels
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
    )

    print(f"Split sizes - Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")

    # 2. Build Pipeline
    features = FeatureUnion([
        ("word_tfidf", TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1,
        )),
        ("char_wb_tfidf", TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            sublinear_tf=True,
            min_df=1,
        )),
    ])

    clf = LogisticRegression(
        C=5.0,
        class_weight="balanced",
        max_iter=1000,
        random_state=42,
        solver="lbfgs",
    )

    pipeline = Pipeline([
        ("expander", NewsExpander()),
        ("features", features),
        ("classifier", clf),
    ])

    # 3. Train
    t0 = time.time()
    pipeline.fit(X_train, y_train)
    train_time = round(time.time() - t0, 4)
    print(f"Training completed in {train_time}s")

    # 4. Evaluate Validation Set
    y_val_pred = pipeline.predict(X_val)
    val_acc = accuracy_score(y_val, y_val_pred)
    val_f1_macro = f1_score(y_val, y_val_pred, average="macro", zero_division=0)

    # 5. Evaluate Held-Out Test Set
    t_inf_start = time.time()
    y_test_pred = pipeline.predict(X_test)
    inf_time_per_sample_ms = round(((time.time() - t_inf_start) / max(len(X_test), 1)) * 1000, 3)

    test_acc = accuracy_score(y_test, y_test_pred)
    test_f1_macro = f1_score(y_test, y_test_pred, average="macro", zero_division=0)
    test_f1_weighted = f1_score(y_test, y_test_pred, average="weighted", zero_division=0)
    test_precision = precision_score(y_test, y_test_pred, average="weighted", zero_division=0)
    test_recall = recall_score(y_test, y_test_pred, average="weighted", zero_division=0)

    report = classification_report(y_test, y_test_pred, output_dict=True, zero_division=0)

    print(f"\n--- Held-Out Test Evaluation (News Classifier) ---")
    print(f"Accuracy:           {test_acc * 100:.2f}%")
    print(f"Macro F1:           {test_f1_macro:.4f}")
    print(f"Weighted F1:        {test_f1_weighted:.4f}")
    print(f"Weighted Precision: {test_precision:.4f}")
    print(f"Weighted Recall:    {test_recall:.4f}")
    print(f"Inference Latency:  {inf_time_per_sample_ms} ms / sample")

    # 6. Save Model and Metrics
    metadata = {
        "classes": list(pipeline.named_steps["classifier"].classes_),
        "num_classes": len(pipeline.named_steps["classifier"].classes_),
        "train_samples": len(X_train),
        "val_samples": len(X_val),
        "test_samples": len(X_test),
        "metrics": {
            "val_accuracy": round(val_acc, 4),
            "val_f1_macro": round(val_f1_macro, 4),
            "test_accuracy": round(test_acc, 4),
            "test_f1_macro": round(test_f1_macro, 4),
            "test_f1_weighted": round(test_f1_weighted, 4),
            "test_precision": round(test_precision, 4),
            "test_recall": round(test_recall, 4),
            "latency_ms": inf_time_per_sample_ms,
        },
        "classification_report": report,
    }

    joblib.dump(pipeline, MODEL_OUT_PATH)
    print(f"\nSaved model artifact to: {MODEL_OUT_PATH}")

    with open(METRICS_OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved evaluation metrics to: {METRICS_OUT_PATH}")

    return metadata

if __name__ == "__main__":
    train()
