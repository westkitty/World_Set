#!/usr/bin/env python3
"""Material library: strip a copy of the library to materials-only, add a
swatch scene, render the swatch sheet, save Materials.blend."""
import os
import math
import bpy

LIB = '/home/user/World_Set/WorldKit/blend/WK_Starlight_Library.blend'
OUT = '/home/user/World_Set/WorldKit/blend/WK_Starlight_Materials.blend'
SWATCH = '/home/user/World_Set/WorldKit/catalog/material_swatches.png'

bpy.ops.wm.open_mainfile(filepath=LIB)
# delete all objects + collections (keep materials/images)
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
for c in list(bpy.data.collections):
    if c.name != 'Collection':
        try:
            bpy.data.collections.remove(c)
        except Exception:
            pass
mats = sorted([m for m in bpy.data.materials if m.name.startswith('M_')],
              key=lambda m: m.name)
print(len(mats), 'materials')

bpy.ops.scene.new(type='NEW')
sc = bpy.context.scene
sc.name = 'SWATCHES'
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = 40
sc.cycles.use_denoising = True
sc.cycles.denoiser = 'OPENIMAGEDENOISE'
sc.render.resolution_x = 1540
sc.render.resolution_y = 1080
sc.render.film_transparent = False
sc.render.image_settings.file_format = 'PNG'
w = bpy.data.worlds.new('SwatchWorld')
w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.03, 0.033, 0.04, 1)
sc.world = w

cols = 7
for i, m in enumerate(mats):
    x, y = (i % cols) * 1.5, -(i // cols) * 1.5
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.55, segments=24, ring_count=16,
                                         location=(x, y, 0.55))
    o = bpy.context.active_object
    o.name = 'SW_' + m.name
    o.data.materials.append(m)
    bpy.ops.object.shade_smooth()
bpy.ops.object.select_all(action='DESELECT')
# ground
bpy.ops.mesh.primitive_plane_add(size=30, location=(4.5, -4.5, 0))
g = bpy.context.active_object
gm = bpy.data.materials.new('M_SwatchGround')
gm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.05, 0.05, 0.055, 1)
gm.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.9
g.data.materials.append(gm)
bpy.ops.object.select_all(action='DESELECT')
# lights
key = bpy.data.lights.new('k', 'SUN')
key.energy = 2.2
ko = bpy.data.objects.new('k', key)
sc.collection.objects.link(ko)
ko.rotation_euler = (0.8, 0.2, 0.6)
fl = bpy.data.lights.new('f', 'SUN')
fl.energy = 0.5
fl.color = (0.6, 0.75, 1.0)
fl.use_shadow = False
fo = bpy.data.objects.new('f', fl)
sc.collection.objects.link(fo)
fo.rotation_euler = (1.0, 0, -0.8)
# camera
cd = bpy.data.cameras.new('SwatchCam')
cd.type = 'ORTHO'
cd.ortho_scale = 13.0
co = bpy.data.objects.new('SwatchCam', cd)
sc.collection.objects.link(co)
co.location = (4.5, -3.75, 14)
co.rotation_euler = (0, 0, 0)
sc.camera = co
sc.render.filepath = SWATCH
bpy.ops.render.render(write_still=True)
print('swatch done')
# label overlay: ortho 13 wide over 1540 px
from PIL import Image as _I, ImageDraw as _D, ImageFont as _F  # noqa: E402
_FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pxu = 1540 / 13.0
im = _I.open(SWATCH)
dd = _D.Draw(im)
fo = _F.truetype(_FB, 17)
for i, m in enumerate(mats):
    x, y = (i % cols) * 1.5, -(i // cols) * 1.5
    cx = (x + 2.0) * pxu
    cy = (0.808 - y) * pxu + 72
    t = m.name
    bb = dd.textbbox((0, 0), t, font=fo)
    tw = bb[2] - bb[0]
    dd.rectangle([cx - tw / 2 - 6, cy - 3, cx + tw / 2 + 6, cy + 22], fill=(5, 7, 12))
    dd.text((cx - tw / 2, cy - 3), t, font=fo, fill=(255, 235, 200))
im.save(SWATCH)
print('swatch labeled')
bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
print('saved', OUT)
