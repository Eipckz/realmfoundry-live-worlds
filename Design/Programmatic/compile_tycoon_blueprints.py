import json


def compile_blueprint(path):
    return execute_tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.compile_blueprint",
        json.dumps({"blueprint": {"refPath": path}, "warnings_as_errors": True}))


def run():
    blueprints = [
        "/Game/Core/Camera/BP_RFStrategyCameraPawn.BP_RFStrategyCameraPawn",
        "/Game/Core/Camera/BP_RFStrategyController.BP_RFStrategyController",
        "/Game/Core/BP_RFGameMode.BP_RFGameMode",
        "/Game/Core/BP_RFSimulationManager.BP_RFSimulationManager",
        "/Game/Core/BuildablesV2/BP_RFBuildable_InnV2.BP_RFBuildable_InnV2",
        "/Game/Core/BuildablesV2/BP_RFBuildable_SmithyV2.BP_RFBuildable_SmithyV2",
        "/Game/Core/BuildablesV2/BP_RFBuildable_UplinkV2.BP_RFBuildable_UplinkV2",
        "/Game/Core/BuildablesV2/BP_RFBuildable_GuildHallV2.BP_RFBuildable_GuildHallV2",
        "/Game/Core/BuildablesV2/BP_RFBuildable_DungeonGateV2.BP_RFBuildable_DungeonGateV2",
        "/Game/Core/BuildablesV2/BP_RFBuildable_TravelDockV2.BP_RFBuildable_TravelDockV2",
    ]
    results = []
    for path in blueprints:
        results.append({"blueprint": path, "result": compile_blueprint(path)})
    return {"compiled": len(results), "results": results}
