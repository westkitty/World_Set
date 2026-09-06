#!/usr/bin/env python3
"""Render the 360° equirectangular environment panorama."""
import bpy

bpy.ops.wm.open_mainfile(filepath='/home/user/World_Set/WorldKit/blend/WK_Starlight_Showcase.blend')
sc = bpy.data.scenes['SHOWCASE']
try:
    bpy.context.window.scene = sc
except Exception:
    pass
sc.camera = bpy.data.objects['CAM_Pano']
sc.render.resolution_x = 2048
sc.render.resolution_y = 1024
sc.cycles.samples = 80
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.04
sc.render.filepath = '/home/user/World_Set/WorldKit/renders/pano_360.png'
bpy.ops.render.render(write_still=True)
print('pano done')
