"""
Citation Builder for SahyogSetu
Builds strongly-typed citations and generates the mandatory markdown section:
"Official Sources & References"
Strictly complies with Package 10 Phase 15 requirements.
"""

from typing import Dict, Any, List

class CitationBuilder:
    """Builds structured citation objects and markdown evidence sections."""

    def build_structured_citation(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures all standard source fields are present and typed."""
        page_num = raw.get("page_number") or raw.get("page")
        if not page_num or str(page_num).strip() == "" or str(page_num) == "0":
            page_display = "Page reference could not be established"
        else:
            page_display = page_num

        return {
            "title": raw.get("title", "Official Government Document"),
            "authority": raw.get("authority") or raw.get("issuingBody", "Government of India"),
            "jurisdiction": raw.get("jurisdiction", "Central"),
            "document_type": raw.get("document_type") or raw.get("doc_type", "Statutory Act"),
            "section": raw.get("section", "General Statutory Framework"),
            "page_number": page_display,
            "page": page_display,
            "publication_date": raw.get("publication_date") or raw.get("documentDate", "Enacted / Official Publication"),
            "original_language": raw.get("original_language", "en"),
            "source_url": raw.get("source_url") or raw.get("url", ""),
            "url": raw.get("source_url") or raw.get("url", ""),
            "official_translation_url": raw.get("official_translation_url", ""),
            "verification_status": raw.get("verification_status", "verified_official"),
            "verbatim_excerpt": raw.get("verbatim_excerpt") or raw.get("verbatimExcerpt", ""),
            "applicability_note": raw.get("applicability_note") or raw.get("applicabilityNote", ""),
        }

    def generate_sources_markdown(self, citations: List[Dict[str, Any]], language: str = "en") -> str:
        """
        Generates the mandatory 'Official Sources & References' section.
        Supports regional headings while maintaining authentic authoritative source citations.
        """
        if not citations:
            return ""

        heading = (
            "### ਸਰਕਾਰੀ ਸਰੋਤ ਅਤੇ ਹਵਾਲੇ (Official Sources & References)"
            if language == "pa"
            else "### आधिकारिक स्रोत एवं संदर्भ (Official Sources & References)"
            if language in ["hi", "bgc"]
            else "### सरकारी स्रोत ते संदर्भ (Official Sources & References)"
            if language == "doi"
            else "### Official Sources & References"
        )

        labels_map = {
            "en": {
                "auth": "Authority", "jur": "Jurisdiction", "sec": "Relevant provision",
                "pg": "PDF page", "date": "Publication / Version date", "src": "Direct Official Source", "trans": "Official Translated Version"
            },
            "hi": {
                "auth": "प्राधिकरण", "jur": "अधिकार क्षेत्र", "sec": "प्रासंगिक प्रावधान",
                "pg": "पीडीएफ पृष्ठ", "date": "प्रकाशन / संस्करण तिथि", "src": "प्रत्यक्ष आधिकारिक स्रोत", "trans": "आधिकारिक अनुवादित संस्करण"
            },
            "doi": {
                "auth": "प्राधिकरण", "jur": "अधिकार क्षेत्र", "sec": "प्रासंगिक प्रावधान",
                "pg": "सफ़ा", "date": "प्रकाशन तिथि", "src": "प्रत्यक्ष आधिकारिक स्रोत", "trans": "आधिकारिक अनुवादित संस्करण"
            },
            "bgc": {
                "auth": "प्राधिकरण", "jur": "अधिकार क्षेत्र", "sec": "प्रासंगिक प्रावधान",
                "pg": "पेज", "date": "प्रकाशन तारीख", "src": "प्रत्यक्ष आधिकारिक स्रोत", "trans": "आधिकारिक अनुवादित संस्करण"
            },
            "pa": {
                "auth": "ਅਥਾਰਟੀ", "jur": "ਅਧਿਕਾਰ ਖੇਤਰ", "sec": "ਸੰਬੰਧਿਤ ਉਪਬੰਧ",
                "pg": "ਪੰਨਾ", "date": "ਪ੍ਰਕਾਸ਼ਨ ਮਿਤੀ", "src": "ਸਿੱਧਾ ਪ੍ਰਮਾਣਿਕ ਸਰੋਤ", "trans": "ਪ੍ਰਮਾਣਿਕ ਅਨੁਵਾਦਿਤ ਰੂਪ"
            },
        }
        lbl = labels_map.get(language, labels_map["en"])

        lines = [heading, ""]
        for idx, c in enumerate(citations, 1):
            title = c.get("title", "")
            auth = c.get("authority", "")
            jur = c.get("jurisdiction", "")
            sec = c.get("section", "")
            pg = c.get("page_number") or c.get("page") or "Page reference could not be established"
            date = c.get("publication_date", "")
            url = c.get("source_url") or c.get("url", "")
            trans_url = c.get("official_translation_url", "")

            lines.append(f"**{idx}. {title}**")
            lines.append(f"- **{lbl['auth']}**: {auth}")
            lines.append(f"- **{lbl['jur']}**: {jur}")
            if sec:
                lines.append(f"- **{lbl['sec']}**: {sec}")
            lines.append(f"- **{lbl['pg']}**: {pg}")
            if date:
                lines.append(f"- **{lbl['date']}**: {date}")
            lines.append(f"- **{lbl['src']}**: [{url}]({url})")
            if trans_url:
                lines.append(f"- **{lbl['trans']}**: [{trans_url}]({trans_url})")
            lines.append("")

        return "\n".join(lines).strip()

citation_builder = CitationBuilder()
