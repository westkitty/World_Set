#!/usr/bin/env python3
"""WORLD KIT v2 "DOUBLE" — second texture bakery.

Adds the 18 textures the v2 assets need, baked at 512 px (2x the density of
the v1 set) and in the same procedural, seeded, PIL+numpy style: no photo
source, no external assets, deterministic output.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.join(os.path.dirname(__file__), '..', 'WorldKit', 'tex')
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(2025)

FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
S = 512


def save(arr, name):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(os.path.join(OUT, name))
    print('tex', name)


def savep(pil, name):
    pil.save(os.path.join(OUT, name))
    print('tex', name)


def noise(h, w, s=1.0):
    return rng.normal(0, 1, (h, w)) * s


def fbm(h, w, octaves=4, base=8):
    acc = np.zeros((h, w))
    amp = 1.0
    for o in range(octaves):
        n = base * 2 ** o
        small = rng.random((max(2, n), max(2, n)))
        im = Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        acc += np.asarray(im, dtype=float) / 255.0 * amp
        amp *= 0.5
    acc -= acc.min()
    return acc / max(acc.max(), 1e-6)


def text_img(size, bg, items, mode='RGB'):
    """items: (xy, text, fontpath, px, fill, anchor)"""
    pil = Image.new(mode, size, bg)
    d = ImageDraw.Draw(pil)
    for xy, txt, fp, px, fill, anchor in items:
        d.text(xy, txt, font=ImageFont.truetype(fp, px), fill=fill, anchor=anchor)
    return pil, d


# ------------------------------------------------------------------ surfaces
def tex_plywood():
    h = w = S
    base = np.zeros((h, w, 3)) + np.array([150, 116, 74])
    chips = fbm(h, w, 5, 10)
    base *= (0.72 + 0.5 * chips)[:, :, None]
    # OSB flakes: short bright rectangles at random angles
    pil = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    for _ in range(420):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        L, W2 = rng.uniform(18, 54), rng.uniform(6, 14)
        a = rng.uniform(0, np.pi)
        dx, dy = np.cos(a) * L / 2, np.sin(a) * L / 2
        px, py = -np.sin(a) * W2 / 2, np.cos(a) * W2 / 2
        c = int(rng.uniform(110, 205))
        d.polygon([(x - dx + px, y - dy + py), (x + dx + px, y + dy + py),
                   (x + dx - px, y + dy - py), (x - dx - px, y - dy - py)],
                  fill=(c, int(c * 0.79), int(c * 0.52)))
    arr = np.asarray(pil, dtype=float) + noise(h, w, 7)[:, :, None]
    save(arr, 'plywood.png')


def tex_cinderblock():
    h = w = S
    img = np.zeros((h, w, 3)) + np.array([126, 126, 120])
    img *= (0.80 + 0.34 * fbm(h, w, 4, 12))[:, :, None]
    pil = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    bh = S // 4                      # 4 courses
    for r in range(4):
        y = r * bh
        d.line([(0, y), (w, y)], fill=(96, 95, 90), width=5)
        off = 0 if r % 2 == 0 else S // 4
        for c in range(2):
            x = (off + c * S // 2) % S
            d.line([(x, y), (x, y + bh)], fill=(96, 95, 90), width=5)
    arr = np.asarray(pil, dtype=float)
    arr += noise(h, w, 9)[:, :, None]
    save(arr, 'cinderblock.png')


def tex_curtain_tv():
    h = w = S
    # cold, flickering TV light behind a thin curtain
    img = np.zeros((h, w, 3))
    glow = np.clip(1.15 - ((np.mgrid[0:h, 0:w][0] - h * 0.55) ** 2 / (h * 0.55) ** 2 +
                           (np.mgrid[0:h, 0:w][1] - w * 0.5) ** 2 / (w * 0.7) ** 2), 0, 1)
    img[:, :, 0] = 40 + 120 * glow
    img[:, :, 1] = 60 + 165 * glow
    img[:, :, 2] = 95 + 205 * glow
    scan = (np.sin(np.mgrid[0:h, 0:w][0] * 0.75) * 0.5 + 0.5) * 16
    img -= scan[:, :, None]
    folds = (np.sin(np.mgrid[0:h, 0:w][1] * 0.10) * 0.5 + 0.5)
    img *= (0.68 + 0.36 * folds)[:, :, None]
    img += noise(h, w, 6)[:, :, None]
    save(img, 'curtain_tv.png')


def tex_upholstery():
    h = w = S
    img = np.zeros((h, w, 3)) + np.array([104, 62, 30])
    yy, xx = np.mgrid[0:h, 0:w]
    weave = (np.sin(xx * 0.9) * np.sin(yy * 0.9)) * 10
    img += weave[:, :, None]
    # 70s zig-zag stripe
    band = ((np.abs(((xx + yy * 0.35) % 96) - 48) < 9)).astype(float)
    img = img * (1 - band[:, :, None]) + band[:, :, None] * np.array([151, 96, 36])
    band2 = ((np.abs(((xx + yy * 0.35) % 96) - 48) < 3)).astype(float)
    img = img * (1 - band2[:, :, None]) + band2[:, :, None] * np.array([61, 78, 47])
    img *= (0.80 + 0.30 * fbm(h, w, 3, 16))[:, :, None]
    save(img, 'upholstery.png')


def tex_fabric():
    h = w = S
    img = np.zeros((h, w, 3)) + np.array([206, 205, 196])
    yy, xx = np.mgrid[0:h, 0:w]
    img += (np.sin(xx * 1.6) * 6 + np.sin(yy * 1.6) * 6)[:, :, None]
    img *= (0.86 + 0.22 * fbm(h, w, 3, 10))[:, :, None]
    save(img, 'fabric.png')


def tex_rv_stripe():
    h = w = S
    img = np.zeros((h, w, 3)) + np.array([222, 214, 196])
    yy = np.mgrid[0:h, 0:w][0]
    for y0, y1, c in ((0.34, 0.44, (188, 96, 40)), (0.45, 0.49, (150, 62, 34)),
                      (0.50, 0.53, (208, 150, 66))):
        m = ((yy > h * y0) & (yy < h * y1)).astype(float)
        img = img * (1 - m[:, :, None]) + m[:, :, None] * np.array(c)
    img *= (0.90 + 0.16 * fbm(h, w, 3, 14))[:, :, None]
    save(img, 'rv_stripe.png')


# ------------------------------------------------------------------ alpha trims
def tex_pine():
    """One needle-branch card (alpha) used many times per tree."""
    px = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(px)
    cx = S // 2
    for i in range(160):
        t = i / 159.0
        y = int(S * (0.06 + 0.9 * t))
        spread = int(S * 0.46 * (t ** 0.85))
        for s in (-1, 1):
            x2 = cx + s * spread + int(rng.uniform(-9, 9))
            y2 = y + int(rng.uniform(-10, 26))
            g = int(rng.uniform(52, 104))
            d.line([(cx, y), (x2, y2)], fill=(int(g * 0.42), g, int(g * 0.46), 255),
                   width=int(rng.uniform(2, 4)))
    d.line([(cx, 0), (cx, S)], fill=(58, 44, 30, 255), width=7)
    savep(px.filter(ImageFilter.GaussianBlur(0.6)), 'pine_needles.png')


def tex_weeds():
    px = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(px)
    for _ in range(70):
        x0 = rng.uniform(0.05, 0.95) * S
        hgt = rng.uniform(0.45, 0.95) * S
        lean = rng.uniform(-0.3, 0.3) * S
        col = (int(rng.uniform(96, 148)), int(rng.uniform(96, 140)), int(rng.uniform(52, 82)), 255)
        pts = [(x0, S)]
        for k in range(1, 7):
            f = k / 6
            pts.append((x0 + lean * f * f, S - hgt * f))
        d.line(pts, fill=col, width=int(rng.uniform(2, 5)), joint='curve')
    savep(px, 'weeds.png')


def tex_screen():
    """Insect screen: fine dark mesh, mostly open."""
    px = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(px)
    step = 10
    for i in range(0, S + 1, step):
        d.line([(i, 0), (i, S)], fill=(22, 24, 26, 255), width=3)
        d.line([(0, i), (S, i)], fill=(22, 24, 26, 255), width=3)
    savep(px, 'screen_mesh.png')


def tex_litter():
    """Scatter of paper / can / wrapper bits on a transparent decal."""
    px = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(px)
    pal = [(196, 188, 170), (172, 60, 52), (60, 82, 142), (206, 178, 62),
           (150, 150, 156), (98, 116, 82), (188, 132, 74)]
    for _ in range(150):
        x, y = rng.uniform(0, S), rng.uniform(0, S)
        r = rng.uniform(3, 11)
        c = pal[int(rng.integers(0, len(pal)))]
        k = rng.random()
        if k < 0.45:
            d.polygon([(x, y - r), (x + r, y), (x + r * 0.3, y + r), (x - r * 0.8, y + r * 0.6)],
                      fill=c + (255,))
        elif k < 0.75:
            d.ellipse([x - r, y - r * 0.55, x + r, y + r * 0.55], fill=c + (255,))
        else:
            d.rectangle([x - r, y - r * 0.35, x + r, y + r * 0.35], fill=c + (255,))
    savep(px.filter(ImageFilter.GaussianBlur(0.4)), 'litter.png')


def tex_tire_tracks():
    """Two wet tyre bands, alpha-blended over asphalt."""
    a = np.zeros((S, S))
    yy, xx = np.mgrid[0:S, 0:S]
    for cx in (S * 0.32, S * 0.68):
        band = np.exp(-((xx - cx) ** 2) / (2 * (S * 0.055) ** 2))
        tread = 0.55 + 0.45 * (np.sin(yy * 0.55) > 0.15)
        a = np.maximum(a, band * tread)
    fade = np.clip(1.25 - np.abs(yy - S / 2) / (S * 0.62), 0, 1)
    a *= fade * fbm(S, S, 3, 12) * 1.6
    a = np.clip(a, 0, 1)
    rgb = np.zeros((S, S, 3)) + np.array([26, 24, 23])
    out = np.dstack([rgb, a * 235])
    savep(Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), 'tire_tracks.png')


# ------------------------------------------------------------------ signage
def glow_text(d, xy, txt, font, fill, glow, anchor='mm'):
    d.text(xy, txt, font=font, fill=fill, anchor=anchor)


def tex_neon_open():
    pil = Image.new('RGB', (S, S // 2), (10, 6, 14))
    d = ImageDraw.Draw(pil)
    f = ImageFont.truetype(FONT_B, 104)
    d.rounded_rectangle([12, 12, S - 12, S // 2 - 12], radius=18, outline=(120, 30, 96), width=7)
    d.text((S // 2, S // 4), 'OPEN', font=f, fill=(255, 92, 196), anchor='mm')
    pil = pil.filter(ImageFilter.GaussianBlur(3))
    d = ImageDraw.Draw(pil)
    d.text((S // 2, S // 4), 'OPEN', font=f, fill=(255, 188, 236), anchor='mm')
    d.rounded_rectangle([12, 12, S - 12, S // 2 - 12], radius=18, outline=(255, 140, 214), width=3)
    savep(pil, 'neon_open.png')


def tex_sign_lot():
    pil = Image.new('RGB', (S, S // 2), (18, 34, 24))
    d = ImageDraw.Draw(pil)
    d.rectangle([8, 8, S - 8, S // 2 - 8], outline=(214, 214, 206), width=5)
    d.text((S // 2, S // 4), 'LOT 12', font=ImageFont.truetype(FONT_B, 96),
           fill=(226, 226, 218), anchor='mm')
    savep(pil, 'sign_lot.png')


def tex_sign_speed():
    pil = Image.new('RGB', (S // 2, S), (232, 231, 224))
    d = ImageDraw.Draw(pil)
    d.rectangle([10, 10, S // 2 - 10, S - 10], outline=(28, 28, 28), width=6)
    d.text((S // 4, 70), 'SPEED', font=ImageFont.truetype(FONT_B, 54), fill=(24, 24, 24), anchor='mm')
    d.text((S // 4, 130), 'LIMIT', font=ImageFont.truetype(FONT_B, 54), fill=(24, 24, 24), anchor='mm')
    d.text((S // 4, 270), '5', font=ImageFont.truetype(FONT_B, 190), fill=(24, 24, 24), anchor='mm')
    d.text((S // 4, 430), 'MPH', font=ImageFont.truetype(FONT_B, 48), fill=(24, 24, 24), anchor='mm')
    savep(pil, 'sign_speed.png')


def tex_sign_stop():
    pil = Image.new('RGB', (S, S), (150, 22, 26))
    d = ImageDraw.Draw(pil)
    r = S * 0.47
    pts = [(S / 2 + r * np.cos(np.pi / 8 + i * np.pi / 4),
            S / 2 + r * np.sin(np.pi / 8 + i * np.pi / 4)) for i in range(8)]
    d.polygon(pts, fill=(158, 24, 28), outline=(226, 226, 222))
    d.line(pts + [pts[0]], fill=(228, 228, 224), width=13)
    d.text((S / 2, S / 2), 'STOP', font=ImageFont.truetype(FONT_B, 150),
           fill=(238, 238, 234), anchor='mm')
    savep(pil, 'sign_stop.png')


def tex_sign_office():
    pil = Image.new('RGB', (S, S // 2), (16, 26, 52))
    d = ImageDraw.Draw(pil)
    d.rectangle([0, 0, S, S // 2], fill=(22, 40, 88))
    d.rectangle([10, 10, S - 10, S // 2 - 10], outline=(198, 214, 240), width=5)
    d.text((S // 2, S // 4), 'OFFICE', font=ImageFont.truetype(FONT_B, 88),
           fill=(224, 234, 248), anchor='mm')
    savep(pil.filter(ImageFilter.GaussianBlur(0.8)), 'sign_office.png')


def tex_sign_laundry():
    pil = Image.new('RGB', (S, S // 3), (226, 224, 210))
    d = ImageDraw.Draw(pil)
    d.rectangle([6, 6, S - 6, S // 3 - 6], outline=(60, 60, 58), width=4)
    d.text((S // 2, S // 6), '24 HR LAUNDRY', font=ImageFont.truetype(FONT_B, 56),
           fill=(38, 38, 40), anchor='mm')
    savep(pil, 'sign_laundry.png')


def tex_plate():
    pil = Image.new('RGB', (S, S // 2), (222, 220, 208))
    d = ImageDraw.Draw(pil)
    d.rectangle([8, 8, S - 8, S // 2 - 8], outline=(46, 62, 108), width=6)
    d.text((S // 2, 62), 'MICHIGAN', font=ImageFont.truetype(FONT, 44),
           fill=(46, 62, 108), anchor='mm')
    d.text((S // 2, 160), 'DKR 419', font=ImageFont.truetype(FONT_B, 104),
           fill=(38, 46, 74), anchor='mm')
    savep(pil, 'plate.png')


def main():
    tex_plywood()
    tex_cinderblock()
    tex_curtain_tv()
    tex_upholstery()
    tex_fabric()
    tex_rv_stripe()
    tex_pine()
    tex_weeds()
    tex_screen()
    tex_litter()
    tex_tire_tracks()
    tex_neon_open()
    tex_sign_lot()
    tex_sign_speed()
    tex_sign_stop()
    tex_sign_office()
    tex_sign_laundry()
    tex_plate()
    print('v2 textures done')


if __name__ == '__main__':
    main()
