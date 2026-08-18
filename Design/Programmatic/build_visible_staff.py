import json


def tool(name, args):
    return execute_tool(name, json.dumps(args))


def asset_exists(path):
    return tool(
        "editor_toolset.toolsets.asset.AssetTools.exists",
        {"path": path})["returnValue"]


def create_child(name):
    path = f"/Game/Characters/Staff/{name}.{name}"
    if asset_exists(path):
        return {"refPath": path}
    return tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.create",
        {
            "folder_path": "/Game/Characters/Staff",
            "asset_name": name,
            "asset_type": {
                "refPath": "/Game/Characters/Subscribers/BP_RFSubscriberRepresentative.BP_RFSubscriberRepresentative_C"
            },
        })["returnValue"]


def compile_blueprint(blueprint):
    tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.compile_blueprint",
        {"blueprint": blueprint, "warnings_as_errors": True})


def set_defaults(blueprint, values):
    cdo = tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.get_default_object",
        {"blueprint": blueprint})["returnValue"]
    tool(
        "editor_toolset.toolsets.object.ObjectTools.set_properties",
        {"instance": cdo, "values": json.dumps(values)})


def ensure_actor(asset_path, actor_name, location, values):
    matches = tool(
        "editor_toolset.toolsets.scene.SceneTools.find_actors",
        {"name": actor_name, "tag": "", "collision_channels": []})["returnValue"]
    actor = matches[0] if matches else tool(
        "editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset",
        {
            "asset_path": asset_path,
            "name": actor_name,
            "xform": {
                "location": location,
                "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
                "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
            },
            "snap_to_ground": False,
        })["returnValue"]
    tool(
        "editor_toolset.toolsets.object.ObjectTools.set_properties",
        {"instance": actor, "values": json.dumps(values)})
    tool(
        "editor_toolset.toolsets.scene.SceneTools.set_actor_folder",
        {"actor": actor, "folder_path": "RealmFoundry/Visible Staff"})
    return actor


def run():
    developer = create_child("BP_RFDeveloperStaff")
    game_master = create_child("BP_RFGameMasterStaff")
    compile_blueprint(developer)
    compile_blueprint(game_master)
    set_defaults(developer, {
        "realName": "Avery Chen",
        "characterName": "ENGINEERING",
        "className": "Realm Developer",
        "staffRole": "Developer",
        "currentActivity": "Developer at workstation",
        "inventorySummary": "Build tools, profiler, bug queue",
        "isStaff": True,
        "hasQuest": False,
        "isCheating": False,
        "orbitRadius": 95.0,
        "happiness": 82.0,
    })
    set_defaults(game_master, {
        "realName": "Jordan Reyes",
        "characterName": "GAME MASTER",
        "className": "Live Operations GM",
        "staffRole": "Game Master",
        "currentActivity": "Game Master resolving tickets",
        "inventorySummary": "Moderation console, escalation queue",
        "isStaff": True,
        "hasQuest": False,
        "isCheating": False,
        "orbitRadius": 115.0,
        "happiness": 76.0,
    })
    compile_blueprint(developer)
    compile_blueprint(game_master)

    staff = [
        ensure_actor(
            "/Game/Characters/Staff/BP_RFDeveloperStaff.BP_RFDeveloperStaff",
            "RF_Developer_Avery",
            {"x": -620.0, "y": -240.0, "z": 65.0},
            {"RealName": "Avery Chen", "PhaseOffset": 0.0}),
        ensure_actor(
            "/Game/Characters/Staff/BP_RFDeveloperStaff.BP_RFDeveloperStaff",
            "RF_Developer_Samira",
            {"x": -620.0, "y": 240.0, "z": 65.0},
            {"RealName": "Samira Okafor", "PhaseOffset": 180.0}),
        ensure_actor(
            "/Game/Characters/Staff/BP_RFGameMasterStaff.BP_RFGameMasterStaff",
            "RF_GameMaster_Jordan",
            {"x": 620.0, "y": -240.0, "z": 65.0},
            {"RealName": "Jordan Reyes", "PhaseOffset": 90.0}),
        ensure_actor(
            "/Game/Characters/Staff/BP_RFGameMasterStaff.BP_RFGameMasterStaff",
            "RF_GameMaster_Mika",
            {"x": 620.0, "y": 240.0, "z": 65.0},
            {"RealName": "Mika Laurent", "PhaseOffset": 270.0}),
    ]
    tool(
        "editor_toolset.toolsets.asset.AssetTools.save_assets",
        {"asset_paths": []})
    return {
        "developer_blueprint": developer["refPath"],
        "gm_blueprint": game_master["refPath"],
        "staff_actors": [actor["refPath"] for actor in staff],
        "status": "four visible developer and game-master staff actors created",
    }
