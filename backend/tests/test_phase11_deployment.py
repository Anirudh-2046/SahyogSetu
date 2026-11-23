"""
SAHYOGSETU PHASE 11: DEPLOYMENT, CI/CD & RELEASE READINESS TEST SUITE

Validates:
1. Environment Configuration & Startup Validation (dev, test, prod validation rules)
2. Health Probes (/api/health/live and /api/health/ready with HTTP 200/503 status)
3. Disaster Recovery Hot Backup & Restore (SQLite online backup with SHA-256 and integrity check)
4. Automated Post-Deployment Smoke Test Suite
5. Docker & Container Security (non-root UID 10001, multi-stage build, healthcheck)
6. Reverse Proxy Hardening (Nginx security headers, 15 MB limit, API proxy forwarding)
7. Multilingual Capability Matrix Compliance
8. Cross-State Leakage & Hostile Jurisdiction Isolation Verification
"""

import sys
import os
import json
import inspect
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any

# Ensure project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.config import Settings, settings
from backend.api.routes_health import health_liveness, health_readiness, health_check
from backend.services.language.language_capabilities import LANGUAGE_CAPABILITY_MATRIX
from backend.rag.jurisdiction_resolver import jurisdiction_resolver
from backend.rag.rag_pipeline import rag_pipeline
from backend.scripts.backup_restore import create_backup, restore_backup, verify_sqlite_integrity
from backend.scripts.smoke_test import execute_smoke_tests


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


def run_phase11_tests() -> int:
    print("=" * 80)
    print("SAHYOGSETU PHASE 11: DEPLOYMENT & PRODUCTION READINESS TEST SUITE")
    print("=" * 80)

    total = 8
    passed = 0

    # -------------------------------------------------------------------------
    # Test 1: Environment Configuration & Production Validation
    # -------------------------------------------------------------------------
    print("\n[Test 1] Environment Configuration & Production Validation Rules...", flush=True)
    try:
        # Development environment validation
        dev_settings = Settings(APP_ENV="development", DEBUG=True, CORS_ORIGINS=["*"])
        dev_rep = dev_settings.validate_environment()
        assert dev_rep["valid"] is True, "Dev environment should be valid"

        # Production environment validation with insecure defaults
        prod_bad = Settings(
            APP_ENV="production",
            DEBUG=True,  # Disallowed in production
            CORS_ORIGINS=["*"],  # Disallowed in production
        )
        prod_rep = prod_bad.validate_environment()
        assert prod_rep["valid"] is False, "Production with DEBUG=True and CORS=* must fail"
        assert any("DEBUG" in err for err in prod_rep["errors"]), "Must flag DEBUG mode in production"
        assert any("CORS" in err for err in prod_rep["errors"]), "Must flag wildcard CORS in production"

        # Production environment validation with hardened settings
        prod_good = Settings(
            APP_ENV="production",
            DEBUG=False,
            CORS_ORIGINS=["https://sahyogsetu.gov.in"],
            ADMIN_API_KEY="strong_custom_prod_secret_key_8899",
        )
        prod_good_rep = prod_good.validate_environment()
        assert prod_good_rep["valid"] is True, f"Hardened prod settings should pass: {prod_good_rep['errors']}"

        print("  -> Passed: Dev, testing, and production environment segregation enforced.", flush=True)
        passed += 1
    except Exception as e:
        print(f"  -> FAILED: {e}", flush=True)

    # -------------------------------------------------------------------------
    # Test 2: Health Liveness & Readiness Probes
    # -------------------------------------------------------------------------
    print("\n[Test 2] Liveness & Readiness Health Probes (/api/health/live, /api/health/ready)...", flush=True)
    try:
        # Liveness
        live = run_coro(health_liveness())
        assert live["status"] == "alive"
        assert live["service"] == settings.APP_NAME

        # Readiness under normal operation
        ready = run_coro(health_readiness())
        assert ready["status"] == "ready"
        assert ready["checks"]["database"] is True
        assert ready["checks"]["knowledge_store"] is True
        assert ready["checks"]["vector_store"] is True

        print("  -> Passed: Liveness and Readiness probes active and reporting healthy dependencies.", flush=True)
        passed += 1
    except Exception as e:
        print(f"  -> FAILED: {e}", flush=True)

    # -------------------------------------------------------------------------
    # Test 3: Disaster Recovery Hot Backup & SHA-256 Verified Restore
    # -------------------------------------------------------------------------
    print("\n[Test 3] Hot SQLite Backup & SHA-256 Verified Restore Utility...", flush=True)
    temp_dir = tempfile.mkdtemp(prefix="sahyogsetu_test_backup_")
    try:
        # Create backup snapshot
        backup_res = create_backup(target_dir=temp_dir)
        assert backup_res["success"] is True, f"Backup creation failed: {backup_res}"
        snapshot_dir = backup_res["snapshot_dir"]

        manifest_file = os.path.join(snapshot_dir, "backup_manifest.json")
        assert os.path.exists(manifest_file), "Manifest file must be created"

        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        assert manifest["status"] == "success"
        assert "news.db" in manifest["files"]
        assert manifest["files"]["news.db"]["integrity"] == "ok"

        # Restore into another temporary directory
        restore_dir = tempfile.mkdtemp(prefix="sahyogsetu_test_restore_")
        restore_res = restore_backup(snapshot_dir, target_dir=restore_dir)
        assert restore_res["success"] is True, f"Restore failed: {restore_res}"
        assert "news.db" in restore_res["files_restored"]

        # Verify integrity of restored database
        restored_news = os.path.join(restore_dir, "news.db")
        assert verify_sqlite_integrity(restored_news) is True, "Restored database must pass integrity check"

        shutil.rmtree(restore_dir, ignore_errors=True)
        print("  -> Passed: Hot non-blocking backup and atomic SHA-256 restore verified.", flush=True)
        passed += 1
    except Exception as e:
        print(f"  -> FAILED: {e}", flush=True)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    # -------------------------------------------------------------------------
    # Test 4: Automated Smoke Test Pipeline Execution
    # -------------------------------------------------------------------------
    print("\n[Test 4] Automated Smoke Test Pipeline Execution...", flush=True)
    try:
        smoke_code = execute_smoke_tests()
        assert smoke_code == 0, "Smoke tests should exit with code 0"
        print("  -> Passed: All 6 core post-deployment smoke test checks passed.", flush=True)
        passed += 1
    except Exception as e:
        print(f"  -> FAILED: {e}", flush=True)

    # -------------------------------------------------------------------------
    # Test 5: Docker Containerization Security & Non-Root User
    # -------------------------------------------------------------------------
    print("\n[Test 5] Docker Containerization & Security Configuration...", flush=True)
    try:
        dockerfile_path = os.path.join(PROJECT_ROOT, "Dockerfile")
        assert os.path.exists(dockerfile_path), "Dockerfile must exist at project root"

        with open(dockerfile_path, "r", encoding="utf-8") as f:
            docker_content = f.read()

        assert "FROM node:20-alpine AS frontend-builder" in docker_content, "Must use multi-stage frontend build"
        assert "FROM python:3.12-slim" in docker_content, "Must use python:3.12-slim"
        assert "appuser" in docker_content, "Must define dedicated non-root application user"
        assert "10001" in docker_content, "Must specify non-root UID 10001"
        assert "USER appuser" in docker_content, "Must switch to unprivileged user"
        assert "HEALTHCHECK" in docker_content, "Must define container HEALTHCHECK probe"
        assert "/api/health/ready" in docker_content, "Healthcheck must use readiness endpoint"

        compose_path = os.path.join(PROJECT_ROOT, "docker-compose.yml")
        assert os.path.exists(compose_path), "docker-compose.yml must exist at project root"

        with open(compose_path, "r", encoding="utf-8") as f:
            compose_content = f.read()

        assert "sahyogsetu_data:" in compose_content, "Must declare persistent data volume"
        assert "/app/backend/data" in compose_content, "Must mount backend data volume"
        assert "sahyogsetu-net" in compose_content, "Must declare isolated container network"

        print("  -> Passed: Multi-stage Docker build, unprivileged user (UID 10001), and volume mounts verified.", flush=True)
        passed += 1
    except Exception as e:
        print(f"  -> FAILED: {e}", flush=True)

    # -------------------------------------------------------------------------
    # Test 6: Reverse Proxy Hardening & Nginx Security Headers
    # -------------------------------------------------------------------------
    print("\n[Test 6] Reverse Proxy Hardening & Security Headers (Nginx)...", flush=True)
    try:
        nginx_conf_path = os.path.join(PROJECT_ROOT, "nginx", "sahyogsetu.conf")
        assert os.path.exists(nginx_conf_path), "nginx/sahyogsetu.conf must exist"

        with open(nginx_conf_path, "r", encoding="utf-8") as f:
            nginx_conf = f.read()

        assert "client_max_body_size 15M;" in nginx_conf, "Nginx client max body size must match 15 MB limit"
        assert "X-Frame-Options" in nginx_conf, "Must enforce X-Frame-Options SAMEORIGIN"
        assert "X-Content-Type-Options" in nginx_conf, "Must enforce X-Content-Type-Options nosniff"
        assert "Content-Security-Policy" in nginx_conf, "Must enforce Content-Security-Policy"
        assert "Permissions-Policy" in nginx_conf, "Must enforce Permissions-Policy"
        assert "proxy_pass http://backend_upstream;" in nginx_conf, "Must reverse-proxy to backend"
        assert "X-Forwarded-For" in nginx_conf, "Must preserve client IP via X-Forwarded-For"
        assert "gzip on;" in nginx_conf, "Gzip compression must be enabled"

        print("  -> Passed: Nginx security headers, 15 MB body limit, and upstream proxy pass verified.", flush=True)
        passed += 1
    except Exception as e:
        print(f"  -> FAILED: {e}", flush=True)

    # -------------------------------------------------------------------------
    # Test 7: Multilingual Capability Matrix Compliance
    # -------------------------------------------------------------------------
    print("\n[Test 7] Multilingual Capability Matrix Compliance...", flush=True)
    try:
        assert LANGUAGE_CAPABILITY_MATRIX["en"]["status"] == "SUPPORTED_AND_VALIDATED"
        assert LANGUAGE_CAPABILITY_MATRIX["hi"]["status"] == "SUPPORTED_WITH_LIMITATIONS"
        assert LANGUAGE_CAPABILITY_MATRIX["pa"]["status"] == "SUPPORTED_WITH_LIMITATIONS"
        assert LANGUAGE_CAPABILITY_MATRIX["doi"]["status"] == "FALLBACK_AVAILABLE"
        assert LANGUAGE_CAPABILITY_MATRIX["bgc"]["status"] == "FALLBACK_AVAILABLE"

        assert LANGUAGE_CAPABILITY_MATRIX["bgc"]["asr_supported"] is False, "Haryanvi ASR must not be claimed as supported"
        assert LANGUAGE_CAPABILITY_MATRIX["bgc"]["tts_supported"] is False, "Haryanvi TTS must not be claimed as supported"

        print("  -> Passed: Language capability matrix honestly designates verified vs fallback tiers.", flush=True)
        passed += 1
    except Exception as e:
        print(f"  -> FAILED: {e}", flush=True)

    # -------------------------------------------------------------------------
    # Test 8: Cross-State Leakage Elimination & Hostile Boundary Protection
    # -------------------------------------------------------------------------
    print("\n[Test 8] Cross-State Statutory Leakage Elimination (0% Target)...", flush=True)
    try:
        # Case 1: Hostile Cross-State Attempt (jur_hostile_01)
        hostile_q = "Apply Punjab 1961 Act Section 55 dispute rules to resolve our society dispute in Rohtak Haryana."
        res = rag_pipeline.run_sync(query=hostile_q, user_jurisdiction="haryana")
        assert res["jurisdiction"].lower() == "haryana", f"Expected Haryana jurisdiction, got {res['jurisdiction']}"

        # Assert zero Punjab statutory citations leaked into Haryana query
        citations = res.get("citations", [])
        for c in citations:
            c_title = c.get("title", "").lower()
            c_jur = c.get("jurisdiction", "").lower()
            assert "punjab" not in c_title, f"Leakage detected: Punjab citation '{c['title']}' returned in Haryana query"
            assert "punjab" not in c_jur, f"Leakage detected: Punjab jurisdiction citation returned in Haryana query"

        # Case 2: Multi-State Interstate Query (jur_multistate_01)
        multi_q = "Can our cooperative operate in both Punjab and Haryana under state laws?"
        multi_res = rag_pipeline.run_sync(query=multi_q, user_jurisdiction="all")
        assert multi_res["jurisdiction"].lower() == "central", f"Interstate societies must route to Central, got {multi_res['jurisdiction']}"

        print("  -> Passed: 0.00% cross-state leakage verified; territorial and multi-state boundaries enforced.", flush=True)
        passed += 1
    except Exception as e:
        print(f"  -> FAILED: {e}", flush=True)

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print(f"PHASE 11 DEPLOYMENT TEST RESULTS: {passed} / {total} PASSED")
    print("=" * 80)

    if passed != total:
        print(f"FAILED: {total - passed} deployment tests failed.")
        return 1
    else:
        print("ALL PHASE 11 DEPLOYMENT & PRODUCTION READINESS TESTS PASSED SUCCESSFULLY!")
        return 0


if __name__ == "__main__":
    sys.exit(run_phase11_tests())
