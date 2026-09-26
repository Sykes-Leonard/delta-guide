#!/usr/bin/env python3
"""
fetch_content.py - Lightweight URL fetcher and metadata extractor for the Ingest skill.
Extracts title, meta description, and plain text content using standard Python libraries.
"""

import sys
import re
import urllib.request
import urllib.parse
from html.parser import HTMLParser

class SimpleHTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_desc = ""
        self.text_parts = []
        self._in_title = False
        self._in_script_or_style = False
        self._skip_tags = {"script", "style", "noscript", "svg", "header", "footer", "nav"}

    def handle_starttag(self, tag, attrs):
        tag_lower = tag.lower()
        if tag_lower == "title":
            self._in_title = True
        elif tag_lower in self._skip_tags:
            self._in_script_or_style = True
        elif tag_lower == "meta":
            attr_dict = dict((k.lower(), v) for k, v in attrs if v)
            if attr_dict.get("name") in ["description", "og:description", "twitter:description"]:
                if not self.meta_desc:
                    self.meta_desc = attr_dict.get("content", "")

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower == "title":
            self._in_title = False
        elif tag_lower in self._skip_tags:
            self._in_script_or_style = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()
        elif not self._in_script_or_style:
            cleaned = data.strip()
            if cleaned:
                self.text_parts.append(cleaned)

    def get_content(self):
        return "\n\n".join(self.text_parts)

def fetch_url(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 KnowledgeGuideIngest/1.0"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            html_raw = resp.read().decode(charset, errors="replace")
            
            parser = SimpleHTMLTextExtractor()
            parser.feed(html_raw)
            
            return {
                "url": url,
                "title": parser.title or "Untitled Document",
                "description": parser.meta_desc or "",
                "text": parser.get_content()
            }
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_content.py <url>")
        sys.exit(1)
        
    res = fetch_url(sys.argv[1])
    if res:
        print(f"=== TITLE: {res['title']} ===")
        print(f"=== DESCRIPTION: {res['description']} ===")
        print("=== CONTENT PREVIEW ===")
        print(res["text"][:1500])
