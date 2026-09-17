# World_Set Operational State
<!-- operational-state:metadata
{
  "schema_version": 1,
  "project_id": "world_set",
  "project_name": "World_Set",
  "project_root": "/Users/andrew/World_Set",
  "artifact_path": "index.html",
  "state_revision": 7,
  "last_updated": "2026-09-17T22:04:26Z",
  "current_baseline": {
    "identity": "WOW pass 2 exponential parcel population atop the uncommitted mega expansion: 46,586 projected logical objects across 484 parcels/cells, 18 canonical GLB prototype types, lazy per-world materialization, sector detail culling, collision and discovery integration; static/integration suites verified; direct visual traversal remains unverified",
    "state": "partially-verified",
    "last_verified": "2026-09-17T22:04:26Z"
  },
  "scope_boundaries": ["World_Set repository", "single-file offline Three.js exploration runtime", "existing 34-asset production kit", "native macOS application wrapper and Dock icon"],
  "linked_parent_state": null
}
-->

## 1. Project Identity and Scope
World_Set is the Site-44 Sub-Aquifer World Kit and its browser exploration runtime. The current task continues the forensic repair, uplift, and native desktop wrapper integration already represented by commits `63c8f70`, `483f232`, and `9007912`, without replacing the canonical world-kit identity.

## 2. Current Baseline
- Branch: `main`; upstream `origin/main` remains at `a2217ee`; current mega-expansion changes are intentionally uncommitted in the working tree.
- Baseline static suites: `tools/test_regression.py` PASS, `tools/test_runtime_repairs.py` PASS, `tools/test_uplift_integration.py` PASS, `tools/test_uplift_ledger.py` PASS, and `tools/validate_kit.py` PASS.
- Browser boot observed in installed Chrome: primary WebGL canvas present, renderer initialized, loader dismissed, origin world active.
- Native application wrapper: `/Applications/World Set.app` installed, ad-hoc signed, and pinned to user Dock at slot 38. Tooling and assets tracked (`tools/world_set_launcher.c`, `tools/generate_dock_icon.py`, `renders/AppIcon.icns`, `renders/app_icon_1024.png`).
- Validation tooling is path-portable: `tools/validate_kit.py` and `tools/test_regression.py` derive the repository root from their script location.
- `tools/enhance_worlds.py` is intentionally retired and non-runtime; kit authority remains `WORLD_DNA`, manifests, and Blender export tools.
- Player playtest on 2026-09-17: load/settings/resize **OBSERVED**; movement/codex **UNKNOWN this pass**.
- Mega expansion working tree: Site-44 gains physically connected Sector 03-B / 06-B annexes; all 16 destination worlds gain larger explorable outer regions, named landmarks, matched collision proxies, and expanded collision envelopes; city/space/sky use bespoke topology rather than the radial template. Destination fog ranges are retuned for the larger spaces, and approaching any of the four named regions per destination emits the existing toast/event discovery path.
- Expansion performance strategy uses deterministic `THREE.InstancedMesh` scatter and preserves the existing single-file/offline architecture; the main camera far plane is raised from 300m to 800m to cover the new 400-520m world diameters.
- WOW pass 2 population contract: 468 destination parcels plus 16 Site-44 annex cells; 42,120 new destination-native procedural objects, 3,794 destination canonical-kit placements, and 672 Site-44 parcel objects for **46,586 projected logical objects**. Every destination parcel plans at least 80 objects and one oversized central story landmark.
- Population delivery is lazy: only the 16 Site-44 cells materialize during boot; each destination parcel layer materializes on first portal entry and remains cached. Canonical WORLD KIT prototypes are preloaded asynchronously from 18 existing GLBs and instanced from shared geometry/materials; no Three.js upgrade or new dependency was introduced.
- Detail populations are sector-binned and distance-toggled; major parcel objects remain present for silhouette/navigation. Parcel-native major objects and collidable canonical-kit instances participate in the existing collision resolver, and parcel arrival emits the existing toast/event path.
- All five project suites PASS after expansion; `/Applications/World Set.app` launches the current repository on port 8000 with HTTP 200. Direct visual traversal of the new outer regions is **UNVERIFIED** because the available macOS browser/screen-capture automation exposed invalid/blank DevTools contexts and screen capture was unavailable.
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
{"id":"INV-002","title":"Packaging and app-wrapper integration completed per user specification","state":"verified","rule":"Dedicated native macOS wrapper, icon generator, and launcher tooling are tracked in source; build intermediates and local .app bundle are protected in .gitignore; /Applications/World Set.app is installed and pinned to Dock.","scope":"Packaging and Git working tree","authority":"Explicit user task contract","evidence":"tools/world_set_launcher.c; tools/generate_dock_icon.py; renders/AppIcon.icns; dockutil verification at slot 38","validation_method":"dockutil --find 'World Set' and codesign -vvv","last_checked":"commit 9007912","status":"active","recheck_trigger":"Any packaging or dock integration change"}
-->
### INV-002 — Packaging and app-wrapper integration completed per user specification
- **State:** `verified`
- **Rule:** Standalone native wrapper and Dock icon are fully installed, tested, and tracked in source control.
<!-- /operational-state:entry -->

<!-- operational-state:entry
{"id":"INV-010","title":"Preserve exponential parcel population and lazy materialization","state":"requested","rule":"WOW pass 2 must project at least 46,500 logical parcel objects, keep at least 24 destination parcels per world and at least 80 planned objects per destination parcel, reuse at least 18 canonical WORLD KIT GLB types, keep one central story landmark per parcel, and never eagerly construct all destination parcel populations during boot.","scope":"Parcel population, destination transition, collision, performance scheduling, regression tests","authority":"Explicit 2026-09-17 user request plus accepted performance correction","evidence":"PARCEL_EXPANSION_V2; PARCEL_KIT_ASSETS; ParcelPopulationDirector; tools/test_regression.py INV-10","validation_method":"Run all five project suites; verify INV-10 quantitative/lazy gates; direct browser traversal remains required for visual promotion","last_checked":"2026-09-17T22:04:26Z","status":"active","recheck_trigger":"Any parcel count, density, asset reuse, world-entry, instancing, culling, collision, or boot-path change"}
-->
### INV-010 — Preserve exponential parcel population and lazy materialization
- **State:** `requested`
- **Rule:** Keep the second-pass density genuinely multiplicative while protecting boot cost: ≥46,500 projected parcel objects, ≥24 destination parcels/world, ≥80 objects/destination parcel, ≥18 canonical GLB types reused, central parcel landmarks, and no eager all-world parcel construction at boot.
<!-- /operational-state:entry -->
## 5. Verified Working Behavior
<!-- operational-state:entry
{"id":"VER-001","title":"Primary browser runtime boots","state":"partially-verified","capability":"The primary exploration view historically initializes a Three.js renderer and visible canvas and clears the loader; the current mega-expansion working tree requires fresh direct canvas observation because camera/render-loop code changed.","scope":"Chrome local HTTP runtime","verification_method":"Current wrapper launch + HTTP 200 + Chrome renderer process observed; prior direct canvas proof from 2026-09-15 retained as historical evidence","evidence":"2026-09-17 current index served on port 8000 with HTTP 200; served SHA-256 323e61323f85fc7b592440ae6b84f305789d23a7f5a592d4ba7f4e9db91fa1c7 exactly matched local index.html; Chrome renderer process launched; direct canvas inspection unavailable because DevTools execution contexts remained about:blank and screencapture was unavailable","artifact_revision":"working tree atop a2217ee","last_verified":"2026-09-17T21:31:59Z","dependencies":["installed Chrome","local HTTP server"],"freshness":"current baseline partial","recheck_trigger":"fresh direct browser canvas smoke on current working tree"}
-->
### VER-001 — Primary browser runtime boots
- **State:** `partially-verified`
- **Capability:** Prior direct Chrome proof remains historical; the current mega-expansion working tree launches through the wrapper and serves successfully, but still needs fresh direct canvas observation.
<!-- /operational-state:entry -->

<!-- operational-state:entry
{"id":"VER-002","title":"Scanner and 3D codex open","state":"verified","capability":"AR scanner activates and the 3D codex opens with 55 lore entries and a WebGL codex canvas.","scope":"WOW-01 user path","verification_method":"Direct browser runtime invocation","evidence":"scanner active=true; codex active=true; entries=55; codex canvas=true","artifact_revision":"final repair state","last_verified":"2026-09-15T10:49:00Z","dependencies":["main renderer","LORE_DATABASE"],"freshness":"current baseline","recheck_trigger":"scanner, codex, lore database, or modal lifecycle change"}
-->
### VER-002 — Scanner and 3D codex open
- **State:** `verified`
- **Capability:** Both flagship component paths are currently reachable.
<!-- /operational-state:entry -->

<!-- operational-state:entry
{"id":"VER-003","title":"Standalone native macOS app wrapper & dock launcher","state":"verified","capability":"/Applications/World Set.app manages background server on port 8000 and launches Chrome/Brave dedicated app mode; pinned to user Dock at slot 38.","scope":"Desktop application wrapper","verification_method":"dockutil and codesign verification","evidence":"dockutil slot 38; codesign valid on disk; curl port 8000 HTTP 200 OK","artifact_revision":"commit 9007912","last_verified":"2026-09-15T19:18:00Z","dependencies":["dockutil","codesign","Chrome/Brave"],"freshness":"current baseline","recheck_trigger":"packaging or launcher source change"}
-->
### VER-003 — Standalone native macOS app wrapper & dock launcher
- **State:** `verified`
- **Capability:** Dedicated desktop application bundle installed, signed, and accessible from Dock.
<!-- /operational-state:entry -->

## 6. Known Not Working
- None known inside the frozen forensic-repair scope after the final static, browser, world-transition, persistence, mobile-layout, and clean-archive validation gates.
## 7. Implemented but Unverified
- Some individual visual/game-feel items in `FORENSIC_UPLIFT_LEDGER.md` remain marked `IMPLEMENTED` rather than individually runtime-observed; they passed source/integration/project validation but were not each manually exercised.
- The 2026-09-17 mega-expansion geometry and collision integration is implemented and statically/integration verified, but the newly expanded outer traversal zones have not yet received trustworthy direct visual/runtime traversal proof.
- WOW pass 2 exponential parcel population is implemented and regression-verified at 46,586 projected logical objects across 484 parcels/cells, including lazy first-entry materialization, 18 canonical GLB prototype types, procedural story landmarks, sector detail culling, collisions, and discovery events. The newly populated parcels remain **implemented-unverified visually** until a trustworthy direct traversal/render pass is available.

## 8. Unknown or Evidence-Stale State
- Physical gamepad hardware was unavailable, so real-device controller feel/haptics remain unverified; Gamepad API polling, edge-trigger routing, and production integration are verified in source/integration tests.
- Repository inspection found no GitHub Actions workflows and no configured GitHub Pages site; CI and deployment are therefore not applicable to this repository state.
- Runtime automation limitation on 2026-09-17: Chrome DevTools targets advertised the local URL while evaluating in blank `about:blank` contexts; macOS `screencapture` returned `could not create image from display`. Treat those automation attempts as harness failure, not application verification.
- A fresh SwiftShader/headless probe during WOW pass 2 again produced repeated macOS `CVDisplayLinkCreateWithCGDisplay` failures and stalled before trustworthy application-state inspection. An initial eager implementation was rejected after server chronology exposed severe boot blocking; the delivered lazy design removes eager destination parcel construction, but current-headless startup/render timing remains untrusted until tested in a normal visible browser session.

## 9. Pending Work
- Prior forensic/packaging phases remain complete at `a2217ee`. Mega expansion + WOW pass 2 exponential parcel population are implemented and suite-verified in the working tree. Before promotion/publication, perform one trustworthy visible-browser traversal of Site-44 and representative radial/city/space/sky destinations, record first-entry parcel materialization cost, confirm canonical-kit hydration, and visually inspect density/readability/collision.

## 10. Active Decisions, Defaults, and Prohibitions
- Preserve the current single-file/offline browser architecture; add no dependency unless evidence makes it necessary.
- Do not implement fake Three.js LOD: narrow the unused stub to a real adaptive update-budget mechanism.
- Native application wrapper tooling and assets are committed; local build directories are protected via `.gitignore`.
- Do not manufacture new improvements merely to repeat already implemented value; count only distinct inspectable behavior.
- Preserve the WOW pass 2 lazy-population architecture: never rebuild all destination parcel populations at boot merely to make counts easier to claim. Full projected density is a contract; materialization is demand-driven by first world entry.
- Continue using the vendored `THREE.InstancedMesh` path for repeated geometry. `BatchedMesh` is absent from the project's vendored Three.js build; do not upgrade Three.js solely to obtain it without a separate migration decision.

## 11. Validation and Evidence Matrix
| ID | Claim | State | Current evidence | Required recheck |
| --- | --- | --- | --- | --- |
| INV-001 | Canonical kit remains intact | verified | clean-archive `validate_kit.py` PASS | recheck on asset/world-kit changes |
| INV-002 | App wrapper & dock integration | verified | wrapper unchanged; `/Applications/World Set.app` launch + port 8000 HTTP 200 on 2026-09-17 | recheck on packaging delivery |
| VER-001 | Main browser runtime boots | partially-verified | current wrapper launch + HTTP 200 + Chrome renderer process; prior direct canvas proof is historical | fresh direct browser canvas smoke on current working tree |
| VER-002 | Scanner/codex reachable | verified | installed Chrome runtime | flagship integration smoke |
| VER-003 | Desktop wrapper & dock launcher | verified | `/Applications/World Set.app` active | recheck on launcher edits |
| VER-004 | All-world mega expansion | partially-verified | 5/5 project suites PASS; expansion-specific regression gates PASS; app serves current index on :8000 | direct visual traversal of base annex + representative radial/city/space/sky outer zones |
| INV-010 | Exponential parcel population remains dense and lazy | verified | INV-10 regression: 46,586 projected logical objects; 468 destination parcels + 16 base cells; ≥80 objects/destination parcel; 18 canonical GLB types; boot eager-build guard PASS | recheck any population/boot/materialization change |
| VER-005 | WOW pass 2 parcels visually populate all worlds | partially-verified | source/integration/regression PASS; all five suites PASS; direct normal-browser visual traversal unavailable | visible-browser traversal + first-entry timing + representative collision/readability checks |
## 12. Current Change Scope and Impact Radius
- Current mega-expansion + WOW pass 2 files changed: `index.html`, `tools/test_regression.py`, and this operational state. No authored GLB/Blend assets, vendored libraries, packaging tools, or dependencies changed. Existing canonical GLBs are referenced/reused at runtime; their source files remain untouched.
- Impact radius: runtime bootstrap, render loop, scanner/codex integration, input routing, persistence, performance scheduling, browser lifecycle handling, documentation truth, and desktop application wrapper.
- Protected outside radius: authored asset files, Blender master, and generated production GLBs.

## 13. Compact Revision Log
- Revision 1 — 2026-09-15: bootstrapped operational state from baseline evidence; recorded shallow uplift-proof gap and frozen repair scope.
- Revision 2 — 2026-09-15: promoted repaired runtime/integration paths after Chrome, 16-world, persistence, mobile, full-suite, and clean-archive proof; implementation commit `466d52a8357109cb4f239490d99190a4de99399c`.
- Revision 3 — 2026-09-15: closed medium-width header overflow/overlap, live audio-mixer routing, and FOV persistence; revalidated 1280/1024/390 layouts, audio user gesture, world sweep, scanner→Codex, and session/settings reload.
- Revision 4 — 2026-09-15: integrated native macOS standalone application bundle (`/Applications/World Set.app`) and high-res Stargate Dock icon at slot 38; synchronized commit `9007912` with upstream `origin/main`; verified 100% PASS across all 5 test suites.
- Revision 5 — 2026-09-17: made `validate_kit.py` and `test_regression.py` repository-root portable, explicitly retired the dead `enhance_worlds.py` stub, preserved player-playtest uncertainty for movement/Codex, and verified all five static suites plus validation/regression from an isolated `/tmp` copy.
- Revision 6 — 2026-09-17: drastically expanded Site-44 and all 16 destination worlds; added deterministic instanced outer-region geometry, four discoverable named regions per destination, collision proxies tied to rendered scatter/towers/modules/beacons, expanded collision envelopes, special city/space/sky traversal topology, reachable Sector 03-B/06-B base annexes, long-range fog tuning, an 800m far plane, and INV-09 regression coverage. Five project suites pass; wrapper launch/HTTP delivery observed; direct visual traversal remains explicitly unverified.
- Revision 7 — 2026-09-17: ran the requested exponential WOW pass over every world. Added 468 destination parcels + 16 Site-44 cells with 46,586 projected logical objects, central parcel landmarks, biome-specific procedural populations, 18 canonical WORLD KIT GLB prototype types instanced from shared geometry/materials, parcel collisions/discovery, and sector distance culling. Rejected an eager first implementation after boot chronology exposed blocking, then converted destination population to lazy first-entry materialization with cached prototypes and added INV-10 quantitative/lazy regression gates. All five project suites PASS; direct visual traversal remains explicitly unverified because the macOS headless/WebGL harness is unreliable.
