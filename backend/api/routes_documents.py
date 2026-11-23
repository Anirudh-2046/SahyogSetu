"""
Document Intelligence & Ingestion API Router
Provides endpoints for:
1. Citizen document analysis & clause extraction (/api/documents/analyze)
2. Document inventory listing with filters (/api/documents)
3. Document metadata details (/api/documents/{doc_id})
4. Document ingestion and batch processing (/api/documents/ingest)
5. Reindexing and status reporting (/api/documents/status, /api/documents/ingestion-report)
"""

from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, Query, HTTPException, Depends
import logging

from ..schemas.document import (
    DocumentAnalysisResponse,
    DocumentListResponse,
    DocumentItemResponse,
    DocumentStatusResponse,
    IngestionReportResponse,
    DocumentIngestResponse,
    BatchIngestResponse,
    DocumentReindexResponse,
)
from ..services.document_service import document_service
from ..services.ingestion.ingestion_service import ingestion_service
from ..exceptions import EntityNotFoundException, FileTooLargeException
from ..security.auth import verify_admin_key
from ..security.input_sanitizer import sanitize_filename
from ..config import settings

logger = logging.getLogger("sahyogsetu.api.documents")

router = APIRouter(prefix="/api/documents", tags=["Documents"])

@router.post("/analyze", response_model=DocumentAnalysisResponse)
async def analyze_document(
    document: UploadFile = File(..., description="Uploaded statutory document (PDF or text)"),
    query: Optional[str] = Form(None, description="Citizen inquiry regarding the document"),
    language: str = Form("en", description="Interface language code"),
    jurisdiction: str = Form("all", description="Target jurisdiction filter"),
):
    """
    Accepts uploaded PDF/text document, extracts text and legal clauses,
    records to database, and produces grounded legal assistance.
    """
    raw_filename = document.filename or "uploaded_document"
    clean_filename = sanitize_filename(raw_filename)
    lower_name = clean_filename.lower()

    # Enforce extension whitelist
    if not (lower_name.endswith(".pdf") or lower_name.endswith(".txt")):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only statutory PDF (.pdf) and plain text (.txt) documents are accepted.",
        )

    # Read contents with bounded size check
    contents = await document.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds maximum upload size limit of {int(settings.MAX_UPLOAD_SIZE_BYTES / (1024 * 1024))} MB.",
        )

    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded document is empty.")

    # Magic-byte check for PDF files
    if lower_name.endswith(".pdf") and not contents.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="Malformed PDF: missing %PDF magic header.")

    res = await document_service.analyze_document(
        contents=contents,
        filename=clean_filename,
        content_type=document.content_type,
        query=query,
        language=language,
        jurisdiction=jurisdiction,
    )
    return res

@router.get("", response_model=DocumentListResponse)
async def list_documents(
    jurisdiction: Optional[str] = Query(None, description="Filter by jurisdiction: central, punjab, haryana, jk"),
    language: Optional[str] = Query(None, description="Filter by language: en, hi, pa, etc."),
    doc_type: Optional[str] = Query(None, description="Filter by document type: act, rules, guidelines, etc."),
    status: Optional[str] = Query(None, description="Filter by processing status: indexed, pending, file_missing, etc."),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Returns catalog of registered legal documents with metadata and processing status."""
    inventory = ingestion_service.get_inventory()

    # Apply filters safely
    filtered = inventory
    eff_jur = jurisdiction if isinstance(jurisdiction, str) else None
    eff_lang = language if isinstance(language, str) else None
    eff_type = doc_type if isinstance(doc_type, str) else None
    eff_status = status if isinstance(status, str) else None
    eff_limit = limit if isinstance(limit, int) else 50
    eff_offset = offset if isinstance(offset, int) else 0

    if eff_jur and eff_jur.lower() != "all":
        filtered = [d for d in filtered if d["jurisdiction"].lower() == eff_jur.lower()]
    if eff_lang and eff_lang.lower() != "all":
        filtered = [d for d in filtered if d["language"].lower() == eff_lang.lower() or d["declared_language"].lower() == eff_lang.lower()]
    if eff_type:
        filtered = [d for d in filtered if eff_type.lower() in d["doc_type"].lower()]
    if eff_status:
        filtered = [d for d in filtered if d["processing_status"].lower() == eff_status.lower()]

    total_matching = len(filtered)
    total_indexed = sum(1 for d in inventory if d["indexed"])
    sliced = filtered[eff_offset : eff_offset + eff_limit]

    return {
        "documents": sliced,
        "total": total_matching,
        "total_indexed": total_indexed,
        "filters_applied": {
            "jurisdiction": eff_jur,
            "language": eff_lang,
            "doc_type": eff_type,
            "status": eff_status,
        },
        "source": "live_backend",
    }

@router.get("/status", response_model=DocumentStatusResponse)
async def get_ingestion_status():
    """Returns vector database status, chunk counts, and processing state breakdown."""
    return {
        **ingestion_service.get_ingestion_status(),
        "source": "live_backend",
    }

@router.get("/ingestion-report", response_model=IngestionReportResponse)
async def get_ingestion_report():
    """Returns comprehensive document audit and ingestion breakdown."""
    return {
        **ingestion_service.get_ingestion_report(),
        "source": "live_backend",
    }

@router.get("/{doc_id}", response_model=DocumentItemResponse)
async def get_document_by_id(doc_id: str):
    """Retrieves metadata and indexing status for a single document."""
    inventory = ingestion_service.get_inventory()
    matching = [d for d in inventory if d["doc_id"] == doc_id]
    if not matching:
        raise HTTPException(status_code=404, detail=f"Document '{doc_id}' not found in manifest.")
    return matching[0]

@router.post("/ingest", response_model=BatchIngestResponse)
async def ingest_all_documents(
    force: bool = Query(False, description="Whether to re-embed already indexed documents"),
    limit: Optional[int] = Query(None, description="Optional cap on number of documents to ingest"),
    _authorized: bool = Depends(verify_admin_key),
):
    """Triggers batch ingestion across registered manifest documents (Admin authorized)."""
    return ingestion_service.ingest_all(force=force, limit=limit)

@router.post("/ingest/{doc_id}", response_model=DocumentIngestResponse)
async def ingest_single_document(
    doc_id: str,
    force: bool = Query(False, description="Whether to force re-indexing"),
    _authorized: bool = Depends(verify_admin_key),
):
    """Triggers ingestion and vector indexing for a single document (Admin authorized)."""
    res = ingestion_service.ingest_document(doc_id, force=force)
    if res.get("status") == "failed":
        raise HTTPException(status_code=500, detail=res.get("message", "Document ingestion failed"))
    return res

@router.post("/reindex", response_model=BatchIngestResponse)
async def reindex_all_documents(_authorized: bool = Depends(verify_admin_key)):
    """Deletes and rebuilds vector index for all available documents (Admin authorized)."""
    return ingestion_service.ingest_all(force=True)

@router.post("/reindex/{doc_id}", response_model=DocumentReindexResponse)
async def reindex_single_document(doc_id: str, _authorized: bool = Depends(verify_admin_key)):
    """Deletes and re-indexes a specific document (Admin authorized)."""
    return ingestion_service.reindex_document(doc_id)
