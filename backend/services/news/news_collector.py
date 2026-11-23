"""
News Collector Service
Orchestrates collection across all independent government connectors,
runs the NLP normalization pipeline, verifies official sources and direct documents,
and saves records into the database.
Guarantees fault-isolation: one unavailable source never blocks others.
"""

import hashlib
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

from .web_connectors import (
    PIBWebConnector,
    PunjabGovWebConnector,
    HaryanaGovWebConnector,
    JKGovWebConnector,
    MinistryOfCooperationWebConnector,
    VerifiedGazetteConnector,
)
from .rss_connectors import OfficialGovRssConnector
from .api_connectors import OfficialGovApiConnector
from .text_cleaner import TextCleaner
from .language_detector import LanguageDetector
from .news_classifier import NewsClassifier
from .jurisdiction_classifier import JurisdictionClassifier
from .summarizer import NewsSummarizer
from .translator import NewsTranslator
from .relevance_analyzer import RelevanceAnalyzer
from .deduplicator import Deduplicator
from .source_registry import SourceRegistry
from .source_verifier import SourceVerifier
from ...database import save_news_item, update_source_status, get_news_items

try:
    from backend.ml.inference.news_inference import news_predictor
except Exception as e:
    news_predictor = None

logger = logging.getLogger("sahyogsetu.news.collector")

class NewsCollector:
    """Manages independent connectors and runs the complete NLP ingestion pipeline."""

    def __init__(self):
        self.deduplicator = Deduplicator()
        self.source_registry = SourceRegistry()
        self.source_verifier = SourceVerifier()
        
        # Instantiate connectors
        self.api_connectors = [
            OfficialGovApiConnector("pib_api", "PIB Official API", "PIB_API_URL", "PIB_API_KEY"),
            OfficialGovApiConnector("coop_api", "Ministry of Cooperation API", "COOP_API_URL", "COOP_API_KEY"),
        ]
        
        self.rss_connectors = [
            OfficialGovRssConnector("pib_rss_main", "PIB Official RSS (All)", "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1", "central", "en"),
            OfficialGovRssConnector("pib_rss_hi", "PIB Official RSS (Hindi)", "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=2", "central", "hi"),
        ]
        
        self.web_connectors = [
            PIBWebConnector(),
            PunjabGovWebConnector(),
            HaryanaGovWebConnector(),
            JKGovWebConnector(),
            MinistryOfCooperationWebConnector(),
            VerifiedGazetteConnector(),
        ]

    async def collect_and_process_all(self) -> Dict[str, Any]:
        """Runs collection across all connectors with full fault-isolation."""
        total_collected = 0
        total_new_saved = 0
        now_str = datetime.now().isoformat()

        # Load existing items to perform duplicate and amendment matching
        existing_items = get_news_items("all", limit=500)

        all_connectors = []
        for ac in self.api_connectors:
            all_connectors.append(("api", ac.source_id, ac.name, "central", getattr(ac, "base_url", "api"), ac))
        for rc in self.rss_connectors:
            all_connectors.append(("rss", rc.source_id, rc.name, rc.jurisdiction, rc.feed_url, rc))
        for wc in self.web_connectors:
            all_connectors.append(("web", wc.source_id, wc.name, getattr(wc, "jurisdiction", "central"), getattr(wc, "source_id", "web"), wc))

        for conn_type, s_id, s_name, j_code, url, connector in all_connectors:
            try:
                raw_items = await connector.fetch_announcements()
                count = len(raw_items)
                total_collected += count

                # Update operational status
                status = "operational" if count > 0 else "active_zero_items"
                update_source_status(s_id, s_name, j_code, url, conn_type, status, count, f"Fetched {count} items.")

                # Process each item through NLP pipeline
                for raw in raw_items:
                    processed = self.process_raw_item(raw, s_name, existing_items)
                    if processed:
                        # Check duplicate / amendment status
                        is_dup, dup_of_id, reason = self.deduplicator.check_duplicate_or_amendment(
                            processed, existing_items
                        )
                        if is_dup:
                            logger.info("Skipping duplicate announcement (%s): %s", reason, processed["headline_original"])
                            continue
                        elif dup_of_id:
                            # It is an amendment linked to an earlier notification!
                            processed["duplicate_of"] = dup_of_id
                            logger.info("Linked amendment to %s: %s", dup_of_id, processed["headline_original"])

                        if save_news_item(processed):
                            total_new_saved += 1
                            existing_items.append(processed)
            except Exception as e:
                logger.error("Connector %s failed: %s", s_name, e)
                update_source_status(s_id, s_name, j_code, url, conn_type, "error", 0, str(e))

        return {
            "timestamp": now_str,
            "total_raw_collected": total_collected,
            "total_new_saved": total_new_saved,
        }

    def process_raw_item(
        self,
        raw: Dict[str, Any],
        default_source_name: str,
        existing_items: Optional[List[Dict[str, Any]]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Executes full verification and NLP pipeline on a single raw announcement."""
        headline = TextCleaner.clean(raw.get("headline", ""))
        desc = TextCleaner.clean(raw.get("description", ""))
        if not headline:
            return None

        full_text = TextCleaner.clean(raw.get("full_text_original", desc))
        combined_text = f"{headline}. {desc}"

        # Stage B: Language identification
        lang, _ = LanguageDetector.detect(combined_text)

        # Stage C: News category classification (Prefer Phase 6 ML Model)
        category = None
        cat_conf = 0.85
        model_version = "rule_based_v1"
        if news_predictor is not None:
            try:
                pred = news_predictor.predict_category(combined_text)
                if pred and not pred.get("is_uncertain", False):
                    category = pred.get("predicted_category")
                    cat_conf = pred.get("confidence", 0.85)
                    model_version = "phase6_logistic_regression_v1"
            except Exception as e:
                logger.warning("ML news predictor failed, falling back: %s", e)

        if not category:
            category, cat_conf, _ = NewsClassifier.classify(combined_text, raw)

        # Stage D: Jurisdiction classification
        jurisdiction, central_rel, j_conf, _ = JurisdictionClassifier.classify(combined_text, raw)

        # Stage E: Source and direct document verification
        raw_source_url = raw.get("source_url") or raw.get("original_source_url", "")
        raw_doc_url = raw.get("document_url", "")
        verification_report = self.source_verifier.verify_source(raw_source_url, raw_doc_url)

        # Content hash for deduplication
        c_hash = hashlib.sha256(f"{headline}_{raw_source_url}".encode("utf-8")).hexdigest()
        news_id = f"news_{jurisdiction}_{c_hash[:12]}"

        # Stage F: Entity keywords
        keywords = [category, jurisdiction]
        for term in ["pacs", "kcc", "ots", "pmfby", "amendment", "arbitration", "registration"]:
            if term in combined_text.lower():
                keywords.append(term)

        # Stage G: Structured & concise summarization
        structured_summary = NewsSummarizer.generate_structured_summary(
            headline=headline,
            description=desc,
            issuing_department=raw.get("issuing_department", default_source_name),
            jurisdiction=jurisdiction,
        )
        summary_orig = structured_summary["concise_summary"]

        # Stage H: Multilingual translation
        translated_headlines = NewsTranslator.translate_headline(headline, lang)
        translated_summaries = NewsTranslator.translate_summary(summary_orig, lang)

        # Stage I: Relevance explanation
        partial_item = {
            "jurisdiction": jurisdiction,
            "issuing_department": raw.get("issuing_department", default_source_name),
            "category": category,
            "central_relevance": central_rel or raw.get("central_relevance", False),
        }
        relevance_exp = RelevanceAnalyzer.generate_explanation(partial_item)

        pub_date = raw.get("publication_date", datetime.now().strftime("%Y-%m-%d"))

        # Relevance scoring (0.0 to 1.0)
        relevance_score = 0.85
        if cat_conf > 0.70:
            relevance_score += 0.05
        if verification_report["is_official_document"]:
            relevance_score += 0.10
        relevance_score = min(round(relevance_score, 2), 1.0)

        now_iso = datetime.now().isoformat()

        return {
            "news_id": news_id,
            "headline_original": headline,
            "description_original": desc,
            "full_text_original": full_text,
            "source_name": raw.get("source_name", default_source_name),
            "source_type": raw.get("source_type", "official_government"),
            "source_url": verification_report["source_url"],
            "original_source_url": verification_report["source_url"],
            "document_url": verification_report["document_url"],
            "source_title": raw.get("source_title", headline),
            "source_reference_number": raw.get("source_reference_number", ""),
            "official_translation_url": raw.get("official_translation_url", ""),
            "translated_source_language": raw.get("translated_source_language", ""),
            "source_verified": verification_report["is_official_source"],
            "source_verification_status": verification_report["official_source_status"],
            "official_source_status": verification_report["official_source_status"],
            "official_document_status": verification_report["official_document_status"],
            "duplicate_of": raw.get("duplicate_of"),
            "relevance_score": relevance_score,
            "model_version": model_version,
            "translation_status": "completed",
            "summary_status": "completed",
            "last_verified_at": raw.get("last_verified_at", now_iso),
            "publication_date": pub_date,
            "fetched_at": now_iso,
            "updated_at": now_iso,
            "jurisdiction": jurisdiction,
            "issuing_department": raw.get("issuing_department", default_source_name),
            "original_language": lang,
            "category": category,
            "keywords": keywords,
            "target_audience": "Cooperative Society Members & Farmers",
            "central_relevance": central_rel or raw.get("central_relevance", False),
            "summary_original": summary_orig,
            "summary_translated": translated_summaries,
            "relevance_explanation": relevance_exp,
            "headline_translated": translated_headlines,
            "verification_status": verification_report["official_source_status"],
            "content_hash": c_hash,
        }


