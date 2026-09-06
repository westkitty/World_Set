import bpy
import math
import os
from mathutils import Vector

bpy.ops.wm.open_mainfile(filepath="/Users/andrew/World_Set/WORLD_KIT_MASTER.blend")
scene = bpy.data.scenes.get("Scene_Showcase")
bpy.context.window.scene = scene

cam_obj = bpy.data.objects.get("Cam_StargatePortal_Obj")
if not cam_obj:
    cam_data = bpy.data.cameras.new("Cam_StargatePortal")
    cam_obj = bpy.data.objects.new("Cam_StargatePortal_Obj", cam_data)
    scene.collection.children["15_SHOWCASE"].objects.link(cam_obj)

cam_obj.data.lens = 22
# Dramatic perspective along runway looking north at Stargate
cam_obj.location = (-1.2, 19.0, 1.8)
target = Vector((0.0, 32.0, 3.8))
direction = target - cam_obj.location
rot_quat = direction.to_track_quat("-Z", "Y")
cam_obj.rotation_euler = rot_quat.to_euler()
print("Cam location:", cam_obj.location)
print("Cam rot euler (deg):", [math.degrees(a) for a in cam_obj.rotation_euler])

# Boost portal vortex light
p_light = bpy.data.objects.get("SC_Light_Portal_Vortex_Obj")
if p_light:
    p_light.data.energy = 14000
    p_light.location = (0, 31.8, 3.8)

# Make sure portal ring is visible
scene.camera = cam_obj
scene.render.engine = "CYCLES"
scene.cycles.samples = 32
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
out_path = "/Users/andrew/World_Set/renders/showcase/05_stargate_portal_chamber.png"
scene.render.filepath = out_path

bpy.ops.wm.save_as_mainfile(filepath="/Users/andrew/World_Set/WORLD_KIT_MASTER.blend")
print("Rendering corrected camera angle...")
bpy.ops.render.render(write_still=True)
print("Rendered:", out_path)
