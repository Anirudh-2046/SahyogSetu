#!/usr/bin/env python3
"""
SahyogSetu Phase 13: Dataset Generator for Development & Validation Partitions
Generates strictly independent Development (N=60) and Validation (N=40) benchmark datasets.
Maintains 100% isolation from the protected Phase 10/12 Gold Benchmark (N=220) to prevent train/test leakage.
"""

import json
import os
from pathlib import Path

OUTPUT_DIR = Path("backend") / "evaluation" / "phase13"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DEV_CASES = [
    # -------------------------------------------------------------------------
    # CENTRAL JURISDICTION - DEV CASES (15)
    # -------------------------------------------------------------------------
    {
        "id": "dev_central_001",
        "query_text": "What is the minimum member requirement for registering a multi-state cooperative society across states?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "MSCS Act 2002 Amendment 2023",
        "expected_section_or_rule": "6",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "at least fifty persons from each of the state"
    },
    {
        "id": "dev_central_002",
        "query_text": "How long is the tenure of the board of a multi-state cooperative under MSCS Act Section 45?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "MSCS Act 2002 Amendment 2023",
        "expected_section_or_rule": "45",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "tenure of the elected members of the board shall be five years"
    },
    {
        "id": "dev_central_003",
        "query_text": "Who conducts elections for multi-state cooperative societies under MSCS Act 2023?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "MSCS Act 2002 Amendment 2023",
        "expected_section_or_rule": "41",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "Co-operative Election Authority"
    },
    {
        "id": "dev_central_004",
        "query_text": "Can a member exercise voting rights without paying dues under MSCS Act Section 19?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "MSCS Act 2002 Amendment 2023",
        "expected_section_or_rule": "19",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "No member of a multi-state co-operative society shall exercise the rights of a member unless he has made such payments"
    },
    {
        "id": "dev_central_005",
        "query_text": "Where should internal disputes of a multi-state society be referred according to Section 84?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Dispute Resolution",
        "difficulty": "Medium",
        "expected_source_document": "MSCS Act 2002 Amendment 2023",
        "expected_section_or_rule": "84",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "dispute shall be referred to arbitration"
    },
    {
        "id": "dev_central_006",
        "query_text": "What is the statutory limitation period for referring disputes under Section 85 of MSCS Act?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Dispute Resolution",
        "difficulty": "Hard",
        "expected_source_document": "MSCS Act 2002 Amendment 2023",
        "expected_section_or_rule": "85",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "limitation period for reference of dispute"
    },
    {
        "id": "dev_central_007",
        "query_text": "How should net profits be disposed under Section 63 of the Multi-State Cooperative Societies Act?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Finance",
        "difficulty": "Hard",
        "expected_source_document": "MSCS Act 2002 Amendment 2023",
        "expected_section_or_rule": "63",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "transfer not less than twenty-five per cent to the reserve fund"
    },
    {
        "id": "dev_central_008",
        "query_text": "What are the permissible modes of investment for multi-state cooperative funds under Section 65?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Finance",
        "difficulty": "Hard",
        "expected_source_document": "MSCS Act 2002 Amendment 2023",
        "expected_section_or_rule": "65",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "cooperative bank, government securities"
    },
    {
        "id": "dev_central_009",
        "query_text": "What is the collateral-free agricultural loan limit under the RBI KCC Master Circular Section 2.1?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Schemes",
        "difficulty": "Easy",
        "expected_source_document": "KCC Master Circular (2018)",
        "expected_section_or_rule": "2.1",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "collateral-free limit is Rs. 1.60 lakh"
    },
    {
        "id": "dev_central_010",
        "query_text": "What is the net effective interest rate for prompt paying farmers under KCC Section 3.4?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Schemes",
        "difficulty": "Easy",
        "expected_source_document": "KCC Master Circular (2018)",
        "expected_section_or_rule": "3.4",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "effective interest rate of 4% per annum"
    },
    {
        "id": "dev_central_011",
        "query_text": "Within how many hours must a farmer intimate crop loss due to localized calamity under PMFBY Section 15.3?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Schemes",
        "difficulty": "Medium",
        "expected_source_document": "PMFBY Operational Guidelines (2023, final)",
        "expected_section_or_rule": "15.3",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "intimation within 72 hours of the occurrence"
    },
    {
        "id": "dev_central_012",
        "query_text": "What is the maximum premium rate payable by farmers for Kharif crops under PMFBY Section 5.1?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Schemes",
        "difficulty": "Easy",
        "expected_source_document": "PMFBY Operational Guidelines (2023, final)",
        "expected_section_or_rule": "5.1",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "maximum premium of 2.0% of sum insured for Kharif foodgrains"
    },
    {
        "id": "dev_central_013",
        "query_text": "Can PACS function as Common Service Centres under the Model Bye-laws Section 1.3?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Schemes",
        "difficulty": "Medium",
        "expected_source_document": "Brief on Model Byelaws for PACS",
        "expected_section_or_rule": "1.3",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "diversify into CSC services and over 25 activities"
    },
    {
        "id": "dev_central_014",
        "query_text": "What are the hardware specifications and cloud hosting guidelines under PACS computerisation Section 3.2?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Schemes",
        "difficulty": "Medium",
        "expected_source_document": "PACS computerisation guidelines",
        "expected_section_or_rule": "3.2",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "cloud-based National Unified Software hosted on State Data Center"
    },
    {
        "id": "dev_central_015",
        "query_text": "What does Section 999 of the Multi-State Co-operative Societies Act say about space exploration cooperatives?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Unsupported",
        "difficulty": "Hard",
        "expected_source_document": None,
        "expected_section_or_rule": None,
        "expected_behavior": "return_no_evidence",
        "expected_evidence": None
    },

    # -------------------------------------------------------------------------
    # PUNJAB JURISDICTION - DEV CASES (15)
    # -------------------------------------------------------------------------
    {
        "id": "dev_punjab_001",
        "query_text": "How many members are needed to register a primary cooperative society under Punjab Act Section 8?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "8",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "consist of at least ten adult persons belonging to separate families"
    },
    {
        "id": "dev_punjab_002",
        "query_text": "ਪੰਜਾਬ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ ਦੀ ਧਾਰਾ 8 ਅਧੀਨ ਸੁਸਾਇਟੀ ਰਜਿਸਟਰ ਕਰਨ ਲਈ ਕਿੰਨੇ ਮੈਂਬਰ ਚਾਹੀਦੇ ਹਨ?",
        "jurisdiction": "punjab",
        "language": "pa",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "8",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "ਘੱਟੋ-ਘੱਟ ਦਸ ਬਾਲਗ ਵਿਅਕਤੀ ਵੱਖ-ਵੱਖ ਪਰਿਵਾਰਾਂ ਨਾਲ ਸਬੰਧਤ"
    },
    {
        "id": "dev_punjab_003",
        "query_text": "Does a member have multiple votes based on shares under Section 19 of Punjab Act 1961?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "19",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "Every member shall have one vote irrespective of shareholding"
    },
    {
        "id": "dev_punjab_004",
        "query_text": "What is the procedure for voting under Section 20 of Punjab Cooperative Societies Act 1961?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "20",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "manner of exercising vote, casting vote of Chairman"
    },
    {
        "id": "dev_punjab_005",
        "query_text": "What is the tenure of managing committee under Section 26 of Punjab Cooperative Societies Act?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "26",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "term of office of the committee shall be five years"
    },
    {
        "id": "dev_punjab_006",
        "query_text": "How can possession of records be secured under Section 28 of Punjab Cooperative Societies Act?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Governance",
        "difficulty": "Hard",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "28",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "apply to District Magistrate for securing possession of records and property"
    },
    {
        "id": "dev_punjab_007",
        "query_text": "Does a cooperative society have first charge on agricultural produce under Section 40 of Punjab Act?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Finance",
        "difficulty": "Medium",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "40",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "prior claim on agricultural produce or cattle for loan outstanding"
    },
    {
        "id": "dev_punjab_008",
        "query_text": "How is charge created on member land under Section 41 of Punjab Cooperative Societies Act?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Finance",
        "difficulty": "Hard",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "41",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "first charge on immovable property owned by member"
    },
    {
        "id": "dev_punjab_009",
        "query_text": "Who is responsible for auditing cooperative societies under Section 48 of the Punjab Act?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Audit",
        "difficulty": "Easy",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "48",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "Registrar shall audit or cause to be audited every registered society at least once in each year"
    },
    {
        "id": "dev_punjab_010",
        "query_text": "When can an inspection of books of an indebted society be made under Section 52 of Punjab Act?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Audit",
        "difficulty": "Hard",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "52",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "inspection on application of creditor"
    },
    {
        "id": "dev_punjab_011",
        "query_text": "Which disputes must be referred to the Registrar under Section 55 of the Punjab Act?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Dispute Resolution",
        "difficulty": "Medium",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "55",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "dispute touching the constitution, management or business of a cooperative society"
    },
    {
        "id": "dev_punjab_012",
        "query_text": "What powers does a liquidator hold under Section 58 of the Punjab Cooperative Societies Act?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Liquidation",
        "difficulty": "Hard",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "58",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "powers of liquidator to institute legal proceedings and determine assets"
    },
    {
        "id": "dev_punjab_013",
        "query_text": "What relief does the PADB OTS Scheme offer to defaulting farmers under Section 1?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Schemes",
        "difficulty": "Easy",
        "expected_source_document": "OTS- The Punjab State Agriculture Development Bank (Amendment)",
        "expected_section_or_rule": "1",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "100% penal interest waiver for default settlement"
    },
    {
        "id": "dev_punjab_014",
        "query_text": "How can an appeal be preferred against Registrar orders under Section 68 of Punjab Act?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Legal Remedy",
        "difficulty": "Medium",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "68",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "appeal to the Government or the Registrar within sixty days"
    },
    {
        "id": "dev_punjab_015",
        "query_text": "Under Punjab law, what is the maximum speed of a cooperative delivery drone under Section 901?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Unsupported",
        "difficulty": "Medium",
        "expected_source_document": None,
        "expected_section_or_rule": None,
        "expected_behavior": "return_no_evidence",
        "expected_evidence": None
    },

    # -------------------------------------------------------------------------
    # HARYANA JURISDICTION - DEV CASES (15)
    # -------------------------------------------------------------------------
    {
        "id": "dev_haryana_001",
        "query_text": "What are the conditions for registration under Section 6 of Haryana Cooperative Societies Act 1984?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "6",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "minimum of ten adult persons residing in the area of operation"
    },
    {
        "id": "dev_haryana_002",
        "query_text": "हरियाणा सहकारी समिति अधिनियम 1984 की धारा 6 के तहत कितने सदस्य आवश्यक हैं?",
        "jurisdiction": "haryana",
        "language": "hi",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "6",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "कम से कम दस वयस्क व्यक्ति अलग-अलग परिवारों से"
    },
    {
        "id": "dev_haryana_003",
        "query_text": "Who can become a member of a society under Section 15 of Haryana Act 1984?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "15",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "individual competent to contract, any other cooperative society"
    },
    {
        "id": "dev_haryana_004",
        "query_text": "Can a member cast more than one vote under Section 19 of Haryana Act?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "19",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "one member one vote, no member shall vote by proxy"
    },
    {
        "id": "dev_haryana_005",
        "query_text": "What is the committee term and reservation under Section 28 of Haryana Cooperative Societies Act?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "28",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "term of committee shall be five years, reservation for women and Scheduled Castes"
    },
    {
        "id": "dev_haryana_006",
        "query_text": "What disqualifies a person from being a committee member under Section 31 of Haryana Act?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "31",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "default in repayment of loan or interest"
    },
    {
        "id": "dev_haryana_007",
        "query_text": "How can records be secured from outgoing committee under Section 35 of Haryana Act?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Governance",
        "difficulty": "Hard",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "35",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "apply to Sub-Divisional Magistrate for search warrant and possession"
    },
    {
        "id": "dev_haryana_008",
        "query_text": "What restrictions exist on borrowings under Section 43 of the Haryana Cooperative Societies Act?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Finance",
        "difficulty": "Medium",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "43",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "restrictions on borrowings from non-members"
    },
    {
        "id": "dev_haryana_009",
        "query_text": "What charge is created on land under Section 47 of Haryana Act?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Finance",
        "difficulty": "Medium",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "47",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "charge on immovable property of borrower for repayment"
    },
    {
        "id": "dev_haryana_010",
        "query_text": "What percentage of net profit must be allocated to reserve fund under Section 59 of Haryana Act?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Finance",
        "difficulty": "Hard",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "59",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "not less than twenty-five per cent transferred to reserve fund"
    },
    {
        "id": "dev_haryana_011",
        "query_text": "Where may society funds be invested under Section 63 of the Haryana Act 1984?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Finance",
        "difficulty": "Hard",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "63",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "cooperative bank, postal savings bank, government securities"
    },
    {
        "id": "dev_haryana_012",
        "query_text": "Who conducts the annual statutory audit under Section 95 of Haryana Cooperative Societies Act?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Audit",
        "difficulty": "Easy",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "95",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "Registrar shall audit or cause to be audited by authorized persons"
    },
    {
        "id": "dev_haryana_013",
        "query_text": "What matters are referable to arbitration under Section 102 of Haryana Act 1984?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Dispute Resolution",
        "difficulty": "Easy",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "102",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "any dispute touching the constitution, management or business of a cooperative society"
    },
    {
        "id": "dev_haryana_014",
        "query_text": "Can civil courts try disputes covered under Section 102 of Haryana Act?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Dispute Resolution",
        "difficulty": "Medium",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "102",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "no court shall have any jurisdiction to entertain any suit or other proceeding"
    },
    {
        "id": "dev_haryana_015",
        "query_text": "What does Haryana Cooperative Societies Act Section 888 state regarding submarine registrations?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Unsupported",
        "difficulty": "Medium",
        "expected_source_document": None,
        "expected_section_or_rule": None,
        "expected_behavior": "return_no_evidence",
        "expected_evidence": None
    },

    # -------------------------------------------------------------------------
    # JAMMU & KASHMIR JURISDICTION - DEV CASES (15)
    # -------------------------------------------------------------------------
    {
        "id": "dev_jk_001",
        "query_text": "How many adult persons are needed to register a cooperative under Section 7 of J&K Act 1989?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "7",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "consist of at least ten adult persons residing in the area of operation"
    },
    {
        "id": "dev_jk_002",
        "query_text": "جموں و کشمیر کوآپریٹو سوسائٹیز ایکٹ کی دفعہ 7 کے تحت کتنے اراکین درکار ہیں؟",
        "jurisdiction": "jk",
        "language": "ur",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "7",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "کم از کم دس بالغ افراد"
    },
    {
        "id": "dev_jk_003",
        "query_text": "How can the liability and name of a society be changed under Section 12 of J&K Act?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "12",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "amendment of bye-laws and approval of the Registrar"
    },
    {
        "id": "dev_jk_004",
        "query_text": "What are member voting rights under Section 20 of Jammu and Kashmir Act 1989?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "20",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "one member one vote, no proxy"
    },
    {
        "id": "dev_jk_005",
        "query_text": "When should the general meeting be convened under Section 28 of J&K Act?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "28",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "general meeting convened within six months of close of financial year"
    },
    {
        "id": "dev_jk_006",
        "query_text": "What is the term of the managing committee under Section 29 of J&K Cooperative Societies Act?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "29",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "term of committee shall be five years"
    },
    {
        "id": "dev_jk_007",
        "query_text": "What records must a cooperative society maintain under Section 36 of J&K Act 1989?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Governance",
        "difficulty": "Hard",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "36",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "register of members, minute book, audited financial accounts"
    },
    {
        "id": "dev_jk_008",
        "query_text": "How does a society establish first charge on agricultural produce under Section 38 of J&K Act?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Finance",
        "difficulty": "Medium",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "38",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "first charge on crops and agricultural produce for loan dues"
    },
    {
        "id": "dev_jk_009",
        "query_text": "What restrictions exist on borrowings under Section 44 of the J&K Cooperative Societies Act?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Finance",
        "difficulty": "Medium",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "44",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "receive deposits and loans only to such extent as specified in bye-laws"
    },
    {
        "id": "dev_jk_010",
        "query_text": "What restrictions govern loans to non-members under Section 46 of J&K Act?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Finance",
        "difficulty": "Hard",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "46",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "society shall not make a loan to any person other than a member"
    },
    {
        "id": "dev_jk_011",
        "query_text": "What is the mandatory statutory reserve fund allocation under Section 54 of J&K Act?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Finance",
        "difficulty": "Hard",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "54",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "transfer at least twenty-five per cent of net profit to reserve fund"
    },
    {
        "id": "dev_jk_012",
        "query_text": "Who performs the annual audit of cooperative accounts under Section 63 of J&K Act 1989?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Audit",
        "difficulty": "Easy",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "63",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "Registrar shall audit or cause to be audited every society once in each year"
    },
    {
        "id": "dev_jk_013",
        "query_text": "Which disputes must be referred to the Registrar under Section 70 of J&K Cooperative Societies Act?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Dispute Resolution",
        "difficulty": "Easy",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "70",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "disputes touching constitution, management or business referred to Registrar"
    },
    {
        "id": "dev_jk_014",
        "query_text": "Can properties be attached prior to an award under Section 71 of J&K Act?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Dispute Resolution",
        "difficulty": "Hard",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "71",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "attachment before award if party intends to defeat execution"
    },
    {
        "id": "dev_jk_015",
        "query_text": "What does Section 777 of J&K Cooperative Societies Act provide for crypto trading licenses?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Unsupported",
        "difficulty": "Medium",
        "expected_source_document": None,
        "expected_section_or_rule": None,
        "expected_behavior": "return_no_evidence",
        "expected_evidence": None
    }
]

VAL_CASES = [
    # -------------------------------------------------------------------------
    # VALIDATION SET (N=40): 10 Central, 10 Punjab, 10 Haryana, 10 J&K
    # -------------------------------------------------------------------------
    # CENTRAL (10)
    {
        "id": "val_central_001",
        "query_text": "What are the registration conditions for a multi-state cooperative under MSCS Act Section 6?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "MSCS Act 2002 Amendment 2023",
        "expected_section_or_rule": "6",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "50 members from each state"
    },
    {
        "id": "val_central_002",
        "query_text": "How often must the board meet under MSCS Act 2002 Section 47?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "MSCS Act 2002 Amendment 2023",
        "expected_section_or_rule": "47",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "board shall meet at least once in every quarter"
    },
    {
        "id": "val_central_003",
        "query_text": "What grounds disqualify a person from being a board member under Section 43 of MSCS Act?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "MSCS Act 2002 Amendment 2023",
        "expected_section_or_rule": "43",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "default, conviction, or interest in conflicting business"
    },
    {
        "id": "val_central_004",
        "query_text": "Who appoints the auditor for a multi-state cooperative under Section 70 of MSCS Act?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Audit",
        "difficulty": "Easy",
        "expected_source_document": "MSCS Act 2002 Amendment 2023",
        "expected_section_or_rule": "70",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "audited by an approved panel of chartered accountants"
    },
    {
        "id": "val_central_005",
        "query_text": "What is the maximum collateral-free KCC crop loan limit without land hypothecation?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Schemes",
        "difficulty": "Easy",
        "expected_source_document": "KCC Master Circular (2018)",
        "expected_section_or_rule": "2.1",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "Rs. 1.60 lakh collateral-free"
    },
    {
        "id": "val_central_006",
        "query_text": "What is the timeline for intimation of localized crop damages under PMFBY Section 15.3?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Schemes",
        "difficulty": "Easy",
        "expected_source_document": "PMFBY Operational Guidelines (2023, final)",
        "expected_section_or_rule": "15.3",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "72 hours window for reporting localized loss"
    },
    {
        "id": "val_central_007",
        "query_text": "What is the maximum premium rate for commercial and horticultural crops under PMFBY Section 5.1?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Schemes",
        "difficulty": "Medium",
        "expected_source_document": "PMFBY Operational Guidelines (2023, final)",
        "expected_section_or_rule": "5.1",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "maximum 5.0% premium for commercial and horticultural crops"
    },
    {
        "id": "val_central_008",
        "query_text": "Under Model Bye-laws Section 4.1, who is eligible to become an active member of a PACS?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Schemes",
        "difficulty": "Medium",
        "expected_source_document": "Brief on Model Byelaws for PACS",
        "expected_section_or_rule": "4.1",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "farmer residing in the village operational radius"
    },
    {
        "id": "val_central_009",
        "query_text": "What are the ERP architecture modules under PACS computerisation Section 2.1?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Schemes",
        "difficulty": "Hard",
        "expected_source_document": "PACS computerisation guidelines",
        "expected_section_or_rule": "2.1",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "core banking, credit, non-credit, and accounting modules"
    },
    {
        "id": "val_central_010",
        "query_text": "Can a multi-state society operate commercial airlines under MSCS Act Section 750?",
        "jurisdiction": "central",
        "language": "en",
        "category": "Unsupported",
        "difficulty": "Medium",
        "expected_source_document": None,
        "expected_section_or_rule": None,
        "expected_behavior": "return_no_evidence",
        "expected_evidence": None
    },

    # PUNJAB (10)
    {
        "id": "val_punjab_001",
        "query_text": "What are the minimum member requirements for registering a cooperative society in Punjab under Section 8?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "8",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "10 adult persons from separate families"
    },
    {
        "id": "val_punjab_002",
        "query_text": "ਪੰਜਾਬ ਵਿੱਚ ਸਹਿਕਾਰੀ ਸਭਾ ਦੀ ਮੈਨੇਜਿੰਗ ਕਮੇਟੀ ਦੀ ਮਿਆਦ ਕਿੰਨੇ ਸਾਲ ਹੁੰਦੀ ਹੈ (ਧਾਰਾ 26)?",
        "jurisdiction": "punjab",
        "language": "pa",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "26",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "ਪੰਜ ਸਾਲ ਦੀ ਮਿਆਦ"
    },
    {
        "id": "val_punjab_003",
        "query_text": "How can the government supersede a defaulting committee under Section 27 of Punjab Act?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "27",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "supersession or suspension of committee by Registrar"
    },
    {
        "id": "val_punjab_004",
        "query_text": "What is the reserve fund contribution required under Section 23 of the Punjab Act?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Finance",
        "difficulty": "Hard",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "23",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "at least 25% of net profit transferred to reserve fund"
    },
    {
        "id": "val_punjab_005",
        "query_text": "What accounts and books must be maintained under Section 44 of Punjab Act 1961?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Audit",
        "difficulty": "Hard",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "44",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "statutory books of accounts and records"
    },
    {
        "id": "val_punjab_006",
        "query_text": "How frequently must a society be audited in Punjab under Section 48?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Audit",
        "difficulty": "Easy",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "48",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "at least once in each financial year"
    },
    {
        "id": "val_punjab_007",
        "query_text": "What constitutes an arbitrable dispute under Section 55 of the Punjab Cooperative Societies Act?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Dispute Resolution",
        "difficulty": "Easy",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "55",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "disputes touching constitution, management, or business"
    },
    {
        "id": "val_punjab_008",
        "query_text": "What is the procedure when a dispute is referred to the Registrar under Section 56 of Punjab Act?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Dispute Resolution",
        "difficulty": "Medium",
        "expected_source_document": "Punjab Cooperative Societies Act 1961",
        "expected_section_or_rule": "56",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "Registrar decides dispute or refers to arbitrator"
    },
    {
        "id": "val_punjab_009",
        "query_text": "Does PADB waive full penal interest under the OTS scheme Section 1?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Schemes",
        "difficulty": "Easy",
        "expected_source_document": "OTS- The Punjab State Agriculture Development Bank (Amendment)",
        "expected_section_or_rule": "1",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "100% penal interest waiver"
    },
    {
        "id": "val_punjab_010",
        "query_text": "Can Punjab cooperative members issue private currency under Section 602?",
        "jurisdiction": "punjab",
        "language": "en",
        "category": "Unsupported",
        "difficulty": "Medium",
        "expected_source_document": None,
        "expected_section_or_rule": None,
        "expected_behavior": "return_no_evidence",
        "expected_evidence": None
    },

    # HARYANA (10)
    {
        "id": "val_haryana_001",
        "query_text": "What is the minimum member count for registration under Section 6 of Haryana Act 1984?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "6",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "10 adult persons from separate households"
    },
    {
        "id": "val_haryana_002",
        "query_text": "हरियाणा सहकारी समिति की प्रबंध समिति का कार्यकाल कितने वर्ष है (धारा 28)?",
        "jurisdiction": "haryana",
        "language": "hi",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "28",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "पाँच वर्ष का कार्यकाल"
    },
    {
        "id": "val_haryana_003",
        "query_text": "When must an Annual General Meeting be held under Section 27 of Haryana Act?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "27",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "within six months of close of cooperative year"
    },
    {
        "id": "val_haryana_004",
        "query_text": "What are grounds for supersession of committee under Section 34 of Haryana Act 1984?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Governance",
        "difficulty": "Hard",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "34",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "persistent default or neglect of duties"
    },
    {
        "id": "val_haryana_005",
        "query_text": "Can loans be given to non-members under Section 51 of Haryana Act?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Finance",
        "difficulty": "Medium",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "51",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "restrictions on loans to non-members"
    },
    {
        "id": "val_haryana_006",
        "query_text": "Who appoints auditors for cooperative society audit under Section 95 of Haryana Act?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Audit",
        "difficulty": "Easy",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "95",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "Registrar audits or causes to be audited"
    },
    {
        "id": "val_haryana_007",
        "query_text": "What happens during an inquiry ordered under Section 97 of Haryana Cooperative Societies Act?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Audit",
        "difficulty": "Hard",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "97",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "inquiry into constitution, working and financial condition"
    },
    {
        "id": "val_haryana_008",
        "query_text": "Does civil court have jurisdiction over disputes covered by Section 102 of Haryana Act?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Dispute Resolution",
        "difficulty": "Easy",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "102",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "civil court jurisdiction is barred"
    },
    {
        "id": "val_haryana_009",
        "query_text": "Who acts as arbitrator for disputes referred under Section 103 of Haryana Act?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Dispute Resolution",
        "difficulty": "Medium",
        "expected_source_document": "Haryana Co-operative Societies Act 1984",
        "expected_section_or_rule": "103",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "Registrar or appointed arbitrator"
    },
    {
        "id": "val_haryana_010",
        "query_text": "What is the maximum subsidy for purchasing spaceships in Haryana under Section 499?",
        "jurisdiction": "haryana",
        "language": "en",
        "category": "Unsupported",
        "difficulty": "Medium",
        "expected_source_document": None,
        "expected_section_or_rule": None,
        "expected_behavior": "return_no_evidence",
        "expected_evidence": None
    },

    # JAMMU & KASHMIR (10)
    {
        "id": "val_jk_001",
        "query_text": "What are the registration conditions under Section 7 of J&K Cooperative Societies Act 1989?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Governance",
        "difficulty": "Easy",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "7",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "10 adult persons residing or owning land in area"
    },
    {
        "id": "val_jk_002",
        "query_text": "جموں و کشمیر میں کوآپریٹو کمیٹی کی مدت کتنی ہوتی ہے (دفعہ 29)؟",
        "jurisdiction": "jk",
        "language": "ur",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "29",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "پانچ سال کی مدت"
    },
    {
        "id": "val_jk_003",
        "query_text": "What disqualifies a member from election to the committee under Section 30 of J&K Act?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Governance",
        "difficulty": "Medium",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "30",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "default, conviction, or interest in conflicting contracts"
    },
    {
        "id": "val_jk_004",
        "query_text": "When can a committee be superseded under Section 31 of J&K Cooperative Societies Act?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Governance",
        "difficulty": "Hard",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "31",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "supersession for persistent negligence or breach of law"
    },
    {
        "id": "val_jk_005",
        "query_text": "What is the statutory reserve fund requirement under Section 54 of J&K Act?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Finance",
        "difficulty": "Hard",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "54",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "at least 25% of net profits transferred to reserve fund"
    },
    {
        "id": "val_jk_006",
        "query_text": "How often is statutory audit conducted under Section 63 of J&K Cooperative Societies Act?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Audit",
        "difficulty": "Easy",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "63",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "audit at least once in each year"
    },
    {
        "id": "val_jk_007",
        "query_text": "Who can order an inquiry into a society's affairs under Section 64 of J&K Act?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Audit",
        "difficulty": "Medium",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "64",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "Registrar may hold an inquiry"
    },
    {
        "id": "val_jk_008",
        "query_text": "Which disputes are referable to the Registrar under Section 70 of J&K Act 1989?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Dispute Resolution",
        "difficulty": "Easy",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "70",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "disputes touching the constitution, management or business"
    },
    {
        "id": "val_jk_009",
        "query_text": "What power does the Registrar have under Section 71 regarding attachment of property?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Dispute Resolution",
        "difficulty": "Hard",
        "expected_source_document": "J&K Cooperative Societies Act 1989 (cooperation.gov.in copy)",
        "expected_section_or_rule": "71",
        "expected_behavior": "retrieve_and_answer",
        "expected_evidence": "attachment before award to prevent disposal of property"
    },
    {
        "id": "val_jk_010",
        "query_text": "Can a J&K cooperative issue nuclear power export permits under Section 555?",
        "jurisdiction": "jk",
        "language": "en",
        "category": "Unsupported",
        "difficulty": "Medium",
        "expected_source_document": None,
        "expected_section_or_rule": None,
        "expected_behavior": "return_no_evidence",
        "expected_evidence": None
    }
]

def main():
    dev_path = OUTPUT_DIR / "dev_benchmark_dataset.json"
    val_path = OUTPUT_DIR / "val_benchmark_dataset.json"

    with open(dev_path, "w", encoding="utf-8") as f:
        json.dump(DEV_CASES, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved {len(DEV_CASES)} development benchmark cases to {dev_path}")

    with open(val_path, "w", encoding="utf-8") as f:
        json.dump(VAL_CASES, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved {len(VAL_CASES)} validation benchmark cases to {val_path}")

if __name__ == "__main__":
    main()
