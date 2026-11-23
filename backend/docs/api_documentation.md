# SahyogSetu — REST API Documentation

**API Version:** 2.0.0  
**Base URL:** `http://localhost:8000` (or reverse-proxied via Nginx at `http://localhost/api/`)  
**Specification:** OpenAPI 3.0 (Interactive Swagger UI available at `/docs`, ReDoc at `/redoc`)  
**Date:** November 2026  

---

## 1. Global API Standards

### Authentication
- **Public Citizen Endpoints:** No authentication required (`/api/chat`, `/api/news`, `/api/conversations`, `/api/tts`, `/api/health`).
- **Protected Administrative Endpoints:** Require HTTP header `X-Admin-Key: <ADMIN_API_KEY>` or Query parameter `?admin_key=<ADMIN_API_KEY>` (e.g. `/api/news/trigger-fetch`, `/api/documents/ingest`).

### Rate Limiting
- Public endpoints enforce an in-memory sliding-window limit of **30 requests per minute per IP address**.
- Rate-limited responses return HTTP `429 Too Many Requests` with a `Retry-After: 60` header.

### Request Sizing
- Maximum request payload size: **15 MB (15,728,640 bytes)**.
- Query string lengths bounded to **2,000 characters** via Pydantic schemas.

---

## 2. Chat & Legal Assistance Endpoints

### `POST /api/chat` (Alias: `POST /chat`)
**Purpose:** Executes source-grounded legal retrieval and structured response generation for cooperative societies.

**Request Body (`application/json`):**
```json
{
  "query": "What is the tenure of managing committee in Haryana under Section 28?",
  "jurisdiction": "haryana",
  "language": "en",
  "conversationId": "conv_abc123"
}
```
*Fields:*
- `query` (str, required): Natural language citizen question (max 2,000 chars).
- `jurisdiction` (str, optional): `"all"`, `"central"`, `"punjab"`, `"haryana"`, `"jk"` (defaults to `"all"`).
- `language` (str, optional): `"en"`, `"hi"`, `"pa"`, `"doi"`, `"bgc"` (defaults to `"en"`).
- `conversationId` (str, optional): UUID of active thread for message persistence.

**Success Response (HTTP 200 OK):**
```json
{
  "conversationId": "conv_abc123",
  "source": "live_backend",
  "response": {
    "shortAnswer": "Under Haryana Co-operative Societies Act 1984 (Section 28), 5-year term for committee; mandates reservation of seats for women and Backward Classes.",
    "plainExplanation": "**Direct Answer:** Under Haryana Co-operative Societies Act 1984 (Section 28), 5-year term for committee...\n\n### Official Sources & References\n1. **Haryana Co-operative Societies Act 1984** — Section 28 (Page 15)\n   *Issuing Authority:* Government of Haryana | ([View Official Document](https://cooperation.gov.in/sites/default/files/inline-files/HARYANA-CO-OPERATIVE-SOCIETIES-ACT.pdf))",
    "summary": "Under Haryana Co-operative Societies Act 1984 (Section 28), 5-year term for committee...",
    "citations": [
      {
        "title": "Haryana Co-operative Societies Act 1984",
        "authority": "Government of Haryana (via cooperation.gov.in)",
        "jurisdiction": "Haryana",
        "documentType": "Act",
        "section": "Section 28",
        "pageNumber": 15,
        "publicationDate": "1984",
        "originalLanguage": "english",
        "sourceUrl": "https://cooperation.gov.in/sites/default/files/inline-files/HARYANA-CO-OPERATIVE-SOCIETIES-ACT.pdf",
        "verificationStatus": "verified_official",
        "retrievalScore": 0.9011
      }
    ],
    "sources_markdown": "### Official Sources & References\n...",
    "jurisdiction": "Haryana",
    "uncertainty": {
      "status": "verified",
      "notice": "All statutory provisions verified against official Gazette records."
    },
    "language": "en"
  }
}
```

---

## 3. Conversation History Endpoints

### `GET /api/conversations`
**Purpose:** Retrieves list of conversation sessions from SQLite database.
**Query Parameters:**
- `limit` (int, optional): Max threads to return (default 50, max 100).
- `user_id` (str, optional): Filter by user identifier.

**Success Response (HTTP 200 OK):**
```json
{
  "conversations": [
    {
      "conversation_id": "conv_1795160439746",
      "title": "Tenure of managing committee in Haryana",
      "jurisdiction": "haryana",
      "language": "en",
      "created_at": "2026-11-20T13:10:39",
      "message_count": 2
    }
  ],
  "source": "live_backend",
  "total": 1
}
```

### `POST /api/conversations`
**Purpose:** Initializes a new conversation session.
**Request Body (`application/json`):**
```json
{
  "title": "Registration in Ludhiana",
  "jurisdiction": "punjab",
  "language": "pa"
}
```
**Success Response (HTTP 201 Created):**
```json
{
  "conversation_id": "conv_987xyz",
  "title": "Registration in Ludhiana",
  "createdAt": "2026-11-20T13:15:00",
  "source": "live_backend"
}
```

### `GET /api/conversations/{conv_id}`
**Purpose:** Retrieves complete message history for a conversation thread.
**Success Response (HTTP 200 OK):**
```json
{
  "conversation_id": "conv_987xyz",
  "title": "Registration in Ludhiana",
  "jurisdiction": "punjab",
  "language": "pa",
  "messages": [
    {
      "message_id": "msg_001",
      "role": "user",
      "content": "What is the procedure to register a PACS?",
      "created_at": "2026-11-20T13:15:05"
    },
    {
      "message_id": "msg_002",
      "role": "assistant",
      "content": "Under Section 8 of the Punjab Cooperative Societies Act 1961...",
      "created_at": "2026-11-20T13:15:06"
    }
  ]
}
```

### `DELETE /api/conversations/{conv_id}`
**Purpose:** Deletes conversation thread and cascades deletion of all associated messages.
**Success Response (HTTP 200 OK):**
```json
{
  "success": true,
  "conversation_id": "conv_987xyz",
  "message": "Conversation conv_987xyz deleted successfully"
}
```

---

## 4. Citizen Feedback Endpoints

### `POST /api/feedback`
**Purpose:** Submits citizen helpfulness rating and qualitative comment.
**Request Body (`application/json`):**
```json
{
  "message_id": "msg_002",
  "rating": "helpful",
  "feedback_text": "Clear statutory reference with direct PDF link.",
  "conversation_id": "conv_987xyz"
}
```
*Ratings Allowed:* `"helpful"`, `"unhelpful"`.
**Success Response (HTTP 200 OK):**
```json
{
  "status": "success",
  "feedback_id": "fb_4455",
  "message": "Feedback recorded successfully"
}
```

---

## 5. Document Intelligence & Upload Endpoints

### `POST /api/documents/analyze`
**Purpose:** Uploads a PDF or text statutory document; extracts clauses; produces grounded analysis.
**Request Type:** `multipart/form-data`
- `document`: Binary file (PDF or TXT, max 15 MB).
- `query` (str, optional): Specific question regarding the uploaded document.
- `jurisdiction` (str, optional): Target state scope.
- `language` (str, optional): Interface language.

**Success Response (HTTP 200 OK):**
```json
{
  "status": "success",
  "document_id": "doc_upl_789",
  "filename": "society_bye_laws.pdf",
  "extracted_clauses": [
    {"clause_title": "Clause 4. Membership Qualification", "summary": "Must be permanent resident of village..."}
  ],
  "analysis": "The uploaded bye-law adheres to Model PACS Byelaws provisions.",
  "is_official": false
}
```

---

## 6. Government News Endpoints

### `GET /api/news`
**Purpose:** Retrieves official government news, notifications, and circulars with faceted filters.
**Query Parameters:**
- `jurisdiction` (str, optional): `"all"`, `"central"`, `"punjab"`, `"haryana"`, `"jk"`.
- `language` (str, optional): `"en"`, `"hi"`, `"pa"`, `"doi"`, `"bgc"`.
- `category` (str, optional): Sector filter (`"coop_laws_regulations"`, `"agri_credit_kcc"`, etc.).
- `limit` (int, optional): Items per page (default 20, max 100).
- `offset` (int, optional): Pagination offset.

**Success Response (HTTP 200 OK):**
```json
{
  "items": [
    {
      "news_id": "news_pb_001",
      "headline": "Punjab Cooperative Department Issues PADB OTS Circular 2024",
      "description": "One-Time Settlement scheme announced for agricultural loan defaults...",
      "source_name": "Department of Cooperation, Punjab",
      "source_url": "http://coopwb.punjab.gov.in/notifications/PADB_OTS_Waiver_Circular_2024.pdf",
      "publication_date": "2024-03-15",
      "jurisdiction": "punjab",
      "category": "subsidies_financial_aid",
      "official_source_status": "verified_official_source",
      "document_type": "official_document"
    }
  ],
  "total_count": 29,
  "jurisdiction": "all",
  "language": "en"
}
```

### `POST /api/news/trigger-fetch` [Admin Protected]
**Purpose:** Manually triggers news ingestion from the 19 registered government sources.
**Headers:** `X-Admin-Key: <ADMIN_API_KEY>`
**Success Response (HTTP 200 OK):**
```json
{
  "status": "completed",
  "sources_polled": 19,
  "items_ingested": 0,
  "duplicates_skipped": 29
}
```

---

## 7. Speech & Translation Endpoints

### `POST /api/tts/generate` (Alias: `POST /api/tts/synthesize`)
**Purpose:** Synthesizes speech audio in requested Indian language with dialect transparency.
**Request Body (`application/json`):**
```json
{
  "text": "Under Section 28, managing committee tenure is 5 years.",
  "language": "pa",
  "voice_gender": "female"
}
```
**Success Response (HTTP 200 OK):**
```json
{
  "status": "success",
  "audio_id": "tts_418bb06fdd637f6c",
  "audio_url": "/api/tts/audio/tts_418bb06fdd637f6c",
  "language": "pa",
  "provider": "SahyogSetu Local Synthesizer",
  "is_alternative": false
}
```

### `GET /api/tts/audio/{audio_id}`
**Purpose:** Streams cached WAV audio bytes.
**Success Response (HTTP 200 OK):** Binary audio stream (`audio/wav`) with `Accept-Ranges: bytes` and `Cache-Control: public, max-age=86400`.

### `GET /api/asr/capabilities`
**Purpose:** Returns honest disclosure of speech recognition capabilities per language.
**Query Parameters:** `language=doi`
**Success Response (HTTP 200 OK):**
```json
{
  "language": "doi",
  "language_name": "Dogri",
  "is_native_supported": false,
  "provider": "Browser Web Speech Engine",
  "disclaimer": "Supported natively via Bhashini ULCA pipeline tasks. When credentials are not configured, transparently offers explicitly labelled Hindi audio alternative.",
  "bhashini_configured": false,
  "supported_formats": ["wav", "mp3", "webm", "ogg", "flac"]
}
```

### `POST /api/translate`
**Purpose:** Translates text between Indian languages while preserving statutory Act names, section numbers, and URLs.
**Request Body (`application/json`):**
```json
{
  "text": "Registration under Section 8 of the Punjab Act.",
  "source_language": "en",
  "target_language": "pa"
}
```
**Success Response (HTTP 200 OK):**
```json
{
  "translated_text": "ਪੰਜਾਬ ਐਕਟ ਦੀ ਧਾਰਾ 8 ਤਹਿਤ ਰਜਿਸਟ੍ਰੇਸ਼ਨ।",
  "source_language": "en",
  "target_language": "pa",
  "entities_preserved": true
}
```

---

## 8. Health, Monitoring & Probes

### `GET /api/health/live` (Alias: `GET /health/live`)
**Purpose:** Liveness probe for Kubernetes and Docker orchestrators.
**Success Response (HTTP 200 OK):**
```json
{
  "status": "alive",
  "service": "SahyogSetu Cooperative Governance & Legal API",
  "version": "2.0.0",
  "timestamp": "2026-11-20T13:10:39"
}
```

### `GET /api/health/ready` (Alias: `GET /health/ready`)
**Purpose:** Readiness probe checking database connectivity and storage readiness.
**Success Response (HTTP 200 OK):**
```json
{
  "status": "ready",
  "service": "SahyogSetu Cooperative Governance & Legal API",
  "checks": {
    "database": true,
    "knowledge_store": true,
    "vector_store": true
  },
  "timestamp": "2026-11-20T13:10:39"
}
```
*Note: Returns HTTP 503 Service Unavailable if database or storage is missing.*

### `GET /api/health` (Alias: `GET /health`)
**Purpose:** Comprehensive system diagnostics reporting record counts and provider states with zero credential leaks.
**Success Response (HTTP 200 OK):**
```json
{
  "status": "healthy",
  "service": "SahyogSetu Cooperative Governance & Legal API",
  "version": "2.0.0",
  "database": {
    "status": "connected",
    "total_news_records": 29,
    "total_conversations": 15,
    "foreign_keys_enforced": true
  },
  "tts": {
    "status": "operational",
    "active_provider": "local_harmonic",
    "supported_languages": 5
  },
  "bhashini": {
    "status": "offline_fallback_active",
    "active_fallback": "Local harmonic synthesizers & browser speech active."
  },
  "timestamp": "2026-11-20T13:10:39"
}
```
