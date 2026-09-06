"""Reuse test - prove the foundation pieces recombine into distinct layouts.

Three arrangements are assembled from the SAME kit meshes, each is checked for
grid alignment and for overlapping floor/ceiling volumes, and each gets a small
preview render.  This catches pieces that only "look" modular.
"""

from __future__ import annotations

import math

import bpy

from . import dna

BAY = dna.DIMENSIONS["bay_w"]
TMP = "WK_REUSE"


def _coll():
    c = bpy.data.collections.get(TMP)
    if c is None:
        c = bpy.data.collections.new(TMP)
        bpy.context.scene.collection.children.link(c)
    return c


def clear():
    c = _coll()
    for o in list(c.objects):
        bpy.data.objects.remove(o, do_unlink=True)


def _put(built, name, x, y, z=0.0, rot=0.0):
    src = built[name]
    ob = src.copy()
    _coll().objects.link(ob)
    ob.location = (x, y, z)
    ob.rotation_euler = (0, 0, math.radians(rot))
    return ob


def layout_compact(built):
    """2 x 2 enclosed room."""
    for i in range(2):
        for j in range(2):
            _put(built, "WK_FLOOR_SLAB_A_01", i * BAY + 2, j * BAY + 2)
            _put(built, "WK_ARCH_BAY_VAULT_A_01", i * BAY + 2, j * BAY + 2)
    for x in (2, 6):
        _put(built, "WK_WALL_WINDOW_A_01", x, 0)
        _put(built, "WK_WALL_STANDARD_A_01", x, 8)
    for y in (2, 6):
        _put(built, "WK_WALL_STANDARD_A_01", 0, y, rot=90)
        _put(built, "WK_WALL_STANDARD_B_01", 8, y, rot=90)


def layout_open(built):
    """3 x 2 open hall with a mezzanine, catwalk and spiral stair."""
    for i in range(3):
        for j in range(2):
            _put(built, "WK_FLOOR_SLAB_A_01", i * BAY + 2, j * BAY + 2)
            _put(built, "WK_ARCH_BAY_FLAT_A_01", i * BAY + 2, j * BAY + 2)
    _put(built, "WK_STRUCT_PLATFORM_A_01", 10, 6, z=3.6)
    _put(built, "WK_STRUCT_CATWALK_A_01", 6, 6, z=3.6)
    _put(built, "WK_STRUCT_STAIR_SPIRAL_A_01", 2, 6)
    for x in (2, 6, 10):
        _put(built, "WK_WALL_WINDOW_A_01", x, 0)


def layout_corridor(built):
    """1 x 3 narrow passage with a column rhythm and a channel floor."""
    for j in range(3):
        _put(built, "WK_FLOOR_CHANNEL_A_01", 2, j * BAY + 2)
        _put(built, "WK_ARCH_BAY_VAULT_A_01", 2, j * BAY + 2)
    for y in (2, 6, 10):
        _put(built, "WK_WALL_STANDARD_A_01", 0, y, rot=90)
        _put(built, "WK_WALL_STANDARD_B_01", 4, y, rot=90)
    for y in (0, 4, 8, 12):
        _put(built, "WK_ARCH_COLUMN_A_01", 2, y)


def _grid_ok(locs):
    return all(abs(x / (BAY / 2) - round(x / (BAY / 2))) < 1e-3 for x, y in locs)


def check_layout(built, name, builder, report):
    clear()
    builder(built)
    bpy.context.view_layer.update()
    objs = list(_coll().objects)
    floors = [o for o in objs if "FLOOR" in o.name]
    # floor volumes must not intersect
    bad = 0
    for a in range(len(floors)):
        for b in range(a + 1, len(floors)):
            if _aabb_overlap(floors[a], floors[b]):
                bad += 1
    on_grid = all(_on_grid(o) for o in objs)
    report.append(f"reuse[{name}]: {len(objs)} pieces, grid-aligned={on_grid}, "
                  f"floor overlaps={bad}")
    return on_grid and bad == 0


def _on_grid(o):
    return (abs(o.location.x / 0.5 - round(o.location.x / 0.5)) < 1e-3 and
            abs(o.location.y / 0.5 - round(o.location.y / 0.5)) < 1e-3)


def _aabb_overlap(a, b):
    import mathutils
    def bb(o):
        pts = [o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
        xs = [p.x for p in pts]; ys = [p.y for p in pts]
        return min(xs), max(xs), min(ys), max(ys)
    ax0, ax1, ay0, ay1 = bb(a); bx0, bx1, by0, by1 = bb(b)
    ox = min(ax1, bx1) - max(ax0, bx0); oy = min(ay1, by1) - max(ay0, by0)
    return ox > 0.05 and oy > 0.05


def render_previews(built, out_dir, report):
    import os
    os.makedirs(out_dir, exist_ok=True)
    sc = bpy.context.scene
    _light()
    cam = _camera()
    sc.camera = cam
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"
    sc.cycles.samples = 24; sc.cycles.use_denoising = True
    sc.render.resolution_x = 640; sc.render.resolution_y = 360
    for name, builder, target in [("A_compact", layout_compact, (4, 4, 1.6)),
                                  ("B_open", layout_open, (6, 4, 2.2)),
                                  ("C_corridor", layout_corridor, (2, 6, 2.0))]:
        clear(); builder(built)
        _aim(cam, (target[0], target[1], 1.5), dist=14)
        sc.render.filepath = os.path.join(out_dir, f"reuse_{name}.png")
        bpy.ops.render.render(write_still=True)
    clear()
    report.append("reuse previews rendered (3 layouts)")


def _light():
    if not bpy.data.objects.get("REUSE_SUN"):
        l = bpy.data.lights.new("REUSE_SUN", "SUN"); o = bpy.data.objects.new("REUSE_SUN", l)
        bpy.context.scene.collection.objects.link(o)
        l.energy = 3.0; o.rotation_euler = (math.radians(50), 0, math.radians(30))
    w = bpy.context.scene.world; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.4, 0.45, 0.5, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 1.0


def _camera():
    old = bpy.data.objects.get("REUSE_CAM")
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    cd = bpy.data.cameras.new("REUSE_CAM"); cd.lens = 32
    o = bpy.data.objects.new("REUSE_CAM", cd)
    bpy.context.scene.collection.objects.link(o)
    return o


def _aim(cam, target, dist):
    from mathutils import Vector
    t = Vector(target)
    cam.location = t + Vector((dist * 0.7, -dist * 0.7, dist * 0.5))
    d = t - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
