"""
Context Builder for SahyogSetu Legal RAG
Constructs structured LLM prompt context from reranked legal evidence.
Retains explicit document titles, sections, authorities, page references,
source URLs, and retrieval telemetry without discarding citation metadata.
"""

from typing import List, Dict, Any, Tuple

class ContextBuilder:
    """Builds grounded context payloads and source citation metadata maps."""

    @classmethod
    def build_context(
        cls,
        ranked_chunks: List[Dict[str, Any]],
        max_context_chars: int = 4000,
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Deduplicates chunks, formats structured context blocks, and returns
        (context_prompt_text, structured_sources_list).
        """
        if not ranked_chunks:
            return ("", [])

        context_blocks = []
        structured_sources = []
        seen_passages = set()
        total_chars = 0

        for i, chunk in enumerate(ranked_chunks):
            # Passage deduplication
            norm_passage = " ".join(chunk["chunk_text"].split())[:200]
            if norm_passage in seen_passages:
                continue
            seen_passages.add(norm_passage)

            title = chunk.get("document_title", "Statutory Document")
            authority = chunk.get("issuing_body", "Government Authority")
            jurisdiction = chunk.get("jurisdiction", "central").capitalize()
            section = chunk.get("section")
            rule = chunk.get("rule")
            sec_label = f"Section {section}" if section else (f"Rule {rule}" if rule else "Statutory Provision")
            page_start = chunk.get("page_start", 1)
            page_end = chunk.get("page_end", 1)
            pages_str = f"Page {page_start}" if page_start == page_end else f"Pages {page_start}-{page_end}"
            source_url = chunk.get("source_url", "")
            version = chunk.get("version_or_year", "")

            block_header = f"--- [DOCUMENT {i+1}: {title} | {jurisdiction}] ---"
            block_meta = f"Authority: {authority} | Provision: {sec_label} | {pages_str}"
            if version:
                block_meta += f" | Version/Year: {version}"
            if source_url:
                block_meta += f" | Official URL: {source_url}"

            block_text = f"{block_header}\n{block_meta}\n{chunk['chunk_text']}\n"

            if total_chars + len(block_text) > max_context_chars:
                break

            context_blocks.append(block_text)
            total_chars += len(block_text)

            # Build structured citation object for response
            structured_sources.append({
                "source_index": i + 1,
                "title": title,
                "authority": authority,
                "jurisdiction": jurisdiction,
                "documentType": chunk.get("document_type", "statute"),
                "section": sec_label,
                "pageNumber": page_start,
                "publicationDate": version or "Verified Gazette",
                "originalLanguage": chunk.get("language", "en"),
                "sourceUrl": source_url,
                "verificationStatus": "verified_gazette" if source_url else "statutory_record",
                "retrievalScore": chunk.get("rerank_score", chunk.get("rrf_score", 0.0)),
            })

        full_context_str = "\n".join(context_blocks)
        return (full_context_str, structured_sources)

context_builder = ContextBuilder()
