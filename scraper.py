import requests
from bs4 import BeautifulSoup

URL = "https://www.ayd.org.tr/alisveris-merkezleri"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers, timeout=30)

print("STATUS:", r.status_code)
print("URL:", r.url)
print("LENGTH:", len(r.text))

with open("ayd_page.html", "w", encoding="utf-8") as f:
    f.write(r.text)

soup = BeautifulSoup(r.text, "html.parser")

print("\nLINKS:")
for a in soup.find_all("a", href=True):
    text = a.get_text(" ", strip=True)
    href = a["href"]

    if text:
        print(text[:100], "=>", href)

print("\nSCRIPTS:")
for s in soup.find_all("script", src=True):
    print(s["src"])


