import bpy, json, struct
bpy.ops.wm.read_factory_settings(use_empty=True)
mat = bpy.data.materials.new('Probe')
print('== render/surface/dither/opaque attrs ==')
for a in sorted(dir(mat)):
    if any(k in a.lower() for k in ('surface', 'render', 'dither', 'opaque', 'volume')):
        try: print(' ', a, '=', repr(getattr(mat, a))[:120])
        except Exception as e: print(' ', a, 'ERR')
print('blend_method choices:', [e.identifier for e in mat.blend_rna.properties['blend_method'].enum_items] if hasattr(mat,'blend_rna') else '?')
try:
    print('surface_render_method' in dir(mat) and mat.surface_render_method)
except Exception as e: print('srm err', e)
