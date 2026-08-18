import unreal


EXPORT_ROOT = r"D:\CodexGames\RealmFoundry\ExternalAssets\DioramaV2\Exports"
DESTINATION = "/Game/Environment/DioramaV2"
IMPORTS = [
    ("RF_TownDiorama_V2.fbx", "SM_RF_TownDioramaV2", True),
    ("RF_Building_Inn_V2.fbx", "SM_RF_InnV2", False),
    ("RF_Building_Smithy_V2.fbx", "SM_RF_SmithyV2", False),
    ("RF_Building_Uplink_V2.fbx", "SM_RF_UplinkV2", False),
    ("RF_Building_GuildHall_V2.fbx", "SM_RF_GuildHallV2", False),
    ("RF_Building_DungeonGate_V2.fbx", "SM_RF_DungeonGateV2", False),
    ("RF_Building_TravelDock_V2.fbx", "SM_RF_TravelDockV2", False),
]

unreal.log("REALMFOUNDRY V2 // importing authored town diorama")

tasks = []
for filename, asset_name, import_materials in IMPORTS:
    task = unreal.AssetImportTask()
    task.filename = EXPORT_ROOT + "\\" + filename
    task.destination_path = DESTINATION
    task.destination_name = asset_name
    task.automated = True
    task.replace_existing = True
    task.save = True

    options = unreal.FbxImportUI()
    options.import_as_skeletal = False
    options.import_mesh = True
    options.import_materials = import_materials
    options.import_textures = False
    options.mesh_type_to_import = unreal.FBXImportType.FBXIT_STATIC_MESH
    options.static_mesh_import_data.combine_meshes = True
    options.static_mesh_import_data.generate_lightmap_u_vs = True
    options.static_mesh_import_data.auto_generate_collision = True
    options.static_mesh_import_data.convert_scene = True
    options.static_mesh_import_data.convert_scene_unit = True
    options.static_mesh_import_data.import_translation = unreal.Vector(0.0, 0.0, 0.0)
    options.static_mesh_import_data.import_rotation = unreal.Rotator(0.0, 0.0, 0.0)
    options.static_mesh_import_data.import_uniform_scale = 1.0
    task.options = options
    tasks.append(task)

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
for task in tasks:
    if not task.imported_object_paths:
        raise RuntimeError(f"RealmFoundry V2 import produced no assets: {task.filename}")
    for path in task.imported_object_paths:
        unreal.log(f"REALMFOUNDRY V2 // imported {path}")

unreal.EditorAssetLibrary.save_directory(DESTINATION, only_if_is_dirty=False, recursive=True)
unreal.log("REALMFOUNDRY V2 // diorama import complete")
