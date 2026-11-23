"""
SahyogSetu Government News Source Audit
Audits genuine official government sources for cooperative announcements:
1. Ministry of Cooperation (cooperation.gov.in)
2. Press Information Bureau (pib.gov.in / www.pib.gov.in)
3. Haryana Government (haryana.gov.in)
4. Jammu & Kashmir Government (jk.gov.in)
5. Punjab Government (punjab.gov.in)
And departmental sources under these governments.
"""

import ssl
import time
from typing import Dict, Any, List
import httpx

# Official sources catalog
AUDIT_TARGETS = [
    {
        "id": "pib_central",
        "name": "Press Information Bureau (PIB) - Central Government",
        "jurisdiction": "central",
        "url": "https://www.pib.gov.in/allRel.aspx?lang=1",
        "type": "official_press_portal",
        "has_public_api": False,
        "api_endpoint": None,
        "auth_required": "None",
        "rate_limits": "Fair usage (approx 30 req/min)",
        "fields_available": ["headline", "publication_date", "article_text", "source_url", "issuing_department", "language"],
        "department": "Ministry of Information & Broadcasting / All Ministries",
    },
    {
        "id": "pib_hindi",
        "name": "Press Information Bureau (PIB Hindi)",
        "jurisdiction": "central",
        "url": "https://www.pib.gov.in/allRel.aspx?lang=2",
        "type": "official_press_portal",
        "has_public_api": False,
        "api_endpoint": None,
        "auth_required": "None",
        "rate_limits": "Fair usage",
        "fields_available": ["headline", "publication_date", "article_text", "source_url", "issuing_department", "language"],
        "department": "Ministry of Information & Broadcasting / PIB Hindi",
    },
    {
        "id": "mocoop_portal",
        "name": "Ministry of Cooperation National Portal",
        "jurisdiction": "central",
        "url": "https://cooperation.gov.in/en/whats-new",
        "type": "official_ministry_website",
        "has_public_api": False,
        "api_endpoint": None,
        "auth_required": "None",
        "rate_limits": "Government firewall/NIC throttling applies",
        "fields_available": ["headline", "publication_date", "pdf_link", "source_url"],
        "department": "Ministry of Cooperation, Government of India",
    },
    {
        "id": "punjab_gov",
        "name": "Government of Punjab Official Portal",
        "jurisdiction": "punjab",
        "url": "https://punjab.gov.in/",
        "type": "official_state_portal",
        "has_public_api": False,
        "api_endpoint": None,
        "auth_required": "None",
        "rate_limits": "Legacy SSL renegotiation required; fair usage",
        "fields_available": ["headline", "publication_date", "article_text", "source_url"],
        "department": "Department of Information and Public Relations, Punjab",
    },
    {
        "id": "punjab_rcs",
        "name": "Registrar Cooperative Societies Punjab",
        "jurisdiction": "punjab",
        "url": "http://rcs.punjab.gov.in/",
        "type": "departmental_subdomain",
        "has_public_api": False,
        "api_endpoint": None,
        "auth_required": "None",
        "rate_limits": "DNS unresolvable",
        "fields_available": [],
        "department": "Department of Cooperation, Punjab",
    },
    {
        "id": "haryana_gov",
        "name": "Government of Haryana Official Portal",
        "jurisdiction": "haryana",
        "url": "https://www.haryana.gov.in/",
        "type": "official_state_portal",
        "has_public_api": False,
        "api_endpoint": None,
        "auth_required": "None",
        "rate_limits": "Fair usage",
        "fields_available": ["headline", "publication_date", "source_url"],
        "department": "Information, Public Relations and Languages Department, Haryana",
    },
    {
        "id": "haryana_rcs",
        "name": "Registrar Cooperative Societies Haryana",
        "jurisdiction": "haryana",
        "url": "https://rcsharyana.gov.in/",
        "type": "departmental_subdomain",
        "has_public_api": False,
        "api_endpoint": None,
        "auth_required": "None",
        "rate_limits": "Endpoint returned 404 (integrated into main portal)",
        "fields_available": [],
        "department": "Cooperation Department, Haryana",
    },
    {
        "id": "jk_gov",
        "name": "Government of Jammu & Kashmir Official Portal",
        "jurisdiction": "jk",
        "url": "https://jk.gov.in/",
        "type": "official_state_portal",
        "has_public_api": False,
        "api_endpoint": None,
        "auth_required": "None",
        "rate_limits": "Network timeouts / geo-restricted gateway",
        "fields_available": ["headline", "notification_date", "pdf_link"],
        "department": "General Administration / Information Department J&K",
    },
    {
        "id": "jk_coop",
        "name": "J&K Cooperative Department",
        "jurisdiction": "jk",
        "url": "http://rcscoop.jk.gov.in/",
        "type": "departmental_subdomain",
        "has_public_api": False,
        "api_endpoint": None,
        "auth_required": "None",
        "rate_limits": "DNS unresolvable",
        "fields_available": [],
        "department": "Cooperative Department, J&K",
    },
]

def run_source_audit() -> List[Dict[str, Any]]:
    """Runs a live network audit of all registered government sources."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.options |= 0x4  # SSL_OP_LEGACY_SERVER_CONNECT for older state servers

    audit_results = []

    for target in AUDIT_TARGETS:
        item = dict(target)
        start_time = time.time()
        try:
            with httpx.Client(verify=ctx, headers=headers, timeout=6.0, follow_redirects=True) as client:
                res = client.get(target["url"])
                latency = round((time.time() - start_time) * 1000, 1)
                
                if res.status_code == 200:
                    item["status"] = "operational"
                    item["http_status"] = 200
                    item["latency_ms"] = latency
                    item["response_bytes"] = len(res.content)
                    item["notes"] = f"Operational via permitted public retrieval ({len(res.content)} bytes)."
                elif res.status_code == 404:
                    item["status"] = "unavailable"
                    item["http_status"] = 404
                    item["latency_ms"] = latency
                    item["notes"] = "Endpoint returned HTTP 404 Not Found (department may have migrated)."
                else:
                    item["status"] = "degraded"
                    item["http_status"] = res.status_code
                    item["latency_ms"] = latency
                    item["notes"] = f"Unexpected HTTP status {res.status_code}."
        except httpx.ConnectTimeout:
            item["status"] = "unavailable"
            item["http_status"] = None
            item["latency_ms"] = None
            item["notes"] = "Connection timed out (portal may have regional gateway restrictions)."
        except httpx.ReadTimeout:
            item["status"] = "degraded"
            item["http_status"] = None
            item["latency_ms"] = None
            item["notes"] = "Read operation timed out (server slow to respond)."
        except httpx.ConnectError as ce:
            item["status"] = "unavailable"
            item["http_status"] = None
            item["latency_ms"] = None
            item["notes"] = f"Connection error: {str(ce)}"
        except Exception as e:
            item["status"] = "unavailable"
            item["http_status"] = None
            item["latency_ms"] = None
            item["notes"] = f"Audit failed: {type(e).__name__}: {str(e)}"

        audit_results.append(item)

    return audit_results

if __name__ == "__main__":
    report = run_source_audit()
    print(f"Audit completed: {len(report)} sources evaluated.")
    for r in report:
        print(f"[{r['status'].upper()}] {r['name']} -> {r.get('notes')}")

