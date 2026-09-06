"""11_DECALS - weathering sheets (alpha-blended, placed over kit surfaces)."""

from .. import dna
from ..geo import vec


def waterline(asset):
    p = asset.part("sheet", "MK_DECAL_OVERLAY_WATERLINE", uv_mode="sheet")
    p.plane(vec(0, 0, 0.8), 4.0, 1.6, normal="Y")
    asset.origin = vec(0, 0, 0)


def crack(asset):
    p = asset.part("sheet", "MK_DECAL_OVERLAY_CRACK", uv_mode="sheet")
    p.plane(vec(0, 0, 0.002), 4.0, 4.0, normal="Z")
    asset.origin = vec(0, 0, 0)
