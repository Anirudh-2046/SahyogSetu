import ssl
import httpx
import feedparser
from bs4 import BeautifulSoup

print("=== 1. AUDITING PIB (PRESS INFORMATION BUREAU) ===")
try:
    r_pib = httpx.get('https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1', timeout=10.0, verify=False)
    feed = feedparser.parse(r_pib.content)
    print(f"PIB Feed Title: {feed.feed.get('title')}")
    print(f"PIB Total Entries: {len(feed.entries)}")
    for i, entry in enumerate(feed.entries[:3]):
        print(f"  [{i}] Title: {entry.get('title')}")
        print(f"      Link: {entry.get('link')}")
        print(f"      Published: {entry.get('published')}")
        print(f"      Summary: {entry.get('summary', '')[:100]}...")
except Exception as e:
    print(f"PIB error: {e}")

print("\n=== 2. AUDITING MINISTRY OF COOPERATION (cooperation.gov.in) ===")
try:
    r_coop = httpx.get('https://cooperation.gov.in/en/whats-new', timeout=10.0, verify=False)
    print(f"Ministry of Cooperation (Whats New): status={r_coop.status_code}, bytes={len(r_coop.content)}")
    if r_coop.status_code == 200:
        soup = BeautifulSoup(r_coop.content, 'html.parser')
        rows = soup.find_all(['tr', 'li', 'article'])
        print(f"Found {len(rows)} elements in what's new")
        # Let's inspect titles or links
        links = soup.find_all('a')
        coop_links = [a for a in links if a.get_text(strip=True) and len(a.get_text(strip=True)) > 20]
        print(f"Found {len(coop_links)} descriptive links. Sample: {coop_links[0].get_text(strip=True) if coop_links else 'None'}")
except Exception as e:
    print(f"Cooperation error: {e}")

print("\n=== 3. AUDITING HARYANA GOVERNMENT (haryana.gov.in) ===")
try:
    r_haryana = httpx.get('https://haryana.gov.in/', timeout=10.0, verify=False)
    print(f"Haryana Gov: status={r_haryana.status_code}, bytes={len(r_haryana.content)}")
    soup = BeautifulSoup(r_haryana.content, 'html.parser')
    news_items = soup.find_all(class_=lambda c: c and ('news' in c.lower() or 'press' in c.lower() or 'update' in c.lower()))
    print(f"Found {len(news_items)} news/press containers")
except Exception as e:
    print(f"Haryana error: {e}")

print("\n=== 4. AUDITING PUNJAB GOVERNMENT (punjab.gov.in) ===")
try:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    with httpx.Client(verify=ctx, timeout=10.0) as client:
        r_pb = client.get('https://punjab.gov.in/')
        print(f"Punjab Gov: status={r_pb.status_code}, bytes={len(r_pb.content)}")
except Exception as e:
    print(f"Punjab error: {e}")

print("\n=== 5. AUDITING JAMMU & KASHMIR (jk.gov.in) ===")
try:
    r_jk = httpx.get('https://jk.gov.in/', timeout=10.0, verify=False)
    print(f"JK Gov: status={r_jk.status_code}, bytes={len(r_jk.content)}")
except Exception as e:
    print(f"JK error: {e}")

