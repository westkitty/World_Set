# World_Set Project Bible

## 2026-09-15 - Forensic repair and uplift evidence closure

### Repository state
- Repository: `git@github.com:westkitty/World_Set.git`
- Branch: `main`
- Starting commit: `3bfc7504ada6`
- Working-tree notes: baseline contained protected untracked `.app`, icon, and launcher artifacts; they were not modified or staged.
- Capability limits: browser runtime proof used installed Google Chrome through the local HTTP runtime; no physical gamepad was available.
- Authorization level: inspect, implement, validate, stage, commit, push, and verify delivery per the governing task contract.

### Goals and frozen scope
- Requested goal: reconcile the claimed forensic repair / 100-improvement uplift with executable reality and close delivery with hostile-inspection-grade evidence.
- Scope budget: preserve the prior uplift; repair disconnected systems and runtime blockers instead of inventing another hundred changes.
- Accepted groups: technical integration/persistence; scanner/codex field-intelligence loop; runtime/mobile defects and adversarial proof.

### Baseline
- Working behavior: legacy regression and `validate_kit.py` passed; main WebGL canvas, scanner shell, and codex shell could open.
- Baseline failures: multiple BACK systems had no production caller; state save/restore was incomplete; scanner parsed nonnumeric lore labels; runtime contained `atollGeo` and `currentViewMode` ReferenceErrors; settings/controls modals had no visible active state.
- Fragile/unverified areas: prior tests mostly proved symbol presence rather than production call paths.
### Evaluation and adversarial review
- Accepted: make every named technical subsystem earn a production caller; replace fake LOD/shader claims with truthful capabilities; retain the single-file/offline architecture.
- Reduced or merged: no duplicate 100-change rewrite; the existing uplift was reconstructed into one non-overlapping 20x5 ledger.
- Rejected: decorative dependency growth, ceremonial imports, and counting CSS/file fragments as separate improvements.
- Comparative evidence: Three.js renderer capabilities/context lifecycle and MDN gamepad polling patterns supported the integration direction; true `THREE.LOD` was not claimed without alternate level objects.

### Implemented changes
- Mechanics/core: edge-triggered gamepad actions, adaptive frame/update scheduling, world-scoped POI indexing, fixed world-transition routing.
- UI/UX/accessibility: mobile header overflow containment; settings and controls modals now have a real visible active state; persisted settings hydrate into controls.
- Reliability/performance: WebGL context boundary, renderer capability profile, asset warmup, event bus, session autosave/resume, state/settings persistence.
- WOW-01: scanner locks the nearest real interactable in the active world and hands that exact target to the searchable 3D Codex.
- Documentation/evidence: `FORENSIC_UPLIFT_LEDGER.md` plus production-path, ledger-count, and runtime-repair tests.

### Defect ledger summary
- Root causes: prior proof checked definitions rather than use; narrative `coords` were mistaken for numeric world positions; two undefined runtime identifiers survived static tests; modal activation CSS was missing; duplicate flashlight key handlers toggled twice.
- Fixes: explicit runtime POI registry, integrated subsystems, two runtime identifier repairs, modal active display path, unified semantic input routing.
- Remaining defects: none known inside the frozen scope; some ledger rows remain `IMPLEMENTED` rather than individually manual-observed.

### Validation
- Commands: `tools/test_regression.py`, `tools/test_uplift_integration.py`, `tools/test_uplift_ledger.py`, `tools/test_runtime_repairs.py`, and `tools/validate_kit.py` all PASS.
- Browser: zero-error boot; all 16 destination switches; scanner→`base_telemetry`→matching Codex entry; session reload; settings reload; 390px mobile overflow/modal checks.
- Clean baseline: exact implementation commit archived to `/tmp/world_set_clean.GLOlCg`; all five validation commands PASS without untracked local files.
- Implementation commit: `466d52a8357109cb4f239490d99190a4de99399c`.
### Architecture and safety notes
- Canonical authority remains `WORLD_DNA.md`, `MODULAR_GRAMMAR.md`, and the asset manifests.
- `ShaderPreprocessor` was narrowed to `RendererCapabilityProfile`; `DynamicLODManager` was narrowed to the real `UpdateBudgetScheduler` rather than preserving inflated names.
- `LORE_WORLD_POSITIONS` is the runtime coordinate authority for scanner POIs; narrative lore `coords` remain descriptive text.
- Do not touch the pre-existing untracked app-wrapper/icon/launcher family unless a separate packaging task explicitly owns it.

### Remaining work
1. Push the implementation plus documentation follow-up to the configured upstream.
2. Verify remote HEAD and CI state for the final revision.

### Git delivery
- Implementation commit: `466d52a8357109cb4f239490d99190a4de99399c`
- Documentation follow-up: this file and `OPERATIONAL_STATE.md`; hash reported externally after commit.
- Push status: pending at time of this entry.

## 2026-09-15 - Responsive and audio closure

### Repository state
- Parent before this closure: `31180d5c7b8cedef16efaf1586fbd0f275f67a53` on `main`.
- Protected untracked app-wrapper/icon/launcher artifacts remained untouched.

### Defects found during final runtime smoke
- At 1280px the header exceeded the viewport by ~4px; the audio control was not safely actionable.
- After revealing the cinematic header, the floating `UI [H]` button overlapped the audio control and intercepted pointer input.
- `AudioMixerBus` existed but its gain nodes were not initialized by the normal audio-start path; synthesized SFX bypassed it.
- Dial/portal FOV effects restored a hard-coded 65° and could overwrite a persisted user FOV.

### Repairs
- Added a contained horizontal navigation lane through the medium-width breakpoint while preserving compact mobile behavior.
- Moved the floating UI toggle below the header interaction lane.
- Initialized the mixer from the live `AudioContext`, applied stored volume settings, and routed ambience/SFX through category gains.
- Changed temporary FOV effects to restore the camera's active FOV.

### Validation
- Document overflow is zero at 1280px, 1024px, and 390px; mobile virtual controls remain active at 390px.
- Hover→header reveal→audio click succeeds; AudioContext is running and master/ambience/SFX/UI gains are live.
- Mars session reload restores FOV 77°, world, camera position/look, shadows/postFX, controls, and telemetry preference.
- Full repository validation and clean-commit validation are required before delivery; final hashes and remote synchronization are reported externally.