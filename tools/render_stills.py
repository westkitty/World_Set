#!/usr/bin/env python3
"""Render the polished hero stills (1080p) from the showcase file.

env:  STILL_ONLY=hero,street   STILL_W=1920  STILL_SPP=96
"""
import os
import time
import bpy

SHOTS = [
    ('CAM_Hero', 'showcase_hero.png'),
    ('CAM_Street', 'showcase_street.png'),
    ('CAM_Court', 'showcase_court.png'),
    ('CAM_Yard', 'showcase_yard.png'),
    ('CAM_Fire', 'showcase_fire.png'),
    ('CAM_Aerial', 'showcase_aerial.png'),
]
only = [s.strip().lower() for s in os.environ.get('STILL_ONLY', '').split(',') if s.strip()]
W = int(os.environ.get('STILL_W', 1920))
SPP = int(os.environ.get('STILL_SPP', 96))

bpy.ops.wm.open_mainfile(filepath='/home/user/World_Set/WorldKit/blend/WK_Starlight_Showcase.blend')
sc = bpy.data.scenes['SHOWCASE']
try:
    bpy.context.window.scene = sc
except Exception:
    pass
sc.render.resolution_x = W
sc.render.resolution_y = int(W * 9 / 16)
sc.cycles.samples = SPP
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.03
sc.render.use_persistent_data = True

for cam, fn in SHOTS:
    if only and not any(o in cam.lower() for o in only):
        continue
    sc.camera = bpy.data.objects[cam]
    sc.render.filepath = f'/home/user/World_Set/WorldKit/renders/{fn}'
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print('still done %-22s %.0fs' % (fn, time.time() - t), flush=True)
print('stills done')
