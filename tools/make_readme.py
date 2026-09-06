#!/usr/bin/env python3
"""Generate the top-level README.md from the live kit data (v2)."""
import json
import os

ROOT = '/home/user/World_Set'
meta = json.load(open(os.path.join(ROOT, 'WorldKit/viewer/assets.json')))
show = json.load(open(os.path.join(ROOT, 'work/showcase_stats.json')))
assets = meta['assets']
T = meta['totals']
ntex = len([f for f in os.listdir(os.path.join(ROOT, 'WorldKit/tex')) if f.endswith('.png')])
ex = show['extent']
foot = '%d × %d m' % (ex['x'][1] - ex['x'][0], ex['y'][1] - ex['y'][0])

rows = '\n'.join('| `%s` | %s | %d | %d | %d | %s |'
                 % (a['name'], a['catname'].title(), a['tris'], a['parts'], a['lights'],
                    ' × '.join('%.2f' % d for d in a['dim']))
                 for a in assets)
catrow = '\n'.join('| `%s` | %d | %s |' % (c['id'], c['n'],
                                           ', '.join(a['label'] for a in assets
                                                     if a['cat'] == c['id']))
                   for c in meta['cats'])

README = f"""# WORLD KIT — STARLIGHT ESTATES

**Input concept:** *1995 trailer park at night* — one strongly defined visual
environment, developed as a modular, reusable world-building kit rather than a
single fixed scene.

**Starlight Estates, est. 1974.** A mobile-home park after dark: sodium
streetlamps, tungsten windows, a buzzing pylon marquee with one vacancy,
chain-link runs, plastic flamingos, a burn barrel in a side yard, a coin
laundromat with a dying OPEN neon, and wires sagging between creosote poles.
The kit builds this park — and any park like it.

![Showcase hero](WorldKit/renders/showcase_hero.png)

> **v2 — "double the world".** The kit grew from 40 to **{T['assets']} assets**
> ({T['tris']:,} triangles, {T['mats']} materials, {ntex} procedural textures) and the
> showcase from a single street to a **{foot}** park with three named streets,
> **{T['instances']} placed instances** and {T['lights']} window-spill lights. New this
> revision: an **interactive 3D kit viewer** (`WorldKit/viewer/`) and a longer
> **crane-out camera walkthrough**.

---

## 1. Deliverables map

| Deliverable | Path |
|---|---|
| Asset library `.blend` ({T['assets']} assets, collections, packed textures) | `WorldKit/blend/WK_Starlight_Library.blend` |
| Material library `.blend` + swatch sheet | `WorldKit/blend/WK_Starlight_Materials.blend`, `WorldKit/catalog/material_swatches.png` |
| Individual GLBs (one per asset, embedded textures, `KHR_lights_punctual`) | `WorldKit/glb/WK_*.glb` ({T['assets']} files) |
| **Interactive kit viewer** (WebGL, no dependencies) | `WorldKit/viewer/index.html` |
| Thumbnail catalog | `WorldKit/catalog/catalog.html`, `contact_sheet.png`, `thumbs/` |
| Assembled showcase scene | `WorldKit/blend/WK_Starlight_Showcase.blend` (scene `SHOWCASE`) |
| 360° environment render | `WorldKit/renders/pano_360.png` (3072×1536 equirect) |
| Camera walkthrough | `WorldKit/video/walkthrough.mp4` (+ `walkthrough_preview.gif`) |
| Hero stills (1080p) | `WorldKit/renders/showcase_{{hero,street,court,yard,fire,aerial}}.png` |
| Procedural source textures | `WorldKit/tex/*.png` ({ntex} files) |
| Build scripts (reproducible pipeline) | `tools/*.py` |

Open `WorldKit/index.html` (or `WorldKit/viewer/index.html`) over a local
server for the viewer:

```bash
python3 -m http.server 8080 --directory WorldKit   # then open /viewer/
```

---

## 2. Art direction — one coherent kit

**Design language.** Chunky low-poly hard-surface with softened edges
(2-segment bevels on hero pieces), flat colour plus small procedural texture
detail, night-first lighting: every asset is authored to read under moonlight +
sodium + tungsten.

**Shared rules across all {T['assets']} assets**

- **Scale:** metric, 1 unit = 1 m. Single-wides 10–12 m, the double-wide 14 × 7 m,
  doors 0.94 × 2.04 m, fence runs 4 m, road tiles 8 × 6 m, wire spans 12 m.
- **Materials:** one family of {T['mats']} Principled materials shared by every asset
  (see §5). No per-asset snowflake shaders.
- **Surface treatment:** painted-metal siding grooves, galvanized posts,
  weathered plank wood, rust blotches, worn asphalt — from {ntex} small procedural
  textures, packed in the `.blend` and embedded in every GLB.
- **Polygon philosophy:** quads, 12–24-gon round profiles, curves only where the
  silhouette matters (wires, string lights, flamingo necks). Whole kit
  ≈ {T['tris'] / 1000:.0f} k tris; the heaviest single asset is ≈ 2.6 k.
- **Colour logic:** desaturated 90s pastels (mint / sand / dusty blue siding)
  under orange sodium and warm tungsten; night sky in deep blues; rust and
  galvanised grey as neutrals; three accent hots only — sign red, neon pink,
  fire orange.

**Modularity proof.** Openings are standardised: every shell carries dark
recesses sized exactly for `WK_DOOR_*` and `WK_WND_*`, so doors, lit, dark, TV-lit
and boarded windows swap freely. Pads tile edge-to-edge (8 m gravel, 4 m
concrete, 6 m grass, 8 m dirt), fence runs chain at 4 m with a matching corner
post, road tiles snap on an 8 m grid (straight / corner / tee). The showcase
instances **only** kit pieces — plus one neutral ground plane, cameras and
scene lights.

---

## 3. Naming convention

```
WK_<CATEGORY>_<Name>                 asset anchor (Empty) + sub-collection
WK_<CATEGORY>_<Name>_P##             mesh part (data-block shares the name)
WK_<CATEGORY>_<Name>_L##             light (exports as KHR_lights_punctual)
M_<Family><Variant>                  material, e.g. M_Siding_Mint, M_Curtain
SHOW_<Asset>                         showcase collection-instance
CAM_Hero / CAM_Street / CAM_Court / CAM_Yard / CAM_Fire / CAM_Aerial / CAM_Pano / CAM_Walk
```

| Category | Assets | Contents |
|---|---|---|
{catrow}

---

## 4. Origin & placement convention

- **Default:** anchor at the **ground-projected base centre**, `z = 0` at the
  underside/contact plane. Drop into any engine at terrain height.
- **Fronts face +Y** (Blender) → +Z after Y-up glTF export. Rotation cheat
  sheet: face −Y = `PI`, +Y = `0`, +X = `−PI/2`, −X = `+PI/2`.
- **Surfaces:** pad / road / grass / decal tops sit exactly at local `z = 0`
  (bodies extend downward) so pieces stack without z-fighting.
- **Spans:** `WireSpan` endpoints at `(±6, 0, 0)` sag −0.9 m; `StringLights`
  endpoints at `(±3, 0, 0)` sag −0.55 m; `ClothesLine` posts at `(±2, 0, 0)`.
- **Mounts:** `PorchLight`, `ACWindowUnit`, `SwampCooler`, `LotNumber` origins are
  the wall-mount point; `Dish` / `TVAntenna` origins are the roof-mount base.
- The viewer draws the 1 m grid and the origin gizmo with every asset so the
  contact plane and facing axis can be checked at a glance.

---

## 5. Material families

All Principled, all glTF-clean (BaseColor ± texture, Emission, MASK/BLEND alpha
where needed, `doubleSided` only on mesh / grille / decal cards).

| Family | Materials | Notes |
|---|---|---|
| Painted siding | `M_Siding_Mint/Sand/Blue/Cream/Brown`, `M_Skirting` | one groove texture × tints |
| Paint & trim | `M_Trim`, `M_Roof`, `M_White`, `M_Black`, `M_Plywood` | |
| Metals | `M_Galv`, `M_Chrome`, `M_DarkMetal`, `M_Rust`, `M_Propane` | rust is a procedural blotch |
| Woods | `M_Wood`, `M_PoleWood`, `M_Picket` | weathered planks / creosote |
| Ground | `M_Asphalt`, `M_Road`, `M_Gravel`, `M_Concrete`, `M_Ground`, `M_Dirt` | road tiles carry painted lines |
| Glass | `M_Curtain` (emissive warm), `M_CurtainTV` (cold flicker blue), `M_GlassDark` | |
| Signage | `M_SignPylon`, `M_SignVacancy`, `M_SignTrespass`, `M_SignStop`, `M_SignSpeed`, `M_LotNumber`, `M_VendFront`, `M_Neon` | texture doubles as emission |
| Light sources | `M_BulbWarm`, `M_LampAmber`, `M_Flame`, `M_Flood` | |
| Alpha trims | `M_Chainlink`, `M_Blade`, `M_Pine`, `M_Weeds` (MASK), `M_Oil`, `M_Puddle`, `M_Tracks`, `M_Litter` (BLEND) | |
| Soft goods | `M_Couch`, `M_Recliner`, `M_PlasticWhite`, `M_Flamingo`, `M_Tire`, `M_Bush` | |
| Vehicles | `M_CarPaint`, `M_TruckPaint`, `M_RVWhite`, `M_CarLightF/R`, `M_DumpsterGreen` | |

---

## 6. The showcase — "Starlight Estates, Lot 1–15"

Built by `tools/build_showcase.py`, **{T['instances']} collection instances of the
{T['assets']} kit assets**, {T['lights']} window-spill point lights, footprint {foot}.

| Street | Layout |
|---|---|
| **Main Street** (`y = 0`, x −40…+40) | ten lots facing each other across the asphalt, marquee + vacancy sign at the west entrance, burn-barrel yard and RV pad at the east end |
| **Sunset Court** (`x = 0`, north spur) | coin laundromat with OPEN neon, vending + payphone, four lots, mailbox cluster |
| **Sunset Row** (`y = 32`, east spur) | three back lots, pine line, chain-link corner, ditch |

Cameras: `CAM_Hero` (30 mm, west entrance) · `CAM_Street` (50 mm, down the row) ·
`CAM_Court` (35 mm, laundromat) · `CAM_Yard` (35 mm, lot detail) · `CAM_Fire`
(35 mm, burn barrel) · `CAM_Aerial` (28 mm, whole park) · `CAM_Pano`
(equirectangular).

**Walkthrough dolly (v2).** One continuous 14 s move at 12 fps: east along Main
Street past the marquee, a turn north into Sunset Court alongside the
laundromat, then a crane up over Sunset Row. Position, look-target and focal
length are all Catmull-Rom splines (30 → 24 mm) with an ease-in-out time curve
and a light hand-held float that damps out as the crane takes over.

---

## 7. Asset list ({T['assets']})

`tris` = evaluated triangles incl. bevels; `parts` = mesh children; `L` = lights;
`size` = W × D × H in metres.

| Asset | Category | tris | parts | L | size |
|---|---|---|---|---|---|
{rows}

**Total ≈ {T['tris'] / 1000:.1f} k tris.** Browse visually:
[`viewer/index.html`](WorldKit/viewer/index.html) ·
[`catalog.html`](WorldKit/catalog/catalog.html) ·
[`contact_sheet.png`](WorldKit/catalog/contact_sheet.png) ·
[`material_swatches.png`](WorldKit/catalog/material_swatches.png)

---

## 8. Use

**Blender** — `File → Link` (or Append) a `WK_*` sub-collection from
`WK_Starlight_Library.blend`, or open `WK_Starlight_Showcase.blend` and copy the
`SHOW_*` instances. Textures are packed, so the file is self-contained.

**Game engines** — import `WorldKit/glb/WK_*.glb` (Unreal, Unity, Godot,
three.js). Origins are placement-ready, lights arrive as `KHR_lights_punctual`,
and emissive signage needs no lightmap work to read at night. Chain-link, grass
and pine use alpha-clip (`MASK`); ground decals use alpha-blend.

**Viewer** — `WorldKit/viewer/` is a dependency-free WebGL browser for the kit:
search and filter by category, orbit any asset, toggle wireframe and the
grid/origin gizmo, read tri counts, bounds, materials and download the GLB;
plus tabs for the showcase stills, the draggable 360° panorama and the
walkthrough.

---

## 9. Reproduce

```bash
pip install bpy pillow numpy imageio-ffmpeg
python3 tools/make_textures.py     # base procedural textures
python3 tools/make_textures_v2.py  # v2 additions
python3 tools/build_library.py     # materials + {T['assets']} assets -> Library.blend
python3 tools/export_glb.py        # {T['assets']} GLBs
python3 tools/build_showcase.py    # SHOWCASE scene ({T['instances']} instances)
python3 tools/render_thumbs.py     # {T['assets']} thumbnails
python3 tools/make_materials.py    # Materials.blend + swatch sheet
python3 tools/render_stills.py     # six 1080p hero stills
python3 tools/render_pano.py       # 360° equirect
python3 tools/render_walk.py       # walkthrough frames
python3 tools/make_video.py        # mp4 + gif
python3 tools/make_viewer.py && python3 tools/make_catalog.py && python3 tools/make_readme.py
```

Renders use Cycles on CPU with OpenImageDenoise; the full chain runs unattended
in about three hours on 2 cores.

---

*Built as WORLD KIT Nº 1 — "Starlight Estates". The target was never
"AI-generated assets". The target was a coherent, artist-designed world kit.*
"""

open(os.path.join(ROOT, 'README.md'), 'w').write(README)
print('README.md written —', len(README.splitlines()), 'lines')
