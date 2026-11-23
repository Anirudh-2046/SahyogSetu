"""
Jurisdiction Classifier for Cooperative Announcements
Classifies announcements into:
- Central Government ('central')
- Haryana ('haryana')
- Jammu & Kashmir ('jk')
- Punjab ('punjab')
Uses issuing authority, source origin, geographical references, and content context.
Flags uncertain classifications for review.
"""

from typing import Tuple, Dict, Any, List

class JurisdictionClassifier:
    """Classifies government announcements into specific jurisdictions."""

    PUNJAB_AUTHORITIES = ["punjab", "padb", "pscb", "markfed", "sugarfed", "ਪੰਜਾਬ", "पंजाब"]
    HARYANA_AUTHORITIES = ["haryana", "harco", "hafed", "हरियाणा", "ਹਰਿਆਣਾ"]
    JK_AUTHORITIES = ["jammu", "kashmir", "jk", "j&k", "jkscb", "अनंतनाग", "बारामूला", "ऊधमपुर", "ਸ਼ੋਪੀਆਂ", "बडगाम"]
    CENTRAL_AUTHORITIES = [
        "ministry of cooperation", "cooperation.gov.in", "pib", "press information bureau",
        "central registrar", "crcs", "rbi", "nabard", "cabinet approves", "central sector scheme"
    ]

    @classmethod
    def classify(cls, text: str, source_info: Dict[str, Any] = None) -> Tuple[str, bool, float, bool]:
        """
        Returns (jurisdiction, is_central_scheme_in_state, confidence, is_uncertain).
        """
        text_lower = text.lower()
        source_dept = (source_info.get("issuing_department", "") if source_info else "").lower()
        source_name = (source_info.get("source_name", "") if source_info else "").lower()
        pre_j = (source_info.get("jurisdiction", "") if source_info else "").lower()

        # 1. If source is explicitly configured as state origin
        if pre_j in ["punjab", "haryana", "jk", "central"]:
            return pre_j, False, 0.95, False

        combined_meta = f"{source_dept} {source_name}"

        # 2. Check issuing authority in metadata first (authoritative origin)
        if any(auth in combined_meta for auth in cls.CENTRAL_AUTHORITIES):
            # Check if it specifically applies to a state
            is_central_in_state = any(auth in text_lower for auth in cls.PUNJAB_AUTHORITIES + cls.HARYANA_AUTHORITIES + cls.JK_AUTHORITIES)
            return "central", is_central_in_state, 0.92, False

        if any(auth in combined_meta for auth in cls.PUNJAB_AUTHORITIES):
            return "punjab", False, 0.92, False

        if any(auth in combined_meta for auth in cls.HARYANA_AUTHORITIES):
            return "haryana", False, 0.92, False

        if any(auth in combined_meta for auth in cls.JK_AUTHORITIES):
            return "jk", False, 0.92, False

        # 3. Check content text for clear state authority mentions
        pb_hits = sum(1 for a in cls.PUNJAB_AUTHORITIES if a in text_lower)
        hr_hits = sum(1 for a in cls.HARYANA_AUTHORITIES if a in text_lower)
        jk_hits = sum(1 for a in cls.JK_AUTHORITIES if a in text_lower)
        central_hits = sum(1 for a in cls.CENTRAL_AUTHORITIES if a in text_lower)

        max_hits = max(pb_hits, hr_hits, jk_hits, central_hits)
        if max_hits == 0:
            return "central", False, 0.50, True

        if pb_hits == max_hits:
            return "punjab", False, 0.80, False
        if hr_hits == max_hits:
            return "haryana", False, 0.80, False
        if jk_hits == max_hits:
            return "jk", False, 0.80, False
        
        return "central", False, 0.80, False

