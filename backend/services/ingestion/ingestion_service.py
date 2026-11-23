"""
Document Ingestion & Lifecycle Service for SahyogSetu
Orchestrates manifest parsing, document validation, duplicate identification,
statutory section chunking, embedding generation, and vector indexing.
Maintains audit trails and supports incremental ingestion and reindexing.
"""

import os
import csv
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

from ..document_processing.text_cleaner import TextCleaner
from ..document_processing.ocr_engine import OCREngine
from ..document_processing.legal_chunker import LegalChunker
from ..embeddings.embedding_service import embedding_service
from ..vector.sqlite_vector_store import sqlite_vector_store
from ..sources.official_document_service import OFFICIAL_DOCUMENT_REGISTRY

logger = logging.getLogger("sahyogsetu.ingestion")

MANIFEST_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "manifest.csv")

# Map manifest doc_ids to official registry keys if names differ slightly
MANIFEST_TO_OFFICIAL_MAP = {
    "mscs_act_2002_amendment_2023": "mscs_act_2002_amended_2023",
    "mscs_act_2002_amended_2023": "mscs_act_2002_amended_2023",
    "brief_on_model_byelaws_for_pacs": "model_byelaws_pacs_2023",
    "model_bye_laws_explained_in_a_parliament_reply": "model_byelaws_pacs_2023",
    "haryana_co_operative_societies_act_1984_pdf": "haryana_act_1984",
    "act_1989_cooperation_gov_in_copy": "jk_act_1989",
    "kcc_master_circular_2018": "kcc_rbi_master_circular",
    "final_pmfby_operational_guidelines_2023_120125": "pmfby_operational_guidelines",
    "the_punjab_cooperative_societies_act_1961_amended_": "punjab_act_1961",
    "gazette_notification_of_the_2021_amendment": "punjab_act_1961",
    "ots_the_punjab_state_agriculture_development_bank_": "padb_ots_scheme_2024",
    "pacs_computerisation_guidelines": "pacs_computerisation_guidelines",
    "cabinet_decision_pib": "pm_kisan_guidelines",
}

class IngestionService:
    """Manages the end-to-end ingestion pipeline from manifest to vector store."""

    def __init__(self, manifest_path: str = MANIFEST_PATH):
        self.manifest_path = manifest_path
        self.chunker = LegalChunker(max_chars=1200, min_chars=250)
        self.document_statuses: Dict[str, str] = {}
        self.processing_errors: Dict[str, str] = {}

    def load_manifest(self, path: Optional[str] = None) -> List[Dict[str, Any]]:
        """Loads and parses manifest.csv with BOM handling."""
        p = path or self.manifest_path
        if not os.path.exists(p):
            # Fallback check relative to workspace
            p = os.path.join(os.getcwd(), "manifest.csv")
            if not os.path.exists(p):
                raise FileNotFoundError(f"Manifest file not found at {p}")

        with open(p, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = [dict(r) for r in reader]

        return rows

    def get_inventory(self) -> List[Dict[str, Any]]:
        """
        Returns full inventory of all 55 documents with disk availability,
        indexing status, page counts, and metadata.
        """
        rows = self.load_manifest()
        indexed_ids = set(sqlite_vector_store.get_indexed_doc_ids())

        inventory = []
        for r in rows:
            doc_id = r["doc_id"]
            local_path = r.get("local_path", "")
            full_path = os.path.join(os.getcwd(), local_path)
            file_exists = os.path.exists(full_path) if local_path else False

            # Check if indexed or in official registry
            is_indexed = doc_id in indexed_ids or MANIFEST_TO_OFFICIAL_MAP.get(doc_id) in indexed_ids

            current_status = self.document_statuses.get(doc_id)
            if not current_status:
                if is_indexed:
                    current_status = "indexed"
                elif r.get("duplicate_of"):
                    current_status = "duplicate"
                elif r.get("status") in ["excluded", "superseded"]:
                    current_status = r.get("status")
                elif r.get("scanned", "").lower() == "yes" or r.get("text_quality") == "needs_ocr":
                    current_status = "OCR_required"
                elif not file_exists:
                    current_status = "file_missing"
                else:
                    current_status = "pending"

            inventory.append({
                "doc_id": doc_id,
                "title": r.get("title", ""),
                "module": r.get("module", ""),
                "jurisdiction": (r.get("state") or "Central").lower(),
                "state": r.get("state", "Central"),
                "doc_type": r.get("doc_type", "statute"),
                "language": r.get("language") or "en",
                "declared_language": r.get("language") or "en",
                "local_path": local_path,
                "source_url": r.get("source_url", ""),
                "version_or_year": r.get("version_or_year", ""),
                "pages": int(r["pages"]) if r.get("pages") and r["pages"].isdigit() else 0,
                "scanned": r.get("scanned", "no"),
                "text_quality": r.get("text_quality", "ok"),
                "manifest_status": r.get("status", "needs_check"),
                "processing_status": current_status,
                "duplicate_of": r.get("duplicate_of") or None,
                "sha256": r.get("sha256", ""),
                "file_present": file_exists,
                "indexed": is_indexed,
            })

        return inventory

    def ingest_document(self, doc_id: str, force: bool = False) -> Dict[str, Any]:
        """
        Processes and indexes a single document:
        1. Checks duplicate and exclusion flags.
        2. Validates PDF text layer or applies OCR.
        3. If file missing locally, uses verified statutory provisions from OFFICIAL_DOCUMENT_REGISTRY.
        4. Applies legal structure-aware chunking.
        5. Generates 384-dimensional dense embeddings.
        6. Stores chunks in SQLite Vector Store.
        """
        rows = self.load_manifest()
        matching = [r for r in rows if r["doc_id"] == doc_id]
        if not matching:
            return {"doc_id": doc_id, "status": "failed", "error": f"Document ID '{doc_id}' not found in manifest."}

        row = matching[0]

        # 1. Check duplicate status
        if row.get("duplicate_of"):
            self.document_statuses[doc_id] = "duplicate"
            return {
                "doc_id": doc_id,
                "status": "duplicate",
                "message": f"Document is duplicate of '{row['duplicate_of']}'. Skipped separate indexing.",
                "duplicate_of": row["duplicate_of"],
            }

        # 2. Check excluded status
        if row.get("status") in ["excluded", "superseded"]:
            self.document_statuses[doc_id] = row["status"]
            return {
                "doc_id": doc_id,
                "status": row["status"],
                "message": f"Document status is '{row['status']}'. Skipped indexing.",
            }

        # 3. Check existing vectors unless force=True
        if not force:
            existing_chunks = sqlite_vector_store.search(
                query_vector=embedding_service.generate_embedding(doc_id),
                top_k=1,
                filters={"doc_id": doc_id},
            )
            if existing_chunks and existing_chunks[0]["doc_id"] == doc_id:
                self.document_statuses[doc_id] = "indexed"
                return {
                    "doc_id": doc_id,
                    "status": "indexed",
                    "message": "Document is already indexed. Pass force=True to reindex.",
                }

        # 4. Extract pages from file or fallback to official registry provisions
        pages: List[Dict[str, Any]] = []
        extraction_method = "text"
        local_path = row.get("local_path", "")
        full_path = os.path.join(os.getcwd(), local_path)

        if local_path and os.path.exists(full_path) and fitz and full_path.lower().endswith(".pdf"):
            self.document_statuses[doc_id] = "extracting"
            try:
                with fitz.open(full_path) as pdf_doc:
                    for i, page in enumerate(pdf_doc):
                        text = page.get_text("text") or ""
                        method = "text"
                        conf = None

                        # Check if OCR required
                        if (row.get("scanned", "").lower() == "yes" or len(text.strip()) < 50) and OCREngine.is_available():
                            extraction_method = "ocr"
                            pix = page.get_pixmap(dpi=200)
                            ocr_txt, ocr_conf, ocr_stat = OCREngine.ocr_image_bytes(pix.tobytes("png"), row.get("language", "en"))
                            if ocr_txt.strip():
                                text = ocr_txt
                                method = "ocr"
                                conf = ocr_conf

                        pages.append({"page": i + 1, "text": text, "method": method, "conf": conf})
            except Exception as e:
                logger.warning("Error reading PDF %s: %s", full_path, e)
                pages = []

        # If pages are still empty, check OFFICIAL_DOCUMENT_REGISTRY for authoritative statutory text
        if not pages:
            reg_key = MANIFEST_TO_OFFICIAL_MAP.get(doc_id, doc_id)
            official_doc = OFFICIAL_DOCUMENT_REGISTRY.get(reg_key)
            if official_doc:
                extraction_method = "official_statutory_registry"
                if not row.get("source_url") and official_doc.get("direct_url"):
                    row["source_url"] = official_doc.get("direct_url")
                sections = official_doc.get("sections", {})
                for sec_num, sec_info in sections.items():
                    sec_text = (
                        f"Section {sec_num}. {sec_info.get('title', '')} —\n"
                        f"{sec_info.get('summary', '')}\n"
                        f"Applicable to: {official_doc.get('title')}.\n"
                        f"Direct Source URL: {official_doc.get('direct_url', '')} (Page {sec_info.get('page', 1)})."
                    )
                    pages.append({
                        "page": sec_info.get("page", 1),
                        "text": sec_text,
                        "method": "official_statutory_registry",
                        "conf": 100.0,
                    })

        if not pages:
            self.document_statuses[doc_id] = "file_missing"
            return {
                "doc_id": doc_id,
                "status": "file_missing",
                "message": f"Local file not found at '{local_path}' and no statutory provisions available.",
            }

        # 5. Legal Structure-Aware Chunking
        self.document_statuses[doc_id] = "chunking"
        chunks = self.chunker.chunk_document(row, pages)
        if not chunks:
            self.document_statuses[doc_id] = "failed"
            return {"doc_id": doc_id, "status": "failed", "message": "Chunking resulted in 0 chunks."}

        # 6. Embedding Generation
        self.document_statuses[doc_id] = "embedding"
        embed_texts = [c.get("embed_text", c["chunk_text"]) for c in chunks]
        hashes = [c["content_hash"] for c in chunks]
        embeddings = embedding_service.generate_batch_embeddings(embed_texts, hashes)

        # 7. Vector Database Storage
        inserted_count = sqlite_vector_store.insert_chunks(chunks, embeddings)
        self.document_statuses[doc_id] = "indexed"

        logger.info("Successfully ingested doc_id=%s with %d chunks.", doc_id, inserted_count)
        return {
            "doc_id": doc_id,
            "title": row.get("title", ""),
            "jurisdiction": (row.get("state") or "Central").lower(),
            "status": "indexed",
            "chunks_count": inserted_count,
            "pages_processed": len(pages),
            "extraction_method": extraction_method,
            "source_url": row.get("source_url", ""),
            "timestamp": datetime.now().isoformat(),
        }

    def ingest_all(self, force: bool = False, limit: Optional[int] = None) -> Dict[str, Any]:
        """Ingests all documents in manifest with batch processing and progress reporting."""
        inventory = self.get_inventory()
        if limit:
            inventory = inventory[:limit]

        results = []
        indexed_count = 0
        skipped_count = 0
        missing_count = 0
        total_chunks = 0

        for item in inventory:
            doc_id = item["doc_id"]
            res = self.ingest_document(doc_id, force=force)
            results.append(res)
            st = res.get("status")
            if st == "indexed":
                indexed_count += 1
                total_chunks += res.get("chunks_count", 0)
            elif st in ["duplicate", "excluded", "superseded"]:
                skipped_count += 1
            elif st == "file_missing":
                missing_count += 1

        return {
            "total_documents_evaluated": len(inventory),
            "indexed_count": indexed_count,
            "skipped_count": skipped_count,
            "missing_file_count": missing_count,
            "total_chunks_created": total_chunks,
            "total_vectors_in_store": sqlite_vector_store.count_vectors(),
            "results": results,
            "timestamp": datetime.now().isoformat(),
        }

    def reindex_document(self, doc_id: str) -> Dict[str, Any]:
        """Deletes previous vectors and re-runs ingestion pipeline for doc_id."""
        deleted_count = sqlite_vector_store.delete_document(doc_id)
        ingest_res = self.ingest_document(doc_id, force=True)
        return {
            "doc_id": doc_id,
            "previous_chunks_deleted": deleted_count,
            "reindex_result": ingest_res,
        }

    def get_ingestion_status(self) -> Dict[str, Any]:
        """Returns current counts and processing status breakdown."""
        inventory = self.get_inventory()
        status_counts: Dict[str, int] = {}
        for item in inventory:
            st = item["processing_status"]
            status_counts[st] = status_counts.get(st, 0) + 1

        return {
            "total_manifest_documents": len(inventory),
            "total_vectors_stored": sqlite_vector_store.count_vectors(),
            "total_indexed_documents": len(sqlite_vector_store.get_indexed_doc_ids()),
            "status_breakdown": status_counts,
            "embedding_model": embedding_service.get_model_info(),
            "vector_store_path": sqlite_vector_store.db_path,
        }

    def get_ingestion_report(self) -> Dict[str, Any]:
        """Produces comprehensive report for audit and verification."""
        inventory = self.get_inventory()
        jurisdictions: Dict[str, int] = {}
        languages: Dict[str, int] = {}
        review_required = []

        total_pages = sum(item["pages"] for item in inventory)

        for item in inventory:
            jur = item["jurisdiction"]
            jurisdictions[jur] = jurisdictions.get(jur, 0) + 1

            lang = item["language"]
            languages[lang] = languages.get(lang, 0) + 1

            if item["processing_status"] in ["OCR_required", "needs_review", "check_garbled"]:
                review_required.append({
                    "doc_id": item["doc_id"],
                    "title": item["title"],
                    "status": item["processing_status"],
                    "notes": item["text_quality"],
                })

        return {
            "timestamp": datetime.now().isoformat(),
            "total_documents": len(inventory),
            "total_pages_declared": total_pages,
            "total_vectors_stored": sqlite_vector_store.count_vectors(),
            "indexed_documents_count": len(sqlite_vector_store.get_indexed_doc_ids()),
            "jurisdiction_distribution": jurisdictions,
            "language_distribution": languages,
            "documents_requiring_review": review_required,
            "review_count": len(review_required),
        }

ingestion_service = IngestionService()
