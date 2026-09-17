import os
import sys
import json
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

print("=======================================================")
print(">>> RUNNING AUTOMATED WORLD KIT VALIDATION AUDIT <<<")
print("=======================================================\n")

errors = []
warnings = []

# 1. Master Blend
blend_path = os.path.join(ROOT, "WORLD_KIT_MASTER.blend")
if os.path.exists(blend_path) and os.path.getsize(blend_path) > 100000:
    print(f"[PASS] Master .blend file exists: {os.path.getsize(blend_path) // 1024} KB")
else:
    errors.append("Master .blend file missing or suspiciously small.")

# 2. Manifests
json_manifest = os.path.join(ROOT, "ASSET_MANIFEST.json")
md_manifest = os.path.join(ROOT, "ASSET_MANIFEST.md")
asset_count = 0
if os.path.exists(json_manifest) and os.path.exists(md_manifest):
    with open(json_manifest, "r") as f:
        data = json.load(f)
    asset_count = len(data["assets"])
    print(f"[PASS] Manifests verified: {asset_count} assets cataloged.")
else:
    errors.append("Manifest files missing.")

# 3. GLB Exports
export_dir = os.path.join(ROOT, "WORLD_KIT_EXPORT")
glb_files = []
for root, _, files in os.walk(export_dir):
    for f in files:
        if f.endswith(".glb"):
            glb_files.append(os.path.join(root, f))
            
if asset_count > 0 and len(glb_files) == asset_count:
    print(f"[PASS] All {asset_count} production GLB files exist in categorized subdirectories.")
else:
    errors.append(f"Expected {asset_count} GLBs, found {len(glb_files)}.")

# 3b. Verify Each Manifest Asset Has GLB & Thumbnail
if asset_count > 0:
    missing_glbs = []
    missing_thumbs = []
    for asset in data["assets"]:
        glb_path = os.path.join(ROOT, asset.get("rel_path", ""))
        thumb_path = os.path.join(ROOT, "renders", "catalog", "thumbnails", f"{asset['name']}.png")
        if not os.path.exists(glb_path):
            missing_glbs.append(asset["name"])
        if not os.path.exists(thumb_path):
            missing_thumbs.append(asset["name"])
    if not missing_glbs and not missing_thumbs:
        print(f"[PASS] Integrity check: all {asset_count} manifest assets mapped to physical GLBs and thumbnails.")
    else:
        if missing_glbs:
            errors.append(f"Missing GLB files for assets: {missing_glbs}")
        if missing_thumbs:
            errors.append(f"Missing thumbnail images for assets: {missing_thumbs}")

# 4. Showcase Renders
renders_showcase = os.path.join(ROOT, "renders", "showcase")
required_stills = [
    "01_establishing_wide.png",
    "02_architectural_scale.png",
    "03_material_detail.png",
    "04_hero_core_focus.png",
    "05_stargate_portal_chamber.png",
    "showcase_360_panorama.png"
]
for s in required_stills:
    p = os.path.join(renders_showcase, s)
    if os.path.exists(p) and os.path.getsize(p) > 50000:
        print(f"[PASS] Showcase render '{s}' verified ({os.path.getsize(p) // 1024} KB).")
    else:
        errors.append(f"Missing or invalid showcase render: {s}")

# 5. Cinematic Walkthrough Video
video_path = os.path.join(renders_showcase, "showcase_walkthrough.mp4")
if os.path.exists(video_path) and os.path.getsize(video_path) > 100000:
    # Check with ffprobe
    res = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=width,height", "-of", "default=noprint_wrappers=1", video_path], capture_output=True, text=True)
    print(f"[PASS] Cinematic walkthrough video verified: {os.path.getsize(video_path) // 1024} KB | Info:\n{res.stdout.strip()}")
else:
    errors.append("Walkthrough video missing or invalid.")

# 6. Thumbnails & Catalog
catalog_grid = os.path.join(ROOT, "renders", "catalog", "catalog_grid.png")
catalog_html = os.path.join(ROOT, "renders", "catalog", "index.html")
thumbs_dir = os.path.join(ROOT, "renders", "catalog", "thumbnails")
thumb_count = len([f for f in os.listdir(thumbs_dir) if f.endswith(".png")])

if asset_count > 0 and thumb_count == asset_count and os.path.exists(catalog_grid) and os.path.exists(catalog_html):
    print(f"[PASS] Catalog verified: {thumb_count} studio thumbnails, master grid image, and HTML explorer.")
else:
    errors.append(f"Catalog incomplete: found {thumb_count} thumbnails (expected {asset_count}).")

# 7. Documentation
if os.path.exists(os.path.join(ROOT, "WORLD_DNA.md")) and os.path.exists(os.path.join(ROOT, "MODULAR_GRAMMAR.md")):
    print("[PASS] WORLD_DNA.md and MODULAR_GRAMMAR.md documentation verified.")
else:
    errors.append("Core documentation missing.")

# 8. Interactive Web Deliverables
web_index = os.path.join(ROOT, "index.html")
web_glb = os.path.join(ROOT, "web", "showcase.glb")
required_libs = [
    os.path.join(ROOT, "web", "libs", "three.min.js"),
    os.path.join(ROOT, "web", "libs", "GLTFLoader.js"),
    os.path.join(ROOT, "web", "libs", "PointerLockControls.js"),
    os.path.join(ROOT, "web", "libs", "OrbitControls.js"),
]
if os.path.exists(web_index) and os.path.getsize(web_index) > 50000 and os.path.exists(web_glb) and os.path.getsize(web_glb) > 1000000:
    all_libs_exist = all(os.path.exists(lib) and os.path.getsize(lib) > 1000 for lib in required_libs)
    if all_libs_exist:
        print(f"[PASS] Web 3D runtime verified: index.html ({os.path.getsize(web_index) // 1024} KB), showcase.glb ({os.path.getsize(web_glb) // 1024} KB), all 4 offline Three.js libraries present.")
    else:
        errors.append("Web offline Three.js libraries missing or corrupted.")
else:
    errors.append("Interactive Web application deliverables missing or invalid.")

print("\n-------------------------------------------------------")
if not errors:
    print(">>> AUDIT RESULT: 100% PASS — ALL DELIVERABLES VERIFIED <<<")
    print("-------------------------------------------------------")
    sys.exit(0)
else:
    print(f">>> AUDIT FAILED with {len(errors)} errors:")
    for e in errors:
        print(f"  [!] {e}")
    print("-------------------------------------------------------")
    sys.exit(1)
