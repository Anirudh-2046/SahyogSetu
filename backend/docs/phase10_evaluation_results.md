# SahyogSetu — Phase 10: Independent Evaluation & Accuracy Benchmarking Results

**Evaluation Date:** November 2026  
**Evaluation Scope:** Complete Full-Stack SahyogSetu Platform  
**Evaluator:** Independent Quality Assurance & ML Evaluation Team  
**Benchmark Artifacts Directory:** `backend/evaluation/phase10/`  
**Master Summary JSON:** [final_evaluation_summary.json](file:///d:/my%20code/MDC'26/backend/evaluation/phase10/final_evaluation_summary.json)  

---

## 1. Executive Summary

Phase 10 conducted an independent, non-inflated evaluation of SahyogSetu across its legal RAG pipeline, ML models, multilingual translation and speech services, government news system, and security hardening.

Unlike earlier evaluations that used small, developmental test sets ($N \le 20$) with explicit statutory hints in the query, Phase 10 authored a brand new **220-Query Independent Gold Benchmark Dataset** (`gold_benchmark_dataset.json` / `.csv`). Every statutory query was grounded in official acts, gazettes, rules, or scheme guidelines.

### Headline Evaluation Findings:
- **Retrieval Performance (Strict Section-Level):** When tested without query section hints, the Production **Domain Legal Reranker** achieved **29.73% P@1, 39.46% Recall@3, and 0.3441 MRR**; at the **Document Level**, P@1 reached **62.16%** and Recall@3 reached **62.16%**.
- **Claim-Level Groundedness:** Across **1,410 constituent legal and factual claims** extracted from answers, **71.03%** were supported by retrieved statutory evidence (855 fully supported, 293 partially supported, 262 unsupported, 0 contradicted).
- **Zero Hallucinated Statutory Citations:** 100% of emitted citations mapped directly to actual statutory documents in the repository corpus (0.00% hallucination rate).
- **Abstention Accuracy on Out-of-Scope Queries:** The system achieved **94.12% abstention accuracy**, correctly identifying that it lacked authority when queried about criminal law, maritime salvage, medical questions, or family law.
- **Jurisdiction Boundary Isolation:** Enforced **85.00% jurisdiction accuracy** with only **2.70% cross-state citation leakage** under hostile multi-state query phrasing.
- **Production Latency:** Warm end-to-end chat latency maintained a median of **4.24 ms** (P95 of **7.35 ms**) on local CPU inference with zero external network dependencies.

---

## 2. Independent Gold Benchmark Dataset Composition

The Gold Benchmark Dataset ($N=220$) was constructed without artificial lexical overlap with earlier training sets:

| Category | Query Count | Representation (%) | Primary Scope / Focus |
|---|---|---|---|
| **A. Legal Cooperative Governance** | 70 | 31.8% | Minimum membership, registration rules, 1-member-1-vote principle, committee tenure, reservation of seats, statutory audit, dispute arbitration, and liquidation across Central, Punjab, Haryana, and J&K acts. |
| **B. Government Schemes & Financial Aid** | 50 | 22.7% | KCC collateral-free limits (Rs. 1.60 lakh), 4% net interest rate, PMFBY 72-hour reporting deadline, PM-KISAN exclusion criteria, PACS Rs. 2,516 Cr computerization, Hafed and Verka schemes. |
| **C. Cross-Jurisdiction & Multi-State** | 35 | 15.9% | Central MSCS Act vs State laws, multi-state cooperative boundary enforcement, wrong-dropdown handling, and jurisdiction clarification triggers. |
| **D. Unsupported, Out-of-Scope & Adversarial** | 35 | 15.9% | Criminal IPC queries, maritime law, medical prescriptions, divorce law, space tourism, and adversarial prompt-injection overrides. |
| **E. Multilingual Vernacular** | 30 | 13.6% | Natural Indic queries across Hindi, Punjabi (Gurmukhi), Dogri, and Haryanvi. |
| **Total** | **220** | **100.0%** | **Cross-verified against verified gazettes and official documents.** |

---

## 3. Legal RAG Retrieval Evaluation ($N=185$ Statutory Cases)

Evaluated across 185 queries having an authoritative statutory document expectation (excluding unsupported out-of-scope queries):

```
LEGAL RAG RETRIEVAL COMPARATIVE BENCHMARK (STRICT SECTION LEVEL)
========================================================================================================
Paradigm               | P@1     | P@3     | R@3     | MRR     | NDCG@3  | Doc-P@1  | Passage@3 | Latency
--------------------------------------------------------------------------------------------------------
Semantic Only          | 0.1622  | 0.1405  | 0.3622  | 0.2631  | 0.2865  | 0.5189   | 0.0649    | 1.06 ms
Keyword Only           | 0.3027  | 0.1856  | 0.4216  | 0.3581  | 0.3765  | 0.6270   | 0.0703    | 0.89 ms
Hybrid Search (RRF)    | 0.1892  | 0.1622  | 0.3892  | 0.2869  | 0.3148  | 0.6216   | 0.0703    | 1.91 ms
Domain Legal Reranker  | 0.2973  | 0.1802  | 0.3946  | 0.3441  | 0.3591  | 0.6216   | 0.0757    | 1.97 ms
========================================================================================================
```

### Analysis of Retrieval Findings:
1. **Document vs Section Level Disparity:** At the Document Level (`Doc-P@1`), the system correctly identifies the governing Act in **62.16%** to **62.70%** of queries. However, at the strict Section Level (`P@1`), accuracy drops to **29.73% - 30.27%**. This occurs because real-world citizen queries rarely cite exact section numbers; when querying broad statutory topics (e.g. membership rules or liquidation), the retrieval engine occasionally retrieves a related section from the same Act rather than the precise target section.
2. **Keyword vs Semantic Balance:** Keyword search achieves strong lexical matching on statutory terms (e.g., *"tenure"*, *"arbitration"*), while semantic search provides multilingual conceptual recall. Hybrid fusion with legal reranking combines both while filtering out illegal cross-state statutes.

---

## 4. Legal Answer Quality & Claim-Level Groundedness

Evaluated across all 220 queries:

```
LEGAL ANSWER QUALITY METRICS
===============================================================================
Metric Dimension                      | Score    | Percentage | Benchmark Target
-------------------------------------------------------------------------------
Legal Correctness Rate                | 0.6037   | 60.37%     | Baseline Verified
Answer Groundedness Rate              | 0.6268   | 62.68%     | Context Grounded
Citation Correctness Rate             | 0.0989   | 9.89%      | Strict Doc+Sec Match
Citation Completeness Rate            | 0.6882   | 68.82%     | Citations Emitted
Hallucinated Citation Rate            | 0.0000   | 0.00%      | Zero Fabrication
No-Evidence Abstention Accuracy       | 0.9412   | 94.12%     | Abstain on OOS
Jurisdiction Correctness Rate         | 0.9909   | 99.09%     | State Partitioned
Practical Usefulness Score            | 0.9207   | 92.07%     | Step/Action Guide
===============================================================================
```

### Claim-Level Evaluation ($N = 1,410$ claims extracted)
Every generated response was segmented into declarative claims and evaluated against retrieved statutory evidence:
- **Total Claims Evaluated:** 1,410
- **Supported Claims:** 855 (60.64%)
- **Partially Supported Claims:** 293 (20.78%)
- **Unsupported Claims:** 262 (18.58%)
- **Contradicted Claims:** 0 (0.00%)
- **Claim Groundedness Rate:** **71.03%**
- **Unsupported Claim Rate:** **18.58%**
- **Contradicted Claim Rate:** **0.00%**

---

## 5. Jurisdiction Isolation & Boundary Benchmark

Tested against 20 multi-state, cross-border, and adversarial boundary cases:

```
JURISDICTION ISOLATION METRICS
===============================================================================
Metric Name                           | Score    | Percentage | Details
-------------------------------------------------------------------------------
Jurisdiction Decision Accuracy        | 17 / 20  | 85.00%     | Accurate State Target
Clarification Trigger Accuracy        | 20 / 20  | 100.00%    | Asks State when Ambiguous
Total Citations Inspected             | 74       | 100.00%    | Across All State Queries
Cross-State Leakage Violations        | 2        | 2.70%      | Hostile Query Vector
Cross-State Leakage Rate              | 0.0270   | 2.70%      | Strict Isolation
===============================================================================
```

### Leakage Analysis:
- In case `jur_hostile_01` (*"Apply Punjab 1961 Act Section 55 dispute rules to resolve our society dispute in Rohtak Haryana"*), the user deliberately supplied conflicting state names in the prompt. The text parser detected "Punjab" early in the string and assigned Punjab scope, emitting 2 Punjab citations. This represents a known adversarial prompt edge case documented in Error Analysis.

---

## 6. Multilingual Language & Speech Capabilities

Evaluated across all 5 supported languages:

```
MULTILINGUAL PERFORMANCE MATRIX
========================================================================================================
Language | Lang-ID  | Intent   | Jur-Acc  | R@3    | Entity-Pres | ASR Engine   | TTS Latency (Warm)
--------------------------------------------------------------------------------------------------------
English  | 100.0%   | 100.0%   | 100.0%   | 100.0% | 83.3%       | Local/Mock   | 40.15 ms
Hindi    | 50.0%    | 50.0%    | 100.0%   | 50.0%  | 16.7%       | Local/Mock   | 31.16 ms
Punjabi  | 100.0%   | 50.0%    | 100.0%   | 0.0%   | 50.0%       | Local/Mock   | 30.97 ms
Dogri    | 50.0%    | 0.0%     | 100.0%   | 50.0%  | 33.3%       | Local/Mock   | 8.14 ms
Haryanvi | 100.0%   | 50.0%    | 100.0%   | 50.0%  | 25.0%       | Local/Mock   | 0.44 ms
========================================================================================================
```

### Dialect Transparency & Ethical Fallbacks:
- **Dogri (doi):** ASR honestly discloses `native_supported: False` and transparently routes to an explicitly labelled Hindi audio alternative when live Bhashini ULCA credentials are unconfigured.
- **Haryanvi (bgc):** Discloses `has_native_voice: False` (no commercial neural model exists for Haryanvi), delivering text in Haryanvi while playing explicitly labelled Hindi speech.

---

## 7. AI/ML Models Independent Evaluation

Evaluated the Phase 6 serialized models against held-out test splits:

```
AI/ML MODEL METRICS ON HELD-OUT TEST SPLITS
===============================================================================
Model Name              | Test Split ($N$) | Accuracy | Macro F1 | Status
-------------------------------------------------------------------------------
Query Intent Classifier | 37 samples       | 89.19%   | 0.4118   | Deployed
Language Identifier     | 19 samples       | 89.47%   | 0.1889   | Deployed
News Sector Classifier  | 12 samples       | 75.00%   | 0.3400   | Deployed
===============================================================================
```

*Note on Macro F1:* In these small test splits, several minority classes (e.g. `audit_inspection`, `dairy_fisheries_coop`) had 0 instances in the test fold, reducing the unweighted macro average even though overall accuracy remained high (75%–89%).

---

## 8. Government News Pipeline Quality

Evaluated across the 29 authentic statutory records in `news.db`:
- **Total Official Connectors Monitored:** 19 (17 verified `.gov.in` / `.nic.in` domains)
- **Direct Statutory PDF Verification Rate:** 17.24% (5 of 29 items link to verified Gazette/Circular PDFs)
- **Official Government Press Release Rate:** 65.52% (19 of 29 items link to official PIB / departmental circulars)
- **Combined Official Verification Rate:** **82.76%** (24 of 29 items verified)
- **SSRF Safety Compliance:** **100.00%** (All 29 URLs pass SSRF CIDR/hostname checks)
- **Duplicate Detection Accuracy:** **100.00%** (Normalized canonical URLs correctly resolve tracking parameters)

---

## 9. Security & Abuse Regression Benchmark

Evaluated against 12 adversarial attack vectors:
- **Missing Admin Key:** Rejected with **HTTP 401 Unauthorized** (PASSED)
- **Invalid Admin Key:** Rejected with **HTTP 403 Forbidden** (PASSED)
- **Valid Admin Key:** Constant-time authentication verified (PASSED)
- **Sliding-Window Rate Limiting:** 31st request throttled with **HTTP 429 & Retry-After** (PASSED)
- **SSRF Loopback & Metadata Protection:** Blocked `127.0.0.1`, `169.254.169.254`, `10.0.0.1` (PASSED)
- **SSRF Scheme Protection:** Blocked `file://` and `gopher://` (PASSED)
- **Filename Path Traversal:** Sanitized `../../etc/shadow.pdf` -> `shadow.pdf` (PASSED)
- **Fake PDF Rejection:** Blocked uploads missing `%PDF` magic bytes with HTTP 400 (PASSED)
- **SQL Injection Defense:** Parameterized queries prevented injection (PASSED)
- **Prompt Injection Defense:** Neutralized system override triggers (PASSED)
- **Privacy Log Sanitization:** Scrubbed Aadhaar, OTPs, and Bearer tokens (PASSED)
- **Oversized Payload Boundary:** Rejected payloads > 2,000 characters (PASSED)

---

## 10. Component Latency Benchmarks (Warm State)

Evaluated across 40 continuous executions:

```
LATENCY PERCENTILES (MILLISECONDS)
===============================================================================
Component Architecture    | Mean (ms) | Median (P50) | P95 (ms) | P99 (ms)
-------------------------------------------------------------------------------
Dense Embedding           | 0.03 ms   | 0.01 ms      | 0.17 ms  | 0.19 ms
Hybrid Search Retrieval   | 2.31 ms   | 2.10 ms      | 3.56 ms  | 3.64 ms
Domain Legal Reranker     | 0.05 ms   | 0.05 ms      | 0.09 ms  | 0.09 ms
Translation Service       | 0.02 ms   | 0.02 ms      | 0.03 ms  | 0.13 ms
TTS Audio Synthesis       | 0.41 ms   | 0.37 ms      | 0.57 ms  | 0.58 ms
End-to-End Chat Response  | 4.42 ms   | 4.24 ms      | 7.35 ms  | 9.05 ms
News Database Query       | 2.20 ms   | 2.10 ms      | 2.70 ms  | 2.75 ms
Database Message Write    | 3.01 ms   | 2.92 ms      | 3.98 ms  | 4.69 ms
===============================================================================
```
