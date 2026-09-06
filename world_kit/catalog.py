"""Thumbnail catalogue - one consistent studio shot per asset + contact sheets."""

from __future__ import annotations

import math
import os

import bpy
from mathutils import Vector

from . import registry

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def _studio():
    sc = bpy.context.scene
    if not bpy.data.objects.get("CAT_SUN"):
        l = bpy.data.lights.new("CAT_SUN", "SUN"); o = bpy.data.objects.new("CAT_SUN", l)
        sc.collection.objects.link(o); l.energy = 3.5
        o.rotation_euler = (math.radians(50), 0, math.radians(35))
    if not bpy.data.objects.get("CAT_FILL"):
        l = bpy.data.lights.new("CAT_FILL", "AREA"); o = bpy.data.objects.new("CAT_FILL", l)
        sc.collection.objects.link(o); l.energy = 200; l.size = 6
        o.location = (-4, -4, 5)
    w = sc.world; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.32, 0.35, 0.38, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.6
    if not bpy.data.objects.get("CAT_CAM"):
        cd = bpy.data.cameras.new("CAT_CAM"); cd.lens = 50
        o = bpy.data.objects.new("CAT_CAM", cd); sc.collection.objects.link(o)
    return bpy.data.objects["CAT_CAM"]


def render_thumbnails(built, out_dir, report):
    os.makedirs(out_dir, exist_ok=True)
    sc = bpy.context.scene
    bpy.context.view_layer.update()
    cam = _studio()
    sc.camera = cam
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"
    sc.cycles.samples = 32; sc.cycles.use_denoising = True
    sc.render.resolution_x = 512; sc.render.resolution_y = 512

    for name in built:
        for other_name, o in built.items():
            o.hide_render = other_name != name
        obj = built[name]
        c = obj.location + (Vector(obj.bound_box[0]) + Vector(obj.bound_box[6])) / 2
        r = max(obj.dimensions) / 2
        cam.location = c + Vector((1.0, -1.0, 0.6)).normalized() * (r * 3.0 + 0.5)
        d = c - cam.location
        cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = os.path.join(out_dir, f"{name}.png")
        bpy.ops.render.render(write_still=True)
    for o in built.values():
        o.hide_render = False
    report.append(f"rendered {len(built)} thumbnails")


def build_sheets(thumb_dir, out_dir, report):
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(out_dir, exist_ok=True)
    cats = {}
    for spec in registry.REGISTRY:
        cats.setdefault(spec.category, []).append(spec.name)
    try:
        font = ImageFont.truetype(FONT, 15)
    except Exception:
        font = ImageFont.load_default()
    T = 200
    produced = []
    for cat, names in cats.items():
        cols = 4
        rows = math.ceil(len(names) / cols)
        sheet = Image.new("RGB", (cols * (T + 8) + 8, rows * (T + 34) + 8), (24, 24, 26))
        dr = ImageDraw.Draw(sheet)
        for i, n in enumerate(names):
            x = (i % cols) * (T + 8) + 8
            y = (i // cols) * (T + 34) + 8
            p = os.path.join(thumb_dir, f"{n}.png")
            if os.path.exists(p):
                sheet.paste(Image.open(p).convert("RGB").resize((T, T)), (x, y))
            dr.text((x + 2, y + T + 4), n.replace("WK_", ""), fill=(230, 230, 230), font=font)
        out = os.path.join(out_dir, f"catalog_{cat.split('_')[0]}_{cat.split('_')[1]}.png")
        sheet.save(out)
        produced.append(out)
    report.append(f"built {len(produced)} category contact sheets")
    return produced
