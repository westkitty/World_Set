"""02_WALLS - straight, corner, opening and damaged modules."""

from .. import dna
from ..geo import vec
from .architecture import arch_profile

D = dna.DIMENSIONS
BAY = D["bay_w"]
H = D["wall_h"]
T = D["wall_t"]
DW, DH = D["door_w"], D["door_h"]


def _dado(asset, key, length, center, along_x=True):
    p = asset.part(key, "MK_CERAMIC_TILE")
    if along_x:
        p.box(center, (length, 0.06, 1.2))
    else:
        p.box(center, (0.06, length, 1.2))
    return p


def _cap(asset, key, length, center, along_x=True):
    p = asset.part(key, "MK_CONCRETE_STRUCT")
    if along_x:
        p.box(center, (length, T + 0.1, 0.18))
    else:
        p.box(center, (T + 0.1, length, 0.18))
    return p


def standard_a(asset):
    asset.part("body", "MK_CONCRETE_STRUCT").box(vec(BAY / 2, 0, H / 2), (BAY, T, H))
    _dado(asset, "dadoP", BAY, vec(BAY / 2, T / 2 + 0.02, 0.6))
    _dado(asset, "dadoN", BAY, vec(BAY / 2, -T / 2 - 0.02, 0.6))
    _cap(asset, "cap", BAY, vec(BAY / 2, 0, H - 0.09))


def standard_b(asset):
    standard_a(asset)
    recess = asset.part("recess", "MK_STEEL_AGED")
    recess.box(vec(BAY / 2, T / 2 + 0.02, 1.5), (1.2, 0.05, 2.0))
    frame = asset.part("recframe", "MK_STEEL_PRIMER")
    frame.box(vec(BAY / 2, T / 2 + 0.05, 2.52), (1.32, 0.05, 0.08))
    frame.box(vec(BAY / 2, T / 2 + 0.05, 0.48), (1.32, 0.05, 0.08))
    frame.box(vec(BAY / 2 - 0.62, T / 2 + 0.05, 1.5), (0.08, 0.05, 2.1))
    frame.box(vec(BAY / 2 + 0.62, T / 2 + 0.05, 1.5), (0.08, 0.05, 2.1))
    cond = asset.part("conduit", "MK_STEEL_PRIMER", uv_mode="cyl")
    cond.cyl(vec(BAY - 0.5, -T / 2 - 0.05, 0), 0.035, 0.035, H, axis="Z", seg=10)


def corner_inner(asset):
    a = asset.part("wA", "MK_CONCRETE_STRUCT").box(vec(BAY / 2, BAY - T / 2, H / 2), (BAY, T, H))
    b = asset.part("wB", "MK_CONCRETE_STRUCT").box(vec(BAY - T / 2, BAY / 2, H / 2), (T, BAY, H))
    _dado(asset, "dadoA", BAY, vec(BAY / 2, BAY - T - 0.03 + 0.0, 0.6), True)
    _dado(asset, "dadoB", BAY, vec(BAY - T - 0.03, BAY / 2, 0.6), False)
    _cap(asset, "capA", BAY, vec(BAY / 2, BAY - T / 2, H - 0.09), True)
    _cap(asset, "capB", BAY - T, vec(BAY - T / 2, (BAY - T) / 2, H - 0.09), False)


def corner_outer(asset):
    asset.part("wA", "MK_CONCRETE_STRUCT").box(vec(BAY / 2, -T / 2, H / 2), (BAY, T, H))
    asset.part("wB", "MK_CONCRETE_STRUCT").box(vec(T / 2, BAY / 2, H / 2), (T, BAY, H))
    asset.part("quoin", "MK_CONCRETE_STRUCT").box(vec(0.0, 0.0, H / 2), (0.62, 0.62, H))
    _dado(asset, "dadoA", BAY, vec(BAY / 2, -T / 2 - 0.03, 0.6), True)
    _dado(asset, "dadoB", BAY, vec(-T / 2 - 0.03, BAY / 2, 0.6), False)
    _cap(asset, "capA", BAY, vec(BAY / 2, -T / 2, H - 0.09), True)
    _cap(asset, "capB", BAY, vec(T / 2, BAY / 2, H - 0.09), False)


def doorway(asset):
    side = (BAY - DW) / 2
    asset.part("L", "MK_CONCRETE_STRUCT").box(vec(side / 2, 0, DH / 2), (side, T, DH))
    asset.part("R", "MK_CONCRETE_STRUCT").box(vec(BAY - side / 2, 0, DH / 2), (side, T, DH))
    asset.part("head", "MK_CONCRETE_STRUCT").box(vec(BAY / 2, 0, (H + DH) / 2), (DW, T, H - DH))
    _dado(asset, "dadoL", side, vec(side / 2, T / 2 + 0.02, 0.6))
    _dado(asset, "dadoR", side, vec(BAY - side / 2, T / 2 + 0.02, 0.6))
    _cap(asset, "cap", BAY, vec(BAY / 2, 0, H - 0.09))

    s = asset.part("surround", "MK_STEEL_PRIMER")
    s.box(vec((BAY - DW) / 2 - 0.06, 0, DH / 2), (0.16, T + 0.08, DH))
    s.box(vec((BAY + DW) / 2 + 0.06, 0, DH / 2), (0.16, T + 0.08, DH))
    s.box(vec(BAY / 2, 0, DH + 0.06), (DW + 0.44, T + 0.08, 0.16))
    s.box(vec(BAY / 2, 0, 0.03), (DW + 0.3, T + 0.1, 0.06))


def window(asset):
    body = asset.part("body", "MK_CONCRETE_STRUCT")
    body.box(vec(BAY / 2, 0, H / 2), (BAY, T, H))
    w = D["window_w"]
    sill = D["window_sill"]
    cutter = asset.cutter("cut", lambda p: (
        p.box(vec(BAY / 2, 0, (sill + 2.4) / 2), (w, T * 3, 2.4 - sill)),
        p.cyl(vec(BAY / 2, -T * 1.5, 2.4), w / 2, w / 2, T * 3, axis="Y", seg=20),
    ))
    asset.boolean("body", cutter)
    _dado(asset, "dadoP", BAY, vec(BAY / 2, T / 2 + 0.02, 0.6))
    _dado(asset, "dadoN", BAY, vec(BAY / 2, -T / 2 - 0.02, 0.6))
    _cap(asset, "cap", BAY, vec(BAY / 2, 0, H - 0.09))
    sillp = asset.part("sill", "MK_CERAMIC_TILE")
    sillp.box(vec(BAY / 2, 0.06, sill - 0.04), (w + 0.3, 0.5, 0.08), rot=(0.12, 0, 0))


def breach(asset):
    body = asset.part("body", "MK_CONCRETE_STRUCT")
    body.box(vec(BAY / 2, 0, H / 2), (BAY, T, H))
    blob = asset.cutter("blob", lambda p: (
        p.box(vec(BAY - 0.9, 0, H + 0.2), (1.9, T * 3, 1.7), rot=(0.3, 0.2, 0.5)),
        p.cyl(vec(BAY - 1.1, 0, H - 0.7), 0.7, 0.5, T * 3, axis="Y", seg=10),
        p.box(vec(BAY - 0.2, 0, H - 1.6), (0.9, T * 3, 1.6), rot=(0, 0.4, 0)),
    ))
    asset.boolean("body", blob)
    _dado(asset, "dadoN", BAY, vec(BAY / 2, -T / 2 - 0.02, 0.6))
    reb = asset.part("rebar", "MK_STEEL_AGED", uv_mode="cyl")
    for i, (x, z, r) in enumerate([(BAY - 1.3, H - 0.5, 0.015), (BAY - 1.0, H - 0.8, 0.015),
                                   (BAY - 1.6, H - 0.3, 0.015)]):
        reb.cyl(vec(x, 0, z), 0.015, 0.015, 0.6, axis="Z", seg=6, rot_offset=i)
    rubble = asset.part("rubble", "MK_CONCRETE_STRUCT")
    import random
    rnd = random.Random(7)
    for i in range(7):
        x = BAY - 1.6 + rnd.uniform(-0.4, 1.2)
        s = rnd.uniform(0.12, 0.3)
        rubble.box(vec(x, rnd.uniform(-0.3, 0.3), s / 2), (s, s * 0.8, s),
                   rot=(rnd.uniform(0, 3), rnd.uniform(0, 3), rnd.uniform(0, 3)))
