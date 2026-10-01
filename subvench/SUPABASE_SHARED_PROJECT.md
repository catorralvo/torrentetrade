# SubvenCH — shared Supabase project

## Existing project identified

Supabase project ref: `nidtuadgopthrydmmqcq`

Project URL: `https://nidtuadgopthrydmmqcq.supabase.co`

Organization plan: Free.

The project was created on 2026-08-27 and is the backend previously prepared for **DON’T 100**. Existing migrations/tables use the `dont100_` prefix. At the time SubvenCH was integrated there were zero Auth users and zero rows in the DON’T 100 tables.

## Decision

For the MVP, SubvenCH reuses this Supabase project instead of creating a second paid/isolated project.

This is acceptable because:

- DON’T 100 and SubvenCH use distinct table prefixes (`dont100_` vs `subvench_`).
- RLS is enabled on the SubvenCH user-owned tables.
- SubvenCH user rows are ownership-scoped by `auth.uid()`.
- A restrictive RLS layer blocks Supabase anonymous users from SubvenCH private tables, allowing DON’T 100 to keep guest/anonymous flows if needed.
- No secret/service key is exposed in browser code.

## Shared-project caveats

Auth configuration, quotas, project uptime and database resources are shared. This is deliberate for the MVP/free stage. If either product reaches material traffic or needs incompatible Auth settings, SubvenCH should be moved to its own Supabase project before scaling.

## Applied migrations

- `subvench_m2`
- `subvench_shared_project_hardening`

The GitHub copies are in `subvench/supabase/migrations/`.

## M3 environment

Use:

```env
NEXT_PUBLIC_SUPABASE_URL=https://nidtuadgopthrydmmqcq.supabase.co
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=<fetch from Supabase project at deploy time>
```

Do not commit secret/service-role credentials.
