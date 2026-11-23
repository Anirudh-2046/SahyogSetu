"""
Factual News Summarizer for Cooperative Announcements
Produces concise, structured, factual summaries preserving figures, percentages, dates,
statutory sections, and issuing authorities.
Strictly removes journalistic speculation, editorial adjectives, and marketing noise.
Answers the 6 core questions:
1. What changed?
2. Who issued it?
3. Who is affected?
4. Jurisdiction?
5. Effective date or deadline?
6. Required action or next steps?
"""

import re
from typing import Dict, Any, List

class NewsSummarizer:
    """Generates concise, factual, legally-grounded summaries of official announcements."""

    SPECULATIVE_PATTERNS = [
        r"\b(it is believed that|sources say|may possibly|could likely|it seems)\b",
        r"\b(game changer|revolutionary|historic milestone|unprecedented)\b",
    ]

    CURRENCY_REGEX = re.compile(r"(?:₹|Rs\.?|INR)\s*[\d,]+(?:\.\d+)?\s*(?:Crore|Lakh|thousand|million|billion)?", re.IGNORECASE)
    PERCENT_REGEX = re.compile(r"\b\d+(?:\.\d+)?%", re.IGNORECASE)
    SECTION_REGEX = re.compile(r"\b(?:Section|Sec\.?|Rule|Act|Order)\s+[0-9A-Za-z\(\)\-]+(?:\s+of\s+\d{4})?", re.IGNORECASE)
    TIMELINE_REGEX = re.compile(r"\b(?:\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d+[- ]*(?:days?|months?|years?|hours?))\b", re.IGNORECASE)
    QUANTITY_REGEX = re.compile(r"\b[\d,]+\+?\s*(?:PACS|societies|farmers|members|panchayats|districts|branches)\b", re.IGNORECASE)

    @classmethod
    def extract_statutory_facts(cls, text: str) -> Dict[str, List[str]]:
        """Extracts strictly preserved figures, percentages, dates, and legal sections."""
        if not text:
            return {
                "currencies": [],
                "percentages": [],
                "statutory_sections": [],
                "timelines": [],
                "quantities": [],
            }

        return {
            "currencies": [m.strip() for m in cls.CURRENCY_REGEX.findall(text)],
            "percentages": [m.strip() for m in cls.PERCENT_REGEX.findall(text)],
            "statutory_sections": [m.strip() for m in cls.SECTION_REGEX.findall(text)],
            "timelines": [m.strip() for m in cls.TIMELINE_REGEX.findall(text)],
            "quantities": [m.strip() for m in cls.QUANTITY_REGEX.findall(text)],
        }

    @classmethod
    def clean_speculation(cls, text: str) -> str:
        """Removes sensationalism and journalistic commentary."""
        cleaned = text
        for pat in cls.SPECULATIVE_PATTERNS:
            cleaned = re.sub(pat, "", cleaned, flags=re.IGNORECASE)
        # Collapse double spaces
        return re.sub(r"\s+", " ", cleaned).strip()

    @classmethod
    def summarize(cls, headline: str, description: str, max_sentences: int = 2) -> str:
        """
        Generates a concise 2-sentence factual summary preserving official numbers and legal terms.
        """
        if not description or len(description.strip()) < len(headline):
            return headline.strip()

        cleaned_desc = cls.clean_speculation(description)

        # Split into sentences
        sentences = re.split(r"(?<=[.!?।])\s+", cleaned_desc.strip())
        meaningful = [s.strip() for s in sentences if len(s.strip()) > 15]

        if not meaningful:
            return headline.strip()

        # Prioritize sentences that contain statutory facts (currencies, percentages, sections)
        scored_sentences = []
        for s in meaningful:
            score = 1
            facts = cls.extract_statutory_facts(s)
            score += len(facts["currencies"]) * 3
            score += len(facts["percentages"]) * 2
            score += len(facts["statutory_sections"]) * 3
            score += len(facts["timelines"]) * 2
            score += len(facts["quantities"]) * 2
            scored_sentences.append((score, s))

        # Sort primarily preserving first sentence if relevant, and high-scoring subsequent sentences
        first = meaningful[0]
        rest = sorted(scored_sentences[1:], key=lambda x: x[0], reverse=True) if len(scored_sentences) > 1 else []

        selected = [first]
        if rest and max_sentences > 1:
            selected.append(rest[0][1])

        summary = " ".join(selected)
        return summary

    @classmethod
    def generate_structured_summary(
        cls,
        headline: str,
        description: str,
        issuing_department: str = "",
        jurisdiction: str = "central",
        target_audience: str = "Cooperative Societies, PACS & Farmer Members",
    ) -> Dict[str, Any]:
        """
        Constructs an explicit 6-point structured summary answering:
        1. What changed?
        2. Who issued it?
        3. Who is affected?
        4. Jurisdiction?
        5. Effective date / deadline?
        6. Required action or next steps?
        """
        full_text = f"{headline}. {description or ''}"
        facts = cls.extract_statutory_facts(full_text)

        # Extract timeline or deadline
        timelines_str = ", ".join(facts["timelines"]) if facts["timelines"] else "Immediate upon official publication"

        # Required action heuristic
        action = "Review statutory circular and ensure governance compliance."
        if "pacs" in full_text.lower():
            if "computerization" in full_text.lower() or "erp" in full_text.lower():
                action = "Participate in hardware/ERP deployment onboarding via district cooperative registrar."
            elif "bye-laws" in full_text.lower() or "model" in full_text.lower():
                action = "Convene special general body meeting to adopt Model Bye-laws."
        elif "kcc" in full_text.lower() or "credit" in full_text.lower() or "loan" in full_text.lower():
            action = "Submit loan renewal/application with updated land records and verification."
        elif "audit" in full_text.lower() or "dispute" in full_text.lower() or "arbitration" in full_text.lower():
            action = "Adhere to the mandated 60-day or statutory timeline for dispute submission."

        # Jurisdiction formatting
        jurisdiction_name = {
            "central": "Central / Multi-State (All India)",
            "punjab": "State of Punjab",
            "haryana": "State of Haryana",
            "jk": "UT of Jammu & Kashmir",
        }.get(jurisdiction.lower(), jurisdiction.capitalize())

        return {
            "what_changed": cls.clean_speculation(headline),
            "issuing_authority": issuing_department or "Registrar of Cooperative Societies / Concerned Ministry",
            "who_is_affected": target_audience,
            "jurisdiction": jurisdiction_name,
            "effective_date_or_timeline": timelines_str,
            "required_action": action,
            "preserved_statutory_facts": facts,
            "concise_summary": cls.summarize(headline, description),
        }


