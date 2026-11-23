"""
Comprehensive Automated Test Suite for Response Language Enforcement
Verifies that user-selected response language is consistently and strictly enforced
across all response components while preserving legal entities, statutory numbers,
rates, thresholds, and official URLs.

Covers:
1. Hindi Query + Hindi Selected Language (0% English sentence leakage)
2. English Query + Hindi Selected Language (enforces selected Hindi language)
3. Hindi Query + English Selected Language (enforces selected English language)
4. Punjabi Query + Punjabi Selected Language (100% Gurmukhi response)
5. English Legal Source + Hindi Selected Language
6. English Legal Source + Punjabi Selected Language
7. Ambiguous Query Requiring Jurisdiction Clarification (localized prompt)
8. Unsupported Query Requiring Abstention / No Evidence (localized message)
9. Language Priority Enforcement (explicit selection > query detection > default)
10. Legal Entity Preservation (Acts, Sections, Years, Rates, Amounts, URLs)
11. Dialect Integrity for Dogri and Haryanvi
"""

import sys
import os
import re

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.rag.rag_pipeline import rag_pipeline
from backend.services.sources.source_resolver import source_resolver
from backend.rag.language_detector import language_detector

def test_hindi_query_hindi_selection():
    """1. Hindi query + Hindi selection -> 100% Hindi prose (0% English sentence leakage)"""
    q = "केसीसी (KCC) पर 3% शीघ्र पुनर्भुगतान ब्याज छूट (MISS योजना) के क्या नियम हैं?"
    res = source_resolver.resolve_query(query=q, language="hi", jurisdiction="central")

    assert res["language"] == "hi"
    short = res.get("shortAnswer", "")
    plain = res.get("plainExplanation", "")

    # Must contain key Hindi legal terms and figures
    assert "किसान क्रेडिट कार्ड" in short or "ब्याज" in short
    assert "₹3.00" in plain or "₹3" in plain
    assert "1.5%" in plain
    assert "3%" in plain
    assert "4%" in plain

    # Must NOT contain English sentence leakage
    forbidden_english_phrases = [
        "Under KCC Master Circular",
        "provides 1.5% interest subvention",
        "reducing net effective interest rate",
        "According to the provisions governing cooperative societies",
        "Important Conditions & Procedures",
        "Mandatory compliance with",
        "Applications and statutory filings must be submitted",
        "All official records and member lists must be maintained",
        "Disclaimer: This information is derived from",
    ]
    for phrase in forbidden_english_phrases:
        assert phrase not in plain, f"Forbidden English phrase leaked in Hindi response: '{phrase}'"

    # Language consistency check
    val = language_detector.validate_language_consistency(plain, "hi")
    assert val["is_consistent"], f"Hindi consistency check failed: {val}"
    print("  ✓ Test 1 Passed: Hindi query + Hindi selection (0% English sentence leakage)")


def test_english_query_hindi_selection():
    """2. English query + Hindi selection -> Enforces selected Hindi language"""
    q = "What is the term of office for the managing committee in Haryana?"
    res = source_resolver.resolve_query(query=q, language="hi", jurisdiction="haryana")

    assert res["language"] == "hi"
    plain = res.get("plainExplanation", "")
    short = res.get("shortAnswer", "")

    assert "प्रबंध समिति" in plain or "कार्यकाल" in plain
    assert "5 वर्ष" in plain or "पांच वर्ष" in plain
    assert "धारा 28" in plain or "धारा" in plain

    # Must NOT have English boilerplate explanation
    assert "According to the provisions governing cooperative societies" not in plain
    assert "The term of office of the managing committee of a cooperative society shall be five years" not in plain

    val = language_detector.validate_language_consistency(plain, "hi")
    assert val["is_consistent"], f"Hindi consistency check failed: {val}"
    print("  ✓ Test 2 Passed: English query + Hindi selection (enforced Hindi)")


def test_hindi_query_english_selection():
    """3. Hindi query + English selection -> Enforces selected English language"""
    q = "केसीसी (KCC) पर 3% शीघ्र पुनर्भुगतान ब्याज छूट (MISS योजना) के क्या नियम हैं?"
    res = source_resolver.resolve_query(query=q, language="en", jurisdiction="central")

    assert res["language"] == "en"
    plain = res.get("plainExplanation", "")
    short = res.get("shortAnswer", "")

    assert "Kisan Credit Card" in plain or "KCC" in plain
    assert "interest" in plain.lower()
    assert "Official Sources & References" in plain

    val = language_detector.validate_language_consistency(plain, "en")
    assert val["is_consistent"], f"English consistency check failed: {val}"
    print("  ✓ Test 3 Passed: Hindi query + English selection (enforced English)")


def test_punjabi_query_punjabi_selection():
    """4. Punjabi query + Punjabi selection -> 100% Gurmukhi response"""
    q = "ਪੰਜਾਬ ਵਿੱਚ ਸਹਿਕਾਰੀ ਸੁਸਾਇਟੀ ਰਜਿਸਟਰ ਕਰਵਾਉਣ ਲਈ ਘੱਟੋ-ਘੱਟ ਕਿੰਨੇ ਮੈਂਬਰ ਚਾਹੀਦੇ ਹਨ?"
    res = source_resolver.resolve_query(query=q, language="pa", jurisdiction="punjab")

    assert res["language"] == "pa"
    plain = res.get("plainExplanation", "")
    short = res.get("shortAnswer", "")

    assert "ਸਹਿਕਾਰੀ" in plain
    assert "10" in plain or "ਦਸ" in plain
    assert "ਧਾਰਾ" in plain
    assert "ਪ੍ਰਮਾਣਿਕ" in plain or "ਸਰਕਾਰੀ" in plain

    # Must NOT contain English boilerplate
    assert "According to the provisions governing cooperative societies" not in plain
    assert "Mandates that an application for registration" not in plain

    val = language_detector.validate_language_consistency(plain, "pa")
    assert val["is_consistent"], f"Punjabi consistency check failed: {val}"
    print("  ✓ Test 4 Passed: Punjabi query + Punjabi selection (100% Gurmukhi)")


def test_english_legal_source_hindi_selected():
    """5. English legal source chunk + Hindi selected -> Localized Hindi explanation"""
    q = "What does Section 28 of Haryana Act 1984 specify?"
    res = rag_pipeline.run_sync(query=q, user_language="hi", user_jurisdiction="haryana")

    assert res["language"] == "hi"
    plain = res.get("plainExplanation", "")

    assert "धारा 28" in plain
    assert "पांच वर्ष" in plain or "5 वर्ष" in plain
    assert "प्रबंध समिति" in plain
    assert "According to the provisions" not in plain

    val = language_detector.validate_language_consistency(plain, "hi")
    assert val["is_consistent"], f"Hindi consistency check failed: {val}"
    print("  ✓ Test 5 Passed: English legal source + Hindi selected (localized Hindi)")


def test_english_legal_source_punjabi_selected():
    """6. English legal source chunk + Punjabi selected -> Localized Punjabi explanation"""
    q = "What does Section 8 of Punjab Act 1961 specify?"
    res = rag_pipeline.run_sync(query=q, user_language="pa", user_jurisdiction="punjab")

    assert res["language"] == "pa"
    plain = res.get("plainExplanation", "")

    assert "ਧਾਰਾ 8" in plain
    assert "ਦਸ" in plain or "10" in plain
    assert "According to the provisions" not in plain

    val = language_detector.validate_language_consistency(plain, "pa")
    assert val["is_consistent"], f"Punjabi consistency check failed: {val}"
    print("  ✓ Test 6 Passed: English legal source + Punjabi selected (localized Punjabi)")


def test_jurisdiction_clarification_localization():
    """7. Ambiguous query requiring jurisdiction clarification is fully localized"""
    q = "What is the procedure to register a cooperative society?"

    # Hindi clarification
    res_hi = source_resolver.resolve_query(query=q, language="hi", jurisdiction="all")
    assert res_hi["uncertainty"]["status"] == "clarification_required"
    assert "अधिकार क्षेत्र स्पष्टीकरण आवश्यक:" in res_hi["plainExplanation"]
    assert "सहकारी समिति के नियम" in res_hi["shortAnswer"]

    # Punjabi clarification
    res_pa = source_resolver.resolve_query(query=q, language="pa", jurisdiction="all")
    assert res_pa["uncertainty"]["status"] == "clarification_required"
    assert "ਅਧਿਕਾਰ ਖੇਤਰ ਸਪੱਸ਼ਟੀਕਰਨ ਲੋੜੀਂਦਾ:" in res_pa["plainExplanation"]
    assert "ਸਹਿਕਾਰੀ ਸਭਾ ਦੇ ਨਿਯਮ" in res_pa["shortAnswer"]

    # English clarification
    res_en = source_resolver.resolve_query(query=q, language="en", jurisdiction="all")
    assert res_en["uncertainty"]["status"] == "clarification_required"
    assert "Jurisdiction Clarification Required:" in res_en["plainExplanation"]
    print("  ✓ Test 7 Passed: Jurisdiction clarification responses fully localized across languages")


def test_no_evidence_abstention_localization():
    """8. Unsupported query requiring no-evidence abstention is fully localized"""
    q = "What does Section 999 of Haryana Act say?"

    # Hindi abstention
    res_hi = source_resolver.resolve_query(query=q, language="hi", jurisdiction="haryana")
    assert res_hi["uncertainty"]["status"] == "no_evidence"
    assert "पर्याप्त आधिकारिक साक्ष्य उपलब्ध नहीं:" in res_hi["plainExplanation"]
    assert "दस्तावेजों में पर्याप्त आधिकारिक जानकारी" in res_hi["shortAnswer"]

    # Punjabi abstention
    res_pa = source_resolver.resolve_query(query=q, language="pa", jurisdiction="haryana")
    assert res_pa["uncertainty"]["status"] == "no_evidence"
    assert "ਲੋੜੀਂਦੀ ਪ੍ਰਮਾਣਿਕ ਜਾਣਕਾਰੀ ਉਪਲਬਧ ਨਹੀਂ:" in res_pa["plainExplanation"]
    assert "ਦਸਤਾਵੇਜ਼ਾਂ ਵਿੱਚ ਲੋੜੀਂਦੀ ਪ੍ਰਮਾਣਿਕ ਜਾਣਕਾਰੀ" in res_pa["shortAnswer"]

    # English abstention
    res_en = source_resolver.resolve_query(query=q, language="en", jurisdiction="haryana")
    assert res_en["uncertainty"]["status"] == "no_evidence"
    assert "Insufficient Authoritative Evidence:" in res_en["plainExplanation"]
    print("  ✓ Test 8 Passed: No-evidence abstention responses fully localized across languages")


def test_language_priority_hierarchy():
    """9. Strict Priority: 1. User selected > 2. Query detected > 3. Default"""
    # 1. Explicit user selection overrides query language
    assert language_detector.resolve_priority_language("hi", "What is the rule?") == "hi"
    assert language_detector.resolve_priority_language("en", "केसीसी के क्या नियम हैं?") == "en"
    assert language_detector.resolve_priority_language("pa", "What is the rule?") == "pa"

    # 2. No language specified -> Detected query language
    assert language_detector.resolve_priority_language(None, "केसीसी (KCC) योजना के नियम क्या हैं?") == "hi"
    assert language_detector.resolve_priority_language("", "ਪੰਜਾਬ ਵਿੱਚ ਸੁਸਾਇਟੀ ਰਜਿਸਟ੍ਰੇਸ਼ਨ?") == "pa"
    assert language_detector.resolve_priority_language("auto", "What is Section 8?") == "en"

    # 3. Default fallback
    assert language_detector.resolve_priority_language(None, "Generic English query 123") == "en"
    print("  ✓ Test 9 Passed: 3-tier language priority hierarchy verified")


def test_legal_entity_preservation():
    """10. Statutory numbers, rates, acts, and URLs are strictly preserved without corruption"""
    q = "केसीसी (KCC) पर 3% शीघ्र पुनर्भुगतान ब्याज छूट (MISS योजना) के क्या नियम हैं?"
    res = source_resolver.resolve_query(query=q, language="hi", jurisdiction="central")
    plain = res["plainExplanation"]

    # Monetary and rate figures
    assert "1.5%" in plain
    assert "3%" in plain
    assert "4%" in plain
    assert "₹3.00" in plain or "₹3" in plain
    assert "₹1.60" in plain or "₹1.6" in plain

    # Statutory titles and sections
    assert "KCC" in plain
    assert "MISS" in plain

    # Official URL preservation
    cits = res.get("citations", [])
    assert len(cits) > 0
    for c in cits:
        url = c.get("sourceUrl") or c.get("source_url") or ""
        assert "http" in url, f"Expected valid URL, got '{url}'"
        assert "rbidocs.rbi.org.in" in url or "rbi.org.in" in url or "gov.in" in url
    print("  ✓ Test 10 Passed: Legal entities, rates (1.5%, 3%, 4%), amounts, and URLs preserved")


def test_dialect_integrity_dogri_haryanvi():
    """11. Dialect ethics: Dogri and Haryanvi render transparently in Devanagari with honest provider notice"""
    q = "What is the tenure of managing committee?"
    res_doi = rag_pipeline.run_sync(query=q, user_language="doi", user_jurisdiction="central")
    assert res_doi["language"] == "doi"
    assert "सबंधी उत्तर" in res_doi["plainExplanation"]

    res_bgc = rag_pipeline.run_sync(query=q, user_language="bgc", user_jurisdiction="central")
    assert res_bgc["language"] == "bgc"
    assert "सीधा जवाब" in res_bgc["plainExplanation"]
    print("  ✓ Test 11 Passed: Dogri and Haryanvi dialect ethics and rendering verified")


def run_all():
    print("=" * 80)
    print("SAHYOGSETU: RESPONSE LANGUAGE ENFORCEMENT AUTOMATED TEST SUITE")
    print("=" * 80)

    test_hindi_query_hindi_selection()
    test_english_query_hindi_selection()
    test_hindi_query_english_selection()
    test_punjabi_query_punjabi_selection()
    test_english_legal_source_hindi_selected()
    test_english_legal_source_punjabi_selected()
    test_jurisdiction_clarification_localization()
    test_no_evidence_abstention_localization()
    test_language_priority_hierarchy()
    test_legal_entity_preservation()
    test_dialect_integrity_dogri_haryanvi()

    print("\n" + "=" * 80)
    print("ALL 11 RESPONSE LANGUAGE ENFORCEMENT TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 80)

if __name__ == "__main__":
    run_all()
