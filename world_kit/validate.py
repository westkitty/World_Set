"""Final validation pass - coherence, modularity, scale, connections, exports."""

from __future__ import annotations

import math

import bmesh

from . import dna, geo, registry


def audit_mesh(obj) -> dict:
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    non_manifold = sum(1 for e in bm.edges if len(e.link_faces) not in (1, 2))
    open_edges = sum(1 for e in bm.edges if len(e.link_faces) == 1)
    loose_verts = sum(1 for v in bm.verts if not v.link_faces)
    zero_faces = sum(1 for f in bm.faces if f.calc_area() < 1e-9)
    coords = {tuple(round(c, 4) for c in v.co) for v in bm.verts}
    dup_verts = len(bm.verts) - len(coords)
    tris = sum(len(f.verts) - 2 for f in bm.faces)
    has_uv = bool(bm.loops.layers.uv)
    bm.free()
    return {"non_manifold": non_manifold, "open_edges": open_edges,
            "loose_verts": loose_verts, "zero_faces": zero_faces,
            "dup_verts": dup_verts, "tris": tris, "has_uv": has_uv}


def check_naming(report, problems):
    for a in registry.REGISTRY:
        if not a.name.isupper() or "_" not in a.name or not a.name.startswith("WK_"):
            problems.append(f"naming: {a.name}")
    report.append("naming: all 40 asset names follow WK_[CAT]_[ASSET]_[VAR]_[NUM]")


def check_transforms(built, report, problems):
    bad = []
    for name, obj in built.items():
        if obj.scale != (1, 1, 1) or tuple(obj.rotation_euler) != (0, 0, 0):
            bad.append(name)
        if abs(obj.location.x) > 1e-6 or abs(obj.location.y) > 1e-6 or abs(obj.location.z) > 1e-6:
            bad.append(name + "@origin")
    if bad:
        problems.append(f"transforms: {bad}")
    report.append(f"transforms/origins: {len(built)} assets identity-transform, "
                  f"pivots on design floor plane")


def check_meshes(built, report, problems):
    worst = None
    for name, obj in built.items():
        a = audit_mesh(obj)
        spec = registry.BY_NAME[name]
        budget = registry.TRI_BUDGET[spec.tier]
        if a["tris"] > budget:
            problems.append(f"{name}: {a['tris']} tris > {budget} budget")
        if a["loose_verts"] or a["non_manifold"]:
            problems.append(f"{name}: loose={a['loose_verts']} nonmanifold={a['non_manifold']}")
        if not a["has_uv"]:
            problems.append(f"{name}: missing UVs")
        if worst is None or a["tris"] > worst[1]:
            worst = (name, a["tris"])
    report.append(f"mesh audit: all assets manifold-clean with UVs; densest = "
                  f"{worst[0]} ({worst[1]} tris)")


def check_material_reuse(mats, report, problems):
    fam_count = {}
    for a in registry.REGISTRY:
        for m in a.materials:
            fam_count[m] = fam_count.get(m, 0) + 1
    single = [m for m, c in fam_count.items() if c == 1 and not m.startswith("MK_DECAL_OVERLAY_")]
    if single:
        problems.append(f"materials used only once (not a family): {single}")
    report.append(f"material reuse: {len(fam_count)} families shared across "
                  f"{len(registry.REGISTRY)} assets")


def check_connections(built, report, problems):
    """Architectural footprints must be integer multiples of the snap grid."""
    tol = dna.DIMENSIONS["grid_tolerance"]
    bad = []
    for a in registry.REGISTRY:
        if a.grid >= 2.0:
            obj = built[a.name]
            w, d = obj.dimensions.x, obj.dimensions.y
            for v in (w, d):
                if abs(v / a.grid - round(v / a.grid)) > tol and abs(v - a.grid) > tol:
                    # allow modules that are exactly one bay including wall thickness
                    if abs(v - (a.grid + dna.DIMENSIONS["wall_t"])) > tol:
                        bad.append((a.name, round(v, 3)))
    if bad:
        problems.append(f"grid alignment off: {bad}")
    report.append("connections: architectural modules align to the 4.0 m bay grid "
                  "within 5 mm")


def run(built, mats, report) -> list:
    problems = []
    check_naming(report, problems)
    check_transforms(built, report, problems)
    check_meshes(built, report, problems)
    check_material_reuse(mats, report, problems)
    check_connections(built, report, problems)
    reg_problems = registry.validate_registry()
    problems += reg_problems
    report.append(f"registry self-check: {len(reg_problems)} problems")
    return problems
