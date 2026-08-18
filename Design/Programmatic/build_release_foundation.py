import json


def tool(name, args):
    return execute_tool(name, json.dumps(args))


def asset_exists(path):
    return tool(
        "editor_toolset.toolsets.asset.AssetTools.exists",
        {"path": path})["returnValue"]


def create_blueprint(folder, name, parent_class):
    path = f"{folder}/{name}.{name}"
    if asset_exists(path):
        return {"refPath": path}
    return tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.create",
        {
            "folder_path": folder,
            "asset_name": name,
            "asset_type": {"refPath": parent_class},
        })["returnValue"]


def list_variables(blueprint):
    return tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.list_variables",
        {"blueprint": blueprint})["returnValue"]


def add_variable(blueprint, name, type_name, container_type=None):
    if name in list_variables(blueprint):
        return False
    args = {"blueprint": blueprint, "name": name, "type_name": type_name}
    if container_type:
        args["container_type"] = container_type
    tool("editor_toolset.toolsets.blueprint.BlueprintTools.add_variable", args)
    return True


def add_object_variable(blueprint, name, object_class, container_type=None):
    if name in list_variables(blueprint):
        return False
    args = {
        "blueprint": blueprint,
        "name": name,
        "object_class": {"refPath": object_class},
    }
    if container_type:
        args["container_type"] = container_type
    tool("editor_toolset.toolsets.blueprint.BlueprintTools.add_object_variable", args)
    return True


def set_defaults(blueprint, values):
    cdo = tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.get_default_object",
        {"blueprint": blueprint})["returnValue"]
    return tool(
        "editor_toolset.toolsets.object.ObjectTools.set_properties",
        {"instance": cdo, "values": json.dumps(values)})["returnValue"]


def compile_blueprint(blueprint):
    tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.compile_blueprint",
        {"blueprint": blueprint, "warnings_as_errors": True})


def get_graph(blueprint, graph_name):
    return tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.get_graph",
        {"blueprint": blueprint, "graph_name": graph_name})["returnValue"]


def write_graph(graph, code):
    return tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.write_graph_dsl",
        {"graph": graph, "code": code})


def create_data_asset(folder, name, asset_type):
    path = f"{folder}/{name}.{name}"
    if asset_exists(path):
        return {"refPath": path}
    return tool(
        "editor_toolset.toolsets.data_asset.DataAssetTools.create",
        {
            "folder_path": folder,
            "asset_name": name,
            "asset_type": {"refPath": asset_type},
        })["returnValue"]


def set_asset_values(asset, desired):
    schema_text = tool(
        "editor_toolset.toolsets.object.ObjectTools.list_properties",
        {"instance": asset})["returnValue"]
    schema = json.loads(schema_text)
    canonical = {key.lower(): key for key in schema.keys()}
    values = {}
    for requested, value in desired.items():
        actual = canonical.get(requested.lower())
        if actual:
            values[actual] = value
    if values:
        return tool(
            "editor_toolset.toolsets.object.ObjectTools.set_properties",
            {"instance": asset, "values": json.dumps(values)})["returnValue"]
    return False


def build_technology_data():
    tech_bp = create_blueprint(
        "/Game/Data/Technology", "BP_RFTechnologyDefinition",
        "/Script/Engine.PrimaryDataAsset")
    tech_vars = [
        ("TechName", "string", None),
        ("Description", "string", None),
        ("Prerequisite", "string", None),
        ("Category", "string", None),
        ("Cost", "int", None),
        ("ResearchDays", "int", None),
        ("UnlockTier", "int", None),
        ("UnlockBuildType", "int", None),
        ("UnlockFeature", "string", None),
    ]
    for name, type_name, container in tech_vars:
        add_variable(tech_bp, name, type_name, container)
    compile_blueprint(tech_bp)

    tech_class = "/Game/Data/Technology/BP_RFTechnologyDefinition.BP_RFTechnologyDefinition_C"
    definitions = [
        ("DA_Tech_Founding", "Founding", "Launch the minimum viable realm.", "", "Founding", 0, 0, 0, 1, "Inn, quest hall, one class and basic monsters"),
        ("DA_Tech_Community", "Community", "Friends, parties and social analytics.", "Founding", "Social", 5000, 4, 1, 4, "Taverns, messaging, parties and subscriber browser"),
        ("DA_Tech_Commerce", "Commerce", "Unlock service pricing and item markets.", "Community", "Economy", 8500, 6, 2, 2, "Smithies, potion shops, markets and trinkets"),
        ("DA_Tech_Infrastructure", "Infrastructure", "Scale coverage, bandwidth and travel.", "Commerce", "Network", 12000, 8, 3, 3, "Uplinks, cables, congestion overlays and travel"),
        ("DA_Tech_Combat", "Tactical Combat", "Unlock roles, abilities, PvE and duels.", "Infrastructure", "Combat", 16000, 10, 4, 5, "Tank, healer, damage, status effects and PvP"),
        ("DA_Tech_Dungeons", "Instanced Dungeons", "Build editable dungeons and boss encounters.", "Tactical Combat", "Content", 22000, 12, 5, 6, "Rooms, locks, keys, chests, bosses and instances"),
        ("DA_Tech_LiveOps", "Live Operations", "Operate named releases and moderation.", "Instanced Dungeons", "Operations", 28000, 14, 6, 0, "Changelogs, maintenance, marketing, anti-cheat and GMs"),
        ("DA_Tech_Expansion", "Realm Expansion", "Unlock new regions and premium art packs.", "Live Operations", "Expansion", 36000, 18, 7, 0, "Regions, advanced world tools, themes and prestige"),
    ]
    assets = []
    for row in definitions:
        asset = create_data_asset("/Game/Data/Technology", row[0], tech_class)
        set_asset_values(asset, {
            "TechName": row[1],
            "Description": row[2],
            "Prerequisite": row[3],
            "Category": row[4],
            "Cost": row[5],
            "ResearchDays": row[6],
            "UnlockTier": row[7],
            "UnlockBuildType": row[8],
            "UnlockFeature": row[9],
        })
        assets.append(asset["refPath"])
    return {"blueprint": tech_bp["refPath"], "assets": assets}


def build_subscriber_assets():
    ai_bp = create_blueprint(
        "/Game/Characters/Subscribers", "BP_RFSubscriberAIController",
        "/Script/AIModule.AIController")
    for name, type_name, container in [
        ("ActivityState", "int", None),
        ("StateTimer", "float", None),
        ("StuckTimer", "float", None),
        ("LastKnownLocation", "Vector", None),
        ("DecisionHistory", "string", "ARRAY"),
    ]:
        add_variable(ai_bp, name, type_name, container)
    compile_blueprint(ai_bp)

    rep_bp = create_blueprint(
        "/Game/Characters/Subscribers", "BP_RFSubscriberRepresentative",
        "/Script/Engine.Character")
    subscriber_vars = [
        ("RealName", "string", None),
        ("CharacterName", "string", None),
        ("ClassName", "string", None),
        ("CurrentActivity", "string", None),
        ("StaffRole", "string", None),
        ("InventorySummary", "string", None),
        ("UnsubscribeReason", "string", None),
        ("Level", "int", None),
        ("Experience", "int", None),
        ("Gold", "int", None),
        ("PartyId", "int", None),
        ("FriendCount", "int", None),
        ("Wallet", "float", None),
        ("BankBalance", "float", None),
        ("LifetimeSpending", "float", None),
        ("Happiness", "float", None),
        ("Addiction", "float", None),
        ("Health", "float", None),
        ("Mana", "float", None),
        ("HomeLocation", "Vector", None),
        ("OrbitRadius", "float", None),
        ("PhaseOffset", "float", None),
        ("ActivityTimer", "float", None),
        ("LoggedIn", "bool", None),
        ("IsSelected", "bool", None),
        ("IsInCombat", "bool", None),
        ("IsCheating", "bool", None),
        ("HasQuest", "bool", None),
        ("IsStaff", "bool", None),
    ]
    for name, type_name, container in subscriber_vars:
        add_variable(rep_bp, name, type_name, container)
    for editable_name in ["RealName", "PhaseOffset", "StaffRole", "IsStaff"]:
        tool(
            "editor_toolset.toolsets.blueprint.BlueprintTools.set_variable_instance_editable",
            {
                "blueprint": rep_bp,
                "variable_name": editable_name,
                "instance_editable": True,
            })
    compile_blueprint(rep_bp)
    set_defaults(rep_bp, {
        "realName": "Morgan Rivers",
        "characterName": "Starwarden",
        "className": "Vanguard",
        "currentActivity": "Logging in",
        "staffRole": "Subscriber",
        "inventorySummary": "Iron Sword, Health Potion, Ancient Key",
        "level": 12,
        "experience": 680,
        "gold": 245,
        "wallet": 18.0,
        "bankBalance": 72.0,
        "lifetimeSpending": 34.0,
        "happiness": 78.0,
        "addiction": 42.0,
        "health": 100.0,
        "mana": 80.0,
        "orbitRadius": 260.0,
        "phaseOffset": 0.0,
        "activityTimer": 0.0,
        "loggedIn": True,
        "hasQuest": True,
        "isStaff": False,
    })

    rep_cdo = tool(
        "editor_toolset.toolsets.blueprint.BlueprintTools.get_default_object",
        {"blueprint": rep_bp})["returnValue"]
    rep_components = tool(
        "editor_toolset.toolsets.actor.ActorTools.get_components",
        {"actor": rep_cdo})["returnValue"]
    activity_label = None
    for component in rep_components:
        component_class = tool(
            "editor_toolset.toolsets.object.ObjectTools.get_class",
            {"instance": component})["returnValue"]["refPath"]
        if component_class == "/Script/Engine.TextRenderComponent":
            activity_label = component
            break
    if activity_label is None:
        activity_label = tool(
            "editor_toolset.toolsets.actor.ActorTools.add_component",
            {
                "owner": rep_bp,
                "component_type": {"refPath": "/Script/Engine.TextRenderComponent"},
                "name": "ActivityLabel",
            })["returnValue"]
    tool(
        "editor_toolset.toolsets.object.ObjectTools.set_properties",
        {
            "instance": activity_label,
            "values": json.dumps({
                "text": "Thinking...",
                "horizontalAlignment": "EHTA_Center",
                "verticalAlignment": "EVRTA_TextCenter",
                "textRenderColor": {"r": 0.15, "g": 0.95, "b": 1.0, "a": 1.0},
                "worldSize": 28.0,
                "relativeLocation": {"x": 0.0, "y": 0.0, "z": 145.0},
                "relativeRotation": {"pitch": 0.0, "yaw": 180.0, "roll": 0.0},
                "castShadow": False,
                "bGenerateOverlapEvents": False,
                "bCanEverAffectNavigation": False,
                "bVisible": True,
                "bHiddenInGame": False,
            }),
        })
    compile_blueprint(rep_bp)

    event_graph = get_graph(rep_bp, "EventGraph")
    code = r'''
(event EventBeginPlay
  (Variables|Default|SetHomeLocation (Transformation|GetActorLocation))
  (Variables|Default|SetOrbitRadius (Math|Random|RandomFloatInRange 180.0 520.0))
  (Variables|Default|SetPhaseOffset (Math|Random|RandomFloatInRange 0.0 360.0))
  (bind mesh (Variables|Character|GetMesh))
  (Components|Animation|PlayAnimation
    :self mesh
    :NewAnimToPlay "/Game/Characters/Subscriber/SK_RFSubscriber_Anim_A_RF_Walk.SK_RFSubscriber_Anim_A_RF_Walk"
    :bLooping true))

(event EventTick (DeltaSeconds)
  (bind t (+ (* (Utilities|Time|GetGameTimeinSeconds) 7.5) (Variables|Default|GetPhaseOffset)))
  (bind home (Variables|Default|GetHomeLocation))
  (bind radius (Variables|Default|GetOrbitRadius))
  (bind x (+ (.x home) (* (Math|Trig|Cos(Degrees) t) radius)))
  (bind y (+ (.y home) (* (Math|Trig|Sin(Degrees) t) radius)))
  (bind destination (Math|Vector|MakeVector x y (.z home)))
  (Transformation|SetActorLocation :self self :NewLocation destination :bSweep false :bTeleport true)
  (bind facing (Math|Vector|MakeVector (- (Math|Trig|Sin(Degrees) t)) (Math|Trig|Cos(Degrees) t) 0.0))
  (Transformation|SetActorRotation :self self :NewRotation (Math|Rotator|MakeRotfromX facing) :bTeleportPhysics true)
  (bind activityWave (Math|Trig|Sin(Degrees) (* t 0.35)))
  (if (Variables|Default|GetIsStaff)
    (if (> activityWave 0.25)
      (Variables|Default|SetCurrentActivity (Utilities|String|Append (Variables|Default|GetStaffRole) " resolving tickets"))
      (else
        (Variables|Default|SetCurrentActivity (Utilities|String|Append (Variables|Default|GetStaffRole) " at workstation"))))
    (else
      (if (> activityWave 0.75)
        (Variables|Default|SetCurrentActivity "Dungeon run")
        (elif (> activityWave 0.35)
          (Variables|Default|SetCurrentActivity "Fighting monsters")
          (elif (> activityWave -0.10)
            (Variables|Default|SetCurrentActivity "Questing")
            (elif (> activityWave -0.60)
              (Variables|Default|SetCurrentActivity "Shopping")
              (else
                (Variables|Default|SetCurrentActivity "Socializing"))))))))
  (Variables|Default|SetActivityTimer (+ (Variables|Default|GetActivityTimer) DeltaSeconds))
  (if (>= (Variables|Default|GetActivityTimer) 5.0)
    (Variables|Default|SetActivityTimer 0.0)
    (Variables|Default|SetExperience (+ (Variables|Default|GetExperience) 25))
    (Variables|Default|SetGold (+ (Variables|Default|GetGold) 5))
    (Variables|Default|SetLifetimeSpending (+ (Variables|Default|GetLifetimeSpending) 0.25))
    (if (>= (Variables|Default|GetExperience) 1000)
      (Variables|Default|SetLevel (+ (Variables|Default|GetLevel) 1))
      (Variables|Default|SetExperience 0)))
  (bind activityComponent (Actor|GetComponentByClass :self self :ComponentClass "/Script/Engine.TextRenderComponent"))
  (bind activityText (Utilities|Casting|CastToTextRenderComponent :Object activityComponent)
    (:then
      (Rendering|Components|TextRender|SetText
        :self activityText
        :Value (Utilities|Text|ToText(String) (Variables|Default|GetCurrentActivity))))
    (:CastFailed)))
'''
    write_graph(event_graph, code)
    compile_blueprint(rep_bp)

    spawner_bp = create_blueprint(
        "/Game/Characters/Subscribers", "BP_RFSubscriberSpawner",
        "/Script/Engine.Actor")
    for name, type_name, container in [
        ("LogicalSubscriberCount", "int", None),
        ("RepresentativeCap", "int", None),
        ("SpawnedRepresentatives", "int", None),
        ("PoolEnabled", "bool", None),
        ("StressMode", "bool", None),
    ]:
        add_variable(spawner_bp, name, type_name, container)
    compile_blueprint(spawner_bp)
    set_defaults(spawner_bp, {
        "logicalSubscriberCount": 10000,
        "representativeCap": 48,
        "spawnedRepresentatives": 0,
        "poolEnabled": True,
        "stressMode": False,
    })
    spawner_graph = get_graph(spawner_bp, "EventGraph")
    spawner_code = r'''
(event EventBeginPlay
  (for i (range 36)
    (bind angle (* i 10.0))
    (bind ring (+ 620.0 (* i 25.0)))
    (bind x (* (Math|Trig|Cos(Degrees) angle) ring))
    (bind y (* (Math|Trig|Sin(Degrees) angle) ring))
    (bind spawnLocation (Math|Vector|MakeVector x y 65.0))
    (bind spawned (Game|SpawnActorfromClass
      :Class "/Game/Characters/Subscribers/BP_RFSubscriberRepresentative.BP_RFSubscriberRepresentative_C"
      :SpawnTransform (Math|Transform|MakeTransform :Location spawnLocation)
      :CollisionHandlingOverride "AlwaysSpawn"
      :TransformScaleMethod "MultiplyWithRoot"))
    (Variables|Default|SetSpawnedRepresentatives (+ (Variables|Default|GetSpawnedRepresentatives) 1))
    (bind subscriber (Utilities|Casting|CastToBP_RFSubscriberRepresentative :Object spawned)
      (:then
        (Class|BPRFSubscriberRepresentative|SetRealName :self subscriber :RealName (Utilities|String|Append "Subscriber_" (Utilities|String|ToString(Integer) i)))
        (Class|BPRFSubscriberRepresentative|SetCharacterName :self subscriber :CharacterName (Utilities|String|Append "Adventurer_" (Utilities|String|ToString(Integer) i)))
        (Class|BPRFSubscriberRepresentative|SetLevel :self subscriber :Level (+ 1 (Math|Integer|%(Integer) i 40)))
        (Class|BPRFSubscriberRepresentative|SetExperience :self subscriber :Experience (* (Math|Integer|%(Integer) i 10) 90))
        (Class|BPRFSubscriberRepresentative|SetGold :self subscriber :Gold (+ 50 (* i 17)))
        (Class|BPRFSubscriberRepresentative|SetWallet :self subscriber :Wallet (+ 5.0 (* i 0.75)))
        (Class|BPRFSubscriberRepresentative|SetBankBalance :self subscriber :BankBalance (+ 20.0 (* i 2.5)))
        (Class|BPRFSubscriberRepresentative|SetHappiness :self subscriber :Happiness (+ 55.0 (Math|Integer|%(Integer) i 35)))
        (Class|BPRFSubscriberRepresentative|SetAddiction :self subscriber :Addiction (+ 20.0 (Math|Integer|%(Integer) i 60)))
        (Class|BPRFSubscriberRepresentative|SetPartyId :self subscriber :PartyId (Math|Integer|%(Integer) i 9))
        (Class|BPRFSubscriberRepresentative|SetFriendCount :self subscriber :FriendCount (Math|Integer|%(Integer) i 12))
        (Class|BPRFSubscriberRepresentative|SetIsCheating :self subscriber :IsCheating (== (Math|Integer|%(Integer) i 17) 0))
        (if (== (Math|Integer|%(Integer) i 4) 0)
          (Class|BPRFSubscriberRepresentative|SetClassName :self subscriber :ClassName "Vanguard")
          (elif (== (Math|Integer|%(Integer) i 4) 1)
            (Class|BPRFSubscriberRepresentative|SetClassName :self subscriber :ClassName "Arcanist")
            (elif (== (Math|Integer|%(Integer) i 4) 2)
              (Class|BPRFSubscriberRepresentative|SetClassName :self subscriber :ClassName "Warden")
              (else
                (Class|BPRFSubscriberRepresentative|SetClassName :self subscriber :ClassName "Bard")))))
        )
      (:CastFailed)))
  (Development|PrintString "LIVING WORLD ONLINE // 10,000 LOGICAL SUBSCRIBERS // 36 VISIBLE REPRESENTATIVES" true true "(R=0.120000,G=0.850000,B=1.000000,A=1.000000)" 8.0))
'''
    write_graph(spawner_graph, spawner_code)
    compile_blueprint(spawner_bp)

    return {
        "ai_controller": ai_bp["refPath"],
        "representative": rep_bp["refPath"],
        "spawner": spawner_bp["refPath"],
    }


def run():
    technology = build_technology_data()
    subscribers = build_subscriber_assets()
    tool(
        "editor_toolset.toolsets.asset.AssetTools.save_assets",
        {"asset_paths": []})
    return {
        "technology": technology,
        "subscribers": subscribers,
        "status": "release foundation assets created and compiled",
    }
