import json


def tool(name, args):
    return execute_tool(name, json.dumps(args))


def run():
    widget = {"refPath": "/Game/UI/WBP_RFOperatorHUD.WBP_RFOperatorHUD"}
    graph = tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.get_graph",
        {"blueprint": widget, "graph_name": "EventGraph"},
    )["returnValue"]
    code = r'''
(event UserInterface|EventPreConstruct (IsDesignTime))

(event UserInterface|EventConstruct)

(event UserInterface|EventTick (MyGeometry InDeltaTime)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then
      (bind serverState (select (Class|BPRFStrategyCameraPawn|GetServersOnline strategy) "ONLINE" "MAINTENANCE"))
      (bind statusLine (Utilities|String|Append
        (Utilities|String|Append
          (Utilities|String|Append "TREASURY $" (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetCash strategy)))
          (Utilities|String|Append "   SUBS " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetSubscribers strategy))))
        (Utilities|String|Append
          (Utilities|String|Append "   PRICE $" (Utilities|String|ToString(Float) (Class|BPRFStrategyCameraPawn|GetPriceSubscription strategy)))
          (Utilities|String|Append "   SERVERS " serverState))))
      (Class|Text|SetText :self (Variables|WBP_RFOperatorHUD|GetStatus) :Text (Utilities|Text|ToText(String) statusLine))

      (bind objectiveLine (Utilities|String|Append
        (Utilities|String|Append
          (Utilities|String|Append "CAMPAIGN " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetCampaignStage strategy)))
          (Utilities|String|Append "   TECH " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetTechTier strategy))))
        (Utilities|String|Append "   // " (Class|BPRFStrategyCameraPawn|GetCampaignStatus strategy))))
      (Class|Text|SetText :self (Variables|WBP_RFOperatorHUD|GetObjective) :Text (Utilities|Text|ToText(String) objectiveLine))

      (bind metricLine (Utilities|String|Append
        (Utilities|String|Append
          (Utilities|String|Append
            (Utilities|String|Append "DAY " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetCurrentDay strategy)))
            (Utilities|String|Append "   ACTIVE " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetActivePlayers strategy))))
          (Utilities|String|Append "   HAPPY " (Utilities|String|ToString(Float) (Class|BPRFStrategyCameraPawn|GetHappiness strategy))))
        (Utilities|String|Append
          (Utilities|String|Append "   RATING " (Utilities|String|ToString(Float) (Class|BPRFStrategyCameraPawn|GetRating strategy)))
          (Utilities|String|Append "   RIVAL " (Utilities|String|ToString(Float) (Class|BPRFStrategyCameraPawn|GetCompetitorScore strategy))))))
      (Class|Text|SetText :self (Variables|WBP_RFOperatorHUD|GetMetrics) :Text (Utilities|Text|ToText(String) metricLine))

      (bind networkLine (Utilities|String|Append
        (Utilities|String|Append
          (Utilities|String|Append
            (Utilities|String|Append "CAP " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetServerCapacity strategy)))
            (Utilities|String|Append "   LOAD " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetNetworkLoad strategy))))
          (Utilities|String|Append "   COVER " (Utilities|String|ToString(Float) (Class|BPRFStrategyCameraPawn|GetNetworkCoverage strategy))))
        (Utilities|String|Append
          (Utilities|String|Append "   BANDWIDTH " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetBandwidth strategy)))
          (Utilities|String|Append "   CONGEST " (Utilities|String|ToString(Float) (Class|BPRFStrategyCameraPawn|GetCongestionPercent strategy))))))
      (Class|Text|SetText :self (Variables|WBP_RFOperatorHUD|GetNetwork) :Text (Utilities|Text|ToText(String) networkLine))

      (bind systemsLine (Utilities|String|Append
        (Utilities|String|Append
          (Utilities|String|Append
            (Utilities|String|Append "QUESTS " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetQuestCompletions strategy)))
            (Utilities|String|Append "   PARTIES " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetPartyCount strategy))))
          (Utilities|String|Append "   COMBAT " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetCombatEncounters strategy))))
        (Utilities|String|Append
          (Utilities|String|Append "   DUNGEONS " (Utilities|String|ToString(Integer) (Class|BPRFStrategyCameraPawn|GetDungeonRuns strategy)))
          (Utilities|String|Append "   BUGS " (Utilities|String|ToString(Integer) (+ (Class|BPRFStrategyCameraPawn|GetCrashBugs strategy) (+ (Class|BPRFStrategyCameraPawn|GetMajorBugs strategy) (Class|BPRFStrategyCameraPawn|GetMinorBugs strategy))))))))
      (Class|Text|SetText :self (Variables|WBP_RFOperatorHUD|GetSystems) :Text (Utilities|Text|ToText(String) systemsLine))

      (Class|Text|SetText :self (Variables|WBP_RFOperatorHUD|GetControls) :Text (Utilities|Text|ToText(String) "BUILD: CLICK TYPE + WORLD   |   Q/E ROTATE   |   U/I UNDO/REDO   |   F5/F9 SAVE/LOAD"))

      (bind selectionLine (Utilities|String|Append
        (Utilities|String|Append
          (Utilities|String|Append "PROFILE " (Class|BPRFStrategyCameraPawn|GetSelectedProfileSummary strategy))
          (Utilities|String|Append "   // " (Class|BPRFStrategyCameraPawn|GetSelectedActivitySummary strategy)))
        (Utilities|String|Append "   // " (Class|BPRFStrategyCameraPawn|GetLastNotification strategy))))
      (Class|Text|SetText :self (Variables|WBP_RFOperatorHUD|GetRelease) :Text (Utilities|Text|ToText(String) selectionLine)))
    (:CastFailed)))

(event OnClicked(BtnInspect)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then
      (Class|BPRFStrategyCameraPawn|SetSelectedBuildType :self strategy :SelectedBuildType 0)
      (Class|BPRFStrategyCameraPawn|SetRequiredBuildTier :self strategy :RequiredBuildTier 0)
      (Class|BPRFStrategyCameraPawn|SetLastNotification :self strategy :LastNotification "Inspection mode: click the world to select a subscriber"))
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
      (Class|BPRFStrategyCameraPawn|SetLastNotification :self strategy :LastNotification "Blacksmith requires Commerce tier 2"))
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

(event OnClicked(BtnServices)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then (Class|BPRFStrategyCameraPawn|OperateServices :self strategy))
    (:CastFailed)))

(event OnClicked(BtnNetwork)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then (Class|BPRFStrategyCameraPawn|UpgradeNetwork :self strategy))
    (:CastFailed)))

(event OnClicked(BtnQuests)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then (Class|BPRFStrategyCameraPawn|LaunchQuestSeason :self strategy))
    (:CastFailed)))

(event OnClicked(BtnCombat)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then (Class|BPRFStrategyCameraPawn|RunCombatTournament :self strategy))
    (:CastFailed)))

(event OnClicked(BtnDungeon)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then (Class|BPRFStrategyCameraPawn|LaunchDungeonExpedition :self strategy))
    (:CastFailed)))

(event OnClicked(BtnLiveOps)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then (Class|BPRFStrategyCameraPawn|RunLiveOperations :self strategy))
    (:CastFailed)))

(event OnClicked(BtnPriceDown)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then
      (if (> (Class|BPRFStrategyCameraPawn|GetPriceSubscription strategy) 1.0)
        (Class|BPRFStrategyCameraPawn|SetPriceSubscription :self strategy :PriceSubscription (- (Class|BPRFStrategyCameraPawn|GetPriceSubscription strategy) 0.5)))
      (Class|BPRFStrategyCameraPawn|SetLastNotification :self strategy :LastNotification "Subscription price reduced"))
    (:CastFailed)))

(event OnClicked(BtnPriceUp)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then
      (Class|BPRFStrategyCameraPawn|SetPriceSubscription :self strategy :PriceSubscription (+ (Class|BPRFStrategyCameraPawn|GetPriceSubscription strategy) 0.5))
      (Class|BPRFStrategyCameraPawn|SetLastNotification :self strategy :LastNotification "Subscription price increased"))
    (:CastFailed)))

(event OnClicked(BtnRotate)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then
      (Class|BPRFStrategyCameraPawn|SetConstructionRotation :self strategy :ConstructionRotation (+ (Class|BPRFStrategyCameraPawn|GetConstructionRotation strategy) 45.0))
      (Class|BPRFStrategyCameraPawn|SetLastNotification :self strategy :LastNotification "Construction rotated right 45 degrees"))
    (:CastFailed)))

(event OnClicked(BtnUndo)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then (Class|BPRFStrategyCameraPawn|UndoLastBuilding :self strategy))
    (:CastFailed)))

(event OnClicked(BtnRedo)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then (Class|BPRFStrategyCameraPawn|RedoLastBuilding :self strategy))
    (:CastFailed)))

(event OnClicked(BtnSave)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then (Class|BPRFStrategyCameraPawn|SaveRealm :self strategy))
    (:CastFailed)))

(event OnClicked(BtnLoad)
  (bind strategy (Utilities|Casting|CastToBP_RFStrategyCameraPawn :Object (Game|GetPlayerPawn 0))
    (:then (Class|BPRFStrategyCameraPawn|LoadRealm :self strategy))
    (:CastFailed)))
'''
    tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.write_graph_dsl",
        {"graph": graph, "code": code},
    )
    tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.compile_blueprint",
        {"blueprint": widget, "warnings_as_errors": True},
    )
    tool("editor_toolset.toolsets.asset.AssetTools.save_assets", {"asset_paths": []})
    return {"widget": widget["refPath"], "status": "full management HUD compiled"}
