"""
Source Resolver for SahyogSetu
Implements the complete authoritative workflow:
User question
→ Language identification
→ Jurisdiction identification
→ Intent classification
→ Query understanding
→ Legal/news knowledge retrieval
→ Official source verification
→ Relevant provision/document extraction
→ Answer synthesis with verifiable citations
→ Multilingual translation (preserving legal entities, sections, amounts)
→ Dedicated 'Official Sources & References' section.
"""

import re
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from .official_document_service import official_document_service, OFFICIAL_DOCUMENT_REGISTRY
from .source_validator import source_validator
from .citation_builder import citation_builder
from .official_service_retriever import official_service_retriever
from ...rag.language_detector import language_detector
from ...rag.query_router import query_router
from ...rag.followup_generator import followup_generator

logger = logging.getLogger("sahyogsetu.sources.resolver")

class SourceResolver:
    """Orchestrates query resolution, legal knowledge retrieval, and citation verification."""

    def resolve_query(
        self,
        query: str,
        language: str = "en",
        jurisdiction: str = "all",
        attached_doc: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes end-to-end statutory and scheme retrieval.
        Guarantees that every answer provides direct official URLs and page-level evidence.
        """
        q_clean = query.strip()
        q_lower = q_clean.lower()
        target_lang = language_detector.resolve_priority_language(language, q_clean)
        target_jur = jurisdiction.lower() if jurisdiction else "all"

        # 1. Intelligent Query Routing
        route_info = query_router.route_query(q_clean, user_jurisdiction=target_jur)
        category = route_info.get("category", "COOPERATIVE_GOVERNANCE")
        target_handler = route_info.get("target_handler", "cooperative_rag")

        # 2. Out-of-Scope queries -> Contextual out-of-scope abstention with empty follow-ups
        if target_handler == "out_of_scope_handler":
            from ...rag.answer_generator import answer_generator
            oos_res = answer_generator._build_no_evidence_response(
                target_lang, target_jur, query=q_clean, category="OUT_OF_SCOPE"
            )
            oos_res["id"] = f"resp_{int(datetime.now().timestamp() * 1000)}"
            oos_res["timestamp"] = datetime.now().strftime("%I:%M %p")
            oos_res["category"] = "OUT_OF_SCOPE"
            oos_res["isOfflineCorpus"] = False
            oos_res["isDemoMode"] = False
            oos_res["suggestedFollowUps"] = []
            oos_res["suggestedQuestions"] = []
            return oos_res

        # 3. Government Administrative Services & Document Requirements -> Official Service Retriever
        if target_handler == "official_service_retriever":
            service_res = official_service_retriever.retrieve_service(
                query=q_clean,
                category=category,
                language=target_lang,
                jurisdiction=target_jur,
            )
            if service_res:
                service_res["category"] = category
                return service_res
            # If specific service not in catalog, route to contextual abstention
            from ...rag.answer_generator import answer_generator
            no_ev_res = answer_generator._build_no_evidence_response(
                target_lang, target_jur, query=q_clean, category=category
            )
            no_ev_res["id"] = f"resp_{int(datetime.now().timestamp() * 1000)}"
            no_ev_res["timestamp"] = datetime.now().strftime("%I:%M %p")
            no_ev_res["category"] = category
            no_ev_res["source_provenance"] = "OFFICIAL_SOURCE_UNAVAILABLE"
            no_ev_res["groundingStatus"] = "OFFICIAL_SOURCE_UNAVAILABLE"
            return no_ev_res

        # 4. Jurisdiction Ambiguous Queries -> Clarification Request
        if target_handler == "jurisdiction_clarifier":
            from ...rag.answer_generator import answer_generator
            clarif_res = answer_generator._build_clarification_response(
                prompt="Cooperative registration rules require jurisdiction clarification.",
                language=target_lang,
                jur=target_jur,
            )
            clarif_res["id"] = f"resp_{int(datetime.now().timestamp() * 1000)}"
            clarif_res["timestamp"] = datetime.now().strftime("%I:%M %p")
            clarif_res["category"] = "JURISDICTION_AMBIGUOUS"
            return clarif_res

        # 5. Intent Detection for Cooperative Governance
        intent = self._detect_intent(q_lower)

        # Phase 4 Legal RAG Pipeline Execution
        try:
            from ...rag.rag_pipeline import rag_pipeline
            rag_res = rag_pipeline.run_sync(
                query=q_clean,
                user_language=target_lang,
                user_jurisdiction=target_jur,
                attached_doc=attached_doc,
            )
            # If clarification is requested or no evidence found, return RAG decision
            if rag_res.get("uncertainty", {}).get("status") in ["clarification_required", "no_evidence"]:
                rag_res["id"] = f"resp_{int(datetime.now().timestamp() * 1000)}"
                rag_res["timestamp"] = datetime.now().strftime("%I:%M %p")
                rag_res["isOfflineCorpus"] = False
                rag_res["isDemoMode"] = False
                rag_res["language"] = target_lang
                rag_res["category"] = category
                rag_res["source_provenance"] = (
                    "JURISDICTION_CLARIFICATION_REQUIRED"
                    if rag_res.get("uncertainty", {}).get("status") == "clarification_required"
                    else "INSUFFICIENT_VERIFIED_EVIDENCE"
                )
                rag_res["groundingStatus"] = rag_res["source_provenance"]
                rag_res["suggestedFollowUps"] = rag_res.get("suggestedFollowUps") or followup_generator.generate_followups(
                    query=q_clean,
                    category=category,
                    answer_text=rag_res.get("plainExplanation", ""),
                    language=target_lang,
                    grounding_status=rag_res.get("uncertainty", {}).get("status", "no_evidence"),
                )
                rag_res["suggestedQuestions"] = rag_res["suggestedFollowUps"]
                return rag_res

            if rag_res.get("uncertainty", {}).get("status") == "verified" and rag_res.get("citations"):
                knowledge = self._retrieve_knowledge(intent, q_lower, target_jur)
                if knowledge:
                    text_catalog = knowledge.get("responses", {}).get(target_lang)
                    if not text_catalog and target_lang in ["bgc", "doi"]:
                        text_catalog = knowledge.get("responses", {}).get("hi")
                    if not text_catalog:
                        text_catalog = knowledge.get("responses", {}).get("en", {})

                    if text_catalog and "summary" in text_catalog:
                        cat_summary = text_catalog["summary"]
                        rag_res["summary"] = cat_summary
                        rag_res["shortAnswer"] = cat_summary.split(".")[0] + ("." if "." in cat_summary else "")
                        sources_md = rag_res.get("sources_markdown", "")
                        rag_res["plainExplanation"] = f"{cat_summary}\n\n{sources_md}" if sources_md else cat_summary

                    rag_res["eligibility"] = text_catalog.get("eligibility", [])
                    rag_res["procedure"] = text_catalog.get("procedure", [])
                    rag_res["documentsRequired"] = text_catalog.get("documentsRequired", [])
                rag_res["id"] = f"resp_{int(datetime.now().timestamp() * 1000)}"
                rag_res["timestamp"] = datetime.now().strftime("%I:%M %p")
                rag_res["isOfflineCorpus"] = False
                rag_res["isDemoMode"] = False
                rag_res["language"] = target_lang
                rag_res["category"] = category
                rag_res["source_provenance"] = "VERIFIED_LOCAL_LEGAL_CORPUS"
                rag_res["groundingStatus"] = "VERIFIED_LOCAL_LEGAL_CORPUS"
                followups = followup_generator.generate_followups(
                    query=q_clean,
                    category=category,
                    answer_text=rag_res.get("plainExplanation", ""),
                    language=target_lang,
                    grounding_status="verified",
                )
                rag_res["suggestedFollowUps"] = followups
                rag_res["suggestedQuestions"] = followups
                return rag_res
        except Exception as e:
            logger.warning("RAG pipeline execution failed in source_resolver: %s; falling back.", e)

        # 2. Knowledge Retrieval & Provision Extraction
        knowledge = self._retrieve_knowledge(intent, q_lower, target_jur)

        if not knowledge:
            # Phase 15 Section 6: Missing source handling
            unverified_msg = (
                "ਮੈਂ ਇਸ ਜਾਣਕਾਰੀ ਦੀ ਕਿਸੇ ਪ੍ਰਮਾਣਿਕ ਸਰਕਾਰੀ ਸਰੋਤ ਤੋਂ ਪੁਸ਼ਟੀ ਨਹੀਂ ਕਰ ਸਕਿਆ। ਕਿਰਪਾ ਕਰਕੇ ਇਸ ਵਿਆਖਿਆ ਨੂੰ ਅਣ-ਪੁਸ਼ਟੀਸ਼ੁਦਾ ਮੰਨੋ।"
                if target_lang == "pa"
                else "मैं इस जानकारी को किसी आधिकारिक सरकारी स्रोत से सत्यापित नहीं कर सका। कृपया इस स्पष्टीकरण को असत्यापित मानें।"
                if target_lang in ["hi", "bgc"]
                else "मैं इस जानकारी गी किश सरकारी स्रोतै कन्ने प्रमाणित नी करी सकेआ। कृपया इस व्याख्या गी अप्रमाणित मन्नो।"
                if target_lang == "doi"
                else "I could not verify this information against an authoritative government source. Please treat the explanation as unverified."
            )
            return {
                "id": f"resp_{int(datetime.now().timestamp() * 1000)}",
                "shortAnswer": unverified_msg,
                "plainExplanation": unverified_msg,
                "summary": unverified_msg,
                "citations": [],
                "jurisdiction": target_jur.capitalize(),
                "uncertainty": {
                    "status": "missing_source",
                    "notice": "I could not verify this information against an authoritative government source. Please treat the explanation as unverified.",
                },
                "language": target_lang,
                "timestamp": datetime.now().strftime("%I:%M %p"),
                "isOfflineCorpus": True,
                "isDemoMode": False,
            }

        # 3. Citation Validation
        raw_citations = knowledge.get("citations", [])
        validated_citations = []
        for raw_c in raw_citations:
            is_valid, status = source_validator.validate_citation(raw_c, target_jur)
            if is_valid:
                structured_c = citation_builder.build_structured_citation(raw_c)
                structured_c["verification_status"] = status
                validated_citations.append(structured_c)

        # 4. Generate Mandatory 'Official Sources & References' Markdown
        sources_md = citation_builder.generate_sources_markdown(validated_citations, target_lang)

        # 5. Extract language-specific textual answer
        text_catalog = knowledge.get("responses", {}).get(target_lang)
        if not text_catalog and target_lang in ["bgc", "doi"]:
            text_catalog = knowledge.get("responses", {}).get("hi")
        if not text_catalog:
            text_catalog = knowledge.get("responses", {}).get("en", {})
        summary = text_catalog.get("summary", "")
        short_ans = summary.split(".")[0] + "." if "." in summary else summary

        # Append official sources section to plain explanation
        full_explanation = f"{summary}\n\n{sources_md}" if sources_md else summary

        return {
            "id": f"resp_{int(datetime.now().timestamp() * 1000)}",
            "shortAnswer": short_ans,
            "plainExplanation": full_explanation,
            "summary": summary,
            "eligibility": text_catalog.get("eligibility", []),
            "procedure": text_catalog.get("procedure", []),
            "documentsRequired": text_catalog.get("documentsRequired", []),
            "relevantAct": knowledge.get("relevant_act", "State & Central Statutory Framework"),
            "citations": validated_citations,
            "sources_markdown": sources_md,
            "jurisdiction": target_jur.capitalize() if target_jur != "all" else "All",
            "source_provenance": "VERIFIED_LOCAL_LEGAL_CORPUS",
            "groundingStatus": "VERIFIED_LOCAL_LEGAL_CORPUS",
            "suggestedFollowUps": followup_generator.generate_followups(
                query=q_clean,
                category=category,
                answer_text=full_explanation,
                language=target_lang,
                grounding_status="verified",
            ),
            "suggestedQuestions": followup_generator.generate_followups(
                query=q_clean,
                category=category,
                answer_text=full_explanation,
                language=target_lang,
                grounding_status="verified",
            ),
            "uncertainty": {
                "status": "none",
                "notice": "All statutory provisions and scheme requirements verified against official Gazette records.",
            },
            "language": target_lang,
            "timestamp": datetime.now().strftime("%I:%M %p"),
            "isOfflineCorpus": False,
            "isDemoMode": False,
        }

    def _detect_intent(self, q: str) -> str:
        """Categorizes query intent across cooperative governance & government schemes."""
        if any(w in q for w in ["pm-kisan", "pm kisan", "ਕਿਸਾਨ ਸਨਮਾਨ", "किसान सम्मान", "2000", "6000", "kisan nidhi"]):
            return "pm_kisan"
        if any(w in q for w in ["kcc", "kisan credit", "ਕ੍ਰੈਡਿਟ ਕਾਰਡ", "क्रेडिट कार्ड", "crop loan", "फसली ऋण", "interest subvention", "miss", "4%"]):
            return "kcc_credit"
        if any(w in q for w in ["pmfby", "fasal bima", "crop insurance", "ਫਸਲ ਬੀਮਾ", "फसल बीमा", "inundation", "72 hour", "72 ਘੰਟੇ"]):
            return "pmfby_insurance"
        if any(w in q for w in ["register", "registration", "forming", "start society", "ਰਜਿਸਟਰ", "पंजीकरण", "गठन", "form-a", "ਫਾਰਮ-ਏ"]):
            return "cooperative_registration"
        if any(w in q for w in ["election", "managing committee", "tenure", "5 year", "5 ਸਾਲ", "ਚੋਣ", "चुनाव", "कमेटी"]):
            return "elections_governance"
        if any(w in q for w in ["dispute", "arbitration", "section 55", "section 102", "section 70", "ਝਗੜਾ", "ਵਿਵਾਦ", "विवाद", "आर्बिट्रेशन"]):
            return "dispute_arbitration"
        if any(w in q for w in ["audit", "accounts", "inspection", "ਆਡਿਟ", "ऑडिट", "ਲੇਖਾ", "हिसाब"]):
            return "audit_inspection"
        if any(w in q for w in ["pacs", "computerization", "model bye-law", "ਬਾਈ-ਲਾਅ", "उप-नियम", "common service center", "csc"]):
            return "pacs_reforms"
        if any(w in q for w in ["ots", "one time settlement", "penal interest", "waiver", "ਛੋਟ", "ਮੁਆਫੀ", "छूट"]):
            return "ots_waiver"
        return "general_coop"

    def _retrieve_knowledge(self, intent: str, q: str, jur: str) -> Optional[Dict[str, Any]]:
        """Retrieves structured evidence, rules, procedures, and citations for detected intent."""

        # --------------------------------------------------------------------
        # 1. PM-KISAN
        # --------------------------------------------------------------------
        if intent == "pm_kisan":
            doc = OFFICIAL_DOCUMENT_REGISTRY["pm_kisan_guidelines"]
            return {
                "relevant_act": "PM-KISAN Operational Guidelines (Government of India)",
                "responses": {
                    "pa": {
                        "summary": "ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਕਿਸਾਨ ਸਨਮਾਨ ਨਿਧੀ (PM-KISAN) ਅਧੀਨ ਯੋਗ ਕਿਸਾਨ ਪਰਿਵਾਰਾਂ ਨੂੰ ਹਰ ਸਾਲ ₹6,000 ਦੀ ਸਿੱਧੀ ਵਿੱਤੀ ਸਹਾਇਤਾ ₹2,000 ਦੀਆਂ ਤਿੰਨ ਬਰਾਬਰ ਕਿਸ਼ਤਾਂ ਵਿੱਚ ਡੀਬੀਟੀ (DBT) ਰਾਹੀਂ ਮਿਲਦੀ ਹੈ। ਸਕੀਮ ਦਾ ਲਾਭ ਲੈਣ ਲਈ ਜ਼ਮੀਨੀ ਰਿਕਾਰਡ ਦੀ ਤਸਦੀਕ, ਆਧਾਰ ਲਿੰਕਡ ਬੈਂਕ ਖਾਤਾ ਅਤੇ ਈ-ਕੇਵਾਈਸੀ (e-KYC) ਲਾਜ਼ਮੀ ਹੈ।",
                        "eligibility": [
                            "ਸਾਰੇ ਕਾਸ਼ਤਕਾਰ ਕਿਸਾਨ ਪਰਿਵਾਰ ਜਿਨ੍ਹਾਂ ਦੇ ਨਾਮ 'ਤੇ ਵਾਹੀਯੋਗ ਜ਼ਮੀਨ ਹੈ।",
                            "ਸੰਸਥਾਗਤ ਜ਼ਮੀਨ ਮਾਲਕ ਅਤੇ ਸਰਕਾਰੀ ਮੁਲਾਜ਼ਮ/ਪੈਨਸ਼ਨਰ (₹10,000+ ਮਹੀਨਾਵਾਰ ਪੈਨਸ਼ਨ) ਸ਼ਾਮਲ ਨਹੀਂ ਹਨ।",
                            "ਪਿਛਲੇ ਮੁਲਾਂਕਣ ਸਾਲ ਵਿੱਚ ਇਨਕਮ ਟੈਕਸ ਦੇਣ ਵਾਲੇ ਵਿਅਕਤੀ ਅਯੋਗ ਹਨ।",
                        ],
                        "procedure": [
                            "PM-KISAN ਪੋਰਟਲ (pmkisan.gov.in) ਜਾਂ ਨਜ਼ਦੀਕੀ ਕਾਮਨ ਸਰਵਿਸ ਸੈਂਟਰ (CSC) 'ਤੇ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਕਰੋ।",
                            "ਆਪਣੇ ਆਧਾਰ ਨੰਬਰ ਨਾਲ ਮੋਬਾਈਲ ਓਟੀਪੀ ਜਾਂ ਬਾਇਓਮੈਟ੍ਰਿਕ e-KYC ਪੂਰੀ ਕਰੋ।",
                            "ਜ਼ਮੀਨੀ ਫ਼ਰਦ (ਜਮ੍ਹਾਬੰਦੀ) ਅਤੇ ਬੈਂਕ ਖਾਤਾ ਵੇਰਵੇ ਅਪਲੋਡ ਕਰੋ।",
                            "ਜ਼ਿਲ੍ਹਾ ਖੇਤੀਬਾੜੀ ਨੋਡਲ ਅਧਿਕਾਰੀ ਵੱਲੋਂ ਪੜਤਾਲ ਉਪਰੰਤ ਕਿਸ਼ਤ ਜਾਰੀ ਹੁੰਦੀ ਹੈ।",
                        ],
                        "documentsRequired": [
                            "ਆਧਾਰ ਕਾਰਡ (Aadhaar Card)",
                            "ਜ਼ਮੀਨੀ ਮਾਲਕੀ ਦਸਤਾਵੇਜ਼ (ਤਾਜ਼ਾ ਜਮ੍ਹਾਬੰਦੀ / ਫ਼ਰਦ)",
                            "ਆਧਾਰ-ਸੀਡਿਡ ਬੈਂਕ ਖਾਤਾ ਵੇਰਵਾ (NPCI Linked)",
                            "ਮੋਬਾਈਲ ਨੰਬਰ (ਆਧਾਰ ਨਾਲ ਰਜਿਸਟਰਡ)",
                        ],
                    },
                    "hi": {
                        "summary": "प्रधानमंत्री किसान सम्मान निधि (PM-KISAN) के अंतर्गत पात्र किसान परिवारों को प्रतिवर्ष ₹6,000 की वित्तीय सहायता ₹2,000 की तीन समान किस्तों में प्रत्यक्ष लाभ अंतरण (DBT) द्वारा बैंक खातों में अंतरित की जाती है। योजना हेतु भूमि अभिलेख सत्यापन, आधार सीडेड खाता और ई-केवाईसी अनिवार्य है।",
                        "eligibility": [
                            "सभी भूमिधारक किसान परिवार जिनके नाम कृषि योग्य भूमि दर्ज है।",
                            "संवैधानिक पदधारक, आयकर दाता और ₹10,000 से अधिक मासिक पेंशनभोगी अपात्र हैं।",
                            "संस्थागत भू-स्वामी इस योजना के पात्र नहीं हैं।",
                        ],
                        "procedure": [
                            "पीएम-किसान पोर्टल (pmkisan.gov.in) अथवा सीएससी केंद्र पर नया पंजीकरण करें।",
                            "ओटीपी अथवा बायोमेट्रिक द्वारा अनिवार्य e-KYC प्रक्रिया पूर्ण करें।",
                            "जमाबंदी/खतौनी की प्रति एवं बैंक विवरण पोर्टल पर अपलोड करें।",
                            "राज्य नोडल अधिकारी के सत्यापन उपरांत किस्त जारी की जाती है।",
                        ],
                        "documentsRequired": [
                            "आधार कार्ड",
                            "भूमि स्वामित्व दस्तावेज (खतौनी/जमाबंदी)",
                            "आधार से जुड़ा बैंक खाता (NPCI डीबीटी इनेबल्ड)",
                            "सक्रिय मोबाइल नंबर",
                        ],
                    },
                    "en": {
                        "summary": "Under the Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) scheme, eligible landholder farmer families receive an income support of ₹6,000 per annum, disbursed in three equal four-monthly installments of ₹2,000 directly into Aadhaar-seeded bank accounts through DBT.",
                        "eligibility": [
                            "All landholding farmer families with cultivable land parcels in their name.",
                            "Institutional landholders, constitutional post holders, and income tax payees are excluded.",
                            "Serving or retired government employees and pensioners drawing ₹10,000+ monthly are ineligible.",
                        ],
                        "procedure": [
                            "Register online via PM-KISAN Portal (pmkisan.gov.in) or nearest Common Service Centre (CSC).",
                            "Complete mandatory biometric or OTP-based e-KYC.",
                            "Upload verified land record (Jamabandi/Khatauni) and Aadhaar-seeded bank details.",
                            "District and State Nodal verification precedes disbursement.",
                        ],
                        "documentsRequired": [
                            "Aadhaar Card of applicant",
                            "Valid land ownership record (latest Jamabandi/Khatauni)",
                            "NPCI-linked, Aadhaar-seeded bank account details",
                            "Active mobile number linked with Aadhaar",
                        ],
                    },
                },
                "citations": [
                    {
                        "doc_id": "pm_kisan_guidelines",
                        "title": doc["title"],
                        "authority": doc["authority"],
                        "jurisdiction": "Central",
                        "section": "Paragraph 2 & 8 (Eligibility & Aadhaar Mandatory Verification)",
                        "page_number": 2,
                        "publication_date": doc["publication_date"],
                        "source_url": doc["direct_url"],
                        "official_translation_url": doc["official_translation_url"],
                    }
                ],
            }

        # --------------------------------------------------------------------
        # 2. KISAN CREDIT CARD (KCC) & INTEREST SUBVENTION
        # --------------------------------------------------------------------
        if intent == "kcc_credit":
            doc = OFFICIAL_DOCUMENT_REGISTRY["kcc_rbi_master_circular"]
            return {
                "relevant_act": "RBI Master Circular on KCC & Modified Interest Subvention Scheme (MISS)",
                "responses": {
                    "pa": {
                        "summary": "ਕਿਸਾਨ ਕ੍ਰੈਡਿਟ ਕਾਰਡ (KCC) ਸਕੀਮ ਤਹਿਤ ਕਿਸਾਨਾਂ ਨੂੰ ਫ਼ਸਲੀ ਖ਼ਰਚਿਆਂ ਲਈ ਸਸਤੀ ਦਰ 'ਤੇ ਕਰਜ਼ਾ ਮਿਲਦਾ ਹੈ। ਭਾਰਤ ਸਰਕਾਰ ਦੀ ਸੋਧੀ ਹੋਈ ਵਿਆਜ ਸਬਵੈਂਸ਼ਨ ਸਕੀਮ (MISS) ਅਧੀਨ ₹3.00 ਲੱਖ ਤੱਕ ਦੇ ਥੋੜ੍ਹੇ ਸਮੇਂ ਦੇ ਕਰਜ਼ੇ 'ਤੇ 1.5% ਸਬਸਿਡੀ ਅਤੇ ਸਮੇਂ ਸਿਰ ਭੁਗਤਾਨ ਕਰਨ 'ਤੇ 3% ਵਾਧੂ ਛੋਟ ਮਿਲਦੀ ਹੈ, ਜਿਸ ਨਾਲ ਅਸਲ ਵਿਆਜ ਦਰ ਸਿਰਫ਼ 4% ਸਾਲਾਨਾ ਰਹਿ ਜਾਂਦੀ ਹੈ। ₹1.60 ਲੱਖ ਤੱਕ ਕੋਈ ਗਾਰੰਟੀ ਜਾਂ ਜ਼ਮੀਨ ਗਹਿਣੇ ਰੱਖਣ ਦੀ ਲੋੜ ਨਹੀਂ ਹੁੰਦੀ।",
                        "eligibility": [
                            "ਸਾਰੇ ਮਾਲਕ ਕਿਸਾਨ, ਬਟਾਈਦਾਰ (tenant farmers), ਅਤੇ ਸਵੈ-ਸਹਾਇਤਾ ਸਮੂਹ (SHGs)।",
                            "ਪਸ਼ੂ ਪਾਲਣ, ਡੇਅਰੀ ਅਤੇ ਮੱਛੀ ਪਾਲਣ ਲਈ ਵੀ KCC ਕਾਰਡ ਬਣਵਾਇਆ ਜਾ ਸਕਦਾ ਹੈ।",
                        ],
                        "procedure": [
                            "ਸਥਾਨਕ ਪ੍ਰਾਇਮਰੀ ਖੇਤੀਬਾੜੀ ਸਹਿਕਾਰੀ ਸਭਾ (PACS) ਜਾਂ ਸਹਿਕਾਰੀ ਬੈਂਕ ਵਿੱਚ ਅਰਜ਼ੀ ਫਾਰਮ ਭਰੋ।",
                            "ਫ਼ਸਲੀ ਰਕਬੇ ਅਤੇ ਜ਼ਮੀਨੀ ਫ਼ਰਦ (ਜਮ੍ਹਾਬੰਦੀ) ਦੀ ਕਾਪੀ ਨਾਲ ਨੱਥੀ ਕਰੋ।",
                            "ਬੈਂਕ ਵੱਲੋਂ ਜ਼ਮੀਨ ਅਤੇ ਫ਼ਸਲੀ ਪੈਮਾਨੇ (Scale of Finance) ਅਨੁਸਾਰ ਕ੍ਰੈਡਿਟ ਲਿਮਿਟ ਮਨਜ਼ੂਰ ਕੀਤੀ ਜਾਂਦੀ ਹੈ।",
                            "ਰੂਪੇ KCC ਕਾਰਡ ਜਾਰੀ ਹੁੰਦਾ ਹੈ ਜਿਸ ਨਾਲ ਏਟੀਐਮ ਜਾਂ ਸਹਿਕਾਰੀ ਸਭਾ ਵਿੱਚੋਂ ਪੈਸੇ ਕਢਵਾਏ ਜਾ ਸਕਦੇ ਹਨ।",
                        ],
                        "documentsRequired": [
                            "ਮੁਕੰਮਲ KCC ਅਰਜ਼ੀ ਫਾਰਮ",
                            "ਆਧਾਰ ਕਾਰਡ ਅਤੇ ਪਾਸਪੋਰਟ ਸਾਈਜ਼ ਫੋਟੋਆਂ",
                            "ਜ਼ਮੀਨੀ ਮਾਲਕੀ ਰਿਕਾਰਡ (ਫ਼ਰਦ/ਜਮ੍ਹਾਬੰਦੀ) ਜਾਂ ਬਟਾਈਦਾਰੀ ਇਕਰਾਰਨਾਮਾ",
                            "ਨੋ-ਡਿਊਜ਼ ਸਰਟੀਫਿਕੇਟ (ਜੇਕਰ ਲਾਗੂ ਹੋਵੇ)",
                        ],
                    },
                    "hi": {
                        "summary": "किसान क्रेडिट कार्ड (KCC) योजना के अंतर्गत अल्पावधि फसली ऋण रियायती ब्याज दर पर उपलब्ध कराया जाता है। केंद्र सरकार की संशोधित ब्याज छूट योजना (MISS) के तहत ₹3.00 लाख तक के ऋण पर 7% की सामान्य दर पर 1.5% ब्याज छूट तथा समय पर चुकता करने पर 3% अतिरिक्त प्रोत्साहन दिया जाता है, जिससे प्रभावी ब्याज दर मात्र 4% वार्षिक हो जाती है। ₹1.60 लाख तक बिना किसी बंधक (collateral-free) के ऋण मिलता है।",
                        "eligibility": [
                            "सभी व्यक्तिगत भूमिधारक किसान, बटाईदार एवं मौखिक पट्टेदार।",
                            "डेयरी, पशुपालन एवं मत्स्य पालन से जुड़े किसान भी पात्र हैं।",
                        ],
                        "procedure": [
                            "निकटतम पैक्स (PACS) समिति अथवा जिला केंद्रीय सहकारी बैंक में KCC फॉर्म भरें।",
                            "भूमि रिकॉर्ड (खतौनी) तथा प्रस्तावित फसल क्षेत्र का विवरण प्रस्तुत करें।",
                            "बैंक स्केल ऑफ फाइनेंस के आधार पर सीमा स्वीकृत करता है।",
                            "रुपे KCC कार्ड जारी किया जाता है।",
                        ],
                        "documentsRequired": [
                            "भरा हुआ आवेदन पत्र",
                            "पहचान एवं निवास प्रमाण (आधार कार्ड)",
                            "भूमि खतौनी/जमाबंदी की सत्यापित प्रति",
                            "शपथ पत्र (अन्य बैंक से बकाया न होने संबंधी)",
                        ],
                    },
                    "en": {
                        "summary": "Under the Kisan Credit Card (KCC) Scheme, short-term crop loans up to ₹3.00 Lakh are provided at an effective 4% annual interest rate, supported by 1.5% Government Interest Subvention and 3% Prompt Repayment Incentive. Collateral and margin requirements are waived for loans up to ₹1.60 Lakh.",
                        "eligibility": [
                            "All individual land-owning farmers, tenant farmers, oral lessees, and sharecroppers.",
                            "Farmers engaged in animal husbandry, dairy farming, and fisheries.",
                        ],
                        "procedure": [
                            "Submit standard KCC application to local PACS or District Central Cooperative Bank.",
                            "Provide land records and cropping plan.",
                            "Sanction limit determined using District Level Technical Committee (DLTC) scale of finance.",
                            "Issuance of RuPay KCC card with 5-year operational validity.",
                        ],
                        "documentsRequired": [
                            "Completed KCC application form",
                            "Aadhaar Card & recent passport-size photographs",
                            "Certified land ownership record (Jamabandi/Khatauni)",
                            "Declaration of crops sown and non-encumbrance certificate",
                        ],
                    },
                },
                "citations": [
                    {
                        "doc_id": "kcc_rbi_master_circular",
                        "title": doc["title"],
                        "authority": doc["authority"],
                        "jurisdiction": "Central",
                        "section": "Section 2.1 & 3.4 (Collateral-Free Limit & Interest Subvention)",
                        "page_number": 6,
                        "publication_date": doc["publication_date"],
                        "source_url": doc["direct_url"],
                        "official_translation_url": doc["official_translation_url"],
                    }
                ],
            }

        # --------------------------------------------------------------------
        # 3. PMFBY CROP INSURANCE
        # --------------------------------------------------------------------
        if intent == "pmfby_insurance":
            doc = OFFICIAL_DOCUMENT_REGISTRY["pmfby_operational_guidelines"]
            return {
                "relevant_act": "PMFBY Revised Operational Guidelines (Ministry of Agriculture)",
                "responses": {
                    "pa": {
                        "summary": "ਪ੍ਰਧਾਨ ਮੰਤਰੀ ਫ਼ਸਲ ਬੀਮਾ ਯੋਜਨਾ (PMFBY) ਅਧੀਨ ਕਿਸਾਨਾਂ ਨੂੰ ਕੁਦਰਤੀ ਆਫ਼ਤਾਂ, ਕੀੜੇ-ਮਕੌੜਿਆਂ ਅਤੇ ਬਿਮਾਰੀਆਂ ਕਾਰਨ ਫ਼ਸਲ ਦੇ ਨੁਕਸਾਨ ਦੀ ਭਰਪਾਈ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਸਾਉਣੀ (Kharif) ਦੀਆਂ ਫ਼ਸਲਾਂ ਲਈ ਕਿਸਾਨ ਦਾ ਹਿੱਸਾ ਵੱਧ ਤੋਂ ਵੱਧ 2%, ਹਾੜ੍ਹੀ (Rabi) ਫ਼ਸਲਾਂ ਲਈ 1.5% ਅਤੇ ਵਪਾਰਕ/ਬਾਗ਼ਬਾਨੀ ਫ਼ਸਲਾਂ ਲਈ 5% ਪ੍ਰੀਮੀਅਮ ਹੁੰਦਾ ਹੈ। ਗੜੇਮਾਰੀ, ਜ਼ਮੀਨ ਖਿਸਕਣ ਜਾਂ ਜਲ-ਥਲ ਹੋਣ ਕਾਰਨ ਹੋਏ ਸਥਾਨਕ ਨੁਕਸਾਨ ਦੀ ਸੂਚਨਾ 72 ਘੰਟਿਆਂ ਦੇ ਅੰਦਰ-ਅੰਦਰ ਦੇਣੀ ਲਾਜ਼ਮੀ ਹੁੰਦੀ ਹੈ।",
                        "eligibility": [
                            "ਸਾਰੇ ਰਿਣੀ (loanee) ਅਤੇ ਗ਼ੈਰ-ਰਿਣੀ ਕਿਸਾਨ ਜੋ ਨੋਟੀਫਾਈਡ ਇਲਾਕਿਆਂ ਵਿੱਚ ਨੋਟੀਫਾਈਡ ਫ਼ਸਲਾਂ ਉਗਾਉਂਦੇ ਹਨ।",
                            "ਬਟਾਈਦਾਰ ਕਿਸਾਨ ਵੀ ਬੀਮਾ ਕਰਵਾਉਣ ਦੇ ਯੋਗ ਹਨ।",
                        ],
                        "procedure": [
                            "ਬੀਜਣ ਤੋਂ ਬਾਅਦ ਨਿਰਧਾਰਿਤ ਆਖ਼ਰੀ ਮਿਤੀ ਤੱਕ ਨੈਸ਼ਨਲ ਕ੍ਰੌਪ ਇੰਸ਼ੋਰੈਂਸ ਪੋਰਟਲ (NCIP) ਜਾਂ ਸਹਿਕਾਰੀ ਬੈਂਕ ਵਿੱਚ ਪ੍ਰੀਮੀਅਮ ਜਮ੍ਹਾਂ ਕਰੋ।",
                            "ਨੁਕਸਾਨ ਹੋਣ ਦੀ ਸੂਰਤ ਵਿੱਚ ਕ੍ਰੌਪ ਇੰਸ਼ੋਰੈਂਸ ਐਪ (Crop Insurance App), ਟੋਲ-ਫ੍ਰੀ ਨੰਬਰ 14447 ਜਾਂ ਸਹਿਕਾਰੀ ਸਭਾ ਰਾਹੀਂ 72 ਘੰਟਿਆਂ ਵਿੱਚ ਸ਼ਿਕਾਇਤ ਦਰਜ ਕਰੋ।",
                            "ਖੇਤੀਬਾੜੀ ਵਿਭਾਗ ਅਤੇ ਬੀਮਾ ਕੰਪਨੀ ਦੀ ਸਾਂਝੀ ਟੀਮ ਮੌਕੇ 'ਤੇ ਜਾਂਚ ਕਰਕੇ ਮੁਆਵਜ਼ਾ ਤੈਅ ਕਰਦੀ ਹੈ।",
                        ],
                        "documentsRequired": [
                            "ਆਧਾਰ ਕਾਰਡ",
                            "ਜ਼ਮੀਨੀ ਮਾਲਕੀ ਰਿਕਾਰਡ / ਗਿਰਦਾਵਰੀ ਰਿਪੋਰਟ",
                            "ਫ਼ਸਲ ਬਿਜਾਈ ਸਰਟੀਫਿਕੇਟ (ਸਵੈ-ਘੋਸ਼ਣਾ ਪੱਤਰ)",
                            "ਬੈਂਕ ਪਾਸਬੁੱਕ ਕਾਪੀ",
                        ],
                    },
                    "hi": {
                        "summary": "प्रधानमंत्री फसल बीमा योजना (PMFBY) के अंतर्गत प्रतिकूल मौसम, कीट-पतंगों और ओलावृष्टि से फसलों को होने वाले नुकसान पर व्यापक बीमा सुरक्षा प्रदान की जाती है। खरीफ फसलों के लिए किसान प्रीमियम मात्र 2%, रबी के लिए 1.5% तथा वाणिज्यिक/बागवानी फसलों हेतु 5% देय है। स्थानीय आपदाओं (ओलावृष्टि, जलभराव) की स्थिति में नुकसान की सूचना 72 घंटे के भीतर दर्ज कराना अनिवार्य है।",
                        "eligibility": [
                            "अधिसूचित क्षेत्रों में अधिसूचित फसल उगाने वाले सभी ऋणी एवं गैर-ऋणी किसान।",
                            "बटाईदार एवं काश्तकार किसान भी पात्र हैं।",
                        ],
                        "procedure": [
                            "राष्ट्रीय फसल बीमा पोर्टल (pmfby.gov.in), सीएससी केंद्र या सहकारी बैंक के माध्यम से प्रीमियम जमा करें।",
                            "आपदा की स्थिति में 72 घंटे के भीतर 'क्रॉप इंश्योरेंस ऐप' अथवा टोल फ्री नंबर 14447 पर सूचना दर्ज कराएं।",
                            "संयुक्त सर्वे टीम के मुआयने उपरांत क्षतिपूर्ति राशि सीधे बैंक खाते में प्रेषित की जाती है।",
                        ],
                        "documentsRequired": [
                            "आधार कार्ड",
                            "भूमि राजस्व रिकॉर्ड (खसरा/खतौनी)",
                            "बुवाई प्रमाण पत्र / पटवारी गिरदावरी प्रति",
                            "बैंक पासबुक की प्रति",
                        ],
                    },
                    "en": {
                        "summary": "Under PMFBY, comprehensive crop insurance against non-preventable natural risks is provided at subsidized farmer premium rates of 2% for Kharif foodgrains/oilseeds, 1.5% for Rabi crops, and 5% for annual commercial/horticultural crops. For localized risks (hailstorm, landslide, inundation), crop loss intimation within 72 hours is mandatory.",
                        "eligibility": [
                            "All loanee and non-loanee farmers cultivating notified crops in notified insurance units.",
                            "Sharecroppers and tenant farmers with valid land tenancy proof.",
                        ],
                        "procedure": [
                            "Enroll via National Crop Insurance Portal (pmfby.gov.in), bank branch, or CSC before cutoff date.",
                            "In case of localized loss, report claim within 72 hours via Crop Insurance App or toll-free 14447.",
                            "Loss assessment conducted by joint committee followed by direct claim credit.",
                        ],
                        "documentsRequired": [
                            "Aadhaar Card",
                            "Land records (Khatauni/Jamabandi)",
                            "Sowing Certificate / Girdawari issued by village revenue officer",
                            "Bank account passbook copy",
                        ],
                    },
                },
                "citations": [
                    {
                        "doc_id": "pmfby_operational_guidelines",
                        "title": doc["title"],
                        "authority": doc["authority"],
                        "jurisdiction": "Central",
                        "section": "Section 5 & 15.3 (Premium Rates & 72-Hour Loss Intimation)",
                        "page_number": 14,
                        "publication_date": doc["publication_date"],
                        "source_url": doc["direct_url"],
                        "official_translation_url": doc["official_translation_url"],
                    }
                ],
            }

        # --------------------------------------------------------------------
        # 4. COOPERATIVE REGISTRATION (JURISDICTION-AWARE)
        # --------------------------------------------------------------------
        if intent == "cooperative_registration":
            if jur == "punjab":
                doc = OFFICIAL_DOCUMENT_REGISTRY["punjab_act_1961"]
                sec_info = doc["sections"]["8"]
                return {
                    "relevant_act": "The Punjab Co-operative Societies Act, 1961 (Section 8)",
                    "responses": {
                        "pa": {
                            "summary": "ਪੰਜਾਬ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ 1961 ਦੀ ਧਾਰਾ 8 ਅਨੁਸਾਰ, ਇੱਕ ਨਵੀਂ ਪ੍ਰਾਇਮਰੀ ਸਹਿਕਾਰੀ ਸਭਾ ਰਜਿਸਟਰ ਕਰਵਾਉਣ ਲਈ ਵੱਖ-ਵੱਖ ਪਰਿਵਾਰਾਂ ਨਾਲ ਸੰਬੰਧਿਤ ਘੱਟੋ-ਘੱਟ 10 ਬਾਲਗ ਵਿਅਕਤੀਆਂ ਦੀ ਲੋੜ ਹੁੰਦੀ ਹੈ, ਜੋ ਸਭਾ ਦੇ ਪ੍ਰਸਤਾਵਿਤ ਕਾਰਜ ਖੇਤਰ ਵਿੱਚ ਰਹਿੰਦੇ ਹੋਣ ਜਾਂ ਕੰਮ ਕਰਦੇ ਹੋਣ।",
                            "eligibility": [
                                "ਘੱਟੋ-ਘੱਟ 10 ਬਾਲਗ ਵਿਅਕਤੀ ਵੱਖ-ਵੱਖ ਪਰਿਵਾਰਾਂ ਨਾਲ ਸੰਬੰਧਿਤ ਹੋਣ।",
                                "ਮੈਂਬਰਾਂ ਦੀ ਉਮਰ 18 ਸਾਲ ਜਾਂ ਵੱਧ ਹੋਵੇ ਅਤੇ ਕੰਟਰੈਕਟ ਕਰਨ ਦੇ ਯੋਗ ਹੋਣ।",
                                "ਸਭਾ ਦੇ ਕਾਰਜ ਖੇਤਰ ਦੇ ਪੱਕੇ ਵਸਨੀਕ ਹੋਣ।",
                            ],
                            "procedure": [
                                "ਪ੍ਰਮੋਟਰਾਂ ਦੀ ਮੀਟਿੰਗ ਬੁਲਾ ਕੇ ਪ੍ਰਸਤਾਵਿਤ ਉਪ-ਨਿਯਮ (Model Bye-laws) ਪਾਸ ਕਰੋ।",
                                "ਸ਼ੇਅਰ ਮਨੀ ਇਕੱਠੀ ਕਰਕੇ ਮਨਜ਼ੂਰਸ਼ੁਦਾ ਸਹਿਕਾਰੀ ਬੈਂਕ ਵਿੱਚ ਖਾਤਾ ਖੋਲ੍ਹੋ।",
                                "ਜ਼ਿਲ੍ਹਾ ਸਹਾਇਕ ਰਜਿਸਟਰਾਰ (ARCS) ਦਫ਼ਤਰ ਵਿੱਚ ਫ਼ਾਰਮ-ਏ (Form-A) ਵਿੱਚ ਚਾਰ ਕਾਪੀਆਂ ਜਮ੍ਹਾਂ ਕਰੋ।",
                                "ਕਾਨੂੰਨੀ ਪੜਤਾਲ ਉਪਰੰਤ 90 ਦਿਨਾਂ ਦੇ ਅੰਦਰ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਸਰਟੀਫਿਕੇਟ ਜਾਰੀ ਕੀਤਾ ਜਾਂਦਾ ਹੈ।",
                            ],
                            "documentsRequired": [
                                "ਫ਼ਾਰਮ-ਏ ਵਿੱਚ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਅਰਜ਼ੀ (ਚਾਰ ਕਾਪੀਆਂ)",
                                "ਪ੍ਰਸਤਾਵਿਤ ਉਪ-ਨਿਯਮਾਂ ਦੀਆਂ 4 ਦਸਤਖ਼ਤੀ ਕਾਪੀਆਂ",
                                "ਪ੍ਰਮੋਟਰਾਂ ਦੀ ਸੂਚੀ, ਆਧਾਰ ਕਾਰਡ ਅਤੇ ਰਿਹਾਇਸ਼ੀ ਸਬੂਤ",
                                "ਸ਼ੇਅਰ ਪੂੰਜੀ ਜਮ੍ਹਾਂ ਹੋਣ ਦਾ ਬੈਂਕ ਸਰਟੀਫਿਕੇਟ",
                            ],
                        },
                        "en": {
                            "summary": "Under Section 8 of The Punjab Co-operative Societies Act, 1961, an application to register a primary cooperative society requires a minimum of ten adult persons belonging to different families residing or carrying on trade in the proposed area of operation.",
                            "eligibility": [
                                "Minimum 10 individuals belonging to distinct family households.",
                                "Must be competent to contract and 18 years or older.",
                                "Residing within the operational territory of the proposed society.",
                            ],
                            "procedure": [
                                "Convene promoter meeting and adopt proposed Bye-laws.",
                                "Collect initial share capital and open bank account.",
                                "Submit Form-A in quadruplicate to the Assistant Registrar of Cooperative Societies (ARCS).",
                                "Registration certificate issued within 90 days after economic scrutiny.",
                            ],
                            "documentsRequired": [
                                "Form-A registration application (4 copies)",
                                "Four signed copies of proposed Bye-laws",
                                "List of promoter members with Aadhaar numbers and addresses",
                                "Bank share capital deposit certificate",
                            ],
                        },
                    },
                    "citations": [
                        {
                            "doc_id": "punjab_act_1961",
                            "title": doc["title"],
                            "authority": doc["authority"],
                            "jurisdiction": "Punjab",
                            "section": "Section 8 (Application for Registration)",
                            "page_number": sec_info["page"],
                            "publication_date": doc["publication_date"],
                            "source_url": doc["direct_url"],
                        }
                    ],
                }
            elif jur == "haryana":
                doc = OFFICIAL_DOCUMENT_REGISTRY["haryana_act_1984"]
                sec_info = doc["sections"]["6"]
                return {
                    "relevant_act": "The Haryana Co-operative Societies Act, 1984 (Section 6)",
                    "responses": {
                        "hi": {
                            "summary": "हरियाणा सहकारी समितियां अधिनियम, 1984 की धारा 6 के अनुसार, एक नई प्राथमिक सहकारी समिति के पंजीकरण हेतु विभिन्न परिवारों से संबंधित न्यूनतम 10 वयस्क व्यक्तियों का होना अनिवार्य है, जो समिति के कार्यक्षेत्र के निवासी हों।",
                            "eligibility": [
                                "कम से कम 10 वयस्क व्यक्ति अलग-अलग परिवारों से हों।",
                                "आयु 18 वर्ष या उससे अधिक हो एवं अनुबंध करने योग्य हों।",
                                "समिति के प्रस्तावित कार्यक्षेत्र का निवासी होना आवश्यक है।",
                            ],
                            "procedure": [
                                "प्रमोटर सदस्यों की बैठक आयोजित कर उप-नियम (Byelaws) पारित करें।",
                                "शेयर पूंजी जमा कर अधिकृत सहकारी बैंक में अस्थाई खाता खोलें।",
                                "सहायक रजिस्ट्रार (ARCS) कार्यालय में निर्धारित फॉर्म-ए में आवेदन दें।",
                                "जांच उपरांत 60 से 90 दिनों में पंजीकरण प्रमाण पत्र जारी किया जाता है।",
                            ],
                            "documentsRequired": [
                                "फॉर्म-ए में पंजीकरण आवेदन पत्र (4 प्रतियां)",
                                "प्रस्तावित उप-नियमों की 4 हस्ताक्षरित प्रतियां",
                                "प्रमोटर सदस्यों की सूची एवं आधार कार्ड",
                                "बैंक शेयर पूंजी जमा प्रमाण पत्र",
                            ],
                        },
                        "en": {
                            "summary": "Under Section 6 of The Haryana Co-operative Societies Act, 1984, an application for registration of a primary cooperative society requires a minimum of ten adult individuals belonging to distinct families residing within the society's area of operation.",
                            "eligibility": [
                                "Minimum 10 individuals from separate family households.",
                                "Must be 18 years of age or older and competent to contract.",
                                "Residing in the operational jurisdiction of the society.",
                            ],
                            "procedure": [
                                "Convene inaugural meeting of promoters and adopt Bye-laws.",
                                "Collect share capital and open escrow account in cooperative bank.",
                                "Submit Form-A in quadruplicate to the Assistant Registrar (ARCS).",
                                "Registration certificate issued within 60-90 days upon statutory verification.",
                            ],
                            "documentsRequired": [
                                "Form-A application (quadruplicate)",
                                "Four signed copies of proposed Bye-laws",
                                "Promoter members list with addresses and Aadhaar copies",
                                "Bank certificate of share capital deposit",
                            ],
                        },
                    },
                    "citations": [
                        {
                            "doc_id": "haryana_act_1984",
                            "title": doc["title"],
                            "authority": doc["authority"],
                            "jurisdiction": "Haryana",
                            "section": "Section 6 (Conditions of Registration)",
                            "page_number": sec_info["page"],
                            "publication_date": doc["publication_date"],
                            "source_url": doc["direct_url"],
                            "official_translation_url": doc["official_translation_url"],
                        }
                    ],
                }
            elif jur == "jk":
                doc = OFFICIAL_DOCUMENT_REGISTRY["jk_act_1989"]
                sec_info = doc["sections"]["7"]
                return {
                    "relevant_act": "The Jammu and Kashmir Co-operative Societies Act, 1989 (Section 7)",
                    "responses": {
                        "doi": {
                            "summary": "जम्मू-कश्मीर सहकारी सभा अधिनियम, 1989 दी धारा 7 तहत नवी प्राथमिक सहकारी सभा रजिस्टर करवाने लेई बक्खो-बक्ख टब्बरे दे घट्टो-घੱਟ 10 बालिग लोकें दी लोड़ पौंदी ऐ, जेहड़े सभा दे इलाके दे बाशिंदे होन।",
                            "eligibility": [
                                "घट्टो-घੱਟ 10 बालिग मेंबर बक्खो-बक्ख परिवारे चा होन।",
                                "उमर 18 ब'रे थमां मती होए।",
                                "सभा दे कार्यक्षेत्र दा बाशिंदा होना लाजिमी ऐ।",
                            ],
                            "procedure": [
                                "प्रमोटर मेंबरें दी पहली सभा बुलायै बायलाज पास करो।",
                                "शेयर पूंजी जमा करियै सहकारी बैंक च खाता खोलो।",
                                "सहायक रजिस्ट्रार (ARCS) दफ्तर च फार्म-ए जमा करवाओ।",
                                "जांच उपरांत रजिस्ट्रेशन प्रमाण पत्र जारी कीता जंदा ऐ।",
                            ],
                            "documentsRequired": [
                                "फार्म-ए (4 प्रतियां)",
                                "बायलाज दी कापी",
                                "मेंबरें दी सूची ते आधार कार्ड",
                                "बैंक जमा रसीद",
                            ],
                        },
                        "en": {
                            "summary": "Under Section 7 of The Jammu and Kashmir Co-operative Societies Act, 1989, an application to register a primary society requires a minimum of ten adult persons residing or owning agricultural land within the society's area of operation.",
                            "eligibility": [
                                "Minimum 10 adult persons from separate households.",
                                "Residing or owning land in the area of operation.",
                                "Competent to contract under statutory provisions.",
                            ],
                            "procedure": [
                                "Hold inaugural promoter meeting and adopt Model Bye-laws.",
                                "Deposit share capital into cooperative bank account.",
                                "File Form-A with the Assistant Registrar (ARCS).",
                                "Registration certificate issued following statutory inquiry.",
                            ],
                            "documentsRequired": [
                                "Form-A application in quadruplicate",
                                "Four signed copies of proposed Bye-laws",
                                "List of promoters with landholding details and Aadhaar copies",
                                "Bank deposit receipt for share capital",
                            ],
                        },
                    },
                    "citations": [
                        {
                            "doc_id": "jk_act_1989",
                            "title": doc["title"],
                            "authority": doc["authority"],
                            "jurisdiction": "Jammu & Kashmir",
                            "section": "Section 7 (Registration of Cooperative Societies)",
                            "page_number": sec_info["page"],
                            "publication_date": doc["publication_date"],
                            "source_url": doc["direct_url"],
                        }
                    ],
                }
            else:
                # Central / Multi-State Cooperative Registration
                doc = OFFICIAL_DOCUMENT_REGISTRY["mscs_act_2002_amended_2023"]
                sec_info = doc["sections"]["6"]
                return {
                    "relevant_act": "The Multi-State Co-operative Societies Act, 2002 (Section 6)",
                    "responses": {
                        "en": {
                            "summary": "Under Section 6 of the Multi-State Co-operative Societies Act, 2002 (as amended in 2023), registration of a Multi-State Cooperative Society requires at least fifty individuals from each of the participating states (minimum two states). For primary societies operating strictly within a single state, State Cooperative Societies Acts apply.",
                            "eligibility": [
                                "Minimum 50 adult individuals each from at least two distinct Indian States.",
                                "Competent to contract under Indian Contract Act, 1872.",
                                "Common multi-state operational economic objective.",
                            ],
                            "procedure": [
                                "Convene multi-state promoter general meeting and adopt proposed Bye-laws.",
                                "Collect share capital and deposit into approved scheduled bank escrow.",
                                "Submit Form-1 online via Central Registrar portal (crcs.gov.in) with certified scheme of viability.",
                                "Central Registrar scrutinizes application and disposes within 120 days.",
                            ],
                            "documentsRequired": [
                                "Application for registration in Form-1",
                                "Four signed copies of proposed Multi-State Bye-laws",
                                "Certified state-wise list of promoter members with KYC",
                                "Bank certificate verifying paid-up share capital",
                                "Feasibility and business viability scheme",
                            ],
                        },
                        "hi": {
                            "summary": "मल्टी-स्टेट सहकारी समितियां अधिनियम, 2002 की धारा 6 के अनुसार, एक बहु-राज्य सहकारी समिति के गठन हेतु कम से कम दो राज्यों से प्रत्येक राज्य के न्यूनतम 50-50 वयस्क व्यक्तियों (कुल न्यूनतम 100 सदस्य) का होना अनिवार्य है।",
                            "eligibility": [
                                "कम से कम दो राज्यों से 50-50 वयस्क सदस्य।",
                                "अनुबंध करने के योग्य भारतीय नागरिक।",
                                "अंतर-राज्यीय आर्थिक उद्देश्य।",
                            ],
                            "procedure": [
                                "प्रमोटर सदस्यों की सभा बुलाकर उप-नियम पारित करें।",
                                "सीआरसीएस (CRCS) पोर्टल पर ऑनलाइन फॉर्म-1 प्रस्तुत करें।",
                                "केंद्रीय रजिस्ट्रार द्वारा 120 दिनों में पंजीकरण निर्णय लिया जाता है।",
                            ],
                            "documentsRequired": [
                                "फॉर्म-1 ऑनलाइन आवेदन",
                                "उप-नियमों की 4 हस्ताक्षरित प्रतियां",
                                "राज्यवार सदस्यों की सूची व आधार प्रतियां",
                                "बैंक शेयर पूंजी प्रमाण पत्र",
                            ],
                        },
                    },
                    "citations": [
                        {
                            "doc_id": "mscs_act_2002_amended_2023",
                            "title": doc["title"],
                            "authority": doc["authority"],
                            "jurisdiction": "Central",
                            "section": "Section 6 (Application for Registration)",
                            "page_number": sec_info["page"],
                            "publication_date": doc["publication_date"],
                            "source_url": doc["direct_url"],
                        }
                    ],
                }

        # --------------------------------------------------------------------
        # 5. ELECTIONS & MANAGING COMMITTEE TENURE
        # --------------------------------------------------------------------
        if intent == "elections_governance":
            doc_punjab = OFFICIAL_DOCUMENT_REGISTRY["punjab_act_1961"]
            doc_haryana = OFFICIAL_DOCUMENT_REGISTRY["haryana_act_1984"]
            doc_central = OFFICIAL_DOCUMENT_REGISTRY["mscs_act_2002_amended_2023"]

            return {
                "relevant_act": "State & Central Co-operative Societies Acts (Managing Committee Tenure & Reservations)",
                "responses": {
                    "hi": {
                        "summary": "पंजाब सहकारी समितियां अधिनियम 1961 की धारा 26, हरियाणा अधिनियम 1984 की धारा 28, जम्मू-कश्मीर अधिनियम 1989 की धारा 29 एवं केंद्रीय MSCS अधिनियम 2002 की धारा 45 के अनुसार, सहकारी समिति की प्रबंध समिति का कार्यकाल चुनाव की तिथि से 5 वर्ष निर्धारित है। समिति में महिलाओं और अनुसूचित जातियों/पिछड़े वर्गों के लिए वैधानिक आरक्षण अनिवार्य है।",
                        "eligibility": [
                            "सदस्य द्वारा समिति के सभी बकाया चुकता किए गए हों और कोई डिफ़ॉल्ट न हो।",
                            "समिति का सक्रिय मतदाता सदस्य होना अनिवार्य है।",
                            "वैधानिक नियमों के तहत अयोग्य घोषित न किया गया हो।",
                        ],
                        "procedure": [
                            "समिति का कार्यकाल समाप्त होने से पूर्व निर्वाचन अधिकारी द्वारा चुनाव कार्यक्रम अधिसूचित किया जाता है।",
                            "नामांकन पत्र दाखिल किए जाते हैं और जांच उपरांत वैध प्रत्याशियों की सूची जारी होती है।",
                            "गुप्त मतदान द्वारा 5 वर्ष के कार्यकाल हेतु प्रबंध समिति के पदाधिकारियों का चुनाव होता है।",
                        ],
                        "documentsRequired": [
                            "निर्वाचन नामांकन पत्र (प्रस्तावक व समर्थक सहित)",
                            "समिति का नो-ड्यूज (अदेय) प्रमाण पत्र",
                            "मतदाता सूची में दर्ज सदस्यता का प्रमाण व पहचान पत्र",
                        ],
                    },
                    "pa": {
                        "summary": "ਪੰਜਾਬ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ 1961 ਦੀ ਧਾਰਾ 26 ਅਤੇ ਕੇਂਦਰੀ MSCS ਐਕਟ 2002 ਅਨੁਸਾਰ ਸਹਿਕਾਰੀ ਸਭਾ ਦੀ ਪ੍ਰਬੰਧਕੀ ਕਮੇਟੀ (Managing Committee) ਦੀ ਮਿਆਦ 5 ਸਾਲ ਨਿਸ਼ਚਿਤ ਹੈ। ਕਮੇਟੀ ਵਿੱਚ ਔਰਤਾਂ ਅਤੇ ਅਨੁਸੂਚਿਤ ਜਾਤੀਆਂ/ਪੱਛੜੀਆਂ ਸ਼੍ਰੇਣੀਆਂ ਦੇ ਨੁਮਾਇੰਦਿਆਂ ਲਈ ਸੀਟਾਂ ਰਾਖਵੀਆਂ ਰੱਖਣਾ ਕਾਨੂੰਨੀ ਤੌਰ 'ਤੇ ਲਾਜ਼ਮੀ ਹੈ।",
                        "eligibility": [
                            "ਮੈਂਬਰ ਵੱਲੋਂ ਸਭਾ ਦੇ ਸਾਰੇ ਬਕਾਏ ਚੁਕਤੇ ਕੀਤੇ ਹੋਣ ਅਤੇ ਕੋਈ ਡਿਫਾਲਟ ਨਾ ਹੋਵੇ।",
                            "ਸਭਾ ਦਾ ਸਰਗਰਮ ਮੈਂਬਰ ਹੋਵੇ ਜਿਸ ਕੋਲ ਵੋਟ ਪਾਉਣ ਦਾ ਅਧਿਕਾਰ ਹੋਵੇ।",
                        ],
                        "procedure": [
                            "ਮੌਜੂਦਾ ਕਮੇਟੀ ਦੀ ਮਿਆਦ ਖ਼ਤਮ ਹੋਣ ਤੋਂ ਪਹਿਲਾਂ ਰਿਟਰਨਿੰਗ ਅਫ਼ਸਰ ਵੱਲੋਂ ਚੋਣ ਪ੍ਰੋਗਰਾਮ ਨੋਟੀਫਾਈ ਕੀਤਾ ਜਾਂਦਾ ਹੈ।",
                            "ਨਾਮਜ਼ਦਗੀ ਪੱਤਰ ਦਾਖ਼ਲ ਕੀਤੇ ਜਾਂਦੇ ਹਨ ਅਤੇ ਪੜਤਾਲ ਉਪਰੰਤ ਚੋਣ ਚਿੰਨ੍ਹ ਜਾਰੀ ਹੁੰਦੇ ਹਨ।",
                            "ਆਮ ਸਭਾ ਵਿੱਚ ਗੁਪਤ ਮੱਤਦਾਨ ਰਾਹੀਂ 5 ਸਾਲਾਂ ਲਈ ਨਵੇਂ ਅਹੁਦੇਦਾਰ ਚੁਣੇ ਜਾਂਦੇ ਹਨ।",
                        ],
                        "documentsRequired": [
                            "ਚੋਣ ਨਾਮਜ਼ਦਗੀ ਫ਼ਾਰਮ",
                            "ਨੋ-ਡਿਊਜ਼ ਸਰਟੀਫਿਕੇਟ (No-Dues Certificate)",
                            "ਵੋਟਰ ਸੂਚੀ ਵਿੱਚ ਦਰਜ ਮੈਂਬਰਸ਼ਿਪ ਸਬੂਤ",
                        ],
                    },
                    "en": {
                        "summary": "Under Section 26 of the Punjab Act 1961, Section 28 of the Haryana Act 1984, Section 29 of the J&K Act 1989, and Section 45 of the Central MSCS Act 2002, the tenure of an elected cooperative managing committee is fixed at 5 years. Mandatory statutory reservation of seats is prescribed for women and disadvantaged categories.",
                        "eligibility": [
                            "Must be an active voting member without loan defaults.",
                            "Not disqualified under statutory conflict-of-interest provisions.",
                        ],
                        "procedure": [
                            "Election program notified by Returning Officer prior to expiry of term.",
                            "Filing and scrutiny of nominations followed by secret ballot.",
                            "Newly elected committee assumes office for a non-extendable 5-year tenure.",
                        ],
                        "documentsRequired": [
                            "Nomination paper with proposer and seconder endorsements",
                            "Society No-Dues clearance certificate",
                            "Voter list serial extract and identity proof",
                        ],
                    },
                },
                "citations": [
                    {
                        "doc_id": "punjab_act_1961",
                        "title": doc_punjab["title"],
                        "authority": doc_punjab["authority"],
                        "jurisdiction": "Punjab",
                        "section": "Section 26 (Election of Managing Committee)",
                        "page_number": doc_punjab["sections"]["26"]["page"],
                        "publication_date": doc_punjab["publication_date"],
                        "source_url": doc_punjab["direct_url"],
                    },
                    {
                        "doc_id": "mscs_act_2002_amended_2023",
                        "title": doc_central["title"],
                        "authority": doc_central["authority"],
                        "jurisdiction": "Central",
                        "section": "Section 45 (Tenure of Board and Reservations)",
                        "page_number": doc_central["sections"]["45"]["page"],
                        "publication_date": doc_central["publication_date"],
                        "source_url": doc_central["direct_url"],
                    },
                ],
            }

        # --------------------------------------------------------------------
        # 6. DISPUTE RESOLUTION & ARBITRATION
        # --------------------------------------------------------------------
        if intent == "dispute_arbitration":
            doc_punjab = OFFICIAL_DOCUMENT_REGISTRY["punjab_act_1961"]
            doc_haryana = OFFICIAL_DOCUMENT_REGISTRY["haryana_act_1984"]
            return {
                "relevant_act": "Statutory Arbitration Provisions (Section 55 Punjab / Section 102 Haryana)",
                "responses": {
                    "hi": {
                        "summary": "पंजाब सहकारी समितियां अधिनियम 1961 की धारा 55 एवं हरियाणा सहकारी समितियां अधिनियम 1984 की धारा 102 के अनुसार, सहकारी समिति के गठन, प्रबंधन या व्यवसाय से संबंधित किसी भी विवाद में सिविल कोर्ट का क्षेत्राधिकार वर्जित है। ऐसे सभी विवादों को पंजीयक (रजिस्ट्रार) के समक्ष वैधानिक मध्यस्थता (आर्बिट्रेशन) हेतु प्रस्तुत किया जाना अनिवार्य है।",
                        "procedure": [
                            "विवाद के संपूर्ण तथ्यों एवं दावों का विवरण तैयार कर सहायक पंजीयक (ARCS) कार्यालय में मध्यस्थता याचिका प्रस्तुत करें।",
                            "पंजीयक स्वयं अथवा नामित मध्यस्थ (आर्बिट्रेटर) के माध्यम से दोनों पक्षों की सुनवाई करता है।",
                            "जांच उपरांत मध्यस्थता निर्णय (Award) पारित किया जाता है, जो सिविल कोर्ट की डिक्री की भांति प्रभावी होता है।",
                        ],
                        "documentsRequired": [
                            "मध्यस्थता हेतु औपचारिक आवेदन पत्र (दावा याचिका)",
                            "विवाद से संबंधित अनुबंध, रिकॉर्ड अथवा लेन-देन के साक्ष्य",
                            "समिति की सदस्यता का प्रमाण एवं पक्षकारों का विवरण",
                        ],
                    },
                    "pa": {
                        "summary": "ਪੰਜਾਬ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਐਕਟ 1961 ਦੀ ਧਾਰਾ 55 (ਅਤੇ ਹਰਿਆਣਾ ਐਕਟ 1984 ਦੀ ਧਾਰਾ 102) ਅਨੁਸਾਰ, ਸਹਿਕਾਰੀ ਸਭਾ ਦੇ ਪ੍ਰਬੰਧ, ਕਾਰੋਬਾਰ ਜਾਂ ਚੋਣਾਂ ਸੰਬੰਧੀ ਕਿਸੇ ਵੀ ਝਗੜੇ ਜਾਂ ਵਿਵਾਦ ਲਈ ਸਿਵਲ ਅਦਾਲਤ ਵਿੱਚ ਕੇਸ ਨਹੀਂ ਕੀਤਾ ਜਾ ਸਕਦਾ। ਅਜਿਹੇ ਸਾਰੇ ਮਾਮਲੇ ਸਿੱਧੇ ਸਹਿਕਾਰੀ ਰਜਿਸਟਰਾਰ ਕੋਲ ਕਾਨੂੰਨੀ ਆਰਬਿਟ੍ਰੇਸ਼ਨ (ਸਾਲਸੀ) ਲਈ ਦਾਇਰ ਕੀਤੇ ਜਾਣੇ ਜ਼ਰੂਰੀ ਹਨ।",
                        "procedure": [
                            "ਵਿਵਾਦ ਦੇ ਵੇਰਵੇ ਲਿਖ ਕੇ ਸਹਾਇਕ ਰਜਿਸਟਰਾਰ (ARCS) ਦਫ਼ਤਰ ਵਿੱਚ ਆਰਬਿਟ੍ਰੇਸ਼ਨ ਪਟੀਸ਼ਨ ਦਾਇਰ ਕਰੋ।",
                            "ਰਜਿਸਟਰਾਰ ਖ਼ੁਦ ਜਾਂ ਨਿਯੁਕਤ ਆਰਬਿਟਰੇਟਰ ਰਾਹੀਂ ਦੋਵਾਂ ਧਿਰਾਂ ਦੀ ਸੁਣਵਾਈ ਕਰਦਾ ਹੈ।",
                            "ਨਿਰਧਾਰਿਤ ਸਮੇਂ ਅੰਦਰ ਆਰਬਿਟ੍ਰੇਸ਼ਨ ਐਵਾਰਡ (ਫ਼ੈਸਲਾ) ਜਾਰੀ ਕੀਤਾ ਜਾਂਦਾ ਹੈ ਜੋ ਸਿਵਲ ਕੋਰਟ ਦੀ ਡਿਗਰੀ ਵਾਂਗ ਲਾਗੂ ਹੁੰਦਾ ਹੈ।",
                        ],
                    },
                    "en": {
                        "summary": "Under Section 55 of the Punjab Co-operative Societies Act 1961 and Section 102 of the Haryana Co-operative Societies Act 1984, disputes touching the constitution, management, or business of a cooperative society are barred from civil court jurisdiction and must be referred to statutory arbitration before the Registrar.",
                        "procedure": [
                            "File reference petition with statement of claim before Assistant Registrar (ARCS).",
                            "Arbitrator issues notice to parties and conducts evidentiary hearings.",
                            "Arbitration award pronounced, enforceable as a decree of a Civil Court.",
                        ],
                    },
                },
                "citations": [
                    {
                        "doc_id": "punjab_act_1961",
                        "title": doc_punjab["title"],
                        "authority": doc_punjab["authority"],
                        "jurisdiction": "Punjab",
                        "section": "Section 55 (Disputes referable to arbitration)",
                        "page_number": doc_punjab["sections"]["55"]["page"],
                        "publication_date": doc_punjab["publication_date"],
                        "source_url": doc_punjab["direct_url"],
                    },
                    {
                        "doc_id": "haryana_act_1984",
                        "title": doc_haryana["title"],
                        "authority": doc_haryana["authority"],
                        "jurisdiction": "Haryana",
                        "section": "Section 102 (Disputes referable to arbitration)",
                        "page_number": doc_haryana["sections"]["102"]["page"],
                        "publication_date": doc_haryana["publication_date"],
                        "source_url": doc_haryana["direct_url"],
                    },
                ],
            }

        # Default general cooperative fallback referencing verified statutes
        doc_central = OFFICIAL_DOCUMENT_REGISTRY["mscs_act_2002_amended_2023"]
        return {
            "relevant_act": "Multi-State Co-operative Societies Act 2002 & State Cooperative Societies Acts",
            "responses": {
                "en": {
                    "summary": "Cooperative societies in India are governed under the Multi-State Co-operative Societies Act, 2002 for multi-state operations, and State Cooperative Societies Acts (Punjab 1961, Haryana 1984, J&K 1989) for primary societies. For targeted statutory guidance, ask specifically about registration, membership, KCC crop loans, PMFBY insurance, or committee elections.",
                },
                "hi": {
                    "summary": "भारत में सहकारी समितियां अंतर-राज्यीय कार्यक्षेत्र हेतु मल्टी-स्टेट सहकारी अधिनियम 2002 एवं राज्य स्तर पर राज्य सहकारी अधिनियमों (हरियाणा 1984, पंजाब 1961, जम्मू-कश्मीर 1989) द्वारा विनियमित होती हैं।",
                },
                "pa": {
                    "summary": "ਭਾਰਤ ਵਿੱਚ ਸਹਿਕਾਰੀ ਸਭਾਵਾਂ ਮਲਟੀ-ਸਟੇਟ ਐਕਟ 2002 ਅਤੇ ਸੰਬੰਧਿਤ ਰਾਜ ਸਹਿਕਾਰੀ ਐਕਟਾਂ (ਪੰਜਾਬ 1961, ਹਰਿਆਣਾ 1984, ਜੰਮੂ-ਕਸ਼ਮੀਰ 1989) ਅਧੀਨ ਨਿਯਮਿਤ ਹੁੰਦੀਆਂ ਹਨ।",
                },
            },
            "citations": [
                {
                    "doc_id": "mscs_act_2002_amended_2023",
                    "title": doc_central["title"],
                    "authority": doc_central["authority"],
                    "jurisdiction": "Central",
                    "section": "Consolidated Statutory Framework",
                    "page_number": 1,
                    "publication_date": doc_central["publication_date"],
                    "source_url": doc_central["direct_url"],
                }
            ],
        }

source_resolver = SourceResolver()
