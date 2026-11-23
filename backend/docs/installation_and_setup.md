# SahyogSetu — Installation & Setup Guide

**Document Version:** 2.0.0  
**Date:** November 2026  
**Audience:** Developers, DevOps Engineers, System Administrators, and Academic Evaluators  

---

## 1. Prerequisites & System Requirements

### Hardware Requirements
- **Processor:** Modern x86_64 or ARM64 processor (Intel Core i5 / AMD Ryzen 5 or higher recommended; Apple Silicon supported).
- **RAM:** Minimum 4 GB RAM (8 GB recommended for simultaneous frontend dev server and backend).
- **Disk Space:** Minimum 2 GB free disk space (includes virtualenv, npm node_modules, SQLite databases, and cached audio files).

### Software Requirements
- **Operating System:** Linux (Ubuntu 22.04+ / Debian 12), macOS (13+), or Windows 10/11 (with PowerShell 5.1+).
- **Python:** Python 3.12 (strictly tested on Python 3.12.10).
- **Node.js:** Node.js 20 LTS (tested on Node 20.x and 22.x) with npm 10+.
- **Git:** Git 2.30+.
- **Docker & Docker Compose (Optional):** Docker 24+ and Docker Compose 2.20+ for containerized deployment.

---

## 2. Repository Cloning & Structure

```bash
# Clone the repository
git clone https://github.com/anirudh-0408/MDC-26.git
cd "MDC'26"
```

Verify directory contents:
```bash
# Windows PowerShell
Get-ChildItem -Name

# Linux / macOS
ls -la
```

---

## 3. Environment Configuration

Copy the template configuration file to `.env`:
```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux / macOS
cp .env.example .env
```

### Key Environment Settings in `.env`:
```ini
# Application Mode ('development', 'testing', 'staging', 'production')
APP_ENV=development
DEBUG=false

# Server Bindings
HOST=127.0.0.1
PORT=8000

# CORS Allowed Origins
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://127.0.0.1:8000

# Administrative API Key (MUST be changed in production)
ADMIN_API_KEY=sahyogsetu_admin_secret_key_2026

# Storage Paths
DATABASE_PATH=backend/data/news.db
TTS_CACHE_DIR=backend/data/tts_cache

# Optional Cloud AI API Keys (leave empty for 100% offline local operation)
BHASHINI_USER_ID=
BHASHINI_API_KEY=
BHASHINI_INFERENCE_KEY=
GEMINI_API_KEY=
OPENAI_API_KEY=
```

---

## 4. Backend Setup & Virtual Environment

### 4.1 Create & Activate Python 3.12 Virtual Environment
```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 4.2 Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Verify installed packages:
```bash
python -c "import fastapi, pydantic, fitz, sklearn, sqlite3; print('All core backend dependencies successfully imported!')"
```

---

## 5. Database & Knowledge Store Initialization

The backend includes a pre-seeded, verified database in `backend/data/`:
- `backend/data/news.db`: 29 verified official government news records.
- `backend/data/vectors.db`: 33 canonical statutory chunks with 384-dimensional dense vectors across 11 Acts.
- `backend/ml/models/`: Pre-trained models (`intent_model.joblib`, `language_model.joblib`, `news_model.joblib`).

To verify database tables and record counts:
```bash
python -c "
import sqlite3
c1 = sqlite3.connect('backend/data/news.db')
print('News records:', c1.execute('SELECT COUNT(*) FROM news_items').fetchone()[0])
c2 = sqlite3.connect('backend/data/vectors.db')
print('Statutory chunks:', c2.execute('SELECT COUNT(*) FROM document_chunks').fetchone()[0])
"
```
Expected output:
```
News records: 29
Statutory chunks: 33
```

---

## 6. Frontend Setup

In a separate terminal window:
```bash
cd frontend

# Install Node dependencies
npm ci

# Validate TypeScript compilation
npm run build
```
The production bundle will be generated into `frontend/dist/`.

---

## 7. Running SahyogSetu Locally

### Option A: Standard Development Mode (Hot Reload)

1. **Start the Backend API Server:**
   ```bash
   # From project root with .venv active
   uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   API Documentation is live at: `http://127.0.0.1:8000/docs`  
   Health check endpoint is live at: `http://127.0.0.1:8000/api/health`

2. **Start the Frontend Vite Development Server:**
   ```bash
   # In frontend/ directory
   npm run dev
   ```
   Open your browser at: `http://localhost:5173`

---

## 8. Running the Complete Verification & Test Suite

The platform includes automated verification scripts across all phases:

### Run Individual Test Suites:
```bash
# Phase 8: Full-Stack Citizen User Journeys (9/9)
python backend/tests/test_phase8_integration.py

# Phase 9: Security Hardening & Rate Limiting (10/10)
python backend/tests/test_phase9_security.py

# Phase 11: Production Deployment & Backup Verification (8/8)
python backend/tests/test_phase11_deployment.py
```

### Run Phase 10 Independent Evaluation Benchmarks:
```bash
# Jurisdiction Isolation & Cross-State Boundary Benchmark
python backend/evaluation/phase10/jurisdiction_eval.py

# Legal Answer Quality & Claim-Level Groundedness Benchmark
python backend/evaluation/phase10/answer_quality_eval.py

# Master Quality Assurance Suite (all 8 stages)
python backend/evaluation/phase10/run_all_evaluations.py
```

### Run Post-Deployment Smoke Test:
```bash
python backend/scripts/smoke_test.py
```

---

## 9. Containerized Setup (Docker & Docker Compose)

To build and run SahyogSetu inside isolated containers:

### 9.1 Build and Start Containers
```bash
# From project root
docker-compose up --build -d
```

### 9.2 Inspect Running Containers
```bash
docker-compose ps
```
You will see two services:
- `sahyogsetu-backend`: FastAPI running under non-root user `appuser` (UID 10001).
- `sahyogsetu-proxy`: Nginx 1.27 serving frontend static bundle on port 80 and reverse proxying `/api/` to the backend.

### 9.3 Verify Container Readiness
```bash
curl -f http://localhost/api/health/ready
```
Expected response:
```json
{
  "status": "ready",
  "service": "SahyogSetu Cooperative Governance & Legal API",
  "checks": {
    "database": true,
    "knowledge_store": true,
    "vector_store": true
  }
}
```

### 9.4 Stop Containers
```bash
docker-compose down
```
*Note: SQLite databases and audio caches persist across container restarts inside the named Docker volume `sahyogsetu_data`.*

---

## 10. Disaster Recovery: Backup and Restore

### Create a Hot Database Snapshot:
```bash
python backend/scripts/backup_restore.py
```
Snapshots are stored in `backend/data/backups/snapshot_YYYYMMDD_HHMMSS/` with SHA-256 checksums and `PRAGMA integrity_check` validation.

### Restore from a Snapshot:
```bash
python backend/scripts/backup_restore.py restore backend/data/backups/snapshot_YYYYMMDD_HHMMSS
```

---

## 11. Troubleshooting Common Problems

| Symptom | Probable Cause | Verified Remediation |
|---|---|---|
| `Port 8000 already in use` | Another Uvicorn/FastAPI instance is running. | Identify and kill the process: `netstat -ano \| findstr 8000` (Windows) or `lsof -i :8000` (Linux), then kill PID. |
| `sqlite3.OperationalError: database is locked` | Simultaneous non-WAL connection or external viewer open. | Ensure SQLite WAL mode is active (`PRAGMA journal_mode = WAL;`) and close external DB browser tools. |
| `Browser microphone not transcribing` | Missing browser permissions or non-localhost HTTP origin. | Grant microphone permissions in browser settings; Chrome requires HTTPS or `http://localhost`. |
| `429 Too Many Requests: Rate limit exceeded` | Client exceeded 30 requests within 60 seconds. | Wait 60 seconds (check `Retry-After` header); rate limiting can be toggled via `RATE_LIMIT_ENABLED=false` in `.env` for benchmarking. |
| `Audio playback produces mechanical voice` | Offline mode active without external Bhashini credentials. | Expected behavior in local offline mode; the platform transparently uses the built-in local harmonic parametric synthesizer. |
| `ModuleNotFoundError: No module named 'backend'` | Running script from inside a subfolder without `PYTHONPATH`. | Always run scripts from the project root: `python backend/scripts/smoke_test.py`. |
