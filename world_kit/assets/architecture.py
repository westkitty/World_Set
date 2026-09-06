"""01_ARCHITECTURE - bays, vaults, columns."""

from .. import dna
from ..geo import vec

D = dna.DIMENSIONS
BAY = D["bay_w"]
WALL_H = D["wall_h"]
RISE = D["vault_rise"]


def arch_profile(width, rise, thick, steps=12, z0=0.0):
    """Closed 2D segmental-arch profile [(u, v)] of given rise and thickness."""
    half = width / 2.0
    R = (half * half + rise * rise) / (2.0 * rise)
    cz = z0 + rise - R
    inner, outer = [], []
    for i in range(steps + 1):
        x = width * i / steps
        dz = (R * R - (x - half) ** 2) ** 0.5
        inner.append((x, cz + dz))
    outer = [(x, v + thick) for (x, v) in inner]
    return inner + outer[::-1]


def bay_vault(asset):
    """Vaulted bay: shell + two ribs + corbels + a steel tie rod."""
    prof = arch_profile(BAY, RISE, 0.22)
    shell = asset.part("shell", "MK_CONCRETE_STRUCT")
    shell.prism(prof, vec(0, BAY, WALL_H), vec(0, -BAY, 0))

    rib_prof = arch_profile(BAY, RISE, 0.42, steps=12)
    for i, y in enumerate((0.55, BAY - 0.55)):
        rib = asset.part(f"rib{i}", "MK_CONCRETE_STRUCT")
        rib.prism(rib_prof, vec(0, y + 0.14, WALL_H - 0.2), vec(0, -0.28, 0))

    for i, (x, y) in enumerate([(0, 0), (BAY, 0), (0, BAY), (BAY, BAY)]):
        cor = asset.part(f"corb{i}", "MK_CONCRETE_STRUCT")
        sx = 1 if x == 0 else -1
        sy = 1 if y == 0 else -1
        cor.tapered_box(vec(x + sx * 0.35, y + sy * 0.35, WALL_H - 0.5),
                        (0.7, 0.7, 0.5), (0.5, 0.5, 0.0), 0.5)

    tie = asset.part("tie", "MK_STEEL_PRIMER")
    tie.cyl(vec(BAY / 2, 0.1, WALL_H - 0.05), 0.035, 0.035, BAY - 0.2,
            axis="Y", seg=10)
    for i, y in enumerate((0.3, BAY - 0.3)):
        plate = asset.part(f"tiep{i}", "MK_STEEL_PRIMER")
        plate.box(vec(BAY / 2, y, WALL_H - 0.05), (0.24, 0.03, 0.24))


def bay_flat(asset):
    """Flat-slab bay with an exposed beam grid."""
    slab = asset.part("slab", "MK_CONCRETE_STRUCT")
    slab.box(vec(BAY / 2, BAY / 2, WALL_H + 0.15), (BAY, BAY, 0.3))

    for i, y in enumerate((BAY * 0.33, BAY * 0.66)):
        b = asset.part(f"beamx{i}", "MK_STEEL_PRIMER")
        b.box(vec(BAY / 2, y, WALL_H - 0.22), (BAY, 0.14, 0.4))
        for f in (-1, 1):
            fl = asset.part(f"flx{i}{f}", "MK_STEEL_PRIMER")
            fl.box(vec(BAY / 2, y, WALL_H - 0.22 + f * 0.21), (BAY, 0.28, 0.04))
    for i, x in enumerate((BAY * 0.33, BAY * 0.66)):
        b = asset.part(f"beamy{i}", "MK_STEEL_PRIMER")
        b.box(vec(x, BAY / 2, WALL_H - 0.22), (0.14, BAY, 0.4))
        for f in (-1, 1):
            fl = asset.part(f"fly{i}{f}", "MK_STEEL_PRIMER")
            fl.box(vec(x, BAY / 2, WALL_H - 0.22 + f * 0.21), (0.28, BAY, 0.04))

    for i, (x, y) in enumerate([(0, 0), (BAY, 0), (0, BAY), (BAY, BAY)]):
        cor = asset.part(f"corb{i}", "MK_CONCRETE_STRUCT")
        sx = 1 if x == 0 else -1
        sy = 1 if y == 0 else -1
        cor.tapered_box(vec(x + sx * 0.35, y + sy * 0.35, WALL_H - 0.5),
                        (0.7, 0.7, 0.5), (0.5, 0.5, 0.0), 0.5)


def bay_oculus(asset):
    """Vault bay with a 2.4 m roof opening and a raised steel curb."""
    prof = arch_profile(BAY, RISE, 0.22)
    shell = asset.part("shell", "MK_CONCRETE_STRUCT")
    shell.prism(prof, vec(0, BAY, WALL_H), vec(0, -BAY, 0))
    cutter = asset.cutter("cut", lambda p: p.box(vec(BAY / 2, BAY / 2, WALL_H + RISE),
                                                  (2.4, 2.4, 3.0)))
    asset.boolean("shell", cutter)

    curb = asset.part("curb", "MK_STEEL_AGED")
    z = WALL_H + RISE - 0.05
    t = 0.16
    curb.box(vec(BAY / 2, BAY / 2 - 1.2 + t / 2, z + 0.15), (2.4 + 2 * t, t, 0.4))
    curb.box(vec(BAY / 2, BAY / 2 + 1.2 - t / 2, z + 0.15), (2.4 + 2 * t, t, 0.4))
    curb.box(vec(BAY / 2 - 1.2 + t / 2, BAY / 2, z + 0.15), (t, 2.4, 0.4))
    curb.box(vec(BAY / 2 + 1.2 - t / 2, BAY / 2, z + 0.15), (t, 2.4, 0.4))

    for i, (x, y) in enumerate([(0, 0), (BAY, 0), (0, BAY), (BAY, BAY)]):
        cor = asset.part(f"corb{i}", "MK_CONCRETE_STRUCT")
        sx = 1 if x == 0 else -1
        sy = 1 if y == 0 else -1
        cor.tapered_box(vec(x + sx * 0.35, y + sy * 0.35, WALL_H - 0.5),
                        (0.7, 0.7, 0.5), (0.5, 0.5, 0.0), 0.5)


def column(asset):
    """Octagonal cast column with base and capital."""
    w = D["col_w"]
    pts = []
    for i in range(8):
        import math
        a = math.pi / 8 + i * math.pi / 4
        pts.append((math.cos(a) * w * 0.62, math.sin(a) * w * 0.62))
    shaft = asset.part("shaft", "MK_CONCRETE_STRUCT", uv_mode="cyl")
    shaft.prism(pts, vec(BAY / 2, BAY / 2, 0.2), vec(0, 0, WALL_H - 0.5))

    base = asset.part("base", "MK_CONCRETE_STRUCT")
    base.tapered_box(vec(BAY / 2, BAY / 2, 0), (0.85, 0.85, 0.22), (0.62, 0.62, 0.0), 0.22)
    base.box(vec(BAY / 2, BAY / 2, 0.05), (0.95, 0.95, 0.1))

    cap = asset.part("cap", "MK_CONCRETE_STRUCT")
    cap.tapered_box(vec(BAY / 2, BAY / 2, WALL_H - 0.3), (0.62, 0.62, 0.3),
                    (0.85, 0.85, 0.0), 0.3)

    band = asset.part("band", "MK_STEEL_PRIMER", uv_mode="cyl")
    band.ring(vec(BAY / 2, BAY / 2, 0.35), w * 0.66, w * 0.58, 0.12, seg=8)
