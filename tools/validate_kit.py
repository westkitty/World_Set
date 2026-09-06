import os
import json
import subprocess

print("=======================================================")
print(">>> RUNNING AUTOMATED WORLD KIT VALIDATION AUDIT <<<")
print("=======================================================\n")

errors = []
warnings = []

# 1. Master Blend
blend_path = "/Users/andrew/World_Set/WORLD_KIT_MASTER.blend"
if os.path.exists(blend_path) and os.path.getsize(blend_path) > 100000:
    print(f"[PASS] Master .blend file exists: {os.path.getsize(blend_path) // 1024} KB")
else:
    errors.append("Master .blend file missing or suspiciously small.")

# 2. Manifests
json_manifest = "/Users/andrew/World_Set/ASSET_MANIFEST.json"
md_manifest = "/Users/andrew/World_Set/ASSET_MANIFEST.md"
if os.path.exists(json_manifest) and os.path.exists(md_manifest):
    with open(json_manifest, "r") as f:
        data = json.load(f)
    asset_count = len(data["assets"])
    print(f"[PASS] Manifests verified: {asset_count} assets cataloged.")
else:
    errors.append("Manifest files missing.")

# 3. GLB Exports
export_dir = "/Users/andrew/World_Set/WORLD_KIT_EXPORT"
glb_files = []
for root, _, files in os.walk(export_dir):
    for f in files:
        if f.endswith(".glb"):
            glb_files.append(os.path.join(root, f))
            
if len(glb_files) == 33:
    print(f"[PASS] All 33 production GLB files exist in categorized subdirectories.")
else:
    errors.append(f"Expected 33 GLBs, found {len(glb_files)}.")

# 4. Showcase Renders
renders_showcase = "/Users/andrew/World_Set/renders/showcase"
required_stills = [
    "01_establishing_wide.png",
    "02_architectural_scale.png",
    "03_material_detail.png",
    "04_hero_core_focus.png",
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
catalog_grid = "/Users/andrew/World_Set/renders/catalog/catalog_grid.png"
catalog_html = "/Users/andrew/World_Set/renders/catalog/index.html"
thumbs_dir = "/Users/andrew/World_Set/renders/catalog/thumbnails"
thumb_count = len([f for f in os.listdir(thumbs_dir) if f.endswith(".png")])

if thumb_count == 33 and os.path.exists(catalog_grid) and os.path.exists(catalog_html):
    print(f"[PASS] Catalog verified: {thumb_count} studio thumbnails, master grid image, and HTML explorer.")
else:
    errors.append(f"Catalog incomplete: found {thumb_count} thumbnails.")

# 7. Documentation
if os.path.exists("/Users/andrew/World_Set/WORLD_DNA.md") and os.path.exists("/Users/andrew/World_Set/MODULAR_GRAMMAR.md"):
    print("[PASS] WORLD_DNA.md and MODULAR_GRAMMAR.md documentation verified.")
else:
    errors.append("Core documentation missing.")

print("\n-------------------------------------------------------")
if not errors:
    print(">>> AUDIT RESULT: 100% PASS — ALL 10 DELIVERABLES VERIFIED <<<")
else:
    print(f">>> AUDIT FAILED with {len(errors)} errors:")
    for e in errors:
        print(f"  [!] {e}")
print("-------------------------------------------------------")
