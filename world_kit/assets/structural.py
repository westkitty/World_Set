"""05_STRUCTURAL - beams, catwalks, platforms, rails, stairs, pipes."""

import math

from .. import dna
from ..geo import vec

D = dna.DIMENSIONS
BAY = D["bay_w"]
BH, BW = D["beam_h"], D["beam_w"]
RAIL = D["rail_h"]


def beam(asset):
    web = asset.part("web", "MK_STEEL_PRIMER")
    web.box(vec(BAY / 2, 0, BH / 2), (BAY, 0.05, BH))
    for z in (0.02, BH - 0.02):
        web.box(vec(BAY / 2, 0, z), (BAY, BW, 0.05))
    for x in (0.12, BAY - 0.12):
        g = asset.part(f"gus{x:.0f}", "MK_STEEL_PRIMER")
        g.prism([(0, 0), (0.34, 0), (0, 0.34)], vec(x - 0.02, -BW / 2, 0), vec(0.04, 0, 0))
        g.prism([(0, 0), (0.34, 0), (0, 0.34)], vec(BAY - x - 0.02, -BW / 2, 0), vec(0.04, 0, 0))


def _rail(asset, key, x0, x1, y):
    p = asset.part(key, "MK_STEEL_PAINTED")
    p.box(vec((x0 + x1) / 2, y, RAIL), (x1 - x0, 0.05, 0.05))
    p.box(vec((x0 + x1) / 2, y, RAIL * 0.55), (x1 - x0, 0.04, 0.04))
    p.box(vec((x0 + x1) / 2, y, 0.07), (x1 - x0, 0.03, 0.14))
    for x in (x0 + 0.05, x1 - 0.05, (x0 + x1) / 2):
        p.box(vec(x, y, RAIL / 2), (0.05, 0.05, RAIL))
    return p


def catwalk(asset):
    cw = D["catwalk_w"]
    deck = asset.part("deck", "MK_STEEL_AGED")
    y = -cw / 2 + 0.08
    while y < cw / 2 - 0.06:
        deck.box(vec(BAY / 2, y, -0.02), (BAY, 0.02, 0.05))
        y += 0.13
    strg = asset.part("stringers", "MK_STEEL_PRIMER")
    for sy in (-cw / 2 + 0.03, cw / 2 - 0.03):
        strg.box(vec(BAY / 2, sy, -0.12), (BAY, 0.06, 0.26))
    _rail(asset, "railP", 0, BAY, cw / 2 - 0.03)
    _rail(asset, "railN", 0, BAY, -cw / 2 + 0.03)


def platform(asset):
    deck = asset.part("deck", "MK_STEEL_AGED")
    y = 0.08
    while y < BAY - 0.06:
        deck.box(vec(BAY / 2, y, -0.02), (BAY - 0.16, 0.02, 0.05))
        y += 0.13
    fr = asset.part("frame", "MK_STEEL_PRIMER")
    for sy in (0.04, BAY - 0.04):
        fr.box(vec(BAY / 2, sy, -0.16), (BAY, 0.08, 0.3))
    for sx in (0.04, BAY - 0.04):
        fr.box(vec(sx, BAY / 2, -0.16), (0.08, BAY, 0.3))
    for i, (x, y) in enumerate([(0.2, 0.2), (BAY - 0.2, 0.2), (0.2, BAY - 0.2), (BAY - 0.2, BAY - 0.2)]):
        g = asset.part(f"g{i}", "MK_STEEL_PRIMER")
        g.box(vec(x, y, -0.34), (0.2, 0.2, 0.1))


def railing(asset):
    _rail(asset, "rail", 0, 2.0, 0.0)


def stair_spiral(asset):
    R = D["stair_radius"]
    steps = D["stair_steps"]
    rise = D["stair_rise"]
    col = asset.part("col", "MK_STEEL_PRIMER", uv_mode="cyl")
    col.cyl(vec(0, 0, 0), 0.2, 0.16, steps * rise + 0.1, axis="Z", seg=16)
    ang = 2 * math.pi / steps
    rail_pts = []
    for i in range(steps):
        a = i * ang
        z = (i + 1) * rise
        t = asset.part(f"step{i}", "MK_STEEL_AGED")
        cx, cy = math.cos(a) * (R * 0.55 + 0.1), math.sin(a) * (R * 0.55 + 0.1)
        t.box(vec(cx, cy, z), (R - 0.25, 0.3, 0.05), rot=(0, 0, a))
        t.box(vec(cx, cy, z - 0.09), (R - 0.25, 0.3, 0.14), rot=(0, 0, a))
        rail_pts.append(vec(math.cos(a) * (R - 0.12), math.sin(a) * (R - 0.12), z + RAIL))
        b = asset.part(f"bal{i}", "MK_STEEL_PAINTED")
        b.box(vec(math.cos(a) * (R - 0.12), math.sin(a) * (R - 0.12), z + RAIL / 2), (0.03, 0.03, RAIL))
    rail_pts.append(vec(math.cos(steps * ang) * (R - 0.12), math.sin(steps * ang) * (R - 0.12),
                        (steps + 1) * rise + RAIL))
    sq = [(-0.03, -0.03), (0.03, -0.03), (0.03, 0.03), (-0.03, 0.03), (-0.03, -0.03)]
    hr = asset.part("handrail", "MK_STEEL_PAINTED")
    hr.sweep(rail_pts, sq)
    cap = asset.part("handcap", "MK_TIMBER", uv_mode="cyl")
    cap.sweep(rail_pts, [(-0.045, 0), (0.045, 0), (0.045, 0.03), (-0.045, 0.03), (-0.045, 0)])


def pipe_run(asset):
    p = asset.part("pipe", "MK_STEEL_PAINTED", uv_mode="cyl", uv_axis="X")
    p.cyl(vec(0, 0, 0.25), 0.11, 0.11, BAY, axis="X", seg=16)
    for x in (1.0, 3.0):
        c = asset.part(f"collar{x:.0f}", "MK_BRASS", uv_mode="cyl", uv_axis="X")
        c.ring(vec(x - 0.06, 0, 0.25), 0.14, 0.11, 0.12, axis="X", seg=16)
    for x in (0.4, 2.0, 3.6):
        b = asset.part(f"brk{x:.0f}", "MK_STEEL_AGED")
        b.box(vec(x, 0, 0.1), (0.06, 0.3, 0.2))
        b.box(vec(x, -0.16, 0.25), (0.06, 0.06, 0.3))
