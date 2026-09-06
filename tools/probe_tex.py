import bpy, math
from PIL import Image, ImageDraw, ImageFont
# asymmetric test texture
p = Image.new('RGB', (256, 128), (20, 30, 40))
d = ImageDraw.Draw(p)
d.rectangle([8, 8, 248, 120], outline=(255,255,255), width=4)
d.text((40, 30), 'ABC▶', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48), fill=(255, 200, 80))
p.save('/home/user/World_Set/work/texprobe.png')
bpy.ops.wm.read_factory_settings(use_empty=True)
img = bpy.data.images.load('/home/user/World_Set/work/texprobe.png')
def mat():
    m = bpy.data.materials.new('t')
    b = m.node_tree.nodes['Principled BSDF']
    t = m.node_tree.nodes.new('ShaderNodeTexImage'); t.image = img
    m.node_tree.links.new(t.outputs['Color'], b.inputs['Base Color'])
    m.node_tree.links.new(t.outputs['Color'], b.inputs['Emission Color'])
    b.inputs['Emission Strength'].default_value = 1.5
    return m
m = mat()
import sys; sys.path.insert(0, '/home/user/World_Set/tools')
from kit_lib import plane
# three orientations at x=-3,0,3
plane('rot_neg90', 2, 1, (-3, 0, 1), rot=(-math.pi/2, 0, 0), mat=m)
plane('rot_pos90', 2, 1, (0, 0, 1), rot=(math.pi/2, 0, 0), mat=m)
bpy.ops.mesh.primitive_cube_add(size=1, location=(3, 0, 1))
c = bpy.context.active_object; c.name='boxface'; c.dimensions=(2, 0.1, 1)
bpy.ops.object.transform_apply(scale=True)
c.data.materials.append(m)
sc = bpy.context.scene
sc.render.engine='CYCLES'; sc.cycles.samples=16; sc.cycles.device='CPU'
sc.render.resolution_x=900; sc.render.resolution_y=300
cd = bpy.data.cameras.new('c'); o = bpy.data.objects.new('c', cd); sc.collection.objects.link(o)
o.location=(0,-5,1); o.rotation_euler=(math.pi/2,0,0)  # look +Y (north)
sc.camera=o
sc.render.filepath='/home/user/World_Set/work/texprobe_from_south.png'
bpy.ops.render.render(write_still=True)
o.location=(0,5,1); o.rotation_euler=(math.pi/2,0,math.pi)  # look -Y (south)
sc.render.filepath='/home/user/World_Set/work/texprobe_from_north.png'
bpy.ops.render.render(write_still=True)
print('probe done')
