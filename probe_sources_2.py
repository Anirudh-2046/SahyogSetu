import ssl
import httpx
import feedparser
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

# 1. Inspect PIB RSS URL variants
pib_urls = [
    'https://pib.gov.in/rss/RssMain.aspx?ModId=6&Lang=1',
    'https://pib.gov.in/rss/rssmain.aspx',
    'https://pib.gov.in/PressReleasePage.aspx',
    'https://pib.gov.in/allRel.aspx'
]
for url in pib_urls:
    try:
        r = httpx.get(url, headers=headers, verify=False, timeout=5.0, follow_redirects=True)
        print(f"PIB [{url}]: {r.status_code}, len={len(r.content)}")
        if 'rss' in url.lower():
            feed = feedparser.parse(r.content)
            print(f"   feed entries: {len(feed.entries)}")
    except Exception as e:
        print(f"PIB [{url}] err: {e}")

# 2. Inspect Haryana Gov with follow_redirects
try:
    r_haryana = httpx.get('https://haryana.gov.in/', headers=headers, verify=False, timeout=8.0, follow_redirects=True)
    print(f"Haryana Gov (followed redirects): {r_haryana.status_code}, final_url={r_haryana.url}, len={len(r_haryana.content)}")
    soup = BeautifulSoup(r_haryana.content, 'html.parser')
    print(f"Haryana title: {soup.title.string if soup.title else 'No title'}")
except Exception as e:
    print(f"Haryana err: {e}")

# 3. Inspect Punjab Gov content
try:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.options |= 0x4
    with httpx.Client(verify=ctx, headers=headers, timeout=8.0, follow_redirects=True) as client:
        r_pb = client.get('https://punjab.gov.in/')
        print(f"Punjab Gov: {r_pb.status_code}, len={len(r_pb.content)}")
        soup = BeautifulSoup(r_pb.content, 'html.parser')
        print(f"Punjab title: {soup.title.string if soup.title else 'No title'}")
        links = soup.find_all('a')
        news_links = [a for a in links if a.get('href') and ('news' in a['href'] or 'press' in a['href'] or 'notif' in a['href'])]
        print(f"Punjab news links found: {len(news_links)}")
except Exception as e:
    print(f"Punjab err: {e}")

