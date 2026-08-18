import json


BT = "editor_toolset.toolsets.blueprint.BlueprintTools"


def tool(name, args):
    return execute_tool(name, json.dumps(args))


def variables(blueprint):
    return tool(f"{BT}.list_variables", {"blueprint": blueprint})["returnValue"]


def add_variable(blueprint, name, type_name, container_type=None):
    if name in variables(blueprint):
        return
    args = {"blueprint": blueprint, "name": name, "type_name": type_name}
    if container_type:
        args["container_type"] = container_type
    tool(f"{BT}.add_variable", args)


def add_object_variable(blueprint, name, object_class, container_type=None):
    if name in variables(blueprint):
        return
    args = {
        "blueprint": blueprint,
        "name": name,
        "object_class": {"refPath": object_class},
    }
    if container_type:
        args["container_type"] = container_type
    tool(f"{BT}.add_object_variable", args)


def ensure_function(blueprint, name):
    for graph in tool(f"{BT}.list_graphs", {"blueprint": blueprint})["returnValue"]:
        if graph["refPath"].endswith(":" + name):
            return graph, False
    return tool(f"{BT}.add_function_graph", {
        "blueprint": blueprint,
        "graph_name": name,
    })["returnValue"], True


def write(graph, code):
    tool(f"{BT}.write_graph_dsl", {"graph": graph, "code": code})


def run():
    strategy = {"refPath": "/Game/Core/Camera/BP_RFStrategyCameraPawn.BP_RFStrategyCameraPawn"}
    save_game = {"refPath": "/Game/Core/Save/BP_RFSaveGame.BP_RFSaveGame"}

    add_variable(strategy, "PlacedBuildTypes", "int", "ARRAY")
    add_variable(strategy, "PlacedBuildTransforms", "Transform", "ARRAY")
    add_object_variable(strategy, "PlacedBuildActors", "/Script/Engine.Actor", "ARRAY")
    add_variable(strategy, "RedoBuildTypes", "int", "ARRAY")
    add_variable(strategy, "RedoBuildTransforms", "Transform", "ARRAY")
    add_variable(strategy, "ScratchBuildTransforms", "Transform", "ARRAY")
    add_object_variable(strategy, "ScratchBuildActors", "/Script/Engine.Actor", "ARRAY")
    add_variable(strategy, "ScratchRedoTransforms", "Transform", "ARRAY")
    add_variable(strategy, "EmptyBuildTransforms", "Transform", "ARRAY")
    add_object_variable(strategy, "EmptyBuildActors", "/Script/Engine.Actor", "ARRAY")
    add_variable(strategy, "ConstructionRotation", "float")
    add_variable(strategy, "UndoDepth", "int")
    add_variable(strategy, "RedoDepth", "int")

    add_variable(save_game, "PlacedBuildTypes", "int", "ARRAY")
    add_variable(save_game, "PlacedBuildTransforms", "Transform", "ARRAY")
    add_variable(save_game, "ConstructionRotation", "float")
    tool(f"{BT}.compile_blueprint", {"blueprint": save_game, "warnings_as_errors": True})
    tool(f"{BT}.compile_blueprint", {"blueprint": strategy, "warnings_as_errors": True})

    register, created = ensure_function(strategy, "RegisterPlacedBuilding")
    if created:
        tool(f"{BT}.add_function_param", {
            "graph": register, "param_name": "BuildType", "param_type": "int", "input_param": True})
        tool(f"{BT}.add_object_function_param", {
            "graph": register, "param_name": "BuildActor",
            "object_class": {"refPath": "/Script/Engine.Actor"}, "input_param": True})
        tool(f"{BT}.add_struct_function_param", {
            "graph": register, "param_name": "BuildTransform",
            "struct_type": {"refPath": "/Script/CoreUObject.Transform"}, "input_param": True})
    write(register, r'''
(fn RegisterPlacedBuilding (BuildType BuildActor BuildTransform)
  (Utilities|Array|Add :TargetArray (Variables|Default|GetPlacedBuildTypes) :NewItem BuildType)
  (Utilities|Array|Add :TargetArray (Variables|Default|GetPlacedBuildTransforms) :NewItem BuildTransform)
  (Utilities|Array|Add :TargetArray (Variables|Default|GetPlacedBuildActors) :NewItem BuildActor)
  (Utilities|Array|Clear (Variables|Default|GetRedoBuildTypes))
  (Utilities|Array|Clear (Variables|Default|GetRedoBuildTransforms))
  (Variables|Default|SetUndoDepth (Utilities|Array|Length (Variables|Default|GetPlacedBuildTypes)))
  (Variables|Default|SetRedoDepth 0))
''')

    deactivate, created = ensure_function(strategy, "DeactivateBuilding")
    if created:
        tool(f"{BT}.add_object_function_param", {
            "graph": deactivate, "param_name": "BuildActor",
            "object_class": {"refPath": "/Script/Engine.Actor"}, "input_param": True})
    write(deactivate, r'''
(fn DeactivateBuilding (BuildActor)
  (Rendering|SetActorHiddenInGame :self BuildActor :bNewHidden true)
  (Collision|SetActorEnableCollision :self BuildActor :bNewActorEnableCollision false)
  (Transformation|SetActorLocation :self BuildActor :NewLocation (Math|Vector|MakeVector 0.0 0.0 -50000.0) :bSweep false :bTeleport true))
''')

    undo, _ = ensure_function(strategy, "UndoLastBuilding")
    write(undo, r'''
(fn UndoLastBuilding ()
  (bind count (Utilities|Array|Length (Variables|Default|GetPlacedBuildTypes)))
  (if (> count 0)
    (bind index (- count 1))
    (bind buildType (Utilities|Array|Get(acopy) (Variables|Default|GetPlacedBuildTypes) index))
    (bind buildTransform (Utilities|Array|Get(acopy) (Variables|Default|GetPlacedBuildTransforms) index))
    (bind buildActor (Utilities|Array|Get(acopy) (Variables|Default|GetPlacedBuildActors) index))
    (Utilities|Array|Add :TargetArray (Variables|Default|GetRedoBuildTypes) :NewItem buildType)
    (Utilities|Array|Add :TargetArray (Variables|Default|GetRedoBuildTransforms) :NewItem buildTransform)
    (CallFunction|DeactivateBuilding :BuildActor buildActor)
    (Variables|Default|SetScratchBuildTransforms (Variables|Default|GetEmptyBuildTransforms))
    (Variables|Default|SetScratchBuildActors (Variables|Default|GetEmptyBuildActors))
    (for j (range index)
      (Utilities|Array|Add :TargetArray (Variables|Default|GetScratchBuildTransforms) :NewItem (Utilities|Array|Get(acopy) (Variables|Default|GetPlacedBuildTransforms) j))
      (Utilities|Array|Add :TargetArray (Variables|Default|GetScratchBuildActors) :NewItem (Utilities|Array|Get(acopy) (Variables|Default|GetPlacedBuildActors) j)))
    (Utilities|Array|Resize :TargetArray (Variables|Default|GetPlacedBuildTypes) :Size index)
    (Variables|Default|SetPlacedBuildTransforms (Variables|Default|GetScratchBuildTransforms))
    (Variables|Default|SetPlacedBuildActors (Variables|Default|GetScratchBuildActors))
    (if (> (Variables|Default|GetBuildCount) 0)
      (Variables|Default|SetBuildCount (- (Variables|Default|GetBuildCount) 1)))
    (Variables|Default|SetCash (+ (Variables|Default|GetCash) 1250.0))
    (Variables|Default|SetUndoDepth (Utilities|Array|Length (Variables|Default|GetPlacedBuildTypes)))
    (Variables|Default|SetRedoDepth (Utilities|Array|Length (Variables|Default|GetRedoBuildTypes)))
    (Variables|Default|SetLastNotification "Undo complete: last building removed and half cost refunded")
    (else
      (Variables|Default|SetLastNotification "Undo unavailable: no player-built structures"))))
''')

    commit_redo, created = ensure_function(strategy, "CommitRedoBuilding")
    if created:
        tool(f"{BT}.add_function_param", {
            "graph": commit_redo, "param_name": "BuildType", "param_type": "int", "input_param": True})
        tool(f"{BT}.add_object_function_param", {
            "graph": commit_redo, "param_name": "BuildActor",
            "object_class": {"refPath": "/Script/Engine.Actor"}, "input_param": True})
        tool(f"{BT}.add_struct_function_param", {
            "graph": commit_redo, "param_name": "BuildTransform",
            "struct_type": {"refPath": "/Script/CoreUObject.Transform"}, "input_param": True})
        tool(f"{BT}.add_function_param", {
            "graph": commit_redo, "param_name": "RemainingCount", "param_type": "int", "input_param": True})
    write(commit_redo, r'''
(fn CommitRedoBuilding (BuildType BuildActor BuildTransform RemainingCount)
  (Utilities|Array|Add :TargetArray (Variables|Default|GetPlacedBuildTypes) :NewItem BuildType)
  (Utilities|Array|Add :TargetArray (Variables|Default|GetPlacedBuildTransforms) :NewItem BuildTransform)
  (Utilities|Array|Add :TargetArray (Variables|Default|GetPlacedBuildActors) :NewItem BuildActor)
  (Variables|Default|SetScratchRedoTransforms (Variables|Default|GetEmptyBuildTransforms))
  (for j (range RemainingCount)
    (Utilities|Array|Add :TargetArray (Variables|Default|GetScratchRedoTransforms) :NewItem (Utilities|Array|Get(acopy) (Variables|Default|GetRedoBuildTransforms) j)))
  (Utilities|Array|Resize :TargetArray (Variables|Default|GetRedoBuildTypes) :Size RemainingCount)
  (Variables|Default|SetRedoBuildTransforms (Variables|Default|GetScratchRedoTransforms))
  (Variables|Default|SetBuildCount (+ (Variables|Default|GetBuildCount) 1))
  (Variables|Default|SetUndoDepth (Utilities|Array|Length (Variables|Default|GetPlacedBuildTypes)))
  (Variables|Default|SetRedoDepth (Utilities|Array|Length (Variables|Default|GetRedoBuildTypes)))
  (Variables|Default|SetLastNotification "Redo complete: structure restored"))
''')

    redo, _ = ensure_function(strategy, "RedoLastBuilding")
    write(redo, r'''
(fn RedoLastBuilding ()
  (bind count (Utilities|Array|Length (Variables|Default|GetRedoBuildTypes)))
  (if (> count 0)
    (bind index (- count 1))
    (bind buildType (Utilities|Array|Get(acopy) (Variables|Default|GetRedoBuildTypes) index))
    (bind buildTransform (Utilities|Array|Get(acopy) (Variables|Default|GetRedoBuildTransforms) index))
    (if (== buildType 1)
      (bind spawned (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_InnV2.BP_RFBuildable_InnV2_C" :SpawnTransform buildTransform :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot"))
      (CallFunction|CommitRedoBuilding :BuildType buildType :BuildActor spawned :BuildTransform buildTransform :RemainingCount index)
      (elif (== buildType 2)
        (bind spawned2 (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_SmithyV2.BP_RFBuildable_SmithyV2_C" :SpawnTransform buildTransform :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot"))
        (CallFunction|CommitRedoBuilding :BuildType buildType :BuildActor spawned2 :BuildTransform buildTransform :RemainingCount index)
        (elif (== buildType 3)
          (bind spawned3 (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_UplinkV2.BP_RFBuildable_UplinkV2_C" :SpawnTransform buildTransform :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot"))
          (CallFunction|CommitRedoBuilding :BuildType buildType :BuildActor spawned3 :BuildTransform buildTransform :RemainingCount index)
          (elif (== buildType 4)
            (bind spawned4 (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_GuildHallV2.BP_RFBuildable_GuildHallV2_C" :SpawnTransform buildTransform :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot"))
            (CallFunction|CommitRedoBuilding :BuildType buildType :BuildActor spawned4 :BuildTransform buildTransform :RemainingCount index)
            (elif (== buildType 5)
              (bind spawned5 (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_DungeonGateV2.BP_RFBuildable_DungeonGateV2_C" :SpawnTransform buildTransform :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot"))
              (CallFunction|CommitRedoBuilding :BuildType buildType :BuildActor spawned5 :BuildTransform buildTransform :RemainingCount index)
              (elif (== buildType 6)
                (bind spawned6 (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_TravelDockV2.BP_RFBuildable_TravelDockV2_C" :SpawnTransform buildTransform :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot"))
                (CallFunction|CommitRedoBuilding :BuildType buildType :BuildActor spawned6 :BuildTransform buildTransform :RemainingCount index)))))))
    (else
      (Variables|Default|SetLastNotification "Redo unavailable: no undone structures"))))
''')

    restore, _ = ensure_function(strategy, "RestorePlacedBuildings")
    write(restore, r'''
(fn RestorePlacedBuildings ()
  (for i (range (Utilities|Array|Length (Variables|Default|GetPlacedBuildActors)))
    (bind oldActor (Utilities|Array|Get(acopy) (Variables|Default|GetPlacedBuildActors) i))
    (CallFunction|DeactivateBuilding :BuildActor oldActor))
  (Variables|Default|SetPlacedBuildActors (Variables|Default|GetEmptyBuildActors))
  (Utilities|Array|Clear (Variables|Default|GetRedoBuildTypes))
  (Utilities|Array|Clear (Variables|Default|GetRedoBuildTransforms))
  (for i (range (Utilities|Array|Length (Variables|Default|GetPlacedBuildTypes)))
    (bind buildType (Utilities|Array|Get(acopy) (Variables|Default|GetPlacedBuildTypes) i))
    (bind buildTransform (Utilities|Array|Get(acopy) (Variables|Default|GetPlacedBuildTransforms) i))
    (if (== buildType 1)
      (bind spawned (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_InnV2.BP_RFBuildable_InnV2_C" :SpawnTransform buildTransform :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot"))
      (Utilities|Array|Add :TargetArray (Variables|Default|GetPlacedBuildActors) :NewItem spawned)
      (elif (== buildType 2)
        (bind spawned2 (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_SmithyV2.BP_RFBuildable_SmithyV2_C" :SpawnTransform buildTransform :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot"))
        (Utilities|Array|Add :TargetArray (Variables|Default|GetPlacedBuildActors) :NewItem spawned2)
        (elif (== buildType 3)
          (bind spawned3 (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_UplinkV2.BP_RFBuildable_UplinkV2_C" :SpawnTransform buildTransform :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot"))
          (Utilities|Array|Add :TargetArray (Variables|Default|GetPlacedBuildActors) :NewItem spawned3)
          (elif (== buildType 4)
            (bind spawned4 (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_GuildHallV2.BP_RFBuildable_GuildHallV2_C" :SpawnTransform buildTransform :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot"))
            (Utilities|Array|Add :TargetArray (Variables|Default|GetPlacedBuildActors) :NewItem spawned4)
            (elif (== buildType 5)
              (bind spawned5 (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_DungeonGateV2.BP_RFBuildable_DungeonGateV2_C" :SpawnTransform buildTransform :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot"))
              (Utilities|Array|Add :TargetArray (Variables|Default|GetPlacedBuildActors) :NewItem spawned5)
              (elif (== buildType 6)
                (bind spawned6 (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_TravelDockV2.BP_RFBuildable_TravelDockV2_C" :SpawnTransform buildTransform :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot"))
                (Utilities|Array|Add :TargetArray (Variables|Default|GetPlacedBuildActors) :NewItem spawned6)))))))
  (Variables|Default|SetBuildCount (Utilities|Array|Length (Variables|Default|GetPlacedBuildTypes)))
  (Variables|Default|SetUndoDepth (Utilities|Array|Length (Variables|Default|GetPlacedBuildTypes)))
  (Variables|Default|SetRedoDepth 0)))
''')

    tool(f"{BT}.compile_blueprint", {"blueprint": strategy, "warnings_as_errors": True})
    tool("editor_toolset.toolsets.asset.AssetTools.save_assets", {"asset_paths": []})
    return {
        "strategy": strategy["refPath"],
        "save_game": save_game["refPath"],
        "status": "rotation, construction history, undo, redo and rebuild functions compiled",
    }
