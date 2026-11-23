"""
Centralized Official Source Registry for SahyogSetu
Maintains authoritative catalog of Central and State government sources for cooperative announcements.
Organizes sources strictly by jurisdiction: Central, Punjab, Haryana, Jammu & Kashmir.
Explicitly discloses collection method, endpoints, rate limits, and verification status.
"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger("sahyogsetu.news.registry")

# Standardized verification statuses
STATUS_LIVE_VERIFIED = "LIVE_SOURCE_VERIFIED"
STATUS_OFFICIAL_VERIFIED = "OFFICIAL_SOURCE_VERIFIED"
STATUS_NOT_LIVE_TESTED = "CONNECTOR_IMPLEMENTED_NOT_LIVE_TESTED"
STATUS_DOC_NOT_VERIFIED = "DOCUMENT_NOT_VERIFIED"
STATUS_UNAVAILABLE = "UNAVAILABLE"
STATUS_FAILED = "FAILED"

OFFICIAL_SOURCES_CATALOG: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # 1. CENTRAL GOVERNMENT SOURCES
    # -------------------------------------------------------------------------
    {
        "source_id": "mocoop_portal",
        "name": "Ministry of Cooperation National Portal",
        "jurisdiction": "central",
        "department": "Ministry of Cooperation, Government of India",
        "source_type": "official_ministry_portal",
        "base_url": "https://cooperation.gov.in",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "https://cooperation.gov.in/en/whats-new",
        "verification_status": STATUS_LIVE_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "Fair usage (max 1 req/2s); NIC server rate limiting applies",
        "notes": "Authoritative portal for MSCS Act, Model Bye-laws, and PACS computerization circulars.",
    },
    {
        "source_id": "crcs_portal",
        "name": "Central Registrar of Cooperative Societies (CRCS)",
        "jurisdiction": "central",
        "department": "Office of Central Registrar, Ministry of Cooperation",
        "source_type": "official_ministry_portal",
        "base_url": "https://crcs.gov.in",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "https://crcs.gov.in/notice",
        "verification_status": STATUS_OFFICIAL_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "Fair usage (max 1 req/3s)",
        "notes": "Publishes MSCS registration orders, arbitration notices, and statutory circulars.",
    },
    {
        "source_id": "pib_central_all",
        "name": "Press Information Bureau (PIB Central)",
        "jurisdiction": "central",
        "department": "Ministry of Information & Broadcasting, Government of India",
        "source_type": "official_press_portal",
        "base_url": "https://pib.gov.in",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1",
        "announcement_page": "https://www.pib.gov.in/allRel.aspx?lang=1",
        "verification_status": STATUS_LIVE_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "30 req/minute",
        "notes": "Direct releases from Ministry of Cooperation, Cabinet decisions, and Agriculture Ministry.",
    },
    {
        "source_id": "pib_central_hindi",
        "name": "Press Information Bureau (PIB Hindi)",
        "jurisdiction": "central",
        "department": "Ministry of Information & Broadcasting / PIB Hindi",
        "source_type": "official_press_portal",
        "base_url": "https://pib.gov.in",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=2",
        "announcement_page": "https://www.pib.gov.in/allRel.aspx?lang=2",
        "verification_status": STATUS_LIVE_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "30 req/minute",
        "notes": "Official Hindi translations of Central Government Cabinet and cooperative releases.",
    },
    {
        "source_id": "rbi_notifications",
        "name": "Reserve Bank of India (RBI)",
        "jurisdiction": "central",
        "department": "Department of Banking Regulation / Rural Planning, RBI",
        "source_type": "central_bank_regulator",
        "base_url": "https://www.rbi.org.in",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": "https://www.rbi.org.in/notifications_rss.xml",
        "announcement_page": "https://www.rbi.org.in/Scripts/NotificationUser.aspx",
        "verification_status": STATUS_OFFICIAL_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "Fair usage (max 1 req/2s)",
        "notes": "Issues Master Circulars on KCC, interest subvention, and rural credit guidelines.",
    },
    {
        "source_id": "nabard_portal",
        "name": "National Bank for Agriculture and Rural Development (NABARD)",
        "jurisdiction": "central",
        "department": "Farm Sector Policy Department, NABARD",
        "source_type": "statutory_board",
        "base_url": "https://www.nabard.org",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "https://www.nabard.org/circulars.aspx",
        "verification_status": STATUS_OFFICIAL_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "Fair usage",
        "notes": "Refinancing guidelines for State Cooperative Banks and PACS computerization outlay.",
    },
    {
        "source_id": "pmfby_portal",
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "jurisdiction": "central",
        "department": "Department of Agriculture & Farmers Welfare",
        "source_type": "official_ministry_portal",
        "base_url": "https://pmfby.gov.in",
        "collection_method": "document_feed",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "https://pmfby.gov.in/pdf/Revised_Operational_Guidelines.pdf",
        "verification_status": STATUS_OFFICIAL_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "Static PDF caching",
        "notes": "Direct operational guidelines, localized calamity reporting rules, and premium rates.",
    },
    {
        "source_id": "egazette_central",
        "name": "The Gazette of India (e-Gazette)",
        "jurisdiction": "central",
        "department": "Directorate of Printing, Ministry of Housing and Urban Affairs",
        "source_type": "official_gazette_portal",
        "base_url": "https://egazette.gov.in",
        "collection_method": "document_feed",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "https://egazette.gov.in",
        "verification_status": STATUS_LIVE_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "NIC throttling (max 1 req/5s)",
        "notes": "Official statutory Gazette Extraordinary notifications for Parliamentary Acts and Amendments.",
    },

    # -------------------------------------------------------------------------
    # 2. PUNJAB GOVERNMENT SOURCES
    # -------------------------------------------------------------------------
    {
        "source_id": "punjab_coop_dept",
        "name": "Department of Cooperation, Punjab",
        "jurisdiction": "punjab",
        "department": "Cooperation Department, Government of Punjab",
        "source_type": "official_ministry_portal",
        "base_url": "http://coopwb.punjab.gov.in",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "http://coopwb.punjab.gov.in/acts-rules.html",
        "verification_status": STATUS_LIVE_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "Legacy SSL renegotiation required; fair usage",
        "notes": "Authoritative repository of Punjab Act 1961, 2021 Amendment Gazette, and circulars.",
    },
    {
        "source_id": "punjab_gov_portal",
        "name": "Government of Punjab Official Portal",
        "jurisdiction": "punjab",
        "department": "Department of Information and Public Relations, Punjab",
        "source_type": "official_state_portal",
        "base_url": "https://punjab.gov.in",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "https://punjab.gov.in",
        "verification_status": STATUS_LIVE_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "Fair usage (max 1 req/3s)",
        "notes": "Cabinet notifications and administrative orders for cooperative societies.",
    },
    {
        "source_id": "punjab_padb",
        "name": "Punjab State Cooperative Agricultural Development Bank (PADB)",
        "jurisdiction": "punjab",
        "department": "PADB, Punjab Cooperation Department",
        "source_type": "statutory_board",
        "base_url": "https://padb.punjab.gov.in",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "https://padb.punjab.gov.in/notifications",
        "verification_status": STATUS_OFFICIAL_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "Fair usage",
        "notes": "One Time Settlement (OTS) circulars and penal interest waiver schemes.",
    },
    {
        "source_id": "verka_milkfed",
        "name": "Punjab State Cooperative Milk Producers' Federation (Verka)",
        "jurisdiction": "punjab",
        "department": "Milkfed Punjab",
        "source_type": "statutory_board",
        "base_url": "https://verka.coop",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "https://verka.coop/announcements",
        "verification_status": STATUS_OFFICIAL_VERIFIED,
        "direct_document_supported": False,
        "rate_limit_policy": "Fair usage",
        "notes": "Milk procurement prices, dairy bonus announcements, and cattle feed subsidies.",
    },

    # -------------------------------------------------------------------------
    # 3. HARYANA GOVERNMENT SOURCES
    # -------------------------------------------------------------------------
    {
        "source_id": "haryana_coop_dept",
        "name": "Department of Cooperation, Haryana",
        "jurisdiction": "haryana",
        "department": "Cooperation Department, Government of Haryana",
        "source_type": "official_ministry_portal",
        "base_url": "https://cooperation.haryana.gov.in",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "https://cooperation.haryana.gov.in/notifications",
        "verification_status": STATUS_LIVE_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "Fair usage (max 1 req/2s)",
        "notes": "Statutory notifications under Haryana Act 1984, Model Bye-laws, and RCS orders.",
    },
    {
        "source_id": "haryana_gov_portal",
        "name": "Government of Haryana Official Portal",
        "jurisdiction": "haryana",
        "department": "Information & Public Relations Department, Haryana",
        "source_type": "official_state_portal",
        "base_url": "https://www.haryana.gov.in",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "https://www.haryana.gov.in",
        "verification_status": STATUS_LIVE_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "Fair usage",
        "notes": "State cabinet decisions, election notifications, and cooperative assistance schemes.",
    },
    {
        "source_id": "harco_bank",
        "name": "Haryana State Cooperative Apex Bank (HARCO Bank)",
        "jurisdiction": "haryana",
        "department": "HARCO Bank, Haryana",
        "source_type": "statutory_board",
        "base_url": "https://harcobank.org.in",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "https://harcobank.org.in/circulars",
        "verification_status": STATUS_OFFICIAL_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "Fair usage",
        "notes": "Digital KCC, 4% interest subvention, and crop loan disbursement circulars.",
    },
    {
        "source_id": "hafed_haryana",
        "name": "Haryana State Cooperative Supply and Marketing Federation (HAFED)",
        "jurisdiction": "haryana",
        "department": "HAFED, Haryana",
        "source_type": "statutory_board",
        "base_url": "https://hafed.gov.in",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "https://hafed.gov.in/news",
        "verification_status": STATUS_OFFICIAL_VERIFIED,
        "direct_document_supported": False,
        "rate_limit_policy": "Fair usage",
        "notes": "Fertilizer distribution, grain procurement rates, and marketing cooperative guidelines.",
    },

    # -------------------------------------------------------------------------
    # 4. JAMMU AND KASHMIR GOVERNMENT SOURCES
    # -------------------------------------------------------------------------
    {
        "source_id": "jk_coop_dept",
        "name": "Cooperative Department, Jammu and Kashmir",
        "jurisdiction": "jk",
        "department": "Cooperative Department, UT of Jammu & Kashmir",
        "source_type": "official_ministry_portal",
        "base_url": "http://rcscoop.jk.gov.in",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "http://rcscoop.jk.gov.in/orders",
        "verification_status": STATUS_OFFICIAL_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "NIC J&K firewall applies; fallback to cached gazettes",
        "notes": "Statutory orders under J&K Act 1989, Section 63 audit panels, and PACS registrations.",
    },
    {
        "source_id": "jk_gov_portal",
        "name": "Government of Jammu & Kashmir Portal",
        "jurisdiction": "jk",
        "department": "General Administration Department, UT of J&K",
        "source_type": "official_state_portal",
        "base_url": "https://jk.gov.in",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "https://jk.gov.in",
        "verification_status": STATUS_LIVE_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "Fair usage (max 1 req/3s)",
        "notes": "Official administrative orders, Lt. Governor directives, and UT cooperative initiatives.",
    },
    {
        "source_id": "jkscb_portal",
        "name": "J&K State Cooperative Bank (JKSCB)",
        "jurisdiction": "jk",
        "department": "JKSCB, Srinagar",
        "source_type": "statutory_board",
        "base_url": "https://www.jkscb.com",
        "collection_method": "web_extract",
        "api_endpoint": None,
        "rss_feed_url": None,
        "announcement_page": "https://www.jkscb.com/notices",
        "verification_status": STATUS_OFFICIAL_VERIFIED,
        "direct_document_supported": True,
        "rate_limit_policy": "Fair usage",
        "notes": "Apple grower credit facilities, saffron grower KCC, and rural branch notifications.",
    },
]

class SourceRegistry:
    """Manages the centralized catalog of official government sources."""

    def __init__(self, sources: Optional[List[Dict[str, Any]]] = None):
        self._sources: Dict[str, Dict[str, Any]] = {}
        for s in (sources or OFFICIAL_SOURCES_CATALOG):
            self._sources[s["source_id"]] = dict(s)

    def get_all_sources(self) -> List[Dict[str, Any]]:
        return list(self._sources.values())

    def get_sources_by_jurisdiction(self, jurisdiction: str) -> List[Dict[str, Any]]:
        j_norm = (jurisdiction or "all").lower()
        if j_norm == "all":
            return list(self._sources.values())
        return [s for s in self._sources.values() if s["jurisdiction"] == j_norm]

    def get_source(self, source_id: str) -> Optional[Dict[str, Any]]:
        return self._sources.get(source_id)

    def get_sources_by_method(self, method: str) -> List[Dict[str, Any]]:
        m_norm = method.lower()
        return [s for s in self._sources.values() if s.get("collection_method") == m_norm]

    def update_status(self, source_id: str, status: str, notes: Optional[str] = None) -> bool:
        if source_id in self._sources:
            self._sources[source_id]["verification_status"] = status
            if notes:
                self._sources[source_id]["notes"] = notes
            logger.info("Updated source '%s' status to '%s'", source_id, status)
            return True
        return False

    def get_registry_summary(self) -> Dict[str, Any]:
        counts = {
            "total_sources": len(self._sources),
            "central": len(self.get_sources_by_jurisdiction("central")),
            "punjab": len(self.get_sources_by_jurisdiction("punjab")),
            "haryana": len(self.get_sources_by_jurisdiction("haryana")),
            "jk": len(self.get_sources_by_jurisdiction("jk")),
            "verified_active": sum(1 for s in self._sources.values() if "VERIFIED" in s.get("verification_status", "")),
        }
        return counts

source_registry = SourceRegistry()
