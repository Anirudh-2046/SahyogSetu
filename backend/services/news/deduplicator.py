"""
Deduplicator and Amendment Tracker for Government Announcements
Prevents duplicate items using:
- Normalized canonical URL matching (protocol, query params, trailing slash stripping)
- Content SHA-256 hash checks
- Headline token Jaccard similarity matching
- Amendment and revision detection (Corrigendum, Extension, Amendment linking)
"""

import hashlib
import re
from typing import Set, List, Dict, Any, Optional, Tuple

class Deduplicator:
    """Detects duplicate news items and tracks official amendments."""

    AMENDMENT_TERMS = {
        "amendment", "amended", "corrigendum", "revised", "revision",
        "extension", "addendum", "modification", "clarification", "gazette notification",
    }

    def __init__(self):
        self.seen_urls: Set[str] = set()
        self.seen_hashes: Set[str] = set()
        self.seen_headlines: Set[str] = set()
        # Maps canonical hash/url to news_id for linking duplicates/amendments
        self.canonical_id_map: Dict[str, str] = {}

    @staticmethod
    def canonical_url(url: str) -> str:
        """Strips tracking queries, hash fragments, and trailing slashes."""
        if not url:
            return ""
        # Remove query parameters and fragments
        url = url.split("#")[0].split("?")[0].rstrip("/").lower()
        # Normalize protocol https/http
        url = re.sub(r"^https?://(www\.)?", "", url)
        return url

    @staticmethod
    def compute_hash(text: str) -> str:
        """Generates SHA-256 content signature."""
        normalized = re.sub(r"\W+", "", (text or "").lower())
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    @staticmethod
    def normalize_headline(headline: str) -> str:
        """Reduces headline to basic alphanumeric tokens."""
        return re.sub(r"\W+", " ", (headline or "").lower()).strip()

    @classmethod
    def get_tokens(cls, text: str) -> Set[str]:
        """Extracts significant tokens for similarity matching."""
        tokens = set(re.findall(r"\b\w{3,}\b", (text or "").lower()))
        # Remove ultra-common noise words
        stop_words = {"the", "and", "for", "with", "from", "under", "all", "has", "have", "been", "per"}
        return tokens - stop_words

    @classmethod
    def calculate_jaccard_similarity(cls, text1: str, text2: str) -> float:
        """Calculates token Jaccard similarity between two texts."""
        tokens1 = cls.get_tokens(text1)
        tokens2 = cls.get_tokens(text2)
        if not tokens1 or not tokens2:
            return 0.0
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        return len(intersection) / len(union) if union else 0.0

    @classmethod
    def is_amendment(cls, headline: str, description: str = "") -> bool:
        """Checks if the announcement is an amendment, corrigendum, or extension."""
        combined = f"{headline} {description}".lower()
        return any(re.search(r"\b" + re.escape(term) + r"\b", combined) for term in cls.AMENDMENT_TERMS)

    def is_duplicate(self, url: str, headline: str, content: str = "") -> bool:
        """
        Standard duplicate check for streaming ingestion.
        Returns True if item is a duplicate.
        """
        can_url = self.canonical_url(url)
        c_hash = self.compute_hash(content or headline)
        norm_hl = self.normalize_headline(headline)

        if can_url and can_url in self.seen_urls:
            return True
        if c_hash in self.seen_hashes:
            return True
        if norm_hl and norm_hl in self.seen_headlines:
            return True

        if can_url:
            self.seen_urls.add(can_url)
        self.seen_hashes.add(c_hash)
        if norm_hl:
            self.seen_headlines.add(norm_hl)

        return False

    def check_duplicate_or_amendment(
        self,
        item: Dict[str, Any],
        existing_items: List[Dict[str, Any]],
        similarity_threshold: float = 0.80,
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Inspects item against a list of existing database items.
        Returns: (is_duplicate: bool, duplicate_of_id: Optional[str], reason: Optional[str])
        """
        item_url = self.canonical_url(item.get("source_url") or item.get("original_source_url", ""))
        item_hl = item.get("headline_original", "") or item.get("headline", "")
        item_desc = item.get("description_original", "") or item.get("description", "")
        item_hash = self.compute_hash(item_hl + " " + item_desc)

        for existing in existing_items:
            ex_id = existing.get("news_id") or existing.get("id")
            if not ex_id:
                continue

            ex_url = self.canonical_url(existing.get("source_url") or existing.get("original_source_url", ""))
            ex_hl = existing.get("headline_original", "") or existing.get("headline", "")
            ex_desc = existing.get("description_original", "") or existing.get("description", "")
            ex_hash = self.compute_hash(ex_hl + " " + ex_desc)

            # 1. Exact canonical URL match
            if item_url and ex_url and item_url == ex_url:
                return True, ex_id, "exact_canonical_url"

            # 2. Exact content hash match
            if item_hash == ex_hash:
                return True, ex_id, "exact_content_hash"

            # 3. Token similarity check
            similarity = self.calculate_jaccard_similarity(item_hl, ex_hl)
            is_amend = self.is_amendment(item_hl, item_desc)
            effective_threshold = 0.50 if is_amend else similarity_threshold

            if similarity >= effective_threshold:
                if is_amend:
                    return False, ex_id, f"amendment_linked (similarity={similarity:.2f})"
                if similarity >= similarity_threshold:
                    return True, ex_id, f"high_similarity (score={similarity:.2f})"

        return False, None, None


