---
name: matter-intake
description: >-
  Turn a recorded or written client-intake conversation that lives on disk into
  a structured seven-section "matter summary" file. Use when you point at an
  audio recording or a transcript and want it digested into a legal intake
  summary, say "summarize this intake", "digest this client recording", "make a
  matter summary from this", or "process this consult". Runs entirely locally:
  local whisper for audio, the running Claude for the structuring, no external
  API and no app. Confidential by design. For a non-legal recording use
  meeting-digest; to distill the current chat use a conversation-distill skill.
argument-hint: "<path to an audio file or transcript> [output_dir]"
disable-model-invocation: false
---

# matter-intake

Digest one client-intake conversation into a clean, skimmable matter summary.
The recording or transcript already lives on the machine, so this is a local
pipeline, not an app: one skill, one bundled script, the running Claude does the
structuring.

Nothing here leaves the machine. Audio is transcribed locally with whisper; the
structuring is done by the Claude you are already running. No API bill, no upload
of privileged content.

## Confidentiality (the whole reason this is local)

Intake content is attorney-client material. Two rules:

1. **Do not write the summary into a synced notes vault by default** (Obsidian,
   iCloud, Dropbox, a git repo). Output lands next to the source recording, or
   an `output_dir` the user passes, so privileged content is not auto-synced or
   committed. Only put it somewhere synced if the user explicitly asks.
2. **Nothing goes to an external service.** Transcription is local whisper.
   Structuring is the local Claude session. If a step would require uploading
   the audio or transcript anywhere, stop and ask first.

## Step 1 - get a transcript

Run the bundled script on whatever path the user gave. It detects audio vs text:
audio gets transcribed locally with whisper, text passes straight through.

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/prepare_transcript.sh" "<input path>" "<optional output_dir>"
```

It prints one line, `TRANSCRIPT=<path>`. Read that file. If the script reports
no transcriber available for an audio input, relay its one-line hint and stop;
do not try to transcribe some other way.

Note on speakers: local whisper does not separate speakers (no diarization).
Attribute lines to attorney vs client only where the wording makes it clear.
Where it is ambiguous, label the point neutrally rather than guessing who said
it. Flag at the top of the summary that speaker attribution is inferred.

## Step 2 - structure into the seven-section matter summary

Read the transcript and produce the summary using this exact structure. Keep it
factual and grounded in what was actually said. Do not invent legal conclusions
or advice. If a section has nothing, write "None noted" rather than padding.

```markdown
# Matter summary - <short matter label> - <date if known>

> Draft from an inferred-speaker transcript. Verify against the recording before
> relying on it. Not legal advice.

## 1. Parties and contacts
- Client:
- Other parties / potential adverse parties (for conflict check):
- Other names mentioned:

## 2. Matter type and jurisdiction

## 3. Client's stated goals and desired outcome

## 4. Timeline of events (as the client described them)

## 5. Key facts and disputed points

## 6. Documents and evidence mentioned or promised

## 7. Action items, deadlines, and follow-ups
- [ ] <item> - owner - due
```

Surface party names in section 1 prominently, since the first real use of this
is a conflicts check.

## Step 3 - write the file

Write the summary to the same directory as the input (or the `output_dir` arg),
named `<input-basename>.matter-summary.md`. Confirm the path back to the user.

If they ask for a PDF, convert the markdown with pandoc:

```bash
pandoc "<summary>.md" -o "<summary>.pdf"
```

## Step 4 - report

Report: the output path, the parties found (for the conflict check), and the
count of action items with deadlines. Keep the privileged content in the file,
not pasted back into a long chat transcript.

## Scope

One conversation at a time. Local only. Legal-intake framing. No app, no cloud
backend, no auto-publishing. For a non-legal recording use the meeting-digest
skill instead.
