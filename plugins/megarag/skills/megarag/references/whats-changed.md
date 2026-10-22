# What Changed Since the December 2025 Guide

The source is "MegaRAG Build Prompts" (41 prompts, 11 phases, December 2025). Everything below was checked on 2026-10-22. Model IDs and package versions move fast, so Phase 0 re-checks them before any code gets written.

## Hard breaks: the original guide will not run as written

| Original | Status Oct 2026 | Replacement |
|---|---|---|
| `text-embedding-004`, 768 dims | **Shut down 2026-01-14** | `gemini-embedding-2`. Multimodal (text, image, video, audio, PDF), 8,192 input tokens, 128 to 3,072 dims (Matryoshka, auto-normalized when truncated). No `task_type` param: put the task in the text, e.g. `task: search result \| query: {q}`. |
| Gemini 2.0 Flash | **Shut down** | `gemini-3.8-flash` (stable workhorse). `gemini-3.5-flash-lite` for bulk cheap work. `gemini-4-argon` only if quality demands it. |
| `@google/generative-ai` | **Deprecated** | `@google/genai` (`new GoogleGenAI({})`, `ai.models.generateContent`, `ai.models.embedContent`, `ai.files.upload`). |
| Upload via FormData to `/api/upload` | **Breaks on Vercel** above 4.5 MB (request body limit) | Browser uploads straight to Supabase Storage with a signed upload URL or TUS resumable upload. The API route only creates the row and starts processing. |
| "Trigger async processing (don't block the response)" | Fire-and-forget promises get killed when a serverless function returns | Workflow SDK (`workflow`, durable steps with retries) or `after()` from `next/server` for short jobs. |

## Deprecated or superseded

| Original | Now | Why it matters |
|---|---|---|
| Next.js 14 | Next.js 16.4 (16.4.1+ for the Oct 2026 security fix). 15 left security support 2026-10-21. | Turbopack is the default bundler. `proxy.ts` replaces `middleware.ts`. Route `params` are async. |
| Supabase `anon` / `service_role` keys | Publishable (`sb_publishable_...`) and secret (`sb_secret_...`) keys | Legacy keys are deprecated by end of 2026. |
| Custom FastAPI Docling wrapper | Official `docling-serve` container (`quay.io/docling-project/docling-serve-cpu`) | Already has `/v1/convert/file`, async jobs, `X-Api-Key` auth, and a built-in HybridChunker (`to_formats: ["chunks"]`). Nothing to write. |
| Railway or Render free tier for Docling | The CPU image is 4.4 GB and needs a few GB of RAM | Free tiers will not hold it. Use a paid small instance or a homelab Docker host. |
| Tailwind 3 config file | Tailwind 4.3, CSS-first config | No `tailwind.config.js`. shadcn CLI handles it. |
| Ask a chat model to transcribe audio | `gemini-3.5-transcribe` | Built for it: speaker diarization, word timestamps, custom vocabulary. |
| "Prompt Gemini to return structured JSON" | Structured output with a JSON schema (`responseJsonSchema`, built from zod 4) | The model is constrained to the schema, so parse failures go away. |
| Raw `fetch` to Gemini for chat answers | AI SDK 7 (`ai`, `@ai-sdk/react` `useChat`, `@ai-sdk/google` or `@ai-sdk/anthropic`) | Streaming tokens to the UI, tool calls, and message persistence come for free. |

## New ideas worth adding

- **Hybrid keyword + vector search, fused with Reciprocal Rank Fusion.** Embeddings blur exact strings: drug names, trial IDs, acronyms, error codes. A Postgres full-text column plus RRF fixes that in one SQL function. Built into `schema.sql`.
- **Reranking.** Retrieve broadly (30 to 50 candidates), rerank, send the best 8 to 12. LightRAG made rerank the default for its `mix` mode in 2025. Options: an LLM rerank with Flash-Lite and a scoring schema, or a hosted reranker API.
- **Contextual retrieval.** Before embedding a chunk, generate one or two sentences that place it in its document ("This section of the 2024 annual report covers Q3 revenue") and embed that with the chunk. Large gains on documents whose chunks lose meaning out of context.
- **Native multimodal embeddings.** `gemini-embedding-2` embeds an image or a video clip directly. Store both the media embedding and the text description, so "the slide with the red bar chart" can match on either.
- **Agentic video understanding.** Gemini 3.6 Flash and later can navigate long videos on demand instead of reading every frame. Up to 88% fewer tokens on long-form content.
- **Structure-aware chunking for documents.** Docling's HybridChunker splits on headings and tables, then caps by token count. Better than a flat 800-token window for PDFs and Office files. Keep the 800/100 window for plain text and transcripts.
- **An evaluation phase.** A golden set of 20 to 50 questions with known answers and source chunks, scored on retrieval hit rate and answer faithfulness. Without it, every tuning change is a guess.
- **Row Level Security and real workspaces.** The guide passed a `workspace` param but never enforced it.
- **Prompt-injection hygiene.** Retrieved text is data, never instructions. Wrap it in delimiters and say so in the system prompt.

## Managed shortcuts that did not exist, or were thin, in December 2025

Not the default here, because the point of MegaRAG is to build and understand the pipeline. Worth knowing about.

- **Gemini API File Search.** Managed RAG: upload files to a store, attach it as a tool, get grounded answers with page-level citations. Now multimodal with `gemini-embedding-2` and custom metadata.
- **LightRAG 1.5** (`lightrag-hku`). Merged RAG-Anything in May 2026, so it now parses PDFs and Office files through Docling or MinerU itself and ships a server with a web UI. The same five query modes MegaRAG copies.

## What did not change

- pgvector on Supabase, HNSW indexes, cosine distance.
- The five LightRAG query modes: naive, local, global, hybrid, mix (default).
- Entity and relation extraction, normalized-name dedupe, embedding `"{name}: {description}"`.
- Gemini Files API for video and audio (upload, poll until ACTIVE, reference by URI). Files expire after 48 hours, so Supabase Storage stays the system of record.
- `next-themes`, `cmdk`, `react-dropzone`, skeleton loading, the undo-toast delete pattern (now with `sonner`).
- The working method: let Claude Code explore first, keep `CLAUDE.md` current, test each phase before moving on.
