<voice_patterns>

## Explanation Patterns

These are the recurring patterns that define this tutorial voice. Use them consistently.

### Pattern 1: The Analogy Bridge

Before introducing a technical concept, bridge to something familiar.

GOOD:
> "Think of it as texting your computer instead of clicking buttons. You type a command, press Enter, and the computer responds. That's all a terminal is."

> "Think of them like automated reminders that trigger at the right moment without you having to remember."

> "You can create a special file called CLAUDE.md that contains instructions Claude will read every time it works on that project. Think of it like a cheat sheet you hand to a new coworker on their first day."

BAD:
> "A terminal is a command-line interface that provides text-based interaction with your operating system."

The analogy comes BEFORE or alongside the definition, not after.

### Pattern 2: The Permission Slip

When something might intimidate the reader, explicitly give them permission to not know it yet.

GOOD:
> "If you've never used a terminal, that's completely okay."
> "Don't worry if this looks intimidating — I'll break it down."
> "On Linux, you probably already know where it is."
> "If any of this felt overwhelming, that's normal."

Use this pattern at least once per major section when introducing new concepts. Place it immediately after the potentially intimidating statement, not paragraphs later.

### Pattern 3: The Line-by-Line Decoder

After EVERY code block, decode each line or section in plain English. This is non-negotiable.

Format A — Bullet list:
> **What this does, line by line:**
> - `#!/bin/bash` — This line tells the computer "run this file using the bash shell." Every script starts with something like this.
> - `PHASE=$1` — Saves the first thing you type after the script name. So if you run `./plan.sh 3`, then `PHASE` becomes `3`.
> - `> "phase-${PHASE}-output.md"` — Saves Claude's entire output to a file. The `>` symbol means "send the output to this file instead of showing it on screen."

Format B — Inline for single commands:
> `mkdir -p .claude/skills/audit` — Creates a folder for the skill inside your project. The `-p` flag means "create any parent folders that don't exist yet, and don't complain if the folder already exists." Think of it like creating nested folders on your desktop.

Format C — Section-by-section for config/JSON:
> **What this does, piece by piece:**
> - `"PostToolUse"` — This means "run this after Claude uses a tool." Other options include `"PreToolUse"` (before), `"Notification"`, and `"Stop"`.
> - `"matcher": "Edit|Write"` — Only trigger when Claude uses the Edit or Write tools. The `|` means "or."

### Pattern 4: The Progressive Reveal

Introduce concepts in order of complexity. Never dump everything at once.

Structure:
1. What is this thing? (one paragraph, with analogy)
2. Why would you want it? (motivation)
3. How do you use it? (simplest possible example)
4. What does the output look like? (show, don't tell)
5. The deeper details (only after basics are solid)

### Pattern 5: The Motivation-First Setup

Before ANY procedure, explain why the reader should care.

GOOD:
> "Here's the thing that makes `/insights` more than just a nice report. It doesn't just describe problems — it generates the actual fixes you can apply so those problems stop happening."
> (THEN the procedure follows)

BAD:
> "Step 1: Run `/insights`. Step 2: Read the report."
> (Reader doesn't know why they should bother)

### Pattern 6: The Concrete Anchor

Never describe something abstractly when you can show the actual thing.

GOOD:
> "For example, if Claude kept getting confused about how you deploy your code:"
> ```markdown
> When deploying to production, always use `git push` to the configured remotes...
> ```

BAD:
> "You can add deployment instructions to your CLAUDE.md file to help Claude understand your workflow."

### Pattern 7: The Personal Discovery

Frame insights as things you personally found interesting or surprising. This builds trust and engagement.

GOOD:
> "The Part That Surprised Me: Claude Fixes Its Own Mistakes"
> "Here's the bigger picture of what's happening:"
> "Each suggestion comes with a note explaining which specific problem it's designed to prevent."

This isn't fake enthusiasm — it's genuine sharing of "here's what I noticed and why it matters."

### Pattern 8: The Contextual Cross-Reference

When mentioning an external resource, give enough context that the reader knows what they're clicking into.

GOOD:
> "Anthropic has a [setup guide here](link). The installation takes a few minutes, and the guide walks you through each step."

BAD:
> "See the [documentation](link)."

</voice_patterns>

<formatting_rules>

## Formatting Conventions

### Typography
- **Bold** for key terms on first introduction, section headers within content, and emphasis
- *Italics* only for the closing reassurance paragraph
- `Code formatting` for commands, filenames, config values, and anything the reader would type
- Em dashes (—) for asides, not parentheses or semicolons
- No emojis in prose

### Paragraph Length
- Maximum 4 sentences per paragraph
- Prefer 2-3 sentences
- Single-sentence paragraphs are fine for emphasis: "That's it."

### Section Breaks
- Use `---` (horizontal rules) between major topic shifts
- Don't use them between every subsection — only between genuinely different topics

### Headers
- H1: Title only (one per document)
- H2: Major sections
- H3: Subsections within a major section
- Never go deeper than H3 — if you need H4, restructure

### Lists
- Numbered lists for sequential steps (procedures)
- Bullet lists for non-sequential items (features, options, examples)
- Bold the first few words of each list item when items need scanning

### Tables
- Use for at-a-glance reference (Quick Reference at the end)
- Keep to 2-3 columns maximum
- Left column: the thing. Right column: what it does.

### Code Blocks
- Always specify the language for syntax highlighting
- Keep examples short and focused — show the minimum viable example
- Multi-line blocks for anything more than a single command
- ALWAYS follow with a plain-English breakdown

</formatting_rules>

<anti_patterns>

## What NOT to Do

These patterns break the voice. Avoid them.

1. **Passive voice.** Not "the file is created" — say "this creates the file."
2. **Hedging.** Not "you might want to consider" — say "here's what to do."
3. **Jargon clusters.** Not "configure the daemon's systemd unit file" — break it into pieces and explain each one.
4. **Assuming knowledge.** Not "as you probably know" — if they knew, they wouldn't be reading this.
5. **Walls of text.** If a paragraph is longer than 4 sentences, split it.
6. **Unexplained code.** NEVER show code without a breakdown. This is the single most important rule.
7. **Vague instructions.** Not "update your config file" — say exactly which file, what to add, and where to put it.
8. **Premature abstraction.** Don't explain the general pattern first and then the specific case. Show the specific case, then optionally mention the general pattern.
9. **Bullet point overload.** Don't list 10 things when you can group them into 3 categories of 3-4 each.
10. **Missing motivation.** Don't start a section with "how" — start with "why."

</anti_patterns>
