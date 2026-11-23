"""
SahyogSetu News Aggregation & Multilingual Service
High-level service interface for querying jurisdiction-aware news,
fetching multilingual translations, inspecting source health, and scheduling background updates.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from .news_collector import NewsCollector
from .news_scheduler import news_scheduler
from .source_registry import SourceRegistry
from .source_verifier import SourceVerifier
from .source_audit import run_source_audit
from ...database import (
    init_db,
    query_news,
    count_news,
    get_news_item_by_id,
    save_news_item,
    get_all_source_statuses,
    get_news_verification_report,
)

logger = logging.getLogger("sahyogsetu.news.service")

class NewsService:
    """Service facade for the frontend and FastAPI API routers."""

    def __init__(self):
        init_db()
        self.collector = NewsCollector()
        self.registry = SourceRegistry()
        self.verifier = SourceVerifier()
        self.scheduler = news_scheduler

    async def get_news_feed(
        self,
        jurisdiction: str = "all",
        language: str = "en",
        limit: int = 20,
        offset: int = 0,
        category: Optional[str] = None,
        department: Optional[str] = None,
        document_type: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves jurisdiction-filtered news formatted for the requested interface language.
        Supports faceted filtering across category, department, document_type, and dates.
        If database is empty on first boot, seeds from verified gazettes.
        """
        total = count_news(
            jurisdiction=jurisdiction,
            category=category,
            department=department,
            document_type=document_type,
            date_from=date_from,
            date_to=date_to,
        )
        if total == 0 and jurisdiction == "all" and not category:
            logger.info("Database empty on query for %s; triggering initial ingestion.", jurisdiction)
            await self.collector.collect_and_process_all()
            total = count_news(
                jurisdiction=jurisdiction,
                category=category,
                department=department,
                document_type=document_type,
                date_from=date_from,
                date_to=date_to,
            )

        raw_items = query_news(
            jurisdiction=jurisdiction,
            limit=limit,
            offset=offset,
            category=category,
            department=department,
            document_type=document_type,
            date_from=date_from,
            date_to=date_to,
        )

        # Format items for frontend consumption
        formatted_items = []
        for item in raw_items:
            h_trans = item.get("headline_translated", {})
            s_trans = item.get("summary_translated", {})
            r_trans = item.get("relevance_explanation", {})

            # Select language text with fallback to English
            headline = h_trans.get(language) or h_trans.get("en") or item.get("headline_original")
            summary = s_trans.get(language) or s_trans.get("en") or item.get("summary_original")
            why_exp = r_trans.get(language) or r_trans.get("en") or ""

            orig_lang = item.get("original_language", "en")
            has_official_trans = bool(item.get("official_translation_url")) and item.get("translated_source_language") == language
            is_ai_trans = (language != orig_lang) and not has_official_trans
            trans_status_note = (
                f"Official {language.upper()} version available."
                if has_official_trans
                else f"AI-translated summary in {language.upper()}; official {language.upper()} version unavailable. Original {orig_lang.upper()} authoritative document preserved."
                if is_ai_trans
                else f"Original {orig_lang.upper()} official text."
            )

            direct_doc_url = item.get("document_url")
            source_url = item.get("original_source_url") or item.get("source_url") or ""

            formatted_items.append({
                "news_id": item["news_id"],
                "id": item["news_id"],
                "headline": h_trans if h_trans else {"en": headline},
                "summary": s_trans if s_trans else {"en": summary},
                "headline_display": headline,
                "summary_display": summary,
                "why_explanation_display": why_exp,
                "why_explanation": r_trans,
                "sourceName": item["source_name"],
                "source_name": item["source_name"],
                "sourceType": "official_announcement" if item.get("source_type") != "media" else "media_report",
                "source_type": item.get("source_type", "official_government"),
                "officialUrl": source_url,
                "source_url": source_url,
                "original_source_url": source_url,
                "document_url": direct_doc_url,
                "source_title": item.get("source_title", item.get("headline_original", "")),
                "source_reference_number": item.get("source_reference_number", ""),
                "official_translation_url": item.get("official_translation_url", ""),
                "translated_source_language": item.get("translated_source_language", ""),
                "source_verified": bool(item.get("source_verified", 1)),
                "source_verification_status": item.get("source_verification_status", "verified_official_document"),
                "official_source_status": item.get("official_source_status", "verified_official_source"),
                "official_document_status": item.get("official_document_status", "verified_official_document" if direct_doc_url else "verified_official_article"),
                "duplicate_of": item.get("duplicate_of"),
                "relevance_score": float(item.get("relevance_score", 1.0)),
                "model_version": item.get("model_version", "phase6_logistic_regression_v1"),
                "translation_status": item.get("translation_status", "completed"),
                "summary_status": item.get("summary_status", "completed"),
                "last_verified_at": item.get("last_verified_at", ""),
                "updated_at": item.get("updated_at", ""),
                "is_ai_translation": is_ai_trans,
                "translation_status_note": trans_status_note,
                "publicationDate": item["publication_date"],
                "publication_date": item["publication_date"],
                "jurisdiction": item["jurisdiction"],
                "category": item["category"],
                "issuingAuthority": {
                    "en": item["issuing_department"],
                    "hi": item["issuing_department"],
                    "pa": item["issuing_department"],
                    "doi": item["issuing_department"],
                    "bgc": item["issuing_department"],
                },
                "issuing_department": item["issuing_department"],
                "original_language": orig_lang,
                "central_relevance": item.get("central_relevance", False),
                "verification_status": item.get("verification_status", "verified_official"),
            })

        return {
            "items": formatted_items,
            "totalAvailable": total,
            "total_available": total,
            "filterApplied": jurisdiction,
            "filter_applied": jurisdiction,
            "categoryFilter": category,
            "documentTypeFilter": document_type,
            "language": language,
            "limit": limit,
            "offset": offset,
            "sourceStatus": "live_feed" if total > 0 else "empty",
            "source_status": "live_feed" if total > 0 else "empty",
            "lastUpdated": datetime.now().strftime("%I:%M %p"),
            "last_updated": datetime.now().isoformat(),
        }

    async def get_news_detail(self, news_id: str) -> Optional[Dict[str, Any]]:
        return get_news_item_by_id(news_id)

    async def get_news_translation(self, news_id: str, language: str) -> Optional[Dict[str, Any]]:
        item = get_news_item_by_id(news_id)
        if not item:
            return None
        h_trans = item.get("headline_translated", {})
        s_trans = item.get("summary_translated", {})
        r_trans = item.get("relevance_explanation", {})
        return {
            "news_id": news_id,
            "language": language,
            "headline": h_trans.get(language) or h_trans.get("en") or item.get("headline_original"),
            "summary": s_trans.get(language) or s_trans.get("en") or item.get("summary_original"),
            "relevance_explanation": r_trans.get(language) or r_trans.get("en") or "",
        }

    async def get_sources_status(self) -> List[Dict[str, Any]]:
        """Returns status of monitored sources, combining registry and database logs."""
        db_statuses = {s["source_id"]: s for s in get_all_source_statuses()}
        combined = []
        for reg in self.registry.get_all_sources():
            s_id = reg.get("source_id")
            db_s = db_statuses.get(s_id, {})
            combined.append({
                "source_id": s_id,
                "name": reg.get("name"),
                "jurisdiction": reg.get("jurisdiction"),
                "url": reg.get("base_url"),
                "direct_document_url": reg.get("announcement_page"),
                "source_type": reg.get("collection_method"),
                "official_status": reg.get("verification_status"),
                "rate_limit_policy": reg.get("rate_limit_policy"),
                "last_status": db_s.get("last_status", "operational"),
                "last_fetched_at": db_s.get("last_fetched_at"),
                "items_collected": db_s.get("items_collected", 0),
                "notes": db_s.get("notes") or reg.get("notes"),
            })
        return combined

    async def get_verification_report(self) -> Dict[str, Any]:
        """Returns comprehensive verification and provenance report."""
        return get_news_verification_report()

    async def reprocess_news_item(self, news_id: str) -> Optional[Dict[str, Any]]:
        """Reprocesses an existing news item through Phase 6 NLP/ML pipeline."""
        item = get_news_item_by_id(news_id)
        if not item:
            return None

        # Build raw structure and re-process
        raw = {
            "headline": item["headline_original"],
            "description": item["description_original"],
            "full_text_original": item.get("full_text_original", ""),
            "source_url": item.get("source_url") or item.get("original_source_url", ""),
            "original_source_url": item.get("original_source_url") or item.get("source_url", ""),
            "document_url": item.get("document_url", ""),
            "source_name": item["source_name"],
            "issuing_department": item["issuing_department"],
            "publication_date": item["publication_date"],
            "source_type": item["source_type"],
            "duplicate_of": item.get("duplicate_of"),
        }

        reprocessed = self.collector.process_raw_item(raw, item["source_name"])
        if reprocessed:
            reprocessed["news_id"] = news_id  # Keep original ID
            save_news_item(reprocessed)
            return get_news_item_by_id(news_id)
        return item

    async def run_audit(self) -> List[Dict[str, Any]]:
        return run_source_audit()

    async def refresh_all(self) -> Dict[str, Any]:
        return await self.collector.collect_and_process_all()

news_service = NewsService()


