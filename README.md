# WORLD KIT — Brine & Salt: A Modular Desalination Plant Environment

**WORLD KIT** is a complete, reusable 3D environment-generation system for
Blender. It is not a fixed scene chopped into pieces, and not a bag of
unrelated props that happen to share a colour palette. It is an
**environment construction language**: a documented design DNA, a modular
grammar, a library of catalogued assets, and an assembled showcase — all of
which can be regenerated from source in one command.

The concept is **"Brine & Salt"**: a decommissioned sea-side desalination /
brine-treatment hall. Weathered cast concrete, oxide-red and teal industrial
enamel, brass fittings, timber duckboards, standing brine under floor
gratings, and a sodium-lit beacon that anchors the space.

---

## The four phases

| Phase | What it is | Where it lives |
|-------|-----------|----------------|
| **P1 — WORLD DNA** | The single visual concept written down as law: architectural language, shape hierarchy, modular dimensions, material families, lighting philosophy, poly/UV/texel rules, storytelling rules, and a set of visual invariants every asset obeys. Source of truth — no drift. | `world_kit/dna.py` → `dist/WORLD_KIT/docs/WORLD_DNA.md` |
| **P2 — MODULAR GRAMMAR** | Dimensions + connection logic for bays, walls, floors, openings, columns, beams, stairs, platforms, railings, catwalks, terrain transitions, prop-attachment zones, signage mounts. Snaps on a 4 m grid; supports straights, corners, intersections, enclosed/open space, vertical variation, repeats and asymmetry. | `world_kit/dna.py` (`GRID`, `GRAMMAR`), `world_kit/assets/*` |
| **P3 — ASSET VOCABULARY** | 40 production-ready reusable assets across architecture, walls, floors, structural, furniture, props, lights, signage, vegetation, decals, terrain and hero objects. Effort hierarchy **FOUNDATION > VARIATION > DETAIL > HERO**. | `world_kit/assets/*.py` → `world_kit/library.py` |
| **Reuse test** | Three meaningfully different layouts (compact / open / corridor) built from the *same* pieces to prove the kit is truly reusable — not one hero layout in disguise. | `world_kit/reuse_test.py` → `dist/WORLD_KIT/reuse/` |
| **P4 — SHOWCASE** | One assembled hall built **only** from WORLD KIT assets (no hidden bespoke geometry), composed deliberately with foreground/mid/background hierarchy, focal points, controlled clutter and negative space; lit practically (not generic three-point); six deliberate cameras + a 360° panorama + a short walkthrough that travels *through* the space. | `world_kit/showcase.py`, `lighting.py`, `cameras.py`, `render.py` |

---

## Deliverables

Everything lands in `dist/WORLD_KIT/` (regenerable, git-ignored):

| # | Deliverable | Path |
|---|-------------|------|
| 1 | Master `.blend` | `WORLD_KIT_master.blend` |
| 2 | Individual GLBs by category | `export/{architecture,walls,floors,structural,furniture,props,lights,signage,vegetation,decals,terrain,hero}/*.glb` |
| 3 | Reusable material library | `textures/` (generated PBR maps, 14 families) |
| 4 | Thumbnail asset catalog | `catalog/` (per-asset thumbs + 13 category contact sheets) |
| 5 | Assembled showcase | `15_SHOWCASE` collection in the master blend |
| 6 | High-quality renders (6 cameras) | `renders/*.png` |
| 7 | 360-degree render | `environment_360.png` |
| 8 | Short cinematic walkthrough | `walkthrough.mp4` |
| 9 | Asset manifest | `docs/asset_manifest.{json,csv}` + `docs/ASSET_MANIFEST.md` |
| 10 | WORLD DNA reference doc | `docs/WORLD_DNA.md` |
| — | Validation report | `docs/VALIDATION_REPORT.md` |

---

## Run it

The whole kit regenerates from source with the pipeline driver. No manual
Blender work is required.

```bash
# 1. one-time environment bootstrap (installs bpy 4.5 + pillow into a venv,
#    builds the X11 stubs so headless Cycles runs without a display server)
tools/bootstrap_env.sh

# 2. generate everything (textures -> assets -> reuse -> showcase -> renders)
export LD_LIBRARY_PATH="$HOME/.wk_xstubs"
"$HOME/.venv/bin/python" tools/wk.py --stage all
```

Individual stages (run any subset; heavy ones can run in the background):

```bash
python tools/wk.py --stage textures   # PBR map atlas
python tools/wk.py --stage assets     # build + audit + export all 40 assets + docs
python tools/wk.py --stage reuse      # 3 reuse layouts + preview renders
python tools/wk.py --stage showcase   # assemble the hall, save master .blend
python tools/wk.py --stage stills     # 6 cinematic camera renders
python tools/wk.py --stage pano       # 360-degree panorama
python tools/wk.py --stage walk       # short walkthrough video
python tools/wk.py --stage catalog    # thumbnails + contact sheets
```

See `PIPELINE.md` for the stage-by-stage detail and the render presets.

---

## Layout

```
world_kit/
  dna.py          P1/P2 source of truth: DNA, grid, grammar, palette, materials spec
  geo.py          primitive helpers (box/cyl/extrude/boolean/bevel) used by all assets
  texgen.py       procedural PBR texture generator (albedo/normal/rough, edge wear)
  materials.py    the 14 shared material families (reused, never per-object dupes)
  registry.py     asset registry + family accounting + self-check
  assets/*.py     the asset vocabulary (one module per category)
  library.py      assembles the full 40-asset kit into the WK collections
  showcase.py     the composed hall (placements only — no bespoke geometry)
  lighting.py     practical + atmospheric lighting rig
  cameras.py      the 6 showcase cameras + walk-through path
  render.py       stills / panorama / walkthrough render drivers
  reuse_test.py   the 3-layout reuse proof
  catalog.py      studio thumbnails + contact sheets
  manifest.py     asset manifest + WORLD_DNA.md + VALIDATION_REPORT.md
  validate.py     mesh / naming / connection / transform audit
  export.py       per-category GLB export
  pipeline.py     stage orchestration
tools/
  wk.py           CLI entry point
  bootstrap_env.sh
  render_all.py   background driver for the heavy render stages
dist/WORLD_KIT/   all deliverables (regenerable, not committed)
```

## Naming & conventions

- Objects: `WK_[CATEGORY]_[ASSET]_[VARIANT]_[NUMBER]` — e.g.
  `WK_WALL_CORNER_INNER_A_01`. Never `Cube.004`.
- Origins sit at the design floor (z = 0), centred on the asset's X/Y
  footprint; mechanical pieces (doors, valves) pivot on their real hinge/axis.
- All transforms applied, consistent forward direction (+Y into the bay),
  engine-friendly scale (metres), grid-snapped connections.

## Honesty about this build

- Renders are Cycles CPU on a 2-core / 3 GB sandbox, so the shipped presets are
  deliberately modest (stills 1024×576 @ 32 spp, panorama 1536×768 @ 32,
  walkthrough 640×360 @ 12 spp) with OIDN denoising. Raise `dna.RENDER` on a
  bigger machine for hero-quality frames — no other change is needed.
- The showcase uses only catalogued kit assets. If a piece was missing it was
  authored as a proper asset first, then placed.
