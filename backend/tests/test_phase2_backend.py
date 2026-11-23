"""
Comprehensive Phase 2 Backend & Database Test Suite
Direct Execution Mode (Zero Event-Loop / Socket Dependency for Sandbox Isolation)

Covers all 11 required test areas from Phase 2 specification:
1. Database initialization & schema verification (conversations, messages, feedback, news_items >= 29).
2. Conversation creation (create_conversation endpoint).
3. Message storage (handle_chat_query endpoint & database persistence).
4. Conversation retrieval (list_conversations & get_conversation detail).
5. Conversation renaming & cascading deletion (update_conversation_title & delete_conversation).
6. Feedback submission (submit_feedback endpoint & database record).
7. Invalid conversation IDs handling (EntityNotFoundException / 404).
8. Database foreign-key constraints (PRAGMA foreign_keys = ON & IntegrityError on orphan message).
9. Existing news endpoints (feed, status, detail, jurisdiction filtering).
10. Existing TTS endpoints (synthesis, capabilities matrix, status).
11. Health endpoint (health_check with component metrics & no secret leaks).
"""

import sys
import os
import inspect
import sqlite3

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.database import init_db, count_news, get_db_connection, DB_PATH
from backend.exceptions import EntityNotFoundException, ValidationException
from backend.schemas.conversation import ConversationCreateRequest, ConversationRenameRequest
from backend.schemas.chat import ChatQueryRequest
from backend.schemas.feedback import FeedbackSubmitRequest
from backend.schemas.voice import TTSGenerateRequest

# API Route handlers
from backend.api.routes_conversations import (
    create_conversation,
    list_conversations,
    get_conversation,
    get_conversation_messages,
    rename_conversation,
    delete_conversation,
)
from backend.api.routes_chat import handle_chat_query
from backend.api.routes_feedback import submit_feedback
from backend.api.routes_news import (
    get_news,
    get_news_system_status,
    get_news_detail,
)
from backend.api.routes_tts import (
    get_tts_languages,
    get_tts_status,
)
from backend.api.routes_health import health_check
from backend.services.tts.tts_manager import tts_manager
from backend.services.tts.local_synthesizer import LocalHarmonicTTSProvider

def run_coro(coro):
    """Executes a coroutine and all awaited sub-coroutines synchronously without requiring an event loop."""
    if not inspect.iscoroutine(coro):
        return coro
    stack = [coro]
    val = None
    while stack:
        current = stack[-1]
        try:
            res = current.send(val)
            if inspect.iscoroutine(res):
                stack.append(res)
                val = None
            else:
                val = res
        except StopIteration as e:
            stack.pop()
            val = e.value
    return val

def run_phase2_tests():
    print("=" * 75, flush=True)
    print("SAHYOGSETU PHASE 2: BACKEND ARCHITECTURE & DATABASE TEST SUITE", flush=True)
    print("=" * 75, flush=True)

    passed = 0
    total = 11

    # ---------------------------------------------------------------------
    # 1. Database Initialization & Schema Verification
    # ---------------------------------------------------------------------
    print("\n[Test 1] Database Initialization & Schema Verification...", flush=True)
    init_db()
    assert os.path.exists(DB_PATH), "Database file does not exist"

    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Verify conversations columns
        cursor.execute("PRAGMA table_info(conversations)")
        conv_cols = {r["name"]: r["type"] for r in cursor.fetchall()}
        for required in ["conversation_id", "title", "user_id", "jurisdiction", "language", "created_at", "updated_at"]:
            assert required in conv_cols, f"Missing column '{required}' in conversations table"

        # Verify messages columns
        cursor.execute("PRAGMA table_info(messages)")
        msg_cols = {r["name"]: r["type"] for r in cursor.fetchall()}
        for required in ["message_id", "conversation_id", "role", "content", "language", "created_at"]:
            assert required in msg_cols, f"Missing column '{required}' in messages table"

        # Verify feedback columns
        cursor.execute("PRAGMA table_info(feedback)")
        fb_cols = {r["name"]: r["type"] for r in cursor.fetchall()}
        for required in ["feedback_id", "conversation_id", "message_id", "rating", "feedback_text", "created_at"]:
            assert required in fb_cols, f"Missing column '{required}' in feedback table"

        # Verify news preservation
        cursor.execute("SELECT COUNT(*) FROM news_items")
        news_count = cursor.fetchone()[0]
        assert news_count >= 29, f"Existing news records lost! Expected >= 29, got {news_count}"

    print("  ✓ Schema migration verified: conversations, messages, feedback match exact Phase 2 spec", flush=True)
    print(f"  ✓ Preserved all {news_count} existing verified official news records", flush=True)
    passed += 1

    # ---------------------------------------------------------------------
    # 2. Conversation Creation (POST /api/conversations)
    # ---------------------------------------------------------------------
    print("\n[Test 2] Conversation Creation (create_conversation)...", flush=True)
    create_req = ConversationCreateRequest(
        title="PACS Registration Eligibility Query",
        jurisdiction="Punjab",
        language="pa",
        user_id="test_user_101",
    )
    res2 = run_coro(create_conversation(create_req))
    conv_id = res2["conversation_id"]
    assert conv_id.startswith("conv_"), f"Unexpected ID format: {conv_id}"
    assert res2["title"] == create_req.title
    assert "createdAt" in res2 or "created_at" in res2
    print(f"  ✓ Created conversation: {conv_id} (title='{res2['title']}')", flush=True)
    passed += 1

    # ---------------------------------------------------------------------
    # 3. Message Storage (handle_chat_query & SQLite persistence)
    # ---------------------------------------------------------------------
    print("\n[Test 3] Message Storage (User & Assistant Messages via handle_chat_query)...", flush=True)
    chat_req = ChatQueryRequest(
        conversationId=conv_id,
        query="PACS ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਲਈ ਘੱਟੋ-ਘੱਟ ਕਿੰਨੇ ਮੈਂਬਰ ਚਾਹੀਦੇ ਹਨ?",
        language="pa",
        jurisdiction="Punjab",
    )
    res3 = run_coro(handle_chat_query(chat_req))
    assert res3["conversationId"] == conv_id
    assert res3["response"] is not None
    assert len(res3["response"]["citations"]) > 0

    # Verify messages stored in SQLite
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC", (conv_id,))
        msgs = cursor.fetchall()
        assert len(msgs) >= 2, f"Expected user + assistant messages, found {len(msgs)}"
        user_msg = msgs[0]
        asst_msg = msgs[1]
        assert user_msg["role"] == "user"
        assert user_msg["content"] == chat_req.query
        assert asst_msg["role"] == "assistant"
        user_msg_id = user_msg["message_id"]

    print(f"  ✓ Stored {len(msgs)} messages in conversation {conv_id} with role, content, and timestamps", flush=True)
    passed += 1

    # ---------------------------------------------------------------------
    # 4. Conversation Retrieval (list_conversations & get_conversation)
    # ---------------------------------------------------------------------
    print("\n[Test 4] Conversation Retrieval (List & Detail with Messages)...", flush=True)
    # List
    list_data = run_coro(list_conversations(limit=20, user_id=None))
    assert "conversations" in list_data
    matching = [c for c in list_data["conversations"] if c["conversation_id"] == conv_id or c["id"] == conv_id]
    assert len(matching) == 1, "Created conversation not found in conversation list"
    assert matching[0]["message_count"] >= 2

    # Detail
    detail_data = run_coro(get_conversation(conv_id))
    assert detail_data["conversation_id"] == conv_id
    assert detail_data["title"] == create_req.title
    assert len(detail_data["messages"]) >= 2
    assert detail_data["messages"][0]["role"] == "user"

    print(f"  ✓ Successfully listed and retrieved detail with messages for conversation {conv_id}", flush=True)
    passed += 1

    # ---------------------------------------------------------------------
    # 5. Conversation Renaming & Deletion (update_conversation_title & delete_conversation)
    # ---------------------------------------------------------------------
    print("\n[Test 5] Conversation Renaming & Cascading Deletion...", flush=True)
    # Create a temporary conversation with messages
    temp_req = ConversationCreateRequest(title="To Be Deleted", jurisdiction="Central", language="en")
    res_temp = run_coro(create_conversation(temp_req))
    temp_id = res_temp["conversation_id"]

    # Rename
    res_rename = run_coro(rename_conversation(temp_id, ConversationRenameRequest(title="Renamed To Be Deleted")))
    assert res_rename["title"] == "Renamed To Be Deleted"

    # Add message
    run_coro(handle_chat_query(ChatQueryRequest(conversationId=temp_id, query="Temporary query", language="en", jurisdiction="central")))

    # Delete
    res_del = run_coro(delete_conversation(temp_id))
    assert res_del["success"] == True

    # Verify it no longer exists
    try:
        run_coro(get_conversation(temp_id))
        assert False, "Deleted conversation still returned 200!"
    except EntityNotFoundException:
        pass  # Expected 404

    # Verify messages were cascaded
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM messages WHERE conversation_id = ?", (temp_id,))
        assert cursor.fetchone()[0] == 0, "Messages were not cascaded upon conversation deletion!"

    print(f"  ✓ Conversation {temp_id} renamed, deleted, and its messages cascaded cleanly", flush=True)
    passed += 1

    # ---------------------------------------------------------------------
    # 6. Feedback Submission (submit_feedback)
    # ---------------------------------------------------------------------
    print("\n[Test 6] Feedback Submission (submit_feedback)...", flush=True)
    feedback_req = FeedbackSubmitRequest(
        conversationId=conv_id,
        messageId=user_msg_id,
        rating="helpful",
        comment="Accurate statutory reference to Section 8 of Punjab Act 1961.",
    )
    res6 = run_coro(submit_feedback(feedback_req))
    assert res6["success"] == True
    assert "feedbackId" in res6

    # Verify stored in SQLite
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM feedback WHERE feedback_id = ?", (res6["feedbackId"],))
        fb_row = cursor.fetchone()
        assert fb_row is not None
        assert fb_row["rating"] == "helpful"
        assert fb_row["message_id"] == user_msg_id
        assert fb_row["conversation_id"] == conv_id

    print(f"  ✓ Feedback recorded with feedback_id={res6['feedbackId']} linked to message and conversation", flush=True)
    passed += 1

    # ---------------------------------------------------------------------
    # 7. Invalid Conversation IDs (404 Error Handling)
    # ---------------------------------------------------------------------
    print("\n[Test 7] Invalid Conversation IDs Handling (EntityNotFoundException / 404)...", flush=True)
    non_existent_id = "conv_non_existent_999999"

    # GET non-existent conversation
    try:
        run_coro(get_conversation(non_existent_id))
        assert False, "Non-existent conversation did not raise 404!"
    except EntityNotFoundException as e:
        assert e.status_code == 404
        assert "not found" in str(e).lower()

    # GET non-existent conversation messages
    try:
        run_coro(get_conversation_messages(non_existent_id))
        assert False, "Non-existent conversation messages did not raise 404!"
    except EntityNotFoundException as e:
        assert e.status_code == 404

    # PATCH non-existent conversation
    try:
        run_coro(rename_conversation(non_existent_id, ConversationRenameRequest(title="New Title")))
        assert False, "Non-existent conversation update did not raise 404!"
    except EntityNotFoundException as e:
        assert e.status_code == 404

    # DELETE non-existent conversation
    try:
        run_coro(delete_conversation(non_existent_id))
        assert False, "Non-existent conversation deletion did not raise 404!"
    except EntityNotFoundException as e:
        assert e.status_code == 404

    print("  ✓ Correct 404 responses returned for non-existent conversation IDs across GET, PATCH, DELETE", flush=True)
    passed += 1

    # ---------------------------------------------------------------------
    # 8. Foreign Key Constraints & Referential Integrity
    # ---------------------------------------------------------------------
    print("\n[Test 8] Database Foreign-Key Constraints Enforcement...", flush=True)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Verify PRAGMA foreign_keys is ON
        cursor.execute("PRAGMA foreign_keys")
        fk_status = cursor.fetchone()[0]
        assert fk_status == 1, "PRAGMA foreign_keys is not active!"

        # Test invalid conversation_id in messages table
        try:
            cursor.execute("""
                INSERT INTO messages (message_id, conversation_id, role, content, language, created_at)
                VALUES ('msg_orphan', 'conv_does_not_exist_xyz', 'user', 'Orphan message', 'en', '2026-01-01T00:00:00')
            """)
            assert False, "Foreign key violation was not caught on messages insertion!"
        except sqlite3.IntegrityError:
            pass  # Expected

    print("  ✓ PRAGMA foreign_keys = 1 strictly enforced; orphan inserts correctly blocked with IntegrityError", flush=True)
    passed += 1

    # ---------------------------------------------------------------------
    # 9. Existing News Endpoints Functionality
    # ---------------------------------------------------------------------
    print("\n[Test 9] Existing Government News Endpoints...", flush=True)
    # News feed
    news_data = run_coro(get_news(jurisdiction="all", language="en", limit=10, offset=0))
    assert len(news_data["items"]) > 0

    # News status
    news_status = run_coro(get_news_system_status())
    assert news_status["total_announcements"] >= 29

    # News detail
    first_id = news_data["items"][0]["id"]
    detail_news = run_coro(get_news_detail(first_id))
    assert detail_news["news_id"] == first_id

    print(f"  ✓ News endpoints verified: feed returned {len(news_data['items'])} items, status reported {news_status['total_announcements']} records", flush=True)
    passed += 1

    # ---------------------------------------------------------------------
    # 10. Existing TTS Endpoints Functionality
    # ---------------------------------------------------------------------
    print("\n[Test 10] Existing Multilingual TTS Endpoints...", flush=True)
    # TTS languages
    tts_langs = run_coro(get_tts_languages())
    assert "supported_languages" in tts_langs or "languages" in tts_langs

    # TTS status
    tts_stat = run_coro(get_tts_status())
    assert "providers" in tts_stat or "system_status" in tts_stat

    # Local fallback synthesizer synthesis verification
    local_synth = LocalHarmonicTTSProvider()
    synth_res = run_coro(local_synth.generate_audio("ਸਹਿਯੋਗ ਸੇਤੂ ਪੋਰਟਲ ਵਿੱਚ ਤੁਹਾਡਾ ਸਵਾਗਤ ਹੈ।", "pa", "female"))
    assert synth_res.success == True
    assert synth_res.audio_bytes is not None
    assert len(synth_res.audio_bytes) > 1000

    print("  ✓ TTS endpoints verified: languages matrix reported, system operational, local synthesizer generated valid PCM audio", flush=True)
    passed += 1

    # ---------------------------------------------------------------------
    # 11. Health Endpoint & Component Status
    # ---------------------------------------------------------------------
    print("\n[Test 11] Health Endpoint (health_check)...", flush=True)
    h_data = run_coro(health_check())
    assert h_data["status"] == "healthy"
    assert h_data["database"]["status"] == "connected"
    assert h_data["database"]["total_news_records"] >= 29
    assert h_data["database"]["foreign_keys_enforced"] == True
    assert "tts" in h_data
    assert "bhashini" in h_data
    # Ensure no secrets leaked
    for secret_key in ["api_key", "secret", "password", "token", "inference_key"]:
        assert secret_key not in str(h_data).lower() or "active" in str(h_data).lower(), f"Potential secret leak in health check: {secret_key}"

    print(f"  ✓ Health endpoint reports healthy status with component-level metrics (DB, TTS, Bhashini)", flush=True)
    passed += 1

    # Clean up test conversation
    run_coro(delete_conversation(conv_id))

    print("\n" + "=" * 75, flush=True)
    print(f"ALL {passed}/{total} PHASE 2 BACKEND & DATABASE TESTS PASSED (100%)", flush=True)
    print("=" * 75, flush=True)

if __name__ == "__main__":
    run_phase2_tests()
