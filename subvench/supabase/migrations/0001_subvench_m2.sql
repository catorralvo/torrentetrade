-- SubvenCH M2 schema
-- Designed for Supabase/Postgres with explicit grants + RLS.

create extension if not exists pgcrypto;

create table if not exists public.subvench_profiles (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  company_name text,
  canton text check (canton in ('VD','GE') or canton is null),
  fte integer check (fte is null or fte >= 0),
  industry_hightech boolean,
  industrial_company boolean,
  rd_or_production_in_canton boolean,
  production_tool_in_canton boolean,
  is_startup boolean,
  market_established boolean,
  swiss_uid text,
  local_jobs_impact boolean,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(user_id)
);

create table if not exists public.subvench_projects (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  profile_id uuid references public.subvench_profiles(id) on delete set null,
  name text not null,
  description text not null default '',
  budget_chf numeric(14,2),
  target_start_date date,
  project_started boolean,
  swiss_research_partner boolean,
  geneva_research_partner boolean,
  foreign_local_partner boolean,
  status text not null default 'draft' check (status in ('draft','active','archived')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.subvench_scans (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  project_id uuid not null references public.subvench_projects(id) on delete cascade,
  engine_version text not null,
  catalog_version text not null,
  input_snapshot jsonb not null,
  result_snapshot jsonb not null,
  created_at timestamptz not null default now()
);

create table if not exists public.subvench_watches (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  project_id uuid not null references public.subvench_projects(id) on delete cascade,
  program_id text,
  watch_type text not null default 'project' check (watch_type in ('project','program')),
  enabled boolean not null default true,
  last_checked_at timestamptz,
  last_change_at timestamptz,
  created_at timestamptz not null default now(),
  unique(user_id, project_id, program_id, watch_type)
);

create table if not exists public.subvench_alerts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  project_id uuid references public.subvench_projects(id) on delete cascade,
  program_id text,
  kind text not null check (kind in ('new_match','program_changed','deadline','eligibility_changed','source_issue')),
  title text not null,
  body text not null,
  payload jsonb not null default '{}'::jsonb,
  read_at timestamptz,
  created_at timestamptz not null default now()
);

create table if not exists public.subvench_program_versions (
  id uuid primary key default gen_random_uuid(),
  program_id text not null,
  source_url text not null,
  source_hash text,
  structured_payload jsonb not null,
  verified_at timestamptz not null default now(),
  effective_from date,
  effective_to date,
  is_current boolean not null default true
);

create index if not exists subvench_profiles_user_idx on public.subvench_profiles(user_id);
create index if not exists subvench_projects_user_idx on public.subvench_projects(user_id);
create index if not exists subvench_scans_user_project_idx on public.subvench_scans(user_id, project_id, created_at desc);
create index if not exists subvench_watches_user_idx on public.subvench_watches(user_id, enabled);
create index if not exists subvench_alerts_user_idx on public.subvench_alerts(user_id, created_at desc);
create index if not exists subvench_program_versions_program_idx on public.subvench_program_versions(program_id, verified_at desc);

alter table public.subvench_profiles enable row level security;
alter table public.subvench_projects enable row level security;
alter table public.subvench_scans enable row level security;
alter table public.subvench_watches enable row level security;
alter table public.subvench_alerts enable row level security;
alter table public.subvench_program_versions enable row level security;

grant select, insert, update, delete on public.subvench_profiles to authenticated;
grant select, insert, update, delete on public.subvench_projects to authenticated;
grant select, insert, delete on public.subvench_scans to authenticated;
grant select, insert, update, delete on public.subvench_watches to authenticated;
grant select, update on public.subvench_alerts to authenticated;
grant select on public.subvench_program_versions to authenticated, anon;

create policy "profiles_select_own" on public.subvench_profiles for select to authenticated using ((select auth.uid()) = user_id);
create policy "profiles_insert_own" on public.subvench_profiles for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "profiles_update_own" on public.subvench_profiles for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "profiles_delete_own" on public.subvench_profiles for delete to authenticated using ((select auth.uid()) = user_id);

create policy "projects_select_own" on public.subvench_projects for select to authenticated using ((select auth.uid()) = user_id);
create policy "projects_insert_own" on public.subvench_projects for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "projects_update_own" on public.subvench_projects for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "projects_delete_own" on public.subvench_projects for delete to authenticated using ((select auth.uid()) = user_id);

create policy "scans_select_own" on public.subvench_scans for select to authenticated using ((select auth.uid()) = user_id);
create policy "scans_insert_own" on public.subvench_scans for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "scans_delete_own" on public.subvench_scans for delete to authenticated using ((select auth.uid()) = user_id);

create policy "watches_select_own" on public.subvench_watches for select to authenticated using ((select auth.uid()) = user_id);
create policy "watches_insert_own" on public.subvench_watches for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "watches_update_own" on public.subvench_watches for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "watches_delete_own" on public.subvench_watches for delete to authenticated using ((select auth.uid()) = user_id);

create policy "alerts_select_own" on public.subvench_alerts for select to authenticated using ((select auth.uid()) = user_id);
create policy "alerts_update_own" on public.subvench_alerts for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);

create policy "program_versions_read" on public.subvench_program_versions for select to anon, authenticated using (true);

-- Program-version and alert writes stay server-side with a secret/service credential.
-- Never expose a secret/service role key in browser code.
