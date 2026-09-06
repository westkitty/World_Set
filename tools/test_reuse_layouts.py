import bpy
import math
import os

BLEND_FILE = "/Users/andrew/World_Set/WORLD_KIT_MASTER.blend"
LAYOUTS_DIR = "/Users/andrew/World_Set/layouts"
os.makedirs(LAYOUTS_DIR, exist_ok=True)

def load_master():
    bpy.ops.wm.open_mainfile(filepath=BLEND_FILE)
    print("Opened master blend file successfully.")

def instance_asset(source_name, inst_name, collection, loc=(0,0,0), rot=(0,0,0)):
    src_obj = bpy.data.objects.get(source_name)
    if not src_obj:
        raise ValueError(f"Source asset '{source_name}' not found!")
    
    inst = bpy.data.objects.new(inst_name, src_obj.data)
    inst.location = loc
    inst.rotation_euler = rot
    collection.objects.link(inst)
    return inst

def setup_test_camera_and_light(scene, col, cam_loc, cam_rot, light_loc, light_energy=2000):
    # Camera
    cam_data = bpy.data.cameras.new("TestCam")
    cam_data.lens = 24
    cam_obj = bpy.data.objects.new("TestCamObj", cam_data)
    cam_obj.location = cam_loc
    cam_obj.rotation_euler = cam_rot
    col.objects.link(cam_obj)
    scene.camera = cam_obj
    
    # Light
    light_data = bpy.data.lights.new("TestKeyLight", "POINT")
    light_data.energy = light_energy
    light_data.color = (1.0, 0.95, 0.88)
    light_obj = bpy.data.objects.new("TestKeyLightObj", light_data)
    light_obj.location = light_loc
    col.objects.link(light_obj)
    
    # Fill light
    fill_data = bpy.data.lights.new("TestFillLight", "POINT")
    fill_data.energy = light_energy * 0.4
    fill_data.color = (0.6, 0.8, 1.0)
    fill_obj = bpy.data.objects.new("TestFillLightObj", fill_data)
    fill_obj.location = (light_loc[0] - 4, light_loc[1] - 4, light_loc[2] - 1)
    col.objects.link(fill_obj)

def render_layout(filepath):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 32
    scene.render.resolution_x = 960
    scene.render.resolution_y = 540
    scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)
    print(f"Rendered layout: {filepath}")

# -------------------------------------------------------------
# TEST 1: Compact Airlock / Maintenance Conduit (4m x 8m)
# -------------------------------------------------------------
def build_test_airlock():
    print("\n--- Testing Layout 1: Compact Airlock Corridor ---")
    scene = bpy.data.scenes.new("Scene_Layout1_Airlock")
    bpy.context.window.scene = scene
    col = bpy.data.collections.new("LAYOUT1_AIRLOCK")
    scene.collection.children.link(col)
    
    # Floors (2 slabs at Y=-2, Y=2)
    instance_asset("WK_FLOOR_SLAB_A_01", "L1_Floor_01", col, (0, -2, 0))
    instance_asset("WK_FLOOR_SLAB_A_01", "L1_Floor_02", col, (0, 2, 0))
    
    # Ceilings
    instance_asset("WK_CEIL_COFFER_A_01", "L1_Ceil_01", col, (0, -2, 4))
    instance_asset("WK_CEIL_COFFER_A_01", "L1_Ceil_02", col, (0, 2, 4))
    
    # Left Wall (X = -2, rot = 90 deg around Z)
    instance_asset("WK_WALL_SOLID_A_01", "L1_Wall_L1", col, (-2, -2, 0), (0, 0, math.radians(90)))
    instance_asset("WK_WALL_PANEL_B_01", "L1_Wall_L2", col, (-2, 2, 0), (0, 0, math.radians(90)))
    
    # Right Wall (X = 2, rot = -90 deg around Z)
    instance_asset("WK_WALL_DOORFRAME_A_01", "L1_Wall_R1", col, (2, -2, 0), (0, 0, math.radians(-90)))
    instance_asset("WK_DOOR_BULKHEAD_A_01", "L1_DoorB_R1", col, (2, -2, 0), (0, 0, math.radians(-90)))
    instance_asset("WK_DOOR_SLAB_A_01", "L1_DoorS_R1", col, (2, -2, 0), (0, 0, math.radians(-90)))
    instance_asset("WK_WALL_SOLID_A_01", "L1_Wall_R2", col, (2, 2, 0), (0, 0, math.radians(-90)))
    
    # End Walls (Y = -4 and Y = +4)
    instance_asset("WK_WALL_DOORFRAME_A_01", "L1_Wall_End1", col, (0, -4, 0))
    instance_asset("WK_DOOR_BULKHEAD_A_01", "L1_DoorB_End1", col, (0, -4, 0))
    instance_asset("WK_WALL_WINDOW_A_01", "L1_Wall_End2", col, (0, 4, 0), (0, 0, math.radians(180)))
    instance_asset("WK_WINDOW_PORTAL_A_01", "L1_Win_End2", col, (0, 4, 2), (0, 0, math.radians(180)))
    
    # Lighting & Utilities
    instance_asset("WK_LIGHT_TROFFER_A_01", "L1_Troffer_01", col, (0, -2, 4))
    instance_asset("WK_LIGHT_TROFFER_A_01", "L1_Troffer_02", col, (0, 2, 4))
    instance_asset("WK_UTIL_PIPE_RUN_A_01", "L1_Pipes_01", col, (-1.9, -2, 3.2), (0, 0, math.radians(90)))
    instance_asset("WK_PROP_EXTINGUISHER_01", "L1_Exting", col, (-1.85, 1.0, 1.2), (0, 0, math.radians(90)))
    instance_asset("WK_SIGN_SECTOR_A_01", "L1_Sign", col, (0, 3.85, 2.4), (0, 0, math.radians(180)))
    
    setup_test_camera_and_light(scene, col, cam_loc=(0, -3.2, 1.8), cam_rot=(math.radians(85), 0, 0),
                                light_loc=(0, 0, 3.5), light_energy=1500)
    render_layout(os.path.join(LAYOUTS_DIR, "layout_airlock_corridor.png"))

# -------------------------------------------------------------
# TEST 2: Multi-Level Core Observation Hall (8m x 12m)
# -------------------------------------------------------------
def build_test_observation_hall():
    print("\n--- Testing Layout 2: Multi-Level Observation Chamber ---")
    scene = bpy.data.scenes.new("Scene_Layout2_Observation")
    bpy.context.window.scene = scene
    col = bpy.data.collections.new("LAYOUT2_OBSERVATION")
    scene.collection.children.link(col)
    
    # Ground Floor: 6 floor tiles (2x3 grid: X in [-2, 2], Y in [-4, 0, 4])
    for gx in [-2, 2]:
        for gy in [-4, 0, 4]:
            if gy == 0 and gx == -2:
                instance_asset("WK_FLOOR_GRATE_B_01", f"L2_Grate_{gx}_{gy}", col, (gx, gy, 0))
            else:
                instance_asset("WK_FLOOR_SLAB_A_01", f"L2_Floor_{gx}_{gy}", col, (gx, gy, 0))
    
    # 4 Heavy Columns
    for cx in [-4, 0, 4]:
        for cy in [-6, 6]:
            instance_asset("WK_STRUCT_COLUMN_A_01", f"L2_Col_{cx}_{cy}", col, (cx, cy, 0))
            
    # Overhead I-beams at Z=4.0
    instance_asset("WK_STRUCT_BEAM_A_01", "L2_Beam_01", col, (0, -2, 4), (0, 0, math.radians(90)))
    instance_asset("WK_STRUCT_BEAM_A_01", "L2_Beam_02", col, (0, 2, 4), (0, 0, math.radians(90)))
    
    # Catwalk & Stairs on right side (X=2, Y in [-2, 2], Z=2.0)
    instance_asset("WK_STRUCT_STAIRS_A_01", "L2_Stairs", col, (2, -6, 0))
    instance_asset("WK_FLOOR_CATWALK_C_01", "L2_Catwalk_01", col, (2, -2, 2))
    instance_asset("WK_FLOOR_CATWALK_C_01", "L2_Catwalk_02", col, (2, 2, 2))
    instance_asset("WK_STRUCT_RAILING_A_01", "L2_Railing_01", col, (1.05, 0, 2), (0, 0, math.radians(90)))
    instance_asset("WK_STRUCT_RAILING_A_01", "L2_Railing_02", col, (2.95, 0, 2), (0, 0, math.radians(90)))
    
    # Hero Core in central bay
    instance_asset("WK_HERO_CORE_A_01", "L2_Hero_Core", col, (-2, 0, 0))
    
    # Monitoring Console on catwalk
    instance_asset("WK_FURN_CONSOLE_A_01", "L2_Console", col, (2, 1.5, 2), (0, 0, math.radians(90)))
    
    # Upper Observation Windows (Z=4.0)
    for wy in [-4, 0, 4]:
        instance_asset("WK_WALL_WINDOW_A_01", f"L2_WinWall_{wy}", col, (-4, wy, 0), (0, 0, math.radians(90)))
        instance_asset("WK_WINDOW_PORTAL_A_01", f"L2_WinPortal_{wy}", col, (-4, wy, 2), (0, 0, math.radians(90)))
        
    setup_test_camera_and_light(scene, col, cam_loc=(4.5, -5.5, 3.6), cam_rot=(math.radians(68), 0, math.radians(35)),
                                light_loc=(-2, 0, 4.5), light_energy=3000)
    render_layout(os.path.join(LAYOUTS_DIR, "layout_observation_hall.png"))

# -------------------------------------------------------------
# TEST 3: Sub-Aquifer Pump Room & Workshop (L-Shaped Bay)
# -------------------------------------------------------------
def build_test_workshop():
    print("\n--- Testing Layout 3: Sub-Aquifer Pump Room & Workshop ---")
    scene = bpy.data.scenes.new("Scene_Layout3_Workshop")
    bpy.context.window.scene = scene
    col = bpy.data.collections.new("LAYOUT3_WORKSHOP")
    scene.collection.children.link(col)
    
    # L-shaped Floor: (0,0), (4,0), (0,4)
    instance_asset("WK_FLOOR_SLAB_A_01", "L3_Fl_01", col, (0, 0, 0))
    instance_asset("WK_FLOOR_GRATE_B_01", "L3_Fl_02", col, (4, 0, 0))
    instance_asset("WK_FLOOR_SLAB_A_01", "L3_Fl_03", col, (0, 4, 0))
    
    # Inside Corner Wall at (-2, -2)
    instance_asset("WK_WALL_CORNER_IN_A_01", "L3_CornerIn", col, (-2, -2, 0))
    
    # Equipment bay walls
    instance_asset("WK_WALL_PANEL_B_01", "L3_Panel_01", col, (2, -2, 0))
    instance_asset("WK_WALL_SOLID_A_01", "L3_Solid_01", col, (-2, 2, 0), (0, 0, math.radians(90)))
    
    # Continuous Pipe Runs along Z=3.2m
    instance_asset("WK_UTIL_PIPE_RUN_A_01", "L3_Pipes_01", col, (2, -1.9, 3.2))
    instance_asset("WK_UTIL_PIPE_RUN_A_01", "L3_Pipes_02", col, (-1.9, 2, 3.2), (0, 0, math.radians(90)))
    
    # Workshop Equipment
    instance_asset("WK_FURN_BENCH_A_01", "L3_Bench", col, (-0.8, -1.5, 0))
    instance_asset("WK_PROP_CRATE_A_01", "L3_Crate_01", col, (3.5, -0.5, 0))
    instance_asset("WK_PROP_CRATE_A_01", "L3_Crate_02", col, (3.5, -0.5, 1.0), (0, 0, math.radians(15)))
    instance_asset("WK_PROP_CANISTER_A_01", "L3_Canister_01", col, (2.2, 0.8, 0))
    instance_asset("WK_PROP_CANISTER_A_01", "L3_Canister_02", col, (2.8, 0.9, 0))
    instance_asset("WK_PROP_JUNCTION_A_01", "L3_Junction", col, (0.8, -1.85, 1.8))
    instance_asset("WK_SIGN_HAZARD_A_01", "L3_HazSign", col, (0.8, -1.85, 2.5))
    
    setup_test_camera_and_light(scene, col, cam_loc=(3.8, 4.2, 2.6), cam_rot=(math.radians(72), 0, math.radians(140)),
                                light_loc=(1, 1, 3.6), light_energy=2200)
    render_layout(os.path.join(LAYOUTS_DIR, "layout_pump_workshop.png"))

if __name__ == "__main__":
    load_master()
    build_test_airlock()
    build_test_observation_hall()
    build_test_workshop()
    print("\n>>> ALL 3 REUSE TESTS COMPLETED AND RENDERED SUCCESSFULLY! <<<")
