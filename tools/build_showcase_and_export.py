import bpy
import math
import os
import json
import subprocess
from mathutils import Vector, Euler

BLEND_FILE = "/Users/andrew/World_Set/WORLD_KIT_MASTER.blend"
EXPORT_ROOT = "/Users/andrew/World_Set/WORLD_KIT_EXPORT"
RENDERS_ROOT = "/Users/andrew/World_Set/renders"
SHOWCASE_DIR = os.path.join(RENDERS_ROOT, "showcase")
FRAMES_DIR = os.path.join(SHOWCASE_DIR, "frames")
CATALOG_DIR = os.path.join(RENDERS_ROOT, "catalog")
THUMBS_DIR = os.path.join(CATALOG_DIR, "thumbnails")

os.makedirs(SHOWCASE_DIR, exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(THUMBS_DIR, exist_ok=True)

# Categorization mapping
ASSET_CATEGORIES = {
    # Walls
    "WK_WALL_SOLID_A_01": "walls",
    "WK_WALL_PANEL_B_01": "walls",
    "WK_WALL_CORNER_IN_A_01": "walls",
    "WK_WALL_CORNER_OUT_A_01": "walls",
    "WK_WALL_DOORFRAME_A_01": "walls",
    "WK_WALL_WINDOW_A_01": "walls",
    # Floors
    "WK_FLOOR_SLAB_A_01": "floors",
    "WK_FLOOR_GRATE_B_01": "floors",
    "WK_FLOOR_CATWALK_C_01": "floors",
    "WK_FLOOR_TRIM_A_01": "floors",
    # Architecture
    "WK_CEIL_COFFER_A_01": "architecture",
    "WK_CEIL_GIRDER_B_01": "architecture",
    # Doors & Windows
    "WK_DOOR_BULKHEAD_A_01": "doors_windows",
    "WK_DOOR_SLAB_A_01": "doors_windows",
    "WK_WINDOW_PORTAL_A_01": "doors_windows",
    # Structural
    "WK_STRUCT_COLUMN_A_01": "structural",
    "WK_STRUCT_BEAM_A_01": "structural",
    "WK_STRUCT_STAIRS_A_01": "structural",
    "WK_STRUCT_RAILING_A_01": "structural",
    "WK_STRUCT_RAILING_2M_01": "structural",
    # Furniture
    "WK_FURN_CONSOLE_A_01": "furniture",
    "WK_FURN_BENCH_A_01": "furniture",
    # Props
    "WK_PROP_CRATE_A_01": "props",
    "WK_PROP_CANISTER_A_01": "props",
    "WK_PROP_JUNCTION_A_01": "props",
    "WK_PROP_EXTINGUISHER_01": "props",
    # Lights
    "WK_LIGHT_TROFFER_A_01": "lights",
    "WK_LIGHT_CAGE_A_01": "lights",
    "WK_LIGHT_STROBE_A_01": "lights",
    # Signage
    "WK_SIGN_SECTOR_A_01": "signage",
    "WK_SIGN_HAZARD_A_01": "signage",
    # Utilities
    "WK_UTIL_PIPE_RUN_A_01": "utilities",
    # Hero
    "WK_HERO_CORE_A_01": "hero",
}

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

# -------------------------------------------------------------
# 1. BUILD SHOWCASE SCENE
# -------------------------------------------------------------
def build_showcase_environment():
    print("\n--- Assembling Showcase Environment (Strict Kit Instances) ---")
    scene = bpy.data.scenes.new("Scene_Showcase")
    bpy.context.window.scene = scene
    col = bpy.data.collections.new("15_SHOWCASE")
    scene.collection.children.link(col)
    
    # Floor: 12m x 16m (3x4 tiles)
    for gx in [-4, 0, 4]:
        for gy in [-6, -2, 2, 6]:
            if gx == 0 and gy in [-2, 2]:
                instance_asset("WK_FLOOR_GRATE_B_01", f"SC_Floor_Grate_{gx}_{gy}", col, (gx, gy, 0))
            else:
                instance_asset("WK_FLOOR_SLAB_A_01", f"SC_Floor_Slab_{gx}_{gy}", col, (gx, gy, 0))
                
    # Centerpiece Hero Core
    instance_asset("WK_HERO_CORE_A_01", "SC_Hero_Core", col, (0, 0, 0))
    
    # 6 Massive Columns
    for cx in [-4, 4]:
        for cy in [-4, 0, 4]:
            instance_asset("WK_STRUCT_COLUMN_A_01", f"SC_Col_{cx}_{cy}", col, (cx, cy, 0))
            
    # Overhead Structural I-Beams at Z=4.0
    for by in [-4, 0, 4]:
        instance_asset("WK_STRUCT_BEAM_A_01", f"SC_Beam_X_{by}", col, (0, by, 4), (0, 0, math.radians(90)))
    for bx in [-4, 4]:
        instance_asset("WK_STRUCT_BEAM_A_01", f"SC_Beam_Y1_{bx}", col, (bx, -2, 4))
        instance_asset("WK_STRUCT_BEAM_A_01", f"SC_Beam_Y2_{bx}", col, (bx, 2, 4))
        
    # Catwalk Gantry on Left (X = -4, Z = 2.0m)
    instance_asset("WK_STRUCT_STAIRS_A_01", "SC_Stairs_L", col, (-4, -8, 0))
    for cy in [-4, 0, 4]:
        instance_asset("WK_FLOOR_CATWALK_C_01", f"SC_Catwalk_{cy}", col, (-4, cy, 2))
    # Railings along inner catwalk edge (X = -3.05)
    instance_asset("WK_STRUCT_RAILING_A_01", "SC_Railing_01", col, (-3.05, -2, 2), (0, 0, math.radians(90)))
    instance_asset("WK_STRUCT_RAILING_A_01", "SC_Railing_02", col, (-3.05, 2, 2), (0, 0, math.radians(90)))
    instance_asset("WK_STRUCT_RAILING_2M_01", "SC_Railing_03", col, (-3.05, 5, 2), (0, 0, math.radians(90)))
    
    # Monitoring Console on Catwalk
    instance_asset("WK_FURN_CONSOLE_A_01", "SC_Console", col, (-3.8, 1.5, 2), (0, 0, math.radians(90)))
    
    # Maintenance Workshop on Right Floor (X = 4)
    instance_asset("WK_FURN_BENCH_A_01", "SC_Bench", col, (3.8, -2.5, 0), (0, 0, math.radians(-90)))
    instance_asset("WK_PROP_CRATE_A_01", "SC_Crate_01", col, (4.2, 1.8, 0))
    instance_asset("WK_PROP_CRATE_A_01", "SC_Crate_02", col, (4.2, 1.8, 1.0), (0, 0, math.radians(12)))
    instance_asset("WK_PROP_CANISTER_A_01", "SC_Canister_01", col, (3.5, 3.8, 0))
    instance_asset("WK_PROP_CANISTER_A_01", "SC_Canister_02", col, (4.1, 4.0, 0))
    instance_asset("WK_PROP_JUNCTION_A_01", "SC_Junction_01", col, (5.85, -2.5, 1.8), (0, 0, math.radians(-90)))
    instance_asset("WK_PROP_EXTINGUISHER_01", "SC_Extinguisher", col, (-5.85, -5.0, 1.2), (0, 0, math.radians(90)))
    
    # North Perimeter Walls (Y = +8)
    instance_asset("WK_WALL_PANEL_B_01", "SC_Wall_N_L", col, (-4, 8, 0))
    instance_asset("WK_WALL_DOORFRAME_A_01", "SC_Wall_N_Door", col, (0, 8, 0))
    instance_asset("WK_DOOR_BULKHEAD_A_01", "SC_Bulkhead_N", col, (0, 8, 0))
    instance_asset("WK_DOOR_SLAB_A_01", "SC_DoorSlab_N", col, (0, 8, 0))
    instance_asset("WK_WALL_PANEL_B_01", "SC_Wall_N_R", col, (4, 8, 0))
    instance_asset("WK_SIGN_SECTOR_A_01", "SC_Sign_Sector_N", col, (0, 7.85, 3.2))
    
    # South Perimeter Walls (Y = -8)
    instance_asset("WK_WALL_SOLID_A_01", "SC_Wall_S_L", col, (-4, -8, 0), (0, 0, math.radians(180)))
    instance_asset("WK_WALL_DOORFRAME_A_01", "SC_Wall_S_Door", col, (0, -8, 0), (0, 0, math.radians(180)))
    instance_asset("WK_DOOR_BULKHEAD_A_01", "SC_Bulkhead_S", col, (0, -8, 0), (0, 0, math.radians(180)))
    instance_asset("WK_WALL_SOLID_A_01", "SC_Wall_S_R", col, (4, -8, 0), (0, 0, math.radians(180)))
    
    # West Walls (X = -6)
    for wy in [-4, 0, 4]:
        instance_asset("WK_WALL_SOLID_A_01", f"SC_Wall_W_{wy}", col, (-6, wy, 0), (0, 0, math.radians(90)))
        # Continuous pipe run along West wall at Z=3.2
        instance_asset("WK_UTIL_PIPE_RUN_A_01", f"SC_Pipe_W_{wy}", col, (-5.85, wy, 3.2), (0, 0, math.radians(90)))
        
    # East Walls with Observation Portals (X = +6)
    for wy in [-4, 0, 4]:
        instance_asset("WK_WALL_WINDOW_A_01", f"SC_Wall_E_{wy}", col, (6, wy, 0), (0, 0, math.radians(-90)))
        instance_asset("WK_WINDOW_PORTAL_A_01", f"SC_Portal_E_{wy}", col, (6, wy, 2), (0, 0, math.radians(-90)))
        instance_asset("WK_UTIL_PIPE_RUN_A_01", f"SC_Pipe_E_{wy}", col, (5.85, wy, 3.2), (0, 0, math.radians(-90)))
        
    # Ceiling Bays at Z=4.0 & 8.0
    for gx in [-4, 0, 4]:
        for gy in [-6, -2, 2, 6]:
            instance_asset("WK_CEIL_GIRDER_B_01", f"SC_Ceil_{gx}_{gy}", col, (gx, gy, 4))
            
    # Overhead Fluorescent Luminaires
    for cy in [-4, 4]:
        instance_asset("WK_LIGHT_TROFFER_A_01", f"SC_Troffer_{cy}", col, (0, cy, 4))
        
    # Wall Cage Lamps & Strobes
    instance_asset("WK_LIGHT_CAGE_A_01", "SC_Cage_01", col, (3.85, -2.5, 2.2), (0, 0, math.radians(-90)))
    instance_asset("WK_LIGHT_CAGE_A_01", "SC_Cage_02", col, (-3.85, 3.5, 3.2), (0, 0, math.radians(90)))
    instance_asset("WK_LIGHT_STROBE_A_01", "SC_Strobe_01", col, (4.4, 0, 4.0))
    instance_asset("WK_LIGHT_STROBE_A_01", "SC_Strobe_02", col, (-4.4, 0, 4.0))

    # Floor cable raceway trims
    for wy in [-6, -2, 2, 6]:
        instance_asset("WK_FLOOR_TRIM_A_01", f"SC_Trim_W_{wy}", col, (-5.8, wy, 0), (0, 0, math.radians(90)))
        instance_asset("WK_FLOOR_TRIM_A_01", f"SC_Trim_E_{wy}", col, (5.8, wy, 0), (0, 0, math.radians(-90)))

    # ---------------------------------------------------------
    # CINEMATIC LIGHTING DESIGN
    # ---------------------------------------------------------
    # 1. Reactor Core Plasma Emission (Cyan Core Glow)
    core_light_data = bpy.data.lights.new("SC_Light_CoreGlow", "POINT")
    core_light_data.energy = 5000
    core_light_data.color = (0.1, 0.9, 1.0)
    core_light_data.shadow_soft_size = 0.8
    core_light_obj = bpy.data.objects.new("SC_Light_CoreGlow_Obj", core_light_data)
    core_light_obj.location = (0, 0, 2.0)
    col.objects.link(core_light_obj)
    
    # 2. Overhead Worklight Bays (Warm Tungsten Key Lights)
    for i, (lx, ly) in enumerate([(0, -4), (0, 4)]):
        overhead_data = bpy.data.lights.new(f"SC_Light_Overhead_{i}", "AREA")
        overhead_data.energy = 3500
        overhead_data.color = (1.0, 0.95, 0.88)
        overhead_data.size = 2.0
        overhead_data.size_y = 0.6
        overhead_obj = bpy.data.objects.new(f"SC_Light_Overhead_{i}_Obj", overhead_data)
        overhead_obj.location = (lx, ly, 3.8)
        col.objects.link(overhead_obj)
        
    # 3. Workstation Task Lamp (Warm Accent)
    desk_data = bpy.data.lights.new("SC_Light_Desk", "SPOT")
    desk_data.energy = 450
    desk_data.color = (1.0, 0.82, 0.60)
    desk_data.spot_size = math.radians(65)
    desk_data.spot_blend = 0.4
    desk_obj = bpy.data.objects.new("SC_Light_Desk_Obj", desk_data)
    desk_obj.location = (-3.8, 1.5, 3.2)
    desk_obj.rotation_euler = (0, math.radians(20), 0)
    col.objects.link(desk_obj)
    
    # 4. Workbench Task Lamp
    bench_data = bpy.data.lights.new("SC_Light_Bench", "SPOT")
    bench_data.energy = 450
    bench_data.color = (1.0, 0.88, 0.70)
    bench_data.spot_size = math.radians(60)
    bench_obj = bpy.data.objects.new("SC_Light_Bench_Obj", bench_data)
    bench_obj.location = (3.8, -2.5, 2.4)
    bench_obj.rotation_euler = (0, math.radians(-25), 0)
    col.objects.link(bench_obj)
    
    # 5. Ambient World Fill (Subdued Slate Cool Tone)
    world = scene.world if scene.world else bpy.data.worlds.new("ShowcaseWorld")
    scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs["Color"].default_value = (0.02, 0.035, 0.05, 1.0)
        bg_node.inputs["Strength"].default_value = 0.35

    print(f"Showcase assembled with {len(col.objects)} instances and lights.")
    return scene, col

# -------------------------------------------------------------
# 2. SETUP CAMERAS & RENDER SHOWCASE STILLS
# -------------------------------------------------------------
def setup_showcase_cameras(scene, col):
    cameras = {}
    
    def add_cam(name, loc, rot, lens=24, cam_type='PERSP', pano_type='EQUIRECTANGULAR'):
        cam_data = bpy.data.cameras.new(name)
        cam_data.type = cam_type
        if cam_type == 'PANO':
            cam_data.panorama_type = pano_type
        else:
            cam_data.lens = lens
        cam_obj = bpy.data.objects.new(name + "_Obj", cam_data)
        cam_obj.location = loc
        cam_obj.rotation_euler = rot
        col.objects.link(cam_obj)
        cameras[name] = cam_obj
        return cam_obj

    # 1. Establishing Wide (20mm, high vantage, sweeping view)
    add_cam("Cam_Establishing", 
            loc=(5.2, -6.8, 3.4), 
            rot=(math.radians(72), 0, math.radians(40)), 
            lens=20)
            
    # 2. Architectural Scale (28mm, low-angle, monolithic columns & rafters)
    add_cam("Cam_Architectural", 
            loc=(-3.6, -6.2, 0.9), 
            rot=(math.radians(82), 0, math.radians(24)), 
            lens=28)
            
    # 3. Material Detail (50mm, focus on console telemetry, vice, concrete seams)
    add_cam("Cam_MaterialDetail", 
            loc=(-2.6, 1.1, 2.35), 
            rot=(math.radians(76), 0, math.radians(68)), 
            lens=50)
            
    # 4. Hero Core Focus (35mm, framing the geothermal compression reactor)
    add_cam("Cam_HeroCore", 
            loc=(0.0, -4.6, 1.6), 
            rot=(math.radians(80), 0, 0), 
            lens=35)
            
    # 5. 360-Degree Equirectangular Panorama
    add_cam("Cam_360_Pano", 
            loc=(-4.0, 0.0, 3.0), 
            rot=(math.radians(90), 0, math.radians(-90)), 
            cam_type='PANO')
            
    return cameras

def render_showcase_stills(scene, cameras):
    print("\n--- Rendering Production Showcase Stills (Cycles) ---")
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 40
    
    stills = [
        ("Cam_Establishing", "01_establishing_wide.png", 1920, 1080),
        ("Cam_Architectural", "02_architectural_scale.png", 1920, 1080),
        ("Cam_MaterialDetail", "03_material_detail.png", 1920, 1080),
        ("Cam_HeroCore", "04_hero_core_focus.png", 1920, 1080),
        ("Cam_360_Pano", "showcase_360_panorama.png", 2048, 1024),
    ]
    
    for cam_name, filename, rx, ry in stills:
        cam_obj = cameras[cam_name]
        scene.camera = cam_obj
        scene.render.resolution_x = rx
        scene.render.resolution_y = ry
        out_path = os.path.join(SHOWCASE_DIR, filename)
        scene.render.filepath = out_path
        print(f"Rendering {cam_name} -> {out_path} ({rx}x{ry})...")
        bpy.ops.render.render(write_still=True)
        print(f"  [✓] Finished: {filename}")

# -------------------------------------------------------------
# 3. ANIMATED CAMERA WALKTHROUGH & VIDEO ENCODING
# -------------------------------------------------------------
def render_walkthrough_video(scene, col):
    print("\n--- Rendering Cinematic Camera Walkthrough ---")
    cam_data = bpy.data.cameras.new("Cam_Walkthrough")
    cam_data.lens = 24
    cam_obj = bpy.data.objects.new("Cam_Walkthrough_Obj", cam_data)
    col.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # 60 frames path (2.5 seconds at 24fps)
    key_points = [
        # Frame 1: Entrance bulkhead door view
        (1,  (0.0, -7.2, 1.8), (math.radians(88), 0, 0)),
        # Frame 20: Moving forward and panning toward catwalk
        (20, (-1.5, -4.0, 1.9), (math.radians(85), 0, math.radians(25))),
        # Frame 40: Ascending alongside catwalk, framing console and hero core
        (40, (-3.2, -1.0, 2.4), (math.radians(78), 0, math.radians(50))),
        # Frame 60: Overlooking hero core and double-height observation hall
        (60, (-2.5, 1.8, 2.5), (math.radians(72), 0, math.radians(75))),
    ]
    
    for f, loc, rot in key_points:
        scene.frame_set(f)
        cam_obj.location = loc
        cam_obj.rotation_euler = rot
        cam_obj.keyframe_insert(data_path="location", frame=f)
        cam_obj.keyframe_insert(data_path="rotation_euler", frame=f)
        
    scene.frame_start = 1
    scene.frame_end = 60
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.cycles.samples = 10
    
    print("Rendering 60 animation frames...")
    for f in range(1, 61):
        scene.frame_set(f)
        frame_path = os.path.join(FRAMES_DIR, f"frame_{f:04d}.png")
        scene.render.filepath = frame_path
        bpy.ops.render.render(write_still=True)
        if f % 10 == 0:
            print(f"  Rendered frame {f}/60")
            
    # Compile video with ffmpeg
    mp4_path = os.path.join(SHOWCASE_DIR, "showcase_walkthrough.mp4")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-framerate", "24",
        "-i", os.path.join(FRAMES_DIR, "frame_%04d.png"),
        "-c:v", "libx264",
        "-profile:v", "high",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        mp4_path
    ]
    print("Compiling video with ffmpeg...")
    subprocess.run(ffmpeg_cmd, check=True)
    print(f"  [✓] Walkthrough video generated: {mp4_path}")

# -------------------------------------------------------------
# 4. EXPORT INDIVIDUAL PRODUCTION GLB ASSETS
# -------------------------------------------------------------
def export_glb_assets():
    print("\n--- Exporting Production GLB Assets by Category ---")
    master_scene = bpy.data.scenes["Scene"]
    bpy.context.window.scene = master_scene
    
    exported_records = []
    
    for asset_name, category in ASSET_CATEGORIES.items():
        obj = bpy.data.objects.get(asset_name)
        if not obj:
            print(f"Warning: Asset '{asset_name}' not found for export!")
            continue
            
        # Select only this object
        for o in bpy.data.objects:
            o.select_set(False)
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        
        target_dir = os.path.join(EXPORT_ROOT, category)
        os.makedirs(target_dir, exist_ok=True)
        glb_path = os.path.join(target_dir, f"{asset_name}.glb")
        
        bpy.ops.export_scene.gltf(
            filepath=glb_path,
            export_format="GLB",
            use_selection=True,
            export_apply=True,
            export_materials="EXPORT"
        )
        
        # Dimensions
        dim = obj.dimensions
        record = {
            "name": asset_name,
            "category": category,
            "filename": f"{asset_name}.glb",
            "rel_path": os.path.relpath(glb_path, "/Users/andrew/World_Set"),
            "dimensions_m": [round(dim.x, 3), round(dim.y, 3), round(dim.z, 3)],
            "vertices": len(obj.data.vertices),
            "polygons": len(obj.data.polygons),
            "materials": [m.name for m in obj.data.materials if m]
        }
        exported_records.append(record)
        print(f"  [✓] Exported: {category}/{asset_name}.glb ({os.path.getsize(glb_path) // 1024} KB)")
        
    return exported_records

# -------------------------------------------------------------
# 5. RENDER ASSET THUMBNAIL CATALOG
# -------------------------------------------------------------
def render_thumbnail_catalog():
    print("\n--- Rendering Asset Thumbnail Catalog ---")
    scene = bpy.data.scenes.new("Scene_Thumbnails")
    bpy.context.window.scene = scene
    col = bpy.data.collections.new("THUMBNAIL_STUDIO")
    scene.collection.children.link(col)
    
    # Camera
    cam_data = bpy.data.cameras.new("ThumbCam")
    cam_data.lens = 45
    cam_obj = bpy.data.objects.new("ThumbCamObj", cam_data)
    col.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # Studio 3-Point Lights
    # Key
    key_data = bpy.data.lights.new("ThumbKey", "POINT")
    key_data.energy = 800
    key_data.color = (1.0, 0.98, 0.95)
    key_obj = bpy.data.objects.new("ThumbKeyObj", key_data)
    key_obj.location = (2.5, -3.0, 2.8)
    col.objects.link(key_obj)
    
    # Fill
    fill_data = bpy.data.lights.new("ThumbFill", "POINT")
    fill_data.energy = 400
    fill_data.color = (0.7, 0.85, 1.0)
    fill_obj = bpy.data.objects.new("ThumbFillObj", fill_data)
    fill_obj.location = (-3.0, -2.0, 2.0)
    col.objects.link(fill_obj)
    
    # Rim
    rim_data = bpy.data.lights.new("ThumbRim", "POINT")
    rim_data.energy = 600
    rim_data.color = (1.0, 1.0, 1.0)
    rim_obj = bpy.data.objects.new("ThumbRimObj", rim_data)
    rim_obj.location = (0, 3.0, 3.5)
    col.objects.link(rim_obj)
    
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 24
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    
    # Background slate
    world = bpy.data.worlds.new("ThumbWorld")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.05, 0.06, 0.07, 1.0)
        bg.inputs["Strength"].default_value = 0.5
        
    for asset_name in ASSET_CATEGORIES.keys():
        src = bpy.data.objects.get(asset_name)
        if not src:
            continue
            
        # Instance object in studio
        inst = bpy.data.objects.new("StudioInst", src.data)
        col.objects.link(inst)
        
        # Frame camera based on object bounds
        dim = src.dimensions
        max_dim = max(dim.x, dim.y, dim.z, 0.5)
        dist = max_dim * 1.8
        center_z = dim.z * 0.45
        
        cam_obj.location = (dist * 0.7, -dist * 0.7, center_z + dist * 0.45)
        # Look at center
        direction = Vector((0, 0, center_z)) - cam_obj.location
        rot_quat = direction.to_track_quat('-Z', 'Y')
        cam_obj.rotation_euler = rot_quat.to_euler()
        
        thumb_path = os.path.join(THUMBS_DIR, f"{asset_name}.png")
        scene.render.filepath = thumb_path
        bpy.ops.render.render(write_still=True)
        print(f"  [✓] Thumbnail: {asset_name}.png")
        
        # Remove instance
        col.objects.unlink(inst)
        bpy.data.objects.remove(inst)

# -------------------------------------------------------------
# 6. ASSET MANIFEST GENERATION
# -------------------------------------------------------------
def generate_asset_manifest(records):
    print("\n--- Generating Asset Manifests ---")
    manifest_data = {
        "kit_name": "WORLD KIT — SITE-44 SUB-AQUIFER RESEARCH COMPLEX",
        "version": "1.0.0",
        "total_assets": len(records),
        "categories": list(set(r["category"] for r in records)),
        "author": "Antigravity Environment Systems",
        "spec_reference": "WORLD_DNA.md",
        "grammar_reference": "MODULAR_GRAMMAR.md",
        "assets": records
    }
    
    json_path = "/Users/andrew/World_Set/ASSET_MANIFEST.json"
    with open(json_path, "w") as f:
        json.dump(manifest_data, f, indent=2)
    print(f"Saved JSON manifest: {json_path}")
    
    # Markdown Manifest
    md_path = "/Users/andrew/World_Set/ASSET_MANIFEST.md"
    with open(md_path, "w") as f:
        f.write("# WORLD KIT ASSET MANIFEST\n")
        f.write("## Site-44 Sub-Aquifer Geothermal Research Facility\n\n")
        f.write(f"**Total Reusable Assets:** {len(records)}  \n")
        f.write(f"**Format:** GLTF/GLB 2.0 (PBR Materials Embedded)  \n")
        f.write(f"**Master Source:** `WORLD_KIT_MASTER.blend`  \n\n")
        f.write("---\n\n")
        f.write("| Asset Identifier | Category | Dimensions (W×D×H) | Verts | Faces | Material Families | Export File |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for r in records:
            dims = f"{r['dimensions_m'][0]}m × {r['dimensions_m'][1]}m × {r['dimensions_m'][2]}m"
            mats = ", ".join(r["materials"])
            f.write(f"| `{r['name']}` | `{r['category']}` | {dims} | {r['vertices']} | {r['polygons']} | {mats} | [`{r['filename']}`]({r['rel_path']}) |\n")
    print(f"Saved Markdown manifest: {md_path}")

# -------------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------------
if __name__ == "__main__":
    load_master()
    scene, col = build_showcase_environment()
    cameras = setup_showcase_cameras(scene, col)
    
    # Save blend file with showcase scene included
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)
    print(f"Saved updated master blend: {BLEND_FILE}")
    
    # 1. Render showcase stills
    render_showcase_stills(scene, cameras)
    
    # 2. Render walkthrough animation & compile video
    render_walkthrough_video(scene, col)
    
    # 3. Export GLB models
    records = export_glb_assets()
    
    # 4. Render thumbnails
    render_thumbnail_catalog()
    
    # 5. Manifest
    generate_asset_manifest(records)
    
    print("\n=======================================================")
    print(">>> PRODUCTION SHOWCASE & ASSET EXPORT COMPLETE! <<<")
    print("=======================================================")
