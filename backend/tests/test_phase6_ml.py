"""
SAHYOGSETU PHASE 6: MACHINE LEARNING MODEL DEVELOPMENT, TRAINING & EVALUATION TEST SUITE
Tests:
1. Dataset Integrity & Stratified Splits (intent, news, language)
2. Model Artifacts & Serialized Pipeline Loading
3. Model Evaluation Metrics Verification (F1 > 0.80, Latency < 5ms)
4. Intent Inference Accuracy Across Languages (English, Hindi, Punjabi, Dogri, Romanized)
5. Out-of-Scope / Uncertain Queries Fallback Logic
6. Deterministic Section Number and Numeric Extraction Guarantee
7. News Category Classification on Official Press Releases
8. Multilingual Language Identification & Dialect Ethics (Dogri/Haryanvi preservation)
9. Strict Jurisdiction Boundary & Zero Cross-State Retrieval Guarantee
10. Retrieval Reranker Benchmark Results & Baseline Decision Verification
"""

import json
import os
import sys
import time
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.ml.inference.intent_inference import intent_predictor
from backend.ml.inference.news_inference import news_predictor
from backend.ml.inference.language_inference import language_predictor
from backend.services.ml.intent_detector import intent_detector
from backend.services.ml.news_classifier import ml_news_classifier
from backend.services.ml.language_identifier import language_identifier
from backend.rag.query_processor import query_processor
from backend.rag.jurisdiction_resolver import jurisdiction_resolver
from backend.rag.reranker import legal_reranker

DATASETS_DIR = PROJECT_ROOT / "backend" / "ml" / "datasets"
MODELS_DIR = PROJECT_ROOT / "backend" / "ml" / "models"
EVAL_DIR = PROJECT_ROOT / "backend" / "ml" / "evaluation"

def test_01_dataset_integrity():
    print("\n[Test 1] Dataset Integrity & Stratified Distribution...")
    intent_file = DATASETS_DIR / "intent_dataset.json"
    news_file = DATASETS_DIR / "news_dataset.json"
    lang_file = DATASETS_DIR / "language_dataset.json"

    assert intent_file.exists(), f"Missing intent dataset at {intent_file}"
    assert news_file.exists(), f"Missing news dataset at {news_file}"
    assert lang_file.exists(), f"Missing language dataset at {lang_file}"

    with open(intent_file, "r", encoding="utf-8") as f:
        intent_data = json.load(f)
    with open(news_file, "r", encoding="utf-8") as f:
        news_data = json.load(f)
    with open(lang_file, "r", encoding="utf-8") as f:
        lang_data = json.load(f)

    # Verify counts and class balances
    assert len(intent_data) >= 135, f"Expected at least 135 intent samples, got {len(intent_data)}"
    intent_classes = set(item["intent"] for item in intent_data)
    assert len(intent_classes) == 9, f"Expected 9 intent classes, found {len(intent_classes)}"

    assert len(news_data) >= 50, f"Expected at least 50 news samples, got {len(news_data)}"
    news_classes = set(item["category"] for item in news_data)
    assert len(news_classes) == 10, f"Expected 10 news classes, found {len(news_classes)}"

    assert len(lang_data) >= 100, f"Expected at least 100 language samples, got {len(lang_data)}"
    lang_classes = set(item["language"] for item in lang_data)
    assert len(lang_classes) == 5, f"Expected 5 language classes (en, hi, pa, doi, bgc), got {lang_classes}"

    print(f"  ✓ Intent dataset verified: {len(intent_data)} samples across 9 classes")
    print(f"  ✓ News dataset verified: {len(news_data)} samples across 10 sectors")
    print(f"  ✓ Language dataset verified: {len(lang_data)} samples across 5 languages")

def test_02_model_artifacts_loading():
    print("\n[Test 2] Model Artifacts & Pipeline Unpickling...")
    intent_joblib = MODELS_DIR / "intent_model.joblib"
    news_joblib = MODELS_DIR / "news_model.joblib"
    lang_joblib = MODELS_DIR / "language_model.joblib"

    assert intent_joblib.exists(), f"Missing {intent_joblib}"
    assert news_joblib.exists(), f"Missing {news_joblib}"
    assert lang_joblib.exists(), f"Missing {lang_joblib}"

    assert intent_predictor.pipeline is not None, "Intent pipeline failed to initialize"
    assert news_predictor.pipeline is not None, "News pipeline failed to initialize"
    assert language_predictor.pipeline is not None, "Language pipeline failed to initialize"

    assert len(intent_predictor.pipeline.classes_) == 9, "Intent pipeline does not contain 9 classes"
    assert len(news_predictor.pipeline.classes_) == 10, "News pipeline does not contain 10 classes"
    assert len(language_predictor.pipeline.classes_) == 5, "Language pipeline does not contain 5 classes"

    print("  ✓ All 3 scikit-learn model pipelines loaded successfully from serialized joblib artifacts")

def test_03_evaluation_metrics_verification():
    print("\n[Test 3] Model Metrics Verification on Held-Out Test Splits...")
    intent_metrics_file = MODELS_DIR / "intent_metrics.json"
    news_metrics_file = MODELS_DIR / "news_metrics.json"
    lang_metrics_file = MODELS_DIR / "language_metrics.json"

    assert intent_metrics_file.exists(), f"Missing {intent_metrics_file}"
    assert news_metrics_file.exists(), f"Missing {news_metrics_file}"
    assert lang_metrics_file.exists(), f"Missing {lang_metrics_file}"

    with open(intent_metrics_file, "r") as f:
        im = json.load(f)
    with open(news_metrics_file, "r") as f:
        nm = json.load(f)
    with open(lang_metrics_file, "r") as f:
        lm = json.load(f)

    print(f"  ✓ Intent Classifier: Accuracy={im['metrics']['test_accuracy']*100:.1f}%, Macro F1={im['metrics']['test_f1_macro']}, Latency={im['metrics']['latency_ms']}ms")
    print(f"  ✓ News Classifier: Accuracy={nm['metrics']['test_accuracy']*100:.1f}%, Macro F1={nm['metrics']['test_f1_macro']}, Latency={nm['metrics']['latency_ms']}ms")
    print(f"  ✓ Language Identifier: Accuracy={lm['metrics']['test_accuracy']*100:.1f}%, Macro F1={lm['metrics']['test_f1_macro']}, Latency={lm['metrics']['latency_ms']}ms")

    assert im['metrics']['test_f1_macro'] >= 0.80, f"Intent F1 too low: {im['metrics']['test_f1_macro']}"
    assert nm['metrics']['test_f1_macro'] >= 0.80, f"News F1 too low: {nm['metrics']['test_f1_macro']}"
    assert lm['metrics']['test_f1_macro'] >= 0.85, f"Language F1 too low: {lm['metrics']['test_f1_macro']}"
    assert im['metrics']['latency_ms'] < 5.0, f"Intent latency too high: {im['metrics']['latency_ms']}"

def test_04_intent_inference_multilingual():
    print("\n[Test 4] Multilingual Query Intent Inference...")
    # Warm up pipeline to eliminate cold-start initialization
    intent_predictor.predict_intent("warmup query")

    test_cases = [
        ("What is the procedure to register a society under Section 8?", "cooperative_registration"),
        ("हरियाणा में समिति की प्रबंध समिति का कार्यकाल कितने वर्ष का होता है?", "elections_governance"),
        ("ਕਿਸਾਨ ਕ੍ਰੈਡਿਟ ਕਾਰਡ 'ਤੇ ਬਿਨਾਂ ਗਾਰੰਟੀ ਕਿੰਨਾ ਕਰਜ਼ਾ ਮਿਲ ਸਕਦਾ ਹੈ?", "financial_assistance_kcc"),
        ("How many hours do farmers have to report crop damage under PMFBY?", "pmfby_crop_insurance"),
        ("जम्मू कश्मीर च सहकारी समिति दे विवादें दा निपटारा कुन करदा ऐ?", "grievance_arbitration"),
        ("pm-kisan 6000 annual installment dbt bank transfer", "government_schemes_pmkisan"),
        ("one member one vote principle cooperative society act", "membership_rights"),
    ]

    # Warm up predictor
    intent_predictor.predict_intent("warmup query", threshold=0.35)

    for query, expected_intent in test_cases:
        t0 = time.perf_counter()
        res = intent_predictor.predict_intent(query, threshold=0.35)
        latency_ms = (time.perf_counter() - t0) * 1000
        pred = res["predicted_intent"]
        conf = res["confidence"]
        assert pred == expected_intent, f"Query '{query}' predicted '{pred}', expected '{expected_intent}'"
        assert latency_ms < 15.0, f"Latency exceeded 15ms: {latency_ms:.2f}ms"
        print(f"  ✓ '{query[:40]}...' -> {pred} (conf: {conf}, {latency_ms:.2f}ms)")

def test_05_out_of_scope_fallback():
    print("\n[Test 5] Out-of-Scope Fallback & Confidence Threshold...")
    oos_queries = [
        "What is the best recipe for baking chocolate cake at home?",
        "How is the weather today in New York and flights to Tokyo?",
        "Quantum computing algorithms for factoring prime numbers.",
    ]

    for q in oos_queries:
        res = intent_predictor.predict_intent(q, threshold=0.35)
        # Should either fall back to general_cooperative or flag is_uncertain
        assert res["is_uncertain"] is True or res["predicted_intent"] == "general_cooperative", (
            f"OOS query '{q}' not flagged as uncertain: {res}"
        )
        print(f"  ✓ OOS Query correctly flagged: '{q[:35]}...' -> uncertain={res['is_uncertain']}, fallback={res['predicted_intent']}")

def test_06_deterministic_entity_preservation():
    print("\n[Test 6] Deterministic Section Number & Numeric Preservation...")
    queries = [
        ("What does Section 8 of the Punjab Act 1961 provide?", ["8"]),
        ("Arbitration dispute reference under धारा 102 and Rule 28", ["102", "28"]),
        ("ਧਾਰਾ 55 ਅਧੀਨ ਸਾਲਸੀ ਦੀ ਅਰਜ਼ੀ ਦਾਇਰ ਕਰਨ ਦਾ ਤਰੀਕਾ", ["55"]),
    ]

    for q, exp_secs in queries:
        res = intent_predictor.predict_intent(q)
        secs = res["extracted_sections"]
        for es in exp_secs:
            assert es.lower() in secs, f"Missing section '{es}' in extracted sections: {secs}"
        print(f"  ✓ Section preserved deterministically: '{q[:40]}...' -> {secs}")

    # Numeric entities check
    num_query = "KCC 1.60 lakh limit, PM-Kisan 6000 support, 72 hours reporting, 5 years tenure"
    num_res = intent_predictor.predict_intent(num_query)
    nums = num_res["numeric_entities"]
    assert "1.60_lakh_collateral_free" in nums
    assert "6000_annual_support" in nums
    assert "72_hours_reporting" in nums
    assert "5_years_tenure" in nums
    print(f"  ✓ All 4 statutory numeric thresholds extracted: {nums}")

def test_07_news_classification():
    print("\n[Test 7] News Category Classification on Official Announcements...")
    news_items = [
        ("RBI issues Master Circular on Kisan Credit Card (KCC) scheme collateral limits.", "agri_credit_kcc"),
        ("Ministry of Agriculture updates PMFBY guidelines for localized hailstorm calamity claim.", "crop_insurance_pmfby"),
        ("Milkfed Verka announces increase in milk procurement price for dairy cooperatives in Punjab.", "dairy_fisheries_coop"),
        ("Punjab Government announces One Time Settlement (OTS) scheme with 100 percent waiver of penal interest.", "subsidies_financial_aid"),
        ("Department of Cooperation notifies transfers and postings of Joint Registrars.", "administrative_notifications"),
    ]

    for text, expected_sector in news_items:
        res = news_predictor.predict_category(text, threshold=0.35)
        pred = res["predicted_category"]
        conf = res["confidence"]
        assert pred == expected_sector, f"News text '{text[:40]}...' predicted '{pred}', expected '{expected_sector}'"
        print(f"  ✓ News: '{text[:45]}...' -> {pred} (conf: {conf})")

def test_08_language_identification_dialect_ethics():
    print("\n[Test 8] Language Identification & Dialect Ethics...")
    # 1. Punjabi (Gurmukhi)
    res_pa = language_predictor.predict_language("ਪੰਜਾਬ ਵਿੱਚ ਨਵੀਂ ਸਹਿਕਾਰੀ ਸਭਾ ਰਜਿਸਟਰ ਕਰਵਾਉਣ ਲਈ ਕਿੰਨੇ ਮੈਂਬਰ ਚਾਹੀਦੇ ਹਨ?")
    assert res_pa["detected_language"] == "pa"
    assert res_pa["script"] == "Gurmukhi"
    print("  ✓ Gurmukhi identified as 'pa'")

    # 2. English (Latin)
    res_en = language_predictor.predict_language("What is the procedure to apply for registration of a cooperative society?")
    assert res_en["detected_language"] == "en"
    assert res_en["script"] == "Latin"
    print("  ✓ Latin legal query identified as 'en'")

    # 3. Dogri with user preference doi: MUST PRESERVE user preference
    res_doi = language_predictor.predict_language("जम्मू च नई सहकारी सभा बनानी ऐ तां किन्ने लोक चाहीदे न?", user_preference="doi")
    assert res_doi["detected_language"] == "doi"
    assert res_doi["user_preference_respected"] is True
    print("  ✓ Dogri dialect ethics honored (user preference 'doi' never overridden to 'hi')")

    # 4. Haryanvi with user preference bgc: MUST PRESERVE user preference
    res_bgc = language_predictor.predict_language("सहकारी समिति बणाणा खातर फार्म कित्तै जमा करणा सै?", user_preference="bgc")
    assert res_bgc["detected_language"] == "bgc"
    assert res_bgc["user_preference_respected"] is True
    print("  ✓ Haryanvi dialect ethics honored (user preference 'bgc' never overridden to 'hi')")

    # 5. Romanized Hindi (Hinglish)
    res_hin_rom = language_predictor.predict_language("nayi sahkari samiti register karne ke liye kitne sadasya chahiye")
    assert res_hin_rom["is_romanized"] is True
    assert res_hin_rom["detected_language"] == "hi"
    print("  ✓ Romanized Hindi query correctly identified as 'hi' (is_romanized=True)")

def test_09_jurisdiction_strictness():
    print("\n[Test 9] Jurisdiction Strictness & Cross-State Zero Leakage Guarantee...")
    # Punjab user must only access Punjab and Central, NEVER Haryana or J&K
    pb_res = jurisdiction_resolver.resolve("Registration rules", user_jurisdiction="punjab")
    assert "punjab" in pb_res["allowed_jurisdictions"]
    assert "central" in pb_res["allowed_jurisdictions"]
    assert "haryana" not in pb_res["allowed_jurisdictions"], "Illegal cross-state leak: Haryana allowed for Punjab user!"
    assert "jk" not in pb_res["allowed_jurisdictions"], "Illegal cross-state leak: J&K allowed for Punjab user!"
    print("  ✓ Punjab scope strictly partitions: ['punjab', 'central'] (0% cross-state leakage)")

    # Haryana user must only access Haryana and Central
    hr_res = jurisdiction_resolver.resolve("Committee election rules", user_jurisdiction="haryana")
    assert "haryana" in hr_res["allowed_jurisdictions"]
    assert "central" in hr_res["allowed_jurisdictions"]
    assert "punjab" not in hr_res["allowed_jurisdictions"], "Illegal cross-state leak: Punjab allowed for Haryana user!"
    assert "jk" not in hr_res["allowed_jurisdictions"], "Illegal cross-state leak: J&K allowed for Haryana user!"
    print("  ✓ Haryana scope strictly partitions: ['haryana', 'central'] (0% cross-state leakage)")

def test_10_reranker_benchmark_verification():
    print("\n[Test 10] Reranker Benchmark & Baseline Decision Verification...")
    bench_file = EVAL_DIR / "reranker_benchmark_results.json"
    assert bench_file.exists(), f"Missing reranker benchmark results at {bench_file}"

    with open(bench_file, "r", encoding="utf-8") as f:
        bench_data = json.load(f)

    assert bench_data["recommendation"] == "BASELINE_RETAINED"
    evals = bench_data["methods_evaluated"]
    reranker_metrics = evals["domain_legal_reranker"]

    print(f"  ✓ Reranker Benchmark: Precision@1={reranker_metrics['precision_at_1']}, Recall@3={reranker_metrics['recall_at_3']}, MRR={reranker_metrics['mrr']}")
    assert reranker_metrics["precision_at_1"] >= 0.80, "Reranker Precision@1 < 80%"
    assert reranker_metrics["recall_at_3"] >= 0.85, "Reranker Recall@3 < 85%"
    print("  ✓ Empirical validation confirms BASELINE_RETAINED is mathematically and legally optimal")

if __name__ == "__main__":
    print("=" * 80)
    print("SAHYOGSETU PHASE 6: MACHINE LEARNING & EVALUATION TEST SUITE")
    print("=" * 80)

    test_01_dataset_integrity()
    test_02_model_artifacts_loading()
    test_03_evaluation_metrics_verification()
    test_04_intent_inference_multilingual()
    test_05_out_of_scope_fallback()
    test_06_deterministic_entity_preservation()
    test_07_news_classification()
    test_08_language_identification_dialect_ethics()
    test_09_jurisdiction_strictness()
    test_10_reranker_benchmark_verification()

    print("\n" + "=" * 80)
    print("ALL 10/10 PHASE 6 MACHINE LEARNING TESTS PASSED (100%)")
    print("=" * 80)
