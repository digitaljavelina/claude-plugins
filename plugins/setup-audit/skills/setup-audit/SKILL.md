---
name: setup-audit
description: "Audit a Claude Code installation on two tracks: (A) instruction files (CLAUDE.md, skills, settings, context, hooks) for bloat, conflicts, and redundancy, and (B) the installed skill/plugin inventory for duplicate and overlapping capabilities. Produces a scored evaluation table, cut list, conflict report, cleaned CLAUDE.md, plus an overlap-cluster report and removal-candidate list for skills/plugins — then offers to remove the flagged items after confirmation. Use this skill whenever the user asks to audit their setup, clean up their Claude config, streamline their installation, find duplicate or overlapping skills/plugins, remove redundant skills, review their instructions, check for conflicts or redundancy, slim down their CLAUDE.md, or anything related to evaluating the quality and signal-to-noise ratio of their Claude Code configuration and installed capabilities."
---

# AI Setup Audit — Installation Review & Streamlining

You are auditing a Claude Code installation. The goal is a leaner, higher-signal setup where every instruction rule AND every installed skill/plugin earns its place. Bloated instructions waste context and create contradictions; duplicate or overlapping skills/plugins clutter discovery, fragment behavior across near-identical tools, and make the installation harder to reason about.

This audit runs on two tracks:

- **Track A — Instruction files**: the _content_ of rules inside CLAUDE.md, skills, settings, and hooks.
- **Track B — Skill & plugin inventory**: the _installed capabilities_ themselves — finding duplicates and overlaps, recommending what to keep vs remove.

Run both tracks unless the user explicitly scopes you to one. Present Track A deliverables first, then Track B, then the removal offer.

---

# Track A — Instruction File Audit

## A1 — Collect All Instruction Files

Read every file that shapes Claude's behavior in this environment. Be thorough — missed files mean missed conflicts.

1. **CLAUDE.md files** — check all of these locations:
   - `~/.claude/CLAUDE.md` (user-level)
   - Project root `CLAUDE.md`
   - Project `.claude/CLAUDE.md`
   - Parent directory CLAUDE.md files (walk up from project root)
2. **Skills folder** — every `SKILL.md` / `.md` file in `~/.claude/skills/` and all subfolders (follow symlinks; many skills symlink to `~/.agents/skills/`)
3. **Context folder** — every file in `.claude/context/` if it exists
4. **Settings files** — `settings.json` and `settings.local.json` in both `~/.claude/` and project `.claude/`
5. **Other instruction files** — `.claudeignore`, hook configs in settings, MCP server configs, or anything else that modifies behavior

**Before proceeding**, list every file you found with its full path. If a folder is empty or missing, say so explicitly. This inventory is the foundation for everything that follows — if you skip a file, you'll miss conflicts.

## A2 — Evaluate Every Rule

Extract each distinct rule, instruction, or preference from ALL files. Evaluate each one against these 5 criteria:

| #   | Criterion            | Flagged (✅) when...                                                                           |
| --- | -------------------- | ---------------------------------------------------------------------------------------------- |
| 1   | **Default behavior** | Claude would do this without being told — it's built into base behavior or the system prompt   |
| 2   | **Conflicts**        | Another rule in a _different_ file says the opposite or sets a contradictory expectation       |
| 3   | **Redundant**        | Another rule in a _different_ file already covers this — same intent, different words          |
| 4   | **Patch job**        | Reads like a one-time fix for a specific bad output rather than a durable behavioral rule      |
| 5   | **Too vague**        | No concrete action or measurable standard — you'd interpret it differently on every invocation |

Present results as a structured table:

```
| File | Rule (quoted) | 1 | 2 | 3 | 4 | 5 | Verdict |
```

Mark each cell `✅` (flagged) or `—` (no issue). Verdict = **KEEP**, **CUT**, or **REWRITE**.

### Important judgment calls

- A rule that corrects a real drift behavior (something Claude does wrong without the instruction) is NOT "default behavior" — keep it even if it seems obvious. Only flag criterion 1 if your base behavior genuinely covers it without the instruction.
- "Redundant" means the _same intent_ appears in a _different file_. Two rules in the same file that reinforce each other are not redundant — they're emphasis.
- "Patch job" means hyper-specific ("always check X before Y" where X was a one-off edge case). General patterns that prevent recurring issues are not patch jobs.

## A3 — Track A Deliverables

Produce these three outputs in order, cleanly separated.

### A. Cut List

Every rule you'd remove. One per line, sorted by file then by criterion number:

```
- [File]: "[exact quoted rule]" — [one-line reason: which criterion it fails]
```

### B. Conflict Report

Every pair of contradictory rules, with a resolution recommendation:

```
- CONFLICT: [File A] says "[rule]" vs [File B] says "[rule]" — [which should win and why]
```

If no conflicts found, state "No conflicts detected." Do not skip this section.

### C. Cleaned CLAUDE.md

Rewrite the main CLAUDE.md with:

- All **CUT** rules removed
- All **REWRITE** rules improved (concrete, measurable, non-redundant)
- All **KEEP** rules preserved exactly as-is (do not rewrite rules that scored KEEP)
- **No new rules added** — only subtract and sharpen
- Preserve the existing section structure where possible

Present the cleaned version as a complete file the user can copy-paste to replace their current one.

---

# Track B — Skill & Plugin Inventory Dedup

This track inventories every installed capability and finds duplicates and overlaps so the installation can be streamlined.

## B1 — Inventory Every Installed Capability

Build a complete list of what is installed. Read metadata only (frontmatter `name` + `description`, plugin manifests) — do NOT read full skill bodies unless you need to break a tie between two near-identical candidates.

1. **Standalone skills** — every entry in `~/.claude/skills/`. Note which are real directories vs symlinks (e.g. `-> ~/.agents/skills/...`); record the symlink target so removal advice points at the right place.
2. **Plugins** — read `~/.claude/plugins/installed_plugins.json` for the authoritative installed list, and `~/.claude/plugins/known_marketplaces.json` for sources. Each plugin lives under `~/.claude/plugins/marketplaces/<name>/`.
3. **Plugin-provided capabilities** — for each installed plugin, list the skills, slash commands, and agents it contributes (check the plugin's `skills/`, `commands/`, `agents/` folders and its manifest). These are what actually create user-facing overlap.
4. **Agents** — entries in `~/.claude/agents/`.
5. **Commands** — entries in `~/.claude/commands/`.

Present the inventory as a compact table grouped by source:

```
| Capability | Type (skill/plugin/command/agent) | Source (standalone / plugin:<name>) | One-line purpose |
```

State totals (e.g. "47 skills, 10 plugins contributing 18 commands and 6 agents"). If a location is empty or missing, say so.

## B2 — Cluster Overlapping Capabilities

Group capabilities that do substantially the same job. Judge overlap by _purpose and trigger conditions_, not name similarity. Two skills overlap when a user request would plausibly match either one.

For each cluster, classify the relationship:

| Relationship      | Meaning                                                                                                                                 |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **DUPLICATE**     | Same capability installed twice (e.g. two copies of a research skill from different marketplaces) — near-identical purpose and triggers |
| **OVERLAP**       | Different implementations of the same job (e.g. multiple code-review skills) — user would have to choose between them for the same task |
| **SUBSUMED**      | One capability's function is fully contained within a broader one                                                                       |
| **COMPLEMENTARY** | Looks similar but serves a genuinely distinct purpose — NOT a removal candidate, list it only to explain why it stays                   |

Present clusters like:

```
### Cluster: <theme, e.g. "Code review">
- Relationship: OVERLAP
- Members:
  - <capability> (source) — <what's distinct about it>
  - <capability> (source) — <what's distinct about it>
- Recommendation: keep <X> because <reason>; remove/disable <Y>, <Z> because <reason>
```

### Judgment calls for Track B

- **Never recommend removing the only tool for a job.** A capability with no overlap is not a removal candidate no matter how niche.
- Prefer keeping the version that is: more capable, more actively maintained, from a source the user controls, or already wired into the user's hooks/commands.
- A capability invoked by another skill, hook, or command is load-bearing — flag that dependency instead of recommending removal.
- When two genuinely overlap but you can't tell which is better, mark it **UNDECIDED** and ask the user rather than guessing.
- Removing a _plugin_ removes everything it contributes. If only one of a plugin's skills overlaps, recommend disabling that skill (or living with it), not uninstalling the whole plugin — unless the entire plugin is redundant.

## B3 — Track B Deliverable: Removal Candidate List

A single prioritized list. One line each, highest-confidence removals first:

```
- [KEEP-INSTEAD: <X>] remove <Y> (<source>) — <relationship>; <one-line reason> — <removal method>
```

`<removal method>` must be concrete and match how the thing is installed:

- Standalone real directory: delete the folder under `~/.claude/skills/`
- Standalone symlink: remove the symlink (and note the shared target stays for other machines)
- Plugin skill: disable via settings or remove the skill file within the plugin
- Whole plugin: the uninstall command / removing it from `installed_plugins.json` + marketplace folder

End with a one-line summary: how many removal candidates, and how many capabilities the installation would drop from → to.

---

# Final Step — Offer to Remove (confirm first)

After presenting all deliverables, offer to act. **Do not delete or disable anything without explicit confirmation in this session.**

1. Summarize the proposed removals as a short numbered checklist (Track A cleaned-CLAUDE.md write + Track B removals), so the user can approve all, some, or none.
2. Ask the user which items to proceed with. Use the AskUserQuestion tool when the choices are discrete.
3. **Before deleting anything, back it up.** Copy targeted skill folders / plugin entries / the current CLAUDE.md into `~/.claude/backups/setup-audit-<timestamp>/` (get the timestamp from the shell, e.g. `date +%Y%m%d-%H%M%S` — do not invent one). State the backup path.
4. Only then remove the confirmed items. For symlinks, remove the link, not the target. After acting, report exactly what was removed and what was kept.
5. If the user declines, leave everything untouched and stop — the report alone is a valid outcome.

# Constraints

- **Quote rules exactly** when referencing them in the Track A table and cut list — do not paraphrase.
- **NEVER delete a rule or capability just because it seems obvious or niche to you** — only flag a rule under criterion 1 if base behavior genuinely covers it without the instruction, and only flag a capability for removal if it genuinely overlaps another. When in doubt, KEEP.
- Track B judges overlap from frontmatter/manifest metadata; only read full skill bodies to break a specific tie.
- If two rules conflict, recommend keeping whichever is more specific and actionable.
- Deliver each section cleanly; do not add commentary between the Track A deliverable sections.
- Do not add new rules, new skills, or unrequested "improvements" — this audit only subtracts and sharpens.
- Never remove, disable, or overwrite anything without explicit per-session confirmation and a backup.
