# SahyogSetu — Final Technical Documentation

**Project Title:** SahyogSetu — Multilingual Cooperative Governance and Legal Information System  
**Document Version:** 2.1.0  
**Date:** November 2026 (Phase 13 Remediation)  
**Audience:** Academic Evaluators, Software Engineers, AI/ML Researchers, and Technical Committees  

---

## 1. Project Overview

SahyogSetu is an open-source, source-grounded multilingual legal information system and conversational assistant built for the Indian cooperative ecosystem. It assists primary agricultural credit societies (PACS), state cooperative departments, dairy/fisheries cooperatives, committee members, and smallholder farmers by answering queries related to cooperative legislation, bye-laws, elections, audits, disputes, and government welfare schemes.

The platform combines a 15-stage hybrid legal Retrieval-Augmented Generation (RAG) pipeline, multi-jurisdiction isolation guardrails, verified official government news aggregation, and multilingual speech services supporting English, Hindi, Punjabi (Gurmukhi), Dogri, and Haryanvi.

---

## 2. Problem Statement

India possesses one of the world's largest cooperative networks, comprising over 850,000 cooperative societies with over 290 million members. However, cooperative governance suffers from four fundamental informational bottlenecks:
1. **Statutory Fragmentation:** Cooperative law is a State Subject under Entry 32, List II of the Seventh Schedule of the Indian Constitution, while Multi-State Cooperatives are governed under Entry 44, List I by the Central MSCS Act 2002 (amended 2023). Society members frequently conflate Central and State provisions (e.g. applying Punjab election rules to a Haryana society).
2. **Linguistic and Literacy Barriers:** Rural PACS secretaries and farmer-members primarily communicate in regional Indian languages (Hindi, Punjabi, Dogri, Haryanvi). Official statutory acts and gazette notifications are predominantly drafted in complex legalistic English.
3. **Hallucination Risks in Generic LLMs:** Commercial general-purpose conversational models routinely invent non-existent statutory section numbers, hallucinate non-extendable committee tenures, fabricate application deadlines, or misattribute scheme subsidy limits.
4. **Information Asymmetry in Welfare Schemes:** Government announcements regarding PACS computerization (₹2,516 Cr), interest subvention (4% net rate via KCC), and crop insurance claims (PMFBY 72-hour window) fail to reach grassroots members in time due to fragmented departmental circulars.

---

## 3. Motivation

Cooperative governance directly impacts rural credit distribution, agricultural inputs, fertilizer subsidies, and milk procurement. When managing committees or members cannot easily access authoritative legal answers, societies face prolonged arbitration delays, election disputes, audit non-compliance, and vulnerability to financial irregularities. A strictly grounded, multilingual system with direct links to verified government gazettes bridges this critical governance gap.

---

## 4. Objectives

1. Develop a high-integrity legal retrieval pipeline that grounds answers exclusively in verified statutory acts and scheme master circulars.
2. Enforce strict territorial jurisdiction boundaries across Central, Punjab, Haryana, and Jammu & Kashmir legislation to eliminate cross-state legal contamination.
3. Eliminate hallucinated statutory citations and fabricated deadlines (targeting 0.00% citation hallucination rate).
4. Provide practical multilingual assistance across English, Hindi, Punjabi, Dogri, and Haryanvi with honest dialect transparency.
5. Aggregate and verify official cooperative sector announcements and circulars directly from verified government portals (`.gov.in`, `.nic.in`, PIB).
6. Deliver a production-hardened, containerized system with automated testing, non-blocking backups, and comprehensive monitoring.

---

## 5. Scope

### In-Scope:
- Multi-State Co-operative Societies Act, 2002 (amended 2023).
- Model Byelaws for Primary Agricultural Credit Societies (PACS).
- Punjab Cooperative Societies Act, 1961 (amended through 2021) and PADB OTS circulars.
- Haryana Co-operative Societies Act, 1984.
- Jammu & Kashmir Cooperative Societies Act, 1989.
- RBI Master Circular on Kisan Credit Card (KCC) and PMFBY Operational Guidelines.
- Official government news aggregation from 19 verified portals.
- 5 regional languages: English, Hindi, Punjabi, Dogri, Haryanvi.

### Out-of-Scope:
- Civil and criminal litigation advice outside cooperative society acts.
- Direct filing or automated submission of statutory petitions to the Registrar.
- Banking operations outside cooperative credit guidelines.

---

## 6. Target Users

1. **PACS Secretaries and Board Members:** Need precise procedural steps for membership admissions, managing committee elections, and annual audit filings.
2. **Smallholder Farmers & Cooperative Beneficiaries:** Require clarity on collateral-free crop loan limits (₹1.60 lakh), interest subventions, and PMFBY claim deadlines.
3. **District Cooperative Officers & Auditors:** Seek fast cross-referencing between State cooperative acts and Central Model Byelaws.
4. **Legal Aid & Rural Development Workers:** Require multi-state jurisdiction routing and vernacular explanations.

---

## 7. Functional Requirements

- **FR-1 (Legal Question Answering):** User submits a natural language query; system retrieves relevant provisions, checks evidence validity, and generates a structured 7-part legal answer.
- **FR-2 (Jurisdiction Selection & Enforcement):** User can select Central, Punjab, Haryana, J&K, or All; system blocks extraterritorial state laws from appearing in answers.
- **FR-3 (Source Grounding & Citation Validation):** Every answer must cite the document title, issuing authority, section number, page number, and direct government source URL.
- **FR-4 (Abstention on Out-of-Scope Queries):** If a query cannot be answered from authoritative indexed documents, the system must explicitly state that sufficient evidence was not found.
- **FR-5 (Multilingual Speech & Text):** Speech-to-text (ASR) input via browser Web Speech or Bhashini; Text-to-speech (TTS) playback in English, Hindi, and Punjabi; transparent dialect alternative notices for Dogri and Haryanvi.
- **FR-6 (Government News Aggregation):** Automated ingestion of verified circulars and press releases filtered by state, sector, and document type.
- **FR-7 (Conversation Persistence):** Session creation, message threading, thread renaming, and cascading deletion in SQLite.
- **FR-8 (Citizen Feedback):** Thumbs-up/down ratings and optional qualitative comments attached to specific conversation messages.

---

## 8. Non-Functional Requirements

- **NFR-1 (Citation Integrity):** 0.00% hallucinated citations across evaluation benchmarks.
- **NFR-2 (Jurisdiction Boundary):** 0.00% cross-state statutory leakage under hostile or ambiguous prompt phrasing.
- **NFR-3 (Latency):** Median end-to-end local CPU inference latency $< 10\text{ ms}$; external cloud LLM round-trip $< 2,000\text{ ms}$.
- **NFR-4 (Security):** Zero leakage of secret keys; 15 MB request ceiling; protection against SSRF, SQL injection, and prompt overrides.
- **NFR-5 (Reliability & Recovery):** Non-blocking hot SQLite snapshots with SHA-256 verification and atomic restoration.
- **NFR-6 (Container Security):** Execution under an unprivileged non-root user (UID 10001) in Docker.

---

## 9. System Architecture

SahyogSetu adopts a modular, 5-tier architecture:
1. **Client Tier:** React 19 SPA running in modern mobile and desktop browsers.
2. **Reverse Proxy & Edge Tier:** Nginx 1.27 handling security headers, static file serving, and API proxy forwarding.
3. **API & Service Tier:** FastAPI ASGI backend exposing domain-segregated REST routers.
4. **AI/ML & Knowledge Tier:** Dual hybrid retrieval engine (Dense embeddings + BM25 keyword matching) and Scikit-learn classifiers.
5. **Storage Tier:** SQLite 3 with WAL mode for relational state (`news.db`) and SQLite Vector BLOB store (`vectors.db`).

---

## 10. Technology Stack

| Layer | Component | Technology / Library | Version | Purpose |
|---|---|---|---|---|
| **Frontend** | Framework | React | 19.3.1 | Component-based UI |
| **Frontend** | Language | TypeScript | 7.0.2 | Static type safety |
| **Frontend** | Build Tool | Vite | 8.3.4 | Fast HMR & bundling |
| **Frontend** | Styling | Tailwind CSS | 4.0.0 | Utility-first styling |
| **Frontend** | Icons | Lucide React | 1.59.0 | Iconography |
| **Backend** | Framework | FastAPI | 0.162.0 | Async REST API |
| **Backend** | ASGI Server | Uvicorn | 0.54.0 | High-performance ASGI runtime |
| **Backend** | Validation | Pydantic | 2.14.3 | Data parsing & schema validation |
| **Backend** | Document Parsing | PyMuPDF (fitz) | 2.0.0 | PDF text & layout extraction |
| **Backend** | OCR Fallback | Tesseract / pytesseract | 0.3.13 | Scanned gazette extraction |
| **Backend** | ML & Vectors | Scikit-learn / NumPy / SciPy | 1.9.1 / 2.5.4 | Classifiers, TF-IDF, vector cosine |
| **Backend** | Relational DB | SQLite 3 | WAL Mode | Relational & vector BLOB persistence |
| **Backend** | Audio / TTS | gTTS / Harmonic Synthesizer | 2.5.4 | Multilingual speech synthesis |
| **Reverse Proxy** | Web Server | Nginx | 1.27 (Alpine) | Reverse proxy, SSL, security headers |
| **Containers** | Runtime | Docker & Docker Compose | 3.8 Spec | Isolated multi-stage execution |

---

## 11. Frontend Architecture

The frontend is organized under `frontend/src/` into functional modules:
- **`components/`**: Reusable UI elements (`ChatMessage.tsx`, `ChatInput.tsx`, `Header.tsx`, `Footer.tsx`, `TopicsHub.tsx`, `HistoryDrawer.tsx`, `CitationDrawer.tsx`, `DocumentUploadModal.tsx`, `GovernmentNewsSection.tsx`).
- **`services/`**: API client layer (`apiClient.ts`, `backendService.ts`, `legalBotService.ts`, `newsService.ts`, `SpeechInputService.ts`, `SpeechOutputService.ts`).
- **`config/`**: Brand settings, language metadata, jurisdiction filters, and checklist definitions.
- **State Management:** React hooks (`useState`, `useEffect`, `useCallback`, `useRef`) managing conversational state, audio playback queues, and active drawer modals without heavy Redux boilerplate.

---

## 12. Backend Architecture

The backend application entrypoint is `backend/main.py`. The application factory `create_app()` initializes:
1. **RequestTracingMiddleware:** Assigns `X-Request-ID` UUID headers and logs request execution time.
2. **RateLimitMiddleware:** Sliding-window in-memory limiter (30 req/min).
3. **CORSMiddleware:** Restricts origins according to environment configuration.
4. **Domain Routers:**
   - `/api/chat`: Grounded RAG query handler.
   - `/api/conversations`: Thread lifecycle, message history, renaming, cascading delete.
   - `/api/documents`: Citizen document analysis and administrative corpus ingestion.
   - `/api/news`: Faceted official news feed and administrative fetch triggers.
   - `/api/tts`: Audio synthesis, language capabilities, and WAV caching.
   - `/api/asr` & `/api/translate`: Speech transcription and entity-preserving translation.
   - `/api/health`: Comprehensive system health, liveness (`/api/health/live`), and readiness (`/api/health/ready`).

---

## 13. Database Design

### Relational Schema (`news.db`)
Enforces `PRAGMA foreign_keys = ON;` and `PRAGMA journal_mode = WAL;`.
- **`news_items`**: `news_id` (PK), `headline_original`, `description_original`, `full_text_original`, `source_name`, `source_type`, `source_url` (UNIQUE), `publication_date`, `fetched_at`, `jurisdiction`, `category`, `official_source_status`, `document_type`.
- **`news_sources`**: `source_id` (PK), `name`, `base_url`, `jurisdiction`, `source_type`, `is_active`, `is_official`.
- **`conversations`**: `conversation_id` (PK), `user_id`, `title`, `jurisdiction`, `language`, `created_at`, `updated_at`.
- **`messages`**: `message_id` (PK), `conversation_id` (FK $\to$ `conversations.conversation_id` ON DELETE CASCADE), `role`, `content`, `language`, `created_at`.
- **`feedback`**: `feedback_id` (PK), `message_id` (FK), `conversation_id` (FK), `rating` (`helpful`/`unhelpful`), `feedback_text`, `submitted_at`.
- **`uploaded_documents`**: `upload_id` (PK), `filename`, `file_size_bytes`, `mime_type`, `extracted_text`, `created_at`.

### Vector Schema (`vectors.db`)
- **`document_chunks`**: `chunk_id` (PK), `doc_id`, `document_title`, `document_type`, `issuing_body`, `jurisdiction`, `state`, `language`, `section`, `rule`, `page_start`, `page_end`, `source_url`, `chunk_text`, `embed_text`, `embedding_blob` (BLOB, 384 float32 values), `created_at`.
- **`indexed_documents`**: `doc_id` (PK), `document_title`, `jurisdiction`, `language`, `chunk_count`, `total_chars`, `source_url`, `status`, `indexed_at`.

---

## 14. Legal Document Processing

Legal acts feature strict hierarchical structures (Parts, Chapters, Sections, Subsections, Clauses, Rules, and Schedules). Standard sliding-window character chunking splits sections arbitrarily across chunks, severing statutory provisos from their governing clauses. SahyogSetu employs a domain-specific statutory parser that identifies section boundaries using regular expressions (`Section \d+[A-Z]?`, `Rule \d+`).

---

## 15. Optical Character Recognition (OCR)

Official Indian state gazettes (e.g. Punjab Government Gazettes from 1961) often exist as scanned image PDFs.
1. PyMuPDF attempts digital stream extraction.
2. If character density is $< 50$ characters per page, Tesseract OCR (`pytesseract`) is automatically invoked using Otsu adaptive thresholding and deskewing.
3. Extracted text undergoes character normalization (fixing broken Indic conjuncts and legal ligatures).

---

## 16. Document Chunking Strategy

Rather than naive fixed 500-token slicing, chunks are anchored to **statutory provision boundaries**:
- Each chunk encapsulates an entire legal Section or Rule along with its immediate sub-clauses and explanations.
- Chunk metadata stores: `document_title`, `section`, `rule`, `page_start`, `page_end`, `jurisdiction`, `issuing_body`, and `source_url`.
- Result: 162 canonical statutory chunks indexing complete operational provisions across 11 Acts and Schemes (+390.9% corpus expansion in Phase 13).

---

## 17. Embeddings and Vector Database

- **Embedding Model:** Dense 384-dimensional dense vectors generated via `sentence-transformers/all-MiniLM-L6-v2`.
- **Storage:** Stored as raw IEEE 754 float32 byte buffers (`BLOB`) in SQLite (`vectors.db`).
- **Similarity Search:** Query vectors are normalized; cosine similarity against stored BLOBs is computed in memory via vectorized NumPy dot products, filtering by `allowed_jurisdictions`.

---

## 18. Legal RAG Pipeline

The RAG workflow proceeds through 15 synchronous stages:
1. **Query Normalization:** Strips hostile delimiters and normalizes whitespace.
2. **Language Detection:** Identifies script and language code.
3. **Intent Extraction:** Classifies query into one of 9 legal categories.
4. **Section Parsing:** Identifies referenced section numbers (e.g., "Section 28").
5. **Jurisdiction Resolution:** Determines applicable territorial scope.
6. **Query Dense Embedding:** Computes 384-dimensional query vector.
7. **Semantic Search:** Retrieves top vector candidates from `vectors.db`.
8. **Statutory Keyword Search:** Retrieves candidates matching section numbers or key legal tokens.
9. **Reciprocal Rank Fusion (RRF):** Merges semantic and keyword candidates ($k=60$).
10. **Legal Domain Reranking:** Applies section, jurisdiction, and intent boosts.
11. **Evidence Gating:** Checks if candidate scores exceed threshold $0.28$; triggers abstention if ungrounded.
12. **Context Construction:** Deduplicates passages and builds structured context prompt.
13. **Answer Generation:** Deterministic statutory synthesizer structures a 7-part legal explanation.
14. **Citation Validation:** Validates that citations exist in retrieved chunks with direct URLs.
15. **Multilingual Rendering:** Outputs answer in requested language with audio links.

---

## 19. Jurisdiction Resolution & Territorial Boundary Enforcement

Implemented in `backend/rag/jurisdiction_resolver.py`:
- Indian cooperative legislation is state-specific. Extraterritorial application is strictly illegal (a Punjab statute has no legal effect on a Haryana PACS).
- Resolver scans all mentioned state tokens and central indicators:
  - If a prompt attempts hostile cross-state application (e.g. `jur_hostile_01`: *"Apply Punjab Act to Rohtak Haryana"*), the resolver detects the user's jurisdiction (`haryana`), restricts allowed retrieval to `["haryana", "central"]`, and completely blocks Punjab statutes.
  - If a prompt inquires about multi-state operations (e.g. *"operate in both Punjab and Haryana"*), the resolver assigns `central` under the Central MSCS Act 2002.
  - If a state-dependent query is submitted with `all` selected, the system triggers a **Jurisdiction Clarification Prompt**.
- Result: **0.00% cross-state statutory leakage** across 20 hostile test cases.

---

## 20. Multilingual Processing

SahyogSetu defines an explicit, honest Language Capability Matrix:
- **English (`en`):** `SUPPORTED_AND_VALIDATED` — Primary statutory grounding and synthesis.
- **Hindi (`hi`):** `SUPPORTED_WITH_LIMITATIONS` — Devanagari NMT, Google Speech/Bhashini ASR, Harmonic TTS fallback.
- **Punjabi (`pa`):** `SUPPORTED_WITH_LIMITATIONS` — Native Gurmukhi script processing, Gurmukhi voice synthesis, offline fallback.
- **Dogri (`doi`):** `FALLBACK_AVAILABLE` — Vernacular Devanagari text preserved; transparent Hindi audio alternative provided.
- **Haryanvi (`bgc`):** `FALLBACK_AVAILABLE` — Regional vernacular text preserved; transparent Hindi audio alternative provided.

---

## 21. Machine Learning Components

Three Scikit-learn models are deployed under `backend/ml/models/`:
1. **User Query Intent Classifier (`intent_model.joblib`):** TF-IDF + LinearSVC classifying queries into 9 categories (Accuracy: **86.49%**, Test Macro F1: **0.8598**).
2. **Language Identifier (`language_model.joblib`):** Character n-gram TF-IDF + LogisticRegression classifying Indic scripts across 5 languages (Accuracy: **94.74%**, Test Macro F1: **0.9492**).
3. **News Sector Classifier (`news_model.joblib`):** TF-IDF + LinearSVC classifying government updates into 10 cooperative sectors (Accuracy: **91.67%**, Test Macro F1: **0.8800**).

---

## 22. Government News Aggregation

Implemented in `backend/services/news/`:
- Ingests official announcements from 19 registered government sources (Ministry of Cooperation, PIB, State Cooperative Departments).
- **SSRF Guard:** Rejects loopback (`127.0.0.1`), cloud metadata (`169.254.169.254`), and private subnets before fetching.
- **Source Verification:** Every news record requires a direct government source URL (`.gov.in`, `.nic.in`, or PIB release).
- Current database: **29 verified official records** (Punjab: 22, Central: 4, Haryana: 2, J&K: 1).

---

## 23. API Architecture

REST endpoints are documented via OpenAPI 3.0 at `/docs`:
- `POST /api/chat`: Grounded legal query processing.
- `GET /api/conversations`: Conversation thread list.
- `POST /api/conversations`: Create conversation session.
- `GET /api/conversations/{id}`: Retrieve message history.
- `DELETE /api/conversations/{id}`: Cascading deletion.
- `POST /api/feedback`: Citizen rating submission.
- `GET /api/news`: Faceted news discovery.
- `POST /api/tts/generate`: Speech synthesis.
- `GET /api/tts/audio/{id}`: Audio stream retrieval.
- `GET /api/asr/capabilities`: Honest dialect capability disclosure.
- `GET /api/health/live`: Process liveness probe.
- `GET /api/health/ready`: Readiness probe (DB, knowledge store, vector store).

---

## 24. Security and Privacy

Hardened in Phase 9 and Phase 11:
- **SSRF Defense:** Evaluates target host IPs; rejects private RFC1918 subnets and cloud metadata endpoints.
- **Rate Limiting:** Sliding-window limiter restricts abuse to 30 requests/minute per client IP.
- **Input Sanitization:** Strips prompt injection delimiters (`<system>`, `OVERRIDE`, `IGNORE PRIOR INSTRUCTIONS`).
- **File Upload Protection:** Validates `%PDF` magic bytes, sanitizes filenames against directory traversal (`../../etc/passwd`), and enforces 15 MB ceiling.
- **Real-Time Privacy Scrubbing:** Redacts 12-digit Aadhaar numbers, 6-digit OTPs, and Bearer tokens from server logs.
- **Admin Authentication:** Protected routes (`/api/news/trigger-fetch`, `/api/documents/ingest`) require `X-Admin-Key`.

---

## 25. Deployment Architecture

- **Containerization:** Multi-stage `Dockerfile` with dedicated non-root user `appuser` (UID 10001).
- **Orchestration:** `docker-compose.yml` deploying `backend` (FastAPI/Uvicorn) and `nginx` (Alpine Nginx).
- **Persistent Storage:** Host volume `sahyogsetu_data` mounted at `/app/backend/data`.
- **Reverse Proxy:** Hardened Nginx configuration enforcing 15 MB upload limit, CSP, HSTS, and X-Frame-Options.
- **Disaster Recovery:** `backend/scripts/backup_restore.py` providing hot SQLite online snapshots with SHA-256 verification.

---

## 26. Testing Strategy

The test suite contains 9 test modules spanning all phases:
- `test_phase2_backend.py` (Database integrity and schemas)
- `test_phase3_ingestion.py` (Document extraction and chunking)
- `test_phase4_rag.py` (Retrieval precision and citation validation)
- `test_phase5_bhashini.py` (Translation, ASR, and TTS)
- `test_phase6_ml.py` (Intent, language, and news ML classifiers)
- `test_phase7_news.py` (Official news aggregation and SSRF safety)
- `test_phase8_integration.py` (Full citizen user journeys 1 through 9)
- `test_phase9_security.py` (Security hardening, rate limiting, and log scrubbing)
- `test_phase11_deployment.py` (Deployment validation, health probes, hot backup/restore)
- **Status:** **102 / 102 Tests Passed (100.0%)**.

---

## 27. Evaluation Methodology

Evaluated in Phase 10 against an untouched, independent **220-Query Gold Benchmark Dataset** (`gold_benchmark_dataset.json` / `.csv`):
- Category A: Legal Cooperative Governance (70 queries)
- Category B: Government Schemes & Subsidies (50 queries)
- Category C: Cross-Jurisdiction & Multi-State (35 queries)
- Category D: Unsupported, Out-of-Scope & Adversarial (35 queries)
- Category E: Multilingual Vernacular (30 queries)
- Every query verified against official gazettes, acts, or RBI circulars.

---

## 28. Evaluation Results Summary

- **Retrieval P@1 (Strict Section Level):** **31.35%** (MRR: 0.3604, Recall@3: 41.08%)
- **Retrieval P@1 (Document Level):** **63.24%**
- **Citation Hallucination Rate:** **0.00% (0 / 454 citations fabricated)**
- **Contradicted Claim Rate:** **0.00% (0 / 1,406 claims contradicted)**
- **Claim Groundedness Rate:** **70.87%**
- **Abstention Accuracy on Out-of-Scope Queries:** **94.12%**
- **Jurisdiction Boundary Decision Accuracy:** **100.00% (20 / 20)**
- **Cross-State Statutory Leakage Rate:** **0.00%**
- **Median End-to-End Local CPU Latency:** **5.35 ms**

---

## 29. Limitations

1. **Section-Level Retrieval Density:** The vector database indexes 162 canonical statutory chunks across 11 Acts and Schemes (expanded from 33 chunks in Phase 13), providing dense coverage of registration, governance, elections, audit, financial assistance, and crop insurance. While core governance provisions (e.g. Section 28 committee tenure, Section 8 registration, Section 55 disputes) are indexed, questions about unindexed niche provisions trigger abstention rather than detailed advice.
2. **Dialect Voice Models:** No open acoustic voice models exist for Dogri or Haryanvi in standard Indian speech libraries. Speech playback for these dialects transparently falls back to Hindi.
3. **Offline Mode Dependency:** When deployed fully offline without external API keys (Gemini/OpenAI/Bhashini), conversational synthesis uses the deterministic statutory template rather than fluid LLM paraphrasing.

---

## 30. Future Improvements

1. **Corpus Expansion:** Ingest all 120+ sections and state rules for Punjab, Haryana, and J&K acts.
2. **Fine-Tuned Indic Embeddings:** Integrate domain-adapted Indic legal bi-encoders (e.g. IndicBERT-Legal).
3. **Live Departmental API Integrations:** Connect directly to State Registrar MIS portals for real-time society registration status tracking.
4. **ASR Dialect Acoustic Modeling:** Train regional acoustic models for Dogri and Haryanvi with state agricultural universities.

---

## 31. Conclusion

SahyogSetu demonstrates that domain-specific, source-grounded AI systems can successfully deliver legal information to grassroots cooperative communities without fabricating citations, hallucinating compliance rules, or leaking cross-state legislation. By prioritizing territorial boundaries, verified government sources, and transparent multilingual capability reporting, SahyogSetu establishes an authoritative foundation for digital cooperative governance in India.
