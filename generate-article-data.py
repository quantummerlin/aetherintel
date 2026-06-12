#!/usr/bin/env python3
"""
generate-article-data.py
Scans the articles/ directory and generates:
  - data/articles.json    → full article metadata for the JS frontend
  - data/search-index.json → lightweight search index

Usage: python generate-article-data.py
"""

import os
import re
import json
from html.parser import HTMLParser
from datetime import datetime

ARTICLES_DIR = "articles"
OUTPUT_DIR = "data"

class ArticleMetaExtractor(HTMLParser):
    """Extract key metadata from article HTML files."""
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.hero = ""
        self.date = ""
        self.category = ""
        self.canonical = ""
        self.in_title = False
        self.in_desc = False
        self.og_type = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == "title":
            self.in_title = True

        if tag == "meta":
            prop = attrs_dict.get("property", "")
            name = attrs_dict.get("name", "")
            content = attrs_dict.get("content", "")

            if name == "description":
                self.description = content
            elif prop == "og:image":
                self.hero = content
            elif prop == "article:published_time":
                self.date = content[:10]  # YYYY-MM-DD
            elif prop == "og:type":
                self.og_type = content

        if tag == "link" and attrs_dict.get("rel") == "canonical":
            self.canonical = attrs_dict.get("href", "")

        # Extract category from badge/cat divs
        if tag in ("span", "div"):
            cls = attrs_dict.get("class", "")
            if "badge" in cls or "article-card-cat" in cls:
                self._capture_category = True

    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()
        if getattr(self, '_capture_category', False):
            self.category = data.strip()
            self._capture_category = False

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False


def extract_from_html(filepath):
    """Parse an article HTML file and return metadata dict."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    parser = ArticleMetaExtractor()
    try:
        parser.feed(content)
    except Exception:
        pass

    # Fallback: regex extract category from card markup
    if not parser.category:
        cat_match = re.search(r'class="article-card-cat[^"]*">([^<]+)', content)
        if cat_match:
            parser.category = cat_match.group(1).strip()
    if not parser.category:
        badge_match = re.search(r'class="badge[^"]*">([^<]+)', content)
        if badge_match:
            parser.category = badge_match.group(1).strip()

    # Fallback: extract date from filename (NN-slug.html → no date)
    if not parser.date:
        # Try to find any date pattern in the file
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', content)
        if date_match:
            parser.date = date_match.group(1)

    # Build URL from canonical or filename
    url = parser.canonical
    if not url:
        fname = os.path.basename(filepath)
        url = f"/articles/{fname}"

    # Clean title (remove " – Aether Intel" suffix)
    title = parser.title.split(" – ")[0].split(" | ")[0].strip()

    # Determine badge class from category
    badge_map = {
        "Agents": "agents",
        "AI Safety": "news",
        "AI News": "news",
        "Dev & Build": "dev",
        "Tools": "dev",
        "Big Picture": "business",
        "AI & Culture": "news",
        "AI & Work": "ethics",
        "AI Research": "news",
        "Money": "business",
        "Honest Take": "news",
        "Business": "business",
        "AI Security": "news",
        "Human Edge": "ethics",
    }
    badge = badge_map.get(parser.category, "news")

    return {
        "title": title,
        "desc": parser.description[:160] if parser.description else "",
        "hero": parser.hero,
        "date": parser.date,
        "category": parser.category,
        "url": url,
        "badge": badge,
        "file": os.path.basename(filepath),
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    articles = []
    for fname in sorted(os.listdir(ARTICLES_DIR)):
        if not fname.endswith(".html"):
            continue
        fpath = os.path.join(ARTICLES_DIR, fname)
        meta = extract_from_html(fpath)
        if meta["title"]:  # Only include if we got a title
            articles.append(meta)
            print(f"  ✓ {fname}: {meta['title'][:60]}")
        else:
            print(f"  ✗ {fname}: no title found")

    # Sort by date descending (newest first)
    articles.sort(key=lambda a: a.get("date", ""), reverse=True)

    # Write full article data
    articles_path = os.path.join(OUTPUT_DIR, "articles.json")
    with open(articles_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {len(articles)} articles to {articles_path}")

    # Write lightweight search index
    search_index = [
        {
            "t": a["title"],
            "d": a["desc"][:120] if a["desc"] else "",
            "c": a["category"],
            "u": a["url"],
            "dt": a["date"],
        }
        for a in articles
    ]
    search_path = os.path.join(OUTPUT_DIR, "search-index.json")
    with open(search_path, "w", encoding="utf-8") as f:
        json.dump(search_index, f, ensure_ascii=False)
    print(f"Wrote search index ({len(search_index)} entries) to {search_path}")

    # Stats
    cats = {}
    for a in articles:
        c = a.get("category", "Unknown")
        cats[c] = cats.get(c, 0) + 1
    print(f"\nCategories:")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()
