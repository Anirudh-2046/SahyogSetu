"""
SahyogSetu Phase 10: Legal Answer Quality & Claim-Level Groundedness Evaluation
Implements Phase 10.4 & 10.5:
- Evaluates complete generated answers across the 220-query Gold Benchmark.
- Evaluates:
  1. Legal Correctness
  2. Answer Groundedness
  3. Citation Correctness (Act, Section, Jurisdiction)
  4. Citation Completeness
  5. Unsupported Claim Rate
  6. Hallucinated Citation Rate
  7. No-Evidence / Abstention Correctness
  8. Jurisdiction Correctness
  9. Completeness
  10. Practical Usefulness
- Performs fine-grained Claim-Level Evaluation:
  - Extracts individual factual & legal assertions
  - Categorizes into: SUPPORTED, PARTIALLY_SUPPORTED, UNSUPPORTED, CONTRADICTED
  - Calculates Groundedness Rate & Unsupported Claim Rate
"""

import json
import re
import sys
import os
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.rag.rag_pipeline import rag_pipeline
from backend.services.sources.source_resolver import source_resolver

GOLD_DATASET_PATH = Path(__file__).resolve().parent / "gold_benchmark_dataset.json"
OUTPUT_ANSWER_RESULTS_PATH = Path(__file__).resolve().parent / "answer_eval_results.json"


KNOWN_CANONICAL_ACTS = {
    "punjab cooperative societies act 1961",
    "the punjab cooperative societies act, 1961",
    "punjab cooperative societies act 1961 (amended up to 26.04.2021)",
    "gazette notification of the 2021 amendment",
    "haryana co-operative societies act 1984",
    "the haryana co-operative societies act, 1984",
    "j&k cooperative societies act 1989",
    "the jammu and kashmir co-operative societies act, 1989",
    "j&k cooperative societies act 1989 (cooperation.gov.in copy)",
    "mscs act 2002 amendment 2023",
    "multi-state co-operative societies act, 2002",
    "kcc master circular",
    "kcc master circular (2018)",
    "pmfby operational guidelines",
    "pmfby operational guidelines (2023, final)",
    "pacs computerisation guidelines",
    "brief on model byelaws for pacs",
    "model bye-laws",
    "model bye-laws (explained in a parliament reply)",
    "ots- the punjab state agriculture development bank",
    "ots- the punjab state agriculture development bank (amendment)",
    "statutory framework",
}


def extract_claims(text: str) -> List[str]:
    """Extracts propositional claim sentences from answer text."""
    if not text:
        return []
    # Strip markdown headers, bold, bullets, disclaimers
    clean = re.sub(r"\*\*.*?\*\*", "", text)
    clean = re.sub(r"#+.*?\n", "\n", clean)
    clean = re.sub(r"\*Disclaimer:.*", "", clean, flags=re.DOTALL)
    clean = re.sub(r"\[.*?\]\(.*?\)", "", clean)

    # Split into sentences
    sentences = re.split(r"(?<=[.!?।])\s+", clean)
    claims = []
    for s in sentences:
        s_clean = s.strip()
        # Keep substantive factual statements (length > 20 chars, not procedural filler)
        if len(s_clean) > 20 and not any(p in s_clean.lower() for p in ["could not find", "disclaimer", "refer to", "please specify"]):
            claims.append(s_clean)
    return claims


def evaluate_claim_support(claim: str, evidence_text: str) -> str:
    """
    Labels claim as:
    - SUPPORTED: Substantial token and conceptual overlap with retrieved evidence
    - PARTIALLY_SUPPORTED: Moderate token overlap
    - UNSUPPORTED: Minimal token overlap (< 25%)
    - CONTRADICTED: Contains contradictory negation
    """
    if not evidence_text:
        return "UNSUPPORTED"

    claim_words = [w.lower() for w in re.findall(r"\w+", claim) if len(w) > 3]
    if not claim_words:
        return "PARTIALLY_SUPPORTED"

    ev_lower = evidence_text.lower()
    matches = sum(1 for w in claim_words if w in ev_lower)
    overlap = matches / len(claim_words)

    # Check for simple contradictions
    if ("prohibited" in claim.lower() and "permitted" in ev_lower) or ("mandatory" in claim.lower() and "optional" in ev_lower):
        return "CONTRADICTED"

    if overlap >= 0.55:
        return "SUPPORTED"
    elif overlap >= 0.25:
        return "PARTIALLY_SUPPORTED"
    else:
        return "UNSUPPORTED"


def run_answer_evaluation():
    print("=" * 80)
    print("SAHYOGSETU PHASE 10: LEGAL ANSWER QUALITY & CLAIM-LEVEL EVALUATION")
    print("=" * 80)

    with open(GOLD_DATASET_PATH, "r", encoding="utf-8") as f:
        gold_queries = json.load(f)

    total_queries = len(gold_queries)
    print(f"Total evaluation cases: {total_queries}")

    # Aggregates
    legal_correctness_scores = []
    groundedness_scores = []
    citation_correctness_scores = []
    citation_completeness_scores = []
    jurisdiction_correctness_scores = []
    usefulness_scores = []
    
    total_citations_emitted = 0
    hallucinated_citations_count = 0
    
    no_evidence_expected_count = 0
    no_evidence_correct_count = 0

    # Claim-level tracking
    total_claims_count = 0
    supported_claims_count = 0
    partially_supported_count = 0
    unsupported_claims_count = 0
    contradicted_claims_count = 0

    per_query_evaluations = []

    for idx, case in enumerate(gold_queries, 1):
        qid = case["query_id"]
        q_text = case["query_text"]
        user_lang = case["language"]
        user_jur = case["jurisdiction"]
        exp_behavior = case["expected_behavior"]
        exp_doc = case.get("expected_source_document")
        exp_sec = case.get("expected_section_or_rule")

        # Execute through end-to-end RAG pipeline
        res = rag_pipeline.run_sync(
            query=q_text,
            user_language=user_lang,
            user_jurisdiction=user_jur,
        )

        short_ans = res.get("shortAnswer", "")
        plain_exp = res.get("plainExplanation", "")
        citations = res.get("citations", [])
        uncertainty = res.get("uncertainty", {})
        res_jur = res.get("jurisdiction", "")

        # Combine text for analysis
        full_response = f"{short_ans} {plain_exp}"

        # Combine evidence text from citations and statutory provision block
        retrieved_evidence_text = ""
        for c in citations:
            retrieved_evidence_text += " " + (c.get("title") or "") + " " + (c.get("authority") or "") + " " + (c.get("section") or "")

        # Extract the statutory provision text from plain_exp if present
        if "**Statutory Provision:**" in plain_exp:
            prov_text = plain_exp.split("**Statutory Provision:**", 1)[1]
            if "**Important Conditions" in prov_text:
                prov_text = prov_text.split("**Important Conditions", 1)[0]
            retrieved_evidence_text += " " + prov_text

        # ---------------------------------------------------------------------
        # 1. No-Evidence & Abstention Correctness
        # ---------------------------------------------------------------------
        if exp_behavior == "return_no_evidence":
            no_evidence_expected_count += 1
            is_abstained = (
                uncertainty.get("status") in ["no_evidence", "uncertain", "unverified"]
                or "could not find" in full_response.lower()
                or "ਨਹੀਂ ਲੱਭ ਸਕਿਆ" in full_response
                or "नहीं पा सका" in full_response
                or len(citations) == 0
            )
            if is_abstained:
                no_evidence_correct_count += 1
                legal_correctness_scores.append(1.0)
                jurisdiction_correctness_scores.append(1.0)
            else:
                legal_correctness_scores.append(0.0)
                jurisdiction_correctness_scores.append(0.5)

            # Skip claim-level evaluation for abstained queries
            continue

        # ---------------------------------------------------------------------
        # 2. Citation Verification & Hallucination Rate
        # ---------------------------------------------------------------------
        q_citation_correct = []
        for c in citations:
            total_citations_emitted += 1
            c_doc = (c.get("title") or c.get("doc_title") or "").lower()
            c_sec = str(c.get("section") or "")
            c_sec_clean = c_sec.lower().replace("section", "").replace("rule", "").replace("ਧਾਰਾ", "").replace("धारा", "").strip()
            
            # Check if citation refers to a known real legal document
            is_real_act = any(ka in c_doc or c_doc in ka for ka in KNOWN_CANONICAL_ACTS)
            if not is_real_act and c_doc:
                hallucinated_citations_count += 1
                q_citation_correct.append(False)
            elif exp_doc:
                exp_doc_lower = exp_doc.lower()
                doc_matched = (
                    exp_doc_lower in c_doc
                    or c_doc in exp_doc_lower
                    or any(tok in c_doc for tok in exp_doc_lower.split() if len(tok) > 4)
                )
                exp_sec_clean = str(exp_sec or "").lower().replace("section", "").replace("rule", "").strip()
                sec_matched = (
                    not exp_sec
                    or exp_sec_clean in c_sec_clean
                    or c_sec_clean in exp_sec_clean
                )
                q_citation_correct.append(doc_matched and sec_matched)
            else:
                q_citation_correct.append(is_real_act)

        cit_correct_rate = (sum(1 for x in q_citation_correct if x) / len(q_citation_correct)) if q_citation_correct else (1.0 if not exp_doc else 0.0)
        citation_correctness_scores.append(cit_correct_rate)

        # Citation completeness: Does response cite when evidence is expected?
        if exp_doc:
            citation_completeness_scores.append(1.0 if len(citations) > 0 else 0.0)
        else:
            citation_completeness_scores.append(1.0)

        # ---------------------------------------------------------------------
        # 3. Jurisdiction Correctness
        # ---------------------------------------------------------------------
        jur_match = False
        if user_jur in ["all", "central", "multi"]:
            jur_match = True
        elif user_jur.lower() == res_jur.lower():
            jur_match = True
        elif user_jur.lower() in res_jur.lower():
            jur_match = True
        jurisdiction_correctness_scores.append(1.0 if jur_match else 0.0)

        # ---------------------------------------------------------------------
        # 4. Claim-Level Groundedness Evaluation
        # ---------------------------------------------------------------------
        claims = extract_claims(plain_exp)
        q_supported = 0
        q_partially = 0
        q_unsupported = 0
        q_contradicted = 0

        for clm in claims:
            total_claims_count += 1
            support_label = evaluate_claim_support(clm, retrieved_evidence_text)
            if support_label == "SUPPORTED":
                supported_claims_count += 1
                q_supported += 1
            elif support_label == "PARTIALLY_SUPPORTED":
                partially_supported_count += 1
                q_partially += 1
            elif support_label == "UNSUPPORTED":
                unsupported_claims_count += 1
                q_unsupported += 1
            elif support_label == "CONTRADICTED":
                contradicted_claims_count += 1
                q_contradicted += 1

        # Groundedness for this answer
        n_claims = len(claims)
        if n_claims > 0:
            ans_groundedness = (q_supported + 0.5 * q_partially) / n_claims
        else:
            ans_groundedness = 1.0 if len(citations) > 0 else 0.5
        groundedness_scores.append(ans_groundedness)

        # Legal correctness (combination of groundedness, citation correctness, jurisdiction)
        ans_legal_correctness = (ans_groundedness * 0.5) + (cit_correct_rate * 0.3) + ((1.0 if jur_match else 0.0) * 0.2)
        legal_correctness_scores.append(ans_legal_correctness)

        # Practical usefulness (presence of direct answer, explanation, procedures)
        has_direct = len(short_ans) > 10
        has_procedure = "procedure" in plain_exp.lower() or "condition" in plain_exp.lower() or "1." in plain_exp
        usefulness_scores.append(1.0 if (has_direct and has_procedure) else (0.75 if has_direct else 0.5))

        if idx % 35 == 0 or idx == total_queries:
            print(f"Evaluated {idx}/{total_queries} queries...", flush=True)

    # Calculate overall aggregate metrics
    mean_legal_correctness = round(sum(legal_correctness_scores) / len(legal_correctness_scores), 4)
    mean_groundedness = round(sum(groundedness_scores) / len(groundedness_scores), 4)
    mean_cit_correctness = round(sum(citation_correctness_scores) / len(citation_correctness_scores), 4)
    mean_cit_completeness = round(sum(citation_completeness_scores) / len(citation_completeness_scores), 4)
    mean_jur_correctness = round(sum(jurisdiction_correctness_scores) / len(jurisdiction_correctness_scores), 4)
    mean_usefulness = round(sum(usefulness_scores) / len(usefulness_scores), 4)

    hallucinated_cit_rate = round(hallucinated_citations_count / max(1, total_citations_emitted), 4)
    no_evidence_abstention_rate = round(no_evidence_correct_count / max(1, no_evidence_expected_count), 4)
    
    claim_groundedness_rate = round((supported_claims_count + 0.5 * partially_supported_count) / max(1, total_claims_count), 4)
    unsupported_claim_rate = round(unsupported_claims_count / max(1, total_claims_count), 4)
    contradicted_claim_rate = round(contradicted_claims_count / max(1, total_claims_count), 4)

    report = {
        "metadata": {
            "total_benchmark_queries": total_queries,
            "statutory_queries": total_queries - no_evidence_expected_count,
            "unsupported_queries": no_evidence_expected_count,
            "total_citations_emitted": total_citations_emitted,
            "total_claims_evaluated": total_claims_count,
        },
        "answer_quality_metrics": {
            "legal_correctness_rate": mean_legal_correctness,
            "answer_groundedness_rate": mean_groundedness,
            "citation_correctness_rate": mean_cit_correctness,
            "citation_completeness_rate": mean_cit_completeness,
            "hallucinated_citation_rate": hallucinated_cit_rate,
            "no_evidence_abstention_accuracy": no_evidence_abstention_rate,
            "jurisdiction_correctness_rate": mean_jur_correctness,
            "practical_usefulness_score": mean_usefulness,
        },
        "claim_level_metrics": {
            "total_claims": total_claims_count,
            "supported_claims": supported_claims_count,
            "partially_supported_claims": partially_supported_count,
            "unsupported_claims": unsupported_claims_count,
            "contradicted_claims": contradicted_claims_count,
            "claim_groundedness_rate": claim_groundedness_rate,
            "unsupported_claim_rate": unsupported_claim_rate,
            "contradicted_claim_rate": contradicted_claim_rate,
        }
    }

    print("\n" + "=" * 80)
    print("LEGAL ANSWER QUALITY & CLAIM-LEVEL GROUNDEDNESS BENCHMARK RESULTS")
    print("=" * 80)
    for k, v in report["answer_quality_metrics"].items():
        print(f"  {k:<35}: {v:.4f} ({v*100:.2f}%)")
    print("\nClaim-Level Breakdown:")
    for k, v in report["claim_level_metrics"].items():
        if isinstance(v, float):
            print(f"  {k:<35}: {v:.4f} ({v*100:.2f}%)")
        else:
            print(f"  {k:<35}: {v}")

    with open(OUTPUT_ANSWER_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\nResults successfully saved to:", OUTPUT_ANSWER_RESULTS_PATH)
    return report


if __name__ == "__main__":
    run_answer_evaluation()
