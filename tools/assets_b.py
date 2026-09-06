#!/usr/bin/env python3
"""WORLD KIT — FURNITURE / PROPS / LIGHTS / SIGNAGE / VEGETATION / DECALS / HERO."""
from kit_lib import *  # noqa
from kit_lib import (box, cyl, cone, plane, sphere, ico, torus, tube, lamp,
                     M, auto_uv, uv_repeat, bevel, finish)


# ================================================================= FURNITURE
def b_fur_chair(home):
    o = []
    P = 'M_PlasticWhite'
    o.append(box('x', (0.46, 0.44, 0.05), (0, 0, 0.43), mat=P))
    for x in (-0.19, 0.19):
        for y in (-0.18, 0.18):
            o.append(cyl('x', 0.022, 0.43, (x, y, 0.215), mat=P))
    back = box('x', (0.46, 0.05, 0.55), (0, -0.23, 0.72), rot=(-0.12, 0, 0), mat=P)
    o.append(back)
    for i in range(3):  # back slats
        o.append(box('x', (0.4, 0.03, 0.09), (0, -0.245 + 0.0, 0.58 + i * 0.14),
                     rot=(-0.12, 0, 0), mat=P))
    for x in (-0.24, 0.24):
        o.append(box('x', (0.05, 0.4, 0.04), (x, -0.02, 0.62), mat=P))
        o.append(box('x', (0.04, 0.04, 0.2), (x, 0.16, 0.52), mat=P))
    return finish('WK_FUR_LawnChair', 'WK_FUR', o, home=home)


def b_fur_picnic(home):
    o = []
    W = 'M_Wood'
    top = box('x', (1.8, 0.72, 0.07), (0, 0, 0.75), mat=W)
    auto_uv(top, (1, 0.5)); o.append(top)
    for y in (-0.62, 0.62):
        o.append(box('x', (1.8, 0.24, 0.06), (0, y, 0.46), mat=W))
    for x in (-0.7, 0.7):
        for s in (-1, 1):
            o.append(box('x', (0.07, 0.07, 1.05), (x, s * 0.3, 0.4), rot=(s * 0.5, 0, 0), mat=W))
    o.append(box('x', (1.5, 0.06, 0.06), (0, 0, 0.62), mat=W))
    return finish('WK_FUR_PicnicTable', 'WK_FUR', o, home=home)


def b_fur_couch(home):
    o = []
    C = 'M_Couch'
    base = box('x', (1.9, 0.8, 0.35), (0, 0, 0.28), mat=C)
    auto_uv(base, (1, 1)); o.append(base)
    for x in (-0.47, 0.47):
        c = box('x', (0.9, 0.68, 0.16), (x, 0.02, 0.53), mat=C)
        bevel(c, 0.04, 2); o.append(c)
    back = box('x', (1.9, 0.24, 0.62), (0, -0.32, 0.72), mat=C); o.append(back)
    for x in (-0.47, 0.47):
        c = box('x', (0.88, 0.18, 0.5), (x, -0.22, 0.78), rot=(-0.1, 0, 0), mat=C)
        bevel(c, 0.04, 2); o.append(c)
    for x in (-0.99, 0.99):
        o.append(box('x', (0.2, 0.8, 0.55), (x, 0, 0.38), mat=C))
    for x in (-0.85, 0.85):
        for y in (-0.3, 0.3):
            o.append(cyl('x', 0.03, 0.12, (x, y, 0.06), mat='M_PoleWood'))
    return finish('WK_FUR_PorchCouch', 'WK_FUR', o, home=home)


# ================================================================= PROPS
def b_prp_trashcan(home):
    o = []
    body = cone('x', 0.30, 0.24, 0.72, (0, 0, 0.38), mat='M_Galv', verts=16)
    o.append(body)
    for z in (0.3, 0.55):
        o.append(cyl('x', 0.285 if z > 0.4 else 0.265, 0.03, (0, 0, z), mat='M_Galv'))
    o.append(cyl('x', 0.32, 0.06, (0, 0, 0.77), mat='M_Galv'))  # lid
    o.append(box('x', (0.16, 0.05, 0.05), (0, 0, 0.83), mat='M_DarkMetal'))
    for s in (-1, 1):
        o.append(box('x', (0.04, 0.1, 0.08), (s * 0.3, 0, 0.55), mat='M_DarkMetal'))
    return finish('WK_PRP_TrashCan', 'WK_PRP', o, home=home)


def b_prp_tires(home):
    o = []
    for i in range(3):
        o.append(torus('x', 0.30, 0.125, (0, 0, 0.125 + i * 0.24), mat='M_Tire'))
    return finish('WK_PRP_TireStack', 'WK_PRP', o, home=home)


def _flamingo(o, dx, rot):
    import math as _m
    P = 'M_Flamingo'
    b = sphere('x', 0.16, (dx, 0, 0.62), mat=P, scale=(1.0, 1.45, 0.9)); o.append(b)
    tail = cone('x', 0.07, 0.01, 0.18, (dx, -0.22, 0.68), rot=(-0.9, 0, 0), mat=P); o.append(tail)
    n = tube('x', [(dx, 0.2, 0.66), (dx, 0.3, 0.86), (dx, 0.24, 1.0), (dx, 0.3, 1.08)],
             0.028, mat=P)
    o.append(n)
    o.append(sphere('x', 0.05, (dx, 0.31, 1.09), mat=P, seg=10, ring=8))
    o.append(cone('x', 0.025, 0.005, 0.12, (dx, 0.31, 1.03), rot=(_m.pi, 0, 0), mat='M_Black'))
    o.append(cyl('x', 0.008, 0.58, (dx + 0.03, 0.02, 0.29), mat='M_Black'))
    o.append(cyl('x', 0.008, 0.58, (dx - 0.03, -0.02, 0.29), mat='M_Black'))
    return o


def b_prp_flamingo(home):
    o = _flamingo([], 0.0, 0)
    o = _flamingo(o, 0.55, 0)
    return finish('WK_PRP_Flamingo', 'WK_PRP', o, home=home)


def b_prp_washer(home):
    o = []
    W = 'M_WasherWhite'
    body = box('x', (0.7, 0.66, 0.92), (0, 0, 0.5), mat=W)
    bevel(body, 0.015, 2); o.append(body)
    o.append(box('x', (0.72, 0.68, 0.06), (0, 0, 0.99), mat=W))  # lid
    o.append(box('x', (0.7, 0.2, 0.14), (0, -0.2, 1.06), mat=W))  # backsplash
    for x in (-0.15, 0.0, 0.15):
        o.append(cyl('x', 0.025, 0.03, (x, -0.09, 1.06), rot=(-math.pi / 2, 0, 0),
                     mat='M_Black'))
    o.append(box('x', (0.71, 0.5, 0.2), (0, 0.06, 0.14), mat='M_Rust'))  # rusted base
    return finish('WK_PRP_WashingMachine', 'WK_PRP', o, home=home)


def b_prp_vending(home):
    o = []
    o.append(box('x', (1.0, 0.85, 1.9), (0, 0, 0.95), mat='M_DarkRed'))
    o.append(box('x', (1.02, 0.87, 0.08), (0, 0, 1.86), mat='M_DarkMetal'))
    o.append(box('x', (1.02, 0.87, 0.1), (0, 0, 0.05), mat='M_Black'))
    front = plane('x', 0.9, 1.66, (0, 0.428, 0.98), rot=(math.pi / 2, 0, math.pi), mat='M_VendFront')
    o.append(front)
    for i in range(3):  # side vents
        o.append(box('x', (0.02, 0.4, 0.04), (0.51, 0, 0.6 + i * 0.12), mat='M_Black'))
    li = [lamp('x', 'POINT', (0, 1.1, 1.2), energy=50, color=(0.7, 0.85, 1.0))]
    return finish('WK_PRP_VendingMachine', 'WK_PRP', o, lights=li, home=home)


def b_prp_pole(home):
    o = []
    P = 'M_PoleWood'
    o.append(cone('x', 0.11, 0.15, 7.5, (0, 0, 3.75), mat=P, verts=10))
    o.append(box('x', (2.2, 0.12, 0.14), (0, 0, 6.85), mat=P))
    for x in (-0.9, -0.3, 0.3, 0.9):
        o.append(cyl('x', 0.035, 0.1, (x, 0, 6.97), mat='M_PlasticWhite'))
    o.append(cyl('x', 0.3, 0.85, (0.35, 0, 5.7), mat='M_Galv'))  # transformer
    o.append(box('x', (0.1, 0.1, 0.3), (0.35, 0, 6.25), mat='M_DarkMetal'))
    for z in (2.2, 3.4, 4.6):  # pole steps
        o.append(box('x', (0.2, 0.04, 0.04), (0, 0.12, z), mat='M_DarkMetal'))
    guy = cyl('x', 0.015, 4.4, (1.05, 0, 2.4), rot=(0, 0.5, 0), mat='M_DarkMetal')
    o.append(guy)
    o.append(box('x', (0.3, 0.3, 0.25), (2.05, 0, 0.1), mat='M_Concrete'))
    return finish('WK_PRP_TelephonePole', 'WK_PRP', o, home=home)


def b_prp_wire(home):
    o = []
    for y in (-0.25, 0.25):
        o.append(tube('x', [(-6, y, 0), (-3, y, -0.62), (0, y, -0.9), (3, y, -0.62), (6, y, 0)],
                      0.02, mat='M_Black', smooth=False))
    return finish('WK_PRP_WireSpan', 'WK_PRP', o, home=home)


def b_prp_dumpster(home):
    o = []
    G = 'M_DumpsterGreen'
    body = box('x', (2.0, 1.05, 1.05), (0, 0, 0.68), mat=G)
    bevel(body, 0.02, 2); o.append(body)
    o.append(box('x', (0.95, 1.0, 0.07), (-0.49, 0, 1.24), mat='M_DarkMetal'))
    lid2 = box('x', (0.95, 1.0, 0.07), (0.49, -0.02, 1.3), rot=(-0.14, 0, 0), mat='M_DarkMetal')
    o.append(lid2)
    for x in (-0.7, 0.7):
        o.append(box('x', (0.12, 1.1, 0.5), (x, 0, 0.85), mat='M_DarkMetal'))  # fork pockets
    for x in (-0.85, 0.85):
        for y in (-0.42, 0.42):
            o.append(cyl('x', 0.07, 0.06, (x, y, 0.07), mat='M_Black'))
    for x in (-0.4, 0.3):  # rust streaks
        o.append(box('x', (0.18, 0.02, 0.5), (x, 0.53, 0.6), mat='M_Rust'))
    return finish('WK_PRP_Dumpster', 'WK_PRP', o, home=home)


# ================================================================= LIGHTS
def b_lgt_street(home):
    o = []
    o.append(cyl('x', 0.09, 7.0, (0, 0, 3.5), mat='M_DarkMetal'))
    o.append(cyl('x', 0.35, 0.5, (0, 0, 0.25), mat='M_Concrete', verts=10))
    o.append(cyl('x', 0.06, 1.4, (0, 0.6, 6.92), rot=(-math.pi / 2, 0, 0), mat='M_DarkMetal'))
    o.append(box('x', (0.32, 0.8, 0.16), (0, 1.25, 6.85), mat='M_DarkMetal'))
    lens = plane('x', 0.26, 0.6, (0, 1.25, 6.76), mat='M_LampAmber')
    lens.rotation_euler = (math.pi, 0, 0)
    o.append(lens)
    li = [lamp('x', 'SPOT', (0, 1.25, 6.7), energy=1400, color=(1, 0.6, 0.25),
               spot_size=1.0, spot_blend=0.4),
          lamp('x', 'POINT', (0, 1.25, 6.5), energy=180, color=(1, 0.62, 0.3))]
    return finish('WK_LGT_StreetLamp', 'WK_LGT', o, lights=li, home=home)


def b_lgt_porch(home):
    o = []
    o.append(box('x', (0.14, 0.05, 0.22), (0, 0, 0.11), mat='M_DarkMetal'))
    o.append(box('x', (0.12, 0.12, 0.05), (0, 0.05, 0.24), mat='M_DarkMetal'))
    pane = box('x', (0.1, 0.09, 0.14), (0, 0.05, 0.12), mat='M_BulbWarm')
    o.append(pane)
    li = [lamp('x', 'POINT', (0, 0.22, 0.12), energy=40, color=(1, 0.7, 0.42))]
    return finish('WK_LGT_PorchLight', 'WK_LGT', o, lights=li, home=home)


def b_lgt_string(home):
    o = []
    pts = [(-3, 0, 0), (-1.5, 0, -0.4), (0, 0, -0.55), (1.5, 0, -0.4), (3, 0, 0)]
    o.append(tube('x', pts, 0.012, mat='M_Black', smooth=False))
    for i in range(12):
        x = -2.75 + i * 0.5
        t = abs(x) / 3.0
        z = -0.55 * (1 - t * t) - 0.1
        o.append(cyl('x', 0.012, 0.06, (x, 0, z + 0.05), mat='M_Black'))
        o.append(sphere('x', 0.035, (x, 0, z), mat='M_BulbWarm', seg=8, ring=6))
    li = [lamp('x', 'POINT', (0, 0, -0.3), energy=25, color=(1, 0.65, 0.35))]
    return finish('WK_LGT_StringLights', 'WK_LGT', o, lights=li, home=home)


# ================================================================= SIGNAGE
def b_sgn_pylon(home):
    o = []
    for x in (-1.3, 1.3):
        o.append(cyl('x', 0.09, 3.6, (x, 0, 1.8), mat='M_DarkMetal'))
        o.append(box('x', (0.5, 0.5, 0.35), (x, 0, 0.17), mat='M_Concrete'))
    o.append(box('x', (3.6, 0.35, 1.5), (0, 0, 4.35), mat='M_DarkMetal'))
    for s in (-1, 1):
        f = plane('x', 3.5, 1.4, (0, s * 0.18, 4.35),
                  rot=(math.pi / 2, 0, math.pi if s > 0 else 0), mat='M_SignPylon')
        o.append(f)
    o.append(box('x', (1.7, 0.25, 0.6), (0, 0, 3.15), mat='M_DarkMetal'))
    for s in (-1, 1):
        f = plane('x', 1.6, 0.5, (0, s * 0.135, 3.15),
                  rot=(math.pi / 2, 0, math.pi if s > 0 else 0), mat='M_SignVacancy')
        o.append(f)
    return finish('WK_SGN_PylonSign', 'WK_SGN', o, home=home)


def b_sgn_trespass(home):
    o = []
    o.append(box('x', (0.09, 0.09, 1.6), (0, 0, 0.8), mat='M_PoleWood'))
    o.append(plane('x', 0.62, 0.4, (0, 0, 1.32), rot=(math.pi / 2, 0, math.pi), mat='M_SignTrespass'))
    return finish('WK_SGN_Trespass', 'WK_SGN', o, home=home)


# ================================================================= VEGETATION
def b_veg_bush(home):
    o = []
    B = 'M_Bush'
    o.append(ico('x', 0.55, (0, 0, 0.45), mat=B, scale=(1.2, 1.0, 0.75)))
    o.append(ico('x', 0.4, (0.45, 0.15, 0.35), mat=B, scale=(1.0, 0.9, 0.7)))
    o.append(ico('x', 0.35, (-0.42, -0.1, 0.32), mat=B, scale=(1.0, 1.0, 0.7)))
    for a in (0.4, 2.4, 4.4):
        o.append(cyl('x', 0.015, 0.5, (0.2 * math.cos(a), 0.2 * math.sin(a), 0.55),
                     rot=(0.3 * math.sin(a), 0.3 * math.cos(a), 0), mat='M_PoleWood'))
    return finish('WK_VEG_ScrubBush', 'WK_VEG', o, home=home)


def b_veg_deadtree(home):
    o = []
    P = 'M_PoleWood'
    o.append(cone('x', 0.09, 0.16, 3.0, (0, 0, 1.5), mat=P, verts=8))
    branches = [((1.1, 0, 2.7), (0, -0.85, 0), 2.1), ((-0.95, 0.25, 3.1), (0.15, 0.9, 0), 1.9),
                ((0.15, 1.0, 3.4), (-0.85, 0, 0), 1.8), ((-0.2, -0.9, 3.0), (0.8, 0.1, 0), 1.7),
                ((0.45, -0.4, 4.0), (-0.5, -0.5, 0), 1.5), ((-0.4, 0.45, 4.2), (0.45, 0.45, 0), 1.3),
                ((0.0, 0.0, 4.6), (0.1, 0.0, 0), 1.2)]
    for (loc, rot, ln) in branches:
        o.append(cone('x', 0.012, 0.045, ln, loc, rot=rot, mat=P, verts=6))
    o.append(cone('x', 0.012, 0.05, 1.1, (0.05, 0, 4.9), rot=(0.08, 0, 0), mat=P, verts=6))
    return finish('WK_VEG_DeadTree', 'WK_VEG', o, home=home)


def b_veg_tuft(home):
    o = []
    for a in (0, math.pi / 3, 2 * math.pi / 3):
        p = plane('x', 0.55, 0.42, (0, 0, 0.2), rot=(math.pi / 2, 0, a), mat='M_Blade')
        o.append(p)
    return finish('WK_VEG_GrassTuft', 'WK_VEG', o, home=home)


# ================================================================= DECALS
def b_dcl_oil(home):
    o = [plane('x', 1.6, 1.2, (0, 0, 0.012), mat='M_Oil')]
    return finish('WK_DCL_OilStain', 'WK_DCL', o, home=home)


def b_dcl_puddle(home):
    o = [plane('x', 2.3, 1.7, (0, 0, 0.012), mat='M_Puddle')]
    return finish('WK_DCL_Puddle', 'WK_DCL', o, home=home)


# ================================================================= HERO
def b_hero_sedan(home):
    o = []
    CP = 'M_CarPaint'
    lower = box('x', (4.4, 1.76, 0.62), (0, 0, 0.62), mat=CP)
    bevel(lower, 0.09, 3); o.append(lower)
    cabin = box('x', (2.15, 1.6, 0.52), (-0.25, 0, 1.16), mat='M_GlassDark')
    bevel(cabin, 0.08, 3); o.append(cabin)
    roof = box('x', (1.9, 1.62, 0.07), (-0.25, 0, 1.44), mat=CP)
    bevel(roof, 0.03, 2); o.append(roof)
    hood = box('x', (1.15, 1.7, 0.1), (1.6, 0, 0.95), mat=CP)
    bevel(hood, 0.04, 2); o.append(hood)
    trunk = box('x', (0.95, 1.7, 0.1), (-1.7, 0, 0.95), mat=CP)
    bevel(trunk, 0.04, 2); o.append(trunk)
    for x, z in [(2.16, 0.55), (-2.16, 0.55)]:  # bumpers
        b = box('x', (0.18, 1.84, 0.16), (x, 0, z), mat='M_Chrome')
        bevel(b, 0.03, 2); o.append(b)
    for x in (-1.45, 1.45):  # wheels
        for y in (-0.82, 0.82):
            o.append(cyl('x', 0.33, 0.22, (x, y, 0.33), rot=(-math.pi / 2, 0, 0), mat='M_Tire',
                         verts=18))
            o.append(cyl('x', 0.15, 0.23, (x, y, 0.33), rot=(-math.pi / 2, 0, 0), mat='M_Galv',
                         verts=12))
    for y in (-0.55, 0.55):  # headlights / taillights
        o.append(box('x', (0.06, 0.34, 0.16), (2.21, y, 0.78), mat='M_CarLightF'))
        o.append(box('x', (0.06, 0.3, 0.14), (-2.21, y, 0.78), mat='M_CarLightR'))
    o.append(box('x', (0.1, 1.5, 0.12), (2.2, 0, 0.55), mat='M_Black'))  # grille
    for y in (-0.95, 0.95):  # mirrors
        o.append(box('x', (0.08, 0.12, 0.08), (0.55, y, 1.15), mat='M_Black'))
    for x in (-1.0, 1.2):  # rust rockers + patches
        o.append(box('x', (1.1, 1.78, 0.12), (x, 0, 0.36), mat='M_Rust'))
    o.append(box('x', (0.5, 0.02, 0.2), (1.85, 0.89, 0.62), mat='M_Rust'))
    o.append(box('x', (0.02, 0.32, 0.16), (-2.26, 0.3, 0.55), mat='M_White'))  # plate
    return finish('WK_HERO_Sedan86', 'WK_HERO', o, home=home)
