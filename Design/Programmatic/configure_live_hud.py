import json


def tool(name, args):
    return execute_tool(name, json.dumps(args))


def run():
    widget = {"refPath": "/Game/UI/WBP_RFOperatorHUD.WBP_RFOperatorHUD"}
    graph = tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.get_graph",
        {"blueprint": widget, "graph_name": "EventGraph"})["returnValue"]

    code = r'''
(event UserInterface|EventPreConstruct (IsDesignTime))

(event UserInterface|EventConstruct)

(event UserInterface|EventTick (MyGeometry InDeltaTime)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then
      (bind cashLine (Utilities|String|Append
        (Utilities|String|Append
          (Utilities|String|Append "TREASURY  $" (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetCash strategy)))
          (Utilities|String|Append "     SUBSCRIBERS  " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetSubscribers strategy))))
        (Utilities|String|Append "     PRICE  $" (Utilities|String|ToString(Float) (Class|BPRFStrategyCameraPawn|GetPriceSubscription strategy)))))
      (Class|Text|SetText :self (Variables|WBP_RFOperatorHUD|GetStatus) :Text (Utilities|Text|ToText(String) cashLine))

      (bind objectiveLine (Utilities|String|Append
        (Utilities|String|Append "MANAGEMENT PANEL  " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetActivePanel strategy)))
        (Utilities|String|Append "     TECHNOLOGY TIER  " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetTechTier strategy)))))
      (Class|Text|SetText :self (Variables|WBP_RFOperatorHUD|GetObjective) :Text (Utilities|Text|ToText(String) objectiveLine))

      (bind metricLine (Utilities|String|Append
        (Utilities|String|Append
          (Utilities|String|Append "REALM DAY  " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetCurrentDay strategy)))
          (Utilities|String|Append "     ACTIVE  " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetActivePlayers strategy))))
        (Utilities|String|Append "     HAPPINESS  " (Utilities|String|ToString(Float) (Class|BPRFStrategyCameraPawn|GetHappiness strategy)))))
      (Class|Text|SetText :self (Variables|WBP_RFOperatorHUD|GetMetrics) :Text (Utilities|Text|ToText(String) metricLine))

      (bind buildLine (Utilities|String|Append
        (Utilities|String|Append
          (Utilities|String|Append "BUILD CARD  " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetSelectedBuildType strategy)))
          (Utilities|String|Append "     REQUIRES TIER  " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetRequiredBuildTier strategy))))
        (Utilities|String|Append
          (Utilities|String|Append "     CAPACITY  " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetServerCapacity strategy)))
          (Utilities|String|Append "     LOAD  " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetNetworkLoad strategy))))))
      (Class|Text|SetText :self (Variables|WBP_RFOperatorHUD|GetNetwork) :Text (Utilities|Text|ToText(String) buildLine))

      (bind researchLine (Utilities|String|Append
        (Utilities|String|Append
          (Utilities|String|Append "RESEARCH  " (Class|BPRFStrategyCameraPawn|GetActiveResearch strategy))
          (Utilities|String|Append "     PROGRESS  " (Utilities|String|ToString(Float) (Class|BPRFStrategyCameraPawn|GetResearchProgress strategy))))
        (Utilities|String|Append
          (Utilities|String|Append "     REVENUE  $" (Utilities|String|ToString(Float) (Class|BPRFStrategyCameraPawn|GetRevenueToday strategy)))
          (Utilities|String|Append "     PROFIT  $" (Utilities|String|ToString(Float) (Class|BPRFStrategyCameraPawn|GetProfitToday strategy))))))
      (Class|Text|SetText :self (Variables|WBP_RFOperatorHUD|GetSystems) :Text (Utilities|Text|ToText(String) researchLine))

      (Class|Text|SetText :self (Variables|WBP_RFOperatorHUD|GetControls) :Text (Utilities|Text|ToText(String) "0 INSPECT | 1-6 BUILD | T RESEARCH | -/+ PRICE | F FOLLOW | F5 SAVE | F9 LOAD | R RELEASE"))

      (bind selectionLine (Utilities|String|Append
        (Utilities|String|Append "SELECTED SUBSCRIBER  " (Class|BPRFStrategyCameraPawn|GetSelectedSubscriberName strategy))
        (Utilities|String|Append "     //  " (Class|BPRFStrategyCameraPawn|GetLastNotification strategy))))
      (Class|Text|SetText :self (Variables|WBP_RFOperatorHUD|GetRelease) :Text (Utilities|Text|ToText(String) selectionLine)))
    (:CastFailed)))

(event OnClicked(BtnInspect)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then
      (Class|BPRFStrategyCameraPawn|SetSelectedBuildType :self strategy :SelectedBuildType 0)
      (Class|BPRFStrategyCameraPawn|SetRequiredBuildTier :self strategy :RequiredBuildTier 0)
      (Class|BPRFStrategyCameraPawn|SetLastNotification :self strategy :LastNotification "Inspection mode: click a subscriber"))
    (:CastFailed)))

(event OnClicked(BtnInn)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then
      (Class|BPRFStrategyCameraPawn|SetSelectedBuildType :self strategy :SelectedBuildType 1)
      (Class|BPRFStrategyCameraPawn|SetRequiredBuildTier :self strategy :RequiredBuildTier 0)
      (Class|BPRFStrategyCameraPawn|SetLastNotification :self strategy :LastNotification "Grand Inn build card selected"))
    (:CastFailed)))

(event OnClicked(BtnSmithy)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then
      (Class|BPRFStrategyCameraPawn|SetSelectedBuildType :self strategy :SelectedBuildType 2)
      (Class|BPRFStrategyCameraPawn|SetRequiredBuildTier :self strategy :RequiredBuildTier 2)
      (Class|BPRFStrategyCameraPawn|SetLastNotification :self strategy :LastNotification "Blacksmith requires technology tier 2"))
    (:CastFailed)))

(event OnClicked(BtnResearch)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then (Class|BPRFStrategyCameraPawn|ResearchNext :self strategy))
    (:CastFailed)))

(event OnClicked(BtnFollow)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then (Class|BPRFStrategyCameraPawn|FollowSelectedSubscriber :self strategy))
    (:CastFailed)))

(event OnClicked(BtnRelease)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then (Class|BPRFStrategyCameraPawn|PublishUpdate :self strategy))
    (:CastFailed)))
'''
    tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.write_graph_dsl",
        {"graph": graph, "code": code})
    tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.compile_blueprint",
        {"blueprint": widget, "warnings_as_errors": True})
    tool(
        "editor_toolset.toolsets.asset.AssetTools.save_assets",
        {"asset_paths": []})
    return {
        "widget": widget["refPath"],
        "status": "operator HUD now renders live strategy, research, build and subscriber state",
    }
