import bpy, sys
bpy.ops.wm.open_mainfile(filepath='/home/user/World_Set/WorldKit/blend/WK_Starlight_Showcase.blend')
sc = bpy.data.scenes['SHOWCASE']
bpy.context.window.scene = sc
sc.render.resolution_x = 960; sc.render.resolution_y = 540
sc.cycles.samples = 32
cam = sys.argv[-1] if len(sys.argv) > 1 and 'CAM' in sys.argv[-1] else 'CAM_Hero'
sc.camera = bpy.data.objects[cam]
sc.render.filepath = f'/home/user/World_Set/work/preview_{cam}.png'
bpy.ops.render.render(write_still=True)
print('preview done', cam)
