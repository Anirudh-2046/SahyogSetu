"""
SahyogSetu Input Sanitization & Prompt Injection Defense
Sanitizes user input queries, validates filenames against path traversal,
and wraps retrieved statutory evidence in strict XML delimiters for RAG safety.
"""

import os
import re
import html
from typing import Tuple, List

# Adversarial prompt injection patterns attempting to override system grounding
PROMPT_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions?", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+(?:in\s+)?(?:developer|unrestricted|god|dan)\s+mode", re.IGNORECASE),
    re.compile(r"(?:print|reveal|output|display)\s+(?:your\s+)?(?:(?:initial\s+)?(?:system\s+)?(?:prompt|instructions)|api\s*keys?|secret\s*keys?)", re.IGNORECASE),
    re.compile(r"(?:system\s+instruction|system\s+override)\s*:", re.IGNORECASE),
    re.compile(r"disregard\s+(?:the\s+)?(?:rules|statutes|jurisdiction|evidence)", re.IGNORECASE),
]

SAFE_FILENAME_REGEX = re.compile(r"[^a-zA-Z0-9_\-\.]")


def sanitize_user_query(query: str, max_chars: int = 2000) -> Tuple[str, bool]:
    """
    Sanitizes user legal query:
    1. Truncates to max_chars to prevent memory bloat.
    2. Strips unprintable control characters.
    3. Detects and neutralizes prompt-injection override attempts.
    Returns (cleaned_query: str, had_injection_attempt: bool).
    """
    if not query:
        return "", False

    # 1. Truncate
    cleaned = query[:max_chars].strip()

    # 2. Strip unprintable control characters (except newline and tab)
    cleaned = "".join(ch for ch in cleaned if ch in ("\n", "\r", "\t") or ch.isprintable())

    # 3. Check for prompt injection patterns
    had_injection = False
    for pattern in PROMPT_INJECTION_PATTERNS:
        if pattern.search(cleaned):
            had_injection = True
            cleaned = pattern.sub("[REDACTED_PROMPT_OVERRIDE_ATTEMPT]", cleaned)

    return cleaned, had_injection


def sanitize_filename(filename: str, default: str = "document.pdf") -> str:
    """
    Sanitizes client-provided filename to prevent path traversal:
    1. Extracts basename only (stripping ../ or C:\\).
    2. Removes dangerous characters.
    3. Ensures safe default if empty.
    """
    if not filename:
        return default

    # Extract basename only
    base = os.path.basename(filename).strip()
    clean_base = SAFE_FILENAME_REGEX.sub("_", base)

    # Prevent hidden files or double dots
    clean_base = clean_base.lstrip(".")
    if not clean_base:
        return default

    return clean_base[:120]


def wrap_rag_context(context: str, query: str) -> str:
    """
    Wraps retrieved statutory context and citizen query in distinct XML data boundaries.
    Instructs the LLM that retrieved evidence is strictly passive data, preventing indirect injection.
    """
    escaped_context = html.escape(context)
    escaped_query = html.escape(query)

    return (
        "<retrieved_evidence integrity=\"untrusted_passive_data\">\n"
        f"{escaped_context}\n"
        "</retrieved_evidence>\n\n"
        "<citizen_query>\n"
        f"{escaped_query}\n"
        "</citizen_query>"
    )
