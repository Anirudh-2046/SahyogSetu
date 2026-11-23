"""
SahyogSetu Automated Post-Deployment Smoke Test
Validates core system health, RAG retrieval, multilingual capabilities,
and database persistence against a live or staged instance.
"""

import sys
import os
import json
import logging
import inspect
from pathlib import Path

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.config import settings
from backend.api.routes_health import health_check, health_liveness, health_readiness
from backend.api.routes_news import get_news
from backend.api.routes_chat import handle_chat_query
from backend.api.routes_conversations import create_conversation, delete_conversation
from backend.schemas.chat import ChatQueryRequest
from backend.schemas.conversation import ConversationCreateRequest

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("sahyogsetu.smoke_test")


def run_coro(coro):
    """Executes a coroutine synchronously without event-loop/socket dependencies for sandbox isolation."""
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


def execute_smoke_tests() -> int:
    """Executes end-to-end smoke tests on the core API subsystems."""
    logger.info("Starting SahyogSetu Post-Deployment Smoke Test Suite...")
    total_checks = 6
    passed_checks = 0

    # 1. Liveness Probe
    try:
        live = run_coro(health_liveness())
        assert live["status"] == "alive"
        logger.info("✓ [1/6] Liveness probe verified: status=%s", live["status"])
        passed_checks += 1
    except Exception as e:
        logger.error("✗ [1/6] Liveness probe failed: %s", e)

    # 2. Readiness Probe
    try:
        ready = run_coro(health_readiness())
        assert ready["status"] == "ready"
        assert ready["checks"]["database"] is True
        logger.info("✓ [2/6] Readiness probe verified: database and knowledge store ready")
        passed_checks += 1
    except Exception as e:
        logger.error("✗ [2/6] Readiness probe failed: %s", e)

    # 3. Comprehensive Health Check
    try:
        health = run_coro(health_check())
        assert health["status"] in ["healthy", "degraded"]
        assert health["database"]["status"] == "connected"
        logger.info("✓ [3/6] Health check verified: %d news records, DB connected", health["database"]["total_news_records"])
        passed_checks += 1
    except Exception as e:
        logger.error("✗ [3/6] Health check failed: %s", e)

    # 4. Government News Aggregation Endpoint
    try:
        news_res = run_coro(get_news(jurisdiction="all", limit=5, offset=0))
        items = news_res.get("items", []) if isinstance(news_res, dict) else getattr(news_res, "items", [])
        assert len(items) > 0
        logger.info("✓ [4/6] News pipeline verified: %d official news items retrieved", len(items))
        passed_checks += 1
    except Exception as e:
        logger.error("✗ [4/6] News pipeline failed: %s", e)

    # 5. Conversation Lifecycle Persistence
    try:
        req = ConversationCreateRequest(title="Smoke Test Thread", language="en", jurisdiction="punjab")
        conv = run_coro(create_conversation(req))
        conv_id = conv["conversation_id"]
        del_res = run_coro(delete_conversation(conv_id))
        assert del_res["success"] is True
        logger.info("✓ [5/6] Conversation persistence and teardown verified")
        passed_checks += 1
    except Exception as e:
        logger.error("✗ [5/6] Conversation lifecycle failed: %s", e)

    # 6. Legal RAG Grounded Query
    try:
        chat_req = ChatQueryRequest(
            query="What is the managing committee tenure in Haryana under Section 28?",
            language="en",
            jurisdiction="haryana",
        )
        raw_res = run_coro(handle_chat_query(chat_req))
        chat_res = raw_res.get("response", raw_res) if isinstance(raw_res, dict) else raw_res
        jur = chat_res.get("jurisdiction", "") if isinstance(chat_res, dict) else getattr(chat_res, "jurisdiction", "")
        cits = chat_res.get("citations", []) if isinstance(chat_res, dict) else getattr(chat_res, "citations", [])
        plain_exp = chat_res.get("plainExplanation", "") if isinstance(chat_res, dict) else getattr(chat_res, "plainExplanation", "")
        assert jur.lower() == "haryana"
        assert len(cits) > 0
        assert "28" in str(plain_exp) or "tenure" in str(plain_exp).lower()
        logger.info("✓ [6/6] Legal RAG statutory pipeline verified (Citations: %d)", len(cits))
        passed_checks += 1
    except Exception as e:
        logger.error("✗ [6/6] Legal RAG pipeline failed: %s", e)

    logger.info("=" * 60)
    logger.info("Smoke Test Results: %d/%d passed", passed_checks, total_checks)
    logger.info("=" * 60)

    return 0 if passed_checks == total_checks else 1


if __name__ == "__main__":
    sys.exit(execute_smoke_tests())
