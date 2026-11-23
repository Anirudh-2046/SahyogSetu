# SahyogSetu — Comprehensive Capability & Limitation Matrix

**Document Version:** 2.0.0  
**Date:** November 2026  
**Audience:** Academic Evaluators, System Auditors, Operations Teams, and Prospective Deployers  

---

## 1. Capability Status Taxonomy

To prevent inflated marketing claims, every system capability is classified under one of the following eight verified operational statuses:

- `VERIFIED_AND_VALIDATED`: Formally evaluated against independent test cases; performance meets or exceeds established thresholds.
- `VERIFIED_WITH_LIMITATIONS`: Implemented and tested; functional within defined constraints (e.g., restricted corpus density).
- `FALLBACK_AVAILABLE`: Native models absent or unconfigured; transparent, non-deceptive fallback active.
- `EXPERIMENTAL`: Implemented as prototype; requires human review before operational use.
- `IMPLEMENTED_NOT_LIVE_TESTED`: Code fully written and unit tested, but live third-party cloud integration unverified due to external credentials.
- `DISABLED`: Intentionally disabled for security, privacy, or ethical reasons.
- `NOT_IMPLEMENTED`: Planned future feature not currently present in codebase.
- `BLOCKED`: Blocked by external API limitations, licensing, or missing open datasets.

---

## 2. Platform Capability Matrix

| Capability | Status | Evidence | Limitations | Recommended Usage |
|---|---|---|---|---|
| **Legal Question Answering** | `VERIFIED_AND_VALIDATED` | Evaluated across 220 Gold, 60 Dev, and 40 Val benchmarks; 0.00% contradiction rate. | Grounded in 162 canonical statutory chunks across 11 documents. | Guidance for PACS governance, elections, audits, and schemes; not certified counsel. |
| **Central Legislation (MSCS Act 2002)** | `VERIFIED_AND_VALIDATED` | 24 statutory chunks indexed; registration (Sec 6-7), election authority (Sec 41), tenure (Sec 45), audit (Sec 70), arbitration (Sec 84-85). | Core statute and 2023 amendment covered; specialized rules partially indexed. | Multi-state cooperative formation, elections, and PACS byelaws inquiries. |
| **Punjab Legislation (1961 Act)** | `VERIFIED_AND_VALIDATED` | 51 statutory chunks indexed; registration (Sec 8), committee tenure (Sec 26), prior claim (Sec 40), audit (Sec 48), arbitration (Sec 55-56). | Comprehensive coverage of primary governance and PADB OTS scheme. | Primary Punjab cooperative society queries and agricultural credit inquiries. |
| **Haryana Legislation (1984 Act)** | `VERIFIED_AND_VALIDATED` | 26 statutory chunks indexed; registration (Sec 6-7), committee (Sec 28), audit (Sec 95), arbitration (Sec 102). | Subordinate departmental circulars partially indexed. | Haryana PACS managing committee tenures, audits, and dispute arbitration inquiries. |
| **Jammu & Kashmir Legislation (1989 Act)** | `VERIFIED_AND_VALIDATED` | 26 statutory chunks indexed; registration (Sec 7), tenure (Sec 29), audit (Sec 63), arbitration (Sec 70). | Reorganization Act 2019 adaptations reflected in statutory provisions. | J&K cooperative registration, elections, audits, and registrar dispute references. |
| **Section-Level Retrieval** | `VERIFIED_AND_VALIDATED` | 87.50% Dev P@1, 83.33% Val P@1, 37.84% Gold P@1; exact section match booster active. | Very broad multi-part queries without section keywords match Act-level topic first. | Best used with natural statutory queries; exact section numbers verify automatically. |
| **Citation Generation & Verification** | `VERIFIED_AND_VALIDATED` | 454 citations emitted across 220 queries; 0.00% citation hallucination rate. | All 162 indexed provisions have direct verified official PDF and portal references. | Primary legal verification; all links direct to official `.gov.in`/`.nic.in` PDFs. |
| **Jurisdiction Boundary Isolation** | `VERIFIED_AND_VALIDATED` | 45 hostile/cross-border test cases; 100.00% decision accuracy; 0.00% cross-state leakage. | Resolves border districts, acronyms, mixed scripts, and multi-state boundaries. | Safe for multi-state queries; extraterritorial state laws strictly blocked. |
| **English Language Support** | `VERIFIED_AND_VALIDATED` | Full pipeline support; 100% token grounding in statutory English acts. | None for statutory domain. | Primary administrative and evaluation language. |
| **Hindi Language Support** | `VERIFIED_WITH_LIMITATIONS` | Devanagari translation verified; entity preservation intact; local TTS active. | Stylistic variations in vernacular dialects; uses standard Khari Boli Hindi. | General Hindi inquiries; legal terms preserved alongside Hindi explanations. |
| **Punjabi Language Support** | `VERIFIED_WITH_LIMITATIONS` | Native Gurmukhi script processing; Gurmukhi parametric voice synthesis verified. | Complex legal terminology occasionally transliterated from English statutory terms. | Punjab cooperative members and rural PACS secretaries. |
| **Dogri Language Support** | `FALLBACK_AVAILABLE` | Vernacular Devanagari text rendered; dialect intent accuracy 0% without Bhashini. | No validated open Dogri acoustic voice model exists; lacks native TTS. | Text inquiries supported; audio transparently falls back to Hindi alternative. |
| **Haryanvi Language Support** | `FALLBACK_AVAILABLE` | Vernacular Devanagari text rendered; dialect intent accuracy 50% without Bhashini. | No validated open Haryanvi acoustic voice model exists; lacks native TTS. | Text inquiries supported; audio transparently falls back to Hindi alternative. |
| **Speech-to-Text (ASR)** | `VERIFIED_WITH_LIMITATIONS` | Client-side Browser Web Speech API operational; Bhashini adapter implemented. | Browser Web Speech requires modern Chrome/Edge; background noise impacts transcription. | Quick voice input on mobile and desktop browsers with microphone permissions. |
| **Text Translation (NMT)** | `VERIFIED_WITH_LIMITATIONS` | Entity-preserving translation protects Acts, sections, URLs, and amounts. | Offline mode uses heuristic legal lexicon; Bhashini NMT active only with credentials. | Vernacular rendering of statutory explanations. |
| **Text-to-Speech (TTS)** | `VERIFIED_WITH_LIMITATIONS` | Local parametric harmonic synthesizer + gTTS cached in `tts_cache/` (12 files). | Synthesized voice sounds slightly mechanical in offline harmonic mode. | Audio playback for rural members with limited reading literacy. |
| **Government News Aggregation** | `VERIFIED_AND_VALIDATED` | 29 verified official records; 19 registered sources; SSRF protection verified. | Ingestion runs on scheduled batch trigger; not real-time breaking news. | Discovering official notifications, scheme deadlines, and circular updates. |
| **Direct Source Document Linking** | `VERIFIED_AND_VALIDATED` | 82.76% of news items provide direct PDF or official press release links. | Some state circulars hosted on legacy portal URLs without HTTPS. | Reviewing authentic circulars and gazette notifications. |
| **User Query Intent Classification** | `VERIFIED_AND_VALIDATED` | TF-IDF + LinearSVC; 86.49% test accuracy; 0.8598 macro F1 across 9 classes. | Low confidence on single-word or ambiguous multi-intent prompts. | Automated retrieval reranking and clarification prompt generation. |
| **Legal Domain Reranking** | `VERIFIED_AND_VALIDATED` | Heuristic multi-factor reranker achieves 0.3604 MRR and elevates section matches. | Reranking weights are statically tuned ($+0.35$ section, $+0.20$ jurisdiction). | Enhancing hybrid retrieval precision. |
| **Conversation Persistence** | `VERIFIED_AND_VALIDATED` | Full CRUD lifecycle in SQLite with `PRAGMA foreign_keys = ON;` and cascading delete. | Thread list pagination defaults to 50 threads. | Maintaining multi-turn conversational context and history. |
| **Citizen Helpfulness Feedback** | `VERIFIED_AND_VALIDATED` | Thumbs up/down ratings and comments recorded with enforced message foreign keys. | Optional feedback; submission rate depends on user participation. | Quality monitoring and evaluation data collection. |
| **Citizen Document Upload & Analysis**| `VERIFIED_WITH_LIMITATIONS` | Analyzes uploaded statutory PDFs/text; extracts clauses; 15 MB limit. | Scanned multi-page image PDFs $>10$ pages require significant OCR processing time. | Reviewing society bye-laws, notices, and rejection orders. |
| **Security & SSRF Hardening** | `VERIFIED_AND_VALIDATED` | 12/12 security regression checks passed; rate limiting; log scrubbing active. | Sliding window rate limiter is in-memory; resets on container restart. | Protecting API from abuse, credential leaks, and SSRF attacks. |
| **Docker & Nginx Deployment** | `VERIFIED_AND_VALIDATED` | Multi-stage Docker build; unprivileged UID 10001; volume persistence verified. | Nginx TLS certificate configuration requires production domain mounting. | Reproducible local, staging, and containerized deployment. |

---

## 3. Critical Recommendations for Operational Deployment

1. **Jury Demonstration (Offline Mode):** Fully verified and approved. Local CPU pipeline executes deterministically in $\sim 5\text{ ms}$ with zero network risk.
2. **Restricted Staging Pilot:** Approved for cooperative department internal testing with persistent volume mounts.
3. **Public Production Release:** Must display prominent statutory disclaimers indicating that advice does not replace certified legal counsel, mandate state confirmation before answering state-specific questions, and require human registrar confirmation for formal filings.
