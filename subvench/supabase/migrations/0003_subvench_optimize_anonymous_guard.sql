-- Optimize the shared-project anonymous-user guard so auth.jwt() is evaluated once per statement.

drop policy if exists "subvench_profiles_no_anonymous" on public.subvench_profiles;
drop policy if exists "subvench_projects_no_anonymous" on public.subvench_projects;
drop policy if exists "subvench_scans_no_anonymous" on public.subvench_scans;
drop policy if exists "subvench_watches_no_anonymous" on public.subvench_watches;
drop policy if exists "subvench_alerts_no_anonymous" on public.subvench_alerts;

create policy "subvench_profiles_no_anonymous"
on public.subvench_profiles as restrictive
for all to authenticated
using (((select auth.jwt())->>'is_anonymous') is distinct from 'true')
with check (((select auth.jwt())->>'is_anonymous') is distinct from 'true');

create policy "subvench_projects_no_anonymous"
on public.subvench_projects as restrictive
for all to authenticated
using (((select auth.jwt())->>'is_anonymous') is distinct from 'true')
with check (((select auth.jwt())->>'is_anonymous') is distinct from 'true');

create policy "subvench_scans_no_anonymous"
on public.subvench_scans as restrictive
for all to authenticated
using (((select auth.jwt())->>'is_anonymous') is distinct from 'true')
with check (((select auth.jwt())->>'is_anonymous') is distinct from 'true');

create policy "subvench_watches_no_anonymous"
on public.subvench_watches as restrictive
for all to authenticated
using (((select auth.jwt())->>'is_anonymous') is distinct from 'true')
with check (((select auth.jwt())->>'is_anonymous') is distinct from 'true');

create policy "subvench_alerts_no_anonymous"
on public.subvench_alerts as restrictive
for all to authenticated
using (((select auth.jwt())->>'is_anonymous') is distinct from 'true')
with check (((select auth.jwt())->>'is_anonymous') is distinct from 'true');
