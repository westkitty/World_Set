import bpy, json, struct
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.preferences.addon_enable(module='io_scene_gltf2')
def mk(name, srm, alpha):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(len(bpy.data.objects)*2, 0, 0))
    o = bpy.context.active_object
    m = bpy.data.materials.new(name)
    m.surface_render_method = srm
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Alpha'].default_value = alpha
    o.data.materials.append(m)
mk('M_A_dither_a1', 'DITHERED', 1.0)
mk('M_B_dither_a05', 'DITHERED', 0.5)
mk('M_C_blend_a05', 'BLENDED', 0.5)
mk('M_D_blend_a1', 'BLENDED', 1.0)
out = '/home/user/World_Set/work/probe4.glb'
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=False)
data = open(out,'rb').read()
clen = struct.unpack('<I', data[12:16])[0]
for m in json.loads(data[20:20+clen])['materials']:
    print(m['name'], '| alphaMode:', m.get('alphaMode','OPAQUE'), '| cutoff:', m.get('alphaCutoff'), '| ds:', m.get('doubleSided', False))
