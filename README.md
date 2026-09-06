# WORLD KIT — STARLIGHT ESTATES

**Input concept:** *1995 trailer park at night* — one strongly defined visual
environment, developed as a modular, reusable world-building kit rather than a
single fixed scene.

**Starlight Estates, est. 1974.** A mobile-home park after dark: sodium
streetlamps, tungsten windows, a buzzing pylon marquee with one vacancy,
chain-link runs, plastic flamingos, a burn barrel in a side yard, a coin
laundromat with a dying OPEN neon, and wires sagging between creosote poles.
The kit builds this park — and any park like it.

![Showcase hero](WorldKit/renders/showcase_hero.png)

> **v2 — "double the world".** The kit grew from 40 to **81 assets**
> (35,212 triangles, 74 materials, 37 procedural textures) and the
> showcase from a single street to a **86 × 63 m** park with three named streets,
> **866 placed instances** and 58 window-spill lights. New this
> revision: an **interactive 3D kit viewer** (`WorldKit/viewer/`) and a longer
> **crane-out camera walkthrough**.

---

## 1. Deliverables map

| Deliverable | Path |
|---|---|
| Asset library `.blend` (81 assets, collections, packed textures) | `WorldKit/blend/WK_Starlight_Library.blend` |
| Material library `.blend` + swatch sheet | `WorldKit/blend/WK_Starlight_Materials.blend`, `WorldKit/catalog/material_swatches.png` |
| Individual GLBs (one per asset, embedded textures, `KHR_lights_punctual`) | `WorldKit/glb/WK_*.glb` (81 files) |
| **Interactive kit viewer** (WebGL, no dependencies) | `WorldKit/viewer/index.html` |
| Thumbnail catalog | `WorldKit/catalog/catalog.html`, `contact_sheet.png`, `thumbs/` |
| Assembled showcase scene | `WorldKit/blend/WK_Starlight_Showcase.blend` (scene `SHOWCASE`) |
| 360° environment render | `WorldKit/renders/pano_360.png` (3072×1536 equirect) |
| Camera walkthrough | `WorldKit/video/walkthrough.mp4` (+ `walkthrough_preview.gif`) |
| Hero stills (1080p) | `WorldKit/renders/showcase_{hero,street,court,yard,fire,aerial}.png` |
| Procedural source textures | `WorldKit/tex/*.png` (37 files) |
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

**Shared rules across all 81 assets**

- **Scale:** metric, 1 unit = 1 m. Single-wides 10–12 m, the double-wide 14 × 7 m,
  doors 0.94 × 2.04 m, fence runs 4 m, road tiles 8 × 6 m, wire spans 12 m.
- **Materials:** one family of 74 Principled materials shared by every asset
  (see §5). No per-asset snowflake shaders.
- **Surface treatment:** painted-metal siding grooves, galvanized posts,
  weathered plank wood, rust blotches, worn asphalt — from 37 small procedural
  textures, packed in the `.blend` and embedded in every GLB.
- **Polygon philosophy:** quads, 12–24-gon round profiles, curves only where the
  silhouette matters (wires, string lights, flamingo necks). Whole kit
  ≈ 35 k tris; the heaviest single asset is ≈ 2.6 k.
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
| `WK_ARCH` | 8 | Carport, LaundryBlock, Porch, Shed, Trailer_A, Trailer_B, Trailer_C_Double, Trailer_D_Camper |
| `WK_STR` | 8 | ACWindowUnit, CinderPier, Dish, HitchTongue, PorchSteps, PropaneTank, SwampCooler, TVAntenna |
| `WK_DOOR` | 3 | ScreenDoor, ShedDouble, TrailerDoor |
| `WK_WND` | 4 | WindowBoarded, WindowDark, WindowLit, WindowTVLit |
| `WK_WALL` | 5 | Chainlink4m, ChainlinkCorner, ChainlinkGate, CinderWall2m, PicketFence4m |
| `WK_FLR` | 3 | ConcretePad, DirtPad, GravelPad |
| `WK_TER` | 5 | Ditch, GrassPatch, RoadCorner, RoadStraight, RoadTee |
| `WK_FUR` | 6 | KettleGrill, LawnChair, PicnicTable, PlasticTable, PorchCouch, Recliner |
| `WK_PRP` | 16 | ClothesLine, Dumpster, Flamingo, KidBike, LeaningLadder, MailboxCluster, MilkCrates, OldTV, PayPhone, ShoppingCart, TelephonePole, TireStack, TrashCan, VendingMachine, WashingMachine, WireSpan |
| `WK_LGT` | 6 | FireBarrel, FloodLight, NeonOpen, PorchLight, StreetLamp, StringLights |
| `WK_SGN` | 5 | LotNumber, PylonSign, SpeedLimit5, StopSign, Trespass |
| `WK_VEG` | 5 | DeadTree, GrassTuft, PineTree, ScrubBush, WeedClump |
| `WK_DCL` | 4 | LitterScatter, OilStain, Puddle, TireTracks |
| `WK_HERO` | 3 | MotorhomeRV, Pickup79, Sedan86 |

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

Built by `tools/build_showcase.py`, **866 collection instances of the
81 kit assets**, 58 window-spill point lights, footprint 86 × 63 m.

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

## 7. Asset list (81)

`tris` = evaluated triangles incl. bevels; `parts` = mesh children; `L` = lights;
`size` = W × D × H in metres.

| Asset | Category | tris | parts | L | size |
|---|---|---|---|---|---|
| `WK_ARCH_Carport` | Architecture | 256 | 8 | 0 | 5.60 × 3.50 × 2.50 |
| `WK_ARCH_LaundryBlock` | Architecture | 380 | 25 | 2 | 6.70 × 5.94 × 3.20 |
| `WK_ARCH_Porch` | Architecture | 264 | 22 | 0 | 3.70 × 2.72 × 2.88 |
| `WK_ARCH_Shed` | Architecture | 144 | 12 | 0 | 2.70 × 2.10 × 2.51 |
| `WK_ARCH_Trailer_A` | Architecture | 292 | 21 | 0 | 12.34 × 3.94 × 3.42 |
| `WK_ARCH_Trailer_B` | Architecture | 328 | 24 | 0 | 10.34 × 3.54 × 3.42 |
| `WK_ARCH_Trailer_C_Double` | Architecture | 428 | 29 | 0 | 14.44 × 7.44 × 3.62 |
| `WK_ARCH_Trailer_D_Camper` | Architecture | 924 | 22 | 0 | 8.21 × 4.48 × 2.75 |
| `WK_STR_ACWindowUnit` | Structural | 332 | 17 | 0 | 0.66 × 0.56 × 0.69 |
| `WK_STR_CinderPier` | Structural | 36 | 3 | 0 | 0.44 × 0.44 × 0.48 |
| `WK_STR_Dish` | Structural | 204 | 5 | 0 | 0.96 × 0.89 × 1.72 |
| `WK_STR_HitchTongue` | Structural | 488 | 16 | 0 | 1.35 × 2.83 × 1.40 |
| `WK_STR_PorchSteps` | Structural | 132 | 11 | 0 | 1.06 × 1.08 × 1.48 |
| `WK_STR_PropaneTank` | Structural | 664 | 9 | 0 | 0.55 × 0.58 × 1.35 |
| `WK_STR_SwampCooler` | Structural | 560 | 34 | 0 | 1.15 × 1.15 × 1.01 |
| `WK_STR_TVAntenna` | Structural | 428 | 9 | 0 | 1.10 × 0.90 × 1.70 |
| `WK_DOOR_ScreenDoor` | Doors | 126 | 10 | 0 | 1.00 × 0.14 × 2.06 |
| `WK_DOOR_ShedDouble` | Doors | 228 | 17 | 0 | 1.70 × 0.19 × 2.06 |
| `WK_DOOR_TrailerDoor` | Doors | 238 | 10 | 0 | 1.02 × 0.14 × 2.12 |
| `WK_WND_WindowBoarded` | Windows | 188 | 13 | 0 | 1.50 × 0.16 × 1.08 |
| `WK_WND_WindowDark` | Windows | 86 | 8 | 0 | 1.50 × 0.16 × 1.08 |
| `WK_WND_WindowLit` | Windows | 86 | 8 | 0 | 1.50 × 0.16 × 1.08 |
| `WK_WND_WindowTVLit` | Windows | 110 | 10 | 1 | 1.50 × 0.16 × 1.08 |
| `WK_WALL_Chainlink4m` | Walls | 318 | 6 | 0 | 4.12 × 0.12 × 1.68 |
| `WK_WALL_ChainlinkCorner` | Walls | 372 | 9 | 0 | 2.11 × 2.11 × 1.74 |
| `WK_WALL_ChainlinkGate` | Walls | 166 | 8 | 0 | 1.40 × 0.15 × 1.60 |
| `WK_WALL_CinderWall2m` | Walls | 48 | 4 | 0 | 2.10 × 0.34 × 0.97 |
| `WK_WALL_PicketFence4m` | Walls | 516 | 43 | 0 | 4.09 × 0.14 × 1.15 |
| `WK_FLR_ConcretePad` | Floors | 12 | 1 | 0 | 4.00 × 4.00 × 0.12 |
| `WK_FLR_DirtPad` | Floors | 12 | 1 | 0 | 8.00 × 8.00 × 0.10 |
| `WK_FLR_GravelPad` | Floors | 12 | 1 | 0 | 8.00 × 8.00 × 0.10 |
| `WK_TER_Ditch` | Terrain | 72 | 15 | 0 | 8.00 × 3.47 × 0.69 |
| `WK_TER_GrassPatch` | Terrain | 12 | 1 | 0 | 6.00 × 6.00 × 0.08 |
| `WK_TER_RoadCorner` | Terrain | 230 | 20 | 0 | 8.11 × 8.11 × 0.14 |
| `WK_TER_RoadStraight` | Terrain | 14 | 2 | 0 | 8.00 × 6.00 × 0.10 |
| `WK_TER_RoadTee` | Terrain | 148 | 14 | 0 | 12.70 × 9.90 × 0.12 |
| `WK_FUR_KettleGrill` | Furniture | 1080 | 11 | 0 | 0.85 × 0.74 × 0.90 |
| `WK_FUR_LawnChair` | Furniture | 316 | 13 | 0 | 0.53 × 0.51 × 1.00 |
| `WK_FUR_PicnicTable` | Furniture | 96 | 8 | 0 | 1.80 × 1.48 × 0.96 |
| `WK_FUR_PlasticTable` | Furniture | 476 | 8 | 0 | 1.02 × 1.02 × 0.76 |
| `WK_FUR_PorchCouch` | Furniture | 688 | 12 | 0 | 2.18 × 0.84 × 1.04 |
| `WK_FUR_Recliner` | Furniture | 612 | 11 | 0 | 1.04 × 1.02 × 1.13 |
| `WK_PRP_ClothesLine` | Props | 1890 | 27 | 0 | 5.10 × 1.30 × 2.02 |
| `WK_PRP_Dumpster` | Props | 388 | 11 | 0 | 2.00 × 1.10 × 1.36 |
| `WK_PRP_Flamingo` | Props | 2576 | 14 | 0 | 0.87 × 0.69 × 1.14 |
| `WK_PRP_KidBike` | Props | 1672 | 26 | 0 | 0.62 × 1.36 × 0.62 |
| `WK_PRP_LeaningLadder` | Props | 212 | 17 | 0 | 0.61 × 1.13 × 3.27 |
| `WK_PRP_MailboxCluster` | Props | 852 | 23 | 0 | 1.80 × 0.44 × 1.46 |
| `WK_PRP_MilkCrates` | Props | 228 | 19 | 0 | 0.60 × 0.60 × 1.09 |
| `WK_PRP_OldTV` | Props | 294 | 12 | 0 | 0.62 × 0.60 × 0.93 |
| `WK_PRP_PayPhone` | Props | 426 | 21 | 1 | 0.49 × 0.35 × 2.05 |
| `WK_PRP_ShoppingCart` | Props | 776 | 36 | 0 | 0.56 × 0.71 × 0.93 |
| `WK_PRP_TelephonePole` | Props | 420 | 13 | 0 | 3.30 × 0.60 × 7.52 |
| `WK_PRP_TireStack` | Props | 1728 | 3 | 0 | 0.85 × 0.85 × 0.73 |
| `WK_PRP_TrashCan` | Props | 252 | 7 | 0 | 0.64 × 0.64 × 0.84 |
| `WK_PRP_VendingMachine` | Props | 74 | 7 | 1 | 1.03 × 0.87 × 1.90 |
| `WK_PRP_WashingMachine` | Props | 300 | 7 | 0 | 0.72 × 0.68 × 1.09 |
| `WK_PRP_WireSpan` | Props | 1560 | 2 | 0 | 12.01 × 0.54 × 0.94 |
| `WK_LGT_FireBarrel` | Lights | 912 | 20 | 2 | 0.74 × 0.72 × 1.43 |
| `WK_LGT_FloodLight` | Lights | 340 | 8 | 2 | 0.85 × 0.72 × 4.48 |
| `WK_LGT_NeonOpen` | Lights | 58 | 5 | 1 | 1.00 × 0.19 × 0.77 |
| `WK_LGT_PorchLight` | Lights | 36 | 3 | 1 | 0.14 × 0.13 × 0.26 |
| `WK_LGT_StreetLamp` | Lights | 154 | 5 | 2 | 0.67 × 2.00 × 7.00 |
| `WK_LGT_StringLights` | Lights | 2364 | 25 | 1 | 6.01 × 0.07 × 0.69 |
| `WK_SGN_LotNumber` | Signage | 40 | 5 | 0 | 0.70 × 0.24 × 1.30 |
| `WK_SGN_PylonSign` | Signage | 160 | 10 | 0 | 3.60 × 0.50 × 5.10 |
| `WK_SGN_SpeedLimit5` | Signage | 80 | 5 | 0 | 0.48 × 0.08 × 2.10 |
| `WK_SGN_StopSign` | Signage | 80 | 5 | 0 | 0.76 × 0.07 × 2.33 |
| `WK_SGN_Trespass` | Signage | 14 | 2 | 0 | 0.62 × 0.09 × 1.60 |
| `WK_VEG_DeadTree` | Vegetation | 188 | 9 | 0 | 3.63 × 3.25 × 5.45 |
| `WK_VEG_GrassTuft` | Vegetation | 6 | 3 | 0 | 0.55 × 0.48 × 0.42 |
| `WK_VEG_PineTree` | Vegetation | 112 | 26 | 0 | 4.52 × 4.31 × 5.70 |
| `WK_VEG_ScrubBush` | Vegetation | 396 | 6 | 0 | 1.58 × 1.10 × 0.83 |
| `WK_VEG_WeedClump` | Vegetation | 10 | 5 | 0 | 0.96 × 0.74 × 0.55 |
| `WK_DCL_LitterScatter` | Decals | 2 | 1 | 0 | 3.00 × 3.00 × 0.00 |
| `WK_DCL_OilStain` | Decals | 2 | 1 | 0 | 1.60 × 1.20 × 0.00 |
| `WK_DCL_Puddle` | Decals | 2 | 1 | 0 | 2.30 × 1.70 × 0.00 |
| `WK_DCL_TireTracks` | Decals | 2 | 1 | 0 | 4.00 × 2.40 × 0.00 |
| `WK_HERO_MotorhomeRV` | Hero Objects | 1488 | 43 | 1 | 8.97 × 3.15 × 3.57 |
| `WK_HERO_Pickup79` | Hero Objects | 1500 | 37 | 0 | 5.54 × 2.16 × 2.65 |
| `WK_HERO_Sedan86` | Hero Objects | 1496 | 26 | 0 | 4.52 × 2.02 × 1.48 |

**Total ≈ 35.2 k tris.** Browse visually:
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
python3 tools/build_library.py     # materials + 81 assets -> Library.blend
python3 tools/export_glb.py        # 81 GLBs
python3 tools/build_showcase.py    # SHOWCASE scene (866 instances)
python3 tools/render_thumbs.py     # 81 thumbnails
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
