<required_reading>
Read ALL of these before starting:

- references/formatter-guide.md — Formatting and transformation rules
- references/voice-guide.md — Voice patterns (8 named patterns)
- references/structure-template.md — Section template and transitions
  </required_reading>

<objective>
Transform a YouTube video into a complete, publication-ready tutorial that reads like original content — not a transcript. Preserve ALL detail from the video while applying the tutorial voice and formatting standards.
</objective>

<process>

## Phase 1: Fetch Transcript

1. **Get the YouTube transcript.** Use the fetch-transcript script via `uv run`:

   ```bash
   uv run "${CLAUDE_PLUGIN_ROOT}/skills/yt-tutorial/scripts/fetch-transcript.py" <youtube-url-or-video-id>
   ```

   Pass the full YouTube URL or just the video ID. The script auto-installs dependencies via uv's inline metadata — no global install needed. It outputs the full transcript text to stdout. Capture the entire output.

2. **Get video metadata** for context. Use `yt-dlp`:

   ```bash
   yt-dlp --print title --print channel --print description --skip-download "<youtube-url>"
   ```

   This returns the title, channel name, and description — useful for informing the tutorial title and introduction.

## Phase 2: Analyze Transcript

4. **Read the entire transcript** before doing anything else. Understand:
   - What is the main topic?
   - What are the major sub-topics or sections?
   - What is the natural progression (beginner → advanced)?
   - Where does the speaker assume knowledge that needs explaining?
   - What examples/demos are included?
   - Are there tangents that should be reorganized?

5. **Identify the thematic structure.** Map the transcript content into logical sections:
   - Group related content together (even if discussed at different times in the video)
   - Order from foundational concepts to advanced techniques
   - Note which sections need researched examples

6. **Draft a section outline.** Map onto the tutorial structure:
   - Title (bold, outcome-oriented, with hook)
   - Subtitle/deck
   - First Things First (the one prerequisite)
   - Core Concept (what and why)
   - Main Content Sections (the bulk — 3-6 H2 sections)
   - Quick Reference table
   - Closing paragraph

7. **Present the outline to the user for approval.** Show:
   - The proposed title
   - The section list with one-line descriptions
   - What you plan to research (if anything)
   - Estimated length (short / standard / deep dive)

   **Wait for approval before writing.**

## Phase 3: Research (if needed)

8. **Research examples and use cases** ONLY when:
   - The user didn't provide their own examples
   - The video explains concepts without practical applications
   - The video's examples are outdated or too specific to the speaker's setup
   - A real-world use case would make an abstract concept click

9. **How to research:**
   - Use web search for current examples, official documentation, and common use cases
   - Use code search (grep.app) for real-world code patterns
   - Look for the minimal working example — smallest possible code/config that demonstrates the concept
   - Find common gotchas — what trips people up when first trying this

10. **Integrate research naturally** — don't create a separate "Additional Examples" section. Place researched examples exactly where they're relevant in the tutorial flow.

## Phase 4: Write

11. **Write the tutorial section by section**, transforming transcript content as you go:

    **For every section, apply these transformations:**
    - Strip all timestamps
    - Convert speaker's conversational style → tutorial voice (second person, direct)
    - Convert assumed knowledge → explicit explanations with analogies
    - Convert bare commands → code blocks with language tags + line-by-line breakdowns
    - Convert chronological ordering → thematic ordering
    - Convert filler/tangents → clean prose reorganized into the right section

    **Voice checks (every paragraph):**
    - [ ] Second person? ("you" not "one")
    - [ ] Paragraphs 4 sentences or fewer?
    - [ ] Every technical term explained on first use?
    - [ ] Motivation before instruction?

    **Code block checks (every code example):**
    - [ ] Language specified for syntax highlighting?
    - [ ] Line-by-line breakdown immediately after?
    - [ ] Flags and symbols explained? (`-p`, `>`, `|`, `~`, etc.)

    **Content preservation checks:**
    - [ ] All examples from the video preserved in full?
    - [ ] All step-by-step instructions preserved?
    - [ ] All technical details, commands, URLs preserved exactly?
    - [ ] All warnings, tips, and caveats preserved?
    - [ ] No summarizing or condensing?

12. **Write the Quick Reference table.** Include every command, tool, concept, and configuration mentioned in the tutorial.

13. **Write the closing paragraph.** Italicized. Follow the pattern:
    - Acknowledge difficulty is normal
    - Point to ONE simple starting action
    - Encourage incremental learning
    - End warmly

## Phase 5: Review and Save

14. **Quality checklist.** Read the completed tutorial and verify:
    - [ ] Title is bold, outcome-oriented, with a hook
    - [ ] Subtitle sets expectations for content and audience
    - [ ] ALL timestamps removed
    - [ ] Content reorganized thematically (not video chronological order)
    - [ ] Every code block has a plain-English breakdown
    - [ ] No unexplained jargon
    - [ ] Progressive complexity (foundational → advanced)
    - [ ] Horizontal rules between major sections
    - [ ] Quick Reference table is complete
    - [ ] Closing paragraph is italicized and reassuring
    - [ ] Content detail matches the original video (nothing lost)
    - [ ] Researched examples integrated naturally (if applicable)
    - [ ] No emojis in prose
    - [ ] Reads like an original tutorial, NOT a transcript

15. **Save the tutorial.** Write a Markdown file:
    - Default location: the current working directory (or the destination folder the user provided)
    - Filename: Descriptive, hyphen-separated (e.g., `Docker-Container-Management-Complete-Guide.md`)
    - No frontmatter unless user requests it

16. **Report to the user:**
    - File path where the tutorial was saved
    - Word count
    - Summary of what was researched (if applicable)
    - Any content from the video that was ambiguous or potentially outdated

</process>

<success_criteria>
The tutorial is done when:

- A complete beginner could follow it without getting stuck
- ALL content from the original video is preserved (just reformatted)
- Every code block has an accompanying plain-English breakdown
- The structure follows the template (title → context → concept → sections → reference → closing)
- The voice is conversational, direct, and reassuring throughout
- Researched examples are integrated naturally (if applicable)
- No timestamps or transcript artifacts remain
- It's saved to disk and ready to publish
  </success_criteria>
