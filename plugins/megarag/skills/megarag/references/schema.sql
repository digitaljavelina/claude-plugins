-- MegaRAG schema, refreshed October 2026.
-- Run as one Supabase migration: `supabase migration new megarag_init`, paste, `supabase db push`.
--
-- Changes from the December 2025 build guide:
--   * vector(1536), not 768. text-embedding-004 shut down 2026-01-14. gemini-embedding-2
--     defaults to 3072 dims; we truncate to 1536 (auto-normalized) because a pgvector
--     HNSW index on `vector` tops out at 2000 dims. Use halfvec(3072) if you want full size.
--   * Full-text column (fts) + GIN index, so retrieval can fuse keyword and vector hits (RRF).
--   * workspace_id on every row, plus Row Level Security. The guide named workspaces in the
--     query API but never enforced them.
--   * chat_sessions / chat_messages tables. The guide's Phase 9 history UI needed them.
--   * `context` column on chunks for contextual retrieval (a short "where this chunk sits
--     in the document" line, embedded with the chunk).

create extension if not exists vector with schema extensions;

-- ---------------------------------------------------------------- enums
create type public.processing_status as enum ('pending', 'processing', 'processed', 'failed');

create type public.chunk_type as enum (
  'text', 'table', 'image',
  'video_overview', 'video_moment', 'video_segment',
  'audio_summary', 'audio_topic', 'audio_segment'
);

create type public.query_mode as enum ('naive', 'local', 'global', 'hybrid', 'mix');

-- ---------------------------------------------------------------- tables
create table public.workspaces (
  id         uuid primary key default gen_random_uuid(),
  name       text not null,
  owner_id   uuid not null default auth.uid() references auth.users (id) on delete cascade,
  created_at timestamptz not null default now()
);

create table public.documents (
  id            uuid primary key default gen_random_uuid(),
  workspace_id  uuid not null references public.workspaces (id) on delete cascade,
  file_name     text not null,
  file_type     text not null,               -- extension, lowercase, no dot
  mime_type     text,
  file_size     bigint,
  storage_path  text not null unique,        -- {workspace_id}/{document_id}/{file_name}
  content_hash  text,                        -- sha-256 of the file; skip re-processing duplicates
  status        public.processing_status not null default 'pending',
  error_message text,
  chunks_count  int not null default 0,
  metadata      jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

create table public.chunks (
  id            uuid primary key default gen_random_uuid(),
  document_id   uuid not null references public.documents (id) on delete cascade,
  workspace_id  uuid not null references public.workspaces (id) on delete cascade,
  chunk_index   int not null,
  chunk_type    public.chunk_type not null default 'text',
  content       text not null,
  context       text,                        -- contextual-retrieval prefix
  embedding     extensions.vector(1536),
  fts           tsvector generated always as (
                  to_tsvector('english', coalesce(context, '') || ' ' || content)
                ) stored,
  page          int,                         -- documents
  start_seconds numeric,                     -- video / audio
  end_seconds   numeric,
  metadata      jsonb not null default '{}'::jsonb,
  created_at    timestamptz not null default now()
);

create table public.entities (
  id               uuid primary key default gen_random_uuid(),
  workspace_id     uuid not null references public.workspaces (id) on delete cascade,
  name             text not null,
  normalized_name  text not null,
  entity_type      text not null,
  description      text,
  embedding        extensions.vector(1536),
  source_chunk_ids uuid[] not null default '{}',
  created_at       timestamptz not null default now(),
  updated_at       timestamptz not null default now(),
  unique (workspace_id, normalized_name)
);

create table public.relations (
  id               uuid primary key default gen_random_uuid(),
  workspace_id     uuid not null references public.workspaces (id) on delete cascade,
  source_entity_id uuid not null references public.entities (id) on delete cascade,
  target_entity_id uuid not null references public.entities (id) on delete cascade,
  relation_type    text not null,
  description      text,
  weight           real not null default 1,  -- bumped each time another chunk repeats the relation
  embedding        extensions.vector(1536),
  source_chunk_ids uuid[] not null default '{}',
  created_at       timestamptz not null default now(),
  unique (workspace_id, source_entity_id, target_entity_id, relation_type)
);

create table public.llm_cache (
  cache_key  text primary key,               -- sha-256 of model + mode + prompt + corpus version
  model      text not null,
  response   jsonb not null,
  created_at timestamptz not null default now(),
  expires_at timestamptz not null default now() + interval '7 days'
);

create table public.chat_sessions (
  id           uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces (id) on delete cascade,
  user_id      uuid not null default auth.uid() references auth.users (id) on delete cascade,
  title        text not null default 'New chat',
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);

create table public.chat_messages (
  id         uuid primary key default gen_random_uuid(),
  session_id uuid not null references public.chat_sessions (id) on delete cascade,
  role       text not null check (role in ('user', 'assistant')),
  content    text not null,
  mode       public.query_mode,
  sources    jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now()
);

-- ---------------------------------------------------------------- indexes
create index chunks_embedding_hnsw    on public.chunks    using hnsw (embedding extensions.vector_cosine_ops);
create index entities_embedding_hnsw  on public.entities  using hnsw (embedding extensions.vector_cosine_ops);
create index relations_embedding_hnsw on public.relations using hnsw (embedding extensions.vector_cosine_ops);
create index chunks_fts_gin           on public.chunks    using gin (fts);
create index chunks_workspace_idx     on public.chunks    (workspace_id);
create index chunks_document_idx      on public.chunks    (document_id);
create index documents_workspace_idx  on public.documents (workspace_id, status);
create index entities_chunks_gin      on public.entities  using gin (source_chunk_ids);
create index relations_source_idx     on public.relations (source_entity_id);
create index relations_target_idx     on public.relations (target_entity_id);
create index chat_messages_session    on public.chat_messages (session_id, created_at);

-- ---------------------------------------------------------------- row level security
-- Browser code uses the publishable key plus the signed-in user's session, so RLS applies.
-- Server-side processing uses the secret key (sb_secret_...), which bypasses RLS.
create function public.my_workspace_ids()
returns setof uuid
language sql stable security definer set search_path = ''
as $$ select id from public.workspaces where owner_id = (select auth.uid()) $$;

alter table public.workspaces    enable row level security;
alter table public.documents     enable row level security;
alter table public.chunks        enable row level security;
alter table public.entities      enable row level security;
alter table public.relations     enable row level security;
alter table public.llm_cache     enable row level security;  -- no policies: server-only
alter table public.chat_sessions enable row level security;
alter table public.chat_messages enable row level security;

create policy "owner manages workspace" on public.workspaces
  for all to authenticated
  using (owner_id = (select auth.uid())) with check (owner_id = (select auth.uid()));

create policy "workspace members" on public.documents for all to authenticated
  using (workspace_id in (select public.my_workspace_ids()))
  with check (workspace_id in (select public.my_workspace_ids()));
create policy "workspace members" on public.chunks for select to authenticated
  using (workspace_id in (select public.my_workspace_ids()));
create policy "workspace members" on public.entities for select to authenticated
  using (workspace_id in (select public.my_workspace_ids()));
create policy "workspace members" on public.relations for select to authenticated
  using (workspace_id in (select public.my_workspace_ids()));
create policy "own sessions" on public.chat_sessions for all to authenticated
  using (user_id = (select auth.uid()) and workspace_id in (select public.my_workspace_ids()))
  with check (user_id = (select auth.uid()) and workspace_id in (select public.my_workspace_ids()));
create policy "own messages" on public.chat_messages for all to authenticated
  using (session_id in (select id from public.chat_sessions where user_id = (select auth.uid())))
  with check (session_id in (select id from public.chat_sessions where user_id = (select auth.uid())));

-- ---------------------------------------------------------------- search functions
-- security invoker (the default): callers only ever see rows RLS lets them see.
-- hnsw.iterative_scan keeps filtered HNSW searches from returning too few rows (pgvector 0.8+).

create function public.search_chunks(
  query_embedding extensions.vector(1536),
  match_threshold float,
  match_count     int,
  p_workspace_id  uuid
)
returns table (
  id uuid, document_id uuid, content text, context text, chunk_type public.chunk_type,
  page int, start_seconds numeric, end_seconds numeric, metadata jsonb, similarity float
)
language sql stable
set search_path = public, extensions
set hnsw.iterative_scan = relaxed_order
as $$
  select c.id, c.document_id, c.content, c.context, c.chunk_type,
         c.page, c.start_seconds, c.end_seconds, c.metadata,
         1 - (c.embedding <=> query_embedding) as similarity
  from chunks c
  where c.workspace_id = p_workspace_id
    and 1 - (c.embedding <=> query_embedding) > match_threshold
  order by c.embedding <=> query_embedding
  limit match_count;
$$;

-- Keyword + vector, fused with Reciprocal Rank Fusion. The default retrieval path for
-- naive mode and the chunk half of mix mode. Catches exact terms (drug names, IDs,
-- acronyms) that embeddings blur.
create function public.hybrid_search_chunks(
  query_text       text,
  query_embedding  extensions.vector(1536),
  match_count      int,
  p_workspace_id   uuid,
  full_text_weight float default 1,
  semantic_weight  float default 1,
  rrf_k            int   default 60
)
returns table (
  id uuid, document_id uuid, content text, context text, chunk_type public.chunk_type,
  page int, start_seconds numeric, end_seconds numeric, metadata jsonb, score float
)
language sql stable
set search_path = public, extensions
set hnsw.iterative_scan = relaxed_order
as $$
  with full_text as (
    select c.id,
           row_number() over (order by ts_rank_cd(c.fts, websearch_to_tsquery('english', query_text)) desc) as rank_ix
    from chunks c
    where c.workspace_id = p_workspace_id
      and c.fts @@ websearch_to_tsquery('english', query_text)
    order by rank_ix
    limit least(match_count, 30) * 2
  ),
  semantic as (
    select c.id,
           row_number() over (order by c.embedding <=> query_embedding) as rank_ix
    from chunks c
    where c.workspace_id = p_workspace_id
    order by rank_ix
    limit least(match_count, 30) * 2
  )
  select c.id, c.document_id, c.content, c.context, c.chunk_type,
         c.page, c.start_seconds, c.end_seconds, c.metadata,
         coalesce(1.0 / (rrf_k + ft.rank_ix), 0.0) * full_text_weight
       + coalesce(1.0 / (rrf_k + s.rank_ix), 0.0) * semantic_weight as score
  from full_text ft
  full outer join semantic s on ft.id = s.id
  join chunks c on c.id = coalesce(ft.id, s.id)
  order by score desc
  limit match_count;
$$;

create function public.search_entities(
  query_embedding extensions.vector(1536),
  match_threshold float,
  match_count     int,
  p_workspace_id  uuid
)
returns table (
  id uuid, name text, entity_type text, description text, source_chunk_ids uuid[], similarity float
)
language sql stable
set search_path = public, extensions
set hnsw.iterative_scan = relaxed_order
as $$
  select e.id, e.name, e.entity_type, e.description, e.source_chunk_ids,
         1 - (e.embedding <=> query_embedding) as similarity
  from entities e
  where e.workspace_id = p_workspace_id
    and 1 - (e.embedding <=> query_embedding) > match_threshold
  order by e.embedding <=> query_embedding
  limit match_count;
$$;

create function public.search_relations(
  query_embedding extensions.vector(1536),
  match_threshold float,
  match_count     int,
  p_workspace_id  uuid
)
returns table (
  id uuid, source_entity_id uuid, source_name text, target_entity_id uuid, target_name text,
  relation_type text, description text, weight real, source_chunk_ids uuid[], similarity float
)
language sql stable
set search_path = public, extensions
set hnsw.iterative_scan = relaxed_order
as $$
  select r.id, r.source_entity_id, s.name, r.target_entity_id, t.name,
         r.relation_type, r.description, r.weight, r.source_chunk_ids,
         1 - (r.embedding <=> query_embedding) as similarity
  from relations r
  join entities s on s.id = r.source_entity_id
  join entities t on t.id = r.target_entity_id
  where r.workspace_id = p_workspace_id
    and 1 - (r.embedding <=> query_embedding) > match_threshold
  order by r.embedding <=> query_embedding
  limit match_count;
$$;

-- ---------------------------------------------------------------- storage
-- Private bucket. 100 MB per file; raise it if the plan allows and you need long video.
-- Supabase's global upload cap (plan setting) still applies on top of this.
insert into storage.buckets (id, name, public, file_size_limit)
values ('documents', 'documents', false, 104857600)
on conflict (id) do nothing;

-- Object paths start with the workspace id: {workspace_id}/{document_id}/{file_name}
create policy "workspace members read" on storage.objects for select to authenticated
  using (bucket_id = 'documents'
         and (storage.foldername(name))[1]::uuid in (select public.my_workspace_ids()));
create policy "workspace members upload" on storage.objects for insert to authenticated
  with check (bucket_id = 'documents'
              and (storage.foldername(name))[1]::uuid in (select public.my_workspace_ids()));
create policy "workspace members delete" on storage.objects for delete to authenticated
  using (bucket_id = 'documents'
         and (storage.foldername(name))[1]::uuid in (select public.my_workspace_ids()));
