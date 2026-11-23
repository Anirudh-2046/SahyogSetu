"""
Official Government News API Router
Serves verified government announcements, circulars, Gazette links, direct documents,
and NLP/ML summaries.
"""

from fastapi import APIRouter, Query, HTTPException, BackgroundTasks, Depends
from typing import Optional
import logging

from ..services.news.news_service import news_service
from ..services.news.news_scheduler import news_scheduler
from ..database import count_news
from ..security.auth import verify_admin_key

logger = logging.getLogger("sahyogsetu.api.news")

router = APIRouter(prefix="/api/news", tags=["News"])

@router.get("")
async def get_news(
    jurisdiction: str = Query("all", description="Jurisdiction filter: all, central, punjab, haryana, jk"),
    language: str = Query("en", description="Interface language: en, hi, pa, doi, bgc"),
    category: Optional[str] = Query(None, description="Cooperative category sector filter"),
    department: Optional[str] = Query(None, description="Department name substring filter"),
    document_type: Optional[str] = Query(None, description="Document type filter: official_document, pdf, article"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Retrieves news feed with direct government source documents and translated summaries."""
    # Normalize values if invoked directly in test harnesses
    if not isinstance(jurisdiction, str):
        jurisdiction = getattr(jurisdiction, "default", "all")
    if not isinstance(language, str):
        language = getattr(language, "default", "en")
    if not isinstance(category, str):
        category = getattr(category, "default", None)
    if not isinstance(department, str):
        department = getattr(department, "default", None)
    if not isinstance(document_type, str):
        document_type = getattr(document_type, "default", None)
    if not isinstance(date_from, str):
        date_from = getattr(date_from, "default", None)
    if not isinstance(date_to, str):
        date_to = getattr(date_to, "default", None)
    if not isinstance(limit, int):
        limit = getattr(limit, "default", 20)
    if not isinstance(offset, int):
        offset = getattr(offset, "default", 0)

    valid_jurisdictions = ["all", "central", "punjab", "haryana", "jk"]
    if jurisdiction not in valid_jurisdictions:
        jurisdiction = "all"

    valid_languages = ["en", "hi", "pa", "doi", "bgc"]
    if language not in valid_languages:
        language = "en"

    return await news_service.get_news_feed(
        jurisdiction=jurisdiction,
        language=language,
        limit=limit,
        offset=offset,
        category=category,
        department=department,
        document_type=document_type,
        date_from=date_from,
        date_to=date_to,
    )

@router.get("/status")
async def get_news_system_status():
    """Returns news system metrics, jurisdiction announcement totals, and scheduler status."""
    verification_summary = await news_service.get_verification_report()
    return {
        "status": "operational",
        "total_announcements": count_news("all"),
        "jurisdiction_counts": {
            "central": count_news("central"),
            "punjab": count_news("punjab"),
            "haryana": count_news("haryana"),
            "jk": count_news("jk"),
        },
        "supported_languages": ["en", "hi", "pa", "doi", "bgc"],
        "scheduler": news_scheduler.get_status(),
        "verification_summary": {
            "verified_official_sources": verification_summary["verified_official_sources"],
            "verified_direct_documents": verification_summary["verified_direct_documents"],
            "articles_or_pending": verification_summary["articles_or_pending_documents"],
            "duplicate_records": verification_summary["duplicate_records"],
        },
    }

@router.get("/sources")
async def get_sources():
    """Returns operational status and registered metadata of monitored official connectors."""
    statuses = await news_service.get_sources_status()
    return {"sources": statuses, "count": len(statuses)}

@router.get("/verification-report")
async def get_verification_report():
    """Returns official source document verification report distinguishing direct docs from articles."""
    return await news_service.get_verification_report()

@router.post("/collect")
async def trigger_collection(_authorized: bool = Depends(verify_admin_key)):
    """Manual or admin trigger to collect and process all official news sources synchronously (Admin authorized)."""
    result = await news_service.refresh_all()
    return {
        "status": "collection_completed",
        "result": result,
        "verification_report": await news_service.get_verification_report(),
    }

@router.post("/refresh")
async def refresh_news(background_tasks: BackgroundTasks, _authorized: bool = Depends(verify_admin_key)):
    """Triggers background news collection from official connectors (Admin authorized)."""
    background_tasks.add_task(news_service.refresh_all)
    return {"status": "refresh_initiated", "message": "News aggregation triggered."}

@router.post("/reprocess/{news_id}")
async def reprocess_news(news_id: str, _authorized: bool = Depends(verify_admin_key)):
    """Reprocesses a specific news announcement through the Phase 6 NLP/ML pipeline (Admin authorized)."""
    item = await news_service.reprocess_news_item(news_id)
    if not item:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return {"status": "reprocessed", "item": item}

@router.get("/audit")
async def run_audit(_authorized: bool = Depends(verify_admin_key)):
    """Performs live connectivity audit of government targets (Admin authorized)."""
    report = await news_service.run_audit()
    return {"audit_report": report, "targets_evaluated": len(report)}

@router.get("/{news_id}")
async def get_news_detail(news_id: str):
    """Retrieves single news announcement detail."""
    item = await news_service.get_news_detail(news_id)
    if not item:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return item

