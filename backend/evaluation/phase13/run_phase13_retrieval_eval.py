#!/usr/bin/env python3
"""
SahyogSetu Phase 13: Retrieval & Reranker Remediation Benchmark Evaluator
Runs ablation and comparison across:
1. Pure Semantic Vector Search (384-dim dense cosine similarity)
2. Pure Keyword / BM25 Search (lexical & section matching)
3. Hybrid RRF Search (Reciprocal Rank Fusion k=60.0)
4. Domain Legal Reranker (Production Pipeline with section & intent boosters)

Supports:
--dataset [dev|val|gold] (Default: dev)
Saves results to: backend/evaluation/phase13/retrieval_eval_results_{dataset}.json
"""

import json
import math
import sys
import os
import time
import argparse
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.rag.hybrid_search import hybrid_search_engine
from backend.rag.reranker import legal_reranker
from backend.rag.query_processor import query_processor
from backend.rag.jurisdiction_resolver import jurisdiction_resolver
from backend.services.embeddings.embedding_service import embedding_service
from backend.services.vector.sqlite_vector_store import sqlite_vector_store

def compute_dcg(relevances: List[int], k: int) -> float:
    dcg = 0.0
    for i in range(min(len(relevances), k)):
        rel = relevances[i]
        dcg += (2**rel - 1) / math.log2(i + 2)
    return dcg

def compute_ndcg(relevances: List[int], k: int) -> float:
    actual_dcg = compute_dcg(relevances, k)
    ideal_relevances = sorted(relevances, reverse=True)
    ideal_dcg = compute_dcg(ideal_relevances, k)
    return (actual_dcg / ideal_dcg) if ideal_dcg > 0 else 0.0

def is_chunk_match(chunk: Dict[str, Any], exp_doc: str, exp_sec: str, exp_evidence: str) -> Tuple[bool, bool, bool]:
    """
    Returns (doc_match, sec_match, passage_match).
    Strict hierarchical legal evaluation.
    """
    if not exp_doc:
        return False, False, False

    c_title = (chunk.get("document_title") or "").lower()
    c_doc_id = (chunk.get("doc_id") or "").lower()
    c_sec = str(chunk.get("section") or "").strip().lower()
    c_text = (chunk.get("chunk_text") or "").lower()

    exp_doc_lower = exp_doc.lower()

    # 1. Document match
    doc_match = (
        exp_doc_lower in c_title
        or c_title in exp_doc_lower
        or exp_doc_lower in c_doc_id
        or any(token in c_title for token in exp_doc_lower.split() if len(token) > 4)
    )

    if not doc_match:
        return False, False, False

    # 2. Section match (requires matching doc AND matching section if expected)
    if not exp_sec or exp_sec.lower() in ("none", ""):
        sec_match = doc_match
    else:
        exp_sec_clean = exp_sec.lower().replace("section", "").replace("rule", "").strip()
        sec_match = (
            c_sec == exp_sec_clean
            or f"section {exp_sec_clean}" in c_text[:250]
            or f"rule {exp_sec_clean}" in c_text[:250]
            or f"ਧਾਰਾ {exp_sec_clean}" in c_text[:250]
            or f"धारा {exp_sec_clean}" in c_text[:250]
        )

    # 3. Passage match (requires sec_match AND overlap with expected evidence)
    passage_match = False
    if sec_match and exp_evidence:
        ev_words = [w.lower() for w in re.findall(r"\w+", exp_evidence) if len(w) > 3]
        if ev_words:
            matched = sum(1 for w in ev_words if w in c_text)
            passage_match = (matched / len(ev_words)) >= 0.30
        else:
            passage_match = True

    return doc_match, sec_match, passage_match

def evaluate_retrieval(dataset_name: str = "dev"):
    print("=" * 80)
    print(f"SAHYOGSETU PHASE 13: RETRIEVAL REMEDIATION BENCHMARK ({dataset_name.upper()})")
    print("=" * 80)

    if dataset_name == "gold":
        dataset_path = Path("backend") / "evaluation" / "phase10" / "gold_benchmark_dataset.json"
    elif dataset_name == "val":
        dataset_path = Path("backend") / "evaluation" / "phase13" / "val_benchmark_dataset.json"
    else:
        dataset_path = Path("backend") / "evaluation" / "phase13" / "dev_benchmark_dataset.json"

    with open(dataset_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    eval_cases = [q for q in cases if q.get("expected_behavior") != "return_no_evidence" and q.get("expected_source_document")]
    total_cases = len(eval_cases)
    unsupported_count = len(cases) - total_cases
    print(f"Total queries: {len(cases)} | Evaluatable statutory: {total_cases} | Abstention/Unsupported: {unsupported_count}")

    paradigms = ["semantic_only", "keyword_only", "hybrid_rrf", "domain_reranker"]

    raw_metrics = {
        p: {
            "p1_sec": [], "p3_sec": [], "p5_sec": [],
            "r3_sec": [], "r5_sec": [],
            "mrr_sec": [], "ndcg3_sec": [], "ndcg5_sec": [],
            "p1_doc": [], "r3_doc": [], "mrr_doc": [],
            "passage_hit3": [],
            "latency_ms": [],
        }
        for p in paradigms
    }

    for idx, case in enumerate(eval_cases, 1):
        q_text = case["query_text"]
        user_lang = case["language"]
        user_jur = case["jurisdiction"]
        exp_doc = case["expected_source_document"]
        exp_sec = case["expected_section_or_rule"]
        exp_evidence = case.get("expected_evidence", "")

        pq = query_processor.process_query(q_text)
        jur_info = jurisdiction_resolver.resolve(query=q_text, user_jurisdiction=user_jur, detected_intent=pq["detected_intent"])
        allowed_jur = jur_info["allowed_jurisdictions"]
        q_vec = embedding_service.generate_embedding(q_text)

        candidates_map = {}

        # 1. Semantic Only
        t0 = time.perf_counter()
        raw_sem = sqlite_vector_store.search(query_vector=q_vec, top_k=15)
        sem_hits = [h for h in raw_sem if not allowed_jur or h["jurisdiction"].lower() in allowed_jur][:5]
        t_sem = (time.perf_counter() - t0) * 1000
        candidates_map["semantic_only"] = (sem_hits, t_sem)

        # 2. Keyword Only
        t0 = time.perf_counter()
        kw_hits = hybrid_search_engine._keyword_search(
            query=q_text,
            allowed_jurisdictions=allowed_jur,
            extracted_sections=pq["extracted_sections"],
            search_tokens=pq.get("search_keywords", []),
            limit=5,
        )
        t_kw = (time.perf_counter() - t0) * 1000
        candidates_map["keyword_only"] = (kw_hits, t_kw)

        # 3. Hybrid RRF
        t0 = time.perf_counter()
        rrf_hits = hybrid_search_engine.search(
            query=q_text,
            query_vector=q_vec,
            allowed_jurisdictions=allowed_jur,
            extracted_sections=pq["extracted_sections"],
            search_tokens=pq.get("search_keywords", []),
            top_k=5,
        )
        t_rrf = (time.perf_counter() - t0) * 1000
        candidates_map["hybrid_rrf"] = (rrf_hits, t_rrf)

        # 4. Domain Legal Reranker (Production)
        t0 = time.perf_counter()
        rrf_pool = hybrid_search_engine.search(
            query=q_text,
            query_vector=q_vec,
            allowed_jurisdictions=allowed_jur,
            extracted_sections=pq["extracted_sections"],
            search_tokens=pq.get("search_keywords", []),
            top_k=8,
        )
        rerank_hits = legal_reranker.rerank(
            candidates=rrf_pool,
            query=q_text,
            target_jurisdiction=jur_info.get("primary_jurisdiction", user_jur),
            extracted_sections=pq["extracted_sections"],
            detected_intent=pq["detected_intent"],
            top_k=5,
        )
        t_rerank = (time.perf_counter() - t0) * 1000
        candidates_map["domain_reranker"] = (rerank_hits, t_rerank)

        # Calculate metrics for each paradigm
        for p in paradigms:
            cand_hits, lat = candidates_map[p]
            raw_metrics[p]["latency_ms"].append(lat)

            # Check matches across top-5
            doc_matches = []
            sec_matches = []
            pas_matches = []

            for rank, hit in enumerate(cand_hits[:5]):
                d_m, s_m, p_m = is_chunk_match(hit, exp_doc, exp_sec, exp_evidence)
                doc_matches.append(d_m)
                sec_matches.append(s_m)
                pas_matches.append(p_m)

            # Pad up to 5 if fewer hits
            while len(sec_matches) < 5:
                doc_matches.append(False)
                sec_matches.append(False)
                pas_matches.append(False)

            # P@1, P@3, P@5 for section
            raw_metrics[p]["p1_sec"].append(1.0 if sec_matches[0] else 0.0)
            raw_metrics[p]["p3_sec"].append(sum(1.0 for m in sec_matches[:3] if m) / 3.0)
            raw_metrics[p]["p5_sec"].append(sum(1.0 for m in sec_matches[:5] if m) / 5.0)

            # Recall@3, Recall@5 for section
            raw_metrics[p]["r3_sec"].append(1.0 if any(sec_matches[:3]) else 0.0)
            raw_metrics[p]["r5_sec"].append(1.0 if any(sec_matches[:5]) else 0.0)

            # MRR for section
            mrr_s = 0.0
            for r_idx, m in enumerate(sec_matches):
                if m:
                    mrr_s = 1.0 / (r_idx + 1)
                    break
            raw_metrics[p]["mrr_sec"].append(mrr_s)

            # NDCG@3, NDCG@5 for section
            rel_scores = [1 if m else 0 for m in sec_matches]
            raw_metrics[p]["ndcg3_sec"].append(compute_ndcg(rel_scores, 3))
            raw_metrics[p]["ndcg5_sec"].append(compute_ndcg(rel_scores, 5))

            # Doc-level metrics
            raw_metrics[p]["p1_doc"].append(1.0 if doc_matches[0] else 0.0)
            raw_metrics[p]["r3_doc"].append(1.0 if any(doc_matches[:3]) else 0.0)
            mrr_d = 0.0
            for r_idx, m in enumerate(doc_matches):
                if m:
                    mrr_d = 1.0 / (r_idx + 1)
                    break
            raw_metrics[p]["mrr_doc"].append(mrr_d)

            # Passage Hit@3
            raw_metrics[p]["passage_hit3"].append(1.0 if any(pas_matches[:3]) else 0.0)

    # Compute summary averages
    summary: Dict[str, Any] = {
        "dataset": dataset_name,
        "total_queries": len(cases),
        "statutory_eval_queries": total_cases,
        "unsupported_queries": unsupported_count,
        "paradigms": {}
    }

    for p in paradigms:
        m = raw_metrics[p]
        n = max(len(m["p1_sec"]), 1)
        summary["paradigms"][p] = {
            "p1_section_level": round(sum(m["p1_sec"]) / n, 4),
            "p3_section_level": round(sum(m["p3_sec"]) / n, 4),
            "p5_section_level": round(sum(m["p5_sec"]) / n, 4),
            "recall3_section_level": round(sum(m["r3_sec"]) / n, 4),
            "recall5_section_level": round(sum(m["r5_sec"]) / n, 4),
            "mrr_section_level": round(sum(m["mrr_sec"]) / n, 4),
            "ndcg3_section_level": round(sum(m["ndcg3_sec"]) / n, 4),
            "ndcg5_section_level": round(sum(m["ndcg5_sec"]) / n, 4),
            "p1_document_level": round(sum(m["p1_doc"]) / n, 4),
            "recall3_document_level": round(sum(m["r3_doc"]) / n, 4),
            "mrr_document_level": round(sum(m["mrr_doc"]) / n, 4),
            "passage_hit3": round(sum(m["passage_hit3"]) / n, 4),
            "mean_latency_ms": round(sum(m["latency_ms"]) / n, 2),
        }

    print("\n" + "=" * 80)
    print("RETRIEVAL EVALUATION RESULTS SUMMARY")
    print("=" * 80)
    print(f"{'Paradigm':<20} | {'Sec P@1':<8} | {'Sec R@3':<8} | {'Sec MRR':<8} | {'Doc P@1':<8} | {'Doc R@3':<8} | {'Passage@3':<10}")
    print("-" * 80)
    for p, stats in summary["paradigms"].items():
        print(f"{p:<20} | {stats['p1_section_level']*100:6.2f}% | {stats['recall3_section_level']*100:6.2f}% | {stats['mrr_section_level']:8.4f} | {stats['p1_document_level']*100:6.2f}% | {stats['recall3_document_level']*100:6.2f}% | {stats['passage_hit3']*100:8.2f}%")
    print("=" * 80)

    # Save output
    out_dir = Path("backend") / "evaluation" / "phase13"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"retrieval_eval_results_{dataset_name}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"✓ Saved results to {out_path}")

    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["dev", "val", "gold"], default="dev")
    args = parser.parse_args()
    evaluate_retrieval(args.dataset)
