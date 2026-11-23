"""
Text Extractor for Government News Announcements
Extracts clean, structured text from raw API responses, RSS payloads, and HTML pages.
"""

from bs4 import BeautifulSoup

class TextExtractor:
    """Extracts relevant textual content from HTML or structured payloads."""

    @staticmethod
    def extract_from_html(html_content: str) -> str:
        if not html_content:
            return ""
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Remove noisy tags
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
            tag.decompose()

        # Find main article container if present
        main = soup.find(["article", "main", "div[role='main']"]) or soup
        return main.get_text(separator="\n", strip=True)

    @staticmethod
    def extract_from_rss_item(entry: dict) -> str:
        """Extracts text from RSS entry summary/content."""
        text = entry.get("summary", "") or entry.get("description", "")
        if "content" in entry and isinstance(entry["content"], list) and len(entry["content"]) > 0:
            text = entry["content"][0].get("value", text)
        return TextExtractor.extract_from_html(text)

