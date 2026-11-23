# SahyogSetu — Phase 10: Evaluation Audit & Benchmark Integrity Review

**Document Version:** 1.0  
**Date:** November 2026  
**Auditor:** Independent Quality Assurance & Evaluation Engineering Team  
**Scope:** Complete forensic audit of evaluation systems, metrics, datasets, scripts, and claim verifiability across Phases 2 through 9.

---

## 1. Executive Summary

Before introducing the new Phase 10 independent evaluation framework, a thorough audit was conducted on all prior evaluation artifacts, benchmark datasets, metric calculation routines, and reported accuracy figures.

The audit revealed that while earlier phases successfully implemented functional services and regression tests, previous quantitative evaluation metrics suffered from significant methodological limitations:
1. **Extremely small test samples:** Prior RAG benchmarks relied on $N=12$ and $N=20$ queries; news classifier test splits contained only 12 samples across 10 categories.
2. **Template-induced train/test leakage:** Synthetic dataset generation created lexical duplicates and near-identical phrasings between training and test sets in Phase 6.
3. **Query hint leakage:** A large proportion of statutory evaluation queries included explicit section numbers in the query text (e.g. *"under Section 8"*, *"under Section 28"*), which artificially inflated keyword matching, retrieval ranking, and heuristic reranker metrics.
4. **Self-referential validation:** Evaluators frequently validated answers against hardcoded expected strings rather than verified statutory ground truth passages evaluated by independent reviewers.

This document establishes the baseline audit findings. All subsequent Phase 10 benchmarks will be conducted on a newly authored, genuinely independent Gold Dataset ($N \ge 200$) with rigorous human and expert statutory review.

---

## 2. Forensic Audit of Existing Metrics

| Metric Name | Phase & Component | Prior Reported Value | Prior Dataset Size ($N$) | Evaluation Method | Genuinely Independent? | Critical Limitations & Biases Identified |
|---|---|---|---|---|---|---|
| **RAG Precision@1** | Phase 4 (Legal RAG) | 0.9000 (90.0%) | $N = 12$ queries | Automated string matching of expected act & section | **NO** (Authored by RAG developers during Phase 4) | N=12 is statistically unrepresentative; 9 of 12 queries contained explicit section numbers; 1 pa, 1 hi, 1 doi, 0 bgc. |
| **RAG Recall@3** | Phase 4 (Legal RAG) | 0.9000 (90.0%) | $N = 12$ queries | Automated match in top 3 citations | **NO** | Reused Phase 4 developmental examples. |
| **RAG MRR** | Phase 4 (Legal RAG) | 0.9000 | $N = 12$ queries | Mean reciprocal rank calculation | **NO** | Small sample; single error drops MRR by ~0.08. |
| **Intent Classification Accuracy** | Phase 6 (NLP/ML) | 86.49% | $N = 37$ (test split of 243) | Scikit-learn test split evaluation | **PARTIAL** (Stratified 15% split from single pool) | Lexical template leakage between train and test sets; ~4 samples per class; synthetic citizen phrasing. |
| **Intent Macro F1** | Phase 6 (NLP/ML) | 0.8598 | $N = 37$ | Scikit-learn classification report | **PARTIAL** | Minority classes (e.g. audit_inspection) had fewer than 3 test instances. |
| **News Sector Accuracy** | Phase 6 (NLP/ML) | 91.67% | $N = 12$ (test split of 80) | Scikit-learn test split evaluation | **NO** | **Severe sample size bias:** 12 test samples across 10 sectors means several sectors had 0 or 1 test instance. Single sample error = 8.33% swing. |
| **News Macro F1** | Phase 6 (NLP/ML) | 0.8800 | $N = 12$ | Scikit-learn classification report | **NO** | Statistically invalid due to severe zero-shot class instances in test fold. |
| **Language ID Accuracy** | Phase 6 (NLP/ML) | 94.74% | $N = 19$ (test split of 125) | Scikit-learn test split evaluation | **PARTIAL** | 19 samples (~3-4 per language); high confusion between Devanagari Hindi and Haryanvi not adequately stress-tested. |
| **Language Macro F1** | Phase 6 (NLP/ML) | 0.9492 | $N = 19$ | Scikit-learn classification report | **PARTIAL** | Limited Romanized Indic dialect representation. |
| **Reranker P@1 & Recall@3** | Phase 6 (Reranker) | P@1=0.90, R@3=0.90 | $N = 20$ queries | Automated ranking against expected act/section | **NO** (Derived from Phase 4 benchmark) | 8 queries were direct Phase 4 copies; section hint in query gives heuristic reranker an unfair +0.35 advantage. |
| **Cross-State Leakage** | Phase 6 & Phase 8 | 0.0% reported | $N = 4$ state queries | Automated check for cross-state acts | **NO** | Tested only 1 query per state; does not evaluate ambiguous or multi-state citizen prompts. |
| **Full-Stack Journey Pass Rate** | Phase 8 (Integration) | 9 / 9 (100%) | $N = 9$ user journeys | End-to-end integration test | **NO** (Pre-scripted integration tests) | Functional smoke test verifying pipeline wiring; not an accuracy benchmark. |
| **Security Hardening Pass Rate** | Phase 9 (Security) | 10 / 10 (100%) | $N = 10$ pillars | Automated unit/integration test suite | **NO** (Targeted vulnerability assertions) | Evaluates security boundaries, not legal correctness or answer quality. |

---

## 3. Analysis of Train/Test Leakage & Methodological Deficiencies

### 3.1 Lexical Template Duplication
Inspection of `backend/ml/datasets/intent_dataset.json` (243 items) revealed that queries were generated from structured linguistic templates:
- Example: *"How do I register a primary agricultural cooperative society in Punjab?"* (Train)
- Example: *"What is the registration process for a cooperative society in Punjab?"* (Test)
Both share n-grams (`"cooperative society"`, `"Punjab"`, `"registration"`, `"register"`). While natural language queries inherently share domain vocabulary, a random stratified train/test split without semantic clustering allows the classifier to memorize specific template patterns rather than generalizing to citizen vernacular.

### 3.2 Query Section Hinting (Data Contamination)
In `backend/rag/evaluation.py` and `backend/ml/evaluation/reranker_eval.py`:
- Out of 20 benchmark queries, 14 explicitly provided the statute name, the act year, or the exact section number (e.g., *"under Section 8"*, *"under Section 63"*, *"Section 84 of MSCS Act"*, *"Section 28"*).
- When a citizen asks *"Under Section 8 of the Punjab Act..."*, keyword matching achieves near-perfect retrieval simply by token matching.
- **Real-world citizen queries rarely cite the exact section number or act title.** A real farmer asks: *"How many people from different families are needed to form a village cooperative?"*
- Benchmarks relying on section hints significantly overestimate retrieval accuracy in practical deployments.

### 3.3 Evaluation Metric Calculation Code Audit
Inspection of `backend/rag/evaluation.py` lines 180–230:
```python
is_act_match = exp_act in act_title or exp_act in chunk_text
is_sec_match = exp_sec in sec_val or exp_sec in chunk_text
```
- **Flaw:** Checking `exp_sec in chunk_text` allows false positive matches if the number appears anywhere in the body text (e.g., "8 days notice" or "page 8"), even if the chunk represents a completely different section!
- **Flaw:** Evaluating retrieval at the document level rather than requiring both correct document AND correct section creates misleadingly high precision scores.

---

## 4. Mandate for Phase 10 Independent Evaluation

To eliminate prior biases and produce trustworthy, publication-grade measurements, Phase 10 establishes the following methodological requirements:

1. **Independent Gold Dataset ($N \ge 200$):**
   - Must be authored completely independently of all Phase 2–9 training and test scripts.
   - Must contain natural citizen queries without artificial section hinting.
   - Must comprehensively span all 4 jurisdictions (Central, Punjab, Haryana, J&K), cross-jurisdiction queries, unsupported out-of-scope queries, and all 5 languages (English, Hindi, Punjabi, Dogri, Haryanvi).
2. **Multi-level Ground-Truth Verification:**
   - Every statutory query must be tied to verified legal ground truth: applicable Act, official Gazette/source document, exact Section/Rule, and exact verified text excerpt.
   - Ground truth labels must be audited with clear status indicators (`HUMAN_VERIFIED`, `SECOND_REVIEWED`).
3. **Rigorous Hierarchical Retrieval Evaluation:**
   - Must separate Document-level match from Section-level match from Supporting Passage-level match.
   - Retrieving the right Act but wrong section must be strictly scored as a failure.
4. **Fine-grained Answer Quality & Claim-level Groundedness:**
   - Generated answers must be parsed into constituent claims and evaluated for support against retrieved passages (`SUPPORTED`, `PARTIALLY_SUPPORTED`, `UNSUPPORTED`, `CONTRADICTED`).
   - Hallucinated citation rates and unsupported claim rates must be transparently reported.
5. **No Metric Inflation Guarantee:**
   - Real failure cases, confusing dialect terms, out-of-scope abstention failures, and latency distributions will be fully documented without obfuscation.
