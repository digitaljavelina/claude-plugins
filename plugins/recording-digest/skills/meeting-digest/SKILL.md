---
name: meeting-digest
description: >-
  Turn a meeting or voice recording (or a transcript) that lives on disk into a
  structured digest note: TL;DR, decisions, action items with owners, and open
  questions. Use when you point at a recording or transcript file and say "digest
  this meeting", "summarize this recording", "turn this call into notes", or
  "what were the action items from this". Runs entirely locally: local whisper
  for audio, the running Claude for the structuring, no external API. This is the
  domain-neutral sibling of matter-intake (which is for legal client intake). For
  distilling the CURRENT chat conversation rather than a file on disk, use a
  conversation-distill skill instead.
argument-hint: "<path to an audio file or transcript> [output_dir]"
disable-model-invocation: false
---

# meeting-digest

Digest one recording or transcript that already lives on the machine into a
clean, skimmable note. One skill, one bundled script, the running Claude does the
structuring. Local only, no app, no cloud, no API bill.

This is the general-purpose sibling of `matter-intake`. Same local pipeline,
different output shape:
- `matter-intake` -> legal client-intake matter summary (seven sections)
- `meeting-digest` -> a domain-neutral meeting digest (this skill)

If the task is to distill the conversation already open in the current chat, that
is a conversation-distill skill, not this. This skill is for a file on disk.

## Where output goes

Default: write the digest next to the source recording, named
`<recording-name>.digest.md`. This is the safe default because some recordings
(for example work meetings) may be confidential and should not auto-sync to a
notes vault.

If the user wants it in a notes vault (Obsidian or similar), they can pass an
`output_dir` under that vault or say so. Do not put plausibly-confidential
content (anything work or employer related) into a synced vault without the user
asking.

## Step 1 - get a transcript

Run the bundled script on whatever path was given. It detects audio vs text:
audio is transcribed locally with whisper, text passes straight through.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/prepare_transcript.sh" "<input path>" "<optional output_dir>"
```

It prints one line, `TRANSCRIPT=<path>`. Read that file. If it reports no
transcriber, relay the one-line hint and stop.

Speaker note: local whisper does not separate speakers. Attribute points to a
person only where the wording makes it obvious. Otherwise keep them neutral.

## Step 2 - structure into the digest

Read the transcript and write the digest using this structure. Stay grounded in
what was actually said. If a section is empty, write "None" rather than padding.

```markdown
# Meeting digest - <short topic> - <date if known>

> Generated from an inferred-speaker transcript. Verify before relying on it.

## TL;DR
- <three bullets max, the "if you read nothing else" version>

## Decisions
- <what was actually decided, not what was discussed>

## Action items
- [ ] <item> - owner - due

## Open questions / parking lot
- <unresolved threads, things deferred>

## Notes by topic
- <short outline of what was covered, grouped by theme>
```

Put owners and due dates on action items wherever they were stated. Where an
owner is unclear, write "owner: unassigned" so it is visibly a gap.

## Step 3 - write and report

Write the file (default next to the input, or the `output_dir` arg). Report the
path, the count of decisions, and the count of action items (and how many have an
owner). Keep the content in the file, not pasted into a long chat.

If the user asks for a PDF, convert with pandoc:

```bash
pandoc "<digest>.md" -o "<digest>.pdf"
```

## Scope

One recording at a time. Local only. Domain-neutral. No app, no cloud backend.
For legal client intake use `matter-intake`.
