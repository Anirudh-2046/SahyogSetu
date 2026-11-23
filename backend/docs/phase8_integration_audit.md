# SAHYOGSETU — PHASE 8: INTEGRATION & CONNECTIVITY AUDIT
## Full-Stack Architecture, API Contracts & User Journey Readiness

**Audit Date:** November 19, 2026  
**Auditor:** Senior Full-Stack Integration Engineer  
**Objective:** Comprehensive audit of frontend components, backend endpoints, contract compatibility, and missing integration glue for Phase 8.

---

## 1. Feature-by-Feature Integration Matrix

| # | Feature / UI Component | Backend Endpoint | Current Status | Contract Compatibility | Missing Functionality / Gaps | Required Integration Tests |
| :- | :--- | :--- | :---: | :--- | :--- | :--- |
| **1** | **Legal Chatbot & Grounded Retrieval**<br>`ChatMessage.tsx`, `ChatInput.tsx`, `App.tsx` | `POST /api/chat` | `PARTIALLY_INTEGRATED` | **High:** `ChatQueryRequest` accepts `conversationId`, `query`, `language`, `jurisdiction`, `attachedDoc`. Response maps to `AssistantResponse`. | • Remote base URL defaults to empty if not in localStorage.<br>• Unhandled network timeouts fall back to mock without user notification.<br>• No-evidence state must clearly show no legal citations. | `Journey 1` (Punjab)<br>`Journey 2` (Haryana)<br>`Journey 3` (J&K)<br>`Journey 4` (Central)<br>`Journey 5` (No-Evidence) |
| **2** | **Conversation History & Persistence**<br>`HistoryDrawer.tsx`, `Header.tsx`, `App.tsx` | `GET /api/conversations`<br>`POST /api/conversations`<br>`GET /api/conversations/{id}`<br>`PATCH /api/conversations/{id}/title`<br>`DELETE /api/conversations/{id}` | `PARTIALLY_INTEGRATED` | **High:** Pydantic schemas support both camelCase and snake_case (`conversationId`, `createdAt`, `updatedAt`, `messageCount`). | • `App.tsx` loads only from `localStorage` on boot; does not auto-sync remote threads from `/api/conversations`.<br>• Need inline conversation title editing in `HistoryDrawer`.<br>• Need delete confirmation dialog before deleting. | `Journey 8` (Create, ask, rename, switch, delete) |
| **3** | **Jurisdiction State & Security Boundary**<br>`Header.tsx` (Jurisdiction selector), `App.tsx` | Passed to `/api/chat`, `/api/news`, `/api/conversations` | `INTEGRATED_AND_E2E_TESTED` | **Full:** Allowed codes `central`, `punjab`, `haryana`, `jk`, `all` match backend validator. | • Ambiguous jurisdiction prompt needs clear guidance.<br>• Ensure zero cross-state leakage is respected on frontend. | `Journey 1–4` (State isolation verification) |
| **4** | **Multilingual Language & Dialect Ethics**<br>`LanguageModal.tsx`, `Header.tsx`, `ChatMessage.tsx` | `POST /api/translate`<br>`GET /api/tts/languages` | `INTEGRATED_AND_E2E_TESTED` | **Full:** Language codes `en`, `hi`, `pa`, `doi`, `bgc` supported. | • Preserve user's Dogri (`doi`) and Haryanvi (`bgc`) preferences without silently substituting Hindi.<br>• Require consent for alternative speech playback. | `Journey 1` (Punjabi)<br>`Journey 2` (Language switch)<br>`Journey 7` (Voice) |
| **5** | **Speech Input (Microphone / ASR)**<br>`ChatInput.tsx`, `SpeechInputService.ts` | `POST /api/asr/transcribe`<br>`GET /api/asr/capabilities` | `PARTIALLY_INTEGRATED` | **High:** Audio payload sent as base64 with language code. | • Centralize base URL resolution.<br>• Allow citizen to review and edit transcript in input box before submission.<br>• Show transparent provider pill (Browser Web Speech vs Remote ASR). | `Journey 7` (Voice interaction & review) |
| **6** | **Speech Output (TTS Audio Playback)**<br>`ChatMessage.tsx`, `SpeechOutputService.ts` | `POST /api/tts/generate`<br>`GET /api/tts/audio/{audio_id}` | `INTEGRATED_AND_E2E_TESTED` | **Full:** Audio streaming with cache headers (`Accept-Ranges: bytes`, 24hr cache). | • Centralize base URL resolution.<br>• Prevent overlapping audio across messages.<br>• Honest provider disclosure (Local Harmonic, Google, Bhashini). | `Journey 1` (Punjabi TTS)<br>`Journey 7` (Speech output) |
| **7** | **Government News & Circulars Dashboard**<br>`GovernmentNewsSection.tsx`, `DashboardView.tsx` | `GET /api/news`<br>`GET /api/news/status`<br>`GET /api/news/sources`<br>`GET /api/news/verification-report` | `INTEGRATED_AND_E2E_TESTED` | **Full:** Phase 7 contracts fully aligned. Supports faceted filtering (`category`, `document_type`, `language`). | • 4 distinct card actions implemented in Phase 7.<br>• Warning pill for unverified documents active.<br>• Zero generic portal links. | `Journey 6` (News filtering, direct docs, warning pill) |
| **8** | **Citizen Helpfulness Feedback**<br>`ChatMessage.tsx` (Thumbs up/down) | `POST /api/feedback` | `PARTIALLY_INTEGRATED` | **Full:** `FeedbackSubmitRequest` accepts `message_id`, `rating`, `feedback_text`, `conversation_id`. | • Confirm remote persistence before displaying confirmation feedback badge.<br>• Handle offline graceful fallback. | Feedback submission & validation test |
| **9** | **Document Upload & Statutory Analysis**<br>`DocumentUploadModal.tsx`, `ChatInput.tsx` | `POST /api/documents/analyze`<br>`POST /api/documents/upload` | `PARTIALLY_INTEGRATED` | **High:** FormData file upload with query and language. | • Extract and format relevant statutory clauses.<br>• Display citation card for analyzed document. | Document upload analysis test |
| **10** | **System Health & Reliability**<br>`ui/ErrorState.tsx`, `ui/LoadingIndicator.tsx`, `App.tsx` | `GET /health` | `PARTIALLY_INTEGRATED` | **Full:** Returns component status (DB, RAG, TTS, News). | • Show friendly offline banner when backend is unreachable.<br>• Strip technical stack traces from citizen view.<br>• Provide one-click retry for failed queries. | `Journey 9` (Downtime simulation & recovery) |

---

## 2. API Communication Layer Audit (Phase 8.1 Gap Analysis)

Currently, base URL resolution is duplicated across multiple services:
1. `backendService.ts` (`getBaseUrl()`)
2. `newsService.ts` (`getConfiguredBaseUrl()`)
3. `SpeechInputService.ts` (`getApiBaseUrl()`)
4. `SpeechOutputService.ts` (`getApiBaseUrl()`)

### Deficiencies Identified:
- **Redundancy:** Four separate implementations of API base URL resolution.
- **Port Inconsistency:** `SpeechInputService.ts` hardcoded `http://127.0.0.1:8000` while others defaulted to `""`.
- **In-flight Deduplication:** No deduplication for simultaneous identical GET requests (e.g., duplicate news queries on tab switches).
- **Timeout Management:** Inconsistent timeouts (4s in news, 8s in chat, none in conversations).
- **Environment Variable Documentation:** Frontend lacked `.env.example`.

### Architecture Plan:
Create a centralized API client in [`frontend/src/services/apiClient.ts`](file:///d:/my%20code/MDC'26/frontend/src/services/apiClient.ts) and export unified helper methods. All services will route network calls through this client.

---

## 3. End-to-End User Journey Test Plan (Phase 8.10)

The following 9 end-to-end user journeys must be codified in `backend/tests/test_phase8_integration.py` and validated on the frontend:

1. **Journey 1 — Punjab Legal Query:**
   Select Punjab + Punjabi. Query cooperative registration. Assert Section 8 citation, Punjab 1961 Act link, Punjabi translation, and Gurmukhi TTS synthesis.
2. **Journey 2 — Haryana Governance Query:**
   Select Haryana. Query managing committee tenure. Assert Section 28 citation, Haryana 1984 Act link, 5-year tenure statutory preservation, and Hindi/English language toggle.
3. **Journey 3 — J&K Dispute Resolution:**
   Select J&K. Query arbitration dispute resolution. Assert Section 70 citation, J&K 1989 Act link, and 0% cross-state leakage (Punjab/Haryana laws excluded).
4. **Journey 4 — Central Government Scheme:**
   Select Central. Query PACS Computerization or KCC limit. Assert ₹2,516 Crore or ₹1.60 Lakh threshold, MoCoop/RBI official link, and Cabinet Note reference.
5. **Journey 5 — Unsupported Legal Query:**
   Query nonexistent statutory provision (e.g. space tourism cooperative). Assert `no_evidence` status, honest disclaimer, and zero fabricated citations.
6. **Journey 6 — News Discovery & Provenance:**
   Select jurisdiction. Filter by category & document type. Assert direct PDF links, official announcement URLs, and warning pill for unverified documents.
7. **Journey 7 — Voice Interaction Workflow:**
   Record voice query. Verify speech recognition transcription preview. Submit query and play audio answer. Verify honest provider disclosure.
8. **Journey 8 — Conversation Management Lifecycle:**
   Create conversation thread. Ask query. Verify SQLite persistence. Rename thread. Switch conversation. Return and delete thread with confirmation.
9. **Journey 9 — Failure Recovery & Graceful Degradation:**
   Simulate backend unavailability. Assert citizen-friendly error message (no stack traces). Restore backend and assert automatic recovery.

---

## 4. Verification Checkpoints

- [x] Frontend and backend codebases audited.
- [ ] Centralized `apiClient.ts` implemented and wired to all services.
- [ ] `App.tsx` conversation sync and persistence enhanced.
- [ ] `HistoryDrawer.tsx` inline rename and delete confirmation integrated.
- [ ] Frontend `.env.example` created.
- [ ] Automated integration test suite `test_phase8_integration.py` passes 100%.
- [ ] Full regression suite (Phases 2 through 7) passes 100%.
- [ ] Frontend production build passes with 0 errors.
- [ ] Comprehensive completion report `phase8_completion_report.md` generated.
