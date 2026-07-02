<voice_patterns>

## Explanation Patterns

These are the recurring patterns that define this tutorial voice. The reader is a competent developer or technical tinkerer who is new to THIS specific tool or topic, not new to computing. Assume fluency with the terminal, shells, git, package managers, editing config/JSON/YAML, reading code, and common CLI conventions. Do not re-teach those. Use these patterns consistently.

### Pattern 1: Precise Framing

Introduce a new tool-specific concept with a clear, precise explanation. Give it a few sentences: what it is, how it actually works, and why it matters. Get to the mental model fast, but do not compress it into a single line the reader has to unpack on their own. A competent reader still wants the concept explained, just not padded or analogized to death.

GOOD:
> "A hook is a shell command Claude Code runs automatically at a defined point in its lifecycle. `PreToolUse` fires before a tool call and can block it. `Stop` fires when Claude finishes a turn."

Reach for an analogy only when a concept is genuinely counterintuitive, and make it earn its place. Never analogize things a working developer already knows.

BAD:
> "Think of the terminal as texting your computer instead of clicking buttons."

The reader already knows what a terminal is. Spend the words on what is actually new.

### Pattern 2: Gotchas Over Reassurance

Do not reassure the reader that a concept is okay to find hard. Spend that space on the sharp edges instead: the non-obvious failure modes, the flag that behaves unexpectedly, the ordering that matters, what breaks in practice.

GOOD:
> "The matcher is a regex, not a glob. `Edit|Write` works, but `*.py` silently matches nothing. Match on the tool name, not the file path."
> "`git push` here pushes to every configured remote, not just origin. If you only meant origin, name it."

BAD:
> "If you have never written a hook before, that's completely okay. Don't worry, we'll take it slow."

### Pattern 3: Decode the Non-Obvious

After a code block, say what it does as a whole in a sentence, then decode the parts a competent reader cannot infer at a glance: the tool's own syntax, novel flags, non-obvious composition, side effects. Give every code block enough surrounding context that the reader never has to stop and reverse-engineer it. You do not need to define standard shell, but do explain what the command accomplishes and why it belongs here.

Format A, bullet list for the parts that need it:
> **What matters here:**
> - `--print title --print channel`: `yt-dlp` prints these fields in order, one per line. Order is how you parse the output.
> - `--skip-download`: metadata only, no media file written. Easy to forget and end up with a stray download.

Format B, inline for a single non-obvious command:
> `hooks.Stop[].matcher`: an empty string matches every Stop event. There is no tool name to filter on for `Stop`, so leave it empty.

You do not need to define `mkdir -p`, `cd`, `>`, or `|` token by token. But do explain what the overall command accomplishes and call out any part that is load-bearing for the point you are making. A bare command with a one-word label is too little. Aim for a short paragraph of context, not a bare list.

### Pattern 4: Core-Model-First Progression

Lead with the tool's mental model, then real usage, then edge cases. Do not slow-walk to the point or re-teach fundamentals.

Structure:
1. The core model: what this is and how it actually works (one tight paragraph)
2. Motivation: when you reach for it, what it replaces, what it costs
3. Real usage: a realistic example, not a toy one
4. Edge cases and gotchas: what bites you once you use it for real

### Pattern 5: Motivation and Tradeoffs First

Before a procedure, explain why, at intermediate altitude. That means the decision, not just the benefit: when to use this, when not to, what it replaces, what it trades away.

GOOD:
> "Hooks run on every matching event, synchronously, and block the turn until they exit. That makes them right for fast guardrails and wrong for anything slow. If your check takes two seconds, you will feel it on every edit."

BAD:
> "Step 1: Add a hook. Step 2: Test it." (No decision context.)

### Pattern 6: Concrete, Realistic Anchors

Never describe something abstractly when you can show the actual thing. Prefer realistic examples over toy ones. Show real commands, real config, real output.

GOOD:
> "For example, a `PreToolUse` hook that blocks edits to `.env` files:"
> ```json
> { "matcher": "Edit|Write", "hooks": [{ "type": "command", "command": "python3 guard-env.py" }] }
> ```

BAD:
> "You can add a hook to your settings to guard certain files."

### Pattern 7: Earned Insight

Share the non-obvious thing you actually learned: the surprising interaction, the thing the docs do not tell you, the opinion you formed from using it. Peer to peer, not performed enthusiasm.

GOOD:
> "The docs frame hooks as automation. The more useful framing is that they are the only place you can make Claude Code do something deterministically. Everything else is a request the model can ignore."

### Pattern 8: Precise Cross-References

When you point at an external resource, link the exact relevant doc or section and say what is there and why the reader would click it.

GOOD:
> "The full matcher grammar is in Anthropic's [hooks reference](link), under Tool Matchers. Worth reading if you need anything beyond a tool-name match."

BAD:
> "See the [documentation](link)."

</voice_patterns>

<formatting_rules>

## Formatting Conventions

### Typography
- **Bold** for key terms on first introduction, section headers within content, and emphasis
- *Italics* for light emphasis and asides
- `Code formatting` for commands, filenames, config values, and anything the reader would type
- Periods, not em dashes. For an aside, use a period and a new sentence, or parentheses. Never a U+2014 em dash.
- No emojis in prose

### Paragraph Length
- Keep paragraphs focused, but err toward explaining a bit more rather than less. A tutorial is prose with commands in it, not a command list with one-line labels. Surround steps and code with enough explanation that the reasoning and the flow are clear.
- A dense paragraph is fine when it explains a real mechanism or tradeoff. Do not pad, and do not artificially chop a coherent explanation into one-sentence fragments.
- Single-sentence paragraphs are fine for emphasis: "That is the whole trick."

### Section Breaks
- Use `---` (horizontal rules) between major topic shifts
- Don't use them between every subsection, only between genuinely different topics

### Headers
- H1: Title only (one per document)
- H2: Major sections
- H3: Subsections within a major section
- Never go deeper than H3. If you need H4, restructure.

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
- Keep examples realistic and focused. Prefer a real example over a toy one.
- Follow a code block with a sentence of context (what it does and why) plus a breakdown of the non-obvious parts (see Pattern 3). You do not need to narrate every trivial token, but never leave a command standing with only a one-line label.

</formatting_rules>

<anti_patterns>

## What NOT to Do

These patterns break the voice. Avoid them.

1. **Re-teaching fundamentals.** The reader knows what a terminal, a flag, git, and a config file are. Do not explain them. Explain what is specific to this tool.
2. **Reassurance filler.** No "don't worry," no "if this feels overwhelming, that's normal." Respect the reader's competence. If something is genuinely tricky, name the specific gotcha instead.
3. **Passive voice.** Not "the file is created," say "this creates the file."
4. **Hedging.** Not "you might want to consider," say "do this" or "here is the tradeoff."
5. **Token-by-token narration of the obvious.** Do not break `mkdir -p` down to "folders on your desktop." Explain what the command does as a whole and decode the non-obvious parts, but skip the trivial symbols.
6. **Unexplained non-obvious code.** The flip side: never show tool-specific syntax or a novel flag and move on. Decode the part that is actually new.
7. **Vague instructions.** Not "update your config file," say exactly which file, what to add, and where.
8. **Premature abstraction.** Show the concrete case first, then generalize if useful.
9. **Bullet point overload.** Don't list 10 things when you can group them into 3 categories of 3-4 each.
10. **Missing motivation or tradeoffs.** Don't start a section with "how." Start with why you would reach for this, and when you would not.
11. **Command dumping.** A wall of commands or steps with one-line labels and no connective prose is not a tutorial. Explain the reasoning and the flow between steps. Lean toward explaining a bit more than feels strictly necessary, just not to the point of re-teaching fundamentals.

</anti_patterns>
