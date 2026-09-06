"""06_FURNITURE - sparse station furniture."""

from .. import dna
from ..geo import vec


def bench(asset):
    for sx in (-0.85, 0.85):
        leg = asset.part(f"leg{sx:.0f}", "MK_CONCRETE_STRUCT")
        leg.tapered_box(vec(sx, 0, 0), (0.16, 0.6, 0.8), (0.12, 0.5, 0.0), 0.8)
    top = asset.part("top", "MK_TIMBER")
    top.box(vec(0, 0, 0.86), (2.0, 0.7, 0.08))
    shelf = asset.part("shelf", "MK_TIMBER")
    for sy in (-0.2, 0.0, 0.2):
        shelf.box(vec(0, sy, 0.28), (1.7, 0.14, 0.04))
    vise = asset.part("vise", "MK_BRASS")
    vise.box(vec(0.7, 0.25, 0.95), (0.16, 0.16, 0.16))
    vise.cyl(vec(0.7, 0.25, 1.0), 0.02, 0.02, 0.3, axis="X", seg=8)
