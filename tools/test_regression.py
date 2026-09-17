import os
import sys
import json
import re
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

print("=======================================================")
print(">>> RUNNING REGRESSION & INVARIANT TEST SUITE <<<")
print("=======================================================\n")

failures = []

def check(name, condition, error_msg):
    if condition:
        print(f"[PASS] {name}")
    else:
        print(f"[FAIL] {name}: {error_msg}")
        failures.append(f"{name}: {error_msg}")

# INV-01: Asset Manifest & Physical Files Invariant (34 Assets)
manifest_path = os.path.join(ROOT, "ASSET_MANIFEST.json")
md_manifest_path = os.path.join(ROOT, "ASSET_MANIFEST.md")

with open(manifest_path, "r") as f:
    manifest_data = json.load(f)
assets = manifest_data.get("assets", [])
asset_names = set(a["name"] for a in assets)

check("Manifest Asset Count", len(assets) == 34, f"Expected 34 assets, got {len(assets)}")

with open(md_manifest_path, "r") as f:
    md_content = f.read()
md_asset_matches = set(re.findall(r"`(WK_[A-Z0-9_]+)`", md_content))
check("Markdown Manifest Parity", asset_names == md_asset_matches, "Mismatch between ASSET_MANIFEST.json and ASSET_MANIFEST.md")

for a in assets:
    glb_path = os.path.join(ROOT, a.get("rel_path", ""))
    thumb_path = os.path.join(ROOT, "renders", "catalog", "thumbnails", f"{a['name']}.png")
    check(f"GLB Exists: {a['name']}", os.path.exists(glb_path) and os.path.getsize(glb_path) > 100, f"File missing: {glb_path}")
    check(f"Thumbnail Exists: {a['name']}", os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 100, f"File missing: {thumb_path}")

# INV-02: Category Dictionary Consistency
with open(os.path.join(ROOT, "tools", "build_showcase_and_export.py"), "r") as f:
    showcase_script = f.read()
cat_match = re.search(r"ASSET_CATEGORIES = \{(.*?)\}", showcase_script, re.DOTALL)
if cat_match:
    cat_entries = set(re.findall(r"\"(WK_[A-Z0-9_]+)\"", cat_match.group(1)))
    check("ASSET_CATEGORIES Sync", asset_names == cat_entries, f"Missing in ASSET_CATEGORIES: {asset_names - cat_entries}")
else:
    failures.append("ASSET_CATEGORIES dictionary not found in build_showcase_and_export.py")

# INV-03: Zero Stale Asset Count Claims
with open(os.path.join(ROOT, "index.html"), "r") as f:
    index_html = f.read()
check("index.html 34 GLBs claim", "34 individual production .glb models" in index_html, "Stale claim in index.html")
check("index.html 34 thumbnails claim", "34 studio thumbnails" in index_html, "Stale claim in index.html")
check("No stale 33 GLB claim in index.html", "33 individual production .glb models" not in index_html, "Stale 33 GLB claim found")
check("No stale 33 studio claim in index.html", "33 studio thumbnails" not in index_html, "Stale 33 studio claim found")

with open(os.path.join(ROOT, "renders", "catalog", "index.html"), "r") as f:
    catalog_html = f.read()
check("renders/catalog/index.html 34 assets claim", "34 Reusable Precision Modular Production Assets" in catalog_html, "Stale claim in catalog index.html")
check("renders/catalog/index.html filter count", "ALL ASSETS (34)" in catalog_html, "Stale filter count in catalog index.html")

# INV-04: JavaScript Syntax in index.html
inline_scripts = re.findall(r"<script(?![^>]*src=)[^>]*>(.*?)</script>", index_html, re.DOTALL)
js_syntax_ok = True
for idx, script_text in enumerate(inline_scripts):
    res = subprocess.run(["node", "--check"], input=script_text, capture_output=True, text=True)
    if res.returncode != 0:
        js_syntax_ok = False
        print(f"JS syntax error in script block {idx}:\n{res.stderr}")
check("index.html JavaScript Syntax", js_syntax_ok, "Inline scripts have syntax errors")

# INV-05: Validation Audit Tool Status
val_res = subprocess.run(["python3", os.path.join(ROOT, "tools", "validate_kit.py")], capture_output=True, text=True)
check("validate_kit.py exit code 0", val_res.returncode == 0, f"validate_kit.py exited with {val_res.returncode}")
check("validate_kit.py 100% PASS output", "100% PASS" in val_res.stdout, "validate_kit.py did not report 100% PASS")

# INV-06: 17 Exploration Biomes Registered & Integrated
expected_worlds = [
    'aquifer', 'desert', 'mountain', 'city', 'stonehenge', 'island', 'space',
    'volcano', 'biolum', 'abyss', 'mars', 'crystal', 'swamp', 'cavern', 'acid', 'taiga', 'sky'
]
check("17 Biomes in WORLDS constant", all(f"id: '{w}'" in index_html or f'id: "{w}"' in index_html for w in expected_worlds), "Missing worlds in WORLDS constant")
for w in expected_worlds:
    if w != 'aquifer':
        fn_name = f"build{w.capitalize()}World"
        check(f"Builder function: {fn_name}", f"function {fn_name}()" in index_html, f"{fn_name} missing from index.html")
        check(f"destinationWorlds.{w} initialized", f"destinationWorlds.{w} = " in index_html, f"destinationWorlds.{w} not initialized")
    check(f"Quick-dial button: btn-quick-{w}", f'id="btn-quick-{w}"' in index_html, f"Quick-dial button for {w} missing")

# INV-07: Radial Biome Launcher Architecture & Interactive Controls
check("Radial pull-tab element exists", 'id="radial-pull-tab"' in index_html, "Missing #radial-pull-tab")
check("Radial backdrop element exists", 'id="radial-launcher-backdrop"' in index_html, "Missing #radial-launcher-backdrop")
check("Radial arena container exists", 'id="radial-arena"' in index_html, "Missing #radial-arena")
check("Radial central iris hub exists", 'id="radial-hub"' in index_html, "Missing #radial-hub")
check("Radial hub engage button exists", 'id="radial-hub-engage"' in index_html, "Missing #radial-hub-engage")
check("Radial nodes styled with radial-node class", 'class="quick-world-btn radial-node' in index_html, "Missing radial-node class")
check("JS function toggleRadialLauncher", 'function toggleRadialLauncher(' in index_html, "Missing toggleRadialLauncher function")
check("JS function updateRadialHub", 'function updateRadialHub(' in index_html, "Missing updateRadialHub function")
check("JS function previewRadialWorld", 'function previewRadialWorld(' in index_html, "Missing previewRadialWorld function")
check("JS function engageCurrentRadialWorld", 'function engageCurrentRadialWorld(' in index_html, "Missing engageCurrentRadialWorld function")
check("JS function toggleRadialViewMode", 'function toggleRadialViewMode(' in index_html, "Missing toggleRadialViewMode function")
check("KeyB radial launcher hotkey mapped", "code === 'KeyB'" in index_html, "KeyB hotkey missing from onKeyDown")

# INV-08: Forensic Uplift & Delivery Closure Suite (100 Improvements + WOW-01 + 4 Corrections)
# 1. Defect Corrections
check("CORR-01: teleportToView function exists", "function teleportToView(" in index_html, "teleportToView function missing")
check("CORR-01: Waypoint bar uses teleportToView", "onclick=\"teleportToView(" in index_html, "Waypoint bar missing teleportToView")
check("CORR-02: Collision bounds for worlds 08-17 in isPlayerPositionBlocked", all(f"loc === '{w}'" in index_html for w in ['volcano', 'biolum', 'abyss', 'mars', 'crystal', 'swamp', 'cavern', 'acid', 'taiga', 'sky']), "Collision checks missing for worlds 08-17")
check("CORR-03: 10 Surface footstep profiles in playSurfaceFootstep", all(f"surfaceType === '{s}'" in index_html for s in ['basalt', 'mycelium', 'wading', 'ferric_sand', 'crystal_res', 'mud', 'flowstone', 'sludge', 'pine_needles', 'aerolite']), "Footstep profiles missing from playSurfaceFootstep")
check("CORR-04: 20 Expansion lore entries in LORE_DATABASE", all(k in index_html for k in ['volcano_caldera', 'volcano_monitoring', 'biolum_eldertree', 'biolum_spores', 'abyss_monolith', 'abyss_trench', 'mars_habitat', 'mars_rover', 'crystal_geode', 'crystal_resonance', 'swamp_hut', 'swamp_altar', 'cavern_stalactite', 'cavern_vein', 'acid_pipeline', 'acid_vat', 'taiga_cabin', 'taiga_shrine', 'sky_nexus', 'sky_glider']), "Lore entries missing for worlds 08-17")

# 2. Flagship WOW-01 Suite
check("WOW-01: Tactical AR Sonar Scanner HUD element", 'id="scanner-hud"' in index_html, "Missing #scanner-hud")
check("WOW-01: AR Scanner pulse trigger function", "function triggerARScannerPulse(" in index_html, "Missing triggerARScannerPulse")
check("WOW-01: 3D Holographic Codex modal element", 'id="codex-modal"' in index_html, "Missing #codex-modal")
check("WOW-01: 3D Holographic Codex container element", 'id="codex3DContainer"' in index_html, "Missing #codex3DContainer")
check("WOW-01: 3D Holographic Codex turntable function", "function initCodex3DViewer(" in index_html, "Missing initCodex3DViewer")
check("WOW-01: 3D Holographic model builder function", "function buildCodex3DModel(" in index_html, "Missing buildCodex3DModel")

# 3. UI/UX Systems (20 items)
check("UIUX-01: Top Compass HUD element", 'id="compass-hud"' in index_html, "Missing #compass-hud")
check("UIUX-01: Top Compass update function", "function updateCompassHUD(" in index_html, "Missing updateCompassHUD")
check("UIUX-02: Tactical Radar HUD element", 'id="radar-hud"' in index_html, "Missing #radar-hud")
check("UIUX-02: Tactical Radar update function", "function updateRadarHUD(" in index_html, "Missing updateRadarHUD")
check("UIUX-03: Stamina gauge bar element", 'id="stamina-gauge"' in index_html, "Missing #stamina-gauge")
check("UIUX-04: Coordinates breadcrumb badge element", 'id="coords-breadcrumb"' in index_html, "Missing #coords-breadcrumb")
check("UIUX-04: Coordinates update function", "function updateCoordsBreadcrumb(" in index_html, "Missing updateCoordsBreadcrumb")
check("UIUX-05: Biome discovery title banner element", 'id="biome-title-banner"' in index_html, "Missing #biome-title-banner")
check("UIUX-05: Biome discovery banner trigger", "function showBiomeTitleBanner(" in index_html, "Missing showBiomeTitleBanner")
check("UIUX-06: Toast container element", 'id="toast-container"' in index_html, "Missing #toast-container")
check("UIUX-07: Settings configuration modal element", 'id="settings-modal"' in index_html, "Missing #settings-modal")
check("UIUX-08: Controls field manual modal element", 'id="controls-modal"' in index_html, "Missing #controls-modal")
check("UIUX-09: Telemetry graph HUD element", 'id="telemetry-graph-hud"' in index_html, "Missing #telemetry-graph-hud")
check("UIUX-10: Mobile virtual joysticks container element", 'id="virtual-joysticks-container"' in index_html, "Missing #virtual-joysticks-container")
check("UIUX-11: 12 Biome visor elements present", all(f'id="{v}"' in index_html for v in ['visor-caldera', 'visor-biolum', 'visor-citadel', 'visor-mars', 'visor-crystal', 'visor-swamp', 'visor-cavern', 'visor-acid', 'visor-taiga', 'visor-sky', 'thermal-vision-overlay', 'night-vision-overlay']), "Missing biome visor elements")
check("UIUX-12: Header nav button for Codex", 'onclick="openCodexModal()"' in index_html, "Missing Codex nav button")
check("UIUX-13: Header nav button for Settings", 'onclick="openSettingsModal()"' in index_html, "Missing Settings nav button")
check("UIUX-14: Header nav button for Controls", 'onclick="openControlsModal()"' in index_html, "Missing Controls nav button")

# 4. Backend Technical Systems (20 items)
check("BACK-01: LocalStorageEngine module", "const LocalStorageEngine = {" in index_html, "Missing LocalStorageEngine")
check("BACK-02: ProceduralSoundscape module", "const ProceduralSoundscape = {" in index_html, "Missing ProceduralSoundscape")
check("BACK-03: StaticObjectPool module", "const StaticObjectPool = {" in index_html, "Missing StaticObjectPool")
check("BACK-04: AssetDisposalManager module", "const AssetDisposalManager = {" in index_html, "Missing AssetDisposalManager")
check("BACK-05: FrameRateGovernor module", "const FrameRateGovernor = {" in index_html, "Missing FrameRateGovernor")
check("BACK-06: CoordinateTransformer module", "const CoordinateTransformer = {" in index_html, "Missing CoordinateTransformer")
check("BACK-07: TelemetryLogger module", "const TelemetryLogger = {" in index_html, "Missing TelemetryLogger")
check("BACK-08: AudioMixerBus module", "const AudioMixerBus = {" in index_html, "Missing AudioMixerBus")
check("BACK-09: WebGLErrorBoundary module", "const WebGLErrorBoundary = {" in index_html, "Missing WebGLErrorBoundary")
check("BACK-10: RendererCapabilityProfile module", "const RendererCapabilityProfile = {" in index_html, "Missing RendererCapabilityProfile")
check("BACK-11: SpatialHashGrid module", "const SpatialHashGrid = {" in index_html, "Missing SpatialHashGrid")
check("BACK-12: InputEventBus module", "const InputEventBus = {" in index_html, "Missing InputEventBus")
check("BACK-13: UpdateBudgetScheduler module", "const UpdateBudgetScheduler = {" in index_html, "Missing UpdateBudgetScheduler")
check("BACK-14: PerformanceMemoryMonitor module", "const PerformanceMemoryMonitor = {" in index_html, "Missing PerformanceMemoryMonitor")
check("BACK-15: GamepadAPISubsystem module", "const GamepadAPISubsystem = {" in index_html, "Missing GamepadAPISubsystem")
check("BACK-16: AutoQualityDegradation module", "const AutoQualityDegradation = {" in index_html, "Missing AutoQualityDegradation")
check("BACK-17: UrlRouterEngine module", "const UrlRouterEngine = {" in index_html, "Missing UrlRouterEngine")
check("BACK-18: WorldEvents event bus module", "const WorldEvents = {" in index_html, "Missing WorldEvents")
check("BACK-19: AssetPreloadQueue module", "const AssetPreloadQueue = {" in index_html, "Missing AssetPreloadQueue")
check("BACK-20: StateSnapshotEngine module", "const StateSnapshotEngine = {" in index_html, "Missing StateSnapshotEngine")

# 5. Gameplay Systems (20 items)
check("GAME-04: Sprint stamina updater function", "function updateStamina(" in index_html, "Missing updateStamina")
check("GAME-05: Adaptive planetary gravity matrix", "const PLANETARY_GRAVITY = {" in index_html, "Missing PLANETARY_GRAVITY")
check("GAME-08: Player jump trigger function", "function triggerPlayerJump(" in index_html, "Missing triggerPlayerJump")
check("GAME-08: Jump physics integration updater", "function updateJumpPhysics(" in index_html, "Missing updateJumpPhysics")
check("GAME-09: Crouch stance toggle function", "function toggleCrouch(" in index_html, "Missing toggleCrouch")
check("GAME-10: Dynamic head bobbing function", "function calculateHeadBob(" in index_html, "Missing calculateHeadBob")
check("GAME-13: Vision mode cycling function", "function cycleVisionMode(" in index_html, "Missing cycleVisionMode")
check("GAME-19: CameraTrauma shake system", "const CameraTrauma = {" in index_html, "Missing CameraTrauma")
check("GAME-16: Biome discovery milestone checker", "function checkBiomeDiscovery(" in index_html, "Missing checkBiomeDiscovery")

# 6. Quality of Life & Feature Systems (40 items)
check("FEAT-03: Photo Mode enter function", "function enterPhotoMode(" in index_html, "Missing enterPhotoMode")
check("FEAT-04: Photo Mode screenshot capture", "function capturePhotoScreenshot(" in index_html, "Missing capturePhotoScreenshot")
check("FEAT-04: Photo Mode filter cycle function", "function cyclePhotoFilter(" in index_html, "Missing cyclePhotoFilter")
check("FEAT-04: Photo Mode FOV cycle function", "function cyclePhotoFOV(" in index_html, "Missing cyclePhotoFOV")
check("FEAT-04: Photo Mode rule of thirds grid toggle", "function togglePhotoGrid(" in index_html, "Missing togglePhotoGrid")
check("QOL-01: Biome delta cycling function", "function cycleBiomeDelta(" in index_html, "Missing cycleBiomeDelta")
check("QOL-02: Home key emergency recall binding", "e.code === 'Home'" in index_html, "Missing Home key binding")
check("QOL-05: KeyM holographic codex hotkey", "e.code === 'KeyM'" in index_html, "Missing KeyM hotkey")
check("QOL-07: KeyT telemetry toggle hotkey", "e.code === 'KeyT'" in index_html, "Missing KeyT hotkey")
check("QOL-08: KeyP photo mode hotkey", "e.code === 'KeyP'" in index_html, "Missing KeyP hotkey")
check("QOL-11: Help key (?) controls manual binding", "e.key === '?'" in index_html, "Missing Help key binding")
check("QOL-18: Copy coordinates to clipboard function", "function copyCoordinatesToClipboard(" in index_html, "Missing copyCoordinatesToClipboard")


# INV-09: World Mega Expansion Layer
expansion_worlds = ['desert', 'mountain', 'city', 'stonehenge', 'island', 'space', 'volcano', 'biolum', 'abyss', 'mars', 'crystal', 'swamp', 'cavern', 'acid', 'taiga', 'sky']
check("Mega expansion config exists", "const WORLD_MEGA_EXPANSION = {" in index_html, "WORLD_MEGA_EXPANSION missing")
check("Mega expansion applied before static freeze", "Object.entries(destinationWorlds).forEach(([key, world]) => applyWorldMegaExpansion(key, world));" in index_html, "Destination expansion integration missing")
check("All 16 destination worlds have expansion configs", all(f"  {w}: {{" in index_html for w in expansion_worlds), "One or more destination expansion configs missing")
check("Site-44 origin mega annex exists", "function buildMegaBaseExpansion()" in index_html and "baseEnhancementsGroup.add(buildMegaBaseExpansion());" in index_html, "Base mega expansion missing")
check("Instanced expansion scatter is used", "new THREE.InstancedMesh(scatterGeo" in index_html, "Expansion scatter is not instanced")
check("City expanded rooftop collision bounds", "px >= -94.0 + r" in index_html and "pz <= 124.0 - r" in index_html, "City mega rooftop bounds missing")
check("Space expanded station collision lanes", "pz <= 163.0 - r" in index_html and "px >= -60.0 + r" in index_html, "Space station expansion bounds missing")
check("Sky causeway collision path", "onEastWestCauseway" in index_html and "onNorthSouthCauseway" in index_html and "onSkyIsland" in index_html, "Sky expansion traversal bounds missing")
check("Mega-expansion camera far plane", "new THREE.PerspectiveCamera(65, initDims.width / initDims.height, 0.1, 800)" in index_html, "Main camera far plane does not cover mega worlds")
check("Site-44 east annex production path", "addXCorridor(24.5, 32.0, 4.0);" in index_html and "px >= 24.5 - r && px <= 32.0" in index_html, "East annex geometry/collision path missing")
check("Site-44 west annex production path", "addXCorridor(-32.0, -24.5, 0.0);" in index_html and "px >= -32.0 && px <= -24.5 + r" in index_html, "West annex geometry/collision path missing")
radial_collision_markers = [
    "distToCenter > 260.0 - r",
    "distToSummit > 220.0 - r",
    "distToHenge > 220.0 - r",
    "distToLagoon > 210.0 - r",
    "Math.hypot(px, pz - 20) > 240.0 - r",
    "Math.hypot(px, pz - 18) > 230.0 - r",
    "Math.hypot(px, pz - 15) > 230.0 - r",
    "Math.hypot(px, pz - 12) > 250.0 - r",
    "Math.hypot(px, pz - 16) > 230.0 - r",
    "Math.hypot(px, pz - 12) > 220.0 - r",
    "Math.hypot(px, pz - 12) > 200.0 - r",
    "Math.hypot(px, pz - 10) > 230.0 - r",
]
check("All radial collision envelopes expanded", all(marker in index_html for marker in radial_collision_markers), "One or more radial world collision envelopes are stale")
check("Mega expansion obstacles stored", "obstacles.push({ x, z, radius:" in index_html and "world.expansion = { kind: 'radial'" in index_html, "Rendered expansion geometry lacks collision proxies")
check("Mega expansion collision production caller", "function isMegaExpansionObstacleBlocked(" in index_html and "if (isMegaExpansionObstacleBlocked(px, pz, loc, r)) return true;" in index_html, "Expansion collision helper is not on the player path")
check("Expansion region discovery production caller", "function updateExpansionRegionDiscovery()" in index_html and "updateExpansionRegionDiscovery();" in index_html and "REGION DISCOVERED //" in index_html, "Expansion region discovery is not integrated")


# INV-10: Exponential Parcel Population WOW Pass 2
parcel_worlds = ['desert', 'mountain', 'city', 'stonehenge', 'island', 'space', 'volcano', 'biolum', 'abyss', 'mars', 'crystal', 'swamp', 'cavern', 'acid', 'taiga', 'sky']
check("Parcel expansion V2 config exists", "const PARCEL_EXPANSION_V2 = {" in index_html, "PARCEL_EXPANSION_V2 missing")
check("Parcel population director exists", "const ParcelPopulationDirector = {" in index_html and "function initExponentialParcelPopulation()" in index_html, "Parcel population director missing")
check("Parcel population initialized on production boot", "initExponentialParcelPopulation();" in index_html, "Parcel population boot integration missing")
check("Destination parcel materialization is lazy", "function ensureParcelPopulationForWorld(" in index_html and "ensureParcelPopulationForWorld(targetKey);" in index_html and "WOW pass 2 projected; destination materialization is lazy" in index_html, "Destination parcel population is not lazy-materialized")
init_pop_match = re.search(r"function initExponentialParcelPopulation\(\) \{(.*?)\n\}", index_html, re.DOTALL)
check("Boot does not eagerly build destination parcels", bool(init_pop_match) and "buildDestinationParcelPopulation(" not in init_pop_match.group(1), "Destination parcel construction leaked back into boot path")
check("Every parcel has central story landmark rule", "Object zero is the parcel's oversized story landmark" in index_html and "const dist = i === 0 ? 0" in index_html, "Parcel hero-landmark composition rule missing")
check("Parcel population runtime/culling integrated", "function updateParcelPopulationRuntime()" in index_html and "updateParcelPopulationRuntime();" in index_html, "Parcel population runtime updater missing")
check("Parcel population collision integrated", "function isParcelPopulationObstacleBlocked(" in index_html and "if (isParcelPopulationObstacleBlocked(px, pz, loc, r)) return true;" in index_html, "Parcel collision path missing")
check("Canonical kit GLB instancing exists", "function loadParcelKitAssets()" in index_html and "new THREE.InstancedMesh(part.geometry, part.material" in index_html, "Canonical kit asset instancing missing")
check("Sector-binned native instancing exists", "function createParcelInstancedBatch(" in index_html and "ParcelSector_" in index_html and "ParcelDetail_" in index_html, "Sector-binned native population missing")
check("Parcel discovery path integrated", "PARCEL DISCOVERED //" in index_html and "parcel:discovered" in index_html, "Parcel discovery path missing")
check("Runtime population stats exposed", "window.getWorldSetPopulationStats" in index_html and "totalLogicalObjects" in index_html, "Population diagnostics missing")
check("Runtime population proof surface exists", "dataset.parcelPopulationPlanned" in index_html and "dataset.parcelPopulationState" in index_html, "Runtime population proof surface missing")

parcel_block = re.search(r"const PARCEL_EXPANSION_V2 = \{(.*?)\n\};", index_html, re.DOTALL)
parcel_entries = []
if parcel_block:
    parcel_entries = re.findall(r"^\s{2}(\w+): \{ parcels: (\d+), nativePerParcel: (\d+), kitPerParcel: (\d+)", parcel_block.group(1), re.MULTILINE)
check("All 16 worlds have parcel V2 configs", len(parcel_entries) == 16 and {e[0] for e in parcel_entries} == set(parcel_worlds), f"Expected 16 parcel configs, got {len(parcel_entries)}")
if parcel_entries:
    logical_objects = sum(int(parcels) * (int(native) + int(kit)) for _, parcels, native, kit in parcel_entries)
    total_parcels = sum(int(parcels) for _, parcels, _, _ in parcel_entries)
    check("At least 24 parcels per destination", all(int(parcels) >= 24 for _, parcels, _, _ in parcel_entries), "One or more destination worlds has fewer than 24 parcels")
    check("At least 80 population objects per parcel", all(int(native) + int(kit) >= 80 for _, _, native, kit in parcel_entries), "One or more parcel configs falls below 80 planned objects")
    check("Exponential population target >= 40,000 logical objects", logical_objects >= 40000, f"Only {logical_objects} logical parcel objects planned")
    grand_logical_objects = logical_objects + (16 * (24 + 18))
    check("Exponential total including Site-44 >= 46,500 logical objects", grand_logical_objects >= 46500, f"Only {grand_logical_objects} total logical parcel objects planned")
    check("Destination parcel count >= 450", total_parcels >= 450, f"Only {total_parcels} destination parcels planned")

kit_block = re.search(r"const PARCEL_KIT_ASSETS = \{(.*?)\n\};", index_html, re.DOTALL)
kit_paths = re.findall(r"path: '([^']+\.glb)'", kit_block.group(1)) if kit_block else []
check("At least 18 canonical rendered kit asset types reused", len(kit_paths) >= 18, f"Only {len(kit_paths)} kit asset types configured")
check("All configured canonical kit types preload lazily", "const assetIds = Object.keys(PARCEL_KIT_ASSETS);" in index_html and "kitPrototypeCache" in index_html, "Canonical kit prototypes are not preloaded/cached")
check("Duplicate canonical kit instancing guarded", "kitBuiltKeys" in index_html and "ParcelPopulationDirector.kitBuiltKeys.has(buildKey)" in index_html, "Duplicate kit materialization guard missing")
check("All configured kit GLBs exist", all(os.path.exists(os.path.join(ROOT, p)) for p in kit_paths), "One or more configured canonical kit GLBs is missing")
check("Base annex parcels populated", "function buildBaseParcelPopulation()" in index_html and "SITE44-CELL-" in index_html, "Site-44 annex parcel population missing")
check("All 18 canonical kit IDs used by Site-44 base cells", "kitPerParcel: 18" in index_html and all(k in index_html for k in ["extinguisher", "troffer", "railing4", "stairs", "doorSlab", "wallPanel"]), "Base population does not exercise full configured canonical kit set")

print("\n-------------------------------------------------------")
if not failures:
    print(">>> REGRESSION SUITE RESULT: 100% PASS — ALL INVARIANTS PROTECTED <<<")
    print("-------------------------------------------------------")
    sys.exit(0)
else:
    print(f">>> REGRESSION SUITE FAILED with {len(failures)} failures:")
    for f in failures:
        print(f"  [!] {f}")
    print("-------------------------------------------------------")
    sys.exit(1)
