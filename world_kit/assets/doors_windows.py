"""04_DOORS_WINDOWS - frames, leaves, arched glazing."""

import math

from .. import dna
from ..geo import vec

D = dna.DIMENSIONS
DW, DH = D["door_w"], D["door_h"]


def door_frame(asset):
    j = asset.part("jambs", "MK_STEEL_PRIMER")
    j.box(vec(-(DW / 2 + 0.06), 0, DH / 2), (0.14, 0.4, DH))
    j.box(vec((DW / 2 + 0.06), 0, DH / 2), (0.14, 0.4, DH))
    j.box(vec(0, 0, DH + 0.06), (DW + 0.4, 0.4, 0.14))
    th = asset.part("thresh", "MK_STEEL_AGED")
    th.box(vec(0, 0, 0.03), (DW + 0.3, 0.44, 0.06))
    g = asset.part("gudgeons", "MK_BRASS", uv_mode="cyl")
    for z in (0.3, 1.2, 2.1):
        g.cyl(vec(-(DW / 2 + 0.06), -0.16, z), 0.03, 0.03, 0.12, axis="Y", seg=8)


def door_leaf(asset):
    asset.part("stiles", "MK_STEEL_PAINTED").box(vec(0, 0, DH / 2), (DW, 0.06, DH))
    face = asset.part("faces", "MK_TIMBER")
    face.box(vec(0, 0.045, DH / 2), (DW - 0.16, 0.02, DH - 0.2))
    face.box(vec(0, -0.045, DH / 2), (DW - 0.16, 0.02, DH - 0.2))
    rail = asset.part("rails", "MK_STEEL_PAINTED")
    rail.box(vec(0, 0.05, 0.3), (DW - 0.1, 0.02, 0.3))
    rail.box(vec(0, -0.05, 0.3), (DW - 0.1, 0.02, 0.3))
    ring = asset.part("porthole", "MK_BRASS", uv_mode="cyl")
    ring.ring(vec(0, 0, 1.62), 0.16, 0.12, 0.1, axis="Y", seg=16)
    asset.part("glass", "MK_GLASS", uv_mode="cyl").cyl(vec(0, 0, 1.62), 0.12, 0.12, 0.02, axis="Y", seg=16)
    latch = asset.part("latch", "MK_STEEL_AGED")
    latch.box(vec(DW / 2 - 0.12, -0.06, 1.0), (0.04, 0.06, 0.2))
    latch.box(vec(DW / 2 - 0.2, -0.09, 1.0), (0.2, 0.03, 0.04))
    asset.origin = vec(-(DW / 2), 0, 0)     # hinge pivot


def window_arch(asset):
    w = D["window_w"]
    f = asset.part("frame", "MK_STEEL_AGED")
    f.box(vec(-(w / 2 - 0.04), 0, 1.0), (0.08, 0.1, 2.0))
    f.box(vec((w / 2 - 0.04), 0, 1.0), (0.08, 0.1, 2.0))
    f.box(vec(0, 0, 0.04), (w, 0.1, 0.08))
    # arched head as a fan of mullions
    for i in range(5):
        a = math.pi * (i + 1) / 6
        m = asset.part(f"fan{i}", "MK_STEEL_AGED")
        x2 = math.cos(a) * (w / 2 - 0.04)
        z2 = 1.4 + math.sin(a) * (w / 2 - 0.04)
        m.sweep([vec(0, 0, 1.4), vec(x2, 0, z2)], [(-0.02, -0.04), (0.02, -0.04), (0.02, 0.04), (-0.02, 0.04), (-0.02, -0.04)])
    # vertical mullion
    vm = asset.part("mull", "MK_STEEL_AGED")
    vm.box(vec(0, 0, 0.72), (0.05, 0.08, 1.36))
    hb = asset.part("transom", "MK_STEEL_AGED")
    hb.box(vec(0, 0, 1.4), (w, 0.08, 0.06))
    asset.part("glass", "MK_GLASS").box(vec(0, 0, 1.0), (w - 0.06, 0.02, 2.0))
    sill = asset.part("sill", "MK_STEEL_PRIMER")
    sill.box(vec(0, 0.05, -0.02), (w + 0.2, 0.3, 0.06), rot=(0.12, 0, 0))
