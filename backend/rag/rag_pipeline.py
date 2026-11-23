"""
Master Legal RAG Pipeline for SahyogSetu
Orchestrates the complete 15-stage retrieval and answer generation workflow:
Query
-> Language Detection
-> Query Normalization & Preprocessing
-> Intent & Section Extraction
-> Jurisdiction Resolution & Hierarchy Enforcement
-> Query Dense Embedding
-> Dual Semantic + Keyword Retrieval
-> Reciprocal Rank Fusion (RRF)
-> Legal Domain Reranking
-> Context Construction & Source Mapping
-> Answer Generation with Strict Grounding
-> Citation Validation against Official Documents
-> Multilingual Output Rendering
-> Structured Citizen Response with Direct Document URLs.
"""

import logging
from typing import Dict, Any, Optional

from .language_detector import language_detector
from .query_processor import query_processor
from .jurisdiction_resolver import jurisdiction_resolver
from .hybrid_search import hybrid_search_engine
from .reranker import legal_reranker
from .context_builder import context_builder
from .answer_generator import answer_generator
from .citation_validator import citation_validator
from ..services.embeddings.embedding_service import embedding_service

logger = logging.getLogger("sahyogsetu.rag.pipeline")

class LegalRAGPipeline:
    """Executes end-to-end grounded legal assistance queries."""

    def run_sync(
        self,
        query: str,
        user_language: str = "en",
        user_jurisdiction: str = "all",
        attached_doc: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Synchronous execution of the 15-stage legal RAG pipeline.
        Zero socket, loopback, or network dependency.
        """
        # 1. Language Priority Resolution & Detection
        eff_lang = language_detector.resolve_priority_language(user_language, query)
        lang_info = language_detector.detect(query, interface_language=eff_lang)
        clean_query = lang_info["normalized_query"]

        # 2. Query Understanding: Intent & Section Extraction
        processed_q = query_processor.process_query(clean_query)
        intent = processed_q["detected_intent"]
        sections = processed_q["extracted_sections"]

        # 3. Jurisdiction Resolution & Scope Enforcement
        jur_info = jurisdiction_resolver.resolve(
            query=clean_query,
            user_jurisdiction=user_jurisdiction,
            detected_intent=intent,
        )
        target_jur = jur_info["resolved_jurisdiction"]
        allowed_jurs = jur_info["allowed_jurisdictions"]

        # If user clarification is needed for state-dependent questions with ambiguous jurisdiction
        if jur_info["requires_clarification"]:
            return answer_generator.generate_answer_sync(
                query=clean_query,
                context="",
                retrieved_chunks=[],
                validated_citations=[],
                target_language=eff_lang,
                jurisdiction=target_jur,
                clarification_prompt=jur_info["clarification_prompt"],
            )

        # 4. Dense Query Embedding with multilingual keyword enrichment
        search_kw = processed_q.get("search_keywords", [])
        dense_q = f"{clean_query} {' '.join(search_kw)}" if search_kw else clean_query
        query_vector = embedding_service.generate_embedding(dense_q)

        # 5. Hybrid Retrieval (Semantic + Keyword via Reciprocal Rank Fusion)
        fused_candidates = hybrid_search_engine.search(
            query=clean_query,
            query_vector=query_vector,
            allowed_jurisdictions=allowed_jurs,
            extracted_sections=sections,
            search_tokens=search_kw,
            top_k=15,
        )

        # 6. Legal Domain Reranking
        ranked_chunks = legal_reranker.rerank(
            candidates=fused_candidates,
            query=dense_q,
            target_jurisdiction=target_jur,
            extracted_sections=sections,
            detected_intent=intent,
            top_k=5,
        )

        # Check for explicitly queried non-existent statutory section or zero authoritative evidence
        is_unsupported = False
        if sections:
            has_matching_sec = any(
                str(c.get("section") or "").strip() in sections
                for c in ranked_chunks
            )
            if not has_matching_sec and (not ranked_chunks or ranked_chunks[0]["rerank_score"] < 0.25):
                is_unsupported = True
        elif ranked_chunks:
            top_chunk = ranked_chunks[0]
            overlap = top_chunk.get("rerank_boosts", {}).get("query_token_overlap", 0.0)
            intent_boost = top_chunk.get("rerank_boosts", {}).get("intent_alignment", 0.0)
            if intent_boost == 0.0 and overlap < 0.05:
                is_unsupported = True
        else:
            is_unsupported = True

        if is_unsupported:
            return answer_generator.generate_answer_sync(
                query=clean_query,
                context="",
                retrieved_chunks=[],
                validated_citations=[],
                target_language=eff_lang,
                jurisdiction=target_jur,
            )

        # 7. Context Construction & Citation Mapping
        context_str, initial_citations = context_builder.build_context(ranked_chunks)

        # 8. Citation Validation against Corpus
        validated_citations = citation_validator.validate_citations(initial_citations, ranked_chunks)

        # 9. Grounded Answer Generation
        answer_result = answer_generator.generate_answer_sync(
            query=clean_query,
            context=context_str,
            retrieved_chunks=ranked_chunks,
            validated_citations=validated_citations,
            target_language=eff_lang,
            jurisdiction=target_jur,
        )

        # Attach retrieval telemetry for auditability
        answer_result["retrievalTelemetry"] = {
            "intent": intent,
            "detectedScript": lang_info["script"],
            "isRomanized": lang_info["is_romanized"],
            "targetJurisdiction": target_jur,
            "allowedJurisdictions": allowed_jurs,
            "extractedSections": sections,
            "totalChunksRetrieved": len(ranked_chunks),
            "topRetrievalScore": ranked_chunks[0]["rerank_score"] if ranked_chunks else 0.0,
        }

        return answer_result

    async def run(
        self,
        query: str,
        user_language: str = "en",
        user_jurisdiction: str = "all",
        attached_doc: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes complete RAG retrieval, reranking, answering, and citation verification.
        """
        # If external LLM key is configured, use async generation path, otherwise sync
        import os
        if not os.getenv("GEMINI_API_KEY") and not os.getenv("OPENAI_API_KEY"):
            return self.run_sync(
                query=query,
                user_language=user_language,
                user_jurisdiction=user_jurisdiction,
                attached_doc=attached_doc,
            )

        # 1. Language Priority Resolution & Detection
        eff_lang = language_detector.resolve_priority_language(user_language, query)
        lang_info = language_detector.detect(query, interface_language=eff_lang)
        clean_query = lang_info["normalized_query"]

        # 2. Query Understanding: Intent & Section Extraction
        processed_q = query_processor.process_query(clean_query)
        intent = processed_q["detected_intent"]
        sections = processed_q["extracted_sections"]

        # 3. Jurisdiction Resolution & Scope Enforcement
        jur_info = jurisdiction_resolver.resolve(
            query=clean_query,
            user_jurisdiction=user_jurisdiction,
            detected_intent=intent,
        )
        target_jur = jur_info["resolved_jurisdiction"]
        allowed_jurs = jur_info["allowed_jurisdictions"]

        # If user clarification is needed for state-dependent questions with ambiguous jurisdiction
        if jur_info["requires_clarification"]:
            return await answer_generator.generate_answer(
                query=clean_query,
                context="",
                retrieved_chunks=[],
                validated_citations=[],
                target_language=eff_lang,
                jurisdiction=target_jur,
                clarification_prompt=jur_info["clarification_prompt"],
            )

        # 4. Dense Query Embedding with multilingual keyword enrichment
        search_kw = processed_q.get("search_keywords", [])
        dense_q = f"{clean_query} {' '.join(search_kw)}" if search_kw else clean_query
        query_vector = embedding_service.generate_embedding(dense_q)

        # 5. Hybrid Retrieval (Semantic + Keyword via Reciprocal Rank Fusion)
        fused_candidates = hybrid_search_engine.search(
            query=clean_query,
            query_vector=query_vector,
            allowed_jurisdictions=allowed_jurs,
            extracted_sections=sections,
            search_tokens=search_kw,
            top_k=15,
        )

        # 6. Legal Domain Reranking
        ranked_chunks = legal_reranker.rerank(
            candidates=fused_candidates,
            query=dense_q,
            target_jurisdiction=target_jur,
            extracted_sections=sections,
            detected_intent=intent,
            top_k=5,
        )

        # Check for explicitly queried non-existent statutory section or zero authoritative evidence
        is_unsupported = False
        if sections:
            has_matching_sec = any(
                str(c.get("section") or "").strip() in sections
                for c in ranked_chunks
            )
            if not has_matching_sec and (not ranked_chunks or ranked_chunks[0]["rerank_score"] < 0.25):
                is_unsupported = True
        elif ranked_chunks:
            top_chunk = ranked_chunks[0]
            overlap = top_chunk.get("rerank_boosts", {}).get("query_token_overlap", 0.0)
            intent_boost = top_chunk.get("rerank_boosts", {}).get("intent_alignment", 0.0)
            if intent_boost == 0.0 and overlap < 0.05:
                is_unsupported = True
        else:
            is_unsupported = True

        if is_unsupported:
            return answer_generator.generate_answer_sync(
                query=clean_query,
                context="",
                retrieved_chunks=[],
                validated_citations=[],
                target_language=eff_lang,
                jurisdiction=target_jur,
            )

        # 7. Context Construction & Citation Mapping
        context_str, initial_citations = context_builder.build_context(ranked_chunks)

        # 8. Citation Validation against Corpus
        validated_citations = citation_validator.validate_citations(initial_citations, ranked_chunks)

        # 9. Grounded Answer Generation
        answer_result = await answer_generator.generate_answer(
            query=clean_query,
            context=context_str,
            retrieved_chunks=ranked_chunks,
            validated_citations=validated_citations,
            target_language=eff_lang,
            jurisdiction=target_jur,
        )

        # Attach retrieval telemetry for auditability
        answer_result["retrievalTelemetry"] = {
            "intent": intent,
            "detectedScript": lang_info["script"],
            "isRomanized": lang_info["is_romanized"],
            "targetJurisdiction": target_jur,
            "allowedJurisdictions": allowed_jurs,
            "extractedSections": sections,
            "totalChunksRetrieved": len(ranked_chunks),
            "topRetrievalScore": ranked_chunks[0]["rerank_score"] if ranked_chunks else 0.0,
        }

        return answer_result

rag_pipeline = LegalRAGPipeline()
