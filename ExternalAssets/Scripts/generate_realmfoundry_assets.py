import bpy
import math
import os
import json
from mathutils import Vector

ROOT = r"D:\CodexGames\RealmFoundry\ExternalAssets\MasterLibrary"
BLEND_PATH = os.path.join(ROOT, "RF_MasterLibrary.blend")
STATIC_GLB = os.path.join(ROOT, "RF_StaticLibrary.glb")
STATIC_FBX = os.path.join(ROOT, "RF_StaticLibrary.fbx")
CHARACTER_FBX = os.path.join(ROOT, "SK_RFSubscriber.fbx")
PREVIEW_PATH = os.path.join(ROOT, "RF_MasterLibrary_Preview.png")
MANIFEST_PATH = os.path.join(ROOT, "RF_MasterLibrary_manifest.json")
SCENE_NAME = "RF_ASSET_SCENE"

os.makedirs(ROOT, exist_ok=True)

# Operate only in the dedicated RealmFoundry scene. Unknown user scenes are untouched.
scene = bpy.data.scenes.get(SCENE_NAME)
if scene:
    for obj in list(scene.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.scenes.remove(scene)
# Failed or interrupted runs can leave unlinked datablocks. Remove only objects
# using this project's reserved prefixes; unrelated scenes remain untouched.
for obj in list(bpy.data.objects):
    if obj.name.startswith(('SM_RF_', 'SK_RF', 'RF_', 'Preview_')):
        bpy.data.objects.remove(obj, do_unlink=True)
for action in list(bpy.data.actions):
    if action.name.startswith('A_RF_'):
        bpy.data.actions.remove(action, do_unlink=True)
for collection in list(bpy.data.collections):
    if collection.name.startswith(('RF_EXPORT', 'RF_PREVIEW', 'RF_RIG')):
        bpy.data.collections.remove(collection)
for armature_data in list(bpy.data.armatures):
    if armature_data.name.startswith('SK_RFSubscriber_Skeleton') and armature_data.users == 0:
        bpy.data.armatures.remove(armature_data)
scene = bpy.data.scenes.new(SCENE_NAME)
bpy.context.window.scene = scene

export_collection = bpy.data.collections.new("RF_EXPORT")
preview_collection = bpy.data.collections.new("RF_PREVIEW")
rig_collection = bpy.data.collections.new("RF_RIG")
scene.collection.children.link(export_collection)
scene.collection.children.link(preview_collection)
scene.collection.children.link(rig_collection)

scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = PREVIEW_PATH
scene.render.film_transparent = False
if scene.world is None:
    scene.world = bpy.data.worlds.new('RF_World')
scene.world.color = (0.008, 0.012, 0.025)


def move_to(obj, collection):
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    collection.objects.link(obj)


def mat(name, color, metallic=0.0, roughness=0.55, emission=None, emission_strength=0.0):
    material = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    material.use_nodes = True
    principled = material.node_tree.nodes.get('Principled BSDF')
    principled.inputs['Base Color'].default_value = (*color, 1.0)
    principled.inputs['Metallic'].default_value = metallic
    principled.inputs['Roughness'].default_value = roughness
    emission_input = principled.inputs.get('Emission Color') or principled.inputs.get('Emission')
    if emission_input:
        emission_input.default_value = (*(emission or color), 1.0)
    strength_input = principled.inputs.get('Emission Strength')
    if strength_input:
        strength_input.default_value = emission_strength
    return material


M_STONE = mat('M_RF_Stone', (0.19, 0.23, 0.30), 0.05, 0.78)
M_WOOD = mat('M_RF_Wood', (0.24, 0.095, 0.035), 0.0, 0.72)
M_ROOF = mat('M_RF_Roof', (0.10, 0.18, 0.25), 0.15, 0.48)
M_METAL = mat('M_RF_Metal', (0.16, 0.20, 0.25), 0.75, 0.25)
M_GOLD = mat('M_RF_Gold', (0.62, 0.31, 0.055), 0.82, 0.22)
M_CYAN = mat('M_RF_Cyan', (0.02, 0.28, 0.42), 0.35, 0.22, (0.0, 0.72, 1.0), 7.0)
M_GREEN = mat('M_RF_Green', (0.03, 0.28, 0.11), 0.15, 0.42, (0.02, 0.65, 0.18), 3.5)
M_RED = mat('M_RF_Red', (0.38, 0.035, 0.045), 0.18, 0.38, (0.9, 0.03, 0.02), 2.2)
M_PURPLE = mat('M_RF_Eldritch', (0.13, 0.025, 0.24), 0.25, 0.30, (0.52, 0.05, 0.95), 5.0)
M_CANDY = mat('M_RF_Confection', (0.72, 0.22, 0.38), 0.0, 0.38)
M_SKIN = mat('M_RF_Skin', (0.52, 0.23, 0.13), 0.0, 0.62)
M_CLOTH = mat('M_RF_Cloth', (0.025, 0.16, 0.28), 0.05, 0.70)
M_TRIM = mat('M_RF_Trim', (0.0, 0.55, 0.78), 0.35, 0.25, (0.0, 0.35, 0.75), 1.4)
M_BONE = mat('M_RF_Bone', (0.72, 0.66, 0.48), 0.0, 0.76)
M_BLACK = mat('M_RF_Black', (0.015, 0.018, 0.025), 0.3, 0.32)


def finish_primitive(obj, name, material, collection=export_collection, bevel=0.04):
    obj.name = name
    move_to(obj, collection)
    # Bake authored world-space transforms before compound meshes are joined.
    # This preserves building elevations and aligns the subscriber with its rig.
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    if material:
        obj.data.materials.append(material)
    if obj.type == 'MESH':
        for polygon in obj.data.polygons:
            polygon.use_smooth = len(polygon.vertices) > 4
    if bevel > 0 and obj.type == 'MESH':
        mod = obj.modifiers.new('RF_Bevel', 'BEVEL')
        mod.width = bevel
        mod.segments = 2
    return obj


def box(name, size, location=(0, 0, 0), material=M_STONE, collection=export_collection, bevel=0.04, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=location, rotation=rotation)
    obj = bpy.context.object
    obj.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish_primitive(obj, name, material, collection, bevel)


def cylinder(name, radius, depth, location=(0, 0, 0), material=M_STONE, collection=export_collection, vertices=16, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location, rotation=rotation)
    return finish_primitive(bpy.context.object, name, material, collection, min(radius * 0.12, 0.05))


def sphere(name, radius, location=(0, 0, 0), material=M_STONE, collection=export_collection, segments=20, rings=12, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=radius, location=location)
    obj = bpy.context.object
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return finish_primitive(obj, name, material, collection, 0.02)


def cone(name, radius1, radius2, depth, location=(0, 0, 0), material=M_ROOF, collection=export_collection, vertices=16, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius1, radius2=radius2, depth=depth, location=location, rotation=rotation)
    return finish_primitive(bpy.context.object, name, material, collection, 0.035)


def torus(name, major, minor, location=(0, 0, 0), material=M_METAL, collection=export_collection, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=20, minor_segments=8, location=location, rotation=rotation)
    return finish_primitive(bpy.context.object, name, material, collection, 0)


def join_parts(name, parts):
    if len(parts) == 1:
        obj = parts[0]
        obj.name = name
        obj['rf_export'] = True
        obj['rf_asset_id'] = name
        return obj
    bpy.ops.object.select_all(action='DESELECT')
    for part in parts:
        part.hide_set(False)
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    obj = bpy.context.object
    obj.name = name
    obj['rf_export'] = True
    obj['rf_asset_id'] = name
    obj.location = (0, 0, 0)
    return obj


def preview_copy(obj, location, scale=1.0, rotation=(0, 0, 0)):
    copy = obj.copy()
    copy.data = obj.data
    copy.name = obj.name + '_PREVIEW'
    copy.location = location
    copy.rotation_euler = rotation
    copy.scale = (scale, scale, scale)
    preview_collection.objects.link(copy)
    obj.hide_render = True
    return copy


def building(name, sign_material=M_CYAN, roof=M_ROOF, variant=0):
    parts = [
        box(name + '_Body', (2.8, 2.4, 1.8), (0, 0, 0.9), M_STONE),
        box(name + '_Door', (0.75, 0.16, 1.35), (0, -1.22, 0.68), M_WOOD),
        cone(name + '_Roof', 2.05, 0.25 if variant % 2 else 0.0, 1.15, (0, 0, 2.32), roof, vertices=4 if variant % 2 == 0 else 12, rotation=(0, 0, math.radians(45 if variant % 2 == 0 else 0))),
        box(name + '_Sign', (1.15, 0.12, 0.42), (0, -1.38, 1.6), sign_material, bevel=0.08),
        cylinder(name + '_Chimney', 0.18, 1.0, (0.85, 0.35, 2.55), M_METAL, vertices=10),
    ]
    return join_parts(name, parts)


assets = []

# Functional buildings and services.
building_specs = [
    ('SM_RF_Inn', M_CYAN, M_ROOF), ('SM_RF_Tavern', M_GOLD, M_ROOF),
    ('SM_RF_Blacksmith', M_RED, M_BLACK), ('SM_RF_PotionShop', M_PURPLE, M_ROOF),
    ('SM_RF_Market', M_GREEN, M_WOOD), ('SM_RF_TrinketCart', M_CANDY, M_CANDY),
    ('SM_RF_Graveyard', M_PURPLE, M_BLACK), ('SM_RF_QuestHall', M_GOLD, M_ROOF),
    ('SM_RF_StartPortal', M_CYAN, M_METAL), ('SM_RF_Landmark', M_GREEN, M_GOLD),
    ('SM_RF_DungeonEntrance', M_RED, M_STONE), ('SM_RF_TravelTower', M_CYAN, M_METAL),
]
for index, spec in enumerate(building_specs):
    obj = building(spec[0], spec[1], spec[2], index)
    assets.append(obj)

# Infrastructure and transport.
parts = [cylinder('Uplink_Base', 0.75, 0.35, (0, 0, 0.18), M_METAL), cylinder('Uplink_Mast', 0.13, 3.2, (0, 0, 1.75), M_METAL), torus('Uplink_RingA', 0.65, 0.08, (0, 0, 2.5), M_CYAN), torus('Uplink_RingB', 0.38, 0.06, (0, 0, 2.9), M_CYAN), sphere('Uplink_Core', 0.25, (0, 0, 3.25), M_CYAN)]
assets.append(join_parts('SM_RF_UplinkNode', parts))

parts = [box('Bridge_Deck', (5.0, 1.5, 0.25), (0, 0, 0.15), M_WOOD), box('Bridge_RailL', (5.0, 0.12, 0.55), (0, -0.69, 0.58), M_METAL), box('Bridge_RailR', (5.0, 0.12, 0.55), (0, 0.69, 0.58), M_METAL)]
assets.append(join_parts('SM_RF_Bridge', parts))

parts = [box('Boat_Hull', (3.0, 1.2, 0.5), (0, 0, 0.35), M_WOOD), box('Boat_Deck', (2.2, 0.85, 0.18), (0, 0, 0.68), M_GOLD), cylinder('Boat_Mast', 0.08, 2.4, (0, 0, 1.75), M_METAL), box('Boat_Sail', (0.08, 1.6, 1.35), (0, 0, 2.1), M_CYAN)]
assets.append(join_parts('SM_RF_Boat', parts))

parts = [cylinder('Flight_Base', 1.55, 0.25, (0, 0, 0.13), M_METAL), torus('Flight_Ring', 1.15, 0.1, (0, 0, 0.35), M_CYAN), sphere('Flight_Core', 0.38, (0, 0, 0.5), M_CYAN)]
assets.append(join_parts('SM_RF_FlightPoint', parts))

parts = [box('Vehicle_Body', (2.4, 1.25, 0.75), (0, 0, 0.75), M_RED), cylinder('Wheel1', 0.32, 0.18, (-0.75, -0.72, 0.42), M_BLACK, rotation=(math.pi/2,0,0)), cylinder('Wheel2', 0.32, 0.18, (0.75, -0.72, 0.42), M_BLACK, rotation=(math.pi/2,0,0)), cylinder('Wheel3', 0.32, 0.18, (-0.75, 0.72, 0.42), M_BLACK, rotation=(math.pi/2,0,0)), cylinder('Wheel4', 0.32, 0.18, (0.75, 0.72, 0.42), M_BLACK, rotation=(math.pi/2,0,0))]
assets.append(join_parts('SM_RF_Vehicle', parts))

parts = [cylinder('Tele_Base', 1.05, 0.28, (0,0,0.15), M_METAL), torus('Tele_Ring', 1.2, 0.12, (0,0,1.25), M_CYAN, rotation=(math.pi/2,0,0)), sphere('Tele_Core', 0.38, (0,0,1.25), M_CYAN)]
assets.append(join_parts('SM_RF_Teleporter', parts))

# Modular town and dungeon pieces on a 1 m grid / 3 m floor height.
module_specs = [
    ('SM_RF_Wall', (3.0, 0.2, 3.0), M_STONE), ('SM_RF_Floor', (3.0, 3.0, 0.2), M_STONE),
    ('SM_RF_Ceiling', (3.0, 3.0, 0.18), M_ROOF), ('SM_RF_Door', (1.2, 0.18, 2.4), M_WOOD),
    ('SM_RF_Window', (1.4, 0.12, 1.1), M_CYAN), ('SM_RF_Column', (0.35, 0.35, 3.0), M_STONE),
    ('SM_RF_Stair', (3.0, 2.0, 1.5), M_WOOD), ('SM_RF_RoofTile', (3.0, 3.0, 0.22), M_ROOF),
    ('SM_RF_DungeonFloor', (4.0, 4.0, 0.2), M_PURPLE), ('SM_RF_DungeonWall', (4.0, 0.25, 3.2), M_STONE),
]
for name, size, material in module_specs:
    assets.append(join_parts(name, [box(name + '_Part', size, (0,0,size[2]/2), material)]))

# Dungeon interaction props.
assets.append(join_parts('SM_RF_Chest', [box('Chest_Base',(1.1,0.7,0.55),(0,0,0.3),M_WOOD), box('Chest_Lid',(1.15,0.74,0.28),(0,0,0.72),M_GOLD), box('Chest_Lock',(0.18,0.08,0.25),(0,-0.4,0.58),M_CYAN)]))
assets.append(join_parts('SM_RF_Key', [torus('Key_Ring',0.22,0.055,(0,0,0),M_GOLD), box('Key_Shaft',(0.75,0.09,0.09),(0.48,0,0),M_GOLD), box('Key_Tooth',(0.12,0.09,0.25),(0.78,0,-0.08),M_GOLD)]))
assets.append(join_parts('SM_RF_Potion', [sphere('Potion_Bottle',0.28,(0,0,0.3),M_PURPLE,scale=(0.75,0.75,1.2)), cylinder('Potion_Neck',0.1,0.28,(0,0,0.7),M_GOLD,vertices=12)]))
assets.append(join_parts('SM_RF_Trinket', [torus('Trinket_Ring',0.3,0.06,(0,0,0),M_GOLD), sphere('Trinket_Gem',0.16,(0,0,-0.31),M_CYAN)]))
assets.append(join_parts('SM_RF_RespawnStone', [cylinder('Respawn_Base',0.7,0.22,(0,0,0.12),M_STONE), sphere('Respawn_Core',0.42,(0,0,0.75),M_CYAN,scale=(0.75,0.75,1.4))]))

# Fourteen core weapons plus the optional ray gun. Readable category silhouettes.
weapon_names = ['Axe','Bone','Bow','Crossbow','CurvedSword','Dagger','Greatsword','Gun','Hammer','Mace','Spear','Staff','Sword','Wand','RayGun']
for idx, weapon in enumerate(weapon_names):
    parts = []
    if weapon in ('Bow','Crossbow'):
        parts += [torus(weapon+'_Arc',0.72,0.055,(0,0,0),M_WOOD,rotation=(math.pi/2,0,0)), box(weapon+'_Grip',(0.15,0.18,1.0),(0,0,0),M_METAL)]
        if weapon == 'Crossbow': parts.append(box('Crossbar',(1.6,0.16,0.16),(0,0,0.45),M_WOOD))
    elif weapon in ('Gun','RayGun'):
        parts += [box(weapon+'_Body',(1.1,0.28,0.34),(0,0,0.25),M_METAL), box(weapon+'_Grip',(0.3,0.25,0.65),(-0.28,0,-0.18),M_WOOD), cylinder(weapon+'_Muzzle',0.15,0.65,(0.75,0,0.28),M_CYAN if weapon=='RayGun' else M_BLACK,rotation=(0,math.pi/2,0))]
    elif weapon in ('Axe','Hammer','Mace','Spear','Staff','Wand','Bone'):
        length = 2.2 if weapon in ('Spear','Staff') else (1.3 if weapon != 'Wand' else 0.75)
        parts.append(cylinder(weapon+'_Shaft',0.07,length,(0,0,length/2),M_BONE if weapon=='Bone' else M_WOOD,vertices=10))
        if weapon=='Axe': parts.append(box('Axe_Head',(0.75,0.16,0.5),(0,0,length),M_METAL))
        elif weapon=='Hammer': parts.append(box('Hammer_Head',(0.75,0.32,0.32),(0,0,length),M_METAL))
        elif weapon=='Mace': parts.append(sphere('Mace_Head',0.28,(0,0,length),M_METAL,segments=12,rings=8))
        elif weapon=='Spear': parts.append(cone('Spear_Tip',0.18,0,0.55,(0,0,length+0.27),M_METAL,vertices=8))
        else: parts.append(sphere(weapon+'_Focus',0.18,(0,0,length),M_PURPLE if weapon=='Wand' else M_CYAN,segments=12,rings=8))
    else:
        length = {'Dagger':0.8,'Greatsword':2.2,'Sword':1.35,'CurvedSword':1.45}.get(weapon,1.2)
        parts += [box(weapon+'_Blade',(0.18,0.055,length),(0,0,length/2),M_METAL,bevel=0.035), box(weapon+'_Guard',(0.62,0.11,0.11),(0,0,0.08),M_GOLD), cylinder(weapon+'_Grip',0.07,0.42,(0,0,-0.18),M_WOOD,vertices=10)]
    obj = join_parts('SM_RF_Weapon_'+weapon, parts)
    obj['weapon_category'] = weapon
    obj['item_level_visual_tiers'] = 3
    assets.append(obj)

# Scenery and themed silhouettes.
assets.append(join_parts('SM_RF_Tree', [cylinder('Tree_Trunk',0.22,2.1,(0,0,1.05),M_WOOD,vertices=10), cone('Tree_Crown',1.05,0,2.5,(0,0,2.65),M_GREEN,vertices=12)]))
assets.append(join_parts('SM_RF_Rock', [sphere('Rock_Main',0.85,(0,0,0.55),M_STONE,segments=12,rings=8,scale=(1.2,0.85,0.7))]))
assets.append(join_parts('SM_RF_WaterfallMarker', [box('Waterfall_Frame',(1.8,0.25,2.6),(0,0,1.3),M_STONE), box('Waterfall_Water',(1.35,0.12,2.2),(0,-0.2,1.1),M_CYAN)]))

# Monster family: slime, golem, and multi-phase boss.
assets.append(join_parts('SM_RF_Monster_Slime', [sphere('Slime_Body',0.72,(0,0,0.55),M_GREEN,segments=18,rings=10,scale=(1.0,0.85,0.72)), sphere('Slime_EyeL',0.09,(-0.22,-0.55,0.72),M_CYAN,segments=10,rings=6), sphere('Slime_EyeR',0.09,(0.22,-0.55,0.72),M_CYAN,segments=10,rings=6)]))
assets.append(join_parts('SM_RF_Monster_Golem', [box('Golem_Torso',(1.25,0.75,1.35),(0,0,1.55),M_STONE), sphere('Golem_Head',0.42,(0,0,2.55),M_STONE,segments=12,rings=8), cylinder('Golem_ArmL',0.22,1.55,(-0.95,0,1.55),M_STONE,vertices=10), cylinder('Golem_ArmR',0.22,1.55,(0.95,0,1.55),M_STONE,vertices=10), sphere('Golem_Core',0.25,(0,-0.42,1.65),M_CYAN,segments=12,rings=8)]))
assets.append(join_parts('SM_RF_Boss_Eldritch', [sphere('Boss_Core',0.8,(0,0,1.65),M_PURPLE,segments=20,rings=12), torus('Boss_RingA',1.35,0.13,(0,0,1.65),M_CYAN,rotation=(math.pi/2,0,0)), torus('Boss_RingB',1.05,0.1,(0,0,1.65),M_GOLD,rotation=(0,math.pi/2,0)), cone('Boss_Crown',0.85,0,1.2,(0,0,3.0),M_PURPLE,vertices=8)]))

# Operator drone.
assets.append(join_parts('SK_RFOperatorDrone', [sphere('Drone_Core',0.5,(0,0,0.65),M_CYAN,segments=20,rings=12), torus('Drone_Ring',0.72,0.08,(0,0,0.65),M_GOLD), sphere('Drone_Eye',0.15,(0,-0.48,0.72),M_GREEN,segments=12,rings=8), cone('Drone_Tail',0.22,0,0.6,(0,0,0.05),M_METAL,vertices=8)]))

# Create an original modular humanoid with a single-root deform skeleton.
arm_data = bpy.data.armatures.new('SK_RFSubscriber_Skeleton')
arm = bpy.data.objects.new('SK_RFSubscriber_Armature', arm_data)
rig_collection.objects.link(arm)
bpy.context.view_layer.objects.active = arm
arm.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
bones = {
    'root': ((0,0,0),(0,0,0.18),None),
    'pelvis': ((0,0,0.18),(0,0,0.55),'root'),
    'spine_01': ((0,0,0.55),(0,0,1.05),'pelvis'),
    'spine_02': ((0,0,1.05),(0,0,1.45),'spine_01'),
    'neck': ((0,0,1.45),(0,0,1.62),'spine_02'),
    'head': ((0,0,1.62),(0,0,1.92),'neck'),
    'upperarm_l': ((0,0,1.38),(-0.48,0,1.34),'spine_02'),
    'lowerarm_l': ((-0.48,0,1.34),(-0.88,0,1.08),'upperarm_l'),
    'hand_l': ((-0.88,0,1.08),(-1.02,0,1.02),'lowerarm_l'),
    'upperarm_r': ((0,0,1.38),(0.48,0,1.34),'spine_02'),
    'lowerarm_r': ((0.48,0,1.34),(0.88,0,1.08),'upperarm_r'),
    'hand_r': ((0.88,0,1.08),(1.02,0,1.02),'lowerarm_r'),
    'thigh_l': ((-0.22,0,0.48),(-0.24,0,0.0),'pelvis'),
    'calf_l': ((-0.24,0,0.0),(-0.24,0,-0.48),'thigh_l'),
    'foot_l': ((-0.24,0,-0.48),(-0.24,-0.26,-0.55),'calf_l'),
    'thigh_r': ((0.22,0,0.48),(0.24,0,0.0),'pelvis'),
    'calf_r': ((0.24,0,0.0),(0.24,0,-0.48),'thigh_r'),
    'foot_r': ((0.24,0,-0.48),(0.24,-0.26,-0.55),'calf_r'),
}
for bone_name, (head, tail, parent) in bones.items():
    edit_bone = arm.data.edit_bones.new(bone_name)
    edit_bone.head = head
    edit_bone.tail = tail
    edit_bone.use_deform = True
    if parent:
        edit_bone.parent = arm.data.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT')

body_parts = []
def body_part(obj, bone_name):
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    group = obj.vertex_groups.new(name=bone_name)
    group.add(list(range(len(obj.data.vertices))), 1.0, 'REPLACE')
    body_parts.append(obj)

body_part(box('Subscriber_Pelvis',(0.58,0.36,0.38),(0,0,0.58),M_CLOTH,rig_collection), 'pelvis')
body_part(box('Subscriber_Torso',(0.78,0.42,0.72),(0,0,1.12),M_CLOTH,rig_collection), 'spine_02')
body_part(sphere('Subscriber_Head',0.28,(0,0,1.82),M_SKIN,rig_collection,segments=18,rings=10,scale=(0.85,0.8,1.0)), 'head')
body_part(cylinder('Subscriber_ArmL',0.11,0.82,(-0.55,0,1.25),M_CLOTH,rig_collection,vertices=12,rotation=(0,math.pi/2,math.radians(-10))), 'upperarm_l')
body_part(cylinder('Subscriber_ArmR',0.11,0.82,(0.55,0,1.25),M_CLOTH,rig_collection,vertices=12,rotation=(0,math.pi/2,math.radians(10))), 'upperarm_r')
body_part(sphere('Subscriber_HandL',0.13,(-0.95,0,1.05),M_SKIN,rig_collection,segments=12,rings=8), 'hand_l')
body_part(sphere('Subscriber_HandR',0.13,(0.95,0,1.05),M_SKIN,rig_collection,segments=12,rings=8), 'hand_r')
body_part(cylinder('Subscriber_LegL',0.14,0.95,(-0.22,0,0.0),M_CLOTH,rig_collection,vertices=12), 'thigh_l')
body_part(cylinder('Subscriber_LegR',0.14,0.95,(0.22,0,0.0),M_CLOTH,rig_collection,vertices=12), 'thigh_r')
body_part(box('Subscriber_FootL',(0.28,0.48,0.2),(-0.22,-0.13,-0.5),M_BLACK,rig_collection), 'foot_l')
body_part(box('Subscriber_FootR',(0.28,0.48,0.2),(0.22,-0.13,-0.5),M_BLACK,rig_collection), 'foot_r')
subscriber = join_parts('SK_RFSubscriber', body_parts)
move_to(subscriber, rig_collection)
modifier = subscriber.modifiers.new('Armature', 'ARMATURE')
modifier.object = arm
subscriber.parent = arm
subscriber['rf_character_height_m'] = 2.0
subscriber['rf_root_motion_policy'] = 'in_place'

def clear_pose():
    for pb in arm.pose.bones:
        pb.rotation_mode = 'XYZ'
        pb.rotation_euler = (0,0,0)
        pb.location = (0,0,0)

def key(frame, rotations=None, root_z=0.0):
    rotations = rotations or {}
    for bone_name, rot in rotations.items():
        pb = arm.pose.bones[bone_name]
        pb.rotation_euler = rot
        pb.keyframe_insert('rotation_euler', frame=frame)
    root = arm.pose.bones['root']
    root.location.z = root_z
    root.keyframe_insert('location', frame=frame)

def make_action(name, length, poses, cyclic=False):
    clear_pose()
    action = bpy.data.actions.new(name)
    arm.animation_data_create()
    arm.animation_data.action = action
    for frame, rotations, root_z in poses:
        key(frame, rotations, root_z)
    # Blender 5.x stores animation curves in layered Action slots. The authored
    # cyclic clips already repeat their first pose at the final frame, which is
    # portable through FBX without relying on version-specific curve modifiers.
    action['rf_frames'] = f'1-{length}'
    action['rf_fps'] = 30
    action['rf_looping'] = cyclic
    action['rf_root_motion'] = 'in_place'
    return action

actions = []
actions.append(make_action('A_RF_Idle',60,[(1,{},0),(30,{'spine_02':(0.035,0,0)},0.025),(60,{},0)],True))
actions.append(make_action('A_RF_Walk',30,[(1,{'thigh_l':(0.55,0,0),'thigh_r':(-0.55,0,0),'upperarm_l':(-0.35,0,0),'upperarm_r':(0.35,0,0)},0),(15,{'thigh_l':(-0.55,0,0),'thigh_r':(0.55,0,0),'upperarm_l':(0.35,0,0),'upperarm_r':(-0.35,0,0)},0.04),(30,{'thigh_l':(0.55,0,0),'thigh_r':(-0.55,0,0),'upperarm_l':(-0.35,0,0),'upperarm_r':(0.35,0,0)},0)],True))
actions.append(make_action('A_RF_Run',24,[(1,{'thigh_l':(0.9,0,0),'thigh_r':(-0.9,0,0),'upperarm_l':(-0.65,0,0),'upperarm_r':(0.65,0,0)},0),(12,{'thigh_l':(-0.9,0,0),'thigh_r':(0.9,0,0),'upperarm_l':(0.65,0,0),'upperarm_r':(-0.65,0,0)},0.08),(24,{'thigh_l':(0.9,0,0),'thigh_r':(-0.9,0,0),'upperarm_l':(-0.65,0,0),'upperarm_r':(0.65,0,0)},0)],True))
actions.append(make_action('A_RF_Talk',45,[(1,{},0),(15,{'upperarm_r':(-0.4,0.2,0.4),'lowerarm_r':(-0.65,0,0)},0),(30,{'upperarm_l':(-0.35,-0.2,-0.35),'lowerarm_l':(-0.55,0,0)},0),(45,{},0)],True))
actions.append(make_action('A_RF_Cheer',45,[(1,{},0),(20,{'upperarm_l':(0,-0.2,-2.2),'upperarm_r':(0,0.2,2.2),'lowerarm_l':(-0.3,0,0),'lowerarm_r':(-0.3,0,0)},0.15),(45,{},0)],False))
actions.append(make_action('A_RF_Melee',24,[(1,{},0),(10,{'spine_02':(0,0,-0.35),'upperarm_r':(-1.1,0.2,0.6),'lowerarm_r':(-0.8,0,0)},0),(16,{'spine_02':(0,0,0.45),'upperarm_r':(0.5,0,-1.1),'lowerarm_r':(-0.15,0,0)},0),(24,{},0)],False))
actions.append(make_action('A_RF_Ranged',30,[(1,{},0),(14,{'upperarm_l':(-1.25,0,0),'upperarm_r':(-1.25,0,0),'lowerarm_l':(-0.2,0,0),'lowerarm_r':(-0.2,0,0)},0),(30,{},0)],False))
actions.append(make_action('A_RF_Cast',40,[(1,{},0),(18,{'upperarm_l':(-0.9,-0.4,-0.4),'upperarm_r':(-0.9,0.4,0.4),'lowerarm_l':(-0.7,0,0),'lowerarm_r':(-0.7,0,0)},0.08),(40,{},0)],False))
actions.append(make_action('A_RF_Hit',15,[(1,{},0),(7,{'spine_02':(-0.45,0,0),'head':(0.2,0,0)},-0.05),(15,{},0)],False))
actions.append(make_action('A_RF_Death',50,[(1,{},0),(25,{'spine_01':(0,0,0.7),'thigh_l':(-0.6,0,0),'thigh_r':(-0.35,0,0)},-0.3),(50,{'spine_01':(0,0,1.45),'spine_02':(0,0,0.5)},-0.52)],False))
actions.append(make_action('A_RF_Ghost',60,[(1,{},0.1),(30,{'spine_02':(0,0,0.08)},0.28),(60,{},0.1)],True))
actions.append(make_action('A_RF_Sit',40,[(1,{},0),(40,{'thigh_l':(-1.4,0,0),'thigh_r':(-1.4,0,0),'calf_l':(1.35,0,0),'calf_r':(1.35,0,0),'spine_01':(0.15,0,0)},-0.4)],False))
actions.append(make_action('A_RF_Type',30,[(1,{'upperarm_l':(-0.75,0,0),'upperarm_r':(-0.75,0,0)},0),(15,{'upperarm_l':(-0.72,0,0.12),'upperarm_r':(-0.72,0,-0.12)},0),(30,{'upperarm_l':(-0.75,0,0),'upperarm_r':(-0.75,0,0)},0)],True))
actions.append(make_action('A_RF_Repair',35,[(1,{},0),(16,{'upperarm_r':(-1.05,0,0.6),'lowerarm_r':(-0.8,0,0)},0),(25,{'upperarm_r':(-0.55,0,-0.35),'lowerarm_r':(-0.4,0,0)},0),(35,{},0)],True))
actions.append(make_action('A_RF_Inspect',40,[(1,{},0),(20,{'head':(0,0,0.35),'upperarm_l':(-0.65,-0.2,-0.2)},0),(40,{},0)],True))

arm.animation_data.action = None
for action in actions:
    track = arm.animation_data.nla_tracks.new()
    track.name = action.name
    strip = track.strips.new(action.name, 1, action)
    strip.action_frame_start = 1
    strip.action_frame_end = int(action.get('rf_frames', '1-60').split('-')[1])
scene.frame_start = 1
scene.frame_end = 60
scene.render.fps = 30

# Preview gallery: linked copies arranged on labeled plinths.
gallery = assets[:]
for index, obj in enumerate(gallery):
    col = index % 10
    row = index // 10
    x = (col - 4.5) * 4.2
    y = (row - 3.0) * 4.2
    preview_copy(obj, (x, y, 0.25), 0.75)
    box('Preview_Plinth_'+str(index),(3.4,3.4,0.18),(x,y,0.08),M_BLACK,preview_collection,0.06)

subscriber_preview = subscriber.copy()
subscriber_preview.data = subscriber.data
subscriber_preview.name = 'SK_RFSubscriber_PREVIEW'
subscriber_preview.parent = None
subscriber_preview.modifiers.clear()
subscriber_preview.location = (-20.5, 17.0, 1.0)
subscriber_preview.scale = (1.6,1.6,1.6)
preview_collection.objects.link(subscriber_preview)

# Hero plinth/title objects.
box('Preview_Ground',(48,44,0.2),(0,0,-0.12),M_BLACK,preview_collection,0)
title_parts = [box('RF_TitleBar',(20,0.35,1.3),(0,18.5,2.6),M_CYAN,preview_collection,0.12), box('RF_TitleCore',(8,0.45,0.55),(0,18.2,4.0),M_GOLD,preview_collection,0.1)]

# Camera and studio lights.
camera_data = bpy.data.cameras.new('RF_PreviewCamera')
camera = bpy.data.objects.new('RF_PreviewCamera', camera_data)
scene.collection.objects.link(camera)
scene.camera = camera
camera.location = (31, -39, 35)
camera.data.lens = 52

def track(obj, point):
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat('-Z','Y').to_euler()
track(camera, (0, 3, 1.5))

sun_data = bpy.data.lights.new('RF_Sun','SUN')
sun_data.energy = 3.0
sun_data.color = (0.68,0.82,1.0)
sun = bpy.data.objects.new('RF_Sun',sun_data)
scene.collection.objects.link(sun)
sun.rotation_euler = (math.radians(32),math.radians(-20),math.radians(-35))

for name, location, color, energy, size in [
    ('RF_Key',(12,-15,22),(0.25,0.65,1.0),1800,8),
    ('RF_Fill',(-18,-8,15),(1.0,0.26,0.12),1400,10),
    ('RF_Rim',(0,18,20),(0.4,0.1,1.0),1700,7),
]:
    data = bpy.data.lights.new(name,'AREA')
    data.energy = energy
    data.color = color
    data.shape = 'DISK'
    data.size = size
    light = bpy.data.objects.new(name,data)
    scene.collection.objects.link(light)
    light.location = location
    track(light,(0,2,1.5))

# Save authoritative source before export.
bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)

# Render preview.
scene.render.filepath = PREVIEW_PATH
bpy.ops.render.render(write_still=True)

# Export production static meshes at origin.
bpy.ops.object.select_all(action='DESELECT')
static_exports = []
for obj in export_collection.objects:
    if obj.type == 'MESH' and obj.get('rf_export'):
        obj.hide_set(False)
        obj.hide_render = False
        obj.select_set(True)
        static_exports.append(obj)
bpy.ops.export_scene.gltf(
    filepath=STATIC_GLB,
    export_format='GLB',
    use_selection=True,
    export_apply=True,
    export_yup=True,
    export_materials='EXPORT',
    export_animations=False,
)
bpy.ops.export_scene.fbx(
    filepath=STATIC_FBX,
    use_selection=True,
    object_types={'MESH'},
    global_scale=100.0,
    apply_unit_scale=True,
    apply_scale_options='FBX_SCALE_UNITS',
    bake_space_transform=False,
    axis_forward='-Y',
    axis_up='Z',
    mesh_smooth_type='FACE',
    use_tspace=True,
    bake_anim=False,
)

# Export the original humanoid skeleton and every named action.
bpy.ops.object.select_all(action='DESELECT')
subscriber.hide_set(False)
arm.hide_set(False)
subscriber.select_set(True)
arm.select_set(True)
bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.fbx(
    filepath=CHARACTER_FBX,
    use_selection=True,
    object_types={'ARMATURE','MESH'},
    global_scale=100.0,
    apply_unit_scale=True,
    apply_scale_options='FBX_SCALE_UNITS',
    bake_space_transform=False,
    axis_forward='-Y',
    axis_up='Z',
    mesh_smooth_type='FACE',
    use_tspace=True,
    add_leaf_bones=False,
    use_armature_deform_only=True,
    bake_anim=True,
    bake_anim_use_all_bones=True,
    bake_anim_use_nla_strips=True,
    bake_anim_use_all_actions=False,
    bake_anim_force_startend_keying=True,
    bake_anim_simplify_factor=0.0,
)

manifest = {
    'project': 'RealmFoundry: Live Worlds',
    'units': '1 Blender meter = 100 Unreal centimeters',
    'static_glb': STATIC_GLB,
    'static_fbx': STATIC_FBX,
    'character_fbx': CHARACTER_FBX,
    'blend_source': BLEND_PATH,
    'preview': PREVIEW_PATH,
    'static_assets': [obj.name for obj in static_exports],
    'character': {
        'mesh': subscriber.name,
        'armature': arm.name,
        'bones': list(bones.keys()),
        'actions': [action.name for action in actions],
        'root_motion': 'in_place',
        'height_m': 2.0,
        'fps': 30,
    },
    'modular_grid_cm': 100,
    'floor_height_cm': 300,
    'collision_plan': 'Unreal simple generated collision; explicit boxes for buildings and modules',
}
with open(MANIFEST_PATH, 'w', encoding='utf-8') as handle:
    json.dump(manifest, handle, indent=2)

bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
print(json.dumps({'success': True, 'outputs': manifest}, separators=(',', ':')))
