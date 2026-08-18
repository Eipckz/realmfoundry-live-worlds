import json


def tool(name, args):
    return execute_tool(name, json.dumps(args))


OBJECT = "editor_toolset.toolsets.object.ObjectTools"


def set_known_properties(instance, desired):
    schema = json.loads(tool(f"{OBJECT}.list_properties", {"instance": instance})["returnValue"])
    canonical = {name.lower(): name for name in schema.keys()}
    values = {}
    for name, value in desired.items():
        if name.lower() in canonical:
            values[canonical[name.lower()]] = value
    if values:
        tool(f"{OBJECT}.set_properties", {"instance": instance, "values": json.dumps(values)})


def run():
    widget_bp = {"refPath": "/Game/UI/WBP_RFOperatorHUD.WBP_RFOperatorHUD"}
    tree = tool("UMGToolSet.UMGToolSet.GetWidgets", {"widgetBlueprint": widget_bp})["returnValue"]
    by_name = {item["widgetName"]: item for item in tree["widgets"]}
    root = by_name["RootStack"]["widget"]

    if "ActionBar" in by_name:
        return {"status": "action bar already exists", "buttons": []}

    bar_info = tool("UMGToolSet.UMGToolSet.AddWidget", {
        "widgetBlueprint": widget_bp,
        "widgetClass": {"refPath": "/Script/UMG.HorizontalBox"},
        "widgetDisplayName": "ActionBar",
        "parentWidget": root,
        "childIndex": -1,
    })["returnValue"]
    set_known_properties(bar_info["widget"], {})
    if bar_info["slot"].get("refPath"):
        set_known_properties(bar_info["slot"], {
            "padding": {"left": 0.0, "top": 10.0, "right": 0.0, "bottom": 0.0},
            "horizontalAlignment": "HAlign_Left",
        })

    specs = [
        ("BtnInspect", "INSPECT [0]"),
        ("BtnInn", "INN [1]"),
        ("BtnSmithy", "SMITHY [2]"),
        ("BtnResearch", "RESEARCH [T]"),
        ("BtnFollow", "FOLLOW [F]"),
        ("BtnRelease", "RELEASE [R]"),
    ]
    created = []
    for button_name, label in specs:
        button_info = tool("UMGToolSet.UMGToolSet.AddWidget", {
            "widgetBlueprint": widget_bp,
            "widgetClass": {"refPath": "/Script/UMG.Button"},
            "widgetDisplayName": button_name,
            "parentWidget": bar_info["widget"],
            "childIndex": -1,
        })["returnValue"]
        set_known_properties(button_info["widget"], {
            "toolTipText": label,
            "isFocusable": True,
        })
        if button_info["slot"].get("refPath"):
            set_known_properties(button_info["slot"], {
                "padding": {"left": 0.0, "top": 0.0, "right": 8.0, "bottom": 0.0},
                "verticalAlignment": "VAlign_Center",
            })
        tool("UMGToolSet.UMGToolSet.ToggleWidgetAsVariable", {
            "widgetBlueprint": widget_bp,
            "widget": button_info["widget"],
            "bIsVariable": True,
        })

        text_info = tool("UMGToolSet.UMGToolSet.AddWidget", {
            "widgetBlueprint": widget_bp,
            "widgetClass": {"refPath": "/Script/UMG.TextBlock"},
            "widgetDisplayName": button_name + "Label",
            "parentWidget": button_info["widget"],
            "childIndex": -1,
        })["returnValue"]
        set_known_properties(text_info["widget"], {
            "text": label,
            "colorAndOpacity": {"specifiedColor": {"r": 0.02, "g": 0.06, "b": 0.08, "a": 1.0}},
        })
        if text_info["slot"].get("refPath"):
            set_known_properties(text_info["slot"], {
                "padding": {"left": 10.0, "top": 6.0, "right": 10.0, "bottom": 6.0},
                "horizontalAlignment": "HAlign_Center",
                "verticalAlignment": "VAlign_Center",
            })
        created.append(button_name)

    tool("UMGToolSet.UMGToolSet.CompileWidgetBlueprint", {"widgetBlueprint": widget_bp})
    for button_name, _ in specs:
        tool("UMGToolSet.UMGToolSet.BindToEventProperty", {
            "widgetBlueprint": widget_bp,
            "eventName": "OnClicked",
            "propertyName": button_name,
            "propertyClass": {"refPath": "/Script/UMG.Button"},
        })
    tool("UMGToolSet.UMGToolSet.CompileWidgetBlueprint", {"widgetBlueprint": widget_bp})
    tool("editor_toolset.toolsets.asset.AssetTools.save_assets", {"asset_paths": []})
    return {"status": "mouse action bar created and click events bound", "buttons": created}
