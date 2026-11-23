"""
Multilingual Text Cleaner for SahyogSetu Legal Documents
Preserves original scripts (Latin, Devanagari, Gurmukhi, Urdu) without translation.
Performs NFC normalization, ligature replacement, line-wrap unwrapping,
and repeated header/footer noise removal.
"""

import re
import unicodedata
from collections import Counter
from typing import List, Tuple, Dict, Any, Optional

LIGATURES = {
    "\ufb01": "fi",
    "\ufb02": "fl",
    "\ufb00": "ff",
    "\u00ad": "",   # soft hyphen
    "\u00a0": " ",  # non-breaking space
    "\u200b": "",   # zero-width space
    "\u200c": "",   # zero-width non-joiner
    "\u200d": "",   # zero-width joiner
}

PAGE_NO_PATTERN = re.compile(
    r"^[\-–—\s]*(page\s*)?\d{1,4}(\s*(of|/)\s*\d{1,4})?[\-–—\s]*$",
    re.I
)

CLAUSE_BULLET_PATTERN = re.compile(
    r"^(\(\s*[0-9A-Za-z]{1,4}\s*\)|[•\u2022*]|\d+(\.\d+)*\.?\s)"
)

class TextCleaner:
    """Provides legal-safe Unicode normalization and noise removal."""

    @staticmethod
    def normalize_text(text: str) -> str:
        """Applies NFC normalization, ligature expansion, and control character removal."""
        if not text:
            return ""
        norm = unicodedata.normalize("NFC", text)
        for k, v in LIGATURES.items():
            norm = norm.replace(k, v)
        # Strip ASCII control characters except newline and tab
        return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", norm)

    @staticmethod
    def detect_script_language(text: str) -> str:
        """
        Detects primary script without external dependencies:
        - Gurmukhi -> pa (Punjabi)
        - Devanagari -> hi (Hindi / Dogri)
        - Arabic -> ur (Urdu)
        - Latin -> en (English)
        """
        if not text:
            return "en"

        counts = {
            "pa": len(re.findall(r"[\u0A00-\u0A7F]", text)),
            "hi": len(re.findall(r"[\u0900-\u097F]", text)),
            "ur": len(re.findall(r"[\u0600-\u06FF]", text)),
            "en": len(re.findall(r"[A-Za-z]", text)),
        }
        top_lang = max(counts, key=counts.get)
        if counts[top_lang] > 10:
            return top_lang
        return "en"

    @classmethod
    def clean_pages(cls, pages: List[Dict[str, Any]]) -> List[Tuple[int, str]]:
        """
        Cleans raw extracted pages by removing recurring headers, footers, and page numbers.
        Returns a list of (page_number, cleaned_line) tuples.
        """
        if not pages:
            return []

        per_page: List[Tuple[int, List[str]]] = []
        for p in pages:
            lines = [cls.normalize_text(l).rstrip() for l in (p.get("text") or "").splitlines()]
            per_page.append((p.get("page", 1), lines))

        # Identify repeating headers/footers across pages (at least 30% of pages in docs >= 6 pages)
        counter = Counter()
        for _, lines in per_page:
            non_empty = [l.strip() for l in lines if l.strip()]
            for edge_line in set(non_empty[:2] + non_empty[-2:]):
                norm_pat = re.sub(r"\d+", "#", edge_line.lower())
                counter[norm_pat] += 1

        total_pages = len(per_page)
        repeated_noise = {
            k for k, c in counter.items()
            if total_pages >= 6 and (c / total_pages) >= 0.3 and len(k) < 100
        }

        cleaned_lines: List[Tuple[int, str]] = []
        for page_no, lines in per_page:
            non_empty_indices = [i for i, l in enumerate(lines) if l.strip()]
            edge_set = set(non_empty_indices[:2] + non_empty_indices[-2:])

            for i, line in enumerate(lines):
                s = line.strip()
                if not s:
                    cleaned_lines.append((page_no, ""))
                    continue

                norm_pat = re.sub(r"\d+", "#", s.lower())
                # Skip isolated page numbers or repeating headers/footers
                if i in edge_set and (PAGE_NO_PATTERN.match(s) or norm_pat in repeated_noise):
                    continue

                # Skip standalone OCR punctuation junk
                if s and not re.search(r"\w", s):
                    continue

                cleaned_lines.append((page_no, s))

        return cleaned_lines

    @classmethod
    def unwrap_paragraphs(cls, lines: List[Tuple[int, str]]) -> List[Tuple[str, int]]:
        """
        Combines wrapped lines and unwraps hyphenated terms while preserving clauses.
        Returns a list of (paragraph_text, page_number) tuples.
        """
        paragraphs: List[Tuple[str, int]] = []
        current_buf = ""
        current_page = None

        def flush():
            nonlocal current_buf, current_page
            if current_buf.strip():
                paragraphs.append((current_buf.strip(), current_page or 1))
            current_buf = ""

        for page, line in lines:
            if not line:
                flush()
                continue

            if current_buf and current_buf.endswith("-") and line[:1].islower() and current_buf[-2:-1].isalpha():
                # Re-join hyphenated word broken across line (e.g. regis- -> registration)
                current_buf = current_buf[:-1] + line
            elif current_buf and not CLAUSE_BULLET_PATTERN.match(line):
                # Continuation line
                current_buf += " " + line
            else:
                flush()
                current_buf = line
                current_page = page

        flush()
        return paragraphs
