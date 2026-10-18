import requests
from bs4 import BeautifulSoup
import json
import time
import os

SITEMAP_URL = "https://www.anthropic.com/sitemap.xml"
OUTPUT_FILE = "task1/anthropic_docs.jsonl"

def get_all_urls():
    print(f"Fetching sitemap: {SITEMAP_URL}")
    resp = requests.get(SITEMAP_URL, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'lxml-xml')
    urls = [loc.text for loc in soup.find_all('loc')]
    print(f"Found {len(urls)} URLs")
    return urls

def scrape_page(url):
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return None
        soup = BeautifulSoup(r.text, 'html.parser')
        # Remove scripts
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()
        text = soup.get_text(separator='\n', strip=True)
        # Clean extra blank lines
        lines = [l.strip() for l in text.splitlines() if len(l.strip()) > 30]
        clean_text = "\n".join(lines)[:10000] # limit 10k chars per page
        if len(clean_text) < 100:
            return None
        return {"url": url, "text": clean_text}
    except Exception as e:
        print(f"  Failed {url}: {e}")
        return None

def main():
    
    urls = get_all_urls()
    os.makedirs("task1", exist_ok=True)
    count = 0
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for i, url in enumerate(urls):
            print(f"[{i+1}/{len(urls)}] Scraping {url}")
            data = scrape_page(url)
            if data:
                f.write(json.dumps(data) + "\n")
                count += 1
            time.sleep(0.5) # polite delay
    print(f"\nDone! Saved {count} pages to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()