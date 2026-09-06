#!/usr/bin/env python3
"""Render per-asset thumbnails (384px, dark studio) from the library .blend."""
import os
import sys
import json
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

LIB = '/home/user/World_Set/WorldKit/blend/WK_Starlight_Library.blend'
OUTDIR = '/home/user/World_Set/WorldKit/catalog/thumbs'
os.makedirs(OUTDIR, exist_ok=True)


def setup_scene():
    sc = bpy.context.scene
    sc.name = 'THUMB'
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = 24
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    sc.cycles.max_bounces = 4
    sc.cycles.diffuse_bounces = 2
    sc.cycles.glossy_bounces = 2
    sc.render.resolution_x = sc.render.resolution_y = 384
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = 'PNG'
    w = bpy.data.worlds.new('ThumbWorld')
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.012, 0.016, 0.028, 1)
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.0
    sc.world = w
    # shadow-catcher ground
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -0.02))
    g = bpy.context.active_object
    g.name = 'ThumbGround'
    g.is_shadow_catcher = True
    bpy.ops.object.select_all(action='DESELECT')
    return sc


def set_lights(center, r):
    for name in ('ThumbKey', 'ThumbFill', 'ThumbRim'):
        o = bpy.data.objects.get(name)
        if o:
            bpy.data.objects.remove(o, do_unlink=True)
    def add(nm, typ, off, energy, color):
        ld = bpy.data.lights.new(nm, typ)
        ld.energy = energy
        ld.color = color
        o = bpy.data.objects.new(nm, ld)
        bpy.context.scene.collection.objects.link(o)
        o.location = center + Vector(off) * r
        return o
    key = add('ThumbKey', 'SPOT', (0.8, 1.0, 1.4), 60 * r * r, (1, 0.93, 0.82))
    key.data.spot_size = 0.9
    # aim key at center
    d = center - key.location
    key.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    add('ThumbFill', 'POINT', (-1.2, 0.6, 0.7), 12 * r * r, (0.5, 0.65, 1.0))
    add('ThumbRim', 'POINT', (0.2, -1.2, 0.9), 20 * r * r, (0.65, 0.75, 1.0))


def bounds(objs):
    pts = []
    for o in objs:
        if o.type != 'MESH':
            continue
        for c in o.bound_box:
            pts.append(o.matrix_world @ Vector(c))
    if not pts:
        return Vector(), 1.0
    mn = Vector(map(min, zip(*pts)))
    mx = Vector(map(max, zip(*pts)))
    return (mn + mx) / 2, max((mx - mn).length / 2, 0.15)


def main():
    bpy.ops.wm.open_mainfile(filepath=LIB)
    stats = json.load(open('/home/user/World_Set/work/asset_stats.json'))
    sc = setup_scene()
    cam_data = bpy.data.cameras.new('ThumbCam')
    cam = bpy.data.objects.new('ThumbCam', cam_data)
    sc.collection.objects.link(cam)
    sc.camera = cam
    cam_data.lens = 40

    anchors = [bpy.data.objects.get(s['name']) for s in stats]
    last = int(os.environ.get('THUMB_LAST', '0'))
    only = [x for x in os.environ.get('THUMB_ONLY', '').split(',') if x]
    wanted = set(s['name'] for s in (stats[-last:] if last else stats))
    if only:
        wanted = set(s['name'] for s in stats if any(x.lower() in s['name'].lower() for x in only))
    for a, s in zip(anchors, stats):
        if s['name'] not in wanted:
            continue
        if a is None:
            print('missing', s['name'])
            continue
        # isolate
        for other in anchors:
            if other is None:
                continue
            hide = other is not a
            other.hide_viewport = hide
            other.hide_render = hide
            for k in other.children_recursive:
                k.hide_viewport = hide
                k.hide_render = hide
        bpy.context.view_layer.update()
        meshes = [k for k in [a] + list(a.children_recursive) if k.type == 'MESH']
        c, r = bounds(meshes)
        ground = bpy.data.objects['ThumbGround']
        ground.location.z = min((o.matrix_world @ Vector(b)).z
                                for o in meshes for b in o.bound_box) - 0.01
        set_lights(c, max(r, 0.6))
        view = Vector((1.0, 0.9, 0.55)).normalized()  # fronts face +Y
        cam.location = c + view * r * 3.0
        d = c - cam.location
        cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
        sc.render.filepath = os.path.join(OUTDIR, s['name'] + '.png')
        bpy.ops.render.render(write_still=True)
        print('thumb', s['name'], f'r={r:.2f}')
    print('done ->', OUTDIR)


if __name__ == '__main__':
    main()
