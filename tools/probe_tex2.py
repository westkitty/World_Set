import bpy, math, sys
bpy.ops.wm.read_factory_settings(use_empty=True)
img = bpy.data.images.load('/home/user/World_Set/work/texprobe.png')
m = bpy.data.materials.new('t')
b = m.node_tree.nodes['Principled BSDF']
t = m.node_tree.nodes.new('ShaderNodeTexImage'); t.image = img
m.node_tree.links.new(t.outputs['Color'], b.inputs['Base Color'])
m.node_tree.links.new(t.outputs['Color'], b.inputs['Emission Color'])
b.inputs['Emission Strength'].default_value = 1.5
sys.path.insert(0, '/home/user/World_Set/tools')
from kit_lib import plane, box
plane('A_pos90', 1.8, 0.9, (-3, 0, 1), rot=(math.pi/2, 0, 0), mat=m)
plane('B_neg90', 1.8, 0.9, (-1, 0, 1), rot=(-math.pi/2, 0, 0), mat=m)
plane('C_pos90_z180', 1.8, 0.9, (1, 0, 1), rot=(math.pi/2, 0, math.pi), mat=m)
box('D_box', (1.8, 0.1, 0.9), (3, 0, 1), mat=m)
sc = bpy.context.scene
sc.render.engine='CYCLES'; sc.cycles.samples=16; sc.cycles.device='CPU'
sc.render.resolution_x=1200; sc.render.resolution_y=300
cd = bpy.data.cameras.new('c'); o = bpy.data.objects.new('c', cd); sc.collection.objects.link(o)
cd.lens = 28
o.location=(0,-7,1); o.rotation_euler=(math.pi/2,0,0)
sc.camera=o
sc.render.filepath='/home/user/World_Set/work/tex2_south.png'
bpy.ops.render.render(write_still=True)
o.location=(0,7,1); o.rotation_euler=(math.pi/2,0,math.pi)
sc.render.filepath='/home/user/World_Set/work/tex2_north.png'
bpy.ops.render.render(write_still=True)
print('probe2 done')
