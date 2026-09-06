"""Geometry toolkit.

Everything in the kit is authored with this module: a small set of primitive
builders (box, prism, cylinder, lathe, sweep, ring, plane, text) operating on
bmesh, plus the :class:`Asset` builder that owns part objects, booleans, UVs,
shading, origins and cleanup.

Design rules enforced here
--------------------------
* an asset is one mesh object with one material slot per family used
* geometry is authored in local space with the object transform at identity,
  so local == world and texel density is predictable
* shading is decided per face from dihedral angles (no auto-smooth modifier,
  so nothing depends on Blender version behaviour)
* UVs are authored in tile units: ``uv = local_coord / tile_m``
"""

from __future__ import annotations

import math

import bmesh
import bpy
from mathutils import Matrix, Vector

TWO_PI = math.pi * 2
EPS = 1e-5


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #
def vec(x, y=None, z=None):
    if y is None:
        return Vector(x)
    return Vector((x, y, z))


def rot_matrix(rx=0.0, ry=0.0, rz=0.0, center=None) -> Matrix:
    m = Matrix.Rotation(rz, 4, "Z") @ Matrix.Rotation(ry, 4, "Y") @ Matrix.Rotation(rx, 4, "X")
    if center is None:
        return m
    c = vec(center)
    return Matrix.Translation(c) @ m @ Matrix.Translation(-c)


def frame_for(direction: Vector):
    """Right-handed frame (right, up, axis) for extruding along *direction*."""
    d = direction.normalized()
    ref = Vector((0, 0, 1)) if abs(d.dot(Vector((0, 0, 1)))) < 0.99 else Vector((1, 0, 0))
    right = ref.cross(d).normalized()
    up = d.cross(right).normalized()
    return right, up, d


def axis_vector(axis: str) -> Vector:
    return {"X": Vector((1, 0, 0)), "Y": Vector((0, 1, 0)), "Z": Vector((0, 0, 1))}[axis.upper()]


def _add_face(bm, verts, mat):
    try:
        f = bm.faces.new(verts)
    except ValueError:
        return None
    f.material_index = mat
    return f


def _quad_ring(bm, lower, upper, mat, wrap=True, flip=False):
    n = len(lower)
    idx = range(n) if wrap else range(n - 1)
    for i in idx:
        j = (i + 1) % n
        quad = [lower[i], lower[j], upper[j], upper[i]]
        if flip:
            quad.reverse()
        _add_face(bm, quad, mat)


def _fan(bm, ring, center, mat, flip=False):
    n = len(ring)
    for i in range(n):
        j = (i + 1) % n
        tri = [center, ring[i], ring[j]]
        if flip:
            tri.reverse()
        _add_face(bm, tri, mat)


# --------------------------------------------------------------------------- #
# primitives (all operate on a bmesh, all take a material index)
# --------------------------------------------------------------------------- #
def box(bm, center, size, rot=None, mat=0):
    cx, cy, cz = center
    sx, sy, sz = [s / 2.0 for s in size]
    pts = [(-sx, -sy, -sz), (sx, -sy, -sz), (sx, sy, -sz), (-sx, sy, -sz),
           (-sx, -sy, sz), (sx, -sy, sz), (sx, sy, sz), (-sx, sy, sz)]
    m = rot_matrix(*rot, center=center) if rot else None
    vs = []
    for p in pts:
        v = vec(p) + vec((cx, cy, cz))
        if m:
            v = m @ v
        vs.append(bm.verts.new(v))
    bm.verts.ensure_lookup_table()
    quads = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5),
             (2, 3, 7, 6), (3, 0, 4, 7)]
    for q in quads:
        _add_face(bm, [vs[i] for i in q], mat)
    return vs


def tapered_box(bm, base_center, base_size, top_size, height, rot=None, mat=0):
    """Box whose top face can be a different size (tapered piers, corbels)."""
    cx, cy, cz = base_center
    b = [s / 2.0 for s in base_size]
    t = [s / 2.0 for s in top_size]
    lo = [(-b[0], -b[1], 0), (b[0], -b[1], 0), (b[0], b[1], 0), (-b[0], b[1], 0)]
    hi = [(-t[0], -t[1], height), (t[0], -t[1], height), (t[0], t[1], height), (-t[0], t[1], height)]
    m = rot_matrix(*rot, center=base_center) if rot else None
    lo_v = [bm.verts.new((m @ (vec(p) + vec((cx, cy, cz)))) if m else (vec(p) + vec((cx, cy, cz)))) for p in lo]
    hi_v = [bm.verts.new((m @ (vec(p) + vec((cx, cy, cz)))) if m else (vec(p) + vec((cx, cy, cz)))) for p in hi]
    _quad_ring(bm, lo_v, hi_v, mat)
    _add_face(bm, [lo_v[0], lo_v[1], lo_v[2], lo_v[3]], mat)
    _add_face(bm, [hi_v[3], hi_v[2], hi_v[1], hi_v[0]], mat)
    return lo_v + hi_v


def cyl(bm, loc, r0, r1, depth, axis="Z", seg=20, mat=0, cap=True, rot_offset=0.0):
    """Tapered cylinder.  r0 at the negative end of *axis*, r1 at the positive."""
    a = axis_vector(axis)
    right, up, _ = frame_for(a)
    o = vec(loc)
    lo, hi = [], []
    for i in range(seg):
        th = rot_offset + TWO_PI * i / seg
        d = right * math.cos(th) + up * math.sin(th)
        lo.append(bm.verts.new(o + d * r0))
        hi.append(bm.verts.new(o + a * depth + d * r1))
    _quad_ring(bm, lo, hi, mat)
    if cap:
        if r0 > EPS:
            _fan(bm, lo, bm.verts.new(o), mat, flip=True)
        if r1 > EPS:
            _fan(bm, hi, bm.verts.new(o + a * depth), mat, flip=False)
    return lo + hi


def lathe(bm, profile, loc, axis="Z", seg=24, mat=0, rot_offset=0.0):
    """Revolve a (radius, height) profile around *axis* through *loc*.

    The profile is an open polyline from the axis outward; ends whose radius is
    greater than EPS are automatically capped so the result is a closed solid.
    """
    a = axis_vector(axis)
    right, up, _ = frame_for(a)
    o = vec(loc)
    rings = []
    for radius, h in profile:
        ring = []
        for i in range(seg):
            th = rot_offset + TWO_PI * i / seg
            d = right * math.cos(th) + up * math.sin(th)
            ring.append(bm.verts.new(o + a * h + d * radius))
        rings.append(ring)
    for i in range(len(rings) - 1):
        _quad_ring(bm, rings[i], rings[i + 1], mat)
    r_first, _ = profile[0]
    r_last, h_last = profile[-1]
    if r_first > EPS:
        _fan(bm, rings[0], bm.verts.new(o + a * profile[0][1]), mat, flip=True)
    if r_last > EPS:
        _fan(bm, rings[-1], bm.verts.new(o + a * h_last), mat, flip=False)
    return [v for ring in rings for v in ring]


def ring(bm, loc, r_out, r_in, depth, axis="Z", seg=24, mat=0, rot_offset=0.0):
    """Hollow tube / collar."""
    profile = [(r_in, 0.0), (r_out, 0.0), (r_out, depth), (r_in, depth), (r_in, 0.0)]
    return lathe(bm, profile, loc, axis=axis, seg=seg, mat=mat, rot_offset=rot_offset)


def prism(bm, profile, origin, direction, mat=0, close=True):
    """Extrude a 2D profile along *direction*.  Profile points are (u, v)."""
    right, up, d = frame_for(direction)
    o = vec(origin)
    dlen = direction.length
    d = d.normalized()
    lo, hi = [], []
    for u, v in profile:
        p = o + right * u + up * v
        lo.append(bm.verts.new(p))
        hi.append(bm.verts.new(p + d * dlen))
    _quad_ring(bm, lo, hi, mat, wrap=False)
    if close:
        _add_face(bm, list(reversed(lo)), mat)
        _add_face(bm, hi, mat)
    return lo + hi


def sweep(bm, path, profile, mat=0, close_ends=True):
    """Sweep a 2D profile along a polyline using parallel transport frames."""
    path = [vec(p) for p in path]
    rings = []
    prev_t = None
    right = None
    up = None
    for i, p in enumerate(path):
        if i == 0:
            t = (path[1] - p).normalized()
        elif i == len(path) - 1:
            t = (p - path[i - 1]).normalized()
        else:
            t = (path[i + 1] - path[i - 1]).normalized()
        if prev_t is None:
            right, up, _ = frame_for(t)
        else:
            # rotate the previous frame towards the new tangent
            b = prev_t.cross(t)
            s = b.length
            c = prev_t.dot(t)
            if s > EPS:
                axis = b.normalized()
                ang = math.atan2(s, c)
                m = Matrix.Rotation(ang, 4, axis)
                right = (m @ right).normalized()
                up = (m @ up).normalized()
        ring = [bm.verts.new(p + right * u + up * v) for u, v in profile]
        rings.append(ring)
        prev_t = t
    for i in range(len(rings) - 1):
        _quad_ring(bm, rings[i], rings[i + 1], mat, wrap=False)
    if close_ends:
        _add_face(bm, list(reversed(rings[0])), mat)
        _add_face(bm, rings[-1], mat)
    return [v for r in rings for v in r]


def plane(bm, center, size_x, size_y, normal="Z", mat=0, seg=1):
    """Flat sheet in the plane whose normal is *normal*, subdivided *seg* times."""
    a = axis_vector(normal)
    right, up, _ = frame_for(a)
    o = vec(center)
    grid = []
    for j in range(seg + 1):
        row = []
        for i in range(seg + 1):
            u = -size_x / 2.0 + size_x * i / seg
            v = -size_y / 2.0 + size_y * j / seg
            row.append(bm.verts.new(o + right * u + up * v))
        grid.append(row)
    for j in range(seg):
        for i in range(seg):
            _add_face(bm, [grid[j][i], grid[j + 1][i], grid[j + 1][i + 1], grid[j][i + 1]], mat)
    return [v for r in grid for v in r]


def arc_profile(cx, cy, r, a0, a1, steps, thickness=0.0, inset=0.0):
    """2D arc polyline (optionally the inner line of a thick arc)."""
    pts = []
    for i in range(steps + 1):
        a = a0 + (a1 - a0) * i / steps
        rr = r - inset
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def text_mesh(bm_target, text, size=0.1, depth=0.012, center=(0, 0, 0),
              normal="Z", mat=0, align="CENTER"):
    """Build extruded lettering into *bm_target* using Blender's bundled font."""
    cu = bpy.data.curves.new(".wk_text", "FONT")
    cu.body = text
    cu.size = size
    cu.align_x = align
    cu.align_y = "CENTER"
    cu.extrude = depth / 2.0
    cu.offset = 0.0
    tmp = bpy.data.objects.new(".wk_text", cu)
    bpy.context.scene.collection.objects.link(tmp)
    dg = bpy.context.evaluated_depsgraph_get()
    me = tmp.evaluated_get(dg).to_mesh()
    src = bmesh.new()
    src.from_mesh(me)
    tmp.evaluated_get(dg).to_mesh_clear()
    bpy.data.objects.remove(tmp, do_unlink=True)
    bpy.data.curves.remove(cu)

    # text is authored in XY facing +Z reading +X; rotate to the requested normal
    n = normal.upper()
    rot = {
        "Z": Matrix.Identity(4),
        "-Z": Matrix.Rotation(math.pi, 4, "X"),
        "-Y": Matrix.Rotation(math.pi / 2.0, 4, "X"),   # readable from -Y
        "Y": Matrix.Rotation(-math.pi / 2.0, 4, "X") @ Matrix.Rotation(math.pi, 4, "Z"),
        "X": Matrix.Rotation(math.pi / 2.0, 4, "Y") @ Matrix.Rotation(-math.pi / 2.0, 4, "X"),
        "-X": Matrix.Rotation(-math.pi / 2.0, 4, "Y") @ Matrix.Rotation(math.pi / 2.0, 4, "X"),
    }[n]
    m = Matrix.Translation(vec(center)) @ rot
    bmesh.ops.transform(src, matrix=m, verts=src.verts[:])
    for f in src.faces:
        f.material_index = mat
    for v in src.verts:
        bm_target.verts.new(v.co)
    bm_target.verts.ensure_lookup_table()
    base = len(bm_target.verts) - len(src.verts)
    newv = bm_target.verts[base:]
    for f in src.faces:
        try:
            nf = bm_target.faces.new([newv[v.index] for v in f.verts])
            nf.material_index = mat
        except ValueError:
            pass
    src.free()


# --------------------------------------------------------------------------- #
# shading, UV, cleanup
# --------------------------------------------------------------------------- #
def auto_shade(bm, angle_deg=42.0, force_flat=False):
    """Per-face smooth flags derived from dihedral angles.

    A face is smoothed only when every one of its boundary edges is a gentle
    crease, so cylinders read as curved while boxes, caps and chamfers stay
    hard.  No modifier and no auto-smooth setting is required.
    """
    limit = math.radians(angle_deg)
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()
    if force_flat:
        for f in bm.faces:
            f.smooth = False
        return
    sharp = set()
    for e in bm.edges:
        if len(e.link_faces) == 2:
            ang = e.calc_face_angle()
            if ang > limit:
                sharp.add(e.index)
        elif len(e.link_faces) != 2:
            sharp.add(e.index)
    for f in bm.faces:
        f.smooth = not any(e.index in sharp for e in f.edges)
        for e in f.edges:
            if e.index in sharp:
                e.smooth = False


def chamfer_convex(bm, width, min_angle_deg=35.0, seg=1):
    """Chamfer convex edges sharper than *min_angle_deg* (INVARIANT IV-06)."""
    if width <= 0:
        return
    limit = math.radians(min_angle_deg)
    bm.edges.ensure_lookup_table()
    targets = []
    for e in bm.edges:
        if len(e.link_faces) != 2:
            continue
        try:
            ang = abs(e.calc_face_angle())
        except ValueError:
            continue
        if ang > limit:
            targets.append(e)
    if not targets:
        return
    bmesh.ops.bevel(bm, geom=targets, offset=width, offset_type="OFFSET",
                    segments=seg, profile=0.5, affect="EDGES",
                    clamp_overlap=True)


def _dominant_axis(normal: Vector) -> str:
    ax, ay, az = abs(normal.x), abs(normal.y), abs(normal.z)
    if az >= ax and az >= ay:
        return "Z"
    if ax >= ay:
        return "X"
    return "Y"


def uv_box(bm, tile_m, uv_name="UVMap"):
    """Box projection with texel density locked to *tile_m* metres per tile."""
    uv = bm.loops.layers.uv.get(uv_name) or bm.loops.layers.uv.new(uv_name)
    for f in bm.faces:
        n = f.normal
        ax = _dominant_axis(n)
        for loop in f.loops:
            co = loop.vert.co
            if ax == "Z":
                u, v = co.x, co.y
            elif ax == "X":
                u, v = co.y, co.z
            else:
                u, v = co.x, co.z
            loop[uv].uv = (u / tile_m, v / tile_m)


def uv_cyl(bm, tile_m, axis="Z", center=(0, 0, 0), uv_name="UVMap"):
    """Cylindrical projection; u is arc length so texel density is constant."""
    uv = bm.loops.layers.uv.get(uv_name) or bm.loops.layers.uv.new(uv_name)
    c = vec(center)
    a = axis_vector(axis)
    for f in bm.faces:
        for loop in f.loops:
            d = loop.vert.co - c
            if a == Vector((0, 0, 1)):
                ang = math.atan2(d.y, d.x)
                rad = math.hypot(d.x, d.y)
                height = d.z
            elif a == Vector((1, 0, 0)):
                ang = math.atan2(d.z, d.y)
                rad = math.hypot(d.y, d.z)
                height = d.x
            else:
                ang = math.atan2(d.x, d.z)
                rad = math.hypot(d.x, d.z)
                height = d.y
            loop[uv].uv = (ang * rad / tile_m, height / tile_m)


def uv_planar(bm, tile_m, normal="Z", uv_name="UVMap"):
    uv = bm.loops.layers.uv.get(uv_name) or bm.loops.layers.uv.new(uv_name)
    a = axis_vector(normal)
    right, up, _ = frame_for(a)
    for f in bm.faces:
        for loop in f.loops:
            co = loop.vert.co
            loop[uv].uv = (co.dot(right) / tile_m, co.dot(up) / tile_m)


def uv_sheet(bm, uv_name="UVMap"):
    """Map the part's bounding box to the 0..1 UV square (decals / sheets)."""
    uv = bm.loops.layers.uv.get(uv_name) or bm.loops.layers.uv.new(uv_name)
    xs = [v.co.x for v in bm.verts]; ys = [v.co.y for v in bm.verts]; zs = [v.co.z for v in bm.verts]
    mnx, mxx = min(xs), max(xs); mny, mxy = min(ys), max(ys); mnz, mxz = min(zs), max(zs)
    dx = max(1e-6, mxx - mnx); dy = max(1e-6, mxy - mny); dz = max(1e-6, mxz - mnz)
    horiz = dx >= dy and dx >= dz      # sheet lies in a vertical X-facing or Z-facing plane
    for f in bm.faces:
        for loop in f.loops:
            co = loop.vert.co
            if dz >= dx and dz >= dy:            # horizontal sheet
                u, v = (co.x - mnx) / dx, (co.y - mny) / dy
            elif dx >= dy:                       # vertical sheet facing Y
                u, v = (co.x - mnx) / dx, (co.z - mnz) / dz
            else:                                # vertical sheet facing X
                u, v = (co.y - mny) / dy, (co.z - mnz) / dz
            loop[uv].uv = (u, v)


def dedupe(bm, dist=1e-5):
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=dist)


def delete_loose(bm, dist=1e-5):
    loose = [v for v in bm.verts if not v.link_faces]
    if loose:
        bmesh.ops.delete(bm, geom=loose, context="VERTS")
    edges = [e for e in bm.edges if not e.link_faces]
    if edges:
        bmesh.ops.delete(bm, geom=edges, context="EDGES")


# --------------------------------------------------------------------------- #
# the asset builder
# --------------------------------------------------------------------------- #
class Part:
    """One sub-mesh of an asset, with exactly one material family."""

    def __init__(self, name, mat_key, uv_mode="box", uv_axis="Z", uv_center=(0, 0, 0)):
        self.name = name
        self.mat_key = mat_key
        self.uv_mode = uv_mode
        self.uv_axis = uv_axis
        self.uv_center = uv_center
        self.bm = bmesh.new()
        self.obj = None

    # convenience proxies so builders read naturally
    def box(self, center, size, rot=None):
        return box(self.bm, center, size, rot=rot, mat=0)

    def tapered_box(self, base_center, base_size, top_size, height, rot=None):
        return tapered_box(self.bm, base_center, base_size, top_size, height, rot=rot, mat=0)

    def cyl(self, loc, r0, r1, depth, axis="Z", seg=20, cap=True, rot_offset=0.0):
        return cyl(self.bm, loc, r0, r1, depth, axis=axis, seg=seg, mat=0,
                   cap=cap, rot_offset=rot_offset)

    def lathe(self, profile, loc, axis="Z", seg=24, rot_offset=0.0):
        return lathe(self.bm, profile, loc, axis=axis, seg=seg, mat=0, rot_offset=rot_offset)

    def ring(self, loc, r_out, r_in, depth, axis="Z", seg=24, rot_offset=0.0):
        return ring(self.bm, loc, r_out, r_in, depth, axis=axis, seg=seg, mat=0,
                    rot_offset=rot_offset)

    def prism(self, profile, origin, direction, close=True):
        return prism(self.bm, profile, origin, direction, mat=0, close=close)

    def sweep(self, path, profile, close_ends=True):
        return sweep(self.bm, path, profile, mat=0, close_ends=close_ends)

    def plane(self, center, size_x, size_y, normal="Z", seg=1):
        return plane(self.bm, center, size_x, size_y, normal=normal, mat=0, seg=seg)

    def text(self, text, size=0.1, depth=0.012, center=(0, 0, 0), normal="Z", align="CENTER"):
        return text_mesh(self.bm, text, size=size, depth=depth, center=center,
                         normal=normal, mat=0, align=align)

    @property
    def tris(self):
        return sum(len(f.verts) - 2 for f in self.bm.faces)


class Asset:
    """Builds one reusable kit asset and registers it with the library."""

    def __init__(self, name, spec, materials, tmp_collection, uv_default="box"):
        self.name = name
        self.spec = spec
        self.materials = materials          # mat_key -> bpy.types.Material
        self.tmp = tmp_collection
        self.parts: dict[str, Part] = {}
        self._uv_default = uv_default
        self.obj = None
        self.origin = None

    # ---- construction -----------------------------------------------------
    def part(self, key, mat_key, uv_mode=None, uv_axis="Z", uv_center=(0, 0, 0)):
        if mat_key not in self.materials:
            raise KeyError(f"{self.name}: material family {mat_key!r} is not in the kit")
        p = Part(key, mat_key, uv_mode or self._uv_default, uv_axis, uv_center)
        self.parts[key] = p
        return p

    def get(self, key):
        return self.parts[key]

    def material_slots(self):
        """Deterministic slot order: the order the parts were created."""
        out = []
        for p in self.parts.values():
            if p.mat_key not in out:
                out.append(p.mat_key)
        return out

    # ---- booleans ---------------------------------------------------------
    def cutter(self, name, build_fn):
        """Make a temporary cutter object by running *build_fn(part)*."""
        p = Part(name, "_CUTTER")
        build_fn(p)
        me = bpy.data.meshes.new(name)
        p.bm.to_mesh(me)
        p.bm.free()
        obj = bpy.data.objects.new(name, me)
        self.tmp.objects.link(obj)
        return obj

    def boolean(self, part_key, cutter_obj, operation="DIFFERENCE"):
        obj = self._ensure_object(part_key)
        mod = obj.modifiers.new("wk_bool", "BOOLEAN")
        mod.operation = operation
        mod.object = cutter_obj
        mod.solver = "EXACT"
        self._apply_modifiers(obj)
        bpy.data.objects.remove(cutter_obj, do_unlink=True)

    # ---- internal ---------------------------------------------------------
    def _ensure_object(self, key):
        """Promote a part's bmesh to a real object (needed before a boolean)."""
        p = self.parts[key]
        if p.obj is None:
            me = bpy.data.meshes.new(f".{self.name}_{key}")
            p.bm.to_mesh(me)
            p.bm.free()
            p.bm = None
            obj = bpy.data.objects.new(f".{self.name}_{key}", me)
            obj.data.materials.append(self.materials[p.mat_key])
            self.tmp.objects.link(obj)
            p.obj = obj
        return p.obj

    @staticmethod
    def _apply_modifiers(obj):
        prev = bpy.context.view_layer.objects.active
        bpy.context.view_layer.objects.active = obj
        for m in list(obj.modifiers):
            bpy.ops.object.modifier_apply(modifier=m.name)
        bpy.context.view_layer.objects.active = prev

    # ---- finalise ---------------------------------------------------------
    def finalize(self, bevel=0.02, shade_angle=42.0, origin=None,
                 keep_sharp_parts=(), weld=True):
        """Clean, UV, shade, join and register the asset object.

        ``origin`` defaults to the horizontal centre of the footprint at its
        lowest point (INVARIANT IV-03); a builder may pin a mechanical pivot by
        setting ``asset.origin``.
        """
        if not self.parts:
            raise RuntimeError(f"{self.name}: asset has no geometry")

        # 1. clean / bevel / uv / shade every part, then materialise it
        for key, p in list(self.parts.items()):
            if p.obj is not None:                    # promoted earlier (boolean)
                bm = bmesh.new()
                bm.from_mesh(p.obj.data)
            elif p.bm is not None and len(p.bm.verts):
                bm = p.bm
            else:
                continue
            if not len(bm.verts):
                bm.free()
                continue

            if bevel > 0 and key not in keep_sharp_parts:
                dedupe(bm, 1e-5)
                chamfer_convex(bm, bevel)
            delete_loose(bm)
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
            tile_m = self.materials[p.mat_key]["wk_tile_m"]
            if p.uv_mode == "box":
                uv_box(bm, tile_m)
            elif p.uv_mode == "cyl":
                uv_cyl(bm, tile_m, axis=p.uv_axis, center=p.uv_center)
            elif p.uv_mode == "planar":
                uv_planar(bm, tile_m, normal=p.uv_axis)
            elif p.uv_mode == "sheet":
                uv_sheet(bm)
            auto_shade(bm, shade_angle,
                       force_flat=(p.mat_key in ("MK_DECAL_OVERLAY",)))

            if p.obj is None:
                me = bpy.data.meshes.new(f".{self.name}_{key}")
                bm.to_mesh(me)
                bm.free()
                obj = bpy.data.objects.new(f".{self.name}_{key}", me)
                obj.data.materials.append(self.materials[p.mat_key])
                self.tmp.objects.link(obj)
                p.obj = obj
            else:
                bm.to_mesh(p.obj.data)
                bm.free()
            p.bm = None
        self.parts = {k: p for k, p in self.parts.items() if p.obj is not None}

        # 2. join
        objs = [p.obj for p in self.parts.values()]
        target = objs[0]
        bpy.ops.object.select_all(action="DESELECT")
        for o in objs:
            o.select_set(True)
        bpy.context.view_layer.objects.active = target
        if len(objs) > 1:
            bpy.ops.object.join()

        # 3. tidy the merged mesh
        bm = bmesh.new()
        bm.from_mesh(target.data)
        if weld:
            dedupe(bm, 1e-5)
        delete_loose(bm)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        bm.to_mesh(target.data)
        bm.free()

        # 4. name, origin, transforms
        target.name = self.name
        target.data.name = self.name
        if origin is None:
            if getattr(self, "origin", None) is not None:
                origin = vec(self.origin)
            else:
                mn, mx = bounds(target)
                # origin sits on the design floor plane (z = 0), not the lowest
                # vertex, so elevated modules (vaults, decks) keep their height
                origin = vec(((mn.x + mx.x) / 2.0, (mn.y + mx.y) / 2.0, 0.0))
        set_origin(target, origin)
        target.matrix_world = Matrix.Identity(4)
        target.rotation_mode = "XYZ"

        # 5. metadata custom properties (readable in-engine and in reports)
        s = self.spec
        target["wk_asset"] = self.name
        target["wk_category"] = s.category
        target["wk_tier"] = s.tier
        target["wk_purpose"] = s.purpose
        target["wk_materials"] = ",".join(self.material_slots())
        target["wk_size"] = ",".join(f"{v:.3f}" for v in s.size)
        target["wk_origin"] = s.origin
        target["wk_grid"] = s.grid

        self.obj = target
        return target


def set_origin(obj, world_loc):
    """Move the object origin to *world_loc* without moving the geometry."""
    world_loc = vec(world_loc)
    inv = obj.matrix_world.inverted()
    local = inv @ world_loc
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.translate(bm, verts=bm.verts[:], vec=-local)
    bm.to_mesh(obj.data)
    bm.free()
    m = obj.matrix_world.copy()
    m.translation = world_loc
    obj.matrix_world = m


def bounds(obj) -> tuple[Vector, Vector]:
    """World-space (min, max) bounds of an object."""
    pts = [obj.matrix_world @ vec(c) for c in obj.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return mn, mx


def size_of(obj) -> Vector:
    mn, mx = bounds(obj)
    return mx - mn


def tri_count(obj) -> int:
    return sum(len(p.vertices) - 2 for p in obj.data.polygons)
