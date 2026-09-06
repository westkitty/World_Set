import bpy
import math
import os
import json
from mathutils import Vector, Euler

BLEND_FILE = "/Users/andrew/World_Set/WORLD_KIT_MASTER.blend"
EXPORT_ROOT = "/Users/andrew/World_Set/WORLD_KIT_EXPORT"
SHOWCASE_DIR = "/Users/andrew/World_Set/renders/showcase"
THUMBS_DIR = "/Users/andrew/World_Set/renders/catalog/thumbnails"
WEB_DIR = "/Users/andrew/World_Set/web"

def load_master():
    bpy.ops.wm.open_mainfile(filepath=BLEND_FILE)
    print("Loaded master blend file.")

def instance_asset(source_name, inst_name, collection, loc=(0,0,0), rot=(0,0,0)):
    src = bpy.data.objects.get(source_name)
    if not src:
        raise ValueError(f"Asset '{source_name}' missing!")
    inst = bpy.data.objects.new(inst_name, src.data)
    inst.location = loc
    inst.rotation_euler = rot
    collection.objects.link(inst)
    return inst

def build_full_expanded_showcase():
    print("\n--- Constructing Unified Showcase: Sector 04 (Core) + Sector 05 (Stargate) ---")
    
    # Clean or create Scene_Showcase
    scene = bpy.data.scenes.get("Scene_Showcase")
    if not scene:
        scene = bpy.data.scenes.new("Scene_Showcase")
    bpy.context.window.scene = scene
    
    # Remove existing collection if present
    for c in scene.collection.children:
        scene.collection.children.unlink(c)
        
    col = bpy.data.collections.new("15_SHOWCASE")
    scene.collection.children.link(col)
    
    # =============================================================
    # SECTOR 04: GEOTHERMAL REACTOR VAULT (Y in [-8, 8], X in [-6, 6])
    # =============================================================
    # Floors: 3x4 tiles
    for gx in [-4, 0, 4]:
        for gy in [-6, -2, 2, 6]:
            if gx == 0 and gy in [-2, 2]:
                instance_asset("WK_FLOOR_GRATE_B_01", f"SC_Floor_Grate_{gx}_{gy}", col, (gx, gy, 0))
            else:
                instance_asset("WK_FLOOR_SLAB_A_01", f"SC_Floor_Slab_{gx}_{gy}", col, (gx, gy, 0))
                
    # Centerpiece Hero Geothermal Compression Reactor
    instance_asset("WK_HERO_CORE_A_01", "SC_Hero_Core", col, (0, 0, 0))
    
    # 6 Columns in Sector 04
    for cx in [-4, 4]:
        for cy in [-4, 0, 4]:
            instance_asset("WK_STRUCT_COLUMN_A_01", f"SC_Col_{cx}_{cy}", col, (cx, cy, 0))
            
    # Overhead Beams at Z=4.0
    for by in [-4, 0, 4]:
        instance_asset("WK_STRUCT_BEAM_A_01", f"SC_Beam_X_{by}", col, (0, by, 4), (0, 0, math.radians(90)))
    for bx in [-4, 4]:
        instance_asset("WK_STRUCT_BEAM_A_01", f"SC_Beam_Y1_{bx}", col, (bx, -2, 4))
        instance_asset("WK_STRUCT_BEAM_A_01", f"SC_Beam_Y2_{bx}", col, (bx, 2, 4))
        
    # Catwalk Gantry on Left (X = -4, Z = 2.0)
    instance_asset("WK_STRUCT_STAIRS_A_01", "SC_Stairs_L", col, (-4, -8, 0))
    for cy in [-4, 0, 4]:
        instance_asset("WK_FLOOR_CATWALK_C_01", f"SC_Catwalk_{cy}", col, (-4, cy, 2))
    instance_asset("WK_STRUCT_RAILING_A_01", "SC_Railing_01", col, (-3.05, -2, 2), (0, 0, math.radians(90)))
    instance_asset("WK_STRUCT_RAILING_A_01", "SC_Railing_02", col, (-3.05, 2, 2), (0, 0, math.radians(90)))
    instance_asset("WK_STRUCT_RAILING_2M_01", "SC_Railing_03", col, (-3.05, 5, 2), (0, 0, math.radians(90)))
    
    # Console & Maintenance Workstation
    instance_asset("WK_FURN_CONSOLE_A_01", "SC_Console", col, (-3.8, 1.5, 2), (0, 0, math.radians(90)))
    instance_asset("WK_FURN_BENCH_A_01", "SC_Bench", col, (3.8, -2.5, 0), (0, 0, math.radians(-90)))
    instance_asset("WK_PROP_CRATE_A_01", "SC_Crate_01", col, (4.2, 1.8, 0))
    instance_asset("WK_PROP_CRATE_A_01", "SC_Crate_02", col, (4.2, 1.8, 1.0), (0, 0, math.radians(12)))
    instance_asset("WK_PROP_CANISTER_A_01", "SC_Canister_01", col, (3.5, 3.8, 0))
    instance_asset("WK_PROP_CANISTER_A_01", "SC_Canister_02", col, (4.1, 4.0, 0))
    instance_asset("WK_PROP_JUNCTION_A_01", "SC_Junction_01", col, (5.85, -2.5, 1.8), (0, 0, math.radians(-90)))
    instance_asset("WK_PROP_EXTINGUISHER_01", "SC_Extinguisher", col, (-5.85, -5.0, 1.2), (0, 0, math.radians(90)))
    
    # South Wall (Y = -8)
    instance_asset("WK_WALL_SOLID_A_01", "SC_Wall_S_L", col, (-4, -8, 0), (0, 0, math.radians(180)))
    instance_asset("WK_WALL_DOORFRAME_A_01", "SC_Wall_S_Door", col, (0, -8, 0), (0, 0, math.radians(180)))
    instance_asset("WK_DOOR_BULKHEAD_A_01", "SC_Bulkhead_S", col, (0, -8, 0), (0, 0, math.radians(180)))
    instance_asset("WK_WALL_SOLID_A_01", "SC_Wall_S_R", col, (4, -8, 0), (0, 0, math.radians(180)))
    
    # West Walls (X = -6) & East Walls (X = +6)
    for wy in [-4, 0, 4]:
        instance_asset("WK_WALL_SOLID_A_01", f"SC_Wall_W_{wy}", col, (-6, wy, 0), (0, 0, math.radians(90)))
        instance_asset("WK_UTIL_PIPE_RUN_A_01", f"SC_Pipe_W_{wy}", col, (-5.85, wy, 3.2), (0, 0, math.radians(90)))
        instance_asset("WK_WALL_WINDOW_A_01", f"SC_Wall_E_{wy}", col, (6, wy, 0), (0, 0, math.radians(-90)))
        instance_asset("WK_WINDOW_PORTAL_A_01", f"SC_Portal_E_{wy}", col, (6, wy, 2), (0, 0, math.radians(-90)))
        instance_asset("WK_UTIL_PIPE_RUN_A_01", f"SC_Pipe_E_{wy}", col, (5.85, wy, 3.2), (0, 0, math.radians(-90)))
        
    # Ceilings in Sector 04
    for gx in [-4, 0, 4]:
        for gy in [-6, -2, 2, 6]:
            instance_asset("WK_CEIL_GIRDER_B_01", f"SC_Ceil_{gx}_{gy}", col, (gx, gy, 4))
            
    # Lights in Sector 04
    for cy in [-4, 4]:
        instance_asset("WK_LIGHT_TROFFER_A_01", f"SC_Troffer_{cy}", col, (0, cy, 4))
        
    # =============================================================
    # AIRLOCK CONNECTOR CORRIDOR (Y in [8, 12])
    # =============================================================
    # Wall dividing Sector 04 and 05 (Y = 8)
    instance_asset("WK_WALL_PANEL_B_01", "SC_Wall_N_L", col, (-4, 8, 0))
    instance_asset("WK_WALL_DOORFRAME_A_01", "SC_Wall_N_Door", col, (0, 8, 0))
    instance_asset("WK_DOOR_BULKHEAD_A_01", "SC_Bulkhead_N", col, (0, 8, 0))
    instance_asset("WK_WALL_PANEL_B_01", "SC_Wall_N_R", col, (4, 8, 0))
    instance_asset("WK_SIGN_SECTOR_A_01", "SC_Sign_Sector_N", col, (0, 7.85, 3.2))
    
    # Connecting Corridor (Y in [8, 12])
    instance_asset("WK_FLOOR_SLAB_A_01", "SC_Air_Fl_01", col, (0, 10, 0))
    instance_asset("WK_WALL_SOLID_A_01", "SC_Air_Wall_W", col, (-2, 10, 0), (0, 0, math.radians(90)))
    instance_asset("WK_WALL_SOLID_A_01", "SC_Air_Wall_E", col, (2, 10, 0), (0, 0, math.radians(-90)))
    instance_asset("WK_CEIL_COFFER_A_01", "SC_Air_Ceil", col, (0, 10, 4))
    instance_asset("WK_WALL_DOORFRAME_A_01", "SC_Air_Door_N", col, (0, 12, 0))
    instance_asset("WK_DOOR_BULKHEAD_A_01", "SC_Air_Bulk_N", col, (0, 12, 0))
    instance_asset("WK_SIGN_SECTOR_A_01", "SC_Air_Sign_N", col, (0, 11.85, 3.2))

    # =============================================================
    # SECTOR 05: THE GREAT PORTAL HALL (X in [-8, 8], Y in [12, 36], Z=8m)
    # =============================================================
    # 4x6 grid of floor tiles: X in [-6, -2, 2, 6], Y in [14, 18, 22, 26, 30, 34]
    for gx in [-6, -2, 2, 6]:
        for gy in [14, 18, 22, 26, 30, 34]:
            if gx in [-2, 2] and gy in [14, 18, 22, 26]:
                instance_asset("WK_FLOOR_GRATE_B_01", f"SC_S5_Grate_{gx}_{gy}", col, (gx, gy, 0))
            else:
                instance_asset("WK_FLOOR_SLAB_A_01", f"SC_S5_Slab_{gx}_{gy}", col, (gx, gy, 0))
                
    # Central Approach Runway (Leading up to Stargate at Y=32)
    for ry in [14, 18, 22, 26]:
        instance_asset("WK_FLOOR_CATWALK_C_01", f"SC_S5_Runway_{ry}", col, (0, ry, 0.05))
        instance_asset("WK_STRUCT_RAILING_A_01", f"SC_S5_RunRail_L_{ry}", col, (-1.05, ry, 0.05), (0, 0, math.radians(90)))
        instance_asset("WK_STRUCT_RAILING_A_01", f"SC_S5_RunRail_R_{ry}", col, (1.05, ry, 0.05), (0, 0, math.radians(90)))

    # COLOSSAL STARGATE PORTAL REACTOR
    instance_asset("WK_HERO_PORTAL_RING_A_01", "SC_Stargate_Portal", col, (0, 32.0, 0))
    
    # 8 Double-Height Structural Columns (X = ±8)
    for cx in [-8, 8]:
        for cy in [12, 20, 28, 36]:
            instance_asset("WK_STRUCT_COLUMN_A_01", f"SC_S5_Col_{cx}_{cy}_L0", col, (cx, cy, 0))
            instance_asset("WK_STRUCT_COLUMN_A_01", f"SC_S5_Col_{cx}_{cy}_L1", col, (cx, cy, 4))
            
    # Overhead Heavy Transverse I-Beams at Z=4.0 and Z=8.0
    for by in [12, 20, 28, 36]:
        instance_asset("WK_STRUCT_BEAM_A_01", f"SC_S5_Beam_M_{by}_L0", col, (0, by, 4), (0, 0, math.radians(90)))
        instance_asset("WK_STRUCT_BEAM_A_01", f"SC_S5_Beam_M_{by}_L1", col, (0, by, 8), (0, 0, math.radians(90)))
        
    for cx in [-8, 8]:
        for by in [16, 24, 32]:
            instance_asset("WK_STRUCT_BEAM_A_01", f"SC_S5_Beam_Y_{cx}_{by}", col, (cx, by, 8))

    # Mezzanine Observation Gantry on West Wall (Z=4.0)
    instance_asset("WK_STRUCT_STAIRS_A_01", "SC_S5_Stairs_W1", col, (-7.0, 14.0, 0))
    instance_asset("WK_STRUCT_STAIRS_A_01", "SC_S5_Stairs_W2", col, (-7.0, 18.0, 2.0))
    for cy in [22, 26, 30, 34]:
        instance_asset("WK_FLOOR_CATWALK_C_01", f"SC_S5_Catwalk_{cy}", col, (-7.0, cy, 4.0))
        instance_asset("WK_STRUCT_RAILING_A_01", f"SC_S5_CatRail_{cy}", col, (-6.05, cy, 4.0), (0, 0, math.radians(90)))
    instance_asset("WK_FURN_CONSOLE_A_01", "SC_S5_Dialing_Console", col, (-6.8, 28.0, 4.0), (0, 0, math.radians(90)))
    
    # North Far Wall behind Stargate (Y = 36)
    for wx in [-6, -2, 2, 6]:
        instance_asset("WK_WALL_PANEL_B_01", f"SC_S5_Wall_N_{wx}_L0", col, (wx, 36, 0), (0, 0, math.radians(180)))
        instance_asset("WK_WALL_PANEL_B_01", f"SC_S5_Wall_N_{wx}_L1", col, (wx, 36, 4), (0, 0, math.radians(180)))
        
    # West Walls (X = -8)
    for wy in [16, 24, 32]:
        instance_asset("WK_WALL_SOLID_A_01", f"SC_S5_Wall_W_{wy}_L0", col, (-8, wy, 0), (0, 0, math.radians(90)))
        instance_asset("WK_WALL_WINDOW_A_01", f"SC_S5_Wall_W_{wy}_L1", col, (-8, wy, 4), (0, 0, math.radians(90)))
        instance_asset("WK_WINDOW_PORTAL_A_01", f"SC_S5_Portal_W_{wy}", col, (-8, wy, 6), (0, 0, math.radians(90)))
        
    # East Walls (X = +8)
    for wy in [16, 24, 32]:
        instance_asset("WK_WALL_SOLID_A_01", f"SC_S5_Wall_E_{wy}_L0", col, (8, wy, 0), (0, 0, math.radians(-90)))
        instance_asset("WK_WALL_SOLID_A_01", f"SC_S5_Wall_E_{wy}_L1", col, (8, wy, 4), (0, 0, math.radians(-90)))
        instance_asset("WK_UTIL_PIPE_RUN_A_01", f"SC_S5_Pipe_E_{wy}", col, (7.85, wy, 3.2), (0, 0, math.radians(-90)))

    # Ceilings at Z=8.0
    for gx in [-6, -2, 2, 6]:
        for gy in [14, 18, 22, 26, 30, 34]:
            instance_asset("WK_CEIL_GIRDER_B_01", f"SC_S5_Ceil_{gx}_{gy}", col, (gx, gy, 8))

    # -------------------------------------------------------------
    # CINEMATIC LIGHTING
    # -------------------------------------------------------------
    # Sector 04 Core Light
    c_light = bpy.data.lights.new("SC_Light_CoreGlow", "POINT")
    c_light.energy = 5000
    c_light.color = (0.1, 0.9, 1.0)
    c_obj = bpy.data.objects.new("SC_Light_CoreGlow_Obj", c_light)
    c_obj.location = (0, 0, 2.0)
    col.objects.link(c_obj)
    
    # Sector 05 Stargate Quantum Event Horizon Light
    portal_light = bpy.data.lights.new("SC_Light_Portal_Vortex", "POINT")
    portal_light.energy = 9000
    portal_light.color = (0.05, 0.88, 1.0)
    portal_light.shadow_soft_size = 1.5
    portal_obj = bpy.data.objects.new("SC_Light_Portal_Vortex_Obj", portal_light)
    portal_obj.location = (0, 32.0, 3.8)
    col.objects.link(portal_obj)
    
    # Chevron Amber Light
    chev_light = bpy.data.lights.new("SC_Light_Chevron", "POINT")
    chev_light.energy = 2500
    chev_light.color = (1.0, 0.65, 0.05)
    chev_obj = bpy.data.objects.new("SC_Light_Chevron_Obj", chev_light)
    chev_obj.location = (0, 31.8, 7.2)
    col.objects.link(chev_obj)
    
    # Portal Hall Overhead Worklights
    for i, ly in enumerate([18, 26]):
        area_light = bpy.data.lights.new(f"SC_S5_Overhead_{i}", "AREA")
        area_light.energy = 4500
        area_light.color = (0.95, 0.98, 1.0)
        area_light.size = 3.0
        area_light.size_y = 1.0
        area_obj = bpy.data.objects.new(f"SC_S5_Overhead_{i}_Obj", area_light)
        area_obj.location = (0, ly, 7.8)
        col.objects.link(area_obj)

    # World background
    world = scene.world if scene.world else bpy.data.worlds.new("ShowcaseWorld")
    scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs["Color"].default_value = (0.02, 0.035, 0.05, 1.0)
        bg_node.inputs["Strength"].default_value = 0.35

    print(f"Total objects in expanded showcase collection: {len(col.objects)}")
    return scene, col

def setup_cameras(scene, col):
    # Stargate Camera
    cam_data = bpy.data.cameras.new("Cam_StargatePortal")
    cam_data.lens = 22
    cam_obj = bpy.data.objects.new("Cam_StargatePortal_Obj", cam_data)
    cam_obj.location = (0.0, 18.5, 2.2)
    cam_obj.rotation_euler = (math.radians(82), 0, math.radians(180))
    col.objects.link(cam_obj)
    return cam_obj

def render_stargate_still(scene, cam_obj):
    print("\n--- Rendering High-Resolution Stargate Still (Cycles) ---")
    scene.camera = cam_obj
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 32
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    out_path = os.path.join(SHOWCASE_DIR, "05_stargate_portal_chamber.png")
    scene.render.filepath = out_path
    print(f"Rendering 05_stargate_portal_chamber.png...")
    bpy.ops.render.render(write_still=True)
    print(f"  [✓] Rendered: {out_path}")

def render_portal_thumbnail():
    print("\n--- Rendering WK_HERO_PORTAL_RING_A_01 Thumbnail ---")
    scene = bpy.data.scenes.new("Scene_Thumbnails_Portal")
    bpy.context.window.scene = scene
    col = bpy.data.collections.new("THUMBNAIL_STUDIO_PORTAL")
    scene.collection.children.link(col)
    
    cam_data = bpy.data.cameras.new("ThumbCam_P")
    cam_data.lens = 45
    cam_obj = bpy.data.objects.new("ThumbCam_P_Obj", cam_data)
    col.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # 3-Point Light
    k = bpy.data.lights.new("ThumbKey", "POINT")
    k.energy = 1000
    ko = bpy.data.objects.new("ThumbKeyObj", k)
    ko.location = (4.0, -5.0, 5.0)
    col.objects.link(ko)
    
    f = bpy.data.lights.new("ThumbFill", "POINT")
    f.energy = 500
    fo = bpy.data.objects.new("ThumbFillObj", f)
    fo.location = (-5.0, -4.0, 3.0)
    col.objects.link(fo)
    
    src = bpy.data.objects.get("WK_HERO_PORTAL_RING_A_01")
    inst = bpy.data.objects.new("StudioInst_Portal", src.data)
    col.objects.link(inst)
    
    cam_obj.location = (6.5, -6.5, 4.5)
    direction = Vector((0, 0, 3.2)) - cam_obj.location
    cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 24
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    thumb_path = os.path.join(THUMBS_DIR, "WK_HERO_PORTAL_RING_A_01.png")
    scene.render.filepath = thumb_path
    bpy.ops.render.render(write_still=True)
    print(f"  [✓] Thumbnail saved: {thumb_path}")

def export_portal_glb():
    print("\n--- Exporting WK_HERO_PORTAL_RING_A_01.glb ---")
    master_scene = bpy.data.scenes["Scene"]
    bpy.context.window.scene = master_scene
    
    for o in bpy.data.objects:
        o.select_set(False)
    obj = bpy.data.objects.get("WK_HERO_PORTAL_RING_A_01")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    out_dir = os.path.join(EXPORT_ROOT, "hero")
    os.makedirs(out_dir, exist_ok=True)
    glb_path = os.path.join(out_dir, "WK_HERO_PORTAL_RING_A_01.glb")
    
    bpy.ops.export_scene.gltf(
        filepath=glb_path,
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_materials="EXPORT"
    )
    print(f"  [✓] Exported: {glb_path} ({os.path.getsize(glb_path) // 1024} KB)")

def reexport_showcase_glb():
    print("\n--- Re-Exporting Full Expanded Facility (web/showcase.glb) ---")
    scene = bpy.data.scenes["Scene_Showcase"]
    bpy.context.window.scene = scene
    
    out_path = os.path.join(WEB_DIR, "showcase.glb")
    bpy.ops.export_scene.gltf(
        filepath=out_path,
        export_format="GLB",
        export_apply=True
    )
    print(f"  [✓] Exported expanded showcase: {out_path} ({os.path.getsize(out_path) // 1024} KB)")

def update_manifests():
    print("\n--- Updating Asset Manifests (34 Total Assets) ---")
    json_path = "/Users/andrew/World_Set/ASSET_MANIFEST.json"
    with open(json_path, "r") as f:
        data = json.load(f)
        
    obj = bpy.data.objects.get("WK_HERO_PORTAL_RING_A_01")
    dim = obj.dimensions
    new_entry = {
        "name": "WK_HERO_PORTAL_RING_A_01",
        "category": "hero",
        "filename": "WK_HERO_PORTAL_RING_A_01.glb",
        "rel_path": "WORLD_KIT_EXPORT/hero/WK_HERO_PORTAL_RING_A_01.glb",
        "dimensions_m": [round(dim.x, 3), round(dim.y, 3), round(dim.z, 3)],
        "vertices": len(obj.data.vertices),
        "polygons": len(obj.data.polygons),
        "materials": [m.name for m in obj.data.materials if m]
    }
    
    data["assets"] = [a for a in data["assets"] if a["name"] != "WK_HERO_PORTAL_RING_A_01"]
    data["assets"].append(new_entry)
    data["assets"].sort(key=lambda x: (x["category"], x["name"]))
    data["total_assets"] = len(data["assets"])
    
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
        
    md_path = "/Users/andrew/World_Set/ASSET_MANIFEST.md"
    with open(md_path, "w") as f:
        f.write("# WORLD KIT ASSET MANIFEST\n")
        f.write("## Site-44 Sub-Aquifer Geothermal Research Facility\n\n")
        f.write(f"**Total Reusable Assets:** {len(data['assets'])}  \n")
        f.write(f"**Format:** GLTF/GLB 2.0 (PBR Materials Embedded)  \n")
        f.write(f"**Master Source:** `WORLD_KIT_MASTER.blend`  \n\n")
        f.write("---\n\n")
        f.write("| Asset Identifier | Category | Dimensions (W×D×H) | Verts | Faces | Material Families | Export File |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for r in data["assets"]:
            dims = f"{r['dimensions_m'][0]}m × {r['dimensions_m'][1]}m × {r['dimensions_m'][2]}m"
            mats = ", ".join(r["materials"])
            f.write(f"| `{r['name']}` | `{r['category']}` | {dims} | {r['vertices']} | {r['polygons']} | {mats} | [`{r['filename']}`]({r['rel_path']}) |\n")
    print("  [✓] Updated ASSET_MANIFEST.json and ASSET_MANIFEST.md")

if __name__ == "__main__":
    load_master()
    scene, col = build_full_expanded_showcase()
    cam = setup_cameras(scene, col)
    
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)
    print("Saved updated master blend file.")
    
    export_portal_glb()
    render_portal_thumbnail()
    reexport_showcase_glb()
    update_manifests()
    render_stargate_still(scene, cam)
    
    print("\n=======================================================")
    print(">>> STARGATE PORTAL EXPANSION COMPLETE! <<<")
    print("=======================================================")
