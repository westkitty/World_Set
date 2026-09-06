import bpy
import bmesh
import math
import os
from mathutils import Vector, Euler, Matrix

TEXTURE_DIR = "/Users/andrew/World_Set/textures"

def clean_scene():
    """Wipe default objects and prepare clean database."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # Ensure view layer exists
    if not bpy.context.scene.view_layers:
        bpy.context.scene.view_layers.new(name="ViewLayer")

def create_collections():
    """Create canonical World Kit collections."""
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
    """Create canonical PBR materials with textures and nodes."""
    materials = {}
    
    def load_or_create_image(filename):
        path = os.path.join(TEXTURE_DIR, filename)
        if os.path.exists(path):
            return bpy.data.images.load(path)
        return None

    # Helper to create Principled BSDF material
    def new_pbr_material(name):
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes.clear()
        
        output = nodes.new("ShaderNodeOutputMaterial")
        output.location = (400, 0)
        
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
        bsdf.location = (0, 0)
        mat.node_tree.links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
        return mat, nodes, bsdf

    # 1. MAT_Concrete_Brutalist
    mat, nodes, bsdf = new_pbr_material("MAT_Concrete_Brutalist")
    alb = load_or_create_image("tex_concrete_albedo.png")
    if alb:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = alb
        tex_node.location = (-400, 100)
        mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = (0.35, 0.37, 0.38, 1.0)
    
    rgh = load_or_create_image("tex_concrete_roughness.png")
    if rgh:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = rgh
        tex_node.image.colorspace_settings.name = "Non-Color"
        tex_node.location = (-400, -150)
        mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Roughness"])
    else:
        bsdf.inputs["Roughness"].default_value = 0.85
        
    nrm = load_or_create_image("tex_concrete_normal.png")
    if nrm:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = nrm
        tex_node.image.colorspace_settings.name = "Non-Color"
        tex_node.location = (-600, -350)
        norm_map = nodes.new("ShaderNodeNormalMap")
        norm_map.location = (-250, -350)
        norm_map.inputs["Strength"].default_value = 1.0
        mat.node_tree.links.new(tex_node.outputs["Color"], norm_map.inputs["Color"])
        mat.node_tree.links.new(norm_map.outputs["Normal"], bsdf.inputs["Normal"])
        
    bsdf.inputs["Metallic"].default_value = 0.0
    materials["concrete"] = mat

    # 2. MAT_Heavy_Steel_Painted
    mat, nodes, bsdf = new_pbr_material("MAT_Heavy_Steel_Painted")
    alb = load_or_create_image("tex_steel_albedo.png")
    if alb:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = alb
        tex_node.location = (-400, 100)
        mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = (0.22, 0.25, 0.23, 1.0)
        
    rgh = load_or_create_image("tex_steel_roughness.png")
    if rgh:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = rgh
        tex_node.image.colorspace_settings.name = "Non-Color"
        tex_node.location = (-400, -150)
        mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Roughness"])
    else:
        bsdf.inputs["Roughness"].default_value = 0.55
        
    met = load_or_create_image("tex_steel_metallic.png")
    if met:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = met
        tex_node.image.colorspace_settings.name = "Non-Color"
        tex_node.location = (-400, -350)
        mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Metallic"])
    else:
        bsdf.inputs["Metallic"].default_value = 0.2
        
    nrm = load_or_create_image("tex_steel_normal.png")
    if nrm:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = nrm
        tex_node.image.colorspace_settings.name = "Non-Color"
        tex_node.location = (-600, -550)
        norm_map = nodes.new("ShaderNodeNormalMap")
        norm_map.location = (-250, -550)
        norm_map.inputs["Strength"].default_value = 1.2
        mat.node_tree.links.new(tex_node.outputs["Color"], norm_map.inputs["Color"])
        mat.node_tree.links.new(norm_map.outputs["Normal"], bsdf.inputs["Normal"])
    materials["steel"] = mat

    # 3. MAT_Galvanized_Grate
    mat, nodes, bsdf = new_pbr_material("MAT_Galvanized_Grate")
    alb = load_or_create_image("tex_grate_albedo.png")
    if alb:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = alb
        tex_node.location = (-400, 100)
        mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = (0.45, 0.48, 0.50, 1.0)
    rgh = load_or_create_image("tex_grate_roughness.png")
    if rgh:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = rgh
        tex_node.image.colorspace_settings.name = "Non-Color"
        tex_node.location = (-400, -150)
        mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Roughness"])
    met = load_or_create_image("tex_grate_metallic.png")
    if met:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = met
        tex_node.image.colorspace_settings.name = "Non-Color"
        tex_node.location = (-400, -350)
        mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Metallic"])
    materials["grate"] = mat

    # 4. MAT_Reinforced_Glass
    mat, nodes, bsdf = new_pbr_material("MAT_Reinforced_Glass")
    bsdf.inputs["Base Color"].default_value = (0.1, 0.28, 0.24, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.12
    if "Transmission Weight" in bsdf.inputs:
        bsdf.inputs["Transmission Weight"].default_value = 0.85
    elif "Transmission" in bsdf.inputs:
        bsdf.inputs["Transmission"].default_value = 0.85
    bsdf.inputs["IOR"].default_value = 1.52
    mat.blend_method = "BLEND" if hasattr(mat, "blend_method") else "OPAQUE"
    materials["glass"] = mat

    # 5. MAT_Rubber_Conduit
    mat, nodes, bsdf = new_pbr_material("MAT_Rubber_Conduit")
    bsdf.inputs["Base Color"].default_value = (0.12, 0.13, 0.14, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.72
    bsdf.inputs["Metallic"].default_value = 0.0
    materials["rubber"] = mat

    # 6. MAT_Emissive_Cyan_UI
    mat, nodes, bsdf = new_pbr_material("MAT_Emissive_Cyan_UI")
    screen_img = load_or_create_image("tex_screen_cyan.png")
    if screen_img:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = screen_img
        tex_node.location = (-400, 100)
        mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
        if "Emission Color" in bsdf.inputs:
            mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Emission Color"])
            bsdf.inputs["Emission Strength"].default_value = 5.0
        elif "Emission" in bsdf.inputs:
            mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Emission"])
    else:
        bsdf.inputs["Base Color"].default_value = (0.1, 0.9, 1.0, 1.0)
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (0.1, 0.9, 1.0, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 5.0
    materials["emissive_cyan"] = mat

    # 7. MAT_Hazard_Stripes
    mat, nodes, bsdf = new_pbr_material("MAT_Hazard_Stripes")
    hz_img = load_or_create_image("tex_hazard_albedo.png")
    if hz_img:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = hz_img
        tex_node.location = (-400, 100)
        mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
    else:
        bsdf.inputs["Base Color"].default_value = (0.95, 0.72, 0.0, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.65
    materials["hazard"] = mat

    # 8. MAT_Sign_Sector
    mat, nodes, bsdf = new_pbr_material("MAT_Sign_Sector")
    sgn_img = load_or_create_image("tex_sign_sector.png")
    if sgn_img:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = sgn_img
        tex_node.location = (-400, 100)
        mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
        if "Emission Color" in bsdf.inputs:
            mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Emission Color"])
            bsdf.inputs["Emission Strength"].default_value = 1.0
    materials["sign_sector"] = mat

    # 9. MAT_Sign_Hazard
    mat, nodes, bsdf = new_pbr_material("MAT_Sign_Hazard")
    haz_img = load_or_create_image("tex_sign_hazard.png")
    if haz_img:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.image = haz_img
        tex_node.location = (-400, 100)
        mat.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
    materials["sign_hazard"] = mat

    # 10. MAT_Brass_Valves
    mat, nodes, bsdf = new_pbr_material("MAT_Brass_Valves")
    bsdf.inputs["Base Color"].default_value = (0.82, 0.65, 0.28, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.95
    bsdf.inputs["Roughness"].default_value = 0.32
    materials["brass"] = mat

    # 11. MAT_Amber_Strobe
    mat, nodes, bsdf = new_pbr_material("MAT_Amber_Strobe")
    bsdf.inputs["Base Color"].default_value = (1.0, 0.6, 0.05, 1.0)
    if "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (1.0, 0.6, 0.05, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 8.0
    materials["amber_strobe"] = mat

    # 12. MAT_Fluorescent_Glow
    mat, nodes, bsdf = new_pbr_material("MAT_Fluorescent_Glow")
    bsdf.inputs["Base Color"].default_value = (0.85, 0.95, 1.0, 1.0)
    if "Emission Color" in bsdf.inputs:
        bsdf.inputs["Emission Color"].default_value = (0.85, 0.95, 1.0, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 6.0
    materials["light_glow"] = mat

    return materials

print("Materials module initialized successfully.")
