"""13_HERO - identity objects."""

import math

from .. import dna
from ..geo import vec


def evaporator(asset):
    shell = asset.part("shell", "MK_STEEL_PAINTED", uv_mode="cyl")
    shell.lathe([
        (0.0, 0.0), (2.2, 0.0), (2.2, 0.9), (2.17, 0.92), (2.17, 1.8),
        (2.14, 1.82), (2.14, 2.7), (2.11, 2.72), (2.11, 3.6), (2.07, 3.62),
        (2.07, 4.5), (2.0, 4.55), (1.9, 5.0), (0.0, 5.1),
    ], vec(0, 0, 0), seg=24)
    hoops = asset.part("hoops", "MK_STEEL_PRIMER", uv_mode="cyl")
    for z, r in ((0.9, 2.2), (1.8, 2.17), (2.7, 2.14), (3.6, 2.11), (4.5, 2.07)):
        hoops.ring(vec(0, 0, z - 0.05), r + 0.02, r - 0.02, 0.1, seg=24)
    stack = asset.part("stack", "MK_BRASS", uv_mode="cyl")
    stack.cyl(vec(0.9, 0, 5.0), 0.14, 0.1, 1.2, axis="Z", seg=12)
    stack.cyl(vec(0.9, 0, 6.1), 0.18, 0.18, 0.1, axis="Z", seg=12)
    glass = asset.part("sight", "MK_EMISSIVE_CYAN")
    glass.box(vec(0, -2.15, 2.2), (0.14, 0.06, 2.2))
    glassf = asset.part("sightframe", "MK_STEEL_AGED")
    glassf.box(vec(0, -2.16, 2.2), (0.2, 0.05, 2.3))
    ladder = asset.part("ladder", "MK_STEEL_AGED")
    for sx in (-0.2, 0.2):
        ladder.cyl(vec(-1.5 + sx, -1.6, 0), 0.03, 0.03, 4.6, axis="Z", seg=8)
    z = 0.4
    while z < 4.6:
        ladder.cyl(vec(-1.5, -1.6, z), 0.02, 0.02, 0.4, axis="X", seg=6)
        z += 0.35
    hatch = asset.part("hatch", "MK_STEEL_PRIMER", uv_mode="cyl")
    hatch.cyl(vec(1.6, 1.4, 4.8), 0.4, 0.4, 0.3, axis="Z", seg=16)


def beacon(asset):
    shaft = asset.part("shaft", "MK_CONCRETE_STRUCT", uv_mode="cyl")
    shaft.lathe([(0.0, 0.0), (1.6, 0.0), (1.45, 0.5), (1.1, 3.0), (0.95, 5.5),
                 (0.9, 6.8), (1.1, 7.0), (0.0, 7.0)], vec(0, 0, 0), seg=20)
    gal = asset.part("gallery", "MK_STEEL_AGED", uv_mode="cyl")
    gal.cyl(vec(0, 0, 7.05), 1.4, 1.4, 0.08, axis="Z", seg=20)
    rail = asset.part("rail", "MK_STEEL_PAINTED", uv_mode="cyl")
    rail.ring(vec(0, 0, 7.9), 1.42, 1.36, 0.05, seg=20)
    rail.ring(vec(0, 0, 7.5), 1.42, 1.38, 0.04, seg=20)
    for i in range(10):
        a = i * math.pi / 5
        rail.cyl(vec(math.cos(a) * 1.4, math.sin(a) * 1.4, 7.5), 0.025, 0.025, 0.9,
                 axis="Z", seg=6)
    lantern = asset.part("lantern", "MK_GLASS", uv_mode="cyl")
    lantern.cyl(vec(0, 0, 7.2), 0.7, 0.7, 1.4, axis="Z", seg=16, cap=False)
    fres = asset.part("fresnel", "MK_BRASS", uv_mode="cyl")
    fres.ring(vec(0, 0, 7.3), 0.74, 0.7, 0.08, seg=16)
    fres.ring(vec(0, 0, 8.3), 0.74, 0.7, 0.08, seg=16)
    core = asset.part("core", "MK_EMISSIVE_AMBER", uv_mode="cyl")
    core.lathe([(0.0, 7.4), (0.35, 7.5), (0.4, 7.9), (0.35, 8.3), (0.0, 8.4)],
               vec(0, 0, 0), seg=16)
    roof = asset.part("roof", "MK_STEEL_PAINTED", uv_mode="cyl")
    roof.lathe([(0.0, 9.6), (0.95, 8.6), (0.9, 8.55), (0.0, 8.5)], vec(0, 0, 0), seg=20)
    fin = asset.part("finial", "MK_STEEL_AGED", uv_mode="cyl")
    fin.cyl(vec(0, 0, 9.6), 0.03, 0.01, 0.8, axis="Z", seg=8)
    door = asset.part("door", "MK_STEEL_PRIMER")
    door.box(vec(0, -1.3, 1.2), (1.0, 0.2, 2.4))


def sluice(asset):
    pier = asset.part("piers", "MK_CONCRETE_STRUCT")
    pier.box(vec(-1.6, 0, 2.1), (0.8, 1.2, 4.2))
    pier.box(vec(1.6, 0, 2.1), (0.8, 1.2, 4.2))
    pier.box(vec(0, 0, 3.9), (4.0, 1.2, 0.7))
    leaf = asset.part("leaf", "MK_STEEL_PRIMER")
    leaf.box(vec(0, 0, 1.5), (2.6, 0.18, 3.0))
    for z in (0.6, 1.5, 2.4):
        leaf.box(vec(0, -0.12, z), (2.6, 0.06, 0.14))
    rods = asset.part("rods", "MK_STEEL_AGED", uv_mode="cyl")
    for sx in (-1.2, 1.2):
        rods.cyl(vec(sx, 0, 2.0), 0.04, 0.04, 4.0, axis="Z", seg=8)
    weight = asset.part("weight", "MK_STEEL_AGED")
    weight.box(vec(0, 0, 3.2), (2.4, 0.6, 0.8))
    win = asset.part("windlass", "MK_BRASS", uv_mode="cyl")
    win.cyl(vec(0, 0, 4.0), 0.12, 0.12, 2.0, axis="X", seg=12)
    win.cyl(vec(1.1, 0, 4.0), 0.03, 0.03, 0.5, axis="Z", seg=6)
    win.cyl(vec(1.1, 0, 4.45), 0.03, 0.03, 0.3, axis="X", seg=6)
