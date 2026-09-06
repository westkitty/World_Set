#!/usr/bin/env python3
"""Probe Blender 5.0 API details: material flags, glTF export params."""
import bpy, json, struct, os

bpy.ops.wm.read_factory_settings(use_empty=True)

mat = bpy.data.materials.new('Probe')
print('== material attrs (side/alpha/blend/cull) ==')
for a in sorted(dir(mat)):
    if any(k in a.lower() for k in ('doubl', 'side', 'alpha', 'blend', 'cull', 'transp', 'shadow')):
        try:
            print(' ', a, '=', getattr(mat, a))
        except Exception as e:
            print(' ', a, 'ERR', e)

print('== glTF export params (subset) ==')
bpy.ops.preferences.addon_enable(module='io_scene_gltf2')
rna = bpy.ops.export_scene.gltf.get_rna_type()
names = sorted(p.identifier for p in rna.properties)
for n in names:
    if any(k in n for k in ('light', 'apply', 'selection', 'yup', 'materials', 'image_format', 'draco', 'sample')):
        print(' ', n)

# build tiny test: alpha-clip plane + emissive cube + point light
bpy.ops.mesh.primitive_plane_add(size=2, location=(-2, 0, 0))
pl = bpy.context.active_object
m_clip = bpy.data.materials.new('M_Clip')
m_clip.use_nodes = True
bsdf = m_clip.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (1, 1, 1, 1)
bsdf.inputs['Alpha'].default_value = 0.5
m_clip.blend_method = 'CLIP'
pl.data.materials.append(m_clip)

bpy.ops.mesh.primitive_cube_add(size=1, location=(2, 0, 0))
cb = bpy.context.active_object
m_em = bpy.data.materials.new('M_Em')
m_em.use_nodes = True
b2 = m_em.node_tree.nodes['Principled BSDF']
b2.inputs['Base Color'].default_value = (0, 0, 0, 1)
b2.inputs['Emission Color'].default_value = (1.0, 0.4, 0.1, 1)
b2.inputs['Emission Strength'].default_value = 3.0
cb.data.materials.append(m_em)

bpy.ops.object.light_add(type='POINT', location=(0, 0, 3))
lt = bpy.context.active_object
lt.data.energy = 100
lt.data.color = (1, 0.8, 0.6)

out = '/home/user/World_Set/work/probe.glb'
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=False)
print('exported', os.path.getsize(out))

with open(out, 'rb') as f:
    data = f.read()
clen = struct.unpack('<I', data[12:16])[0]
js = json.loads(data[20:20 + clen])
print('== materials ==')
print(json.dumps(js.get('materials', []), indent=1)[:2000])
print('== extensionsUsed:', js.get('extensionsUsed'))
print('== lights:', json.dumps((js.get('extensions', {}) or {}).get('KHR_lights_punctual', {}), indent=1)[:600])
print('== node w/ light ext:', [n.get('name') for n in js.get('nodes', []) if 'extensions' in n])
