# DON’T 100 — Production Audit V5

## Goal
Move DON’T 100 from iterative prototype quality to commercial mobile-game production quality while preserving the approved mascot, 100-level structure, backend, timers, checkpoints and multilingual shell.

## Current structural risk
The Android build currently reconstructs the embedded game and then applies a chain of Python patches:
- rc12_patch.py
- rc_final_patch.py
- rc_final2_patch.py
- rc_visualpro_patch.py
- rc_pro3d_patch.py
- rc_gameplayfix_patch.py

This patch chain is now the main source of regressions. New visual changes can unintentionally override earlier mechanics, CSS or rendering assumptions.

## Production direction
1. Freeze v4.x as reference.
2. Build v5 on a clean branch.
3. Consolidate the generated runtime into maintainable source modules instead of text-replacement patches.
4. Keep the existing product shell and backend.
5. Replace the ad-hoc arcade rendering layer with a proper game-engine layer.
6. Migrate arcade games incrementally, not as a full rewrite.

## Recommended rendering/game layer
Phaser 4.2.1, integrated only for arcade scenes at first.

Why:
- WebGL renderer
- particles
- tweens
- cameras
- physics
- filters/glow/shadow
- dynamic textures
- mobile web support
- open-source MIT framework
- can stay inside the existing Android WebView / Capacitor-style delivery model

The existing DOM shell can continue handling:
- top bar
- language
- level progression
- total timer
- checkpoint UI
- ranking
- backend / analytics

Phaser handles:
- arcade scenes
- input
- sprite animation
- collisions
- particle effects
- camera effects
- game object lifecycle
- high-DPI rendering

## Art production pipeline
Approved mascot remains unchanged.

Create a coherent asset system:
- 6–8 environment families
- prop sheets
- reusable UI/gameplay objects
- particle textures
- lighting overlays
- consistent shadows
- sprite atlases

Use AI generation only for source art and references, then normalize assets to a consistent palette and scale.

Useful sources:
- Higgsfield for art-direction references, background concepts and animation references
- OpenAI image generation for consistent transparent props/background layers
- Kenney CC0 assets as production-safe supporting material where useful
- original vector/canvas assets for brand-specific elements

## Animation
Replace rapid pose swapping with:
- named animation states
- frame durations
- anticipation
- action
- settle
- success/fail reactions
- easing curves
- minimum readable hold time

Mascot animation should be event-driven, not permanently cycling.

## Audio
Current sound feedback is too lightweight for commercial polish.

Add:
- UI click family
- correct / wrong
- combo / streak
- countdown
- level clear
- fail
- checkpoint
- arcade-specific SFX
- short adaptive music loop
- ducking and volume groups

Recommended runtime: Howler.js or Phaser audio.

## Game feel
Every arcade should include the appropriate subset of:
- impact flash
- particles
- scale punch
- screen/camera shake
- easing
- anticipation
- trails
- combo feedback
- danger feedback
- near-miss feedback

No effect should reduce gameplay readability.

## Mobile controls
Finger must not hide important action.

Control patterns:
- lower trackpad for continuous horizontal motion
- separate fire/action button
- direct manipulation only when the object remains visible
- generous touch targets
- pointer smoothing
- dead zones where needed

## QA gates
No build may be labeled FINAL until:
- all 100 mechanics render without JS errors
- 36 arcade mechanics receive input smoke tests
- critical games receive gameplay simulations
- no vertical scroll in gameplay
- 320x568 and 390x844 both pass
- screenshots reviewed visually
- “do nothing and win” tests fail where interaction is required
- “impossible despite correct input” tests fail
- performance stays smooth on mid-range Android target

## Performance
Targets:
- 60 FPS on normal gameplay
- stable memory across repeated level transitions
- texture reuse
- sprite atlases
- no orphan animation loops/listeners
- no repeated asset decoding
- DPR capped sensibly on high-density phones

## Priority production milestones
P0 Architecture:
- freeze v4
- clean v5 source
- remove patch-chain dependency

P1 Vertical slice:
Rebuild 5 representative arcades to production quality:
- Star Blaster
- Breakout
- Waiter Balance
- Whack
- Flappy

P2 Art/animation/audio system:
- reusable scene backgrounds
- VFX
- sound system
- mascot animation controller

P3 Full migration:
- migrate remaining arcade scenes
- balance pass
- mobile control pass

P4 Production QA:
- automated visual/input regression
- device testing
- store-ready package

## Definition of professional
Professional quality does not mean simply “more 3D.”
For DON’T 100 it means:
- coherent art direction
- reliable controls
- readable gameplay
- polished animation
- audio feedback
- effects
- difficulty fairness
- performance
- consistency across all 100 levels
- zero obvious prototype regressions

## Immediate next action
Build one production-quality vertical slice in Phaser 4.2.1 without touching the current playable v4 branch. Once the slice is better than the current Canvas equivalent, migrate the rest incrementally.
