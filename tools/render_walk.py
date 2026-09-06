#!/usr/bin/env python3
"""WORLD KIT walkthrough dolly v2 - 14 s move through the doubled world.

The camera rolls east down Main Street, turns north into Sunset Court past the
laundromat and then lifts into a slow crane over Sunset Row.

env:  WALK_W=1024  WALK_SPP=16  WALK_N=168  WALK_FROM=1  WALK_TO=168
"""
import os
import math
import bpy

FRAMES = '/home/user/World_Set/work/frames'
os.makedirs(FRAMES, exist_ok=True)

W = int(os.environ.get('WALK_W', 1024))
SPP = int(os.environ.get('WALK_SPP', 16))
N = int(os.environ.get('WALK_N', 168))
F0 = int(os.environ.get('WALK_FROM', 1))
F1 = int(os.environ.get('WALK_TO', N))

bpy.ops.wm.open_mainfile(filepath='/home/user/World_Set/WorldKit/blend/WK_Starlight_Showcase.blend')
sc = bpy.data.scenes['SHOWCASE']
try:
    bpy.context.window.scene = sc
except Exception:
    pass

cd = bpy.data.cameras.new('CAM_Walk')
cd.lens = 30
cam = bpy.data.objects.new('CAM_Walk', cd)
sc.collection.objects.link(cam)
look = bpy.data.objects.new('CAM_Walk_Look', None)
sc.collection.objects.link(look)
c = cam.constraints.new('TRACK_TO')
c.target = look
c.track_axis = 'TRACK_NEGATIVE_Z'
c.up_axis = 'UP_Y'

# --- dolly v2.1 -------------------------------------------------------------
CAM = [(-42.0, -3.0, 2.00), (-33.0, -2.8, 2.00), (-24.0, -2.6, 2.00),
       (-15.0, -2.6, 2.10), (-6.0, -2.4, 2.10), (2.0, -2.2, 2.20),
       (4.5, 2.0, 2.40), (4.0, 8.0, 2.60), (3.4, 15.0, 3.40),
       (3.0, 22.0, 7.00), (3.0, 26.5, 16.00)]
LOOK = [(-30.0, 3.0, 3.0), (-22.0, 4.0, 2.6), (-12.0, 3.5, 2.4),
        (-3.0, 4.0, 2.4), (6.0, 5.0, 2.4), (10.0, 9.0, 2.6),
        (5.0, 16.0, 2.4), (-4.0, 20.0, 2.6), (-2.0, 30.0, 2.6),
        (6.0, 36.0, 2.0), (11.0, 40.0, 1.0)]
LENS = [30, 30, 30, 31, 32, 33, 32, 30, 28, 26, 24]


def catmull(keys, t):
    """Uniform Catmull-Rom through `keys`, t in [0,1]."""
    n = len(keys) - 1
    seg = min(int(t * n), n - 1)
    f = t * n - seg
    p0 = keys[max(seg - 1, 0)]
    p1, p2 = keys[seg], keys[seg + 1]
    p3 = keys[min(seg + 2, n)]
    out = []
    for i in range(len(p1)):
        a, b, cc, d = p0[i], p1[i], p2[i], p3[i]
        out.append(0.5 * ((2 * b) + (-a + cc) * f +
                          (2 * a - 5 * b + 4 * cc - d) * f * f +
                          (-a + 3 * b - 3 * cc + d) * f * f * f))
    return out


def ease(t):
    return t * t * (3 - 2 * t)


sc.camera = cam
sc.render.resolution_x = W
sc.render.resolution_y = int(W * 9 / 16)
sc.cycles.samples = SPP
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.05
sc.render.use_persistent_data = True
sc.render.image_settings.file_format = 'PNG'

for f in range(F0, F1 + 1):
    t = ease((f - 1) / (N - 1))
    cx, cy, cz = catmull(CAM, t)
    # gentle hand-held float, fading out as the crane takes over
    damp = 1.0 - min(t / 0.85, 1.0) * 0.7
    cz += math.sin(t * 21.0) * 0.035 * damp
    cx += math.sin(t * 13.0 + 1.1) * 0.045 * damp
    cam.location = (cx, cy, cz)
    look.location = catmull(LOOK, t)
    cam.data.lens = catmull([(v,) for v in LENS], t)[0]
    bpy.context.view_layer.update()
    sc.render.filepath = FRAMES + f'/walk_{f:04d}.png'
    bpy.ops.render.render(write_still=True)
    print('walk frame %d/%d' % (f, N), flush=True)
print('walk done')
