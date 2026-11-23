"""
RSS/Atom Feed Connectors for Official Government Feeds
Fetches announcements from verified government RSS feeds.
"""

import ssl
import logging
from typing import List, Dict, Any
import feedparser

from ...security.ssrf_protection import safe_fetch_url, SSRFValidationError

logger = logging.getLogger("sahyogsetu.news.rss")

class OfficialGovRssConnector:
    """Connects to official RSS/Atom feeds provided by government agencies."""

    def __init__(self, source_id: str, name: str, feed_url: str, jurisdiction: str, default_lang: str = "en"):
        self.source_id = source_id
        self.name = name
        self.feed_url = feed_url
        self.jurisdiction = jurisdiction
        self.default_lang = default_lang

    async def fetch_announcements(self) -> List[Dict[str, Any]]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SahyogSetu/1.0",
            "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml;q=0.9",
        }
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.options |= 0x4  # SSL_OP_LEGACY_SERVER_CONNECT

        items = []
        try:
            resp = await safe_fetch_url(self.feed_url, timeout=8.0, headers=headers)
            if resp.status_code == 200:
                feed = feedparser.parse(resp.content)
                for entry in feed.entries:
                    title = entry.get("title", "").strip()
                    link = entry.get("link", "").strip()
                    summary = entry.get("summary", "") or entry.get("description", "")
                    published = entry.get("published", "") or entry.get("updated", "")
                    if title and link:
                        items.append({
                            "headline": title,
                            "description": summary,
                            "source_url": link,
                            "publication_date": published,
                            "source_name": self.name,
                            "jurisdiction": self.jurisdiction,
                            "source_type": "official_government",
                            "original_language": self.default_lang,
                        })
        except Exception as e:
            logger.warning("RSS fetch failed for %s (%s): %s", self.name, self.feed_url, e)

        return items

