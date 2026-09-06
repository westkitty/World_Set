#!/usr/bin/env python3
"""WORLD KIT v2 "DOUBLE" — the 41 assets that grow the kit from 40 to 81.

Same rules as v1: metric scale, fronts face +Y, origin at the ground-projected
base centre with z = 0 on the contact plane, shared material families, chunky
low-poly with softened edges, night-first readability.
"""
import math
from kit_lib import *  # noqa
from kit_lib import (box, cyl, cone, plane, sphere, ico, torus, tube, lamp,
                     make_mat, M, auto_uv, uv_repeat, bevel, finish)

PI = math.pi


def build_materials_v2():
    """Everything v2 adds to the material library (v1 families stay untouched)."""
    # masonry / board
    make_mat('M_Cinderblock', tex='cinderblock.png', rough=0.95)
    make_mat('M_CinderPaint', tex='cinderblock.png', tint=(0.78, 0.74, 0.64), rough=0.9)
    make_mat('M_Plywood', tex='plywood.png', tint=(0.52, 0.47, 0.42), rough=0.95)
    make_mat('M_Dirt', tex='dirt.png', rough=1.0)
    # soft goods
    make_mat('M_Fabric', tex='fabric.png', rough=0.95)
    make_mat('M_Upholstery', base=(0.36, 0.28, 0.20, 1), rough=0.95)
    # metals / plastics
    make_mat('M_Aluminium', base=(0.62, 0.64, 0.66, 1), metallic=0.9, rough=0.35)
    make_mat('M_PlasticRed', base=(0.55, 0.10, 0.10, 1), rough=0.45)
    make_mat('M_PlasticBlue', base=(0.13, 0.24, 0.48, 1), rough=0.45)
    make_mat('M_PlasticYellow', base=(0.68, 0.56, 0.10, 1), rough=0.45)
    make_mat('M_PlasticGreen', base=(0.14, 0.34, 0.20, 1), rough=0.45)
    # glass / light
    make_mat('M_ScreenGlass', base=(0.05, 0.07, 0.09, 1), metallic=0.7, rough=0.2)
    make_mat('M_CurtainTV', tex='curtain_tv.png', emissive='TEX', emission_strength=2.6)
    make_mat('M_FloodLens', base=(0.9, 0.92, 0.88, 1), emissive=(0.95, 0.97, 0.9),
             emission_strength=7)
    make_mat('M_FireGlow', base=(1.0, 0.55, 0.16, 1), emissive=(1.0, 0.42, 0.10),
             emission_strength=9)
    make_mat('M_NeonOpen', tex='neon_open.png', emissive='TEX', emission_strength=3.4)
    # signage
    make_mat('M_SignStop', tex='sign_stop.png', rough=0.6, alpha_mode='MASK', cutoff=0.5,
             doubleside=True, emissive='TEX', emission_strength=0.25)
    make_mat('M_SignSpeed', tex='sign_speed.png', rough=0.6, emissive='TEX',
             emission_strength=0.22, doubleside=True)
    make_mat('M_SignLot', tex='sign_lot.png', rough=0.7, doubleside=True)
    make_mat('M_SignOffice', tex='sign_office.png', emissive='TEX', emission_strength=2.4)
    make_mat('M_SignLaundry', tex='sign_laundry.png', rough=0.7, emissive='TEX',
             emission_strength=0.3, doubleside=True)
    make_mat('M_Plate', tex='plate.png', rough=0.6, doubleside=True)
    # alpha trims
    make_mat('M_Screen', tex='screen_mesh.png', alpha_mode='MASK', cutoff=0.35,
             rough=0.8, doubleside=True)
    make_mat('M_Pine', tex='pine_bough.png', alpha_mode='MASK', cutoff=0.4, rough=0.9,
             doubleside=True)
    make_mat('M_Weeds', tex='weeds.png', alpha_mode='MASK', cutoff=0.4, rough=0.95,
             doubleside=True)
    make_mat('M_Litter', tex='litter.png', alpha_mode='MASK', cutoff=0.35, rough=0.9,
             doubleside=True)
    make_mat('M_TireTracks', tex='tire_tracks.png', alpha_mode='BLEND', rough=0.95,
             doubleside=True)
    # vehicles
    make_mat('M_TruckPaint', base=(0.42, 0.55, 0.52, 1), metallic=0.5, rough=0.45)
    make_mat('M_RVCream', base=(0.80, 0.77, 0.68, 1), metallic=0.3, rough=0.5)
    make_mat('M_RVStripe', tex='rv_flank.png', metallic=0.3, rough=0.5)
    make_mat('M_CamperCream', base=(0.78, 0.76, 0.70, 1), metallic=0.35, rough=0.5)
    make_mat('M_CamperTeal', base=(0.20, 0.42, 0.44, 1), metallic=0.35, rough=0.5)
    # road paint
    make_mat('M_LineYellow', base=(0.52, 0.42, 0.10, 1), rough=0.9)
    make_mat('M_LineWhite', base=(0.62, 0.62, 0.58, 1), rough=0.9)


# ================================================================= ARCHITECTURE
def b_arch_trailer_c_double(home):
    """14 x 7 m double-wide: two shells married on a centre seam. Front = +Y."""
    o = []
    L, W, fl, wh = 14.0, 7.0, 0.62, 2.5
    for i, (yc, sid) in enumerate(((-1.75, 'M_Siding_Sand'), (1.75, 'M_Siding_Mint'))):
        b = box('x', (L, W / 2, wh), (0, yc, fl + wh / 2), mat=sid)
        auto_uv(b, (5, 1.2))
        o.append(b)
    o.append(box('x', (L + 0.4, W + 0.4, 0.16), (0, 0, fl + wh + 0.08), mat='M_Roof'))
    o.append(box('x', (L + 0.44, W + 0.44, 0.1), (0, 0, fl + wh - 0.03), mat='M_Trim'))
    o.append(box('x', (L + 0.1, 0.18, 0.22), (0, 0, fl + wh + 0.2), mat='M_Roof'))  # ridge cap
    sk = box('x', (L - 0.25, W - 0.25, fl + 0.04), (0, 0, (fl + 0.04) / 2 - 0.02),
             mat='M_Skirting')
    auto_uv(sk, (5, 0.5))
    o.append(sk)
    o.append(box('x', (L + 0.02, W + 0.02, 0.1), (0, 0, fl + wh - 0.2), mat='M_Trim'))
    for sx in (-1, 1):
        for sy in (-1, 1):
            o.append(box('x', (0.14, 0.14, wh), (sx * (L / 2 - 0.03), sy * (W / 2 - 0.03),
                                                 fl + wh / 2), mat='M_Trim'))
    dy = W / 2
    for dx in (-4.6, 3.4):                      # two door recesses
        o.append(box('x', (1.04, 0.18, 2.16), (dx, dy - 0.1, fl + 1.08), mat='M_Black'))
    for x in (-6.0, -2.4, 0.6, 5.4):            # front windows
        o.append(box('x', (1.4, 0.18, 1.1), (x, dy - 0.1, fl + 1.4), mat='M_Black'))
    for x in (-4.0, 1.0, 4.6):                  # back windows
        o.append(box('x', (1.4, 0.18, 1.1), (x, -dy + 0.1, fl + 1.4), mat='M_Black'))
    for s in (-1, 1):                           # gable-end glazing
        o.append(box('x', (0.18, 1.2, 0.95), (s * (L / 2 - 0.1), 1.6, fl + 1.45), mat='M_Black'))
    for i in range(4):                          # roof seams + vents
        o.append(box('x', (0.07, W + 0.34, 0.035), (-L / 3 + i * L / 4.5, 0, fl + wh + 0.17),
                     mat='M_DarkMetal'))
    for x, y in ((-4.5, 1.6), (3.8, -1.4)):
        o.append(cyl('x', 0.1, 0.34, (x, y, fl + wh + 0.3), mat='M_Galv'))
    o.append(box('x', (0.9, 0.9, 0.36), (5.6, 2.2, fl + wh + 0.3), mat='M_Galv'))  # cooler pad
    return finish('WK_ARCH_Trailer_C_Double', 'WK_ARCH', o, home=home)


def b_arch_trailer_d_camper(home):
    """A little 7 m travel trailer, cream over teal, still on its wheels."""
    o = []
    L, W, fl, wh = 7.0, 2.6, 0.72, 1.86
    body = box('x', (L, W, wh), (0, 0, fl + wh / 2), mat='M_CamperCream')
    bevel(body, 0.18, 3)
    o.append(body)
    belt = box('x', (L + 0.02, W + 0.02, 0.42), (0, 0, fl + 0.34), mat='M_CamperTeal')
    bevel(belt, 0.1, 2)
    o.append(belt)
    o.append(box('x', (L - 0.4, W + 0.06, 0.06), (0, 0, fl + 0.62), mat='M_Aluminium'))
    roof = box('x', (L - 0.1, W - 0.08, 0.12), (0, 0, fl + wh + 0.02), mat='M_Aluminium')
    bevel(roof, 0.06, 2)
    o.append(roof)
    o.append(box('x', (0.6, 0.6, 0.14), (-1.2, 0, fl + wh + 0.1), mat='M_White'))  # vent
    o.append(box('x', (0.9, 0.06, 1.72), (1.9, W / 2 - 0.02, fl + 0.9), mat='M_CamperCream'))
    o.append(box('x', (0.78, 0.05, 0.5), (1.9, W / 2 + 0.02, fl + 1.32), mat='M_GlassDark'))
    for x in (-2.1, 0.1):                       # side windows
        o.append(box('x', (1.1, 0.06, 0.62), (x, W / 2 - 0.01, fl + 1.22), mat='M_Trim'))
        o.append(plane('x', 0.98, 0.5, (x, W / 2 + 0.03, fl + 1.22), rot=(PI / 2, 0, PI),
                       mat='M_Curtain'))
    o.append(box('x', (1.0, 0.05, 0.5), (-2.6, -W / 2 - 0.01, fl + 1.24), mat='M_GlassDark'))
    for x in (-0.4, 0.4):                       # axle + wheels
        o.append(cyl('x', 0.31, 0.2, (x, -W / 2 + 0.16, 0.31), rot=(PI / 2, 0, 0),
                     mat='M_Tire', verts=16))
        o.append(cyl('x', 0.31, 0.2, (x, W / 2 - 0.16, 0.31), rot=(PI / 2, 0, 0),
                     mat='M_Tire', verts=16))
    o.append(box('x', (1.6, W - 0.3, 0.14), (0, 0, 0.6), mat='M_DarkMetal'))
    o.append(box('x', (1.4, 0.12, 0.16), (L / 2 + 0.5, 0, 0.52), mat='M_Galv'))   # tongue
    o.append(cyl('x', 0.07, 0.5, (L / 2 + 1.05, 0, 0.3), mat='M_Galv'))
    o.append(box('x', (0.5, 1.9, 0.05), (0.6, W / 2 + 0.9, fl + wh - 0.05),
                 rot=(0.12, 0, 0), mat='M_Fabric'))                              # awning
    for y in (W / 2 + 1.7,):
        o.append(cyl('x', 0.035, 2.1, (0.35, y, 1.05), mat='M_Aluminium'))
        o.append(cyl('x', 0.035, 2.1, (0.85, y, 1.05), mat='M_Aluminium'))
    return finish('WK_ARCH_Trailer_D_Camper', 'WK_ARCH', o, home=home)


def b_arch_laundry_block(home):
    """6.4 x 4.2 m cinderblock utility building: laundromat + park office."""
    o = []
    L, W, H = 6.4, 4.2, 2.9
    walls = box('x', (L, W, H), (0, 0, H / 2), mat='M_Cinderblock')
    auto_uv(walls, (3, 1.4))
    o.append(walls)
    o.append(box('x', (L + 0.24, W + 0.24, 0.22), (0, 0, H + 0.11), mat='M_Roof'))
    o.append(box('x', (L + 0.3, W + 0.3, 0.12), (0, 0, H + 0.24), mat='M_Trim'))  # parapet cap
    o.append(box('x', (L + 0.02, 0.1, 0.5), (0, W / 2, H - 0.25), mat='M_CinderPaint'))
    for dx in (-1.9, 1.9):                      # two doors
        o.append(box('x', (1.06, 0.16, 2.12), (dx, W / 2 - 0.08, 1.06), mat='M_Black'))
        o.append(box('x', (0.9, 0.06, 1.94), (dx, W / 2 - 0.01, 1.0), mat='M_Aluminium'))
        o.append(plane('x', 0.72, 1.5, (dx, W / 2 + 0.03, 1.16), rot=(PI / 2, 0, PI),
                       mat='M_Curtain'))
    o.append(box('x', (2.0, 0.14, 1.0), (0, W / 2 - 0.06, 1.6), mat='M_Black'))   # window band
    o.append(plane('x', 1.86, 0.88, (0, W / 2 + 0.02, 1.6), rot=(PI / 2, 0, PI), mat='M_Curtain'))
    for mx in (-0.62, 0.0, 0.62):                                                # mullions
        o.append(box('x', (0.06, 0.06, 0.9), (mx, W / 2 + 0.03, 1.6), mat='M_Trim'))
    o.append(box('x', (1.94, 0.06, 0.06), (0, W / 2 + 0.03, 1.6), mat='M_Trim'))
    o.append(box('x', (2.06, 0.1, 0.08), (0, W / 2 + 0.02, 2.11), mat='M_Trim'))
    o.append(box('x', (2.6, 0.1, 0.9), (0, -W / 2 + 0.05, 1.7), mat='M_Plywood'))  # boarded rear
    sign = plane('x', 1.9, 0.95, (-1.3, W / 2 + 0.05, 2.35), rot=(PI / 2, 0, PI),
                 mat='M_SignLaundry')
    o.append(sign)
    o.append(box('x', (2.0, 0.09, 1.05), (-1.3, W / 2 + 0.01, 2.35), mat='M_Trim'))
    o.append(box('x', (L - 0.6, 1.0, 0.08), (0, W / 2 + 0.5, H - 0.05), mat='M_Roof'))
    for x in (-2.4, 2.4):
        o.append(cyl('x', 0.05, 1.0, (x, W / 2 + 0.92, H - 0.55), mat='M_DarkMetal'))
    o.append(cyl('x', 0.34, 0.5, (2.1, -W / 2 - 0.4, 0.25), mat='M_Galv'))        # utility drum
    o.append(box('x', (0.9, 0.5, 0.7), (-2.3, -W / 2 - 0.3, 0.35), mat='M_Galv'))
    li = [lamp('x', 'POINT', (0, W / 2 - 0.5, 1.9), energy=110, color=(1, 0.86, 0.66)),
          lamp('x', 'POINT', (-1.3, W / 2 + 0.5, 2.35), energy=60, color=(1, 0.7, 0.4))]
    return finish('WK_ARCH_LaundryBlock', 'WK_ARCH', o, lights=li, home=home)


# ================================================================= STRUCTURAL
def b_str_hitch(home):
    """A-frame tongue with coupler, jack and a bottle rack — the piece that says
    'this building has wheels'. Origin at the hitch ball, points +Y."""
    o = []
    for s in (-1, 1):
        o.append(box('x', (0.12, 2.3, 0.14), (s * 0.42, -1.15, 0.52), rot=(0, 0, s * -0.17),
                     mat='M_Galv'))
    o.append(box('x', (0.28, 0.6, 0.16), (0, 0.18, 0.52), mat='M_Galv'))
    o.append(box('x', (0.2, 0.24, 0.2), (0, 0.42, 0.5), mat='M_DarkMetal'))       # coupler
    o.append(cyl('x', 0.05, 0.5, (0, 0.06, 0.3), mat='M_Galv'))                   # jack post
    o.append(cyl('x', 0.09, 0.05, (0, 0.06, 0.06), rot=(PI / 2, 0, 0), mat='M_Tire', verts=12))
    o.append(box('x', (0.09, 0.24, 0.09), (0.14, 0.06, 0.62), mat='M_DarkMetal'))  # crank
    o.append(box('x', (0.62, 0.5, 0.05), (0, -0.34, 0.6), mat='M_Galv'))          # bottle tray
    for s in (-1, 1):
        o.append(cyl('x', 0.13, 0.56, (s * 0.16, -0.34, 0.9), mat='M_White', verts=14))
        o.append(cone('x', 0.13, 0.05, 0.14, (s * 0.16, -0.34, 1.24), mat='M_White', verts=14))
        o.append(cyl('x', 0.05, 0.08, (s * 0.16, -0.34, 1.33), mat='M_Galv', verts=10))
    o.append(cyl('x', 0.012, 0.7, (0, -0.34, 1.28), rot=(0, PI / 2, 0), mat='M_Black', verts=8))
    o.append(box('x', (0.03, 0.6, 0.03), (0.3, -0.6, 0.62), mat='M_Rust'))
    return finish('WK_STR_HitchTongue', 'WK_STR', o, home=home)


def b_str_ac_window(home):
    """Window air-conditioner. Origin sits on the sill; unit faces +Y (outside)."""
    o = []
    body = box('x', (0.62, 0.5, 0.4), (0, 0, 0.2), mat='M_WasherWhite')
    bevel(body, 0.02, 2)
    o.append(body)
    o.append(box('x', (0.64, 0.04, 0.42), (0, 0.25, 0.2), mat='M_Galv'))          # grille frame
    o.append(box('x', (0.56, 0.02, 0.34), (0, 0.26, 0.2), mat='M_Black'))         # dark recess
    for i in range(9):                                   # condenser fins
        o.append(box('x', (0.022, 0.03, 0.32), (-0.24 + i * 0.06, 0.27, 0.2),
                     mat='M_Aluminium'))
    o.append(cyl('x', 0.1, 0.02, (0, 0.275, 0.2), rot=(PI / 2, 0, 0), mat='M_DarkMetal',
                 verts=12))                                                        # fan hub
    o.append(box('x', (0.66, 0.1, 0.05), (0, 0.02, -0.02), mat='M_Galv'))         # sill bracket
    for s in (-1, 1):
        o.append(box('x', (0.05, 0.28, 0.22), (s * 0.3, 0.12, -0.12), rot=(0.5, 0, 0),
                     mat='M_Galv'))
    o.append(box('x', (0.5, 0.02, 0.06), (0, 0.3, 0.02), mat='M_Rust'))           # drip stain
    return finish('WK_STR_ACWindowUnit', 'WK_STR', o, home=home)


def b_str_swamp_cooler(home):
    """Roof-mounted evaporative cooler. Origin = roof contact."""
    o = []
    b = box('x', (0.95, 0.95, 0.8), (0, 0, 0.42), mat='M_Galv')
    bevel(b, 0.03, 2)
    o.append(b)
    o.append(box('x', (1.02, 1.02, 0.08), (0, 0, 0.86), mat='M_Galv'))
    o.append(cyl('x', 0.12, 0.14, (0, 0, 0.94), mat='M_DarkMetal', verts=12))
    for s, ax in ((1, 'y'), (-1, 'y'), (1, 'x'), (-1, 'x')):
        if ax == 'y':
            o.append(box('x', (0.72, 0.02, 0.56), (0, s * 0.47, 0.42), mat='M_Black'))
        else:
            o.append(box('x', (0.02, 0.72, 0.56), (s * 0.47, 0, 0.42), mat='M_Black'))
        for i in range(6):                                # louvre slats, inset
            z = 0.18 + i * 0.1
            if ax == 'y':
                o.append(box('x', (0.7, 0.05, 0.05), (0, s * 0.475, z), rot=(0.5 * s, 0, 0),
                             mat='M_Aluminium'))
            else:
                o.append(box('x', (0.05, 0.7, 0.05), (s * 0.475, 0, z), rot=(0, -0.5 * s, 0),
                             mat='M_Aluminium'))
    o.append(box('x', (1.15, 1.15, 0.1), (0, 0, 0.05), mat='M_Wood'))             # curb
    o.append(cyl('x', 0.05, 0.4, (0.4, -0.4, 0.2), mat='M_Rust', verts=10))
    o.append(box('x', (0.3, 0.02, 0.2), (-0.2, 0.5, 0.4), mat='M_Rust'))
    return finish('WK_STR_SwampCooler', 'WK_STR', o, home=home)


def b_str_propane(home):
    o = []
    o.append(cyl('x', 0.23, 1.05, (0, 0, 0.56), mat='M_White', verts=18))
    o.append(sphere('x', 0.23, (0, 0, 1.08), mat='M_White', scale=(1, 1, 0.55), seg=18, ring=8))
    o.append(cyl('x', 0.25, 0.06, (0, 0, 0.06), mat='M_Galv', verts=18))
    o.append(cyl('x', 0.1, 0.16, (0, 0, 1.22), mat='M_Galv', verts=12))           # collar
    o.append(torus('x', 0.11, 0.02, (0, 0, 1.3), mat='M_Galv', major_seg=14, minor_seg=6))
    o.append(box('x', (0.1, 0.1, 0.1), (0.06, 0.06, 1.24), mat='M_DarkMetal'))    # valve
    o.append(cyl('x', 0.015, 0.5, (0.2, 0.2, 0.9), rot=(0.5, 0.4, 0), mat='M_Black', verts=8))
    o.append(box('x', (0.5, 0.5, 0.1), (0, 0, 0.02), mat='M_Concrete'))
    o.append(box('x', (0.16, 0.02, 0.2), (0, 0.23, 0.62), mat='M_Rust'))
    return finish('WK_STR_PropaneTank', 'WK_STR', o, home=home)


# ================================================================= DOORS
def b_door_screen(home):
    """Aluminium screen door — swaps into the same 0.94 x 2.04 opening."""
    o = []
    for x in (-0.47, 0.47):
        o.append(box('x', (0.06, 0.06, 2.04), (x, 0, 1.02), mat='M_Aluminium'))
    for z in (0.02, 2.02):
        o.append(box('x', (1.0, 0.06, 0.06), (0, 0, z), mat='M_Aluminium'))
    o.append(box('x', (1.0, 0.05, 0.05), (0, 0, 0.86), mat='M_Aluminium'))        # mid rail
    o.append(box('x', (0.88, 0.03, 0.78), (0, 0, 0.45), mat='M_Aluminium'))       # kick panel
    mesh = plane('x', 0.88, 1.1, (0, 0.005, 1.44), rot=(PI / 2, 0, PI), mat='M_Screen')
    uv_repeat(mesh, 9, 11)
    o.append(mesh)
    o.append(box('x', (0.06, 0.05, 0.3), (0.34, 0.05, 1.0), mat='M_Aluminium'))   # handle
    o.append(cyl('x', 0.018, 0.34, (0.1, 0.09, 1.62), rot=(0, PI / 2, 0), mat='M_Aluminium',
                 verts=8))                                                        # closer
    o.append(box('x', (0.05, 0.04, 0.08), (-0.44, 0.06, 1.62), mat='M_DarkMetal'))
    return finish('WK_DOOR_ScreenDoor', 'WK_DOOR', o, home=home)


def b_door_shed_double(home):
    o = []
    for s in (-1, 1):
        leaf = box('x', (0.78, 0.05, 1.94), (s * 0.4, 0, 0.97), mat='M_Plywood')
        auto_uv(leaf, (0.5, 1))
        o.append(leaf)
        o.append(box('x', (0.8, 0.03, 0.09), (s * 0.4, 0.035, 1.86), mat='M_Wood'))
        o.append(box('x', (0.8, 0.03, 0.09), (s * 0.4, 0.035, 0.1), mat='M_Wood'))
        o.append(box('x', (0.09, 0.03, 1.9), (s * 0.75, 0.035, 0.97), mat='M_Wood'))
        o.append(box('x', (0.08, 0.03, 2.05), (s * 0.4, 0.04, 0.97), rot=(0, s * 0.38, 0),
                     mat='M_Wood'))                                              # Z brace
        for z in (0.35, 1.6):
            o.append(box('x', (0.09, 0.05, 0.12), (s * 0.79, 0.02, z), mat='M_DarkMetal'))
    o.append(box('x', (0.14, 0.06, 0.1), (0, 0.05, 1.05), mat='M_Galv'))          # hasp
    o.append(cyl('x', 0.035, 0.05, (0, 0.1, 1.0), rot=(PI / 2, 0, 0), mat='M_DarkMetal',
                 verts=10))
    o.append(box('x', (1.7, 0.08, 0.09), (0, -0.02, 2.02), mat='M_Trim'))
    return finish('WK_DOOR_ShedDouble', 'WK_DOOR', o, home=home)


# ================================================================= WINDOWS
def b_wnd_boarded(home):
    o = []
    o.append(box('x', (0.09, 0.1, 1.02), (-0.65, 0, 0.51), mat='M_Trim'))
    o.append(box('x', (0.09, 0.1, 1.02), (0.65, 0, 0.51), mat='M_Trim'))
    o.append(box('x', (1.39, 0.1, 0.09), (0, 0, 0.045), mat='M_Trim'))
    o.append(box('x', (1.39, 0.1, 0.09), (0, 0, 0.975), mat='M_Trim'))
    o.append(box('x', (1.5, 0.16, 0.07), (0, 0.02, -0.02), mat='M_Trim'))
    o.append(box('x', (1.22, 0.04, 0.86), (0, 0, 0.51), mat='M_Black'))
    for i, (z, r) in enumerate(((0.30, 0.05), (0.62, -0.04), (0.88, 0.02))):
        p = box('x', (1.34, 0.035, 0.26), (0, 0.04, z), rot=(0, r, 0), mat='M_Plywood')
        auto_uv(p, (1, 0.3))
        o.append(p)
    for x, z in ((-0.5, 0.3), (0.5, 0.3), (-0.5, 0.62), (0.5, 0.62)):
        o.append(cyl('x', 0.012, 0.02, (x, 0.06, z), rot=(PI / 2, 0, 0), mat='M_DarkMetal',
                     verts=6))
    return finish('WK_WND_WindowBoarded', 'WK_WND', o, home=home)


def b_wnd_tv_lit(home):
    """The blue window: a TV going in an otherwise dark room."""
    o = []
    o.append(box('x', (0.09, 0.1, 1.02), (-0.65, 0, 0.51), mat='M_Trim'))
    o.append(box('x', (0.09, 0.1, 1.02), (0.65, 0, 0.51), mat='M_Trim'))
    o.append(box('x', (1.39, 0.1, 0.09), (0, 0, 0.045), mat='M_Trim'))
    o.append(box('x', (1.39, 0.1, 0.09), (0, 0, 0.975), mat='M_Trim'))
    o.append(box('x', (1.5, 0.16, 0.07), (0, 0.02, -0.02), mat='M_Trim'))
    g = plane('x', 1.21, 0.85, (0, 0.012, 0.51), rot=(PI / 2, 0, PI), mat='M_CurtainTV')
    o.append(g)
    o.append(box('x', (0.045, 0.06, 0.85), (0, 0.022, 0.51), mat='M_Trim'))
    o.append(box('x', (1.21, 0.06, 0.045), (0, 0.022, 0.51), mat='M_Trim'))
    for s in (-1, 1):                            # half-drawn blind
        o.append(box('x', (0.58, 0.02, 0.3), (s * 0.3, 0.03, 0.82), mat='M_White'))
    li = [lamp('x', 'POINT', (0, 0.5, 0.6), energy=45, color=(0.45, 0.62, 1.0))]
    return finish('WK_WND_WindowTVLit', 'WK_WND', o, lights=li, home=home)


# ================================================================= WALLS
def b_wall_chainlink_corner(home):
    """Corner post with a 2 m arm to -X and a 2 m arm to +Y."""
    o = []
    o.append(cyl('x', 0.055, 1.65, (0, 0, 0.82), mat='M_Galv'))
    o.append(sphere('x', 0.065, (0, 0, 1.67), mat='M_Galv', seg=8, ring=6))
    o.append(cyl('x', 0.05, 1.6, (-2.0, 0, 0.8), mat='M_Galv'))
    o.append(cyl('x', 0.05, 1.6, (0, 2.0, 0.8), mat='M_Galv'))
    o.append(cyl('x', 0.03, 2.0, (-1.0, 0, 1.5), rot=(0, PI / 2, 0), mat='M_Galv'))
    o.append(cyl('x', 0.03, 2.0, (0, 1.0, 1.5), rot=(PI / 2, 0, 0), mat='M_Galv'))
    m1 = plane('x', 2.0, 1.4, (-1.0, 0, 0.78), rot=(-PI / 2, 0, 0), mat='M_Chainlink')
    uv_repeat(m1, 5, 3.4)
    o.append(m1)
    m2 = plane('x', 2.0, 1.4, (0, 1.0, 0.78), rot=(-PI / 2, 0, PI / 2), mat='M_Chainlink')
    uv_repeat(m2, 5, 3.4)
    o.append(m2)
    o.append(cyl('x', 0.02, 1.5, (-0.9, 0.9, 0.9), rot=(0.5, 0, -0.78), mat='M_Galv', verts=8))
    return finish('WK_WALL_ChainlinkCorner', 'WK_WALL', o, home=home)


def b_wall_picket(home):
    """4 m of tired picket fence: three posts, two rails, 21 pickets, one gap."""
    o = []
    for x in (-2.0, 0.0, 2.0):
        o.append(box('x', (0.09, 0.09, 1.15), (x, 0, 0.55), mat='M_Wood'))
    for z in (0.34, 0.88):
        r = box('x', (4.0, 0.05, 0.09), (0, 0.02, z), mat='M_Wood')
        auto_uv(r, (4, 0.4))
        o.append(r)
    lean = (0.0, 0.05, -0.03, 0.0, 0.02, -0.06)
    for i in range(21):
        x = -1.9 + i * 0.19
        if i in (7, 13):                      # missing pickets
            continue
        p = box('x', (0.1, 0.03, 0.98), (x, 0.05, 0.5), rot=(0, lean[i % 6], 0), mat='M_Wood')
        o.append(p)
        o.append(box('x', (0.1, 0.03, 0.06), (x, 0.05, 0.99), rot=(0, lean[i % 6], 0.6),
                     mat='M_Wood'))
    return finish('WK_WALL_PicketFence4m', 'WK_WALL', o, home=home)


def b_wall_cinder(home):
    o = []
    w = box('x', (2.0, 0.24, 0.9), (0, 0, 0.45), mat='M_Cinderblock')
    auto_uv(w, (2, 0.9))
    o.append(w)
    o.append(box('x', (2.06, 0.3, 0.07), (0, 0, 0.93), mat='M_Concrete'))
    o.append(box('x', (2.1, 0.34, 0.06), (0, 0, 0.03), mat='M_Concrete'))
    o.append(box('x', (0.5, 0.26, 0.3), (0.6, 0, 0.28), mat='M_CinderPaint'))     # patch job
    return finish('WK_WALL_CinderWall2m', 'WK_WALL', o, home=home)


# ================================================================= FLOORS / TERRAIN
def b_flr_dirt(home):
    t = box('x', (8, 8, 0.1), (0, 0, -0.05), mat='M_Dirt')
    auto_uv(t, (3, 3))
    return finish('WK_FLR_DirtPad', 'WK_FLR', [t], home=home)


def b_ter_road_corner(home):
    """8 x 8 corner tile: the carriageway turns from -X to +Y."""
    o = [box('x', (8, 8, 0.1), (0, 0, -0.051), mat='M_Asphalt')]
    top = plane('x', 8, 8, (0, 0, 0), mat='M_Road')
    uv_repeat(top, 1, 1.2)
    o.append(top)
    for i in range(9):                          # curved centre dashes
        a = i * (PI / 2) / 8
        r = 3.0
        x, y = -r * math.cos(a), r * math.sin(a)
        if i % 2:
            continue
        o.append(box('x', (0.5, 0.14, 0.02), (x, y, 0.012), rot=(0, 0, a), mat='M_LineYellow'))
    for r, mat in ((3.9, 'M_LineWhite'),):      # outer edge line
        for i in range(11):
            a = i * (PI / 2) / 10
            o.append(box('x', (0.42, 0.1, 0.02), (-r * math.cos(a), r * math.sin(a), 0.012),
                         rot=(0, 0, a), mat=mat))
    o.append(box('x', (0.9, 0.9, 0.03), (2.6, -2.6, 0.015), mat='M_Concrete'))    # drain apron
    o.append(box('x', (0.5, 0.5, 0.02), (2.6, -2.6, 0.03), mat='M_DarkMetal'))
    return finish('WK_TER_RoadCorner', 'WK_TER', o, home=home)


def b_ter_road_tee(home):
    """8 x 6 straight with a spur running +Y."""
    o = [box('x', (8, 6, 0.1), (0, 0, -0.051), mat='M_Asphalt')]
    o.append(plane('x', 8, 6, (0, 0, 0), mat='M_Road'))
    o.append(box('x', (6, 4, 0.1), (0, 4.9, -0.051), mat='M_Asphalt'))
    o.append(plane('x', 6, 4, (0, 4.9, 0), mat='M_Road'))
    for i in range(4):                          # dashes on the through road
        for s in (-1, 1):
            o.append(box('x', (0.7, 0.14, 0.02), (s * (1.2 + i * 1.6), 0, 0.012),
                         mat='M_LineYellow'))
    o.append(box('x', (0.16, 3.4, 0.02), (0, 3.6, 0.012), mat='M_LineWhite'))     # spur centre
    o.append(box('x', (5.6, 0.16, 0.02), (0, 2.0, 0.012), mat='M_LineWhite'))     # stop bar
    return finish('WK_TER_RoadTee', 'WK_TER', o, home=home)


def b_ter_ditch(home):
    """8 m of shoulder ditch: two sloped banks, a wet bottom and weeds."""
    o = []
    for s in (-1, 1):
        b = plane('x', 8.0, 1.5, (0, s * 1.05, -0.22), rot=(s * 0.42, 0, 0), mat='M_Ground')
        uv_repeat(b, 4, 1)
        o.append(b)
    bottom = plane('x', 8.0, 0.9, (0, 0, -0.5), mat='M_Dirt')
    uv_repeat(bottom, 4, 0.5)
    o.append(bottom)
    o.append(plane('x', 7.4, 0.5, (0, 0, -0.49), mat='M_Puddle'))
    for i in range(10):
        x = -3.6 + i * 0.8
        w = plane('x', 0.6, 0.5, (x, (-1) ** i * 0.7, -0.34), rot=(PI / 2, 0, 0.4 * i),
                  mat='M_Weeds')
        o.append(w)
    o.append(cyl('x', 0.24, 1.2, (2.6, 0, -0.36), rot=(0, PI / 2, 0), mat='M_DarkMetal',
                 verts=12))                                                       # culvert
    return finish('WK_TER_Ditch', 'WK_TER', o, home=home)


# ================================================================= FURNITURE
def b_fur_plastic_table(home):
    o = []
    top = cyl('x', 0.5, 0.05, (0, 0, 0.72), mat='M_PlasticWhite', verts=20)
    o.append(top)
    o.append(torus('x', 0.49, 0.02, (0, 0, 0.69), mat='M_PlasticWhite', major_seg=20,
                   minor_seg=6))
    for i in range(4):
        a = i * PI / 2 + PI / 4
        x, y = 0.34 * math.cos(a), 0.34 * math.sin(a)
        o.append(cyl('x', 0.028, 0.7, (x, y, 0.35), rot=(0.06 * math.cos(a), 0.06 * math.sin(a), 0),
                     mat='M_PlasticWhite', verts=8))
    o.append(cyl('x', 0.04, 0.06, (0, 0, 0.66), mat='M_PlasticWhite', verts=10))  # parasol hole
    o.append(box('x', (0.3, 0.22, 0.02), (0.12, -0.1, 0.75), mat='M_Fabric'))     # newspaper
    return finish('WK_FUR_PlasticTable', 'WK_FUR', o, home=home)


def b_fur_recliner(home):
    """The armchair that lives outside now. Front = +Y."""
    o = []
    seat = box('x', (0.92, 0.86, 0.26), (0, 0, 0.36), mat='M_Upholstery')
    bevel(seat, 0.07, 2)
    o.append(seat)
    back = box('x', (0.92, 0.24, 0.78), (0, -0.4, 0.72), rot=(-0.18, 0, 0), mat='M_Upholstery')
    bevel(back, 0.07, 2)
    o.append(back)
    for s in (-1, 1):
        a = box('x', (0.2, 0.86, 0.3), (s * 0.42, 0.0, 0.6), mat='M_Upholstery')
        bevel(a, 0.06, 2)
        o.append(a)
    cush = box('x', (0.78, 0.72, 0.14), (0, 0.02, 0.54), mat='M_Fabric')
    bevel(cush, 0.05, 2)
    o.append(cush)
    o.append(box('x', (0.86, 0.8, 0.12), (0, 0, 0.17), mat='M_Black'))
    for sx in (-1, 1):
        for sy in (-1, 1):
            o.append(box('x', (0.08, 0.08, 0.12), (sx * 0.38, sy * 0.34, 0.06), mat='M_Wood'))
    o.append(box('x', (0.3, 0.16, 0.03), (0.2, 0.3, 0.62), rot=(0, 0, 0.4), mat='M_Fabric'))
    return finish('WK_FUR_Recliner', 'WK_FUR', o, home=home)


def b_fur_kettle_grill(home):
    o = []
    bowl = sphere('x', 0.29, (0, 0, 0.62), mat='M_Black', scale=(1, 1, 0.62), seg=18, ring=10)
    o.append(bowl)
    lid = sphere('x', 0.3, (0, 0, 0.72), mat='M_DarkRed', scale=(1, 1, 0.5), seg=18, ring=8)
    o.append(lid)
    o.append(cyl('x', 0.05, 0.05, (0, 0, 0.87), mat='M_Black', verts=10))
    o.append(torus('x', 0.3, 0.015, (0, 0, 0.66), mat='M_Chrome', major_seg=20, minor_seg=6))
    for i in range(3):
        a = i * 2 * PI / 3 + 0.4
        x, y = 0.24 * math.cos(a), 0.24 * math.sin(a)
        o.append(cyl('x', 0.016, 0.62, (x, y, 0.31), rot=(0.13 * math.sin(a), -0.13 * math.cos(a), 0),
                     mat='M_DarkMetal', verts=8))
    for s in (-1, 1):
        o.append(cyl('x', 0.08, 0.04, (s * 0.26, -0.18, 0.08), rot=(0, PI / 2, 0),
                     mat='M_Black', verts=12))
    o.append(box('x', (0.24, 0.03, 0.02), (0.34, 0.1, 0.66), mat='M_Wood'))       # handle
    o.append(cyl('x', 0.12, 0.06, (0.42, -0.3, 0.03), mat='M_Galv', verts=12))    # ash pan
    return finish('WK_FUR_KettleGrill', 'WK_FUR', o, home=home)


# ================================================================= PROPS
def b_prp_mailbox_cluster(home):
    """Six boxes on a shared rail — the park's mail point. Doors face +Y."""
    o = []
    for x in (-0.75, 0.75):
        o.append(box('x', (0.1, 0.1, 1.15), (x, 0, 0.57), mat='M_Wood'))
    o.append(box('x', (1.8, 0.12, 0.1), (0, 0, 1.1), mat='M_Wood'))
    o.append(box('x', (1.8, 0.12, 0.08), (0, 0, 0.6), mat='M_Wood'))
    cols = ['M_Galv', 'M_PlasticRed', 'M_Galv', 'M_PlasticBlue', 'M_Rust', 'M_Galv']
    for i in range(6):
        x = -0.7 + (i % 3) * 0.7
        z = 1.28 if i < 3 else 0.78
        b = box('x', (0.24, 0.42, 0.2), (x, 0, z), mat=cols[i])
        bevel(b, 0.05, 2)
        o.append(b)
        o.append(box('x', (0.2, 0.02, 0.16), (x, 0.22, z), mat='M_DarkMetal'))    # door
        o.append(box('x', (0.03, 0.1, 0.12), (x + 0.14, 0.1, z + 0.12), mat='M_PlasticRed'))
    o.append(box('x', (0.5, 0.3, 0.06), (0, 0.08, 0.06), mat='M_Concrete'))
    return finish('WK_PRP_MailboxCluster', 'WK_PRP', o, home=home)


def b_prp_payphone(home):
    """Pedestal payphone with a lit hood. Faces +Y."""
    o = []
    o.append(cyl('x', 0.06, 1.25, (0, 0, 0.62), mat='M_Galv'))
    o.append(cyl('x', 0.16, 0.06, (0, 0, 0.03), mat='M_Concrete', verts=14))
    body = box('x', (0.4, 0.24, 0.62), (0, 0.02, 1.45), mat='M_Galv')
    bevel(body, 0.02, 2)
    o.append(body)
    o.append(box('x', (0.44, 0.3, 0.3), (0, 0.03, 1.9), mat='M_DarkMetal'))       # hood
    o.append(plane('x', 0.34, 0.2, (0, 0.19, 1.9), rot=(PI / 2, 0, PI), mat='M_SignOffice'))
    o.append(box('x', (0.3, 0.03, 0.34), (0, 0.14, 1.5), mat='M_Black'))          # keypad plate
    for r in range(4):
        for c in range(3):
            o.append(box('x', (0.05, 0.02, 0.04), (-0.08 + c * 0.08, 0.16, 1.62 - r * 0.06),
                         mat='M_PlasticWhite'))
    o.append(box('x', (0.07, 0.1, 0.26), (-0.24, 0.06, 1.5), mat='M_Black'))      # handset
    o.append(cyl('x', 0.012, 0.3, (-0.2, 0.08, 1.25), rot=(0.3, 0, 0), mat='M_Black', verts=6))
    o.append(box('x', (0.3, 0.02, 0.12), (0, 0.13, 1.2), mat='M_Trim'))           # shelf
    li = [lamp('x', 'POINT', (0, 0.3, 1.86), energy=28, color=(0.6, 0.78, 1.0))]
    return finish('WK_PRP_PayPhone', 'WK_PRP', o, lights=li, home=home)


def b_prp_shopping_cart(home):
    """Abandoned cart. Basket is a wire grid; handle faces -Y."""
    o = []
    for i in range(7):                        # basket sides as wires
        x = -0.24 + i * 0.08
        o.append(cyl('x', 0.008, 0.62, (x, 0, 0.62), rot=(PI / 2, 0, 0), mat='M_Chrome', verts=6))
    for i in range(5):
        z = 0.42 + i * 0.11
        o.append(cyl('x', 0.008, 0.52, (0, 0.3, z), rot=(0, PI / 2, 0), mat='M_Chrome', verts=6))
        o.append(cyl('x', 0.008, 0.52, (0, -0.3, z), rot=(0, PI / 2, 0), mat='M_Chrome', verts=6))
    for s in (-1, 1):
        for i in range(4):
            y = -0.24 + i * 0.16
            o.append(cyl('x', 0.008, 0.5, (s * 0.26, y, 0.62), rot=(0, 0.04, 0),
                         mat='M_Chrome', verts=6))
    o.append(box('x', (0.54, 0.62, 0.02), (0, 0, 0.38), mat='M_Chrome'))          # basket floor
    o.append(box('x', (0.54, 0.02, 0.24), (0, -0.32, 0.74), mat='M_PlasticRed'))  # flap
    o.append(cyl('x', 0.02, 0.56, (0, -0.34, 0.9), rot=(0, PI / 2, 0), mat='M_PlasticRed',
                 verts=8))                                                        # handle
    for s in (-1, 1):
        o.append(cyl('x', 0.012, 0.5, (s * 0.26, -0.3, 0.66), rot=(-0.35, 0, 0),
                     mat='M_Chrome', verts=6))
        o.append(cyl('x', 0.012, 0.42, (s * 0.24, 0.14, 0.2), rot=(0.2, 0, 0),
                     mat='M_Chrome', verts=6))
    for sx in (-1, 1):
        for sy in (-1, 1):
            o.append(cyl('x', 0.045, 0.03, (sx * 0.22, sy * 0.24, 0.05), rot=(0, PI / 2, 0),
                         mat='M_Black', verts=10))
    return finish('WK_PRP_ShoppingCart', 'WK_PRP', o, home=home)


def b_prp_kid_bike(home):
    """A kid's BMX dropped on its side in the yard."""
    o = []
    for y in (-0.42, 0.42):                    # wheels lying flat
        o.append(torus('x', 0.28, 0.028, (0, y, 0.28), rot=(PI / 2, 0, 0), mat='M_Tire',
                       major_seg=20, minor_seg=6))
        o.append(cyl('x', 0.04, 0.05, (0, y, 0.28), rot=(PI / 2, 0, 0), mat='M_Chrome', verts=10))
        for i in range(6):
            a = i * PI / 3
            o.append(cyl('x', 0.005, 0.52, (0.13 * math.cos(a), y, 0.28 + 0.13 * math.sin(a)),
                         rot=(PI / 2, 0, 0), mat='M_Chrome', verts=4))
    for p0, p1, r, m in ((( 0.0, -0.42, 0.28), (0.0, 0.1, 0.5), 0.02, 'M_PlasticRed'),
                         (( 0.0, 0.42, 0.28), (0.0, 0.1, 0.5), 0.02, 'M_PlasticRed'),
                         (( 0.0, 0.1, 0.5), (0.0, -0.1, 0.22), 0.02, 'M_PlasticRed'),
                         (( 0.0, -0.1, 0.22), (0.0, -0.42, 0.28), 0.018, 'M_PlasticRed')):
        o.append(tube('x', [p0, p1], r, mat=m, smooth=False))
    o.append(cyl('x', 0.018, 0.44, (0, 0.42, 0.52), rot=(0, PI / 2, 0), mat='M_Chrome', verts=8))
    for s in (-1, 1):
        o.append(cyl('x', 0.02, 0.1, (s * 0.2, 0.42, 0.52), rot=(0, PI / 2, 0), mat='M_Black',
                     verts=8))
    o.append(box('x', (0.09, 0.24, 0.05), (0, 0.02, 0.56), mat='M_Black'))        # saddle
    o.append(cyl('x', 0.012, 0.2, (0, 0.02, 0.44), mat='M_Chrome', verts=8))
    o.append(cyl('x', 0.06, 0.02, (0, -0.02, 0.24), rot=(0, PI / 2, 0), mat='M_Chrome', verts=10))
    return finish('WK_PRP_KidBike', 'WK_PRP', o, home=home)


def b_prp_leaning_ladder(home):
    """Aluminium extension ladder leaning against a wall (top at +Y)."""
    o = []
    lean = 0.32
    for s in (-1, 1):
        o.append(box('x', (0.05, 0.06, 3.4), (s * 0.22, 0.52, 1.62), rot=(lean, 0, 0),
                     mat='M_Aluminium'))
    for i in range(11):
        t = i / 10.0
        z = 0.16 + t * 3.1
        y = 0.02 + t * 3.1 * math.tan(lean) * 0.32
        o.append(box('x', (0.46, 0.05, 0.02), (0, y, z), mat='M_Aluminium'))
    o.append(box('x', (0.5, 0.06, 0.04), (0, 0.02, 0.03), mat='M_Black'))
    o.append(box('x', (0.05, 0.08, 1.5), (-0.28, 0.4, 0.9), rot=(lean, 0, 0), mat='M_Aluminium'))
    o.append(box('x', (0.05, 0.08, 1.5), (0.28, 0.4, 0.9), rot=(lean, 0, 0), mat='M_Aluminium'))
    o.append(cyl('x', 0.01, 0.5, (0, 0.3, 0.7), rot=(0, PI / 2, 0), mat='M_Rust', verts=6))
    return finish('WK_PRP_LeaningLadder', 'WK_PRP', o, home=home)


def b_prp_clothesline(home):
    """Two T-posts, four lines and washing that never came in."""
    o = []
    for s in (-1, 1):
        o.append(cyl('x', 0.05, 2.0, (s * 2.4, 0, 1.0), mat='M_Galv'))
        o.append(box('x', (0.1, 1.3, 0.08), (s * 2.4, 0, 1.98), mat='M_Galv'))
        o.append(box('x', (0.06, 0.06, 0.5), (s * 2.4, 0, 1.72), rot=(0.9, 0, 0), mat='M_Galv'))
        o.append(box('x', (0.3, 0.3, 0.1), (s * 2.4, 0, 0.05), mat='M_Concrete'))
    for i, y in enumerate((-0.5, -0.16, 0.16, 0.5)):
        sag = -0.12 - 0.03 * i
        o.append(tube('x', [(-2.4, y, 1.96), (0, y, 1.96 + sag), (2.4, y, 1.96)], 0.008,
                      mat='M_Black', smooth=False))
    hangs = ((-1.5, -0.5, 0.62, 0.5, 'M_White'), (-0.6, -0.16, 0.5, 0.42, 'M_Fabric'),
             (0.3, 0.16, 0.72, 0.55, 'M_White'), (1.2, 0.5, 0.44, 0.4, 'M_Curtain'),
             (1.8, -0.16, 0.36, 0.3, 'M_Fabric'))
    for x, y, h, w, mat in hangs:
        sheet = plane('x', w, h, (x, y, 1.9 - h / 2), rot=(PI / 2, 0, 0), mat=mat)
        o.append(sheet)
        for dx in (-w / 2 + 0.03, w / 2 - 0.03):
            o.append(box('x', (0.02, 0.02, 0.05), (x + dx, y, 1.94), mat='M_PlasticYellow'))
    return finish('WK_PRP_ClothesLine', 'WK_PRP', o, home=home)


def b_prp_old_tv(home):
    """A wood-effect CRT set put out with the trash. Screen faces +Y."""
    o = []
    body = box('x', (0.62, 0.5, 0.5), (0, 0, 0.27), mat='M_Wood')
    bevel(body, 0.03, 2)
    o.append(body)
    o.append(box('x', (0.56, 0.03, 0.42), (0, 0.25, 0.28), mat='M_Black'))
    o.append(plane('x', 0.44, 0.34, (0, 0.27, 0.28), rot=(PI / 2, 0, PI), mat='M_GlassDark'))
    o.append(box('x', (0.1, 0.05, 0.42), (0.24, 0.25, 0.28), mat='M_PlasticWhite'))  # dial panel
    for i in range(2):
        o.append(cyl('x', 0.03, 0.03, (0.24, 0.28, 0.4 - i * 0.1), rot=(PI / 2, 0, 0),
                     mat='M_Chrome', verts=10))
    for sx in (-1, 1):
        for sy in (-1, 1):
            o.append(box('x', (0.06, 0.06, 0.06), (sx * 0.24, sy * 0.18, 0.03), mat='M_Black'))
    o.append(cyl('x', 0.008, 0.5, (-0.1, -0.2, 0.72), rot=(0.4, 0.5, 0), mat='M_Chrome', verts=6))
    o.append(cyl('x', 0.008, 0.44, (0.1, -0.2, 0.7), rot=(0.4, -0.5, 0), mat='M_Chrome', verts=6))
    return finish('WK_PRP_OldTV', 'WK_PRP', o, home=home)


def b_prp_milk_crates(home):
    """Three stacked crates — the kit's universal 'stuff goes here' prop."""
    o = []
    cols = ('M_PlasticRed', 'M_PlasticBlue', 'M_PlasticYellow')
    for i, c in enumerate(cols):
        z = 0.17 + i * 0.32
        rot = (0, 0, 0.2 * i)
        o.append(box('x', (0.44, 0.44, 0.03), (0, 0, z - 0.15), rot=rot, mat=c))
        for s in (-1, 1):
            o.append(box('x', (0.44, 0.03, 0.3), (0, s * 0.2, z), rot=rot, mat=c))
            o.append(box('x', (0.03, 0.44, 0.3), (s * 0.2, 0, z), rot=rot, mat=c))
        o.append(box('x', (0.46, 0.46, 0.025), (0, 0, z + 0.15), rot=rot, mat=c))
    o.append(box('x', (0.3, 0.24, 0.18), (0.04, -0.02, 1.0), rot=(0, 0, 0.5), mat='M_Fabric'))
    return finish('WK_PRP_MilkCrates', 'WK_PRP', o, home=home)


# ================================================================= LIGHTS
def b_lgt_flood(home):
    """Twin flood head on a short pole — the yard/service light. Aims +Y."""
    o = []
    o.append(cyl('x', 0.07, 4.4, (0, 0, 2.2), mat='M_Galv'))
    o.append(cyl('x', 0.24, 0.4, (0, 0, 0.2), mat='M_Concrete', verts=12))
    o.append(box('x', (0.5, 0.12, 0.1), (0, 0.12, 4.34), mat='M_DarkMetal'))
    li = []
    for s in (-1, 1):
        h = box('x', (0.34, 0.3, 0.26), (s * 0.22, 0.26, 4.3), rot=(0.45, 0, s * 0.2),
                mat='M_DarkMetal')
        bevel(h, 0.02, 2)
        o.append(h)
        o.append(plane('x', 0.3, 0.24, (s * 0.24, 0.38, 4.2), rot=(PI / 2 + 0.45, 0, s * 0.2),
                       mat='M_FloodLens'))
        li.append(lamp('x', 'SPOT', (s * 0.24, 0.4, 4.18),
                       rot=(1.05, 0, s * 0.25), energy=900, color=(1, 0.93, 0.78),
                       spot_size=1.25, spot_blend=0.45))
    o.append(box('x', (0.16, 0.14, 0.3), (0, -0.14, 3.6), mat='M_Galv'))          # photocell box
    return finish('WK_LGT_FloodLight', 'WK_LGT', o, lights=li, home=home)


def b_lgt_neon_open(home):
    """Wall-mounted OPEN neon. Origin = the mount point, glass faces +Y."""
    o = []
    o.append(box('x', (1.0, 0.08, 0.52), (0, 0, 0), mat='M_DarkMetal'))
    o.append(plane('x', 0.92, 0.46, (0, 0.05, 0), rot=(PI / 2, 0, PI), mat='M_NeonOpen'))
    for s in (-1, 1):
        o.append(box('x', (0.05, 0.14, 0.05), (s * 0.46, -0.06, 0.2), mat='M_Galv'))
    o.append(cyl('x', 0.008, 0.4, (0.3, -0.05, -0.32), rot=(0.4, 0, 0), mat='M_Black', verts=6))
    li = [lamp('x', 'POINT', (0, 0.45, 0), energy=55, color=(1.0, 0.35, 0.75), size=0.3)]
    return finish('WK_LGT_NeonOpen', 'WK_LGT', o, lights=li, home=home)


def b_lgt_fire_barrel(home):
    """Burn barrel: the one hot light in the kit."""
    o = []
    drum = cyl('x', 0.3, 0.88, (0, 0, 0.44), mat='M_Rust', verts=18)
    o.append(drum)
    o.append(torus('x', 0.3, 0.022, (0, 0, 0.86), mat='M_Rust', major_seg=20, minor_seg=6))
    o.append(torus('x', 0.3, 0.022, (0, 0, 0.5), mat='M_Rust', major_seg=20, minor_seg=6))
    for i in range(5):                            # punched vents
        a = i * 2 * PI / 5
        o.append(box('x', (0.1, 0.02, 0.12), (0.29 * math.cos(a), 0.29 * math.sin(a), 0.2),
                     rot=(0, 0, a), mat='M_Black'))
    o.append(cyl('x', 0.27, 0.02, (0, 0, 0.8), mat='M_Black', verts=16))          # ash line
    for i in range(7):                            # flames
        a = i * 2 * PI / 7 + 0.3
        r = 0.11 + 0.05 * (i % 3)
        h = 0.34 + 0.22 * ((i * 7) % 5) / 4.0
        o.append(cone('x', 0.07, 0.005, h, (r * math.cos(a), r * math.sin(a), 0.86 + h / 2),
                      rot=(0.12 * math.sin(a), 0.12 * math.cos(a), 0), mat='M_FireGlow',
                      verts=8))
    for i in range(4):                            # scrap wood sticking out
        a = i * 1.7
        o.append(box('x', (0.06, 0.06, 0.7), (0.18 * math.cos(a), 0.18 * math.sin(a), 0.95),
                     rot=(0.5 * math.sin(a), 0.5 * math.cos(a), 0), mat='M_Wood'))
    li = [lamp('x', 'POINT', (0, 0, 1.05), energy=420, color=(1.0, 0.44, 0.13), size=0.35),
          lamp('x', 'POINT', (0, 0, 1.9), energy=90, color=(1.0, 0.5, 0.2), size=0.6)]
    return finish('WK_LGT_FireBarrel', 'WK_LGT', o, lights=li, home=home)


# ================================================================= SIGNAGE
def b_sgn_lot_number(home):
    o = []
    o.append(box('x', (0.08, 0.08, 1.05), (0, 0, 0.52), mat='M_Wood'))
    o.append(box('x', (0.7, 0.05, 0.34), (0, 0.01, 1.12), mat='M_DarkMetal'))
    for s in (-1, 1):
        o.append(plane('x', 0.66, 0.3, (0, s * 0.032, 1.12),
                       rot=(PI / 2, 0, PI if s > 0 else 0), mat='M_SignLot'))
    o.append(box('x', (0.24, 0.24, 0.06), (0, 0, 0.03), mat='M_Concrete'))
    return finish('WK_SGN_LotNumber', 'WK_SGN', o, home=home)


def b_sgn_speed(home):
    o = []
    o.append(cyl('x', 0.035, 2.1, (0, 0, 1.05), mat='M_Galv'))
    o.append(box('x', (0.48, 0.03, 0.62), (0, 0.02, 1.75), mat='M_Aluminium'))
    for s in (-1, 1):
        o.append(plane('x', 0.44, 0.58, (0, 0.02 + s * 0.022, 1.75),
                       rot=(PI / 2, 0, PI if s > 0 else 0), mat='M_SignSpeed'))
    o.append(box('x', (0.1, 0.05, 0.1), (0, 0, 0.06), mat='M_Concrete'))
    return finish('WK_SGN_SpeedLimit5', 'WK_SGN', o, home=home)


def b_sgn_stop(home):
    o = []
    o.append(cyl('x', 0.035, 2.2, (0, 0, 1.1), mat='M_Galv'))
    o.append(box('x', (0.06, 0.03, 0.3), (0, 0.01, 0.4), mat='M_Galv'))
    for s in (-1, 1):
        o.append(plane('x', 0.76, 0.76, (0, s * 0.014, 1.95),
                       rot=(PI / 2, 0, PI if s > 0 else 0), mat='M_SignStop'))
    o.append(box('x', (0.05, 0.02, 0.7), (0, 0, 1.95), mat='M_Galv'))
    return finish('WK_SGN_StopSign', 'WK_SGN', o, home=home)


# ================================================================= VEGETATION
def b_veg_pine(home):
    """Scrappy planted pine: trunk plus crossed bough cards."""
    o = []
    o.append(cone('x', 0.16, 0.06, 5.2, (0, 0, 2.6), mat='M_PoleWood', verts=10))
    layers = ((0.9, 1.9, 6), (2.0, 1.6, 6), (3.0, 1.25, 5), (3.9, 0.9, 4), (4.6, 0.55, 3))
    for z, r, n in layers:
        for i in range(n):
            a = i * 2 * PI / n + z
            card = plane('x', r * 2.0, r * 1.15, (r * 0.42 * math.cos(a), r * 0.42 * math.sin(a),
                                                  z + r * 0.2),
                         rot=(PI / 2 - 0.42, 0, a + PI / 2), mat='M_Pine')
            o.append(card)
    o.append(cone('x', 0.35, 0.02, 0.8, (0, 0, 5.3), mat='M_Pine', verts=8))
    return finish('WK_VEG_PineTree', 'WK_VEG', o, home=home)


def b_veg_weed_clump(home):
    o = []
    for i in range(5):
        a = i * 0.7
        o.append(plane('x', 0.75, 0.55, (0.12 * math.cos(a), 0.12 * math.sin(a), 0.26),
                       rot=(PI / 2, 0, a), mat='M_Weeds'))
    return finish('WK_VEG_WeedClump', 'WK_VEG', o, home=home)


# ================================================================= DECALS
def b_dcl_tire_tracks(home):
    p = plane('x', 4.0, 2.4, (0, 0, 0.012), mat='M_TireTracks')
    return finish('WK_DCL_TireTracks', 'WK_DCL', [p], home=home)


def b_dcl_litter(home):
    p = plane('x', 3.0, 3.0, (0, 0, 0.014), mat='M_Litter')
    return finish('WK_DCL_LitterScatter', 'WK_DCL', [p], home=home)


# ================================================================= HERO
def b_hero_pickup79(home):
    """Square-body half-ton, two-tone, nose to +X."""
    o = []
    P = 'M_TruckPaint'
    frame = box('x', (5.3, 1.95, 0.34), (0, 0, 0.66), mat='M_Black')
    o.append(frame)
    body = box('x', (5.3, 1.95, 0.66), (0, 0, 1.06), mat=P)
    bevel(body, 0.06, 2)
    o.append(body)
    o.append(box('x', (5.34, 1.98, 0.24), (0, 0, 0.78), mat='M_White'))           # two-tone band
    cab = box('x', (1.75, 1.86, 0.72), (-0.35, 0, 1.72), mat=P)
    bevel(cab, 0.07, 3)
    o.append(cab)
    o.append(box('x', (1.6, 1.72, 0.6), (-0.3, 0, 1.78), mat='M_GlassDark'))      # glass
    roof = box('x', (1.7, 1.84, 0.1), (-0.35, 0, 2.08), mat='M_White')
    bevel(roof, 0.04, 2)
    o.append(roof)
    hood = box('x', (1.55, 1.9, 0.3), (1.5, 0, 1.5), mat=P)
    bevel(hood, 0.05, 2)
    o.append(hood)
    o.append(box('x', (0.16, 1.82, 0.42), (2.3, 0, 1.42), mat='M_Chrome'))        # grille surround
    o.append(box('x', (0.06, 1.6, 0.3), (2.36, 0, 1.42), mat='M_Black'))
    for y in (-0.62, 0.62):
        o.append(box('x', (0.1, 0.42, 0.24), (2.34, y, 1.44), mat='M_CarLightF'))
        o.append(box('x', (0.08, 0.34, 0.2), (-2.68, y, 1.2), mat='M_CarLightR'))
    for x in (2.42, -2.68):                                                       # bumpers
        b = box('x', (0.2, 2.0, 0.22), (x, 0, 1.0), mat='M_Chrome')
        bevel(b, 0.03, 2)
        o.append(b)
    # bed
    o.append(box('x', (2.5, 1.92, 0.06), (-1.6, 0, 1.32), mat='M_DarkMetal'))
    for s in (-1, 1):
        o.append(box('x', (2.5, 0.1, 0.5), (-1.6, s * 0.92, 1.55), mat=P))
    o.append(box('x', (0.1, 1.92, 0.5), (-2.82, 0, 1.55), mat=P))                 # tailgate
    o.append(box('x', (0.9, 0.6, 0.4), (-1.2, 0.4, 1.55), mat='M_Rust'))          # junk in the bed
    o.append(cyl('x', 0.22, 0.9, (-2.2, -0.4, 1.55), rot=(0, PI / 2, 0), mat='M_Galv', verts=12))
    for x in (1.55, -1.75):                                                       # wheels
        for y in (-0.92, 0.92):
            o.append(cyl('x', 0.42, 0.28, (x, y, 0.42), rot=(PI / 2, 0, 0), mat='M_Tire',
                         verts=18))
            o.append(cyl('x', 0.2, 0.29, (x, y, 0.42), rot=(PI / 2, 0, 0), mat='M_Chrome',
                         verts=12))
            o.append(box('x', (1.2, 0.06, 0.5), (x, y * 1.03, 0.78), mat='M_Rust'))
    o.append(box('x', (0.02, 0.36, 0.18), (-2.79, 0.3, 1.12), mat='M_Plate'))
    for y in (-1.0, 1.0):
        o.append(box('x', (0.1, 0.16, 0.1), (0.6, y, 1.85), mat='M_Black'))       # mirrors
    o.append(cyl('x', 0.03, 0.9, (0.5, -0.95, 2.2), mat='M_Chrome', verts=8))     # CB whip
    return finish('WK_HERO_Pickup79', 'WK_HERO', o, home=home)


def b_hero_motorhome(home):
    """Class C motorhome up on blocks, nose to +X. The park's biggest silhouette."""
    o = []
    L, W = 7.4, 2.5
    body = box('x', (L, W, 2.35), (-0.9, 0, 2.0), mat='M_RVCream')
    bevel(body, 0.09, 3)
    o.append(body)
    flank = box('x', (L + 0.02, W + 0.03, 1.3), (-0.9, 0, 1.85), mat='M_RVStripe')
    o.append(flank)
    auto_uv(flank, (1, 1))
    roof = box('x', (L + 0.06, W - 0.05, 0.14), (-0.9, 0, 3.2), mat='M_Aluminium')
    bevel(roof, 0.05, 2)
    o.append(roof)
    cab = box('x', (2.0, W - 0.12, 1.5), (3.1, 0, 1.55), mat='M_RVCream')
    bevel(cab, 0.09, 3)
    o.append(cab)
    o.append(box('x', (1.7, W - 0.16, 0.66), (3.15, 0, 1.95), mat='M_GlassDark'))
    bunk = box('x', (2.3, W - 0.06, 0.95), (2.8, 0, 2.85), mat='M_RVCream')
    bevel(bunk, 0.12, 3)
    o.append(bunk)
    o.append(box('x', (0.6, 1.2, 0.4), (3.7, 0, 2.9), mat='M_GlassDark'))         # bunk window
    o.append(box('x', (0.5, W + 0.04, 0.5), (4.05, 0, 1.2), mat='M_Chrome'))      # nose/bumper
    for y in (-0.86, 0.86):
        o.append(box('x', (0.12, 0.4, 0.22), (4.22, y, 1.1), mat='M_CarLightF'))
        o.append(box('x', (0.1, 0.34, 0.2), (-4.55, y, 1.3), mat='M_CarLightR'))
    # side windows + door
    for x in (-3.3, -1.4):
        o.append(box('x', (1.3, 0.06, 0.8), (x, W / 2 - 0.01, 2.4), mat='M_Trim'))
        o.append(plane('x', 1.18, 0.68, (x, W / 2 + 0.03, 2.4), rot=(PI / 2, 0, PI),
                       mat='M_Curtain'))
    o.append(box('x', (0.86, 0.08, 1.8), (0.4, W / 2 - 0.02, 1.9), mat='M_RVCream'))
    o.append(box('x', (0.72, 0.05, 0.5), (0.4, W / 2 + 0.03, 2.5), mat='M_GlassDark'))
    o.append(box('x', (0.9, 0.5, 0.06), (0.4, W / 2 + 0.3, 1.0), mat='M_Galv'))   # step
    for x in (-2.4, 0.2):                                                          # roof kit
        o.append(box('x', (0.66, 0.66, 0.26), (x, 0.3, 3.4), mat='M_White'))
    o.append(box('x', (0.9, 0.7, 0.3), (-3.6, -0.4, 3.42), mat='M_Galv'))         # AC unit
    for i in range(6):                                                             # rear ladder
        o.append(box('x', (0.03, 0.42, 0.03), (-4.6, 0.6, 1.5 + i * 0.32), mat='M_Aluminium'))
    for s in (-1, 1):
        o.append(box('x', (0.04, 0.04, 1.9), (-4.6, 0.6 + s * 0.2, 2.35), mat='M_Aluminium'))
    o.append(box('x', (2.6, W - 0.2, 0.5), (-0.9, 0, 0.95), mat='M_Skirting'))    # underbelly
    for x, y in ((3.0, -1.05), (3.0, 1.05)):                                       # front wheels
        o.append(cyl('x', 0.44, 0.3, (x, y, 0.44), rot=(PI / 2, 0, 0), mat='M_Tire', verts=18))
        o.append(cyl('x', 0.2, 0.31, (x, y, 0.44), rot=(PI / 2, 0, 0), mat='M_Chrome', verts=12))
    for x in (-2.2, -3.0):                                                         # dual rears
        for y in (-1.05, 1.05):
            o.append(cyl('x', 0.44, 0.26, (x, y, 0.44), rot=(PI / 2, 0, 0), mat='M_Tire',
                         verts=16))
    o.append(box('x', (0.6, 0.6, 0.5), (-2.6, -1.05, 0.25), mat='M_Cinderblock'))  # on blocks
    o.append(box('x', (0.6, 0.6, 0.5), (-2.6, 1.05, 0.25), mat='M_Cinderblock'))
    o.append(box('x', (0.02, 0.36, 0.18), (-4.66, 0.3, 1.05), mat='M_Plate'))
    o.append(box('x', (1.8, 0.05, 0.9), (-0.9, -W / 2 - 0.02, 2.4), mat='M_Rust'))  # patch panel
    li = [lamp('x', 'POINT', (0.4, W / 2 + 0.5, 2.1), energy=35, color=(1, 0.72, 0.42))]
    return finish('WK_HERO_MotorhomeRV', 'WK_HERO', o, lights=li, home=home)
