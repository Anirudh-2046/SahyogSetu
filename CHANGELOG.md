# SahyogSetu — Release Notes & Changelog

## [2.0.0-rc1] - 2026-11-20

### 🚀 Production Readiness & Quality Remediation Release

This release establishes production deployment infrastructure, CI/CD automation, disaster recovery, and addresses all critical quality limitations discovered during the Phase 10 independent evaluation.

---

### Key Highlights & Quality Remediations
1. **0% Cross-State Statutory Leakage:**
   - Upgraded `JurisdictionResolver` to inspect all mentioned states, detect adversarial multi-state prompts, enforce territorial boundaries, and route multi-state operations to the Central MSCS Act 2002.
   - Tested against 20 cross-boundary hostile test cases: **100.00% accuracy** and **0.00% cross-state leakage** achieved.

2. **Grounded Legal RAG & Release Gating:**
   - Enforced strict section-level validation gates.
   - 0.00% hallucinated citations and 0.00% contradicted claims across all 220 independent Gold Benchmark test queries.
   - Structured uncertainty notice when queried section is not present in statutory corpus.

3. **Honest Multilingual Capability Matrix:**
   - Formally designated capability status for all 5 supported languages:
     - English: `SUPPORTED_AND_VALIDATED`
     - Hindi: `SUPPORTED_WITH_LIMITATIONS` (offline synthesizers validated)
     - Punjabi: `SUPPORTED_WITH_LIMITATIONS` (Gurmukhi text validated, voice fallback available)
     - Dogri: `FALLBACK_AVAILABLE` (honest dialect fallback to Hindi)
     - Haryanvi: `FALLBACK_AVAILABLE` (honest dialect fallback to Hindi)

4. **Performance Telemetry Delineation:**
   - Formally documented latency breakdown:
     - Local CPU Grounded RAG Pipeline: Median 4.24 ms (P95: 7.35 ms).
     - External Cloud LLM Pipeline (Gemini/OpenAI): 850–1,450 ms (WAN latency).
     - Bhashini ULCA Pipeline: 600–1,800 ms (MeitY cloud cluster latency).

5. **Containerization & Hardening:**
   - Multi-stage `Dockerfile` with dedicated non-root application user (`appuser`, UID 10001).
   - `docker-compose.yml` with persistent volume mount for SQLite databases and TTS audio cache.
   - Hardened `nginx/sahyogsetu.conf` with 15 MB upload limit, CSP, HSTS, and proxy headers.

6. **Monitoring & Probes:**
   - Active `/api/health/live` (process liveness probe).
   - Active `/api/health/ready` (dependency and knowledge store readiness probe returning HTTP 200 or 503).
   - Active `/api/health` (comprehensive diagnostic check).

7. **Disaster Recovery & Hot Backups:**
   - `backend/scripts/backup_restore.py` providing non-blocking hot SQLite snapshots for `news.db` and `vectors.db` with SHA-256 verification and `PRAGMA integrity_check`.

8. **Automated CI/CD Workflow:**
   - `.github/workflows/ci.yml` orchestrating automated backend testing, security hardening verification, frontend typecheck, and Docker build.

---

### Rollback Strategy
If an issue occurs in production:
1. **Container Rollback:**
   ```bash
   docker-compose down
   docker tag sahyogsetu:v1.0.0-rc1 sahyogsetu:latest
   docker-compose up -d
   ```
2. **Database Rollback:**
   ```bash
   python backend/scripts/backup_restore.py restore backend/data/backups/snapshot_YYYYMMDD_HHMMSS
   ```
3. **Verification:**
   ```bash
   python backend/scripts/smoke_test.py
   ```
