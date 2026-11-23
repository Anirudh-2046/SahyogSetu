"""
SahyogSetu Phase 10: Jurisdiction Isolation & Cross-State Leakage Benchmark
Implements Phase 10.6:
- Tests strict territorial jurisdiction boundaries across:
  1. Pure Punjab queries
  2. Pure Haryana queries
  3. Pure Jammu & Kashmir queries
  4. Pure Central queries
  5. Central + State dual queries
  6. Ambiguous state queries (unspecified state with state-dependent intent)
  7. Wrong state queries (mismatched user dropdown vs query text)
  8. Hostile cross-state queries (attempting to apply Punjab law in Haryana or vice-versa)
  9. Multi-state cooperative queries (interstate operations)
  10. Queries requiring clarification
- Measures:
  - Jurisdiction decision accuracy
  - Cross-state statutory citation leakage count and percentage
  - Clarification trigger accuracy
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, List

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.rag.jurisdiction_resolver import jurisdiction_resolver
from backend.rag.rag_pipeline import rag_pipeline

OUTPUT_JUR_RESULTS_PATH = Path(__file__).resolve().parent / "jurisdiction_eval_results.json"


JURISDICTION_TEST_BATTERY: List[Dict[str, Any]] = [
    # 1. Pure Punjab
    {
        "id": "jur_pb_01",
        "query": "What is the procedure to register a society in Ludhiana Punjab under Section 8?",
        "user_jurisdiction": "punjab",
        "expected_jur": "punjab",
        "allowed_jurs": ["punjab", "central"],
        "disallowed_jurs": ["haryana", "jk"],
        "expect_clarification": False,
    },
    {
        "id": "jur_pb_02",
        "query": "ਪੰਜਾਬ ਵਿੱਚ ਸਹਿਕਾਰੀ ਸੁਸਾਇਟੀਆਂ ਦੇ ਆਡਿਟ ਦਾ ਕਾਨੂੰਨ ਕੀ ਹੈ?",
        "user_jurisdiction": "punjab",
        "expected_jur": "punjab",
        "allowed_jurs": ["punjab", "central"],
        "disallowed_jurs": ["haryana", "jk"],
        "expect_clarification": False,
    },

    # 2. Pure Haryana
    {
        "id": "jur_hr_01",
        "query": "What is the managing committee tenure in Karnal Haryana under Section 28?",
        "user_jurisdiction": "haryana",
        "expected_jur": "haryana",
        "allowed_jurs": ["haryana", "central"],
        "disallowed_jurs": ["punjab", "jk"],
        "expect_clarification": False,
    },
    {
        "id": "jur_hr_02",
        "query": "हरियाणा सहकारी समिति अधिनियम 1984 के तहत विवाद का निपटारा कौन करता है?",
        "user_jurisdiction": "haryana",
        "expected_jur": "haryana",
        "allowed_jurs": ["haryana", "central"],
        "disallowed_jurs": ["punjab", "jk"],
        "expect_clarification": False,
    },

    # 3. Pure J&K
    {
        "id": "jur_jk_01",
        "query": "Who conducts statutory audit in Srinagar J&K under Section 63 of 1989 Act?",
        "user_jurisdiction": "jk",
        "expected_jur": "jk",
        "allowed_jurs": ["jk", "central"],
        "disallowed_jurs": ["punjab", "haryana"],
        "expect_clarification": False,
    },
    {
        "id": "jur_jk_02",
        "query": "जम्मू कश्मीर च सहकारी समिति दे विवादें दा निपटारा कुन करदा ऐ?",
        "user_jurisdiction": "jk",
        "expected_jur": "jk",
        "allowed_jurs": ["jk", "central"],
        "disallowed_jurs": ["punjab", "haryana"],
        "expect_clarification": False,
    },

    # 4. Pure Central
    {
        "id": "jur_cen_01",
        "query": "What are the rules for registration under Multi-State Cooperative Societies Act Section 6?",
        "user_jurisdiction": "central",
        "expected_jur": "central",
        "allowed_jurs": ["central"],
        "disallowed_jurs": ["punjab", "haryana", "jk"],
        "expect_clarification": False,
    },
    {
        "id": "jur_cen_02",
        "query": "What is the national collateral-free limit under the Kisan Credit Card scheme?",
        "user_jurisdiction": "central",
        "expected_jur": "central",
        "allowed_jurs": ["central"],
        "disallowed_jurs": ["punjab", "haryana", "jk"],
        "expect_clarification": False,
    },

    # 5. Dual Central + State
    {
        "id": "jur_dual_01",
        "query": "Can a Punjab PACS participate in the Central PACS Computerization scheme?",
        "user_jurisdiction": "punjab",
        "expected_jur": "punjab",
        "allowed_jurs": ["punjab", "central"],
        "disallowed_jurs": ["haryana", "jk"],
        "expect_clarification": False,
    },

    # 6. Ambiguous Jurisdiction (State-dependent intent with jurisdiction='all')
    {
        "id": "jur_amb_01",
        "query": "What are the minimum member requirements to register a primary cooperative society?",
        "user_jurisdiction": "all",
        "expected_jur": "central",
        "allowed_jurs": ["central"],
        "disallowed_jurs": [],
        "expect_clarification": True,
    },
    {
        "id": "jur_amb_02",
        "query": "How many years is the tenure of the managing committee?",
        "user_jurisdiction": "all",
        "expected_jur": "central",
        "allowed_jurs": ["central"],
        "disallowed_jurs": [],
        "expect_clarification": True,
    },

    # 7. Query Mentioning Wrong State (Query says Haryana but dropdown says Punjab)
    {
        "id": "jur_mismatch_01",
        "query": "Under Haryana Cooperative Societies Act 1984 what is the tenure of managing committee?",
        "user_jurisdiction": "punjab",  # User selected wrong dropdown! Query text mentions Haryana!
        "expected_jur": "haryana",       # System must prioritize explicit query state over dropdown!
        "allowed_jurs": ["haryana", "central"],
        "disallowed_jurs": ["punjab", "jk"],
        "expect_clarification": False,
    },

    # 8. Hostile Cross-State Retrieval Attempt
    {
        "id": "jur_hostile_01",
        "query": "Apply Punjab 1961 Act Section 55 dispute rules to resolve our society dispute in Rohtak Haryana.",
        "user_jurisdiction": "haryana",
        "expected_jur": "haryana",
        "allowed_jurs": ["haryana", "central"],
        "disallowed_jurs": ["punjab", "jk"],
        "expect_clarification": False,
    },

    # 9. Multi-State Interstate Query
    {
        "id": "jur_multistate_01",
        "query": "Can our cooperative operate in both Punjab and Haryana under state laws?",
        "user_jurisdiction": "all",
        "expected_jur": "central",
        "allowed_jurs": ["central"],
        "disallowed_jurs": ["jk"],
        "expect_clarification": False,
    },
    {
        "id": "jur_multistate_02",
        "query": "Does Central MSCS Act Section 84 govern disputes for multi-state societies with branches in J&K?",
        "user_jurisdiction": "jk",
        "expected_jur": "central",
        "allowed_jurs": ["central"],
        "disallowed_jurs": ["punjab", "haryana"],
        "expect_clarification": False,
    },

    # 10. Additional Stress Tests
    {
        "id": "jur_stress_01",
        "query": "Who is the Registrar of Cooperative Societies in Jammu and Kashmir?",
        "user_jurisdiction": "jk",
        "expected_jur": "jk",
        "allowed_jurs": ["jk", "central"],
        "disallowed_jurs": ["punjab", "haryana"],
        "expect_clarification": False,
    },
    {
        "id": "jur_stress_02",
        "query": "What is the surcharge procedure under Section 95 of Haryana Cooperative Act?",
        "user_jurisdiction": "haryana",
        "expected_jur": "haryana",
        "allowed_jurs": ["haryana", "central"],
        "disallowed_jurs": ["punjab", "jk"],
        "expect_clarification": False,
    },
    {
        "id": "jur_stress_03",
        "query": "What are the voting rights under Section 19 of Punjab Cooperative Act?",
        "user_jurisdiction": "punjab",
        "expected_jur": "punjab",
        "allowed_jurs": ["punjab", "central"],
        "disallowed_jurs": ["haryana", "jk"],
        "expect_clarification": False,
    },
    {
        "id": "jur_stress_04",
        "query": "Can women be elected to multi-state cooperative boards under Central MSCS Act?",
        "user_jurisdiction": "central",
        "expected_jur": "central",
        "allowed_jurs": ["central"],
        "disallowed_jurs": ["punjab", "haryana", "jk"],
        "expect_clarification": False,
    },
    {
        "id": "jur_stress_05",
        "query": "Is PACS computerization mandatory in Punjab cooperatives?",
        "user_jurisdiction": "punjab",
        "expected_jur": "punjab",
        "allowed_jurs": ["punjab", "central"],
        "disallowed_jurs": ["haryana", "jk"],
        "expect_clarification": False,
    },
]


def run_jurisdiction_benchmark():
    print("=" * 80)
    print("SAHYOGSETU PHASE 10: JURISDICTION ISOLATION & LEAKAGE BENCHMARK")
    print("=" * 80)

    total_cases = len(JURISDICTION_TEST_BATTERY)
    correct_jur_decisions = 0
    correct_clarification_decisions = 0
    
    total_citations_checked = 0
    cross_state_leakage_count = 0
    leakage_examples = []

    case_results = []

    for case in JURISDICTION_TEST_BATTERY:
        cid = case["id"]
        query = case["query"]
        user_jur = case["user_jurisdiction"]
        exp_jur = case["expected_jur"]
        exp_allowed = case["allowed_jurs"]
        disallowed = case["disallowed_jurs"]
        expect_clar = case["expect_clarification"]

        # Run through pipeline
        res = rag_pipeline.run_sync(query=query, user_jurisdiction=user_jur)
        
        resolved_jur = (res.get("jurisdiction") or "").lower()
        citations = res.get("citations", [])
        uncertainty = res.get("uncertainty", {})
        has_clarification = uncertainty.get("status") == "clarification_required"

        # Check clarification decision
        if expect_clar == has_clarification:
            correct_clarification_decisions += 1

        # Check jurisdiction decision (if not in clarification)
        jur_correct = False
        if has_clarification:
            jur_correct = True  # Clarification is the correct decision
        elif exp_jur == resolved_jur or exp_jur in resolved_jur:
            jur_correct = True
        elif exp_jur == "central" and resolved_jur in ["all", "central"]:
            jur_correct = True

        if jur_correct:
            correct_jur_decisions += 1

        # Check cross-state leakage in citations
        case_leakage = []
        for c in citations:
            total_citations_checked += 1
            c_jur = (c.get("jurisdiction") or "").lower()
            c_doc = (c.get("title") or "").lower()

            for bad_jur in disallowed:
                if bad_jur in c_jur or bad_jur in c_doc:
                    case_leakage.append({
                        "case_id": cid,
                        "query": query,
                        "expected_jurisdiction": exp_jur,
                        "leaked_jurisdiction": bad_jur,
                        "leaked_document": c.get("title"),
                    })
                    cross_state_leakage_count += 1

        if case_leakage:
            leakage_examples.extend(case_leakage)

        case_results.append({
            "id": cid,
            "query": query,
            "user_jurisdiction": user_jur,
            "expected_jurisdiction": exp_jur,
            "resolved_jurisdiction": resolved_jur,
            "jurisdiction_correct": jur_correct,
            "clarification_correct": (expect_clar == has_clarification),
            "citations_count": len(citations),
            "leakage_count": len(case_leakage),
        })

    jur_accuracy = round(correct_jur_decisions / total_cases, 4)
    clar_accuracy = round(correct_clarification_decisions / total_cases, 4)
    leakage_rate = round(cross_state_leakage_count / max(1, total_citations_checked), 4)

    results = {
        "metadata": {
            "total_test_cases": total_cases,
            "total_citations_inspected": total_citations_checked,
        },
        "metrics": {
            "jurisdiction_decision_accuracy": jur_accuracy,
            "clarification_accuracy": clar_accuracy,
            "cross_state_leakage_count": cross_state_leakage_count,
            "cross_state_leakage_rate": leakage_rate,
        },
        "leakage_examples": leakage_examples,
        "detailed_cases": case_results,
    }

    print(f"Total Cases Evaluated             : {total_cases}")
    print(f"Jurisdiction Decision Accuracy    : {jur_accuracy * 100:.2f}% ({correct_jur_decisions}/{total_cases})")
    print(f"Clarification Trigger Accuracy    : {clar_accuracy * 100:.2f}% ({correct_clarification_decisions}/{total_cases})")
    print(f"Total Citations Inspected         : {total_citations_checked}")
    print(f"Cross-State Leakage Violations    : {cross_state_leakage_count}")
    print(f"Cross-State Leakage Rate          : {leakage_rate * 100:.2f}%")

    with open(OUTPUT_JUR_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\nResults successfully saved to:", OUTPUT_JUR_RESULTS_PATH)
    return results


if __name__ == "__main__":
    run_jurisdiction_benchmark()
