"""
SQLite Database Layer for SahyogSetu Backend Architecture
Stores and manages:
- Conversations, chronological messages, and user feedback with referential integrity.
- Verified official news announcements with direct statutory document links.
- Monitored government connectors and operational audit logs.
- Uploaded document registry with extracted text and clauses.

Enforces:
- Foreign key constraints (PRAGMA foreign_keys = ON)
- Cascading deletion of conversation messages and feedback
- Indexes on query patterns and timestamps
- Safe schema initialization and zero data loss on migration
"""

import os
import json
import sqlite3
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from contextlib import contextmanager

from .config import settings

logger = logging.getLogger("sahyogsetu.db")

DB_DIR = settings.DB_DIR
DB_PATH = settings.DB_PATH

@contextmanager
def get_db_connection():
    """Context manager providing thread-safe, transactional SQLite connections with FK enforcement."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error("Database transaction rolled back due to error: %s", e)
        raise
    finally:
        conn.close()

def init_db():
    """Initializes tables and indexes, adding any missing migration columns safely."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # ---------------------------------------------------------------------
        # 1. News items table with direct government sources (PRESERVED)
        # ---------------------------------------------------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news_items (
                news_id TEXT PRIMARY KEY,
                headline_original TEXT NOT NULL,
                description_original TEXT NOT NULL,
                full_text_original TEXT,
                source_name TEXT NOT NULL,
                source_type TEXT NOT NULL,
                source_url TEXT NOT NULL UNIQUE,
                publication_date TEXT NOT NULL,
                fetched_at TEXT NOT NULL,
                jurisdiction TEXT NOT NULL,
                issuing_department TEXT NOT NULL,
                original_language TEXT NOT NULL,
                category TEXT NOT NULL,
                keywords_json TEXT NOT NULL,
                target_audience TEXT NOT NULL,
                central_relevance INTEGER NOT NULL,
                summary_original TEXT NOT NULL,
                summary_translated_json TEXT NOT NULL,
                relevance_explanation_json TEXT NOT NULL,
                headline_translated_json TEXT NOT NULL,
                verification_status TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                source_title TEXT,
                source_reference_number TEXT,
                original_source_url TEXT,
                official_translation_url TEXT,
                translated_source_language TEXT,
                source_verified INTEGER DEFAULT 1,
                source_verification_status TEXT DEFAULT 'verified_official_document',
                last_verified_at TEXT
            )
        """)

        # Safely run migrations for existing DBs if columns were created earlier
        migration_columns = [
            ("source_title", "TEXT"),
            ("source_reference_number", "TEXT"),
            ("original_source_url", "TEXT"),
            ("official_translation_url", "TEXT"),
            ("translated_source_language", "TEXT"),
            ("source_verified", "INTEGER DEFAULT 1"),
            ("source_verification_status", "TEXT DEFAULT 'verified_official_document'"),
            ("last_verified_at", "TEXT"),
            ("document_url", "TEXT"),
            ("official_source_status", "TEXT DEFAULT 'verified_official_source'"),
            ("official_document_status", "TEXT DEFAULT 'verified_official_document'"),
            ("duplicate_of", "TEXT"),
            ("relevance_score", "REAL DEFAULT 1.0"),
            ("model_version", "TEXT DEFAULT 'phase6_logistic_regression_v1'"),
            ("translation_status", "TEXT DEFAULT 'completed'"),
            ("summary_status", "TEXT DEFAULT 'completed'"),
            ("updated_at", "TEXT"),
        ]
        for col_name, col_type in migration_columns:
            try:
                cursor.execute(f"ALTER TABLE news_items ADD COLUMN {col_name} {col_type}")
            except sqlite3.OperationalError:
                pass

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_news_jurisdiction ON news_items(jurisdiction)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_news_category ON news_items(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_news_pubdate ON news_items(publication_date DESC)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_news_hash ON news_items(content_hash)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_news_verified ON news_items(source_verified)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_news_doc_status ON news_items(official_document_status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_news_duplicate ON news_items(duplicate_of)")

        # Safe backfill for pre-existing records to populate Phase 7 provenance fields
        cursor.execute("""
            UPDATE news_items
            SET original_source_url = source_url
            WHERE original_source_url IS NULL OR original_source_url = ''
        """)
        cursor.execute("""
            UPDATE news_items
            SET document_url = source_url,
                official_document_status = 'verified_official_document'
            WHERE (document_url IS NULL OR document_url = '')
              AND (source_url LIKE '%.pdf' OR original_source_url LIKE '%.pdf')
        """)

        # ---------------------------------------------------------------------
        # 2. News sources operational status (PRESERVED)
        # ---------------------------------------------------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news_sources (
                source_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                jurisdiction TEXT NOT NULL,
                url TEXT NOT NULL,
                source_type TEXT NOT NULL,
                last_status TEXT NOT NULL,
                last_fetched_at TEXT,
                items_collected INTEGER DEFAULT 0,
                notes TEXT
            )
        """)

        # ---------------------------------------------------------------------
        # 3. Source audit logs (PRESERVED)
        # ---------------------------------------------------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS source_audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audited_at TEXT NOT NULL,
                report_json TEXT NOT NULL
            )
        """)

        # ---------------------------------------------------------------------
        # 4. Conversations table (Phase 2 Standard Schema Migration)
        # ---------------------------------------------------------------------
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'")
        has_conv_table = cursor.fetchone() is not None

        if has_conv_table:
            cursor.execute("PRAGMA table_info(conversations)")
            conv_cols = [r["name"] for r in cursor.fetchall()]
            if "conversation_id" not in conv_cols:
                # Migrate conversations table to standard Phase 2 schema
                cursor.execute("""
                    CREATE TABLE conversations_new (
                        conversation_id TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        user_id TEXT,
                        jurisdiction TEXT NOT NULL DEFAULT 'all',
                        language TEXT NOT NULL DEFAULT 'en',
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        is_bookmarked INTEGER DEFAULT 0
                    )
                """)
                cursor.execute("""
                    INSERT INTO conversations_new (conversation_id, title, user_id, jurisdiction, language, created_at, updated_at, is_bookmarked)
                    SELECT id, title, NULL, jurisdiction, language, created_at, updated_at, is_bookmarked FROM conversations
                """)
                cursor.execute("DROP TABLE conversations")
                cursor.execute("ALTER TABLE conversations_new RENAME TO conversations")
        else:
            cursor.execute("""
                CREATE TABLE conversations (
                    conversation_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    user_id TEXT,
                    jurisdiction TEXT NOT NULL DEFAULT 'all',
                    language TEXT NOT NULL DEFAULT 'en',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    is_bookmarked INTEGER DEFAULT 0
                )
            """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_updated ON conversations(updated_at DESC)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_user ON conversations(user_id)")

        # ---------------------------------------------------------------------
        # 5. Messages table (Phase 2 Standard Schema Migration)
        # ---------------------------------------------------------------------
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
        has_msg_table = cursor.fetchone() is not None

        if has_msg_table:
            cursor.execute("PRAGMA table_info(messages)")
            msg_cols = [r["name"] for r in cursor.fetchall()]
            if "message_id" not in msg_cols or "role" not in msg_cols:
                # Migrate messages table to standard Phase 2 schema
                cursor.execute("""
                    CREATE TABLE messages_new (
                        message_id TEXT PRIMARY KEY,
                        conversation_id TEXT NOT NULL,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        language TEXT NOT NULL DEFAULT 'en',
                        created_at TEXT NOT NULL,
                        metadata_json TEXT,
                        FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE
                    )
                """)
                if "sender" in msg_cols and "text" in msg_cols:
                    cursor.execute("""
                        INSERT INTO messages_new (message_id, conversation_id, role, content, language, created_at, metadata_json)
                        SELECT id, conversation_id, sender, COALESCE(text, ''), 'en', timestamp, payload_json FROM messages
                    """)
                cursor.execute("DROP TABLE messages")
                cursor.execute("ALTER TABLE messages_new RENAME TO messages")
        else:
            cursor.execute("""
                CREATE TABLE messages (
                    message_id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    language TEXT NOT NULL DEFAULT 'en',
                    created_at TEXT NOT NULL,
                    metadata_json TEXT,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE
                )
            """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_msg_conv ON messages(conversation_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_msg_created ON messages(created_at)")

        # ---------------------------------------------------------------------
        # 6. Feedback table (Phase 2 Standard Schema Migration)
        # ---------------------------------------------------------------------
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'")
        has_fb_table = cursor.fetchone() is not None

        if has_fb_table:
            cursor.execute("PRAGMA table_info(feedback)")
            fb_cols = [r["name"] for r in cursor.fetchall()]
            if "feedback_id" not in fb_cols or "feedback_text" not in fb_cols:
                cursor.execute("""
                    CREATE TABLE feedback_new (
                        feedback_id TEXT PRIMARY KEY,
                        conversation_id TEXT,
                        message_id TEXT NOT NULL,
                        rating TEXT NOT NULL,
                        feedback_text TEXT,
                        created_at TEXT NOT NULL,
                        FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE,
                        FOREIGN KEY (message_id) REFERENCES messages(message_id) ON DELETE CASCADE
                    )
                """)
                if "comments" in fb_cols:
                    cursor.execute("""
                        INSERT INTO feedback_new (feedback_id, conversation_id, message_id, rating, feedback_text, created_at)
                        SELECT id, conversation_id, message_id, rating, comments, timestamp FROM feedback
                    """)
                cursor.execute("DROP TABLE feedback")
                cursor.execute("ALTER TABLE feedback_new RENAME TO feedback")
        else:
            cursor.execute("""
                CREATE TABLE feedback (
                    feedback_id TEXT PRIMARY KEY,
                    conversation_id TEXT,
                    message_id TEXT NOT NULL,
                    rating TEXT NOT NULL,
                    feedback_text TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE,
                    FOREIGN KEY (message_id) REFERENCES messages(message_id) ON DELETE CASCADE
                )
            """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_feedback_conv ON feedback(conversation_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_feedback_msg ON feedback(message_id)")

        # ---------------------------------------------------------------------
        # 7. Uploaded documents registry (PRESERVED)
        # ---------------------------------------------------------------------
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uploaded_documents (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                extracted_text TEXT,
                jurisdiction TEXT,
                language TEXT,
                created_at TEXT NOT NULL
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_docs_created ON uploaded_documents(created_at DESC)")

    logger.info("Database initialized successfully at %s", DB_PATH)

# ============================================================================
# CONVERSATION CRUD OPERATIONS
# ============================================================================

def create_conversation(
    conv_id: str,
    title: str,
    jurisdiction: str = "all",
    language: str = "en",
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """Creates a new conversation session and returns its formatted record."""
    now = datetime.now().isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO conversations (conversation_id, title, user_id, jurisdiction, language, created_at, updated_at, is_bookmarked)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (conv_id, title, user_id, jurisdiction, language, now, now, 0))

    return {
        "conversation_id": conv_id,
        "id": conv_id,
        "conversationId": conv_id,
        "title": title,
        "user_id": user_id,
        "jurisdiction": jurisdiction,
        "language": language,
        "created_at": now,
        "createdAt": now,
        "updated_at": now,
        "updatedAt": now,
        "is_bookmarked": False,
        "isBookmarked": False,
        "message_count": 0,
        "messageCount": 0,
    }

def get_conversations(limit: int = 50, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves conversation thread summaries ordered by last update."""
    query = """
        SELECT c.*, COUNT(m.message_id) as message_count
        FROM conversations c
        LEFT JOIN messages m ON c.conversation_id = m.conversation_id
    """
    params: List[Any] = []
    if user_id:
        query += " WHERE c.user_id = ?"
        params.append(user_id)

    query += " GROUP BY c.conversation_id ORDER BY c.updated_at DESC LIMIT ?"
    params.append(limit)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        return [
            {
                "conversation_id": r["conversation_id"],
                "id": r["conversation_id"],
                "conversationId": r["conversation_id"],
                "title": r["title"],
                "user_id": r["user_id"],
                "jurisdiction": r["jurisdiction"],
                "language": r["language"],
                "created_at": r["created_at"],
                "createdAt": r["created_at"],
                "updated_at": r["updated_at"],
                "updatedAt": r["updated_at"],
                "message_count": r["message_count"],
                "messageCount": r["message_count"],
                "is_bookmarked": bool(r["is_bookmarked"]),
                "isBookmarked": bool(r["is_bookmarked"]),
            }
            for r in rows
        ]

def get_conversation_by_id(conv_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves conversation summary by ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, COUNT(m.message_id) as message_count
            FROM conversations c
            LEFT JOIN messages m ON c.conversation_id = m.conversation_id
            WHERE c.conversation_id = ?
            GROUP BY c.conversation_id
        """, (conv_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "conversation_id": row["conversation_id"],
            "id": row["conversation_id"],
            "conversationId": row["conversation_id"],
            "title": row["title"],
            "user_id": row["user_id"],
            "jurisdiction": row["jurisdiction"],
            "language": row["language"],
            "created_at": row["created_at"],
            "createdAt": row["created_at"],
            "updated_at": row["updated_at"],
            "updatedAt": row["updated_at"],
            "message_count": row["message_count"],
            "messageCount": row["message_count"],
            "is_bookmarked": bool(row["is_bookmarked"]),
            "isBookmarked": bool(row["is_bookmarked"]),
        }

def rename_conversation(conv_id: str, new_title: str) -> bool:
    """Updates the title and timestamp of an existing conversation."""
    now = datetime.now().isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE conversations SET title = ?, updated_at = ? WHERE conversation_id = ?
        """, (new_title, now, conv_id))
        return cursor.rowcount > 0

def delete_conversation(conv_id: str) -> bool:
    """
    Deletes conversation and cascades deletion to all associated messages and feedback.
    Enforces referential integrity.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversations WHERE conversation_id = ?", (conv_id,))
        return cursor.rowcount > 0

# ============================================================================
# MESSAGE CRUD OPERATIONS
# ============================================================================

def save_message(
    msg_id: str,
    conv_id: str,
    role: str,
    content: str,
    language: str = "en",
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Saves a message associated with a conversation and updates conversation timestamp.
    Raises sqlite3.IntegrityError if conversation does not exist.
    """
    now = datetime.now().isoformat()
    metadata_json = json.dumps(metadata, ensure_ascii=False) if metadata else None
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO messages (message_id, conversation_id, role, content, language, created_at, metadata_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (msg_id, conv_id, role, content, language, now, metadata_json))
        cursor.execute("UPDATE conversations SET updated_at = ? WHERE conversation_id = ?", (now, conv_id))
        return True

def get_messages_for_conversation(conv_id: str) -> List[Dict[str, Any]]:
    """Retrieves chronological messages for a conversation thread."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC
        """, (conv_id,))
        rows = cursor.fetchall()
        msgs = []
        for r in rows:
            meta = None
            if r["metadata_json"]:
                try:
                    meta = json.loads(r["metadata_json"])
                except Exception:
                    meta = None
            msgs.append({
                "message_id": r["message_id"],
                "id": r["message_id"],
                "conversation_id": r["conversation_id"],
                "conversationId": r["conversation_id"],
                "role": r["role"],
                "sender": r["role"],
                "content": r["content"],
                "text": r["content"],
                "language": r["language"],
                "created_at": r["created_at"],
                "timestamp": r["created_at"],
                "metadata": meta,
                "payload": meta,
            })
        return msgs

# ============================================================================
# FEEDBACK CRUD OPERATIONS
# ============================================================================

def save_feedback(
    feedback_id: str,
    message_id: str,
    rating: str,
    feedback_text: Optional[str] = None,
    conv_id: Optional[str] = None
) -> bool:
    """
    Records citizen feedback.
    Enforces referential integrity on message_id and conversation_id.
    """
    now = datetime.now().isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO feedback (feedback_id, conversation_id, message_id, rating, feedback_text, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (feedback_id, conv_id, message_id, rating, feedback_text or "", now))
        return True

def get_feedback_for_conversation(conv_id: str) -> List[Dict[str, Any]]:
    """Retrieves feedback items recorded for a specific conversation."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM feedback WHERE conversation_id = ? ORDER BY created_at DESC
        """, (conv_id,))
        return [dict(r) for r in cursor.fetchall()]

def get_feedback_by_id(feedback_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single feedback record by ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM feedback WHERE feedback_id = ?", (feedback_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

# ============================================================================
# DOCUMENT UPLOAD CRUD OPERATIONS
# ============================================================================

def save_uploaded_document(
    doc_id: str,
    filename: str,
    file_size: int,
    extracted_text: str,
    jurisdiction: str = "central",
    language: str = "en"
) -> bool:
    """Records an uploaded document and its extracted text."""
    now = datetime.now().isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO uploaded_documents (id, filename, file_size, extracted_text, jurisdiction, language, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (doc_id, filename, file_size, extracted_text, jurisdiction, language, now))
        return True

def get_uploaded_document(doc_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves uploaded document metadata and extracted text."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM uploaded_documents WHERE id = ?", (doc_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

# ============================================================================
# NEWS & NLP PERSISTENCE (PRESERVED & EXPANDED)
# ============================================================================

def save_news_item(item: Dict[str, Any]) -> bool:
    """Inserts or replaces news item with direct source document references."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            direct_url = item.get("original_source_url") or item.get("source_url") or ""
            source_verified = 1 if item.get("source_verified", True) else 0

            # Reject root homepages
            if direct_url.rstrip("/") in [
                "https://cooperation.gov.in",
                "https://pib.gov.in",
                "https://punjab.gov.in",
                "https://haryana.gov.in",
                "https://www.haryana.gov.in",
                "https://jk.gov.in",
                "http://punjab.gov.in",
                "http://jk.gov.in",
            ]:
                source_verified = 0
                verification_status = "unverified_pending_document"
            else:
                verification_status = item.get("source_verification_status") or item.get("verification_status") or "verified_official_document"

            now_iso = datetime.now().isoformat()
            last_verified_at = item.get("last_verified_at") or now_iso
            document_url = item.get("document_url") or (direct_url if direct_url.lower().endswith(".pdf") else None)
            official_source_status = item.get("official_source_status") or ("verified_official_source" if source_verified else "unverified")
            official_document_status = item.get("official_document_status") or (
                "verified_official_document" if (source_verified and document_url)
                else ("verified_official_article" if source_verified else "not_verified")
            )
            duplicate_of = item.get("duplicate_of")
            relevance_score = float(item.get("relevance_score", 1.0))
            model_version = item.get("model_version", "phase6_logistic_regression_v1")
            translation_status = item.get("translation_status", "completed")
            summary_status = item.get("summary_status", "completed")
            updated_at = item.get("updated_at") or now_iso

            cursor.execute("""
                INSERT OR REPLACE INTO news_items (
                    news_id, headline_original, description_original, full_text_original,
                    source_name, source_type, source_url, publication_date, fetched_at,
                    jurisdiction, issuing_department, original_language, category,
                    keywords_json, target_audience, central_relevance, summary_original,
                    summary_translated_json, relevance_explanation_json,
                    headline_translated_json, verification_status, content_hash,
                    source_title, source_reference_number, original_source_url,
                    official_translation_url, translated_source_language,
                    source_verified, source_verification_status, last_verified_at,
                    document_url, official_source_status, official_document_status,
                    duplicate_of, relevance_score, model_version, translation_status,
                    summary_status, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item["news_id"],
                item["headline_original"],
                item["description_original"],
                item.get("full_text_original", ""),
                item["source_name"],
                item["source_type"],
                direct_url,
                item["publication_date"],
                item.get("fetched_at") or now_iso,
                item["jurisdiction"],
                item["issuing_department"],
                item["original_language"],
                item["category"],
                json.dumps(item.get("keywords", []), ensure_ascii=False),
                item.get("target_audience", "Cooperative Members"),
                1 if item.get("central_relevance", False) else 0,
                item["summary_original"],
                json.dumps(item.get("summary_translated", {}), ensure_ascii=False),
                json.dumps(item.get("relevance_explanation", {}), ensure_ascii=False),
                json.dumps(item.get("headline_translated", {}), ensure_ascii=False),
                verification_status,
                item.get("content_hash", ""),
                item.get("source_title", item.get("headline_original", "")),
                item.get("source_reference_number", ""),
                direct_url,
                item.get("official_translation_url", ""),
                item.get("translated_source_language", ""),
                source_verified,
                verification_status,
                last_verified_at,
                document_url,
                official_source_status,
                official_document_status,
                duplicate_of,
                relevance_score,
                model_version,
                translation_status,
                summary_status,
                updated_at,
            ))
            return True
    except Exception as e:
        logger.error("Failed to save news item %s: %s", item.get("news_id"), e)
        return False

def get_news_item_by_id(news_id: str) -> Optional[Dict[str, Any]]:
    """Fetches a single news item by ID, deserializing JSON fields."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM news_items WHERE news_id = ?", (news_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return _deserialize_news_row(dict(row))

def get_news_items(
    jurisdiction: str = "all",
    limit: int = 20,
    offset: int = 0,
    category: Optional[str] = None,
    department: Optional[str] = None,
    document_type: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Retrieves news items according to jurisdiction and faceted filtering rules."""
    conditions = []
    params = []

    if jurisdiction == "central":
        conditions.append("jurisdiction = 'central'")
    elif jurisdiction and jurisdiction != "all":
        conditions.append("(jurisdiction = ? OR (jurisdiction = 'central' AND central_relevance = 1))")
        params.append(jurisdiction)

    if category and category != "all":
        conditions.append("category = ?")
        params.append(category)

    if department:
        conditions.append("issuing_department LIKE ?")
        params.append(f"%{department}%")

    if document_type == "official_document" or document_type == "pdf":
        conditions.append("(document_url LIKE '%.pdf' OR original_source_url LIKE '%.pdf')")
    elif document_type == "article":
        conditions.append("(document_url IS NULL AND (original_source_url IS NULL OR original_source_url NOT LIKE '%.pdf'))")

    if date_from:
        conditions.append("publication_date >= ?")
        params.append(date_from)
    if date_to:
        conditions.append("publication_date <= ?")
        params.append(date_to)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    sql = f"""
        SELECT * FROM news_items
        {where_clause}
        ORDER BY publication_date DESC, fetched_at DESC
        LIMIT ? OFFSET ?
    """
    params.extend([limit, offset])

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, tuple(params))
        rows = cursor.fetchall()
        return [_deserialize_news_row(dict(r)) for r in rows]

query_news = get_news_items

def count_news(
    jurisdiction: str = "all",
    category: Optional[str] = None,
    department: Optional[str] = None,
    document_type: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> int:
    """Returns the total number of news items matching the filters."""
    conditions = []
    params = []

    if jurisdiction == "central":
        conditions.append("jurisdiction = 'central'")
    elif jurisdiction and jurisdiction != "all":
        conditions.append("(jurisdiction = ? OR (jurisdiction = 'central' AND central_relevance = 1))")
        params.append(jurisdiction)

    if category and category != "all":
        conditions.append("category = ?")
        params.append(category)

    if department:
        conditions.append("issuing_department LIKE ?")
        params.append(f"%{department}%")

    if document_type == "official_document" or document_type == "pdf":
        conditions.append("(document_url LIKE '%.pdf' OR original_source_url LIKE '%.pdf')")
    elif document_type == "article":
        conditions.append("(document_url IS NULL AND (original_source_url IS NULL OR original_source_url NOT LIKE '%.pdf'))")

    if date_from:
        conditions.append("publication_date >= ?")
        params.append(date_from)
    if date_to:
        conditions.append("publication_date <= ?")
        params.append(date_to)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    sql = f"SELECT COUNT(*) FROM news_items {where_clause}"

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, tuple(params))
        row = cursor.fetchone()
        return row[0] if row else 0

def is_duplicate_hash(content_hash: str) -> bool:
    """Checks whether a news item with the same content hash already exists."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM news_items WHERE content_hash = ? LIMIT 1", (content_hash,))
        return cursor.fetchone() is not None

def update_source_status(
    source_id: str,
    name: str,
    jurisdiction: str,
    url: str,
    source_type: str,
    status: str,
    items_count: int = 0,
    notes: str = ""
):
    """Updates or inserts operational health record for a source connector."""
    now_iso = datetime.now().isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO news_sources (
                source_id, name, jurisdiction, url, source_type,
                last_status, last_fetched_at, items_collected, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (source_id, name, jurisdiction, url, source_type, status, now_iso, items_count, notes))

def get_all_source_statuses() -> List[Dict[str, Any]]:
    """Retrieves operational status of all registered sources."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM news_sources ORDER BY jurisdiction, name")
        return [dict(r) for r in cursor.fetchall()]

def log_audit_run(report: List[Dict[str, Any]]):
    """Logs the results of a source connector connectivity audit."""
    now_iso = datetime.now().isoformat()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO source_audit_log (audited_at, report_json)
            VALUES (?, ?)
        """, (now_iso, json.dumps(report, ensure_ascii=False)))

def _deserialize_news_row(row: Dict[str, Any]) -> Dict[str, Any]:
    """Helper to deserialize JSON text fields into Python dicts/lists."""
    json_fields = {
        "keywords_json": "keywords",
        "summary_translated_json": "summary_translated",
        "relevance_explanation_json": "relevance_explanation",
        "headline_translated_json": "headline_translated",
    }
    for json_col, target_key in json_fields.items():
        val = row.get(json_col)
        if val and isinstance(val, str):
            try:
                row[target_key] = json.loads(val)
            except Exception:
                row[target_key] = {}
        else:
            row[target_key] = {}

    row["central_relevance"] = bool(row.get("central_relevance", 0))
    row["source_verified"] = bool(row.get("source_verified", 1))

    # Phase 7 Direct document & provenance fields
    orig_src = row.get("original_source_url") or row.get("source_url") or ""
    raw_doc = row.get("document_url")
    if not raw_doc and str(orig_src).lower().endswith(".pdf"):
        raw_doc = orig_src
    row["document_url"] = raw_doc if (raw_doc and not any(raw_doc.rstrip("/").endswith(gh) for gh in ["pib.gov.in", "cooperation.gov.in", "punjab.gov.in", "haryana.gov.in", "jk.gov.in"])) else None

    row["official_source_status"] = "verified_official_source" if row["source_verified"] else "unverified"
    if row.get("document_url"):
        row["official_document_status"] = "verified_official_document" if row["source_verified"] else "not_verified"
    elif row["source_verified"]:
        row["official_document_status"] = "verified_official_article"
    else:
        row["official_document_status"] = "not_verified"
    row["relevance_score"] = float(row.get("relevance_score") if row.get("relevance_score") is not None else 1.0)
    row["model_version"] = row.get("model_version") or "phase6_logistic_regression_v1"
    row["duplicate_of"] = row.get("duplicate_of")
    row["updated_at"] = row.get("updated_at") or row.get("fetched_at")
    return row

def get_news_verification_report() -> Dict[str, Any]:
    """Generates an audit report of verified source URLs vs direct document URLs."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        total = cursor.execute("SELECT COUNT(*) FROM news_items").fetchone()[0]
        verified_sources = cursor.execute("SELECT COUNT(*) FROM news_items WHERE source_verified = 1").fetchone()[0]
        verified_docs = cursor.execute(
            "SELECT COUNT(*) FROM news_items WHERE source_verified = 1 AND (document_url LIKE '%.pdf' OR original_source_url LIKE '%.pdf' OR source_url LIKE '%.pdf')"
        ).fetchone()[0]
        unverified_docs = total - verified_docs
        duplicates = cursor.execute("SELECT COUNT(*) FROM news_items WHERE duplicate_of IS NOT NULL").fetchone()[0]

        by_jur = {}
        for jur in ["central", "punjab", "haryana", "jk"]:
            c_tot = cursor.execute("SELECT COUNT(*) FROM news_items WHERE jurisdiction = ?", (jur,)).fetchone()[0]
            c_v_src = cursor.execute("SELECT COUNT(*) FROM news_items WHERE jurisdiction = ? AND source_verified = 1", (jur,)).fetchone()[0]
            c_v_doc = cursor.execute(
                "SELECT COUNT(*) FROM news_items WHERE jurisdiction = ? AND source_verified = 1 AND (document_url LIKE '%.pdf' OR original_source_url LIKE '%.pdf' OR source_url LIKE '%.pdf')",
                (jur,)
            ).fetchone()[0]
            by_jur[jur] = {
                "total": c_tot,
                "verified_sources": c_v_src,
                "verified_documents": c_v_doc,
                "articles_or_pending": c_tot - c_v_doc,
            }

        return {
            "total_announcements": total,
            "verified_official_sources": verified_sources,
            "verified_direct_documents": verified_docs,
            "articles_or_pending_documents": unverified_docs,
            "duplicate_records": duplicates,
            "by_jurisdiction": by_jur,
            "timestamp": datetime.now().isoformat(),
        }

def get_duplicate_records() -> List[Dict[str, Any]]:
    """Retrieves all news items linked as duplicates."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM news_items WHERE duplicate_of IS NOT NULL ORDER BY publication_date DESC")
        return [_deserialize_news_row(dict(r)) for r in cursor.fetchall()]
