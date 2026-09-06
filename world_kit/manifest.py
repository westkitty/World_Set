"""Documentation + manifest generation (all derived from the DNA / registry)."""

from __future__ import annotations

import csv
import json
import os

from . import dna, registry


def asset_records(built):
    recs = []
    for spec in registry.REGISTRY:
        obj = built.get(spec.name)
        dims = tuple(round(v, 2) for v in obj.dimensions) if obj else spec.size
        recs.append({
            "asset_name": spec.name,
            "category": spec.category,
            "tier": spec.tier,
            "purpose": spec.purpose,
            "dimensions_m": {"w": dims[0], "d": dims[1], "h": dims[2]},
            "material_family": list(spec.materials),
            "filename": f"{dna.CATEGORY_EXPORT_DIRS[spec.category]}/{spec.name}.glb",
            "snap_grid_m": spec.grid,
            "origin": spec.origin,
        })
    return recs


def write_manifest(built, out_dir, report):
    os.makedirs(out_dir, exist_ok=True)
    recs = asset_records(built)
    with open(os.path.join(out_dir, "asset_manifest.json"), "w") as f:
        json.dump({"kit": dna.KIT_ID, "name": dna.KIT_NAME, "assets": recs}, f, indent=2)
    with open(os.path.join(out_dir, "asset_manifest.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["asset_name", "category", "tier", "purpose",
                                          "material_family", "filename", "snap_grid_m"])
        w.writeheader()
        for r in recs:
            row = dict(r); row["material_family"] = "|".join(r["material_family"])
            row["dimensions_m"] = r["dimensions_m"]
            w.writerow({k: row[k] for k in w.fieldnames})
    md = ["# WORLD KIT - Asset Manifest", "",
          f"Kit: **{dna.KIT_ID}** - {dna.KIT_NAME}",
          f"Assets: {len(recs)}", ""]
    for cat in dict(dna.COLLECTIONS):
        rows = [r for r in recs if r["category"] == cat]
        if not rows:
            continue
        md += [f"## {cat}", "",
               "| Asset | Tier | Size (m) | Materials | File |",
               "|---|---|---|---|---|"]
        for r in rows:
            d = r["dimensions_m"]
            md.append(f"| {r['asset_name']} | {r['tier']} | "
                      f"{d['w']:.2f} x {d['d']:.2f} x {d['h']:.2f} | "
                      f"{', '.join(r['material_family'])} | `{r['filename']}` |")
        md.append("")
    with open(os.path.join(out_dir, "ASSET_MANIFEST.md"), "w") as f:
        f.write("\n".join(md))
    report.append(f"manifest written ({len(recs)} assets)")
    return recs


def write_world_dna(out_dir, report):
    d = dna.DIMENSIONS
    L = ["# WORLD DNA", "",
         f"**{dna.KIT_ID}** - {dna.KIT_NAME}", "",
         "## Concept", "", dna.CONCEPT["one_liner"], "",
         f"- Era: {dna.CONCEPT['era']}", f"- Climate: {dna.CONCEPT['climate']}",
         f"- Occupancy: {dna.CONCEPT['occupancy']}", "",
         "Narrative beats:"] + [f"- {b}" for b in dna.CONCEPT["narrative_beats"]] + ["",
         "## Modular grammar (metres)", "",
         "| Parameter | Value |", "|---|---|"] + \
        [f"| {k} | {v} |" for k, v in d.items()] + ["",
         "## Visual invariants", ""] + [f"- **{a} {b}** - {c}" for a, b, c in dna.INVARIANTS] + ["",
         "## Design language", ""]
    for k, v in dna.LANGUAGE.items():
        L.append(f"### {k}")
        L.append("")
        if isinstance(v, list):
            L += [f"- {x}" for x in v]
        else:
            L.append(v)
        L.append("")
    L += ["## Material families", "", "| Family | Label | Tile (m) | Texels/m | Note |",
          "|---|---|---|---|---|"]
    for k, f in dna.MATERIAL_FAMILIES.items():
        L.append(f"| {k} | {f['label']} | {f['tile_m']} | {f['texels_per_m']} | {f['note']} |")
    L += ["", "## Lighting philosophy", "", dna.LANGUAGE["lighting_philosophy"], ""]
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "WORLD_DNA.md"), "w") as f:
        f.write("\n".join(L))
    report.append("WORLD_DNA.md written")


def write_validation(out_dir, report, problems, ):
    os.makedirs(out_dir, exist_ok=True)
    L = ["# WORLD KIT - Validation Report", "",
         f"Kit: {dna.KIT_ID}", "", "## Checks", ""] + [f"- {r}" for r in report] + \
        ["", "## Problems", ""]
    if problems:
        L += [f"- {p}" for p in problems]
    else:
        L.append("- none - all validation checks passed")
    with open(os.path.join(out_dir, "VALIDATION_REPORT.md"), "w") as f:
        f.write("\n".join(L))
    return len(problems) == 0
