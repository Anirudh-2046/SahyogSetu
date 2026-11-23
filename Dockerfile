# syntax=docker/dockerfile:1
# ==============================================================================
# SahyogSetu Production Multi-Stage Container Definition
# ==============================================================================

# Stage 1: Build Frontend Static Bundle
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# Stage 2: Production Python Backend Runtime
FROM python:3.12-slim AS backend

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_ENV=production \
    PORT=8000 \
    HOST=0.0.0.0

WORKDIR /app

# Install security updates and operational utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install Python production dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root dedicated application user (UID 10001)
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/bash -m appuser

# Copy application directories
COPY backend/ ./backend/
COPY processed/ ./processed/
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Ensure persistent directories exist and have proper non-root ownership
RUN mkdir -p /app/backend/data/tts_cache /app/backend/data/backups && \
    chown -R appuser:appgroup /app

# Switch to unprivileged execution user
USER appuser

EXPOSE 8000

# Container healthcheck using standard readiness probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ready || exit 1

# Production application entrypoint with Uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
