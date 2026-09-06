"""Procedural texture authoring.

Every texture in the kit is generated deterministically here from a seed, so
the kit reproduces byte-identically and needs no external asset library.  Each
material family gets an albedo / normal / roughness set plus a shared salt-dirt
mask, authored at the texel density declared in :mod:`world_kit.dna`.
"""

from __future__ import annotations

import math
import os

import numpy as np
from PIL import Image

from . import dna

SEED_BASE = 20260906


# --------------------------------------------------------------------------- #
# noise primitives (all tileable)
# --------------------------------------------------------------------------- #
def _smooth(t):
    return t * t * (3.0 - 2.0 * t)


def value_noise(freq: int, size: int, seed: int) -> np.ndarray:
    """Tileable bilinear value noise in [0, 1]."""
    rng = np.random.default_rng(seed)
    g = rng.random((freq, freq)).astype(np.float32)
    xs = np.arange(size, dtype=np.float32) * (freq / size)
    fl = np.floor(xs)
    x0 = fl.astype(int) % freq
    x1 = (x0 + 1) % freq
    fx = _smooth(xs - fl).astype(np.float32)
    a = g[np.ix_(x0, x0)]
    b = g[np.ix_(x0, x1)]
    c = g[np.ix_(x1, x0)]
    d = g[np.ix_(x1, x1)]
    top = a * (1.0 - fx)[None, :] + b * fx[None, :]
    bot = c * (1.0 - fx)[None, :] + d * fx[None, :]
    return top * (1.0 - fx)[:, None] + bot * fx[:, None]


def fbm(size: int, seed: int, base=4, octaves=6, gain=0.5, lacunarity=2.0) -> np.ndarray:
    out = np.zeros((size, size), dtype=np.float32)
    amp = 1.0
    tot = 0.0
    f = base
    for i in range(octaves):
        out += value_noise(int(f), size, seed + 101 * i) * amp
        tot += amp
        amp *= gain
        f *= lacunarity
    return out / tot


def ridged(size: int, seed: int, base=4, octaves=5) -> np.ndarray:
    out = np.zeros((size, size), dtype=np.float32)
    amp, tot, f = 1.0, 0.0, base
    for i in range(octaves):
        n = 1.0 - np.abs(value_noise(int(f), size, seed + 311 * i) * 2.0 - 1.0)
        out += (n * n) * amp
        tot += amp
        amp *= 0.5
        f *= 2.0
    return out / tot


def voronoi(size: int, cells: int, seed: int, jitter=0.85) -> tuple[np.ndarray, np.ndarray]:
    """Tileable F1 voronoi -> (distance, cell id)."""
    rng = np.random.default_rng(seed)
    pts = rng.random((cells, cells, 2)).astype(np.float32) * jitter + 0.5 * (1.0 - jitter)
    uv = (np.arange(size, dtype=np.float32) / size * cells)
    gx, gy = np.meshgrid(uv, uv, indexing="xy")
    cx = np.floor(gx).astype(int)
    cy = np.floor(gy).astype(int)
    best = np.full((size, size), 1e9, dtype=np.float32)
    bid = np.zeros((size, size), dtype=np.int32)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            ny = (cy + dy) % cells
            nx = (cx + dx) % cells
            p = pts[ny, nx]                       # (size, size, 2)
            px = (nx.astype(np.float32) + p[..., 0]) / cells
            py = (ny.astype(np.float32) + p[..., 1]) / cells
            ddx = gx / cells - px
            ddy = gy / cells - py
            # wrap-aware distance
            ddx -= np.round(ddx)
            ddy -= np.round(ddy)
            d = np.sqrt(ddx * ddx + ddy * ddy)
            hit = d < best
            best = np.where(hit, d, best)
            bid = np.where(hit, (ny * cells + nx).astype(np.int32), bid)
    return best, bid


def clamp(a, lo=0.0, hi=1.0):
    return np.clip(a, lo, hi)


def remap(a, lo, hi):
    return clamp((a - lo) / max(1e-6, hi - lo))


def normal_from_height(h: np.ndarray, strength=1.0) -> np.ndarray:
    """Height field -> tangent-space normal map stored as uint8 RGB."""
    dx = np.gradient(h.astype(np.float32), axis=1)
    dy = np.gradient(h.astype(np.float32), axis=0)
    n = np.stack([-dx * strength, -dy * strength, np.ones_like(dx)], axis=-1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    return ((n * 0.5 + 0.5) * 255.0).astype(np.uint8)


def srgb_u8(linear_rgb) -> np.ndarray:
    """Linear float triple -> uint8 sRGB triple."""
    out = []
    for c in linear_rgb:
        c = float(np.clip(c, 0.0, 1.0))
        s = c * 12.92 if c <= 0.0031308 else 1.055 * (c ** (1.0 / 2.4)) - 0.055
        out.append(int(round(s * 255.0)))
    return np.array(out, dtype=np.uint8)


def hex_rgb(h: int) -> np.ndarray:
    return np.array([(h >> 16) & 0xFF, (h >> 8) & 0xFF, h & 0xFF], dtype=np.uint8)


def tint(rgb_u8: np.ndarray, scale: float) -> np.ndarray:
    return np.clip(rgb_u8.astype(np.float32) * scale, 0, 255).astype(np.uint8)


def mix_rgb(a_u8: np.ndarray, b_u8: np.ndarray, m: np.ndarray) -> np.ndarray:
    """Blend two RGB arrays by a mask that may be 2D (h, w) or 3D (h, w, 3)."""
    m = np.asarray(m, dtype=np.float32)
    if m.ndim == np.asarray(a_u8).ndim - 1:
        m = m[..., None]
    return (a_u8.astype(np.float32) * (1 - m) + b_u8.astype(np.float32) * m).astype(np.uint8)


def save_rgb(path, arr):
    Image.fromarray(arr.astype(np.uint8), "RGB").save(path, optimize=True)


def save_rgba(path, arr):
    Image.fromarray(arr.astype(np.uint8), "RGBA").save(path, optimize=True)


def save_single(path, arr):
    g = np.repeat(arr[..., None].astype(np.uint8), 3, axis=-1)
    Image.fromarray(g, "RGB").save(path, optimize=True)


# --------------------------------------------------------------------------- #
# individual texture sets
# --------------------------------------------------------------------------- #
def _shared_dirt(size, seed):
    """The one weathering mask every family consumes (DNA: MK_DIRT_SALT)."""
    grime = fbm(size, seed, base=3, octaves=5)
    streaks = np.zeros((size, size), dtype=np.float32)
    rng = np.random.default_rng(seed + 7)
    for _ in range(46):
        x = int(rng.integers(0, size))
        w = int(rng.integers(3, 16))
        length = int(rng.integers(size // 8, size))
        y0 = int(rng.integers(0, size))
        n = max(1, min(length, size - y0))
        prof = np.exp(-((np.arange(size) - x) ** 2) / (2.0 * (w / 2.4) ** 2))
        col = np.zeros(size, dtype=np.float32)
        col[y0:y0 + n] = np.linspace(0.9, 0.0, n)
        streaks += np.outer(col, prof)
    streaks = clamp(streaks * 0.9)
    pool = remap(fbm(size, seed + 13, base=2, octaves=3), 0.45, 0.95)
    return clamp(grime * 0.35 + streaks * 0.45 + pool * 0.2)


def make_concrete(size, seed, out):
    base = hex_rgb(dna.PALETTE["concrete_light"])
    dark = hex_rgb(dna.PALETTE["concrete_dark"])
    mid = hex_rgb(dna.PALETTE["concrete_mid"])
    salt = hex_rgb(dna.PALETTE["salt_crust"])

    grain = fbm(size, seed, base=64, octaves=3)
    mottle = fbm(size, seed + 1, base=6, octaves=6)
    blotch = fbm(size, seed + 2, base=2, octaves=4)

    col = np.zeros((size, size, 3), dtype=np.float32) + base
    col = mix_rgb(col, mid, remap(mottle, 0.3, 0.75))
    col = mix_rgb(col, dark, remap(blotch, 0.62, 0.98) * 0.6)
    col = mix_rgb(col, tint(base, 1.08), remap(grain, 0.55, 0.95) * 0.35)

    # board-form lines every 0.5 m of a 4 m tile -> 8 lines
    y = np.arange(size, dtype=np.float32) / size
    lines = np.abs(((y * 8.0) % 1.0) - 0.5)
    board = remap(1.0 - lines * 16.0, 0.0, 1.0)
    board = board[None, :] * 0.5
    col = mix_rgb(col, dark, board[..., None].repeat(3, axis=-1) * 0.55)

    # blowholes: small, sparse, clustered in damp blotches
    holes, _ = voronoi(size, 70, seed + 5, jitter=0.9)
    hole_mask = remap(1.0 - holes * 60.0, 0.0, 1.0)
    clust = remap(fbm(size, seed + 7, base=4, octaves=3), 0.45, 0.85)
    hole_mask = hole_mask * clust
    col = mix_rgb(col, tint(dark, 0.72), hole_mask[..., None] * 0.85)

    dirt = _shared_dirt(size, seed + 9)
    col = mix_rgb(col, dark, (dirt * 0.45)[..., None])
    saltm = remap(fbm(size, seed + 21, base=5, octaves=4), 0.62, 0.99)
    col = mix_rgb(col, salt, (saltm * 0.30)[..., None])

    hgt = mottle * 0.35 + grain * 0.25 + hole_mask * 0.9 + board[..., 0] * 0.5
    save_rgb(f"{out}_albedo.png", col)
    save_rgb(f"{out}_normal.png", normal_from_height(hgt, 2.2))
    rough = 0.78 + (mottle - 0.5) * 0.12 + dirt * 0.14
    save_single(f"{out}_rough.png", (clamp(rough) * 255))
    save_single(f"{out}_dirt.png", (clamp(dirt) * 255))


def make_tile(size, seed, out):
    body = hex_rgb(dna.PALETTE["tile_body"])
    glaze = hex_rgb(dna.PALETTE["tile_glaze"])
    grout = hex_rgb(0x54503F)
    salt = hex_rgb(dna.PALETTE["salt_crust"])

    cells = 10                                   # 0.2 m tiles in a 2.0 m tile-set
    cs = size / cells
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    lx = (xx % cs) / cs
    ly = (yy % cs) / cs
    edge = np.minimum(np.minimum(lx, 1 - lx), np.minimum(ly, 1 - ly))
    grout_m = remap(1.0 - edge * 26.0, 0.0, 1.0)

    # per-tile identity straight from the tile grid (no voronoi wobble)
    yy2, xx2 = np.mgrid[0:size, 0:size].astype(np.int64)
    cid = (yy2 // cs).astype(np.int64) * cells + (xx2 // cs).astype(np.int64)
    rng = np.random.default_rng(seed)
    per = rng.random(cells * cells).astype(np.float32)
    var = per[cid]
    col = np.zeros((size, size, 3), dtype=np.float32) + body
    col = mix_rgb(col, tint(body, 0.90), (remap(var, 0.0, 1.0) * 0.55)[..., None])
    col = mix_rgb(col, grout, (grout_m * 0.95)[..., None])
    # glazed tiles: a minority of tiles carry a soft teal sheen across the face
    glazed = remap(var, 0.62, 0.98)
    face = remap(edge, 0.04, 0.30)          # 0 at grout -> 1 at tile centre
    col = mix_rgb(col, glaze, (glazed * face * 0.45)[..., None])
    # salt-etched rim just inside the grout
    rim = remap(1.0 - edge * 10.0, 0.0, 1.0)
    col = mix_rgb(col, tint(body, 1.1), (rim * 0.30)[..., None])

    saltm = remap(fbm(size, seed + 3, base=8, octaves=4), 0.60, 0.99)
    col = mix_rgb(col, salt, (saltm * 0.22)[..., None])
    dirt = _shared_dirt(size, seed + 5)
    col = mix_rgb(col, tint(grout, 0.75), (dirt * 0.30)[..., None])

    hgt = grout_m * -0.9 + edge * 0.15 + var * 0.05
    save_rgb(f"{out}_albedo.png", col)
    save_rgb(f"{out}_normal.png", normal_from_height(hgt, 2.6))
    rough = 0.22 + grout_m * 0.55 + (1.0 - glazed * face) * 0.10 + dirt * 0.12
    save_single(f"{out}_rough.png", (clamp(rough) * 255))
    save_single(f"{out}_dirt.png", (clamp(dirt) * 255))


def make_paint(size, seed, out, paint_hex, primer_hex, chip_scale=1.0):
    paint = hex_rgb(paint_hex)
    primer = hex_rgb(primer_hex)
    rust = hex_rgb(dna.PALETTE["rust"])
    salt = hex_rgb(dna.PALETTE["salt_crust"])

    grain = fbm(size, seed, base=48, octaves=3)
    mottle = fbm(size, seed + 1, base=8, octaves=5)
    col = np.zeros((size, size, 3), dtype=np.float32) + paint
    col = mix_rgb(col, tint(paint, 1.10), (remap(mottle, 0.5, 0.9) * 0.4)[..., None])
    col = mix_rgb(col, tint(paint, 0.86), (remap(mottle, 0.05, 0.4) * 0.45)[..., None])

    # chips: paint fails, primer shows through, rust blooms below the chip
    chip_n = fbm(size, seed + 2, base=24, octaves=4)
    chip = remap(chip_n, 0.60 / chip_scale, 0.78 / chip_scale)
    chip *= remap(fbm(size, seed + 3, base=4, octaves=3), 0.35, 0.9)
    col = mix_rgb(col, primer, (chip * 0.92)[..., None])

    bloom_n = fbm(size, seed + 4, base=12, octaves=5)
    bloom = remap(bloom_n, 0.55, 0.95) * remap(chip, 0.15, 0.7)
    col = mix_rgb(col, rust, (bloom * 0.55)[..., None])

    saltm = remap(fbm(size, seed + 6, base=6, octaves=4), 0.66, 1.0)
    col = mix_rgb(col, salt, (saltm * 0.22)[..., None])
    dirt = _shared_dirt(size, seed + 8)
    col = mix_rgb(col, tint(primer, 0.5), (dirt * 0.32)[..., None])

    hgt = grain * 0.20 + mottle * 0.15 - chip * 0.55 - bloom * 0.30
    save_rgb(f"{out}_albedo.png", col)
    save_rgb(f"{out}_normal.png", normal_from_height(hgt, 1.9))
    rough = 0.46 + mottle * 0.14 + chip * 0.30 + dirt * 0.14
    save_single(f"{out}_rough.png", (clamp(rough) * 255))
    save_single(f"{out}_dirt.png", (clamp(dirt) * 255))


def make_steel(size, seed, out):
    base = hex_rgb(dna.PALETTE["steel_aged"])
    rust = hex_rgb(dna.PALETTE["rust"])
    dark = hex_rgb(0x3A3733)

    streak = value_noise(6, size, seed) * 0.5 + value_noise(192, size, seed + 1) * 0.5
    mottle = fbm(size, seed + 2, base=10, octaves=5)
    col = np.zeros((size, size, 3), dtype=np.float32) + base
    col = mix_rgb(col, tint(base, 1.14), (remap(streak, 0.5, 0.95) * 0.35)[..., None])
    col = mix_rgb(col, dark, (remap(mottle, 0.0, 0.35) * 0.5)[..., None])

    rustm = remap(fbm(size, seed + 3, base=14, octaves=6), 0.58, 0.92)
    rustm *= remap(mottle, 0.3, 1.0)
    col = mix_rgb(col, rust, (rustm * 0.75)[..., None])
    pitting, _ = voronoi(size, 40, seed + 4, jitter=0.9)
    pit = remap(1.0 - pitting * 40.0, 0.0, 1.0)
    col = mix_rgb(col, dark, (pit * 0.5)[..., None])

    hgt = mottle * 0.25 - pit * 0.8 - rustm * 0.2
    save_rgb(f"{out}_albedo.png", col)
    save_rgb(f"{out}_normal.png", normal_from_height(hgt, 1.7))
    rough = 0.42 + mottle * 0.16 + rustm * 0.28 + pit * 0.2
    save_single(f"{out}_rough.png", (clamp(rough) * 255))


def make_brass(size, seed, out):
    brass = hex_rgb(dna.PALETTE["brass"])
    patina = hex_rgb(dna.PALETTE["brass_patina"])
    dark = hex_rgb(0x4A3A1C)

    brush = value_noise(128, size, seed) * 0.6 + value_noise(384, size, seed + 1) * 0.4
    mottle = fbm(size, seed + 2, base=8, octaves=5)
    col = np.zeros((size, size, 3), dtype=np.float32) + brass
    col = mix_rgb(col, tint(brass, 1.16), (remap(brush, 0.55, 1.0) * 0.4)[..., None])
    col = mix_rgb(col, dark, (remap(mottle, 0.0, 0.3) * 0.45)[..., None])
    verd = remap(fbm(size, seed + 3, base=6, octaves=5), 0.58, 0.95)
    col = mix_rgb(col, patina, (verd * 0.72)[..., None])

    hgt = brush * 0.10 + mottle * 0.10 - verd * 0.25
    save_rgb(f"{out}_albedo.png", col)
    save_rgb(f"{out}_normal.png", normal_from_height(hgt, 1.1))
    rough = 0.20 + mottle * 0.10 + verd * 0.40
    save_single(f"{out}_rough.png", (clamp(rough) * 255))


def make_wood(size, seed, out):
    base = hex_rgb(dna.PALETTE["wood_slat"])
    dark = hex_rgb(0x3E2C1D)
    salt = hex_rgb(dna.PALETTE["salt_crust"])

    warp = fbm(size, seed, base=4, octaves=4)
    rings = np.sin((np.arange(size, dtype=np.float32)[None, :] / size * 15.0 + warp * 2.2)
                   * math.pi * 2.0)
    rings = remap(rings, -1.0, 1.0)
    col = np.zeros((size, size, 3), dtype=np.float32) + base
    col = mix_rgb(col, dark, (rings * 0.30)[..., None])
    grain = fbm(size, seed + 1, base=96, octaves=3)
    col = mix_rgb(col, tint(base, 1.12), (remap(grain, 0.55, 1.0) * 0.3)[..., None])
    wet = remap(fbm(size, seed + 2, base=3, octaves=4), 0.55, 1.0)
    col = mix_rgb(col, tint(dark, 0.7), (wet * 0.4)[..., None])
    saltm = remap(fbm(size, seed + 3, base=6, octaves=4), 0.68, 1.0)
    col = mix_rgb(col, salt, (saltm * 0.28)[..., None])

    hgt = rings * 0.25 + grain * 0.15 - wet * 0.2
    save_rgb(f"{out}_albedo.png", col)
    save_rgb(f"{out}_normal.png", normal_from_height(hgt, 1.6))
    rough = 0.62 + rings * 0.10 + wet * 0.2 + grain * 0.08
    save_single(f"{out}_rough.png", (clamp(rough) * 255))


def make_salt(size, seed, out):
    crust = hex_rgb(dna.PALETTE["salt_crust"])
    base = hex_rgb(dna.PALETTE["concrete_mid"])
    v, cid = voronoi(size, 34, seed, jitter=0.95)
    rng = np.random.default_rng(seed)
    per = rng.random(34 * 34).astype(np.float32)
    col = np.zeros((size, size, 3), dtype=np.float32) + base
    mask = remap(1.0 - v * 30.0, 0.0, 1.0)
    mask = clamp(mask * remap(per[cid], 0.15, 1.0))
    mask *= remap(fbm(size, seed + 1, base=5, octaves=5), 0.35, 0.95)
    col = mix_rgb(col, crust, (mask * 0.95)[..., None])
    col = mix_rgb(col, tint(crust, 0.86), (remap(v * 40.0, 0.0, 1.0) * mask * 0.5)[..., None])

    hgt = mask * 0.9 - remap(v * 40.0, 0.0, 1.0) * mask * 0.4
    save_rgb(f"{out}_albedo.png", col)
    save_rgb(f"{out}_normal.png", normal_from_height(hgt, 2.4))
    rough = 0.55 + mask * 0.4
    save_single(f"{out}_rough.png", (clamp(rough) * 255))


def make_enamel(size, seed, out):
    white = hex_rgb(dna.PALETTE["salt_crust"])
    teal = hex_rgb(dna.PALETTE["paint_teal"])
    edge = hex_rgb(0x9AA08C)
    col = np.zeros((size, size, 3), dtype=np.float32) + white
    # rolled rim + bolt holes are baked so signage reads without extra geometry
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32) / size
    border = np.minimum(np.minimum(xx, 1 - xx), np.minimum(yy, 1 - yy))
    rim = remap(1.0 - border * 26.0, 0.0, 1.0)
    col = mix_rgb(col, edge, (rim * 0.8)[..., None])
    for (bx, by) in ((0.07, 0.14), (0.93, 0.14), (0.07, 0.86), (0.93, 0.86)):
        d = np.sqrt((xx - bx) ** 2 + ((yy - by) * 1.0) ** 2)
        col = mix_rgb(col, hex_rgb(0x2A2A28), (remap(1.0 - d * 60.0, 0.0, 1.0))[..., None])
    mottle = fbm(size, seed, base=24, octaves=4)
    col = mix_rgb(col, tint(white, 0.96), (remap(mottle, 0.5, 1.0) * 0.25)[..., None])
    chip = remap(fbm(size, seed + 1, base=60, octaves=3), 0.72, 0.92) * rim
    col = mix_rgb(col, teal, (chip * 0.7)[..., None])

    hgt = -rim * 0.5 + mottle * 0.05
    save_rgb(f"{out}_albedo.png", col)
    save_rgb(f"{out}_normal.png", normal_from_height(hgt, 1.2))
    rough = 0.18 + mottle * 0.08 + chip * 0.3
    save_single(f"{out}_rough.png", (clamp(rough) * 255))


def make_water(size, seed, out):
    n1 = fbm(size, seed, base=8, octaves=5)
    n2 = fbm(size, seed + 1, base=22, octaves=4)
    hgt = n1 * 0.6 + n2 * 0.4
    save_rgb(f"{out}_normal.png", normal_from_height(hgt, 0.9))
    col = np.zeros((size, size, 3), dtype=np.float32) + hex_rgb(dna.PALETTE["water_brine"])
    col = mix_rgb(col, hex_rgb(0x1E5D60), (remap(hgt, 0.4, 0.9) * 0.6)[..., None])
    save_rgb(f"{out}_albedo.png", col)


def make_decal_waterline(size, seed, out):
    """4.0 x 1.6 m sheet: tide band + salt bloom + downward streaks (RGBA)."""
    w = size
    h = max(1, size // 4)                       # 4 m x 1.6 m aspect
    v = (np.arange(h, dtype=np.float32) / h)[:, None]
    band = np.exp(-((v - 0.55) ** 2) / (2.0 * 0.16 ** 2))
    tide = remap(fbm(w, seed, base=10, octaves=4)[0, :][None, :] * 0.6 + 0.4, 0.0, 1.0)
    a = clamp(band * tide * 1.15)
    bloom = remap(fbm(w, seed + 1, base=6, octaves=5), 0.45, 0.95)[:h, :]
    low = remap(1.0 - v / 0.62, 0.0, 1.0)
    a = clamp(a + bloom * low * 0.55)
    rng = np.random.default_rng(seed + 2)
    streaks = np.zeros((h, w), dtype=np.float32)
    for _ in range(38):
        x0 = int(rng.integers(0, w))
        ww = float(rng.uniform(2.0, 9.0))
        ln = int(rng.uniform(h * 0.2, h * 0.8))
        y0 = int(rng.uniform(0, h * 0.4))
        prof = np.exp(-((np.arange(w) - x0) ** 2) / (2 * ww ** 2))
        col = np.zeros(h, dtype=np.float32)
        col[y0:min(h, y0 + ln)] = np.linspace(0.85, 0.0, min(h, y0 + ln) - y0)
        streaks += np.outer(col, prof)
    a = clamp(a + streaks * 0.8)
    rgb = np.zeros((h, w, 3), dtype=np.float32)
    dark = hex_rgb(0x3B362C).astype(np.float32)
    salt = hex_rgb(dna.PALETTE["salt_crust"]).astype(np.float32)
    m = (bloom * low)[..., None]
    rgb = dark[None, None, :] * (1 - m) + salt[None, None, :] * m
    save_rgba(out, np.dstack([rgb.astype(np.uint8), (a * 235).astype(np.uint8)]))


def make_decal_crack(size, seed, out):
    """4.0 x 4.0 m crack / spall sheet (RGBA)."""
    a = np.zeros((size, size), dtype=np.float32)
    rgb = np.zeros((size, size, 3), dtype=np.float32) + hex_rgb(0x4A443A).astype(np.float32)
    rng = np.random.default_rng(seed)

    def stamp(x, y, radius, alpha, colour):
        """Blend a soft disc into the sheet (windowed, so it stays cheap)."""
        r = max(2, int(radius * 3.0))
        x0, x1 = max(0, int(x) - r), min(size, int(x) + r)
        y0, y1 = max(0, int(y) - r), min(size, int(y) + r)
        if x1 <= x0 or y1 <= y0:
            return
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        d = np.sqrt((xx - x) ** 2 + (yy - y) ** 2)
        m = remap(1.0 - d / max(radius, 1e-3), 0.0, 1.0) * alpha
        sub_a = a[y0:y1, x0:x1]
        a[y0:y1, x0:x1] = np.maximum(sub_a, m)
        w = np.maximum(m, sub_a)[..., None] * 0.6
        rgb[y0:y1, x0:x1] = (rgb[y0:y1, x0:x1] * (1 - w) +
                             colour[None, None, :] * w)

    def walk(x, y, ang, width, steps, branch):
        for i in range(steps):
            ang += float(rng.normal(0, 0.22))
            x += math.cos(ang) * 6.0
            y += math.sin(ang) * 6.0
            if not (0 <= x < size and 0 <= y < size):
                return
            r = max(1.2, width * (1.0 - i / steps * 0.6))
            stamp(x, y, r, 0.92, hex_rgb(0x241F19).astype(np.float32))
            if branch and rng.random() < 0.10:
                walk(x, y, ang + float(rng.uniform(-1.2, 1.2)), width * 0.55,
                     max(2, steps // 4), False)

    for _ in range(3):
        walk(float(rng.uniform(size * 0.2, size * 0.8)), float(rng.uniform(0, size * 0.2)),
             float(rng.uniform(1.0, 2.1)), float(rng.uniform(3.5, 6.0)), size // 5, True)
    for _ in range(70):
        walk(float(rng.uniform(0, size)), float(rng.uniform(0, size)),
             float(rng.uniform(0, 6.28)), 1.3, int(rng.uniform(4, 16)), False)

    # spalled patches with exposed aggregate
    agg, _ = voronoi(size, 90, seed + 6, jitter=0.9)
    grey = mix_rgb(np.full((size, size, 3), 0x6E6A5E, dtype=np.uint8).astype(np.float32),
                   np.full((size, size, 3), 0x9A968A, dtype=np.uint8).astype(np.float32),
                   remap(1.0 - agg * 90.0, 0.0, 1.0)[..., None])
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    for _ in range(5):
        cx = float(rng.uniform(0.1, 0.9) * size)
        cy = float(rng.uniform(0.1, 0.9) * size)
        rr = float(rng.uniform(0.04, 0.10) * size)
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        blob = remap(1.0 - d / rr, 0.0, 1.0) * remap(fbm(size, seed + 5, base=12, octaves=4), 0.3, 0.9)
        a = np.maximum(a, blob * 0.95)
        rgb = rgb * (1 - blob[..., None]) + grey * blob[..., None]
    save_rgba(out, np.dstack([rgb.astype(np.uint8), (clamp(a) * 240).astype(np.uint8)]))


# --------------------------------------------------------------------------- #
# driver
# --------------------------------------------------------------------------- #
SET_SIZES = {
    "concrete": 1024, "tile": 1024, "paint_teal": 1024, "paint_oxide": 1024,
    "steel": 1024, "brass": 512, "wood": 512, "salt": 512, "enamel": 512,
    "water": 512, "decal_waterline": 1024, "decal_crack": 1024,
}


def build_all(tex_dir: str, only=None) -> list[str]:
    os.makedirs(tex_dir, exist_ok=True)
    s = SEED_BASE
    jobs = [
        ("concrete", lambda o: make_concrete(SET_SIZES["concrete"], s + 1, o)),
        ("tile", lambda o: make_tile(SET_SIZES["tile"], s + 2, o)),
        ("paint_teal", lambda o: make_paint(SET_SIZES["paint_teal"], s + 3, o,
                                            dna.PALETTE["paint_teal"],
                                            dna.PALETTE["oxide_primer"], 1.0)),
        ("paint_oxide", lambda o: make_paint(SET_SIZES["paint_oxide"], s + 4, o,
                                             dna.PALETTE["oxide_primer"],
                                             dna.PALETTE["rust"], 0.8)),
        ("steel", lambda o: make_steel(SET_SIZES["steel"], s + 5, o)),
        ("brass", lambda o: make_brass(SET_SIZES["brass"], s + 6, o)),
        ("wood", lambda o: make_wood(SET_SIZES["wood"], s + 7, o)),
        ("salt", lambda o: make_salt(SET_SIZES["salt"], s + 8, o)),
        ("enamel", lambda o: make_enamel(SET_SIZES["enamel"], s + 9, o)),
        ("water", lambda o: make_water(SET_SIZES["water"], s + 10, o)),
        ("decal_waterline", lambda o: make_decal_waterline(SET_SIZES["decal_waterline"],
                                                           s + 11, f"{o}.png")),
        ("decal_crack", lambda o: make_decal_crack(SET_SIZES["decal_crack"],
                                                   s + 12, f"{o}.png")),
    ]
    written = []
    for key, fn in jobs:
        if only and key not in only:
            continue
        out = os.path.join(tex_dir, f"MK_{key}")
        fn(out)
        written.append(key)
    return written
