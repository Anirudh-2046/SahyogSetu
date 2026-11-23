"""
Persistent SQLite Vector Database for SahyogSetu
Stores 384-dimensional dense vectors alongside 24-field legal chunk metadata.
Provides fast matrix dot-product cosine similarity retrieval with ACID transactional
metadata filtering on jurisdiction, language, document type, and statutory provisions.
"""

import os
import sqlite3
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import numpy as np

from .vector_store_base import VectorStoreBase

logger = logging.getLogger("sahyogsetu.vector.sqlite")

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
DEFAULT_VECTOR_DB_PATH = os.path.join(DB_DIR, "vectors.db")

class PersistentSqliteVectorStore(VectorStoreBase):
    """ACID-compliant SQLite Vector Database with NumPy cosine ranking."""

    def __init__(self, db_path: str = DEFAULT_VECTOR_DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.initialize()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize(self) -> None:
        """Creates tables and indices for vector chunks and document registry."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 1. Document Chunks Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS document_chunks (
                    chunk_id TEXT PRIMARY KEY,
                    doc_id TEXT NOT NULL,
                    document_title TEXT NOT NULL,
                    document_type TEXT,
                    issuing_body TEXT,
                    jurisdiction TEXT NOT NULL,
                    state TEXT,
                    language TEXT NOT NULL,
                    detected_language TEXT,
                    chapter TEXT,
                    section TEXT,
                    subsection TEXT,
                    rule TEXT,
                    clause TEXT,
                    schedule TEXT,
                    page_start INTEGER,
                    page_end INTEGER,
                    source_url TEXT,
                    version_or_year TEXT,
                    date_retrieved TEXT,
                    date_audited TEXT,
                    text_quality TEXT,
                    extraction_method TEXT,
                    chunk_text TEXT NOT NULL,
                    embed_text TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    embedding_blob BLOB NOT NULL,
                    created_at TEXT NOT NULL
                );
            """)

            # 2. Indexed Documents Registry Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS indexed_documents (
                    doc_id TEXT PRIMARY KEY,
                    document_title TEXT NOT NULL,
                    jurisdiction TEXT NOT NULL,
                    language TEXT NOT NULL,
                    chunk_count INTEGER NOT NULL DEFAULT 0,
                    total_chars INTEGER NOT NULL DEFAULT 0,
                    source_url TEXT,
                    version_or_year TEXT,
                    sha256 TEXT,
                    status TEXT NOT NULL DEFAULT 'indexed',
                    indexed_at TEXT NOT NULL
                );
            """)

            # Indices for rapid metadata filtering
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_doc_id ON document_chunks(doc_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_jurisdiction ON document_chunks(jurisdiction);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_language ON document_chunks(language);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_section ON document_chunks(section);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_chunks_hash ON document_chunks(content_hash);")
            conn.commit()

        logger.info("Initialized PersistentSqliteVectorStore at: %s", self.db_path)

    def insert_chunks(
        self,
        chunks: List[Dict[str, Any]],
        embeddings: List[np.ndarray],
    ) -> int:
        """Stores chunk records and their float32 embedding blobs in a single transaction."""
        if not chunks or len(chunks) != len(embeddings):
            raise ValueError("Chunks list and embeddings list must be non-empty and equal in length.")

        now_iso = datetime.now().isoformat()
        records_to_insert = []
        doc_stats: Dict[str, Dict[str, Any]] = {}

        for chunk, emb in zip(chunks, embeddings):
            emb_blob = emb.astype(np.float32).tobytes()
            doc_id = chunk["doc_id"]

            records_to_insert.append((
                chunk["chunk_id"],
                doc_id,
                chunk.get("document_title", ""),
                chunk.get("document_type", "statute"),
                chunk.get("issuing_body", ""),
                chunk.get("jurisdiction", "central"),
                chunk.get("state", ""),
                chunk.get("language", "en"),
                chunk.get("detected_language", "en"),
                chunk.get("chapter"),
                chunk.get("section"),
                chunk.get("subsection"),
                chunk.get("rule"),
                chunk.get("clause"),
                chunk.get("schedule"),
                chunk.get("page_start", 1),
                chunk.get("page_end", 1),
                chunk.get("source_url", ""),
                chunk.get("version_or_year", ""),
                chunk.get("date_retrieved", ""),
                chunk.get("date_audited", ""),
                chunk.get("text_quality", "ok"),
                chunk.get("extraction_method", "text"),
                chunk["chunk_text"],
                chunk.get("embed_text", chunk["chunk_text"]),
                chunk.get("content_hash", ""),
                emb_blob,
                now_iso,
            ))

            # Aggregate stats per document
            if doc_id not in doc_stats:
                doc_stats[doc_id] = {
                    "title": chunk.get("document_title", ""),
                    "jurisdiction": chunk.get("jurisdiction", "central"),
                    "language": chunk.get("language", "en"),
                    "source_url": chunk.get("source_url", ""),
                    "version_or_year": chunk.get("version_or_year", ""),
                    "sha256": chunk.get("doc_sha256", ""),
                    "count": 0,
                    "chars": 0,
                }
            doc_stats[doc_id]["count"] += 1
            doc_stats[doc_id]["chars"] += len(chunk["chunk_text"])

        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Insert chunks with REPLACE semantics to support safe idempotent reindexing
            cursor.executemany("""
                INSERT OR REPLACE INTO document_chunks (
                    chunk_id, doc_id, document_title, document_type, issuing_body,
                    jurisdiction, state, language, detected_language, chapter,
                    section, subsection, rule, clause, schedule, page_start, page_end,
                    source_url, version_or_year, date_retrieved, date_audited,
                    text_quality, extraction_method, chunk_text, embed_text,
                    content_hash, embedding_blob, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, records_to_insert)

            # Update indexed_documents registry
            for doc_id, stat in doc_stats.items():
                cursor.execute("""
                    INSERT OR REPLACE INTO indexed_documents (
                        doc_id, document_title, jurisdiction, language,
                        chunk_count, total_chars, source_url, version_or_year,
                        sha256, status, indexed_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'indexed', ?)
                """, (
                    doc_id, stat["title"], stat["jurisdiction"], stat["language"],
                    stat["count"], stat["chars"], stat["source_url"], stat["version_or_year"],
                    stat["sha256"], now_iso
                ))

            conn.commit()

        logger.info("Inserted %d chunks across %d documents into vector store.", len(chunks), len(doc_stats))
        return len(chunks)

    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Executes metadata filtering and cosine similarity ranking.
        Supports filtering by: jurisdiction, language, doc_id, document_type, state.
        """
        sql = """
            SELECT chunk_id, doc_id, document_title, document_type, issuing_body,
                   jurisdiction, state, language, detected_language, chapter,
                   section, subsection, rule, clause, schedule, page_start, page_end,
                   source_url, version_or_year, text_quality, extraction_method,
                   chunk_text, embed_text, content_hash, embedding_blob
            FROM document_chunks
        """
        where_clauses = []
        params = []

        if filters:
            if "jurisdiction" in filters and filters["jurisdiction"] and filters["jurisdiction"].lower() != "all":
                where_clauses.append("LOWER(jurisdiction) = ?")
                params.append(filters["jurisdiction"].lower())

            if "language" in filters and filters["language"] and filters["language"].lower() != "all":
                where_clauses.append("(LOWER(language) = ? OR LOWER(detected_language) = ?)")
                params.extend([filters["language"].lower(), filters["language"].lower()])

            if "doc_id" in filters and filters["doc_id"]:
                where_clauses.append("doc_id = ?")
                params.append(filters["doc_id"])

            if "document_type" in filters and filters["document_type"]:
                where_clauses.append("document_type = ?")
                params.append(filters["document_type"])

            if "state" in filters and filters["state"]:
                where_clauses.append("LOWER(state) = ?")
                params.append(filters["state"].lower())

        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()

        if not rows:
            return []

        # Vectorized dot product calculation
        q_norm = np.linalg.norm(query_vector)
        q_vec = (query_vector / q_norm).astype(np.float32) if q_norm > 1e-6 else query_vector.astype(np.float32)

        results = []
        for row in rows:
            emb = np.frombuffer(row["embedding_blob"], dtype=np.float32)
            score = float(np.dot(emb, q_vec))

            results.append({
                "score": round(score, 4),
                "chunk_id": row["chunk_id"],
                "doc_id": row["doc_id"],
                "document_title": row["document_title"],
                "document_type": row["document_type"],
                "issuing_body": row["issuing_body"],
                "jurisdiction": row["jurisdiction"],
                "state": row["state"],
                "language": row["language"],
                "detected_language": row["detected_language"],
                "chapter": row["chapter"],
                "section": row["section"],
                "subsection": row["subsection"],
                "rule": row["rule"],
                "clause": row["clause"],
                "schedule": row["schedule"],
                "page_start": row["page_start"],
                "page_end": row["page_end"],
                "source_url": row["source_url"],
                "version_or_year": row["version_or_year"],
                "text_quality": row["text_quality"],
                "extraction_method": row["extraction_method"],
                "chunk_text": row["chunk_text"],
                "embed_text": row["embed_text"],
                "content_hash": row["content_hash"],
            })

        # Sort descending by cosine similarity score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def get_chunk(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves single chunk by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT chunk_id, doc_id, document_title, document_type, issuing_body,
                       jurisdiction, state, language, detected_language, chapter,
                       section, subsection, rule, clause, schedule, page_start, page_end,
                       source_url, version_or_year, text_quality, extraction_method,
                       chunk_text, embed_text, content_hash
                FROM document_chunks
                WHERE chunk_id = ?
            """, (chunk_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return dict(row)

    def delete_document(self, doc_id: str) -> int:
        """Deletes all chunks and registry entries for a document."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM document_chunks WHERE doc_id = ?", (doc_id,))
            deleted_count = cursor.rowcount
            cursor.execute("DELETE FROM indexed_documents WHERE doc_id = ?", (doc_id,))
            conn.commit()
        logger.info("Deleted %d chunks for doc_id=%s", deleted_count, doc_id)
        return deleted_count

    def count_vectors(self) -> int:
        """Returns total chunk vector count."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM document_chunks")
            return cursor.fetchone()[0]

    def get_indexed_doc_ids(self) -> List[str]:
        """Returns list of all indexed doc_ids."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT doc_id FROM indexed_documents ORDER BY doc_id ASC")
            return [r[0] for r in cursor.fetchall()]

    def get_indexed_documents(self) -> List[Dict[str, Any]]:
        """Returns all indexed document summaries."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT doc_id, document_title, jurisdiction, language, chunk_count,
                       total_chars, source_url, version_or_year, sha256, status, indexed_at
                FROM indexed_documents
                ORDER BY jurisdiction ASC, document_title ASC
            """)
            return [dict(r) for r in cursor.fetchall()]

    def clear(self) -> None:
        """Clears all vectors and document indices."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM document_chunks")
            cursor.execute("DELETE FROM indexed_documents")
            conn.commit()

sqlite_vector_store = PersistentSqliteVectorStore()
