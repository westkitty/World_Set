#!/usr/bin/env python3
"""WORLD KIT v2 — assemble the STARLIGHT ESTATES showcase world (2x).

Opens the library .blend and instances ONLY kit assets into a SHOWCASE scene:
Main Street east-west, Sunset Court running north off the T-junction, and
Sunset Row branching east at the top. Fifteen dressed lots, five home types,
night lighting, six hero cameras plus an equirect pano camera.

    NOSTILLS=1 python3 tools/build_showcase.py     # build + save only
"""
import os
import sys
import math
import json
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

LIB = '/home/user/World_Set/WorldKit/blend/WK_Starlight_Library.blend'
OUT = '/home/user/World_Set/WorldKit/blend/WK_Starlight_Showcase.blend'
STILLDIR = '/home/user/World_Set/WorldKit/renders'
os.makedirs(STILLDIR, exist_ok=True)
PI = math.pi
RNG = random.Random(1995)

COUNT = {'inst': 0}
SPILL = []          # (loc, energy, color) queued by the dressing code


def inst(asset, loc, rot_z=0.0, rot_xyz=None, name=None):
    o = bpy.data.objects.new(name or ('SHOW_' + asset), None)
    o.instance_type = 'COLLECTION'
    o.instance_collection = bpy.data.collections[asset]
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = rot_xyz if rot_xyz else (0, 0, rot_z)
    COUNT['inst'] += 1
    return o


def marker(name, loc):
    o = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    return o


def trackto(cam, target):
    c = cam.constraints.new('TRACK_TO')
    c.target = target
    c.track_axis = 'TRACK_NEGATIVE_Z'
    c.up_axis = 'UP_Y'


# --------------------------------------------------------------- lot helper
class Lot:
    """A lot with its own local frame: +Y is the way the home faces."""

    def __init__(self, x, y, facing):
        self.o = Vector((x, y, 0.0))
        self.f = facing                       # radians, 0 = fronts face +Y

    def world(self, lx, ly, lz=0.0):
        c, s = math.cos(self.f), math.sin(self.f)
        return (self.o.x + lx * c - ly * s, self.o.y + lx * s + ly * c, lz)

    def put(self, asset, lx, ly, lz=0.0, spin=0.0):
        return inst(asset, self.world(lx, ly, lz), rot_z=self.f + spin)

    def spill(self, lx, ly, lz, energy, color):
        SPILL.append((self.world(lx, ly, lz), energy, color))


# --------------------------------------------------------------- home types
def dress_single_a(L, lit=(True, False, True), tv=False):
    """12 x 3.6 single-wide, mint. Door at local +4.2, front face y = +1.8."""
    L.put('WK_ARCH_Trailer_A', 0, 0)
    L.put('WK_DOOR_TrailerDoor', 4.2, 1.78, 0.6)
    L.put('WK_STR_PorchSteps', 4.2, 0.55, 0)
    for i, wx in enumerate((-4.2, -1.2, 1.6)):
        if tv and i == 1:
            L.put('WK_WND_WindowTVLit', wx, 1.78, 1.44)
            L.spill(wx, 3.0, 1.9, 22, (0.45, 0.62, 1.0))
        elif lit[i % len(lit)]:
            L.put('WK_WND_WindowLit', wx, 1.78, 1.44)
            L.spill(wx, 3.0, 1.9, 20, (1.0, 0.62, 0.32))
        else:
            L.put('WK_WND_WindowDark', wx, 1.78, 1.44)
    for wx in (-3.0, 2.0):
        L.put('WK_WND_WindowDark', wx, -1.78, 1.44, spin=PI)
    L.put('WK_WND_WindowLit', 6.02, 0.0, 1.49, spin=-PI / 2)
    L.spill(7.4, 0.0, 1.9, 14, (1.0, 0.62, 0.32))
    L.put('WK_WND_WindowDark', -6.02, 0.0, 1.49, spin=PI / 2)
    for px in (-4.5, 0.0, 4.5):               # piers under the belly
        L.put('WK_STR_CinderPier', px, 1.4, 0)
        L.put('WK_STR_CinderPier', px, -1.4, 0)
    L.put('WK_LGT_PorchLight', 4.95, 1.74, 2.0)
    L.spill(4.95, 2.4, 1.9, 26, (1.0, 0.70, 0.42))
    L.put('WK_STR_TVAntenna', -2.5, 0.0, 3.14)
    L.put('WK_STR_ACWindowUnit', -4.2, 1.86, 1.44)


def dress_single_b(L, office=False, boarded=False):
    """10 x 3.2 single-wide, sand. Door at local -1.4, front face y = +1.6."""
    L.put('WK_ARCH_Trailer_B', 0, 0)
    L.put('WK_DOOR_ScreenDoor' if not office else 'WK_DOOR_TrailerDoor', -1.4, 1.58, 0.6)
    L.put('WK_STR_PorchSteps', -1.4, 0.4, 0)
    for wx in (-3.4, 0.6):
        if boarded and wx < 0:
            L.put('WK_WND_WindowBoarded', wx, 1.58, 1.44)
        else:
            L.put('WK_WND_WindowLit', wx, 1.58, 1.44)
            L.spill(wx, 2.8, 1.9, 24, (1.0, 0.66, 0.38))
    for wx in (-1.4, 2.6):
        L.put('WK_WND_WindowDark', wx, -1.58, 1.44, spin=PI)
    L.put('WK_STR_Dish', -2.0, 0.0, 3.14)
    L.put('WK_LGT_PorchLight', -0.65, 1.54, 2.0)
    L.spill(-0.65, 2.2, 1.9, 24, (1.0, 0.70, 0.42))
    for px in (-3.5, 0.0, 3.5):
        L.put('WK_STR_CinderPier', px, 1.2, 0)
        L.put('WK_STR_CinderPier', px, -1.2, 0)
    if office:
        L.put('WK_PRP_VendingMachine', 3.9, 1.4, 0)
        L.spill(3.9, 2.4, 1.2, 26, (0.75, 0.87, 1.0))
        L.put('WK_SGN_LotNumber', 5.4, 2.6, 0)


def dress_double_c(L, tv=True):
    """14 x 7 double-wide. Doors at local -4.6 / +3.4, front face y = +3.5."""
    L.put('WK_ARCH_Trailer_C_Double', 0, 0)
    for dx in (-4.6, 3.4):
        L.put('WK_DOOR_TrailerDoor', dx, 3.4, 0.62)
        L.put('WK_STR_PorchSteps', dx, 2.2, 0)
    wins = ((-6.0, 'lit'), (-2.4, 'tv' if tv else 'lit'), (0.6, 'dark'), (5.4, 'lit'))
    for wx, kind in wins:
        if kind == 'lit':
            L.put('WK_WND_WindowLit', wx, 3.4, 1.51)
            L.spill(wx, 4.6, 2.0, 22, (1.0, 0.64, 0.34))
        elif kind == 'tv':
            L.put('WK_WND_WindowTVLit', wx, 3.4, 1.51)
            L.spill(wx, 4.6, 2.0, 26, (0.45, 0.62, 1.0))
        else:
            L.put('WK_WND_WindowDark', wx, 3.4, 1.51)
    for wx in (-4.0, 1.0, 4.6):
        L.put('WK_WND_WindowDark', wx, -3.4, 1.51, spin=PI)
    L.put('WK_LGT_PorchLight', -3.9, 3.36, 2.05)
    L.spill(-3.9, 4.2, 1.95, 26, (1.0, 0.70, 0.42))
    L.put('WK_STR_SwampCooler', 5.6, 2.2, 3.28)
    L.put('WK_STR_TVAntenna', -5.5, -1.0, 3.28)
    L.put('WK_STR_ACWindowUnit', 0.6, 3.5, 1.5)
    for px in (-5.5, 0.0, 5.5):
        for py in (-3.0, 0.0, 3.0):
            L.put('WK_STR_CinderPier', px, py, 0)


def dress_camper_d(L):
    """7 m travel trailer, still hitched to nothing."""
    L.put('WK_ARCH_Trailer_D_Camper', 0, 0)
    L.put('WK_STR_HitchTongue', 4.4, 0, 0, spin=PI)
    L.put('WK_FUR_PlasticTable', -1.2, 3.2, 0)
    L.put('WK_FUR_LawnChair', 0.4, 3.6, 0, spin=2.1)
    L.put('WK_PRP_MilkCrates', 2.2, 2.4, 0)
    L.spill(0.4, 1.6, 1.9, 18, (1.0, 0.68, 0.4))


def dress_rv(L):
    L.put('WK_HERO_MotorhomeRV', 0, 0)
    L.put('WK_PRP_LeaningLadder', -4.9, 1.4, 0)
    L.put('WK_STR_PropaneTank', 3.4, 2.2, 0)
    L.put('WK_FUR_KettleGrill', 1.4, 3.0, 0)
    L.put('WK_PRP_MilkCrates', 2.6, 3.4, 0)
    L.spill(0.4, 2.4, 2.2, 20, (1.0, 0.72, 0.42))


def dress_yard(L, kind=0, w=9.0, d=7.0):
    """Generic yard dressing in front of / around a home."""
    if kind % 3 == 0:
        L.put('WK_FUR_PicnicTable', -w * 0.28, d * 0.55, 0, spin=0.25)
        L.put('WK_FUR_LawnChair', -w * 0.42, d * 0.4, 0, spin=2.3)
        L.put('WK_PRP_Flamingo', w * 0.2, d * 0.5, 0, spin=0.6)
    elif kind % 3 == 1:
        L.put('WK_FUR_Recliner', -w * 0.3, d * 0.45, 0, spin=0.2)
        L.put('WK_FUR_KettleGrill', -w * 0.05, d * 0.5, 0)
        L.put('WK_PRP_TireStack', w * 0.34, d * 0.62, 0)
    else:
        L.put('WK_FUR_PlasticTable', -w * 0.22, d * 0.5, 0)
        L.put('WK_FUR_LawnChair', -w * 0.05, d * 0.42, 0, spin=-0.8)
        L.put('WK_PRP_KidBike', w * 0.3, d * 0.35, 0, spin=1.1)
    L.put('WK_PRP_TrashCan', w * 0.46, d * 0.75, 0)
    L.put('WK_VEG_ScrubBush', -w * 0.5, d * 0.3, 0, spin=RNG.uniform(0, 3))
    L.put('WK_VEG_ScrubBush', w * 0.45, d * 0.2, 0, spin=RNG.uniform(0, 3))
    L.put('WK_VEG_WeedClump', -w * 0.55, d * 0.7, 0, spin=RNG.uniform(0, 3))
    L.put('WK_SGN_LotNumber', w * 0.55, d * 0.92, 0)
    L.put('WK_DCL_TireTracks', 0.0, d * 0.95, 0, spin=RNG.uniform(-0.1, 0.1))


# --------------------------------------------------------------- the world
def layout():
    R = PI

    # ---------------- ground bed -------------------------------------------
    for gx in range(-42, 43, 6):
        for gy in range(-18, 46, 6):
            if abs(gy) < 4:                       # Main Street corridor
                continue
            if abs(gx) < 4 and -2 < gy < 34:      # Sunset Court corridor
                continue
            if abs(gy - 32) < 4 and gx > -2:      # Sunset Row corridor
                continue
            inst('WK_TER_GrassPatch', (gx, gy, -0.06))
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 8, -0.17))
    base = bpy.context.active_object
    base.name = 'SHOW_BaseDirt'
    base.scale = (900, 900, 1)                    # far past every horizon
    bpy.ops.object.transform_apply(scale=True)
    m = bpy.data.materials.new('M_BaseDirt')
    m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.02, 0.023, 0.02, 1)
    m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 1.0
    base.data.materials.append(m)
    bpy.ops.object.select_all(action='DESELECT')

    # ---------------- roads -------------------------------------------------
    for x in (-40, -32, -24, -16, -8, 8, 16, 24, 32, 40):
        inst('WK_TER_RoadStraight', (x, 0, 0))
    inst('WK_TER_RoadTee', (0, 0, 0))                       # junction, spur +Y
    for y in (8, 16, 24):                                   # Sunset Court
        inst('WK_TER_RoadStraight', (0, y, 0), rot_z=PI / 2)
    inst('WK_TER_RoadCorner', (0, 32, 0), rot_z=PI)         # turns east
    for x in (8, 16, 24):                                   # Sunset Row
        inst('WK_TER_RoadStraight', (x, 32, 0))
    inst('WK_FLR_GravelPad', (31, 32, 0))                   # turnaround
    inst('WK_FLR_DirtPad', (38, 32, 0))

    # road dressing
    for x, y, r in ((-26.5, 1.4, 0.3), (13.5, -1.6, 2.1), (-6.0, 2.0, 1.2),
                    (2.5, 18.0, 0.4), (19.0, 30.0, 2.4)):
        inst('WK_DCL_Puddle', (x, y, 0), rot_z=r)
    for x, y, r in ((-18.0, -1.2, 1.0), (5.5, 1.1, 2.6), (28.0, -1.5, 0.5),
                    (-2.2, 12.0, 1.7)):
        inst('WK_DCL_OilStain', (x, y, 0), rot_z=r)
    for x, y in ((-30, -4.6), (-10, 4.6), (22, -4.6)):
        inst('WK_DCL_TireTracks', (x, y, 0))
    for x, y in ((-24.5, 5.0), (11.0, -5.2), (4.6, 20.0)):
        inst('WK_DCL_LitterScatter', (x, y, 0), rot_z=RNG.uniform(0, 3))

    # ---------------- south side of Main Street (fronts face +Y) -----------
    south = [
        (-34.0, 'A', 0), (-22.0, 'B', 1), (-9.0, 'C', 2), (6.0, 'A', 0),
        (20.0, 'D', 1), (31.0, 'RV', 2),
    ]
    for x, kind, dk in south:
        L = Lot(x, -10.5, 0.0)
        if kind == 'A':
            inst('WK_FLR_GravelPad', L.world(0, 0)[:2] + (0,))
            dress_single_a(L, lit=(True, False, True), tv=(x > 0))
        elif kind == 'B':
            inst('WK_FLR_GravelPad', L.world(0, 0)[:2] + (0,))
            dress_single_b(L, boarded=True)
        elif kind == 'C':
            inst('WK_FLR_DirtPad', L.world(0, 0)[:2] + (0,))
            dress_double_c(L)
        elif kind == 'D':
            inst('WK_FLR_DirtPad', L.world(0, 0)[:2] + (0,))
            dress_camper_d(L)
        else:
            inst('WK_FLR_GravelPad', L.world(0, 0)[:2] + (0,))
            dress_rv(L)
        dress_yard(L, dk, w=10 if kind in 'AC' else 8, d=7.5)

    # ---------------- north side of Main Street (fronts face -Y) -----------
    north = [(-30.0, 'A', 1), (-17.0, 'C', 0), (11.0, 'B', 2), (24.0, 'A', 1)]
    for x, kind, dk in north:
        L = Lot(x, 11.0, PI)
        inst('WK_FLR_GravelPad', L.world(0, 0)[:2] + (0,))
        if kind == 'A':
            dress_single_a(L, lit=(False, True, True))
        elif kind == 'B':
            dress_single_b(L, office=True)
        else:
            dress_double_c(L, tv=False)
        dress_yard(L, dk, w=10, d=7.5)

    # ---------------- Sunset Court: laundromat + four lots -----------------
    laundry = Lot(-8.0, 15.0, -PI / 2)            # faces +X, onto the court
    inst('WK_FLR_ConcretePad', laundry.world(0, 3.2)[:2] + (0,))
    laundry.put('WK_ARCH_LaundryBlock', 0, 0)
    laundry.put('WK_LGT_NeonOpen', 2.3, 2.16, 2.35)
    laundry.put('WK_PRP_WashingMachine', -2.4, 2.9, 0, spin=0.4)
    laundry.put('WK_PRP_WashingMachine', -1.4, 3.4, 0, spin=-0.2)
    laundry.put('WK_PRP_ShoppingCart', 1.6, 3.6, 0, spin=1.2)
    laundry.put('WK_PRP_VendingMachine', 3.0, 2.1, 0)
    laundry.put('WK_PRP_PayPhone', 3.4, 3.6, 0)
    laundry.put('WK_PRP_MailboxCluster', -3.4, 4.2, 0, spin=0.1)
    laundry.put('WK_PRP_Dumpster', -4.6, -1.6, 0, spin=0.4)
    laundry.put('WK_LGT_FloodLight', 4.2, -1.8, 0, spin=-0.6)
    laundry.spill(3.4, 2.6, 2.4, 40, (1.0, 0.36, 0.72))
    laundry.spill(0.0, 2.6, 1.9, 30, (1.0, 0.82, 0.6))
    laundry.put('WK_DCL_LitterScatter', 2.0, 4.6, 0)

    court = [(11.0, 9.0, PI / 2, 'A', 0), (11.0, 22.0, PI / 2, 'B', 1),
             (-11.0, 26.0, -PI / 2, 'A', 2), (11.0, 30.0, PI / 2, 'D', 0)]
    for x, y, f, kind, dk in court:
        L = Lot(x, y, f)
        inst('WK_FLR_GravelPad', L.world(0, 0)[:2] + (0,))
        if kind == 'A':
            dress_single_a(L, lit=(True, True, False))
        elif kind == 'B':
            dress_single_b(L)
        else:
            dress_camper_d(L)
        dress_yard(L, dk, w=9, d=7.0)

    # ---------------- Sunset Row: the east branch --------------------------
    row = [(10.0, 40.0, PI, 'B', 2), (22.0, 40.0, PI, 'A', 0), (30.0, 24.0, 0.0, 'C', 1)]
    for x, y, f, kind, dk in row:
        L = Lot(x, y, f)
        inst('WK_FLR_DirtPad' if kind == 'C' else 'WK_FLR_GravelPad',
             L.world(0, 0)[:2] + (0,))
        if kind == 'A':
            dress_single_a(L, lit=(True, False, False), tv=True)
        elif kind == 'B':
            dress_single_b(L, boarded=True)
        else:
            dress_double_c(L, tv=False)
        dress_yard(L, dk, w=10, d=7.0)

    # ---------------- the burn-barrel yard (south side, near the junction) --
    fire = Lot(4.0, -6.5, 0.0)
    fire.put('WK_LGT_FireBarrel', 0, 0, 0)
    fire.put('WK_FUR_LawnChair', -1.6, 0.9, 0, spin=0.9)
    fire.put('WK_FUR_LawnChair', 1.7, 0.6, 0, spin=-1.1)
    fire.put('WK_PRP_MilkCrates', 1.2, -1.4, 0)
    fire.put('WK_PRP_OldTV', -2.2, -1.2, 0, spin=0.6)
    fire.put('WK_PRP_ClothesLine', -0.5, 3.6, 0, spin=0.1)
    fire.put('WK_VEG_WeedClump', 2.6, 2.2, 0)
    inst('WK_LGT_StringLights', (1.6, -4.0, 2.5), rot_z=0.15)
    inst('WK_PRP_TelephonePole', (-1.6, -4.4, 0), rot_z=0.1)

    # ---------------- park entry: marquee, office corner --------------------
    inst('WK_SGN_PylonSign', (-35.6, 4.6, 0), rot_z=R)
    SPILL.append(((-35.6, 2.6, 4.4), 70, (1.0, 0.45, 0.62)))
    inst('WK_SGN_SpeedLimit5', (-30.0, 4.4, 0), rot_z=R)
    inst('WK_SGN_StopSign', (4.6, -4.4, 0), rot_z=-0.4)
    inst('WK_SGN_StopSign', (4.6, 27.0, 0), rot_z=PI - 0.3)
    inst('WK_SGN_Trespass', (41.0, 4.0, 0), rot_z=-PI / 2)

    # ---------------- utility spine ----------------------------------------
    for x in (-36, -20, -4, 12, 28, 40):
        inst('WK_LGT_StreetLamp', (x, -4.4, 0))
    for x in (-28, -12, 20, 36):
        inst('WK_LGT_StreetLamp', (x, 4.4, 0), rot_z=PI)
    for y in (10, 22):
        inst('WK_LGT_StreetLamp', (4.4, y, 0), rot_z=-PI / 2)
    for x in (12, 26):
        inst('WK_LGT_StreetLamp', (x, 36.4, 0), rot_z=PI)
    for x in (-38, -26, -14, -2, 10, 22, 34):
        inst('WK_PRP_TelephonePole', (x, -6.4, 0), rot_z=0.03 * x)
    for x in (-32, -20, -8, 4, 16, 28):
        inst('WK_PRP_WireSpan', (x, -6.4, 6.9))
    for y in (14, 26):
        inst('WK_PRP_TelephonePole', (6.6, y, 0), rot_z=PI / 2)
    inst('WK_PRP_WireSpan', (6.6, 20, 6.9), rot_z=PI / 2)

    # ---------------- ditch along the south shoulder ------------------------
    for x in (-36, -28, 20, 28, 36):
        inst('WK_TER_Ditch', (x, -5.6, 0))

    # ---------------- perimeter: chain link, picket, cinder -----------------
    for x in range(-40, 41, 4):                        # north boundary
        inst('WK_WALL_Chainlink4m', (x, 45.0, 0))
    for y in range(-14, 45, 4):                        # west boundary
        inst('WK_WALL_Chainlink4m', (-43.0, y, 0), rot_z=PI / 2)
    inst('WK_WALL_ChainlinkCorner', (-43.0, 45.0, 0), rot_z=-PI / 2)
    for y in (8, 12, 16, 20):                          # east gate run
        inst('WK_WALL_Chainlink4m', (43.0, y, 0), rot_z=PI / 2)
    inst('WK_WALL_ChainlinkGate', (43.0, 5.3, 0), rot_z=PI / 2)
    for x in (-16.0, -12.0, -8.0):                     # picket between lots
        inst('WK_WALL_PicketFence4m', (x, -16.5, 0))
    for x in (8.0, 12.0):
        inst('WK_WALL_PicketFence4m', (x, 16.5, 0))
    for y in (-13.0, -9.0):
        inst('WK_WALL_PicketFence4m', (14.0, y, 0), rot_z=PI / 2)
    for x in (-24.0, -20.0):
        inst('WK_WALL_CinderWall2m', (x, 6.2, 0))
    inst('WK_WALL_CinderWall2m', (-18.0, 6.2, 0))

    # ---------------- back-of-lot service yard ------------------------------
    inst('WK_ARCH_Shed', (-38.0, 14.0, 0), rot_z=PI + 0.12)
    inst('WK_DOOR_ShedDouble', (-37.4, 12.6, 0.02), rot_z=PI + 0.12)
    inst('WK_ARCH_Shed', (30.0, 12.0, 0), rot_z=-0.2)
    inst('WK_DOOR_ShedDouble', (30.3, 10.6, 0.02), rot_z=-0.2)
    inst('WK_ARCH_Carport', (18.0, 12.0, 0))
    inst('WK_HERO_Sedan86', (18.0, 12.0, 0), rot_z=0.08)
    inst('WK_HERO_Pickup79', (-25.5, -6.0, 0), rot_z=PI - 0.06)
    inst('WK_HERO_Pickup79', (26.0, 34.5, 0), rot_z=-0.1)
    inst('WK_HERO_Sedan86', (-3.5, 22.0, 0), rot_z=PI / 2 + 0.1)
    inst('WK_ARCH_Porch', (-30.0, 7.2, 0), rot_z=PI)
    inst('WK_PRP_Dumpster', (-40.0, 19.0, 0), rot_z=0.35)
    inst('WK_PRP_Dumpster', (34.0, 18.0, 0), rot_z=-0.25)
    inst('WK_PRP_TireStack', (-39.0, 16.5, 0))
    inst('WK_PRP_TireStack', (32.5, 14.5, 0))
    inst('WK_PRP_LeaningLadder', (-36.6, 12.2, 0), rot_z=PI)
    inst('WK_LGT_FloodLight', (-34.0, 16.0, 0), rot_z=-2.2)
    inst('WK_LGT_FloodLight', (33.0, 16.0, 0), rot_z=2.5)
    inst('WK_PRP_MailboxCluster', (-33.0, 4.8, 0), rot_z=PI)
    inst('WK_PRP_ShoppingCart', (-19.0, 3.4, 0), rot_z=2.0)
    inst('WK_PRP_ShoppingCart', (27.5, 30.0, 0), rot_z=0.4)
    inst('WK_PRP_MilkCrates', (41.0, 30.0, 0))

    # ---------------- planting ---------------------------------------------
    for x, y in ((-40, 34), (-30, 38), (-16, 40), (2, 41), (16, 44), (34, 40),
                 (-42, 24), (42, 26), (-6.0, 28.0), (14.0, 6.0)):
        inst('WK_VEG_PineTree', (x, y, 0), rot_z=RNG.uniform(0, 3))
    for x, y in ((-26.0, 12.0), (8.0, -14.0), (36.0, 8.0), (-12.0, 34.0)):
        inst('WK_VEG_DeadTree', (x, y, 0), rot_z=RNG.uniform(0, 3))
    placed, guard = 0, 0
    while placed < 90 and guard < 2000:
        guard += 1
        x, y = RNG.uniform(-42, 42), RNG.uniform(-18, 45)
        if abs(y) < 4.2 or (abs(x) < 4.2 and -2 < y < 34):
            continue
        if abs(y - 32) < 4.2 and x > -2:
            continue
        inst(RNG.choice(('WK_VEG_GrassTuft', 'WK_VEG_GrassTuft', 'WK_VEG_WeedClump')),
             (x, y, -0.05), rot_z=RNG.uniform(0, PI))
        placed += 1


def spill_lights():
    n = 0
    for loc, energy, color in SPILL:
        ld = bpy.data.lights.new('spill', 'POINT')
        ld.energy = energy
        ld.color = color
        ld.shadow_soft_size = 0.4
        o = bpy.data.objects.new('SHOW_Spill_%03d' % n, ld)
        bpy.context.scene.collection.objects.link(o)
        o.location = loc
        n += 1
    return n


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

    def cam(name, loc, look, lens=35):
        cd = bpy.data.cameras.new(name)
        cd.lens = lens
        o = bpy.data.objects.new(name, cd)
        sc.collection.objects.link(o)
        o.location = loc
        trackto(o, marker(name + '_Look', look))
        return o
    cams = {
        'hero': cam('CAM_Hero', (-33.5, -3.4, 2.2), (-8, 9, 2.2), 30),
        'street': cam('CAM_Street', (33, -3.6, 1.75), (-16, 4, 2.2), 50),
        'court': cam('CAM_Court', (4.6, 5.0, 2.15), (-7.4, 15.6, 2.0), 35),
        'yard': cam('CAM_Yard', (-13.6, -2.2, 2.35), (-25.0, -10.5, 1.9), 35),
        'fire': cam('CAM_Fire', (12, -8.5, 2.3), (-14, 8, 2.4), 35),
        'aerial': cam('CAM_Aerial', (-30, -30, 30), (0, 14, 0), 28),
    }
    pano_cd = bpy.data.cameras.new('CAM_Pano')
    pano_cd.type = 'PANO'
    pano_cd.panorama_type = 'EQUIRECTANGULAR'
    pano = bpy.data.objects.new('CAM_Pano', pano_cd)
    sc.collection.objects.link(pano)
    pano.location = (-1, -2, 2.2)
    pano.rotation_euler = (PI / 2, 0, 0)
    return cams


def render_settings(sc):
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = 96
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
    nlights = spill_lights()
    cams = skycams()
    render_settings(sc)
    print('instances:', COUNT['inst'], 'spill lights:', nlights)
    with open('/home/user/World_Set/work/showcase_stats.json', 'w') as f:
        json.dump({'instances': COUNT['inst'], 'spill_lights': nlights,
                   'extent': {'x': [-43, 43], 'y': [-18, 45]},
                   'cameras': sorted(c.name for c in bpy.data.objects if c.type == 'CAMERA')},
                  f, indent=1)
    bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)
    print('saved', OUT)
    if stills:
        for key, fn in (('hero', 'showcase_hero.png'), ('street', 'showcase_street.png')):
            sc.camera = cams[key]
            sc.render.filepath = os.path.join(STILLDIR, fn)
            bpy.ops.render.render(write_still=True)
            print('still', fn)


if __name__ == '__main__':
    main(stills=os.environ.get('NOSTILLS', '') == '')
