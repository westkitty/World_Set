"""Pipeline orchestration.  See ``tools/wk.py`` for the CLI.

Stages are individually re-runnable so the heavy renders can be backgrounded.
Everything is written under ``<repo>/dist/WORLD_KIT/``.
"""

from __future__ import annotations

import os

import bpy

from . import (cameras, catalog, dna, export, library, lighting, manifest,
               render, reuse_test, showcase, texgen, validate)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(REPO, "dist", "WORLD_KIT")

LIB_COLL = ["01_ARCHITECTURE", "02_WALLS", "03_FLOORS", "04_DOORS_WINDOWS",
            "05_STRUCTURAL", "06_FURNITURE", "07_PROPS", "08_LIGHTS",
            "09_SIGNAGE", "10_VEGETATION", "11_DECALS", "12_TERRAIN", "13_HERO"]


def _dir(*parts):
    path = os.path.join(DIST, *parts)
    os.makedirs(path, exist_ok=True)
    return path


def tex_dir():
    return _dir("textures")


def build():
    report = []
    td = tex_dir()
    if not os.path.exists(os.path.join(td, "MK_concrete_albedo.png")):
        texgen.build_all(td)
        report.append("generated texture set")
    built = library.build_library(td, report)
    return built, report


def _hide_library(hide=True):
    for c in LIB_COLL:
        cc = bpy.data.collections.get(c)
        if cc:
            cc.hide_render = hide
            cc.hide_viewport = hide


def stage_assets():
    built, report = build()
    problems = validate.run(built, {}, report)
    export.export_all(built, _dir("export"), report)
    manifest.write_manifest(built, _dir("docs"), report)
    manifest.write_world_dna(os.path.join(DIST, "docs"), report)
    ok = manifest.write_validation(os.path.join(DIST, "docs"), report, problems)
    return report, problems, ok, built


def stage_reuse():
    built, report = build()
    _hide_library(True)
    good = True
    for name, builder in [("A_compact", reuse_test.layout_compact),
                          ("B_open", reuse_test.layout_open),
                          ("C_corridor", reuse_test.layout_corridor)]:
        good &= reuse_test.check_layout(built, name, builder, report)
    reuse_test.render_previews(built, os.path.join(DIST, "reuse"), report)
    _hide_library(False)
    return report, good


def stage_showcase(save=True):
    built, report = build()
    n = showcase.build(built)
    lighting.setup(bpy.context.scene)
    cameras.build_stills(); cameras.build_panorama()
    report.append(f"showcase assembled with {n} placed instances (all kit assets)")
    if save:
        _hide_library(False)
        library.save_master(os.path.join(DIST, "WORLD_KIT_master.blend"))
        report.append("saved WORLD_KIT_master.blend")
    _hide_library(True)
    return built, report


def stage_stills():
    built, report = stage_showcase(save=False)
    render.render_stills(bpy.context.scene, os.path.join(DIST, "renders"), report)
    return report


def stage_pano():
    built, report = stage_showcase(save=False)
    render.render_pano(bpy.context.scene, os.path.join(DIST, "renders"), report)
    return report


def stage_walk():
    built, report = stage_showcase(save=False)
    render.render_walkthrough(bpy.context.scene, os.path.join(DIST, "renders"), report)
    return report


def stage_catalog():
    built, report = build()
    _hide_library(True)
    tdir = os.path.join(DIST, "catalog", "thumbs")
    catalog.render_thumbnails(built, tdir, report)
    catalog.build_sheets(tdir, os.path.join(DIST, "catalog"), report)
    _hide_library(False)
    return report


def stage_textures():
    texgen.build_all(tex_dir())
    return ["textures generated"], []


STAGES = {
    "textures": stage_textures,
    "assets": stage_assets,
    "reuse": stage_reuse,
    "showcase": stage_showcase,
    "stills": stage_stills,
    "pano": stage_pano,
    "walk": stage_walk,
    "catalog": stage_catalog,
}


def run(stage="all"):
    if stage != "all":
        return STAGES[stage]()
    out = []
    problems = []
    for s in ["textures", "assets", "reuse", "showcase", "catalog"]:
        r = STAGES[s]()
        out += r[0]
    return out, problems
