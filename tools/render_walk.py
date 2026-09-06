#!/usr/bin/env python3
"""Camera walkthrough: 8 s dolly along the road, 960x540 @12 fps."""
import os
import bpy

FRAMES = '/home/user/World_Set/work/frames'
os.makedirs(FRAMES, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath='/home/user/World_Set/WorldKit/blend/WK_Starlight_Showcase.blend')
sc = bpy.data.scenes['SHOWCASE']
try:
    bpy.context.window.scene = sc
except Exception:
    pass

# camera + look target
cd = bpy.data.cameras.new('CAM_Walk')
cd.lens = 32
cam = bpy.data.objects.new('CAM_Walk', cd)
sc.collection.objects.link(cam)
look = bpy.data.objects.new('CAM_Walk_Look', None)
sc.collection.objects.link(look)
c = cam.constraints.new('TRACK_TO')
c.target = look
c.track_axis = 'TRACK_NEGATIVE_Z'
c.up_axis = 'UP_Y'

N = 96
cam_keys = [(-14, -2.6, 1.7), (-7, -2.3, 1.7), (0, -2.3, 1.75), (7, -2.6, 1.7), (14, -2.4, 1.7)]
look_keys = [(-13.5, 4.5, 2.6), (-6, 7.5, 1.9), (1, 8.0, 1.8), (8, 8.0, 1.7), (13.5, 8.5, 1.6)]


def lerp_keys(keys, t):
    seg = min(int(t * (len(keys) - 1)), len(keys) - 2)
    f = t * (len(keys) - 1) - seg
    a, b = keys[seg], keys[seg + 1]
    return tuple(a[i] + (b[i] - a[i]) * f for i in range(3))


sc.camera = cam
sc.render.resolution_x = 960
sc.render.resolution_y = 540
sc.cycles.samples = 40
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.05
sc.render.use_persistent_data = True
sc.render.image_settings.file_format = 'PNG'
for f in range(1, N + 1):
    t = (f - 1) / (N - 1)
    cam.location = lerp_keys(cam_keys, t)
    look.location = lerp_keys(look_keys, t)
    bpy.context.view_layer.update()
    sc.render.filepath = FRAMES + f'/walk_{f:04d}.png'
    bpy.ops.render.render(write_still=True)
    print('walk frame', f, flush=True)
print('walk done')
