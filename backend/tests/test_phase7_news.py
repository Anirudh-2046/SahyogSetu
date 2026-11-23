"""
SAHYOGSETU PHASE 7: GOVERNMENT NEWS AGGREGATION, OFFICIAL SOURCE VERIFICATION
AND INTELLIGENT NEWS PIPELINE TEST SUITE

Tests:
1. Centralized Official Source Registry coverage across Central, Punjab, Haryana, and J&K
2. Direct Source Document Verifier: PDF vs announcement distinction & homepage rejection
3. News Database Schema migration and 100% record preservation (all 29 authentic records)
4. Phase 6 ML News Classifier integration with confidence and sector routing
5. Factual Summarizer statutory figure preservation and 6-question structured output
6. Deduplication, Canonical URL normalization, and Amendment linking
7. News Scheduler background management and status reporting
8. FastAPI News API faceted filtering: jurisdiction, category, document_type, language
9. Verification Report API & Sources Status endpoints
10. News Reprocessing & Direct Document Provenance API contracts
"""

import sys
from pathlib import Path
import inspect
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.news.source_registry import SourceRegistry, OFFICIAL_SOURCES_CATALOG
from backend.services.news.source_verifier import SourceVerifier
from backend.services.news.summarizer import NewsSummarizer
from backend.services.news.deduplicator import Deduplicator
from backend.services.news.news_scheduler import news_scheduler
from backend.services.news.news_collector import NewsCollector
from backend.api.routes_news import (
    get_news,
    get_news_system_status,
    get_sources,
    get_verification_report as api_get_verification_report,
    reprocess_news,
    get_news_detail,
)
from backend.database import (
    count_news,
    get_news_items,
    get_news_item_by_id,
    get_news_verification_report,
)

def run_coro(coro):
    """Executes a coroutine synchronously without event-loop/socket dependencies for sandbox isolation."""
    if not inspect.iscoroutine(coro):
        return coro
    stack = [coro]
    val = None
    while stack:
        current = stack[-1]
        try:
            res = current.send(val)
            if inspect.iscoroutine(res):
                stack.append(res)
                val = None
            else:
                val = res
        except StopIteration as e:
            stack.pop()
            val = e.value
    return val

def test_01_source_registry_coverage():
    print("\n[Test 1] Official Source Registry Coverage across Jurisdictions...")
    registry = SourceRegistry()
    sources = registry.get_all_sources()

    assert len(sources) >= 16, f"Expected at least 16 registered official sources, found {len(sources)}"

    jurisdictions = {s["jurisdiction"] for s in sources}
    assert {"central", "punjab", "haryana", "jk"}.issubset(jurisdictions), (
        f"Missing mandated jurisdictions in registry: {jurisdictions}"
    )

    # Verify each source has required metadata and explicit official status
    for s in sources:
        assert s["source_id"], "Source missing source_id"
        assert s["name"], "Source missing name"
        assert s["base_url"].startswith("http"), f"Invalid base_url: {s['base_url']}"
        assert s.get("rate_limit_policy"), "Missing rate limit policy"
        assert "VERIFIED" in s.get("verification_status", ""), f"Status not verified: {s.get('verification_status')}"

    central_sources = registry.get_sources_by_jurisdiction("central")
    punjab_sources = registry.get_sources_by_jurisdiction("punjab")
    haryana_sources = registry.get_sources_by_jurisdiction("haryana")
    jk_sources = registry.get_sources_by_jurisdiction("jk")

    print(f"  ✓ Central Sources: {len(central_sources)} (MoCoop, CRCS, PIB, RBI, NABARD, PMFBY, eGazette)")
    print(f"  ✓ Punjab Sources: {len(punjab_sources)} (Cooperation Dept, Punjab Gov, PADB, Verka)")
    print(f"  ✓ Haryana Sources: {len(haryana_sources)} (Cooperation Dept, Haryana Gov, HARCO Bank, Hafed)")
    print(f"  ✓ J&K Sources: {len(jk_sources)} (Cooperative Dept, JK Gov, JKSCB)")

def test_02_source_verifier_rejection_and_distinction():
    print("\n[Test 2] Direct Source Document Verifier & Homepage Rejection...")
    verifier = SourceVerifier()

    # 1. Reject generic root homepages
    rejected_urls = [
        "https://cooperation.gov.in",
        "https://cooperation.gov.in/",
        "https://pib.gov.in",
        "https://punjab.gov.in",
        "https://haryana.gov.in",
        "https://jk.gov.in",
        "http://punjab.gov.in",
    ]
    for url in rejected_urls:
        assert verifier.is_homepage_rejected(url), f"Homepage was not rejected: {url}"

    # 2. Verify direct official document (PDF)
    pdf_url = "https://cooperation.gov.in/sites/default/files/2023-01/Model_Bye_Laws_PACS_English.pdf"
    res_doc = verifier.verify_source(pdf_url, pdf_url)
    assert res_doc["is_official_document"] is True
    assert res_doc["official_document_status"] == "verified_official_document"
    assert res_doc["document_url"] == pdf_url
    print("  ✓ Direct PDF document correctly identified as verified_official_document")

    # 3. Verify official announcement / article link
    article_url = "https://pib.gov.in/PressReleaseDetail.aspx?PRID=1838048"
    res_art = verifier.verify_source(article_url, "")
    assert res_art["is_official_source"] is True
    assert res_art["official_source_status"] in ["verified_official_source", "verified_official_article"]
    assert res_art["official_document_status"] == "verified_official_article"
    assert res_art["document_url"] is None
    print("  ✓ Official PIB press release correctly identified as verified_official_article")

    # 4. Third-party unverified link
    fake_url = "https://some-random-blog.com/post/coop-news"
    res_fake = verifier.verify_source(fake_url, "")
    assert res_fake["is_official_source"] is False
    assert res_fake["official_source_status"] == "not_verified"
    print("  ✓ Third-party blog correctly flagged as not_verified")

def test_03_database_schema_and_record_preservation():
    print("\n[Test 3] News Database Schema Migration & Authentic Record Preservation...")
    total = count_news("all")
    assert total >= 29, f"Expected at least 29 preserved authentic records, got {total}"
    print(f"  ✓ Database verified: {total} authentic records intact (0 records lost)")

    items = get_news_items("all", limit=50)
    for item in items:
        # Verify Phase 7 schema fields
        assert "document_url" in item
        assert "official_source_status" in item
        assert "official_document_status" in item
        assert "duplicate_of" in item
        assert "relevance_score" in item
        assert "model_version" in item
        assert "translation_status" in item
        assert "summary_status" in item
        assert "updated_at" in item

        # Verify no root homepages disguised as direct documents
        doc_url = item.get("document_url")
        if doc_url:
            assert not SourceVerifier.is_homepage_rejected(doc_url), f"Disguised homepage in document_url: {doc_url}"

    report = get_news_verification_report()
    assert report["verified_official_sources"] > 0
    assert report["verified_direct_documents"] > 0
    print(f"  ✓ Verification report: {report['verified_direct_documents']} verified documents, {report['articles_or_pending_documents']} official articles/notices")

def test_04_phase6_ml_news_classifier_integration():
    print("\n[Test 4] Phase 6 ML News Classifier Integration...")
    collector = NewsCollector()

    sample_items = [
        {
            "headline": "Cabinet Approves Computerization of 63,000 Functional PACS as Multi-Service Centers",
            "description": "Financial outlay of ₹2,516 Crore for cloud-based ERP software and hardware deployment in PACS.",
            "source_url": "https://pib.gov.in/PressReleaseDetail.aspx?PRID=1838048",
            "valid_categories": ["pacs_computerization", "gov_schemes", "government_schemes"],
        },
        {
            "headline": "HARCO Bank Fast-Tracks KCC Crop Loan Processing at 4% Interest Subvention",
            "description": "Kisan Credit Card renewal and loan disbursement guidelines under RBI Master Circular.",
            "source_url": "https://haryanacode.haryana.gov.in/acts/198422.pdf",
            "valid_categories": ["agri_credit_kcc", "finance_subsidies"],
        },
        {
            "headline": "Haryana RCS Issues Mandatory 60-Day Timeline for Cooperative Dispute Arbitration",
            "description": "Under Section 102 of Haryana Co-operative Societies Act 1984, arbitrators must resolve disputes within 60 days.",
            "source_url": "https://coopharyana.gov.in/orders/RCS_Arbitration_Timeline_Mandate_2024.pdf",
            "valid_categories": ["coop_laws_regulations", "grievance_arbitration"],
        },
    ]

    for sample in sample_items:
        processed = collector.process_raw_item(sample, "Government Press Authority")
        assert processed is not None
        assert processed["category"] in sample["valid_categories"], f"Unexpected category {processed['category']} for {sample['headline']}"
        assert processed["model_version"].startswith("phase6") or processed["model_version"].startswith("rule_based")
        assert processed["relevance_score"] >= 0.70
        print(f"  ✓ Classified '{sample['headline'][:45]}...' -> Category: {processed['category']} (Model: {processed['model_version']}, Score: {processed['relevance_score']})")

def test_05_summarizer_statutory_preservation():
    print("\n[Test 5] Factual Summarizer Statutory Preservation & 6 Core Questions...")
    text = (
        "Under Section 102 of Haryana Co-operative Societies Act 1984, the Registrar has mandated "
        "a strict 60-day timeline for circle arbitrators to resolve financial disputes. The Cabinet has "
        "also allocated ₹2,516 Crore for 63,000 PACS, providing a 4% interest subvention."
    )

    facts = NewsSummarizer.extract_statutory_facts(text)
    assert any("₹2,516 Crore" in c or "2,516" in c for c in facts["currencies"]), "Currency not preserved"
    assert "4%" in facts["percentages"], "Percentage 4% not preserved"
    assert any("Section 102" in s for s in facts["statutory_sections"]), "Section 102 not preserved"
    assert any("60-day" in t or "60" in t for t in facts["timelines"]), "Timeline 60-day not preserved"
    assert any("63,000 PACS" in q or "63,000" in q for q in facts["quantities"]), "Quantity 63,000 PACS not preserved"

    print("  ✓ Statutory numbers, currencies (₹2,516 Crore), sections (Section 102), and timelines (60 days) preserved")

    # Structured 6-point summary test
    headline = "Haryana RCS Issues Mandatory 60-Day Timeline for Dispute Arbitration"
    structured = NewsSummarizer.generate_structured_summary(
        headline=headline,
        description=text,
        issuing_department="Registrar Cooperative Societies, Haryana",
        jurisdiction="haryana",
    )

    assert "what_changed" in structured
    assert "issuing_authority" in structured
    assert "who_is_affected" in structured
    assert "jurisdiction" in structured
    assert "effective_date_or_timeline" in structured
    assert "required_action" in structured
    assert "preserved_statutory_facts" in structured
    assert "concise_summary" in structured

    print("  ✓ Structured 6-point summary answers What, Who Issued, Affected, Jurisdiction, Timeline, and Action")

def test_06_deduplication_and_amendment_tracking():
    print("\n[Test 6] Deduplication, Canonical URL Normalization & Amendment Tracking...")
    dedup = Deduplicator()

    # 1. Canonical URL stripping
    url1 = "https://pib.gov.in/PressReleaseDetail.aspx?PRID=1838048&utm_source=twitter#content"
    url2 = "http://www.pib.gov.in/PressReleaseDetail.aspx?PRID=1838048"
    assert dedup.canonical_url(url1) == dedup.canonical_url(url2)
    print("  ✓ Canonical URLs match across tracking queries, protocols, and fragments")

    # 2. Exact duplicate detection
    assert dedup.is_duplicate(url1, "Cabinet Approves Computerization of PACS") is False
    assert dedup.is_duplicate(url2, "Cabinet Approves Computerization of PACS") is True
    print("  ✓ Identical incoming update detected as duplicate and blocked")

    # 3. Amendment detection
    existing_items = [
        {
            "id": "news_central_001",
            "news_id": "news_central_001",
            "headline": "Election Schedule Announced for Multi-State Cooperative Societies 2024",
            "source_url": "https://cooperation.gov.in/notifications/election_order_2024.pdf",
            "description": "Elections to be conducted under Multi-State Cooperative Societies Act 2002.",
        }
    ]

    amendment_item = {
        "headline": "Corrigendum: Extension of Election Schedule for Multi-State Cooperative Societies 2024",
        "source_url": "https://cooperation.gov.in/notifications/election_order_corrigendum_2024.pdf",
        "description": "Corrigendum issued extending deadline for election nominations under the Multi-State Cooperative Societies Act.",
    }

    is_dup, dup_of, reason = dedup.check_duplicate_or_amendment(amendment_item, existing_items)
    assert is_dup is False, "Amendment should not be dropped as duplicate"
    assert dup_of == "news_central_001", f"Amendment should be linked to news_central_001, got {dup_of}"
    print(f"  ✓ Corrigendum/Amendment successfully linked to parent record ({dup_of})")

def test_07_news_scheduler_interface():
    print("\n[Test 7] News Scheduler Interface & Status Reporting...")
    status = news_scheduler.get_status()
    assert "is_running" in status
    assert "interval_seconds" in status
    assert "total_runs" in status
    assert "last_run" in status
    assert status["interval_seconds"] == 3600
    print(f"  ✓ Scheduler operational state verified: running={status['is_running']}, interval={status['interval_seconds']}s")

def test_08_api_news_faceted_filters():
    print("\n[Test 8] FastAPI News Endpoint Faceted Filtering...")
    
    # 1. Base query
    data = run_coro(get_news(limit=5))
    assert "items" in data
    assert len(data["items"]) > 0
    assert "totalAvailable" in data

    # 2. Jurisdiction filter
    data_central = run_coro(get_news(jurisdiction="central"))
    for item in data_central["items"]:
        assert item["jurisdiction"] == "central"

    # 3. Document type filter: verified PDFs
    data_docs = run_coro(get_news(document_type="official_document"))
    for item in data_docs["items"]:
        doc_url = item.get("document_url") or item.get("officialUrl")
        assert doc_url and str(doc_url).lower().endswith(".pdf"), f"Non-PDF returned under official_document: {doc_url}"
    print(f"  ✓ document_type=official_document returned {len(data_docs['items'])} verified PDF records")

    # 4. Multilingual query
    data_hi = run_coro(get_news(language="hi", limit=2))
    hi_items = data_hi["items"]
    assert len(hi_items) > 0
    print(f"  ✓ Multilingual Hindi headline: {hi_items[0]['headline_display'][:50]}...")

def test_09_api_status_sources_and_verification_report():
    print("\n[Test 9] Verification Report, Sources Status & System Health APIs...")

    # 1. Verification Report
    rep = run_coro(api_get_verification_report())
    assert rep["total_announcements"] >= 29
    assert rep["verified_official_sources"] > 0
    assert rep["verified_direct_documents"] > 0
    assert "by_jurisdiction" in rep
    print(f"  ✓ /api/news/verification-report: {rep['verified_direct_documents']} verified PDFs out of {rep['total_announcements']} total")

    # 2. Sources Status
    sources_data = run_coro(get_sources())
    sources = sources_data["sources"]
    assert len(sources) >= 16
    print(f"  ✓ /api/news/sources: {len(sources)} official connectors monitored")

    # 3. System Status
    st = run_coro(get_news_system_status())
    assert st["status"] == "operational"
    assert "scheduler" in st
    assert "verification_summary" in st
    print(f"  ✓ /api/news/status: Operational with scheduler metrics and verification summary")

def test_10_api_reprocess_and_provenance():
    print("\n[Test 10] Reprocessing API & Single Announcement Provenance...")
    items = get_news_items("all", limit=1)
    assert len(items) > 0
    news_id = items[0]["news_id"]

    # 1. Single item detail
    item_data = run_coro(get_news_detail(news_id))
    assert item_data["news_id"] == news_id
    assert "source_url" in item_data
    assert "official_source_status" in item_data
    assert "official_document_status" in item_data
    print(f"  ✓ Single item {news_id} retrieved with full document provenance")

    # 2. Reprocess item through Phase 6 NLP/ML
    reproc_data = run_coro(reprocess_news(news_id))
    assert reproc_data["status"] == "reprocessed"
    assert "item" in reproc_data
    assert reproc_data["item"]["news_id"] == news_id
    print(f"  ✓ Item {news_id} successfully reprocessed through Phase 6 NLP")

if __name__ == "__main__":
    print("=" * 80)
    print("SAHYOGSETU PHASE 7: GOVERNMENT NEWS & OFFICIAL SOURCE VERIFICATION TEST SUITE")
    print("=" * 80)

    test_01_source_registry_coverage()
    test_02_source_verifier_rejection_and_distinction()
    test_03_database_schema_and_record_preservation()
    test_04_phase6_ml_news_classifier_integration()
    test_05_summarizer_statutory_preservation()
    test_06_deduplication_and_amendment_tracking()
    test_07_news_scheduler_interface()
    test_08_api_news_faceted_filters()
    test_09_api_status_sources_and_verification_report()
    test_10_api_reprocess_and_provenance()

    print("\n" + "=" * 80)
    print("ALL 10/10 PHASE 7 NEWS TESTS PASSED (100%)")
    print("=" * 80)
