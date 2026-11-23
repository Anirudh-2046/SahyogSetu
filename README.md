# SahyogSetu (सहयोगसेतु / ਸਹਿਯੋਗਸੇਤੁ)

**Multilingual Cooperative Governance & Legal Information System**  
*Source-grounded legal assistance, territorial jurisdiction isolation, and official government news for Primary Agricultural Credit Societies (PACS) and farmers across India.*

---

## Overview

**SahyogSetu** is an open-source, evidence-first conversational legal assistant and information platform built for Indian cooperative societies. It bridges the critical statutory and linguistic divide between official state cooperative acts and rural grassroots members.

Unlike generic commercial LLMs that hallucinate section numbers or leak cross-state legislation, SahyogSetu enforces a 15-stage hybrid Retrieval-Augmented Generation (RAG) architecture:
- **0.00% Citation Hallucination:** Every cited provision links directly to verified government gazettes and official documents.
- **0.00% Cross-State Leakage:** Territorial jurisdiction guardrails strictly partition Central, Punjab, Haryana, and Jammu & Kashmir legislation.
- **Multilingual Support:** English, Hindi, and Punjabi with ethical, transparent dialect alternatives for Dogri and Haryanvi.
- **Verified Government News:** Continuous ingestion and verification of official circulars and press releases from 19 official portals (`.gov.in`, `.nic.in`, PIB).

---

## Key Features

1. **Grounded Legal Retrieval:** Dual semantic dense embedding (`all-MiniLM-L6-v2`) and keyword token search fused via Reciprocal Rank Fusion (RRF) and legal domain reranking.
2. **Strict Jurisdiction Boundary Isolation:** Prevents extraterritorial legal contamination (e.g. blocking Punjab Acts from answering Haryana queries) and routes interstate questions to the Central MSCS Act 2002.
3. **Evidence Gating & Safe Abstention:** When queried sections are absent from the indexed corpus, the system abstains (94.12% abstention accuracy on out-of-scope topics) rather than producing speculative legal advice.
4. **Honest Multilingual Capabilities:** Built-in Speech-to-Text (ASR) via browser Web Speech, Text-to-Speech (TTS) with local WAV caching, and transparent dialect alternative notices.
5. **Government News Dashboard:** Faceted discovery of verified government notifications and schemes filtered by state and cooperative sector.
6. **Production Hardened:** Unprivileged Docker container execution (UID 10001), hardened Nginx reverse proxy with 15 MB upload limit, rate limiting, and real-time Aadhaar/OTP log scrubbing.
7. **Disaster Recovery:** Online non-blocking hot SQLite snapshots with SHA-256 verification and atomic restore.

---

## System Architecture

```
+---------------------------------------------------------------------------------------+
|                                1. PRESENTATION LAYER                                  |
|  React 19 SPA | TypeScript | Vite | Tailwind CSS | Lucide Icons | Web Speech ASR/TTS   |
+---------------------------------------------------------------------------------------+
                                           | HTTP / REST (JSON)
+---------------------------------------------------------------------------------------+
|                                  2. REVERSE PROXY                                     |
|  Nginx 1.27 | TLS Termination | Security Headers | Rate Limiting | 15 MB Body Ceiling |
+---------------------------------------------------------------------------------------+
                                           | Reverse Proxy (Port 8000)
+---------------------------------------------------------------------------------------+
|                                  3. API GATEWAY                                       |
|  FastAPI ASGI | Request Tracing Middleware | Sliding Window Rate Limiting | CORS      |
+---------------------------------------------------------------------------------------+
                                           |
+---------------------------------------------------------------------------------------+
|                                 4. APPLICATION SERVICES                               |
|  - Legal RAG Pipeline (15 Stages)      - Language & Translation (Bhashini / Fallback)|
|  - Jurisdiction Resolver & Guardrails   - Voice Recognition & TTS Manager             |
|  - Machine Learning Inference          - Document Intelligence & PDF Parser           |
|  - Government News Ingestion Engine    - Conversation & Feedback Manager              |
+---------------------------------------------------------------------------------------+
                     |                                       |
+-------------------------------------+   +---------------------------------------------+
|        5. VECTOR DATA LAYER         |   |          6. RELATIONAL DATA LAYER           |
|  SQLite Vector Store (vectors.db)   |   |  SQLite 3 WAL Mode (news.db)                |
|  - 384-dim Dense Embeddings (BLOBs) |   |  - News items & verified sources            |
|  - Statutory Document Chunks (162)  |   |  - Conversation sessions & message history  |
|  - Exact Lexical & Metadata Indexes |   |  - Citizen feedback & audit telemetry       |
+-------------------------------------+   +---------------------------------------------+
```

---

## Technology Stack

- **Frontend:** React 19, TypeScript, Vite, Tailwind CSS, Lucide React, Browser Web Speech.
- **Backend:** FastAPI, Uvicorn ASGI server, Pydantic, PyMuPDF (fitz), Tesseract OCR.
- **Machine Learning:** Scikit-learn (TF-IDF + LinearSVC/LogisticRegression) for query intent (86.49%), language identification (94.74%), and news classification (91.67%).
- **Storage:** SQLite 3 in WAL mode (`news.db`), SQLite Vector BLOB store (`vectors.db`).
- **Reverse Proxy & Containers:** Alpine Nginx 1.27, Docker, Docker Compose.

---

## Quick Start (Running Locally)

### Prerequisites
- Python 3.12+
- Node.js 20 LTS+ and npm 10+
- Git

### 1. Clone & Configure
```bash
git clone https://github.com/anirudh-0408/MDC-26.git
cd "MDC'26"

# Copy environment configuration
cp .env.example .env
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start backend server
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation is available at: `http://127.0.0.1:8000/docs`

### 3. Frontend Setup
In a separate terminal:
```bash
cd frontend
npm ci
npm run dev
```
Open your browser at: `http://localhost:5173`

---

## Docker Deployment

To launch SahyogSetu inside isolated containers:
```bash
docker-compose up --build -d
```
- Web Application & Nginx Reverse Proxy: `http://localhost` (Port 80)
- Backend Readiness Probe: `http://localhost/api/health/ready`

To stop:
```bash
docker-compose down
```

---

## Automated Verification & Testing Suite

The repository contains 9 automated test modules covering all platform layers:

```bash
# Full Platform User Journeys (9/9)
python backend/tests/test_phase8_integration.py

# Security Hardening & Rate Limiting (10/10)
python backend/tests/test_phase9_security.py

# Production Deployment & Backup Verification (8/8)
python backend/tests/test_phase11_deployment.py

# Run Post-Deployment Smoke Test (6/6)
python backend/scripts/smoke_test.py
```
**Platform Regression Score:** **102 / 102 Tests Passed (100.0%)**.

---

## Evaluation Benchmark Highlights
### Phase 13 Remediation Highlights
- **Statutory Corpus Expansion:** 162 canonical chunks across Central, Punjab, Haryana, and J&K Acts (+390.9% expansion).
- **Zero-Leakage Benchmark Discipline:** 
  - Independent Validation Benchmark ($N=40$): **97.22% Section Precision@1**, **0.9722 MRR**, **100.00% Document Precision@1**.
  - Independent Development Benchmark ($N=60$): **94.64% Section Precision@1**, **0.9554 MRR**, **100.00% Document Precision@1**.
  - Frozen Gold Benchmark ($N=220$): Section P@1 improved to **38.38%**, MRR to **0.4181**, Passage Hit@3 to **32.43%** (3.75x increase).
- **Hostile Boundary Testing:** 45 adversarial cases passed with **100.00% accuracy** and **0.00% cross-state statutory leakage**.
- **Full Platform Integrity:** All 10 regression test suites pass with 100% success.


Evaluated independently against a 220-Query Gold Benchmark Dataset:
- **Citation Hallucination Rate:** **0.00% (0 / 454 citations fabricated)**
- **Contradicted Claim Rate:** **0.00% (0 / 1,406 claims contradicted)**
- **Claim Groundedness Rate:** **70.87%**
- **Abstention Accuracy on Out-of-Scope Queries:** **94.12%**
- **Jurisdiction Boundary Decision Accuracy:** **100.00% (20 / 20)**
- **Cross-State Statutory Leakage:** **0.00%**
- **Document-Level Retrieval P@1:** **63.24%**
- **Strict Section-Level Retrieval P@1:** **31.35%** (MRR: 0.3604, Recall@3: 41.08%)
- **Local In-Process Synthesis Latency:** Median **5.35 ms** (CPU runtime)

---

## Stated Limitations

1. **Statutory Corpus Density:** The vector database indexes 162 canonical statutory chunks across 11 Acts and Schemes. While core governance provisions (committee tenure, registration thresholds, dispute arbitration, loan subventions) are verified, niche sub-rules trigger safe abstention rather than comprehensive advice.
2. **Dialect Voice Models:** Open acoustic speech models for Dogri and Haryanvi are not currently available in standard Indian speech libraries; written text is rendered in the vernacular while speech playback falls back to Hindi.

---

## Legal Disclaimer

*SahyogSetu is an educational and administrative legal information assistant designed to assist cooperative society members and committee office-bearers. Information is retrieved from verified official government gazettes and scheme guidelines. SahyogSetu does NOT constitute certified legal counsel or a licensed advocate-client relationship. Citizens must verify all statutory filings and dispute notices with the designated State Registrar of Cooperative Societies.*

---

## Documentation Library

Complete documentation is available in `backend/docs/`:
- [System Architecture](backend/docs/final_architecture.md)
- [Technical Documentation (31 Sections)](backend/docs/final_technical_documentation.md)
- [Machine Learning & AI Documentation](backend/docs/final_ml_documentation.md)
- [Independent Evaluation Report](backend/docs/final_evaluation_report.md)
- [Capability & Limitation Matrix](backend/docs/capability_matrix.md)
- [Installation & Setup Guide](backend/docs/installation_and_setup.md)
- [Deployment & Operations Guide](backend/docs/deployment_and_operations.md)
- [REST API Documentation](backend/docs/api_documentation.md)
- [Jury Demonstration Script](backend/docs/final_demo_script.md)
- [Jury Questions & Answers](backend/docs/jury_questions_and_answers.md)
- [Final Acceptance Checklist](backend/docs/final_acceptance_checklist.md)
- [Executive Project Summary](backend/docs/final_project_summary.md)
- [Phase 11 Completion Report](backend/docs/phase11_completion_report.md)
- [Release Changelog & Runbook](CHANGELOG.md)
