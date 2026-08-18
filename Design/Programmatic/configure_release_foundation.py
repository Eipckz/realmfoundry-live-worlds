import json


def tool(name, args):
    return execute_tool(name, json.dumps(args))


def run():
    rep_bp = {"refPath": "/Game/Characters/Subscribers/BP_RFSubscriberRepresentative.BP_RFSubscriberRepresentative"}
    cdo = tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.get_default_object",
        {"blueprint": rep_bp})["returnValue"]
    tool(
        "editor_toolset.toolsets.object.ObjectTools.set_properties",
        {
            "instance": cdo,
            "values": json.dumps({
                "autoPossessAI": "PlacedInWorldOrSpawned",
                "aIControllerClass": {
                    "refPath": "/Game/Characters/Subscribers/BP_RFSubscriberAIController.BP_RFSubscriberAIController_C"
                },
                "bUseControllerRotationYaw": False,
            }),
        })

    components = tool(
        "editor_toolset.toolsets.actor.ActorTools.get_components",
        {"actor": cdo})["returnValue"]
    configured_mesh = None
    for component in components:
        component_class = tool(
            "editor_toolset.toolsets.object.ObjectTools.get_class",
            {"instance": component})["returnValue"]["refPath"]
        if component_class == "/Script/Engine.SkeletalMeshComponent":
            tool(
                "editor_toolset.toolsets.object.ObjectTools.set_properties",
                {
                    "instance": component,
                    "values": json.dumps({
                        "skeletalMeshAsset": {
                            "refPath": "/Game/Characters/Subscriber/SK_RFSubscriber.SK_RFSubscriber"
                        },
                        "animationMode": "AnimationSingleNode",
                        "animationData": {
                            "animToPlay": {
                                "refPath": "/Game/Characters/Subscriber/SK_RFSubscriber_Anim_A_RF_Walk.SK_RFSubscriber_Anim_A_RF_Walk"
                            },
                            "bSavedLooping": True,
                            "bSavedPlaying": True,
                            "savedPosition": 0.0,
                            "savedPlayRate": 1.0,
                        },
                        "relativeLocation": {"x": 0.0, "y": 0.0, "z": -88.0},
                        "relativeRotation": {"pitch": 0.0, "yaw": -90.0, "roll": 0.0},
                        "relativeScale3D": {"x": 1.0, "y": 1.0, "z": 1.0},
                        "bHiddenInGame": False,
                        "visibilityBasedAnimTickOption": "AlwaysTickPoseAndRefreshBones",
                    }),
                })
            configured_mesh = component["refPath"]

    tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.compile_blueprint",
        {"blueprint": rep_bp, "warnings_as_errors": True})

    existing = tool(
        "editor_toolset.toolsets.scene.SceneTools.find_actors",
        {"name": "RF Subscriber Population", "tag": "", "collision_channels": []})["returnValue"]
    if existing:
        spawner_actor = existing[0]
    else:
        spawner_actor = tool(
            "editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset",
            {
                "asset_path": "/Game/Characters/Subscribers/BP_RFSubscriberSpawner",
                "name": "RF Subscriber Population",
                "xform": {
                    "location": {"x": 0.0, "y": 0.0, "z": 0.0},
                    "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
                    "scale": {"x": 1.0, "y": 1.0, "z": 1.0},
                },
                "snap_to_ground": False,
            })["returnValue"]
        tool(
            "editor_toolset.toolsets.actor.ActorTools.add_tag",
            {"actor": spawner_actor, "tag": "RF.Subscribers.Spawner"})

    tool(
        "editor_toolset.toolsets.asset.AssetTools.save_assets",
        {"asset_paths": []})

    return {
        "representative_mesh_component": configured_mesh,
        "spawner_actor": spawner_actor,
        "status": "subscriber mesh, animation, AI controller and population spawner configured",
    }
