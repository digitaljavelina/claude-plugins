<structure_template>

## Tutorial Structure

Every tutorial follows this skeleton. Sections can be added or removed based on the topic, but the ordering and voice conventions are fixed.

### 1. Title (H1)

Bold, specific, and outcome-oriented. Promise the reader something concrete.

Pattern: **[Subject] [Verb Phrase That Promises an Outcome] — [Supplementary Hook]**

Examples:

- "Claude Code Has a Secret Command That Makes It Smarter Over Time — Here's How to Use It"
- "You Can Run a Full Home Server on a $35 Raspberry Pi — Here's the Setup I Use"
- "NixOS Lets You Version-Control Your Entire Operating System — Here's How to Get Started"

Avoid:

- "A Guide to X" (boring)
- "How to Do X" (acceptable but try for more energy)
- "Everything You Need to Know About X" (too vague, sounds like filler)

### 2. Subtitle / Deck (bold paragraph, right after title)

One or two sentences that tell the reader exactly what the tutorial covers and who it's for. Set expectations.

Pattern: **"[What we'll cover], [why it matters], and [who this is for] — [permission slip]."**

Example:

> **There's a hidden command in Claude Code called `/insights` that studies how you work and then tells you exactly how to make it work better for you. Let's walk through what it does, why it matters, and how to use it — even if you've never opened a terminal before.**

### 3. Horizontal Rule

```
---
```

### 4. Core Concept Section (H2)

Explain WHAT the thing is and WHY it matters. No instructions yet — just understanding.

Pattern:

- "So What Is [X]?"
- Describe what it does in plain language
- List the specific questions it answers or problems it solves (bullet list)
- Highlight the most important aspect: "That last point is the important one. We'll get to it shortly."

### 5. Horizontal Rule

### 6. How-To Section (H2)

Step-by-step instructions. Numbered steps. Each step is short and focused.

Pattern:

- "How to [Do the Thing]"
- "This part is simple." (if it is — set the tone)
- **Step 1:** [Instruction] + context for beginners
- **Step 2:** [Instruction]
- **Step 3:** [Instruction]
- Close with what to expect: "That's it. Claude will think for a bit and then..."

### 7. Horizontal Rule

### 8. What to Expect / Output Section (H2)

Show the reader what the result looks like. Walk through each part.

Pattern:

- "What [the Output] Looks Like"
- Describe each section/component of the output
- Use **bold labels** followed by an em-dash explanation
- Example: **At a Glance** — A quick summary. What's working well, what's causing problems.

### 9. Horizontal Rule

### 10. Deep Dive Sections (H2, multiple)

The meat of the tutorial. Each section covers one major sub-topic.

Pattern for each:

- H2 with an engaging title (can use "The Part That Surprised Me" framing)
- Open with WHY this matters
- Show a concrete example (code block, config, screenshot description)
- Follow with the line-by-line breakdown
- Include a practical note about variations or gotchas
- Optionally use H3 subsections (Fix 1, Fix 2, Fix 3...)

### 11. Horizontal Rule

### 12. The Bigger Picture Section (H2)

Zoom out. Explain how everything fits together.

Pattern:

- "Here's the bigger picture of what's happening:"
- Numbered list showing the workflow/feedback loop
- Explain why this compounds over time
- Optionally include supporting data or metrics

### 13. Horizontal Rule

### 14. Advanced / What's Next Section (H2, optional)

For readers who want to go further. Keep it brief — just plant seeds.

### 15. Horizontal Rule

### 16. Quick Reference Table (H2)

Summarize every command, concept, or tool mentioned in the tutorial.

Format:

```markdown
## Quick Reference: [Topic] Mentioned in This Guide

| [Thing]           | What It Does      |
| ----------------- | ----------------- |
| `command`         | Brief description |
| `another-command` | Brief description |
```

### 17. Horizontal Rule

### 18. Closing Paragraph (italicized)

Normalize difficulty. Encourage incremental learning. End warmly.

Pattern:

> _If any of this felt overwhelming, that's normal. [Acknowledge the complexity]. Start with just [one simple thing]. You don't have to [do everything at once]. Pick one [thing], try it, and see if it helps. That's how everyone learns this stuff — one piece at a time._

</structure_template>

<section_transitions>

## Transition Patterns Between Sections

Sections should flow naturally. Here are transition patterns that maintain voice:

**Core Concept → How-To:**

> "Let's set it up." / "Here's what you do." / "This part is simple."

**How-To → Output:**

> "Once you run that, here's what you'll see."

**Output → Deep Dive:**

> "The [section name] is where it gets useful." / "Here's the thing that makes this more than just a [basic thing]."

**Deep Dive → Deep Dive:**

> Use H3 sub-headers (Fix 1, Fix 2) or start the new section by connecting it to the previous: "Beyond [previous topic], the report also includes..."

**Deep Dive → Bigger Picture:**

> "Here's the bigger picture of what's happening:" / "So why does all of this matter?"

**Bigger Picture → Quick Reference:**

> (Just use a horizontal rule. No transition needed.)

**Quick Reference → Closing:**

> (Just use a horizontal rule. The closing paragraph stands alone.)

</section_transitions>
