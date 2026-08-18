import json


def tool(name, args):
    return execute_tool(name, json.dumps(args))


OBJECT = "editor_toolset.toolsets.object.ObjectTools"


def set_known(instance, desired):
    schema = json.loads(tool(f"{OBJECT}.list_properties", {"instance": instance})["returnValue"])
    names = {name.lower(): name for name in schema.keys()}
    values = {
        names[name.lower()]: value
        for name, value in desired.items()
        if name.lower() in names
    }
    if values:
        tool(f"{OBJECT}.set_properties", {"instance": instance, "values": json.dumps(values)})


def run():
    widget_bp = {"refPath": "/Game/UI/WBP_RFOperatorHUD.WBP_RFOperatorHUD"}
    tree = tool("UMGToolSet.UMGToolSet.GetWidgets", {"widgetBlueprint": widget_bp})[
        "returnValue"
    ]
    by_name = {item["widgetName"]: item for item in tree["widgets"]}
    if "OperationsBar" in by_name:
        return {"status": "operations bar already exists"}
    root = by_name["RootStack"]["widget"]
    bar = tool(
        "UMGToolSet.UMGToolSet.AddWidget",
        {
            "widgetBlueprint": widget_bp,
            "widgetClass": {"refPath": "/Script/UMG.HorizontalBox"},
            "widgetDisplayName": "OperationsBar",
            "parentWidget": root,
            "childIndex": -1,
        },
    )["returnValue"]
    set_known(bar["widget"], {})
    if bar["slot"].get("refPath"):
        set_known(
            bar["slot"],
            {
                "padding": {"left": 0.0, "top": 6.0, "right": 0.0, "bottom": 0.0},
                "horizontalAlignment": "HAlign_Left",
            },
        )

    specs = [
        ("BtnServices", "SERVICES"),
        ("BtnNetwork", "NETWORK"),
        ("BtnQuests", "QUESTS"),
        ("BtnCombat", "COMBAT"),
        ("BtnDungeon", "DUNGEON"),
        ("BtnLiveOps", "LIVE OPS"),
    ]
    for button_name, label in specs:
        button = tool(
            "UMGToolSet.UMGToolSet.AddWidget",
            {
                "widgetBlueprint": widget_bp,
                "widgetClass": {"refPath": "/Script/UMG.Button"},
                "widgetDisplayName": button_name,
                "parentWidget": bar["widget"],
                "childIndex": -1,
            },
        )["returnValue"]
        set_known(button["widget"], {"toolTipText": label, "isFocusable": True})
        if button["slot"].get("refPath"):
            set_known(
                button["slot"],
                {
                    "padding": {"left": 0.0, "top": 0.0, "right": 8.0, "bottom": 0.0},
                    "verticalAlignment": "VAlign_Center",
                },
            )
        tool(
            "UMGToolSet.UMGToolSet.ToggleWidgetAsVariable",
            {
                "widgetBlueprint": widget_bp,
                "widget": button["widget"],
                "bIsVariable": True,
            },
        )
        text_widget = tool(
            "UMGToolSet.UMGToolSet.AddWidget",
            {
                "widgetBlueprint": widget_bp,
                "widgetClass": {"refPath": "/Script/UMG.TextBlock"},
                "widgetDisplayName": button_name + "Label",
                "parentWidget": button["widget"],
                "childIndex": -1,
            },
        )["returnValue"]
        set_known(
            text_widget["widget"],
            {
                "text": label,
                "colorAndOpacity": {
                    "specifiedColor": {"r": 0.02, "g": 0.06, "b": 0.08, "a": 1.0}
                },
            },
        )
        if text_widget["slot"].get("refPath"):
            set_known(
                text_widget["slot"],
                {
                    "padding": {"left": 10.0, "top": 6.0, "right": 10.0, "bottom": 6.0},
                    "horizontalAlignment": "HAlign_Center",
                    "verticalAlignment": "VAlign_Center",
                },
            )

    tool("UMGToolSet.UMGToolSet.CompileWidgetBlueprint", {"widgetBlueprint": widget_bp})
    for button_name, _ in specs:
        tool(
            "UMGToolSet.UMGToolSet.BindToEventProperty",
            {
                "widgetBlueprint": widget_bp,
                "eventName": "OnClicked",
                "propertyName": button_name,
                "propertyClass": {"refPath": "/Script/UMG.Button"},
            },
        )
    tool("UMGToolSet.UMGToolSet.CompileWidgetBlueprint", {"widgetBlueprint": widget_bp})
    tool("editor_toolset.toolsets.asset.AssetTools.save_assets", {"asset_paths": []})
    return {"status": "six-button operations bar created", "buttons": [x[0] for x in specs]}
