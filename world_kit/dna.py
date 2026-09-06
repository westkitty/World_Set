"""WORLD DNA - the single source of truth for the WORLD KIT.

Everything downstream (geometry, materials, showcase, manifest, docs) reads from
this module.  Re-targeting the kit at another environment concept means editing
CONCEPT / PALETTE / DIMENSIONS and the builder modules; no other file hard-codes
a dimension or a colour.

CONCEPT CHOSEN FOR THIS KIT
---------------------------
BRINEFALL SALTLIGHT STATION - a decommissioned tidal salt-works and signal
station, cast in mass concrete and bolted to a sea wall.  The world reads as
"heavy civil engineering that has been losing a fifty-year argument with salt
water": segmental arch ribs, salt-glazed ceramic tile, red-oxide primer under
flaking brine-teal paint, patinated brass, and a cold cyan brine that still
glows under the floor grating.
"""

from __future__ import annotations

KIT_ID = "WK-BRINEFALL-001"
KIT_NAME = "WORLD KIT - Brinefall Saltlight Station"
KIT_VERSION = "1.0"

# --------------------------------------------------------------------------- #
# CONCEPT
# --------------------------------------------------------------------------- #
CONCEPT = {
    "name": "Brinefall Saltlight Station",
    "one_liner": (
        "A decommissioned tidal salt-works and signal station: mass concrete "
        "arches, salt-glazed tile and flaking brine-teal steel, built onto a "
        "sea wall and slowly being reclaimed by the brine it used to process."
    ),
    "era": "1928 built, 1971 abandoned, 2024 explored",
    "climate": "Cold temperate coast, constant salt spray, overcast diffuse light",
    "occupancy": "Unmanned. Left in a hurry; salt has done the rest.",
    "narrative_beats": [
        "The brine still circulates - the cyan glow under the gratings is real.",
        "Every painted surface is failing at its edges first.",
        "The signal beacon is the only thing anyone ever maintained.",
        "Salt crystallises wherever water stopped moving.",
    ],
}

# --------------------------------------------------------------------------- #
# DIMENSIONS  (metres)  -- the modular grammar
# --------------------------------------------------------------------------- #
DIMENSIONS = {
    # grid
    "grid_arch": 4.0,          # architectural bay / snap for architecture
    "grid_prop": 1.0,          # prop + detail snap
    "grid_tolerance": 0.005,   # max deviation allowed when snapping

    # bay
    "bay_w": 4.0,
    "bay_d": 4.0,
    "wall_h": 3.6,             # finished floor -> underside of vault springing
    "wall_t": 0.4,             # wall thickness
    "vault_rise": 1.2,         # arch rise above the springing line
    "floor_t": 0.3,            # slab thickness (slab top is z = 0)

    # members
    "col_w": 0.5,
    "col_d": 0.5,
    "beam_h": 0.45,
    "beam_w": 0.28,
    "trim_h": 0.18,

    # openings
    "door_w": 1.2,
    "door_h": 2.4,
    "window_w": 1.6,
    "window_h": 1.4,
    "window_sill": 1.2,
    "arch_opening_w": 2.0,
    "arch_opening_h": 2.6,

    # circulation
    "catwalk_w": 1.2,
    "rail_h": 1.0,
    "stair_rise": 0.18,
    "stair_steps": 20,         # 20 x 0.18 = 3.6 m  (one full storey)
    "stair_radius": 1.7,
    "ladder_w": 0.5,

    # human reference
    "human_h": 1.8,
    "eye_h": 1.62,
    "handrail_grip": 0.05,
    "step_nose": 0.03,
}

# --------------------------------------------------------------------------- #
# PALETTE  (linear-ish sRGB hex; authored as art direction, converted in code)
# --------------------------------------------------------------------------- #
PALETTE = {
    # colour hierarchy: 1 = dominant mass, 4 = accents (< 5% of any frame)
    "concrete_light": 0x8C8677,   # L1 dominant mass
    "concrete_mid":   0x7A7568,
    "concrete_dark":  0x5D594F,
    "tile_glaze":     0x37666A,   # L2 secondary surface
    "tile_body":      0xCFC9B8,
    "paint_teal":     0x2E5A5C,   # L2 secondary paint
    "paint_teal_hi":  0x3B6E70,
    "oxide_primer":   0x8A3A22,   # L3 revealed substrate
    "safety_ochre":   0xC9A227,   # L4 accent, aged
    "brass":          0xB08A3E,   # L4 accent
    "brass_patina":   0x4E7A63,
    "steel_aged":     0x6A6560,
    "rust":           0x7A4A2A,
    "salt_crust":     0xE8E4D8,   # highest value = read as "salt", never white
    "wood_slat":      0x6B4B32,
    "glass_tint":     0xA8C4B8,
    "water_brine":    0x123B3F,
    "lamp_amber":     0xFFB45E,   # emissive
    "brine_glow":     0x4FD6C8,   # emissive
}

# --------------------------------------------------------------------------- #
# VISUAL INVARIANTS - every asset must obey all of these
# --------------------------------------------------------------------------- #
INVARIANTS = [
    ("IV-01", "Scale", "Every asset is authored in metres, 1 unit = 1 m, "
     "with a 1.8 m human as the only scale reference."),
    ("IV-02", "Snap", "Architectural footprints are integer multiples of the "
     "4.0 m bay; props snap to 1.0 m; nothing sits off-grid in the showcase."),
    ("IV-03", "Origin", "Origins sit on the floor plane (z=0) at the centre of "
     "the module footprint, except articulated parts (door leaf, valve wheel, "
     "beacon lantern) which pivot on their mechanical axis."),
    ("IV-04", "Forward", "Forward is -Y. Long axis of linear modules runs X."),
    ("IV-05", "Silhouette", "Heavy at the base, tapered upward. No element is "
     "wider at the top than at the bottom unless it is a bracket."),
    ("IV-06", "Bevel", "Every silhouette edge that a viewer can see carries a "
     "0.02 m chamfer. No infinitely sharp convex edges, no >0.05 m fillets on "
     "structural members."),
    ("IV-07", "Segments", "Cylinders 16-24 segments, small fittings 12, "
     "lathe profiles never exceed 24 profile points."),
    ("IV-08", "Colour", "Concrete + tile carry >= 70% of frame area. Painted "
     "steel 20-25%. Brass and ochre accents never exceed 5%."),
    ("IV-09", "Wear", "Wear is directional and gravity-fed: damage at edges "
     "and corners first, salt crust at or below the waterline, rust streaks "
     "running downward from every fastener."),
    ("IV-10", "Texel", "256 texels/metre on architecture and terrain, "
     "512 texels/metre on props, furniture, signage and hero assets."),
    ("IV-11", "Materials", "An asset may only use material families from the "
     "14_MATERIALS library. No asset-specific one-off materials."),
    ("IV-12", "Density", "Foundation module <= 45k tris, variation <= 25k, "
     "detail <= 6k, hero <= 60k. Silhouette beats triangle count."),
    ("IV-13", "Emissive", "Exactly two light colours exist: amber sodium "
     "(2000 K) and cyan brine. Nothing else emits."),
    ("IV-14", "Naming", "WK_[CATEGORY]_[ASSET]_[VARIANT]_[NUMBER], upper "
     "case, no dots, no 'final', no 'copy'."),
]

# --------------------------------------------------------------------------- #
# DESIGN LANGUAGE (prose sections; rendered verbatim into docs/WORLD_DNA.md)
# --------------------------------------------------------------------------- #
LANGUAGE = {
    "architectural_language": (
        "Tidal-industrial masonry. Segmental arch ribs spring from a 2.4 m "
        "corbel line; bays are square and repeated; everything is built from "
        "the same 4.0 m bay and the same 0.4 m wall. No curved plan geometry - "
        "curves exist only in section (arches, tanks, pipes)."
    ),
    "dominant_shapes_silhouettes": (
        "Square bay, segmental arch, octagonal column, cylinder (tank, pipe, "
        "barrel), and the tapering beacon. A silhouette test: if a piece reads "
        "as a box with a chamfered top edge, it belongs; if it reads as "
        "organic, it does not."
    ),
    "shape_hierarchy": (
        "1) bay masses and the beacon tower, 2) arch ribs, columns, tanks, "
        "3) beams, catwalks, stairs, pipes, 4) trim, brackets, fittings, "
        "5) decals and salt. Higher levels are never decorated by lower ones."
    ),
    "structural_logic": (
        "Load runs arch -> corbel -> column -> footing. Every bracket visibly "
        "bolts to something. Gussets are triangular and never ornamental."
    ),
    "modular_dimensions": (
        "Bay 4.0 x 4.0 x 3.6 m, wall 0.4 m thick, slab 0.3 m thick, column "
        "0.5 x 0.5 m, catwalk 1.2 m wide, rail 1.0 m high. One storey = 3.6 m "
        "= 20 risers of 0.18 m."
    ),
    "proportions": (
        "Openings are narrow and tall (1.2 x 2.4 m doors, 1.6 x 1.4 m windows "
        "at a 1.2 m sill) because the wall is load-bearing. Wall-to-void ratio "
        "never exceeds 1:1 on any elevation."
    ),
    "construction_logic": (
        "Cast in place first, bolted on later. Cast elements (concrete, tile) "
        "are monolithic; bolted elements (steel, brass, timber) are visibly "
        "attached with flanges, collars and gussets."
    ),
    "material_families": (
        "Fourteen families: structural concrete, glazed ceramic tile, painted "
        "steel (teal), primer steel (oxide), aged steel, brass, timber, glass, "
        "brine water, emissive amber, emissive cyan, signage enamel, decal "
        "overlay, and a shared dirt/salt overlay used as a mask rather than a "
        "surface."
    ),
    "surface_treatment": (
        "Concrete is board-formed with a 0.2 m board rhythm and blowholes. "
        "Tile is 0.2 m square with a 6 mm grout line. Painted steel shows a "
        "rolled grain. Nothing is smooth and nothing is noisy."
    ),
    "wear_and_aging_logic": (
        "Three ageing agents, in order of strength: salt (crusts below the "
        "1.6 m waterline, effloresces in corners), water (streaks down from "
        "every fastener and joint), and mechanical wear (paint fails on convex "
        "edges, primer shows through, never bare metal first)."
    ),
    "colour_hierarchy": (
        "Concrete and tile dominate (>= 70%). Brine-teal paint is the "
        "identifying secondary (20-25%). Red oxide is revealed substrate, "
        "never a design colour. Ochre and brass are accents under 5%."
    ),
    "lighting_philosophy": (
        "Overcast cold sea daylight enters only through the arched openings on "
        "the seaward wall - it is the key light and it is always low and cool. "
        "Amber sodium fittings are the only interior sources. Cyan brine glow "
        "bounces up through floor gratings as fill. Shadows are soft; contrast "
        "comes from colour temperature, not from intensity."
    ),
    "polygon_density_philosophy": (
        "Geometry is spent on silhouette, never on surface detail. Surface "
        "detail lives in the texture set. A foundation module stays under "
        "45k tris; a hero under 60k; props under 6k."
    ),
    "bevel_philosophy": (
        "0.02 m chamfer on every readable convex edge, two segments. Larger "
        "radii only where a human hand or a rope would touch (rail tops, hatch "
        "coamings) and never above 0.05 m."
    ),
    "uv_philosophy": (
        "Box projection for cast members, cylindrical projection for lathed "
        "members, planar for decals. UVs are authored in tile units so that "
        "texel density is a property of the material family, not of the asset."
    ),
    "texel_density_target": "256 texels/m architecture and terrain, 512 texels/m props, furniture, signage, hero.",
    "prop_detail_hierarchy": (
        "Tier A props (barrel, valve) get a full lathe profile, real collars "
        "and a working pivot. Tier B props (crate, sack) are panel-built with "
        "chamfered edges. Nothing in Tier B gets a subdivision surface."
    ),
    "signage_language": (
        "Vitreous enamel plates, white body, brine-teal lettering, two bolt "
        "holes top and bottom, always mounted on a wall or a post, never "
        "hanging free. Lettering is condensed sans capitals; hazard placards "
        "use an ochre field with a black triangle."
    ),
    "environmental_storytelling_rules": [
        "Every prop must answer 'who used this last, and why did they leave it?'",
        "Salt crust marks the historic high-water line and nothing else.",
        "A doorway that is used is worn; a doorway that is not used is crusted.",
        "Never place a prop that implies a person is currently present.",
    ],
    "repetition_rules": (
        "Architectural modules repeat freely - that is the point. Props never "
        "repeat adjacently: no two identical props within one bay, no three "
        "identical props within a 8 m radius, and no prop cluster with a "
        "regular spacing under 1.5 m."
    ),
    "asymmetry_rules": (
        "The architecture is symmetric; the contents are not. Break bay "
        "symmetry by placing at least one off-grid prop, one damaged module "
        "and one signage plate per three bays."
    ),
    "vegetation_logic": (
        "Only salt-tolerant growth: a low grey-green saltbush that colonises "
        "cracked slab and never grows taller than 0.6 m. It marks neglect, so "
        "it clusters at breaches and unused edges, never in circulation."
    ),
    "terrain_language": (
        "The station stands on a concrete sea wall over open brine. Terrain is "
        "expressed as water plane, embankment rubble and rock armour - flat, "
        "horizontal, heavy. No hills, no organic landforms."
    ),
}

# --------------------------------------------------------------------------- #
# MATERIAL FAMILIES - shared logic, controlled variants
# --------------------------------------------------------------------------- #
# texels_per_m is enforced by the UV projector, tile_m is the authored repeat.
MATERIAL_FAMILIES = {
    "MK_CONCRETE_STRUCT": {
        "label": "Structural Concrete",
        "base_color": "concrete_light", "tile_m": 4.0, "texels_per_m": 256,
        "roughness": (0.78, 0.95), "metallic": 0.0, "normal_strength": 0.55,
        "note": "Board-formed mass concrete. The dominant family.",
    },
    "MK_CERAMIC_TILE": {
        "label": "Salt-Glazed Ceramic Tile",
        "base_color": "tile_body", "tile_m": 2.0, "texels_per_m": 256,
        "roughness": (0.22, 0.55), "metallic": 0.0, "normal_strength": 0.8,
        "note": "0.2 m squares, 6 mm grout, glaze pooling at edges.",
    },
    "MK_STEEL_PAINTED": {
        "label": "Painted Steel - Brine Teal",
        "base_color": "paint_teal", "tile_m": 2.0, "texels_per_m": 256,
        "roughness": (0.42, 0.72), "metallic": 0.0, "normal_strength": 0.5,
        "note": "Top coat over oxide primer; chips reveal primer, never bare metal.",
    },
    "MK_STEEL_PRIMER": {
        "label": "Primer Steel - Red Oxide",
        "base_color": "oxide_primer", "tile_m": 2.0, "texels_per_m": 256,
        "roughness": (0.6, 0.85), "metallic": 0.05, "normal_strength": 0.6,
        "note": "Revealed substrate. Used for worn faces and hidden structure.",
    },
    "MK_STEEL_AGED": {
        "label": "Aged Steel",
        "base_color": "steel_aged", "tile_m": 1.0, "texels_per_m": 512,
        "roughness": (0.35, 0.7), "metallic": 0.85, "normal_strength": 0.7,
        "note": "Unpainted fittings, gratings, fasteners. Rusted at contact.",
    },
    "MK_BRASS": {
        "label": "Patinated Brass",
        "base_color": "brass", "tile_m": 0.5, "texels_per_m": 512,
        "roughness": (0.18, 0.5), "metallic": 1.0, "normal_strength": 0.4,
        "note": "Accent metal. Verdigris in recesses only.",
    },
    "MK_TIMBER": {
        "label": "Brine-Soaked Timber",
        "base_color": "wood_slat", "tile_m": 1.0, "texels_per_m": 512,
        "roughness": (0.6, 0.9), "metallic": 0.0, "normal_strength": 0.7,
        "note": "Slats and packing only, always chamfered, always greyed.",
    },
    "MK_GLASS": {
        "label": "Wired Glass",
        "base_color": "glass_tint", "tile_m": 1.0, "texels_per_m": 512,
        "roughness": (0.05, 0.18), "metallic": 0.0, "normal_strength": 0.0,
        "alpha": 0.28,
        "note": "Arched window units. Slight green cast, salt-etched.",
    },
    "MK_WATER_BRINE": {
        "label": "Brine Water",
        "base_color": "water_brine", "tile_m": 4.0, "texels_per_m": 256,
        "roughness": (0.02, 0.08), "metallic": 0.0, "normal_strength": 1.0,
        "alpha": 0.55,
        "note": "Stagnant, glowing, flat. Never animated in stills.",
    },
    "MK_EMISSIVE_AMBER": {
        "label": "Emissive - Sodium Amber",
        "base_color": "lamp_amber", "tile_m": 1.0, "texels_per_m": 512,
        "roughness": (0.4, 0.4), "metallic": 0.0, "normal_strength": 0.0,
        "emission": "lamp_amber", "emission_strength": 12.0,
        "note": "2000 K sodium. The only warm light in the world.",
    },
    "MK_EMISSIVE_CYAN": {
        "label": "Emissive - Brine Cyan",
        "base_color": "brine_glow", "tile_m": 1.0, "texels_per_m": 512,
        "roughness": (0.3, 0.3), "metallic": 0.0, "normal_strength": 0.0,
        "emission": "brine_glow", "emission_strength": 6.0,
        "note": "Cherenkov-ish brine glow. Fill light only, never a key.",
    },
    "MK_SIGNAGE_ENAMEL": {
        "label": "Vitreous Enamel Signage",
        "base_color": "salt_crust", "tile_m": 1.0, "texels_per_m": 512,
        "roughness": (0.18, 0.35), "metallic": 0.0, "normal_strength": 0.35,
        "note": "Glossy enamel plate with chipped rim and two bolt holes.",
    },
    "MK_DECAL_OVERLAY": {
        "label": "Decal Overlay",
        "base_color": "concrete_dark", "tile_m": 4.0, "texels_per_m": 256,
        "roughness": (0.5, 0.9), "metallic": 0.0, "normal_strength": 0.0,
        "alpha": 1.0,
        "note": "Alpha-blended storytelling sheets: waterline, cracks, salt, marks.",
    },
    "MK_DIRT_SALT": {
        "label": "Dirt / Salt Overlay Mask",
        "base_color": "salt_crust", "tile_m": 4.0, "texels_per_m": 256,
        "roughness": (0.8, 1.0), "metallic": 0.0, "normal_strength": 0.0,
        "note": "Shared weathering mask consumed by other families.",
    },
}

# --------------------------------------------------------------------------- #
# COLLECTION LAYOUT (Blender collections)
# --------------------------------------------------------------------------- #
COLLECTIONS = [
    ("00_WORLD_DNA",   "Spec sheets: dimension reference, palette, human scale."),
    ("01_ARCHITECTURE", "Bays, vaults, columns - the load-bearing vocabulary."),
    ("02_WALLS",        "Straight, corner, opening and damaged wall modules."),
    ("03_FLOORS",       "Slabs, gratings, transitions, brine channels."),
    ("04_DOORS_WINDOWS", "Frames, leaves, arched glazing."),
    ("05_STRUCTURAL",   "Beams, catwalks, platforms, rails, stairs, pipes."),
    ("06_FURNITURE",    "Station furniture, sparse by design."),
    ("07_PROPS",        "Barrels, crates, valves - the storytelling tier."),
    ("08_LIGHTS",       "Physical fixtures; the only emissive geometry."),
    ("09_SIGNAGE",      "Enamel plates, directional and hazard placards."),
    ("10_VEGETATION",   "Salt-tolerant growth only."),
    ("11_DECALS",       "Weathering sheets."),
    ("12_TERRAIN",      "Water plane and ground armour."),
    ("13_HERO",         "Identity objects."),
    ("14_MATERIALS",    "Shared material family library."),
    ("15_SHOWCASE",     "The assembled demonstration environment."),
]

CATEGORY_EXPORT_DIRS = {
    "01_ARCHITECTURE": "architecture",
    "02_WALLS": "walls",
    "03_FLOORS": "floors",
    "04_DOORS_WINDOWS": "doors_windows",
    "05_STRUCTURAL": "structural",
    "06_FURNITURE": "furniture",
    "07_PROPS": "props",
    "08_LIGHTS": "lights",
    "09_SIGNAGE": "signage",
    "10_VEGETATION": "vegetation",
    "11_DECALS": "decals",
    "12_TERRAIN": "terrain",
    "13_HERO": "hero",
}

# --------------------------------------------------------------------------- #
# LIGHTING / RENDER PHILOSOPHY (consumed by lighting.py and render.py)
# --------------------------------------------------------------------------- #
LIGHTING = {
    "key": {
        "role": "Overcast sea daylight through the seaward arched openings",
        "color": 0xBFD4E0, "strength": 6.0, "elevation_deg": 14.0,
        "azimuth_deg": 205.0, "angle_deg": 45.0,
    },
    "fill_sky": {
        "role": "Cold skylight dome", "color": 0x7E96A8, "strength": 0.35,
    },
    "bounce_brine": {
        "role": "Cyan bounce off the brine under the gratings",
        "color": 0x2E8F8A, "strength": 3.0,
    },
    "practical_amber": {
        "role": "Sodium fixtures", "color": 0xFFB45E, "strength": 18.0,
        "radius": 0.35,
    },
    "beacon": {
        "role": "Beacon lantern - the focal point", "color": 0xFFD9A0,
        "strength": 60.0, "radius": 0.6,
    },
    "world_strength": 0.25,
    "exposure": 0.0,
}

RENDER = {
    "engine": "CYCLES",
    "device": "CPU",
    "denoiser": "OIDN",
    "stills": {"width": 1024, "height": 576, "samples": 32, "denoise": True},
    "reuse_previews": {"width": 640, "height": 360, "samples": 48, "denoise": True},
    "thumbnails": {"width": 384, "height": 384, "samples": 24, "denoise": True},
    "panorama": {"width": 1536, "height": 768, "samples": 32, "denoise": True},
    "walkthrough": {
        "width": 640, "height": 360, "samples": 12, "denoise": True,
        "fps": 24, "seconds": 5,
    },
    "color_management": {"view": "Filmic", "look": "Medium Contrast",
                          "exposure": 0.0},
}


def hex_to_linear(hex_int: int) -> tuple[float, float, float]:
    """sRGB 8-bit hex -> linear RGB triple (Blender stores colours linearly)."""
    out = []
    for shift in (16, 8, 0):
        c = ((hex_int >> shift) & 0xFF) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


def color(name: str) -> tuple[float, float, float, float]:
    """Named palette colour as an RGBA linear tuple for Blender sockets."""
    r, g, b = hex_to_linear(PALETTE[name])
    return (r, g, b, 1.0)


def hex_srgb(hex_int: int) -> str:
    return "#{:06X}".format(hex_int)


def dim(key: str) -> float:
    return DIMENSIONS[key]


def summary_lines() -> list[str]:
    """Compact human-readable DNA summary, used in logs and reports."""
    d = DIMENSIONS
    return [
        f"kit        : {KIT_ID} / {KIT_NAME}",
        f"concept    : {CONCEPT['name']}",
        f"grid       : {d['grid_arch']} m bay / {d['grid_prop']} m prop",
        f"bay        : {d['bay_w']} x {d['bay_d']} x {d['wall_h']} m "
        f"(wall {d['wall_t']} m, slab {d['floor_t']} m)",
        f"vault      : springing {d['wall_h']} m + rise {d['vault_rise']} m",
        f"openings   : door {d['door_w']}x{d['door_h']}  "
        f"window {d['window_w']}x{d['window_h']} @ {d['window_sill']}",
        f"stair      : {d['stair_steps']} x {d['stair_rise']} m "
        f"= {d['stair_steps'] * d['stair_rise']:.2f} m rise",
        f"materials  : {len(MATERIAL_FAMILIES)} families",
        f"invariants : {len(INVARIANTS)} rules",
    ]
