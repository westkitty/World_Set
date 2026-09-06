"""GLB export - one file per reusable asset, organised by category."""

from __future__ import annotations

import os

import bpy

from . import dna, registry


def export_all(built, out_dir: str, report) -> int:
    os.makedirs(out_dir, exist_ok=True)
    count = 0
    for spec in registry.REGISTRY:
        if not spec.export:
            continue
        cat_dir = dna.CATEGORY_EXPORT_DIRS[spec.category]
        d = os.path.join(out_dir, cat_dir)
        os.makedirs(d, exist_ok=True)
        obj = built[spec.name]
        # ensure selectable/visible
        obj.hide_set(False)
        obj.hide_render = False
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        path = os.path.join(d, f"{spec.name}.glb")
        bpy.ops.export_scene.gltf(
            filepath=path, export_format="GLB", use_selection=True,
            export_apply=True, export_yup=True, export_materials="EXPORT",
            export_texcoords=True, export_normals=True, export_tangents=False,
        )
        count += 1
    report.append(f"exported {count} GLB assets to {out_dir}")
    return count
