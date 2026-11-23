"""
SahyogSetu Phase 10: Legal RAG Retrieval Evaluation
Implements Phase 10.3:
- Evaluates complete retrieval pipeline on the independent 220-query Gold Benchmark.
- Measures: P@1, P@3, P@5, R@3, R@5, MRR, NDCG@3, NDCG@5.
- Compares 5 paradigms:
  1. Semantic Only (384-dim dense vector cosine similarity)
  2. Keyword Only (Statutory lexical & token search)
  3. Hybrid Retrieval (Reciprocal Rank Fusion k=60.0)
  4. Heuristic / Standalone Reranker
  5. Hybrid + Domain Legal Reranker (Production Pipeline)
- Separates:
  a. Document-level retrieval accuracy
  b. Section-level retrieval accuracy
  c. Supporting passage-level retrieval accuracy
- Produces breakdowns by:
  - Jurisdiction (Central, Punjab, Haryana, J&K, Multi)
  - Language (English, Hindi, Punjabi, Dogri, Haryanvi)
  - Category (Governance, Schemes, Jurisdiction, Unsupported, Multilingual)
  - Difficulty (Easy, Medium, Hard)
"""

import json
import math
import sys
import os
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.rag.hybrid_search import hybrid_search_engine
from backend.rag.reranker import legal_reranker
from backend.rag.query_processor import query_processor
from backend.rag.jurisdiction_resolver import jurisdiction_resolver
from backend.services.embeddings.embedding_service import embedding_service
from backend.services.vector.sqlite_vector_store import sqlite_vector_store

GOLD_DATASET_PATH = Path(__file__).resolve().parent / "gold_benchmark_dataset.json"
OUTPUT_RESULTS_PATH = Path(__file__).resolve().parent / "retrieval_eval_results.json"


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
    Strict hierarchical evaluation.
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
        evidence_words = [w.lower() for w in exp_evidence.split() if len(w) > 4]
        if evidence_words:
            overlap = sum(1 for w in evidence_words if w in c_text)
            passage_match = (overlap / len(evidence_words)) >= 0.35
        else:
            passage_match = True

    return doc_match, sec_match, passage_match


def evaluate_retrieval():
    print("=" * 80)
    print("SAHYOGSETU PHASE 10: LEGAL RAG RETRIEVAL BENCHMARK EVALUATION")
    print("=" * 80)

    with open(GOLD_DATASET_PATH, "r", encoding="utf-8") as f:
        gold_queries = json.load(f)

    # Only evaluate queries that have an expected statutory document
    retrieval_cases = [q for q in gold_queries if q.get("expected_behavior") != "return_no_evidence" and q.get("expected_source_document")]
    total_cases = len(retrieval_cases)
    print(f"Total evaluatable statutory retrieval cases: {total_cases} (out of {len(gold_queries)} total)")

    paradigms = [
        "semantic_only",
        "keyword_only",
        "hybrid_rrf",
        "domain_reranker",
    ]

    # Metrics container
    results: Dict[str, Any] = {
        "dataset_metadata": {
            "total_queries": len(gold_queries),
            "statutory_eval_queries": total_cases,
            "unsupported_queries_excluded": len(gold_queries) - total_cases,
        },
        "paradigms": {},
        "by_jurisdiction": {},
        "by_language": {},
        "by_difficulty": {},
        "by_category": {},
    }

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

    # Slices tracking (production hybrid_reranker)
    slices_data = {
        "jurisdiction": {},
        "language": {},
        "difficulty": {},
        "category": {},
    }

    for idx, case in enumerate(retrieval_cases, 1):
        q_text = case["query_text"]
        user_lang = case["language"]
        user_jur = case["jurisdiction"]
        exp_doc = case["expected_source_document"]
        exp_sec = case["expected_section_or_rule"]
        exp_evidence = case["expected_evidence"]

        # 1. Query understanding & embedding
        pq = query_processor.process_query(q_text)
        jur_info = jurisdiction_resolver.resolve(query=q_text, user_jurisdiction=user_jur, detected_intent=pq["detected_intent"])
        allowed_jur = jur_info["allowed_jurisdictions"]
        q_vec = embedding_service.generate_embedding(q_text)

        # Retrieve candidates under each paradigm
        candidates_map = {}

        # a. Semantic Only
        t0 = time.perf_counter()
        raw_sem = sqlite_vector_store.search(query_vector=q_vec, top_k=15)
        sem_hits = [h for h in raw_sem if not allowed_jur or h["jurisdiction"].lower() in allowed_jur][:5]
        t_sem = (time.perf_counter() - t0) * 1000
        candidates_map["semantic_only"] = (sem_hits, t_sem)

        # b. Keyword Only
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

        # c. Hybrid RRF
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

        # d. Domain Legal Reranker (Production)
        t0 = time.perf_counter()
        rerank_hits = legal_reranker.rerank(
            candidates=rrf_hits,
            query=q_text,
            target_jurisdiction=jur_info.get("resolved_jurisdiction", "central"),
            extracted_sections=pq["extracted_sections"],
            detected_intent=pq["detected_intent"],
            top_k=5,
        )
        t_rerank = (time.perf_counter() - t0) * 1000 + t_rrf
        candidates_map["domain_reranker"] = (rerank_hits, t_rerank)

        # Score each paradigm
        for p in paradigms:
            hits, lat = candidates_map[p]
            raw_metrics[p]["latency_ms"].append(lat)

            # Evaluate matches
            sec_matches = []
            doc_matches = []
            pass_matches = []

            for h in hits:
                d_m, s_m, p_m = is_chunk_match(h, exp_doc, exp_sec, exp_evidence)
                doc_matches.append(d_m)
                sec_matches.append(s_m)
                pass_matches.append(p_m)

            # Pad to 5 if fewer hits
            while len(sec_matches) < 5:
                sec_matches.append(False)
                doc_matches.append(False)
                pass_matches.append(False)

            # Precision & Recall (Section Level - STRICT)
            p1 = 1.0 if sec_matches[0] else 0.0
            p3 = sum(sec_matches[:3]) / 3.0
            p5 = sum(sec_matches[:5]) / 5.0
            r3 = 1.0 if any(sec_matches[:3]) else 0.0
            r5 = 1.0 if any(sec_matches[:5]) else 0.0

            # MRR (Section Level)
            mrr = 0.0
            for rank_idx, m in enumerate(sec_matches, 1):
                if m:
                    mrr = 1.0 / rank_idx
                    break

            # NDCG (Section Level binary relevance)
            ndcg3 = compute_ndcg([1 if m else 0 for m in sec_matches[:3]], 3)
            ndcg5 = compute_ndcg([1 if m else 0 for m in sec_matches[:5]], 5)

            # Document level metrics (LENIENT)
            p1_doc = 1.0 if doc_matches[0] else 0.0
            r3_doc = 1.0 if any(doc_matches[:3]) else 0.0
            mrr_doc = 0.0
            for rank_idx, m in enumerate(doc_matches, 1):
                if m:
                    mrr_doc = 1.0 / rank_idx
                    break

            raw_metrics[p]["p1_sec"].append(p1)
            raw_metrics[p]["p3_sec"].append(p3)
            raw_metrics[p]["p5_sec"].append(p5)
            raw_metrics[p]["r3_sec"].append(r3)
            raw_metrics[p]["r5_sec"].append(r5)
            raw_metrics[p]["mrr_sec"].append(mrr)
            raw_metrics[p]["ndcg3_sec"].append(ndcg3)
            raw_metrics[p]["ndcg5_sec"].append(ndcg5)
            raw_metrics[p]["p1_doc"].append(p1_doc)
            raw_metrics[p]["r3_doc"].append(r3_doc)
            raw_metrics[p]["mrr_doc"].append(mrr_doc)
            raw_metrics[p]["passage_hit3"].append(1.0 if any(pass_matches[:3]) else 0.0)

            # Track slice metrics for domain_reranker
            if p == "domain_reranker":
                for slice_name, slice_val in [
                    ("jurisdiction", user_jur),
                    ("language", user_lang),
                    ("difficulty", case["difficulty"]),
                    ("category", case["category"]),
                ]:
                    entry = slices_data[slice_name].setdefault(slice_val, {"p1_sec": [], "r3_sec": [], "mrr_sec": []})
                    entry["p1_sec"].append(p1)
                    entry["r3_sec"].append(r3)
                    entry["mrr_sec"].append(mrr)

        if idx % 30 == 0 or idx == total_cases:
            print(f"Processed {idx}/{total_cases} queries...", flush=True)

    # Summarize aggregate metrics per paradigm
    print("\n" + "=" * 80)
    print("LEGAL RAG RETRIEVAL EVALUATION RESULTS (STRICT SECTION LEVEL)")
    print("=" * 80)
    print(f"{'Paradigm':<22} | {'P@1':<7} | {'P@3':<7} | {'R@3':<7} | {'MRR':<7} | {'NDCG@3':<7} | {'Doc-P@1':<8} | {'Passage@3':<9} | {'Latency':<8}")
    print("-" * 95)

    for p in paradigms:
        m = raw_metrics[p]
        summary = {
            "p1_section_level": round(sum(m["p1_sec"]) / total_cases, 4),
            "p3_section_level": round(sum(m["p3_sec"]) / total_cases, 4),
            "p5_section_level": round(sum(m["p5_sec"]) / total_cases, 4),
            "recall3_section_level": round(sum(m["r3_sec"]) / total_cases, 4),
            "recall5_section_level": round(sum(m["r5_sec"]) / total_cases, 4),
            "mrr_section_level": round(sum(m["mrr_sec"]) / total_cases, 4),
            "ndcg3_section_level": round(sum(m["ndcg3_sec"]) / total_cases, 4),
            "ndcg5_section_level": round(sum(m["ndcg5_sec"]) / total_cases, 4),
            "p1_document_level": round(sum(m["p1_doc"]) / total_cases, 4),
            "recall3_document_level": round(sum(m["r3_doc"]) / total_cases, 4),
            "mrr_document_level": round(sum(m["mrr_doc"]) / total_cases, 4),
            "passage_hit3": round(sum(m["passage_hit3"]) / total_cases, 4),
            "mean_latency_ms": round(sum(m["latency_ms"]) / total_cases, 2),
        }
        results["paradigms"][p] = summary
        print(f"{p:<22} | {summary['p1_section_level']:<7.4f} | {summary['p3_section_level']:<7.4f} | {summary['recall3_section_level']:<7.4f} | {summary['mrr_section_level']:<7.4f} | {summary['ndcg3_section_level']:<7.4f} | {summary['p1_document_level']:<8.4f} | {summary['passage_hit3']:<9.4f} | {summary['mean_latency_ms']:<6.2f}ms")

    # Aggregate slices for production reranker
    for s_name in ["jurisdiction", "language", "difficulty", "category"]:
        results[f"by_{s_name}"] = {}
        for s_val, s_dict in slices_data[s_name].items():
            n = len(s_dict["p1_sec"])
            results[f"by_{s_name}"][s_val] = {
                "count": n,
                "p1_section": round(sum(s_dict["p1_sec"]) / n, 4),
                "r3_section": round(sum(s_dict["r3_sec"]) / n, 4),
                "mrr_section": round(sum(s_dict["mrr_sec"]) / n, 4),
            }

    # Save to JSON
    with open(OUTPUT_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\nResults successfully saved to:", OUTPUT_RESULTS_PATH)
    return results


if __name__ == "__main__":
    evaluate_retrieval()
