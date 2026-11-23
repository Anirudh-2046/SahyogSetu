# SahyogSetu — Final System Architecture Documentation

**Document Version:** 2.1.0  
**Date:** November 2026 (Phase 13 Remediation) (Phase 13 Remediation)  
**Project:** SahyogSetu — Multilingual Cooperative Governance & Legal Assistance System  
**Audience:** System Architects, Academic Evaluators, Senior Software Engineers, and Operations Teams  

---

## 1. System Overview

SahyogSetu is a domain-specific, source-grounded multilingual legal information system and conversational assistant designed for Indian primary cooperative societies (PACS), state cooperative departments, dairy/fishery cooperatives, and farming communities.

Unlike open-domain conversational models that speculate or produce hallucinated statutory interpretations, SahyogSetu enforces a **strict evidence-first Retrieval-Augmented Generation (RAG) architecture**. Every emitted legal interpretation or compliance procedure is explicitly tethered to verified statutory gazettes, parliamentary acts, departmental notifications, or scheme master circulars across four defined jurisdictions:
1. **Central Jurisdiction:** Multi-State Co-operative Societies Act 2002 (amended 2023), Model Byelaws for PACS, RBI Kisan Credit Card (KCC) Master Circulars, and PMFBY Guidelines.
2. **Punjab Jurisdiction:** Punjab Cooperative Societies Act 1961 (amended through 2021), PADB One-Time Settlement (OTS) Guidelines, and Cooperative Department Circulars.
3. **Haryana Jurisdiction:** Haryana Co-operative Societies Act 1984.
4. **Jammu & Kashmir Jurisdiction:** Jammu & Kashmir Cooperative Societies Act 1989.

---

## 2. Architectural Layers

SahyogSetu is structured into decoupled, modular architectural layers:

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
|  - RAG Retrieval & Orchestration       - Language & Translation (Bhashini / Fallback)|
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

### Detailed Layer Specifications:
1. **Presentation Layer (Frontend):**
   - Single-Page Application (SPA) built with React 19, TypeScript, and Vite.
   - Core interfaces: Chat interface with markdown parsing, jurisdiction dropdown (Central, Punjab, Haryana, J&K), language selector (English, Hindi, Punjabi, Dogri, Haryanvi), citation drawer, document upload modal, and government news dashboard.
   - Client-side audio handling: Browser Web Speech API for voice input; HTML5 Audio streaming for neural and harmonic TTS output.
2. **Reverse Proxy Layer (Nginx):**
   - Hardened Alpine Nginx instance acting as reverse proxy and static asset server.
   - Injects security headers (`X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff`, `Content-Security-Policy`, `Permissions-Policy`).
   - Limits client request payloads to 15 MB to match application boundaries.
   - Forwards client IP headers (`X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`).
3. **API Gateway Layer (FastAPI):**
   - Asynchronous Python REST API running under Uvicorn ASGI server.
   - Request tracing middleware attaches unique UUID correlation IDs to every request.
   - Sliding-window rate limiter prevents API abuse (30 requests/minute per IP with `Retry-After: 60s`).
   - Global exception handlers catch domain exceptions (`EntityNotFoundException`, `ValidationException`, `FileTooLargeException`) and return safe structured error envelopes.
4. **Application Services Layer:**
   - **Legal RAG Pipeline:** 15-stage retrieval and answer generation pipeline.
   - **Jurisdiction Resolver:** Multi-state detection, extraterritorial application blocking, and clarification trigger engine.
   - **Language Services:** Transparent router supporting Bhashini ULCA cloud endpoints when configured, with offline fallback synthesizers and Web Speech.
   - **ML Inference Engines:** Scikit-learn TF-IDF + LinearSVC/LogisticRegression models for intent classification, news relevance, and language identification.
   - **News Ingestion Engine:** Periodic collector with SSRF-protected HTTP fetching, official source verification, and duplicate detection.
5. **Data Layers:**
   - **Relational Store (`news.db`):** SQLite 3 with Write-Ahead Logging (`PRAGMA journal_mode=WAL;`) and strict foreign key integrity (`PRAGMA foreign_keys=ON;`). Stores news items, news sources, conversations, messages, feedback ratings, and document uploads.
   - **Vector Store (`vectors.db`):** Stores 162 canonical statutory chunks across 11 indexed Acts and Schemes (Central: 24, Punjab: 51, Haryana: 26, J&K: 26, plus schemes) with 384-dimensional dense embeddings stored as binary BLOBs alongside complete 24-field structured statutory metadata (doc_id, section, rule, jurisdiction, page, source_url).

---

## 3. Architectural Diagrams

### 3.1 High-Level System Architecture

```mermaid
flowchart TD
    subgraph Client["Client Browser / Citizen Interface"]
        UI["React 19 Single Page App"]
        SpeechIn["Web Speech ASR (Microphone)"]
        AudioOut["HTML5 Audio Player"]
    end

    subgraph Proxy["Reverse Proxy & Gateway"]
        Nginx["Nginx Reverse Proxy (Port 80/443)"]
    end

    subgraph BackendApp["FastAPI Application Server"]
        Router["API Gateway / Routers"]
        RateLimiter["Sliding-Window Rate Limiter"]
        Tracing["Request Tracing (UUID)"]
        
        subgraph CoreServices["Domain Services"]
            RAG["Legal RAG Pipeline"]
            JurRes["Jurisdiction Resolver"]
            LangSvc["Multilingual Language Service"]
            MLInference["ML Classifiers (Intent, News, Lang)"]
            NewsSvc["Government News Pipeline"]
            ConvSvc["Conversation Manager"]
        end
    end

    subgraph Storage["Persistent Storage Layer"]
        NewsDB[("news.db (SQLite WAL)\nConversations, News, Feedback")]
        VectorDB[("vectors.db (SQLite BLOBs)\n162 Statutory Chunks & Embeddings")]
        TTSCache[("tts_cache/\nAudio WAV Files")]
    end

    subgraph External["External Cloud Services (Optional)"]
        Bhashini["MeitY Bhashini ULCA Cluster"]
        CloudLLM["Google Gemini / OpenAI"]
        OfficialGov["Official Portals (.gov.in / .nic.in)"]
    end

    UI <-->|HTTP / REST| Nginx
    SpeechIn -.->|Client-side transcription| UI
    Nginx <-->|Proxy pass /api/| Router
    Router --> RateLimiter --> Tracing --> CoreServices
    
    RAG --> JurRes
    RAG --> MLInference
    RAG <--> VectorDB
    RAG -.-> CloudLLM
    
    LangSvc -.-> Bhashini
    LangSvc --> TTSCache
    AudioOut <-->|Stream /api/tts/audio| Router
    
    NewsSvc -.-> OfficialGov
    NewsSvc <--> NewsDB
    ConvSvc <--> NewsDB
```

---

### 3.2 Legal Document Ingestion Pipeline

```mermaid
flowchart LR
    Doc["Official Gazette / Statutory Act (PDF)"] --> Validate["Magic-Byte & Extension Validation (%PDF)"]
    Validate --> Extract["PyMuPDF (fitz) Text & Layout Extraction"]
    Extract --> OCR["Tesseract OCR Fallback (Scanned Gazettes)"]
    OCR --> Clean["Text Normalization & Noise Filtering"]
    Clean --> Chunk["Statutory Chunking (Section, Rule, Schedule)"]
    Chunk --> Metadata["Metadata Enrichment (Act, Authority, Year, URL)"]
    Metadata --> Embed["Dense Vector Embedding (384-dim all-MiniLM-L6-v2)"]
    Embed --> Store[("SQLite Vector Store (vectors.db)\nBLOB storage + SQL indexing")]
```

---

### 3.3 Legal RAG Query & Answer Generation Pipeline

```mermaid
sequenceDiagram
    autonumber
    actor User as Citizen / Cooperative Member
    participant UI as React Frontend
    participant API as FastAPI Gateway
    participant Jur as Jurisdiction Resolver
    participant RAG as Legal RAG Pipeline
    participant VecStore as Vector Store (vectors.db)
    participant Rerank as Legal Domain Reranker
    participant Gen as Answer Generator
    participant Val as Citation Validator

    User->>UI: Submit Question ("What is committee tenure in Haryana under Section 28?")
    UI->>API: POST /api/chat {query, jurisdiction: "haryana", language: "en"}
    API->>RAG: run_sync(query, user_jurisdiction, user_language)
    
    RAG->>Jur: resolve(query, user_jurisdiction)
    Jur-->>RAG: {target: "haryana", allowed: ["haryana", "central"]}
    
    RAG->>VecStore: Dual Search: Semantic (Vector Cosine) + Keyword (Section/Lexical)
    VecStore-->>RAG: Top-35 Candidate Chunks (Fused via RRF k=60.0, keyword weight 1.1)
    
    RAG->>Rerank: Rerank candidates by Section Match + Jurisdiction + Intent Boost
    Rerank-->>RAG: Top-5 Re-ranked Chunks
    
    RAG->>Gen: Synthesize Answer (Evidence-First Grounding)
    Gen->>Val: Validate citations against corpus & check direct URLs
    Val-->>Gen: Validated citation metadata blocks
    Gen-->>RAG: Structured 7-part legal response
    
    RAG-->>API: Response payload with citations and uncertainty status
    API-->>UI: JSON response
    UI-->>User: Display answer, official source URLs, and audio playback button
```

---

### 3.4 Jurisdiction-Aware Retrieval & Territorial Boundary Flow

```mermaid
flowchart TD
    Q["User Query Received"] --> DetectTokens["Extract All Mentioned States & Indicators"]
    DetectTokens --> CheckMSCS{"Explicit MSCS or\nMulti-State Query?"}
    
    CheckMSCS -- Yes --> ResolveCentral["Resolve Target = 'central'\nAllowed = ['central']"]
    CheckMSCS -- No --> CheckMultiStates{"Multiple States\nMentioned in Query?"}
    
    CheckMultiStates -- Interstate Operation --> RouteCentral["Resolve Target = 'central'\n(MSCS Act 2002 governs interstate societies)"]
    CheckMultiStates -- Hostile Extraterritorial --> BindUser["Bind to User Selected Jurisdiction\n(Extraterritorial application blocked)"]
    
    CheckMultiStates -- No (Single State) --> MatchSingle["Resolve Target = Detected State\nAllowed = [State, 'central']"]
    
    CheckMultiStates -- No State Detected --> CheckDropdown{"User Selected State\nin UI Dropdown?"}
    CheckDropdown -- State Selected --> BindDropdown["Resolve Target = Selected State\nAllowed = [Selected, 'central']"]
    CheckDropdown -- 'All' Selected --> CheckIntent{"State-Dependent\nIntent?"}
    
    CheckIntent -- Yes --> Clarify["Trigger Clarification Notice\n(Ask user to specify state)"]
    CheckIntent -- No --> DefaultCentral["Resolve Target = 'central'\nAllowed = ['central']"]
    
    ResolveCentral --> FilterQuery["Execute Retrieval with Strict SQL Filter:\nWHERE jurisdiction IN allowed_jurisdictions"]
    RouteCentral --> FilterQuery
    BindUser --> FilterQuery
    MatchSingle --> FilterQuery
    BindDropdown --> FilterQuery
    DefaultCentral --> FilterQuery
```

---

### 3.5 Multilingual Query & Speech Services Flow

```mermaid
flowchart TD
    UserAudio["Citizen Voice Audio (Mic)"] --> ASRCheck{"Bhashini Credentials\nConfigured?"}
    ASRCheck -- Yes --> MeitYASR["MeitY ULCA ASR API"]
    ASRCheck -- No --> WebSpeech["Browser Web Speech API (Client-side)"]
    
    MeitYASR --> QueryText["Transcribed Query Text"]
    WebSpeech --> QueryText
    
    QueryText --> LangDetect["Script & Keyword Language Detection\n(en, hi, pa, doi, bgc)"]
    LangDetect --> CheckDialect{"Language Tier?"}
    
    CheckDialect -- English (en) --> DirectProcess["SUPPORTED_AND_VALIDATED:\nDirect Retrieval & Grounding"]
    CheckDialect -- Hindi (hi) / Punjabi (pa) --> TranslationLayer["SUPPORTED_WITH_LIMITATIONS:\nEntity-Preserving NMT / Local Fallback"]
    CheckDialect -- Dogri (doi) / Haryanvi (bgc) --> FallbackLayer["FALLBACK_AVAILABLE:\nPreserve dialect text; offer transparent Hindi audio fallback"]
    
    DirectProcess --> AnswerText["Grounded Answer Generated"]
    TranslationLayer --> AnswerText
    FallbackLayer --> AnswerText
    
    AnswerText --> TTSCheck{"Bhashini TTS\nAvailable?"}
    TTSCheck -- Yes --> MeitYTTS["Bhashini Neural Voice"]
    TTSCheck -- No --> HarmonicTTS["SahyogSetu Local Parametric Synthesizer"]
    
    MeitYTTS --> AudioCache["Cache Audio in tts_cache/ (WAV)"]
    HarmonicTTS --> AudioCache
    AudioCache --> CitizenAudio["Citizen Listens to Audio Playback"]
```

---

### 3.6 Government News Aggregation & Verification Pipeline

```mermaid
flowchart LR
    Sources["19 Official Government Portals\n(PIB, Cooperation.gov.in, State Gazettes)"] --> SSRF["SSRF & Domain Whitelist Validator\n(Reject 127.0.0.1, metadata, private IPs)"]
    SSRF --> Fetch["Async HTTP Collector (with timeout & retry)"]
    Fetch --> Parse["HTML / RSS / PDF Parser (BeautifulSoup4, Feedparser)"]
    Parse --> Dedupe["Deduplication Engine (URL + Headline Hash)"]
    Dedupe --> Classify["ML News Sector Classifier (TF-IDF + LinearSVC)"]
    Classify --> Verify["Official Source Verifier\n(Direct Document URL Check)"]
    Verify --> StoreDB[("news.db (SQLite)\nPreserve direct document link")]
    StoreDB --> Feed["Faceted News Feed API (/api/news)\nFilter by State, Category, Document Type"]
```

---

### 3.7 Deployment Architecture

```mermaid
flowchart TD
    subgraph HostEnvironment["Physical / Virtual Server (Linux / Windows)"]
        DockerHost["Docker Engine / Docker Compose"]
        
        subgraph ContainerNet["Isolated Bridge Network: sahyogsetu-net"]
            NginxCont["Container: sahyogsetu-proxy (nginx:1.27-alpine)\n- Listens: 80 / 443\n- Enforces 15 MB limit\n- Security headers\n- Serves /frontend/dist"]
            BackendCont["Container: sahyogsetu-backend (python:3.12-slim)\n- User: appuser (UID 10001)\n- Uvicorn (2 workers, port 8000)\n- Healthcheck on /api/health/ready"]
        end
        
        subgraph HostStorage["Host Persistent Volumes"]
            VolData["Volume: sahyogsetu_data\nMounted at: /app/backend/data\n- news.db\n- vectors.db\n- tts_cache/"]
        end
    end

    Internet["Public Traffic / Citizen Devices"] -->|HTTP / HTTPS| NginxCont
    NginxCont -->|Proxy pass /api/| BackendCont
    BackendCont <-->|Read / Write| VolData
```

---

## 4. End-to-End Citizen Query Data Flow

1. **Submission:**
   The citizen enters a natural language query via the chat input or microphone. The interface sends an HTTP `POST /api/chat` with:
   - `query`: Text string (sanitized against prompt injection delimiters).
   - `jurisdiction`: Selected UI dropdown (`all`, `central`, `punjab`, `haryana`, `jk`).
   - `language`: Selected interface language (`en`, `hi`, `pa`, `doi`, `bgc`).
   - `conversation_id`: UUID for thread persistence.

2. **Language Normalization:**
   The language detector determines the script (Latin, Devanagari, Gurmukhi). If Hindi or Punjabi, entity-preserving translation normalizes the query for retrieval while safeguarding statutory terms (e.g., section numbers, Act names).

3. **Jurisdiction Determination & Hierarchy Enforcement:**
   `JurisdictionResolver` inspects the query text and dropdown selection:
   - If multiple states are mentioned in an adversarial context (e.g. applying Punjab law in Haryana), it binds the query to the local society jurisdiction (Haryana) and restricts allowed retrieval to `["haryana", "central"]`, completely blocking Punjab statutes.
   - If the query concerns multi-state operations, it assigns `central` (Central MSCS Act 2002).
   - If the query asks a state-dependent question (e.g. committee tenure) without specifying a state and with `all` selected, it returns a **Jurisdiction Clarification Prompt**.

4. **Dual Retrieval & Reciprocal Rank Fusion (RRF):**
   - **Semantic Search:** Dense 384-dimensional embedding generated via `all-MiniLM-L6-v2` and compared via cosine similarity against vectors in `vectors.db`.
   - **Keyword Search:** Exact statutory token, section number, and BM25 token matching in SQLite.
   - **RRF Fusion:** Merges the candidate lists with reciprocal rank scoring ($k=60$).

5. **Legal Domain Reranking:**
   Reranks top candidates using domain-specific boost heuristics:
   - $+0.35$ for exact section match.
   - $+0.20$ for primary jurisdiction alignment.
   - $+0.15$ for query token overlap.
   - $+0.10$ for intent category match.

6. **Evidence Gating & Abstention:**
   If a specific section was queried and no matching section exists in the retrieved chunks, or if the top reranking score is below $0.28$, the system triggers the **No-Evidence Abstention** mechanism. It outputs a truthful notice stating that sufficient authoritative evidence was not found, preventing hallucinations.

7. **Grounded Answer Generation & Citation Validation:**
   - The structured statutory synthesizer constructs a 7-part legal answer (Direct Answer, Plain Explanation, Statutory Provision Details, Important Conditions, Disclaimer, and Source References).
   - `CitationValidator` cross-references every cited source against the retrieved chunks, verifying document titles, page numbers, and official government URLs (`.pdf` or `.gov.in` portal links).

8. **Multilingual Rendering & Audio Synthesis:**
   - The answer is rendered in the citizen's target language.
   - For Dogri and Haryanvi, text is displayed in the vernacular with an explicit, honest disclosure offering a standard Hindi audio alternative.
   - Audio is synthesized, cached in `tts_cache/`, and returned with audio streaming links.
