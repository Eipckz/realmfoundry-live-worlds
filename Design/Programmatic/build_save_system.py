import json


def tool(name, args):
    return execute_tool(name, json.dumps(args))


BT = "editor_toolset.toolsets.blueprint.BlueprintTools"


def add_variable(blueprint, name, type_name):
    variables = tool(f"{BT}.list_variables", {"blueprint": blueprint})["returnValue"]
    if name not in variables:
        tool(f"{BT}.add_variable", {
            "blueprint": blueprint,
            "name": name,
            "type_name": type_name,
        })


def ensure_function(blueprint, name):
    graphs = tool(f"{BT}.list_graphs", {"blueprint": blueprint})["returnValue"]
    for graph in graphs:
        if graph["refPath"].endswith(":" + name):
            return graph
    return tool(f"{BT}.add_function_graph", {
        "blueprint": blueprint,
        "graph_name": name,
    })["returnValue"]


def run():
    save_bp = {"refPath": "/Game/Core/Save/BP_RFSaveGame.BP_RFSaveGame"}
    strategy = {"refPath": "/Game/Core/Camera/BP_RFStrategyCameraPawn.BP_RFStrategyCameraPawn"}
    for name, type_name in [
        ("TechTier", "int"),
        ("BuildCount", "int"),
        ("Hype", "float"),
        ("SelectedBuildType", "int"),
        ("RequiredBuildTier", "int"),
        ("Researching", "bool"),
        ("ResearchProgress", "float"),
        ("ResearchDuration", "float"),
        ("ActiveResearch", "string"),
        ("PriceSubscription", "float"),
    ]:
        add_variable(save_bp, name, type_name)
    tool(f"{BT}.compile_blueprint", {"blueprint": save_bp, "warnings_as_errors": True})

    save_graph = ensure_function(strategy, "SaveRealm")
    save_code = r'''
(fn SaveRealm ()
  (bind rawSave (SaveGame|CreateSaveGameObject "/Game/Core/Save/BP_RFSaveGame.BP_RFSaveGame_C"))
  (bind realmSave (Utilities|Casting|CastToBP_RFSaveGame :Object rawSave)
    (:then
      (Class|BPRFSaveGame|SetCash :self realmSave :Cash (Variables|Default|GetCash))
      (Class|BPRFSaveGame|SetSubscribers :self realmSave :Subscribers (Variables|Default|GetSubscribers))
      (Class|BPRFSaveGame|SetTechTier :self realmSave :TechTier (Variables|Default|GetTechTier))
      (Class|BPRFSaveGame|SetBuildCount :self realmSave :BuildCount (Variables|Default|GetBuildCount))
      (Class|BPRFSaveGame|SetHype :self realmSave :Hype (Variables|Default|GetHype))
      (Class|BPRFSaveGame|SetSavedatDay :self realmSave :SavedAtDay (Variables|Default|GetCurrentDay))
      (Class|BPRFSaveGame|SetSelectedBuildType :self realmSave :SelectedBuildType (Variables|Default|GetSelectedBuildType))
      (Class|BPRFSaveGame|SetRequiredBuildTier :self realmSave :RequiredBuildTier (Variables|Default|GetRequiredBuildTier))
      (Class|BPRFSaveGame|SetResearching :self realmSave :Researching (Variables|Default|GetResearching))
      (Class|BPRFSaveGame|SetResearchProgress :self realmSave :ResearchProgress (Variables|Default|GetResearchProgress))
      (Class|BPRFSaveGame|SetResearchDuration :self realmSave :ResearchDuration (Variables|Default|GetResearchDuration))
      (Class|BPRFSaveGame|SetActiveResearch :self realmSave :ActiveResearch (Variables|Default|GetActiveResearch))
      (Class|BPRFSaveGame|SetPriceSubscription :self realmSave :PriceSubscription (Variables|Default|GetPriceSubscription))
      (if (SaveGame|SaveGametoSlot realmSave "RealmFoundry_Auto" 0)
        (Variables|Default|SetLastNotification "Realm saved to RealmFoundry_Auto")
        (Development|PrintString "REALM SAVED // F9 RESTORES THIS STATE" true true "(R=0.180000,G=1.000000,B=0.650000,A=1.000000)" 4.0)
        (else
          (Variables|Default|SetLastNotification "Save failed")
          (Development|PrintString "SAVE FAILED" true true "(R=1.000000,G=0.200000,B=0.120000,A=1.000000)" 4.0))))
    (:CastFailed
      (Variables|Default|SetLastNotification "Save object creation failed"))))
'''
    tool(f"{BT}.write_graph_dsl", {"graph": save_graph, "code": save_code})

    load_graph = ensure_function(strategy, "LoadRealm")
    load_code = r'''
(fn LoadRealm ()
  (if (SaveGame|DoesSaveGameExist "RealmFoundry_Auto" 0)
    (bind rawSave (SaveGame|LoadGamefromSlot "RealmFoundry_Auto" 0))
    (bind realmSave (Utilities|Casting|CastToBP_RFSaveGame :Object rawSave)
      (:then
        (Variables|Default|SetCash (Class|BPRFSaveGame|GetCash realmSave))
        (Variables|Default|SetSubscribers (Class|BPRFSaveGame|GetSubscribers realmSave))
        (Variables|Default|SetTechTier (Class|BPRFSaveGame|GetTechTier realmSave))
        (Variables|Default|SetBuildCount (Class|BPRFSaveGame|GetBuildCount realmSave))
        (Variables|Default|SetHype (Class|BPRFSaveGame|GetHype realmSave))
        (Variables|Default|SetCurrentDay (Class|BPRFSaveGame|GetSavedatDay realmSave))
        (Variables|Default|SetSelectedBuildType (Class|BPRFSaveGame|GetSelectedBuildType realmSave))
        (Variables|Default|SetRequiredBuildTier (Class|BPRFSaveGame|GetRequiredBuildTier realmSave))
        (Variables|Default|SetResearching (Class|BPRFSaveGame|GetResearching realmSave))
        (Variables|Default|SetResearchProgress (Class|BPRFSaveGame|GetResearchProgress realmSave))
        (Variables|Default|SetResearchDuration (Class|BPRFSaveGame|GetResearchDuration realmSave))
        (Variables|Default|SetActiveResearch (Class|BPRFSaveGame|GetActiveResearch realmSave))
        (Variables|Default|SetPriceSubscription (Class|BPRFSaveGame|GetPriceSubscription realmSave))
        (Variables|Default|SetLastNotification "Realm state restored from disk")
        (Development|PrintString "REALM RESTORED // STATE LOADED FROM DISK" true true "(R=0.150000,G=0.780000,B=1.000000,A=1.000000)" 4.0))
      (:CastFailed
        (Variables|Default|SetLastNotification "Load failed: incompatible save")))
    (else
      (Variables|Default|SetLastNotification "No RealmFoundry_Auto save exists")
      (Development|PrintString "NO SAVE FOUND // PRESS F5 FIRST" true true "(R=1.000000,G=0.500000,B=0.150000,A=1.000000)" 4.0))))
'''
    tool(f"{BT}.write_graph_dsl", {"graph": load_graph, "code": load_code})
    tool(f"{BT}.compile_blueprint", {"blueprint": strategy, "warnings_as_errors": True})
    tool("editor_toolset.toolsets.asset.AssetTools.save_assets", {"asset_paths": []})
    return {
        "save_blueprint": save_bp["refPath"],
        "strategy": strategy["refPath"],
        "slot": "RealmFoundry_Auto",
        "status": "disk-backed save and load functions compiled",
    }
