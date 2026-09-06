#!/usr/bin/env python3
"""Fast low-res composition preview of the showcase cameras (~2 min)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bpy

from world_kit import cameras, lighting, pipeline, showcase

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "dist", "preview")
os.makedirs(OUT, exist_ok=True)

built, report = pipeline.build()
showcase.build(built)
lighting.setup(bpy.context.scene)
cams = cameras.build_stills()
pano = cameras.build_panorama()

# hide the library originals so only the showcase renders
for c in list(bpy.data.collections):
    if c.name.split("_")[0].isdigit() and c.name != "15_SHOWCASE":
        c.hide_render = True
        c.hide_viewport = True

sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = 8
sc.cycles.use_denoising = True
sc.render.resolution_x = 480
sc.render.resolution_y = 270

for name, cam in cams.items():
    sc.camera = cam
    sc.render.filepath = os.path.join(OUT, f"pv_{name}.png")
    bpy.ops.render.render(write_still=True)
    print("preview", name, flush=True)

sc.camera = pano
sc.render.resolution_x = 640
sc.render.resolution_y = 320
sc.render.filepath = os.path.join(OUT, "pv_pano.png")
bpy.ops.render.render(write_still=True)
print("preview pano", flush=True)
print("PREVIEWS DONE", flush=True)
