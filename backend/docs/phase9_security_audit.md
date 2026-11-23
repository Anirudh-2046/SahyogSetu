# SahyogSetu — Phase 9 Security & Privacy Audit Report
## Comprehensive Vulnerability Assessment & Risk Inventory

**Date:** 2026-11-19  
**Auditor:** SahyogSetu Senior Security & Backend Architecture Engineering  
**Application Scope:** Full-stack legal RAG chatbot, multilingual speech/translation services, government news pipeline, SQLite database, and React frontend.  
**Audit Status:** `COMPLETE`  

---

## 1. Executive Summary

A comprehensive, zero-assumption security and privacy audit was conducted across the backend codebase, API routes, middleware, document ingestion, vector retrieval, external network connectors, and frontend client application.

No hardcoded production secrets, API keys, or database credentials were found committed to the repository. However, several critical and high-priority architectural hardening opportunities were identified, primarily regarding:
1. **Server-Side Request Forgery (SSRF)** in news and document URL fetching.
2. **Missing Administrative Authorization** on privileged data-collection and re-indexing routes.
3. **Absence of API Rate Limiting** on compute-heavy chat, TTS, and document analysis endpoints.
4. **Input Length and File Upload Boundaries** on public submission routes.
5. **Prompt Injection Hardening** in legal RAG and LLM context synthesis.

---

## 2. Findings Matrix

| Finding ID | Severity | Component | Vulnerability Description | Evidence | Potential Risk | Proposed Remediation | Status |
|---|---|---|---|---|---|---|---|
| **SEC-01** | **High** | News & Document Connectors | Unrestricted outbound HTTP requests without SSRF protection, IP filtering, or scheme validation. | `web_connectors.py`, `source_verifier.py` call `httpx.get(url, follow_redirects=True)` without checking destination IP. | SSRF attacks accessing loopback (`127.0.0.1`), private subnets (`10.0.0.0/8`, `192.168.0.0/16`), or cloud metadata (`169.254.169.254`). | Implement centralized SSRF guard (`ssrf_protection.py`) validating scheme, resolving DNS, blocking private/reserved IPs, and validating redirects. | **Fixed** |
| **SEC-02** | **High** | Admin Endpoints | Privileged administrative operations lack authentication and access control. | `POST /api/documents/ingest`, `POST /api/documents/reindex`, `POST /api/news/collect`, `POST /api/news/reprocess` are unauthenticated. | Unauthorized users could trigger full database re-indexing, excessive scraping, or data replacement. | Implement `verify_admin_key` FastAPI dependency requiring valid `X-Admin-Key` or `Authorization: Bearer <key>` matching `settings.ADMIN_API_KEY`. | **Fixed** |
| **SEC-03** | **Medium** | API Gateway | Absence of rate limiting across compute-intensive and network endpoints. | No rate limiting middleware exists in `backend/main.py`. | API abuse, resource starvation, DoS on CPU-intensive PDF parsing, OCR, and TTS synthesis. | Implement in-memory sliding-window rate limiter middleware with tiered limits (Chat: 30/min, TTS: 25/min, Docs: 10/min, Admin: 5/min). | **Fixed** |
| **SEC-04** | **Medium** | File Uploads | Unbounded file read and lack of extension/MIME validation on document upload. | `document.read()` in `routes_documents.py` reads entire payload before validation; un-sanitized filenames. | Memory exhaustion DoS, upload of malicious executable files, script files, or path traversal via filenames. | Sanitize filename with `os.path.basename`; restrict extensions to `.pdf`/`.txt`; enforce magic-byte verification; cap PDF page count. | **Fixed** |
| **SEC-05** | **Medium** | Request Validation | Missing `max_length` constraints and unconstrained strings in Pydantic request models. | `ChatQueryRequest.query` has `min_length=1` without `max_length`; conversation titles lack size caps. | Memory bloat, buffer overflow attempts, SQLite storage spam. | Add explicit `max_length` bounds: query (2000), title (200), feedback (1000), speech text (5000), base64 audio (15MB). | **Fixed** |
| **SEC-06** | **Medium** | RAG Pipeline | Indirect prompt injection risk if retrieved context or user query is passed un-delimited to LLMs. | `answer_generator.py` formatted raw string prompts without strict XML delimiter tags. | Malicious retrieved document passages or adversarial queries attempting to override system grounding or exfiltrate data. | Wrap retrieved evidence in `<retrieved_evidence>` tags; instruct LLM that content is untrusted data; sanitize prompt injection triggers. | **Fixed** |
| **SEC-07** | **Low** | Observability | Missing distributed request tracing identifier (`X-Request-ID`) and structured latency metrics. | Standard logging does not correlate requests across services. | Difficulty in incident response, debugging, and identifying source IPs of abusive traffic. | Add Request Tracing Middleware generating UUID4 `X-Request-ID`, attaching to response, and logging structured audit events. | **Fixed** |
| **SEC-08** | **Low** | Health Checks | Single `/health` endpoint combines basic liveness and complete readiness. | No distinct `/health/liveness` and `/health/readiness` routes. | Container orchestrator could inappropriately kill healthy containers when optional third-party APIs are down. | Expose `/health/liveness` (fast process check) and `/health/readiness` (DB and vector storage readiness). | **Fixed** |
| **SEC-09** | **Low** | Repository Config | Missing `.gitignore` file and unpinned production `requirements.txt`. | No `.gitignore` existed in workspace root. | Risk of accidental commits of `.env`, SQLite databases (`news.db`), and cache files. | Add comprehensive `.gitignore` and pin production dependencies in `requirements.txt`. | **Fixed** |
| **SEC-10** | **Low** | CORS Policy | Overly permissive default CORS policy (`*`) with credentials allowed. | `CORS_ORIGINS=*` in `Settings`. | Cross-origin request exploitation in production environments. | Warn and restrict CORS origins when `APP_ENV=production` or `DEBUG=false`. | **Fixed** |

---

## 3. Secret & Credential Audit Summary

1. **Static Code Analysis**:
   - Zero hardcoded OpenAI (`sk-`), Gemini (`AIza`), or Bhashini keys found in source code.
   - All credentials consistently resolve through `os.getenv` via `backend/config.py`.
2. **Frontend Bundle Inspection**:
   - Zero secret tokens embedded in Vite client bundle (`dist/assets/index.js`).
   - Client accesses only public endpoints via `apiClient.ts`.
3. **Health Check Inspection**:
   - Health check explicitly checks `settings.is_bhashini_configured` (boolean) without exposing user IDs or keys.
   - Component status returns zero sensitive credential fields.
4. **Credential Rotation Procedure**:
   - If an operational key is suspected of compromise, rotate via cloud console (Bhashini Portal, Google AI Studio, OpenAI Platform).
   - Update `.env` on backend server and reload `uvicorn`. No code modification required.

---

## 4. Privacy & Personal Data Assessment

1. **Citizen Chat Queries**:
   - The frontend includes client-side regex detection ([ChatInput.tsx](file:///d:/my%20code/MDC'26/frontend/src/components/ChatInput.tsx#L48)) warning citizens against entering Aadhaar numbers, OTPs, or passwords.
   - Conversation histories in SQLite are tied to random UUIDs (`conv_...`), not personal identities.
2. **Audio Processing**:
   - Voice audio sent to `/api/asr/transcribe` is processed in-memory and discarded; raw voice is never permanently written to disk.
   - TTS synthesized audio is cached by SHA-256 hash in `backend/data/tts_cache/` for performance and can be purged at any time.
3. **Data Deletion**:
   - Citizen deletion requests in the UI invoke `DELETE /api/conversations/{id}`, which triggers cascading deletion of all associated messages and feedback rows in SQLite.
