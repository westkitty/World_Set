#!/usr/bin/env python3
"""WORLD KIT — assemble the STARLIGHT ESTATES showcase scene.

Opens the library .blend, instances ONLY kit assets into a new SHOWCASE
scene, adds night lighting + cameras, saves Showcase.blend, renders stills.
"""
import os
import sys
import math
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

LIB = '/home/user/World_Set/WorldKit/blend/WK_Starlight_Library.blend'
OUT = '/home/user/World_Set/WorldKit/blend/WK_Starlight_Showcase.blend'
STILLDIR = '/home/user/World_Set/WorldKit/renders'
os.makedirs(STILLDIR, exist_ok=True)
PI = math.pi


def inst(asset, loc, rot_z=0.0, rot_xyz=None, name=None):
    o = bpy.data.objects.new(name or ('SHOW_' + asset), None)
    o.instance_type = 'COLLECTION'
    o.instance_collection = bpy.data.collections[asset]
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = rot_xyz if rot_xyz else (0, 0, rot_z)
    return o


def trackto(cam, target):
    c = cam.constraints.new('TRACK_TO')
    c.target = target
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'


def marker(name, loc):
    o = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    return o


def layout():
    R = PI  # 180°: face fronts (-Y world) toward road
    # ---------------- ground: kit grass tiles + base plane for horizon
    for gx in range(-18, 19, 6):
        for gy in (-3, 3, 9, 15):
            inst('WK_TER_GrassPatch', (gx, gy, -0.06))
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 4, -0.16))
    base = bpy.context.active_object
    base.name = 'SHOW_BaseDirt'
    base.scale = (70, 55, 1)
    bpy.ops.object.transform_apply(scale=True)
    m = bpy.data.materials.new('M_BaseDirt')
    m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.02, 0.023, 0.02, 1)
    m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 1.0
    base.data.materials.append(m)
    bpy.ops.object.select_all(action='DESELECT')

    # ---------------- road + decals
    for rx in (-8, 0, 8):
        inst('WK_TER_RoadStraight', (rx, 0, 0))
    inst('WK_DCL_Puddle', (-4.5, 1.2, 0), rot_z=0.3)
    inst('WK_DCL_Puddle', (5.5, -1.4, 0), rot_z=2.1)
    inst('WK_DCL_OilStain', (1.5, 0.8, 0), rot_z=1.0)
    inst('WK_DCL_OilStain', (-9.5, -1.0, 0), rot_z=2.6)

    # ---------------- gravel + concrete pads
    for px, py in ((-9.5, 8.5), (-1.5, 8.5), (3.5, 9.0), (11.5, 9.0)):
        inst('WK_FLR_GravelPad', (px, py, 0))
    for px, py, rz in ((8.6, 6.9, 0), (-13.0, 9.0, 0.15), (13.5, 12.3, 0.3)):
        inst('WK_FLR_ConcretePad', (px, py, 0), rot_z=rz)

    # ---------------- Trailer A (mint) + porch
    A = (-5.5, 8.5)
    inst('WK_ARCH_Trailer_A', (A[0], A[1], 0), rot_z=R)
    inst('WK_ARCH_Porch', (-9.7, 5.6, 0), rot_z=R)
    inst('WK_STR_PorchSteps', (-9.7, 4.37, 0), rot_z=R)
    inst('WK_DOOR_TrailerDoor', (-9.7, 6.72, 0.6), rot_z=R)
    for wx, lit in ((-1.3, True), (-4.3, True), (-7.1, False)):
        inst('WK_WND_WindowLit' if lit else 'WK_WND_WindowDark', (wx, 6.72, 1.44), rot_z=R)
    for wx in ((-2.5, 10.28), (-7.5, 10.28)):  # back windows face +Y world
        inst('WK_WND_WindowDark', (wx[0], wx[1], 1.44))
    inst('WK_WND_WindowLit', (0.52, 8.5, 1.49), rot_z=-PI / 2)   # east gable
    inst('WK_WND_WindowDark', (-11.52, 8.5, 1.49), rot_z=PI / 2)  # west gable
    inst('WK_STR_TVAntenna', (-2.5, 8.5, 3.14))
    # porch dressing
    inst('WK_FUR_PorchCouch', (-9.7, 6.2, 0.58), rot_z=R)
    inst('WK_FUR_LawnChair', (-10.9, 5.2, 0.58), rot_z=2.2)
    inst('WK_PRP_WashingMachine', (-10.8, 3.4, 0), rot_z=0.5)
    inst('WK_LGT_PorchLight', (-8.95, 6.66, 2.0), rot_z=R)

    # ---------------- Trailer B (sand, office) + carport
    B = (6.0, 9.0)
    inst('WK_ARCH_Trailer_B', (B[0], B[1], 0), rot_z=R)
    inst('WK_DOOR_TrailerDoor', (7.4, 7.42, 0.6), rot_z=R)
    inst('WK_STR_PorchSteps', (7.4, 7.27 - 0.0, 0), rot_z=R)
    inst('WK_WND_WindowLit', (9.4, 7.42, 1.44), rot_z=R)
    inst('WK_WND_WindowLit', (5.4, 7.42, 1.44), rot_z=R)
    inst('WK_WND_WindowDark', (7.4, 10.6, 1.44))
    inst('WK_WND_WindowDark', (3.4, 10.6, 1.44))
    inst('WK_STR_Dish', (4.0, 8.5, 3.14))
    inst('WK_LGT_PorchLight', (8.15, 7.36, 2.0), rot_z=R)
    inst('WK_PRP_VendingMachine', (9.9, 6.9, 0), rot_z=R)
    inst('WK_ARCH_Carport', (11.8, 8.5, 0))
    inst('WK_HERO_Sedan86', (11.8, 8.5, 0), rot_z=0.08)
    inst('WK_DCL_OilStain', (13.3, 8.2, 0), rot_z=0.7)

    # ---------------- shed + clutter corner
    inst('WK_ARCH_Shed', (-13.0, 10.5, 0), rot_z=PI + 0.15)
    inst('WK_DOOR_TrailerDoor', (-12.37, 9.68, 0.02), rot_z=PI + 0.15)
    inst('WK_PRP_TireStack', (-14.3, 9.0, 0))
    inst('WK_PRP_TireStack', (-11.4, 10.8, 0))
    inst('WK_PRP_TrashCan', (-11.9, 9.3, 0))
    inst('WK_PRP_TrashCan', (-14.0, 11.6, 0.28), rot_xyz=(PI / 2, 0, 0.5))  # tipped
    inst('WK_PRP_Dumpster', (-15.0, 13.0, 0), rot_z=0.35)

    # ---------------- pylon + office corner
    inst('WK_SGN_PylonSign', (-14.5, 4.2, 0), rot_z=R)
    inst('WK_SGN_Trespass', (16.75, 2.65, 0), rot_z=-PI / 2)
    inst('WK_PRP_Dumpster', (14.5, 13.0, 0), rot_z=-0.25)
    inst('WK_PRP_TrashCan', (13.4, 12.2, 0))
    inst('WK_PRP_TrashCan', (-11.6, 5.2, 0))

    # ---------------- street lamps + poles + wires
    for lx in (-8, 8):
        inst('WK_LGT_StreetLamp', (lx, -4.2, 0))
    inst('WK_LGT_StreetLamp', (1.5, 4.3, 0), rot_z=PI)
    for px in (-12, 0, 12):
        inst('WK_PRP_TelephonePole', (px, 13.2, 0), rot_z=0.05 * px)
    for wx in (-6, 6):
        inst('WK_PRP_WireSpan', (wx, 13.2, 6.9))

    # ---------------- fence: back run + gated side entry
    for fx in (-14, -10, -6, -2, 2, 6, 10, 14):
        inst('WK_WALL_Chainlink4m', (fx, 14.5, 0))
    inst('WK_WALL_ChainlinkGate', (16.5, 2.65, 0), rot_z=PI / 2)
    inst('WK_WALL_Chainlink4m', (16.5, 5.3, 0), rot_z=PI / 2)
    inst('WK_WALL_Chainlink4m', (16.5, 9.3, 0), rot_z=PI / 2)
    inst('WK_WALL_Chainlink4m', (16.5, 13.3, 0), rot_z=PI / 2)

    # ---------------- yard life
    inst('WK_FUR_PicnicTable', (0.5, 5.0, 0), rot_z=0.2)
    inst('WK_FUR_LawnChair', (-0.7, 4.1, 0), rot_z=2.6)
    inst('WK_FUR_LawnChair', (1.8, 5.9, 0), rot_z=-0.7)
    inst('WK_PRP_Flamingo', (-4.0, 5.2, 0), rot_z=0.4)
    inst('WK_PRP_Flamingo', (4.9, 6.3, 0), rot_z=2.8)
    # string lights: porch post -> dead tree (6 m span)
    p1 = Vector((-8.2, 4.6, 2.62))
    d = (Vector((0.5, 5.0, 2.62)) - p1)
    d.z = 0
    d.normalize()
    sail = inst('WK_LGT_StringLights', p1 + d * 3.0, rot_z=math.atan2(d.y, d.x))
    sail.location.z = 2.62
    inst('WK_VEG_DeadTree', (p1.x + d.x * 6.0, p1.y + d.y * 6.0, 0), rot_z=0.7)
    inst('WK_VEG_DeadTree', (-16.5, 7.5, 0), rot_z=2.2)
    # bushes + tufts
    for bx, by, s in ((-11.0, 6.2, 0), (-0.5, 6.4, 1), (2.5, 6.9, 2), (12.8, 6.6, 0),
                      (-15.5, 12.0, 1), (15.5, 10.5, 2), (7.0, 12.8, 0)):
        inst('WK_VEG_ScrubBush', (bx, by, 0), rot_z=s * 1.3)
    import random
    rng = random.Random(95)
    placed = 0
    guard = 0
    while placed < 26 and guard < 400:
        guard += 1
        x, y = rng.uniform(-17, 17), rng.uniform(-5.5, 14)
        if abs(y) < 3.4:
            continue
        if -13.5 < x < 2.5 and 4.5 < y < 12.5:
            continue
        if -0.5 < x < 15.5 and 5.0 < y < 13.0:
            continue
        inst('WK_VEG_GrassTuft', (x, y, -0.05), rot_z=rng.uniform(0, PI))
        placed += 1


def spill_lights():
    def pt(loc, energy, color):
        ld = bpy.data.lights.new('spill', 'POINT')
        ld.energy = energy
        ld.color = color
        o = bpy.data.objects.new('SHOW_Spill', ld)
        bpy.context.scene.collection.objects.link(o)
        o.location = loc
        return o
    for wx in (-1.3, -4.3):  # trailer A lit windows
        pt((wx, 6.0, 1.9), 18, (1, 0.62, 0.32))
    pt((1.6, 8.5, 1.9), 14, (1, 0.62, 0.32))     # east gable
    for wx in (9.4, 5.4):  # office windows
        pt((wx, 6.7, 1.9), 30, (1, 0.66, 0.38))
    pt((-14.5, 2.6, 4.2), 60, (1, 0.45, 0.6))    # pylon wash
    pt((9.9, 5.6, 1.2), 25, (0.75, 0.87, 1.0))   # vending wash


def skycams():
    sc = bpy.context.scene
    w = bpy.data.worlds.new('NightWorld')
    w.use_nodes = True
    bg = w.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0.010, 0.014, 0.032, 1)
    bg.inputs['Strength'].default_value = 1.0
    sc.world = w
    moon = bpy.data.lights.new('Moon', 'SUN')
    moon.energy = 0.45
    moon.color = (0.55, 0.68, 0.95)
    moon.angle = 0.06
    mo = bpy.data.objects.new('SHOW_Moon', moon)
    sc.collection.objects.link(mo)
    mo.rotation_euler = (0.9, 0.15, 2.4)
    fill = bpy.data.lights.new('SkyFill', 'SUN')
    fill.energy = 0.1
    fill.color = (0.3, 0.45, 0.8)
    fill.use_shadow = False
    fo = bpy.data.objects.new('SHOW_SkyFill', fill)
    sc.collection.objects.link(fo)
    fo.rotation_euler = (1.1, 0, -0.7)

    def cam(name, loc, look):
        cd = bpy.data.cameras.new(name)
        cd.lens = 35
        o = bpy.data.objects.new(name, cd)
        sc.collection.objects.link(o)
        o.location = loc
        t = marker(name + '_Look', look)
        trackto(o, t)
        return o
    hero = cam('CAM_Hero', (8.0, -11.0, 2.8), (-5.0, 7.5, 1.6))
    street = cam('CAM_Street', (-15.5, -1.2, 1.7), (6, 7.5, 1.6))
    pano_cd = bpy.data.cameras.new('CAM_Pano')
    pano_cd.type = 'PANO'
    pano_cd.panorama_type = 'EQUIRECTANGULAR'
    pano = bpy.data.objects.new('CAM_Pano', pano_cd)
    sc.collection.objects.link(pano)
    pano.location = (-2, -1, 2.1)
    pano.rotation_euler = (PI / 2, 0, 0)
    return hero, street


def render_settings(sc):
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = 128
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    sc.cycles.max_bounces = 6
    sc.cycles.diffuse_bounces = 3
    sc.cycles.glossy_bounces = 3
    sc.cycles.transmission_bounces = 0
    sc.render.resolution_x = 1920
    sc.render.resolution_y = 1080
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = 'PNG'


def main(stills=True):
    bpy.ops.wm.open_mainfile(filepath=LIB)
    bpy.ops.scene.new(type='NEW')
    sc = bpy.context.scene
    sc.name = 'SHOWCASE'
    sc.unit_settings.system = 'METRIC'
    layout()
    spill_lights()
    hero, street = skycams()
    render_settings(sc)
    bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
    print('saved', OUT)
    if stills:
        for cam, fn in ((hero, 'showcase_hero.png'), (street, 'showcase_street.png')):
            sc.camera = cam
            sc.render.filepath = os.path.join(STILLDIR, fn)
            bpy.ops.render.render(write_still=True)
            print('still', fn)


if __name__ == '__main__':
    main(stills=os.environ.get('NOSTILLS', '') == '')
