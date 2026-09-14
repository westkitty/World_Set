import os
import sys
import json
import re
import subprocess

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
manifest_path = "/Users/andrew/World_Set/ASSET_MANIFEST.json"
md_manifest_path = "/Users/andrew/World_Set/ASSET_MANIFEST.md"

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
    glb_path = os.path.join("/Users/andrew/World_Set", a.get("rel_path", ""))
    thumb_path = os.path.join("/Users/andrew/World_Set/renders/catalog/thumbnails", f"{a['name']}.png")
    check(f"GLB Exists: {a['name']}", os.path.exists(glb_path) and os.path.getsize(glb_path) > 100, f"File missing: {glb_path}")
    check(f"Thumbnail Exists: {a['name']}", os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 100, f"File missing: {thumb_path}")

# INV-02: Category Dictionary Consistency
with open("/Users/andrew/World_Set/tools/build_showcase_and_export.py", "r") as f:
    showcase_script = f.read()
cat_match = re.search(r"ASSET_CATEGORIES = \{(.*?)\}", showcase_script, re.DOTALL)
if cat_match:
    cat_entries = set(re.findall(r"\"(WK_[A-Z0-9_]+)\"", cat_match.group(1)))
    check("ASSET_CATEGORIES Sync", asset_names == cat_entries, f"Missing in ASSET_CATEGORIES: {asset_names - cat_entries}")
else:
    failures.append("ASSET_CATEGORIES dictionary not found in build_showcase_and_export.py")

# INV-03: Zero Stale Asset Count Claims
with open("/Users/andrew/World_Set/index.html", "r") as f:
    index_html = f.read()
check("index.html 34 GLBs claim", "34 individual production .glb models" in index_html, "Stale claim in index.html")
check("index.html 34 thumbnails claim", "34 studio thumbnails" in index_html, "Stale claim in index.html")
check("No stale 33 GLB claim in index.html", "33 individual production .glb models" not in index_html, "Stale 33 GLB claim found")
check("No stale 33 studio claim in index.html", "33 studio thumbnails" not in index_html, "Stale 33 studio claim found")

with open("/Users/andrew/World_Set/renders/catalog/index.html", "r") as f:
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
val_res = subprocess.run(["python3", "/Users/andrew/World_Set/tools/validate_kit.py"], capture_output=True, text=True)
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
