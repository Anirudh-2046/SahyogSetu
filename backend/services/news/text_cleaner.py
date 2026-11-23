"""
Text Cleaner for Government Announcements
Normalizes Unicode, strips formatting artifacts, collapses redundant whitespace,
and preserves meaningful punctuation, numbers, schemes, and dates.
"""

import re
import unicodedata

class TextCleaner:
    """Normalizes and cleans multilingual official text."""

    @staticmethod
    def clean(text: str) -> str:
        if not text:
            return ""

        # Normalize unicode (NFC for Indic and Latin scripts)
        text = unicodedata.normalize("NFC", text)

        # Replace non-breaking spaces and irregular whitespace
        text = text.replace("\u00a0", " ").replace("\u200b", "").replace("\ufeff", "")

        # Normalize quotes and dashes
        text = text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
        text = text.replace("—", " - ").replace("–", " - ")

        # Strip remaining HTML tags
        text = re.sub(r"<[^>]+>", " ", text)

        # Collapse excessive whitespace and blank lines
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n\s*\n+", "\n\n", text)

        return text.strip()

