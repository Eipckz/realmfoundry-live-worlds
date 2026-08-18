import json


def tool(name, args):
    return execute_tool(name, json.dumps(args))


def run():
    widget_bp = {"refPath": "/Game/UI/WBP_RFOperatorHUD.WBP_RFOperatorHUD"}
    tree = tool("UMGToolSet.UMGToolSet.GetWidgets", {"widgetBlueprint": widget_bp})["returnValue"]
    root = next(item["widget"] for item in tree["widgets"] if item["widgetName"] == "RootStack")
    transform = {
        "translation": {"x": 0.0, "y": 0.0},
        "scale": {"x": 0.65, "y": 0.65},
        "shear": {"x": 0.0, "y": 0.0},
        "angle": 0.0,
    }
    tool(
        "editor_toolset.toolsets.object.ObjectTools.set_properties",
        {
            "instance": root,
            "values": json.dumps(
                {
                    "renderTransform": transform,
                    "renderTransformPivot": {"x": 0.0, "y": 0.0},
                    "clipping": "Inherit",
                }
            ),
        },
    )
    tool("UMGToolSet.UMGToolSet.CompileWidgetBlueprint", {"widgetBlueprint": widget_bp})
    tool("editor_toolset.toolsets.asset.AssetTools.save_assets", {"asset_paths": []})
    return {"widget": widget_bp["refPath"], "root_scale": 0.65, "status": "HUD scaled for 1920x1080 standalone presentation"}
