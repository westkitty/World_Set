import bpy, os, sys, time
bpy.ops.wm.open_mainfile(filepath='/home/user/World_Set/WorldKit/blend/WK_Starlight_Showcase.blend')
sc = bpy.data.scenes['SHOWCASE']
try: bpy.context.window.scene = sc
except Exception: pass
sc.render.resolution_x = 800; sc.render.resolution_y = 450
sc.cycles.samples = 24
for cam in os.environ.get('CAMS','CAM_Hero').split(','):
    sc.camera = bpy.data.objects[cam]
    sc.render.filepath = '/tmp/q_%s.png' % cam
    t=time.time(); bpy.ops.render.render(write_still=True)
    print('QUICK', cam, '%.0fs' % (time.time()-t), flush=True)
