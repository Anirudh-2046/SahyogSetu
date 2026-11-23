"""
User Query Intent Detector for SahyogSetu
Implements Phase 6D:
Categorizes user queries into 9 defined cooperative intents:
1. legal_information
2. cooperative_registration
3. membership_rights
4. elections_governance
5. financial_assistance_kcc
6. government_schemes_pmkisan
7. pmfby_crop_insurance
8. grievance_arbitration
9. general_cooperative
"""

from typing import Tuple, Dict, Any

INTENT_KEYWORDS: Dict[str, list] = {
    "government_schemes_pmkisan": [
        "pm-kisan", "pm kisan", "kisan samman", "ਕਿਸਾਨ ਸਨਮਾਨ", "किसान सम्मान", "2000", "6000", "kisan nidhi", "किस्त", "ਕਿਸ਼ਤ"
    ],
    "financial_assistance_kcc": [
        "kcc", "kisan credit", "crop loan", "interest subvention", "miss", "4%", "ਕ੍ਰੈਡਿਟ ਕਾਰਡ", "क्रेडिट कार्ड", "फसली ऋण", "ਕਰਜ਼ਾ", "ऋण", "कर्ज"
    ],
    "pmfby_crop_insurance": [
        "pmfby", "fasal bima", "crop insurance", "ਫਸਲ ਬੀਮਾ", "फसल बीमा", "inundation", "72 hour", "72 ਘੰਟੇ", "72 घंटे", "ਗੜੇਮਾਰੀ", "ओलावृष्टि"
    ],
    "cooperative_registration": [
        "register", "registration", "forming", "formation", "start society", "ਰਜਿਸਟਰ", "पंजीकरण", "गठन", "form-a", "ਫਾਰਮ-ਏ", "फॉर्म-ए", "बणाणा"
    ],
    "membership_rights": [
        "member", "membership", "voting", "expulsion", "one member one vote", "ਮੈਂਬਰਸ਼ਿਪ", "ਮੈਂਬਰ", "सदस्यता", "सदस्य", "ਵੋਟ ਦਾ ਅਧਿਕਾਰ"
    ],
    "elections_governance": [
        "election", "managing committee", "tenure", "5 year", "board", "ਵੋਟਾਂ", "ਚੋਣ", "चुनाव", "कमेटी", "आरक्षण", "reservation"
    ],
    "grievance_arbitration": [
        "dispute", "arbitration", "section 55", "section 102", "section 70", "ombudsman", "ਝਗੜਾ", "ਵਿਵਾਦ", "विवाद", "आर्बिट्रेशन", "शिकायत", "ਰਪਟ"
    ],
    "legal_information": [
        "act", "rule", "section", "amendment", "law", "statute", "ਐਕਟ", "ਨਿਯਮ", "ਕਾਨੂੰਨ", "धारा", "अधिनियम", "नियम"
    ],
}

class QueryIntentDetector:
    """Classifies user intent from natural language cooperative queries using ML with rule-based fallback."""

    def detect(self, query: str) -> Tuple[str, float, Dict[str, Any]]:
        # 1. Attempt ML Intent Classification
        try:
            from backend.ml.inference.intent_inference import intent_predictor
            ml_res = intent_predictor.predict_intent(query, threshold=0.35)
            if not ml_res.get("is_uncertain", False):
                return (
                    ml_res["predicted_intent"],
                    round(float(ml_res["confidence"]), 2),
                    {
                        "source": "ml_intent_model",
                        "all_probabilities": ml_res.get("all_probabilities", {}),
                        "extracted_sections": ml_res.get("extracted_sections", []),
                    },
                )
        except Exception as e:
            pass

        # 2. Deterministic Rule-Based Fallback
        q = query.lower()
        matched_intents = {}

        for intent, kw_list in INTENT_KEYWORDS.items():
            matches = [k for k in kw_list if k in q]
            if matches:
                matched_intents[intent] = len(matches)

        if not matched_intents:
            return "general_cooperative", 0.65, {"source": "rule_fallback", "matches": []}

        top_intent = max(matched_intents, key=matched_intents.get)
        count = matched_intents[top_intent]
        confidence = min(0.98, max(0.70, 0.60 + (count * 0.12)))

        return top_intent, round(confidence, 2), {
            "source": "rule_fallback",
            "matched_intents": matched_intents,
            "top_intent": top_intent,
        }

intent_detector = QueryIntentDetector()
