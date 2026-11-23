import httpx
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

r = httpx.get('https://pib.gov.in/allRel.aspx', headers=headers, verify=False, timeout=10.0)
soup = BeautifulSoup(r.content, 'html.parser')

# Find release links
releases = []
for a in soup.find_all('a'):
    href = a.get('href', '')
    text = a.get_text(strip=True)
    if 'PressReleasePage.aspx' in href or 'PressReleaseIframePage.aspx' in href or 'PRID=' in href:
        releases.append((text, href))

print(f"Total PIB release links found: {len(releases)}")
for i, (text, href) in enumerate(releases[:8]):
    full_url = href if href.startswith('http') else f"https://pib.gov.in/{href.lstrip('/')}"
    print(f"  [{i}] {text} -> {full_url}")

