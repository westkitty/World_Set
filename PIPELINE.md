# WORLD KIT — Pipeline

Everything in `dist/WORLD_KIT/` is generated from source by
`world_kit/pipeline.py`, driven by `tools/wk.py`. No step requires opening
Blender by hand. The pipeline is deterministic: given the same source it
rebuilds the same kit, the same showcase, and the same deliverables.

## Environment

Blender's `bpy` module (4.5 LTS) is used headless. `tools/bootstrap_env.sh`
creates `~/.venv` (bpy + pillow) and builds `~/.wk_xstubs`, a set of stub
shared objects that satisfy the X11/GL symbols `bpy` links against so it can
run with no display server. Cycles runs on **CPU**.

```bash
export LD_LIBRARY_PATH="$HOME/.wk_xstubs"
"$HOME/.venv/bin/python" tools/wk.py --stage <stage>
```

## Stages

| Stage | Entry | Produces |
|-------|-------|----------|
| `textures` | `texgen.build_all` | `textures/*.png` — procedural PBR maps for the 14 material families (albedo / normal / rough, plus edge-wear and decal overlays) |
| `assets` | `library.build_library` → `validate` → `export` → `manifest` | builds all 40 assets into the `WORLD_KIT` collections, audits them, exports per-category GLBs, writes the manifest + WORLD_DNA.md + VALIDATION_REPORT.md |
| `reuse` | `reuse_test` | 3 layouts (compact / open / corridor) + grid/overlap checks + preview renders in `reuse/` |
| `showcase` | `showcase.build` + `lighting.setup` + `cameras` | assembles the hall, then saves `WORLD_KIT_master.blend` |
| `stills` | `render.render_stills` | 6 cinematic camera renders in `renders/` |
| `pano` | `render.render_pano` | `renders/environment_360.png` |
| `walk` | `render.render_walkthrough` | `renders/walkthrough.mp4` (FFmpeg H.264) |
| `catalog` | `catalog` | per-asset thumbnails + category contact sheets in `catalog/` |

`--stage all` runs `textures → assets → reuse → showcase → catalog`. The heavy
render stages (`stills`, `pano`, `walk`) are excluded from `all` so they can be
backgrounded separately; `tools/render_all.py` runs
`showcase → stills → pano → walk → catalog` in sequence for exactly that.

## Render presets (`dna.RENDER`)

Tuned for a 2-core CPU sandbox; raise them freely on a bigger machine.

| Pass | Resolution | Samples | Notes |
|------|-----------|---------|-------|
| stills | 1024×576 | 32 | OIDN denoise |
| panorama | 1536×768 | 32 | equirectangular |
| walkthrough | 640×360 | 12 | 24 fps, 5 s (120 frames), persistent data |
| thumbnails | 512×512 (studio) | 24 | consistent sun + fill + framing |
| reuse previews | 640×360 | 48 | one per layout |

## Guarantees the pipeline enforces

- **Single source of truth.** Every asset reads dimensions, palette, material
  families and invariants from `dna.py`; nothing is hard-coded per asset.
- **Shared materials.** `materials.build_all` builds the 14 families once and
  every asset references them — no per-object duplicates.
- **Validation before export.** `validate.run` checks naming, transforms,
  origins, pivots, mesh sanity and connection tolerances; `manifest.write_validation`
  records the result in `VALIDATION_REPORT.md`.
- **Showcase uses only kit assets.** `showcase.build` places instances of
  registered assets; it never authors bespoke geometry. If a piece were
  missing it would be added to the registry first.
