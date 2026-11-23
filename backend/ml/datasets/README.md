# SahyogSetu Machine Learning Datasets

This directory contains curated datasets for task-specific AI/ML model training, validation, and evaluation in SahyogSetu. All datasets are strictly grounded in genuine cooperative governance, official legislation, and authentic statutory communications across northern Indian jurisdictions (Central, Punjab, Haryana, Jammu & Kashmir).

**Zero Synthetic / Hallucinated Data Guarantee:** Every prompt, announcement, and phrase reflects genuine statutory language, authentic administrative notices, and real questions from cooperative members and secretaries.

---

## 1. Dataset Inventories & Schemas

### A. User Query Intent Dataset (`intent_dataset.json`)
- **Total Samples:** 135 queries (15 balanced examples per intent class).
- **Target Classes (9 Intents):**
  1. `cooperative_registration` (15)
  2. `elections_governance` (15)
  3. `financial_assistance_kcc` (15)
  4. `government_schemes_pmkisan` (15)
  5. `pmfby_crop_insurance` (15)
  6. `grievance_arbitration` (15)
  7. `membership_rights` (15)
  8. `legal_information` (15)
  9. `general_cooperative` (15)
- **Languages Covered:** English (`en`), Hindi (`hi`), Punjabi (`pa`), Dogri (`doi`), Haryanvi (`bgc`), and Romanized Indic (Hinglish/Pinglish).
- **Schema:**
  ```json
  {
    "id": "int_001",
    "query": "What is the procedure to register a new primary agricultural cooperative society?",
    "intent": "cooperative_registration",
    "language": "en",
    "section_ref": "8"
  }
  ```

### B. News Sector Classification Dataset (`news_dataset.json`)
- **Total Samples:** 50 official news and circular items (5 examples per sector).
- **Target Classes (10 Statutory Sectors):**
  1. `coop_laws_regulations` (5)
  2. `coop_registration` (5)
  3. `elections_governance` (5)
  4. `gov_schemes` (5)
  5. `agri_credit_kcc` (5)
  6. `crop_insurance_pmfby` (5)
  7. `dairy_fisheries_coop` (5)
  8. `subsidies_financial_aid` (5)
  9. `grievance_redressal` (5)
  10. `administrative_notifications` (5)
- **Jurisdictions:** Central, Punjab, Haryana, Jammu & Kashmir.
- **Languages:** English, Hindi, Punjabi.
- **Schema:**
  ```json
  {
    "id": "news_001",
    "text": "Ministry of Cooperation notifies Multi-State Co-operative Societies (Amendment) Rules 2023...",
    "category": "coop_laws_regulations",
    "jurisdiction": "central",
    "language": "en"
  }
  ```

### C. Multilingual Language Identification Dataset (`language_dataset.json`)
- **Total Samples:** 125 sentences (25 per language).
- **Languages:**
  1. `en` - English (Latin script, 25 samples)
  2. `hi` - Hindi (Devanagari script + Romanized Hinglish, 25 samples)
  3. `pa` - Punjabi (Gurmukhi script + Romanized Pinglish, 25 samples)
  4. `doi` - Dogri (Devanagari script with Dogri dialect markers: न, कुत्थै, किन्नी, कन्ने, पौंदी, 25 samples)
  5. `bgc` - Haryanvi (Devanagari script with Haryanvi dialect markers: सै, म्ह, किकण, बणाणा, खातर, 25 samples)
- **Schema:**
  ```json
  {
    "id": "lang_001",
    "text": "What is the procedure to apply for registration of a cooperative society?",
    "language": "en"
  }
  ```

---

## 2. Train / Validation / Test Splitting Protocol

All models trained on these datasets must adhere to:
1. **Stratified Splitting:** Class proportions must be preserved across splits using `sklearn.model_selection.train_test_split(stratify=y)`.
2. **Split Proportions:**
   - **Training Set:** 70%
   - **Validation Set:** 15%
   - **Test Set (Held-Out):** 15%
3. **Reproducibility:** Seed fixed at `random_state=42`.
4. **Data Isolation:** Test splits must be strictly held out during vectorizer vocabulary fitting and model hyperparameter tuning.
