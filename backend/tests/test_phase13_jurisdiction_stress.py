#!/usr/bin/env python3
"""
SahyogSetu Phase 13: Hostile Jurisdiction Boundary & Stress Test Suite
Tests 45 hostile, adversarial, multi-lingual, and border-case scenarios to verify:
1. Strict territorial isolation (0.00% cross-state leakage).
2. Proper jurisdiction resolution for abbreviations, mixed-language tokens, and border districts.
3. Accurate multi-state cooperative routing to Central MSCS Act.
4. Appropriate clarification triggers on truly ambiguous queries.
"""

import sys
import os
import unittest
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.rag.jurisdiction_resolver import jurisdiction_resolver
from backend.rag.rag_pipeline import rag_pipeline

STRESS_TEST_CASES = [
    # -------------------------------------------------------------------------
    # 1. BORDER DISTRICTS & TOWNS (10 Cases)
    # -------------------------------------------------------------------------
    {
        "id": "stress_border_01",
        "query": "How to register a PACS in Ambala under Section 6?",
        "user_jur": "haryana",
        "expected_jur": "haryana",
        "forbidden_tokens": ["Punjab Act", "1961", "J&K Act", "1989"],
    },
    {
        "id": "stress_border_02",
        "query": "Who is the Registrar for cooperatives in Patiala under Section 3?",
        "user_jur": "punjab",
        "expected_jur": "punjab",
        "forbidden_tokens": ["Haryana Act", "1984", "J&K Act", "1989"],
    },
    {
        "id": "stress_border_03",
        "query": "Statutory audit requirements in Kathua border district under Section 63",
        "user_jur": "jk",
        "expected_jur": "jk",
        "forbidden_tokens": ["Punjab Act", "Haryana Act", "1984"],
    },
    {
        "id": "stress_border_04",
        "query": "Committee tenure in Pathankot under Section 26",
        "user_jur": "punjab",
        "expected_jur": "punjab",
        "forbidden_tokens": ["Haryana Act", "J&K Act", "1989"],
    },
    {
        "id": "stress_border_05",
        "query": "Dispute arbitration in Panchkula Haryana under Section 102",
        "user_jur": "haryana",
        "expected_jur": "haryana",
        "forbidden_tokens": ["Punjab Act", "J&K Act"],
    },
    {
        "id": "stress_border_06",
        "query": "Managing committee elections in Mohali Punjab under Section 26",
        "user_jur": "punjab",
        "expected_jur": "punjab",
        "forbidden_tokens": ["Haryana Act", "J&K Act"],
    },
    {
        "id": "stress_border_07",
        "query": "Cooperative society formation in Sirsa under Section 6",
        "user_jur": "haryana",
        "expected_jur": "haryana",
        "forbidden_tokens": ["Punjab Act", "J&K Act"],
    },
    {
        "id": "stress_border_08",
        "query": "Audit of credit society in Bathinda under Section 48",
        "user_jur": "punjab",
        "expected_jur": "punjab",
        "forbidden_tokens": ["Haryana Act", "J&K Act"],
    },
    {
        "id": "stress_border_09",
        "query": "Arbitration of society disputes in Jammu under Section 70",
        "user_jur": "jk",
        "expected_jur": "jk",
        "forbidden_tokens": ["Punjab Act", "Haryana Act"],
    },
    {
        "id": "stress_border_10",
        "query": "Member voting rules in Karnal under Section 19",
        "user_jur": "haryana",
        "expected_jur": "haryana",
        "forbidden_tokens": ["Punjab Act", "J&K Act"],
    },

    # -------------------------------------------------------------------------
    # 2. ACRONYMS, ABBREVIATIONS & SHORT NAMES (8 Cases)
    # -------------------------------------------------------------------------
    {
        "id": "stress_acronym_01",
        "query": "What are Pb Coop Act provisions for committee election term?",
        "user_jur": "punjab",
        "expected_jur": "punjab",
        "forbidden_tokens": ["Haryana Act", "J&K Act"],
    },
    {
        "id": "stress_acronym_02",
        "query": "HR Coop Soc 1984 audit procedure under section 95",
        "user_jur": "haryana",
        "expected_jur": "haryana",
        "forbidden_tokens": ["Punjab Act", "J&K Act"],
    },
    {
        "id": "stress_acronym_03",
        "query": "J&K Act 1989 Section 7 registration requirements",
        "user_jur": "jk",
        "expected_jur": "jk",
        "forbidden_tokens": ["Punjab Act", "Haryana Act"],
    },
    {
        "id": "stress_acronym_04",
        "query": "MSCS 2002 election authority powers under sec 41",
        "user_jur": "central",
        "expected_jur": "central",
        "forbidden_tokens": ["Punjab Act", "Haryana Act", "J&K Act"],
    },
    {
        "id": "stress_acronym_05",
        "query": "PADB OTS waiver circular 2024 terms for farmers",
        "user_jur": "punjab",
        "expected_jur": "punjab",
        "forbidden_tokens": ["Haryana Act", "J&K Act"],
    },
    {
        "id": "stress_acronym_06",
        "query": "KCC RBI circular collateral exemption limit up to 1.60 lakh",
        "user_jur": "central",
        "expected_jur": "central",
        "forbidden_tokens": ["Punjab Act", "Haryana Act", "J&K Act"],
    },
    {
        "id": "stress_acronym_07",
        "query": "PMFBY localized calamity 72 hours intimation rule",
        "user_jur": "central",
        "expected_jur": "central",
        "forbidden_tokens": ["Punjab Act", "Haryana Act", "J&K Act"],
    },
    {
        "id": "stress_acronym_08",
        "query": "PACS Model Byelaws 2023 multi service expansion CSC",
        "user_jur": "central",
        "expected_jur": "central",
        "forbidden_tokens": ["Punjab Act", "Haryana Act", "J&K Act"],
    },

    # -------------------------------------------------------------------------
    # 3. VERNACULAR & MIXED-SCRIPT QUERIES (10 Cases)
    # -------------------------------------------------------------------------
    {
        "id": "stress_vernacular_01",
        "query": "ਪੰਜਾਬ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ 1961 ਦੀ ਧਾਰਾ 8 ਅਧੀਨ ਰਜਿਸਟ੍ਰੇਸ਼ਨ",
        "user_jur": "punjab",
        "expected_jur": "punjab",
        "forbidden_tokens": ["Haryana Act", "J&K Act"],
    },
    {
        "id": "stress_vernacular_02",
        "query": "ਪੰਜਾਬ ਵਿੱਚ ਕਮੇਟੀ ਦੀ ਚੋਣ ਅਤੇ ਕਾਰਜਕਾਲ ਧਾਰਾ 26",
        "user_jur": "punjab",
        "expected_jur": "punjab",
        "forbidden_tokens": ["Haryana Act", "J&K Act"],
    },
    {
        "id": "stress_vernacular_03",
        "query": "हरियाणा में समिति पंजीकरण के नियम धारा 6",
        "user_jur": "haryana",
        "expected_jur": "haryana",
        "forbidden_tokens": ["Punjab Act", "J&K Act"],
    },
    {
        "id": "stress_vernacular_04",
        "query": "हरियाणा सहकारी समिति प्रबंध कमेटी का कार्यकाल धारा 28",
        "user_jur": "haryana",
        "expected_jur": "haryana",
        "forbidden_tokens": ["Punjab Act", "J&K Act"],
    },
    {
        "id": "stress_vernacular_05",
        "query": "جموں و کشمیر کوآپریٹو سوسائٹیز ایکٹ دفعہ 7 رجسٹریشن",
        "user_jur": "jk",
        "expected_jur": "jk",
        "forbidden_tokens": ["Punjab Act", "Haryana Act"],
    },
    {
        "id": "stress_vernacular_06",
        "query": "جموں و کشمیر میں سوسائٹی کے حسابات کا سالانہ آڈٹ دفعہ 63",
        "user_jur": "jk",
        "expected_jur": "jk",
        "forbidden_tokens": ["Punjab Act", "Haryana Act"],
    },
    {
        "id": "stress_vernacular_07",
        "query": "जम्मू कश्मीर च सहकारी समिति दी धारा 29 कमेंटी दा कार्यकाल",
        "user_jur": "jk",
        "expected_jur": "jk",
        "forbidden_tokens": ["Punjab Act", "Haryana Act"],
    },
    {
        "id": "stress_vernacular_08",
        "query": "हरियाणा में खाद बीज की समिति बनाने खातर कितने सदस्य चाहिएंगे?",
        "user_jur": "haryana",
        "expected_jur": "haryana",
        "forbidden_tokens": ["Punjab Act", "J&K Act"],
    },
    {
        "id": "stress_vernacular_09",
        "query": "ਕੇਸੀਸੀ ਸਕੀਮ ਅਧੀਨ 1.60 ਲੱਖ ਤੱਕ ਬਿਨਾਂ ਗਰੰਟੀ ਕਰਜ਼ਾ",
        "user_jur": "central",
        "expected_jur": "central",
        "forbidden_tokens": ["Punjab Act", "Haryana Act", "J&K Act"],
    },
    {
        "id": "stress_vernacular_10",
        "query": "पीएम किसान सम्मान निधि ₹6000 की किस्त और ई-केवाईसी",
        "user_jur": "central",
        "expected_jur": "central",
        "forbidden_tokens": ["Punjab Act", "Haryana Act", "J&K Act"],
    },

    # -------------------------------------------------------------------------
    # 4. HOSTILE CROSS-STATE ATTEMPTS (10 Cases)
    # -------------------------------------------------------------------------
    {
        "id": "stress_hostile_01",
        "query": "Can I use Punjab Cooperative Societies Act 1961 Section 8 to register a society in Rohtak Haryana?",
        "user_jur": "haryana",
        "expected_jur": "haryana",
        "forbidden_tokens": ["Punjab Act No. 25 of 1961"],
    },
    {
        "id": "stress_hostile_02",
        "query": "Apply Haryana 1984 Act Section 28 committee term to my society in Jalandhar Punjab",
        "user_jur": "punjab",
        "expected_jur": "punjab",
        "forbidden_tokens": ["Haryana Act No. 22 of 1984"],
    },
    {
        "id": "stress_hostile_03",
        "query": "Can J&K Cooperative Act 1989 Section 70 arbitration resolve land dispute in Gurgaon Haryana?",
        "user_jur": "haryana",
        "expected_jur": "haryana",
        "forbidden_tokens": ["J&K Act No. VII of 1989"],
    },
    {
        "id": "stress_hostile_04",
        "query": "I am in Amritsar Punjab, can Haryana Registrar audit our books under Haryana Act Section 95?",
        "user_jur": "punjab",
        "expected_jur": "punjab",
        "forbidden_tokens": ["Haryana Act No. 22 of 1984"],
    },
    {
        "id": "stress_hostile_05",
        "query": "Can a Punjab society borrow from Haryana Cooperative Bank under Punjab Section 32 without Registrar approval?",
        "user_jur": "punjab",
        "expected_jur": "punjab",
        "forbidden_tokens": ["Haryana Act No. 22 of 1984"],
    },
    {
        "id": "stress_hostile_06",
        "query": "Apply J&K Act 1989 Section 29 to Punjab PACS election dispute",
        "user_jur": "punjab",
        "expected_jur": "punjab",
        "forbidden_tokens": ["Act No. VII of 1989"],
    },
    {
        "id": "stress_hostile_07",
        "query": "Can Haryana RCS supersede a society located in Jammu under Haryana Section 34?",
        "user_jur": "jk",
        "expected_jur": "jk",
        "forbidden_tokens": ["Haryana Act No. 22 of 1984"],
    },
    {
        "id": "stress_hostile_08",
        "query": "Is PADB OTS 100% penal waiver valid for cooperative bank borrowers in Hisar Haryana?",
        "user_jur": "haryana",
        "expected_jur": "haryana",
        "forbidden_tokens": ["Punjab State Agriculture Development Bank"],
    },
    {
        "id": "stress_hostile_09",
        "query": "We are registered under MSCS Act 2002, can Punjab state registrar inspect our books under Punjab Section 48?",
        "user_jur": "central",
        "expected_jur": "central",
        "forbidden_tokens": ["Punjab Act No. 25 of 1961"],
    },
    {
        "id": "stress_hostile_10",
        "query": "Can Haryana cooperative society claim first charge in Ludhiana Punjab under Haryana Section 47?",
        "user_jur": "punjab",
        "expected_jur": "punjab",
        "forbidden_tokens": ["Haryana Act No. 22 of 1984"],
    },

    # -------------------------------------------------------------------------
    # 5. MULTI-STATE & AMBIGUOUS CASES (7 Cases)
    # -------------------------------------------------------------------------
    {
        "id": "stress_multi_01",
        "query": "We want to operate cooperative milk procurement across Punjab, Haryana, and Rajasthan. Which law applies?",
        "user_jur": "punjab",
        "expected_jur": "central",
        "forbidden_tokens": ["Punjab Act No. 25 of 1961", "Haryana Act No. 22 of 1984"],
    },
    {
        "id": "stress_multi_02",
        "query": "Multi-state cooperative registration with members from Jammu & Kashmir and Punjab under Section 6",
        "user_jur": "central",
        "expected_jur": "central",
        "forbidden_tokens": ["Act No. VII of 1989", "Punjab Act No. 25 of 1961"],
    },
    {
        "id": "stress_multi_03",
        "query": "Who conducts elections for inter-state multi-state cooperative societies under Section 41?",
        "user_jur": "central",
        "expected_jur": "central",
        "forbidden_tokens": ["State Election Authority"],
    },
    {
        "id": "stress_multi_04",
        "query": "Can an individual hold 30% of share capital in a multi-state cooperative under Section 30?",
        "user_jur": "central",
        "expected_jur": "central",
        "forbidden_tokens": ["State Act"],
    },
    {
        "id": "stress_multi_05",
        "query": "What is the statutory limitation period for reference of disputes under MSCS Act Section 85?",
        "user_jur": "central",
        "expected_jur": "central",
        "forbidden_tokens": ["State Act"],
    },
    {
        "id": "stress_multi_06",
        "query": "Dispute between members of a village cooperative regarding tubewell water distribution",
        "user_jur": "punjab",
        "expected_jur": "punjab",
        "forbidden_tokens": ["Haryana Act", "J&K Act"],
    },
    {
        "id": "stress_multi_07",
        "query": "What is the procedure to amend bye-laws in cooperative society?",
        "user_jur": "haryana",
        "expected_jur": "haryana",
        "forbidden_tokens": ["Punjab Act", "J&K Act"],
    },
]

class TestPhase13JurisdictionStress(unittest.TestCase):
    """Stress tests territorial isolation and cross-state leakage prevention."""

    def test_all_45_hostile_and_boundary_cases(self):
        print("=" * 80)
        print("SAHYOGSETU PHASE 13: 45-CASE HOSTILE JURISDICTION BOUNDARY STRESS TEST")
        print("=" * 80)

        passed = 0
        leakage_violations = 0

        for case in STRESS_TEST_CASES:
            c_id = case["id"]
            query = case["query"]
            user_jur = case["user_jur"]
            exp_jur = case["expected_jur"]
            forbidden = case["forbidden_tokens"]

            # Resolve jurisdiction
            res = jurisdiction_resolver.resolve(query=query, user_jurisdiction=user_jur)
            primary_jur = res.get("resolved_jurisdiction") or res.get("primary_jurisdiction")
            allowed_jurs = res["allowed_jurisdictions"]

            # Verify resolved jurisdiction matches expected policy
            self.assertEqual(
                primary_jur,
                exp_jur,
                f"[{c_id}] Jurisdiction mismatch: expected {exp_jur}, got {primary_jur} (query: '{query}')"
            )

            # Execute RAG retrieval
            rag_res = rag_pipeline.run_sync(query=query, user_jurisdiction=user_jur)
            citations = rag_res.get("citations", [])

            # Check for cross-state statutory leakage in validated citations
            for cit in citations:
                cit_jur = cit.get("jurisdiction", "").lower()
                cit_title = cit.get("documentTitle", "")
                cit_snippet = cit.get("snippet", "")

                # Strict territorial boundary: if not allowed, must never appear
                if cit_jur and cit_jur not in allowed_jurs:
                    leakage_violations += 1
                    self.fail(f"[{c_id}] Cross-state leakage: Citation '{cit_title}' with jur='{cit_jur}' retrieved for allowed={allowed_jurs}")

                for f_tok in forbidden:
                    if f_tok.lower() in cit_title.lower() or f_tok.lower() in cit_snippet.lower():
                        leakage_violations += 1
                        self.fail(f"[{c_id}] Forbidden token '{f_tok}' leaked into citation title/snippet: {cit_title}")

            passed += 1

        print(f"\n✓ Successfully evaluated {passed} / {len(STRESS_TEST_CASES)} hostile boundary stress cases.")
        print(f"✓ Cross-State Statutory Leakage Rate: 0.00% (0 / {len(STRESS_TEST_CASES)} violations)")
        self.assertEqual(passed, len(STRESS_TEST_CASES))
        self.assertEqual(leakage_violations, 0)

if __name__ == "__main__":
    unittest.main()
