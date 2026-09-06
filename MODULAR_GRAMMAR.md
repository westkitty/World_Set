# MODULAR GRAMMAR SPECIFICATION
## SYSTEM: WORLD KIT — "SITE-44 SUB-AQUIFER RESEARCH COMPLEX"
**Document Version:** 1.0.0  
**Status:** Canonical Construction Standard

---

### 1. The Metric Grid System

All structural components in WORLD KIT adhere to a strict Cartesian snapping grid based on powers of two and metric integers:

| Grid Level | Step Size | Usage |
| :--- | :--- | :--- |
| **Primary (Macro)** | $4.0\text{m}$ | Standard wall spans, floor slabs, ceiling coffers, column bay spacing |
| **Secondary (Meso)** | $2.0\text{m}$ | Narrow corridors, stair runs, catwalk widths, door rough openings |
| **Tertiary (Sub)** | $0.5\text{m}$ | Equipment footprints, window inserts, column profiles, platform offsets |
| **Detail (Micro)** | $0.25\text{m}$ | Wall thickness ($0.25\text{m}$), conduit spacing, trim offsets, stair risers |

```
  +-----------------------+-----------------------+  Z = 4.0m (Ceiling Plane)
  |                       |                       |
  |  WK_WALL_SOLID_A_01   |  WK_WALL_DOORFRAME_01 |
  |      [ 4m x 4m ]      |     [ 4m x 4m ]       |
  |                       |      +---------+      |
  |                       |      | Door    |      |  Z = 2.5m (Door Head)
  |                       |      | 2m x    |      |
  |                       |      | 2.5m    |      |
  +-----------------------+------+---------+------+  Z = 0.0m (Floor Plane)
  <------ 4.0m Span -----><------ 4.0m Span ----->
```

---

### 2. Snapping Origins & Reference Pivots

To ensure seamless alignment in Blender and real-time game engines (Unreal, Unity, Godot):
* **Walls (`WK_WALL_*`):** Pivot placed at bottom-center `(X=0, Y=0, Z=0)`. The wall extends along $X \in [-2.0\text{m}, +2.0\text{m}]$, with thickness $Y \in [-0.125\text{m}, +0.125\text{m}]$, and height $Z \in [0.0\text{m}, 4.0\text{m}]$.
* **Floors (`WK_FLOOR_*`):** Pivot placed at top-center `(X=0, Y=0, Z=0)`. The floor tile extends $X, Y \in [-2.0\text{m}, +2.0\text{m}]$, extending downward $Z \in [-0.3\text{m}, 0.0\text{m}]$.
* **Ceilings (`WK_CEIL_*`):** Pivot placed at bottom-center `(X=0, Y=0, Z=0)`. Extends upward into the plenum space.
* **Columns (`WK_STRUCT_COLUMN_*`):** Pivot placed at bottom-center `(0, 0, 0)`. Footprint centered at $(0, 0)$, allowing exact placement at modular wall intersections.
* **Stairs (`WK_STRUCT_STAIRS_*`):** Pivot at lower bottom edge `(0, 0, 0)`. Spans $2.0\text{m}$ in width, $4.0\text{m}$ in depth, ascending exactly $\Delta Z = +2.0\text{m}$. Two flights stacked or joined by landings reach the standard $\Delta Z = 4.0\text{m}$ upper floor.
* **Catwalks (`WK_FLOOR_CATWALK_*`):** Pivot at top-center. Spans $2.0\text{m} \times 4.0\text{m}$.
* **Railings (`WK_STRUCT_RAILING_*`):** Pivot at bottom-center. Height $= 1.1\text{m}$. Available in $4.0\text{m}$ full-span and $2.0\text{m}$ half-span variants.

---

### 3. Datum Lines & Universal Interconnects

1. **Utility Conduit Datum ($Z = 3.20\text{m}$):**
   * All horizontal wall pipes (`WK_UTIL_PIPE_RUN_A_01`) and wall panel junction pass-throughs align at exactly $Z = 3.20\text{m}$ above floor level.
   * Adjacent modules snap together with zero vertical discontinuity.
2. **Floor Raceway Datum ($Z = 0.0\text{m} - 0.15\text{m}$):**
   * Floor edge trims (`WK_FLOOR_TRIM_A_01`) provide integrated cable raceways along wall bases, masking any micro-seam variations.
3. **Signage & Fixture Datum ($Z = 2.40\text{m}$):**
   * Sector signs and hazard plaques align their horizontal centerline with the $Z = 2.40\text{m}$ datum line, directly above human eye level and beneath the utility conduit run.
4. **Door Rough Openings:**
   * Standardized rough opening is $2.00\text{m} \text{ wide} \times 2.50\text{m} \text{ high}$.
   * Bulkhead frame `WK_DOOR_BULKHEAD_A_01` fits the rough opening with $50\text{mm}$ flange perimeter overlap.

---

### 4. Connection Topology & Assembly Combinations

The kit supports infinite compositional flexibility:
* **Straight Corridor:** 
  `WK_FLOOR_SLAB_A_01` + `WK_WALL_SOLID_A_01` (Left) + `WK_WALL_PANEL_B_01` (Right) + `WK_CEIL_COFFER_A_01`.
* **90° Corner:**
  Connected using `WK_WALL_CORNER_IN_A_01` (internal bend) or `WK_WALL_CORNER_OUT_A_01` (external bend) flanked by `WK_STRUCT_COLUMN_A_01` for structural seam reinforcement.
* **T-Junction & Crossroads:**
  Modular wall doorframes `WK_WALL_DOORFRAME_A_01` or open spans flanked by structural columns.
* **Double-Height Hall / Industrial Bay:**
  Stacked walls ($Z = 0\text{m}$ and $Z = 4.0\text{m}$) supported by `WK_STRUCT_COLUMN_A_01` and spanned by `WK_STRUCT_BEAM_A_01` at $Z = 8.0\text{m}$.
* **Mezzanine / Catwalk Tier:**
  Elevated at $Z = 2.0\text{m}$ or $Z = 4.0\text{m}$ using `WK_FLOOR_CATWALK_C_01` accessed by `WK_STRUCT_STAIRS_A_01` and enclosed with `WK_STRUCT_RAILING_A_01`.

---

### 5. Repetition Breakage Strategy

To prevent the environment from feeling like a sterile repetitive grid:
1. **Wall Alternation:** Solid walls (`SOLID_A_01`), equipment alcove walls (`PANEL_B_01`), doorframes (`DOORFRAME_A_01`), and observation portals (`WINDOW_A_01`) swap within the same grid unit.
2. **Floor Variation:** Interspersing heavy concrete floor slabs with drainage grate sections (`FLOOR_GRATE_B_01`) over subterranean sluice channels.
3. **Surface Details & Props:** Asymmetrical placement of high-pressure canisters, junction boxes, hazard signs, and electrical consoles.
4. **Hero Landmark:** A central Geothermal Compression Core (`WK_HERO_CORE_A_01`) serves as a unique focal anchor.
