# SahyogSetu — Phase 9: Privacy and Data Minimization Review

**Document Version:** 1.0  
**Date:** November 2026  
**Compliance Standard:** Digital Personal Data Protection (DPDP) Act, 2023 (India) & MeitY Guidelines  
**Status:** Approved & Verified

---

## 1. Executive Summary

SahyogSetu is designed as a sovereign, public-interest cooperative governance and legal guidance platform. Because it serves grassroots citizens, cooperative society members, farmers, and committee office-bearers across India, safeguarding citizen privacy and practicing strict data minimization is a foundational engineering mandate.

This document details the data taxonomy, retention policies, redaction safeguards, and compliance posture implemented across SahyogSetu.

---

## 2. Citizen Data Classification & Taxonomy

SahyogSetu explicitly categorizes all inbound and stored data according to statutory risk tiers:

| Data Category | Specific Elements | Processing Location | Storage / Persistence | Statutory Sensitivity |
|---|---|---|---|---|
| **Citizen Queries** | Natural language text regarding cooperative laws, rules, elections | Local backend server | SQLite `conversation_messages` (if conversation thread created) | Low (Non-PII public interest queries) |
| **Voice Audio (ASR)** | Raw WAV / MP3 / WebM voice clips of citizen queries | Memory / Bhashini ULCA API | **Ephemeral only** (decidedly NOT saved to disk or DB) | High (Biometric Voice Print) |
| **Synthesized Audio (TTS)** | MP3/WAV speech audio generated for legal responses | Local disk cache (`backend/data/tts_cache/`) | Cached by SHA256 content hash for offline delivery | Low (Public statutory text audio) |
| **Uploaded Documents** | Bylaws, audit notices, circulars uploaded by users | Local disk (`backend/data/uploaded_docs/`) | Registered in `uploaded_documents` table | Medium (Private cooperative documents) |
| **Feedback Ratings** | Helpfulness rating (1-5, thumbs), voluntary comments | Local backend server | SQLite `user_feedback` table | Low |
| **Government News** | Official circulars, gazettes, press releases | Local database | SQLite `news_items` | Public Domain Data |
| **Server Logs** | Timestamps, endpoint paths, status codes, UUIDs | Local stdout / rotating log | In-memory / console log (Scrubbed) | Internal Operational |

---

## 3. Data Minimization & PII Redaction Practices

### 3.1 Strict Non-Collection of Personal Identifiers
- **No Mandatory Login / Aadhaar / Phone:** SahyogSetu does not require user registration, Aadhaar numbers, PAN numbers, voter IDs, or phone numbers to query legal provisions or browse government announcements.
- **Anonymous Session Identifiers:** Conversation threads use client-generated or server-minted UUIDs (`conv_<uuid>`) with no link to IP addresses or citizen identity.

### 3.2 Real-time Log Sanitization
The system implements a centralized log sanitization engine (`backend/security/logging_middleware.py`) that scrubs sensitive tokens, credentials, and potential PII before lines are written:
- **Aadhaar Numbers:** 12-digit Indian national identity numbers are masked: `\b\d{4}\s?\d{4}\s?\d{4}\b` -> `[REDACTED_AADHAAR]`.
- **One-Time Passwords (OTPs):** 6-digit verification codes are masked: `\b(?i:otp|code)[:=\s]*\d{4,8}\b` -> `[REDACTED_OTP]`.
- **API Keys and Passwords:** High-entropy secret patterns, Authorization headers, and Bearer tokens are scrubbed.

### 3.3 Ephemeral Voice Processing (Zero Audio Retention)
- Citizen speech captured via microphone is converted to Base64 in the browser and transmitted to `/api/asr/transcribe`.
- The backend decodes the audio in-memory for transcription via the configured ASR provider (Bhashini ULCA or local synthesizer).
- **The raw citizen audio stream is discarded immediately upon completion of transcription.** At no point is citizen voice audio stored in the database or persisted to the filesystem.

---

## 4. Retention & Deletion Architecture

### 4.1 Right to Erasure (DPDP Act Section 12)
Citizens maintain complete control over their consultation history:
- **Conversation Deletion Endpoint:** `DELETE /api/conversations/{conversation_id}`.
- **Cascading Referential Cleanup:** Deleting a conversation triggers a database foreign-key cascade (`PRAGMA foreign_keys = ON`), purging:
  1. The parent `conversations` record.
  2. All historical messages in `conversation_messages`.
  3. All linked citizen feedback entries in `user_feedback`.
- **No Shadow Retention:** Deletion is permanent and immediate within the transactional database layer.

### 4.2 Cache Expiration Policy
- **TTS Audio Cache:** Cached files in `backend/data/tts_cache/` represent standardized statutory responses keyed by content hash (`sha256(text + lang)`). No citizen identifiers exist in filenames or metadata. Files older than 30 days are scheduled for eviction.
- **Uploaded Document Expiry:** Uploaded documents in `backend/data/uploaded_docs/` are associated with individual user sessions and can be deleted via document management API calls.

---

## 5. Third-Party Data Transmission & External Providers

SahyogSetu limits external outbound communication strictly to verified service providers:

| Provider | Purpose | Data Transmitted | Security Measures |
|---|---|---|---|
| **Digital India Bhashini (ULCA)** | ASR, NMT, TTS | Spoken audio bytes, query text, language code | HTTPS TLS 1.3, User-ID & API-Key headers, zero retention requested |
| **Official Government Portals** | RSS feeds, circulars, PDFs | None (Outbound HTTP GET for public announcements) | Strict SSRF filter, IP subnet validation, domain whitelist |
| **Google Gemini / OpenAI (Optional)** | LLM answer generation | Statutory context chunks + sanitized query | Outbound HTTPS POST with `<retrieved_evidence>` boundary tags |

**Zero Third-Party Trackers:** SahyogSetu includes zero commercial analytics scripts, zero tracking pixels, and zero advertising SDKs in both frontend and backend.

---

## 6. Security & Encryption Controls

1. **In-Transit Protection:** All client-backend and backend-provider communications mandate TLS (HTTPS).
2. **At-Rest Protection:** SQLite database is stored with filesystem permissions restricted to the backend service user (`chmod 600`).
3. **Database Integrity:** Parameterized queries protect against SQL injection; transaction rollbacks prevent partial state corruption.
4. **Administrative Protection:** Administrative endpoints (`/api/documents/ingest`, `/api/news/refresh`, etc.) require cryptographically verified API keys (`X-Admin-Key`).

---

## 7. Conclusion & Compliance Certification

SahyogSetu complies with the foundational principles of the **Digital Personal Data Protection Act, 2023 (India)**:
- **Purpose Limitation:** Data is processed solely to provide cooperative legal assistance and official news.
- **Data Minimization:** No personal citizen identifiers are requested or logged.
- **Storage Limitation:** Ephemeral voice transcription and user-triggered conversation erasure.
- **Integrity & Confidentiality:** Input sanitization, log scrubbing, rate limiting, and SSRF prevention.
