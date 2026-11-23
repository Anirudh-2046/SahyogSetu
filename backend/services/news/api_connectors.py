"""
API Connectors for Official Government News Sources
Prioritizes genuine official REST/JSON APIs where provided by government ministries.
Uses environment variables for any credentials.
Never invents endpoints or fake credentials.
"""

import os
import logging
from typing import List, Dict, Any, Optional

from ...security.ssrf_protection import safe_fetch_url, SSRFValidationError

logger = logging.getLogger("sahyogsetu.news.api")

class OfficialGovApiConnector:
    """Connector for official government APIs when configured via environment variables."""

    def __init__(self, source_id: str, name: str, base_url_env_var: str, api_key_env_var: Optional[str] = None):
        self.source_id = source_id
        self.name = name
        self.base_url = os.getenv(base_url_env_var, "").strip()
        self.api_key = os.getenv(api_key_env_var, "").strip() if api_key_env_var else None

    def is_configured(self) -> bool:
        return bool(self.base_url)

    async def fetch_announcements(self) -> List[Dict[str, Any]]:
        """Fetches from official API if endpoint is configured; returns empty list if not configured."""
        if not self.is_configured():
            logger.info("Official API endpoint not configured for %s (no public REST API exposed).", self.name)
            return []

        headers = {"User-Agent": "SahyogSetu-OfficialCollector/1.0"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            resp = await safe_fetch_url(self.base_url, headers=headers, timeout=10.0)
            if resp.status_code == 200:
                data = resp.json()
                # Expect array or items wrapper
                items = data.get("items", data) if isinstance(data, dict) else data
                if isinstance(items, list):
                    return items
            else:
                logger.warning("API for %s returned status %d", self.name, resp.status_code)
        except Exception as e:
            logger.error("Error querying API for %s: %s", self.name, e)

        return []

