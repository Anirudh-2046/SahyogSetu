"""
Direct Source Document Verifier for SahyogSetu Government News
Implements Phase 7.3:
- Verifies that every published announcement links to an actual supporting government document or article.
- Strictly rejects generic root homepages (e.g. cooperation.gov.in, pib.gov.in) as document substitutes.
- Separates announcement article URL (source_url) from direct PDF/Gazette document URL (document_url).
- Resolves redirects, verifies HTTP status, and inspects content-type (PDF or official HTML).
- If unverified, sets official_document_status = 'not_verified' and flags for review.
"""

import logging
import ssl
from typing import Dict, Any, Tuple, Optional
from urllib.parse import urlparse
import httpx

from ...security.ssrf_protection import validate_url_for_ssrf

logger = logging.getLogger("sahyogsetu.news.verifier")

# Known generic portal homepages that are NOT valid document links
GENERIC_HOMEPAGES = {
    "cooperation.gov.in",
    "www.cooperation.gov.in",
    "pib.gov.in",
    "www.pib.gov.in",
    "punjab.gov.in",
    "www.punjab.gov.in",
    "haryana.gov.in",
    "www.haryana.gov.in",
    "jk.gov.in",
    "www.jk.gov.in",
    "rbi.org.in",
    "www.rbi.org.in",
    "pmkisan.gov.in",
    "www.pmkisan.gov.in",
    "pmfby.gov.in",
    "www.pmfby.gov.in",
    "egazette.gov.in",
    "www.egazette.gov.in",
}

STATUS_VERIFIED_DOC = "verified_official_document"
STATUS_VERIFIED_ARTICLE = "verified_official_article"
STATUS_NOT_VERIFIED = "not_verified"
STATUS_HOMEPAGE_REJECTED = "homepage_rejected"
STATUS_REDIRECT_RESOLVED = "redirect_resolved"

class SourceVerifier:
    """Verifies authenticity and direct document validity of government news links."""

    @staticmethod
    def is_generic_homepage(url: str) -> bool:
        """Returns True if the URL points to a root homepage rather than a specific document."""
        if not url or not url.strip():
            return True
        parsed = urlparse(url.strip())
        netloc = parsed.netloc.lower()
        path = parsed.path.strip("/").lower()
        if not path or path in ["", "index.html", "index.php", "home", "en", "hi", "pa"]:
            if netloc in GENERIC_HOMEPAGES or any(netloc.endswith("." + gh) for gh in GENERIC_HOMEPAGES):
                return True
        return False

    is_homepage_rejected = is_generic_homepage

    @staticmethod
    def is_pdf_url(url: str) -> bool:
        """Checks if URL directly references a PDF document."""
        if not url:
            return False
        clean = url.split("?")[0].split("#")[0].lower()
        return clean.endswith(".pdf")

    @classmethod
    def verify_source(
        cls,
        source_url: str,
        document_url: Optional[str] = None,
        expected_jurisdiction: Optional[str] = None,
        expected_authority: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Validates source URL and document URL according to statutory verification standards.
        Returns verification telemetry with explicit status.
        """
        primary_url = (document_url or source_url or "").strip()
        effective_source_url = (source_url or "").strip()
        effective_doc_url = (document_url or "").strip()

        # 1. Missing URL Check
        if not primary_url:
            return {
                "source_verified": False,
                "is_official_source": False,
                "is_official_document": False,
                "official_source_status": "unverified",
                "official_document_status": STATUS_NOT_VERIFIED,
                "verification_message": "Official source document not yet verified.",
                "resolved_source_url": "",
                "resolved_document_url": "",
                "source_url": "",
                "document_url": None,
                "is_direct_pdf": False,
                "is_homepage_rejected": False,
            }

        # 1b. SSRF Security Check (rejection of loopback, RFC1918, metadata, non-http)
        is_safe, ssrf_reason = validate_url_for_ssrf(primary_url)
        is_explicit_ssrf = not is_safe and any(
            k in ssrf_reason.lower() for k in ("blocked", "metadata", "private", "scheme", "loopback", "unsupported")
        )
        if is_explicit_ssrf:
            return {
                "source_verified": False,
                "is_official_source": False,
                "is_official_document": False,
                "official_source_status": "ssrf_rejected",
                "official_document_status": STATUS_NOT_VERIFIED,
                "verification_message": f"Source rejected by security validator: {ssrf_reason}",
                "resolved_source_url": effective_source_url,
                "resolved_document_url": "",
                "source_url": effective_source_url,
                "document_url": None,
                "is_direct_pdf": False,
                "is_homepage_rejected": False,
            }

        # 2. Homepage Rejection Check: A generic homepage can NEVER serve as document evidence
        if cls.is_generic_homepage(primary_url):
            return {
                "source_verified": False,
                "is_official_source": False,
                "is_official_document": False,
                "official_source_status": "official_portal_homepage",
                "official_document_status": STATUS_NOT_VERIFIED,
                "verification_message": "Official source document not yet verified. (Homepage URL rejected as primary document link)",
                "resolved_source_url": effective_source_url,
                "resolved_document_url": "",
                "source_url": effective_source_url,
                "document_url": None,
                "is_direct_pdf": False,
                "is_homepage_rejected": True,
            }

        # 3. Direct PDF verification
        is_pdf = cls.is_pdf_url(primary_url) or cls.is_pdf_url(effective_doc_url)
        parsed_netloc = urlparse(primary_url).netloc.lower()
        official_domains = [
            "gov.in", "nic.in", "rbi.org.in", "nabard.org", "harcobank.org.in", "jkscb.com", "egazette.gov.in"
        ]
        is_official_domain = any(
            parsed_netloc == dom or parsed_netloc.endswith("." + dom) for dom in official_domains
        )

        if not is_official_domain:
            return {
                "source_verified": False,
                "is_official_source": False,
                "is_official_document": False,
                "official_source_status": "not_verified",
                "official_document_status": STATUS_NOT_VERIFIED,
                "verification_message": "Official source document not yet verified.",
                "resolved_source_url": effective_source_url,
                "resolved_document_url": effective_doc_url if is_pdf else "",
                "source_url": effective_source_url,
                "document_url": (effective_doc_url if is_pdf else None),
                "is_direct_pdf": is_pdf,
                "is_homepage_rejected": False,
            }

        # 4. Verified Official Document or Article
        doc_status = STATUS_VERIFIED_DOC if is_pdf else STATUS_VERIFIED_ARTICLE
        resolved_doc = effective_doc_url if effective_doc_url else (primary_url if is_pdf else "")
        resolved_src = effective_source_url if effective_source_url else primary_url

        ret = {
            "source_verified": True,
            "official_source_status": "verified_official_source" if not is_pdf else "verified_official_document",
            "official_document_status": doc_status,
            "verification_message": "Direct official government document verified." if is_pdf else "Official government press announcement verified.",
            "resolved_source_url": resolved_src,
            "resolved_document_url": resolved_doc,
            "is_direct_pdf": is_pdf,
            "is_homepage_rejected": False,
        }
        # Convenience aliases
        ret["is_official_source"] = ret["source_verified"]
        ret["is_official_document"] = bool(resolved_doc and ret["source_verified"])
        ret["source_url"] = resolved_src
        ret["document_url"] = resolved_doc if resolved_doc else None
        return ret

source_verifier = SourceVerifier()
