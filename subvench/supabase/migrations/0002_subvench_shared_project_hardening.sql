-- SubvenCH M2 hardening for the existing shared Supabase project.
-- The same project also hosts DON’T 100 tables, which may use anonymous Auth.
-- Keep SubvenCH private user data inaccessible to anonymous Supabase users.

create index if not exists subvench_projects_profile_idx on public.subvench_projects(profile_id);
create index if not exists subvench_scans_project_idx on public.subvench_scans(project_id);
create index if not exists subvench_watches_project_idx on public.subvench_watches(project_id);
create index if not exists subvench_alerts_project_idx on public.subvench_alerts(project_id);

create policy "subvench_profiles_no_anonymous"
on public.subvench_profiles as restrictive
for all to authenticated
using ((select auth.jwt()->>'is_anonymous') is distinct from 'true')
with check ((select auth.jwt()->>'is_anonymous') is distinct from 'true');

create policy "subvench_projects_no_anonymous"
on public.subvench_projects as restrictive
for all to authenticated
using ((select auth.jwt()->>'is_anonymous') is distinct from 'true')
with check ((select auth.jwt()->>'is_anonymous') is distinct from 'true');

create policy "subvench_scans_no_anonymous"
on public.subvench_scans as restrictive
for all to authenticated
using ((select auth.jwt()->>'is_anonymous') is distinct from 'true')
with check ((select auth.jwt()->>'is_anonymous') is distinct from 'true');

create policy "subvench_watches_no_anonymous"
on public.subvench_watches as restrictive
for all to authenticated
using ((select auth.jwt()->>'is_anonymous') is distinct from 'true')
with check ((select auth.jwt()->>'is_anonymous') is distinct from 'true');

create policy "subvench_alerts_no_anonymous"
on public.subvench_alerts as restrictive
for all to authenticated
using ((select auth.jwt()->>'is_anonymous') is distinct from 'true')
with check ((select auth.jwt()->>'is_anonymous') is distinct from 'true');
