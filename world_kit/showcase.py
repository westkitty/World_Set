"""15_SHOWCASE - 'Brinefall Pump Hall', assembled ONLY from kit assets.

Every object in the scene is a linked duplicate of a kit mesh (shared data), so
the showcase doubles as proof that the modular system actually builds a
finished location.  No bespoke geometry is created here.
"""

from __future__ import annotations

import math

import bpy

from . import dna

COL = "15_SHOWCASE"
BAY = dna.DIMENSIONS["bay_w"]


def _coll():
    c = bpy.data.collections.get(COL)
    if c is None:
        c = bpy.data.collections.new(COL)
        bpy.data.collections["WORLD_KIT"].children.link(c)
    return c


def clear():
    c = _coll()
    for o in list(c.objects):
        bpy.data.objects.remove(o, do_unlink=True)


def put(built, name, x, y, z=0.0, rot=0.0, scale=1.0):
    src = built[name]
    ob = src.copy()                      # linked duplicate: shares mesh data
    _coll().objects.link(ob)
    ob.location = (x, y, z)
    ob.rotation_euler = (0, 0, math.radians(rot))
    ob.scale = (scale, scale, scale)
    ob.name = f"SC_{name}_{len(_coll().objects):03d}"
    return ob


def build(built) -> int:
    clear()
    n = 0

    # ---- floors (6) -----------------------------------------------------
    floor_plan = {
        (0, 0): "WK_FLOOR_CHANNEL_A_01", (1, 0): "WK_FLOOR_CHANNEL_A_01",
        (2, 0): "WK_FLOOR_SLAB_A_01",
        (0, 1): "WK_FLOOR_SLAB_A_01", (1, 1): "WK_FLOOR_SLAB_A_01",
        (2, 1): "WK_FLOOR_SLAB_A_01",
    }
    for (i, j), name in floor_plan.items():
        put(built, name, i * BAY + 2, j * BAY + 2); n += 1

    # ---- ceilings (6) ---------------------------------------------------
    ceil_plan = {
        (0, 0): "WK_ARCH_BAY_VAULT_A_01", (1, 0): "WK_ARCH_BAY_VAULT_A_01",
        (2, 0): "WK_ARCH_BAY_VAULT_A_01",
        (0, 1): "WK_ARCH_BAY_FLAT_A_01", (1, 1): "WK_ARCH_BAY_OCULUS_A_01",
        (2, 1): "WK_ARCH_BAY_FLAT_A_01",
    }
    for (i, j), name in ceil_plan.items():
        put(built, name, i * BAY + 2, j * BAY + 2); n += 1

    # ---- perimeter walls ------------------------------------------------
    for x in (2, 6, 10):                       # seaward (south) glazed wall
        put(built, "WK_WALL_WINDOW_A_01", x, 0); n += 1
    for x, name in ((2, "WK_WALL_STANDARD_B_01"), (6, "WK_WALL_STANDARD_A_01"),
                    (10, "WK_WALL_DOORWAY_A_01")):
        put(built, name, x, 8); n += 1
    for y in (2, 6):                           # west
        put(built, "WK_WALL_STANDARD_A_01", 0, y, rot=90); n += 1
    put(built, "WK_WALL_BREACH_A_01", 12, 2, rot=90); n += 1   # east damaged
    put(built, "WK_WALL_STANDARD_A_01", 12, 6, rot=90); n += 1

    # ---- columns at every grid intersection (cap junctions + carry arches)
    for i in range(4):
        for j in range(3):
            put(built, "WK_ARCH_COLUMN_A_01", i * BAY, j * BAY); n += 1

    # ---- hero: the great evaporator under the oculus -------------------
    put(built, "WK_HERO_EVAPORATOR_A_01", 6, 6); n += 1

    # ---- vertical circulation: spiral stair + platform + rails (west) ---
    put(built, "WK_STRUCT_STAIR_SPIRAL_A_01", 2, 6); n += 1
    put(built, "WK_STRUCT_PLATFORM_A_01", 2, 6, z=3.6); n += 1
    put(built, "WK_STRUCT_RAILING_A_01", 3.0, 4.9, z=3.6, rot=90); n += 1
    put(built, "WK_STRUCT_RAILING_A_01", 3.0, 7.1, z=3.6, rot=90); n += 1

    # ---- pipe run along west wall + a valve -----------------------------
    put(built, "WK_STRUCT_PIPE_RUN_A_01", 0.45, 4, z=0.6, rot=90); n += 1
    put(built, "WK_PROP_VALVE_A_01", 0.9, 4, rot=-90); n += 1

    # ---- catwalk over the channel (east bay) ----------------------------
    put(built, "WK_STRUCT_CATWALK_A_01", 10, 2, z=2.0, rot=90); n += 1
    put(built, "WK_STRUCT_BEAM_A_01", 10, 2, z=1.85, rot=90); n += 1

    # ---- furniture + props (storytelling, never adjacent repeats) -------
    put(built, "WK_FURN_BENCH_A_01", 1.6, 2.2, rot=90); n += 1
    put(built, "WK_PROP_BARREL_A_01", 10.6, 0.9); n += 1
    put(built, "WK_PROP_BARREL_A_01", 11.1, 1.3, rot=40); n += 1
    put(built, "WK_PROP_CRATE_A_01", 9.3, 7.2, rot=15); n += 1
    put(built, "WK_PROP_CRATE_A_01", 9.9, 7.3, rot=-30, scale=0.85); n += 1
    put(built, "WK_PROP_BARREL_A_01", 1.2, 7.2); n += 1

    # ---- lights ----------------------------------------------------------
    for (x, y, r) in [(2, 0.4, 0), (6, 0.4, 0), (10, 0.4, 0),
                      (0.4, 4, 90), (11.6, 4, -90)]:
        put(built, "WK_LIGHT_LAMP_WALL_A_01", x, y, z=2.6, rot=r); n += 1
    put(built, "WK_LIGHT_LAMP_PENDANT_A_01", 1.6, 2.2, z=3.6); n += 1
    put(built, "WK_LIGHT_LAMP_PENDANT_A_01", 9.6, 7.0, z=3.6); n += 1

    # ---- signage ---------------------------------------------------------
    put(built, "WK_SIGN_PLAQUE_A_01", 8.6, 7.77, z=1.7, rot=180); n += 1
    put(built, "WK_SIGN_WARNING_A_01", 11.3, 7.77, z=1.5, rot=180); n += 1
    put(built, "WK_SIGN_DIRECTIONAL_A_01", 0.23, 3.2, z=1.6, rot=90); n += 1

    # ---- decals ----------------------------------------------------------
    put(built, "WK_DECAL_WATERLINE_A_01", 3, 7.78, z=0.9, rot=180); n += 1
    put(built, "WK_DECAL_WATERLINE_A_01", 11.78, 2, z=0.9, rot=-90); n += 1
    put(built, "WK_DECAL_CRACK_A_01", 10, 2, z=0.001); n += 1

    # ---- vegetation at the breach + unused corner -----------------------
    put(built, "WK_VEG_SALTBUSH_A_01", 11.4, 1.2, scale=1.1); n += 1
    put(built, "WK_VEG_SALTBUSH_A_01", 12.2, 2.6, rot=60, scale=0.8); n += 1
    put(built, "WK_VEG_SALTBUSH_A_01", 11.5, 7.4, scale=0.7); n += 1

    # ---- exterior: the brine + the beacon --------------------------------
    for i in range(3):
        for j in (-1, -2):
            put(built, "WK_TERRAIN_WATER_A_01", i * BAY + 2, j * BAY + 2, z=-0.3); n += 1
    put(built, "WK_HERO_BEACON_A_01", 2, -7); n += 1
    put(built, "WK_HERO_SLUICE_A_01", 10, -1.0, rot=0); n += 1

    return n
