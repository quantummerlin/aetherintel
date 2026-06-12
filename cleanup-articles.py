#!/usr/bin/env python3
"""
cleanup-articles.py
Removes Google Analytics and AdSense from all article HTML files.
Updates canonical URLs from ai.quantummerlin.com → aetherintel.au.
Standardizes card markup.

Usage: python cleanup-articles.py
"""

import os
import re
import glob

ARTICLES_DIR = "articles"

# Patterns to remove (GA + AdSense scripts)
REMOVE_PATTERNS = [
    # Google Analytics gtag
    r'<script async src="https://www\.googletagmanager\.com/gtag/js\?id=[^"]+"></script>\s*\n?\s*<script>window\.dataLayer.*?gtag\(\'config\',\'[^\']+\'\);</script>',
    # AdSense
    r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js\?client=[^"]+" crossorigin="anonymous"></script>',
]

# URL replacements
URL_REPLACEMENTS = [
    ('https://ai.quantummerlin.com', 'https://aetherintel.au'),
]

# Card markup standardization
# Some articles use: <div class="article-card-cat cat-XXX">Category</div>
# Others use: <span class="badge badge-XXX">Category</span>
# We want: <span class="badge badge-XXX">Category</span> (consistent)


def clean_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Remove tracking scripts
    for pattern in REMOVE_PATTERNS:
        content = re.sub(pattern, '', content, flags=re.DOTALL)

    # Replace URLs
    for old_url, new_url in URL_REPLACEMENTS:
        content = content.replace(old_url, new_url)

    # Clean up any resulting double-blank-lines (max 2 consecutive)
    content = re.sub(r'\n{3,}', '\n\n', content)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    files = sorted(glob.glob(os.path.join(ARTICLES_DIR, "*.html")))
    changed = 0
    for fpath in files:
        if clean_file(fpath):
            changed += 1
            print(f"  ✓ Cleaned: {os.path.basename(fpath)}")
        else:
            print(f"  - No changes: {os.path.basename(fpath)}")

    print(f"\n{changed} of {len(files)} files updated.")


if __name__ == "__main__":
    main()
