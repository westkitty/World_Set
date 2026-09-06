"""Material family library.

Turns the PNG sets produced by :mod:`world_kit.texgen` into Blender node
materials - one per family in :data:`world_kit.dna.MATERIAL_FAMILIES`.  Every
material carries the ``wk_tile_m`` and ``wk_texels_per_m`` custom properties the
UV projector and the validator read, so density is enforced in one place.

Builders get exactly these materials.  Decals may ask for a *controlled
variant* of :data:`MK_DECAL_OVERLAY` (:func:`decal_variant`) that reuses the
overlay node logic but points at a specific sheet.
"""

from __future__ import annotations

import os

import bpy

from . import dna

TEX_SUFFIX = {
    "MK_CONCRETE_STRUCT": "concrete",
    "MK_CERAMIC_TILE": "tile",
    "MK_STEEL_PAINTED": "paint_teal",
    "MK_STEEL_PRIMER": "paint_oxide",
    "MK_STEEL_AGED": "steel",
    "MK_BRASS": "brass",
    "MK_TIMBER": "wood",
    "MK_WATER_BRINE": "water",
    "MK_SIGNAGE_ENAMEL": "enamel",
}

# families that are masks/abstract and never become a surface material
NON_SURFACE = {"MK_DIRT_SALT"}


def _img(tex_dir, name, non_color=False):
    path = os.path.join(tex_dir, f"{name}.png")
    key = "wk_" + os.path.basename(path) + ("_nc" if non_color else "")
    img = bpy.data.images.get(key)
    if img is None:
        img = bpy.data.images.load(path, check_existing=True)
        img.name = key
    if non_color:
        img.colorspace_settings.name = "Non-Color"
    return img


def _new_mat(key: str) -> bpy.types.Material:
    name = f"MF_{key}"
    m = bpy.data.materials.get(name)
    if m:
        bpy.data.materials.remove(m)
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m["wk_family"] = key
    fam = dna.MATERIAL_FAMILIES[key]
    m["wk_tile_m"] = fam["tile_m"]
    m["wk_texels_per_m"] = fam["texels_per_m"]
    return m


def _princ(m):
    return m.node_tree.nodes["Principled BSDF"]


def _set(p, socket, value):
    if socket in p.inputs:
        p.inputs[socket].default_value = value


def _wire_pbr(m, tex_dir, fam, base_img, normal_img, rough_img):
    nt = m.node_tree
    p = _princ(m)
    tb = nt.nodes.new("ShaderNodeTexImage"); tb.image = base_img
    tb.location = (-600, 300)
    nt.links.new(tb.outputs["Color"], p.inputs["Base Color"])

    if normal_img:
        tn = nt.nodes.new("ShaderNodeTexImage"); tn.image = normal_img
        tn.location = (-600, 0)
        nm = nt.nodes.new("ShaderNodeNormalMap"); nm.location = (-300, -100)
        nm.inputs["Strength"].default_value = fam.get("normal_strength", 1.0)
        nt.links.new(tn.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], p.inputs["Normal"])

    if rough_img:
        tr = nt.nodes.new("ShaderNodeTexImage"); tr.image = rough_img
        tr.location = (-600, -300)
        nt.links.new(tr.outputs["Color"], p.inputs["Roughness"])
    else:
        lo, hi = fam["roughness"]
        p.inputs["Roughness"].default_value = (lo + hi) / 2.0

    _set(p, "Metallic", fam["metallic"])
    return p


def build_all(tex_dir: str) -> dict:
    """Return ``{family_key: Material}`` for every surface family."""
    mats: dict = {}
    for key, fam in dna.MATERIAL_FAMILIES.items():
        if key in NON_SURFACE:
            continue
        m = _new_mat(key)
        p = _princ(m)
        suffix = TEX_SUFFIX.get(key)

        if key == "MK_GLASS":
            c = dna.color("glass_tint")
            _set(p, "Base Color", c)
            _set(p, "Roughness", 0.1)
            _set(p, "Metallic", 0.0)
            _set(p, "Alpha", fam.get("alpha", 0.3))
            _set(p, "IOR", 1.45)
            m.blend_method = "BLEND"

        elif key in ("MK_EMISSIVE_AMBER", "MK_EMISSIVE_CYAN"):
            e = dna.color(fam["emission"])
            _set(p, "Base Color", e)
            if "Emission Color" in p.inputs:
                p.inputs["Emission Color"].default_value = e
            _set(p, "Emission Strength", fam["emission_strength"])
            m["wk_emit"] = 1

        elif key == "MK_WATER_BRINE":
            wimg = _img(tex_dir, "MK_water_normal", True)
            nt = m.node_tree
            tn = nt.nodes.new("ShaderNodeTexImage"); tn.image = wimg
            nm = nt.nodes.new("ShaderNodeNormalMap")
            nm.inputs["Strength"].default_value = fam.get("normal_strength", 1.0)
            nt.links.new(tn.outputs["Color"], nm.inputs["Color"])
            nt.links.new(nm.outputs["Normal"], p.inputs["Normal"])
            _set(p, "Base Color", dna.color("water_brine"))
            _set(p, "Roughness", 0.05)
            _set(p, "Alpha", fam.get("alpha", 0.55))
            _set(p, "IOR", 1.33)
            if "Emission Color" in p.inputs:
                p.inputs["Emission Color"].default_value = dna.color("brine_glow")
                p.inputs["Emission Strength"].default_value = 0.6
            m.blend_method = "BLEND"

        elif suffix:
            base = _img(tex_dir, f"MK_{suffix}_albedo")
            normal = _img(tex_dir, f"MK_{suffix}_normal", True)
            rough = _img(tex_dir, f"MK_{suffix}_rough", True)
            _wire_pbr(m, tex_dir, fam, base, normal, rough)
        mats[key] = m
    return mats


def decal_variant(tex_dir: str, name: str, sheet: str, family="MK_DECAL_OVERLAY") -> bpy.types.Material:
    """A controlled decal-overlay variant bound to one RGBA sheet."""
    m = bpy.data.materials.get(name)
    if m:
        bpy.data.materials.remove(m)
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m["wk_family"] = family
    m["wk_tile_m"] = dna.MATERIAL_FAMILIES[family]["tile_m"]
    m["wk_texels_per_m"] = dna.MATERIAL_FAMILIES[family]["texels_per_m"]
    m.blend_method = "BLEND"
    m.show_transparent_back = False
    m.use_backface_culling = True
    nt = m.node_tree
    p = _princ(m)
    img = _img(tex_dir, sheet)
    tb = nt.nodes.new("ShaderNodeTexImage"); tb.image = img
    nt.links.new(tb.outputs["Color"], p.inputs["Base Color"])
    nt.links.new(tb.outputs["Alpha"], p.inputs["Alpha"])
    _set(p, "Roughness", 0.8)
    _set(p, "Specular IOR Level", 0.1)
    return m


def pack_all(mats: dict):
    """Pack textures into the .blend so it is self-contained."""
    for m in mats.values():
        for node in m.node_tree.nodes:
            if node.type == "TEX_IMAGE" and node.image:
                try:
                    node.image.pack()
                except Exception:
                    pass
