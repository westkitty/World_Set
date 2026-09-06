#!/usr/bin/env python3
"""WORLD KIT shared helpers: materials, primitives, collections, origins."""
import math
import bpy

TEXDIR = '/home/user/World_Set/WorldKit/tex'
_images = {}


# ------------------------------------------------------------- images
def img(name, srgb=True):
    if name not in _images:
        im = bpy.data.images.load(TEXDIR + '/' + name)
        im.colorspace_settings.name = 'sRGB' if srgb else 'Non-Color'
        _images[name] = im
    return _images[name]


def pack_all():
    for im in _images.values():
        try:
            im.pack()
        except Exception:
            pass


# ------------------------------------------------------------- materials
def make_mat(name, base=(0.8, 0.8, 0.8, 1.0), metallic=0.0, rough=0.7,
             tex=None, tint=(1, 1, 1), alpha_mode='OPAQUE', cutoff=0.5,
             emissive=None, emission_strength=1.0, doubleside=False):
    """Create (or reuse) a Principled material.

    tex: color texture filename (also feeds Emission when emissive='TEX').
    alpha_mode: OPAQUE | MASK (Math GreaterThan -> MASK in glTF) | BLEND.
    emissive: None | 'TEX' | (r,g,b).
    """
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = bpy.data.materials.new(name)
    bsdf = m.node_tree.nodes['Principled BSDF']
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Base Color'].default_value = (base[0] * tint[0], base[1] * tint[1],
                                                base[2] * tint[2], base[3] if len(base) > 3 else 1.0)
    nt = m.node_tree
    if tex:
        t = nt.nodes.new('ShaderNodeTexImage')
        t.image = img(tex)
        t.location = (-420, 320)
        if alpha_mode == 'OPAQUE' and tint == (1, 1, 1):
            nt.links.new(t.outputs['Color'], bsdf.inputs['Base Color'])
        else:
            # multiply texture color by tint via Mix node
            mx = nt.nodes.new('ShaderNodeMix')
            mx.data_type = 'RGBA'
            mx.blend_type = 'MULTIPLY'
            mx.inputs['Factor'].default_value = 1.0
            mx.inputs['A'].default_value = (tint[0], tint[1], tint[2], 1.0)
            mx.location = (-200, 380)
            nt.links.new(t.outputs['Color'], mx.inputs['B'])
            nt.links.new(mx.outputs['Result'], bsdf.inputs['Base Color'])
        if alpha_mode == 'MASK':
            g = nt.nodes.new('ShaderNodeMath')
            g.operation = 'GREATER_THAN'
            g.inputs[1].default_value = cutoff
            g.location = (-200, 120)
            nt.links.new(t.outputs['Alpha'], g.inputs[0])
            nt.links.new(g.outputs['Value'], bsdf.inputs['Alpha'])
            m.surface_render_method = 'DITHERED'
        elif alpha_mode == 'BLEND':
            nt.links.new(t.outputs['Alpha'], bsdf.inputs['Alpha'])
            m.surface_render_method = 'BLENDED'
    if emissive == 'TEX' and tex:
        tnode = [n for n in nt.nodes if n.type == 'TEX_IMAGE'][0]
        nt.links.new(tnode.outputs['Color'], bsdf.inputs['Emission Color'])
        bsdf.inputs['Emission Strength'].default_value = emission_strength
    elif emissive is not None:
        bsdf.inputs['Emission Color'].default_value = (emissive[0], emissive[1], emissive[2], 1.0)
        bsdf.inputs['Emission Strength'].default_value = emission_strength
    m.use_backface_culling = not doubleside
    return m


def M(name):
    return bpy.data.materials[name]


# ------------------------------------------------------------- selection/object utils
def desel():
    bpy.ops.object.select_all(action='DESELECT')


def sel(obj):
    desel()
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def apply_scale(obj):
    sel(obj)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)


def shade_smooth(obj, auto_angle=0.6):
    sel(obj)
    try:
        bpy.ops.object.shade_smooth()
    except Exception:
        pass
    try:
        bpy.ops.object.modifier_add(type='SMOOTH_BY_ANGLE')
        obj.modifiers[-1].angle_limit = auto_angle
    except Exception:
        pass


def bevel(obj, width=0.02, seg=2, angle=0.6):
    sel(obj)
    try:
        bpy.ops.object.modifier_add(type='BEVEL')
        b = obj.modifiers[-1]
        b.width = width
        b.segments = seg
        b.limit_method = 'ANGLE'
        b.angle_limit = angle
    except Exception:
        pass


def auto_uv(obj, repeat=(1, 1)):
    sel(obj)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')
    if repeat != (1, 1):
        uv_repeat(obj, *repeat)


def uv_repeat(obj, rx, ry):
    me = obj.data
    if not me.uv_layers:
        return
    uv = me.uv_layers.active.data
    for d in uv:
        d.uv[0] *= rx
        d.uv[1] *= ry


# ------------------------------------------------------------- primitives
def _finish_prim(obj, name, dims, mat, smooth):
    obj.name = name
    if dims is not None:
        obj.dimensions = dims
        apply_scale(obj)
    if mat is not None:
        obj.data.materials.append(mat if isinstance(mat, bpy.types.Material) else M(mat))
    if smooth:
        shade_smooth(obj)
    desel()
    return obj


def box(name, dims, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, smooth=False):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.active_object
    o.rotation_euler = rot
    return _finish_prim(o, name, dims, mat, smooth)


def cyl(name, r, h, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, verts=14, smooth=True):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, vertices=verts, location=loc,
                                        end_fill_type='NGON')
    o = bpy.context.active_object
    o.rotation_euler = rot
    return _finish_prim(o, name, None, mat, smooth)


def cone(name, r1, r2, h, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, verts=14, smooth=True):
    bpy.ops.mesh.primitive_cone_add(radius1=r1, radius2=r2, depth=h, vertices=verts, location=loc)
    o = bpy.context.active_object
    o.rotation_euler = rot
    return _finish_prim(o, name, None, mat, smooth)


def plane(name, w, h, loc=(0, 0, 0), rot=(0, 0, 0), mat=None):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
    o = bpy.context.active_object
    o.scale = (w, h, 1)
    apply_scale(o)
    o.rotation_euler = rot
    return _finish_prim(o, name, None, mat, False)


def sphere(name, r, loc=(0, 0, 0), mat=None, scale=(1, 1, 1), smooth=True, seg=16, ring=12):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=seg, ring_count=ring, location=loc)
    o = bpy.context.active_object
    o.scale = scale
    apply_scale(o)
    return _finish_prim(o, name, None, mat, smooth)


def ico(name, r, loc=(0, 0, 0), mat=None, scale=(1, 1, 1), smooth=True, subdiv=2):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=r, subdivisions=subdiv, location=loc)
    o = bpy.context.active_object
    o.scale = scale
    apply_scale(o)
    return _finish_prim(o, name, None, mat, smooth)


def torus(name, major, minor, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, smooth=True,
          major_seg=24, minor_seg=12):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
                                     major_segments=major_seg, minor_segments=minor_seg,
                                     location=loc)
    o = bpy.context.active_object
    o.rotation_euler = rot
    return _finish_prim(o, name, None, mat, smooth)


def tube(name, points, radius, mat=None, smooth=True):
    cu = bpy.data.curves.new(name + '_Curve', type='CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = radius
    cu.bevel_resolution = 2
    cu.use_fill_caps = True
    sp = cu.splines.new('BEZIER')
    sp.bezier_points.add(len(points) - 1)
    for i, p in enumerate(points):
        bp = sp.bezier_points[i]
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = 'AUTO'
    o = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(o)
    sel(o)
    bpy.ops.object.convert(target='MESH')
    o = bpy.context.active_object
    o.name = name
    if mat is not None:
        o.data.materials.append(mat if isinstance(mat, bpy.types.Material) else M(mat))
    if smooth:
        shade_smooth(o)
    desel()
    return o


def lamp(name, type, loc=(0, 0, 0), rot=(0, 0, 0), energy=100, color=(1, 1, 1),
         size=0.15, spot_size=0.9, spot_blend=0.3):
    ld = bpy.data.lights.new(name, type)
    ld.energy = energy
    ld.color = color
    if type == 'SPOT':
        ld.spot_size = spot_size
        ld.spot_blend = spot_blend
        ld.shadow_buffer_clip_start = 0.5
    try:
        ld.shadow_soft_size = size
    except Exception:
        pass
    o = bpy.data.objects.new(name, ld)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = rot
    desel()
    return o


# ------------------------------------------------------------- collections / anchors
def col(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


def move_to(objs, coll):
    for o in objs:
        for c in list(o.users_collection):
            try:
                c.objects.unlink(o)
            except Exception:
                pass
        coll.objects.link(o)


def finish(name, cat, objs, lights=(), home=(0, 0, 0)):
    """Parent parts under an anchor Empty at `home`, file into collection."""
    anchor = bpy.data.objects.new(name, None)
    anchor.empty_display_size = 0.3
    anchor.location = home
    bpy.context.scene.collection.objects.link(anchor)
    bpy.context.view_layer.update()
    inv = anchor.matrix_world.inverted()
    idx = 1
    allkids = list(objs) + list(lights)
    for o in allkids:
        o.parent = anchor
        o.matrix_parent_inverse = inv
        if o in lights:
            o.name = f'{name}_L{idx:02d}'
        else:
            o.name = f'{name}_P{idx:02d}'
        if o.data is not None:
            o.data.name = o.name
        idx += 1
    catcol = col(cat)
    sub = bpy.data.collections.get(name)
    if sub is None:
        sub = bpy.data.collections.new(name)
    if sub.name not in [c.name for c in catcol.children]:
        catcol.children.link(sub)
    move_to([anchor] + allkids, sub)
    desel()
    return anchor


def tri_count(objs):
    n = 0
    dg = bpy.context.evaluated_depsgraph_get()
    for o in objs:
        if o.type != 'MESH':
            continue
        try:
            eo = o.evaluated_get(dg)
            me = eo.to_mesh()
            me.calc_loop_triangles()
            n += len(me.loop_triangles)
            eo.to_mesh_clear()
        except Exception:
            try:
                me = o.data
                me.calc_loop_triangles()
                n += len(me.loop_triangles)
            except Exception:
                pass
    return n


def children_recursive(anchor):
    out = []

    def walk(o):
        for c in o.children:
            out.append(c)
            walk(c)
    walk(anchor)
    return out
