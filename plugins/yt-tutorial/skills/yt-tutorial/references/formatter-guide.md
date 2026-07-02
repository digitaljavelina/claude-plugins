<formatting_requirements>

## Title Creation

Create a bold, specific title that follows this pattern:

**Pattern:** `[Subject] [Verb Phrase That Promises an Outcome], [Supplementary Hook]`

Examples:
- "Docker Runs Anything in Isolated Containers. Here's the Setup From Scratch."
- "Tailscale Turns Your Devices Into a Private Network, No Port Forwarding"
- "NixOS Version-Controls Your Whole OS: the Setup That Changed How I Manage Servers"

Follow the title with a bold deck paragraph that states what the reader will learn and the assumed baseline.

## Document Organization

### Required Sections (in order)

1. **Title** (H1): Bold, outcome-oriented, specific
2. **Deck** (bold paragraph): States the angle and the assumed baseline
3. **Horizontal rule** (`---`)
4. **Prerequisites & Assumptions** (H2, brief): What the reader should already know and what needs installing. Skip if nothing non-trivial.
5. **Horizontal rule**
6. **Core Concept** (H2): The mental model, then why it matters and the tradeoff
7. **Horizontal rule**
8. **Main Content Sections** (H2 each): The bulk of the tutorial, organized thematically
9. **Horizontal rule**
10. **Quick Reference Table** (H2): Every command/concept summarized
11. **Horizontal rule**
12. **Closing** (optional, brief): A peer note, not reassurance. The honest limitation or the real next step.

### Section Heading Rules

- Major sections: `##` with title case (e.g., `## Installation and Basic Setup`)
- Subsections: `###` or **bold text** (e.g., `**Initial Configuration**`)
- Make headings descriptive: "Setting Up Your First Container" not "Setup"
- Never go deeper than H3; restructure instead
- Horizontal rules between major topic shifts only

## Text Formatting Standards

**Emphasis:**
- **Bold**: Key terms on first introduction, subsection headings, important concepts
- *Italics*: Light emphasis, technical modes, terms on second+ use
- `Code formatting`: Commands, filenames, config values, anything the reader would type

**Typography:**
- Periods, not em dashes. For an aside, use a period and a new sentence, or parentheses. Never a U+2014 em dash.
- No emojis in prose
- Focused paragraphs; a dense paragraph is fine when explaining a real mechanism or tradeoff
- Single-sentence paragraphs fine for emphasis

**Bullet Points:**
- Use sparingly, only for listing options, tips, or related items
- Not for general prose or explanations
- Bold the first few words when items need scanning

## Content Transformation Rules

### From Transcript to Tutorial

The transcript is raw material. Transform it by:

1. **Stripping ALL timestamps**: No trace of time markers anywhere
2. **Reorganizing thematically**: Group related content together even if discussed at different points in the video. Move from foundational to advanced.
3. **Applying voice patterns**: Use Precise Framing, Gotchas Over Reassurance, Decode the Non-Obvious, and Motivation and Tradeoffs First from the voice guide
4. **Explaining at intermediate altitude**: Where the speaker assumed tool-specific knowledge, add the explanation. Define tool-specific terms on first use. Assume standard tooling (terminals, flags, git, config files); do not re-teach it.
5. **Formatting code/commands**: Put all commands in code blocks with language tags. Follow each code block with a sentence of context plus a breakdown of the non-obvious parts, never a bare command with a one-line label.

### What to Preserve Exactly

- All technical terminology (spelling, casing)
- All commands, code snippets, and syntax
- All numbers, prices, URLs, and specific references
- All examples and demonstrations (in full)
- All step-by-step instructions
- All warnings, tips, and caveats

### What to Transform

- Conversational filler to clean prose
- Chronological ordering to thematic ordering
- Assumed tool-specific knowledge to explicit explanation (standard tooling stays assumed)
- Bare code/commands to code blocks plus a breakdown of the non-obvious parts
- Speaker's voice to tutorial voice (second person, direct)

## Handling Common Transcript Patterns

**When the video covers multiple tools or options:**
- Create separate H2 sections for each tool/approach
- Use bold subsection headings to distinguish features
- Preserve all comparative details and trade-offs

**When the video includes live demos:**
- Reconstruct the demo as a step-by-step procedure (Step 1, Step 2...)
- Format all code/commands in code blocks
- Add a breakdown of the non-obvious parts
- Keep all explanations of what the demo shows

**When the speaker goes on tangents:**
- Reorganize the tangent content into the thematically appropriate section
- Preserve ALL information from the tangent, don't cut it
- Add smooth transitions so it reads naturally in its new location

**When the speaker uses tool-specific jargon without explaining:**
- Add a concise, precise definition on first use
- Reach for an analogy only if the concept is genuinely counterintuitive
- Bold the term on first introduction
- Do not explain standard tooling the reader already knows

</formatting_requirements>

<research_guidelines>

## When and How to Research

### When to Research

Research examples and use cases when:
- The video explains concepts but doesn't show practical applications
- The video's examples are outdated or specific to the speaker's setup
- The user didn't provide their own examples
- A real-world use case would make an abstract concept concrete

### When NOT to Research

Skip research when:
- The user explicitly provided examples or use cases to include
- The video already has thorough, current examples
- The topic is opinion-based or subjective (no "correct" examples exist)

### What to Research

For each major concept in the tutorial, look for:
1. **A real use case**: "Here's a scenario where you'd actually reach for this"
2. **A minimal working example**: The smallest code/config that demonstrates the concept
3. **Common gotchas**: What trips people up when they first try this for real

### How to Integrate Research

- Weave researched examples naturally into the tutorial flow
- Don't create a separate "Additional Examples" section, place examples where they're relevant
- Show the specific thing, then explain what it demonstrates
- Cite the source if the example comes from official docs (link it with context)

</research_guidelines>
