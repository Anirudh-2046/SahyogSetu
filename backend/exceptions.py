"""
SahyogSetu Custom Application Exceptions and Exception Handlers
Provides uniform, strongly-typed error responses for all API endpoints.
"""

from typing import Optional, Any
from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("sahyogsetu.exceptions")

class SahyogSetuException(Exception):
    """Base exception for SahyogSetu API."""
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, error_type: str = "bad_request"):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_type = error_type

class EntityNotFoundException(SahyogSetuException):
    """Raised when a requested resource (conversation, news, document) does not exist."""
    def __init__(self, entity_name: str, entity_id: str):
        message = f"{entity_name} with ID '{entity_id}' not found."
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND, error_type="entity_not_found")
        self.entity_name = entity_name
        self.entity_id = entity_id

class DatabaseException(SahyogSetuException):
    """Raised when a database transaction or integrity constraint fails."""
    def __init__(self, message: str, original_error: Optional[Any] = None):
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error_type="database_error")
        self.original_error = original_error

class ValidationException(SahyogSetuException):
    """Raised when business validation rules fail."""
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, error_type="validation_error")

class FileTooLargeException(SahyogSetuException):
    """Raised when uploaded file exceeds allowed size."""
    def __init__(self, max_mb: int = 15):
        message = f"File size exceeds maximum permitted limit ({max_mb} MB)."
        super().__init__(message, status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, error_type="file_too_large")

async def sahyogsetu_exception_handler(request: Request, exc: SahyogSetuException) -> JSONResponse:
    """Formats application exceptions into clean JSON error payloads."""
    logger.warning("Application error on %s %s: [%s] %s", request.method, request.url.path, exc.error_type, exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_type,
            "detail": exc.message,
            "status_code": exc.status_code,
        },
    )
