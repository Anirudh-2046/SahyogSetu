"""
Cooperative News Category Classifier
Classifies announcements into 11 statutory and public service categories:
1. coop_laws_regulations
2. coop_registration
3. elections_governance
4. gov_schemes
5. agri_credit_kcc
6. crop_insurance_pmfby
7. dairy_fisheries_coop
8. subsidies_financial_aid
9. grievance_redressal
10. administrative_notifications
11. other_updates
"""

import re
from typing import Tuple, List, Dict, Any

CATEGORIES: Dict[str, Dict[str, Any]] = {
    "coop_laws_regulations": {
        "title": "Cooperative laws and regulations",
        "keywords": [
            "act", "rule", "section", "amendment", "statutory", "bye-law", "byelaw", "ordinance",
            "कानून", "अधिनियम", "धारा", "नियम", "उप-नियम", "ਸੋਧ", "ਐਕਟ", "ਧਾਰਾ", "ਕਾਨੂੰਨ", "ਬਾਈ-ਲਾਜ਼",
            "arbitration", "section 102", "section 9", "mscs"
        ]
    },
    "coop_registration": {
        "title": "Cooperative society registration",
        "keywords": [
            "registration", "register", "incorporation", "formation", "new pacs", "society formation",
            "पंजीकरण", "रजिस्ट्रेशन", "गठन", "नई समिति", "ਰਜਿਸਟ੍ਰੇਸ਼ਨ", "ਗਠਨ", "ਨਵੀਂ ਸਭਾ"
        ]
    },
    "elections_governance": {
        "title": "Elections and governance",
        "keywords": [
            "election", "managing committee", "board", "director", "general body", "agm", "audit", "voting",
            "चुनाव", "निर्वाचन", "प्रबंध समिति", "आम सभा", "ऑडिट", "ਚੋਣ", "ਪ੍ਰਬੰਧਕ ਕਮੇਟੀ", "ਆਮ ਮੀਟਿੰਗ", "ਆਡਿਟ"
        ]
    },
    "gov_schemes": {
        "title": "Government schemes",
        "keywords": [
            "scheme", "mission", "program", "pacs computerization", "aif", "agriculture infrastructure",
            "योजना", "मिशन", "परियोजना", "ਸਕੀਮ", "ਮਿਸ਼ਨ", "ਕੰਪਿਊਟਰੀਕਰਨ", "erp", "cloud"
        ]
    },
    "agri_credit_kcc": {
        "title": "Agricultural credit and KCC",
        "keywords": [
            "kisan credit card", "kcc", "crop loan", "interest subvention", "rbi circular", "short-term loan",
            "केसीसी", "फसली ऋण", "किसान क्रेडिट कार्ड", "ब्याज अनुदान", "ਕਰਜ਼ਾ", "ਫ਼ਸਲੀ ਕਰਜ਼ਾ", "ਵਿਆਜ ਛੋਟ"
        ]
    },
    "crop_insurance_pmfby": {
        "title": "PMFBY and crop insurance",
        "keywords": [
            "pmfby", "crop insurance", "claim", "damage", "hailstorm", "flood", "yield",
            "फसल बीमा", "बीमा दावा", "मुआवजा", "ਫ਼ਸਲ ਬੀਮਾ", "ਨੁਕਸਾਨ", "ਮੁਆਵਜ਼ਾ"
        ]
    },
    "dairy_fisheries_coop": {
        "title": "Dairy and fisheries cooperatives",
        "keywords": [
            "dairy", "milk", "fisheries", "cattle", "livestock", "animal husbandry", "verka", "vita",
            "डेयरी", "दुग्ध", "मत्स्य", "ਪਸ਼ੂ ਪਾਲਣ", "ਡੇਅਰੀ", "ਦੁੱਧ", "ਮੱਛੀ ਪਾਲਣ"
        ]
    },
    "subsidies_financial_aid": {
        "title": "Financial assistance and subsidies",
        "keywords": [
            "subsidy", "financial assistance", "grant", "ots", "one-time settlement", "waiver",
            "सब्सिडी", "वित्तीय सहायता", "छूट", "मुआवजा", "ਇੱਕਮੁਸ਼ਤ", "ਮੁਆਫ਼ੀ", "ਸਬਸਿਡੀ", "ਗ੍ਰਾਂਟ"
        ]
    },
    "grievance_redressal": {
        "title": "Grievance redressal",
        "keywords": [
            "grievance", "complaint", "ombudsman", "dispute", "investigation", "inquiry",
            "शिकायत", "लोकपाल", "विवाद", "ਜਾਂਚ", "ਸ਼ਿਕਾਇਤ", "ਨਿਵਾਰਨ"
        ]
    },
    "administrative_notifications": {
        "title": "Administrative notifications",
        "keywords": [
            "transfer", "posting", "order", "notification", "circular", "directive", "gazette",
            "आदेश", "अधिसूचना", "परिपत्र", "ਹੁਕਮ", "ਸਰਕੂਲਰ", "ਨੋਟੀਫਿਕੇਸ਼ਨ"
        ]
    },
    "other_updates": {
        "title": "Other relevant government updates",
        "keywords": []
    }
}

class NewsClassifier:
    """Classifies news items into cooperative categories based on lexical and contextual rules."""

    @classmethod
    def classify(cls, text: str, source_metadata: Dict[str, Any] = None) -> Tuple[str, float, bool]:
        """
        Returns (category_id, confidence_score, is_uncertain).
        """
        if not text:
            return "other_updates", 0.5, True

        text_lower = text.lower()
        scores: Dict[str, int] = {cat: 0 for cat in CATEGORIES}

        # Match keywords
        for cat_id, cat_info in CATEGORIES.items():
            for kw in cat_info["keywords"]:
                if kw.lower() in text_lower:
                    scores[cat_id] += 1

        # Check explicit category hints in source metadata if present
        if source_metadata and "category" in source_metadata and source_metadata["category"] in CATEGORIES:
            scores[source_metadata["category"]] += 3

        # Integrate ML News Classifier prediction
        try:
            from backend.ml.inference.news_inference import news_predictor
            ml_res = news_predictor.predict_category(text, threshold=0.35)
            if not ml_res.get("is_uncertain", False):
                ml_cat = ml_res["predicted_category"]
                if ml_cat in scores:
                    scores[ml_cat] += 2
        except Exception:
            pass

        best_cat = max(scores, key=scores.get)
        max_score = scores[best_cat]

        if max_score >= 3:
            return best_cat, 0.90, False
        elif max_score >= 1:
            return best_cat, 0.75, False
        else:
            return "other_updates", 0.50, True
