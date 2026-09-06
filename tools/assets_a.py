#!/usr/bin/env python3
"""WORLD KIT — materials + ARCH / STR / DOOR / WINDOW / WALL / FLOOR / TERRAIN."""
from kit_lib import *  # noqa
from kit_lib import (box, cyl, cone, plane, sphere, ico, torus, tube, lamp,
                     make_mat, M, auto_uv, uv_repeat, bevel, finish)


def build_materials():
    G = 'siding_groove.png'
    make_mat('M_Siding_Mint', tex=G, tint=(0.60, 0.79, 0.70), metallic=0.35, rough=0.55)
    make_mat('M_Siding_Sand', tex=G, tint=(0.81, 0.72, 0.57), metallic=0.35, rough=0.55)
    make_mat('M_Siding_Blue', tex=G, tint=(0.52, 0.66, 0.78), metallic=0.35, rough=0.55)
    make_mat('M_Skirting', tex=G, tint=(0.40, 0.41, 0.44), metallic=0.1, rough=0.7)
    make_mat('M_Trim', base=(0.87, 0.88, 0.86, 1), metallic=0.2, rough=0.5)
    make_mat('M_Roof', base=(0.15, 0.15, 0.17, 1), metallic=0.6, rough=0.65)
    make_mat('M_Rust', tex='rust.png', rough=0.9)
    make_mat('M_Galv', tex='galv.png', metallic=0.75, rough=0.45)
    make_mat('M_Chrome', base=(0.9, 0.9, 0.92, 1), metallic=1.0, rough=0.25)
    make_mat('M_DarkMetal', base=(0.09, 0.09, 0.10, 1), metallic=0.6, rough=0.55)
    make_mat('M_Wood', tex='wood_planks.png', rough=0.85)
    make_mat('M_PoleWood', base=(0.15, 0.10, 0.07, 1), rough=0.9)
    make_mat('M_Asphalt', tex='asphalt.png', rough=0.95)
    make_mat('M_Road', tex='road_top.png', rough=0.95)
    make_mat('M_Gravel', tex='gravel.png', rough=1.0)
    make_mat('M_Concrete', tex='concrete.png', rough=0.9)
    make_mat('M_Ground', tex='grass_ground.png', rough=1.0)
    make_mat('M_Curtain', tex='curtain_lit.png', emissive='TEX', emission_strength=2.2)
    make_mat('M_GlassDark', base=(0.03, 0.05, 0.08, 1), metallic=0.9, rough=0.12)
    make_mat('M_SignPylon', tex='pylon_face.png', emissive='TEX', emission_strength=2.5)
    make_mat('M_SignVacancy', tex='vacancy.png', emissive='TEX', emission_strength=2.5)
    make_mat('M_SignTrespass', tex='trespass.png', emissive='TEX', emission_strength=0.35,
             doubleside=True)
    make_mat('M_VendFront', tex='vending_front.png', emissive='TEX', emission_strength=2.6)
    make_mat('M_BulbWarm', base=(1, 0.9, 0.75, 1), emissive=(1, 0.62, 0.28), emission_strength=5)
    make_mat('M_LampAmber', base=(1, 0.85, 0.6, 1), emissive=(1, 0.55, 0.15), emission_strength=6)
    make_mat('M_Chainlink', tex='chainlink.png', tint=(0.72, 0.74, 0.76),
             metallic=0.6, rough=0.4, alpha_mode='MASK', cutoff=0.4, doubleside=True)
    make_mat('M_Blade', tex='grass_blade.png', rough=0.9, alpha_mode='MASK', cutoff=0.4,
             doubleside=True)
    make_mat('M_Oil', tex='oil_blob.png', rough=0.35, metallic=0.2, alpha_mode='BLEND')
    make_mat('M_Puddle', tex='puddle.png', rough=0.15, metallic=0.1, alpha_mode='BLEND',
             emissive='TEX', emission_strength=0.35)
    make_mat('M_PlasticWhite', base=(0.82, 0.83, 0.80, 1), rough=0.5)
    make_mat('M_Flamingo', base=(0.93, 0.32, 0.52, 1), rough=0.55)
    make_mat('M_Tire', base=(0.03, 0.03, 0.035, 1), rough=0.95)
    make_mat('M_Couch', tex='couch_fabric.png', rough=0.95)
    make_mat('M_CarPaint', base=(0.24, 0.44, 0.46, 1), metallic=0.5, rough=0.45)
    make_mat('M_CarLightF', base=(0.70, 0.72, 0.65, 1), emissive=(0.9, 0.95, 0.8),
             emission_strength=0.6, rough=0.3)
    make_mat('M_CarLightR', base=(0.35, 0.03, 0.03, 1), emissive=(0.5, 0.05, 0.05),
             emission_strength=0.8, rough=0.3)
    make_mat('M_White', base=(0.92, 0.92, 0.90, 1), rough=0.6)
    make_mat('M_Black', base=(0.02, 0.02, 0.02, 1), rough=0.8)
    make_mat('M_DumpsterGreen', base=(0.16, 0.32, 0.20, 1), metallic=0.3, rough=0.7)
    make_mat('M_DarkRed', base=(0.35, 0.05, 0.06, 1), metallic=0.3, rough=0.5)
    make_mat('M_WasherWhite', base=(0.75, 0.76, 0.72, 1), metallic=0.4, rough=0.5)
    make_mat('M_Bush', base=(0.10, 0.16, 0.07, 1), rough=1.0)


# ================================================================= ARCH
def b_trailer(a_name, L, W, siding, win_front, win_back, door_x, shutters=False):
    """Single-wide shell. Floor at z=0.6. Front faces +Y. Recesses accept
    WK_DOOR_TrailerDoor (0.94w) and WK_WND_* (1.3w) kits."""
    o = []
    fl, wh = 0.6, 2.4
    body = box('x', (L, W, wh), (0, 0, fl + wh / 2), mat=siding)
    auto_uv(body, (4, 1.2)); o.append(body)
    o.append(box('x', (L + 0.3, W + 0.3, 0.14), (0, 0, fl + wh + 0.07), mat='M_Roof'))  # roof
    o.append(box('x', (L + 0.34, W + 0.34, 0.09), (0, 0, fl + wh - 0.02), mat='M_Trim'))  # fascia
    skirt = box('x', (L - 0.2, W - 0.2, fl + 0.04), (0, 0, (fl + 0.04) / 2 - 0.02), mat='M_Skirting')
    auto_uv(skirt, (4, 0.5)); o.append(skirt)
    o.append(box('x', (L + 0.02, W + 0.02, 0.09), (0, 0, fl + wh - 0.18), mat='M_Trim'))  # belly band
    for sx in (-1, 1):  # corner boards
        for sy in (-1, 1):
            o.append(box('x', (0.12, 0.12, wh), (sx * (L / 2 - 0.02), sy * (W / 2 - 0.02),
                                              fl + wh / 2), mat='M_Trim'))
    for i in range(3):  # roof seams + vent
        o.append(box('x', (0.06, W + 0.28, 0.03), (-L / 4 + i * L / 4, 0, fl + wh + 0.15),
                     mat='M_DarkMetal'))
    o.append(cyl('x', 0.09, 0.3, (L / 2 - 1.2, 0.5, fl + wh + 0.25), mat='M_Galv'))
    # door recess (front)
    dy = W / 2
    o.append(box('x', (1.02, 0.16, 2.14), (door_x, dy - 0.09, fl + 1.07), mat='M_Black'))
    # window recesses
    for (x, s) in [(x, 1) for x in win_front] + [(x, -1) for x in win_back]:
        o.append(box('x', (1.38, 0.16, 1.08), (x, s * (dy - 0.09), fl + 1.35), mat='M_Black'))
        if shutters and s > 0:
            for ox in (-0.85, 0.85):
                o.append(box('x', (0.28, 0.05, 1.08), (x + ox, dy + 0.015, fl + 1.35),
                             mat='M_Trim'))
    for x in (-L / 2, L / 2):  # gable-end windows
        e = box('x', (0.16, 1.1, 0.9), ((L / 2 - 0.09) * (1 if x > 0 else -1), 0, fl + 1.4), mat='M_Black')
        o.append(e)
    return o


def b_arch_trailer_a(home):
    o = b_trailer('A', 12.0, 3.6, 'M_Siding_Mint', [-4.2, -1.2, 1.6], [-3.0, 2.0], 4.2)
    return finish('WK_ARCH_Trailer_A', 'WK_ARCH', o, home=home)


def b_arch_trailer_b(home):
    o = b_trailer('B', 10.0, 3.2, 'M_Siding_Sand', [-3.4, 0.6], [-1.4, 2.6], -1.4 + 0.0,
                  shutters=True)
    # B's door sits between front windows; shift door clear of glass
    return finish('WK_ARCH_Trailer_B', 'WK_ARCH', o, home=home)


def b_arch_porch(home):
    o = []
    deck = box('x', (3.2, 2.2, 0.12), (0, 0, 0.52), mat='M_Wood')
    auto_uv(deck, (2, 1.5)); o.append(deck)
    for x in (-1.5, 1.5):
        for y in (-1.0, 1.0):
            o.append(box('x', (0.12, 0.12, 0.5), (x, y, 0.25), mat='M_Wood'))  # posts under
    for x in (-1.5, 1.5):
        for y in (-1.0, 1.0):
            o.append(box('x', (0.1, 0.1, 2.1), (x, y, 1.6), mat='M_Trim'))  # roof posts
    roof = box('x', (3.7, 2.7, 0.08), (0, 0.1, 2.72), rot=(-0.09, 0, 0), mat='M_Roof')
    o.append(roof)
    o.append(box('x', (3.7, 0.1, 0.12), (0, 1.42, 2.6), mat='M_Trim'))
    for x in (-1.5, 1.5):  # railing, street side only (steps side open)
        o.append(box('x', (0.08, 0.08, 0.85), (x, 1.0, 1.0), mat='M_Wood'))
    o.append(box('x', (3.1, 0.09, 0.09), (0, 1.0, 1.42), mat='M_Wood'))
    for i in range(7):
        o.append(box('x', (0.05, 0.05, 0.78), (-1.32 + i * 0.44, 1.0, 1.0), mat='M_Wood'))
    o.append(box('x', (3.2, 0.06, 0.46), (0, -1.08, 0.3), mat='M_Wood'))  # back skirt
    return finish('WK_ARCH_Porch', 'WK_ARCH', o, home=home)


def b_arch_shed(home):
    o = []
    L, W, H = 2.4, 1.8, 2.3
    walls = box('x', (L, W, H), (0, 0, H / 2), mat='M_Siding_Blue')
    auto_uv(walls, (1.2, 1)); o.append(walls)
    o.append(box('x', (L + 0.3, W + 0.3, 0.09), (0, 0.05, H + 0.1), rot=(-0.06, 0, 0),
                 mat='M_Roof'))
    o.append(box('x', (1.02, 0.14, 2.14), (-0.5, W / 2 - 0.09, 1.09), mat='M_Black'))  # door recess
    o.append(box('x', (1.06, 0.06, 0.08), (-0.5, W / 2 + 0.03, 2.2), mat='M_Trim'))
    o.append(box('x', (0.5, 0.1, 0.4), (0.6, W / 2 - 0.02, 1.7), mat='M_Black'))  # vent
    for i in range(3):
        o.append(box('x', (0.5, 0.04, 0.05), (0.6, W / 2 + 0.02, 1.6 + i * 0.1), mat='M_Trim'))
    for sx in (-1, 1):
        for sy in (-1, 1):
            o.append(box('x', (0.1, 0.1, H), (sx * (L / 2 - 0.02), sy * (W / 2 - 0.02), H / 2),
                         mat='M_Trim'))
    return finish('WK_ARCH_Shed', 'WK_ARCH', o, home=home)


def b_arch_carport(home):
    o = []
    roof = box('x', (5.5, 3.4, 0.09), (0, 0, 2.45), mat='M_Roof')
    o.append(roof)
    o.append(box('x', (5.6, 3.5, 0.07), (0, 0, 2.36), mat='M_Trim'))
    for x in (-2.6, 2.6):
        for y in (-1.55, 1.55):
            o.append(cyl('x', 0.055, 2.4, (x, y, 1.2), mat='M_Galv'))
    for y in (-1.55, 1.55):
        o.append(box('x', (5.4, 0.09, 0.14), (0, y, 2.28), mat='M_Galv'))
    return finish('WK_ARCH_Carport', 'WK_ARCH', o, home=home)


# ================================================================= STR
def b_str_steps(home):
    o = []
    for i in range(3):
        o.append(box('x', (1.0, 0.3, 0.07), (0, 0.45 - i * 0.29, 0.19 + i * 0.19), mat='M_Wood'))
    for s in (-1, 1):
        o.append(box('x', (0.06, 1.15, 0.1), (s * 0.5, 0.16, 0.3), rot=(0.62, 0, 0),
                     mat='M_Wood'))  # stringers
        o.append(box('x', (0.05, 0.05, 0.95), (s * 0.5, 0.62, 0.5), mat='M_Galv'))
        o.append(box('x', (0.05, 0.05, 0.6), (s * 0.5, -0.12, 0.68), mat='M_Galv'))
        o.append(box('x', (0.05, 1.1, 0.05), (s * 0.5, 0.25, 1.12), rot=(0.5, 0, 0),
                     mat='M_Galv'))  # handrail
    return finish('WK_STR_PorchSteps', 'WK_STR', o, home=home)


def b_str_pier(home):
    o = []
    c1 = box('x', (0.4, 0.2, 0.2), (0, 0, 0.1), mat='M_Concrete'); o.append(c1)
    o.append(box('x', (0.2, 0.4, 0.2), (0, 0, 0.3), mat='M_Concrete'))
    o.append(box('x', (0.44, 0.44, 0.08), (0, 0, 0.44), mat='M_Concrete'))
    auto_uv(c1, (0.5, 0.5))
    return finish('WK_STR_CinderPier', 'WK_STR', o, home=home)


def b_str_antenna(home):
    o = [cyl('x', 0.02, 1.7, (0, 0, 0.85), mat='M_DarkMetal')]
    o.append(box('x', (0.12, 0.12, 0.1), (0, 0, 0.05), mat='M_DarkMetal'))
    for i, w in enumerate((1.1, 0.85, 0.6)):
        z = 1.55 - i * 0.22
        o.append(cyl('x', 0.012, w, (0, 0, z), rot=(0, math.pi / 2, 0), mat='M_Galv'))
        o.append(cyl('x', 0.009, 0.5 - i * 0.1, (0.25 - i * 0.12, 0, z),
                     rot=(0.5, math.pi / 2, 0.3), mat='M_Galv'))
    o.append(cyl('x', 0.01, 0.9, (0, 0, 1.28), rot=(-math.pi / 2, 0, 0), mat='M_Galv'))
    return finish('WK_STR_TVAntenna', 'WK_STR', o, home=home)


def b_str_dish(home):
    o = [cyl('x', 0.035, 1.15, (0, 0, 0.575), mat='M_Galv')]
    o.append(box('x', (0.2, 0.2, 0.08), (0, 0, 0.04), mat='M_DarkMetal'))
    d = cone('x', 0.48, 0.06, 0.2, (0, 0, 1.28), rot=(0.9, 0, 0), mat='M_PlasticWhite', verts=20)
    o.append(d)
    o.append(cyl('x', 0.015, 0.5, (0, 0.28, 1.18), rot=(1.1, 0, 0), mat='M_DarkMetal'))
    o.append(box('x', (0.07, 0.14, 0.07), (0, 0.42, 1.0), mat='M_DarkMetal'))
    return finish('WK_STR_Dish', 'WK_STR', o, home=home)


# ================================================================= DOOR / WINDOW
def b_door(home):
    o = []
    o.append(box('x', (0.08, 0.1, 2.06), (-0.47, 0, 1.03), mat='M_Trim'))  # jambs
    o.append(box('x', (0.08, 0.1, 2.06), (0.47, 0, 1.03), mat='M_Trim'))
    o.append(box('x', (1.02, 0.1, 0.08), (0, 0, 2.08), mat='M_Trim'))
    slab = box('x', (0.88, 0.055, 2.0), (0, -0.01, 1.0), mat='M_Siding_Blue')
    auto_uv(slab, (0.4, 1)); o.append(slab)
    o.append(box('x', (0.5, 0.07, 0.55), (0, 0.0, 1.55), mat='M_Trim'))  # window frame
    o.append(box('x', (0.42, 0.03, 0.47), (0, -0.01, 1.55), mat='M_Black'))  # pane backing
    o.append(plane('x', 0.42, 0.47, (0, 0.012, 1.55), rot=(math.pi / 2, 0, math.pi),
                   mat='M_Curtain'))  # lit pane
    o.append(box('x', (0.86, 0.065, 0.18), (0, 0.0, 0.14), mat='M_Galv'))  # kick plate
    o.append(sphere('x', 0.035, (0.36, 0.06, 1.02), mat='M_Chrome', seg=10, ring=8))  # knob
    o.append(box('x', (0.05, 0.02, 0.12), (0.36, 0.035, 1.02), mat='M_Chrome'))
    return finish('WK_DOOR_TrailerDoor', 'WK_DOOR', o, home=home)


def _window(o, glass):
    o.append(box('x', (0.09, 0.1, 1.02), (-0.65, 0, 0.51), mat='M_Trim'))
    o.append(box('x', (0.09, 0.1, 1.02), (0.65, 0, 0.51), mat='M_Trim'))
    o.append(box('x', (1.39, 0.1, 0.09), (0, 0, 0.045), mat='M_Trim'))
    o.append(box('x', (1.39, 0.1, 0.09), (0, 0, 0.975), mat='M_Trim'))
    o.append(box('x', (1.5, 0.16, 0.07), (0, 0.02, -0.02), mat='M_Trim'))  # sill
    g = plane('x', 1.21, 0.85, (0, 0.01, 0.51), rot=(math.pi / 2, 0, math.pi), mat=glass)
    o.append(g)
    o.append(box('x', (0.045, 0.06, 0.85), (0, 0.02, 0.51), mat='M_Trim'))  # mullions
    o.append(box('x', (1.21, 0.06, 0.045), (0, 0.02, 0.51), mat='M_Trim'))
    return o


def b_wnd_lit(home):
    return finish('WK_WND_WindowLit', 'WK_WND', _window([], 'M_Curtain'), home=home)


def b_wnd_dark(home):
    return finish('WK_WND_WindowDark', 'WK_WND', _window([], 'M_GlassDark'), home=home)


# ================================================================= WALL
def b_wall_chainlink(home):
    o = []
    for x in (-2, 2):
        o.append(cyl('x', 0.05, 1.6, (x, 0, 0.8), mat='M_Galv'))
        o.append(sphere('x', 0.06, (x, 0, 1.62), mat='M_Galv', seg=8, ring=6))
    o.append(cyl('x', 0.03, 4.0, (0, 0, 1.5), rot=(0, math.pi / 2, 0), mat='M_Galv'))
    mesh = plane('x', 4.0, 1.4, (0, 0, 0.78), rot=(-math.pi / 2, 0, 0), mat='M_Chainlink')
    uv_repeat(mesh, 10, 3.4)
    o.append(mesh)
    return finish('WK_WALL_Chainlink4m', 'WK_WALL', o, home=home)


def b_wall_gate(home):
    o = []
    for x in (-0.65, 0.65):
        o.append(cyl('x', 0.05, 1.6, (x, 0, 0.8), mat='M_Galv'))
    o.append(box('x', (1.2, 0.05, 0.05), (0, 0, 1.42), mat='M_Galv'))
    o.append(box('x', (1.2, 0.05, 0.05), (0, 0, 0.18), mat='M_Galv'))
    o.append(box('x', (0.05, 0.05, 1.3), (-0.58, 0, 0.8), mat='M_Galv'))
    o.append(box('x', (0.05, 0.05, 1.3), (0.58, 0, 0.8), mat='M_Galv'))
    mesh = plane('x', 1.1, 1.18, (0, 0, 0.8), rot=(-math.pi / 2, 0, 0), mat='M_Chainlink')
    uv_repeat(mesh, 2.8, 2.9)
    o.append(mesh)
    o.append(box('x', (0.06, 0.1, 0.12), (0.58, 0.05, 1.0), mat='M_DarkMetal'))  # latch
    return finish('WK_WALL_ChainlinkGate', 'WK_WALL', o, home=home)


# ================================================================= FLOOR / TERRAIN
def _pad(name, cat, w, h, t, mat, rep, home):
    top = box('x', (w, h, t), (0, 0, -t / 2), mat=mat)
    auto_uv(top, rep)
    return finish(name, cat, [top], home=home)


def b_flr_gravel(home):
    return _pad('WK_FLR_GravelPad', 'WK_FLR', 8, 8, 0.1, 'M_Gravel', (4, 4), home)


def b_flr_concrete(home):
    return _pad('WK_FLR_ConcretePad', 'WK_FLR', 4, 4, 0.12, 'M_Concrete', (2, 2), home)


def b_ter_road(home):
    o = [box('x', (8, 6, 0.1), (0, 0, -0.051), mat='M_Asphalt')]
    o.append(plane('x', 8, 6, (0, 0, 0.0), mat='M_Road'))
    return finish('WK_TER_RoadStraight', 'WK_TER', o, home=home)


def b_ter_grass(home):
    return _pad('WK_TER_GrassPatch', 'WK_TER', 6, 6, 0.08, 'M_Ground', (3, 3), home)
