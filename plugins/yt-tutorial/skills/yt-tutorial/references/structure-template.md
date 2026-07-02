<structure_template>

## Tutorial Structure

Every tutorial follows this skeleton. Sections can be added or removed based on the topic. Right-size the piece to the topic. Do not pad to hit a length. See the length note at the end.

### 1. Title (H1)

Bold, specific, and outcome-oriented. Promise the reader something concrete.

Pattern: **[Subject] [Verb Phrase That Promises an Outcome], [Supplementary Hook]**

Examples:

- "Claude Code Hooks Let You Enforce Rules the Model Can't Ignore"
- "Run a Full Home Server on a $35 Raspberry Pi: the Setup I Actually Use"
- "NixOS Version-Controls Your Whole OS. Here's the Reproducible Setup."

Avoid:

- "A Guide to X" (boring)
- "Everything You Need to Know About X" (vague filler)

### 2. Subtitle / Deck (bold paragraph, right after title)

One or two sentences: what the piece covers and the angle. State the level and any assumed baseline plainly rather than reassuring.

Pattern: **"[What we cover] and [the non-obvious payoff]. Assumes [baseline]."**

Example:

> **`/insights` reads how you actually work and then writes the fixes for the friction it finds. This walks through what it does, how the feedback loop works, and where it surprises you. Assumes you already use Claude Code day to day.**

### 3. Horizontal Rule

```
---
```

### 4. Prerequisites & Assumptions (H2, brief)

A tight note, not a beginner level-set. State what the reader should already know and what needs to be installed or configured. One short paragraph or a few bullets. Skip it entirely if there is nothing non-trivial to flag.

Pattern:

- "Assumes: [baseline knowledge]. You need: [tools/versions installed]."
- Flag only the prerequisites that actually trip people up.

### 5. Horizontal Rule

### 6. Core Concept Section (H2)

Explain WHAT the thing is and its mental model, then WHY it matters. Get to the model fast.

Pattern:

- "How [X] Actually Works"
- Describe the mechanism in precise, plain language
- The tradeoffs: when you reach for it, when you don't, what it replaces
- Highlight the load-bearing point: "That last part is the one that matters. More on it below."

### 7. Horizontal Rule

### 8. How-To Section (H2)

Step-by-step instructions. Numbered steps. Each step focused. Lead with the decision context, not just the mechanics.

Pattern:

- "Setting It Up"
- **Step 1:** [Instruction] + the why or the gotcha
- **Step 2:** [Instruction]
- **Step 3:** [Instruction]
- Close with what to expect and the first thing that usually goes wrong

### 9. Horizontal Rule

### 10. What to Expect / Output Section (H2)

Show what the result looks like. Walk through the parts that are not self-evident.

Pattern:

- "What You Get"
- Describe each meaningful part of the output
- Use **bold labels** followed by a short explanation
- Example: **At a Glance:** a quick summary of what is working and what is causing friction.

### 11. Horizontal Rule

### 12. Deep Dive Sections (H2, multiple)

The meat. Each section covers one sub-topic in real depth.

Pattern for each:

- H2 with a direct, specific title
- Open with why this matters (the decision or the tradeoff)
- Show a concrete, realistic example (code, config, real output)
- Decode the non-obvious parts
- Include the practical gotcha, edge case, or variation
- Optionally use H3 subsections

### 13. Horizontal Rule

### 14. The Bigger Picture Section (H2, optional)

Zoom out. Explain how the pieces fit and why it compounds. Keep it earned, not a summary for its own sake.

### 15. Horizontal Rule

### 16. Advanced / What's Next Section (H2, optional)

Where to go further: deeper config, related tools, the harder version of the problem. Point to the real next step, briefly.

### 17. Horizontal Rule

### 18. Quick Reference Table (H2)

Summarize every command, concept, or tool mentioned.

Format:

```markdown
## Quick Reference: [Topic]

| [Thing]           | What It Does      |
| ----------------- | ----------------- |
| `command`         | Brief description |
| `another-command` | Brief description |
```

### 19. Horizontal Rule

### 20. Closing (optional, brief)

Not a reassurance paragraph. If you close, close like a peer: the honest limitation, the next thing worth trying, or the tradeoff to keep in mind. Skip it entirely if the Quick Reference is a cleaner ending.

Pattern:

> "The main limitation is [X]. If you push past the basics, the next thing to reach for is [Y]. [One honest note on when this is or isn't worth it.]"

Do not normalize difficulty, do not say "one piece at a time," do not reassure. The reader is competent.

## Length

Default to a focused, right-sized tutorial. Cover the topic and stop. Do not pad to a word count. Right-sized does not mean terse: each section should carry explanatory prose that makes the reasoning and the flow clear, not just steps and code blocks with one-line labels.

Long-form, publication-ready blog treatment (fuller hooks, bigger-picture framing, 2,000+ words) is an explicit mode. Apply it only when the user asks for a long-form blog post. Otherwise keep it lean.

</structure_template>

<section_transitions>

## Transition Patterns Between Sections

Sections should flow. Keep transitions direct.

**Core Concept to How-To:**

> "Here's how to set it up." / "The setup is short."

**How-To to Output:**

> "Once that runs, here's what you get."

**Output to Deep Dive:**

> "The useful part is [X]." / "Here's where it stops being a toy."

**Deep Dive to Deep Dive:**

> Use H3 sub-headers, or connect to the previous: "Beyond [previous topic], there's also..."

**Deep Dive to Bigger Picture:**

> "Step back and here's what's actually happening:" / "So why does this compound?"

**Bigger Picture to Quick Reference:**

> (Just use a horizontal rule.)

**Quick Reference to Closing:**

> (Just use a horizontal rule.)

</section_transitions>
</structure_template>
