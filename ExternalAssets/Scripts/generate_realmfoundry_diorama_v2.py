import bpy
import math
import os
import random
from mathutils import Vector


ROOT = r"D:\CodexGames\RealmFoundry\ExternalAssets\DioramaV2"
BLEND_PATH = os.path.join(ROOT, "RF_DioramaV2.blend")
PREVIEW_PATH = os.path.join(ROOT, "RF_DioramaV2_Preview.png")
EXPORT_PATH = os.path.join(ROOT, "Exports", "RF_TownDiorama_V2.fbx")
COLLECTION_NAME = "RF_DIORAMA_V2"
random.seed(240819)
os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)


def remove_collection(name):
    col = bpy.data.collections.get(name)
    if not col:
        return
    for obj in list(col.all_objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.collections.remove(col)


remove_collection(COLLECTION_NAME)
root = bpy.data.collections.new(COLLECTION_NAME)
bpy.context.scene.collection.children.link(root)

# Keep the previous library in the source file but out of this render/export.
for col in bpy.context.scene.collection.children:
    col.hide_render = col != root
    col.hide_viewport = col != root


def mat(name, color, rough=0.7, metallic=0.0, emission=None, strength=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1.0)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metallic
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = strength
    return m


M = {
    "grass": mat("RF2_Grass", (0.13, 0.31, 0.16), 0.92),
    "grass2": mat("RF2_GrassLight", (0.25, 0.48, 0.21), 0.92),
    "earth": mat("RF2_Earth", (0.20, 0.105, 0.055), 1.0),
    "road": mat("RF2_Road", (0.43, 0.31, 0.20), 0.96),
    "stone": mat("RF2_Stone", (0.34, 0.37, 0.39), 0.88),
    "stone2": mat("RF2_StoneWarm", (0.50, 0.45, 0.36), 0.91),
    "plaster": mat("RF2_Plaster", (0.77, 0.67, 0.49), 0.84),
    "plaster_red": mat("RF2_PlasterRed", (0.47, 0.16, 0.12), 0.82),
    "wood": mat("RF2_Wood", (0.18, 0.075, 0.027), 0.86),
    "wood2": mat("RF2_WoodWarm", (0.39, 0.16, 0.055), 0.82),
    "roof": mat("RF2_Roof", (0.075, 0.095, 0.115), 0.72),
    "roof_red": mat("RF2_RoofRed", (0.33, 0.085, 0.055), 0.78),
    "gold": mat("RF2_Gold", (0.78, 0.46, 0.09), 0.28, 0.72),
    "metal": mat("RF2_Metal", (0.08, 0.10, 0.12), 0.28, 0.82),
    "water": mat("RF2_Water", (0.035, 0.23, 0.31), 0.18, 0.08, (0.02, 0.16, 0.20), 0.3),
    "glass": mat("RF2_Window", (0.18, 0.42, 0.55), 0.2, 0.1, (1.0, 0.46, 0.10), 4.0),
    "magic": mat("RF2_Magic", (0.10, 0.32, 0.42), 0.15, 0.15, (0.06, 0.65, 1.0), 8.0),
    "purple": mat("RF2_Purple", (0.25, 0.07, 0.34), 0.48, 0.08, (0.35, 0.03, 0.75), 0.5),
    "leaf": mat("RF2_Leaf", (0.07, 0.24, 0.105), 0.94),
    "leaf2": mat("RF2_LeafGold", (0.47, 0.25, 0.055), 0.91),
    "cloth_blue": mat("RF2_ClothBlue", (0.04, 0.18, 0.34), 0.91),
    "cloth_red": mat("RF2_ClothRed", (0.43, 0.06, 0.055), 0.91),
    "skin": mat("RF2_Skin", (0.52, 0.27, 0.15), 0.82),
}


def move_to_root(obj):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    root.objects.link(obj)
    return obj


def box(name, loc, scale, material, bevel=0.12, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = move_to_root(bpy.context.object)
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = o.modifiers.new("SoftEdges", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    o.data.materials.append(material)
    return o


def cyl(name, loc, radius, depth, material, vertices=16, rot=(0, 0, 0), bevel=0.08):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc, rotation=rot)
    o = move_to_root(bpy.context.object)
    o.name = name
    if bevel:
        mod = o.modifiers.new("SoftEdges", "BEVEL")
        mod.width = bevel
        mod.segments = 2
    o.data.materials.append(material)
    return o


def sphere(name, loc, scale, material, segments=16, rings=8):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    o = move_to_root(bpy.context.object)
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    return o


def cone(name, loc, r1, r2, depth, material, vertices=16, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    o = move_to_root(bpy.context.object)
    o.name = name
    o.data.materials.append(material)
    return o


def prism_roof(name, loc, width, depth, height, material, rot_z=0):
    verts = [
        (-width / 2, -depth / 2, 0), (width / 2, -depth / 2, 0),
        (-width / 2, depth / 2, 0), (width / 2, depth / 2, 0),
        (0, -depth / 2, height), (0, depth / 2, height),
    ]
    faces = [(0, 1, 4), (2, 5, 3), (0, 2, 3, 1), (0, 4, 5, 2), (1, 3, 5, 4)]
    mesh = bpy.data.meshes.new(name + "_Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    o = bpy.data.objects.new(name, mesh)
    root.objects.link(o)
    o.location = loc
    o.rotation_euler.z = rot_z
    mod = o.modifiers.new("RoofEdge", "BEVEL")
    mod.width = 0.09
    mod.segments = 2
    o.data.materials.append(material)
    return o


def beam_frame(prefix, center, sx, sy, base_z, top_z, rot_z=0):
    cx, cy = center
    for side in (-1, 1):
        for along in (-1, 1):
            x = cx + side * sx
            y = cy + along * sy
            box(prefix + "_Post", (x, y, (base_z + top_z) / 2), (0.11, 0.11, (top_z - base_z) / 2), M["wood"], 0.04, (0, 0, rot_z))
    box(prefix + "_TopBeam", (cx, cy - sy, top_z), (sx + 0.16, 0.10, 0.10), M["wood"], 0.035, (0, 0, rot_z))
    box(prefix + "_TopBeam", (cx, cy + sy, top_z), (sx + 0.16, 0.10, 0.10), M["wood"], 0.035, (0, 0, rot_z))


def window(prefix, loc, scale=(0.34, 0.09, 0.46), rot_z=0):
    box(prefix + "_Frame", loc, (scale[0] + 0.10, scale[1] + 0.03, scale[2] + 0.10), M["wood"], 0.04, (0, 0, rot_z))
    glass = box(prefix + "_Glow", (loc[0], loc[1] - 0.025, loc[2]), scale, M["glass"], 0.03, (0, 0, rot_z))
    return glass


def door(prefix, loc, width=0.55, height=1.05, rot_z=0):
    box(prefix + "_Door", loc, (width, 0.10, height), M["wood2"], 0.10, (0, 0, rot_z))
    box(prefix + "_Lintel", (loc[0], loc[1] - 0.02, loc[2] + height + 0.12), (width + 0.12, 0.14, 0.12), M["stone2"], 0.06, (0, 0, rot_z))
    cyl(prefix + "_Knob", (loc[0] + width * 0.55, loc[1] - 0.13, loc[2]), 0.055, 0.10, M["gold"], 12, (math.pi / 2, 0, 0), 0)


def chimney(prefix, loc, height=1.8):
    box(prefix + "_Stack", (loc[0], loc[1], loc[2] + height / 2), (0.32, 0.28, height / 2), M["stone"], 0.08)
    box(prefix + "_Cap", (loc[0], loc[1], loc[2] + height), (0.42, 0.38, 0.12), M["stone2"], 0.05)


def sign(prefix, loc, icon="mug"):
    box(prefix + "_Bracket", (loc[0], loc[1], loc[2] + 0.35), (0.08, 0.08, 0.55), M["metal"], 0.03)
    box(prefix + "_Arm", (loc[0] + 0.45, loc[1], loc[2] + 0.82), (0.5, 0.07, 0.07), M["metal"], 0.03)
    board = box(prefix + "_Board", (loc[0] + 0.78, loc[1], loc[2] + 0.35), (0.40, 0.08, 0.38), M["wood2"], 0.11)
    if icon == "mug":
        cyl(prefix + "_Icon", (loc[0] + 0.78, loc[1] - 0.10, loc[2] + 0.35), 0.15, 0.05, M["gold"], 12, (math.pi / 2, 0, 0), 0)
    elif icon == "hammer":
        box(prefix + "_Icon", (loc[0] + 0.78, loc[1] - 0.11, loc[2] + 0.35), (0.06, 0.03, 0.25), M["gold"], 0.02, (0, 0, -0.55))
        box(prefix + "_IconHead", (loc[0] + 0.88, loc[1] - 0.11, loc[2] + 0.52), (0.18, 0.04, 0.07), M["gold"], 0.02, (0, 0, -0.55))
    return board


def timber_building(prefix, center, size=(3.2, 2.6), floors=2, roof_mat=None, plaster=None):
    x, y = center
    sx, sy = size
    plaster = plaster or M["plaster"]
    roof_mat = roof_mat or M["roof_red"]
    box(prefix + "_Foundation", (x, y, 0.32), (sx + 0.22, sy + 0.22, 0.32), M["stone"], 0.16)
    box(prefix + "_Lower", (x, y, 1.15), (sx, sy, 0.82), plaster, 0.13)
    upper_z = 2.42 if floors > 1 else 1.6
    if floors > 1:
        box(prefix + "_Upper", (x, y, 2.35), (sx + 0.28, sy + 0.18, 0.58), plaster, 0.12)
        beam_frame(prefix, center, sx + 0.25, sy + 0.15, 1.78, 2.95)
    beam_frame(prefix, center, sx, sy, 0.42, 1.95)
    roof_z = 3.0 if floors > 1 else 2.05
    prism_roof(prefix + "_Roof", (x, y, roof_z), (sx + 0.65) * 2, (sy + 0.6) * 2, 1.55, roof_mat)
    # Tile ridges and bargeboards give the silhouette a crafted finish.
    box(prefix + "_Ridge", (x, y, roof_z + 1.5), (0.10, sy + 0.72, 0.10), M["gold"], 0.04)
    for dx in (-sx * 0.55, sx * 0.55):
        window(prefix, (x + dx, y - sy - 0.12, 2.38 if floors > 1 else 1.3), (0.34, 0.075, 0.40))
    window(prefix, (x, y - sy - 0.13, 2.38 if floors > 1 else 1.35), (0.38, 0.075, 0.42))
    door(prefix, (x, y - sy - 0.16, 1.10), 0.55, 1.02)
    chimney(prefix, (x + sx * 0.55, y + sy * 0.34, roof_z + 0.35), 1.65)
    return (x, y, roof_z + 1.55)


def build_grand_inn():
    x, y = -4.4, -1.0
    timber_building("Inn", (x, y), (3.1, 2.15), 2, M["roof_red"], M["plaster"])
    timber_building("InnWing", (x - 3.4, y + 0.65), (1.45, 1.55), 1, M["roof"], M["plaster_red"])
    # Deep front porch, steps, balcony and readable service sign.
    box("Inn_Porch", (x, y - 2.62, 0.38), (2.25, 0.72, 0.18), M["wood2"], 0.10)
    for px in (x - 1.75, x + 1.75):
        box("Inn_PorchPost", (px, y - 2.95, 1.28), (0.12, 0.12, 0.92), M["wood"], 0.04)
    prism_roof("Inn_PorchRoof", (x, y - 2.82, 2.15), 4.7, 1.75, 0.68, M["roof"])
    box("Inn_Balcony", (x, y - 2.34, 2.12), (1.35, 0.25, 0.10), M["wood2"], 0.04)
    for bx in (-1.15, -0.55, 0.0, 0.55, 1.15):
        box("Inn_Baluster", (x + bx, y - 2.57, 2.47), (0.05, 0.05, 0.32), M["wood"], 0.02)
    box("Inn_Rail", (x, y - 2.57, 2.76), (1.35, 0.06, 0.07), M["wood"], 0.02)
    sign("Inn", (x + 2.35, y - 2.45, 1.7), "mug")
    for i in range(5):
        box("Inn_Step", (x, y - 3.35 - i * 0.13, 0.19 - i * 0.04), (0.85 + i * 0.10, 0.22, 0.07), M["stone2"], 0.04)


def build_smithy():
    x, y = 4.8, -1.4
    timber_building("Smithy", (x, y), (2.55, 1.95), 1, M["roof"], M["stone2"])
    box("Smithy_OpenForge", (x - 1.35, y - 2.18, 1.06), (1.0, 0.44, 0.82), M["stone"], 0.10)
    box("Smithy_Embers", (x - 1.35, y - 2.65, 0.84), (0.72, 0.10, 0.18), M["glass"], 0.06)
    chimney("Smithy_ForgeChimney", (x - 1.55, y - 0.55, 1.55), 2.9)
    sign("Smithy", (x + 1.75, y - 2.05, 1.55), "hammer")
    # Anvil, cooling barrel, stacked ingots.
    box("Smithy_AnvilBase", (x + 0.55, y - 2.65, 0.55), (0.18, 0.22, 0.45), M["wood"], 0.04)
    box("Smithy_Anvil", (x + 0.55, y - 2.65, 1.02), (0.48, 0.22, 0.15), M["metal"], 0.08)
    cone("Smithy_AnvilHorn", (x + 1.03, y - 2.65, 1.02), 0.18, 0.03, 0.55, M["metal"], 12, (0, math.pi / 2, 0))
    cyl("Smithy_Barrel", (x + 1.6, y - 2.75, 0.55), 0.42, 0.9, M["wood2"], 16, bevel=0.06)
    for z in (0.26, 0.76):
        cyl("Smithy_BarrelBand", (x + 1.6, y - 2.75, z + 0.1), 0.44, 0.08, M["metal"], 16, bevel=0.02)
    for i in range(4):
        box("Smithy_Ingot", (x - 0.2 + i * 0.25, y - 2.83, 0.36 + (i % 2) * 0.15), (0.20, 0.08, 0.08), M["gold"], 0.035)


def build_arcane_uplink():
    x, y = 2.3, 5.0
    cyl("Uplink_Base", (x, y, 0.42), 2.65, 0.84, M["stone"], 12, bevel=0.12)
    cyl("Uplink_Tower", (x, y, 2.55), 1.62, 4.25, M["plaster_red"], 12, bevel=0.10)
    for z in (0.78, 2.0, 3.5, 4.65):
        cyl("Uplink_Band", (x, y, z), 1.78 if z < 4 else 1.66, 0.18, M["stone2"], 12, bevel=0.04)
    for ang in range(0, 360, 60):
        a = math.radians(ang)
        window("Uplink", (x + math.sin(a) * 1.46, y - math.cos(a) * 1.46, 2.55), (0.28, 0.08, 0.54), a)
    cone("Uplink_Roof", (x, y, 5.35), 2.18, 0.14, 2.2, M["roof"], 12)
    cyl("Uplink_Spire", (x, y, 6.68), 0.10, 1.05, M["gold"], 12)
    sphere("Uplink_Crystal", (x, y, 7.42), (0.48, 0.48, 0.78), M["magic"], 12, 6)
    for ang in range(0, 360, 90):
        a = math.radians(ang)
        px, py = x + math.cos(a) * 2.05, y + math.sin(a) * 2.05
        cyl("Uplink_Pylon", (px, py, 1.0), 0.18, 1.8, M["stone2"], 8)
        sphere("Uplink_Rune", (px, py, 2.08), (0.24, 0.24, 0.34), M["magic"], 12, 6)
        box("Uplink_Arc", ((px + x) / 2, (py + y) / 2, 2.0), (0.045, 1.0, 0.045), M["magic"], 0.02, (0, 0, a - math.pi / 2))


def build_guildhall():
    x, y = -3.7, 5.6
    timber_building("Guild", (x, y), (3.45, 2.35), 2, M["roof"], M["plaster"])
    # Twin turrets and a heraldic entrance.
    for tx in (x - 3.1, x + 3.1):
        cyl("Guild_Turret", (tx, y, 1.65), 0.82, 3.3, M["stone"], 12, bevel=0.08)
        cone("Guild_TurretRoof", (tx, y, 3.85), 1.16, 0.05, 1.8, M["roof_red"], 12)
        sphere("Guild_Finial", (tx, y, 4.82), (0.14, 0.14, 0.22), M["gold"], 10, 5)
    box("Guild_Canopy", (x, y - 2.65, 2.25), (1.2, 0.48, 0.15), M["cloth_blue"], 0.10, (0.10, 0, 0))
    for sx in (-0.72, 0.72):
        box("Guild_Banner", (x + sx, y - 2.72, 2.78), (0.25, 0.04, 0.72), M["cloth_blue"], 0.03)
        cone("Guild_BannerTip", (x + sx, y - 2.72, 1.98), 0.25, 0, 0.30, M["cloth_blue"], 3)


def build_dungeon_gate():
    x, y = 7.6, 5.8
    # Stone mound and ruined arch around a magical doorway.
    for i, (dx, dy, s) in enumerate([(-1.8, .2, 1.2), (1.8, .1, 1.25), (-1.2, .8, .8), (1.1, .9, .85)]):
        sphere("Dungeon_Rock", (x + dx, y + dy, 0.55), (s, s * .8, .72), M["stone"], 12, 6)
    box("Dungeon_LeftPier", (x - 1.25, y, 1.65), (0.58, 0.68, 1.65), M["stone2"], 0.18)
    box("Dungeon_RightPier", (x + 1.25, y, 1.65), (0.58, 0.68, 1.65), M["stone2"], 0.18)
    box("Dungeon_Lintel", (x, y, 3.05), (1.85, 0.72, 0.48), M["stone2"], 0.16)
    box("Dungeon_Portal", (x, y - 0.72, 1.65), (0.78, 0.08, 1.28), M["purple"], 0.32)
    for z in (0.65, 1.65, 2.65):
        sphere("Dungeon_Rune", (x - 1.28, y - 0.71, z), (.13, .07, .13), M["magic"], 10, 5)
        sphere("Dungeon_Rune", (x + 1.28, y - 0.71, z), (.13, .07, .13), M["magic"], 10, 5)
    for i in range(7):
        box("Dungeon_Step", (x, y - 1.25 - i * .32, .34 - i * .03), (1.42 + i * .10, .24, .12), M["stone"], .06)


def build_travel_dock():
    x, y = -8.0, 6.2
    # Airship terminal with balloon and gold route beacon.
    cyl("Travel_Tower", (x, y, 1.25), 1.05, 2.5, M["stone"], 12, bevel=.1)
    cone("Travel_Roof", (x, y, 3.0), 1.45, .15, 1.5, M["roof_red"], 12)
    box("Travel_Platform", (x, y - 1.55, 1.55), (2.3, .75, .16), M["wood2"], .08)
    for px in (x - 2.0, x + 2.0):
        box("Travel_Post", (px, y - 1.55, .9), (.11, .11, .8), M["wood"], .04)
    sphere("Travel_Balloon", (x, y - 3.1, 4.2), (1.55, 1.25, 2.05), M["cloth_blue"], 20, 12)
    cyl("Travel_BalloonBand", (x, y - 3.1, 4.2), 1.38, .12, M["gold"], 20)
    box("Travel_Gondola", (x, y - 3.1, 2.05), (1.15, .65, .38), M["wood2"], .12)
    for dx in (-.82, .82):
        box("Travel_Rope", (x + dx, y - 3.1, 3.05), (.025, .025, 1.0), M["metal"], .01)
    sphere("Travel_Beacon", (x, y, 4.55), (.30, .30, .42), M["magic"], 12, 6)


def add_island():
    # Hand-shaped raised island, cliff skirt, village plateau, waterways and plaza.
    verts_top = []
    verts_bot = []
    n = 64
    for i in range(n):
        a = 2 * math.pi * i / n
        r = 15.5 + math.sin(a * 3) * 1.4 + math.sin(a * 7) * .7
        verts_top.append((math.cos(a) * r, math.sin(a) * r * .78, 0.0))
        verts_bot.append((math.cos(a) * (r + .7), math.sin(a) * (r + .7) * .80, -2.4))
    verts = verts_top + verts_bot + [(0, 0, 0), (0, 0, -2.4)]
    faces = []
    top_c, bot_c = n * 2, n * 2 + 1
    for i in range(n):
        j = (i + 1) % n
        faces.append((top_c, i, j))
        faces.append((bot_c, n + j, n + i))
        faces.append((i, n + i, n + j, j))
    mesh = bpy.data.meshes.new("RF2_IslandMesh")
    mesh.from_pydata(verts, [], faces)
    mesh.materials.append(M["grass"])
    island = bpy.data.objects.new("RF2_Island", mesh)
    root.objects.link(island)
    bevel = island.modifiers.new("IslandSoft", "BEVEL")
    bevel.width = .35
    bevel.segments = 3
    # Water plane below and shallow inset river strips.
    cyl("RF2_WaterPlane", (0, 0, -2.45), 24, .18, M["water"], 64, bevel=.02)
    # Central plaza with layered circular stonework.
    cyl("RF2_Plaza", (0, 0.8, .12), 4.0, .22, M["stone2"], 32, bevel=.15)
    cyl("RF2_PlazaInset", (0, .8, .25), 2.45, .10, M["road"], 32, bevel=.06)
    # Roads as broad beveled curves.
    road_points = [
        [(-4.4, -3.4, .25), (-3.0, -1.0, .25), (-1.0, .6, .25), (0, .8, .25)],
        [(4.8, -3.4, .25), (3.2, -1.1, .25), (1.4, .3, .25), (0, .8, .25)],
        [(0, .8, .25), (1.2, 2.8, .25), (2.3, 4.2, .25), (2.3, 5.0, .25)],
        [(0, .8, .25), (-1.8, 3.0, .25), (-3.7, 4.8, .25), (-3.7, 5.6, .25)],
        [(2.2, 2.1, .25), (4.2, 3.4, .25), (6.2, 4.6, .25), (7.6, 5.8, .25)],
        [(-2.3, 2.8, .25), (-4.5, 4.0, .25), (-6.4, 5.0, .25), (-8.0, 6.2, .25)],
    ]
    for idx, pts in enumerate(road_points):
        curve = bpy.data.curves.new(f"RF2_RoadCurve_{idx}", "CURVE")
        curve.dimensions = "3D"
        curve.bevel_depth = .48
        curve.bevel_resolution = 3
        spl = curve.splines.new("BEZIER")
        spl.bezier_points.add(len(pts) - 1)
        for bp, co in zip(spl.bezier_points, pts):
            bp.co = co
            bp.handle_left_type = "AUTO"
            bp.handle_right_type = "AUTO"
        obj = bpy.data.objects.new(f"RF2_Road_{idx}", curve)
        root.objects.link(obj)
        obj.data.materials.append(M["road"])


def tree(name, loc, scale=1.0, autumn=False):
    x, y, z = loc
    cyl(name + "_Trunk", (x, y, z + .85 * scale), .20 * scale, 1.7 * scale, M["wood2"], 10, bevel=.04)
    leaves = M["leaf2"] if autumn else M["leaf"]
    sphere(name + "_CrownA", (x, y, z + 2.2 * scale), (.85 * scale, .75 * scale, .95 * scale), leaves, 12, 6)
    sphere(name + "_CrownB", (x - .45 * scale, y + .05 * scale, z + 1.95 * scale), (.62 * scale, .57 * scale, .72 * scale), leaves, 12, 6)
    sphere(name + "_CrownC", (x + .42 * scale, y + .12 * scale, z + 1.92 * scale), (.64 * scale, .60 * scale, .75 * scale), leaves, 12, 6)


def lantern(name, loc):
    x, y, z = loc
    box(name + "_Post", (x, y, z + .75), (.07, .07, .75), M["metal"], .025)
    box(name + "_Arm", (x + .18, y, z + 1.45), (.22, .05, .05), M["metal"], .02)
    box(name + "_Glow", (x + .37, y, z + 1.25), (.15, .15, .22), M["glass"], .04)
    cone(name + "_Cap", (x + .37, y, z + 1.53), .24, .03, .20, M["metal"], 4)


def citizen(name, loc, cloth, scale=.72):
    x, y, z = loc
    cyl(name + "_Body", (x, y, z + .70 * scale), .24 * scale, .88 * scale, cloth, 12, bevel=.05)
    sphere(name + "_Head", (x, y, z + 1.34 * scale), (.25 * scale, .25 * scale, .28 * scale), M["skin"], 12, 6)
    cone(name + "_Cape", (x, y + .12 * scale, z + .73 * scale), .36 * scale, .12 * scale, .75 * scale, cloth, 12, (math.pi, 0, 0))
    for dx in (-.12, .12):
        box(name + "_Leg", (x + dx * scale, y, z + .20 * scale), (.07 * scale, .08 * scale, .22 * scale), M["wood"], .03)


add_island()
build_grand_inn()
build_smithy()
build_arcane_uplink()
build_guildhall()
build_dungeon_gate()
build_travel_dock()

# World dressing: a curated perimeter, lantern network, fences, market carts and residents.
tree_spots = [(-11, -3), (-9, -7), (-5, -8), (0, -9), (6, -8), (10, -5), (11, 0),
              (11, 7), (6, 9), (0, 9), (-8, 9), (-12, 5), (-12, 0), (-1, -5), (8, 2)]
for i, (x, y) in enumerate(tree_spots):
    tree(f"Tree_{i:02d}", (x, y, .05), random.uniform(.75, 1.25), i % 4 == 0)

for i, (x, y) in enumerate([(-2.2, -1.0), (2.3, -1.0), (-1.7, 2.7), (1.8, 2.8), (-5.3, 3.7), (5.0, 3.8)]):
    lantern(f"Lantern_{i:02d}", (x, y, .25))

for i in range(9):
    a = i * 2 * math.pi / 9 + .2
    citizen(f"Citizen_{i:02d}", (math.cos(a) * 2.0, .8 + math.sin(a) * 1.45, .32), M["cloth_blue"] if i % 2 else M["cloth_red"], random.uniform(.62, .78))

# Market stalls and lived-in prop clusters.
for idx, x in enumerate((-1.4, 1.4)):
    box(f"Market_{idx}_Counter", (x, -3.45, .72), (.78, .38, .55), M["wood2"], .08)
    box(f"Market_{idx}_Canopy", (x, -3.45, 1.68), (.95, .55, .10), M["cloth_blue"] if idx else M["cloth_red"], .08, (.07, 0, 0))
    for sx in (-.76, .76):
        box(f"Market_{idx}_Post", (x + sx, -3.45, 1.05), (.05, .05, .65), M["wood"], .02)
    for p in range(5):
        sphere(f"Market_{idx}_Goods", (x - .45 + p * .23, -3.78, 1.25), (.10, .10, .10), M["gold"] if p % 2 else M["grass2"], 10, 5)

# Cliff rocks and flowers add natural scale cues.
for i in range(28):
    a = random.random() * math.tau
    r = random.uniform(12.3, 15.0)
    x, y = math.cos(a) * r, math.sin(a) * r * .76
    sphere(f"CliffRock_{i:02d}", (x, y, -.25), (random.uniform(.28, .65), random.uniform(.25, .55), random.uniform(.25, .7)), M["stone"], 10, 5)
for i in range(60):
    a = random.random() * math.tau
    r = random.uniform(4.5, 12.0)
    x, y = math.cos(a) * r, math.sin(a) * r * .72
    cyl(f"FlowerStem_{i:02d}", (x, y, .22), .025, .30, M["grass2"], 6, bevel=0)
    sphere(f"Flower_{i:02d}", (x, y, .40), (.08, .08, .06), M["gold"] if i % 3 else M["purple"], 8, 4)

# Presentation camera and lighting.
bpy.ops.object.camera_add(location=(25.5, -31.5, 29.0))
camera = move_to_root(bpy.context.object)
camera.name = "RF2_PresentationCamera"
camera.data.type = "ORTHO"
camera.data.ortho_scale = 33.5
camera.data.lens = 48
direction = Vector((0, 0.5, 1.0)) - camera.location
camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
bpy.context.scene.camera = camera

bpy.ops.object.light_add(type="AREA", location=(-7, -12, 24))
key = move_to_root(bpy.context.object)
key.name = "RF2_KeyLight"
key.data.energy = 2600
key.data.shape = "DISK"
key.data.size = 13
key.data.color = (1.0, .68, .42)
key.rotation_euler = (math.radians(24), 0, math.radians(-24))

bpy.ops.object.light_add(type="AREA", location=(12, 9, 15))
fill = move_to_root(bpy.context.object)
fill.name = "RF2_FillLight"
fill.data.energy = 1800
fill.data.size = 11
fill.data.color = (.32, .58, 1.0)
fill.rotation_euler = (math.radians(-34), 0, math.radians(145))

bpy.ops.object.light_add(type="AREA", location=(-12, 10, 10))
rim = move_to_root(bpy.context.object)
rim.name = "RF2_RimLight"
rim.data.energy = 1200
rim.data.size = 8
rim.data.color = (.5, .72, 1.0)
rim.rotation_euler = (math.radians(-40), 0, math.radians(215))

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = PREVIEW_PATH
scene.render.film_transparent = False
scene.render.image_settings.color_mode = "RGBA"
scene.world.color = (.015, .025, .055)
scene.view_settings.look = "AgX - Medium High Contrast"
scene.render.engine = "BLENDER_EEVEE"
scene.render.image_settings.color_depth = "8"

# Dark blue backdrop plane far below the island, preventing a white showroom read.
box("RF2_Backdrop", (0, 0, -3.2), (28, 22, .2), mat("RF2_BackdropMat", (.008, .018, .044), .95), .3)

# Render from authored source before producing the game export.
bpy.context.view_layer.objects.active = camera
bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
bpy.ops.render.render(write_still=True)

# Export only generated visible mesh/curve objects; cameras/lights remain source-only.
bpy.ops.object.select_all(action="DESELECT")
for obj in root.all_objects:
    if obj.type in {"MESH", "CURVE"} and obj.name != "RF2_Backdrop":
        obj.select_set(True)
bpy.ops.export_scene.fbx(
    filepath=EXPORT_PATH,
    use_selection=True,
    apply_unit_scale=True,
    apply_scale_options="FBX_SCALE_ALL",
    axis_forward="-Y",
    axis_up="Z",
    add_leaf_bones=False,
    bake_anim=False,
    use_mesh_modifiers=True,
    path_mode="AUTO",
)

print({
    "collection": COLLECTION_NAME,
    "objects": len(root.all_objects),
    "blend": BLEND_PATH,
    "preview": PREVIEW_PATH,
    "export": EXPORT_PATH,
})
