import json


def tool(name, args):
    return execute_tool(name, json.dumps(args))


def run():
    paths = [
        "/Game/Core/Camera/BP_RFStrategyCameraPawn.BP_RFStrategyCameraPawn",
        "/Game/Core/Save/BP_RFSaveGame.BP_RFSaveGame",
        "/Game/UI/WBP_RFOperatorHUD.WBP_RFOperatorHUD",
        "/Game/Characters/Subscribers/BP_RFSubscriberAIController.BP_RFSubscriberAIController",
        "/Game/Characters/Subscribers/BP_RFSubscriberRepresentative.BP_RFSubscriberRepresentative",
        "/Game/Characters/Subscribers/BP_RFSubscriberSpawner.BP_RFSubscriberSpawner",
        "/Game/Data/Technology/BP_RFTechnologyDefinition.BP_RFTechnologyDefinition",
    ]
    compiled = []
    for path in paths:
        blueprint = {"refPath": path}
        tool(
            "editor_toolset.toolsets.blueprint.BlueprintTools.compile_blueprint",
            {"blueprint": blueprint, "warnings_as_errors": True})
        compiled.append(path)

    representative = {"refPath": paths[4]}
    cdo = tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.get_default_object",
        {"blueprint": representative})["returnValue"]
    components = tool(
        "editor_toolset.toolsets.actor.ActorTools.get_components",
        {"actor": cdo})["returnValue"]
    component_counts = {}
    for component in components:
        class_path = tool(
            "editor_toolset.toolsets.object.ObjectTools.get_class",
            {"instance": component})["returnValue"]["refPath"]
        component_counts[class_path] = component_counts.get(class_path, 0) + 1
    if component_counts.get("/Script/Engine.SpringArmComponent", 0) != 1:
        raise RuntimeError("Subscriber representative must have exactly one SpringArmComponent")
    if component_counts.get("/Script/Engine.CameraComponent", 0) != 1:
        raise RuntimeError("Subscriber representative must have exactly one CameraComponent")

    tool("editor_toolset.toolsets.asset.AssetTools.save_assets", {"asset_paths": []})
    return {
        "compiled": compiled,
        "subscriber_component_counts": component_counts,
        "status": "release blueprints compile cleanly and subscriber camera topology is deterministic",
    }
