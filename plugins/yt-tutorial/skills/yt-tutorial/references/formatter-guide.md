<formatting_requirements>

## Title Creation

Create a bold, hook-y title that follows this title pattern:

**Pattern:** `[Subject] [Verb Phrase That Promises an Outcome] — [Supplementary Hook]`

Examples:
- "Docker Lets You Run Anything in Isolated Containers — Here's How to Set It Up From Scratch"
- "Tailscale Turns Your Devices Into a Private Network — No Port Forwarding Required"
- "NixOS Lets You Version-Control Your Entire OS — Here's the Setup That Changed How I Manage Servers"

Follow the title with a bold subtitle/deck paragraph that tells the reader what they'll learn and who it's for.

## Document Organization

### Required Sections (in order)

1. **Title** (H1) — Bold, outcome-oriented, with hook
2. **Subtitle/Deck** — Bold paragraph setting expectations
3. **Horizontal rule** (`---`)
4. **"First Things First" / Context Section** (H2) — Level-set on prerequisites
5. **Horizontal rule**
6. **Core Concept** (H2) — What is this thing and why does it matter
7. **Horizontal rule**
8. **Main Content Sections** (H2 each) — The bulk of the tutorial, organized thematically
9. **Horizontal rule**
10. **Quick Reference Table** (H2) — Every command/concept summarized
11. **Horizontal rule**
12. **Closing Paragraph** — Italicized, reassuring, encourages incremental learning

### Section Heading Rules

- Major sections: `##` with title case (e.g., `## Installation and Basic Setup`)
- Subsections: `###` or **bold text** (e.g., `**Initial Configuration**`)
- Make headings descriptive — "Setting Up Your First Container" not "Setup"
- Never go deeper than H3; restructure instead
- Horizontal rules between major topic shifts only

## Text Formatting Standards

**Emphasis:**
- **Bold**: Key terms on first introduction, subsection headings, important concepts
- *Italics*: Technical modes, specific terms on second+ use, the closing paragraph
- `Code formatting`: Commands, filenames, config values, anything the reader would type

**Typography:**
- Em dashes (—) for asides, not parentheses or semicolons
- No emojis in prose
- Short paragraphs (2-4 sentences maximum)
- Single-sentence paragraphs fine for emphasis

**Bullet Points:**
- Use sparingly — only for listing options, tips, or related items
- Not for general prose or explanations
- Bold the first few words when items need scanning

## Content Transformation Rules

### From Transcript to Tutorial

The transcript is raw material. Transform it by:

1. **Stripping ALL timestamps** — No trace of time markers anywhere
2. **Reorganizing thematically** — Group related content together even if discussed at different points in the video. Move from foundational to advanced.
3. **Adding voice patterns** — Apply the Analogy Bridge, Permission Slip, Line-by-Line Decoder, and Motivation-First Setup patterns from the voice guide
4. **Expanding explanations** — If the speaker assumed knowledge, add the beginner-friendly explanation. Every technical term gets defined on first use.
5. **Formatting code/commands** — Put all commands in code blocks with language tags. Follow EVERY code block with a plain-English breakdown.

### What to Preserve Exactly

- All technical terminology (spelling, casing)
- All commands, code snippets, and syntax
- All numbers, prices, URLs, and specific references
- All examples and demonstrations (in full)
- All step-by-step instructions
- All warnings, tips, and caveats

### What to Transform

- Conversational filler → clean prose
- Chronological ordering → thematic ordering
- Assumed knowledge → explicit explanations
- Bare code/commands → code blocks + breakdowns
- Speaker's voice → tutorial voice (second person, direct, reassuring)

## Handling Common Transcript Patterns

**When the video covers multiple tools or options:**
- Create separate H2 sections for each tool/approach
- Use bold subsection headings to distinguish features
- Preserve all comparative details and trade-offs

**When the video includes live demos:**
- Reconstruct the demo as a step-by-step procedure (Step 1, Step 2...)
- Format all code/commands in code blocks
- Add line-by-line breakdowns
- Keep all explanations of what the demo shows

**When the speaker goes on tangents:**
- Reorganize the tangent content into the thematically appropriate section
- Preserve ALL information from the tangent — don't cut it
- Add smooth transitions so it reads naturally in its new location

**When the speaker uses jargon without explaining:**
- Add the explanation using the Analogy Bridge pattern
- "Think of it like..." before or alongside the first use
- Bold the term on first introduction

</formatting_requirements>

<research_guidelines>

## When and How to Research

### When to Research

Research examples and use cases when:
- The video explains concepts but doesn't show practical applications
- The video's examples are outdated or specific to the speaker's setup
- The user didn't provide their own examples
- Adding a real-world use case would make an abstract concept click

### When NOT to Research

Skip research when:
- The user explicitly provided examples or use cases to include
- The video already has thorough, current examples
- The topic is opinion-based or subjective (no "correct" examples exist)

### What to Research

For each major concept in the tutorial, look for:
1. **A concrete use case** — "Here's a real scenario where you'd use this"
2. **A minimal working example** — The smallest possible code/config that demonstrates the concept
3. **Common gotchas** — What trips people up when they first try this

### How to Integrate Research

- Weave researched examples naturally into the tutorial flow
- Don't create a separate "Additional Examples" section — place examples where they're relevant
- Use the Concrete Anchor pattern: show the specific thing, then explain what it demonstrates
- Cite the source if the example comes from official docs (link it with context)

</research_guidelines>
