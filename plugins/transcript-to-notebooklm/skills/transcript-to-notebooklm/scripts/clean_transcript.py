#!/usr/bin/env python3
"""Convert .srt / .vtt / timestamped transcripts into clean, flowing .txt.

The goal is to take subtitle or transcript files (which are cluttered with cue
indices, timecodes, formatting tags, and sometimes duplicated rolling-caption
lines) and turn them into readable prose suitable for feeding to NotebookLM or
any other reader. Files that are already clean prose (no timecodes) are passed
through with light whitespace normalization so the same command works on a
whole mixed folder.

Usage:
    clean_transcript.py INPUT [INPUT ...] [--outdir DIR]
                              [--no-reflow] [--strip-speakers]

Each INPUT produces "<stem>.txt" in --outdir (default: ./converted). The script
prints one summary line per file and exits non-zero only if every input failed.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# A subtitle timecode line, e.g. "00:00:03,158 --> 00:00:04,081" (SRT uses a
# comma before millis, VTT uses a dot). Hours are optional in some tools.
TIMECODE_RE = re.compile(
    r"\d{1,2}:\d{2}(?::\d{2})?[.,]\d{1,3}\s*-->\s*\d{1,2}:\d{2}(?::\d{2})?[.,]\d{1,3}"
)
# A standalone cue index (a line that is nothing but an integer).
INDEX_RE = re.compile(r"^\d+$")
# Inline tags: HTML-ish (<i>, <c.color>), VTT karaoke timestamps (<00:00:01.000>).
TAG_RE = re.compile(r"<[^>]+>")
# ASS/SSA style override blocks like {\an8}.
CURLY_RE = re.compile(r"\{[^}]*\}")
# A leading timestamp on a transcript line: "[00:01:23]", "(0:45)", "00:01 - ".
LEADING_TS_RE = re.compile(
    r"^\s*[\[\(]?\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d{1,3})?[\]\)]?\s*[-–—]?\s*"
)
# A line that is only a bracketed non-speech cue: "[Music]", "(applause)".
SOUND_CUE_RE = re.compile(r"^\s*[\[\(](?:music|applause|laughter|inaudible|crosstalk|silence)[^\])]*[\]\)]\s*$", re.I)
# An optional speaker label at the start of a line: "John:", "SPEAKER 1:".
SPEAKER_RE = re.compile(r"^\s*[A-Z][A-Za-z0-9 .'_-]{0,30}:\s+")
# VTT structural lines we always drop.
VTT_NOISE_RE = re.compile(r"^(WEBVTT|NOTE\b|STYLE\b|REGION\b)", re.I)


def looks_like_subtitle(text: str) -> bool:
    """True if the file contains subtitle timecodes (so it's SRT/VTT-shaped)."""
    return TIMECODE_RE.search(text) is not None


def strip_inline(line: str) -> str:
    """Remove inline tags and override blocks, collapse internal whitespace."""
    line = TAG_RE.sub("", line)
    line = CURLY_RE.sub("", line)
    return re.sub(r"\s+", " ", line).strip()


def parse_subtitle(text: str, strip_speakers: bool) -> list[str]:
    """Pull just the spoken text out of an SRT/VTT file.

    We drop cue indices, timecode lines, and VTT structural lines, then keep the
    remaining text. Consecutive identical fragments are de-duplicated, which
    cleans up YouTube-style rolling captions that repeat the previous line.
    """
    fragments: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if TIMECODE_RE.search(line):
            continue
        if INDEX_RE.match(line):
            continue
        if VTT_NOISE_RE.match(line):
            continue
        cleaned = strip_inline(line)
        if not cleaned or SOUND_CUE_RE.match(cleaned):
            continue
        if strip_speakers:
            cleaned = SPEAKER_RE.sub("", cleaned)
        # De-dup consecutive repeats (rolling captions).
        if fragments and fragments[-1] == cleaned:
            continue
        fragments.append(cleaned)
    return fragments


def parse_plain(text: str, strip_speakers: bool) -> list[str]:
    """Clean a plain transcript: strip leading timestamps and sound cues.

    Already-clean prose survives this untouched apart from whitespace tidying,
    so the same command can run over a mixed folder of subtitles and prose.
    """
    out: list[str] = []
    for raw in text.splitlines():
        line = LEADING_TS_RE.sub("", raw.strip())
        line = strip_inline(line)
        if not line or SOUND_CUE_RE.match(line):
            continue
        if strip_speakers:
            line = SPEAKER_RE.sub("", line)
        out.append(line)
    return out


def reflow(fragments: list[str], target: int = 350) -> str:
    """Join fragments into prose and regroup into readable paragraphs.

    Subtitle fragments are tiny (a few words each); joined raw they form a wall
    of text. We join with spaces, then start a new paragraph once the current
    one passes ~target characters and a sentence has just ended, which keeps
    paragraphs reasonable without guessing at the original structure.
    """
    joined = re.sub(r"\s+", " ", " ".join(fragments)).strip()
    if not joined:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+", joined)
    paras: list[str] = []
    cur = ""
    for s in sentences:
        cur = f"{cur} {s}".strip()
        if len(cur) >= target:
            paras.append(cur)
            cur = ""
    if cur:
        paras.append(cur)
    # Auto-generated captions often have no sentence punctuation, so the split
    # above yields one giant paragraph. Hard-wrap any over-long paragraph at word
    # boundaries so the output stays readable. Well-punctuated text stays under
    # the limit and is left alone.
    wrapped: list[str] = []
    for para in paras:
        if len(para) <= target * 3:
            wrapped.append(para)
            continue
        words, line = para.split(), ""
        for w in words:
            if line and len(line) + 1 + len(w) > target * 2:
                wrapped.append(line)
                line = w
            else:
                line = f"{line} {w}".strip()
        if line:
            wrapped.append(line)
    return "\n\n".join(wrapped)


def convert_one(path: Path, outdir: Path, do_reflow: bool, strip_speakers: bool) -> Path:
    text = path.read_text(encoding="utf-8", errors="replace")
    if looks_like_subtitle(text):
        fragments = parse_subtitle(text, strip_speakers)
    else:
        fragments = parse_plain(text, strip_speakers)

    if do_reflow:
        body = reflow(fragments)
    else:
        body = "\n".join(fragments)

    outdir.mkdir(parents=True, exist_ok=True)
    out_path = outdir / f"{path.stem}.txt"
    out_path.write_text(body + "\n", encoding="utf-8")
    return out_path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="Transcript/subtitle files to convert")
    ap.add_argument("--outdir", default="converted", help="Output directory (default: ./converted)")
    ap.add_argument("--no-reflow", action="store_true", help="Keep one line per cue instead of reflowing into paragraphs")
    ap.add_argument("--strip-speakers", action="store_true", help="Remove leading speaker labels like 'John:'")
    args = ap.parse_args(argv)

    outdir = Path(args.outdir)
    ok = 0
    for raw in args.inputs:
        p = Path(raw)
        if not p.is_file():
            print(f"skip (not a file): {p}", file=sys.stderr)
            continue
        try:
            out = convert_one(p, outdir, not args.no_reflow, args.strip_speakers)
        except Exception as e:  # keep going on the rest of the batch
            print(f"FAIL {p.name}: {e}", file=sys.stderr)
            continue
        chars = out.stat().st_size
        print(f"ok  {p.name}  ->  {out}  ({chars} bytes)")
        ok += 1

    print(f"\nConverted {ok}/{len(args.inputs)} file(s) into {outdir}/")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
