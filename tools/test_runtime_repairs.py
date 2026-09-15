from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "index.html").read_text()
checks = [
    ("CORR-05 atoll geometry is defined before use",
     "const atollGeo = new THREE.CylinderGeometry" in source and
     source.index("const atollGeo") < source.index("new THREE.Mesh(atollGeo, atollMat)")),
    ("CORR-06 view mode is declared and updated",
     "let currentViewMode = 'walkthrough';" in source and "currentViewMode = viewName;" in source),
    ("CORR-07 utility modals have a visible active state",
     "#settings-modal.active, #controls-modal.active" in source),
    ("CORR-08 flashlight has one keyboard toggle caller",
     source.count("toggleFlashlight();") == 1),
    ("Mobile header contains overflow in nav lane",
     ".nav-tabs::-webkit-scrollbar" in source and "overflow-x: auto;" in source),
    ("CORR-11 medium-width header uses contained scroll lane",
     "@media (max-width: 1280px)" in source and "flex: 1 1 auto;" in source),
    ("CORR-12 floating UI toggle sits below header controls",
     "#ui-toggle-btn {" in source and "top: 68px;" in source),
    ("BACK-08 mixer initializes from the live audio context",
     "AudioMixerBus.init(audioCtx);" in source and "AudioMixerBus.setVolumes(userAudioSettings.masterVol" in source),
    ("BACK-08 ambience and SFX route through mixer buses",
     "gainNode.connect(AudioMixerBus.ambienceGain || audioCtx.destination);" in source and
     "AudioMixerBus.sfxGain || audioCtx.destination" in source and
     "connect(audioCtx.destination)" not in source),
    ("CORR-14 dial and transit effects preserve the active FOV setting",
     source.count("const origFov = camera.fov || 65;") == 2 and "const origFov = 65;" not in source),
]

failures = []
for name, passed in checks:
    print(f"[{'PASS' if passed else 'FAIL'}] {name}")
    if not passed:
        failures.append(name)

if failures:
    print(f"RUNTIME REPAIR STATIC RESULT: FAIL ({len(failures)})")
    sys.exit(1)
print("RUNTIME REPAIR STATIC RESULT: PASS")
sys.exit(0)
