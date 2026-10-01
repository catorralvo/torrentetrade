# Codex build brief — SubvenCH M3

## Mission

Convert the existing static M2 prototype in `/subvench` into a production-oriented browser application while preserving the evidence-first eligibility engine and the current visual identity.

Do not redesign the product concept. Do not add payments. Do not make an LLM decide eligibility.

## Stack

- Next.js App Router + TypeScript
- Supabase Postgres + Auth
- `@supabase/supabase-js` and `@supabase/ssr`, pinned versions + committed lockfile
- Node 22
- Deploy target: standard Next.js hosting; keep hosting provider decoupled

### Supabase target already selected

M3 must use the existing Supabase project `nidtuadgopthrydmmqcq` (`https://nidtuadgopthrydmmqcq.supabase.co`). This project also contains the DON’T 100 backend. Do not modify or rename any `dont100_*` object. SubvenCH objects are isolated by the `subvench_*` prefix and their own RLS policies. Read `SUPABASE_SHARED_PROJECT.md` before changing Auth/RLS because DON’T 100 may use anonymous Auth while SubvenCH explicitly blocks anonymous users from private tables.

Migrations `subvench_m2`, `subvench_shared_project_hardening`, and `subvench_optimize_anonymous_guard` have already been applied to the live project. Keep the matching SQL files in source control; future schema changes must be new migrations, not manual drift.

Use current Supabase conventions:

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`
- server-only secret key only if a privileged job actually needs it; never prefix it `NEXT_PUBLIC_`
- use `getClaims()` for protected page identity checks in SSR flows
- explicit Data API grants + RLS

## Preserve these domain invariants

1. Hard factual incompatibility overrides relevance score.
2. Unknown conditions become `to_verify`; never hallucinate them as satisfied.
3. Eligibility status and relevance percentage are separate concepts.
4. Every result must expose its official source and last verification date.
5. Historical scans are immutable snapshots.
6. Programme data is versioned.
7. Final eligibility and award decision remain with the authority.

## Existing reusable modules

- `/subvench/engine.mjs`: port to TypeScript with identical behavior first; improve only behind tests.
- `/subvench/data/programs.json` plus `/subvench/data/programs.m21.json`: seed catalogue inputs.
- `/subvench/workspace.mjs`: reference behavior for profiles/projects/scans/watches/alerts.
- `/subvench/supabase/migrations/`: live backend contract and hardening history.
- `/subvench/tests/`: regression expectations.

## Required routes

- `/` landing + CTA
- `/login`
- `/app` dashboard
- `/app/company` company profile
- `/app/projects/new`
- `/app/projects/[id]`
- `/app/projects/[id]/results`
- `/app/watch`
- `/app/alerts`

## M3 data behavior

### Company profile

One primary company profile per authenticated user in M3. Save canton, FTE, company classification and reusable eligibility attributes.

### Projects

Users can create multiple projects. Project-specific questions must not overwrite company-level facts.

### Scans

Each run stores:

- engine version
- catalog version
- full normalized input snapshot
- lean result snapshot
- timestamp

Never update an old scan in place.

### GrantWatch

When the catalogue version changes:

1. identify enabled watched projects;
2. run the deterministic engine using their last known input snapshot;
3. compare against the latest saved scan;
4. create alerts for:
   - new viable match,
   - eligibility status change,
   - material relevance change,
   - source unavailable / programme status changed;
5. save a new immutable scan.

M3 may implement the scheduled job as an explicit server route/worker contract if no scheduler is connected yet. Do not hardwire a paid service.

## Local-data migration

The current browser prototype stores M2 state in `localStorage` key `subvench:m2:workspace`.

After first authenticated login, if local M2 data exists and the account has no server projects:

- show a one-time import action;
- validate the JSON shape;
- insert profile/projects/scans/watches safely;
- mark local state as imported only after successful transaction-like completion;
- never silently discard local data.

## Security requirements

- RLS enabled on every exposed table.
- Explicit grants are mandatory.
- Every user-owned policy combines `TO authenticated` with ownership predicate `(select auth.uid()) = user_id`.
- SubvenCH private tables must retain the restrictive `is_anonymous` guard because this Supabase project is shared with DON’T 100.
- UPDATE policies need both `USING` and `WITH CHECK`.
- Do not use `user_metadata` for authorization.
- Do not expose service/secret keys to the client.
- Do not use `SECURITY DEFINER` merely to bypass a permission problem.
- If a privileged function is genuinely needed, place it in a non-exposed schema, revoke PUBLIC execute, and validate `auth.uid()` where relevant.
- Add indexes for columns used by RLS and common filters.
- Do not change shared project-wide Auth behavior solely for SubvenCH without checking DON’T 100 compatibility.

## Testing

Minimum automated coverage:

- current engine regression tests ported to TypeScript;
- hard canton exclusion;
- FTE limit exclusion;
- project-already-started exclusion;
- unknown requirement => `to_verify`;
- GrantWatch: new match alert;
- GrantWatch: eligibility changed alert;
- user A cannot read/update/delete user B profile/project/scan/watch/alert;
- anonymous Supabase user cannot read or write SubvenCH user-owned tables;
- catalogue audit: unique IDs, source URL, verification date, required fields.

## UI

Keep the current SubvenCH brand: restrained Swiss B2B interface, navy/teal, no generic AI gradients. Mobile responsive. Avoid dashboard clutter.

Each result card must show:

- authority
- programme name
- eligibility label
- relevance percentage
- funding summary
- why it matched
- blockers if excluded
- conditions to verify
- official source
- last verified date

## Not in M3

- billing / Stripe
- full dossier generation
- AI avatar/video
- nationwide 26-canton coverage
- advisor multi-client portal
- automatic submission to authorities

## Definition of done

M3 is done when an authenticated user can create a company profile, create a project, run the existing evidence engine, persist the scan, return later, see scan history, enable GrantWatch, and see generated alerts after a catalog-version change — with RLS tests proving cross-user isolation and anonymous-user exclusion.