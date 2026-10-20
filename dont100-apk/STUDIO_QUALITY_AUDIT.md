# DON'T 100 — Studio-quality gap audit (2026-10-20)

Status: preliminary static audit, NOT gameplay QA or release approval.
Branch: dont100-apk-test-v4-2. Target: v4.4 STUDIO RC.

## Verified from repository
- Workflow reconstructs index.html from compressed webchunks and applies six sequential Python patches.
- Workflow checks JavaScript syntax with node --check and builds Android API 36 debug APK.
- Existing game-fix patch replaces runWhack and runWaiterBalance.
- Whack: 5 spawn spots, 7 successful taps, 2 misses fail, X expires without miss.
- Waiter: auto bias and periodic direction changes, fall/spill failure, 8.5s win.
- Current workflow labels its artifact v4.3.1, not v4.4.
- Patch files include fragile string matching/replacements; refactor only with regression checks.

## Highest priority gaps
P0: executable behavior tests for 36 arcades, idle-input loss, reachable wins, single pass/fail, timer cleanup, 100-level invariants.
P0: reproducible build manifest, checksums, regression snapshots before patch consolidation.
P1: unified mobile input and accessibility audit across 320x568 and 390x844.
P1: art style guide, consistent backgrounds, FX budget, animation timing, transitions.
P1: audio cue taxonomy, mute control, mobile audio-unlock behavior, haptics fallback.
P2: analytics funnels and balancing, low-end device profiling, store assets and release QA.

## Tooling to evaluate without spend
- Playwright + Chromium screenshots and touch emulation for smoke testing (environment permitting).
- Node built-in test runner for deterministic game state/physics extracted into modules.
- GitHub Actions matrix for JS checks, HTML build, screenshots, regression tests.
- Procedural Canvas 2D effects before adding WebGL dependency.
- Web Audio procedural SFX; CC0 assets from Kenney/OpenGameArt only after license review.
- Existing Supabase events for anonymized win/fail duration metrics.
- Higgsfield optional for trailer only; never spend credits without authorization.

## Acceptance gates for v4.4
1. All 100 challenges reachable; no 101; special level 100 preserved.
2. Every arcade: demonstrable win, loss, idle loss, cleanup, input usability.
3. Whack and Waiter scripted tests plus screenshots.
4. No JavaScript console errors or blank canvas at target viewports.
5. Manual device check and user approval before calling build FINAL.

## Next implementation tasks
1. Extract reproducible reconstructed HTML into test fixture without altering production.
2. Implement browser harness and baseline snapshots.
3. Fix observed failures; preserve KEEP-UP no-time-limit rule.
4. Add shared audio/FX/input layers only after gameplay gates.
5. Compile v4.4 RC and publish as Actions artifact, not production release.
