---
name: yt-tutorial
description: Transform YouTube videos into beginner-friendly, publication-ready tutorials. Fetches the transcript, researches examples, and writes in the established tutorial voice. Use when converting a YouTube video into a blog post or guide.
---

<essential_principles>

## What This Skill Does

This skill takes a YouTube URL and produces a complete, publication-ready tutorial. It combines three systems:

1. **Transcript extraction** — Uses `yt-dlp` and `youtube-transcript-api` to pull the video transcript and metadata
2. **Tutorial voice** — Applies a conversational, beginner-friendly explainer voice (the 8 named patterns in `references/voice-guide.md`)
3. **Transcript formatting** — Structures the raw transcript into a professionally organized document

The output reads like an original tutorial, not like a transcript. All timestamps are stripped, content is reorganized thematically, and every technical concept gets the full explainer treatment (analogies, code breakdowns, reassurance patterns).

## Voice Rules

This skill bundles all of its voice rules. Before writing, ALWAYS read:

- `references/voice-guide.md` — The 8 named voice patterns
- `references/structure-template.md` — Section-by-section template

Key rules that apply to every paragraph:

- Second person always ("you" not "one" or "the user")
- Explain every technical term on first use
- WHY before HOW — motivate before instructing
- Analogies for abstract concepts
- Short paragraphs (2-4 sentences max)
- Every code block followed by a plain-English breakdown
- Em dashes for asides, no emojis in prose
- Reassurance near anything potentially intimidating

## Content Preservation

**CRITICAL**: Do not summarize, condense, or paraphrase the video's content. The tutorial must contain the same level of detail as the original transcript. Preserve:

- All examples and demonstrations
- All explanations and reasoning
- All step-by-step instructions
- All technical specifications and commands
- All practical use cases
- All warnings, tips, and additional context

The job is to REFORMAT and REWRITE in tutorial voice — not to shorten.

</essential_principles>

<intake>
What video would you like to turn into a tutorial?

Provide:

1. **YouTube URL** (required)
2. **Destination folder** (optional) — Default: `Inbox/` in the Obsidian vault
3. **Specific examples or use cases to include** (optional) — If not provided, I'll research relevant ones

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Next Action |
|----------|-------------|
| YouTube URL provided | Route to workflows/transcript-to-tutorial.md |
| URL + specific examples/use cases | Skip research phase, route to workflows/transcript-to-tutorial.md |
| "help" | Explain skill capabilities |

Before writing, ALWAYS read these references:

- references/formatter-guide.md — Formatting and structural requirements
- references/voice-guide.md — Voice patterns (8 named patterns)
- references/structure-template.md — Section template and transitions

**After reading the workflow and references, follow them exactly.**
</routing>

<success_criteria>
A completed yt-tutorial:

- Reads like an original tutorial, not a transcript
- Contains ALL detail from the original video (no summarizing)
- Every technical term explained on first use with an analogy
- Every code block followed by a plain-English breakdown
- Organized thematically (not chronologically from the video)
- Has: title, introduction, major sections, conclusion, quick reference table, italicized closing
- Includes researched examples/use cases (unless user provided their own)
- No timestamps remain anywhere in the document
- Saved to the vault and ready to publish
  </success_criteria>
