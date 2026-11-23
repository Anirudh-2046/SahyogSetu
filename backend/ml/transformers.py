"""
Custom Scikit-Learn Transformers for SahyogSetu Machine Learning Pipelines
Provides domain-specific lexicons and cross-lingual expansions.
"""

from typing import List
from sklearn.base import BaseEstimator, TransformerMixin

INTENT_CROSS_LINGUAL_MAP = {
    "ਰਜਿਸਟਰ": "registration", "ਪੰਜੀਕਰਨ": "registration", "ਪੰਜੀਕਰਣ": "registration", "ਗਠਨ": "formation",
    "ਰਜਿਸਟਰੇਸ਼ਨ": "registration", "पंजीकरण": "registration", "ਮੈਂਬਰ": "member", "ਮੈਂਬਰਸ਼ਿਪ": "membership",
    "ਸਦੱਸ": "member", "ਸਦੱਸਤਾ": "membership", "सदस्य": "member", "सदस्यता": "membership",
    "ਚੋਣ": "election", "ਚੋਣਾਂ": "election", "ਵੋਟਾਂ": "election", "ਵੋਟਰ": "voter", "ਵੋਟ": "vote",
    "चुनाव": "election", "निर्वाचन": "election", "कमेटी": "committee", "ਕਮੇਟੀ": "committee",
    "ਕਾਰਜਕਾਲ": "tenure", "कार्यकाल": "tenure", "ਮਿਆਦ": "tenure", "अवधि": "tenure",
    "ਕਰਜ਼ਾ": "loan", "ਫ਼ਸਲੀ ਕਰਜ਼ਾ": "crop loan", "ऋण": "loan", "कर्जा": "loan", "ਬਿਆਜ": "interest", "ब्याज": "interest",
    "ਬੀਮਾ": "insurance", "बीमा": "insurance", "ਖਰਾਬਾ": "damage", "ਨੁਕਸਾਨ": "damage", "ਓਲਾ": "hailstorm", "ਗੜੇਮਾਰੀ": "hailstorm",
    "ਝਗੜਾ": "dispute", "ਵਿਵਾਦ": "dispute", "विवाद": "dispute", "ਸਾਲਸੀ": "arbitration", "ਸਾਲਸ": "arbitrator",
    "ਮੱਧਸਥਤਾ": "arbitration", "आर्बिट्रेशन": "arbitration", "मध्यस्थता": "arbitration", "ਗਬਨ": "surcharge", "गबन": "surcharge",
    "ਆਡਿਟ": "audit", "ऑडिट": "audit", "ਅੰਕੇਕਸ਼ਣ": "audit", "ਕਾਨੂੰਨ": "legal", "ਐਕਟ": "act", "ਅਧਿਨਿਯਮ": "act", "अधिनियम": "act", "ਨਿਯਮ": "rules", "धारा": "section", "ਧਾਰਾ": "section",
    "ਪੈਕਸ": "pacs", "पैक्स": "pacs", "ਕੰਪਿਊਟਰੀਕਰਨ": "computerization", "कंप्यूटरीकरण": "computerization",
    "ਕਿਸਾਨ ਸਨਮਾਨ": "pmkisan", "किसान सम्मान": "pmkisan", "ਕਿਸ਼ਤ": "installment", "किस्त": "installment",
}

NEWS_CROSS_LINGUAL_MAP = {
    "kcc": "kcc_credit", "ਕ੍ਰੈਡਿਟ ਕਾਰਡ": "kcc_credit", "क्रेडिट कार्ड": "kcc_credit", "crop loan": "kcc_credit",
    "pmfby": "crop_insurance", "fasal bima": "crop_insurance", "ਫਸਲ ਬੀਮਾ": "crop_insurance", "फसल बीमा": "crop_insurance", "hailstorm": "crop_insurance",
    "verka": "dairy_coop", "vita": "dairy_coop", "milk": "dairy_coop", "dairy": "dairy_coop", "fisheries": "dairy_coop", "ਦੁੱਧ": "dairy_coop",
    "ots": "subsidy_waiver", "waiver": "subsidy_waiver", "settlement": "subsidy_waiver", "ਮੁਆਫੀ": "subsidy_waiver", "छूट": "subsidy_waiver",
    "election": "election_governance", "tenure": "election_governance", "managing committee": "election_governance", "ਚੋਣਾਂ": "election_governance", "चुनाव": "election_governance",
    "dispute": "grievance_dispute", "arbitration": "grievance_dispute", "ombudsman": "grievance_dispute", "ਵਿਵਾਦ": "grievance_dispute", "ਝਗੜਾ": "grievance_dispute",
    "transfer": "administrative_notice", "posting": "administrative_notice", "circular": "administrative_notice", "ਤਬਾਦਲੇ": "administrative_notice", "स्थानांतरण": "administrative_notice",
    "registration": "coop_registration_form", "incorporation": "coop_registration_form", "ਫਾਰਮ-ਏ": "coop_registration_form", "ਰਜਿਸਟਰ": "coop_registration_form",
    "erp": "gov_schemes_tech", "cloud": "gov_schemes_tech", "computerization": "gov_schemes_tech", "ਕੰਪਿਊਟਰੀਕਰਨ": "gov_schemes_tech", "pm kisan": "gov_schemes_tech"
}

class CrossLingualExpander(BaseEstimator, TransformerMixin):
    """Augments raw query text with canonical cross-lingual semantic anchors."""
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        out = []
        for text in X:
            t_lower = text.lower()
            tokens = [t_lower]
            for term, canonical in INTENT_CROSS_LINGUAL_MAP.items():
                if term in t_lower:
                    tokens.append(canonical)
            out.append(" ".join(tokens))
        return out

class NewsExpander(BaseEstimator, TransformerMixin):
    """Enriches statutory news text with canonical sector indicators."""
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        out = []
        for text in X:
            t_lower = text.lower()
            tokens = [t_lower]
            for term, canonical in NEWS_CROSS_LINGUAL_MAP.items():
                if term in t_lower:
                    tokens.append(canonical)
            out.append(" ".join(tokens))
        return out
