import bpy, json, struct
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.preferences.addon_enable(module='io_scene_gltf2')
img = bpy.data.images.load('/home/user/World_Set/WorldKit/tex/chainlink.png')
def mk(name, srm, cull):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(len(bpy.data.objects)*2, 0, 0))
    o = bpy.context.active_object
    m = bpy.data.materials.new(name)
    m.surface_render_method = srm
    m.use_backface_culling = cull
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    t = nt.nodes.new('ShaderNodeTexImage')
    t.image = img
    nt.links.new(t.outputs['Color'], b.inputs['Base Color'])
    nt.links.new(t.outputs['Alpha'], b.inputs['Alpha'])
    o.data.materials.append(m)
mk('M_E_dither_cullT', 'DITHERED', True)
mk('M_F_dither_cullF', 'DITHERED', False)
mk('M_G_blend_cullT', 'BLENDED', True)
out = '/home/user/World_Set/work/probe5.glb'
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=False)
data = open(out,'rb').read()
clen = struct.unpack('<I', data[12:16])[0]
for m in json.loads(data[20:20+clen])['materials']:
    print(m['name'], '| alphaMode:', m.get('alphaMode','OPAQUE'), '| cutoff:', m.get('alphaCutoff'), '| ds:', m.get('doubleSided', False))
