# SahyogSetu — Comprehensive Jury Questions & Answers Guide

**Document Version:** 2.0.0  
**Date:** November 2026  
**Audience:** Project Presenters, Academic Reviewers, and Evaluators  

---

## 1. Project Motivation & Scope Questions

### Q1.1: Why did you choose cooperative governance instead of general legal advice?
**Answer:**  
In India, cooperative societies (PACS, dairy federations, urban cooperative banks) represent the backbone of the rural agricultural economy, serving over 290 million members. While mainstream legal tech focuses on High Court/Supreme Court litigation and commercial contract drafting, primary cooperative societies suffer from severe statutory neglect. PACS secretaries and committee members are governed by state-specific Cooperative Societies Acts and departmental circulars that are rarely available in accessible regional languages. By focusing specifically on cooperative governance, we solve an urgent real-world problem where misinformation directly leads to election disqualifications, audit penalties, and loan defaults.

### Q1.2: What makes SahyogSetu fundamentally different from ChatGPT, Claude, or Perplexity?
**Answer:**  
Commercial general-purpose LLMs operate as probabilistic next-token predictors. When queried on specialized statutory law, they routinely hallucinate:
1. They invent plausible-sounding section numbers (e.g. claiming Section 42 governs elections when Section 28 does).
2. They conflate state boundaries—frequently citing Punjab cooperative laws when asked about a society in Haryana.
3. They fabricate deadlines (e.g. inventing 30-day election filing windows) and produce generic, ungrounded summaries.
In contrast, SahyogSetu is an **evidence-first legal information system**:
- It retrieves actual statutory chunks from indexed official gazettes.
- It enforces strict territorial boundaries (0.00% cross-state leakage).
- It verifies citations against the physical corpus, guaranteeing a **0.00% citation hallucination rate**.
- If statutory evidence does not exist in the corpus, it abstains rather than inventing an answer.

---

## 2. Artificial Intelligence & Machine Learning Questions

### Q2.1: Why use Retrieval-Augmented Generation (RAG) instead of fine-tuning a Large Language Model?
**Answer:**  
Fine-tuning an LLM modifies its parametric weights. In the legal domain, parametric knowledge has major fatal flaws:
1. **Hallucination Persistence:** Fine-tuned models still hallucinate section numbers and provisions because knowledge remains probabilistic.
2. **Inability to Cite Direct Sources:** A fine-tuned weight cannot output a verified byte-level citation URL with an authentic page number from an official gazette.
3. **Temporal Invalidation:** When a state gazette amends an Act (e.g. Punjab's 2021 Amendment modifying committee terms), a fine-tuned model requires expensive, slow re-training.
RAG cleanly separates **reasoning** from **statutory memory**. Legal acts are stored as immutable, auditable chunks in the vector store. When an Act is amended, we simply update the chunk in `vectors.db` without retraining.

### Q2.2: What is the exact role of embeddings, and why did you select `all-MiniLM-L6-v2`?
**Answer:**  
Embeddings map natural language sentences into a continuous 384-dimensional dense semantic vector space $\mathbb{R}^{384}$. In legal queries, citizens rarely use formal statutory phrasing (e.g., a farmer asks *"how many years can our committee stay in office?"*, while the Act states *"the term of the committee shall be five years from the date of election"*). Semantic embeddings bridge this vocabulary mismatch by mapping both sentences to proximate coordinates in vector space. We selected `all-MiniLM-L6-v2` because it achieves strong semantic retrieval accuracy while computing in under **1.1 ms on a standard CPU**, enabling high-speed offline inference without requiring expensive GPU infrastructure.

### Q2.3: Why do you combine Dense Semantic Search and Keyword Search (Hybrid RRF)?
**Answer:**  
Semantic search and keyword search have complementary strengths:
- Semantic search understands conceptual intent and synonyms, but often blurs exact section numbers (treating "Section 28" and "Section 29" as almost identical vectors).
- Keyword search excels at exact statutory lexical matching (e.g. locating "Section 28", "surcharge", "OTS", or "arbitration"), but fails when users use colloquial synonyms.
We fuse both rank orders using **Reciprocal Rank Fusion (RRF)**:
$$\text{RRF\_Score}(d) = \frac{1.0}{60 + \text{rank}_{\text{semantic}}(d)} + \frac{0.9}{60 + \text{rank}_{\text{keyword}}(d)}$$
This guarantees that candidates containing both conceptual relevance and exact statutory section numbers are prioritized.

### Q2.4: What are the actual trained Machine Learning models in SahyogSetu?
**Answer:**  
SahyogSetu features three trained Scikit-learn models:
1. **User Query Intent Classifier (`intent_model.joblib`):** Word-level TF-IDF $(1,2)$ n-grams + `LinearSVC` trained on $N=243$ samples across 9 classes (Accuracy: **86.49%**, Test Macro F1: **0.8598**).
2. **Language Identifier (`language_model.joblib`):** Character n-gram TF-IDF $(2,5)$ + `LogisticRegression` trained on $N=125$ samples across 5 languages (Accuracy: **94.74%**, Test Macro F1: **0.9492**).
3. **News Sector Classifier (`news_model.joblib`):** TF-IDF $(1,2)$ n-grams + `LinearSVC` trained on $N=80$ samples across 10 categories (Accuracy: **91.67%**, Test Macro F1: **0.8800**).
All three models run locally on CPU in $< 0.3\text{ ms}$.

---

## 3. Legal Reliability & Grounding Questions

### Q3.1: How do you guarantee a 0.00% Citation Hallucination rate?
**Answer:**  
Every citation emitted by the system passes through the `CitationValidator` in `backend/rag/citation_validator.py`. Citations are NOT generated freely by an LLM. Instead:
1. Candidate citations are extracted strictly from the metadata of chunks physically retrieved from `vectors.db` for that specific query.
2. The validator cross-checks that the document title, issuing authority, and section exist in the retrieved evidence set.
3. It confirms that the source URL points to an authentic government endpoint (`.pdf` or `.gov.in`).
4. If an LLM or query refers to an unindexed citation, it is intercepted and stripped. Across all 454 citations emitted during the 220-query Gold Benchmark evaluation, 100% mapped to verified indexed gazettes (0.00% hallucination rate).

### Q3.2: How do you prevent cross-state legal contamination?
**Answer:**  
In Indian constitutional law, cooperative legislation is strictly territorial. A Punjab Act cannot govern a Haryana society. In Phase 10, adversarial testing revealed that prompts mentioning multiple states (`"Apply Punjab Act to Rohtak Haryana"`) leaked Punjab citations because the parser took the first matching token.
In Phase 11, we overhauled `JurisdictionResolver`:
1. It extracts all state tokens and central indicators across the entire query.
2. If hostile cross-state application is detected, it binds the query to the user's selected jurisdiction (`haryana`) and restricts allowed retrieval scopes to `["haryana", "central"]`, completely blocking Punjab documents.
3. If an interstate query is detected (*"operate in both Punjab and Haryana"*), it routes the query to `central` under the Central MSCS Act 2002.
4. In re-testing against the 20 hostile boundary cases, cross-state leakage dropped from 2.70% to **0.00%**.

### Q3.3: What happens when an unindexed legal section is queried?
**Answer:**  
SahyogSetu implements an **Evidence Gating & Abstention Gate**:
- If a citizen asks about a section not present in our 33 indexed chunks, or if the top reranking score is below $0.28$, the system triggers the **No-Evidence Abstention mechanism**.
- Rather than guessing or substituting unrelated provisions, it outputs: *"I could not find sufficient authoritative information in the available documents to answer this question."*
- In Phase 10 evaluation, this achieved **94.12% abstention accuracy** on out-of-scope topics.

---

## 4. Multilingual & Speech Processing Questions

### Q4.1: How do you support Punjabi and Hindi?
**Answer:**  
- **Text & Scripts:** We support native Devanagari (Hindi) and Gurmukhi (Punjabi). Our query processor uses script detection and entity-preserving translation, safeguarding statutory Act names, section numbers, and numerical limits while translating explanations.
- **Speech (ASR & TTS):** In browser environments, Speech-to-Text uses the client-side Web Speech API. For voice output, we provide offline parametric harmonic synthesizers and gTTS with local WAV caching in `tts_cache/`.

### Q4.2: Are Dogri and Haryanvi truly supported, or are you claiming capabilities that don't exist?
**Answer:**  
We are brutally honest: **no open acoustic voice models exist for Dogri or Haryanvi in standard Indian speech libraries**.
Rather than faking native voice models or claiming unsupported capabilities:
1. We render written answers in the vernacular Dogri or Haryanvi text.
2. For audio playback, we enforce our **Dialect Ethics Policy**: we transparently inform the citizen that native Dogri/Haryanvi voice models are unavailable, and offer an explicitly labelled Hindi audio alternative.
3. In our Language Capability Matrix, Dogri and Haryanvi are formally classified as `FALLBACK_AVAILABLE`, not `SUPPORTED_AND_VALIDATED`.

### Q4.3: What is the status of Bhashini integration?
**Answer:**  
SahyogSetu includes a complete MeitY Bhashini ULCA client adapter in `backend/services/bhashini/bhashini_client.py`. When valid MeitY credentials (`BHASHINI_USER_ID`, `BHASHINI_API_KEY`, `BHASHINI_INFERENCE_KEY`) are present in `.env`, the system queries live cloud pipeline endpoints. When credentials are not configured, the system operates gracefully in **ethical offline fallback mode** using local harmonic synthesizers and browser Web Speech. A mock synthesizer is never presented as a live Bhashini integration.

---

## 5. Engineering, Security & Operations Questions

### Q5.1: Why did you choose SQLite over PostgreSQL or a dedicated vector database like Pinecone or Milvus?
**Answer:**  
1. **Zero External Daemon Dependencies:** Primary cooperative societies and district offices often operate in constrained local environments with intermittent internet connectivity. SQLite requires zero server daemons, zero external socket configuration, and zero memory overhead.
2. **Unified Relational & Vector State:** Storing dense vector embeddings as 384-dimensional `BLOB`s in `vectors.db` and transactional state in `news.db` enables atomic hot backups using SQLite's native `backup()` API.
3. **Performance:** For a focused corpus of canonical statutory provisions, vectorized in-memory NumPy cosine similarity executes in **$< 1.5\text{ ms}$**, which is significantly faster than network round-trips to remote cloud vector databases.

### Q5.2: How do you secure the application against abuse and SSRF?
**Answer:**  
1. **SSRF Defense:** In `backend/services/news/source_verifier.py`, every news URL is evaluated before fetching: loopback addresses (`127.0.0.1`, `localhost`), cloud metadata endpoints (`169.254.169.254`), and private RFC1918 subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) are blocked.
2. **Rate Limiting:** In-memory sliding-window limiter restricts clients to 30 requests per minute.
3. **Upload Security:** Enforces a 15 MB boundary, validates `%PDF` magic bytes, and sanitizes filenames against path traversal.
4. **Privacy Scrubbing:** Server logs automatically redact 12-digit Aadhaar numbers, OTPs, and Bearer authorization tokens.

### Q5.3: How are backups and disaster recovery handled?
**Answer:**  
The script `backend/scripts/backup_restore.py` executes non-blocking hot SQLite snapshots using `sqlite3.connect().backup()`. It verifies source integrity with `PRAGMA integrity_check;`, computes SHA-256 hashes for all database files, records a `backup_manifest.json`, and allows atomic point-in-time restore with checksum verification before replacement.

---

## 6. Evaluation & Accuracy Questions

### Q6.1: Why is strict Section-Level Precision@1 only 31.35%?
**Answer:**  
This is an honest, scientifically grounded metric that reflects two factors:
1. **Unhinted Natural Queries:** Unlike artificial benchmarks where the query literally contains the section number (*"What does Section 28 say?"*), our 220-query Gold Benchmark uses realistic citizen phrasing (*"How many years can our managing committee stay in office?"*).
2. **Corpus Chunk Density:** Currently, our vector database indexes 33 canonical statutory chunks across 11 Acts. When a citizen asks about a broad statutory topic, the retrieval engine retrieves the governing Act in **63.24% of queries (`Doc-P@1`)**, but occasionally selects an adjacent section from the same Act.
Crucially, when an unindexed section is queried, the system's evidence-gating mechanism abstains rather than producing a hallucinated legal answer.

### Q6.2: What does 70.87% Claim Groundedness mean?
**Answer:**  
In our claim-level evaluation, every generated answer across all 220 benchmark queries was decomposed into atomic declarative claims (1,406 claims in total). Each claim was cross-referenced against the retrieved statutory chunks:
- **60.38% (849 claims)** were fully supported by statutory text.
- **20.98% (295 claims)** were partially supported (general procedural steps).
- **18.63% (262 claims)** were unsupported (general statutory context).
- **0.00% (0 claims)** were contradicted.
This yields an overall claim groundedness rate of **70.87%** with **zero legal contradictions**.

---

## 7. Future Improvements & Production Roadmap

### Q7.1: What are the immediate next steps before full statewide production deployment?
**Answer:**  
1. **Corpus Expansion:** Ingest all 120+ sections and subordinate rules for the Punjab, Haryana, and J&K Cooperative Societies Acts to raise section-level P@1 above 75%.
2. **Cooperative MIS Integration:** Connect to State Registrar online registration portals via authenticated APIs for real-time society application tracking.
3. **Acoustic Dialect Modeling:** Partner with regional institutions to record verified acoustic datasets for Dogri and Haryanvi.
4. **Human-in-the-Loop Verification:** Integrate an administrative review dashboard where designated legal registrars can audit citizen queries and approve newly released departmental circulars.
