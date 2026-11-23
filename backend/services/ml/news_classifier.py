"""
News Category Classifier for SahyogSetu
Implements Phase 6B:
Classifies news announcements across the 10 mandated cooperative sectors:
1. coop_laws_regulations
2. coop_registration
3. elections_governance
4. government_schemes
5. agri_credit_kcc
6. pmfby_insurance
7. dairy_fisheries
8. finance_subsidies
9. grievance_arbitration
10. government_notifications
"""

from typing import Tuple, Dict, Any, List

CATEGORY_RULES: Dict[str, Dict[str, Any]] = {
    "pmfby_insurance": {
        "keywords": ["pmfby", "fasal bima", "crop insurance", "ਫਸਲ ਬੀਮਾ", "फसल बीमा", "inundation", "hailstorm", "calamity", "weather-based"],
        "weight": 3.0,
    },
    "agri_credit_kcc": {
        "keywords": ["kcc", "kisan credit card", "crop loan", "interest subvention", "miss", "4%", "ਕ੍ਰੈਡਿਟ ਕਾਰਡ", "क्रेडिट कार्ड", "फसली ऋण", "rbi master circular"],
        "weight": 2.8,
    },
    "pacs_computerization": {
        "keywords": ["computerization", "erp", "pacs", "63,000", "multi-service", "ਕੰਪਿਊਟਰੀਕਰਨ", "कंप्यूटरीकरण", "software", "hardware"],
        "weight": 2.5,
    },
    "coop_registration": {
        "keywords": ["register", "registration", "forming", "formation", "new society", "ਫਾਰਮ-ਏ", "ਰਜਿਸਟਰ", "पंजीकरण", "गठन", "form-a"],
        "weight": 2.5,
    },
    "elections_governance": {
        "keywords": ["election", "managing committee", "tenure", "5 years", "board", "ਵੋਟਾਂ", "ਚੋਣ", "चुनाव", "कमेटी", "आरक्षण", "reservation"],
        "weight": 2.2,
    },
    "grievance_arbitration": {
        "keywords": ["dispute", "arbitration", "section 55", "section 102", "section 70", "ombudsman", "ਝਗੜਾ", "ਵਿਵਾਦ", "विवाद", "आर्बिट्रेशन", "शिकायत"],
        "weight": 2.5,
    },
    "dairy_fisheries": {
        "keywords": ["dairy", "milk", "fisheries", "matsya", "verka", "vita", "ਦੁੱਧ", "ਡੇਅਰੀ", "डेयरी", "मत्स्य", "मछली"],
        "weight": 2.2,
    },
    "finance_subsidies": {
        "keywords": ["ots", "settlement", "waiver", "subsidy", "outlay", "penal interest", "ਮੁਆਫੀ", "ਛੋਟ", "अनुदान", "ब्याज छूट"],
        "weight": 2.4,
    },
    "coop_laws_regulations": {
        "keywords": ["act", "rules", "amendment", "statutory", "section", "clause", "ਐਕਟ", "ਨਿਯਮ", "ਅਧਿਨਿਯਮ", "कानून", "धारा", "उप-नियम"],
        "weight": 2.0,
    },
    "government_notifications": {
        "keywords": ["notification", "gazette", "order", "circular", "directive", "ਨੋਟੀਫਿਕੇਸ਼ਨ", "ਗਜ਼ਟ", "ਅਧਿਸੂਚਨਾ", "राजपत्र", "आदेश"],
        "weight": 1.5,
    },
}

class MLNewsClassifier:
    """Classifies government text into structured cooperative categories using ML with rule-based fallback."""

    def classify(self, text: str) -> Tuple[str, float, Dict[str, Any]]:
        # 1. Attempt ML News Classification
        try:
            from backend.ml.inference.news_inference import news_predictor
            ml_res = news_predictor.predict_category(text, threshold=0.35)
            if not ml_res.get("is_uncertain", False):
                return (
                    ml_res["predicted_category"],
                    round(float(ml_res["confidence"]), 2),
                    {
                        "source": "ml_news_model",
                        "top_sectors": ml_res.get("top_sectors", []),
                        "all_probabilities": ml_res.get("all_probabilities", {}),
                    },
                )
        except Exception:
            pass

        # 2. Deterministic Rule-Based Fallback
        t_lower = text.lower()
        scores: Dict[str, float] = {}

        for cat, data in CATEGORY_RULES.items():
            matches = [kw for kw in data["keywords"] if kw in t_lower]
            if matches:
                scores[cat] = len(matches) * data["weight"]

        if not scores:
            return "government_notifications", 0.60, {"source": "rule_fallback", "reason": "default_fallback"}

        top_cat = max(scores, key=scores.get)
        raw_score = scores[top_cat]
        conf = min(0.98, max(0.65, 0.50 + (raw_score * 0.10)))

        return top_cat, round(conf, 2), {"source": "rule_fallback", "scores": scores, "top_category": top_cat}

ml_news_classifier = MLNewsClassifier()
