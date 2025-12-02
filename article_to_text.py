import trafilatura
import hashlib
import os

def link_to_id(url: str) -> str:
    """Generate deterministic unique ID from URL."""
    return hashlib.sha256(url.encode()).hexdigest()[:16]   # shorter but still safe

def download(url: str):
    article_id = link_to_id(url)

    downloaded = trafilatura.fetch_url(url)
    if downloaded is None:
        print(f"❌ Failed to fetch: {url}")
        return

    blog_text = trafilatura.extract(
        downloaded,
        output_format="json",
        with_metadata=True,
        include_tables=True,
        include_links=True,
        include_comments=False
    )

    if blog_text is None:
        print(f"❌ Trafilatura couldn't extract content: {url}")
        return

    filename = f"article_{article_id}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(blog_text)

    print(f"✔ Saved → {filename}")

if __name__ == "__main__":
    # download("https://www.cnbc.com/2025/11/27/puma-shares-chinas-anta-sports-is-reportedly-looking-to-buy-the-firm.html") -- great
    # download("https://www.gsmarena.com/compare.php3?idPhone1=14050&idPhone2=13315") -- failed
    # download("https://medium.com/ai-advances/the-reality-of-agentic-ai-why-my-weekend-project-became-a-nightmare-3899df1ea1dd") -- failed to fetch
    download("")
