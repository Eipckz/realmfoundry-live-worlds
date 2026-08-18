import json


def tool(name, args):
    return execute_tool(name, json.dumps(args))


BLUEPRINT_TOOLS = "editor_toolset.toolsets.blueprint.BlueprintTools"
ACTOR_TOOLS = "editor_toolset.toolsets.actor.ActorTools"
OBJECT_TOOLS = "editor_toolset.toolsets.object.ObjectTools"
ASSET_TOOLS = "editor_toolset.toolsets.asset.AssetTools"


def bp(path):
    return {"refPath": path}


def list_variables(blueprint):
    return tool(f"{BLUEPRINT_TOOLS}.list_variables", {"blueprint": blueprint})["returnValue"]


def add_variable(blueprint, name, type_name):
    if name not in list_variables(blueprint):
        tool(f"{BLUEPRINT_TOOLS}.add_variable", {
            "blueprint": blueprint,
            "name": name,
            "type_name": type_name,
        })


def add_object_variable(blueprint, name, object_class):
    if name not in list_variables(blueprint):
        tool(f"{BLUEPRINT_TOOLS}.add_object_variable", {
            "blueprint": blueprint,
            "name": name,
            "object_class": {"refPath": object_class},
        })


def set_defaults(blueprint, values):
    cdo = tool(f"{BLUEPRINT_TOOLS}.get_default_object", {"blueprint": blueprint})["returnValue"]
    schema = json.loads(tool(f"{OBJECT_TOOLS}.list_properties", {"instance": cdo})["returnValue"])
    names = {name.lower(): name for name in schema.keys()}
    resolved = {names[key.lower()]: value for key, value in values.items() if key.lower() in names}
    if resolved:
        tool(f"{OBJECT_TOOLS}.set_properties", {"instance": cdo, "values": json.dumps(resolved)})
    return cdo


def graph(blueprint, name):
    return tool(f"{BLUEPRINT_TOOLS}.get_graph", {
        "blueprint": blueprint,
        "graph_name": name,
    })["returnValue"]


def ensure_function(blueprint, name):
    graphs = tool(f"{BLUEPRINT_TOOLS}.list_graphs", {"blueprint": blueprint})["returnValue"]
    for item in graphs:
        if item["refPath"].endswith(":" + name):
            return item
    return tool(f"{BLUEPRINT_TOOLS}.add_function_graph", {
        "blueprint": blueprint,
        "graph_name": name,
    })["returnValue"]


def write_graph(target_graph, code):
    return tool(f"{BLUEPRINT_TOOLS}.write_graph_dsl", {"graph": target_graph, "code": code})


def compile_blueprint(blueprint):
    tool(f"{BLUEPRINT_TOOLS}.compile_blueprint", {
        "blueprint": blueprint,
        "warnings_as_errors": True,
    })


def configure_subscriber_camera():
    representative = bp("/Game/Characters/Subscribers/BP_RFSubscriberRepresentative.BP_RFSubscriberRepresentative")
    cdo = tool(f"{BLUEPRINT_TOOLS}.get_default_object", {"blueprint": representative})["returnValue"]
    components = tool(f"{ACTOR_TOOLS}.get_components", {"actor": cdo})["returnValue"]

    capsule = None
    boom = None
    camera = None
    extra_cameras = []
    extra_booms = []
    for component in components:
        path = component["refPath"]
        cls = tool(f"{OBJECT_TOOLS}.get_class", {"instance": component})["returnValue"]["refPath"]
        if cls == "/Script/Engine.CapsuleComponent":
            capsule = component
        elif cls == "/Script/Engine.SpringArmComponent":
            if ":SubscriberBoom_GEN_VARIABLE" in path:
                boom = component
            else:
                extra_booms.append(component)
        elif cls == "/Script/Engine.CameraComponent":
            if ":FollowCamera_GEN_VARIABLE" in path:
                camera = component
            else:
                extra_cameras.append(component)

    # Recovery-safe cleanup for partial/retried authoring runs: retain exactly one named pair.
    for component in extra_cameras + extra_booms:
        tool(f"{ACTOR_TOOLS}.remove_component", {"component": component})

    if boom is None:
        boom = tool(f"{ACTOR_TOOLS}.add_component", {
            "owner": representative,
            "component_type": {"refPath": "/Script/Engine.SpringArmComponent"},
            "name": "SubscriberBoom",
        })["returnValue"]
    if capsule:
        tool(f"{ACTOR_TOOLS}.set_parent_component", {"component": boom, "parent": capsule})
    tool(f"{OBJECT_TOOLS}.list_properties", {"instance": boom})
    tool(f"{OBJECT_TOOLS}.set_properties", {
        "instance": boom,
        "values": json.dumps({
            "targetArmLength": 420.0,
            "relativeLocation": {"x": 0.0, "y": 0.0, "z": 95.0},
            "relativeRotation": {"pitch": -12.0, "yaw": 0.0, "roll": 0.0},
            "bDoCollisionTest": False,
            "bUsePawnControlRotation": False,
            "bEnableCameraLag": True,
            "cameraLagSpeed": 5.0,
        }),
    })

    if camera is None:
        camera = tool(f"{ACTOR_TOOLS}.add_component", {
            "owner": representative,
            "component_type": {"refPath": "/Script/Engine.CameraComponent"},
            "name": "FollowCamera",
        })["returnValue"]
    tool(f"{ACTOR_TOOLS}.set_parent_component", {"component": camera, "parent": boom})
    tool(f"{OBJECT_TOOLS}.list_properties", {"instance": camera})
    tool(f"{OBJECT_TOOLS}.set_properties", {
        "instance": camera,
        "values": json.dumps({
            "fieldOfView": 72.0,
            "bAutoActivate": True,
        }),
    })
    compile_blueprint(representative)
    return {"boom": boom["refPath"], "camera": camera["refPath"]}


def build_strategy_core():
    strategy = bp("/Game/Core/Camera/BP_RFStrategyCameraPawn.BP_RFStrategyCameraPawn")
    for name, type_name in [
        ("TechTier", "int"),
        ("RequiredBuildTier", "int"),
        ("Researching", "bool"),
        ("ResearchProgress", "float"),
        ("ResearchDuration", "float"),
        ("ResearchCost", "int"),
        ("ActiveResearch", "string"),
        ("ActivePanel", "int"),
        ("OverlayMode", "int"),
        ("GameSpeed", "int"),
        ("FollowMode", "bool"),
        ("LastNotification", "string"),
        ("SelectedSubscriberName", "string"),
    ]:
        add_variable(strategy, name, type_name)
    add_object_variable(strategy, "SelectedSubscriber", "/Script/Engine.Character")
    compile_blueprint(strategy)
    set_defaults(strategy, {
        "techTier": 0,
        "requiredBuildTier": 0,
        "researching": False,
        "researchProgress": 0.0,
        "researchDuration": 4.0,
        "researchCost": 5000,
        "activeResearch": "Founding complete",
        "activePanel": 0,
        "overlayMode": 0,
        "gameSpeed": 1,
        "followMode": False,
        "lastNotification": "Realm operations ready",
        "selectedSubscriberName": "None",
    })

    research_next = ensure_function(strategy, "ResearchNext")
    write_graph(research_next, r'''
(fn ResearchNext ()
  (if (Variables|Default|GetResearching)
    (Development|PrintString "RESEARCH ALREADY IN PROGRESS" true true "(R=1.000000,G=0.650000,B=0.120000,A=1.000000)" 3.0)
    (elif (>= (Variables|Default|GetTechTier) 7)
      (Development|PrintString "ALL TECHNOLOGY TIERS UNLOCKED" true true "(R=0.200000,G=1.000000,B=0.650000,A=1.000000)" 3.0)
      (else
        (bind cost (+ 5000 (* (Variables|Default|GetTechTier) 3500)))
        (if (>= (Variables|Default|GetCash) cost)
          (Variables|Default|SetResearchCost cost)
          (Variables|Default|SetCash (- (Variables|Default|GetCash) cost))
          (Variables|Default|SetResearchProgress 0.0)
          (Variables|Default|SetResearchDuration (+ 4.0 (* (Variables|Default|GetTechTier) 2.0)))
          (Variables|Default|SetResearching true)
          (Variables|Default|SetActiveResearch "Researching next technology tier")
          (Variables|Default|SetLastNotification "Research started; progress advances in simulation time")
          (Development|PrintString "RESEARCH STARTED // TIER UNLOCKS ONLY AFTER COMPLETION" true true "(R=0.200000,G=0.720000,B=1.000000,A=1.000000)" 5.0)
          (else
            (Variables|Default|SetLastNotification "Research blocked: insufficient cash")
            (Development|PrintString "RESEARCH BLOCKED // INSUFFICIENT CASH" true true "(R=1.000000,G=0.240000,B=0.120000,A=1.000000)" 4.0)))))))
''')

    process_research = ensure_function(strategy, "ProcessResearch")
    # DeltaSeconds was added when this graph was first created. Function parameters are
    # not reported by list_variables, so repeated add attempts are intentionally avoided.
    write_graph(process_research, r'''
(fn ProcessResearch (DeltaSeconds)
  (if (Variables|Default|GetResearching)
    (Variables|Default|SetResearchProgress (+ (Variables|Default|GetResearchProgress) DeltaSeconds))
    (if (>= (Variables|Default|GetResearchProgress) (Variables|Default|GetResearchDuration))
      (Variables|Default|SetTechTier (+ (Variables|Default|GetTechTier) 1))
      (Variables|Default|SetResearching false)
      (Variables|Default|SetResearchProgress 0.0)
      (Variables|Default|SetActiveResearch "Technology tier completed")
      (Variables|Default|SetLastNotification "Research complete: new build and management capabilities unlocked")
      (Development|PrintString "RESEARCH COMPLETE // NEW CAPABILITIES UNLOCKED" true true "(R=0.160000,G=1.000000,B=0.620000,A=1.000000)" 6.0))))
''')

    select_subscriber = ensure_function(strategy, "SelectSubscriberUnderCursor")
    write_graph(select_subscriber, r'''
(fn SelectSubscriberUnderCursor ()
  (bind controller (Game|GetPlayerController 0))
  (bind hit (Game|Player|GetHitResultUnderCursorByChannel controller "TraceTypeQuery1" false))
  (bind (blocking initial hitTime distance location impactPoint normal impactNormal physMat hitActor hitComponent hitBone bone hitItem element face traceStart traceEnd) (Collision|BreakHitResult hit))
  (if blocking
    (bind character (Utilities|Casting|CastToCharacter :Object hitActor)
      (:then
        (Variables|Default|SetSelectedSubscriber character)
        (Variables|Default|SetSelectedSubscriberName (Utilities|GetDisplayName character))
        (Variables|Default|SetActivePanel 3)
        (Variables|Default|SetLastNotification "Subscriber selected; press F to follow")
        (Development|PrintString "SUBSCRIBER SELECTED // F FOLLOW // ESC RETURN" true true "(R=0.100000,G=0.850000,B=1.000000,A=1.000000)" 4.0))
      (:CastFailed
        (Variables|Default|SetLastNotification "No subscriber under cursor")))))
''')

    follow = ensure_function(strategy, "FollowSelectedSubscriber")
    write_graph(follow, r'''
(fn FollowSelectedSubscriber ()
  (bind controller (Game|GetPlayerController 0))
  (if (Utilities|IsValid (Variables|Default|GetSelectedSubscriber))
    (Game|Player|SetViewTargetWithBlend :self controller :NewViewTarget (Variables|Default|GetSelectedSubscriber) :BlendTime 0.65 :BlendFunc "VTBlend_EaseInOut" :BlendExp 2.0 :bLockOutgoing false)
    (Variables|Default|SetFollowMode true)
    (Variables|Default|SetLastNotification "Following selected subscriber in third person")
    (else
      (Variables|Default|SetLastNotification "Select a subscriber before entering follow mode")
      (Development|PrintString "NO SUBSCRIBER SELECTED // PRESS 0 THEN CLICK A CHARACTER" true true "(R=1.000000,G=0.400000,B=0.150000,A=1.000000)" 4.0))))
''')

    return_view = ensure_function(strategy, "ReturnToStrategyView")
    write_graph(return_view, r'''
(fn ReturnToStrategyView ()
  (bind controller (Game|GetPlayerController 0))
  (Game|Player|SetViewTargetWithBlend :self controller :NewViewTarget self :BlendTime 0.5 :BlendFunc "VTBlend_EaseInOut" :BlendExp 2.0 :bLockOutgoing false)
  (Variables|Default|SetFollowMode false)
  (Variables|Default|SetLastNotification "Returned to realm strategy view"))
''')

    place_graph = graph(strategy, "PlaceSelected")
    write_graph(place_graph, r'''
(fn PlaceSelected ()
  (bind controller (Game|GetPlayerController 0))
  (bind hit (Game|Player|GetHitResultUnderCursorByChannel controller "TraceTypeQuery1" false))
  (bind (blocking initial hitTime distance location impactPoint normal impactNormal physMat hitActor hitComponent hitBone bone hitItem element face traceStart traceEnd) (Collision|BreakHitResult hit))
  (bind snapped (Math|Vector|VectorSnappedtoGrid impactPoint 250.0))
  (bind spawnLocation (+ snapped (Math|Vector|MakeVector 0.0 0.0 35.0)))
  (if (<= (Variables|Default|GetSelectedBuildType) 0)
    (Development|PrintString "INSPECTION MODE // CLICK A SUBSCRIBER OR SELECT BUILD 1-6" true true "(R=0.180000,G=0.820000,B=1.000000,A=1.000000)" 3.0)
    (elif (< (Variables|Default|GetTechTier) (Variables|Default|GetRequiredBuildTier))
      (Variables|Default|SetLastNotification "Placement blocked by technology prerequisite")
      (Development|PrintString "TECHNOLOGY LOCKED // RESEARCH WITH T" true true "(R=1.000000,G=0.240000,B=0.120000,A=1.000000)" 4.0)
      (elif (< (Variables|Default|GetCash) 2500.0)
        (Variables|Default|SetLastNotification "Placement blocked by insufficient cash")
        (Development|PrintString "INSUFFICIENT CASH // BUILD COST $2,500" true true "(R=1.000000,G=0.240000,B=0.120000,A=1.000000)" 4.0)
        (else
          (if blocking
            (if (== (Variables|Default|GetSelectedBuildType) 1)
              (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_InnV2.BP_RFBuildable_InnV2_C" :SpawnTransform (Math|Transform|MakeTransform :Location spawnLocation) :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot")
              (CallFunction|ApplyBuildEconomy)
              (Variables|Default|SetLastNotification "Grand Inn constructed")
              (elif (== (Variables|Default|GetSelectedBuildType) 2)
                (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_SmithyV2.BP_RFBuildable_SmithyV2_C" :SpawnTransform (Math|Transform|MakeTransform :Location spawnLocation) :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot")
                (CallFunction|ApplyBuildEconomy)
                (Variables|Default|SetLastNotification "Blacksmith economy online")
                (elif (== (Variables|Default|GetSelectedBuildType) 3)
                  (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_UplinkV2.BP_RFBuildable_UplinkV2_C" :SpawnTransform (Math|Transform|MakeTransform :Location spawnLocation) :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot")
                  (CallFunction|ApplyBuildEconomy)
                  (Variables|Default|SetLastNotification "Arcane uplink capacity online")
                  (elif (== (Variables|Default|GetSelectedBuildType) 4)
                    (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_GuildHallV2.BP_RFBuildable_GuildHallV2_C" :SpawnTransform (Math|Transform|MakeTransform :Location spawnLocation) :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot")
                    (CallFunction|ApplyBuildEconomy)
                    (Variables|Default|SetLastNotification "Guild hall social systems online")
                    (elif (== (Variables|Default|GetSelectedBuildType) 5)
                      (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_DungeonGateV2.BP_RFBuildable_DungeonGateV2_C" :SpawnTransform (Math|Transform|MakeTransform :Location spawnLocation) :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot")
                      (CallFunction|ApplyBuildEconomy)
                      (Variables|Default|SetLastNotification "Dungeon gate and instancing online")
                      (elif (== (Variables|Default|GetSelectedBuildType) 6)
                        (Game|SpawnActorfromClass :Class "/Game/Core/BuildablesV2/BP_RFBuildable_TravelDockV2.BP_RFBuildable_TravelDockV2_C" :SpawnTransform (Math|Transform|MakeTransform :Location spawnLocation) :CollisionHandlingOverride "AlwaysSpawn" :TransformScaleMethod "MultiplyWithRoot")
                        (CallFunction|ApplyBuildEconomy)
                        (Variables|Default|SetLastNotification "Sky dock paid travel online")))))))))))))
''')

    event_graph = graph(strategy, "EventGraph")
    write_graph(event_graph, r'''
(event EventBeginPlay
  (bind controller (Game|GetPlayerController 0))
  (bind hud (UserInterface|CreateWidget "/Game/UI/WBP_RFOperatorHUD.WBP_RFOperatorHUD_C" controller))
  (UserInterface|Viewport|AddToViewport hud 10)
  (Input|SetInputModeGameAndUI controller hud "DoNotLock" false)
  (Development|PrintString "REALMFOUNDRY // LIVING MMO OPERATIONS // 0 INSPECT // 1-6 BUILD // T RESEARCH // F FOLLOW // ESC RETURN" true true "(R=0.170000,G=0.950000,B=0.750000,A=1.000000)" 12.0))

(event Collision|EventActorBeginOverlap (OtherActor))

(event EventTick (DeltaSeconds)
  (bind controller (Game|GetPlayerController 0))
  (CallFunction|ProcessResearch :DeltaSeconds DeltaSeconds)
  (CallFunction|ProcessEconomy :DeltaSeconds DeltaSeconds)
  (if (not (Variables|Default|GetFollowMode))
    (if (Game|Player|IsInputKeyDown controller "W")
      (Pawn|Input|AddMovementInput self (Math|Vector|MakeVector 0.707 0.707)))
    (if (Game|Player|IsInputKeyDown controller "S")
      (Pawn|Input|AddMovementInput self (Math|Vector|MakeVector 0.707 0.707) -1.0))
    (if (Game|Player|IsInputKeyDown controller "D")
      (Pawn|Input|AddMovementInput self (Math|Vector|MakeVector 0.707 -0.707)))
    (if (Game|Player|IsInputKeyDown controller "A")
      (Pawn|Input|AddMovementInput self (Math|Vector|MakeVector 0.707 -0.707) -1.0)))
  (if (Game|Player|WasInputKeyJustPressed controller "Zero")
    (Variables|Default|SetSelectedBuildType 0)
    (Variables|Default|SetRequiredBuildTier 0)
    (Variables|Default|SetLastNotification "Inspection mode: click a subscriber"))
  (if (Game|Player|WasInputKeyJustPressed controller "One")
    (Variables|Default|SetSelectedBuildType 1)
    (Variables|Default|SetRequiredBuildTier 0))
  (if (Game|Player|WasInputKeyJustPressed controller "Two")
    (Variables|Default|SetSelectedBuildType 2)
    (Variables|Default|SetRequiredBuildTier 2))
  (if (Game|Player|WasInputKeyJustPressed controller "Three")
    (Variables|Default|SetSelectedBuildType 3)
    (Variables|Default|SetRequiredBuildTier 3))
  (if (Game|Player|WasInputKeyJustPressed controller "Four")
    (Variables|Default|SetSelectedBuildType 4)
    (Variables|Default|SetRequiredBuildTier 1))
  (if (Game|Player|WasInputKeyJustPressed controller "Five")
    (Variables|Default|SetSelectedBuildType 5)
    (Variables|Default|SetRequiredBuildTier 5))
  (if (Game|Player|WasInputKeyJustPressed controller "Six")
    (Variables|Default|SetSelectedBuildType 6)
    (Variables|Default|SetRequiredBuildTier 3))
  (if (Game|Player|WasInputKeyJustPressed controller "LeftMouseButton")
    (if (== (Variables|Default|GetSelectedBuildType) 0)
      (CallFunction|SelectSubscriberUnderCursor)
      (else (CallFunction|PlaceSelected))))
  (if (Game|Player|WasInputKeyJustPressed controller "T")
    (CallFunction|ResearchNext))
  (if (Game|Player|WasInputKeyJustPressed controller "F")
    (CallFunction|FollowSelectedSubscriber))
  (if (Game|Player|WasInputKeyJustPressed controller "Escape")
    (CallFunction|ReturnToStrategyView))
  (if (Game|Player|WasInputKeyJustPressed controller "F5")
    (CallFunction|SaveRealm))
  (if (Game|Player|WasInputKeyJustPressed controller "F9")
    (CallFunction|LoadRealm))
  (if (Game|Player|WasInputKeyJustPressed controller "Hyphen")
    (if (> (Variables|Default|GetPriceSubscription) 1.0)
      (Variables|Default|SetPriceSubscription (- (Variables|Default|GetPriceSubscription) 0.5))
      (Variables|Default|SetLastNotification "Subscription price reduced")))
  (if (Game|Player|WasInputKeyJustPressed controller "Equals")
    (Variables|Default|SetPriceSubscription (+ (Variables|Default|GetPriceSubscription) 0.5))
    (Variables|Default|SetLastNotification "Subscription price increased"))
  (if (Game|Player|WasInputKeyJustPressed controller "Tab")
    (Variables|Default|SetActivePanel (+ (Variables|Default|GetActivePanel) 1))
    (if (> (Variables|Default|GetActivePanel) 7) (Variables|Default|SetActivePanel 0)))
  (if (Game|Player|WasInputKeyJustPressed controller "R")
    (CallFunction|PublishUpdate)))
''')

    compile_blueprint(strategy)
    return strategy["refPath"]


def expose_hud_widgets():
    widget_bp = bp("/Game/UI/WBP_RFOperatorHUD.WBP_RFOperatorHUD")
    tree = tool("UMGToolSet.UMGToolSet.GetWidgets", {"widgetBlueprint": widget_bp})["returnValue"]
    exposed = []
    for info in tree["widgets"]:
        name = info["widgetName"]
        if name in ["Status", "Objective", "Metrics", "Network", "Systems", "Controls", "Release"]:
            tool(f"{OBJECT_TOOLS}.list_properties", {"instance": info["widget"]})
            if info["slot"].get("refPath"):
                tool(f"{OBJECT_TOOLS}.list_properties", {"instance": info["slot"]})
            tool("UMGToolSet.UMGToolSet.ToggleWidgetAsVariable", {
                "widgetBlueprint": widget_bp,
                "widget": info["widget"],
                "bIsVariable": True,
            })
            exposed.append(name)
    tool("UMGToolSet.UMGToolSet.CompileWidgetBlueprint", {"widgetBlueprint": widget_bp})
    return exposed


def run():
    camera = configure_subscriber_camera()
    strategy = build_strategy_core()
    exposed = expose_hud_widgets()
    tool(f"{ASSET_TOOLS}.save_assets", {"asset_paths": []})
    return {
        "strategy": strategy,
        "subscriber_camera": camera,
        "hud_widgets_exposed": exposed,
        "status": "management core, enforced technology gates, inspection and third-person follow compiled",
    }
