"""
Audio Cache and Ephemeral Storage Manager
Stores synthesized speech by SHA-256 content hash with automatic expiry.
Prevents redundant API calls and protects storage limits.
"""

import os
import time
import hashlib
import logging
from typing import Optional, Tuple, Dict, Any

logger = logging.getLogger("sahyogsetu.tts.cache")

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "tts_cache")
MAX_CACHE_AGE_SECONDS = 24 * 60 * 60  # 24 Hours expiry

class AudioCache:
    """Manages disk and memory caching of generated audio files."""

    def __init__(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        self.meta_index: Dict[str, Dict[str, Any]] = {}
        self._prune_expired()

    @staticmethod
    def compute_audio_id(text: str, language: str, voice_gender: str = "female") -> str:
        payload = f"{language}_{voice_gender}_{text.strip()}".encode("utf-8")
        return f"tts_{hashlib.sha256(payload).hexdigest()[:16]}"

    def get_audio(self, audio_id: str) -> Optional[Tuple[bytes, str]]:
        """Retrieves cached audio bytes and MIME type if present and not expired."""
        for ext, mime in [(".mp3", "audio/mpeg"), (".wav", "audio/wav")]:
            fpath = os.path.join(CACHE_DIR, f"{audio_id}{ext}")
            if os.path.isfile(fpath):
                # Check file modification time
                mtime = os.path.getmtime(fpath)
                if time.time() - mtime < MAX_CACHE_AGE_SECONDS:
                    try:
                        with open(fpath, "rb") as f:
                            data = f.read()
                        return data, mime
                    except Exception as e:
                        logger.warning("Error reading cache file %s: %s", fpath, e)
                else:
                    # Expired, clean up
                    try:
                        os.remove(fpath)
                    except Exception:
                        pass
        return None

    def save_audio(self, audio_id: str, audio_bytes: bytes, audio_format: str, metadata: Dict[str, Any] = None) -> str:
        """Saves generated audio to cache directory."""
        ext = ".wav" if "wav" in audio_format.lower() else ".mp3"
        fpath = os.path.join(CACHE_DIR, f"{audio_id}{ext}")
        try:
            with open(fpath, "wb") as f:
                f.write(audio_bytes)
            if metadata:
                self.meta_index[audio_id] = {
                    **metadata,
                    "saved_at": time.time(),
                    "file_path": fpath,
                }
            return fpath
        except Exception as e:
            logger.error("Failed to write audio cache for %s: %s", audio_id, e)
            return ""

    def get_stats(self) -> Dict[str, Any]:
        """Returns cache storage metrics."""
        count = 0
        total_size = 0
        if os.path.exists(CACHE_DIR):
            for fname in os.listdir(CACHE_DIR):
                fpath = os.path.join(CACHE_DIR, fname)
                if os.path.isfile(fpath):
                    count += 1
                    total_size += os.path.getsize(fpath)

        return {
            "cached_files_count": count,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "cache_dir": CACHE_DIR,
            "max_age_hours": MAX_CACHE_AGE_SECONDS / 3600,
        }

    def _prune_expired(self):
        """Removes files older than 24 hours on initialization."""
        now = time.time()
        if not os.path.exists(CACHE_DIR):
            return
        for fname in os.listdir(CACHE_DIR):
            fpath = os.path.join(CACHE_DIR, fname)
            if os.path.isfile(fpath):
                try:
                    if now - os.path.getmtime(fpath) > MAX_CACHE_AGE_SECONDS:
                        os.remove(fpath)
                except Exception:
                    pass

audio_cache = AudioCache()

