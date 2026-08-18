import bpy
import os


ROOT = r"D:\CodexGames\RealmFoundry\ExternalAssets\DioramaV2\Exports"
COLLECTION_NAME = "RF_DIORAMA_V2"
os.makedirs(ROOT, exist_ok=True)

root = bpy.data.collections.get(COLLECTION_NAME)
if root is None:
    raise RuntimeError(f"Missing generated collection: {COLLECTION_NAME}")


def export_selected(path):
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        apply_unit_scale=True,
        apply_scale_options="FBX_SCALE_ALL",
        axis_forward="-Y",
        axis_up="Z",
        add_leaf_bones=False,
        bake_anim=False,
        use_mesh_modifiers=True,
        mesh_smooth_type="FACE",
        path_mode="AUTO",
    )


# Re-export the whole town with explicit smoothing groups for clean Unreal logs.
bpy.ops.object.select_all(action="DESELECT")
for obj in root.all_objects:
    if obj.type in {"MESH", "CURVE"} and obj.name != "RF2_Backdrop":
        obj.select_set(True)
export_selected(os.path.join(ROOT, "RF_TownDiorama_V2.fbx"))

specs = {
    "Inn": (("Inn_", "InnWing_"), (-4.4, -1.0, 0.0)),
    "Smithy": (("Smithy_",), (4.8, -1.4, 0.0)),
    "Uplink": (("Uplink_",), (2.3, 5.0, 0.0)),
    "GuildHall": (("Guild_",), (-3.7, 5.6, 0.0)),
    "DungeonGate": (("Dungeon_",), (7.6, 5.8, 0.0)),
    "TravelDock": (("Travel_",), (-8.0, 6.2, 0.0)),
}

for label, (prefixes, center) in specs.items():
    temp = bpy.data.collections.new("RF_EXPORT_TEMP")
    bpy.context.scene.collection.children.link(temp)
    duplicates = []
    for source in root.all_objects:
        if source.type != "MESH" or not source.name.startswith(prefixes):
            continue
        dup = source.copy()
        dup.data = source.data.copy()
        temp.objects.link(dup)
        dup.location.x -= center[0]
        dup.location.y -= center[1]
        dup.location.z -= center[2]
        duplicates.append(dup)

    if not duplicates:
        raise RuntimeError(f"No objects found for {label}")
    bpy.ops.object.select_all(action="DESELECT")
    for obj in duplicates:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = duplicates[0]
    export_selected(os.path.join(ROOT, f"RF_Building_{label}_V2.fbx"))

    for obj in duplicates:
        bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.collections.remove(temp)

print({"exports": sorted(specs.keys()), "root": ROOT})
