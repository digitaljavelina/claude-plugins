<required_reading>
Read ALL of these before starting:

- references/formatter-guide.md: Formatting and transformation rules
- references/voice-guide.md: Voice patterns
- references/structure-template.md: Section template and transitions
</required_reading>

<objective>
Transform a YouTube video into a complete, publishable tutorial that reads like original content, not a transcript. Preserve ALL detail from the video while rewriting it at an intermediate reading level: assume competence, skip fundamentals, name the gotchas.
</objective>

<process>

## Phase 1: Fetch Transcript

1. **Get the YouTube transcript.** Use the fetch-transcript script via `uv run`:

   ```bash
   uv run "${CLAUDE_PLUGIN_ROOT}/skills/yt-tutorial/scripts/fetch-transcript.py" <youtube-url-or-video-id>
   ```

   Pass the full YouTube URL or just the video ID. The script auto-installs dependencies via uv's inline metadata, no global install needed. It outputs the full transcript text to stdout. Capture the entire output.

2. **Get video metadata** for context. Use `yt-dlp`:

   ```bash
   yt-dlp --print title --print channel --print description --skip-download "<youtube-url>"
   ```

   This returns the title, channel name, and description, useful for informing the tutorial title and introduction.

## Phase 2: Analyze Transcript

4. **Read the entire transcript** before doing anything else. Understand:
   - What is the main topic?
   - What are the major sub-topics or sections?
   - What is the natural progression (foundational → advanced)?
   - Where does the speaker assume tool-specific knowledge that needs explaining?
   - What examples/demos are included?
   - Are there tangents that should be reorganized?

5. **Identify the thematic structure.** Map the transcript content into logical sections:
   - Group related content together (even if discussed at different times in the video)
   - Order from foundational concepts to advanced techniques
   - Note which sections need researched examples

6. **Draft a section outline.** Map onto the tutorial structure:
   - Title (bold, outcome-oriented, specific)
   - Deck (angle + assumed baseline)
   - Prerequisites & Assumptions (brief, only if non-trivial)
   - Core Concept (mental model, then why and the tradeoff)
   - Main Content Sections (the bulk, organized thematically)
   - Quick Reference table
   - Closing (optional peer note)

7. **Present the outline to the user for approval.** Show:
   - The proposed title
   - The section list with one-line descriptions
   - What you plan to research (if anything)
   - Estimated length (lean tutorial by default; long-form only if requested)

   **Wait for approval before writing.**

## Phase 3: Research (if needed)

8. **Research examples and use cases** ONLY when:
   - The user didn't provide their own examples
   - The video explains concepts without practical applications
   - The video's examples are outdated or too specific to the speaker's setup
   - A real-world use case would make an abstract concept concrete

9. **How to research:**
   - Use web search for current examples, official documentation, and common use cases
   - Use code search (grep.app) for real-world code patterns
   - Look for the minimal working example, the smallest code/config that demonstrates the concept
   - Find common gotchas, what trips people up when first trying this for real

10. **Integrate research naturally**, don't create a separate "Additional Examples" section. Place researched examples exactly where they're relevant in the tutorial flow.

## Phase 4: Write

11. **Write the tutorial section by section**, transforming transcript content as you go:

    **For every section, apply these transformations:**
    - Strip all timestamps
    - Convert speaker's conversational style to tutorial voice (second person, direct)
    - Convert tool-specific assumed knowledge to explicit explanation (standard tooling stays assumed)
    - Convert bare commands to code blocks with language tags plus a breakdown of the non-obvious parts
    - Convert chronological ordering to thematic ordering
    - Convert filler/tangents to clean prose reorganized into the right section

    **Voice checks (every paragraph):**
    - [ ] Second person? ("you" not "one")
    - [ ] Assumes baseline competence (no re-teaching terminals, flags, git)?
    - [ ] Every tool-specific term explained on first use?
    - [ ] Motivation and tradeoff before instruction?

    **Code block checks (every code example):**
    - [ ] Language specified for syntax highlighting?
    - [ ] A sentence of context plus a breakdown of the non-obvious parts (not just a one-line label)?
    - [ ] Tool-specific syntax and novel flags decoded, standard shell skipped?

    **Content preservation checks:**
    - [ ] All examples from the video preserved in full?
    - [ ] All step-by-step instructions preserved?
    - [ ] All technical details, commands, URLs preserved exactly?
    - [ ] All warnings, tips, and caveats preserved?
    - [ ] No summarizing or condensing?

12. **Write the Quick Reference table.** Include every command, tool, concept, and configuration mentioned in the tutorial.

13. **Write the closing (optional).** A peer note, not reassurance:
    - The honest limitation, or
    - The real next step to reach for, or
    - The tradeoff to keep in mind
    - Do not normalize difficulty, do not reassure

## Phase 5: Review and Save

14. **Quality checklist.** Read the completed tutorial and verify:
    - [ ] Title is bold, outcome-oriented, specific
    - [ ] Deck states the angle and the assumed baseline
    - [ ] ALL timestamps removed
    - [ ] Content reorganized thematically (not video chronological order)
    - [ ] Every code block has a breakdown of its non-obvious parts
    - [ ] No unexplained tool-specific jargon; no re-teaching of fundamentals
    - [ ] Right-altitude progression (foundational → advanced)
    - [ ] Horizontal rules between major sections
    - [ ] Quick Reference table is complete
    - [ ] Gotchas named instead of reassurance filler
    - [ ] Content detail matches the original video (nothing lost)
    - [ ] Researched examples integrated naturally (if applicable)
    - [ ] No emojis in prose, no em dashes (periods instead)
    - [ ] Reads like an original tutorial, NOT a transcript

15. **Save the tutorial.** Write a Markdown file:
    - Default location: `Inbox/` in the vault (or the destination folder the user provided)
    - Filename: Descriptive, hyphen-separated (e.g., `Docker-Container-Management-Guide.md`)
    - No frontmatter unless user requests it

16. **Report to the user:**
    - File path where the tutorial was saved
    - Word count
    - Summary of what was researched (if applicable)
    - Any content from the video that was ambiguous or potentially outdated

</process>

<success_criteria>
The tutorial is done when:

- A competent developer new to the topic could follow it without getting stuck, and it gets them past the real gotchas
- ALL content from the original video is preserved (just reformatted at intermediate altitude)
- Every code block has a breakdown of its non-obvious parts
- The structure follows the template (title, prerequisites, concept, sections, reference, optional closing)
- The voice is direct and concrete, assumes competence, and names the sharp edges
- Researched examples are integrated naturally (if applicable)
- No timestamps or transcript artifacts remain
- It's saved to disk and ready to publish
</success_criteria>
