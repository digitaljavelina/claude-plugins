---
name: transcript-to-notebooklm
description: >-
  Convert .srt / .vtt subtitle files or any timestamped video transcript into
  clean, timestamp-free .txt, then create a new NotebookLM notebook (asking the
  user what to name it) and upload the cleaned files as sources. Use this
  whenever the user has subtitle or transcript files (e.g. a folder of .srt
  files, exported YouTube captions, Zoom/Otter/Whisper transcripts) and wants
  them cleaned up, reformatted as plain text, and/or loaded into NotebookLM.
  Triggers on phrases like "strip the timestamps", "clean up these captions",
  "turn these .srt files into a notebook", "make a NotebookLM notebook from
  these transcripts", "put these in NotebookLM", or pointing at a folder of
  subtitle/transcript files. Handles a whole folder at once and passes
  already-clean transcripts through unchanged.
---

# Transcript → NotebookLM

Take messy subtitle/transcript files, strip the timecodes and cue clutter into
readable `.txt`, then drop them into a freshly created NotebookLM notebook.

The NotebookLM side uses the `nlm` CLI (the `notebooklm-mcp-cli` package, command
name `nlm`). Confirm it exists with `which nlm` before relying on it.

## Workflow

### 1. Find the input files
Look in the target folder (default: the current working directory unless the user
names another) for transcript-shaped files:
- Subtitles: `*.srt`, `*.vtt`
- Transcripts: `*.txt` that contain timecodes, plus already-clean `*.txt`

List what you found and confirm the set with the user if it's ambiguous (e.g. the
folder also has unrelated `.txt` files). The cleaner passes already-clean prose
through untouched, so including plain transcripts is safe.

### 2. Clean them into .txt
Run the bundled converter over every input at once. It strips cue indices,
timecodes, formatting tags, and bracketed sound cues (`[Music]`), de-duplicates
rolling captions, and reflows the text into readable paragraphs. Already-clean
files just get whitespace tidied.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/transcript-to-notebooklm/scripts/clean_transcript.py" \
  *.srt *.vtt *.txt \
  --outdir converted
```

(`${CLAUDE_PLUGIN_ROOT}` is the plugin's install directory, set by Claude Code.
Quote globs/paths if names contain
spaces; you can also pass an explicit list of files.) Useful flags:
- `--no-reflow` — keep one line per cue instead of paragraphs.
- `--strip-speakers` — drop leading speaker labels like `John:`.

The cleaned files land in `converted/` with the same base names. Spot-check one
output to confirm timestamps are gone and the text reads naturally before
uploading.

### 3. Make sure NotebookLM is authenticated
NotebookLM sessions are short-lived (~20 min) and `nlm login` opens a real
browser, so it has to be run interactively by the user — you cannot complete it
for them. Check first:

```bash
nlm login --check
```

A logged-in profile prints `✓`; an unauthenticated one prints
`✗ Authentication failed: Profile not found: default` (the command still exits 0,
so read the output, don't trust the exit code). (Note: some `nlm` docs mention
`nlm auth status`, but that subcommand does not exist in the installed version —
use `nlm login --check`.)

If authenticated, continue. If not (or it errors with expired cookies), ask the
user to run the login themselves and wait for them to confirm. In Claude Code,
tell them to type:

```
! nlm login
```

Do not try to script or auto-run `nlm login`; just pause until they've done it,
then re-check with `nlm login --check`.

### 4. Ask the user what to name the notebook
Use the AskUserQuestion tool to get the notebook name — this is required, don't
guess a name silently. Offer a sensible default derived from the folder or
content as the first option (e.g. the folder name "voice-agent"), plus a couple
of reasonable alternatives, and let the user type their own. Keep the question
short; the user can always pick "Other" to free-type.

### 5. Create the notebook and capture its ID
```bash
nlm notebook create "<chosen name>"
```

Then resolve the notebook's ID reliably by listing notebooks as JSON and matching
the title you just created (take the most recent if the title isn't unique):

```bash
nlm notebook list --json
```

Parse out the `id` (a UUID) for your title. Hold onto it for the next step. (You
can optionally `nlm alias set <short-name> <id>` to make later commands readable.)

### 6. Upload each cleaned .txt as a source
NotebookLM accepts `.txt` uploads. Add each file with `--wait` (so processing
finishes before moving on) and `--title` (so the source is named cleanly, without
the `.txt` extension). Two things learned from real runs that this loop guards
against:

- **Pace the uploads.** Firing 20+ adds back-to-back can trip a server-side
  rate limit and a contiguous block of adds fails with "Could not add file
  source." A short `sleep` between adds avoids the burst.
- **Make it idempotent.** A failed `--wait` add sometimes still creates the
  source (it just errored while waiting), and on that partial failure the title
  can default to the filename *with* the `.txt` extension. So before adding,
  check the titles already in the notebook and skip ones present, to avoid
  duplicates when re-running or retrying.

```bash
NB=<notebook-id>
nlm source list "$NB" --json 2>/dev/null \
  | python3 -c "import sys,json;[print(s['title']) for s in json.load(sys.stdin)]" > /tmp/have_titles.txt
for f in converted/*.txt; do
  title="$(basename "$f" .txt)"
  grep -Fxq "$title" /tmp/have_titles.txt && continue   # already added
  nlm source add "$NB" --file "$f" --title "$title" --wait || echo "FAILED: $title"
  sleep 2
done
```

If a `--file` upload of a `.txt` ever fails outright, fall back to piping the
content in as text: `nlm source add "$NB" --text "$(cat "$f")" --title "$title"
--wait`. Prefer `--file` first; `--text` is only a fallback (very long
transcripts can exceed shell argument limits).

If auth expires mid-batch, re-run `nlm login`, then just run the loop again — it
skips what's already there and finishes the rest.

### 7. Report back
Confirm what happened: how many files were cleaned, the notebook name and ID, and
how many sources were added. Verify with `nlm source list <notebook-id>` and share
the count. Mention the local `converted/` folder so the user knows where the plain
-text versions live.

## Notes
- The converter is pure-Python stdlib (no install needed) and is safe to re-run;
  it overwrites files of the same name in `--outdir`.
- It auto-detects format per file by looking for subtitle timecodes, so a mixed
  folder of `.srt` + already-clean `.txt` works in one pass.
- For non-subtitle inputs (a video file, a YouTube URL), there's no transcript to
  clean — NotebookLM can ingest a YouTube URL directly via
  `nlm source add <id> --youtube <url>`, or transcribe audio/video first, then run
  this skill on the resulting transcript.
