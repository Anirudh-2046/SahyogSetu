"""
SahyogSetu Backend Configuration
Manages all environment variables and operational settings with secure defaults.
Never exposes secret keys or tokens in logs or responses.
"""

import os
from typing import List
from dataclasses import dataclass, field

@dataclass
class Settings:
    # Service Information
    APP_NAME: str = "SahyogSetu Cooperative Governance & Legal API"
    APP_VERSION: str = "2.0.0"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "t")

    # Host & Port
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Database Path
    DB_DIR: str = os.path.join(os.path.dirname(__file__), "data")
    DB_PATH: str = os.getenv("DATABASE_PATH", os.path.join(DB_DIR, "news.db"))

    @property
    def DATABASE_PATH(self) -> str:
        return self.DB_PATH

    # Audio Cache Directory
    TTS_CACHE_DIR: str = os.getenv("TTS_CACHE_DIR", os.path.join(DB_DIR, "tts_cache"))

    # CORS
    CORS_ORIGINS: List[str] = field(default_factory=lambda: [
        origin.strip() for origin in os.getenv("CORS_ORIGINS", "*").split(",") if origin.strip()
    ])

    # Administrative Security & Key
    ADMIN_API_KEY: str = os.getenv("ADMIN_API_KEY", "sahyogsetu_admin_secret_key_2026").strip()

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "true").lower() in ("true", "1", "t")

    # Uploads
    MAX_UPLOAD_SIZE_BYTES: int = int(os.getenv("MAX_UPLOAD_SIZE_BYTES", str(15 * 1024 * 1024)))  # 15 MB
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Bhashini ULCA API Credentials (Optional)
    BHASHINI_USER_ID: str = os.getenv("BHASHINI_USER_ID", "").strip()
    BHASHINI_API_KEY: str = os.getenv("BHASHINI_API_KEY", "").strip()
    BHASHINI_INFERENCE_KEY: str = os.getenv("BHASHINI_INFERENCE_KEY", "").strip()
    BHASHINI_TIMEOUT: float = float(os.getenv("BHASHINI_TIMEOUT", "8.0"))

    @property
    def is_bhashini_configured(self) -> bool:
        return bool(self.BHASHINI_USER_ID and self.BHASHINI_API_KEY and self.BHASHINI_INFERENCE_KEY)

    def validate_environment(self, strict: bool = False) -> dict:
        """
        Validates environment configuration, file permissions, and directory structures.
        """
        errors = []
        warnings = []

        valid_envs = {"development", "testing", "staging", "production"}
        if self.APP_ENV not in valid_envs:
            warnings.append(f"APP_ENV '{self.APP_ENV}' is not standard {valid_envs}.")

        if self.APP_ENV == "production":
            if self.DEBUG:
                errors.append("DEBUG mode must be disabled in production.")
            if "*" in self.CORS_ORIGINS:
                errors.append("Wildcard CORS ('*') is not allowed in production.")
            if self.ADMIN_API_KEY == "sahyogsetu_admin_secret_key_2026":
                warnings.append("ADMIN_API_KEY is using the default development key.")

        # Ensure DB directory exists
        if not os.path.exists(self.DB_DIR):
            try:
                os.makedirs(self.DB_DIR, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create database directory {self.DB_DIR}: {e}")

        # Check DB directory is writable
        if os.path.exists(self.DB_DIR) and not os.access(self.DB_DIR, os.W_OK):
            errors.append(f"Database directory {self.DB_DIR} is not writable.")

        # Check vectors.db
        vector_db = os.path.join(self.DB_DIR, "vectors.db")
        if not os.path.exists(vector_db):
            warnings.append(f"Vector store {vector_db} not found on disk; statutory RAG will be empty until initialized.")

        # Ensure TTS cache dir exists or can be created
        if not os.path.exists(self.TTS_CACHE_DIR):
            try:
                os.makedirs(self.TTS_CACHE_DIR, exist_ok=True)
            except Exception as e:
                warnings.append(f"Cannot create TTS cache directory {self.TTS_CACHE_DIR}: {e}")

        is_valid = len(errors) == 0
        report = {
            "valid": is_valid,
            "environment": self.APP_ENV,
            "debug": self.DEBUG,
            "errors": errors,
            "warnings": warnings,
        }

        if strict and not is_valid:
            raise ValueError(f"Environment validation failed: {errors}")

        return report

settings = Settings()
