"""
OCR Engine Module for SahyogSetu
Handles optical character recognition for scanned legal PDFs and forms.
Supports English, Hindi (Devanagari), Punjabi (Gurmukhi), and Urdu where installed.
Provides confidence tracking and marks low-confidence pages for human review.
"""

import io
import sys
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("sahyogsetu.ocr")

try:
    import pytesseract
    from PIL import Image

    # Configure Windows default Tesseract path if present
    if sys.platform == "win32":
        win_tess = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
        if win_tess.exists():
            pytesseract.pytesseract.tesseract_cmd = str(win_tess)
except ImportError:
    pytesseract = None
    Image = None

LANG_TESSERACT_MAP = {
    "english": "eng",
    "en": "eng",
    "hindi": "hin",
    "hi": "hin",
    "punjabi": "pan",
    "pa": "pan",
    "urdu": "urd",
    "ur": "urd",
    "dogri": "hin",
    "doi": "hin",
}

class OCREngine:
    """Manages document OCR extraction with language validation and confidence metrics."""

    @staticmethod
    def is_available() -> bool:
        """Checks if pytesseract and Tesseract engine are operational."""
        if not pytesseract:
            return False
        try:
            langs = pytesseract.get_languages()
            return len(langs) > 0
        except Exception:
            return False

    @staticmethod
    def get_supported_languages() -> List[str]:
        """Returns installed Tesseract language models."""
        if not pytesseract:
            return []
        try:
            return pytesseract.get_languages()
        except Exception:
            return []

    @classmethod
    def ocr_image_bytes(cls, image_bytes: bytes, language: str = "en") -> Tuple[str, float, str]:
        """
        Performs OCR on image bytes.
        Returns (extracted_text, mean_confidence_percentage, processing_status).
        """
        if not pytesseract or not Image:
            return ("", 0.0, "tesseract_not_installed")

        tess_lang = LANG_TESSERACT_MAP.get(language.lower(), "eng")
        installed = cls.get_supported_languages()

        # Combine with English for multilingual legal numerals
        req_lang = tess_lang if tess_lang in installed else "eng"
        if req_lang != "eng" and "eng" in installed:
            req_lang = f"{req_lang}+eng"

        try:
            img = Image.open(io.BytesIO(image_bytes))
            data = pytesseract.image_to_data(img, lang=req_lang, output_type=pytesseract.Output.DICT)

            lines: Dict[Tuple[int, int, int], List[str]] = {}
            confidences: List[float] = []

            for i, word in enumerate(data.get("text", [])):
                w = word.strip()
                if not w:
                    continue
                block_key = (data["block_num"][i], data["par_num"][i], data["line_num"][i])
                lines.setdefault(block_key, []).append(w)

                try:
                    conf = float(data["conf"][i])
                    if conf >= 0:
                        confidences.append(conf)
                except (ValueError, KeyError):
                    pass

            # Assemble paragraphs
            text_lines: List[str] = []
            prev_block: Optional[Tuple[int, int]] = None
            for key in sorted(lines):
                cur_block = key[:2]
                if prev_block and cur_block != prev_block:
                    text_lines.append("")  # Paragraph separator
                text_lines.append(" ".join(lines[key]))
                prev_block = cur_block

            extracted_text = "\n".join(text_lines)
            mean_conf = round(sum(confidences) / len(confidences), 1) if confidences else 0.0
            status = "ok" if mean_conf >= 60.0 else "needs_review"

            return (extracted_text, mean_conf, status)

        except Exception as e:
            logger.warning("OCR processing error: %s", e)
            return ("", 0.0, f"error: {str(e)}")
