import json


def tool(name, args):
    return execute_tool(name, json.dumps(args))


BT = "editor_toolset.toolsets.blueprint.BlueprintTools"
OT = "editor_toolset.toolsets.object.ObjectTools"
AT = "editor_toolset.toolsets.asset.AssetTools"


def variables(blueprint):
    return tool(f"{BT}.list_variables", {"blueprint": blueprint})["returnValue"]


def ensure_variable(blueprint, name, type_name):
    if name not in variables(blueprint):
        tool(
            f"{BT}.add_variable",
            {"blueprint": blueprint, "name": name, "type_name": type_name},
        )


def ensure_function(blueprint, name):
    for graph in tool(f"{BT}.list_graphs", {"blueprint": blueprint})["returnValue"]:
        if graph["refPath"].endswith(":" + name):
            return graph, False
    return (
        tool(
            f"{BT}.add_function_graph",
            {"blueprint": blueprint, "graph_name": name},
        )["returnValue"],
        True,
    )


def write_function(blueprint, name, code):
    graph, _ = ensure_function(blueprint, name)
    tool(f"{BT}.write_graph_dsl", {"graph": graph, "code": code})


def set_defaults(blueprint, desired):
    cdo = tool(f"{BT}.get_default_object", {"blueprint": blueprint})["returnValue"]
    schema = json.loads(tool(f"{OT}.list_properties", {"instance": cdo})["returnValue"])
    canonical = {name.lower(): name for name in schema.keys()}
    values = {
        canonical[name.lower()]: value
        for name, value in desired.items()
        if name.lower() in canonical
    }
    tool(f"{OT}.set_properties", {"instance": cdo, "values": json.dumps(values)})


def run():
    strategy = {
        "refPath": "/Game/Core/Camera/BP_RFStrategyCameraPawn.BP_RFStrategyCameraPawn"
    }
    for name, type_name in [
        ("OperationsClock", "float"),
        ("CampaignStage", "int"),
        ("CampaignWon", "bool"),
        ("CampaignFailed", "bool"),
        ("CampaignStatus", "string"),
        ("Developers", "int"),
        ("GameMasters", "int"),
        ("CrashBugs", "int"),
        ("MajorBugs", "int"),
        ("MinorBugs", "int"),
        ("ServersOnline", "bool"),
        ("MaintenanceScheduled", "bool"),
        ("AntiCheatLevel", "int"),
        ("SuspectedCheaters", "int"),
        ("ModerationCases", "int"),
        ("ServiceUses", "int"),
        ("ServiceIncome", "float"),
        ("MicrotransactionIncome", "float"),
        ("RouteUses", "int"),
        ("RouteIncome", "float"),
        ("NetworkCoverage", "float"),
        ("Bandwidth", "int"),
        ("CongestionPercent", "float"),
        ("QuestTemplates", "int"),
        ("QuestCompletions", "int"),
        ("PartyCount", "int"),
        ("FriendLinks", "int"),
        ("CombatEncounters", "int"),
        ("PvPDuels", "int"),
        ("DungeonRooms", "int"),
        ("DungeonRuns", "int"),
        ("BossKills", "int"),
        ("DungeonEntryPrice", "float"),
        ("ReleasesPublished", "int"),
        ("VersionMajor", "int"),
        ("MarketingSpend", "float"),
        ("AwardsWon", "int"),
        ("CompetitorScore", "float"),
        ("ConstructionRotation", "float"),
        ("UndoDepth", "int"),
        ("RedoDepth", "int"),
        ("SelectedProfileSummary", "string"),
        ("SelectedActivitySummary", "string"),
        ("MasterVolume", "float"),
        ("TextScale", "float"),
        ("ReducedMotion", "bool"),
        ("ColorblindMode", "int"),
        ("LanguageIndex", "int"),
        ("ModsEnabled", "bool"),
    ]:
        ensure_variable(strategy, name, type_name)

    tool(f"{BT}.compile_blueprint", {"blueprint": strategy, "warnings_as_errors": True})
    set_defaults(
        strategy,
        {
            "operationsClock": 0.0,
            "campaignStage": 0,
            "campaignWon": False,
            "campaignFailed": False,
            "campaignStatus": "FOUNDING: launch one service and unlock Community",
            "developers": 3,
            "gameMasters": 1,
            "crashBugs": 0,
            "majorBugs": 2,
            "minorBugs": 6,
            "serversOnline": True,
            "maintenanceScheduled": False,
            "antiCheatLevel": 1,
            "suspectedCheaters": 3,
            "moderationCases": 0,
            "serviceUses": 0,
            "serviceIncome": 0.0,
            "microtransactionIncome": 0.0,
            "routeUses": 0,
            "routeIncome": 0.0,
            "networkCoverage": 42.0,
            "bandwidth": 1000,
            "congestionPercent": 20.0,
            "questTemplates": 3,
            "questCompletions": 0,
            "partyCount": 4,
            "friendLinks": 24,
            "combatEncounters": 0,
            "pVPDuels": 0,
            "dungeonRooms": 8,
            "dungeonRuns": 0,
            "bossKills": 0,
            "dungeonEntryPrice": 4.99,
            "releasesPublished": 0,
            "versionMajor": 1,
            "marketingSpend": 0.0,
            "awardsWon": 0,
            "competitorScore": 52.0,
            "constructionRotation": 0.0,
            "undoDepth": 0,
            "redoDepth": 0,
            "selectedProfileSummary": "No subscriber selected",
            "selectedActivitySummary": "Click a subscriber to inspect",
            "masterVolume": 0.8,
            "textScale": 1.0,
            "reducedMotion": False,
            "colorblindMode": 0,
            "languageIndex": 0,
            "modsEnabled": True,
        },
    )

    write_function(
        strategy,
        "OperateServices",
        r'''
(fn OperateServices ()
  (if (< (Variables|Default|GetTechTier) 2)
    (Variables|Default|SetLastNotification "Commerce locked: complete technology tier 2")
    (else
      (Variables|Default|SetServiceUses (+ (Variables|Default|GetServiceUses) 25))
      (Variables|Default|SetServiceIncome (+ (Variables|Default|GetServiceIncome) 625.0))
      (Variables|Default|SetMicrotransactionIncome (+ (Variables|Default|GetMicrotransactionIncome) 135.0))
      (Variables|Default|SetCash (+ (Variables|Default|GetCash) 760.0))
      (Variables|Default|SetLastNotification "Service pricing resolved: inns, shops, markets and trinkets earned $760"))))
''',
    )
    write_function(
        strategy,
        "UpgradeNetwork",
        r'''
(fn UpgradeNetwork ()
  (if (< (Variables|Default|GetTechTier) 3)
    (Variables|Default|SetLastNotification "Infrastructure locked: complete technology tier 3")
    (elif (< (Variables|Default|GetCash) 4000.0)
      (Variables|Default|SetLastNotification "Network upgrade needs $4,000")
      (else
        (Variables|Default|SetCash (- (Variables|Default|GetCash) 4000.0))
        (Variables|Default|SetServerCapacity (+ (Variables|Default|GetServerCapacity) 1200))
        (Variables|Default|SetBandwidth (+ (Variables|Default|GetBandwidth) 500))
        (Variables|Default|SetNetworkCoverage (+ (Variables|Default|GetNetworkCoverage) 8.0))
        (Variables|Default|SetRouteUses (+ (Variables|Default|GetRouteUses) 12))
        (Variables|Default|SetLastNotification "Uplink, fiber and route capacity upgraded")))))
''',
    )
    write_function(
        strategy,
        "LaunchQuestSeason",
        r'''
(fn LaunchQuestSeason ()
  (if (< (Variables|Default|GetTechTier) 1)
    (Variables|Default|SetLastNotification "Community technology required for a quest season")
    (elif (< (Variables|Default|GetCash) 2500.0)
      (Variables|Default|SetLastNotification "Quest season needs $2,500")
      (else
        (Variables|Default|SetCash (- (Variables|Default|GetCash) 2500.0))
        (Variables|Default|SetQuestTemplates (+ (Variables|Default|GetQuestTemplates) 1))
        (Variables|Default|SetQuestCompletions (+ (Variables|Default|GetQuestCompletions) 40))
        (Variables|Default|SetPartyCount (+ (Variables|Default|GetPartyCount) 3))
        (Variables|Default|SetFriendLinks (+ (Variables|Default|GetFriendLinks) 18))
        (Variables|Default|SetSubscribers (+ (Variables|Default|GetSubscribers) 120))
        (Variables|Default|SetHappiness (+ (Variables|Default|GetHappiness) 2.0))
        (Variables|Default|SetLastNotification "Quest season launched: parties share objectives and loot")))))
''',
    )
    write_function(
        strategy,
        "RunCombatTournament",
        r'''
(fn RunCombatTournament ()
  (if (< (Variables|Default|GetTechTier) 4)
    (Variables|Default|SetLastNotification "Tactical combat locked: complete technology tier 4")
    (else
      (Variables|Default|SetCombatEncounters (+ (Variables|Default|GetCombatEncounters) 32))
      (Variables|Default|SetPvPDuels (+ (Variables|Default|GetPvPDuels) 12))
      (Variables|Default|SetHype (+ (Variables|Default|GetHype) 8))
      (Variables|Default|SetHappiness (+ (Variables|Default|GetHappiness) 1.0))
      (Variables|Default|SetLastNotification "Tactical tournament active: tanks, healers, ranged roles and PvP duels"))))
''',
    )
    write_function(
        strategy,
        "LaunchDungeonExpedition",
        r'''
(fn LaunchDungeonExpedition ()
  (if (< (Variables|Default|GetTechTier) 5)
    (Variables|Default|SetLastNotification "Dungeons locked: complete technology tier 5")
    (else
      (Variables|Default|SetDungeonRuns (+ (Variables|Default|GetDungeonRuns) 6))
      (Variables|Default|SetBossKills (+ (Variables|Default|GetBossKills) 1))
      (Variables|Default|SetDungeonRooms (+ (Variables|Default|GetDungeonRooms) 2))
      (Variables|Default|SetServiceIncome (+ (Variables|Default|GetServiceIncome) (* (Variables|Default|GetDungeonEntryPrice) 24.0)))
      (Variables|Default|SetCash (+ (Variables|Default|GetCash) (* (Variables|Default|GetDungeonEntryPrice) 24.0)))
      (Variables|Default|SetHype (+ (Variables|Default|GetHype) 5))
      (Variables|Default|SetLastNotification "Dungeon expedition complete: keys, chest loot and multi-phase boss resolved"))))
''',
    )
    write_function(
        strategy,
        "RunLiveOperations",
        r'''
(fn RunLiveOperations ()
  (if (< (Variables|Default|GetTechTier) 6)
    (Variables|Default|SetLastNotification "Live operations locked: complete technology tier 6")
    (elif (Variables|Default|GetServersOnline)
      (Variables|Default|SetServersOnline false)
      (Variables|Default|SetMaintenanceScheduled true)
      (if (> (Variables|Default|GetCrashBugs) 0) (Variables|Default|SetCrashBugs (- (Variables|Default|GetCrashBugs) 1)))
      (if (> (Variables|Default|GetMajorBugs) 0) (Variables|Default|SetMajorBugs (- (Variables|Default|GetMajorBugs) 1)))
      (if (> (Variables|Default|GetMinorBugs) 1) (Variables|Default|SetMinorBugs (- (Variables|Default|GetMinorBugs) 2)))
      (Variables|Default|SetModerationCases (+ (Variables|Default|GetModerationCases) 3))
      (if (> (Variables|Default|GetSuspectedCheaters) 0) (Variables|Default|SetSuspectedCheaters (- (Variables|Default|GetSuspectedCheaters) 1)))
      (Variables|Default|SetLastNotification "Maintenance started: players offline, debugging and moderation accelerated")
      (else
        (Variables|Default|SetServersOnline true)
        (Variables|Default|SetMaintenanceScheduled false)
        (Variables|Default|SetReleasesPublished (+ (Variables|Default|GetReleasesPublished) 1))
        (Variables|Default|SetVersionMajor (+ (Variables|Default|GetVersionMajor) 1))
        (Variables|Default|SetHype (+ (Variables|Default|GetHype) 20))
        (Variables|Default|SetSubscribers (+ (Variables|Default|GetSubscribers) 450))
        (Variables|Default|SetLastNotification "Named major update released; servers online and release history updated")))))
''',
    )

    process, created = ensure_function(strategy, "ProcessFullOperations")
    if created:
        tool(
            f"{BT}.add_function_param",
            {
                "graph": process,
                "param_name": "DeltaSeconds",
                "param_type": "float",
                "input_param": True,
            },
        )
    tool(
        f"{BT}.write_graph_dsl",
        {
            "graph": process,
            "code": r'''
(fn ProcessFullOperations (DeltaSeconds)
  (Variables|Default|SetOperationsClock (+ (Variables|Default|GetOperationsClock) DeltaSeconds))
  (if (>= (Variables|Default|GetOperationsClock) 6.0)
    (Variables|Default|SetOperationsClock 0.0)
    (if (Variables|Default|GetServersOnline)
      (Variables|Default|SetServiceUses (+ (Variables|Default|GetServiceUses) (* (Variables|Default|GetBuildCount) 3)))
      (Variables|Default|SetQuestCompletions (+ (Variables|Default|GetQuestCompletions) (+ 1 (Variables|Default|GetBuildCount))))
      (Variables|Default|SetPartyCount (+ (Variables|Default|GetPartyCount) 1))
      (Variables|Default|SetFriendLinks (+ (Variables|Default|GetFriendLinks) 4)))
    (if (>= (Variables|Default|GetTechTier) 3)
      (Variables|Default|SetRouteUses (+ (Variables|Default|GetRouteUses) 2))
      (Variables|Default|SetRouteIncome (+ (Variables|Default|GetRouteIncome) 18.0)))
    (if (>= (Variables|Default|GetTechTier) 4)
      (Variables|Default|SetCombatEncounters (+ (Variables|Default|GetCombatEncounters) 3))
      (Variables|Default|SetPvPDuels (+ (Variables|Default|GetPvPDuels) 1)))
    (if (>= (Variables|Default|GetTechTier) 5)
      (Variables|Default|SetDungeonRuns (+ (Variables|Default|GetDungeonRuns) 1)))
    (if (> (Variables|Default|GetServerCapacity) 0)
      (Variables|Default|SetCongestionPercent (* (/ (Variables|Default|GetNetworkLoad) (Variables|Default|GetServerCapacity)) 100.0)))
    (if (and (== (Variables|Default|GetCampaignStage) 0) (and (>= (Variables|Default|GetTechTier) 1) (>= (Variables|Default|GetBuildCount) 1)))
      (Variables|Default|SetCampaignStage 1)
      (Variables|Default|SetCampaignStatus "GROWTH: reach 1,000 subscribers and four services"))
    (if (and (== (Variables|Default|GetCampaignStage) 1) (and (>= (Variables|Default|GetSubscribers) 1000) (>= (Variables|Default|GetBuildCount) 4)))
      (Variables|Default|SetCampaignStage 2)
      (Variables|Default|SetCampaignStatus "ADVENTURE: unlock combat and complete a dungeon run"))
    (if (and (== (Variables|Default|GetCampaignStage) 2) (and (>= (Variables|Default|GetTechTier) 5) (> (Variables|Default|GetDungeonRuns) 0)))
      (Variables|Default|SetCampaignStage 3)
      (Variables|Default|SetCampaignStatus "LIVE SERVICE: publish a major update after maintenance"))
    (if (and (== (Variables|Default|GetCampaignStage) 3) (> (Variables|Default|GetReleasesPublished) 0))
      (Variables|Default|SetCampaignStage 4)
      (Variables|Default|SetCampaignWon true)
      (Variables|Default|SetAwardsWon (+ (Variables|Default|GetAwardsWon) 1))
      (Variables|Default|SetCampaignStatus "REALM LEGEND: campaign complete; sandbox continues"))
    (if (or (< (Variables|Default|GetCash) -25000.0) (< (Variables|Default|GetHappiness) 10.0))
      (Variables|Default|SetCampaignFailed true)
      (Variables|Default|SetCampaignStatus "CRISIS: recover treasury or happiness to continue"))
    (Variables|Default|SetCompetitorScore (+ 48.0 (* (Variables|Default|GetRating) 3.0)))))
''',
        },
    )

    tool(f"{BT}.compile_blueprint", {"blueprint": strategy, "warnings_as_errors": True})
    tool(f"{AT}.save_assets", {"asset_paths": []})
    return {
        "strategy": strategy["refPath"],
        "systems": [
            "services",
            "network",
            "quests/social",
            "combat/PvP",
            "dungeons",
            "live operations",
            "campaign",
            "settings state",
        ],
        "status": "full operations state, actions and campaign progression compiled",
    }
