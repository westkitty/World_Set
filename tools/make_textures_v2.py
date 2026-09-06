#!/usr/bin/env python3
"""WORLD KIT v2 "DOUBLE" — additional procedural textures (2x density).

Same bakery rules as make_textures.py: deterministic, PIL + numpy only, small
tiling maps that stay in the kit's colour logic. Everything here is new surface
vocabulary the v2 assets needed: masonry, board-up plywood, insect screen,
pine, weeds, litter, tyre tracks, TV light and the signage set.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.join(os.path.dirname(__file__), '..', 'WorldKit', 'tex')
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(2025)

FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def save(arr, name):
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    Image.fromarray(arr).save(os.path.join(OUT, name))
    print('tex', name)


def save_im(im, name):
    im.save(os.path.join(OUT, name))
    print('tex', name)


def noise(h, w, s=1.0):
    return rng.normal(0, 1, (h, w)) * s


def blobs(n, h, w, rmin, rmax):
    yy, xx = np.mgrid[0:h, 0:w]
    acc = np.zeros((h, w))
    for _ in range(n):
        cx, cy, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(rmin, rmax)
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
        acc += np.clip(1 - d, 0, 1) ** 2
    return acc / max(acc.max(), 1e-6)


# ------------------------------------------------------------------ masonry
def tex_cinderblock():
    h = w = 512
    img = np.zeros((h, w, 3)) + np.array([124, 123, 116])
    img += noise(h, w, 7)[..., None]
    img += (rng.random((h, w, 3)) - 0.5) * 18
    bh, bw = 128, 256                      # 40x20 cm blocks
    for r in range(h // bh):
        off = (bw // 2) if r % 2 else 0
        img[r * bh:r * bh + 6, :] *= 0.55   # bed joint
        for c in range(-1, w // bw + 1):
            x = c * bw + off
            if 0 <= x < w:
                img[r * bh:(r + 1) * bh, x:x + 6] *= 0.55   # head joint
        # slight per-course tone shift
        img[r * bh + 6:(r + 1) * bh] *= 0.95 + 0.1 * rng.random()
    img -= blobs(14, h, w, 30, 90)[..., None] * 26
    save(img, 'cinderblock.png')


def tex_plywood():
    h = w = 512
    img = np.zeros((h, w, 3)) + np.array([150, 116, 74])
    x = np.arange(w)
    grain = (np.sin(x / 6.0) * 4 + np.sin(x / 23.0) * 7 + np.sin(x / 71.0) * 10)
    img += grain[None, :, None]
    img += noise(h, w, 6)[..., None]
    for _ in range(22):                    # knots and streaks
        cx, cy, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(6, 22)
        yy, xx = np.mgrid[0:h, 0:w]
        d = np.sqrt(((xx - cx) / r) ** 2 + ((yy - cy) / (r * 0.55)) ** 2)
        img -= (np.clip(1 - d, 0, 1) ** 2)[..., None] * np.array([70, 60, 45])
    img[:4] *= 0.7
    img[-4:] *= 0.7
    save(img, 'plywood.png')


def tex_dirt():
    h = w = 512
    img = np.zeros((h, w, 3)) + np.array([74, 62, 48])
    img += blobs(40, h, w, 18, 70)[..., None] * np.array([26, 20, 12])
    img -= blobs(24, h, w, 10, 40)[..., None] * np.array([22, 20, 16])
    img += noise(h, w, 8)[..., None]
    img += (rng.random((h, w, 3)) - 0.5) * 22
    save(img, 'dirt.png')


def tex_fabric():
    h = w = 256
    base = np.array([96, 78, 60])
    img = np.zeros((h, w, 3)) + base
    yy, xx = np.mgrid[0:h, 0:w]
    weave = (np.sin(xx * np.pi / 3) * np.sin(yy * np.pi / 3)) * 9
    img += weave[..., None]
    img += (rng.random((h, w, 3)) - 0.5) * 12
    stripe = ((yy // 26) % 2) == 0
    img[stripe] *= 0.9
    save(img, 'fabric.png')


# ------------------------------------------------------------------ alpha trims
def tex_screen():
    """Insect screen: fine dark mesh, mostly transparent."""
    h = w = 256
    a = np.zeros((h, w))
    a[::4, :] = 255
    a[:, ::4] = 255
    rgb = np.zeros((h, w, 3)) + 26
    rgb += noise(h, w, 5)[..., None]
    save_im(Image.fromarray(np.clip(np.dstack([rgb, a]), 0, 255).astype(np.uint8), 'RGBA'),
            'screen_mesh.png')


def tex_pine():
    """A pine bough card: needles radiating off a centre stem."""
    h = w = 512
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx = w // 2
    for i in range(150):
        t = i / 149.0
        y = int(12 + t * (h - 24))
        spread = int((1 - t) * 0.44 * w + 18)
        for s in (-1, 1):
            x2 = cx + s * rng.integers(spread // 3, spread)
            y2 = y + rng.integers(6, 26)
            g = int(46 + 40 * rng.random())
            d.line([(cx, y), (x2, y2)], fill=(int(g * 0.42), g, int(g * 0.44), 255),
                   width=int(rng.integers(2, 4)))
    d.line([(cx, 0), (cx, h)], fill=(40, 30, 20, 255), width=6)
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    save_im(im, 'pine_bough.png')


def tex_weeds():
    h = w = 256
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for _ in range(70):
        x = rng.integers(0, w)
        top = rng.integers(30, 150)
        c = int(70 + 60 * rng.random())
        d.line([(x, h), (x + rng.integers(-22, 22), h - top)],
               fill=(int(c * 0.95), c, int(c * 0.45), 255), width=int(rng.integers(2, 5)))
    save_im(im.filter(ImageFilter.GaussianBlur(0.5)), 'weeds.png')


def tex_litter():
    """Scatter decal: crushed cans, paper, bottle caps on transparency."""
    h = w = 512
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cols = [(196, 186, 168), (150, 40, 38), (60, 82, 130), (190, 168, 60),
            (140, 140, 136), (86, 104, 70)]
    for _ in range(90):
        x, y = rng.uniform(20, w - 20), rng.uniform(20, h - 20)
        s = rng.uniform(4, 13)
        c = cols[int(rng.integers(0, len(cols)))]
        a = int(rng.integers(150, 235))
        if rng.random() < 0.45:
            d.ellipse([x - s, y - s * 0.5, x + s, y + s * 0.5], fill=c + (a,))
        else:
            d.polygon([(x - s, y), (x, y - s * 0.7), (x + s, y + s * 0.2), (x - s * 0.3, y + s)],
                      fill=c + (a,))
    save_im(im.filter(ImageFilter.GaussianBlur(0.4)), 'litter.png')


def tex_tiretracks():
    """Two dark tread bands with alpha falloff, for a ground decal."""
    h = w = 512
    a = np.zeros((h, w))
    yy, xx = np.mgrid[0:h, 0:w]
    for cx in (w * 0.32, w * 0.68):
        band = np.exp(-((xx - cx) / (w * 0.055)) ** 2)
        tread = 0.55 + 0.45 * (np.sin(yy * np.pi / 9) > -0.2)
        a = np.maximum(a, band * tread * 255)
    a *= 0.72 + 0.28 * blobs(10, h, w, 60, 200)   # break it up
    a *= np.clip(1.6 - np.abs(yy / h - 0.5) * 2.2, 0, 1)
    rgb = np.zeros((h, w, 3)) + 12 + noise(h, w, 4)[..., None]
    save_im(Image.fromarray(np.clip(np.dstack([rgb, a]), 0, 255).astype(np.uint8), 'RGBA'),
            'tire_tracks.png')


# ------------------------------------------------------------------ light / glass
def tex_curtain_tv():
    """Cold TV wash behind a curtain — the counter-note to the warm windows."""
    h = w = 256
    img = np.zeros((h, w, 3)) + np.array([26, 34, 52])
    glow = blobs(3, h, w, 60, 130)
    img += glow[..., None] * np.array([70, 110, 190])
    for y in range(0, h, 3):                       # scanline shimmer
        img[y] *= 1.06
    img += (rng.random((h, w, 3)) - 0.5) * 16
    fold = (np.sin(np.arange(w) / 7.0) * 0.5 + 0.5)[None, :, None] * 22
    img += fold
    save(img, 'curtain_tv.png')


def glow_text(im, xy, text, font, fill, glow, blur=7, anchor='mm'):
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.text(xy, text, font=font, fill=glow + (255,), anchor=anchor)
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))
    d = ImageDraw.Draw(im)
    d.text(xy, text, font=font, fill=fill + (255,), anchor=anchor)
    return im


# ------------------------------------------------------------------ signage
def tex_neon_open():
    w, h = 512, 256
    im = Image.new('RGBA', (w, h), (10, 6, 14, 255))
    d = ImageDraw.Draw(im)
    d.rectangle([6, 6, w - 7, h - 7], outline=(40, 30, 46, 255), width=4)
    f = ImageFont.truetype(FONT_B, 108)
    glow_text(im, (w // 2, h // 2 - 22), 'OPEN', f, (255, 236, 250), (255, 40, 180), blur=12)
    f2 = ImageFont.truetype(FONT_B, 30)
    glow_text(im, (w // 2, h // 2 + 68), '24 HR LAUNDRY', f2, (190, 240, 255), (30, 130, 255),
              blur=9)
    save_im(im.convert('RGB'), 'neon_open.png')


def tex_stop():
    s = 512
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    import math
    r = s * 0.47
    pts = [(s / 2 + r * math.cos(math.pi / 8 + i * math.pi / 4),
            s / 2 + r * math.sin(math.pi / 8 + i * math.pi / 4)) for i in range(8)]
    d.polygon(pts, fill=(150, 22, 24, 255), outline=(226, 226, 220, 255))
    d.line(pts + [pts[0]], fill=(226, 226, 220, 255), width=12)
    f = ImageFont.truetype(FONT_B, 150)
    d.text((s / 2, s / 2), 'STOP', font=f, fill=(238, 236, 230, 255), anchor='mm')
    a = np.array(im).astype(float)
    a[..., :3] -= (rng.random(a[..., :3].shape) * 22)          # weathering
    save_im(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 'sign_stop.png')


def tex_speed():
    w, h = 384, 512
    im = Image.new('RGB', (w, h), (222, 220, 210))
    d = ImageDraw.Draw(im)
    d.rectangle([10, 10, w - 11, h - 11], outline=(30, 30, 32), width=8)
    f1 = ImageFont.truetype(FONT_B, 52)
    f2 = ImageFont.truetype(FONT_B, 190)
    f3 = ImageFont.truetype(FONT_B, 44)
    d.text((w / 2, 74), 'SPEED', font=f1, fill=(28, 28, 30), anchor='mm')
    d.text((w / 2, 108), 'LIMIT', font=f1, fill=(28, 28, 30), anchor='mm')
    d.text((w / 2, 250), '5', font=f2, fill=(24, 24, 26), anchor='mm')
    d.text((w / 2, 420), 'M.P.H.', font=f3, fill=(28, 28, 30), anchor='mm')
    a = np.array(im).astype(float) - rng.random((h, w, 3)) * 26
    save(a, 'sign_speed.png')


def tex_lot():
    w, h = 512, 256
    im = Image.new('RGB', (w, h), (196, 190, 174))
    d = ImageDraw.Draw(im)
    d.rectangle([8, 8, w - 9, h - 9], outline=(52, 58, 52), width=7)
    f = ImageFont.truetype(FONT_B, 120)
    d.text((w / 2, h / 2), 'LOT 12', font=f, fill=(38, 46, 40), anchor='mm')
    a = np.array(im).astype(float) - rng.random((h, w, 3)) * 20
    save(a, 'sign_lot.png')


def tex_office():
    w, h = 512, 256
    im = Image.new('RGBA', (w, h), (16, 22, 34, 255))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=(70, 90, 120, 255), width=6)
    f = ImageFont.truetype(FONT_B, 92)
    glow_text(im, (w // 2, h // 2 - 14), 'OFFICE', f, (236, 244, 255), (90, 150, 255), blur=10)
    f2 = ImageFont.truetype(FONT, 30)
    glow_text(im, (w // 2, h // 2 + 66), 'RENT PAID HERE', f2, (200, 220, 240), (60, 110, 190),
              blur=7)
    save_im(im.convert('RGB'), 'sign_office.png')


def tex_laundry():
    w, h = 512, 256
    im = Image.new('RGB', (w, h), (206, 200, 186))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=(120, 116, 106), width=5)
    f = ImageFont.truetype(FONT_B, 70)
    f2 = ImageFont.truetype(FONT, 34)
    d.text((w / 2, 84), 'LAUNDRY', font=f, fill=(38, 52, 82), anchor='mm')
    d.text((w / 2, 160), 'WASH · DRY · FOLD', font=f2, fill=(58, 62, 70), anchor='mm')
    d.text((w / 2, 210), '50¢', font=f2, fill=(150, 40, 40), anchor='mm')
    a = np.array(im).astype(float) - rng.random((h, w, 3)) * 24
    save(a, 'sign_laundry.png')


def tex_plate():
    w, h = 512, 256
    im = Image.new('RGB', (w, h), (214, 212, 200))
    d = ImageDraw.Draw(im)
    d.rectangle([8, 8, w - 9, h - 9], outline=(40, 60, 46), width=7)
    f = ImageFont.truetype(FONT_B, 118)
    d.text((w / 2, h / 2 + 8), 'MI 4B7', font=f, fill=(38, 62, 46), anchor='mm')
    f2 = ImageFont.truetype(FONT, 30)
    d.text((w / 2, 34), 'MICHIGAN', font=f2, fill=(60, 80, 64), anchor='mm')
    a = np.array(im).astype(float) - rng.random((h, w, 3)) * 18
    save(a, 'plate.png')


def tex_rv_stripe():
    """Cream RV flank with the period double stripe."""
    w, h = 512, 256
    img = np.zeros((h, w, 3)) + np.array([214, 206, 186])
    img += noise(h, w, 5)[..., None]
    for y0, y1, c in ((150, 168, [178, 96, 52]), (172, 182, [150, 66, 40]),
                      (186, 192, [96, 104, 120])):
        img[y0:y1] = np.array(c) + noise(y1 - y0, w, 4)[..., None]
    img[:6] *= 0.85
    img[-8:] *= 0.8
    save(img, 'rv_flank.png')


if __name__ == '__main__':
    tex_cinderblock()
    tex_plywood()
    tex_dirt()
    tex_fabric()
    tex_screen()
    tex_pine()
    tex_weeds()
    tex_litter()
    tex_tiretracks()
    tex_curtain_tv()
    tex_neon_open()
    tex_stop()
    tex_speed()
    tex_lot()
    tex_office()
    tex_laundry()
    tex_plate()
    tex_rv_stripe()
    print('v2 textures done')
