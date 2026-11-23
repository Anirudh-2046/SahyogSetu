# SahyogSetu — Targeted Remediation Report: General Government Assistance, Official-Source Retrieval & Contextual Abstention

**Document Version:** 1.0.0  
**Date:** November 2026  
**Status:** RESOLVED & VERIFIED  
**Component:** Intelligent Query Router (`query_router.py`), Official Service Retriever (`official_service_retriever.py`), Contextual Follow-up Generator (`followup_generator.py`), Answer Synthesizer (`answer_generator.py`), Source Resolver (`source_resolver.py`), Frontend Chat Message (`ChatMessage.tsx`)  

---

## 1. Confirmed Root Causes

### Reported Defect:
When a citizen asked an administrative government question outside the local statutory cooperative corpus, such as:
> *"I want to change address on my Aadhaar card, what documents I need?"*

The system previously failed with two severe usability defects:
1. **Unhelpful Blanket Abstention:** It immediately returned:
   > *"I could not find sufficient authoritative information in the available documents to answer this question."*
2. **Contextually Irrelevant Suggested Follow-up:** It rendered:
   > *"Where can a dispute or grievance under this provision be filed?"*

### Root Cause Diagnosis:
1. **Absence of General Administrative Query Routing:**
   `source_resolver.py` only checked for 9 cooperative intents (`pm_kisan`, `kcc_credit`, `pmfby_insurance`, `cooperative_registration`, `elections_governance`, `dispute_arbitration`, `audit_inspection`, `pacs_reforms`, `ots_waiver`). Any query outside these categories was labeled `"general_coop"` and sent straight into the local statutory legal RAG pipeline.
2. **Local Corpus Evidence Failure:**
   `vectors.db` contains only cooperative legislation and central agriculture schemes (11 Acts/Guidelines). Searching it with an Aadhaar query produced `intent_boost == 0.0 and overlap < 0.05`, triggering `is_unsupported = True` and causing immediate generic abstention.
3. **Hardcoded Dispute Follow-up Fallback in Frontend UI:**
   In `frontend/src/components/ChatMessage.tsx` (lines 436–446), `getContextualFollowUps()` checked for `'register'` and `'kcc'`, and unconditionally defaulted to:
   > `"Where can a dispute or grievance under this provision be filed?"`
   It did not inspect backend-provided follow-ups, and had no awareness of whether the response discussed a statutory provision or was an administrative inquiry.
4. **Lack of Controlled Official External Source Retrieval:**
   While `services/news/` possessed web connectors for government portals, the core assistant had no controlled service retriever for authoritative citizen administration portals like UIDAI (`uidai.gov.in`, `myaadhaar.uidai.gov.in`).

---

## 2. Previous Routing vs. New Routing Architecture

### Previous Architecture:
```
User Query ──> Language Detector ──> Cooperative Intent Classifier (9 intents) ──> vectors.db Search ──> [0 matches] ──> Generic Abstention ──> Frontend Hardcoded "Dispute under this provision?"
```

### New Intelligent Routing Architecture:
```mermaid
flowchart TD
    A[Citizen Query] --> B[Language Priority Resolver]
    B --> C[Intelligent Query Router]
    C -->|COOPERATIVE_LAW / SCHEME / GOVERNANCE / DISPUTE| D[Core Cooperative Legal RAG Pipeline]
    C -->|GOVERNMENT_SERVICE / DOCUMENT_REQUIREMENTS| E[Official Service Retriever]
    C -->|JURISDICTION_AMBIGUOUS| F[Jurisdiction Clarifier]
    C -->|OUT_OF_SCOPE| G[Contextual Out-of-Scope Handler]
    
    D --> H[Local Grounded Synthesis & Citations]
    E --> I[Authoritative Government Sources: UIDAI / Income Tax / ECI]
    F --> J[Localized Jurisdiction Options]
    G --> K[Domain Boundary Explanation + Official Portal Links]
    
    H --> L[Contextual Follow-up Generator]
    I --> L
    F --> L
    G --> M[Empty Follow-up List: []]
    
    L --> N[Structured Citizen Response with Provenance Tag]
    M --> N
```

---

## 3. The 10 Query Taxonomy Categories

| Category | Description | Target Execution Handler | Source Provenance |
| :--- | :--- | :--- | :--- |
| **`COOPERATIVE_LAW`** | Statutory sections, legal provisions, acts, amendments, byelaws. | `cooperative_rag` | `VERIFIED_LOCAL_LEGAL_CORPUS` |
| **`COOPERATIVE_SCHEME`** | PM-KISAN, KCC, PMFBY, PADB OTS, PACS computerization. | `cooperative_rag` | `VERIFIED_LOCAL_LEGAL_CORPUS` |
| **`COOPERATIVE_GOVERNANCE`** | Managing committee elections, tenure, registration, audit, membership. | `cooperative_rag` | `VERIFIED_LOCAL_LEGAL_CORPUS` |
| **`GOVERNMENT_SERVICE`** | Public administrative services (Aadhaar update, PAN card, Voter ID, Passport, DL, Ration Card). | `official_service_retriever` | `VERIFIED_OFFICIAL_EXTERNAL_SOURCE` |
| **`DOCUMENT_REQUIREMENTS`** | Acceptable Proof of Address (POA), Proof of Identity (POI), and KYC documents. | `official_service_retriever` | `VERIFIED_OFFICIAL_EXTERNAL_SOURCE` |
| **`GENERAL_PUBLIC_INFORMATION`** | Citizen service portals (services.india.gov.in, CSC centers, public helplines). | `official_service_retriever` | `VERIFIED_OFFICIAL_EXTERNAL_SOURCE` |
| **`LEGAL_DISPUTE`** | Arbitration under Section 55/102/70, registrar references, civil court bars. | `cooperative_rag` | `VERIFIED_LOCAL_LEGAL_CORPUS` |
| **`JURISDICTION_AMBIGUOUS`** | Cooperative questions lacking state or central specification. | `jurisdiction_clarifier` | `JURISDICTION_CLARIFICATION_REQUIRED` |
| **`OUT_OF_SCOPE`** | Topics outside Indian public governance (NASA Mars mission, movies, cricket, coding). | `out_of_scope_handler` | `INSUFFICIENT_VERIFIED_EVIDENCE` |
| **`UNSUPPORTED_OR_UNCLEAR`** | Incomprehensible or garbled requests. | `out_of_scope_handler` | `INSUFFICIENT_VERIFIED_EVIDENCE` |

---

## 4. Controlled Official-Source Assistance

### Authoritative Source Hierarchy
The retriever strictly adheres to the following source hierarchy:
1. **Primary Authority Portals:** Dedicated statutory government portals (`uidai.gov.in`, `myaadhaar.uidai.gov.in`, `incometax.gov.in`, `voters.eci.gov.in`, `passportindia.gov.in`, `parivahan.gov.in`, `nfsa.gov.in`).
2. **National Service Aggregators:** National Government Services Portal (`services.india.gov.in`, `india.gov.in`).
3. **Statutory Guidelines & Gazette Circulars:** Official lists of valid documents published by issuing ministries.
4. **Prohibited Sources:** Random blogs, commercial SEO portals, unverified social media, and forum posts are strictly blocked.

### Verified Aadhaar Address Update Coverage:
- **Authority:** Unique Identification Authority of India (UIDAI), Ministry of Electronics & IT, Government of India.
- **Portals:** `https://myaadhaar.uidai.gov.in` and `https://uidai.gov.in`.
- **Statutory Fee:** ₹50 (Online on myAadhaar portal) / ₹50 (Aadhaar Seva Kendra).
- **Processing Timeline:** 5 to 15 working days.
- **Valid Proof of Address (POA) Documents Extracted:**
  1. Passport
  2. Bank Statement or Passbook (with applicant's photograph, signed & stamped by the bank)
  3. Ration Card
  4. Voter Identity Card (EPIC)
  5. Driving License
  6. Electricity / Water / Piped Gas Bill (not older than 3 months)
  7. Property Tax Receipt (not older than 1 year)
  8. Registered Rent Agreement / Sale Deed / Lease Deed
  9. Standard Certificate issued by Gazetted Officer / Village Panchayat Head / Tehsildar (in official UIDAI template)
  10. Head of Family (HoF) based update: If no document in own name, address update via HoF's Aadhaar + Relationship proof (Ration card, Marriage certificate) with HoF OTP consent.
- **Step-by-Step Procedure:**
  1. Login to `myaadhaar.uidai.gov.in` using 12-digit Aadhaar number and OTP received on registered mobile.
  2. Select 'Address Update' $\rightarrow$ 'Update Aadhaar Online' (or 'Head of Family (HoF) based Address Update').
  3. Enter new address details matching supporting proof document.
  4. Upload clear, self-attested scanned copy (PDF/JPEG/PNG).
  5. Pay non-refundable fee of ₹50 online via UPI, net banking, or debit card.
  6. Download acknowledgment receipt with 14-digit Service Request Number (SRN) to track status.
- **Mandatory Prerequisites:**
  - Mobile number must be active and linked to Aadhaar for OTP verification. (If not linked, citizen must visit an Aadhaar Seva Kendra in person).
  - Supporting document must be in applicant's name (unless utilizing the HoF route).

---

## 5. Security & Safety Protections

1. **SSRF Protections & Domain Whitelisting:**
   `official_service_retriever.py` enforces a strict whitelist of Indian government domains (`.gov.in`, `.nic.in`, `rbi.org.in`, `uidai.gov.in`, `myaadhaar.uidai.gov.in`).
2. **Private IP and Loopback Blocking:**
   Any request resolving to private/internal subnets (`127.0.0.1`, `localhost`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) is blocked before network egress.
3. **Prompt Injection Defense & Content Sanitization:**
   Retrieved content is sanitized through `sanitize_retrieved_content()`. Script tags, style elements, and jailbreak markers (`ignore previous instructions`, `you are now`, `system prompt`) are stripped before parsing.
4. **Untrusted Data Isolation:**
   External text is treated purely as untrusted reference data and cannot override system prompts or jurisdiction barriers.

---

## 6. Contextual Abstention Engine

When evidence is unavailable, the system produces constructive, category-aware explanations rather than generic boilerplate:

| Scenario | Previous Flawed Output | Remediated Contextual Output |
| :--- | :--- | :--- |
| **Out-of-Scope (e.g. NASA Mars)** | *"I could not find sufficient authoritative information in the available documents to answer this question."* + Follow-up: *"Where can a dispute or grievance under this provision be filed?"* | **"Inquiry Outside Platform Scope:"** Explains that SahyogSetu is dedicated to Indian public governance, welfare schemes, and citizen administrative services. Directs citizen to official portals (e.g. `nasa.gov` or `isro.gov.in`). **Suggested Follow-ups: `[]` (Empty)**. |
| **Missing / Unverified External Source** | *"I could not find sufficient authoritative information..."* | **"Authoritative Source Verification Unavailable:"** Explains that document requirements could not be verified from an authoritative source and directs citizen to `uidai.gov.in` or `services.india.gov.in`. Generates relevant next-step follow-ups. |
| **Cooperative Law Missing Evidence** | *"I could not find sufficient authoritative information..."* | **"Insufficient Authoritative Evidence:"** Explains that statutory database does not contain this specific cooperative section, and advises consulting District Assistant Registrar (ARCS) or state RCS portal. |

---

## 7. Contextual Follow-up Questions

`backend/rag/followup_generator.py` replaces hardcoded templates with category-aware logic:

1. **Aadhaar Queries:**
   - *"How can I update my address online without a document using Head of Family (HoF) consent?"*
   - *"What is the official fee and processing timeline for an Aadhaar address update on myAadhaar?"*
   - *"Can I update my address if my mobile number is not linked with Aadhaar?"*
2. **Cooperative Queries:**
   - *"What is the statutory fee and list of annexures required for filing Form-A with the Registrar?"*
   - *"How many minimum adult promoter members are needed to register a primary cooperative society?"*
3. **Out-of-Scope Queries:**
   - Returns `[]` (strictly empty list).
4. **Statutory Preservation:**
   - Never refers to "this provision" unless the response actually cites an official statutory section.
5. **Frontend Priority (`ChatMessage.tsx`):**
   - Prioritizes `data.suggestedFollowUps` and `data.suggestedQuestions` returned by the backend.
   - Fallback logic checks for statutory context before offering dispute options, and returns `[]` for abstentions.

---

## 8. Response Language Enforcement

The remediation strictly preserves the previously established response-language enforcement:
- **Hindi (`hi`):** Full Devanagari synthesis for answers, document lists, procedures, citations, and follow-up chips.
- **Punjabi (`pa`):** Full Gurmukhi synthesis for answers, document lists, procedures, citations, and follow-up chips.
- **English (`en`):** Clean authoritative English legal and administrative prose.
- **Dogri (`doi`) & Haryanvi (`bgc`):** Rendered in standard Devanagari Hindi with transparent dialect notice badge.

---

## 9. Automated Test Results

### Dedicated Test Suite: `backend/tests/test_official_source_retrieval.py`
Execution: `python -m unittest backend.tests.test_official_source_retrieval -v`
```
test_aadhaar_address_update_retrieval ... ok
test_contextual_abstention ... ok
test_contextual_followups ... ok
test_end_to_end_chat_api ... ok
test_multilingual_response_language_enforcement ... ok
test_query_routing_taxonomy ... ok
test_ssrf_and_security_protections ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.030s

OK (100% Passed)
```

### Response Language Enforcement Suite: `backend/tests/test_response_language_enforcement.py`
Execution: `python backend/tests/test_response_language_enforcement.py`
```
================================================================================
ALL 11 RESPONSE LANGUAGE ENFORCEMENT TESTS PASSED WITH 100% SUCCESS!
================================================================================
```

### Full Platform Regression Suite Runner: `backend/scripts/run_all_phase13_regressions.py`
Execution: `python backend/scripts/run_all_phase13_regressions.py`
```
================================================================================
SAHYOGSETU PHASE 13: FULL PLATFORM REGRESSION RUNNER
================================================================================
Running Phase 2 Backend Architecture... ✓ PASSED
Running Phase 3 Ingestion & Vectors...   ✓ PASSED
Running Phase 4 Legal RAG Engine...     ✓ PASSED
Running Phase 5 Bhashini Multilingual...✓ PASSED
Running Phase 6 ML Classifiers...       ✓ PASSED
Running Phase 7 News Aggregation...     ✓ PASSED
Running Phase 8 Full-Stack Integration..✓ PASSED
Running Phase 9 Production Security...  ✓ PASSED
Running Phase 11 Production Deployment..✓ PASSED
Running Phase 13 Jurisdiction Stress... ✓ PASSED

================================================================================
REGRESSION RESULTS: 10 / 10 SUITES PASSED
ALL REGRESSION SUITES PASSED WITH 100% SUCCESS!
================================================================================
```

---

## 10. Manual Verification Results

All required verification scenarios were manually verified in-process through the FastAPI `/api/chat` endpoint:

| # | Query | Selected Language | Routed Category | Result & Provenance | Contextual Follow-up Generated |
| :-: | :--- | :-: | :-: | :--- | :--- |
| **1** | *"How many members are needed to register a cooperative society in Punjab under Section 8?"* | `en` | `COOPERATIVE_LAW` | Verified Section 8 answer (minimum 10 persons). `VERIFIED_LOCAL_LEGAL_CORPUS` | *"What is the statutory fee and list of annexures required for filing Form-A with the Registrar?"* |
| **2** | *"How to apply for PM-KISAN annual installment?"* | `en` | `COOPERATIVE_SCHEME` | Verified PM-KISAN guidelines, DBT ₹6,000 in 3 installments. `VERIFIED_LOCAL_LEGAL_CORPUS` | *"How can a farmer complete mandatory Aadhaar e-KYC on the PM-KISAN mobile app?"* |
| **3** | *"I want to change address on my Aadhaar card, what documents I need?"* | `en` | `DOCUMENT_REQUIREMENTS` | Full POA list, ₹50 fee, myAadhaar portal steps. `VERIFIED_OFFICIAL_EXTERNAL_SOURCE` | *"How can I update my address online without a document using Head of Family (HoF) consent?"* |
| **4** | *"What documents do I need to link PAN with Aadhaar?"* | `en` | `GOVERNMENT_SERVICE` | Income Tax Dept procedures, Section 139AA mandate. `VERIFIED_OFFICIAL_EXTERNAL_SOURCE` | *"What is the procedure and fee to link PAN with Aadhaar on the Income Tax e-filing portal?"* |
| **5** | *"How to register a new primary cooperative society?"* (no state given) | `en` | `JURISDICTION_AMBIGUOUS` | Jurisdiction clarification prompt (Central, Punjab, Haryana, J&K). `JURISDICTION_CLARIFICATION_REQUIRED` | State-specific prompt options. |
| **6** | General service query with unavailable source | `en` | `GOVERNMENT_SERVICE` | Contextual abstention directing to `services.india.gov.in`. `OFFICIAL_SOURCE_UNAVAILABLE` | Next-step portal navigation follow-up. |
| **7** | *"What is NASA's Mars rover exploration mission?"* | `en` | `OUT_OF_SCOPE` | Domain boundary explanation directing to `nasa.gov` / `isro.gov.in`. `INSUFFICIENT_VERIFIED_EVIDENCE` | `[]` (Strictly Empty). |
| **8** | *"आधार कार्ड में पता बदलने के लिए कौन से दस्तावेज चाहिए?"* | `hi` | `DOCUMENT_REQUIREMENTS` | 100% Devanagari Hindi response, POA list, ₹50 शुल्क, myAadhaar पोर्टल। `VERIFIED_OFFICIAL_EXTERNAL_SOURCE` | *"क्या बिना दस्तावेज के परिवार के मुखिया (HoF) की सहमति से आधार में पता बदल सकते हैं?"* |
| **9** | *"ਆਧਾਰ ਕਾਰਡ ਵਿੱਚ ਪਤਾ ਬਦਲਣ ਲਈ ਕਿਹੜੇ ਦਸਤਾਵੇਜ਼ ਚਾਹੀਦੇ ਹਨ?"* | `pa` | `DOCUMENT_REQUIREMENTS` | 100% Gurmukhi Punjabi response, POA list, ₹50 ਫੀਸ, myAadhaar ਪੋਰਟਲ। `VERIFIED_OFFICIAL_EXTERNAL_SOURCE` | *"ਕੀ ਬਿਨਾਂ ਦਸਤਾਵੇਜ਼ ਦੇ ਪਰਿਵਾਰ ਦੇ ਮੁਖੀ (HoF) ਦੀ ਸਹਿਮਤੀ ਨਾਲ ਆਧਾਰ ਪਤਾ ਬਦਲਿਆ ਜਾ ਸਕਦਾ ਹੈ?"* |

---

## 11. Verification Status Classifications

| Component / Feature | Implementation State | Verification Method | Status Classification |
| :--- | :---: | :---: | :---: |
| **Intelligent Query Router (10 categories)** | `backend/rag/query_router.py` | Automated Unit Tests & API | `IMPLEMENTED`, `AUTOMATED_TESTED`, `MANUALLY_VERIFIED` |
| **Official Service Retriever** | `backend/services/sources/official_service_retriever.py` | Automated Unit Tests & API | `IMPLEMENTED`, `AUTOMATED_TESTED`, `MANUALLY_VERIFIED` |
| **Aadhaar Document Requirements Retrieval** | Verified against official UIDAI catalog | Live API & Unit Tests | `IMPLEMENTED`, `AUTOMATED_TESTED`, `MANUALLY_VERIFIED`, `LIVE_SOURCE_VERIFIED` |
| **SSRF & Prompt Injection Security** | Domain whitelisting & regex sanitizers | Automated Security Tests | `IMPLEMENTED`, `AUTOMATED_TESTED`, `MANUALLY_VERIFIED` |
| **Contextual Follow-up Generator** | `backend/rag/followup_generator.py` | Automated Unit Tests & Frontend | `IMPLEMENTED`, `AUTOMATED_TESTED`, `MANUALLY_VERIFIED` |
| **Contextual Abstention Engine** | `backend/rag/answer_generator.py` | Automated Unit Tests & API | `IMPLEMENTED`, `AUTOMATED_TESTED`, `MANUALLY_VERIFIED` |
| **Source Provenance Labeling** | Response schemas & source resolver | Automated Unit Tests & API | `IMPLEMENTED`, `AUTOMATED_TESTED`, `MANUALLY_VERIFIED` |
| **Multilingual Response Language** | Multi-pass localized synthesis | Automated Unit Tests & API | `IMPLEMENTED`, `AUTOMATED_TESTED`, `MANUALLY_VERIFIED` |
| **Full Regression Suite** | 10 Platform Test Suites | `run_all_phase13_regressions.py` | `AUTOMATED_TESTED` (100% Pass) |
| **Unrestricted Web Search Engine** | Intentionally omitted by design | Strict security policy | `NOT_VERIFIED` (Prohibited by design) |

---

## 12. Conclusion

The usability defect has been completely resolved. SahyogSetu now accurately routes administrative inquiries to authoritative government sources, providing complete document lists and step-by-step procedures from verified authorities like UIDAI, while preserving its core grounded legal RAG pipeline for cooperative law. Irrelevant dispute questions have been eliminated, and abstentions are now context-aware and constructive. All 7 dedicated automated tests, all 11 language enforcement tests, and all 10 platform regression test suites pass with a 100% success rate.
