# WORLD DNA SPECIFICATION
## SYSTEM: WORLD KIT — "SITE-44 SUB-AQUIFER RESEARCH COMPLEX"
**Document Version:** 1.0.0  
**Status:** Canonical Source of Truth  
**Target Engine/Platform:** Blender 4.5+ / Real-time PBR (GLTF/GLB 2.0)

---

### 1. Architectural Language
* **Style:** Monolithic Brutalist Retro-Industrial Subterranean.
* **Core Influences:** Late-20th-century heavy civil hydro-engineering, deep-crust subterranean containment facilities, Soviet/Eastern Bloc seismic monitoring bunkers, and retro-speculative sci-fi (analog instruments, thick hydraulic bulkheads, exposed conduit arteries).
* **Atmospheric Tone:** Claustrophobic yet grand; utilitarian, imposing, over-engineered against immense lithostatic and hydrostatic pressures.

---

### 2. Dominant Shapes & Silhouettes
* **Primary Silhouettes:** Heavy rectangular and chamfered trapezoidal forms. Walls taper inward slightly at structural collars; doorways feature prominent 45° chamfered upper corners to distribute shear stress.
* **Secondary Silhouettes:** Cylindrical pressure vessels, longitudinal pipe conduits running along designated architectural datums, and heavy I-beam structural ribs with triangular gusset reinforcement plates.
* **Silhouette Hierarchy:**
  1. *Tertiary (Micro):* Hex bolts, pressure dial bezels, toggle switch plates, conduit bracket clamps, weld seams (2mm – 10cm).
  2. *Secondary (Meso):* Door frames, column footings, cable trays, structural stiffener ribs, recessed equipment alcoves (15cm – 1.0m).
  3. *Primary (Macro):* Massive cast wall slabs, 4m x 4m load-bearing arches, 0.8m thick structural pillars, cavernous double-height ceiling trusses (1.0m – 8.0m+).

---

### 3. Structural Logic & Construction Grammar
* **Load-Bearing Law:** Every vertical span must terminate in a visually convincing load-bearing element. Ceilings rest on heavy I-beams; I-beams rest on column brackets or reinforced wall piers; columns anchor into floor slabs via bolted gusset footings.
* **Pressure Resistance:** No large, unsupported flat glass spans. All observation ports are inset, circular or chamfered octagonal, reinforced by exterior brass tension studs and internal diamond-wire mesh.
* **Utility Routing:** Utilities never cross open walking spaces arbitrarily. Electrical lines, pneumatic hoses, and coolant pipes are strictly channeled through:
  * Wall-to-floor baseboard raceways ($y = 0.0\text{m} - 0.2\text{m}$).
  * Overhead horizontal conduit raceways at the standard $3.2\text{m}$ datum line.
  * Ceiling truss cable trays ($y = 3.8\text{m} - 4.2\text{m}$).

---

### 4. Modular Dimensions & Metric Grid
* **Primary Module:** $4.0\text{m} \times 4.0\text{m}$ (Standard wall width, floor tile span, ceiling coffer width).
* **Half Module:** $2.0\text{m} \times 4.0\text{m}$ (Stairs, narrow walkways, catwalk bays, portal walls).
* **Vertical Grid:**
  * Base Floor Height: $4.0\text{m}$ floor-to-ceiling clearance.
  * Double Height Bay: $8.0\text{m}$ for industrial reactor chambers and cistern reservoirs.
  * Intermediate Platform: $2.0\text{m}$ elevation step (stairs precisely match $\Delta Z = 2.0\text{m}$, $\Delta Y = 4.0\text{m}$).
* **Sub-Grid:** $0.5\text{m}$ and $0.25\text{m}$ for equipment alcoves, column footprints, and conduit brackets.
* **Wall Thickness:** Exactly $0.25\text{m}$ standard ($0.125\text{m}$ half-thickness from center line).
* **Clearance Standards:**
  * Standard Bulkhead Door Rough Opening: $2.0\text{m} \text{ wide} \times 2.5\text{m} \text{ high}$.
  * Catwalk Walkway Width: $1.8\text{m}$ clear between safety handrails.
  * Stair Tread: $0.25\text{m}$ run $\times$ $0.20\text{m}$ rise (10 risers per 2m tier).
* **Human Reference Scale:** $1.8\text{m}$ adult human reference; handrails at $1.1\text{m}$ height; consoles centered at $1.0\text{m}$ work plane with eye-level monitors at $1.4\text{m} - 1.6\text{m}$.

---

### 5. Material Families & Surface Response
All assets draw strictly from 7 coherent PBR material families:

1. **`MAT_Concrete_Brutalist` (Macro Architectural Structural):**
   * *Base Color:* Weathered slate grey `#525659` with subtle aggregate grain and damp water-staining gradients near floor joints.
   * *Roughness:* $0.78 - 0.92$, low specular ($0.35$), non-metallic ($0.0$).
   * *Normal/Bump:* Board-formed wood grain texture and micro-pitted concrete pore noise.
2. **`MAT_Heavy_Steel_Painted` (Structural Framing & Bulkheads):**
   * *Base Color:* Industrial oxidized olive drab `#3B4239` or safety slate `#2F363F`.
   * *Roughness:* $0.45 - 0.65$ base coat, jumping to $0.85$ at chipped edges where raw oxidized steel is exposed.
   * *Metallic:* $0.0$ on paint, $0.95$ on chipped edge cavities.
3. **`MAT_Galvanized_Grate` (Catwalks, Stairs & Decks):**
   * *Base Color:* Aged zinc / galvanized iron `#6B7277` with localized oil drops and chemical tarnishing.
   * *Roughness:* $0.38 - 0.55$, metallic $0.88$, high anisotropic micro-scratching.
4. **`MAT_Reinforced_Glass` (Observation Portals):**
   * *Base Color:* Deep sea green tint `#1A3330`, transmission $0.85$.
   * *Roughness:* $0.12$ surface polish with internal diamond wire mesh lattice embedment.
5. **`MAT_Rubber_Conduit` (Cables, Gaskets & Shock Mounts):**
   * *Base Color:* Carbon matte black `#1E1F21`.
   * *Roughness:* $0.60 - 0.75$, metallic $0.0$, subtle ribbing normal map.
6. **`MAT_Emissive_Cyan_UI` (Diagnostic Displays & Indicator Strips):**
   * *Base Color:* Phosphor cyan `#1BE7FF` or warning amber `#FF9F1C`.
   * *Emission Strength:* $4.0 - 8.0\,\text{W/sr/m}^2$, with raster scanline modulation.
7. **`MAT_Hazard_Stripes` (Thresholds & Pinch Points):**
   * *Base Color:* High-visibility yellow `#F5B700` and charcoal black `#1C1C1E` in 45° diagonal chevron bands.
   * *Roughness:* $0.65$ with heavy abrasion and scuffing in walking lanes.

---

### 6. Wear, Aging & Environmental History
* **Facility Age:** Active continuous service for 35+ years in a high-humidity subterranean geothermal aquifer zone.
* **Wear Logic:**
  * *Bottom-Up Grime:* Floor edges, column bases, and wall corners accumulate dark mineral residue and moisture staining ($Z < 0.4\text{m}$).
  * *Edge Chipping:* High-contact mechanical corners (stair nosings, door frames, console edges) show chipped paint reveals down to raw oxidized primer.
  * *Top-Down Dust/Condensation:* Ceilings and upper pipe crowns collect dry industrial dust and thermal condensation trails.

---

### 7. Lighting Philosophy
* **Atmospheric Scheme:** High-contrast, moody, pragmatic, non-decorative. Subterranean deep facility with zero external sunlight.
* **Color Temperature Hierarchy:**
  * *Primary Ambient / Fill:* Subdued cool industrial cyan/slate-blue ($4500\text{K} - 6500\text{K}$, low fill intensity) creating cavernous depth.
  * *Functional Task Worklights:* Warm tungsten ($2700\text{K} - 3200\text{K}$) over workbenches, stairwell landings, and equipment consoles.
  * *Emergency / Hazard Indicators:* Pure monochromatic amber ($590\text{nm}$) and alarm crimson ($630\text{nm}$) on bulkheads and reactors.
* **Contrast & Falloff:** Crisp shadows, volumetric moisture haze capturing light beams through grated walkways, highlighting structural silhouettes.

---

### 8. Geometric Density, Bevel & UV Philosophy
* **Polygon Density Philosophy:** Real-time production efficiency with silhouette fidelity. Structural panels range from $800 - 4,000$ triangles; intricate hero units up to $15,000 - 25,000$ triangles. Zero waste on flat planar interiors.
* **Bevel Philosophy:** Unbroken sharp $90^\circ$ computer edges are strictly forbidden. All structural corners feature a $15\text{mm} - 30\text{mm}$ weighted normal bevel (2-segment or weighted profile) to catch specular highlights.
* **UV & Texel Density:** Standardized to $512\,\text{px/meter}$ target texel density across all modular assets to ensure uniform visual resolution when placed side-by-side.

---

### 9. Signage & Environmental Typography
* **Typography:** Utilitarian, bold grotesque sans-serif (DIN 1451 / Helvetica Bold / Soviet GOST style).
* **Format:** Monochromatic stencil lettering stamped on steel plates, or backlit rectangular acrylic sector signs with hazard stripes and alphanumeric sector designations (`"SECTOR 04"`, `"SUB-AQUIFER VALVE STATION"`, `"HIGH PRESSURE HAZARD"`).

---

### 10. Visual Invariants (The Unbreakable Rules)
Every asset in the WORLD KIT must adhere to these 6 immutable laws:
1. **Grid Snap Compatibility:** Every structural piece must snap to the $4.0\text{m}$, $2.0\text{m}$, or $0.5\text{m}$ grid with origin points at bottom-center or modular edge anchors.
2. **Standard Conduit Datum:** Horizontal wall utilities must align continuously across adjacent modules at $Z = 3.2\text{m} \pm 0.05\text{m}$.
3. **No Stylistic Drift:** No whimsical fantasy elements, no sleek glass-curtain high-tech, no futuristic floating lights. Everything is bolted, welded, hydro-tested, and functional.
4. **Material Uniformity:** All assets must use the 7 canonical material families; no rogue one-off ad-hoc shaders.
5. **Beveled Specular Edges:** Every silhouette corner must catch light via controlled chamfers or bevels.
6. **Engine-Ready Transforms:** Scale must always be applied to `(1.0, 1.0, 1.0)`, rotations cleared to canonical orientation, and geometry verified manifold with outward normals.
