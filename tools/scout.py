#!/usr/bin/env python3
"""Cheap camera-scouting renders: fire a list of (name, pos, target, lens)
through the showcase at 640x360 / low spp so compositions can be judged in
~20 s each instead of 7 minutes.

    LD_LIBRARY_PATH=~/stublibs python3 tools/scout.py hero:-33.5,-3.4,2.2:-8,9,2.2:30
"""
import os
import sys
import bpy

W = int(os.environ.get('SCOUT_W', 640))
SPP = int(os.environ.get('SCOUT_SPP', 16))
OUT = '/home/user/World_Set/work/scout'
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.open_mainfile(
    filepath='/home/user/World_Set/WorldKit/blend/WK_Starlight_Showcase.blend')
sc = bpy.data.scenes['SHOWCASE']
try:
    bpy.context.window.scene = sc
except Exception:
    pass
sc.render.resolution_x = W
sc.render.resolution_y = int(W * 9 / 16)
sc.cycles.samples = SPP
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.08
sc.render.use_persistent_data = True

cd = bpy.data.cameras.new('CAM_Scout')
cam = bpy.data.objects.new('CAM_Scout', cd)
sc.collection.objects.link(cam)
look = bpy.data.objects.new('CAM_Scout_Look', None)
sc.collection.objects.link(look)
c = cam.constraints.new('TRACK_TO')
c.target = look
c.track_axis = 'TRACK_NEGATIVE_Z'
c.up_axis = 'UP_Y'
sc.camera = cam

for spec in sys.argv[1:]:
    name, p, t, lens = spec.split(':')
    cam.location = [float(v) for v in p.split(',')]
    look.location = [float(v) for v in t.split(',')]
    cd.lens = float(lens)
    bpy.context.view_layer.update()
    sc.render.filepath = f'{OUT}/{name}.png'
    bpy.ops.render.render(write_still=True)
    print('scout', name, flush=True)
print('scout done')
