import ssl
import httpx
from bs4 import BeautifulSoup
import feedparser

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

def probe_all():
    results = {}
    sources = [
        ("PIB Releases", "https://www.pib.gov.in/allRel.aspx?lang=1"),
        ("PIB Hindi", "https://www.pib.gov.in/allRel.aspx?lang=2"),
        ("Ministry of Cooperation", "https://cooperation.gov.in/"),
        ("Ministry of Cooperation What's New", "https://cooperation.gov.in/en/whats-new"),
        ("Haryana Government Portal", "https://www.haryana.gov.in/"),
        ("Haryana RCS", "https://rcsharyana.gov.in/"),
        ("Punjab Government Portal", "https://punjab.gov.in/"),
        ("Punjab RCS", "http://rcs.punjab.gov.in/"),
        ("J&K Government Portal", "https://jk.gov.in/"),
        ("J&K Cooperative Dept", "http://rcscoop.jk.gov.in/"),
    ]

    for name, url in sources:
        print(f"Auditing {name} ({url})...")
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.options |= 0x4  # SSL_OP_LEGACY_SERVER_CONNECT
        try:
            with httpx.Client(verify=ctx, headers=headers, timeout=8.0, follow_redirects=True) as client:
                res = client.get(url)
                print(f"  -> Status: {res.status_code}, Bytes: {len(res.content)}, Final: {res.url}")
        except Exception as e:
            print(f"  -> Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    probe_all()

