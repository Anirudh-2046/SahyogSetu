"""
SahyogSetu Phase 10: Performance, Latency & System Resource Benchmark
Implements Phase 10.11:
- Measures latency distributions across all architectural components:
  1. Dense Query Embedding (embedding_service)
  2. Dense + Keyword Retrieval (hybrid_search_engine)
  3. Domain Legal Reranker (legal_reranker)
  4. End-to-End Chat Response (rag_pipeline)
  5. Cross-Lingual Translation (language_service)
  6. Speech Synthesis (TTS Manager)
  7. News Retrieval (database query)
  8. Conversation Thread Persistence (database write)
- Calculates Mean, Median (P50), P95, and P99 latency percentiles across warm and cold runs.
- Records hardware profile, provider state, and environment telemetry.
- Saves results to backend/evaluation/phase10/performance_eval_results.json
"""

import json
import time
import platform
import statistics
import sys
import os
import inspect
from pathlib import Path
from typing import Dict, Any, List

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.rag.rag_pipeline import rag_pipeline
from backend.rag.hybrid_search import hybrid_search_engine
from backend.rag.reranker import legal_reranker
from backend.services.embeddings.embedding_service import embedding_service
from backend.services.language import language_service, TranslationRequest
from backend.database import get_db_connection, get_news_items, create_conversation
from backend.config import settings

OUTPUT_PERF_RESULTS_PATH = Path(__file__).resolve().parent / "performance_eval_results.json"


def run_coro(coro):
    if not inspect.iscoroutine(coro):
        return coro
    stack = [coro]
    val = None
    while stack:
        current = stack[-1]
        try:
            res = current.send(val)
            if inspect.iscoroutine(res):
                stack.append(res)
                val = None
            else:
                val = res
        except StopIteration as e:
            stack.pop()
            val = e.value
    return val


def compute_percentiles(latencies: List[float]) -> Dict[str, float]:
    sorted_l = sorted(latencies)
    n = len(sorted_l)
    if n == 0:
        return {"mean": 0.0, "median": 0.0, "p95": 0.0, "p99": 0.0}
    
    mean_val = statistics.mean(sorted_l)
    median_val = statistics.median(sorted_l)
    p95_idx = min(int(n * 0.95), n - 1)
    p99_idx = min(int(n * 0.99), n - 1)

    return {
        "mean_ms": round(mean_val, 2),
        "median_ms": round(median_val, 2),
        "p95_ms": round(sorted_l[p95_idx], 2),
        "p99_ms": round(sorted_l[p99_idx], 2),
        "min_ms": round(sorted_l[0], 2),
        "max_ms": round(sorted_l[-1], 2),
        "samples": n,
    }


def run_performance_benchmarks():
    print("=" * 80)
    print("SAHYOGSETU PHASE 10: PERFORMANCE, LATENCY & RESOURCE BENCHMARK")
    print("=" * 80)

    # 1. Hardware & System Profiling
    sys_info = {
        "os": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }
    print(f"System: {sys_info['os']} {sys_info['machine']} | Python {sys_info['python_version']}")

    sample_queries = [
        "What are the requirements to register a cooperative society in Punjab?",
        "How long is the managing committee tenure under Haryana cooperative law?",
        "What is the collateral-free agricultural loan limit under Kisan Credit Card?",
        "How many hours do farmers have to notify localized crop loss under PMFBY?",
        "What relief does the PADB One Time Settlement scheme provide?",
    ]

    timings = {
        "embedding": [],
        "retrieval": [],
        "reranking": [],
        "translation": [],
        "tts_synthesis": [],
        "chat_end_to_end": [],
        "news_db_query": [],
        "db_conversation_write": [],
    }

    # Cold start timing
    t0 = time.perf_counter()
    _ = embedding_service.generate_embedding(sample_queries[0])
    cold_start_embedding_ms = round((time.perf_counter() - t0) * 1000, 2)
    print(f"Cold Start Embedding Latency: {cold_start_embedding_ms} ms")

    # Run 50 iterations across queries to get statistically sound distributions
    N_RUNS = 40
    print(f"Benchmarking warm execution across {N_RUNS} runs...")

    for i in range(N_RUNS):
        q = sample_queries[i % len(sample_queries)]

        # 1. Embedding
        t0 = time.perf_counter()
        vec = embedding_service.generate_embedding(q)
        timings["embedding"].append((time.perf_counter() - t0) * 1000)

        # 2. Retrieval
        t0 = time.perf_counter()
        hits = hybrid_search_engine.search(query=q, query_vector=vec, top_k=5)
        timings["retrieval"].append((time.perf_counter() - t0) * 1000)

        # 3. Reranking
        t0 = time.perf_counter()
        reranked = legal_reranker.rerank(candidates=hits, query=q, target_jurisdiction="all", top_k=3)
        timings["reranking"].append((time.perf_counter() - t0) * 1000)

        # 4. Translation
        t0 = time.perf_counter()
        trans_res = run_coro(language_service.translate_text(
            text="Under Section 8 of the Punjab Act 1961, registration requires 10 members.",
            source_language="en",
            target_language="pa",
        ))
        timings["translation"].append((time.perf_counter() - t0) * 1000)

        # 5. Speech Synthesis (TTS)
        t0 = time.perf_counter()
        tts_res = run_coro(language_service.generate_speech(
            text="Cooperative society registration requires ten adult members.",
            language="en",
        ))
        timings["tts_synthesis"].append((time.perf_counter() - t0) * 1000)

        # 6. News DB Query
        t0 = time.perf_counter()
        _ = get_news_items(limit=10)
        timings["news_db_query"].append((time.perf_counter() - t0) * 1000)

        # 7. DB Conversation Write
        t0 = time.perf_counter()
        test_conv_id = f"perf_bench_conv_{i}"
        create_conversation(conv_id=test_conv_id, title="Perf Test", jurisdiction="all", language="en")
        timings["db_conversation_write"].append((time.perf_counter() - t0) * 1000)

        # Cleanup test conv
        with get_db_connection() as conn:
            conn.execute("DELETE FROM conversations WHERE conversation_id = ?", (test_conv_id,))

        # 8. End-to-End Chat Pipeline
        t0 = time.perf_counter()
        _ = rag_pipeline.run_sync(query=q, user_language="en", user_jurisdiction="all")
        timings["chat_end_to_end"].append((time.perf_counter() - t0) * 1000)

    # Compute percentiles
    benchmarks_summary = {}
    print("\n" + "=" * 80)
    print("COMPONENT LATENCY DISTRIBUTIONS (MILLISECONDS)")
    print("=" * 80)
    print(f"{'Component':<25} | {'Mean':<8} | {'Median':<8} | {'P95':<8} | {'P99':<8} | {'Min':<8} | {'Max':<8}")
    print("-" * 88)

    for comp, lats in timings.items():
        stats = compute_percentiles(lats)
        benchmarks_summary[comp] = stats
        print(f"{comp:<25} | {stats['mean_ms']:<8.2f} | {stats['median_ms']:<8.2f} | {stats['p95_ms']:<8.2f} | {stats['p99_ms']:<8.2f} | {stats['min_ms']:<8.2f} | {stats['max_ms']:<8.2f}")

    report = {
        "hardware_profile": sys_info,
        "cold_start": {
            "embedding_initialization_ms": cold_start_embedding_ms,
        },
        "warm_benchmarks": benchmarks_summary,
        "sample_size_per_component": N_RUNS,
    }

    with open(OUTPUT_PERF_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\nResults successfully saved to:", OUTPUT_PERF_RESULTS_PATH)
    return report


if __name__ == "__main__":
    run_performance_benchmarks()
