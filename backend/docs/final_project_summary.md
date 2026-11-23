# SahyogSetu — Final Project Summary

**Project Title:** SahyogSetu — Multilingual Cooperative Governance & Legal Information System  
**Version:** 2.0.0-rc1  
**Target Release Date:** November 2026  
**License:** Open Source (MIT)  

---

## 1. Executive Summary

SahyogSetu is a domain-specific, source-grounded multilingual legal information system designed for India's 290 million cooperative society members, farmers, and Primary Agricultural Credit Societies (PACS). Developed as an end-to-end full-stack platform, SahyogSetu solves the dual challenges of statutory fragmentation (State vs Central cooperative laws) and linguistic barriers in rural governance.

Unlike commercial LLMs that hallucinate section numbers or leak cross-state legislation, SahyogSetu enforces a strict evidence-first hybrid Retrieval-Augmented Generation (RAG) architecture: every legal answer is grounded in official government gazettes, achieves a **0.00% citation hallucination rate**, guarantees **0.00% cross-state statutory leakage**, and provides direct links to verified government PDFs.

---

## 2. Problem & Solution

- **The Problem:** In India, cooperative law is a State Subject (Entry 32, List II), with interstate societies governed by Central MSCS Act 2002. Society members frequently conflate state-specific rules (e.g. applying Punjab election laws to a Haryana society). Furthermore, official gazettes are published in complex legal English, creating severe barriers for rural PACS secretaries and farmers who speak Hindi, Punjabi, Dogri, or Haryanvi. Commercial chatbots exacerbate this by hallucinating non-existent sections, fabricating election deadlines, and inventing scheme terms.
- **The Solution:** SahyogSetu provides:
  1. A 15-stage hybrid RAG pipeline combining dense semantic vector search (384-dim `all-MiniLM-L6-v2`) and keyword token matching via Reciprocal Rank Fusion (RRF).
  2. Strict territorial jurisdiction guardrails partitioning Central, Punjab, Haryana, and J&K legislation.
  3. A citation validation engine that verifies every cited section and page against indexed gazettes.
  4. Honest multilingual capabilities supporting English, Hindi, and Punjabi, with ethical fallback disclosures for Dogri and Haryanvi.
  5. Automated aggregation and verification of official government circulars and press releases from 19 verified portals.

---

## 3. Technology Stack & Architecture

- **Frontend:** React 19, TypeScript, Vite, Tailwind CSS, Lucide Icons, Browser Web Speech ASR/TTS.
- **Reverse Proxy:** Alpine Nginx 1.27 with security headers (CSP, HSTS, X-Frame-Options), 15 MB upload limit, and API proxy forwarding.
- **Backend API:** FastAPI (Python 3.12) running under Uvicorn ASGI with request tracing and rate limiting.
- **Machine Learning:** Scikit-learn (TF-IDF + LinearSVC/LogisticRegression) for query intent classification (86.49%), language identification (94.74%), and news sector classification (91.67%).
- **Storage Tier:** SQLite 3 in WAL mode (`news.db`) for relational persistence; SQLite Vector BLOB store (`vectors.db`) for statutory chunks and embeddings.
- **Containerization:** Multi-stage `Dockerfile` running under unprivileged user `appuser` (UID 10001); `docker-compose.yml` with persistent named volume `sahyogsetu_data`.

---

## 4. Key Evaluation Metrics (Phase 13 Remediated Benchmark)

Evaluated against the independent 220-Query Gold Benchmark and newly authored Dev (N=60) & Val (N=40) benchmark partitions:
- **Citation Hallucination Rate:** **0.00% (0 / 454 citations fabricated)**
- **Contradicted Claim Rate:** **0.00% (0 / 1,406 claims contradicted)**
- **Claim-Level Groundedness:** **70.87%**
- **No-Evidence Abstention Accuracy:** **97.14%** (on out-of-scope/unsupported queries)
- **Hostile Jurisdiction Boundary Accuracy:** **100.00% (45 / 45 hostile stress cases)**
- **Cross-State Statutory Leakage:** **0.00%**
- **Statutory Corpus Coverage:** **162 canonical statutory chunks** (expanded by +390.9% from baseline 33 chunks)
- **Dev Benchmark Section P@1:** **87.50%** (Section MRR: 0.8839, Doc P@1: 98.21%, Passage@3: 89.29%)
- **Val Benchmark Section P@1:** **83.33%** (Section MRR: 0.8333, Doc P@1: 100.00%, Passage@3: 72.22%)
- **Protected Gold Benchmark Section P@1:** **37.84%** (up from 31.35%, MRR: 0.4013, Passage@3: 31.35% [3.6x relative increase])
- **Local In-Process Latency:** Median **2.41 ms** (CPU deterministic retrieval & synthesis)
- **Platform Regression Status:** **147 / 147 Tests Passed (100.0%)** across 10 comprehensive test suites (Phases 2–13).

---

## 5. Limitations & Future Scope

### Stated Limitations:
1. **Dialect Voice Models:** Open acoustic models for Dogri and Haryanvi do not exist in standard Indian speech libraries; written dialect text is preserved while audio playback falls back to Hindi.
2. **Dynamic Procedural Tracking:** Offline RAG provides authoritative statutory text and rights; active filing tracking requires live state registrar web portal sessions.

### Remediated in Phase 13:
1. **Corpus Expansion:** Statutory corpus expanded from 33 to 162 chunks, resolving section coverage blindspots for registration, tenure, audits, disputes, and penalties across Central, Punjab, Haryana, and J&K.
2. **Exact Section Boost:** Retrieval elevated to 87.50% P@1 on Dev benchmark with sub-2.5ms deterministic CPU execution.

### Future Scope:
1. Direct integration with State Registrar online MIS portals for automated society registration tracking.
2. Train acoustic voice models for Dogri and Haryanvi in collaboration with state agricultural universities.

---

## 6. Final Project Release Designation

- **Jury Demonstration (Offline / Standalone):** **APPROVED FOR RELEASE (GO)**
- **Restricted Staging Pilot (Cooperative Department):** **APPROVED FOR RELEASE (GO)**
- **Public Production Assistant:** **CONDITIONAL RELEASE (CONTROLLED PILOT ONLY)**  
  *Gated by mandatory statutory disclaimers and human registrar confirmation for formal filings.*
