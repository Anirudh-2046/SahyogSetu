"""
Legal Reranker for SahyogSetu
Applies domain-specific legal reranking to fused retrieval results:
- Exact Section / Rule number alignment (+0.35)
- Distinctive intent statutory keyword alignment (+0.25)
- Query token overlap in provision text (+0.20)
- Target state priority over generic central statutes (+0.15)
Preserves original retrieval scores (semantic, keyword, RRF) alongside final rerank scores.
"""

from typing import List, Dict, Any, Optional
import re

DISTINCTIVE_INTENT_TERMS = {
    "cooperative_registration": ["registration", "register", "forming", "formation", "members required", "minimum members", "ten persons", "10 persons", "adult", "ਪੰਜੀਕਰਨ", "ਰਜਿਸਟਰ", "पंजीकरण", "गठन"],
    "elections_governance": ["election", "managing committee", "tenure", "5-year", "5 year", "five years", "term of office", "term", "reservation", "women", "ਚੋਣ", "चुनाव", "कमेटी", "कार्यकाल"],
    "dispute_arbitration": ["dispute", "arbitration", "arbitrator", "reference", "conciliation", "tribunal", "ਝਗੜਾ", "ਵਿਵਾਦ", "विवाद", "आर्बिट्रेशन"],
    "audit_inspection": ["audit", "accounts", "inspection", "chartered accountant", "financial year", "ਆਡਿਟ", "ऑडिट"],
    "financial_assistance_kcc": ["kcc", "kisan credit", "crop loan", "subvention", "collateral", "1.60 lakh", "4%"],
    "pmfby_crop_insurance": ["pmfby", "crop insurance", "calamities", "calamity", "72 hours", "damage", "inundation", "localized", "intimation", "premium"],
    "pm_kisan": ["pm-kisan", "pm kisan", "samman", "6000", "2000", "dbt", "e-kyc", "installment"],
    "ots_waiver": ["ots", "one-time settlement", "penal interest", "waiver", "defaulter", "lump sum", "ਛੋਟ", "छूट"],
    "pacs_reforms": ["pacs", "computerisation", "computerization", "model bye-law", "csc", "diversify"],
}

STOP_WORDS = {"what", "are", "the", "for", "in", "of", "and", "a", "an", "is", "to", "how", "many", "under", "which"}

class LegalReranker:
    """Scores and re-orders candidate legal chunks for optimal LLM context grounding."""

    @classmethod
    def rerank(
        cls,
        candidates: List[Dict[str, Any]],
        query: str,
        target_jurisdiction: str,
        extracted_sections: Optional[List[str]] = None,
        detected_intent: Optional[str] = None,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Reranks retrieved candidate chunks and attaches transparent scoring telemetry.
        """
        if not candidates:
            return []

        q_lower = query.lower()
        query_words = [w for w in re.findall(r"\w+", q_lower) if w not in STOP_WORDS and len(w) > 2]
        reranked = []

        for item in candidates:
            score = item.get("rrf_score", 0.0)
            chunk_sec = str(item.get("section") or "").strip().lower()
            chunk_jur = str(item.get("jurisdiction") or "").strip().lower()
            chunk_text = (item.get("chunk_text") or "").lower()
            chunk_title = (item.get("document_title") or "").lower()

            boosts = {}

            # 1. Exact Section Number Match Boost
            if extracted_sections:
                for es in extracted_sections:
                    es_l = es.lower()
                    if chunk_sec and chunk_sec == es_l:
                        boosts["section_match"] = 0.40
                        score += 0.40
                        break
                    elif f"section {es_l}" in chunk_text[:250] or f"rule {es_l}" in chunk_text[:250] or f"ਧਾਰਾ {es_l}" in chunk_text[:250] or f"धारा {es_l}" in chunk_text[:250]:
                        boosts["section_match"] = 0.35
                        score += 0.35
                        break

            # 2. Distinctive Intent Keyword Match Boost
            if detected_intent and detected_intent in DISTINCTIVE_INTENT_TERMS:
                distinctive_terms = DISTINCTIVE_INTENT_TERMS[detected_intent]
                if any(term in chunk_text or term in chunk_title for term in distinctive_terms):
                    boosts["intent_alignment"] = 0.25
                    score += 0.25

            # 3. Query Token Overlap Boost
            if query_words:
                overlap_count = sum(1 for w in query_words if w in chunk_text)
                overlap_ratio = overlap_count / len(query_words)
                if overlap_ratio > 0:
                    boost_val = round(overlap_ratio * 0.20, 4)
                    boosts["query_token_overlap"] = boost_val
                    score += boost_val

            # 4. Target Jurisdiction Alignment Boost
            if target_jurisdiction != "central" and chunk_jur == target_jurisdiction:
                boosts["target_jurisdiction_priority"] = 0.15
                score += 0.15
            elif target_jurisdiction == "central" and chunk_jur == "central":
                boosts["target_jurisdiction_priority"] = 0.10
                score += 0.10

            record = dict(item)
            record["rerank_score"] = round(score, 5)
            record["rerank_boosts"] = boosts
            reranked.append(record)

        reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
        return reranked[:top_k]

legal_reranker = LegalReranker()
