import re
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

BASE = "https://www.avmlist.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AVMListResearch/1.0)"
}

def fetch(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text

def extract_links(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        u = urljoin(BASE, a["href"])

        if urlparse(u).netloc.endswith("avmlist.com"):
            links.append(u)

    return sorted(set(links))

def main():
    pages = [
        BASE,
        BASE + "avmler/",
        BASE + "avm/",
        BASE + "sitemap.xml",
        BASE + "sitemap_index.xml",
        BASE + "wp-sitemap.xml",
        BASE + "robots.txt",
    ]

    all_links = set()
    report = []

    for url in pages:
        try:
            html = fetch(url)
            links = extract_links(html)
            all_links.update(links)
            report.append(f"{url} -> {len(links)} links")
        except Exception as e:
            report.append(f"{url} -> ERROR: {e}")

    avm_links = sorted(
        u.rstrip("/") + "/"
        for u in all_links
        if re.match(
            r"^https?://(?:www\.)?avmlist\.com/avm/[^/]+/?$",
            u
        )
    )

    with open("discovery.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report))
        f.write("\n\nAVM LINKS\n")
        f.write("\n".join(avm_links))
        f.write(f"\n\nCOUNT={len(avm_links)}\n")

    print(f"Found {len(avm_links)} AVM URLs")

if __name__ == "__main__":
    main()
