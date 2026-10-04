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

# Try importing YouTube transcript helper
try:
    from .fetch_youtube_transcript import is_youtube_url, fetch_youtube_transcript, extract_video_id
except ImportError:
    try:
        from fetch_youtube_transcript import is_youtube_url, fetch_youtube_transcript, extract_video_id
    except ImportError:
        # Fallback if fetch_youtube_transcript.py is in the same directory
        import os
        scripts_dir = os.path.dirname(os.path.abspath(__file__))
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        try:
            from fetch_youtube_transcript import is_youtube_url, fetch_youtube_transcript, extract_video_id
        except ImportError:
            is_youtube_url = lambda u: False
            fetch_youtube_transcript = None
            extract_video_id = lambda u: None

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

def fetch_url(url: str, include_timestamps: bool = True):
    """
    Fetches content and metadata from a web page or YouTube video URL.
    """
    # 1. Handle YouTube URLs
    if is_youtube_url(url):
        if fetch_youtube_transcript is None:
            print("Warning: fetch_youtube_transcript module not available. Install youtube-transcript-api.", file=sys.stderr)
            return None
        try:
            yt_data = fetch_youtube_transcript(url, include_timestamps=include_timestamps)
            return {
                "url": yt_data["url"],
                "title": f"{yt_data['title']} — {yt_data['author']} (YouTube)",
                "raw_title": yt_data["title"],
                "author": yt_data["author"],
                "author_url": yt_data["author_url"],
                "description": yt_data["description"] or f"YouTube video transcript for '{yt_data['title']}' by {yt_data['author']}.",
                "text": yt_data["text"],
                "duration_formatted": yt_data["duration_formatted"],
                "language": yt_data["language"],
                "is_generated": yt_data["is_generated"],
                "is_video": True,
                "video_id": yt_data["video_id"],
                "paragraphs": yt_data.get("paragraphs", [])
            }
        except Exception as e:
            print(f"Error fetching YouTube transcript: {e}", file=sys.stderr)
            return None

    # 2. Handle standard web URLs
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
                "text": parser.get_content(),
                "is_video": False
            }
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fetch URL content or YouTube video transcripts.")
    parser.add_argument("url", help="URL to fetch (webpage or YouTube video)")
    parser.add_argument("--full", action="store_true", help="Print entire content instead of preview")
    parser.add_argument("--no-timestamps", action="store_true", help="Omit timestamps for YouTube transcripts")
    args = parser.parse_args()

    res = fetch_url(args.url, include_timestamps=not args.no_timestamps)
    if res:
        print(f"=== TITLE: {res['title']} ===")
        if res.get("is_video"):
            print(f"=== CHANNEL: {res.get('author', 'N/A')} ===")
            print(f"=== DURATION: {res.get('duration_formatted', 'N/A')} ===")
            print(f"=== LANGUAGE: {res.get('language', 'en')} (Generated: {res.get('is_generated', False)}) ===")
        print(f"=== DESCRIPTION: {res['description']} ===")
        print("=== CONTENT PREVIEW ===")
        if args.full:
            print(res["text"])
        else:
            print(res["text"][:1500])
            if len(res["text"]) > 1500:
                print("\n... [Run with --full to view entire content]")

