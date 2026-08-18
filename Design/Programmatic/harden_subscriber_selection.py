import json


def tool(name, args):
    return execute_tool(name, json.dumps(args))


def run():
    actor_tools = "editor_toolset.toolsets.actor.ActorTools"
    blueprint_tools = "editor_toolset.toolsets.blueprint.BlueprintTools"
    object_tools = "editor_toolset.toolsets.object.ObjectTools"
    asset_tools = "editor_toolset.toolsets.asset.AssetTools"
    representative = {
        "refPath": "/Game/Characters/Subscribers/BP_RFSubscriberRepresentative.BP_RFSubscriberRepresentative"
    }
    cdo = tool(
        f"{blueprint_tools}.get_default_object", {"blueprint": representative}
    )["returnValue"]
    components = tool(f"{actor_tools}.get_components", {"actor": cdo})["returnValue"]
    capsule = None
    hitbox = None
    for component in components:
        component_class = tool(
            f"{object_tools}.get_class", {"instance": component}
        )["returnValue"]["refPath"]
        if component_class == "/Script/Engine.CapsuleComponent":
            capsule = component
        if (
            component_class == "/Script/Engine.SphereComponent"
            and ":SelectionHitbox_GEN_VARIABLE" in component["refPath"]
        ):
            hitbox = component

    if hitbox is None:
        hitbox = tool(
            f"{actor_tools}.add_component",
            {
                "owner": representative,
                "component_type": {"refPath": "/Script/Engine.SphereComponent"},
                "name": "SelectionHitbox",
            },
        )["returnValue"]
    if capsule:
        tool(
            f"{actor_tools}.set_parent_component",
            {"component": hitbox, "parent": capsule},
        )

    # Property discovery is deliberate; it catches engine-version naming drift.
    schema_text = tool(f"{object_tools}.list_properties", {"instance": hitbox})[
        "returnValue"
    ]
    schema = json.loads(schema_text)
    canonical = {name.lower(): name for name in schema.keys()}
    current = json.loads(
        tool(
            f"{object_tools}.get_properties",
            {"instance": hitbox, "properties": ["bodyInstance"]},
        )["returnValue"]
    )
    body = current["bodyInstance"]
    body["collisionProfileName"] = "Custom"
    body["collisionEnabled"] = "QueryOnly"
    for response in body["collisionResponses"]["responseArray"]:
        response["response"] = (
            "ECR_Block" if response["channel"] == "Visibility" else "ECR_Ignore"
        )
    requested = {
        "sphereRadius": 105.0,
        "bodyInstance": body,
        "bHiddenInGame": True,
        "bVisible": True,
    }
    values = {
        canonical[name.lower()]: value
        for name, value in requested.items()
        if name.lower() in canonical
    }
    tool(
        f"{object_tools}.set_properties",
        {"instance": hitbox, "values": json.dumps(values)},
    )
    tool(
        f"{blueprint_tools}.compile_blueprint",
        {"blueprint": representative, "warnings_as_errors": True},
    )
    tool(f"{asset_tools}.save_assets", {"asset_paths": []})
    return {
        "selection_hitbox": hitbox["refPath"],
        "configured_properties": values,
        "status": "selection hitbox added and representative compiled",
    }
