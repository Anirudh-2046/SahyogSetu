# SahyogSetu Phase 7: Government News Aggregation & Intelligent Pipeline — Technical Audit

**Date:** 2026-11-17  
**Scope:** Architecture & Component Audit of Existing News Services, Database Schema, NLP Stages, Connectors, and Frontend Dashboard  
**Status:** Audit Complete  

---

## 1. Existing News Collection Sources

The repository currently maintains references and connectors to official government portals across Central and State jurisdictions:
- **Central Government:**
  - Press Information Bureau (PIB) English (`https://www.pib.gov.in/allRel.aspx?lang=1`)
  - Press Information Bureau (PIB) Hindi (`https://www.pib.gov.in/allRel.aspx?lang=2`)
  - PIB Official RSS Feeds (`https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1`, `Lang=2`)
  - Ministry of Cooperation What's New Portal (`https://cooperation.gov.in/en/whats-new`)
  - Reserve Bank of India (RBI) Notifications & Master Circulars (`rbidocs.rbi.org.in`)
  - Verified Statutory Gazette Corpus (`VerifiedGazetteConnector` in `backend/services/news/web_connectors.py`)
- **State Governments:**
  - Government of Punjab Official Portal (`https://punjab.gov.in/`)
  - Government of Haryana Official Portal (`https://www.haryana.gov.in/`)
  - Government of Jammu & Kashmir Official Portal (`https://jk.gov.in/`)
  - Verka / Punjab State Cooperative Milk Producers' Federation
  - HARCO Bank & Haryana Hafed Notifications

---

## 2. Existing API / RSS Connectors

1. **`OfficialGovApiConnector` (`backend/services/news/api_connectors.py`):**
   - Implements configurable REST/JSON API connectors using `httpx`.
   - Supports environment variables for endpoints (`PIB_API_URL`, `COOP_API_URL`) and authorization (`PIB_API_KEY`, `COOP_API_KEY`).
   - Honestly reports non-configured status when government portals do not provide public JSON APIs (which is typical for NIC state portals).
2. **`OfficialGovRssConnector` (`backend/services/news/rss_connectors.py`):**
   - Parses RSS 2.0 / Atom feeds using `feedparser`.
   - Configured with legacy SSL context (`SSL_OP_LEGACY_SERVER_CONNECT`) to support Indian government certificates and NIC servers.
3. **`WebConnectors` (`backend/services/news/web_connectors.py`):**
   - `PIBWebConnector`: Extracts Press Release links, titles, ministry headers, and dates.
   - `PunjabGovWebConnector`: Scrapes permitted public announcement lists.
   - `HaryanaGovWebConnector`: Scrapes public state notifications.
   - `JKGovWebConnector`: Scrapes public orders and gazettes.
   - `MinistryOfCooperationWebConnector`: Scrapes what's new circulars.
   - `VerifiedGazetteConnector`: Supplies verified Gazette notifications and scheme circulars with direct PDF URLs.

---

## 3. Current Collection Frequency & Ingestion Mode

- Currently, news collection is triggered on-demand via:
  - Empty database boot check in `NewsService.get_news_feed()`
  - Manual API endpoint `POST /api/news/refresh`
  - Asynchronous background task execution (`BackgroundTasks` in FastAPI)
- **Gap Identified:** Automated cron/interval scheduling is not yet formalized into a persistent scheduler module with execution logs and health telemetry.

---

## 4. Existing News Database Schema

The SQLite database (`backend/data/news.db`) contains two primary tables:
1. **`news_items` Table:**
   - `news_id` (TEXT PRIMARY KEY)
   - `headline_original` (TEXT)
   - `description_original` (TEXT)
   - `full_text_original` (TEXT)
   - `source_name` (TEXT)
   - `source_type` (TEXT)
   - `source_url` (TEXT UNIQUE)
   - `publication_date` (TEXT)
   - `fetched_at` (TEXT)
   - `jurisdiction` (TEXT)
   - `issuing_department` (TEXT)
   - `original_language` (TEXT)
   - `category` (TEXT)
   - `keywords_json` (TEXT)
   - `target_audience` (TEXT)
   - `central_relevance` (INTEGER)
   - `summary_original` (TEXT)
   - `summary_translated_json` (TEXT)
   - `relevance_explanation_json` (TEXT)
   - `headline_translated_json` (TEXT)
   - `verification_status` (TEXT)
   - `content_hash` (TEXT)
   - `source_title` (TEXT)
   - `source_reference_number` (TEXT)
   - `original_source_url` (TEXT)
   - `official_translation_url` (TEXT)
   - `translated_source_language` (TEXT)
   - `source_verified` (INTEGER)
   - `source_verification_status` (TEXT)
   - `last_verified_at` (TEXT)
2. **`news_sources` Table:**
   - Tracks operational status, last fetch time, item counts, and connector notes.
- **Status of Records:** All **29 authentic records** preserved intact.
- **Fields to Add for Phase 7 (Non-Destructive Migration):**
  - `document_url`: Direct PDF or Gazette document URL (distinct from `source_url`).
  - `official_source_status`: Status of announcement portal (`verified_official_source`, `unverified`).
  - `official_document_status`: Status of supporting document (`verified_official_document`, `not_verified`).
  - `duplicate_of`: Canonical news ID if this record is a duplicate/amendment.
  - `relevance_score`: Quantitative relevance to cooperative governance (0.0 to 1.0).
  - `model_version`: Identifier of the classification model used.
  - `updated_at`: Timestamp of latest amendment or verification.

---

## 5. Current Source URL Handling

- `source_url`: Currently holds the article or notification link.
- `original_source_url`: Stores the direct document link for gazette items.
- Generic root homepages (`pib.gov.in`, `cooperation.gov.in`, `punjab.gov.in`, etc.) are recognized in `news_collector.py` and flagged as `unverified_pending_document`.
- **Gap Identified:** The distinction between the **announcement page** (`source_url`) and the **direct supporting PDF/document** (`document_url`) must be formalized as first-class separate database fields and displayed as separate actions on frontend cards.

---

## 6. Existing Classification & Relevance Models

- `backend/services/news/news_classifier.py`: Rule-based lexical matching with keyword dictionary.
- `backend/services/news/jurisdiction_classifier.py`: Authority and keyword heuristics mapping text to Central, Punjab, Haryana, or J&K.
- `backend/ml/models/news_model.joblib`: Phase 6 trained TF-IDF + `NewsExpander` + Logistic Regression classifier achieving **91.67% accuracy and 0.88 Macro F1** across 10 statutory cooperative sectors.
- **Integration Target:** Connect `backend/ml/inference/news_inference.py` directly into stage 3 of the 8-stage NLP pipeline in `news_collector.py`.

---

## 7. Existing Summarization & Translation

- `backend/services/news/summarizer.py`: Sentence-level extractive summarizer.
- `backend/services/news/translator.py`: Multilingual template and statutory term dictionary translator for English, Hindi, Punjabi, Dogri, and Haryanvi.
- Grounded "Why am I seeing this?" explanation generator in `relevance_analyzer.py`.
- **Target Enhancement:** Ensure summaries answer the 6 statutory questions:
  1. What changed?
  2. Who issued it?
  3. Who is affected?
  4. Which jurisdiction applies?
  5. When does it take effect?
  6. What action is required?
  Preserve all section numbers, dates, deadlines, and amounts; distinctly label AI-generated summaries and translations.

---

## 8. Existing Frontend News-Card Implementation

- `frontend/src/components/GovernmentNewsSection.tsx`:
  - Renders news cards with badges for jurisdiction, source type, and publication date.
  - Collapsible "Why this?" relevance explanation.
  - Renders button with `getSourceActionLabel(item)`.
- **Deficiencies to Rectify in Phase 7:**
  - Card currently combines source link and document link into a single primary button.
  - Must provide **separate, explicit actions**:
    1. **Read Official Announcement** (opens `source_url`)
    2. **View Official Document** (opens `document_url` only if verified)
    3. **View AI Summary** (toggles summary)
    4. **Read in Selected Language** (shows translated text)
  - Must explicitly show: "Official source document not yet verified." whenever `document_url` is unverified.
  - No generic "Portal" redirect button.

---

## 9. Missing Functionality to Implement

1. **`source_registry.py`:** Centralized, authoritative catalog of all government sources organized by jurisdiction with verification statuses.
2. **`source_verifier.py`:** Dedicated document URL verifier checking domain origin, content type, redirect resolution, and content relevance.
3. **Dedicated `document_url` Column:** Clean separation between article URL and supporting document URL.
4. **Automated Collection Scheduler Interface:** `news_scheduler.py` with manual CLI and programmatically scheduled background hooks.
5. **Admin Management & Verification Endpoints:**
   - `POST /api/news/collect`
   - `POST /api/news/reprocess/{news_id}`
   - `GET /api/news/verification-report`
   - `GET /api/news/sources` (extended with registry metadata)

---

## 10. Components to Preserve (Do NOT Recreate)

- **8-Stage News NLP Pipeline Architecture:** Maintain the modular design (`TextCleaner`, `LanguageDetector`, `NewsClassifier`, `JurisdictionClassifier`, `NewsSummarizer`, `NewsTranslator`, `RelevanceAnalyzer`, `Deduplicator`).
- **All 29 Existing Verified News Records:** In SQLite `news_items` table.
- **Phase 6 ML Classifier (`news_model.joblib`):** Reused directly via `backend.ml.inference.news_inference`.
- **Deterministic Jurisdiction Boundaries:** No ML model may override statutory state filters.
