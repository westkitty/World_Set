#!/usr/bin/env python3
"""Thumbnail contact sheet + HTML catalog for the kit."""
import os
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = '/home/user/World_Set/WorldKit'
TH = os.path.join(ROOT, 'catalog', 'thumbs')
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

stats = json.load(open('/home/user/World_Set/work/asset_stats.json'))
CATS = ['WK_ARCH', 'WK_STR', 'WK_DOOR', 'WK_WND', 'WK_WALL', 'WK_FLR', 'WK_TER',
        'WK_FUR', 'WK_PRP', 'WK_LGT', 'WK_SGN', 'WK_VEG', 'WK_DCL', 'WK_HERO']
CATNAMES = {'WK_ARCH': 'ARCHITECTURE', 'WK_STR': 'STRUCTURAL', 'WK_DOOR': 'DOORS',
            'WK_WND': 'WINDOWS', 'WK_WALL': 'WALLS', 'WK_FLR': 'FLOORS',
            'WK_TER': 'TERRAIN', 'WK_FUR': 'FURNITURE', 'WK_PRP': 'PROPS',
            'WK_LGT': 'LIGHTS', 'WK_SGN': 'SIGNAGE', 'WK_VEG': 'VEGETATION',
            'WK_DCL': 'DECALS', 'WK_HERO': 'HERO OBJECTS'}
for s in stats:
    s['cat'] = '_'.join(s['name'].split('_')[:2])
stats.sort(key=lambda s: (CATS.index(s['cat']), s['name']))

# ---- contact sheet
TW, PAD, LAB = 300, 14, 54
cols = 6
rows = (len(stats) + cols - 1) // cols
sheet = Image.new('RGB', (cols * (TW + PAD) + PAD, rows * (TW + LAB + PAD) + PAD + 70),
                  (10, 13, 20))
d = ImageDraw.Draw(sheet)
d.text((PAD + 4, 14), 'WORLD KIT — STARLIGHT ESTATES · 1995 TRAILER PARK AT NIGHT · '
       f'{len(stats)} ASSETS · {sum(s["tris"] for s in stats):,} TRIS',
       font=ImageFont.truetype(FB, 22), fill=(235, 220, 190))
for i, s in enumerate(stats):
    x = PAD + (i % cols) * (TW + PAD)
    y = 70 + PAD + (i // cols) * (TW + LAB + PAD)
    im = Image.open(os.path.join(TH, s['name'] + '.png')).resize((TW, TW), Image.LANCZOS)
    sheet.paste(im, (x, y))
    d.text((x + 4, y + TW + 4), s['name'], font=ImageFont.truetype(FB, 13), fill=(255, 235, 200))
    d.text((x + 4, y + TW + 24), f"{CATNAMES[s['cat']]} · {s['tris']} tris · {s['parts']} parts",
           font=ImageFont.truetype(FR, 12), fill=(150, 165, 190))
sheet.save(os.path.join(ROOT, 'catalog', 'contact_sheet.png'))
print('contact sheet done')

# ---- HTML catalog
cards = []
for s in stats:
    cards.append(f"""<div class="card"><img src="thumbs/{s['name']}.png" loading="lazy">
<div class="n">{s['name']}</div>
<div class="m">{CATNAMES[s['cat']]} · {s['tris']} tris · {s['parts']} parts · GLB ✓</div></div>""")
html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>WORLD KIT — Starlight Estates · Asset Catalog</title>
<style>
body{{background:#0a0d14;color:#e8e2d4;font-family:system-ui,sans-serif;margin:0;padding:32px}}
h1{{font-size:26px;margin:0}}p.sub{{color:#9aa7bd}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;margin-top:20px}}
.card{{background:#121722;border:1px solid #232c40;border-radius:10px;overflow:hidden}}
.card img{{width:100%;display:block;aspect-ratio:1;object-fit:cover;background:#05070c}}
.n{{padding:10px 12px 2px;font-weight:600;font-size:13px;color:#ffebc8}}
.m{{padding:0 12px 12px;font-size:12px;color:#9aa7bd}}
img.hero{{width:100%;border-radius:10px;border:1px solid #232c40;margin-top:16px}}
a.vw{{display:inline-block;margin-top:14px;padding:9px 16px;border-radius:8px;background:#ffb43f;
color:#20160a;font-weight:700;text-decoration:none;font-size:13px}}
</style></head><body>
<h1>WORLD KIT — STARLIGHT ESTATES</h1>
<p class="sub">1995 trailer park at night · {len(stats)} modular assets · 1 m = 1 unit · origins at ground-projected base center · fronts face +Y</p>
<p><a class="vw" href="../viewer/index.html">▶ open the interactive kit viewer (3D)</a></p>
<img class="hero" src="../renders/showcase_hero.png">
<div class="grid">{''.join(cards)}</div>
<p class="sub">Materials: see material_swatches.png · Library: blend/WK_Starlight_Library.blend ·
Showcase: blend/WK_Starlight_Showcase.blend · Panorama: renders/pano_360.png · Walkthrough: video/walkthrough.mp4</p>
</body></html>"""
open(os.path.join(ROOT, 'catalog', 'catalog.html'), 'w').write(html)
print('html done')
