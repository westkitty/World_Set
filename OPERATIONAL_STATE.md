# World_Set Operational State
<!-- operational-state:metadata
{
  "schema_version": 1,
  "project_id": "world_set",
  "project_name": "World_Set",
  "project_root": "/Users/andrew/World_Set",
  "artifact_path": "index.html",
  "state_revision": 3,
  "last_updated": "2026-09-15T10:50:00Z",
  "current_baseline": {
    "identity": "final repair state on main; parent 31180d5c7b8cedef16efaf1586fbd0f275f67a53; final SHA reported externally",
    "state": "verified",
    "last_verified": "2026-09-15T10:49:00Z"
  },
  "scope_boundaries": ["World_Set repository", "single-file offline Three.js exploration runtime", "existing 34-asset production kit"],
  "linked_parent_state": null
}
-->

## 1. Project Identity and Scope
World_Set is the Site-44 Sub-Aquifer World Kit and its browser exploration runtime. The current task continues the forensic repair and uplift already represented by commit `63c8f70`, without replacing the canonical world-kit identity.

## 2. Current Baseline
- Branch: `main`; upstream: `origin/main`; starting HEAD: `3bfc7504ada6`; ahead/behind: `0/0`.
- Baseline static suites: `tools/test_regression.py` PASS and `tools/validate_kit.py` PASS.
- Browser boot observed in installed Chrome: primary WebGL canvas present, renderer initialized, loader dismissed, origin world active.
- Pre-existing untracked `.app`, icon, and launcher artifacts are protected and excluded from this pass.
## 3. Artifact Contract
The browser artifact must remain offline-capable, preserve existing exploration behavior, use the existing Three.js/runtime architecture, and keep current world-kit assets and canonical specifications authoritative. The forensic uplift count must be supported by integrated behavior rather than symbol existence.

## 4. Active Invariants
<!-- operational-state:entry
{"id":"INV-001","title":"Preserve canonical world-kit identity","state":"requested","rule":"WORLD_DNA.md, MODULAR_GRAMMAR.md, and the 34-asset manifest remain authoritative for Site-44 visual and modular identity.","scope":"All repository changes","authority":"Canonical project files plus current task","evidence":"WORLD_DNA.md; MODULAR_GRAMMAR.md; ASSET_MANIFEST.md","validation_method":"Run validate_kit.py and inspect attributable diff","last_checked":"baseline 3bfc7504ada6","status":"active","recheck_trigger":"Any asset, world-kit, rendering, or documentation change"}
-->
### INV-001 — Preserve canonical world-kit identity
- **State:** `requested`
- **Rule:** Canonical world DNA, modular grammar, and 34-asset manifest remain controlling.
<!-- /operational-state:entry -->

<!-- operational-state:entry
{"id":"INV-002","title":"Preserve pre-existing user work","state":"requested","rule":"Do not modify, stage, reset, or commit the pre-existing untracked app-wrapper, icon, or launcher artifacts.","scope":"Git working tree","authority":"Current task safety contract","evidence":"Baseline git status","validation_method":"Compare final git status and staged diff to baseline","last_checked":"baseline 3bfc7504ada6","status":"active","recheck_trigger":"Any Git staging or delivery action"}
-->
### INV-002 — Preserve pre-existing user work
- **State:** `requested`
- **Rule:** Pre-existing untracked app-wrapper/icon/launcher work remains untouched and unstaged.
<!-- /operational-state:entry -->
## 5. Verified Working Behavior
<!-- operational-state:entry
{"id":"VER-001","title":"Primary browser runtime boots","state":"verified","capability":"The primary exploration view initializes a Three.js renderer and visible canvas and clears the loader.","scope":"Chrome local HTTP runtime","verification_method":"Headless installed Chrome against http://127.0.0.1:8765/index.html","evidence":"viewport canvas=true; renderer=true; activeWorldKey=aquifer; currentLocation=base; loader=none","artifact_revision":"final repair state","last_verified":"2026-09-15T10:49:00Z","dependencies":["installed Chrome","local HTTP server"],"freshness":"current baseline","recheck_trigger":"index.html runtime/bootstrap/render-loop change"}
-->
### VER-001 — Primary browser runtime boots
- **State:** `verified`
- **Capability:** Main WebGL exploration path initializes successfully in installed Chrome.
<!-- /operational-state:entry -->

<!-- operational-state:entry
{"id":"VER-002","title":"Scanner and 3D codex open","state":"verified","capability":"AR scanner activates and the 3D codex opens with 55 lore entries and a WebGL codex canvas.","scope":"WOW-01 user path","verification_method":"Direct browser runtime invocation","evidence":"scanner active=true; codex active=true; entries=55; codex canvas=true","artifact_revision":"final repair state","last_verified":"2026-09-15T10:49:00Z","dependencies":["main renderer","LORE_DATABASE"],"freshness":"current baseline","recheck_trigger":"scanner, codex, lore database, or modal lifecycle change"}
-->
### VER-002 — Scanner and 3D codex open
- **State:** `verified`
- **Capability:** Both flagship component paths are currently reachable.
<!-- /operational-state:entry -->

## 6. Known Not Working
- None known inside the frozen forensic-repair scope after the final static, browser, world-transition, persistence, mobile-layout, and clean-archive validation gates.
## 7. Implemented but Unverified
- Some individual visual/game-feel items in `FORENSIC_UPLIFT_LEDGER.md` remain marked `IMPLEMENTED` rather than individually runtime-observed; they passed source/integration/project validation but were not each manually exercised.

## 8. Unknown or Evidence-Stale State
- Physical gamepad hardware was unavailable, so real-device controller feel/haptics remain unverified; Gamepad API polling, edge-trigger routing, and production integration are verified in source/integration tests.
- Repository inspection found no GitHub Actions workflows and no configured GitHub Pages site; CI and deployment are therefore not applicable to this repository state.

## 9. Pending Work
- No completion-blocking source work remains. Final upstream synchronization is verified externally after the containing commit is created.

## 10. Active Decisions, Defaults, and Prohibitions
- Preserve the current single-file/offline browser architecture; add no dependency unless evidence makes it necessary.
- Do not implement fake Three.js LOD: narrow the unused stub to a real adaptive update-budget mechanism.
- Do not touch or stage baseline untracked app-wrapper/icon/launcher artifacts.
- Do not manufacture new improvements merely to repeat already implemented value; count only distinct inspectable behavior.

## 11. Validation and Evidence Matrix
| ID | Claim | State | Current evidence | Required recheck |
| --- | --- | --- | --- | --- |
| INV-001 | Canonical kit remains intact | verified | clean-archive `validate_kit.py` PASS | recheck on asset/world-kit changes |
| INV-002 | User work preserved | verified | protected untracked paths remain unstaged | recheck on Git delivery |
| VER-001 | Main browser runtime boots | verified | installed Chrome runtime | browser smoke after edits |
| VER-002 | Scanner/codex reachable | verified | installed Chrome runtime | flagship integration smoke |
## 12. Current Change Scope and Impact Radius
- Primary files allowed to change: `index.html`, uplift/integration tests, operational state, forensic ledger, and project Bible.
- Impact radius: runtime bootstrap, render loop, scanner/codex integration, input routing, persistence, performance scheduling, browser lifecycle handling, and documentation truth.
- Protected outside radius: authored asset files, Blender master, generated production GLBs, and baseline untracked app-wrapper artifacts.

## 13. Compact Revision Log
- Revision 1 — 2026-09-15: bootstrapped operational state from baseline evidence; recorded shallow uplift-proof gap and frozen repair scope.
- Revision 2 — 2026-09-15: promoted repaired runtime/integration paths after Chrome, 16-world, persistence, mobile, full-suite, and clean-archive proof; implementation commit `466d52a8357109cb4f239490d99190a4de99399c`.
- Revision 3 — 2026-09-15: closed medium-width header overflow/overlap, live audio-mixer routing, and FOV persistence; revalidated 1280/1024/390 layouts, audio user gesture, world sweep, scanner→Codex, and session/settings reload.