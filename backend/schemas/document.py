"""
Document & Ingestion Pydantic Schemas
Defines validation contracts for legal document analysis, chunking,
inventory listing, and vector database ingestion status.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class DocumentAnalysisResponse(BaseModel):
    documentId: str = Field(..., description="Unique document record ID")
    filename: str = Field(..., description="Uploaded file name")
    fileSizeBytes: int = Field(..., description="File size in bytes")
    detectedLanguage: str = Field("en", description="Detected language code")
    extractedTextPreview: str = Field(..., description="Snippet of extracted text")
    detectedSections: List[str] = Field(default_factory=list, description="List of detected statutory sections or headings")
    relevantClauses: List[str] = Field(default_factory=list, description="Extracted legal clauses and rules")
    extractionQuality: str = Field("ok", description="Extraction quality: ok, needs_review, check_garbled")
    pageReferences: List[int] = Field(default_factory=list, description="Pages containing extracted content")
    processingStatus: str = Field("analyzed", description="Processing status")
    disclaimer: str = Field(
        "Extracted clauses are generated via automated analysis and do not constitute certified legal counsel.",
        description="Statutory non-advice disclaimer"
    )
    assistantExplanation: Dict[str, Any] = Field(..., description="Structured legal breakdown")
    source: str = "live_backend"

class DocumentItemResponse(BaseModel):
    doc_id: str
    title: str
    module: str
    jurisdiction: str
    state: str
    doc_type: str
    language: str
    declared_language: str
    source_url: str
    version_or_year: str
    pages: int
    scanned: str
    text_quality: str
    manifest_status: str
    processing_status: str
    duplicate_of: Optional[str] = None
    sha256: str
    file_present: bool
    indexed: bool

class DocumentListResponse(BaseModel):
    documents: List[DocumentItemResponse] = Field(default_factory=list)
    total: int = 0
    total_indexed: int = 0
    filters_applied: Dict[str, Any] = Field(default_factory=dict)
    source: str = "live_backend"

class DocumentStatusResponse(BaseModel):
    total_manifest_documents: int
    total_vectors_stored: int
    total_indexed_documents: int
    status_breakdown: Dict[str, int]
    embedding_model: Dict[str, Any]
    vector_store_path: str
    source: str = "live_backend"

class IngestionReportResponse(BaseModel):
    timestamp: str
    total_documents: int
    total_pages_declared: int
    total_vectors_stored: int
    indexed_documents_count: int
    jurisdiction_distribution: Dict[str, int]
    language_distribution: Dict[str, int]
    documents_requiring_review: List[Dict[str, Any]]
    review_count: int
    source: str = "live_backend"

class DocumentIngestResponse(BaseModel):
    doc_id: str
    status: str
    title: Optional[str] = None
    jurisdiction: Optional[str] = None
    chunks_count: Optional[int] = None
    pages_processed: Optional[int] = None
    extraction_method: Optional[str] = None
    message: Optional[str] = None
    duplicate_of: Optional[str] = None
    source_url: Optional[str] = None
    timestamp: Optional[str] = None

class BatchIngestResponse(BaseModel):
    total_documents_evaluated: int
    indexed_count: int
    skipped_count: int
    missing_file_count: int
    total_chunks_created: int
    total_vectors_in_store: int
    results: List[Dict[str, Any]]
    timestamp: str

class DocumentReindexResponse(BaseModel):
    doc_id: str
    previous_chunks_deleted: int
    reindex_result: Dict[str, Any]
