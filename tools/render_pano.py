#!/usr/bin/env python3
"""Render the 360x180 equirectangular environment panorama of the showcase."""
import os
import time
import bpy

W = int(os.environ.get('PANO_W', 3072))
SPP = int(os.environ.get('PANO_SPP', 56))

bpy.ops.wm.open_mainfile(filepath='/home/user/World_Set/WorldKit/blend/WK_Starlight_Showcase.blend')
sc = bpy.data.scenes['SHOWCASE']
try:
    bpy.context.window.scene = sc
except Exception:
    pass
sc.camera = bpy.data.objects['CAM_Pano']
sc.render.resolution_x = W
sc.render.resolution_y = W // 2
sc.cycles.samples = SPP
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.04
sc.render.filepath = '/home/user/World_Set/WorldKit/renders/pano_360.png'
t = time.time()
bpy.ops.render.render(write_still=True)
print('pano done %.0fs' % (time.time() - t))
