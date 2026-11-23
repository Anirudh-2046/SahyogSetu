# SahyogSetu — Deployment & Operations Guide

**Document Version:** 2.0.0  
**Date:** November 2026  
**Audience:** DevOps Engineers, Site Reliability Engineers, System Administrators, and Project Reviewers  

---

## 1. Deployment Tiers & Release Readiness Taxonomy

SahyogSetu defines four distinct deployment tiers with explicit operational gates:

```
+---------------------------------------------------------------------------------------------------+
|                                 SAHYOGSETU DEPLOYMENT TIERS                                       |
+---------------------------------------------------------------------------------------------------+
| 1. JURY & ACADEMIC DEMONSTRATION TIER [APPROVED - GO]                                             |
|    - Target: Academic juries, hackathons, and technical evaluation panels.                        |
|    - Infrastructure: Single host or laptop; local CPU execution; zero external cloud dependencies.|
|    - Latency: ~5 ms local deterministic statutory synthesizer.                                    |
|    - Quality Status: 0.00% citation hallucination; 0.00% cross-state leakage.                    |
+---------------------------------------------------------------------------------------------------+
| 2. RESTRICTED STAGING PILOT TIER [APPROVED - GO]                                                  |
|    - Target: Internal state cooperative departments, PACS training centres, and pilot societies.  |
|    - Infrastructure: Docker Compose with Nginx reverse proxy, persistent volume, and IP whitelist.|
|    - Quality Status: Managed users aware of the 33-chunk canonical statutory corpus scope.        |
+---------------------------------------------------------------------------------------------------+
| 3. CONTROLLED PUBLIC PILOT TIER [CONDITIONAL GO]                                                  |
|    - Target: Public citizen pilot across selected districts in Punjab, Haryana, or J&K.          |
|    - Conditions Required: Prominent statutory disclaimer; mandatory user jurisdiction confirmation|
|      before answering state-specific queries; human registrar review for formal compliance filings|
+---------------------------------------------------------------------------------------------------+
| 4. UNRESTRICTED PUBLIC PRODUCTION TIER [NOT RECOMMENDED WITHOUT CORPUS EXPANSION]                |
|    - Reason: Current section-level retrieval P@1 is 31.35% due to 33 canonical statutory chunks.  |
|      While the system safely abstains on unindexed topics, full unrestricted production requires  |
|      expanding corpus density across all 120+ sections and state rules.                           |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Docker & Container Deployment Architecture

The application is packaged into two decoupled containers running on an isolated bridge network:

```
[Public Internet]
       │
       ▼ (Port 80 / 443)
┌────────────────────────────────────────────────────────┐
│ Container: sahyogsetu-proxy (nginx:1.27-alpine)        │
│ - Enforces 15 MB upload ceiling                        │
│ - Injects HSTS, CSP, X-Frame-Options                   │
│ - Serves pre-built React 19 SPA static assets          │
│ - Forwards /api/ traffic to upstream                   │
└──────────────────────┬─────────────────────────────────┘
                       │ (Internal bridge network: sahyogsetu-net)
                       ▼ (Port 8000)
┌────────────────────────────────────────────────────────┐
│ Container: sahyogsetu-backend (python:3.12-slim)       │
│ - Dedicated unprivileged user: appuser (UID 10001)     │
│ - Uvicorn ASGI server with 2 worker processes          │
│ - Active healthcheck probe on /api/health/ready        │
│ - Mounts persistent volume /app/backend/data           │
└──────────────────────┬─────────────────────────────────┘
                       │
                       ▼
┌────────────────────────────────────────────────────────┐
│ Persistent Host Volume: sahyogsetu_data                │
│ - news.db (SQLite WAL mode)                            │
│ - vectors.db (Indexed chunks & dense embeddings)       │
│ - tts_cache/ (Synthesized WAV audio files)             │
└────────────────────────────────────────────────────────┘
```

---

## 3. Production Environment Variables Reference

| Variable Name | Default Value | Recommended Production Value | Description |
|---|---|---|---|
| `APP_ENV` | `development` | `production` | Operational environment profile. |
| `DEBUG` | `false` | `false` | Must be strictly `false` in production to prevent stack trace leaks. |
| `HOST` | `127.0.0.1` | `0.0.0.0` | Host interface binding inside container. |
| `PORT` | `8000` | `8000` | HTTP port for ASGI server. |
| `CORS_ORIGINS` | `*` | `https://sahyogsetu.gov.in` | Explicit domain origins (wildcard `*` rejected in prod). |
| `ADMIN_API_KEY` | `sahyogsetu...` | Random 32-char hex string | Protects admin endpoints (`trigger-fetch`, `ingest`). |
| `RATE_LIMIT_ENABLED` | `true` | `true` | Activates 30 req/min sliding-window limiter per IP. |
| `MAX_UPLOAD_SIZE_BYTES` | `15728640` | `15728640` | 15 MB boundary enforced across Nginx and FastAPI. |
| `DATABASE_PATH` | `backend/data/news.db` | `/app/backend/data/news.db`| Path to relational SQLite database. |
| `TTS_CACHE_DIR` | `backend/data/tts_cache` | `/app/backend/data/tts_cache`| Path to persistent synthesized audio cache. |
| `LOG_LEVEL` | `INFO` | `INFO` or `WARNING` | Server logging verbosity. |

---

## 4. Reverse Proxy & HTTPS Configuration

The production reverse proxy is configured in `nginx/sahyogsetu.conf`.

### 4.1 HTTPS & SSL/TLS Production Setup (Let's Encrypt)
To enable HTTPS in production:
1. Obtain an SSL certificate using Certbot:
   ```bash
   sudo certbot certonly --standalone -d sahyogsetu.gov.in
   ```
2. Mount certificates into the Nginx container in `docker-compose.yml`:
   ```yaml
   volumes:
     - /etc/letsencrypt/live/sahyogsetu.gov.in/fullchain.pem:/etc/nginx/certs/fullchain.pem:ro
     - /etc/letsencrypt/live/sahyogsetu.gov.in/privkey.pem:/etc/nginx/certs/privkey.pem:ro
   ```
3. Add SSL server block in `nginx/sahyogsetu.conf`:
   ```nginx
   server {
       listen 443 ssl http2;
       server_name sahyogsetu.gov.in;

       ssl_certificate /etc/nginx/certs/fullchain.pem;
       ssl_certificate_key /etc/nginx/certs/privkey.pem;
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers HIGH:!aNULL:!MD5;
       ssl_prefer_server_ciphers on;

       # HSTS (Strict-Transport-Security)
       add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
       ...
   }
   ```

---

## 5. Health Monitoring & Observability

### 5.1 Container Health Probes
- **Liveness Probe (`GET /api/health/live`):**
  - Confirms web process event-loop responsiveness.
  - Return: HTTP 200 `{"status": "alive"}`.
- **Readiness Probe (`GET /api/health/ready`):**
  - Confirms database connectivity, knowledge store file existence, and vector store availability.
  - Return: HTTP 200 `{"status": "ready"}` or HTTP 503 `{"status": "not_ready"}` if dependencies fail.
- **Diagnostic Inspection (`GET /api/health`):**
  - Reports news record totals, active conversations, TTS engine status, and Bhashini configuration status with zero secret leaks.

### 5.2 Structured Logging & Privacy Scrubbing
- Server logs conform to standard format: `%(asctime)s [%(levelname)s] %(name)s: %(message)s`.
- Privacy middleware automatically redacts sensitive citizen patterns in real-time before writing to log sinks:
  - 12-digit Aadhaar numbers $\to$ `[AADHAAR_REDACTED]`
  - 6-digit OTP codes $\to$ `[OTP_REDACTED]`
  - Bearer tokens $\to$ `[TOKEN_REDACTED]`

---

## 6. Disaster Recovery: Backup, Verification & Restore

### 6.1 Automated Hot Backup
The utility `backend/scripts/backup_restore.py` executes an online, non-blocking snapshot using SQLite's native backup API:
```bash
python backend/scripts/backup_restore.py
```
- Performs `PRAGMA integrity_check;` on source databases.
- Backs up `news.db` and `vectors.db` to `backend/data/backups/snapshot_YYYYMMDD_HHMMSS/`.
- Computes SHA-256 hashes and outputs `backup_manifest.json`.

### 6.2 Safe Atomic Restore
```bash
python backend/scripts/backup_restore.py restore backend/data/backups/snapshot_YYYYMMDD_HHMMSS
```
- Validates SHA-256 hashes of snapshot files against `backup_manifest.json`.
- Runs `PRAGMA integrity_check;` on the backup files.
- Restores files atomically via temporary swap files (`.tmp_restore`), ensuring zero database corruption if interrupted.

---

## 7. CI/CD Pipeline & Automated Release Gates

Configured in `.github/workflows/ci.yml`:
1. **Pull Request & Commit Gate:**
   - Triggers on every push and PR to `main`.
2. **Automated Testing Matrix:**
   - Runs full regression suite across Phases 2 through 9.
   - Runs Phase 10 quality benchmarks (`jurisdiction_eval.py`, `answer_quality_eval.py`, `performance_eval.py`).
   - Runs Phase 11 deployment and backup test suite (`test_phase11_deployment.py`).
3. **Frontend Gate:**
   - Validates TypeScript types (`npx tsc -b`).
   - Executes Vite production build (`npm run build`).
4. **Docker Validation Gate:**
   - Builds multi-stage Docker image to verify container reproducibility.

---

## 8. Release Management & Rollback Strategy

### 8.1 Semantic Versioning
- Releases follow Semantic Versioning (`MAJOR.MINOR.PATCH`).
- Current Target: `v2.0.0-rc1` (Release Candidate 1).

### 8.2 Production Rollback Runbook
If an operational regression is detected post-deployment:
1. **Container Rollback:**
   ```bash
   docker-compose down
   docker tag sahyogsetu:v1.0.0-rc1 sahyogsetu:latest
   docker-compose up -d
   ```
2. **Database Rollback:**
   ```bash
   python backend/scripts/backup_restore.py restore backend/data/backups/snapshot_PREVIOUS_VERSION
   ```
3. **Verification:**
   ```bash
   python backend/scripts/smoke_test.py
   ```

---

## 9. Pre-Deployment Operations Checklist

Before approving a production deployment, verify all checklist gates:

- [x] Host environment meets minimum specifications (4 GB RAM, 2 GB disk).
- [x] Python 3.12 and Node.js 20 LTS installed.
- [x] `.env` configured with `APP_ENV=production` and `DEBUG=false`.
- [x] `ADMIN_API_KEY` changed from default development key.
- [x] `CORS_ORIGINS` configured with explicit allowed domain (no wildcard `*`).
- [x] Persistent volume `sahyogsetu_data` verified.
- [x] Multi-stage Docker build succeeds under non-root user `appuser` (UID 10001).
- [x] Nginx reverse proxy enforces 15 MB upload limit and security headers.
- [x] Liveness (`/api/health/live`) and readiness (`/api/health/ready`) probes return HTTP 200.
- [x] Hot backup snapshot taken and verified with SHA-256 manifest.
- [x] Automated smoke tests pass 100% (`smoke_test.py`).
- [x] Mandatory statutory disclaimers visible in UI footer and API responses.
