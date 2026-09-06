import bpy, os
print('version:', bpy.app.version_string)
# clean scene
bpy.ops.wm.read_factory_settings(use_empty=True)
# primitive
bpy.ops.mesh.primitive_cube_add(size=2, location=(0,0,1))
cube = bpy.context.active_object
cube.name = 'SmokeCube'
# material with emission
mat = bpy.data.materials.new('M_Smoke')
mat.use_nodes = True
bsdf = mat.node_tree.nodes['Principled BSDF']
print('BSDF inputs:', [i.name for i in bsdf.inputs])
bsdf.inputs['Base Color'].default_value = (0.8, 0.2, 0.2, 1)
cube.data.materials.append(mat)
# smart uv
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02)
bpy.ops.object.mode_set(mode='OBJECT')
# light + camera
bpy.ops.object.light_add(type='SUN', location=(5,5,5))
bpy.ops.object.camera_add(location=(4,-4,3), rotation=(1.1,0,0.785))
cam = bpy.context.active_object
bpy.context.scene.camera = cam
# render settings cycles cpu tiny
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = 8
sc.render.resolution_x, sc.render.resolution_y = 256, 256
sc.render.film_transparent = False
sc.render.filepath = '/home/user/World_Set/work/smoke.png'
sc.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
print('RENDER OK', os.path.getsize('/home/user/World_Set/work/smoke.png'))
# gltf addon check
try:
    bpy.ops.preferences.addon_enable(module='io_scene_gltf2')
    print('GLTF addon enabled')
except Exception as e:
    print('GLTF addon enable:', e)
print('has export op:', hasattr(bpy.ops.export_scene, 'gltf'))
bpy.ops.export_scene.gltf(filepath='/home/user/World_Set/work/smoke.glb', export_format='GLB', use_selection=False)
print('GLB OK', os.path.getsize('/home/user/World_Set/work/smoke.glb'))
bpy.ops.wm.save_as_mainfile(filepath='/home/user/World_Set/work/smoke.blend')
print('BLEND OK')
