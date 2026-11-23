"""
Legal Structure-Aware Document Chunker
Segments legal statutes, rules, and guidelines according to statutory hierarchy:
Act -> Chapter -> Section / Rule -> Subsection / Clause -> Schedule.
Attaches 24-field metadata to each chunk, guaranteeing full context retention.
"""

import re
import hashlib
from typing import List, Dict, Any, Tuple, Optional
from .text_cleaner import TextCleaner

# Regex Patterns for Statutory Headings
SECTION_DASH_PATTERN = re.compile(
    r"^(?:Section\s+|Rule\s+|Clause\s+|Para\s+)?(\d{1,3}[A-Z]{0,2}(?:\.\d{1,2}){0,2})\.\s+([A-Z(][^\n]{1,160}?)(?:\s*\.?\s*[—–-]{1,2}|\s*:)"
)
CHAPTER_PATTERN = re.compile(r"^(CHAPTER|PART)\s+[IVXLC\d]+[A-Z]?\b.*$", re.I)
SCHEDULE_PATTERN = re.compile(r"^(THE\s+)?([A-Z]+\s+)?(SCHEDULE|ANNEXURE|APPENDIX)\b.*$", re.I)
NUMERIC_HEADING_PATTERN = re.compile(r"^(\d{1,2}(?:\.\d{1,2}){0,3})\.?\s+([A-Z][^\n]{2,100})$")
CAPS_HEADING_PATTERN = re.compile(r"^[A-Z][A-Z0-9 ,&/()\-:]{4,80}$")

class LegalChunker:
    """Performs structure-preserving chunking for cooperative legal acts and guidelines."""

    def __init__(self, max_chars: int = 1200, min_chars: int = 250):
        self.max_chars = max_chars
        self.min_chars = min_chars

    def chunk_document(
        self,
        doc_metadata: Dict[str, Any],
        pages: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Executes structural segmentation, paragraph unwrapping, and metadata tagging.
        """
        cleaned_lines = TextCleaner.clean_pages(pages)
        if not cleaned_lines:
            return []

        doc_title = doc_metadata.get("title", "")
        units, doc_mode = self._segment_units(cleaned_lines, doc_title)

        # Build raw candidate pieces from units
        pieces = []
        for u in units:
            paras = TextCleaner.unwrap_paragraphs(u["lines"])
            packed = self._pack_paragraphs(paras, self.max_chars)
            for k, (text, p_start, p_end) in enumerate(packed):
                cont_suffix = " (cont.)" if k > 0 else ""
                pieces.append({
                    "label": u["label"] + cont_suffix,
                    "title": u["title"],
                    "chapter": u["chapter"],
                    "schedule": u.get("schedule", ""),
                    "text": text,
                    "page_start": p_start,
                    "page_end": p_end,
                })

        # Merge tiny adjacent pieces
        merged_pieces = self._merge_small_pieces(pieces, self.min_chars, self.max_chars)

        # Assemble final structured chunks with all 24 required fields
        doc_id = doc_metadata.get("doc_id", "doc_unknown")
        state = doc_metadata.get("state") or doc_metadata.get("jurisdiction", "Central")
        raw_jur = (doc_metadata.get("state") or doc_metadata.get("jurisdiction") or "Central").lower()
        if "j&k" in raw_jur or "jk" in raw_jur or "jammu" in raw_jur:
            jurisdiction = "jk"
        elif "punjab" in raw_jur:
            jurisdiction = "punjab"
        elif "haryana" in raw_jur:
            jurisdiction = "haryana"
        else:
            jurisdiction = "central"

        by_page = {p.get("page", i + 1): p for i, p in enumerate(pages)}
        chunks: List[Dict[str, Any]] = []

        for idx, piece in enumerate(merged_pieces):
            chunk_id = f"{doc_id}::{idx:04d}"
            chunk_text = piece["text"]

            # Compute content hash
            content_hash = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()

            # Detect language of chunk text
            detected_lang = TextCleaner.detect_script_language(chunk_text)
            declared_lang = doc_metadata.get("language") or "en"

            # Parse section number / rule number from piece label
            sec_num = ""
            rule_num = ""
            label = piece["label"]
            if label.startswith("Section"):
                m = re.search(r"Section\s+([0-9A-Za-z.]+)", label)
                if m:
                    sec_num = m.group(1).rstrip(".")
            elif label.startswith("Rule"):
                m = re.search(r"Rule\s+([0-9A-Za-z.]+)", label)
                if m:
                    rule_num = m.group(1).rstrip(".")
            elif label.startswith("Para") or label.startswith("Clause"):
                m = re.search(r"(?:Para|Clause)\s+([0-9A-Za-z.]+)", label)
                if m:
                    sec_num = m.group(1).rstrip(".")

            # Determine extraction method from pages spanned
            used_pages = [by_page[p] for p in range(piece["page_start"], piece["page_end"] + 1) if p in by_page]
            methods = {p.get("method", "text") for p in used_pages}
            extraction_method = "mixed" if len(methods) > 1 else (methods.pop() if methods else "text")

            # Format parent contextual header
            ctx_header = f"{doc_title} ({state})"
            if piece["chapter"]:
                ctx_header += f" | {piece['chapter']}"
            if label and label != "Preamble":
                ctx_header += f" | {label}"
                if piece["title"]:
                    ctx_header += f": {piece['title']}"

            embed_text = f"{ctx_header}\n{chunk_text}"

            chunk_record = {
                "chunk_id": chunk_id,
                "doc_id": doc_id,
                "document_title": doc_title,
                "document_type": doc_metadata.get("doc_type", "statute"),
                "issuing_body": doc_metadata.get("issuing_body", "Government Authority"),
                "jurisdiction": jurisdiction,
                "state": state,
                "language": declared_lang,
                "detected_language": detected_lang,
                "chapter": piece["chapter"] or None,
                "section": sec_num or None,
                "subsection": None,
                "rule": rule_num or None,
                "clause": None,
                "schedule": piece.get("schedule") or None,
                "page_start": piece["page_start"],
                "page_end": piece["page_end"],
                "source_url": doc_metadata.get("source_url", ""),
                "version_or_year": doc_metadata.get("version_or_year", ""),
                "date_retrieved": doc_metadata.get("date_retrieved", ""),
                "date_audited": doc_metadata.get("date_audited", ""),
                "text_quality": doc_metadata.get("text_quality", "ok"),
                "extraction_method": extraction_method,
                "chunk_text": chunk_text,
                "embed_text": embed_text,
                "content_hash": content_hash,
                "section_label": label,
                "section_title": piece["title"],
            }
            chunks.append(chunk_record)

        return chunks

    def _segment_units(self, lines: List[Tuple[int, str]], title: str) -> Tuple[List[Dict[str, Any]], str]:
        """Segments lines by Section/Rule or guideline headings."""
        legal_matches = sum(1 for _, l in lines if SECTION_DASH_PATTERN.match(l))
        is_legal = legal_matches >= 1 or ("act" in title.lower() or "rules" in title.lower())
        word = "Rule" if ("rules" in title.lower() and "act" not in title.lower()) else "Section"

        units: List[Dict[str, Any]] = []
        cur_unit: Optional[Dict[str, Any]] = None
        cur_chapter = ""
        cur_schedule = ""

        def start_new_unit(label: str, ttl: str, page: int):
            nonlocal cur_unit
            cur_unit = {
                "label": label,
                "title": ttl,
                "chapter": cur_chapter,
                "schedule": cur_schedule,
                "page": page,
                "lines": [],
            }
            units.append(cur_unit)

        start_new_unit("Preamble", "", lines[0][0] if lines else 1)

        i = 0
        while i < len(lines):
            page, line = lines[i]

            if CHAPTER_PATTERN.match(line):
                cur_chapter = line[:120]
                if i + 1 < len(lines) and CAPS_HEADING_PATTERN.match(lines[i + 1][1]):
                    cur_chapter += " - " + lines[i + 1][1][:120]
                start_new_unit("Chapter heading", cur_chapter, page)
                cur_unit["lines"].append((page, line))
            elif SCHEDULE_PATTERN.match(line):
                cur_schedule = line[:120]
                start_new_unit("Schedule", cur_schedule, page)
                cur_unit["lines"].append((page, line))
            elif is_legal:
                m = SECTION_DASH_PATTERN.match(line)
                if m:
                    sec_label = f"{word} {m.group(1)}"
                    sec_title = m.group(2).strip(" .")
                    start_new_unit(sec_label, sec_title, page)
                    cur_unit["lines"].append((page, line))
                else:
                    cur_unit["lines"].append((page, line))
            else:
                m_num = NUMERIC_HEADING_PATTERN.match(line)
                if m_num:
                    para_label = f"Para {m_num.group(1)}"
                    para_title = m_num.group(2).strip(" .")
                    start_new_unit(para_label, para_title, page)
                    cur_unit["lines"].append((page, line))
                elif CAPS_HEADING_PATTERN.match(line) and len(line) < 80:
                    start_new_unit("Heading", line, page)
                    cur_unit["lines"].append((page, line))
                else:
                    cur_unit["lines"].append((page, line))
            i += 1

        valid_units = [u for u in units if any(x[1].strip() for x in u["lines"])]
        return valid_units, ("legal" if is_legal else "guideline")

    def _pack_paragraphs(
        self,
        paras: List[Tuple[str, int]],
        max_chars: int,
    ) -> List[Tuple[str, int, int]]:
        """Packs paragraphs into chunks without breaking sentences when possible."""
        pieces: List[Tuple[str, int, int]] = []
        buf = ""
        buf_pages: List[int] = []

        def emit():
            nonlocal buf, buf_pages
            if buf.strip():
                pieces.append((buf.strip(), buf_pages[0], buf_pages[-1]))
            buf = ""
            buf_pages = []

        for text, page in paras:
            parts = [text]
            was_split = False
            if len(text) > max_chars:
                # Split along sentence boundaries (period, danda, semicolon)
                split_parts = re.split(r"(?<=[.;:।])\s+", text)
                if len(split_parts) > 1:
                    parts = split_parts
                    was_split = True

            for k, part in enumerate(parts):
                if buf and len(buf) + len(part) + 2 > max_chars:
                    emit()
                sep = " " if (was_split and k > 0) else "\n"
                buf += (sep if buf else "") + part
                buf_pages.append(page)

        emit()
        return pieces

    def _merge_small_pieces(
        self,
        pieces: List[Dict[str, Any]],
        min_chars: int,
        max_chars: int,
    ) -> List[Dict[str, Any]]:
        """Merges small non-statutory fragments while strictly keeping statutory Sections and Rules separate."""
        merged: List[Dict[str, Any]] = []
        acc: Optional[Dict[str, Any]] = None

        for p in pieces:
            acc_is_statutory = bool(acc and (acc["label"].startswith("Section") or acc["label"].startswith("Rule") or acc["label"].startswith("Para")))
            p_is_statutory = bool(p["label"].startswith("Section") or p["label"].startswith("Rule") or p["label"].startswith("Para"))

            # Only merge if neither piece is an autonomous statutory provision
            if acc and not acc_is_statutory and not p_is_statutory and len(acc["text"]) < min_chars and (len(acc["text"]) + len(p["text"]) + 1 <= max_chars):
                acc["text"] += "\n" + p["text"]
                acc["page_end"] = p["page_end"]
                if not acc.get("chapter") and p.get("chapter"):
                    acc["chapter"] = p["chapter"]
            else:
                if acc:
                    merged.append(acc)
                acc = dict(p)

        if acc:
            merged.append(acc)

        return merged
