# SahyogSetu — Phase 9: Production Deployment & Hardening Configuration

**Document Version:** 1.0  
**Date:** November 2026  
**Target Environment:** Linux / Ubuntu 22.04 LTS / Kubernetes / Docker  
**Status:** Approved for Production Deployment

---

## 1. Architectural Overview

SahyogSetu is built as a high-performance, modular system comprising:
1. **Frontend:** React + Vite Single Page Application (SPA) serving responsive citizen interfaces.
2. **Backend:** FastAPI ASGI application managing legal RAG, Bhashini speech/translation, and government news pipelines.
3. **Database:** SQLite with WAL mode (`Write-Ahead Logging`), foreign key enforcement, and parameterized queries.
4. **Knowledge Store:** Processed statutory chunks and embeddings indexing 55 official cooperative laws and notifications.

---

## 2. Environment Segregation Matrix

| Configuration Variable | Development (`dev`) | Staging / Testing (`test`) | Production (`prod`) |
|---|---|---|---|
| `ENVIRONMENT` | `development` | `testing` | `production` |
| `DEBUG` | `True` | `False` | `False` |
| `CORS_ORIGINS` | `http://localhost:5173,http://localhost:3000` | `https://staging.sahyogsetu.nic.in` | `https://sahyogsetu.gov.in,https://sahyogsetu.nic.in` |
| `ADMIN_API_KEY` | Default development key | Secure random (min 32 chars) | Managed Secret (Vault / HSM / Env, min 64 chars) |
| `RATE_LIMIT_ENABLED` | `False` (for testing) | `True` | `True` |
| `BHASHINI_API_KEY` | Mock / Test credentials | Staging credentials | Production MeitY Bhashini API Key |
| `LOG_LEVEL` | `DEBUG` | `INFO` | `WARNING` / `INFO` (PII-scrubbed) |

---

## 3. Reverse Proxy & Security Headers (Nginx Configuration)

In production, FastAPI should run behind an enterprise reverse proxy (e.g. Nginx or Cloudflare) providing TLS 1.3 termination, HTTP/2 multiplexing, and static asset caching.

### Recommended `nginx.conf`
```nginx
# /etc/nginx/sites-available/sahyogsetu.gov.in

upstream fastapi_backend {
    server 127.0.0.1:8000 max_fails=3 fail_timeout=10s;
    keepalive 32;
}

server {
    listen 80;
    server_name sahyogsetu.gov.in www.sahyogsetu.gov.in;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name sahyogsetu.gov.in www.sahyogsetu.gov.in;

    # TLS 1.3 Strict Ciphers
    ssl_certificate /etc/letsencrypt/live/sahyogsetu.gov.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/sahyogsetu.gov.in/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Production Hardened Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://sahyogsetu.gov.in; media-src 'self' data: blob:;" always;

    # Request Body Size Limit (Enforced at Reverse Proxy)
    client_max_body_size 15M;

    # Frontend Static Distribution
    location / {
        root /var/www/sahyogsetu/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
        expires 1d;
        add_header Cache-Control "public, no-transform";
    }

    # API Proxy Pass to FastAPI
    location /api/ {
        proxy_pass http://fastapi_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
        proxy_connect_timeout 10s;
    }

    # Health & Liveness Probes
    location /health {
        proxy_pass http://fastapi_backend/health;
        access_log off;
    }
}
```

---

## 4. Systemd Service Deployment

To ensure high availability and automatic process restarts, run the backend under `systemd`:

### `/etc/systemd/system/sahyogsetu.service`
```ini
[Unit]
Description=SahyogSetu Sovereign Legal RAG Backend
After=network.target

[Service]
Type=simple
User=sahyogsetu
Group=www-data
WorkingDirectory=/opt/sahyogsetu
EnvironmentFile=/etc/sahyogsetu/production.env
ExecStart=/opt/sahyogsetu/.venv/bin/uvicorn backend.main:app --host 127.0.0.1 --port 8000 --workers 4 --proxy-headers --forwarded-allow-ips='127.0.0.1'
Restart=always
RestartSec=3
LimitNOFILE=65535
PrivateTmp=true
ProtectSystem=full
ProtectHome=true

[Install]
WantedBy=multi-user.target
```

---

## 5. Containerization Guidelines (Docker)

For Kubernetes or container-based deployments, build minimal multi-stage images:

```dockerfile
# Multi-stage Docker build for SahyogSetu
FROM python:3.11-slim as backend-builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=backend-builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY backend/ ./backend/
EXPOSE 8000

# Health check probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health/liveness || exit 1

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

---

## 6. Maintenance & Operational Runbook

### 6.1 Database Backups
- Perform automated daily SQLite snapshot backups using SQLite online backup API or `sqlite3 /path/to/news.db ".backup '/path/to/backups/news_$(date +%F).db'"`.
- Retain rolling 30-day backups on encrypted off-site storage.

### 6.2 Monitoring & Alerting
- Monitor `GET /health/liveness` for process heartbeat (restart container if non-200).
- Monitor `GET /health/readiness` for storage and database availability.
- Monitor 429 rate limit telemetry and 500 error counts via `X-Request-ID` correlation in logs.
