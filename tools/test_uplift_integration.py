from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "index.html").read_text()
failures = []


def check(name, condition, detail):
    if condition:
        print(f"[PASS] {name}")
    else:
        print(f"[FAIL] {name}: {detail}")
        failures.append(f"{name}: {detail}")


print("=== FORENSIC UPLIFT PRODUCTION-PATH TESTS ===")

check("BACK-05 frame governor called by render loop",
      "FrameRateGovernor.getClampedDelta()" in source,
      "render loop does not consume the frame governor")
check("BACK-09 WebGL boundary initialized on live canvas",
      "WebGLErrorBoundary.init(renderer.domElement)" in source and "WebGLErrorBoundary.contextLost" in source,
      "context-loss boundary lacks live renderer integration")
check("BACK-10 renderer capability profile detected",
      "RendererCapabilityProfile.detect(renderer)" in source and "ShaderPreprocessor" not in source,
      "renderer capabilities are not profiled or stale shader claim remains")
check("BACK-11 scanner uses active-scope spatial index",
      "SpatialHashGrid.queryNear(p.x, p.z, 50.0)" in source and
      "SpatialHashGrid.rebuildForScope(scope)" in source and
      "const scope = currentLocation === 'base' ? 'base' : currentLocation;" in source,
      "scanner is not world-scoped through SpatialHashGrid")
check("BACK-12 unified input bus has keyboard production callers",
      "InputEventBus.trigger('scan')" in source and "InputEventBus.trigger('codex-toggle')" in source,
      "hotkeys bypass InputEventBus")
check("BACK-12 unified input bus has gamepad production callers",
      "if (pressedOnce(3)) InputEventBus.trigger('scan');" in source,
      "gamepad bypasses InputEventBus")
check("BACK-13 adaptive update scheduler drives runtime channels",
      "UpdateBudgetScheduler.shouldRun('proximity'" in source and
      "UpdateBudgetScheduler.shouldRun('telemetry'" in source and
      "DynamicLODManager" not in source,
      "update budget is disconnected or stale fake LOD claim remains")
check("BACK-18 world event bus has publisher and subscriber",
      "WorldEvents.emit('world:entered'" in source and "WorldEvents.on('world:entered'" in source,
      "world event bus is ceremonial")
check("BACK-19 critical asset warmup is called",
      "AssetPreloadQueue.warmCriticalAssets();" in source,
      "preload queue has no production caller")
check("BACK-20 state snapshot has save, restore, apply, and autosave paths",
      "StateSnapshotEngine.initAutosave();" in source and
      "StateSnapshotEngine.applyPending();" in source and
      "StateSnapshotEngine.save();" in source,
      "state snapshot is not a complete production path")
check("Persisted settings load on startup",
      "loadStoredSettings('settings_graphics'" in source and
      "loadStoredSettings('settings_audio'" in source and
      "loadStoredSettings('settings_controls'" in source and
      "applyStoredSettingsToRuntime();" in source,
      "settings are saved but not restored")
check("Gamepad toggles are edge-triggered",
      "const pressedOnce = index =>" in source and "this.previousButtons = gp.buttons.map" in source,
      "held gamepad buttons can repeatedly toggle actions")
check("Flashlight keyboard path is singular",
      source.count("toggleFlashlight();") == 1,
      f"expected one flashlight toggle caller, found {source.count('toggleFlashlight();')}")
check("WOW scanner-to-codex handoff is integrated",
      "lastScannedPOIKey = closestPOI.key;" in source and
      "openCodexModal(lastScannedPOIKey || null)" in source and
      "[M] OPEN TARGET IN CODEX" in source,
      "scanner lock cannot hand its target to the codex")

production_paths = {
    "BACK-01 LocalStorageEngine": "LocalStorageEngine.set('session_snapshot'",
    "BACK-02 ProceduralSoundscape": "ProceduralSoundscape.setBiomeSoundscape(worldKey)",
    "BACK-03 StaticObjectPool": "StaticObjectPool.getVec3(worldPos.x",
    "BACK-04 AssetDisposalManager": "AssetDisposalManager.disposeHierarchy(codex3DMesh)",
    "BACK-06 CoordinateTransformer": "CoordinateTransformer.worldToScreen(",
    "BACK-07 TelemetryLogger": "TelemetryLogger.update(renderer)",
    "BACK-08 AudioMixerBus": "AudioMixerBus.setVolumes(",
    "BACK-14 PerformanceMemoryMonitor": "PerformanceMemoryMonitor.getMemoryStats()",
    "BACK-15 GamepadAPISubsystem": "GamepadAPISubsystem.poll(delta)",
    "BACK-16 AutoQualityDegradation": "AutoQualityDegradation.checkPerformance(_currentFPS)",
    "BACK-17 UrlRouterEngine": "UrlRouterEngine.setHash(targetKey, currentViewMode)",
}
for label, caller in production_paths.items():
    check(f"{label} production caller", caller in source, f"missing production caller: {caller}")

check("Scanner no longer full-scans cross-world lore",
      "Object.keys(LORE_DATABASE).forEach" not in source[source.index("function scanForNearbyPOIs"):source.index("function playSonarPulseChirp")],
      "scanner still scans every world's lore on each pulse")
check("Session route records current location",
      "location: currentLocation" in source and "const targetLocation = snap.location" in source,
      "snapshot cannot distinguish base from a dialed foreign horizon")

print()
if failures:
    print(f"UPLIFT INTEGRATION RESULT: FAIL ({len(failures)} failures)")
    for failure in failures:
        print(f" - {failure}")
    sys.exit(1)

print("UPLIFT INTEGRATION RESULT: PASS")
sys.exit(0)
