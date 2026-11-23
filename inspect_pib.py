import httpx
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

r = httpx.get('https://pib.gov.in/allRel.aspx', headers=headers, verify=False, timeout=10.0)
soup = BeautifulSoup(r.content, 'html.parser')

print("Title:", soup.title.string if soup.title else "No title")
# Find all a tags
all_a = soup.find_all('a')
print(f"Total <a> tags: {len(all_a)}")
for a in all_a[:15]:
    print("  href:", a.get('href'), "text:", a.get_text(strip=True)[:60])

# Also check for li tags, ul tags, or divs with releases
divs = soup.find_all('div', class_=True)
classes = set(c for d in divs for c in d.get('class', []))
print("Sample classes in page:", list(classes)[:15])

