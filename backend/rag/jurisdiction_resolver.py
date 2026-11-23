"""
Jurisdiction Resolver for SahyogSetu
Enforces jurisdiction boundaries and hierarchy:
- Central: retrieves Central statutes, rules, and national schemes.
- Punjab: retrieves Punjab statutory provisions AND applicable Central legislation.
- Haryana: retrieves Haryana statutory provisions AND applicable Central legislation.
- J&K: retrieves J&K statutory provisions AND applicable Central legislation.
- Blocks cross-state retrieval (e.g. never returns Haryana laws to a Punjab user).
"""

import re
from typing import Dict, Any, List, Optional, Tuple

JURISDICTION_KEYWORDS = {
    "punjab": ["punjab", "pb", "ਪੰਜਾਬ", "पंजाब", "chandigarh", "ludhiana", "amritsar", "jalandhar", "patiala", "bathinda"],
    "haryana": ["haryana", "hr", "हरियाणा", "gurugram", "karnal", "hisar", "panchkula", "rohtak", "ambala", "faridabad", "sirsa"],
    "jk": ["jammu", "kashmir", "j&k", "jk", "ਜੰਮੂ", "ਕਸ਼ਮੀਰ", "जम्मू", "कश्मीर", "srinagar", "anantnag", "baramulla", "udhampur"],
    "central": ["central", "mscs", "multi-state", "multi state", "multistate", "india", "national", "ਕੇਂਦਰ", "केंद्र", "भारत"],
}

MULTISTATE_INDICATORS = [
    "mscs",
    "multi-state",
    "multi state",
    "multistate",
    "multi state cooperative",
    "central mscs act",
    "multi-state cooperative societies act",
]

INTERSTATE_INDICATORS = [
    "both",
    "across",
    "across states",
    "inter-state",
    "interstate",
    "multiple states",
    "different states",
    "more than one state",
    "two states",
    "multi-state",
    "multistate",
]

STATE_DEPENDENT_INTENTS = [
    "cooperative_registration",
    "elections_governance",
    "dispute_arbitration",
    "audit_inspection",
    "ots_waiver",
]

class JurisdictionResolver:
    """Resolves applicable statutory jurisdictions and retrieval filter scopes."""

    @classmethod
    def resolve(
        cls,
        query: str,
        user_jurisdiction: Optional[str] = None,
        detected_intent: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Determines the target jurisdiction, allowed retrieval scopes, and whether clarification is needed.
        Strictly prevents cross-state leakage and hostile cross-state application.
        """
        q_lower = query.lower() if query else ""

        eff_user_jur = (user_jurisdiction or "all").lower()
        if eff_user_jur not in ["central", "punjab", "haryana", "jk", "all"]:
            eff_user_jur = "all"

        # 1. Detect multi-state and central legislation indicators
        is_explicit_mscs = any(
            re.search(rf"\b{re.escape(ind)}\b", q_lower) for ind in MULTISTATE_INDICATORS
        )
        is_interstate = any(
            re.search(rf"\b{re.escape(ind)}\b", q_lower) for ind in INTERSTATE_INDICATORS
        )

        # 2. Detect which specific state jurisdictions are mentioned
        matched_states = []
        for state in ["punjab", "haryana", "jk"]:
            keywords = JURISDICTION_KEYWORDS[state]
            if any(re.search(rf"\b{re.escape(kw)}\b", q_lower) for kw in keywords):
                matched_states.append(state)

        has_central = any(
            re.search(rf"\b{re.escape(kw)}\b", q_lower) for kw in JURISDICTION_KEYWORDS["central"]
        )

        # 3. Resolve Target Jurisdiction
        query_jur = None
        selected_jur = "central"
        is_clarification_needed = False
        clarification_prompt = None

        if is_explicit_mscs or (is_interstate and len(matched_states) > 1):
            # Governed by Central MSCS Act 2002
            query_jur = "central"
            selected_jur = "central"
        elif len(matched_states) > 1:
            # Multiple states mentioned in query
            if is_interstate:
                query_jur = "central"
                selected_jur = "central"
            elif eff_user_jur in matched_states:
                # User's society belongs to user's selected jurisdiction; alien state law has no extraterritorial force
                query_jur = eff_user_jur
                selected_jur = eff_user_jur
            else:
                # Conflicting states without user disambiguation: prioritize territorial location in query
                # E.g. "in Rohtak Haryana" vs "Punjab Act"
                loc_state = None
                for state in matched_states:
                    if re.search(rf"\bin\s+[\w\s,]*\b({state}|{'|'.join(JURISDICTION_KEYWORDS[state])})\b", q_lower):
                        loc_state = state
                        break
                selected_jur = loc_state or matched_states[0]
                query_jur = selected_jur
        elif len(matched_states) == 1:
            detected_state = matched_states[0]
            query_jur = detected_state
            if eff_user_jur in ["all", detected_state]:
                selected_jur = detected_state
            else:
                # Query explicitly specifies one state act (e.g. user selected Punjab but typed "Haryana Act 1984")
                selected_jur = detected_state
        else:
            # No state explicitly detected in query
            if has_central:
                query_jur = "central"
                selected_jur = eff_user_jur if eff_user_jur != "all" else "central"
            else:
                query_jur = None
                selected_jur = eff_user_jur if eff_user_jur != "all" else "central"

            if not query_jur and eff_user_jur == "all" and detected_intent in STATE_DEPENDENT_INTENTS:
                is_clarification_needed = True
                clarification_prompt = (
                    "Cooperative society regulations (such as registration thresholds, committee terms, and audit rules) "
                    "vary across Central, Punjab, Haryana, and Jammu & Kashmir jurisdictions. "
                    "Please specify which state or jurisdiction applies to your society."
                )

        # 4. Build Allowed Retrieval Jurisdictions Hierarchy
        # State legislation + Central legislation is valid; Cross-state is strictly blocked
        if selected_jur == "punjab":
            allowed_jurisdictions = ["punjab", "central"]
        elif selected_jur == "haryana":
            allowed_jurisdictions = ["haryana", "central"]
        elif selected_jur == "jk":
            allowed_jurisdictions = ["jk", "central"]
        else:
            allowed_jurisdictions = ["central"]

        return {
            "resolved_jurisdiction": selected_jur,
            "query_detected_jurisdiction": query_jur,
            "user_selected_jurisdiction": eff_user_jur,
            "allowed_jurisdictions": allowed_jurisdictions,
            "requires_clarification": is_clarification_needed,
            "clarification_prompt": clarification_prompt,
        }

jurisdiction_resolver = JurisdictionResolver()
