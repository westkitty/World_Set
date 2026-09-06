"""07_PROPS - barrels, crates, valves: the storytelling tier."""

import random

from .. import dna
from ..geo import vec


def barrel(asset):
    stave = asset.part("stave", "MK_TIMBER", uv_mode="cyl")
    stave.lathe([(0.0, 0.0), (0.28, 0.0), (0.315, 0.12), (0.335, 0.45),
                 (0.315, 0.78), (0.28, 0.9), (0.0, 0.9)], vec(0, 0, 0), seg=16)
    hoops = asset.part("hoops", "MK_STEEL_AGED", uv_mode="cyl")
    for z, r in ((0.16, 0.325), (0.45, 0.345), (0.74, 0.325)):
        hoops.ring(vec(0, 0, z - 0.03), r + 0.012, r - 0.01, 0.06, seg=16)
    bung = asset.part("bung", "MK_STEEL_PRIMER", uv_mode="cyl")
    bung.cyl(vec(0, -0.33, 0.6), 0.045, 0.045, 0.04, axis="Y", seg=10)


def crate_a(asset):
    w, d, h = 0.8, 0.6, 0.6
    w2, d2 = w / 2, d / 2
    post = asset.part("posts", "MK_TIMBER")
    for sx in (-w2 + 0.03, w2 - 0.03):
        for sy in (-d2 + 0.03, d2 - 0.03):
            post.box(vec(sx, sy, h / 2), (0.06, 0.06, h))
    frame = asset.part("frame", "MK_TIMBER")
    for z in (0.04, h - 0.04):
        frame.box(vec(0, 0, z), (w, 0.05, 0.08))
        frame.box(vec(0, 0, z), (0.05, d, 0.08))
    slat = asset.part("slats", "MK_TIMBER")
    for sy in (-d2, d2):
        for z in (0.18, 0.33, 0.48):
            slat.box(vec(0, sy, z), (w - 0.1, 0.02, 0.1))
    for sx in (-w2, w2):
        for z in (0.18, 0.33, 0.48):
            slat.box(vec(sx, 0, z), (0.02, d - 0.1, 0.1))
    strap = asset.part("straps", "MK_STEEL_AGED")
    for sx in (-w2, w2):
        for sy in (-d2, d2):
            strap.box(vec(sx, sy, h / 2), (0.08, 0.08, h + 0.02))


def valve(asset):
    base = asset.part("stand", "MK_STEEL_PRIMER")
    base.box(vec(0, 0, 0.04), (0.4, 0.4, 0.08))
    base.cyl(vec(0, 0, 0.3), 0.09, 0.07, 0.5, axis="Z", seg=12)
    body = asset.part("body", "MK_BRASS", uv_mode="cyl")
    body.lathe([(0.0, 0.5), (0.14, 0.5), (0.16, 0.56), (0.12, 0.62), (0.0, 0.62)],
               vec(0, 0, 0), seg=16)
    body.cyl(vec(0, 0, 0.56), 0.05, 0.05, 0.16, axis="Y", seg=12)
    wheel = asset.part("wheel", "MK_STEEL_PAINTED", uv_mode="cyl")
    wheel.ring(vec(0, -0.2, 0.56), 0.18, 0.15, 0.03, axis="Y", seg=16)
    for i in range(3):
        import math
        a = i * math.pi * 2 / 3
        wheel.box(vec(math.cos(a) * 0.08, -0.185, 0.56 + math.sin(a) * 0.08),
                  (0.03, 0.03, 0.16), rot=(0, a, 0))
    asset.origin = vec(0, 0, 0)
