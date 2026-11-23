"""
Legal Query Processor for SahyogSetu
Extracts statutory section numbers, legal intents, scheme names,
and cleans query strings for hybrid semantic and keyword retrieval.
"""

import re
from typing import Dict, Any, List, Optional

INTENT_KEYWORD_MAP = {
    "pm_kisan": ["pm-kisan", "pm kisan", "ਕਿਸਾਨ ਸਨਮਾਨ", "किसान सम्मान", "2000", "6000", "kisan nidhi", "samman nidhi"],
    "financial_assistance_kcc": ["kcc", "kisan credit", "ਕ੍ਰੈਡਿਟ ਕਾਰਡ", "क्रेडिट कार्ड", "crop loan", "फसली ऋण", "interest subvention", "miss", "collateral", "1.60 lakh", "4%"],
    "pmfby_crop_insurance": ["pmfby", "fasal bima", "crop insurance", "ਫਸਲ ਬੀਮਾ", "फसल बीमा", "inundation", "calamity", "damage", "72 hour", "72 ਘੰਟੇ", "72 घंटे", "crop damage", "kharif", "rabi", "reporting", "deadline"],
    "cooperative_registration": ["register", "registration", "forming", "start society", "ਰਜਿਸਟਰ", "ਪੰਜੀਕਰਨ", "पंजीकरण", "गठन", "members required", "minimum members", "ਕਿੰਨੇ ਮੈਂਬਰ", "कितने सदस्य", "ਘੱਟੋ-ਘੱਟ", "ਸੁਸਾਇਟੀ", "ਸਭਾ"],
    "elections_governance": ["election", "managing committee", "tenure", "5 year", "5-year", "5 ਸਾਲ", "5 वर्ष", "5 साल", "ਚੋਣ", "चुनाव", "कमेटी", "कार्यकाल", "ਕਾਰਜਕਾਲ", "ਮਿਆਦ", "अवधि", "board of directors", "reservation"],
    "dispute_arbitration": ["dispute", "arbitration", "section 55", "section 102", "section 70", "section 84", "ਝਗੜਾ", "ਵਿਵਾਦ", "विवाद", "आर्बिट्रेशन", "arbitrator", "ਨਿਪਟਾਰਾ", "सुलह", "फैसला", "ਸਾਲਸੀ"],
    "audit_inspection": ["audit", "accounts", "inspection", "ਆਡਿਟ", "ऑडिट", "ਲੇਖਾ", "हिसाब", "chartered accountant"],
    "pacs_reforms": ["pacs", "computerization", "model bye-law", "model byelaw", "ਬਾਈ-ਲਾਅ", "उप-नियम", "common service center", "csc", "diversify"],
    "ots_waiver": ["ots", "one time settlement", "penal interest", "waiver", "ਛੋਟ", "ਮੁਆਫੀ", "छूट", "defaulter"],
}

# Cross-lingual expansion to English statutory terminology
CROSS_LINGUAL_TERMS = {
    "कार्यकाल": ["tenure", "5-year", "committee"],
    "ਕਾਰਜਕਾਲ": ["tenure", "5-year", "committee"],
    "ਮਿਆਦ": ["tenure", "5-year", "committee"],
    "अवधि": ["tenure", "5-year", "committee"],
    "प्रबंध समिति": ["managing committee", "committee"],
    "ਪ੍ਰਬੰਧਕੀ": ["managing committee", "committee"],
    "ਕਮੇਟੀ": ["committee", "managing committee"],
    "पंजीकरण": ["registration", "members"],
    "ਰਜਿਸਟਰ": ["registration", "members"],
    "ਸੁਸਾਇਟੀ": ["society", "registration"],
    "ਮੈਂਬਰ": ["members", "persons", "adult"],
    "ਮੈਂਬਰਾਂ": ["members", "persons"],
    "ਸਦੱਸ": ["members", "persons"],
    "सदस्य": ["members", "persons", "adult"],
    "सदस्यों": ["members", "persons"],
    "ਘੱਟੋ-ਘੱਟ": ["minimum", "at least"],
    "ਘੱਟੋ ਘੱਟ": ["minimum", "at least"],
    "कम से कम": ["minimum", "at least"],
    "ਅਰਜ਼ੀ": ["application", "procedure"],
    "ਦਰਖਾਸਤ": ["application", "procedure"],
    "आवेदन": ["application", "procedure"],
    "ਨਿਯਮ": ["rules", "byelaws", "bye-laws"],
    "ਨਿਯਮਾਂ": ["rules", "byelaws"],
    "ਕਾਨੂੰਨ": ["act", "statute", "provisions"],
    "विवाद": ["dispute", "arbitration"],
    "ਝਗੜਾ": ["dispute", "arbitration"],
    "ਨਿਪਟਾਰਾ": ["dispute", "settlement"],
    "ऑडिट": ["audit", "accounts"],
    "ਆਡਿਟ": ["audit", "accounts"],
    "फसल बीमा": ["crop insurance", "pmfby"],
    "ਫਸਲ ਬੀਮਾ": ["crop insurance", "pmfby"],
    "ਨੁਕਸਾਨ": ["calamity", "damage", "72 hours"],
    "नुकसान": ["calamity", "damage", "72 hours"],
}

class QueryProcessor:
    """Processes legal queries into structured search requests."""

    @classmethod
    def process_query(cls, query: str) -> Dict[str, Any]:
        """
        Extracts intent, section references, numeric parameters, and search tokens.
        """
        q_clean = query.strip()
        q_lower = q_clean.lower()

        # 1. Detect Intent using ML Intent Classifier with Rule Fallback
        detected_intent = "general_coop"
        try:
            from backend.ml.inference.intent_inference import intent_predictor
            ml_intent_res = intent_predictor.predict_intent(q_clean, threshold=0.35)
            if not ml_intent_res.get("is_uncertain", False):
                raw_pred = ml_intent_res["predicted_intent"]
                # Align naming with internal RAG conventions
                INTENT_NORMALIZATION = {
                    "government_schemes_pmkisan": "pm_kisan",
                    "grievance_arbitration": "dispute_arbitration",
                    "general_cooperative": "general_coop",
                }
                detected_intent = INTENT_NORMALIZATION.get(raw_pred, raw_pred)
        except Exception:
            pass

        if detected_intent == "general_coop":
            for intent, keywords in INTENT_KEYWORD_MAP.items():
                if any(kw in q_lower for kw in keywords):
                    detected_intent = intent
                    break

        # 2. Extract Statutory Section Numbers (e.g. Section 8, Rule 28, ਧਾਰਾ 55, धारा 6, Section 15.3, 2.1)
        extracted_sections: List[str] = []
        sec_matches = re.findall(r"(?:section|rule|sec|ਧਾਰਾ|धारा|clause|para|paragraph)\s*(\d+(?:\.\d+)?[A-Za-z]?)", q_lower)
        for sm in sec_matches:
            clean_sm = sm.rstrip(".")
            if clean_sm not in extracted_sections:
                extracted_sections.append(clean_sm)
        # Handle standalone section numbers if preceded or followed by statutory words
        if not extracted_sections:
            standalone = re.findall(r"\b(?:u/s|under\s+s\.)\s*(\d+(?:\.\d+)?[A-Za-z]?)", q_lower)
            for sa in standalone:
                if sa not in extracted_sections:
                    extracted_sections.append(sa.rstrip("."))

        # 3. Extract Key Monetary or Numeric Limits (e.g. 6000, 1.60 lakh, 10 members)
        numeric_entities: List[str] = []
        if re.search(r"\b(?:6000|₹6,?000)\b", q_lower):
            numeric_entities.append("6000_annual_support")
        if re.search(r"\b(?:1\.60|1\.6|160000|1,60,000)\b", q_lower):
            numeric_entities.append("1.60_lakh_collateral_free")
        if re.search(r"\b(?:72\s*(?:hours|ਘੰਟੇ|घंटे|hrs))\b", q_lower):
            numeric_entities.append("72_hours_reporting")
        if re.search(r"\b(?:5\s*(?:years|ਸਾਲ|वर्ष|साल))\b", q_lower):
            numeric_entities.append("5_years_tenure")

        # 4. Generate Search Keywords
        # Strip stop words and punctuation for BM25/keyword retrieval
        clean_tokens = re.findall(r"[\w]+", q_lower)
        stop_words = {"the", "a", "an", "is", "of", "and", "in", "to", "for", "what", "how", "many", "are", "under"}
        keywords = [t for t in clean_tokens if t not in stop_words and len(t) > 2]

        for native_term, eng_terms in CROSS_LINGUAL_TERMS.items():
            if native_term in q_lower:
                for et in eng_terms:
                    for tok in et.split():
                        if tok not in keywords:
                            keywords.append(tok)

        return {
            "original_query": q_clean,
            "detected_intent": detected_intent,
            "extracted_sections": extracted_sections,
            "numeric_entities": numeric_entities,
            "search_keywords": keywords,
        }

query_processor = QueryProcessor()
