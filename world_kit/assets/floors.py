"""03_FLOORS - slabs, gratings, transitions, brine channels."""

from .. import dna
from ..geo import vec

D = dna.DIMENSIONS
BAY = D["bay_w"]
FT = D["floor_t"]


def _kerb(asset, key, inset=0.2, z=0.02):
    p = asset.part(key, "MK_CONCRETE_STRUCT")
    p.box(vec(BAY / 2, inset / 2, z), (BAY, inset, 0.06))
    p.box(vec(BAY / 2, BAY - inset / 2, z), (BAY, inset, 0.06))
    p.box(vec(inset / 2, BAY / 2, z), (inset, BAY - 2 * inset, 0.06))
    p.box(vec(BAY - inset / 2, BAY / 2, z), (inset, BAY - 2 * inset, 0.06))
    return p


def _grating(asset, key, x0, x1, y0=0.08, y1=None, seg=0.13):
    y1 = BAY - 0.08 if y1 is None else y1
    p = asset.part(key, "MK_STEEL_AGED")
    y = y0
    n = 0
    while y < y1:
        p.box(vec((x0 + x1) / 2, y, -0.02), (x1 - x0, 0.02, 0.05))
        y += seg
        n += 1
    return p


def _frame(asset, key, x0, x1):
    p = asset.part(key, "MK_STEEL_PRIMER")
    p.box(vec((x0 + x1) / 2, 0.04, -0.1), (x1 - x0, 0.08, 0.2))
    p.box(vec((x0 + x1) / 2, BAY - 0.04, -0.1), (x1 - x0, 0.08, 0.2))
    for y in (1.0, 2.0, 3.0):
        p.box(vec((x0 + x1) / 2, y, -0.2), (x1 - x0, 0.06, 0.28))
    return p


def slab_a(asset):
    asset.part("slab", "MK_CONCRETE_STRUCT").box(vec(BAY / 2, BAY / 2, -FT / 2), (BAY, BAY, FT))
    asset.part("tile", "MK_CERAMIC_TILE").box(vec(BAY / 2, BAY / 2, -0.03), (BAY - 0.4, BAY - 0.4, 0.06))
    _kerb(asset, "kerb")


def slab_b(asset):
    _frame(asset, "frame", 0, BAY)
    _grating(asset, "grate", 0.08, BAY - 0.08)
    # a few cross bars for stiffness
    cross = asset.part("cross", "MK_STEEL_PRIMER")
    for x in (1.0, 2.0, 3.0):
        cross.box(vec(x, BAY / 2, -0.06), (0.04, BAY - 0.16, 0.05))


def transition(asset):
    # concrete half
    asset.part("slab", "MK_CONCRETE_STRUCT").box(vec(BAY * 0.25, BAY / 2, -FT / 2), (BAY / 2, BAY, FT))
    asset.part("tile", "MK_CERAMIC_TILE").box(vec(BAY * 0.25, BAY / 2, -0.03), (BAY / 2 - 0.2, BAY - 0.4, 0.06))
    # grating half
    _frame(asset, "frame", BAY / 2, BAY)
    _grating(asset, "grate", BAY / 2 + 0.06, BAY - 0.08)
    # bolted nosing plate at the seam
    nosing = asset.part("nosing", "MK_STEEL_AGED")
    nosing.box(vec(BAY / 2, BAY / 2, 0.0), (0.14, BAY, 0.05))
    for y in (0.5, 1.5, 2.5, 3.5):
        nosing.cyl(vec(BAY / 2, y, 0.03), 0.03, 0.03, 0.02, axis="Z", seg=6)


def channel(asset):
    cy = BAY / 2
    ch = 0.6
    # two side slabs
    asset.part("slabL", "MK_CONCRETE_STRUCT").box(vec(BAY / 2, (cy - ch / 2) / 2, -FT / 2), (BAY, cy - ch / 2, FT))
    asset.part("slabR", "MK_CONCRETE_STRUCT").box(vec(BAY / 2, (BAY + cy + ch / 2) / 2, -FT / 2), (BAY, BAY - cy - ch / 2, FT))
    # channel walls + floor
    asset.part("chL", "MK_CONCRETE_STRUCT").box(vec(BAY / 2, cy - ch / 2 + 0.05, -0.2), (BAY, 0.1, 0.4))
    asset.part("chR", "MK_CONCRETE_STRUCT").box(vec(BAY / 2, cy + ch / 2 - 0.05, -0.2), (BAY, 0.1, 0.4))
    asset.part("chF", "MK_CONCRETE_STRUCT").box(vec(BAY / 2, cy, -0.32), (BAY, ch, 0.1))
    # water
    asset.part("water", "MK_WATER_BRINE", uv_mode="sheet").plane(vec(BAY / 2, cy, -0.2), BAY, ch - 0.16)
    # grate run across the channel
    g = asset.part("grate", "MK_STEEL_AGED")
    x = 0.15
    while x < BAY - 0.1:
        g.box(vec(x, cy, -0.02), (0.03, ch + 0.2, 0.05))
        x += 0.25
    _kerb(asset, "kerb")
