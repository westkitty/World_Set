"""Lighting - deliberate key/fill/practical scheme from the WORLD DNA."""

from __future__ import annotations

import math

import bpy

from . import dna


def _color(key):
    return dna.color(dna.LIGHTING[key]["color"]) if isinstance(dna.LIGHTING[key]["color"], int) else dna.LIGHTING[key]["color"]


def hexc(h):
    r, g, b = dna.hex_to_linear(h)
    return (r, g, b, 1.0)


def setup(scene) -> None:
    L = dna.LIGHTING
    # ---- world: cold overcast dome -------------------------------------
    w = scene.world or bpy.data.worlds.new("WORLD_KIT_SKY")
    scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes.get("Background")
    bg.inputs[0].default_value = hexc(L["fill_sky"]["color"])
    bg.inputs[1].default_value = L["world_strength"]

    # ---- key: low, cold sea light from the seaward (-Y) side -----------
    key = bpy.data.objects.get("LGT_KEY")
    if key is None:
        kl = bpy.data.lights.new("LGT_KEY", "SUN")
        key = bpy.data.objects.new("LGT_KEY", kl)
        scene.collection.objects.link(key)
    kd = key.data
    kd.type = "SUN"
    kd.energy = L["key"]["strength"]
    kd.color = hexc(L["key"]["color"])[:3]
    kd.angle = math.radians(L["key"]["angle_deg"])
    el = math.radians(L["key"]["elevation_deg"])
    az = math.radians(L["key"]["azimuth_deg"])
    # sun direction: from azimuth/elevation toward the scene
    key.rotation_euler = (math.pi / 2 - el, 0, az)

    # ---- brine bounce: wide cool-cyan area light low, pointing up --------
    bounce = bpy.data.objects.get("LGT_BRINE")
    if bounce is None:
        bl = bpy.data.lights.new("LGT_BRINE", "AREA")
        bounce = bpy.data.objects.new("LGT_BRINE", bl)
        scene.collection.objects.link(bounce)
    bd = bounce.data
    bd.type = "AREA"
    bd.shape = "RECTANGLE"
    bd.size = 10.0
    bd.size_y = 6.0
    bd.energy = L["bounce_brine"]["strength"] * 60
    bd.color = hexc(L["bounce_brine"]["color"])[:3]
    bounce.location = (6, 2, -1.4)
    bounce.rotation_euler = (math.pi, 0, 0)     # face up

    # ---- beacon focal: warm point high at the beacon ---------------------
    beacon = bpy.data.objects.get("LGT_BEACON")
    if beacon is None:
        pl = bpy.data.lights.new("LGT_BEACON", "POINT")
        beacon = bpy.data.objects.new("LGT_BEACON", pl)
        scene.collection.objects.link(beacon)
    pd = beacon.data
    pd.type = "POINT"
    pd.energy = L["beacon"]["strength"] * 20
    pd.color = hexc(L["beacon"]["color"])[:3]
    pd.shadow_soft_size = L["beacon"]["radius"]
    beacon.location = (2, -7, 8.0)

    # ---- sodium practical rig (matches the showcase fixture layout) ------
    practicals = [
        (2, 0.6, 2.6), (6, 0.6, 2.6), (10, 0.6, 2.6),
        (0.6, 4, 2.6), (11.4, 4, 2.6),
        (1.6, 2.2, 3.3), (6, 2, 3.0),
    ]
    for i, (x, y, z) in enumerate(practicals):
        name = f"LGT_PRAC_{i}"
        o = bpy.data.objects.get(name)
        if o is None:
            pl = bpy.data.lights.new(name, "POINT")
            o = bpy.data.objects.new(name, pl)
            scene.collection.objects.link(o)
        o.data.type = "POINT"
        o.data.energy = L["practical_amber"]["strength"] * 2.0
        o.data.color = hexc(L["practical_amber"]["color"])[:3]
        o.data.shadow_soft_size = L["practical_amber"]["radius"]
        o.location = (x, y, z)

    # ---- colour management ----------------------------------------------
    vs = scene.view_settings
    try:
        vs.view_transform = dna.RENDER["color_management"]["view"]
        vs.look = dna.RENDER["color_management"]["look"]
    except TypeError:
        vs.view_transform = "Filmic"
        vs.look = "None"
    vs.exposure = dna.RENDER["color_management"]["exposure"]
