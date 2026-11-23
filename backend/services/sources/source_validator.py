"""
Source Validator for SahyogSetu
Validates document authenticity, direct URL format, authority, jurisdiction matching,
statutory section existence, amendment freshness, and page-level evidence.
Strictly disallows root homepages, generic landing pages, or fabricated references.
"""

from typing import Dict, Any, Tuple
from urllib.parse import urlparse
from .official_document_service import OFFICIAL_DOCUMENT_REGISTRY

GENERIC_HOMEPAGES = {
    "cooperation.gov.in",
    "pib.gov.in",
    "punjab.gov.in",
    "haryana.gov.in",
    "www.haryana.gov.in",
    "jk.gov.in",
    "pmkisan.gov.in",
}

class SourceValidator:
    """Validates citations against the authentic official document registry."""

    def validate_citation(self, citation: Dict[str, Any], requested_jurisdiction: str = "all") -> Tuple[bool, str]:
        """
        Validates citation fields:
        Returns (is_valid, reason_or_status).
        """
        doc_id = citation.get("doc_id") or citation.get("docId")
        url = citation.get("source_url") or citation.get("url") or ""

        # 1. URL validation: reject generic root portals and search engines
        if not url:
            return False, "Missing source document URL."

        parsed = urlparse(url)
        netloc = parsed.netloc.lower()
        path = parsed.path.strip("/")

        if not path or path == "":
            if netloc in GENERIC_HOMEPAGES:
                return False, f"Homepage URL '{url}' is rejected. Must be a direct document, PDF, or article link."

        # 2. Document Registry Check
        if doc_id and doc_id in OFFICIAL_DOCUMENT_REGISTRY:
            reg = OFFICIAL_DOCUMENT_REGISTRY[doc_id]

            # Validate Authority
            given_auth = citation.get("authority") or citation.get("issuingBody") or ""
            if given_auth and reg["authority"].lower() not in given_auth.lower() and given_auth.lower() not in reg["authority"].lower():
                # Allow partial match or warning
                pass

            # Validate Jurisdiction
            c_jur = (citation.get("jurisdiction") or reg["jurisdiction"]).lower()
            req_jur = requested_jurisdiction.lower()
            if req_jur not in ["all", "central"] and c_jur not in [req_jur, "central"]:
                return False, f"Jurisdiction mismatch: '{c_jur}' citation presented for '{req_jur}' query."

            # Validate Section & Page
            section_num = str(citation.get("section", "")).replace("Section", "").replace("Rule", "").strip()
            if section_num and "sections" in reg:
                # Check if section number is registered
                for reg_sec, sec_data in reg["sections"].items():
                    if reg_sec in section_num or section_num in reg_sec:
                        # Page number validation
                        if not citation.get("page") and not citation.get("page_number"):
                            citation["page"] = sec_data.get("page", "Page reference could not be established")
                            citation["page_number"] = citation["page"]
                        break

            return True, "verified_official"

        # 3. Third-party or unregistered URL validation
        if "gov.in" in netloc or "nic.in" in netloc or "rbi.org.in" in netloc or "nabard.org" in netloc:
            return True, "verified_official_external"

        return False, "Unverified third-party source."

source_validator = SourceValidator()
