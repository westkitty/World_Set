import bpy
import bmesh
import math
import os
from mathutils import Vector, Euler, Matrix

TEXTURE_DIR = "/Users/andrew/World_Set/textures"
BLEND_OUTPUT = "/Users/andrew/World_Set/WORLD_KIT_MASTER.blend"

def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if not bpy.context.scene.view_layers:
        bpy.context.scene.view_layers.new(name="ViewLayer")

def create_collections():
    root_col = bpy.data.collections.new("WORLD_KIT")
    bpy.context.scene.collection.children.link(root_col)
    
    col_names = [
        "00_WORLD_DNA",
        "01_ARCHITECTURE",
        "02_WALLS",
        "03_FLOORS",
        "04_DOORS_WINDOWS",
        "05_STRUCTURAL",
        "06_FURNITURE",
        "07_PROPS",
        "08_LIGHTS",
        "09_SIGNAGE",
        "10_VEGETATION",
        "11_DECALS",
        "12_TERRAIN",
        "13_HERO",
        "14_MATERIALS",
        "15_SHOWCASE"
    ]
    collections = {}
    for cname in col_names:
        col = bpy.data.collections.new(cname)
        root_col.children.link(col)
        collections[cname] = col
    return collections

def setup_materials():
    materials = {}
    def load_img(name):
        p = os.path.join(TEXTURE_DIR, name)
        return bpy.data.images.load(p) if os.path.exists(p) else None

    def make_pbr(name):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes.clear()
        out = nodes.new("ShaderNodeOutputMaterial")
        out.location = (400, 0)
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
        bsdf.location = (0, 0)
        mat.node_tree.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
        return mat, nodes, bsdf

    # 1. Concrete
    m, n, b = make_pbr("MAT_Concrete_Brutalist")
    alb = load_img("tex_concrete_albedo.png")
    if alb:
        t = n.new("ShaderNodeTexImage"); t.image = alb; t.location = (-400, 100)
        m.node_tree.links.new(t.outputs["Color"], b.inputs["Base Color"])
    else:
        b.inputs["Base Color"].default_value = (0.35, 0.37, 0.38, 1.0)
    rgh = load_img("tex_concrete_roughness.png")
    if rgh:
        t = n.new("ShaderNodeTexImage"); t.image = rgh; t.image.colorspace_settings.name = "Non-Color"; t.location = (-400, -150)
        m.node_tree.links.new(t.outputs["Color"], b.inputs["Roughness"])
    else:
        b.inputs["Roughness"].default_value = 0.85
    nrm = load_img("tex_concrete_normal.png")
    if nrm:
        t = n.new("ShaderNodeTexImage"); t.image = nrm; t.image.colorspace_settings.name = "Non-Color"; t.location = (-600, -350)
        nm = n.new("ShaderNodeNormalMap"); nm.location = (-250, -350); nm.inputs["Strength"].default_value = 1.0
        m.node_tree.links.new(t.outputs["Color"], nm.inputs["Color"])
        m.node_tree.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    materials["concrete"] = m

    # 2. Heavy Steel
    m, n, b = make_pbr("MAT_Heavy_Steel_Painted")
    alb = load_img("tex_steel_albedo.png")
    if alb:
        t = n.new("ShaderNodeTexImage"); t.image = alb; t.location = (-400, 100)
        m.node_tree.links.new(t.outputs["Color"], b.inputs["Base Color"])
    else:
        b.inputs["Base Color"].default_value = (0.22, 0.25, 0.23, 1.0)
    rgh = load_img("tex_steel_roughness.png")
    if rgh:
        t = n.new("ShaderNodeTexImage"); t.image = rgh; t.image.colorspace_settings.name = "Non-Color"; t.location = (-400, -150)
        m.node_tree.links.new(t.outputs["Color"], b.inputs["Roughness"])
    else:
        b.inputs["Roughness"].default_value = 0.55
    met = load_img("tex_steel_metallic.png")
    if met:
        t = n.new("ShaderNodeTexImage"); t.image = met; t.image.colorspace_settings.name = "Non-Color"; t.location = (-400, -350)
        m.node_tree.links.new(t.outputs["Color"], b.inputs["Metallic"])
    else:
        b.inputs["Metallic"].default_value = 0.2
    nrm = load_img("tex_steel_normal.png")
    if nrm:
        t = n.new("ShaderNodeTexImage"); t.image = nrm; t.image.colorspace_settings.name = "Non-Color"; t.location = (-600, -550)
        nm = n.new("ShaderNodeNormalMap"); nm.location = (-250, -550); nm.inputs["Strength"].default_value = 1.2
        m.node_tree.links.new(t.outputs["Color"], nm.inputs["Color"])
        m.node_tree.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    materials["steel"] = m

    # 3. Grate
    m, n, b = make_pbr("MAT_Galvanized_Grate")
    alb = load_img("tex_grate_albedo.png")
    if alb:
        t = n.new("ShaderNodeTexImage"); t.image = alb; t.location = (-400, 100)
        m.node_tree.links.new(t.outputs["Color"], b.inputs["Base Color"])
    else:
        b.inputs["Base Color"].default_value = (0.45, 0.48, 0.50, 1.0)
    rgh = load_img("tex_grate_roughness.png")
    if rgh:
        t = n.new("ShaderNodeTexImage"); t.image = rgh; t.image.colorspace_settings.name = "Non-Color"; t.location = (-400, -150)
        m.node_tree.links.new(t.outputs["Color"], b.inputs["Roughness"])
    met = load_img("tex_grate_metallic.png")
    if met:
        t = n.new("ShaderNodeTexImage"); t.image = met; t.image.colorspace_settings.name = "Non-Color"; t.location = (-400, -350)
        m.node_tree.links.new(t.outputs["Color"], b.inputs["Metallic"])
    materials["grate"] = m

    # 4. Glass
    m, n, b = make_pbr("MAT_Reinforced_Glass")
    b.inputs["Base Color"].default_value = (0.1, 0.28, 0.24, 1.0)
    b.inputs["Roughness"].default_value = 0.12
    if "Transmission Weight" in b.inputs: b.inputs["Transmission Weight"].default_value = 0.85
    elif "Transmission" in b.inputs: b.inputs["Transmission"].default_value = 0.85
    b.inputs["IOR"].default_value = 1.52
    materials["glass"] = m

    # 5. Rubber
    m, n, b = make_pbr("MAT_Rubber_Conduit")
    b.inputs["Base Color"].default_value = (0.12, 0.13, 0.14, 1.0)
    b.inputs["Roughness"].default_value = 0.72
    materials["rubber"] = m

    # 6. Cyan Screen UI
    m, n, b = make_pbr("MAT_Emissive_Cyan_UI")
    scr = load_img("tex_screen_cyan.png")
    if scr:
        t = n.new("ShaderNodeTexImage"); t.image = scr; t.location = (-400, 100)
        m.node_tree.links.new(t.outputs["Color"], b.inputs["Base Color"])
        if "Emission Color" in b.inputs:
            m.node_tree.links.new(t.outputs["Color"], b.inputs["Emission Color"])
            b.inputs["Emission Strength"].default_value = 5.0
    else:
        b.inputs["Base Color"].default_value = (0.1, 0.9, 1.0, 1.0)
        if "Emission Color" in b.inputs:
            b.inputs["Emission Color"].default_value = (0.1, 0.9, 1.0, 1.0)
            b.inputs["Emission Strength"].default_value = 5.0
    materials["emissive_cyan"] = m

    # 7. Hazard
    m, n, b = make_pbr("MAT_Hazard_Stripes")
    hz = load_img("tex_hazard_albedo.png")
    if hz:
        t = n.new("ShaderNodeTexImage"); t.image = hz; t.location = (-400, 100)
        m.node_tree.links.new(t.outputs["Color"], b.inputs["Base Color"])
    else:
        b.inputs["Base Color"].default_value = (0.95, 0.72, 0.0, 1.0)
    materials["hazard"] = m

    # 8. Sector Sign
    m, n, b = make_pbr("MAT_Sign_Sector")
    sgn = load_img("tex_sign_sector.png")
    if sgn:
        t = n.new("ShaderNodeTexImage"); t.image = sgn; t.location = (-400, 100)
        m.node_tree.links.new(t.outputs["Color"], b.inputs["Base Color"])
        if "Emission Color" in b.inputs:
            m.node_tree.links.new(t.outputs["Color"], b.inputs["Emission Color"])
            b.inputs["Emission Strength"].default_value = 1.0
    materials["sign_sector"] = m

    # 9. Hazard Sign
    m, n, b = make_pbr("MAT_Sign_Hazard")
    haz = load_img("tex_sign_hazard.png")
    if haz:
        t = n.new("ShaderNodeTexImage"); t.image = haz; t.location = (-400, 100)
        m.node_tree.links.new(t.outputs["Color"], b.inputs["Base Color"])
    materials["sign_hazard"] = m

    # 10. Brass
    m, n, b = make_pbr("MAT_Brass_Valves")
    b.inputs["Base Color"].default_value = (0.82, 0.65, 0.28, 1.0)
    b.inputs["Metallic"].default_value = 0.95
    b.inputs["Roughness"].default_value = 0.32
    materials["brass"] = m

    # 11. Amber Strobe
    m, n, b = make_pbr("MAT_Amber_Strobe")
    b.inputs["Base Color"].default_value = (1.0, 0.6, 0.05, 1.0)
    if "Emission Color" in b.inputs:
        b.inputs["Emission Color"].default_value = (1.0, 0.6, 0.05, 1.0)
        b.inputs["Emission Strength"].default_value = 8.0
    materials["amber_strobe"] = m

    # 12. Fluorescent Glow
    m, n, b = make_pbr("MAT_Fluorescent_Glow")
    b.inputs["Base Color"].default_value = (0.85, 0.95, 1.0, 1.0)
    if "Emission Color" in b.inputs:
        b.inputs["Emission Color"].default_value = (0.85, 0.95, 1.0, 1.0)
        b.inputs["Emission Strength"].default_value = 6.0
    materials["light_glow"] = m

    return materials

# Modeling Helpers
def bmesh_add_box(bm, center, size, mat_idx=0):
    dx, dy, dz = size[0]*0.5, size[1]*0.5, size[2]*0.5
    cx, cy, cz = center
    v1 = bm.verts.new((cx - dx, cy - dy, cz - dz))
    v2 = bm.verts.new((cx + dx, cy - dy, cz - dz))
    v3 = bm.verts.new((cx + dx, cy + dy, cz - dz))
    v4 = bm.verts.new((cx - dx, cy + dy, cz - dz))
    v5 = bm.verts.new((cx - dx, cy - dy, cz + dz))
    v6 = bm.verts.new((cx + dx, cy - dy, cz + dz))
    v7 = bm.verts.new((cx + dx, cy + dy, cz + dz))
    v8 = bm.verts.new((cx - dx, cy + dy, cz + dz))
    faces = [
        bm.faces.new((v1, v4, v3, v2)),
        bm.faces.new((v5, v6, v7, v8)),
        bm.faces.new((v1, v2, v6, v5)),
        bm.faces.new((v2, v3, v7, v6)),
        bm.faces.new((v3, v4, v8, v7)),
        bm.faces.new((v4, v1, v5, v8)),
    ]
    for f in faces:
        f.material_index = mat_idx
    return faces

def bmesh_add_cylinder(bm, center, radius, height, segments=16, axis="Z", mat_idx=0):
    cx, cy, cz = center
    half_h = height * 0.5
    circle_pts = []
    for i in range(segments):
        angle = 2.0 * math.pi * i / segments
        ca, sa = math.cos(angle) * radius, math.sin(angle) * radius
        circle_pts.append((ca, sa))
    
    bot_verts = []
    top_verts = []
    for ca, sa in circle_pts:
        if axis == "Z":
            bot_verts.append(bm.verts.new((cx + ca, cy + sa, cz - half_h)))
            top_verts.append(bm.verts.new((cx + ca, cy + sa, cz + half_h)))
        elif axis == "X":
            bot_verts.append(bm.verts.new((cx - half_h, cy + ca, cz + sa)))
            top_verts.append(bm.verts.new((cx + half_h, cy + ca, cz + sa)))
        elif axis == "Y":
            bot_verts.append(bm.verts.new((cx + ca, cy - half_h, cz + sa)))
            top_verts.append(bm.verts.new((cx + ca, cy + half_h, cz + sa)))

    f_bot = bm.faces.new(reversed(bot_verts))
    f_bot.material_index = mat_idx
    f_top = bm.faces.new(top_verts)
    f_top.material_index = mat_idx
    
    for i in range(segments):
        i_next = (i + 1) % segments
        f_side = bm.faces.new((bot_verts[i], bot_verts[i_next], top_verts[i_next], top_verts[i]))
        f_side.material_index = mat_idx

def finalize_asset(name, bm, collection, mats, bevel=True, bevel_w=0.015):
    mesh = bpy.data.meshes.new(name + "_mesh")
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    
    for m in mats:
        obj.data.materials.append(m)
        
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cube_project(cube_size=4.0)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    if bevel:
        bev = obj.modifiers.new("Bevel", "BEVEL")
        bev.width = bevel_w
        bev.segments = 2
        bev.limit_method = "ANGLE"
        bev.angle_limit = math.radians(35)
        bev.use_clamp_overlap = True
        
    obj.select_set(False)
    return obj

# -------------------------------------------------------------
# 32 ASSET GENERATOR FUNCTIONS
# -------------------------------------------------------------

# 1. WK_WALL_SOLID_A_01
def create_wall_solid(cols, mats):
    bm = bmesh.new()
    # Concrete main slab (mat 0)
    bmesh_add_box(bm, (0, 0, 2.0), (4.0, 0.25, 4.0), mat_idx=0)
    # Steel baseboard footing (mat 1)
    bmesh_add_box(bm, (0, 0, 0.1), (4.0, 0.29, 0.2), mat_idx=1)
    # Steel top lintel trim (mat 1)
    bmesh_add_box(bm, (0, 0, 3.9), (4.0, 0.28, 0.2), mat_idx=1)
    # Vertical side interlock flanges (mat 1)
    bmesh_add_box(bm, (-1.96, 0, 2.0), (0.08, 0.27, 3.6), mat_idx=1)
    bmesh_add_box(bm, (1.96, 0, 2.0), (0.08, 0.27, 3.6), mat_idx=1)
    # Conduit chase at Z=3.2m (mat 2 rubber)
    bmesh_add_box(bm, (0, 0.13, 3.2), (4.0, 0.03, 0.08), mat_idx=2)
    bmesh_add_box(bm, (0, -0.13, 3.2), (4.0, 0.03, 0.08), mat_idx=2)
    return finalize_asset("WK_WALL_SOLID_A_01", bm, cols["02_WALLS"], [mats["concrete"], mats["steel"], mats["rubber"]])

# 2. WK_WALL_PANEL_B_01
def create_wall_panel(cols, mats):
    bm = bmesh.new()
    # Left & right structural piers
    bmesh_add_box(bm, (-1.5, 0, 2.0), (1.0, 0.25, 4.0), mat_idx=0)
    bmesh_add_box(bm, (1.5, 0, 2.0), (1.0, 0.25, 4.0), mat_idx=0)
    # Bottom sill and top lintel
    bmesh_add_box(bm, (0, 0, 0.4), (2.0, 0.25, 0.8), mat_idx=0)
    bmesh_add_box(bm, (0, 0, 3.6), (2.0, 0.25, 0.8), mat_idx=0)
    # Recessed steel backing plate
    bmesh_add_box(bm, (0, 0.04, 2.0), (2.0, 0.12, 2.4), mat_idx=1)
    # Steel footing
    bmesh_add_box(bm, (0, 0, 0.1), (4.0, 0.29, 0.2), mat_idx=1)
    # Unistrut equipment channels
    bmesh_add_box(bm, (-0.6, 0.0, 2.0), (0.08, 0.06, 2.2), mat_idx=1)
    bmesh_add_box(bm, (0.6, 0.0, 2.0), (0.08, 0.06, 2.2), mat_idx=1)
    # Telemetry terminal
    bmesh_add_box(bm, (0, -0.04, 2.0), (0.8, 0.16, 0.6), mat_idx=1)
    bmesh_add_box(bm, (0, -0.125, 2.05), (0.6, 0.02, 0.4), mat_idx=3) # Emissive screen
    # Horizontal conduit datum
    bmesh_add_box(bm, (0, 0.13, 3.2), (4.0, 0.03, 0.08), mat_idx=2)
    return finalize_asset("WK_WALL_PANEL_B_01", bm, cols["02_WALLS"], [mats["concrete"], mats["steel"], mats["rubber"], mats["emissive_cyan"]])

# 3. WK_WALL_CORNER_IN_A_01
def create_wall_corner_in(cols, mats):
    bm = bmesh.new()
    # X leg (from 0 to 2m)
    bmesh_add_box(bm, (1.0, 0, 2.0), (2.0, 0.25, 4.0), mat_idx=0)
    # Y leg (from 0 to 2m)
    bmesh_add_box(bm, (0, 1.0, 2.0), (0.25, 2.0, 4.0), mat_idx=0)
    # Footing trims
    bmesh_add_box(bm, (1.0, 0, 0.1), (2.0, 0.29, 0.2), mat_idx=1)
    bmesh_add_box(bm, (0, 1.0, 0.1), (0.29, 2.0, 0.2), mat_idx=1)
    # Vertical corner conduit riser (mat 2)
    bmesh_add_cylinder(bm, (0.18, 0.18, 2.0), radius=0.08, height=4.0, segments=16, axis="Z", mat_idx=2)
    # Riser bracket clamps
    for z in [1.0, 2.0, 3.0]:
        bmesh_add_box(bm, (0.18, 0.18, z), (0.22, 0.22, 0.05), mat_idx=1)
    return finalize_asset("WK_WALL_CORNER_IN_A_01", bm, cols["02_WALLS"], [mats["concrete"], mats["steel"], mats["rubber"]])

# 4. WK_WALL_CORNER_OUT_A_01
def create_wall_corner_out(cols, mats):
    bm = bmesh.new()
    bmesh_add_box(bm, (1.0, 0, 2.0), (2.0, 0.25, 4.0), mat_idx=0)
    bmesh_add_box(bm, (0, 1.0, 2.0), (0.25, 2.0, 4.0), mat_idx=0)
    bmesh_add_box(bm, (1.0, 0, 0.1), (2.0, 0.29, 0.2), mat_idx=1)
    bmesh_add_box(bm, (0, 1.0, 0.1), (0.29, 2.0, 0.2), mat_idx=1)
    # Heavy corner steel armor plate
    bmesh_add_box(bm, (0.15, -0.13, 2.0), (0.3, 0.02, 4.0), mat_idx=1)
    bmesh_add_box(bm, (-0.13, 0.15, 2.0), (0.02, 0.3, 4.0), mat_idx=1)
    # Hazard bumper at base
    bmesh_add_box(bm, (0.16, -0.14, 0.6), (0.26, 0.02, 1.2), mat_idx=2)
    return finalize_asset("WK_WALL_CORNER_OUT_A_01", bm, cols["02_WALLS"], [mats["concrete"], mats["steel"], mats["hazard"]])

# 5. WK_WALL_DOORFRAME_A_01
def create_wall_doorframe(cols, mats):
    bm = bmesh.new()
    bmesh_add_box(bm, (-1.5, 0, 2.0), (1.0, 0.25, 4.0), mat_idx=0)
    bmesh_add_box(bm, (1.5, 0, 2.0), (1.0, 0.25, 4.0), mat_idx=0)
    bmesh_add_box(bm, (0, 0, 3.25), (2.0, 0.25, 1.5), mat_idx=0)
    # Footing trims
    bmesh_add_box(bm, (-1.5, 0, 0.1), (1.0, 0.29, 0.2), mat_idx=1)
    bmesh_add_box(bm, (1.5, 0, 0.1), (1.0, 0.29, 0.2), mat_idx=1)
    # Steel frame jambs & lintel
    bmesh_add_box(bm, (-1.02, 0, 1.25), (0.08, 0.28, 2.5), mat_idx=1)
    bmesh_add_box(bm, (1.02, 0, 1.25), (0.08, 0.28, 2.5), mat_idx=1)
    bmesh_add_box(bm, (0, 0, 2.52), (2.12, 0.28, 0.08), mat_idx=1)
    return finalize_asset("WK_WALL_DOORFRAME_A_01", bm, cols["02_WALLS"], [mats["concrete"], mats["steel"]])

# 6. WK_WALL_WINDOW_A_01
def create_wall_window(cols, mats):
    bm = bmesh.new()
    bmesh_add_box(bm, (0, 0, 0.6), (4.0, 0.25, 1.2), mat_idx=0)
    bmesh_add_box(bm, (0, 0, 3.4), (4.0, 0.25, 1.2), mat_idx=0)
    bmesh_add_box(bm, (-1.5, 0, 2.0), (1.0, 0.25, 1.6), mat_idx=0)
    bmesh_add_box(bm, (1.5, 0, 2.0), (1.0, 0.25, 1.6), mat_idx=0)
    # Steel sill
    bmesh_add_box(bm, (0, 0, 1.2), (2.1, 0.32, 0.08), mat_idx=1)
    bmesh_add_box(bm, (0, 0, 2.8), (2.1, 0.32, 0.08), mat_idx=1)
    # Window glass pane
    bmesh_add_box(bm, (0, 0, 2.0), (1.98, 0.04, 1.58), mat_idx=2)
    # Tension brass bolts
    for x in [-0.8, -0.3, 0.3, 0.8]:
        bmesh_add_cylinder(bm, (x, -0.13, 1.26), radius=0.02, height=0.04, segments=8, axis="Y", mat_idx=3)
        bmesh_add_cylinder(bm, (x, -0.13, 2.74), radius=0.02, height=0.04, segments=8, axis="Y", mat_idx=3)
    return finalize_asset("WK_WALL_WINDOW_A_01", bm, cols["02_WALLS"], [mats["concrete"], mats["steel"], mats["glass"], mats["brass"]])

# 7. WK_FLOOR_SLAB_A_01
def create_floor_slab(cols, mats):
    bm = bmesh.new()
    bmesh_add_box(bm, (0, 0, -0.15), (4.0, 4.0, 0.3), mat_idx=0)
    # 4 corner steel anchor pads
    for cx, cy in [(-1.8, -1.8), (1.8, -1.8), (-1.8, 1.8), (1.8, 1.8)]:
        bmesh_add_box(bm, (cx, cy, -0.005), (0.35, 0.35, 0.01), mat_idx=1)
    # Expansion joint grooves
    bmesh_add_box(bm, (0, 0, -0.005), (4.0, 0.03, 0.01), mat_idx=1)
    bmesh_add_box(bm, (0, 0, -0.005), (0.03, 4.0, 0.01), mat_idx=1)
    return finalize_asset("WK_FLOOR_SLAB_A_01", bm, cols["03_FLOORS"], [mats["concrete"], mats["steel"]])

# 8. WK_FLOOR_GRATE_B_01
def create_floor_grate(cols, mats):
    bm = bmesh.new()
    # Perimeter concrete curbs
    bmesh_add_box(bm, (0, -1.7, -0.15), (4.0, 0.6, 0.3), mat_idx=0)
    bmesh_add_box(bm, (0, 1.7, -0.15), (4.0, 0.6, 0.3), mat_idx=0)
    bmesh_add_box(bm, (-1.7, 0, -0.15), (0.6, 2.8, 0.3), mat_idx=0)
    bmesh_add_box(bm, (1.7, 0, -0.15), (0.6, 2.8, 0.3), mat_idx=0)
    # Recessed sump basin
    bmesh_add_box(bm, (0, 0, -0.28), (2.8, 2.8, 0.04), mat_idx=1)
    # Sub-support I-beams
    bmesh_add_box(bm, (0, -0.7, -0.15), (2.8, 0.08, 0.2), mat_idx=1)
    bmesh_add_box(bm, (0, 0.7, -0.15), (2.8, 0.08, 0.2), mat_idx=1)
    # Drainage grate insert
    bmesh_add_box(bm, (0, 0, -0.01), (2.78, 2.78, 0.02), mat_idx=2)
    return finalize_asset("WK_FLOOR_GRATE_B_01", bm, cols["03_FLOORS"], [mats["concrete"], mats["steel"], mats["grate"]])

# 9. WK_FLOOR_CATWALK_C_01
def create_floor_catwalk(cols, mats):
    bm = bmesh.new()
    # Side channel beams
    bmesh_add_box(bm, (-0.95, 0, -0.1), (0.1, 4.0, 0.2), mat_idx=0)
    bmesh_add_box(bm, (0.95, 0, -0.1), (0.1, 4.0, 0.2), mat_idx=0)
    bmesh_add_box(bm, (0, -1.95, -0.1), (1.8, 0.1, 0.2), mat_idx=0)
    bmesh_add_box(bm, (0, 1.95, -0.1), (1.8, 0.1, 0.2), mat_idx=0)
    # Under-trusses
    for y in [-0.9, 0.0, 0.9]:
        bmesh_add_box(bm, (0, y, -0.12), (1.8, 0.08, 0.12), mat_idx=0)
    # Grated walking deck
    bmesh_add_box(bm, (0, 0, -0.01), (1.9, 3.9, 0.02), mat_idx=1)
    # Yellow hazard warning edge
    bmesh_add_box(bm, (0, -1.98, -0.005), (1.9, 0.04, 0.01), mat_idx=2)
    bmesh_add_box(bm, (0, 1.98, -0.005), (1.9, 0.04, 0.01), mat_idx=2)
    return finalize_asset("WK_FLOOR_CATWALK_C_01", bm, cols["03_FLOORS"], [mats["steel"], mats["grate"], mats["hazard"]])

# 10. WK_FLOOR_TRIM_A_01
def create_floor_trim(cols, mats):
    bm = bmesh.new()
    bmesh_add_box(bm, (0, 0, 0.075), (4.0, 0.35, 0.15), mat_idx=0)
    bmesh_add_box(bm, (0, 0, 0.15), (3.96, 0.31, 0.02), mat_idx=1)
    return finalize_asset("WK_FLOOR_TRIM_A_01", bm, cols["03_FLOORS"], [mats["steel"], mats["grate"]])

# 11. WK_CEIL_COFFER_A_01
def create_ceil_coffer(cols, mats):
    bm = bmesh.new()
    # Perimeter beams
    bmesh_add_box(bm, (0, -1.85, 0.2), (4.0, 0.3, 0.4), mat_idx=0)
    bmesh_add_box(bm, (0, 1.85, 0.2), (4.0, 0.3, 0.4), mat_idx=0)
    bmesh_add_box(bm, (-1.85, 0, 0.2), (0.3, 3.4, 0.4), mat_idx=0)
    bmesh_add_box(bm, (1.85, 0, 0.2), (0.3, 3.4, 0.4), mat_idx=0)
    # Cross dividing ribs
    bmesh_add_box(bm, (0, 0, 0.2), (4.0, 0.25, 0.35), mat_idx=0)
    bmesh_add_box(bm, (0, 0, 0.2), (0.25, 4.0, 0.35), mat_idx=0)
    # Roof backing slab
    bmesh_add_box(bm, (0, 0, 0.38), (4.0, 4.0, 0.04), mat_idx=0)
    # Acoustic steel insert panels
    for cx, cy in [(-0.9, -0.9), (0.9, -0.9), (-0.9, 0.9), (0.9, 0.9)]:
        bmesh_add_box(bm, (cx, cy, 0.34), (1.4, 1.4, 0.04), mat_idx=1)
    return finalize_asset("WK_CEIL_COFFER_A_01", bm, cols["01_ARCHITECTURE"], [mats["concrete"], mats["steel"]])

# 12. WK_CEIL_GIRDER_B_01
def create_ceil_girder(cols, mats):
    bm = bmesh.new()
    # Two main steel I-beams along Y
    for bx in [-1.2, 1.2]:
        bmesh_add_box(bm, (bx, 0, 0.03), (0.3, 4.0, 0.06), mat_idx=0) # bot flange
        bmesh_add_box(bm, (bx, 0, 0.57), (0.3, 4.0, 0.06), mat_idx=0) # top flange
        bmesh_add_box(bm, (bx, 0, 0.3), (0.04, 4.0, 0.5), mat_idx=0)  # web
    # Transverse bracing
    for by in [-1.2, 0.0, 1.2]:
        bmesh_add_box(bm, (0, by, 0.3), (2.1, 0.08, 0.12), mat_idx=0)
    # Perforated cable tray
    bmesh_add_box(bm, (0, 0, 0.2), (0.6, 4.0, 0.1), mat_idx=1)
    # Conduits
    for cx in [-0.15, 0.0, 0.15]:
        bmesh_add_cylinder(bm, (cx, 0, 0.22), radius=0.03, height=4.0, segments=8, axis="Y", mat_idx=2)
    return finalize_asset("WK_CEIL_GIRDER_B_01", bm, cols["01_ARCHITECTURE"], [mats["steel"], mats["grate"], mats["rubber"]])

# 13. WK_DOOR_BULKHEAD_A_01
def create_door_bulkhead(cols, mats):
    bm = bmesh.new()
    # Left & right jambs
    bmesh_add_box(bm, (-0.95, 0, 1.25), (0.2, 0.35, 2.5), mat_idx=0)
    bmesh_add_box(bm, (0.95, 0, 1.25), (0.2, 0.35, 2.5), mat_idx=0)
    # Door head track casing
    bmesh_add_box(bm, (0, 0, 2.55), (2.1, 0.38, 0.2), mat_idx=0)
    # Hydraulic overhead actuator cylinders
    bmesh_add_cylinder(bm, (0, 0.12, 2.55), radius=0.04, height=1.6, segments=12, axis="X", mat_idx=3)
    # Perimeter rubber gasket
    bmesh_add_box(bm, (-0.84, 0, 1.25), (0.03, 0.15, 2.4), mat_idx=1)
    bmesh_add_box(bm, (0.84, 0, 1.25), (0.03, 0.15, 2.4), mat_idx=1)
    bmesh_add_box(bm, (0, 0, 2.44), (1.7, 0.15, 0.03), mat_idx=1)
    # Hazard threshold ramp
    bmesh_add_box(bm, (0, 0, 0.03), (1.8, 0.4, 0.06), mat_idx=2)
    return finalize_asset("WK_DOOR_BULKHEAD_A_01", bm, cols["04_DOORS_WINDOWS"], [mats["steel"], mats["rubber"], mats["hazard"], mats["brass"]])

# 14. WK_DOOR_SLAB_A_01
def create_door_slab(cols, mats):
    bm = bmesh.new()
    bmesh_add_box(bm, (0, 0, 1.2), (1.8, 0.12, 2.4), mat_idx=0)
    # Recessed stiffener panels
    bmesh_add_box(bm, (-0.45, -0.065, 0.7), (0.7, 0.02, 0.9), mat_idx=0)
    bmesh_add_box(bm, (0.45, -0.065, 0.7), (0.7, 0.02, 0.9), mat_idx=0)
    # Manual emergency dogging wheel
    bmesh_add_cylinder(bm, (0, -0.08, 1.2), radius=0.12, height=0.04, segments=8, axis="Y", mat_idx=3)
    bmesh_add_cylinder(bm, (0, -0.10, 1.2), radius=0.02, height=0.7, segments=8, axis="X", mat_idx=3)
    bmesh_add_cylinder(bm, (0, -0.10, 1.2), radius=0.02, height=0.7, segments=8, axis="Z", mat_idx=3)
    # Reinforced viewport
    bmesh_add_box(bm, (0, 0, 1.8), (0.35, 0.14, 0.45), mat_idx=0)
    bmesh_add_box(bm, (0, 0, 1.8), (0.28, 0.04, 0.38), mat_idx=2) # Glass
    # Hazard stripe leading edge
    bmesh_add_box(bm, (-0.85, 0, 1.2), (0.1, 0.13, 2.4), mat_idx=1)
    return finalize_asset("WK_DOOR_SLAB_A_01", bm, cols["04_DOORS_WINDOWS"], [mats["steel"], mats["hazard"], mats["glass"], mats["brass"]])

# 15. WK_WINDOW_PORTAL_A_01
def create_window_portal(cols, mats):
    bm = bmesh.new()
    # Octagonal chamfered outer frame
    bmesh_add_box(bm, (0, 0, 0), (2.0, 0.25, 1.6), mat_idx=0)
    # Inset double-pane glass
    bmesh_add_box(bm, (0, 0, 0), (1.7, 0.06, 1.3), mat_idx=1)
    # 8 brass tension lugs around perimeter
    for x in [-0.7, -0.25, 0.25, 0.7]:
        bmesh_add_cylinder(bm, (x, -0.13, 0.7), radius=0.025, height=0.05, segments=8, axis="Y", mat_idx=2)
        bmesh_add_cylinder(bm, (x, -0.13, -0.7), radius=0.025, height=0.05, segments=8, axis="Y", mat_idx=2)
    return finalize_asset("WK_WINDOW_PORTAL_A_01", bm, cols["04_DOORS_WINDOWS"], [mats["steel"], mats["glass"], mats["brass"]])

# 16. WK_STRUCT_COLUMN_A_01
def create_struct_column(cols, mats):
    bm = bmesh.new()
    # Bolted steel base plate
    bmesh_add_box(bm, (0, 0, 0.04), (1.0, 1.0, 0.08), mat_idx=1)
    # 8 hex anchor bolts
    for bx, by in [(-0.42, -0.42), (0.42, -0.42), (-0.42, 0.42), (0.42, 0.42),
                   (0, -0.44), (0, 0.44), (-0.44, 0), (0.44, 0)]:
        bmesh_add_cylinder(bm, (bx, by, 0.09), radius=0.03, height=0.04, segments=6, axis="Z", mat_idx=1)
    # Octagonal concrete shaft
    bmesh_add_box(bm, (0, 0, 1.9), (0.8, 0.8, 3.64), mat_idx=0)
    # Capital collar with cantilever corbels
    bmesh_add_box(bm, (0, 0, 3.84), (1.0, 1.0, 0.32), mat_idx=1)
    bmesh_add_box(bm, (-0.5, 0, 3.75), (0.2, 0.4, 0.2), mat_idx=1)
    bmesh_add_box(bm, (0.5, 0, 3.75), (0.2, 0.4, 0.2), mat_idx=1)
    return finalize_asset("WK_STRUCT_COLUMN_A_01", bm, cols["05_STRUCTURAL"], [mats["concrete"], mats["steel"]])

# 17. WK_STRUCT_BEAM_A_01
def create_struct_beam(cols, mats):
    bm = bmesh.new()
    # Wide flange I-beam: top at Z=0.0, extends down to Z=-0.5
    bmesh_add_box(bm, (0, 0, -0.02), (0.4, 4.0, 0.04), mat_idx=0) # top flange
    bmesh_add_box(bm, (0, 0, -0.48), (0.4, 4.0, 0.04), mat_idx=0) # bot flange
    bmesh_add_box(bm, (0, 0, -0.25), (0.04, 4.0, 0.42), mat_idx=0) # web
    # Web stiffener plates
    for y in [-1.5, -0.5, 0.5, 1.5]:
        bmesh_add_box(bm, (0, y, -0.25), (0.36, 0.02, 0.42), mat_idx=0)
    # End connection plates
    bmesh_add_box(bm, (0, -1.99, -0.25), (0.42, 0.02, 0.5), mat_idx=0)
    bmesh_add_box(bm, (0, 1.99, -0.25), (0.42, 0.02, 0.5), mat_idx=0)
    return finalize_asset("WK_STRUCT_BEAM_A_01", bm, cols["05_STRUCTURAL"], [mats["steel"]])

# 18. WK_STRUCT_STAIRS_A_01
def create_struct_stairs(cols, mats):
    bm = bmesh.new()
    # 2 diagonal stringer beams
    bmesh_add_box(bm, (-0.95, 2.0, 1.0), (0.1, 4.2, 0.25), mat_idx=0)
    bmesh_add_box(bm, (0.95, 2.0, 1.0), (0.1, 4.2, 0.25), mat_idx=0)
    # 10 steps
    for i in range(10):
        y_pos = 0.2 + i * 0.4
        z_pos = 0.1 + i * 0.2
        bmesh_add_box(bm, (0, y_pos, z_pos), (1.8, 0.38, 0.04), mat_idx=1) # Grated tread
        bmesh_add_box(bm, (0, y_pos - 0.15, z_pos - 0.08), (1.8, 0.04, 0.16), mat_idx=0) # Sub-bracket
    # Mounting pads
    bmesh_add_box(bm, (-0.95, 0, 0.02), (0.2, 0.2, 0.04), mat_idx=0)
    bmesh_add_box(bm, (0.95, 0, 0.02), (0.2, 0.2, 0.04), mat_idx=0)
    return finalize_asset("WK_STRUCT_STAIRS_A_01", bm, cols["05_STRUCTURAL"], [mats["steel"], mats["grate"]])

# 19. WK_STRUCT_RAILING_A_01
def create_struct_railing(cols, mats):
    bm = bmesh.new()
    # 3 stanchions
    for x in [-1.95, 0.0, 1.95]:
        bmesh_add_cylinder(bm, (x, 0, 0.55), radius=0.03, height=1.1, segments=12, axis="Z", mat_idx=0)
        bmesh_add_box(bm, (x, 0, 0.02), (0.12, 0.12, 0.04), mat_idx=0)
    # Handrail & midrail
    bmesh_add_cylinder(bm, (0, 0, 1.08), radius=0.025, height=4.0, segments=12, axis="X", mat_idx=0)
    bmesh_add_cylinder(bm, (0, 0, 0.55), radius=0.018, height=4.0, segments=12, axis="X", mat_idx=0)
    # Toe board kickplate
    bmesh_add_box(bm, (0, 0, 0.08), (4.0, 0.015, 0.15), mat_idx=1)
    return finalize_asset("WK_STRUCT_RAILING_A_01", bm, cols["05_STRUCTURAL"], [mats["steel"], mats["hazard"]])

# 20. WK_STRUCT_RAILING_2M_01
def create_struct_railing_2m(cols, mats):
    bm = bmesh.new()
    for x in [-0.95, 0.95]:
        bmesh_add_cylinder(bm, (x, 0, 0.55), radius=0.03, height=1.1, segments=12, axis="Z", mat_idx=0)
        bmesh_add_box(bm, (x, 0, 0.02), (0.12, 0.12, 0.04), mat_idx=0)
    bmesh_add_cylinder(bm, (0, 0, 1.08), radius=0.025, height=2.0, segments=12, axis="X", mat_idx=0)
    bmesh_add_cylinder(bm, (0, 0, 0.55), radius=0.018, height=2.0, segments=12, axis="X", mat_idx=0)
    bmesh_add_box(bm, (0, 0, 0.08), (2.0, 0.015, 0.15), mat_idx=1)
    return finalize_asset("WK_STRUCT_RAILING_2M_01", bm, cols["05_STRUCTURAL"], [mats["steel"], mats["hazard"]])

# 21. WK_FURN_CONSOLE_A_01
def create_furn_console(cols, mats):
    bm = bmesh.new()
    # Rack base
    bmesh_add_box(bm, (0, 0, 0.4), (2.0, 0.9, 0.8), mat_idx=0)
    # Work desk
    bmesh_add_box(bm, (0, -0.1, 0.86), (1.95, 0.45, 0.12), mat_idx=0)
    # Dual CRT monitors
    for mx in [-0.5, 0.5]:
        bmesh_add_box(bm, (mx, 0.15, 1.15), (0.7, 0.45, 0.4), mat_idx=0)
        bmesh_add_box(bm, (mx, 0.0, 1.15), (0.55, 0.02, 0.32), mat_idx=1) # Cyan Screen
    # Control dials
    for dx in [-0.8, -0.6, -0.4, 0.4, 0.6, 0.8]:
        bmesh_add_cylinder(bm, (dx, -0.15, 0.93), radius=0.025, height=0.03, segments=8, axis="Z", mat_idx=2)
    return finalize_asset("WK_FURN_CONSOLE_A_01", bm, cols["06_FURNITURE"], [mats["steel"], mats["emissive_cyan"], mats["brass"]])

# 22. WK_FURN_BENCH_A_01
def create_furn_bench(cols, mats):
    bm = bmesh.new()
    # 4 legs
    for lx, ly in [(-0.82, -0.24), (0.82, -0.24), (-0.82, 0.24), (0.82, 0.24)]:
        bmesh_add_box(bm, (lx, ly, 0.4), (0.08, 0.08, 0.8), mat_idx=0)
    # Tabletop
    bmesh_add_box(bm, (0, 0, 0.82), (1.8, 0.65, 0.06), mat_idx=0)
    # Bottom shelf
    bmesh_add_box(bm, (0, 0, 0.2), (1.68, 0.52, 0.03), mat_idx=1)
    # Bench vise on left corner
    bmesh_add_cylinder(bm, (-0.7, -0.2, 0.87), radius=0.08, height=0.04, segments=12, axis="Z", mat_idx=0)
    bmesh_add_box(bm, (-0.7, -0.2, 0.95), (0.16, 0.22, 0.12), mat_idx=0)
    bmesh_add_cylinder(bm, (-0.7, -0.32, 0.95), radius=0.015, height=0.3, segments=8, axis="X", mat_idx=2)
    return finalize_asset("WK_FURN_BENCH_A_01", bm, cols["06_FURNITURE"], [mats["steel"], mats["grate"], mats["brass"]])

# 23. WK_PROP_CRATE_A_01
def create_prop_crate(cols, mats):
    bm = bmesh.new()
    # Forklift skids
    bmesh_add_box(bm, (0, -0.4, 0.05), (1.2, 0.12, 0.1), mat_idx=0)
    bmesh_add_box(bm, (0, 0.4, 0.05), (1.2, 0.12, 0.1), mat_idx=0)
    # Main box
    bmesh_add_box(bm, (0, 0, 0.55), (1.16, 1.16, 0.9), mat_idx=0)
    # X ribs
    bmesh_add_box(bm, (0, -0.585, 0.55), (1.0, 0.02, 0.75), mat_idx=0)
    # Hazard sign
    bmesh_add_box(bm, (0, -0.598, 0.6), (0.35, 0.01, 0.35), mat_idx=2)
    # Hazard stripe band
    bmesh_add_box(bm, (0, 0, 0.95), (1.18, 1.18, 0.08), mat_idx=1)
    return finalize_asset("WK_PROP_CRATE_A_01", bm, cols["07_PROPS"], [mats["steel"], mats["hazard"], mats["sign_hazard"]])

# 24. WK_PROP_CANISTER_A_01
def create_prop_canister(cols, mats):
    bm = bmesh.new()
    # Base ring
    bmesh_add_cylinder(bm, (0, 0, 0.04), radius=0.22, height=0.08, segments=16, axis="Z", mat_idx=0)
    # Cylinder tank
    bmesh_add_cylinder(bm, (0, 0, 0.65), radius=0.24, height=1.1, segments=16, axis="Z", mat_idx=0)
    # Roll cage
    for a in [0, math.pi*0.5, math.pi, math.pi*1.5]:
        rx, ry = math.cos(a)*0.26, math.sin(a)*0.26
        bmesh_add_cylinder(bm, (rx, ry, 1.3), radius=0.015, height=0.25, segments=8, axis="Z", mat_idx=0)
    # Brass regulator & valve
    bmesh_add_cylinder(bm, (0, 0, 1.28), radius=0.06, height=0.1, segments=12, axis="Z", mat_idx=1)
    bmesh_add_cylinder(bm, (0.08, 0, 1.28), radius=0.04, height=0.04, segments=8, axis="X", mat_idx=1)
    # Hazard band
    bmesh_add_cylinder(bm, (0, 0, 0.65), radius=0.245, height=0.2, segments=16, axis="Z", mat_idx=2)
    return finalize_asset("WK_PROP_CANISTER_A_01", bm, cols["07_PROPS"], [mats["steel"], mats["brass"], mats["hazard"]])

# 25. WK_PROP_JUNCTION_A_01
def create_prop_junction(cols, mats):
    bm = bmesh.new()
    # Main enclosure
    bmesh_add_box(bm, (0, 0.15, 0), (0.58, 0.28, 0.78), mat_idx=0)
    # Door
    bmesh_add_box(bm, (0, 0.30, 0), (0.56, 0.02, 0.76), mat_idx=0)
    # Disconnect handle
    bmesh_add_cylinder(bm, (0.31, 0.18, 0.1), radius=0.02, height=0.08, segments=8, axis="X", mat_idx=2)
    bmesh_add_box(bm, (0.36, 0.18, 0.18), (0.02, 0.04, 0.18), mat_idx=2)
    # Hazard sign on door
    bmesh_add_box(bm, (0, 0.312, 0.05), (0.28, 0.005, 0.28), mat_idx=1)
    return finalize_asset("WK_PROP_JUNCTION_A_01", bm, cols["07_PROPS"], [mats["steel"], mats["sign_hazard"], mats["brass"]])

# 26. WK_PROP_EXTINGUISHER_01
def create_prop_extinguisher(cols, mats):
    bm = bmesh.new()
    bmesh_add_box(bm, (0, 0.02, 0), (0.2, 0.02, 0.8), mat_idx=0)
    # Bottle
    bmesh_add_cylinder(bm, (0, 0.16, -0.05), radius=0.11, height=0.65, segments=16, axis="Z", mat_idx=0)
    # Brass top valve
    bmesh_add_cylinder(bm, (0, 0.16, 0.32), radius=0.04, height=0.08, segments=8, axis="Z", mat_idx=2)
    # Rubber hose
    bmesh_add_cylinder(bm, (0.12, 0.16, 0.1), radius=0.02, height=0.45, segments=8, axis="Z", mat_idx=1)
    return finalize_asset("WK_PROP_EXTINGUISHER_01", bm, cols["07_PROPS"], [mats["steel"], mats["rubber"], mats["brass"]])

# 27. WK_LIGHT_TROFFER_A_01
def create_light_troffer(cols, mats):
    bm = bmesh.new()
    bmesh_add_box(bm, (0, 0, -0.1), (2.0, 0.6, 0.2), mat_idx=0)
    bmesh_add_box(bm, (0, 0, -0.01), (2.1, 0.7, 0.02), mat_idx=0)
    bmesh_add_box(bm, (0, 0, -0.18), (1.9, 0.5, 0.02), mat_idx=1) # Glow lens
    return finalize_asset("WK_LIGHT_TROFFER_A_01", bm, cols["08_LIGHTS"], [mats["steel"], mats["light_glow"]])

# 28. WK_LIGHT_CAGE_A_01
def create_light_cage(cols, mats):
    bm = bmesh.new()
    bmesh_add_cylinder(bm, (0, 0, 0.03), radius=0.12, height=0.06, segments=12, axis="Z", mat_idx=0)
    bmesh_add_cylinder(bm, (0, 0, 0.2), radius=0.08, height=0.26, segments=16, axis="Z", mat_idx=1) # Glass
    bmesh_add_cylinder(bm, (0, 0, 0.2), radius=0.02, height=0.1, segments=8, axis="Z", mat_idx=2) # Filament glow
    # 4 cage bars
    for a in [0, math.pi*0.5, math.pi, math.pi*1.5]:
        cx, cy = math.cos(a)*0.09, math.sin(a)*0.09
        bmesh_add_cylinder(bm, (cx, cy, 0.2), radius=0.008, height=0.28, segments=6, axis="Z", mat_idx=0)
    return finalize_asset("WK_LIGHT_CAGE_A_01", bm, cols["08_LIGHTS"], [mats["steel"], mats["glass"], mats["light_glow"]])

# 29. WK_LIGHT_STROBE_A_01
def create_light_strobe(cols, mats):
    bm = bmesh.new()
    bmesh_add_cylinder(bm, (0, 0, 0.08), radius=0.08, height=0.16, segments=12, axis="Z", mat_idx=0)
    bmesh_add_cylinder(bm, (0, 0, 0.24), radius=0.09, height=0.18, segments=16, axis="Z", mat_idx=1) # Amber strobe
    bmesh_add_cylinder(bm, (0, 0, 0.34), radius=0.10, height=0.03, segments=12, axis="Z", mat_idx=0)
    return finalize_asset("WK_LIGHT_STROBE_A_01", bm, cols["08_LIGHTS"], [mats["steel"], mats["amber_strobe"]])

# 30. WK_SIGN_SECTOR_A_01
def create_sign_sector(cols, mats):
    bm = bmesh.new()
    for sx, sz in [(-0.8, -0.25), (0.8, -0.25), (-0.8, 0.25), (0.8, 0.25)]:
        bmesh_add_cylinder(bm, (sx, 0.04, sz), radius=0.02, height=0.08, segments=8, axis="Y", mat_idx=0)
    bmesh_add_box(bm, (0, 0.085, 0), (1.82, 0.02, 0.62), mat_idx=0)
    bmesh_add_box(bm, (0, 0.096, 0), (1.8, 0.005, 0.6), mat_idx=1) # Sign sector
    return finalize_asset("WK_SIGN_SECTOR_A_01", bm, cols["09_SIGNAGE"], [mats["steel"], mats["sign_sector"]])

# 31. WK_SIGN_HAZARD_A_01
def create_sign_hazard(cols, mats):
    bm = bmesh.new()
    bmesh_add_box(bm, (0, 0.01, 0), (0.6, 0.02, 0.52), mat_idx=0)
    return finalize_asset("WK_SIGN_HAZARD_A_01", bm, cols["09_SIGNAGE"], [mats["sign_hazard"]])

# 32. WK_UTIL_PIPE_RUN_A_01
def create_util_pipe_run(cols, mats):
    bm = bmesh.new()
    # 2 wall mounting brackets
    for bx in [-1.2, 1.2]:
        bmesh_add_box(bm, (bx, 0.04, 0), (0.12, 0.08, 0.4), mat_idx=0)
        bmesh_add_box(bm, (bx, 0.16, 0), (0.1, 0.16, 0.38), mat_idx=0)
    # 4 pipes
    bmesh_add_cylinder(bm, (0, 0.12, 0.10), radius=0.04, height=4.0, segments=12, axis="X", mat_idx=0)
    bmesh_add_cylinder(bm, (0, 0.12, -0.08), radius=0.035, height=4.0, segments=12, axis="X", mat_idx=0)
    bmesh_add_cylinder(bm, (0, 0.22, 0.05), radius=0.025, height=4.0, segments=12, axis="X", mat_idx=0)
    bmesh_add_cylinder(bm, (0, 0.22, -0.05), radius=0.02, height=4.0, segments=12, axis="X", mat_idx=2) # Rubber
    # Brass center valve
    bmesh_add_cylinder(bm, (0, 0.12, 0.10), radius=0.06, height=0.12, segments=8, axis="X", mat_idx=1)
    bmesh_add_cylinder(bm, (0, 0.20, 0.10), radius=0.12, height=0.03, segments=12, axis="Y", mat_idx=1)
    return finalize_asset("WK_UTIL_PIPE_RUN_A_01", bm, cols["11_DECALS"], [mats["steel"], mats["brass"], mats["rubber"]])

# 33. WK_HERO_CORE_A_01
def create_hero_core(cols, mats):
    bm = bmesh.new()
    # Octagonal base pedestal (Z in [0, 0.6])
    bmesh_add_cylinder(bm, (0, 0, 0.3), radius=1.8, height=0.6, segments=8, axis="Z", mat_idx=0)
    # Manifold ring with feeder pipes & valves
    bmesh_add_cylinder(bm, (0, 0, 0.7), radius=1.3, height=0.2, segments=16, axis="Z", mat_idx=0)
    for i in range(8):
        ang = i * math.pi * 0.25
        px, py = math.cos(ang)*1.4, math.sin(ang)*1.4
        bmesh_add_cylinder(bm, (px*0.9, py*0.9, 0.7), radius=0.06, height=0.4, segments=8, axis="Z", mat_idx=4)
    # Main compression chamber (Z in [0.8, 3.2])
    bmesh_add_cylinder(bm, (0, 0, 2.0), radius=1.0, height=2.4, segments=24, axis="Z", mat_idx=0)
    # Plasma observation band (Z in [1.7, 2.3])
    bmesh_add_cylinder(bm, (0, 0, 2.0), radius=1.02, height=0.6, segments=24, axis="Z", mat_idx=1) # Cyan plasma
    # 4 hydraulic stabilization struts
    for a in [math.pi*0.25, math.pi*0.75, math.pi*1.25, math.pi*1.75]:
        sx, sy = math.cos(a)*1.4, math.sin(a)*1.4
        bmesh_add_box(bm, (sx, sy, 1.6), (0.2, 0.2, 2.2), mat_idx=3) # Hazard
    # Confinement ring at top
    bmesh_add_cylinder(bm, (0, 0, 3.4), radius=1.2, height=0.25, segments=16, axis="Z", mat_idx=6) # Rubber
    # Tapered exhaust cowl (Z in [3.5, 4.4])
    bmesh_add_cylinder(bm, (0, 0, 3.9), radius=0.8, height=0.8, segments=8, axis="Z", mat_idx=0)
    # Crowning amber strobe
    bmesh_add_cylinder(bm, (0, 0, 4.5), radius=0.15, height=0.3, segments=12, axis="Z", mat_idx=5) # Amber
    return finalize_asset("WK_HERO_CORE_A_01", bm, cols["13_HERO"], 
                          [mats["steel"], mats["emissive_cyan"], mats["glass"], mats["hazard"], mats["brass"], mats["amber_strobe"], mats["rubber"]])

def build_all_assets():
    print("Building World Kit Asset Vocabulary...")
    clean_scene()
    cols = create_collections()
    mats = setup_materials()
    
    asset_builders = [
        create_wall_solid,
        create_wall_panel,
        create_wall_corner_in,
        create_wall_corner_out,
        create_wall_doorframe,
        create_wall_window,
        create_floor_slab,
        create_floor_grate,
        create_floor_catwalk,
        create_floor_trim,
        create_ceil_coffer,
        create_ceil_girder,
        create_door_bulkhead,
        create_door_slab,
        create_window_portal,
        create_struct_column,
        create_struct_beam,
        create_struct_stairs,
        create_struct_railing,
        create_struct_railing_2m,
        create_furn_console,
        create_furn_bench,
        create_prop_crate,
        create_prop_canister,
        create_prop_junction,
        create_prop_extinguisher,
        create_light_troffer,
        create_light_cage,
        create_light_strobe,
        create_sign_sector,
        create_sign_hazard,
        create_util_pipe_run,
        create_hero_core,
        create_hero_portal_ring,
    ]
    
    created_objects = []
    for builder in asset_builders:
        obj = builder(cols, mats)
        created_objects.append(obj)
        print(f"  [+] Built: {obj.name} (verts: {len(obj.data.vertices)}, faces: {len(obj.data.polygons)})")
        
    print(f"\nTotal assets generated: {len(created_objects)}")
    
    # Save blend file
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUTPUT)
    print(f"Saved master file: {BLEND_OUTPUT}")
    return created_objects

# 34. WK_HERO_PORTAL_RING_A_01 (Colossal Stargate Style Singularity Portal Reactor)
def create_hero_portal_ring(cols, mats):
    bm = bmesh.new()
    
    # 1. Heavy Base Pedestal Cradle (Concrete + Steel) at Z in [0, 1.2]
    bmesh_add_box(bm, (0, 0, 0.3), (6.0, 2.2, 0.6), mat_idx=0) # Concrete base
    bmesh_add_box(bm, (0, 0, 0.8), (5.2, 1.8, 0.4), mat_idx=1) # Steel upper cradle
    
    # 2. Dual Hydraulic Cradle Support Rams on left and right
    for sx in [-2.2, 2.2]:
        bmesh_add_box(bm, (sx, 0, 1.8), (0.6, 1.2, 1.6), mat_idx=1)
        bmesh_add_cylinder(bm, (sx, 0, 2.4), radius=0.15, height=1.4, segments=12, axis="Z", mat_idx=3) # Hazard
        
    # 3. Outer Stator Torus Ring (Diameter 6.4m, radius 3.2m, centered at Z=3.8m)
    # Built using 32 faceted segments
    num_segs = 32
    r_center = 3.2
    ring_thick_y = 0.8
    ring_width_r = 0.45
    center_z = 3.8
    
    for i in range(num_segs):
        a1 = i * (2.0 * math.pi / num_segs)
        a2 = (i + 1) * (2.0 * math.pi / num_segs)
        
        # Segment center
        amid = (a1 + a2) * 0.5
        x_mid = math.sin(amid) * r_center
        z_mid = center_z + math.cos(amid) * r_center
        
        # Length of segment
        seg_len = 2.0 * r_center * math.sin(math.pi / num_segs)
        
        # We can create a box segment oriented along tangent
        # Tangent angle
        rot_ang = amid + math.pi*0.5
        # Add box
        bmesh_add_box(bm, (x_mid, 0, z_mid), (seg_len * 1.05, ring_thick_y, ring_width_r), mat_idx=1)
        
    # 4. 9 Chevron Lock Clamps around perimeter
    # Chevrons are situated at 9 radial points
    for c_idx in range(9):
        ang = c_idx * (2.0 * math.pi / 9.0) - math.pi*0.5
        cx = math.cos(ang) * 3.35
        cz = center_z + math.sin(ang) * 3.35
        
        # Chevron housing
        bmesh_add_box(bm, (cx, 0, cz), (0.5, 1.0, 0.5), mat_idx=1)
        # Chevron indicator light (Amber)
        bmesh_add_box(bm, (cx * 0.95, -0.52, cz), (0.25, 0.05, 0.25), mat_idx=5) # Amber Strobe
        # Chevron side clamp teeth (Hazard)
        bmesh_add_box(bm, (cx * 0.98, 0, cz), (0.4, 1.1, 0.2), mat_idx=3)
        
    # 5. Inner Stepped Glyph / Rotor Track (radius 2.3m to 2.7m)
    for i in range(24):
        ang = i * (2.0 * math.pi / 24.0)
        gx = math.cos(ang) * 2.5
        gz = center_z + math.sin(ang) * 2.5
        bmesh_add_box(bm, (gx, 0, gz), (0.35, 0.6, 0.25), mat_idx=4) # Brass / Rotor
        
    # 6. Quantum Event Horizon Vortex Disc (radius 2.3m, facing Y)
    # Circle disc of glowing cyan plasma at Y = 0.0
    bmesh_add_cylinder(bm, (0, 0, center_z), radius=2.3, height=0.08, segments=32, axis="Y", mat_idx=2) # Cyan Plasma
    
    # 7. Heavy Coolant Feeder Conduits (Black Rubber)
    for fx in [-1.5, 1.5]:
        bmesh_add_cylinder(bm, (fx, 0.6, 1.5), radius=0.10, height=2.4, segments=12, axis="Z", mat_idx=6)
        bmesh_add_cylinder(bm, (fx, -0.6, 1.5), radius=0.10, height=2.4, segments=12, axis="Z", mat_idx=6)
    return finalize_asset("WK_HERO_PORTAL_RING_A_01", bm, cols["13_HERO"],
                          [mats["concrete"], mats["steel"], mats["emissive_cyan"], mats["hazard"], mats["brass"], mats["amber_strobe"], mats["rubber"]])

if __name__ == "__main__":
    build_all_assets()
