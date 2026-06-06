#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "youtube-transcript-api>=1.0.0",
#     "requests",
# ]
# ///
"""
Fetch YouTube transcript using youtube-transcript-api.
Uses uv for automatic dependency management - no manual install needed.

Usage:
    ./fetch-transcript.py <youtube-url-or-video-id>
    # or
    uv run fetch-transcript.py <youtube-url-or-video-id>

Output:
    Prints the full transcript text to stdout (no timestamps).
    Prints video metadata as JSON comment at the start.
"""

import sys
import re
import json
from pathlib import Path

COOKIE_FILE = Path.home() / ".config" / "yt-cookies" / "youtube.txt"


def extract_video_id(url_or_id):
    """Extract video ID from various YouTube URL formats."""
    # Already a video ID
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id

    # Standard watch URL
    match = re.search(r'[?&]v=([a-zA-Z0-9_-]{11})', url_or_id)
    if match:
        return match.group(1)

    # Short URL (youtu.be)
    match = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', url_or_id)
    if match:
        return match.group(1)

    # Embed URL
    match = re.search(r'embed/([a-zA-Z0-9_-]{11})', url_or_id)
    if match:
        return match.group(1)

    # Shorts URL
    match = re.search(r'shorts/([a-zA-Z0-9_-]{11})', url_or_id)
    if match:
        return match.group(1)

    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def fetch_transcript(video_id):
    """Fetch transcript and return as plain text."""
    from youtube_transcript_api import YouTubeTranscriptApi

    # Create API instance with cookies if available (bypasses YouTube bot detection)
    if COOKIE_FILE.exists():
        import http.cookiejar
        import requests
        cj = http.cookiejar.MozillaCookieJar(str(COOKIE_FILE))
        cj.load(ignore_discard=True, ignore_expires=True)
        session = requests.Session()
        session.cookies = cj
        ytt_api = YouTubeTranscriptApi(http_client=session)
    else:
        ytt_api = YouTubeTranscriptApi()

    try:
        # Try to get transcript, preferring manual captions over auto-generated
        transcript_list = ytt_api.list_transcripts(video_id)

        # Try manual transcripts first (more accurate)
        try:
            transcript = transcript_list.find_manually_created_transcript(['en'])
        except:
            # Fall back to auto-generated
            try:
                transcript = transcript_list.find_generated_transcript(['en'])
            except:
                # Last resort: get any available transcript
                transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])

        # Fetch the actual transcript data
        transcript_data = transcript.fetch()

        # Join all text segments
        full_text = ' '.join([entry.text for entry in transcript_data])

        return full_text

    except Exception as e:
        # If the fancy method fails, try the simple fetch method
        try:
            transcript_data = ytt_api.fetch(video_id)
            full_text = ' '.join([entry.text for entry in transcript_data])
            return full_text
        except Exception as fallback_error:
            raise Exception(f"Could not fetch transcript: {e}. Fallback also failed: {fallback_error}")


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run fetch-transcript.py <youtube-url-or-video-id>", file=sys.stderr)
        sys.exit(1)

    url_or_id = sys.argv[1]

    try:
        video_id = extract_video_id(url_or_id)
        transcript = fetch_transcript(video_id)

        # Output metadata as JSON comment
        metadata = {
            "video_id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}"
        }
        print(f"<!-- VIDEO_METADATA: {json.dumps(metadata)} -->")
        print()
        print(transcript)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
