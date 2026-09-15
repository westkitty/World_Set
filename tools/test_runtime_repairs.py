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
