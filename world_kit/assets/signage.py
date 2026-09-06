"""09_SIGNAGE - enamel plates with cast lettering."""

from .. import dna
from ..geo import vec


def _bolts(asset, w, h):
    b = asset.part("bolts", "MK_BRASS", uv_mode="cyl")
    for sx in (-w / 2 + 0.05, w / 2 - 0.05):
        for sz in (0.05, h - 0.05):
            b.cyl(vec(sx, -0.02, sz), 0.018, 0.018, 0.02, axis="Y", seg=8)


def plaque(asset):
    asset.part("plate", "MK_SIGNAGE_ENAMEL").box(vec(0, 0, 0.22), (0.7, 0.03, 0.44))
    t = asset.part("lettering", "MK_STEEL_PAINTED")
    t.text("BRINEFALL", size=0.1, depth=0.012, center=vec(0, -0.02, 0.28), normal="-Y")
    t.text("SALTLIGHT STATION", size=0.05, depth=0.01, center=vec(0, -0.02, 0.16), normal="-Y")
    _bolts(asset, 0.7, 0.44)


def directional(asset):
    asset.part("board", "MK_SIGNAGE_ENAMEL").box(vec(0, 0, 0.1), (0.62, 0.03, 0.2))
    ar = asset.part("arrow", "MK_STEEL_AGED")
    ar.prism([(-0.26, 0.1), (-0.05, 0.1), (-0.05, 0.14), (0.12, 0.1),
              (-0.05, 0.06), (-0.05, 0.1), (-0.26, 0.1)], vec(0, -0.02, 0), vec(0, -0.012, 0))
    t = asset.part("lettering", "MK_STEEL_PAINTED")
    t.text("PIER 3", size=0.06, depth=0.01, center=vec(0.12, -0.02, 0.1), normal="-Y", align="CENTER")
    _bolts(asset, 0.62, 0.2)


def warning(asset):
    asset.part("plate", "MK_SIGNAGE_ENAMEL").box(vec(0, 0, 0.2), (0.4, 0.03, 0.4))
    tri = asset.part("triangle", "MK_STEEL_AGED")
    tri.prism([(0, 0.32), (-0.13, 0.12), (0.13, 0.12), (0, 0.32)], vec(0, -0.02, 0), vec(0, -0.012, 0))
    t = asset.part("lettering", "MK_STEEL_PAINTED")
    t.text("LIVE", size=0.05, depth=0.01, center=vec(0, -0.02, 0.1), normal="-Y")
    t.text("BRINE", size=0.05, depth=0.01, center=vec(0, -0.02, 0.05), normal="-Y")
    _bolts(asset, 0.4, 0.4)
