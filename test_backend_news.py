"""
Test script for SahyogSetu News Aggregation & Multilingual Pipeline
"""

import asyncio
from backend.services.news.news_service import news_service
from backend.services.news.source_audit import run_source_audit
from backend.database import init_db, count_news, query_news

async def main():
    print("=== 1. INITIALIZING DATABASE ===")
    init_db()
    print("Database initialized successfully.")

    print("\n=== 2. RUNNING SOURCE AUDIT ===")
    audit_report = run_source_audit()
    print(f"Audit completed: {len(audit_report)} sources.")
    for a in audit_report:
        print(f"  [{a['status'].upper()}] {a['name']}: {a.get('notes', '')[:70]}")

    print("\n=== 3. RUNNING NEWS AGGREGATION & NLP PIPELINE ===")
    result = await news_service.refresh_all()
    print(f"Collection result: {result}")
    total = count_news("all")
    print(f"Total stored news in DB: {total}")

    print("\n=== 4. TESTING JURISDICTION FILTERING ===")
    for j in ["all", "central", "punjab", "haryana", "jk"]:
        feed = await news_service.get_news_feed(jurisdiction=j, language="en")
        print(f"Jurisdiction '{j}': {feed['totalAvailable']} items available, returned {len(feed['items'])}")
        # Check that state feed does not contain unrelated states
        if j in ["punjab", "haryana", "jk"]:
            other_states = [s for s in ["punjab", "haryana", "jk"] if s != j]
            unrelated = [it for it in feed['items'] if it['jurisdiction'] in other_states]
            assert len(unrelated) == 0, f"Violation: found {len(unrelated)} unrelated state items in {j} feed!"
            print(f"  -> Verified: 0 unrelated state items found in '{j}' feed.")

    print("\n=== 5. TESTING MULTILINGUAL SUMMARIES & 'WHY AM I SEEING THIS?' ===")
    sample_item_id = feed["items"][0]["news_id"]
    for lang in ["en", "hi", "pa", "doi", "bgc"]:
        f_lang = await news_service.get_news_feed(jurisdiction="all", language=lang, limit=1)
        item = f_lang["items"][0]
        print(f"Language [{lang.upper()}]:")
        print(f"  Headline: {item['headline_display'][:75]}...")
        print(f"  Summary: {item['summary_display'][:85]}...")
        print(f"  Why seeing this: {item['why_explanation_display'][:85]}...")

    print("\n=== ALL PIPELINE VERIFICATIONS PASSED SUCCESSFULLY ===")

if __name__ == "__main__":
    asyncio.run(main())

