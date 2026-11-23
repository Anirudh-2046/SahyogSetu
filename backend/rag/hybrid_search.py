"""
Hybrid Search Engine for SahyogSetu Legal RAG
Combines 384-dimensional dense semantic vector similarity with
exact statutory token & BM25 keyword matching using Reciprocal Rank Fusion (RRF).
Enforces strict jurisdiction boundaries across Central, Punjab, Haryana, and J&K.
"""

import sqlite3
import re
from typing import List, Dict, Any, Optional
import numpy as np

from ..services.vector.sqlite_vector_store import sqlite_vector_store
from ..services.embeddings.embedding_service import embedding_service

RRF_K = 60.0

class HybridSearchEngine:
    """Fuses dense semantic embeddings and statutory keyword search."""

    def __init__(self, vector_store=sqlite_vector_store):
        self.vector_store = vector_store

    def search(
        self,
        query: str,
        query_vector: Optional[np.ndarray] = None,
        allowed_jurisdictions: Optional[List[str]] = None,
        extracted_sections: Optional[List[str]] = None,
        search_tokens: Optional[List[str]] = None,
        top_k: int = 8,
    ) -> List[Dict[str, Any]]:
        """
        Executes dual semantic + keyword retrieval and fuses via Reciprocal Rank Fusion.
        """
        if not query or not query.strip():
            return []

        # 1. Dense Semantic Vector Search
        if query_vector is None:
            query_vector = embedding_service.generate_embedding(query)

        candidate_pool_size = max(top_k * 4, 35)

        raw_semantic_hits = self.vector_store.search(
            query_vector=query_vector,
            top_k=candidate_pool_size,
        )

        # Filter semantic hits by allowed jurisdictions
        semantic_hits = []
        for h in raw_semantic_hits:
            if not allowed_jurisdictions or h["jurisdiction"].lower() in allowed_jurisdictions:
                semantic_hits.append(h)

        # 2. Statutory Token & Keyword Search
        keyword_hits = self._keyword_search(
            query=query,
            allowed_jurisdictions=allowed_jurisdictions,
            extracted_sections=extracted_sections,
            search_tokens=search_tokens,
            limit=candidate_pool_size,
        )

        # 3. Reciprocal Rank Fusion (RRF)
        fused_scores: Dict[str, float] = {}
        chunk_map: Dict[str, Dict[str, Any]] = {}
        rank_details: Dict[str, Dict[str, Any]] = {}

        # Process Semantic Ranks
        for rank, hit in enumerate(semantic_hits):
            cid = hit["chunk_id"]
            chunk_map[cid] = hit
            fused_scores[cid] = fused_scores.get(cid, 0.0) + (1.0 / (RRF_K + rank + 1))
            rank_details.setdefault(cid, {})["semantic_rank"] = rank + 1
            rank_details[cid]["semantic_score"] = hit.get("score", 0.0)

        # Process Keyword Ranks
        for rank, hit in enumerate(keyword_hits):
            cid = hit["chunk_id"]
            chunk_map[cid] = hit
            fused_scores[cid] = fused_scores.get(cid, 0.0) + (1.1 / (RRF_K + rank + 1))
            rank_details.setdefault(cid, {})["keyword_rank"] = rank + 1
            rank_details[cid]["keyword_score"] = hit.get("keyword_score", 0.0)

        # Section-level direct boost in RRF if chunk matches extracted_sections
        if extracted_sections:
            for cid, hit in chunk_map.items():
                sec_val = str(hit.get("section") or "").lower()
                if any(es.lower() == sec_val for es in extracted_sections):
                    fused_scores[cid] += 0.025

        # 4. Assemble and Sort Fused Hits
        fused_results = []
        for cid, rrf_score in fused_scores.items():
            record = dict(chunk_map[cid])
            record["rrf_score"] = round(rrf_score, 5)
            record["semantic_rank"] = rank_details.get(cid, {}).get("semantic_rank")
            record["keyword_rank"] = rank_details.get(cid, {}).get("keyword_rank")
            record["original_semantic_score"] = rank_details.get(cid, {}).get("semantic_score", 0.0)
            fused_results.append(record)

        fused_results.sort(key=lambda x: x["rrf_score"], reverse=True)
        return fused_results[:top_k]

    def _keyword_search(
        self,
        query: str,
        allowed_jurisdictions: Optional[List[str]] = None,
        extracted_sections: Optional[List[str]] = None,
        search_tokens: Optional[List[str]] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Executes exact keyword, token density, and section-number search."""
        tokens = [t.lower() for t in re.findall(r"[\w]+", query) if len(t) > 2]
        if search_tokens:
            for st in search_tokens:
                st_l = st.lower()
                if st_l not in tokens:
                    tokens.append(st_l)

        if not tokens and not extracted_sections:
            return []

        sql = """
            SELECT chunk_id, doc_id, document_title, document_type, issuing_body,
                   jurisdiction, state, language, detected_language, chapter,
                   section, subsection, rule, clause, schedule, page_start, page_end,
                   source_url, version_or_year, text_quality, extraction_method,
                   chunk_text, embed_text, content_hash
            FROM document_chunks
        """
        where_clauses = []
        params = []

        if allowed_jurisdictions:
            placeholders = ",".join("?" for _ in allowed_jurisdictions)
            where_clauses.append(f"LOWER(jurisdiction) IN ({placeholders})")
            params.extend([j.lower() for j in allowed_jurisdictions])

        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)

        with sqlite3.connect(self.vector_store.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()

        results = []
        for row in rows:
            text_lower = (row["chunk_text"] or "").lower()
            title_lower = (row["document_title"] or "").lower()
            sec = str(row["section"]).lower() if row["section"] else ""

            score = 0.0

            # Section number boost
            if extracted_sections:
                for es in extracted_sections:
                    es_l = es.lower()
                    if sec and sec == es_l:
                        score += 8.0
                    elif f"section {es_l}" in text_lower[:250] or f"rule {es_l}" in text_lower[:250] or f"ਧਾਰਾ {es_l}" in text_lower[:250] or f"धारा {es_l}" in text_lower[:250]:
                        score += 5.0

            # Token overlap score
            for t in tokens:
                if t in text_lower:
                    score += 1.0
                if t in title_lower:
                    score += 1.5

            if score > 0.0:
                item = dict(row)
                item["keyword_score"] = round(score, 2)
                results.append(item)

        results.sort(key=lambda x: x["keyword_score"], reverse=True)
        return results[:limit]

hybrid_search_engine = HybridSearchEngine()
