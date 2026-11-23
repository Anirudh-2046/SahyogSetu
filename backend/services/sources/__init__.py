"""
SahyogSetu Direct Government Sources & Citation Resolution Architecture
Implements Package 10:
- Official document service (central and state acts, rules, circulars, gazettes)
- Source validator (authenticity, amendments, page existence, active status)
- Citation builder (structured citations, official sources section)
- Source resolver (workflow from question to validated evidence)
"""

from .official_document_service import official_document_service
from .source_validator import source_validator
from .citation_builder import citation_builder
from .source_resolver import source_resolver

__all__ = [
    "official_document_service",
    "source_validator",
    "citation_builder",
    "source_resolver",
]

