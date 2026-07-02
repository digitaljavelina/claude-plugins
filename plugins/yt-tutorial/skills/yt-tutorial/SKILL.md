---
name: yt-tutorial
description: Transform YouTube videos into intermediate-level, publishable tutorials. Fetches the transcript, researches examples, and rewrites in a direct explainer voice pitched at a competent reader new to the topic. Use when converting a YouTube video into a written guide.
---

<essential_principles>

## What This Skill Does

This skill takes a YouTube URL and produces a complete, publishable tutorial. It combines three systems:

1. **Transcript extraction**: Uses `yt-dlp` and `youtube-transcript-api` to pull the video transcript and metadata
2. **Tutorial voice**: Applies a direct, concrete explainer voice pitched at a competent developer new to the topic (the named patterns in `references/voice-guide.md`)
3. **Transcript formatting**: Structures the raw transcript into a professionally organized document

The output reads like an original tutorial, not like a transcript. All timestamps are stripped, content is reorganized thematically, and every tool-specific concept gets a precise explanation. Standard tooling (terminals, flags, git, config files) is assumed, not re-taught.

## Voice Rules

This skill bundles all of its voice rules. Before writing, ALWAYS read:

- `references/voice-guide.md`: The named voice patterns
- `references/structure-template.md`: Section-by-section template

Key rules that apply to every paragraph:

- Second person always ("you" not "one" or "the user")
- Assume baseline competence; explain tool-specific terms on first use, not fundamentals
- Why and the tradeoff before how
- Analogies only when a concept is genuinely counterintuitive
- Focused paragraphs, but err toward explaining a bit more; dense is fine when explaining a real mechanism
- Code blocks followed by a sentence of context plus a breakdown of the non-obvious parts; never a bare command with a one-line label
- Periods, not em dashes; no emojis in prose
- Name the real gotcha instead of reassuring

## Content Preservation

**CRITICAL**: Do not summarize, condense, or paraphrase the video's content. The tutorial must contain the same level of detail as the original transcript. Preserve:

- All examples and demonstrations
- All explanations and reasoning
- All step-by-step instructions
- All technical specifications and commands
- All practical use cases
- All warnings, tips, and additional context

The job is to REFORMAT and REWRITE in tutorial voice at an intermediate reading level, not to shorten. "Intermediate" changes the altitude of the explanation (assume competence, skip fundamentals, name gotchas), never the completeness of the coverage.

</essential_principles>

<intake>
What video would you like to turn into a tutorial?

Provide:

1. **YouTube URL** (required)
2. **Destination folder** (optional): Default: `Inbox/` in the Obsidian vault
3. **Specific examples or use cases to include** (optional): If not provided, I'll research relevant ones

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Next Action |
|----------|-------------|
| YouTube URL provided | Route to workflows/transcript-to-tutorial.md |
| URL + specific examples/use cases | Skip research phase, route to workflows/transcript-to-tutorial.md |
| "help" | Explain skill capabilities |

Before writing, ALWAYS read these references:

- references/formatter-guide.md: Formatting and structural requirements
- references/voice-guide.md: Voice patterns
- references/structure-template.md: Section template and transitions

**After reading the workflow and references, follow them exactly.**
</routing>

<success_criteria>
A completed yt-tutorial:

- Reads like an original tutorial, not a transcript
- Contains ALL detail from the original video (no summarizing)
- Explains tool-specific terms on first use; assumes standard tooling
- Every code block followed by a breakdown of its non-obvious parts
- Organized thematically (not chronologically from the video)
- Has: title, deck, major sections, quick reference table, and an optional peer closing
- Names the real gotchas instead of reassuring
- Includes researched examples/use cases (unless user provided their own)
- No timestamps remain anywhere in the document
- Saved to the vault and ready to publish
</success_criteria>
