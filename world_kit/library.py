"""Library assembly: build every registered asset into organised collections."""

from __future__ import annotations

import importlib
import time

import bpy

from . import dna, geo, materials, registry


def _scene():
    return bpy.context.scene


def _root():
    root = bpy.data.collections.get("WORLD_KIT")
    if root is None:
        root = bpy.data.collections.new("WORLD_KIT")
        _scene().collection.children.link(root)
    return root


def get_collections() -> dict:
    root = _root()
    out = {}
    for name, _desc in dna.COLLECTIONS:
        c = bpy.data.collections.get(name)
        if c is None:
            c = bpy.data.collections.new(name)
            root.children.link(c)
        out[name] = c
    return out


def _dispatch(path: str):
    mod_name, fn = path.split(":")
    mod = importlib.import_module(f"world_kit.assets.{mod_name}")
    return getattr(mod, fn)


def _bevel_for(spec) -> float:
    if spec.category == "11_DECALS":
        return 0.0
    if spec.category == "10_VEGETATION":
        return 0.01
    if spec.tier in (registry.DETAIL, registry.HERO):
        return 0.015
    return 0.02


def build_world_dna_collection(cols: dict):
    """00_WORLD_DNA: reference empties for scale + grid so the spec is visible."""
    c = cols["00_WORLD_DNA"]
    d = dna.DIMENSIONS
    # human scale reference
    h = bpy.data.objects.get("DNA_HUMAN_1_8M")
    if h is None:
        h = bpy.data.objects.new("DNA_HUMAN_1_8M", None)
        h.empty_display_type = "SINGLE_ARROW"
        h.empty_display_size = d["human_h"]
        c.objects.link(h)
    h.location = (0, 0, 0)
    # grid reference
    g = bpy.data.objects.get("DNA_BAY_4M")
    if g is None:
        g = bpy.data.objects.new("DNA_BAY_4M", None)
        g.empty_display_type = "CUBE"
        g.empty_display_size = 1.0
        c.objects.link(g)
    g.location = (0, 0, 0)
    g.scale = (d["bay_w"] / 2, d["bay_d"] / 2, d["wall_h"] / 2)


def build_library(tex_dir: str, report: list) -> dict:
    t0 = time.time()
    cols = get_collections()
    mats = materials.build_all(tex_dir)
    mats["MK_DECAL_OVERLAY_WATERLINE"] = materials.decal_variant(
        tex_dir, "MF_DECAL_WATERLINE", "MK_decal_waterline")
    mats["MK_DECAL_OVERLAY_CRACK"] = materials.decal_variant(
        tex_dir, "MF_DECAL_CRACK", "MK_decal_crack")
    build_world_dna_collection(cols)

    tmp = bpy.data.collections.get("WK_TMP")
    if tmp is None:
        tmp = bpy.data.collections.new("WK_TMP")
        _scene().collection.children.link(tmp)

    built = {}
    for spec in registry.REGISTRY:
        asset = geo.Asset(spec.name, spec, mats, tmp)
        _dispatch(spec.builder)(asset)
        obj = asset.finalize(bevel=_bevel_for(spec))
        # move from tmp into its category collection
        for uc in list(obj.users_collection):
            uc.objects.unlink(obj)
        cols[spec.category].objects.link(obj)
        built[spec.name] = obj
        report.append(f"built {spec.name:32s} tris={geo.tri_count(obj):6d} "
                      f"size=({obj.dimensions.x:.2f},{obj.dimensions.y:.2f},{obj.dimensions.z:.2f})")
    # tidy tmp
    for o in list(tmp.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    report.append(f"library built in {time.time() - t0:.1f}s, {len(built)} assets")
    return built


def save_master(path: str):
    materials.pack_all({m.name: m for m in bpy.data.materials if m.use_nodes})
    bpy.ops.wm.save_as_mainfile(filepath=path)
