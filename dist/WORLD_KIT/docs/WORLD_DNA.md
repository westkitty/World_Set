# WORLD DNA

**WK-BRINEFALL-001** - WORLD KIT - Brinefall Saltlight Station

## Concept

A decommissioned tidal salt-works and signal station: mass concrete arches, salt-glazed tile and flaking brine-teal steel, built onto a sea wall and slowly being reclaimed by the brine it used to process.

- Era: 1928 built, 1971 abandoned, 2024 explored
- Climate: Cold temperate coast, constant salt spray, overcast diffuse light
- Occupancy: Unmanned. Left in a hurry; salt has done the rest.

Narrative beats:
- The brine still circulates - the cyan glow under the gratings is real.
- Every painted surface is failing at its edges first.
- The signal beacon is the only thing anyone ever maintained.
- Salt crystallises wherever water stopped moving.

## Modular grammar (metres)

| Parameter | Value |
|---|---|
| grid_arch | 4.0 |
| grid_prop | 1.0 |
| grid_tolerance | 0.005 |
| bay_w | 4.0 |
| bay_d | 4.0 |
| wall_h | 3.6 |
| wall_t | 0.4 |
| vault_rise | 1.2 |
| floor_t | 0.3 |
| col_w | 0.5 |
| col_d | 0.5 |
| beam_h | 0.45 |
| beam_w | 0.28 |
| trim_h | 0.18 |
| door_w | 1.2 |
| door_h | 2.4 |
| window_w | 1.6 |
| window_h | 1.4 |
| window_sill | 1.2 |
| arch_opening_w | 2.0 |
| arch_opening_h | 2.6 |
| catwalk_w | 1.2 |
| rail_h | 1.0 |
| stair_rise | 0.18 |
| stair_steps | 20 |
| stair_radius | 1.7 |
| ladder_w | 0.5 |
| human_h | 1.8 |
| eye_h | 1.62 |
| handrail_grip | 0.05 |
| step_nose | 0.03 |

## Visual invariants

- **IV-01 Scale** - Every asset is authored in metres, 1 unit = 1 m, with a 1.8 m human as the only scale reference.
- **IV-02 Snap** - Architectural footprints are integer multiples of the 4.0 m bay; props snap to 1.0 m; nothing sits off-grid in the showcase.
- **IV-03 Origin** - Origins sit on the floor plane (z=0) at the centre of the module footprint, except articulated parts (door leaf, valve wheel, beacon lantern) which pivot on their mechanical axis.
- **IV-04 Forward** - Forward is -Y. Long axis of linear modules runs X.
- **IV-05 Silhouette** - Heavy at the base, tapered upward. No element is wider at the top than at the bottom unless it is a bracket.
- **IV-06 Bevel** - Every silhouette edge that a viewer can see carries a 0.02 m chamfer. No infinitely sharp convex edges, no >0.05 m fillets on structural members.
- **IV-07 Segments** - Cylinders 16-24 segments, small fittings 12, lathe profiles never exceed 24 profile points.
- **IV-08 Colour** - Concrete + tile carry >= 70% of frame area. Painted steel 20-25%. Brass and ochre accents never exceed 5%.
- **IV-09 Wear** - Wear is directional and gravity-fed: damage at edges and corners first, salt crust at or below the waterline, rust streaks running downward from every fastener.
- **IV-10 Texel** - 256 texels/metre on architecture and terrain, 512 texels/metre on props, furniture, signage and hero assets.
- **IV-11 Materials** - An asset may only use material families from the 14_MATERIALS library. No asset-specific one-off materials.
- **IV-12 Density** - Foundation module <= 45k tris, variation <= 25k, detail <= 6k, hero <= 60k. Silhouette beats triangle count.
- **IV-13 Emissive** - Exactly two light colours exist: amber sodium (2000 K) and cyan brine. Nothing else emits.
- **IV-14 Naming** - WK_[CATEGORY]_[ASSET]_[VARIANT]_[NUMBER], upper case, no dots, no 'final', no 'copy'.

## Design language

### architectural_language

Tidal-industrial masonry. Segmental arch ribs spring from a 2.4 m corbel line; bays are square and repeated; everything is built from the same 4.0 m bay and the same 0.4 m wall. No curved plan geometry - curves exist only in section (arches, tanks, pipes).

### dominant_shapes_silhouettes

Square bay, segmental arch, octagonal column, cylinder (tank, pipe, barrel), and the tapering beacon. A silhouette test: if a piece reads as a box with a chamfered top edge, it belongs; if it reads as organic, it does not.

### shape_hierarchy

1) bay masses and the beacon tower, 2) arch ribs, columns, tanks, 3) beams, catwalks, stairs, pipes, 4) trim, brackets, fittings, 5) decals and salt. Higher levels are never decorated by lower ones.

### structural_logic

Load runs arch -> corbel -> column -> footing. Every bracket visibly bolts to something. Gussets are triangular and never ornamental.

### modular_dimensions

Bay 4.0 x 4.0 x 3.6 m, wall 0.4 m thick, slab 0.3 m thick, column 0.5 x 0.5 m, catwalk 1.2 m wide, rail 1.0 m high. One storey = 3.6 m = 20 risers of 0.18 m.

### proportions

Openings are narrow and tall (1.2 x 2.4 m doors, 1.6 x 1.4 m windows at a 1.2 m sill) because the wall is load-bearing. Wall-to-void ratio never exceeds 1:1 on any elevation.

### construction_logic

Cast in place first, bolted on later. Cast elements (concrete, tile) are monolithic; bolted elements (steel, brass, timber) are visibly attached with flanges, collars and gussets.

### material_families

Fourteen families: structural concrete, glazed ceramic tile, painted steel (teal), primer steel (oxide), aged steel, brass, timber, glass, brine water, emissive amber, emissive cyan, signage enamel, decal overlay, and a shared dirt/salt overlay used as a mask rather than a surface.

### surface_treatment

Concrete is board-formed with a 0.2 m board rhythm and blowholes. Tile is 0.2 m square with a 6 mm grout line. Painted steel shows a rolled grain. Nothing is smooth and nothing is noisy.

### wear_and_aging_logic

Three ageing agents, in order of strength: salt (crusts below the 1.6 m waterline, effloresces in corners), water (streaks down from every fastener and joint), and mechanical wear (paint fails on convex edges, primer shows through, never bare metal first).

### colour_hierarchy

Concrete and tile dominate (>= 70%). Brine-teal paint is the identifying secondary (20-25%). Red oxide is revealed substrate, never a design colour. Ochre and brass are accents under 5%.

### lighting_philosophy

Overcast cold sea daylight enters only through the arched openings on the seaward wall - it is the key light and it is always low and cool. Amber sodium fittings are the only interior sources. Cyan brine glow bounces up through floor gratings as fill. Shadows are soft; contrast comes from colour temperature, not from intensity.

### polygon_density_philosophy

Geometry is spent on silhouette, never on surface detail. Surface detail lives in the texture set. A foundation module stays under 45k tris; a hero under 60k; props under 6k.

### bevel_philosophy

0.02 m chamfer on every readable convex edge, two segments. Larger radii only where a human hand or a rope would touch (rail tops, hatch coamings) and never above 0.05 m.

### uv_philosophy

Box projection for cast members, cylindrical projection for lathed members, planar for decals. UVs are authored in tile units so that texel density is a property of the material family, not of the asset.

### texel_density_target

256 texels/m architecture and terrain, 512 texels/m props, furniture, signage, hero.

### prop_detail_hierarchy

Tier A props (barrel, valve) get a full lathe profile, real collars and a working pivot. Tier B props (crate, sack) are panel-built with chamfered edges. Nothing in Tier B gets a subdivision surface.

### signage_language

Vitreous enamel plates, white body, brine-teal lettering, two bolt holes top and bottom, always mounted on a wall or a post, never hanging free. Lettering is condensed sans capitals; hazard placards use an ochre field with a black triangle.

### environmental_storytelling_rules

- Every prop must answer 'who used this last, and why did they leave it?'
- Salt crust marks the historic high-water line and nothing else.
- A doorway that is used is worn; a doorway that is not used is crusted.
- Never place a prop that implies a person is currently present.

### repetition_rules

Architectural modules repeat freely - that is the point. Props never repeat adjacently: no two identical props within one bay, no three identical props within a 8 m radius, and no prop cluster with a regular spacing under 1.5 m.

### asymmetry_rules

The architecture is symmetric; the contents are not. Break bay symmetry by placing at least one off-grid prop, one damaged module and one signage plate per three bays.

### vegetation_logic

Only salt-tolerant growth: a low grey-green saltbush that colonises cracked slab and never grows taller than 0.6 m. It marks neglect, so it clusters at breaches and unused edges, never in circulation.

### terrain_language

The station stands on a concrete sea wall over open brine. Terrain is expressed as water plane, embankment rubble and rock armour - flat, horizontal, heavy. No hills, no organic landforms.

## Material families

| Family | Label | Tile (m) | Texels/m | Note |
|---|---|---|---|---|
| MK_CONCRETE_STRUCT | Structural Concrete | 4.0 | 256 | Board-formed mass concrete. The dominant family. |
| MK_CERAMIC_TILE | Salt-Glazed Ceramic Tile | 2.0 | 256 | 0.2 m squares, 6 mm grout, glaze pooling at edges. |
| MK_STEEL_PAINTED | Painted Steel - Brine Teal | 2.0 | 256 | Top coat over oxide primer; chips reveal primer, never bare metal. |
| MK_STEEL_PRIMER | Primer Steel - Red Oxide | 2.0 | 256 | Revealed substrate. Used for worn faces and hidden structure. |
| MK_STEEL_AGED | Aged Steel | 1.0 | 512 | Unpainted fittings, gratings, fasteners. Rusted at contact. |
| MK_BRASS | Patinated Brass | 0.5 | 512 | Accent metal. Verdigris in recesses only. |
| MK_TIMBER | Brine-Soaked Timber | 1.0 | 512 | Slats and packing only, always chamfered, always greyed. |
| MK_GLASS | Wired Glass | 1.0 | 512 | Arched window units. Slight green cast, salt-etched. |
| MK_WATER_BRINE | Brine Water | 4.0 | 256 | Stagnant, glowing, flat. Never animated in stills. |
| MK_EMISSIVE_AMBER | Emissive - Sodium Amber | 1.0 | 512 | 2000 K sodium. The only warm light in the world. |
| MK_EMISSIVE_CYAN | Emissive - Brine Cyan | 1.0 | 512 | Cherenkov-ish brine glow. Fill light only, never a key. |
| MK_SIGNAGE_ENAMEL | Vitreous Enamel Signage | 1.0 | 512 | Glossy enamel plate with chipped rim and two bolt holes. |
| MK_DECAL_OVERLAY | Decal Overlay | 4.0 | 256 | Alpha-blended storytelling sheets: waterline, cracks, salt, marks. |
| MK_DIRT_SALT | Dirt / Salt Overlay Mask | 4.0 | 256 | Shared weathering mask consumed by other families. |

## Lighting philosophy

Overcast cold sea daylight enters only through the arched openings on the seaward wall - it is the key light and it is always low and cool. Amber sodium fittings are the only interior sources. Cyan brine glow bounces up through floor gratings as fill. Shadows are soft; contrast comes from colour temperature, not from intensity.
