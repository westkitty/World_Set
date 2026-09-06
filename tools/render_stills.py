#!/usr/bin/env python3
"""Render the final polished stills (1080p) from the showcase file."""
import bpy

bpy.ops.wm.open_mainfile(filepath='/home/user/World_Set/WorldKit/blend/WK_Starlight_Showcase.blend')
sc = bpy.data.scenes['SHOWCASE']
try:
    bpy.context.window.scene = sc
except Exception:
    pass
sc.render.resolution_x = 1920
sc.render.resolution_y = 1080
sc.cycles.samples = 112
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.03
for cam, fn in (('CAM_Hero', 'showcase_hero.png'), ('CAM_Street', 'showcase_street.png')):
    sc.camera = bpy.data.objects[cam]
    sc.render.filepath = f'/home/user/World_Set/WorldKit/renders/{fn}'
    bpy.ops.render.render(write_still=True)
    print('still done', fn)
