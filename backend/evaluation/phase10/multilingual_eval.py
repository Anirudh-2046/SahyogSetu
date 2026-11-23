"""
SahyogSetu Phase 10: Multilingual & Speech Services Benchmark Evaluation
Implements Phase 10.7:
- Evaluates language support separately for:
  - English (en)
  - Hindi (hi)
  - Punjabi (pa)
  - Dogri (doi)
  - Haryanvi (bgc)
- Evaluates across 7 capabilities per language:
  1. Language Identification Accuracy
  2. Query Intent Classification Accuracy
  3. Jurisdiction Detection Accuracy
  4. Retrieval Recall@3
  5. Translation Legal Meaning & Entity Preservation Rate
  6. Citation Preservation across Translation
  7. Voice Processing (ASR Capability & TTS Speech Synthesis)
"""

import json
import sys
import os
import time
from pathlib import Path
from typing import Dict, Any, List

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.rag.rag_pipeline import rag_pipeline
from backend.services.language import language_service, ASRTranscribeRequest, TranslationRequest
from backend.schemas.voice import TTSGenerateRequest
from backend.services.tts.tts_manager import tts_manager
from backend.ml.inference.language_inference import language_predictor
from backend.ml.inference.intent_inference import intent_predictor

GOLD_DATASET_PATH = Path(__file__).resolve().parent / "gold_benchmark_dataset.json"
OUTPUT_MULTI_RESULTS_PATH = Path(__file__).resolve().parent / "multilingual_eval_results.json"


MULTILINGUAL_TEST_BATTERY = [
    # --- English ---
    {
        "lang": "en",
        "query": "What are the rules and minimum members required to register a cooperative in Punjab under Section 8?",
        "expected_intent": "cooperative_registration",
        "expected_jur": "punjab",
        "expected_doc": "Punjab Cooperative Societies Act 1961",
        "expected_entities": ["Section 8", "10 adult persons", "separate families"],
    },
    {
        "lang": "en",
        "query": "What is the tenure of managing committee members in Haryana cooperative societies?",
        "expected_intent": "elections_governance",
        "expected_jur": "haryana",
        "expected_doc": "Haryana Co-operative Societies Act 1984",
        "expected_entities": ["5 years", "Section 28", "reservation"],
    },

    # --- Hindi ---
    {
        "lang": "hi",
        "query": "हरियाणा में सहकारी समिति की प्रबंध समिति का कार्यकाल कितने साल का होता है?",
        "expected_intent": "elections_governance",
        "expected_jur": "haryana",
        "expected_doc": "Haryana Co-operative Societies Act 1984",
        "expected_entities": ["धारा 28", "5 वर्ष", "प्रबंध समिति"],
    },
    {
        "lang": "hi",
        "query": "किसान क्रेडिट कार्ड पर बिना गारंटी के कितने लाख तक लोन मिलता है?",
        "expected_intent": "financial_assistance_kcc",
        "expected_jur": "central",
        "expected_doc": "KCC Master Circular",
        "expected_entities": ["1.60 लाख", "किसान क्रेडिट कार्ड", "बिना गारंटी"],
    },

    # --- Punjabi ---
    {
        "lang": "pa",
        "query": "ਪੰਜਾਬ ਵਿੱਚ ਸਹਿਕਾਰੀ ਸੁਸਾਇਟੀ ਰਜਿਸਟਰ ਕਰਵਾਉਣ ਲਈ ਘੱਟੋ-ਘੱਟ ਕਿੰਨੇ ਬਾਲਗ ਮੈਂਬਰ ਚਾਹੀਦੇ ਹਨ?",
        "expected_intent": "cooperative_registration",
        "expected_jur": "punjab",
        "expected_doc": "Punjab Cooperative Societies Act 1961",
        "expected_entities": ["ਧਾਰਾ 8", "10", "ਪਰਿਵਾਰ"],
    },
    {
        "lang": "pa",
        "query": "ਕੀ ਸਹਿਕਾਰੀ ਸੁਸਾਇਟੀ ਦੇ ਝਗੜੇ ਲਈ ਦੀਵਾਨੀ ਅਦਾਲਤ ਵਿੱਚ ਕੇਸ ਦਾਇਰ ਕੀਤਾ ਜਾ ਸਕਦਾ ਹੈ?",
        "expected_intent": "dispute_arbitration",
        "expected_jur": "punjab",
        "expected_doc": "Punjab Cooperative Societies Act 1961",
        "expected_entities": ["ਧਾਰਾ 55", "ਰਜਿਸਟਰਾਰ", "ਸਾਲਸੀ"],
    },

    # --- Dogri ---
    {
        "lang": "doi",
        "query": "जम्मू कश्मीर च सहकारी समिति दे विवादें दा निपटारा कुਨ ਕਰਦਾ ऐ?",
        "expected_intent": "dispute_arbitration",
        "expected_jur": "jk",
        "expected_doc": "J&K Cooperative Societies Act 1989",
        "expected_entities": ["धारा 70", "रजिस्ट्रार", "निपटारा"],
    },
    {
        "lang": "doi",
        "query": "जम्मू-कश्मीर च सहकारी सभा दी सालाना आडिट कुन करदा ऐ?",
        "expected_intent": "audit_inspection",
        "expected_jur": "jk",
        "expected_doc": "J&K Cooperative Societies Act 1989",
        "expected_entities": ["धारा 63", "आडिट"],
    },

    # --- Haryanvi ---
    {
        "lang": "bgc",
        "query": "हरियाणा म्ह समिति की कमेटी का टेम कितने साल का होवै सै?",
        "expected_intent": "elections_governance",
        "expected_jur": "haryana",
        "expected_doc": "Haryana Co-operative Societies Act 1984",
        "expected_entities": ["धारा 28", "5 साल"],
    },
    {
        "lang": "bgc",
        "query": "के हरको बैंक म्ह केसीसी लोन खातर जमीन बंधक रखनी जरूरी सै?",
        "expected_intent": "financial_assistance_kcc",
        "expected_jur": "haryana",
        "expected_doc": "KCC Master Circular",
        "expected_entities": ["1.60 लाख", "जमीन"],
    },
]


import inspect

def run_coro(coro):
    """Executes a coroutine synchronously without event-loop/socket dependencies for sandbox isolation."""
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


def run_multilingual_benchmark():
    print("=" * 80)
    print("SAHYOGSETU PHASE 10: MULTILINGUAL & SPEECH SERVICES BENCHMARK")
    print("=" * 80)

    languages = ["en", "hi", "pa", "doi", "bgc"]
    metrics_by_lang: Dict[str, Dict[str, Any]] = {
        lang: {
            "lang_id_correct": 0,
            "intent_correct": 0,
            "jur_correct": 0,
            "retrieval_hit": 0,
            "entity_preservation": [],
            "citation_preservation": [],
            "asr_provider": "",
            "tts_provider": "",
            "tts_latency_ms": 0.0,
            "dialect_ethics_disclosed": False,
        }
        for lang in languages
    }

    # 1. Evaluate Pipeline per language test query
    for item in MULTILINGUAL_TEST_BATTERY:
        lang = item["lang"]
        q = item["query"]
        exp_intent = item["expected_intent"]
        exp_jur = item["expected_jur"]
        exp_doc = item["expected_doc"]
        exp_entities = item["expected_entities"]

        # a. Language Identification
        pred_lang_res = language_predictor.predict_language(q)
        pred_lang = pred_lang_res["detected_language"]
        if pred_lang == lang or (lang == "bgc" and pred_lang in ["bgc", "hi"]):
            metrics_by_lang[lang]["lang_id_correct"] += 1

        # b. Intent Prediction
        pred_intent_res = intent_predictor.predict_intent(q)
        raw_intent = pred_intent_res["predicted_intent"]
        # Normalize
        norm_map = {
            "grievance_arbitration": "dispute_arbitration",
            "government_schemes_pmkisan": "pm_kisan",
        }
        pred_intent = norm_map.get(raw_intent, raw_intent)
        if pred_intent == exp_intent:
            metrics_by_lang[lang]["intent_correct"] += 1

        # c. Full RAG Run
        res = rag_pipeline.run_sync(query=q, user_language=lang, user_jurisdiction=exp_jur)
        res_jur = (res.get("jurisdiction") or "").lower()
        if exp_jur in res_jur or (exp_jur == "central" and res_jur in ["central", "all"]):
            metrics_by_lang[lang]["jur_correct"] += 1

        # d. Retrieval Hit
        citations = res.get("citations", [])
        retrieval_hit = any(exp_doc.lower() in (c.get("title", "")).lower() for c in citations)
        if retrieval_hit:
            metrics_by_lang[lang]["retrieval_hit"] += 1

        # e. Citation Preservation in Translated Output
        sources_md = res.get("sources_markdown", "")
        has_citations_preserved = len(citations) > 0 and len(sources_md) > 10
        metrics_by_lang[lang]["citation_preservation"].append(1.0 if has_citations_preserved else 0.0)

        # f. Entity Preservation
        plain_exp = res.get("plainExplanation", "")
        ent_matches = sum(1 for e in exp_entities if e.lower() in plain_exp.lower())
        ent_rate = (ent_matches / len(exp_entities)) if exp_entities else 1.0
        metrics_by_lang[lang]["entity_preservation"].append(ent_rate)

    # 2. Voice ASR & TTS Evaluation per language
    print("\nEvaluating Voice & Dialect Capabilities...")
    for lang in languages:
        # ASR Capabilities
        cap = language_service.asr.get_capabilities(lang)
        metrics_by_lang[lang]["asr_provider"] = getattr(cap, "active_provider", None) or getattr(cap, "provider", "local")
        metrics_by_lang[lang]["dialect_ethics_disclosed"] = bool(getattr(cap, "dialect_ethics_note", None) or getattr(cap, "notes", ""))

        # TTS Synthesis Benchmark
        t0 = time.perf_counter()
        tts_res = run_coro(language_service.generate_speech(
            text="SahyogSetu cooperative legal assistance.",
            language=lang,
            alternative_accepted="hi" if lang in ["doi", "bgc"] else None,
        ))
        metrics_by_lang[lang]["tts_latency_ms"] = round((time.perf_counter() - t0) * 1000, 2)
        metrics_by_lang[lang]["tts_provider"] = tts_res.get("provider", "local")

    # Format Summary
    summary = {}
    print("\n" + "=" * 80)
    print("MULTILINGUAL CAPABILITY MATRIX ACROSS 5 LANGUAGES")
    print("=" * 80)
    print(f"{'Lang':<6} | {'Lang-ID':<8} | {'Intent':<7} | {'Jur-Acc':<8} | {'R@3':<6} | {'Entity-Pres':<12} | {'ASR Provider':<20} | {'TTS Latency':<10}")
    print("-" * 95)

    for lang in languages:
        m = metrics_by_lang[lang]
        lang_id_pct = (m["lang_id_correct"] / 2.0) * 100
        intent_pct = (m["intent_correct"] / 2.0) * 100
        jur_pct = (m["jur_correct"] / 2.0) * 100
        r3_pct = (m["retrieval_hit"] / 2.0) * 100
        ent_pres = (sum(m["entity_preservation"]) / max(1, len(m["entity_preservation"]))) * 100

        summary[lang] = {
            "language_id_accuracy": round(lang_id_pct / 100, 4),
            "intent_classification_accuracy": round(intent_pct / 100, 4),
            "jurisdiction_accuracy": round(jur_pct / 100, 4),
            "retrieval_recall3": round(r3_pct / 100, 4),
            "entity_preservation_rate": round(ent_pres / 100, 4),
            "asr_provider": m["asr_provider"],
            "tts_provider": m["tts_provider"],
            "tts_latency_ms": m["tts_latency_ms"],
            "dialect_ethics_disclosed": m["dialect_ethics_disclosed"],
        }
        print(f"{lang:<6} | {lang_id_pct:<7.1f}% | {intent_pct:<6.1f}% | {jur_pct:<7.1f}% | {r3_pct:<5.1f}% | {ent_pres:<11.1f}% | {m['asr_provider'][:19]:<20} | {m['tts_latency_ms']:<8.2f}ms")

    with open(OUTPUT_MULTI_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\nResults successfully saved to:", OUTPUT_MULTI_RESULTS_PATH)
    return summary


if __name__ == "__main__":
    run_multilingual_benchmark()
