import json


def list_properties(instance):
    return execute_tool(
        "editor_toolset.toolsets.object.ObjectTools.list_properties",
        json.dumps({"instance": instance}))


def get_properties(instance, properties):
    return execute_tool(
        "editor_toolset.toolsets.object.ObjectTools.get_properties",
        json.dumps({"instance": instance, "properties": properties}))


def set_properties(instance, values):
    return execute_tool(
        "editor_toolset.toolsets.object.ObjectTools.set_properties",
        json.dumps({"instance": instance, "values": values}))


def run():
    base = "/Game/UI/WBP_RFOperatorHUD.WBP_RFOperatorHUD:WidgetTree."
    rows = {
        "Title": ("REALMFOUNDRY // LIVE WORLDS — MMO TYCOON", "{\"text\":\"REALMFOUNDRY // LIVE WORLDS — MMO TYCOON\",\"colorAndOpacity\":{\"specifiedColor\":{\"r\":0.10,\"g\":0.95,\"b\":0.78,\"a\":1.0},\"colorUseRule\":\"UseColor_Specified\"}}"),
        "Status": ("DAY 1  |  CASH $28,000  |  SUBSCRIBERS 250  |  HYPE 8", "{\"text\":\"DAY 1  |  CASH $28,000  |  SUBSCRIBERS 250  |  HYPE 8\",\"colorAndOpacity\":{\"specifiedColor\":{\"r\":1.0,\"g\":0.70,\"b\":0.16,\"a\":1.0},\"colorUseRule\":\"UseColor_Specified\"}}"),
        "Objective": ("BUILD THE NEXT MAJOR UPDATE: PLACE 6 SERVICES, THEN PRESS R TO RELEASE", "{\"text\":\"BUILD THE NEXT MAJOR UPDATE: PLACE 6 SERVICES, THEN PRESS R TO RELEASE\",\"colorAndOpacity\":{\"specifiedColor\":{\"r\":0.32,\"g\":1.0,\"b\":0.48,\"a\":1.0},\"colorUseRule\":\"UseColor_Specified\"}}"),
        "Metrics": ("[1] GRAND INN     [2] BLACKSMITH     [3] ARCANE UPLINK", "{\"text\":\"[1] GRAND INN     [2] BLACKSMITH     [3] ARCANE UPLINK\",\"colorAndOpacity\":{\"specifiedColor\":{\"r\":0.86,\"g\":0.94,\"b\":1.0,\"a\":1.0},\"colorUseRule\":\"UseColor_Specified\"}}"),
        "Network": ("[4] GUILD HALL     [5] DUNGEON GATE     [6] SKY DOCK", "{\"text\":\"[4] GUILD HALL     [5] DUNGEON GATE     [6] SKY DOCK\",\"colorAndOpacity\":{\"specifiedColor\":{\"r\":0.32,\"g\":0.78,\"b\":1.0,\"a\":1.0},\"colorUseRule\":\"UseColor_Specified\"}}"),
        "Systems": ("$2,500 EACH  |  +400 SUBSCRIBERS  |  +7 HYPE  |  +1 CHANGELOG", "{\"text\":\"$2,500 EACH  |  +400 SUBSCRIBERS  |  +7 HYPE  |  +1 CHANGELOG\",\"colorAndOpacity\":{\"specifiedColor\":{\"r\":0.82,\"g\":0.62,\"b\":1.0,\"a\":1.0},\"colorUseRule\":\"UseColor_Specified\"}}"),
        "Controls": ("WASD PAN  |  1–6 SELECT  |  LEFT CLICK PLACE  |  R RELEASE", "{\"text\":\"WASD PAN  |  1–6 SELECT  |  LEFT CLICK PLACE  |  R RELEASE\",\"colorAndOpacity\":{\"specifiedColor\":{\"r\":0.78,\"g\":0.84,\"b\":0.90,\"a\":1.0},\"colorUseRule\":\"UseColor_Specified\"}}"),
        "Release": ("MAJOR RELEASE REQUIRES 6 BUILDS  |  REWARD +$15K / +4K SUBSCRIBERS", "{\"text\":\"MAJOR RELEASE REQUIRES 6 BUILDS  |  REWARD +$15K / +4K SUBSCRIBERS\",\"colorAndOpacity\":{\"specifiedColor\":{\"r\":1.0,\"g\":0.34,\"b\":0.54,\"a\":1.0},\"colorUseRule\":\"UseColor_Specified\"}}"),
    }
    inspected = []
    changed = []
    for name, payload in rows.items():
        ref = {"refPath": base + name}
        list_properties(ref)
        get_properties(ref, ["text", "colorAndOpacity", "shadowOffset", "shadowColorAndOpacity", "visibility"])
        inspected.append(name)
        result = set_properties(ref, payload[1])
        changed.append({"widget": name, "result": result})
    return {"inspected": inspected, "changed": changed}
