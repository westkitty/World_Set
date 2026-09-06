#!/usr/bin/env python3
"""WORLD KIT / STARLIGHT ESTATES — procedural texture bakery.

Generates the small shared texture set used by every kit material.
Deterministic (seeded). Pure PIL + numpy. Textures are packed into the
.blend at build time and embedded in each GLB on export.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.join(os.path.dirname(__file__), '..', 'WorldKit', 'tex')
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(1995)

FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def save(arr, name):
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    Image.fromarray(arr).save(os.path.join(OUT, name))
    print('tex', name)


def noise(h, w, scale=1.0):
    return rng.normal(0, 1, (h, w)) * scale


def soft_blobs(n, h, w, rmin, rmax):
    """Sum of soft radial blobs in [0,1]."""
    yy, xx = np.mgrid[0:h, 0:w]
    acc = np.zeros((h, w))
    for _ in range(n):
        cx, cy = rng.uniform(0, w), rng.uniform(0, h)
        r = rng.uniform(rmin, rmax)
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
        acc += np.clip(1 - d, 0, 1) ** 2
    acc /= max(acc.max(), 1e-6)
    return acc


# ---------------------------------------------------------------- siding
def tex_siding():
    h = w = 256
    row = np.arange(h) % 32
    prof = 235 - 55 * (row / 31.0) ** 1.5
    prof[row == 31] = 120  # groove shadow line
    prof[row == 0] = 250   # top highlight lip
    img = np.repeat(prof[:, None], w, axis=1)
    img = img + noise(h, w, 9) + soft_blobs(7, h, w, 20, 60) * -30
    save(np.dstack([img] * 3), 'siding_groove.png')


# ---------------------------------------------------------------- rust
def tex_rust():
    h = w = 256
    base = np.zeros((h, w, 3)) + np.array([107, 58, 30])
    blotch = soft_blobs(26, h, w, 12, 55)
    dark = np.array([48, 24, 12])
    lite = np.array([176, 100, 44])
    m = blotch[..., None]
    img = base * (1 - m) + dark * m * 0.7 + lite * (m ** 3) * 0.5
    img += noise(h, w, 14)[..., None]
    img += (rng.random((h, w, 3)) - 0.5) * 26
    save(img, 'rust.png')


# ---------------------------------------------------------------- wood planks (vertical)
def tex_wood():
    h = w = 256
    pw = w // 6
    img = np.zeros((h, w, 3))
    for p in range(6):
        tone = rng.uniform(0.75, 1.1)
        base = np.array([122, 104, 84]) * tone
        x0, x1 = p * pw, (p + 1) * pw
        grain = np.cumsum(noise(h, x1 - x0, 2.2), axis=0)
        grain = (grain - grain.min()) / max(grain.ptp(), 1e-6)
        plank = base[None, None, :] + (grain - 0.5)[..., None] * 46
        plank += noise(h, x1 - x0, 8)[..., None]
        img[:, x0:x1] = plank
        img[:, x0:x0 + 2] *= 0.35  # gap shadow
        img[:, x1 - 1:x1] *= 1.12
    for _ in range(7):  # knots
        cx, cy = rng.uniform(0, w), rng.uniform(0, h)
        yy, xx = np.mgrid[0:h, 0:w]
        d = np.sqrt(((xx - cx) / 5) ** 2 + ((yy - cy) / 8) ** 2)
        img[d < 1] *= 0.45
    save(img, 'wood_planks.png')


# ---------------------------------------------------------------- asphalt / road / gravel / concrete / grass
def tex_asphalt():
    h = w = 256
    img = np.zeros((h, w, 3)) + np.array([34, 34, 38])
    img += noise(h, w, 10)[..., None]
    sp = rng.random((h, w))
    img[sp > 0.985] += 26
    img[sp < 0.02] -= 14
    save(img, 'asphalt.png')


def tex_road():
    h = w = 512
    img = np.zeros((h, w, 3)) + np.array([33, 33, 37])
    img += noise(h, w, 9)[..., None]
    sp = rng.random((h, w))
    img[sp > 0.986] += 24
    y = np.arange(h)[:, None]
    # worn double-yellow center (road runs along X)
    for yc, col in ((h // 2 - 7, (150, 118, 30)), (h // 2 + 7, (150, 118, 30))):
        band = np.clip(1 - np.abs(y - yc) / 4.5, 0, 1)
        wear = (soft_blobs(40, h, w, 3, 14) > 0.28).astype(float)
        m = band * wear * 0.85
        img = img * (1 - m[..., None]) + np.array(col) * m[..., None]
    # edge lines
    for yc in (26, h - 26):
        band = np.clip(1 - np.abs(y - yc) / 3.5, 0, 1)
        wear = (soft_blobs(40, h, w, 3, 14) > 0.32).astype(float)
        m = band * wear * 0.6
        img = img * (1 - m[..., None]) + np.array([150, 150, 148]) * m[..., None]
    save(img, 'road_top.png')


def tex_gravel():
    h = w = 256
    img = np.zeros((h, w, 3)) + np.array([96, 87, 76])
    img += noise(h, w, 8)[..., None]
    pil = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    for _ in range(2600):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        r = rng.uniform(0.8, 2.6)
        t = int(rng.uniform(88, 168))
        tone = (t, int(t * rng.uniform(0.9, 0.98)), int(t * rng.uniform(0.8, 0.9)))
        d.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=tone)
    pil.save(os.path.join(OUT, 'gravel.png'))
    print('tex gravel.png')


def tex_concrete():
    h = w = 256
    img = np.zeros((h, w, 3)) + np.array([138, 138, 134])
    img += noise(h, w, 7)[..., None]
    img += (soft_blobs(9, h, w, 20, 70)[..., None] - 0.5) * 36
    pil = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    for _ in range(3):  # cracks
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        for _ in range(40):
            nx, ny = x + rng.uniform(-9, 9), y + rng.uniform(-9, 9)
            d.line([x, y, nx, ny], fill=(70, 70, 68), width=1)
            x, y = nx, ny
    pil.save(os.path.join(OUT, 'concrete.png'))
    print('tex concrete.png')


def tex_grass():
    h = w = 256
    img = np.zeros((h, w, 3)) + np.array([44, 54, 30])
    img += (soft_blobs(14, h, w, 15, 60)[..., None] - 0.5) * np.array([30, 34, 10])
    dirt = soft_blobs(6, h, w, 18, 50)
    img = img * (1 - dirt[..., None] * 0.7) + np.array([74, 62, 40]) * dirt[..., None] * 0.7
    img += noise(h, w, 11)[..., None]
    sp = rng.random((h, w))
    img[sp > 0.975] += np.array([26, 34, 8])
    save(img, 'grass_ground.png')


# ---------------------------------------------------------------- alpha trims
def tex_chainlink():
    s = 128
    pil = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(pil)
    step = 16
    col = (178, 182, 186, 255)
    for i in range(-s, s * 2, step):
        d.line([i, 0, i + s, s], fill=col, width=2)
        d.line([i + s, 0, i, s], fill=col, width=2)
    pil.save(os.path.join(OUT, 'chainlink.png'))
    print('tex chainlink.png')


def tex_blades():
    s = 128
    pil = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(pil)
    for _ in range(30):
        x = rng.uniform(4, s - 4)
        lean = rng.uniform(-14, 14)
        hh = rng.uniform(40, 120)
        g = int(rng.uniform(70, 130))
        d.line([x, s, x + lean, s - hh], fill=(34, g, 26, 255), width=int(rng.uniform(2, 4)))
    pil.save(os.path.join(OUT, 'grass_blade.png'))
    print('tex grass_blade.png')


def tex_curtain():
    h = w = 128
    yy, xx = np.mgrid[0:h, 0:w]
    glow = np.clip(1 - np.abs(xx - w * 0.5) / (w * 0.62), 0, 1)
    glow *= 0.55 + 0.45 * np.clip(1 - yy / h, 0, 1)
    folds = 0.82 + 0.18 * np.sin(xx / w * np.pi * 9 + 1.2)
    warm = np.array([255, 196, 128])
    img = warm * (glow * folds)[..., None]
    img[:14] *= 0.35   # valance shadow
    img[-6:] *= 0.6
    save(img, 'curtain_lit.png')


# ---------------------------------------------------------------- signage
def glow_text(base, xy, s, font, fill, glow, blur=6):
    layer = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.text(xy, s, font=font, fill=glow, anchor='mm')
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(layer)
    d = ImageDraw.Draw(base)
    d.text(xy, s, font=font, fill=fill, anchor='mm')


def tex_pylon():
    w, h = 512, 256
    pil = Image.new('RGBA', (w, h), (8, 26, 30, 255))
    d = ImageDraw.Draw(pil)
    n = np.array(pil).astype(float)
    n[..., :3] += noise(h, w, 6)[..., None]
    pil = Image.fromarray(np.clip(n, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    d.rounded_rectangle([8, 8, w - 8, h - 8], radius=18, outline=(255, 110, 180, 255), width=5)
    f_big = ImageFont.truetype(FONT_B, 74)
    f_mid = ImageFont.truetype(FONT_B, 44)
    f_sm = ImageFont.truetype(FONT, 24)
    glow_text(pil, (w // 2 + 28, 78), 'STARLIGHT', f_big, (255, 240, 220, 255), (255, 90, 160, 255), 10)
    glow_text(pil, (w // 2 + 28, 156), 'ESTATES', f_mid, (190, 245, 255, 255), (60, 200, 230, 255), 8)
    d.text((w // 2 + 28, 208), '· EST. 1974 ·', font=f_sm, fill=(255, 200, 130, 255), anchor='mm')
    # star
    cx, cy, r = 66, 108, 44
    pts = []
    for i in range(10):
        a = -np.pi / 2 + i * np.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * np.cos(a), cy + rr * np.sin(a)))
    d.polygon(pts, fill=(255, 210, 120, 255), outline=(255, 140, 80, 255))
    pil.convert('RGB').save(os.path.join(OUT, 'pylon_face.png'))
    print('tex pylon_face.png')


def tex_vacancy():
    w, h = 256, 96
    pil = Image.new('RGBA', (w, h), (10, 8, 8, 255))
    d = ImageDraw.Draw(pil)
    d.rectangle([4, 4, w - 4, h - 4], outline=(255, 70, 60, 255), width=3)
    glow_text(pil, (w // 2, h // 2), 'VACANCY', ImageFont.truetype(FONT_B, 44),
              (255, 120, 110, 255), (255, 40, 30, 255), 7)
    pil.convert('RGB').save(os.path.join(OUT, 'vacancy.png'))
    print('tex vacancy.png')


def tex_trespass():
    w, h = 256, 160
    pil = Image.new('RGBA', (w, h), (168, 24, 20, 255))
    n = np.array(pil).astype(float)
    n[..., :3] += noise(h, w, 8)[..., None]
    pil = Image.fromarray(np.clip(n, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(pil)
    d.rectangle([5, 5, w - 5, h - 5], outline=(245, 245, 240, 255), width=4)
    glow_text(pil, (w // 2, 52), 'NO', ImageFont.truetype(FONT_B, 40),
              (255, 255, 255, 255), (255, 255, 255, 0), 1)
    glow_text(pil, (w // 2, 100), 'TRESPASSING', ImageFont.truetype(FONT_B, 27),
              (255, 255, 255, 255), (255, 255, 255, 0), 1)
    d.text((w // 2, 134), 'VIOLATORS WILL BE PROSECUTED', font=ImageFont.truetype(FONT, 12),
           fill=(255, 255, 255, 255), anchor='mm')
    pil.convert('RGB').save(os.path.join(OUT, 'trespass.png'))
    print('tex trespass.png')


def tex_vending():
    w, h = 256, 480
    pil = Image.new('RGBA', (w, h), (26, 10, 12, 255))
    d = ImageDraw.Draw(pil)
    # header band
    d.rectangle([0, 0, w, 120], fill=(150, 22, 26, 255))
    d.ellipse([28, 14, w - 28, 106], fill=(200, 30, 34, 255), outline=(255, 235, 235, 255), width=3)
    d.text((w // 2, 60), 'COLA', font=ImageFont.truetype(FONT_B, 52), fill=(255, 245, 245, 255), anchor='mm')
    # glowing product window
    d.rectangle([22, 136, w - 22, 330], fill=(150, 190, 210, 255))
    for r in range(3):
        for c in range(4):
            x0, y0 = 32 + c * 50, 148 + r * 60
            pick = rng.choice([(200, 60, 60), (70, 140, 200), (220, 220, 225), (70, 180, 90)])
            d.rectangle([x0, y0, x0 + 38, y0 + 46], fill=tuple(int(v) for v in pick) + (255,))
    # glass streak
    d.polygon([(150, 136), (190, 136), (150, 330), (110, 330)], fill=(255, 255, 255, 60))
    # lower panel
    d.rectangle([22, 344, w - 22, 458], fill=(18, 18, 20, 255), outline=(90, 90, 95, 255), width=2)
    d.rectangle([40, 364, 140, 400], fill=(30, 30, 34, 255), outline=(140, 140, 145, 255))
    d.text((90, 382), '25¢', font=ImageFont.truetype(FONT_B, 22), fill=(220, 220, 220, 255), anchor='mm')
    d.rectangle([160, 364, 214, 400], fill=(60, 60, 64, 255))
    d.text((127, 432), 'ICE COLD', font=ImageFont.truetype(FONT_B, 20), fill=(170, 210, 225, 255), anchor='mm')
    pil.convert('RGB').save(os.path.join(OUT, 'vending_front.png'))
    print('tex vending_front.png')


# ---------------------------------------------------------------- decals / misc
def tex_blobs(name, rgb, streaks=False):
    h = w = 256
    a = soft_blobs(9, h, w, 22, 70)
    a = np.clip((a - 0.18) * 1.6, 0, 1)
    pil_a = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
    a = np.array(pil_a).astype(float) / 255
    img = np.zeros((h, w, 4))
    img[..., :3] = np.array(rgb)
    if streaks:  # pale reflection streaks baked into a puddle
        yy, xx = np.mgrid[0:h, 0:w]
        for _ in range(7):
            yc = rng.uniform(0, h)
            band = np.clip(1 - np.abs(yy - yc) / rng.uniform(3, 9), 0, 1)
            band *= np.clip(1 - np.abs(xx - w / 2) / rng.uniform(40, 110), 0, 1)
            img[..., :3] += band[..., None] * np.array([52, 74, 96]) * rng.uniform(0.4, 1.0)
    img[..., 3] = a * 235
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).save(os.path.join(OUT, name))
    print('tex', name)


def tex_galv():
    h = w = 128
    img = np.zeros((h, w, 3)) + np.array([172, 178, 182])
    img += np.cumsum(noise(h, w, 1.6), axis=0)[..., None] * 2.0
    img += noise(h, w, 6)[..., None]
    save(img, 'galv.png')


def tex_couch():
    h = w = 128
    img = np.zeros((h, w, 3)) + np.array([92, 88, 58])
    yy, xx = np.mgrid[0:h, 0:w]
    img[((xx // 16) % 2 == 0)] *= np.array([0.82, 0.8, 0.85])
    img[((yy // 16) % 2 == 0)] *= np.array([0.9, 0.82, 0.8])
    img[((xx // 32) % 4 == 0)] += np.array([26, 10, 4])
    img[((yy // 32) % 4 == 0)] += np.array([26, 10, 4])
    img += noise(h, w, 7)[..., None]
    save(img, 'couch_fabric.png')


if __name__ == '__main__':
    tex_siding()
    tex_rust()
    tex_wood()
    tex_asphalt()
    tex_road()
    tex_gravel()
    tex_concrete()
    tex_grass()
    tex_chainlink()
    tex_blades()
    tex_curtain()
    tex_pylon()
    tex_vacancy()
    tex_trespass()
    tex_vending()
    tex_blobs('oil_blob.png', (8, 8, 10))
    tex_blobs('puddle.png', (26, 38, 56), streaks=True)
    tex_galv()
    tex_couch()
    print('textures ->', OUT)
