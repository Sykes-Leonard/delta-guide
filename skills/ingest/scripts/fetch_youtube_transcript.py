#!/usr/bin/env python3
"""
fetch_youtube_transcript.py - YouTube Video Transcript & Metadata Extractor

Fetches captions/transcripts from YouTube videos using `youtube-transcript-api`
and retrieves video metadata (title, author, description) via public oEmbed and meta tags.
Part of the OKF v0.2 Knowledge Base Ingestion Skill.
"""

import sys
import os
import re
import json
import urllib.request
import urllib.parse
from typing import Dict, List, Optional, Any, Tuple

# Regex to match various YouTube URL formats or standalone video IDs
YOUTUBE_URL_PATTERN = re.compile(
    r'(?:https?:\/\/)?(?:www\.|m\.)?(?:youtube\.com\/(?:watch\?(?:.*&)?v=|embed\/|v\/|shorts\/|live\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
)
VIDEO_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{11}$')


def extract_video_id(url_or_id: str) -> Optional[str]:
    """Extract 11-character YouTube video ID from a URL or raw ID string."""
    url_or_id = url_or_id.strip()
    match = YOUTUBE_URL_PATTERN.search(url_or_id)
    if match:
        return match.group(1)
    if VIDEO_ID_PATTERN.match(url_or_id):
        return url_or_id
    return None


def is_youtube_url(url_or_id: str) -> bool:
    """Return True if the input represents a YouTube video URL or ID."""
    return extract_video_id(url_or_id) is not None


def format_timestamp(seconds: float) -> str:
    """Convert seconds into HH:MM:SS or MM:SS format."""
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def fetch_youtube_metadata(video_id: str) -> Dict[str, Any]:
    """
    Fetch public video metadata using YouTube's official oEmbed endpoint
    and scrape description/tags from the watch page meta tags.
    """
    canonical_url = f"https://www.youtube.com/watch?v={video_id}"
    metadata: Dict[str, Any] = {
        "video_id": video_id,
        "url": canonical_url,
        "title": f"YouTube Video ({video_id})",
        "author_name": "YouTube Creator",
        "author_url": "",
        "thumbnail_url": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
        "description": "",
    }

    # 1. Fetch oEmbed metadata
    oembed_url = f"https://www.youtube.com/oembed?url={urllib.parse.quote(canonical_url)}&format=json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 KnowledgeGuideIngest/1.0"
    }

    try:
        req = urllib.request.Request(oembed_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
            if "title" in data:
                metadata["title"] = data["title"]
            if "author_name" in data:
                metadata["author_name"] = data["author_name"]
            if "author_url" in data:
                metadata["author_url"] = data["author_url"]
            if "thumbnail_url" in data:
                metadata["thumbnail_url"] = data["thumbnail_url"]
    except Exception as e:
        print(f"Warning: Could not fetch oEmbed metadata for {video_id}: {e}", file=sys.stderr)

    # 2. Extract description from watch page HTML meta tags
    try:
        req = urllib.request.Request(canonical_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
            desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.DOTALL)
            if not desc_match:
                desc_match = re.search(r'<meta\s+property=["\']og:description["\']\s+content=["\'](.*?)["\']', html, re.DOTALL)
            if desc_match:
                metadata["description"] = desc_match.group(1).strip()
    except Exception as e:
        # Non-critical, description can remain empty
        pass

    return metadata


def _chunk_snippets(snippets: List[Any], chunk_seconds: int = 30, max_chars: int = 400) -> List[Tuple[float, str]]:
    """
    Groups raw transcript snippets into natural, readable paragraphs
    anchored by a starting timestamp.
    """
    chunks: List[Tuple[float, str]] = []
    curr_start: Optional[float] = None
    curr_texts: List[str] = []

    for s in snippets:
        # Support both object attributes (.text, .start) and dict keys (['text'], ['start'])
        text = getattr(s, "text", None) if hasattr(s, "text") else s.get("text", "")
        start = getattr(s, "start", 0.0) if hasattr(s, "start") else s.get("start", 0.0)

        cleaned = text.strip().replace("\n", " ")
        if not cleaned:
            continue

        if curr_start is None:
            curr_start = start

        curr_texts.append(cleaned)
        combined = " ".join(curr_texts)

        if (start - curr_start >= chunk_seconds) or (len(combined) >= max_chars):
            chunks.append((curr_start, combined))
            curr_start = None
            curr_texts = []

    if curr_texts and curr_start is not None:
        chunks.append((curr_start, " ".join(curr_texts)))

    return chunks


def fetch_youtube_transcript(
    url_or_id: str,
    languages: Optional[List[str]] = None,
    include_timestamps: bool = True,
    chunk_seconds: int = 30,
) -> Dict[str, Any]:
    """
    Fetches transcript and video metadata for a YouTube video.

    Returns a dict with:
        url: canonical YouTube URL
        video_id: 11-character video ID
        title: video title
        author: channel name
        author_url: channel URL
        description: video description
        language: transcript language code used
        is_generated: bool indicating if captions are auto-generated
        paragraphs: list of {"timestamp": "MM:SS", "seconds": float, "text": str}
        text: formatted transcript string
        raw_snippets: list of raw snippets
    """
    video_id = extract_video_id(url_or_id)
    if not video_id:
        raise ValueError(f"Invalid YouTube URL or Video ID: '{url_or_or_id}'" if 'url_or_or_id' in locals() else f"Invalid YouTube URL or Video ID: '{url_or_id}'")

    # Verify dependency is installed
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        import youtube_transcript_api._errors as yt_errors
    except ImportError:
        raise ImportError(
            "The 'youtube-transcript-api' library is required to ingest YouTube videos.\n"
            "Please install it with:\n"
            "    pip install youtube-transcript-api\n"
            "or (on macOS with externally-managed Python):\n"
            "    pip install --break-system-packages youtube-transcript-api"
        )

    # 1. Fetch metadata
    meta = fetch_youtube_metadata(video_id)

    # 2. Setup preferred languages
    preferred_languages = languages or ["en", "en-US", "en-GB"]

    fetched_snippets = None
    lang_used = "en"
    is_generated = False

    # Instantiate API
    ytt = YouTubeTranscriptApi()

    # Attempt fetching via TranscriptList to inspect available languages & fallbacks
    try:
        transcript_list = ytt.list(video_id)

        # First, try to find a transcript matching preferred languages
        transcript_obj = None
        try:
            transcript_obj = transcript_list.find_transcript(preferred_languages)
        except Exception:
            pass

        # If not found directly, check for any manually created transcript
        if transcript_obj is None:
            try:
                transcript_obj = transcript_list.find_manually_created_transcript(preferred_languages)
            except Exception:
                pass

        # If still not found, check for any auto-generated transcript
        if transcript_obj is None:
            try:
                transcript_obj = transcript_list.find_generated_transcript(preferred_languages)
            except Exception:
                pass

        # If still not found, try translating the first available transcript to English
        if transcript_obj is None:
            for t in transcript_list:
                try:
                    if t.is_translatable:
                        transcript_obj = t.translate(preferred_languages[0])
                        break
                except Exception:
                    continue

        # Ultimate fallback: pick the very first transcript available
        if transcript_obj is None:
            for t in transcript_list:
                transcript_obj = t
                break

        if transcript_obj is not None:
            lang_used = getattr(transcript_obj, "language_code", "en")
            is_generated = getattr(transcript_obj, "is_generated", False)
            fetched_snippets = transcript_obj.fetch()
    except Exception as e:
        # Fallback to direct fetch shortcut if list() fails or in older versions
        try:
            fetched_snippets = ytt.fetch(video_id, languages=preferred_languages)
        except Exception as inner_e:
            raise RuntimeError(
                f"Failed to fetch transcript for YouTube video {video_id} ('{meta['title']}').\n"
                f"Reason: {e} (Fallback also failed: {inner_e})"
            )

    if not fetched_snippets:
        raise RuntimeError(f"No transcript content could be retrieved for YouTube video {video_id}.")

    # 3. Format chunks & paragraphs
    chunks = _chunk_snippets(fetched_snippets, chunk_seconds=chunk_seconds)

    paragraphs_data = []
    formatted_lines = []

    for start_sec, text in chunks:
        ts_str = format_timestamp(start_sec)
        paragraphs_data.append({
            "timestamp": ts_str,
            "seconds": start_sec,
            "text": text
        })
        if include_timestamps:
            formatted_lines.append(f"[{ts_str}] {text}")
        else:
            formatted_lines.append(text)

    formatted_text = "\n\n".join(formatted_lines)

    total_duration = 0.0
    if paragraphs_data:
        last = paragraphs_data[-1]
        total_duration = last["seconds"]

    return {
        "url": meta["url"],
        "video_id": video_id,
        "title": meta["title"],
        "author": meta["author_name"],
        "author_url": meta["author_url"],
        "thumbnail_url": meta["thumbnail_url"],
        "description": meta["description"],
        "language": lang_used,
        "is_generated": is_generated,
        "duration_seconds": total_duration,
        "duration_formatted": format_timestamp(total_duration),
        "paragraph_count": len(paragraphs_data),
        "paragraphs": paragraphs_data,
        "text": formatted_text,
        "is_video": True
    }


def generate_okf_markdown_transcript(data: Dict[str, Any]) -> str:
    """Formats the extracted transcript into a ready-to-use Markdown document."""
    lines = [
        f"# {data['title']}",
        "",
        "---",
        "",
        "## Video Information",
        f"- **Channel / Creator**: [{data['author']}]({data['author_url']})" if data['author_url'] else f"- **Channel / Creator**: {data['author']}",
        f"- **Source URL**: [{data['url']}]({data['url']})",
        f"- **Language**: `{data['language']}` {'(auto-generated captions)' if data.get('is_generated') else '(official transcript)'}",
        f"- **Approximate Duration**: {data.get('duration_formatted', 'N/A')}",
        "",
    ]

    if data.get("description"):
        lines.extend([
            "### Video Description",
            "> " + data["description"].replace("\n", "\n> "),
            "",
        ])

    lines.extend([
        "---",
        "",
        "## Transcript",
        "",
        data["text"],
        ""
    ])

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Extract YouTube video transcripts and metadata using youtube-transcript-api."
    )
    parser.add_argument("url_or_id", help="YouTube video URL or 11-character video ID")
    parser.add_argument("-t", "--timestamps", action="store_true", default=True, help="Include timestamps in output (default: True)")
    parser.add_argument("--no-timestamps", dest="timestamps", action="store_false", help="Omit timestamps")
    parser.add_argument("-l", "--languages", help="Comma-separated language codes in priority order (default: 'en,en-US,en-GB')")
    parser.add_argument("-f", "--format", choices=["text", "markdown", "json", "preview"], default="preview", help="Output format (default: preview)")
    parser.add_argument("-o", "--output", help="Write output to specified file path")
    parser.add_argument("--chunk-seconds", type=int, default=30, help="Seconds to group into each paragraph (default: 30)")

    args = parser.parse_args()

    langs = [lang.strip() for lang in args.languages.split(",")] if args.languages else None

    try:
        data = fetch_youtube_transcript(
            args.url_or_id,
            languages=langs,
            include_timestamps=args.timestamps,
            chunk_seconds=args.chunk_seconds
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        output = json.dumps(data, indent=2, ensure_ascii=False)
    elif args.format == "markdown":
        output = generate_okf_markdown_transcript(data)
    elif args.format == "text":
        output = data["text"]
    else:  # preview
        preview_chars = 1500
        output = (
            f"=== TITLE: {data['title']} ===\n"
            f"=== CHANNEL: {data['author']} ===\n"
            f"=== URL: {data['url']} ===\n"
            f"=== LANGUAGE: {data['language']} (Generated: {data['is_generated']}) ===\n"
            f"=== DURATION: {data['duration_formatted']} ({data['paragraph_count']} paragraphs) ===\n"
            f"=== DESCRIPTION PREVIEW ===\n{data['description'][:300]}...\n\n"
            f"=== TRANSCRIPT PREVIEW (First {preview_chars} chars) ===\n"
            f"{data['text'][:preview_chars]}\n"
            f"...\n[Transcript truncated for preview. Use --format text or --format markdown to see all]"
        )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Transcript written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
