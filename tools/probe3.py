import bpy, json, struct
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.preferences.addon_enable(module='io_scene_gltf2')
def mk(name, srm, cull):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(len(bpy.data.objects), 0, 0))
    o = bpy.context.active_object
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.surface_render_method = srm
    m.use_backface_culling = cull
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Alpha'].default_value = 0.5
    o.data.materials.append(m)
mk('M_Opaque_Cull', 'OPAQUE', True)
mk('M_Dither_NoCull', 'DITHERED', False)
mk('M_Blend_Cull', 'BLENDED', True)
out = '/home/user/World_Set/work/probe3.glb'
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=False)
data = open(out,'rb').read()
clen = struct.unpack('<I', data[12:16])[0]
for m in json.loads(data[20:20+clen])['materials']:
    print(m['name'], '| alphaMode:', m.get('alphaMode','OPAQUE'), '| cutoff:', m.get('alphaCutoff'), '| doubleSided:', m.get('doubleSided', False))
