#!/usr/bin/env python3
"""Export every kit asset as an individual GLB (origin at asset anchor)."""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
from mathutils import Matrix  # noqa: E402

LIB = '/home/user/World_Set/WorldKit/blend/WK_Starlight_Library.blend'
OUTDIR = '/home/user/World_Set/WorldKit/glb'
os.makedirs(OUTDIR, exist_ok=True)


def main():
    bpy.ops.wm.open_mainfile(filepath=LIB)
    bpy.ops.preferences.addon_enable(module='io_scene_gltf2')
    stats = json.load(open('/home/user/World_Set/work/asset_stats.json'))
    for s in stats:
        a = bpy.data.objects.get(s['name'])
        if a is None:
            print('missing', s['name'])
            continue
        # Assets are authored at the world origin and parented to an anchor that
        # sits at the asset's slot in the library layout. Zero the anchor AND
        # clear the parent inverses so the exported root sits at (0,0,0) with the
        # geometry centred on it and the contact plane at y=0 (engine-ready).
        home = a.location.copy()
        inverses = [(k, k.matrix_parent_inverse.copy()) for k in a.children_recursive]
        a.location = (0, 0, 0)
        for k, _ in inverses:
            if k.parent is a:
                k.matrix_parent_inverse = Matrix.Identity(4)
        bpy.context.view_layer.update()
        bpy.ops.object.select_all(action='DESELECT')
        a.select_set(True)
        for k in a.children_recursive:
            k.select_set(True)
        out = os.path.join(OUTDIR, s['name'] + '.glb')
        bpy.ops.export_scene.gltf(
            filepath=out, export_format='GLB', use_selection=True,
            export_yup=True, export_apply=True, export_materials='EXPORT',
            export_image_format='AUTO', export_lights=True,
            export_cameras=False, export_animations=False, export_skins=False,
            export_morph=False, use_visible=False, use_renderable=True)
        a.location = home
        for k, mi in inverses:
            k.matrix_parent_inverse = mi
        bpy.context.view_layer.update()
        print('glb', s['name'], os.path.getsize(out) // 1024, 'KB')


if __name__ == '__main__':
    main()
