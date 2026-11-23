"""
Intelligent Query Router for SahyogSetu
Classifies incoming citizen requests into appropriate functional domains:
1. COOPERATIVE_LAW: Statutory legal questions referencing acts, sections, rules, byelaws.
2. COOPERATIVE_SCHEME: Agricultural and cooperative welfare schemes (PM-KISAN, KCC, PMFBY, PADB OTS, PACS).
3. COOPERATIVE_GOVERNANCE: Internal governance (registration, elections, tenure, audit, membership).
4. GOVERNMENT_SERVICE: Citizen administrative public services (Aadhaar, PAN, Voter ID, Passport, DL, Ration Card).
5. DOCUMENT_REQUIREMENTS: Inquiries specifically regarding acceptable supporting documents and KYC.
6. GENERAL_PUBLIC_INFORMATION: General government portals, citizen service centers, helplines.
7. LEGAL_DISPUTE: Arbitration, registrar reference, court bars, dispute adjudication.
8. JURISDICTION_AMBIGUOUS: Multi-jurisdiction questions lacking state or central specification.
9. OUT_OF_SCOPE: Queries unrelated to Indian governance, public administration, or cooperatives (e.g. NASA Mars, movies).
10. UNSUPPORTED_OR_UNCLEAR: Garbled or ambiguous inputs.

Preserves core legal RAG for cooperative governance while routing public administrative questions
to authoritative official external sources.
"""

import re
from typing import Dict, Any, Tuple, Optional
import logging

logger = logging.getLogger("sahyogsetu.rag.router")

# Category Taxonomies
OUT_OF_SCOPE_KEYWORDS = [
    "nasa", "mars", "space", "astronomy", "galaxy", "planet", "telescope", "spacex",
    "hollywood", "bollywood", "movie", "cinema", "cricket match", "football", "gaming",
    "python code", "javascript", "c++", "write a poem", "write a story", "recipe", "cooking",
    "मंगल मिशन", "अंतरिक्ष", "ग्रह", "सिनेमा", "फिल्म"
]

GOV_SERVICE_KEYWORDS = [
    "aadhaar", "aadhar", "uidai", "myaadhaar", "आधार", "ਆਧਾਰ",
    "pan card", "pan number", "nsdl", "utiitsl", "पैन कार्ड", "ਪੈਨ ਕਾਰਡ",
    "voter id", "epic", "voter card", "nvsp", "election commission", "मतदाता", "ਵੋਟਰ",
    "passport", "passport seva", "psk", "पासपोर्ट", "ਪਾਸਪੋਰਟ",
    "driving license", "driving licence", "parivahan", "sarathi", "ड्राइविंग लाइसेंस", "ਲਾਇਸੈਂਸ",
    "ration card", "nfsa", "onorc", "राशन कार्ड", "ਰਾਸ਼ਨ ਕਾਰਡ",
    "jeevan pramaan", "life certificate", "pensioner certificate", "जीवन प्रमाण",
    "caste certificate", "income certificate", "domicile certificate", "निवास प्रमाण", "जाति प्रमाण",
]

DOC_REQUIREMENTS_KEYWORDS = [
    "what documents", "which documents", "documents i need", "documents required",
    "proof of address", "proof of identity", "poa", "poi", "supporting documents",
    "कौन से दस्तावेज", "क्या दस्तावेज", "दस्तावेज़", "ਕਿਹੜੇ ਦਸਤਾਵੇਜ਼", "ਕਾਗਜ਼ਾਤ", "ਪਛਾਣ ਪੱਤਰ",
    "form-a", "फ़ॉर्म-ए", "ਫ਼ਾਰਮ-ਏ",
]

COOP_SCHEME_KEYWORDS = [
    "pm-kisan", "pm kisan", "kisan samman", "ਕਿਸਾਨ ਸਨਮਾਨ", "किसान सम्मान", "2000", "6000", "kisan nidhi",
    "kcc", "kisan credit", "crop loan", "interest subvention", "miss", "4%", "ਕ੍ਰੈਡਿਟ ਕਾਰਡ", "क्रेडिट कार्ड", "फसली ऋण",
    "pmfby", "fasal bima", "crop insurance", "ਫਸਲ ਬੀਮਾ", "फसल बीमा", "inundation", "72 hour", "72 ਘੰਟੇ", "72 घंटे",
    "ots", "one time settlement", "padb", "penal interest waiver", "ਮੁਆਫੀ", "ਛੋਟ",
    "pacs", "computerization", "model bye-law", "बाइ-लॉ", "कम्प्यूटरीकरण",
]

COOP_LAW_KEYWORDS = [
    "section", "rule", "act", "clause", "sub-section", "amendment", "statute", "bye-law", "byelaw",
    "धारा", "अधिनियम", "नियम", "उप-नियम", "ਧਾਰਾ", "ਐਕਟ", "ਉਪ-ਨਿਯਮ",
    "mscs", "multi-state", "1961", "1984", "1989", "2002", "2023",
]

COOP_GOVERNANCE_KEYWORDS = [
    "register", "registration", "forming", "formation", "start society", "गठन", "ਫਾਰਮ-ਏ",
    "managing committee", "board of directors", "tenure", "5 year", "5 years", "election",
    "quorum", "agm", "annual general meeting", "audit", "accounts", "inspection",
    "membership", "voting rights", "expulsion", "reservation",
    "प्रबंध समिति", "कार्यकाल", "चुनाव", "ऑडिट", "सदस्यता", "पंजीकरण",
    "ਪ੍ਰਬੰਧਕ ਕਮੇਟੀ", "ਕਾਰਜਕਾਲ", "ਚੋਣਾਂ", "ਆਡਿਟ", "ਮੈਂਬਰਸ਼ਿਪ", "ਰਜਿਸਟਰ",
]

LEGAL_DISPUTE_KEYWORDS = [
    "dispute", "arbitration", "arbitrator", "reference of disputes", "registrar appeal",
    "civil court bar", "tribunal", "section 55", "section 102", "section 70", "section 84",
    "विवाद", "मध्यस्थता", "सुलह", "अपील", "ਝਗੜਾ", "ਸਾਲਸੀ", "ਨਿਪਟਾਰਾ",
]

class QueryRouter:
    """Intelligently routes queries to appropriate execution pipelines."""

    def route_query(
        self,
        query: str,
        user_jurisdiction: str = "all",
    ) -> Dict[str, Any]:
        """
        Analyzes the query and returns taxonomy category, confidence, and target execution handler.
        """
        q_clean = query.strip()
        q_lower = q_clean.lower()

        # 1. Check for Out-of-Scope (e.g. NASA Mars, movies, programming)
        for oos in OUT_OF_SCOPE_KEYWORDS:
            if re.search(rf"\b{re.escape(oos)}\b", q_lower):
                return {
                    "category": "OUT_OF_SCOPE",
                    "confidence": 0.95,
                    "target_handler": "out_of_scope_handler",
                    "reasoning": f"Query contains out-of-scope domain topic: '{oos}'",
                }

        # 2. Check for Government Administrative Services (Aadhaar, PAN, Voter, Passport, DL, Ration Card)
        matched_gov_services = [k for k in GOV_SERVICE_KEYWORDS if k in q_lower]
        is_doc_req = any(dr in q_lower for dr in DOC_REQUIREMENTS_KEYWORDS)

        if matched_gov_services:
            category = "DOCUMENT_REQUIREMENTS" if is_doc_req else "GOVERNMENT_SERVICE"
            return {
                "category": category,
                "confidence": 0.92,
                "target_handler": "official_service_retriever",
                "matched_service": matched_gov_services[0],
                "is_document_requirement": is_doc_req,
                "reasoning": f"Query matches public administrative service: '{matched_gov_services[0]}'",
            }

        # 3. Check for Cooperative Legal Disputes & Arbitration
        if any(w in q_lower for w in LEGAL_DISPUTE_KEYWORDS):
            return {
                "category": "LEGAL_DISPUTE",
                "confidence": 0.90,
                "target_handler": "cooperative_rag",
                "reasoning": "Query concerns cooperative dispute adjudication or statutory arbitration",
            }

        # 4. Check for Cooperative Welfare Schemes (PM-KISAN, KCC, PMFBY, OTS, PACS)
        matched_schemes = [k for k in COOP_SCHEME_KEYWORDS if k in q_lower]
        if matched_schemes:
            category = "DOCUMENT_REQUIREMENTS" if is_doc_req else "COOPERATIVE_SCHEME"
            return {
                "category": category,
                "confidence": 0.92,
                "target_handler": "cooperative_rag",
                "matched_scheme": matched_schemes[0],
                "reasoning": f"Query matches statutory cooperative scheme: '{matched_schemes[0]}'",
            }

        # 5. Check for Cooperative Law (Acts, Sections, Rules)
        has_sec = bool(re.search(r"\b(?:section|rule|sec|धारा|ਧਾਰਾ)\s*\d+", q_lower))
        if has_sec or any(w in q_lower for w in COOP_LAW_KEYWORDS):
            return {
                "category": "COOPERATIVE_LAW",
                "confidence": 0.90,
                "target_handler": "cooperative_rag",
                "reasoning": "Query inquires about specific statutory act or legal section",
            }

        # 6. Check for Cooperative Governance (Elections, Committee, Registration, Audit)
        if any(w in q_lower for w in COOP_GOVERNANCE_KEYWORDS):
            # Check if jurisdiction is ambiguous (e.g. "how to register a society" without state)
            if user_jurisdiction == "all" and any(w in q_lower for w in ["register", "registration", "पंजीकरण", "ਰਜਿਸਟਰ"]):
                if not any(j in q_lower for j in ["punjab", "haryana", "jk", "jammu", "kashmir", "central", "multi-state"]):
                    return {
                        "category": "JURISDICTION_AMBIGUOUS",
                        "confidence": 0.88,
                        "target_handler": "jurisdiction_clarifier",
                        "reasoning": "Cooperative registration requires state or central jurisdiction clarification",
                    }
            return {
                "category": "COOPERATIVE_GOVERNANCE",
                "confidence": 0.88,
                "target_handler": "cooperative_rag",
                "reasoning": "Query concerns internal cooperative management or governance rules",
            }

        # 7. Check if it's general document requirements without explicit entity
        if is_doc_req:
            return {
                "category": "DOCUMENT_REQUIREMENTS",
                "confidence": 0.80,
                "target_handler": "official_service_retriever",
                "reasoning": "Query concerns document requirements for public citizen processes",
            }

        # 8. Check if it is a general public administrative question
        if any(w in q_lower for w in ["portal", "csc", "common service", "helpline", "शिकायत", "सेवा केंद्र"]):
            return {
                "category": "GENERAL_PUBLIC_INFORMATION",
                "confidence": 0.75,
                "target_handler": "official_service_retriever",
                "reasoning": "Query inquires about general public information or portals",
            }

        # 9. Default to Cooperative RAG with lower confidence
        return {
            "category": "COOPERATIVE_GOVERNANCE",
            "confidence": 0.60,
            "target_handler": "cooperative_rag",
            "reasoning": "Default route to cooperative legal RAG engine",
        }

query_router = QueryRouter()
