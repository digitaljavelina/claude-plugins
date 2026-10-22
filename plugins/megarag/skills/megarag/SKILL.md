---
name: megarag
description: Build MegaRAG, a production multimodal RAG app (documents, images, video, audio, knowledge graph, 5 query modes, streaming chat with citations) on Next.js 16, Supabase pgvector, Gemini, Docling, and the Vercel Workflow SDK. A phase-by-phase build driven by Claude Code, updated in October 2026 from the December 2025 "MegaRAG Build Prompts" guide, with every dead API replaced. Use when the user says "megarag", "build a RAG app", "multimodal RAG", "RAG over my documents and videos", "knowledge graph RAG", "LightRAG-style app", or asks to resume a MegaRAG build.
---

# MegaRAG Builder

Build a full multimodal RAG system phase by phase, in the user's project directory, with a test gate at the end of every phase. The phases are in `references/phases.md`. What changed since the source guide, with dates, is in `references/whats-changed.md`. The database migration, tested against pgvector, is `references/schema.sql`.

## Rules

- **Never use n8n**, or any other no-code automation tool, for any part of this build. Background processing is TypeScript code in the app, using the Workflow SDK. Claude Code is the builder. If a reference repo or doc suggests n8n, skip that suggestion.
- **Python goes through `uv`.** `uvx` or `uv run`, never pip. That covers Docling locally and any eval scripts written in Python.
- **One file holds every model ID** (`src/lib/ai/models.ts`). Never hardcode a model ID anywhere else.
- **Verify before you build on it.** Model IDs and package versions in these references were current on 2026-10-22. Phase 0.3 re-checks them. If a model is gone, use its documented successor and update `docs/decisions.md`.
- **The secret Supabase key never reaches the browser.** Any module that uses it imports `server-only`.
- **Dark theme by default** in the UI.
- **A gate is a real check.** Run the build, the typecheck, and the gate's described test, then show the output. A phase without a passing gate is not done.

## Start or Resume

1. Look for `docs/progress.md` in the current project. If it exists, read it, read `CLAUDE.md` and `docs/decisions.md`, and resume at the first unchecked phase. Say which phase you are resuming.
2. If it does not exist, this is a new build. Confirm the target directory with the user (an empty folder, or a new folder under the current one), then run the interview.

## The Interview (Phase 0, before any code)

Ask all of these in one AskUserQuestion call. Put the recommended default first.

1. **Answer model.** Gemini `gemini-3.8-flash` (one vendor, one key, the default). Or Claude Sonnet 5.5 for the chat answers via `@ai-sdk/anthropic`, with Gemini still doing embeddings, video, and audio.
2. **Docling host.** Homelab Docker host reached over Tailscale Funnel or a Cloudflare Tunnel (the default for a user who has one). Or a paid small instance on Railway, Render, or Fly. The CPU image is 4.4 GB, so free tiers will not hold it.
3. **Reranker.** An LLM rerank with `gemini-3.5-flash-lite` and a scoring schema (the default, no new vendor). Or a hosted rerank API (Cohere, Voyage, or Jina), which needs one more key.
4. **Build or managed.** Build the pipeline (the default, and the point of MegaRAG). Or start from Gemini File Search as a managed baseline, then build alongside it and compare in Phase 11.

Fixed defaults, which you state but do not ask about: Supabase Auth with email magic link; embeddings at 1536 dims; Vercel for the app; one workspace created per user at signup.

Write the answers to `docs/decisions.md`, one line each with the reason. Then create `docs/progress.md`:

```markdown
# MegaRAG Progress
- [ ] Phase 0: Learn, decide, record
- [ ] Phase 1: Supabase
- [ ] Phase 2: Next.js project
- [ ] Phase 3: Upload and basic UI
- [ ] Phase 4: Text pipeline
- [ ] Phase 5: Documents (PDF, Office)
- [ ] Phase 6: Video and audio
- [ ] Phase 7: Knowledge graph
- [ ] Phase 8: Retrieval and answers
- [ ] Phase 9: Chat interface
- [ ] Phase 10: Polish and deploy
- [ ] Phase 11: Evaluate
- [ ] Phase 12: Enhancements
```

## Running a Phase

For each phase in `references/phases.md`:

1. **Explore.** Read the parts of the codebase this phase touches. For phases that touch several files, use plan mode and show the plan.
2. **Build.** Carry out the phase's prompts in order, filling `{placeholders}` from `docs/decisions.md`. Use parallel subagents only for independent pieces, like the five repo studies in 0.1.
3. **Gate.** Run `npm run build`, `npx tsc --noEmit`, and the phase's Gate test. Show the output. Fix failures and re-run, never skip.
4. **Record.** Tick the phase in `docs/progress.md` with the date and one line on anything surprising. Add any new architectural decision to `CLAUDE.md`.
5. **Commit.** One commit per phase, `feat(phase-N): <summary>`, on the project's current branch.
6. **Pause.** Tell the user the phase passed, what they can try now, and what the next phase does. Wait for a go-ahead before starting the next phase, unless the user said to run straight through.

Phases 1 to 4 are the spine. Phases 5 and 6 can run in either order. Phase 7 needs Phase 4. Phase 8 needs Phases 4 and 7.

## Keys the User Will Need

Ask for these when the phase that needs them begins, not up front. Never print a key back.

- Supabase project URL, publishable key, secret key (Phase 1 for local, Phase 10 for prod)
- `GEMINI_API_KEY` (Phase 4)
- `ANTHROPIC_API_KEY` if Claude answers (Phase 8)
- `DOCLING_SERVE_API_KEY`, a long random string the user generates (Phase 5)
- A rerank API key if a hosted reranker was chosen (Phase 8)

Local secrets go in `.env.local`, which must be in `.gitignore` before the first commit.

## When Things Go Wrong

- **An embedding-dimension mismatch** ("expected 1536 dimensions") means a call skipped `outputDimensionality`. Fix it in `embeddings.ts`, not by changing the column.
- **A video stuck in processing** usually means the Gemini file never reached ACTIVE. Check the poll loop, then the workflow run in `npx workflow web`.
- **Docling timeouts on large PDFs** mean switching to the `/async` endpoint and polling, or raising `DOCLING_SERVE_MAX_NUM_PAGES`.
- **A 413 on upload** means file bytes are going through a Next.js route. They must go browser to Storage directly (Phase 3.1).
- **Empty results with a workspace filter** on a big table: confirm the search functions kept `set hnsw.iterative_scan = relaxed_order`.
