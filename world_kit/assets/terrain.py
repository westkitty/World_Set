"""12_TERRAIN - water plane and ground armour."""

from .. import dna
from ..geo import vec

BAY = dna.DIMENSIONS["bay_w"]


def water(asset):
    asset.part("surface", "MK_WATER_BRINE", uv_mode="sheet").plane(vec(0, 0, -0.05), BAY, BAY)
    asset.part("glow", "MK_EMISSIVE_CYAN", uv_mode="sheet").plane(vec(0, 0, -0.14), BAY, BAY)
    asset.origin = vec(0, 0, 0)
