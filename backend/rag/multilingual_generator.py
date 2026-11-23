"""
Multilingual Answer Generator & Translation Preserver for SahyogSetu
Translates structured legal answers into English, Hindi, Punjabi, Dogri, and Haryanvi
while strictly preserving legal entity names, statutory section numbers, monetary amounts, and URLs.
"""

import re
import logging
from typing import Dict, Any, Optional

from ..services.language import translation_service

logger = logging.getLogger("sahyogsetu.multilingual")

# Common statutory entity translations preserving exact section and scheme tokens
STATUTORY_TERMS_MAP = {
    "pa": {
        "Direct Answer": "ਸਿੱਧਾ ਜਵਾਬ",
        "Statutory Provision": "ਕਾਨੂੰਨੀ ਉਪਬੰਧ",
        "Eligibility & Procedure": "ਯੋਗਤਾ ਅਤੇ ਪ੍ਰਕਿਰਿਆ",
        "Key Conditions": "ਮੁੱਖ ਸ਼ਰਤਾਂ",
        "Section": "ਧਾਰਾ",
        "Rule": "ਨਿਯਮ",
        "Registrar": "ਰਜਿਸਟਰਾਰ",
        "Cooperative Society": "ਸਹਿਕਾਰੀ ਸਭਾ",
        "Managing Committee": "ਪ੍ਰਬੰਧਕ ਕਮੇਟੀ",
        "Arbitration": "ਸਾਲਸੀ / ਆਰਬਿਟ੍ਰੇਸ਼ਨ",
        "Audit": "ਲੇਖਾ ਪੜਤਾਲ (ਆਡਿਟ)",
    },
    "hi": {
        "Direct Answer": "सीधा उत्तर",
        "Statutory Provision": "वैधानिक प्रावधान",
        "Eligibility & Procedure": "पात्रता एवं प्रक्रिया",
        "Key Conditions": "मुख्य शर्तें",
        "Section": "धारा",
        "Rule": "नियम",
        "Registrar": "पंजीयक (रजिस्ट्रार)",
        "Cooperative Society": "सहकारी समिति",
        "Managing Committee": "प्रबंध समिति",
        "Arbitration": "मध्यस्थता (आर्बिट्रेशन)",
        "Audit": "लेखा परीक्षा (ऑडिट)",
    },
    "doi": {
        "Direct Answer": "सबंधी उत्तर",
        "Statutory Provision": "कानूनी प्रावधान",
        "Eligibility & Procedure": "योग्यता ते प्रक्रिया",
        "Key Conditions": "मुक्ख शर्तौ",
        "Section": "धारा",
        "Rule": "नियम",
    },
    "bgc": {
        "Direct Answer": "सीधा जवाब",
        "Statutory Provision": "कानूनी प्रावधान",
        "Eligibility & Procedure": "पात्रता और प्रक्रिया",
        "Key Conditions": "मुख्य शर्तें",
        "Section": "धारा",
        "Rule": "नियम",
    },
}

class MultilingualGenerator:
    """Delivers answers in requested language without corrupting legal entities or markdown links."""

    @classmethod
    def translate_answer_sync(
        cls,
        answer_text: str,
        target_language: str,
        source_language: str = "en",
    ) -> str:
        """
        Synchronous translation preserving legal entities and links without network dependency.
        """
        res = translation_service.translate_sync(
            text=answer_text,
            source_language=source_language,
            target_language=target_language,
            preserve_legal_entities=True,
        )
        return res["translated_text"]

    @classmethod
    async def translate_answer(
        cls,
        answer_text: str,
        target_language: str,
        source_language: str = "en",
    ) -> str:
        """
        Translates answer text into user's requested language.
        Preserves Markdown links `[text](url)` and monetary symbols (₹).
        """
        res = await translation_service.translate(
            text=answer_text,
            source_language=source_language,
            target_language=target_language,
            preserve_legal_entities=True,
        )
        return res["translated_text"]

    @classmethod
    def translate_statutory_text(
        cls,
        text: str,
        target_language: str,
        source_language: str = "en",
    ) -> str:
        """
        Translates statutory excerpt or text into target language while preserving entities.
        """
        if not text or not text.strip() or target_language in ["en", "english"]:
            return text
        res = translation_service.translate_sync(
            text=text,
            source_language=source_language,
            target_language=target_language,
            preserve_legal_entities=True,
        )
        return res["translated_text"]

    @classmethod
    def _render_grounded_translation(cls, text: str, target_lang: str) -> str:
        """Translates legal headings and phrases while protecting sections and URLs."""
        term_map = STATUTORY_TERMS_MAP.get(target_lang, {})
        rendered = text

        for en_term, target_term in term_map.items():
            rendered = re.sub(rf"\b{re.escape(en_term)}\b", target_term, rendered, flags=re.IGNORECASE)

        return rendered

multilingual_generator = MultilingualGenerator()
