"""Asset registry - the catalogue of the kit.

One entry per reusable asset.  Every field here is authored metadata that ends
up in the manifest, the thumbnail catalogue and the export filenames, so the
registry is the contract between the builders and everything downstream.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import dna

FOUNDATION = "FOUNDATION"
VARIATION = "VARIATION"
DETAIL = "DETAIL"
HERO = "HERO"

TRI_BUDGET = {FOUNDATION: 45000, VARIATION: 25000, DETAIL: 6000, HERO: 60000}


@dataclass
class AssetSpec:
    name: str
    category: str
    tier: str
    purpose: str
    materials: tuple[str, ...]
    size: tuple[float, float, float]          # w (X), d (Y), h (Z) in metres
    origin: str = "footprint centre at floor level (z=0)"
    grid: float = 1.0                          # snap increment, metres
    builder: str = ""                          # "module:function"
    notes: str = ""
    # connection edges, in grid cells, used by the reuse test
    connects: tuple[str, ...] = field(default_factory=tuple)
    export: bool = True


def _s(name, category, tier, purpose, materials, size, **kw):
    kw.setdefault("builder", "")
    return AssetSpec(name=name, category=category, tier=tier, purpose=purpose,
                     materials=tuple(materials), size=tuple(size), **kw)


C = {
    "arch": "01_ARCHITECTURE", "walls": "02_WALLS", "floors": "03_FLOORS",
    "dw": "04_DOORS_WINDOWS", "struct": "05_STRUCTURAL",
    "furn": "06_FURNITURE", "props": "07_PROPS", "lights": "08_LIGHTS",
    "sign": "09_SIGNAGE", "veg": "10_VEGETATION", "decals": "11_DECALS",
    "terrain": "12_TERRAIN", "hero": "13_HERO",
}

_CONC = "MK_CONCRETE_STRUCT"
_TILE = "MK_CERAMIC_TILE"
_TEAL = "MK_STEEL_PAINTED"
_OXIDE = "MK_STEEL_PRIMER"
_STEEL = "MK_STEEL_AGED"
_BRASS = "MK_BRASS"
_WOOD = "MK_TIMBER"
_GLASS = "MK_GLASS"
_WATER = "MK_WATER_BRINE"
_AMBER = "MK_EMISSIVE_AMBER"
_CYAN = "MK_EMISSIVE_CYAN"
_ENAMEL = "MK_SIGNAGE_ENAMEL"
_DECAL = "MK_DECAL_OVERLAY"

BAY = dna.DIMENSIONS["bay_w"]

REGISTRY: list[AssetSpec] = [
    # ------------------------------------------------------------- 01 ARCH
    _s("WK_ARCH_BAY_VAULT_A_01", C["arch"], FOUNDATION,
       "Primary structural bay: board-formed concrete shell with two segmental "
       "arch ribs, springing corbels and a coffered crown. Everything in the "
       "world is built from this piece.",
       (_CONC, _TILE, _OXIDE), (BAY, BAY, 4.8), grid=BAY,
       builder="architecture:bay_vault",
       connects=("-x", "+x", "-y", "+y"),
       notes="Origin at footprint centre, floor level. Vault springing at 3.6 m."),
    _s("WK_ARCH_BAY_FLAT_A_01", C["arch"], FOUNDATION,
       "Open-plan bay with a flat slab soffit and exposed beam grid. Used for "
       "working floors where the vault would block crane access.",
       (_CONC, _OXIDE, _STEEL), (BAY, BAY, 3.9), grid=BAY,
       builder="architecture:bay_flat", connects=("-x", "+x", "-y", "+y")),
    _s("WK_ARCH_BAY_OCULUS_A_01", C["arch"], VARIATION,
       "Vault bay with a 2.4 m square roof opening and a raised steel curb, so "
       "tall equipment and daylight can pass between levels.",
       (_CONC, _STEEL, _OXIDE), (BAY, BAY, 5.1), grid=BAY,
       builder="architecture:bay_oculus", connects=("-x", "+x", "-y", "+y")),
    _s("WK_ARCH_COLUMN_A_01", C["arch"], FOUNDATION,
       "Octagonal cast column with a splayed base and a corbelled capital. "
       "Carries every arch in the station.",
       (_CONC, _OXIDE), (0.7, 0.7, 3.6), grid=1.0,
       builder="architecture:column"),

    # -------------------------------------------------------------- 02 WALLS
    _s("WK_WALL_STANDARD_A_01", C["walls"], FOUNDATION,
       "4.0 m straight wall, 3.6 m high, 0.4 m thick, board-formed face with a "
       "tile dado and a concrete cap.",
       (_CONC, _TILE), (BAY, 0.4, 3.6), grid=BAY,
       builder="walls:standard_a", connects=("-x", "+x")),
    _s("WK_WALL_STANDARD_B_01", C["walls"], VARIATION,
       "Same wall with a recessed service panel and conduit chase. Breaks the "
       "rhythm of STANDARD_A without changing a single dimension.",
       (_CONC, _TILE, _STEEL, _OXIDE), (BAY, 0.4, 3.6), grid=BAY,
       builder="walls:standard_b", connects=("-x", "+x")),
    _s("WK_WALL_CORNER_INNER_A_01", C["walls"], FOUNDATION,
       "Inside 90 degree corner. Two wall faces meet on the 4.0 m grid with "
       "shared thickness so both return flush.",
       (_CONC, _TILE), (BAY, BAY, 3.6), grid=BAY,
       builder="walls:corner_inner", connects=("+x", "+y")),
    _s("WK_WALL_CORNER_OUTER_A_01", C["walls"], FOUNDATION,
       "Outside 90 degree corner with a quoin block at the arris. Completes the "
       "enclosure grammar together with CORNER_INNER.",
       (_CONC, _TILE), (BAY, BAY, 3.6), grid=BAY,
       builder="walls:corner_outer", connects=("+x", "-y")),
    _s("WK_WALL_DOORWAY_A_01", C["walls"], FOUNDATION,
       "Wall module carrying the standard 1.2 x 2.4 m opening with a cast "
       "surround. Pairs with WK_DOOR_FRAME_A_01 / WK_DOOR_LEAF_A_01.",
       (_CONC, _TILE, _OXIDE), (BAY, 0.4, 3.6), grid=BAY,
       builder="walls:doorway", connects=("-x", "+x")),
    _s("WK_WALL_WINDOW_A_01", C["walls"], FOUNDATION,
       "Wall module with a segmental arched opening at the standard sill. The "
       "only route daylight takes into the station.",
       (_CONC, _TILE, _OXIDE), (BAY, 0.4, 3.6), grid=BAY,
       builder="walls:window", connects=("-x", "+x")),
    _s("WK_WALL_BREACH_A_01", C["walls"], VARIATION,
       "Storm-breached wall: spalled arris, exposed rebar stubs and a rubble "
       "apron. The kit's damaged state, and the reason saltbush exists.",
       (_CONC, _STEEL, _TILE), (BAY, 0.4, 3.6), grid=BAY,
       builder="walls:breach", connects=("-x", "+x")),

    # ------------------------------------------------------------- 03 FLOORS
    _s("WK_FLOOR_SLAB_A_01", C["floors"], FOUNDATION,
       "Primary 4.0 m floor slab, 0.3 m thick, with a tile inlay field and a "
       "kerbed edge. The ground plane of the whole kit.",
       (_CONC, _TILE), (BAY, BAY, 0.3), grid=BAY, builder="floors:slab_a",
       notes="Slab top is z=0; the body sits below the floor plane."),
    _s("WK_FLOOR_SLAB_B_01", C["floors"], FOUNDATION,
       "Steel grating deck on a bearers-and-bolts frame. Lets the brine glow "
       "through and defines the working platforms.",
       (_STEEL, _OXIDE), (BAY, BAY, 0.3), grid=BAY, builder="floors:slab_b"),
    _s("WK_FLOOR_TRANSITION_A_01", C["floors"], VARIATION,
       "Slab-to-grating transition with a bolted nosing plate. Makes mixed "
       "floors read as deliberate rather than accidental.",
       (_CONC, _TILE, _STEEL), (BAY, BAY, 0.3), grid=BAY,
       builder="floors:transition"),
    _s("WK_FLOOR_CHANNEL_A_01", C["floors"], VARIATION,
       "Slab with a 0.6 m brine channel and a removable grate run down its "
       "centre line. Carries water, cyan light and sightlines.",
       (_CONC, _STEEL, _WATER), (BAY, BAY, 0.3), grid=BAY,
       builder="floors:channel"),

    # ------------------------------------------------------ 04 DOORS/WINDOWS
    _s("WK_DOOR_FRAME_A_01", C["dw"], FOUNDATION,
       "Riveted steel frame and head for the 1.2 x 2.4 m opening, with a "
       "threshold plate and hinge gudgeons.",
       (_OXIDE, _STEEL, _BRASS), (1.44, 0.44, 2.52), grid=0.1,
       builder="doors_windows:door_frame"),
    _s("WK_DOOR_LEAF_A_01", C["dw"], FOUNDATION,
       "Timber-faced steel leaf with a brass porthole and a lever latch. "
       "Pivots on its hinge edge, so it can be posed open or ajar.",
       (_TEAL, _WOOD, _BRASS, _GLASS), (1.2, 0.06, 2.4), grid=0.1,
       builder="doors_windows:door_leaf",
       origin="hinge edge at floor level, pivot on Z"),
    _s("WK_WINDOW_ARCH_A_01", C["dw"], FOUNDATION,
       "Segmental arched glazing unit: steel mullions, wired glass, salt-etched "
       "lower pane and a sloped sill that sheds spray.",
       (_STEEL, _GLASS, _OXIDE), (2.0, 0.12, 2.0), grid=0.1,
       builder="doors_windows:window_arch"),

    # ---------------------------------------------------------- 05 STRUCTURAL
    _s("WK_STRUCT_BEAM_A_01", C["struct"], FOUNDATION,
       "4.0 m riveted I-beam with end gussets. Spans a bay, carries catwalks "
       "and defines the horizontal rhythm.",
       (_OXIDE, _STEEL), (BAY, 0.28, 0.45), grid=BAY,
       builder="structural:beam"),
    _s("WK_STRUCT_CATWALK_A_01", C["struct"], FOUNDATION,
       "4.0 m grating catwalk, 1.2 m wide, with rails both sides and a "
       "kickplate. The main circulation module above floor level.",
       (_STEEL, _OXIDE, _TEAL), (BAY, 1.2, 1.0), grid=BAY,
       builder="structural:catwalk"),
    _s("WK_STRUCT_PLATFORM_A_01", C["struct"], FOUNDATION,
       "4.0 x 4.0 m mezzanine deck with edge kerbs and bearer pockets. The "
       "upper working floor.",
       (_STEEL, _OXIDE), (BAY, BAY, 0.35), grid=BAY,
       builder="structural:platform"),
    _s("WK_STRUCT_RAILING_A_01", C["struct"], VARIATION,
       "2.0 m rail segment: two horizontals, a 0.15 m kickplate and chamfered "
       "post caps. Fits every deck edge.",
       (_TEAL, _STEEL), (2.0, 0.1, 1.0), grid=1.0,
       builder="structural:railing"),
    _s("WK_STRUCT_STAIR_SPIRAL_A_01", C["struct"], FOUNDATION,
       "Helical stair, one full 3.6 m storey in 20 risers, inside a 4.0 m "
       "shaft. The kit's only vertical circulation that fits a single bay.",
       (_STEEL, _OXIDE, _TEAL, _WOOD), (3.6, 3.6, 3.6), grid=BAY,
       builder="structural:stair_spiral",
       notes="20 risers x 0.18 m; continuous handrail at 1.0 m."),
    _s("WK_STRUCT_PIPE_RUN_A_01", C["struct"], VARIATION,
       "4.0 m brine pipe run: 0.22 m ceramic-lined pipe, two collars and wall "
       "brackets. Runs along walls and under catwalks.",
       (_TEAL, _BRASS, _STEEL), (BAY, 0.4, 0.4), grid=BAY,
       builder="structural:pipe_run"),

    # ----------------------------------------------------------- 06 FURNITURE
    _s("WK_FURN_BENCH_A_01", C["furn"], DETAIL,
       "Salt-stained work bench: cast legs, timber top, a lower slat shelf and "
       "a brass vise mount. The only furniture the station ever had.",
       (_CONC, _WOOD, _STEEL, _BRASS), (2.0, 0.7, 0.9), grid=1.0,
       builder="furniture:bench"),

    # ---------------------------------------------------------------- 07 PROPS
    _s("WK_PROP_BARREL_A_01", C["props"], DETAIL,
       "Brine barrel: lathed stave profile, three steel hoops, a bung and a "
       "stencilled batch mark. Reads at any distance.",
       (_WOOD, _STEEL, _OXIDE), (0.62, 0.62, 0.9), grid=1.0,
       builder="props:barrel",
       notes="Stave lathe at 16 segments; hoops are real geometry."),
    _s("WK_PROP_CRATE_A_01", C["props"], DETAIL,
       "Slatted packing crate with chamfered battens and steel corner straps.",
       (_WOOD, _STEEL), (0.8, 0.6, 0.6), grid=1.0, builder="props:crate_a"),
    _s("WK_PROP_VALVE_A_01", C["props"], DETAIL,
       "Flanged brine valve on a stub stand: brass body, cast wheel with a "
       "mechanically meaningful pivot, gauge boss.",
       (_BRASS, _STEEL, _TEAL, _OXIDE), (0.7, 0.5, 0.9), grid=1.0,
       builder="props:valve", origin="flange centre at floor level"),

    # ---------------------------------------------------------------- 08 LIGHTS
    _s("WK_LIGHT_LAMP_WALL_A_01", C["lights"], DETAIL,
       "Caged sodium wall lamp: cast bracket, brass cap, wired guard and an "
       "emissive tube. The only warm light source in the world.",
       (_OXIDE, _BRASS, _AMBER, _STEEL), (0.34, 0.3, 0.42), grid=1.0,
       builder="lights:lamp_wall"),
    _s("WK_LIGHT_LAMP_PENDANT_A_01", C["lights"], DETAIL,
       "Suspended enamel-shade pendant with a chain and an emissive core. "
       "Hangs over benches and consoles.",
       (_TEAL, _STEEL, _AMBER), (0.5, 0.5, 1.4), grid=1.0,
       builder="lights:lamp_pendant", origin="ceiling attach point"),

    # --------------------------------------------------------------- 09 SIGNS
    _s("WK_SIGN_PLAQUE_A_01", C["sign"], DETAIL,
       "Vitreous enamel station plaque: white body, brine-teal capitals, four "
       "bolt holes, chipped rim. Carries the world's name.",
       (_ENAMEL, _TEAL, _BRASS), (0.7, 0.03, 0.44), grid=0.1,
       builder="signage:plaque"),
    _s("WK_SIGN_DIRECTIONAL_A_01", C["sign"], DETAIL,
       "Directional board with a cast arrow and a destination plate. Mounts to "
       "a wall or a railing post.",
       (_ENAMEL, _TEAL, _STEEL), (0.62, 0.03, 0.2), grid=0.1,
       builder="signage:directional"),
    _s("WK_SIGN_WARNING_A_01", C["sign"], DETAIL,
       "Ochre hazard placard with a black triangle and a two-line warning. "
       "Marks live brine and unstable floor.",
       (_ENAMEL, _STEEL), (0.4, 0.03, 0.4), grid=0.1,
       builder="signage:warning"),

    # ---------------------------------------------------------- 10 VEGETATION
    _s("WK_VEG_SALTBUSH_A_01", C["veg"], DETAIL,
       "Low grey-green saltbush cluster, never taller than 0.6 m. Marks "
       "neglect: breaches, unused edges, cracked slab.",
       (_CONC,), (1.0, 1.0, 0.6), grid=1.0, builder="vegetation:saltbush"),

    # -------------------------------------------------------------- 11 DECALS
    _s("WK_DECAL_WATERLINE_A_01", C["decals"], DETAIL,
       "4.0 x 1.6 m waterline stain sheet: tide band, salt bloom and downward "
       "streaks. Applied at the historic high-water mark.",
       ("MK_DECAL_OVERLAY_WATERLINE",), (BAY, 1.6, 0.01), grid=1.0,
       builder="decals:waterline"),
    _s("WK_DECAL_CRACK_A_01", C["decals"], DETAIL,
       "4.0 x 4.0 m crack and spall sheet for slabs and walls: hairline "
       "crazing plus two structural cracks with exposed aggregate.",
       ("MK_DECAL_OVERLAY_CRACK",), (BAY, BAY, 0.01), grid=1.0,
       builder="decals:crack"),

    # ------------------------------------------------------------- 12 TERRAIN
    _s("WK_TERRAIN_WATER_A_01", C["terrain"], FOUNDATION,
       "4.0 m brine water pane: translucent, cyan emissive, faintly rippled. "
       "The ground under the station.",
       (_WATER, _CYAN), (BAY, BAY, 0.05), grid=BAY, builder="terrain:water"),

    # ----------------------------------------------------------------- 13 HERO
    _s("WK_HERO_EVAPORATOR_A_01", C["hero"], HERO,
       "Great evaporator tank: 4.4 m riveted shell, banded courses, a laddered "
       "access cage, a brass relief stack and a cyan sight glass. The reason "
       "the station exists.",
       (_TEAL, _OXIDE, _STEEL, _BRASS, _CYAN), (4.4, 4.4, 6.4), grid=BAY,
       builder="hero:evaporator"),
    _s("WK_HERO_BEACON_A_01", C["hero"], HERO,
       "Signal beacon: tapering cast shaft, a glazed lantern with a brass "
       "fresnel ring, a gallery rail and a finial. The identity of the world.",
       (_CONC, _TEAL, _BRASS, _GLASS, _AMBER, _STEEL), (3.2, 3.2, 10.4),
       grid=BAY, builder="hero:beacon"),
    _s("WK_HERO_SLUICE_A_01", C["hero"], HERO,
       "Sluice gate assembly: cast portal, counterweighted steel leaf, chain "
       "and windlass. Where the tide is let into the works.",
       (_CONC, _OXIDE, _STEEL, _BRASS, _TEAL), (4.0, 1.2, 4.2), grid=BAY,
       builder="hero:sluice"),
]

BY_NAME: dict[str, AssetSpec] = {a.name: a for a in REGISTRY}


def assets_in(category: str) -> list[AssetSpec]:
    return [a for a in REGISTRY if a.category == category]


def assets_by_tier(tier: str) -> list[AssetSpec]:
    return [a for a in REGISTRY if a.tier == tier]


def used_materials() -> list[str]:
    used: list[str] = []
    for a in REGISTRY:
        for m in a.materials:
            if m not in used:
                used.append(m)
    return used


# meta-families: consumed as masks / variant bases, never bound to a surface directly
ABSTRACT_FAMILIES = {"MK_DIRT_SALT", "MK_DECAL_OVERLAY"}


def unused_materials() -> list[str]:
    return [m for m in dna.MATERIAL_FAMILIES
            if m not in used_materials() and m not in ABSTRACT_FAMILIES]


def validate_registry() -> list[str]:
    """Static self-check on the registry itself (runs before any geometry)."""
    problems: list[str] = []
    for a in REGISTRY:
        if not a.name.startswith("WK_"):
            problems.append(f"{a.name}: name does not start with WK_")
        if len(a.name.split("_")) < 5:
            problems.append(f"{a.name}: name is not WK_CAT_ASSET_VAR_NUM")
        if not a.name.isupper():
            problems.append(f"{a.name}: name must be upper case")
        if a.category not in dict(dna.COLLECTIONS):
            problems.append(f"{a.name}: unknown category {a.category}")
        if a.tier not in TRI_BUDGET:
            problems.append(f"{a.name}: unknown tier {a.tier}")
        for m in a.materials:
            if m not in dna.MATERIAL_FAMILIES and not m.startswith("MK_DECAL_OVERLAY_"):
                problems.append(f"{a.name}: unknown material family {m}")
        if min(a.size) <= 0:
            problems.append(f"{a.name}: non-positive dimensions {a.size}")
        if not a.builder:
            problems.append(f"{a.name}: no builder assigned")
    if len(BY_NAME) != len(REGISTRY):
        problems.append("duplicate asset names in registry")
    for m in unused_materials():
        problems.append(f"material family {m} is defined but never used")
    return problems
