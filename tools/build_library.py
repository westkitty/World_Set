#!/usr/bin/env python3
"""WORLD KIT — build the asset-library .blend (materials + 40 assets)."""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
from kit_lib import pack_all, tri_count, children_recursive  # noqa: E402
import assets_a  # noqa: E402
import assets_b  # noqa: E402

OUT = '/home/user/World_Set/WorldKit/blend/WK_Starlight_Library.blend'
os.makedirs(os.path.dirname(OUT), exist_ok=True)

BUILDERS = [
    ('WK_ARCH', assets_a.b_arch_trailer_a), ('WK_ARCH', assets_a.b_arch_trailer_b),
    ('WK_ARCH', assets_a.b_arch_porch), ('WK_ARCH', assets_a.b_arch_shed),
    ('WK_ARCH', assets_a.b_arch_carport),
    ('WK_STR', assets_a.b_str_steps), ('WK_STR', assets_a.b_str_pier),
    ('WK_STR', assets_a.b_str_antenna), ('WK_STR', assets_a.b_str_dish),
    ('WK_DOOR', assets_a.b_door),
    ('WK_WND', assets_a.b_wnd_lit), ('WK_WND', assets_a.b_wnd_dark),
    ('WK_WALL', assets_a.b_wall_chainlink), ('WK_WALL', assets_a.b_wall_gate),
    ('WK_FLR', assets_a.b_flr_gravel), ('WK_FLR', assets_a.b_flr_concrete),
    ('WK_TER', assets_a.b_ter_road), ('WK_TER', assets_a.b_ter_grass),
    ('WK_FUR', assets_b.b_fur_chair), ('WK_FUR', assets_b.b_fur_picnic),
    ('WK_FUR', assets_b.b_fur_couch),
    ('WK_PRP', assets_b.b_prp_trashcan), ('WK_PRP', assets_b.b_prp_tires),
    ('WK_PRP', assets_b.b_prp_flamingo), ('WK_PRP', assets_b.b_prp_washer),
    ('WK_PRP', assets_b.b_prp_vending), ('WK_PRP', assets_b.b_prp_pole),
    ('WK_PRP', assets_b.b_prp_wire), ('WK_PRP', assets_b.b_prp_dumpster),
    ('WK_LGT', assets_b.b_lgt_street), ('WK_LGT', assets_b.b_lgt_porch),
    ('WK_LGT', assets_b.b_lgt_string),
    ('WK_SGN', assets_b.b_sgn_pylon), ('WK_SGN', assets_b.b_sgn_trespass),
    ('WK_VEG', assets_b.b_veg_bush), ('WK_VEG', assets_b.b_veg_deadtree),
    ('WK_VEG', assets_b.b_veg_tuft),
    ('WK_DCL', assets_b.b_dcl_oil), ('WK_DCL', assets_b.b_dcl_puddle),
    ('WK_HERO', assets_b.b_hero_sedan),
]


def main():
    only = [s for s in os.environ.get('ONLY', '').split(',') if s]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.name = 'LIBRARY'
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0
    assets_a.build_materials()
    print(f'materials: {len(bpy.data.materials)}')

    anchors = []
    cols, spacing = 8, 11.0
    for i, (cat, fn) in enumerate(BUILDERS):
        home = ((i % cols) * spacing, -(i // cols) * spacing, 0)
        if only and not any(fn.__name__ == 'b_' + s.lower().replace('wk_', '') or
                            s in fn.__name__ or fn.__name__.endswith(s.lower())
                            for s in only):
            # match by asset substring instead
            pass
        try:
            a = fn(home)
            if only and not any(s.lower() in a.name.lower() for s in only):
                # remove non-matching (test mode)
                kids = children_recursive(a)
                for k in kids:
                    bpy.data.objects.remove(k, do_unlink=True)
                bpy.data.objects.remove(a, do_unlink=True)
                continue
            anchors.append(a)
            print(f'built {a.name}')
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f'FAILED {fn.__name__}: {e}')
            if not only:
                raise

    stats = []
    for a in anchors:
        kids = children_recursive(a)
        parts = [k for k in kids if k.type == 'MESH']
        lights = [k for k in kids if k.type == 'LIGHT']
        stats.append({'name': a.name,
                      'cat': a.users_collection[0].name if a.users_collection else '?',
                      'tris': tri_count(parts), 'parts': len(parts),
                      'lights': len(lights), 'home': list(a.location)})
    with open('/home/user/World_Set/work/asset_stats.json', 'w') as f:
        json.dump(stats, f, indent=1)
    print('total tris:', sum(s['tris'] for s in stats))

    pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
    print('saved', OUT)


if __name__ == '__main__':
    main()
