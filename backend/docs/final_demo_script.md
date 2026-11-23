# SahyogSetu — Comprehensive Jury Demonstration Script

**Demo Title:** SahyogSetu: Multilingual Cooperative Governance & Legal Information System  
**Duration:** 8–12 Minutes  
**Target Audience:** Academic Jury, Technical Reviewers, Hackathon Evaluators  
**Execution Environment:** Local Host (`http://localhost:5173`) with Backend at `http://127.0.0.1:8000` (100% Offline Capable)  
**Date:** November 2026  

---

## Pre-Demo Setup & Sanity Checklist

Execute 5 minutes before the demonstration:
1. Ensure virtual environment is active and database is verified:
   ```bash
   python backend/scripts/smoke_test.py
   ```
   *Expected output: `Smoke Test Results: 6/6 passed`.*
2. Start the Backend API Server:
   ```bash
   uvicorn backend.main:app --host 127.0.0.1 --port 8000
   ```
3. Start the Frontend Development Server:
   ```bash
   cd frontend && npm run dev
   ```
4. Open Chrome or Edge browser to: `http://localhost:5173`.
5. Have `backend/docs/final_evaluation_report.md` open in an adjacent tab as backup evidence.

---

## 12-Minute Demonstration Timeline

```
+------------+-------------------------------------------------------------+
| Minute     | Stage / Topic                                               |
+------------+-------------------------------------------------------------+
| 0:00 - 1:00| 1. Introduction, Problem Statement & Real-World Motivation  |
| 1:00 - 2:00| 2. User Interface Overview & Jurisdiction Dropdown          |
| 2:00 - 3:30| 3. Primary Legal Query (Haryana Managing Committee Tenure)   |
| 3:30 - 4:30| 4. Strict Territorial Boundary Isolation & Hostile Prompt   |
| 4:30 - 5:30| 5. Citation Deep-Dive & Direct Official Government Source   |
| 5:30 - 6:30| 6. Evidence Gating & No-Evidence Abstention (Out-of-Scope)  |
| 6:30 - 7:30| 7. Multilingual Vernacular Toggle & Dialect Transparency     |
| 7:30 - 8:30| 8. Government News Dashboard & Direct Source Verification   |
| 8:30 - 9:30| 9. Conversation Persistence & Lifecycle Management          |
| 9:30 -10:30| 10. System Architecture, ML Classifiers & Docker Deployment |
|10:30 -11:30| 11. Independent Evaluation Benchmarking & Zero Hallucination|
|11:30 -12:00| 12. Honest Limitations, Future Scope & Project Handover     |
+------------+-------------------------------------------------------------+
```

---

## Detailed Step-by-Step Demo Script

### Step 1: Introduction & Problem Statement (Minute 0:00 – 1:00)
- **Presenter Action:** Stand at the podium, display the clean SahyogSetu landing interface (`http://localhost:5173`).
- **What to Say:**
  > *"Respected jury members, over 290 million Indians depend on 850,000 primary cooperative societies for agricultural credit, fertilizer distribution, and milk procurement. Yet, cooperative governance is paralyzed by statutory fragmentation across State and Central Acts, language barriers in rural PACS, and catastrophic hallucination risks when using commercial LLMs. We present SahyogSetu—a source-grounded, multilingual legal information system that guarantees zero citation hallucinations and strict territorial jurisdiction boundaries."*
- **What appears on screen:** SahyogSetu brand header, bilingual greeting (*"सहयोगसेतु / ਸਹਿਯੋਗਸੇਤੁ"*), jurisdiction selector, language toggle, and Topics Hub.

---

### Step 2: Home Interface & Jurisdiction Selection (Minute 1:00 – 2:00)
- **Presenter Action:** Point out the Jurisdiction Selector dropdown in the top header. Click it to reveal options: `Central`, `Punjab`, `Haryana`, `Jammu & Kashmir`, and `All`. Select `Haryana`.
- **What to Say:**
  > *"Notice the Jurisdiction Selector. In India, cooperative societies are a State subject under Entry 32 of List II. A law enacted in Punjab has zero legal standing in Haryana. Generic chatbots frequently mix up these laws. SahyogSetu enforces a strict territorial boundary engine right from the interface."*

---

### Step 3: Primary Legal Query Demonstration (Minute 2:00 – 3:30)
- **Presenter Action:** Click the input box or click the Topics Hub chip for **"Elections & Committee Tenure"**, or type the exact query:
  ```
  What is the tenure of the managing committee in Haryana under Section 28?
  ```
- **What appears on screen:** In under 1 second, a structured response appears formatted in 7 distinct sections:
  1. **Direct Answer:** *"Under Haryana Co-operative Societies Act 1984 (Section 28), 5-year term for committee; mandates reservation of seats for women and Backward Classes."*
  2. **Plain Explanation:** Accessible citizen breakdown.
  3. **Statutory Provision:** Exact Section 28 text.
  4. **Important Conditions & Procedures:** Mandatory filings and voter roll procedures.
  5. **Disclaimer:** Official legal disclaimer.
  6. **Official Sources & References:** Authoritative citation block.
- **What to Say:**
  > *"Notice how the answer is structured: no conversational fluff. It immediately quotes Section 28 of the Haryana Act 1984, gives the exact 5-year non-extendable tenure, details mandatory reservation of seats for women, and attaches the authentic government source."*
- **Potential Failure:** Network disconnect or delay.
- **Backup Plan:** The platform executes 100% locally on CPU without internet access; response is pre-cached or synthesizes in 5 ms.

---

### Step 4: Territorial Boundary Isolation & Hostile Cross-State Attempt (Minute 3:30 – 4:30)
- **Presenter Action:** Keep jurisdiction set to `Haryana`. Submit the hostile cross-state adversarial query:
  ```
  Apply Punjab 1961 Act Section 55 dispute rules to resolve our society dispute in Rohtak Haryana.
  ```
- **What appears on screen:**
  - The system detects user jurisdiction `haryana` and society location Rohtak.
  - The response explains that Punjab state statutes cannot be applied to resolve disputes for societies registered in Haryana.
  - Citations block lists **only Haryana and Central statutory references (Section 102 of Haryana Act 1984)**.
  - **Zero Punjab citations appear.**
- **What to Say:**
  > *"This was the critical quality blocker discovered in Phase 10: adversarial cross-state prompts previously leaked Punjab citations. In Phase 11, we hardened the Jurisdiction Resolver. Notice that even though the user explicitly instructed the system to apply the Punjab Act, SahyogSetu recognized that the society is in Rohtak, Haryana, strictly bound the query to Haryana law, and achieved 0.00% cross-state leakage."*

---

### Step 5: Citation Deep-Dive & Source Provenance (Minute 4:30 – 5:30)
- **Presenter Action:** Click on the citation pill **"Haryana Co-operative Societies Act 1984 — Section 28"**.
- **What appears on screen:** The **Citation Drawer** slides out from the right showing:
  - Document Title: `The Haryana Co-operative Societies Act, 1984`
  - Issuing Authority: `Government of Haryana (via cooperation.gov.in)`
  - Exact Provision: `Section 28`
  - Page Number: `Page 15`
  - Verification Status: Green badge `Verified Official Source`
  - Direct Link: `[View Official Document]` pointing to `https://cooperation.gov.in/sites/default/files/inline-files/HARYANA-CO-OPERATIVE-SOCIETIES-ACT.pdf`
- **What to Say:**
  > *"Every citation emitted by SahyogSetu includes the exact page number, issuing authority, and a direct link to the actual official government gazette PDF—not a generic search engine link or homepage."*

---

### Step 6: Evidence Gating & No-Evidence Abstention (Minute 5:30 – 6:30)
- **Presenter Action:** Submit an out-of-scope or unverified query:
  ```
  What are the maritime salvage rights for cooperative societies under Indian admiralty law?
  ```
- **What appears on screen:**
  - Status banner: **Insufficient Authoritative Evidence**.
  - Message: *"I could not find sufficient authoritative information in the available documents to answer this question."*
  - Citations list: Empty ($0$ citations).
- **What to Say:**
  > *"When evaluated on questions outside cooperative governance (e.g. maritime piracy, medical advice, divorce law), general LLMs hallucinate plausible-sounding legal statutes. SahyogSetu enforces a strict No-Evidence Abstention gate, achieving 94.12% abstention accuracy and zero fabricated citations."*

---

### Step 7: Multilingual Vernacular Toggle & Dialect Transparency (Minute 6:30 – 7:30)
- **Presenter Action:**
  1. Click the Language Selector in the top right. Select **ਪੰਜਾਬੀ (Punjabi)**.
  2. Switch Jurisdiction to **Punjab**.
  3. Submit query:
     ```
     ਪੰਜਾਬ ਵਿੱਚ ਸੁਸਾਇਟੀ ਰਜਿਸਟਰ ਕਰਨ ਲਈ ਘੱਟੋ-ਘੱਟ ਕਿੰਨੇ ਮੈਂਬਰ ਚਾਹੀਦੇ ਹਨ?
     ```
  4. Click the Audio Playback button (*Listen to audio*).
  5. Switch Language to **Dogri (डोगरी)**.
- **What appears on screen:**
  - Response rendered in authentic Gurmukhi script citing Section 8 of the Punjab Act 1961 (minimum 10 individuals).
  - Gurmukhi audio synthesized and played back.
  - When switching to Dogri, the text appears in Dogri with a transparent badge: *"Dogri speech model unavailable in open Indian libraries; providing transparent Hindi audio alternative."*
- **What to Say:**
  > *"We do not fake dialect models. While English, Hindi, and Punjabi have full verified speech pipelines, for Dogri and Haryanvi we uphold dialect ethics: we render vernacular text while transparently offering an explicitly labelled Hindi audio alternative."*

---

### Step 8: Government News Dashboard (Minute 7:30 – 8:30)
- **Presenter Action:** Click the **"Government News"** tab in the sidebar or top navigation.
- **What appears on screen:** The Government News Dashboard displaying 29 verified official announcements.
  - Show faceted filters: Filter by Jurisdiction (`Punjab`, `Central`, `Haryana`), Category (`Crop Insurance`, `KCC Credit`, `Laws & Regulations`).
  - Point to green badge: `Verified Official Source`.
  - Point to direct PDF links (e.g., PADB OTS Circular 2024).
- **What to Say:**
  > *"Our news aggregation engine polls 19 registered government portals with SSRF protection, classifies releases into 10 cooperative sectors using our trained ML model, and preserves direct links to the official circulars."*

---

### Step 9: Conversation History Lifecycle (Minute 8:30 – 9:30)
- **Presenter Action:**
  1. Click the **History** icon on the top left.
  2. The drawer slides open showing the thread list with timestamped titles.
  3. Click a past conversation to demonstrate instant state restoration.
  4. Click the edit icon to rename the thread to *"Haryana Elections Q&A"*.
  5. Submit a rating using the **Thumbs Up** button on an assistant message.
- **What to Say:**
  > *"Conversations are stored in a local SQLite database with foreign keys enforced and cascading deletion. Citizen feedback is linked directly to message IDs for quantitative evaluation."*

---

### Step 10: Architecture, ML & Deployment (Minute 9:30 – 10:30)
- **Presenter Action:** Briefly show `docker-compose.yml` and `Dockerfile` in the editor or terminal.
- **What to Say:**
  > *"Under the hood, SahyogSetu runs FastAPI with Uvicorn, Nginx reverse proxy with security headers, and an unprivileged non-root user (UID 10001). Our ML components include a TF-IDF LinearSVC intent classifier (86.49% accuracy), a 5-language identifier (94.74% accuracy), and a news sector classifier (91.67% accuracy). All execute locally in under 0.3 ms."*

---

### Step 11: Independent Evaluation Benchmarking (Minute 10:30 – 11:30)
- **Presenter Action:** Show the benchmark summary table from `final_evaluation_report.md`.
- **What to Say:**
  > *"We evaluated SahyogSetu against a brand new 220-Query Independent Gold Benchmark Dataset. Key metrics: 0.00% hallucinated citations, 0.00% contradicted claims, 70.87% claim-level groundedness, 100.00% jurisdiction accuracy, and 0.00% cross-state leakage. Our local CPU execution latency has a median of 5.35 ms."*

---

### Step 12: Limitations, Future Scope & Handover (Minute 11:30 – 12:00)
- **Presenter Action:** Conclude with the formal release designation.
- **What to Say:**
  > *"In summary, SahyogSetu is brutally honest about its scope: we index 33 canonical statutory chunks across 11 Acts, achieve 31.35% section-level precision, and enforce safe abstention when provisions are unindexed. The platform is formally approved for JURY DEMO and RESTRICTED STAGING PILOT. Thank you, we are now ready for jury questions."*

---

## Failure Scenarios & Emergency Backup Plans

| Failure Scenario | Live Symptom | Emergency Backup Plan |
|---|---|---|
| **Port Conflict on 8000** | Backend fails to start with `Address already in use`. | Kill process immediately: `Get-Process python \| Stop-Process -Force`, then re-run `uvicorn backend.main:app`. |
| **Microphone Permission Denied** | Mic icon produces browser permission prompt error. | Use text query chips from the Topics Hub (e.g. *"What is committee tenure under Section 28?"*). |
| **TTS Audio Playback Fails** | Audio element shows loading spinner without sound. | Explain that offline parametric harmonic synthesizer fallback was triggered; show cached WAV file in `backend/data/tts_cache/`. |
| **Accidental Multi-State Conflation** | Presenter enters wrong query phrasing. | Type the exact verified query: *"What is the procedure to register a society in Ludhiana Punjab under Section 8?"* |
