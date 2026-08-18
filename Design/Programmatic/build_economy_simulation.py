import json


def tool(name, args):
    return execute_tool(name, json.dumps(args))


BT = "editor_toolset.toolsets.blueprint.BlueprintTools"


def ensure_variable(blueprint, name, type_name):
    variables = tool(f"{BT}.list_variables", {"blueprint": blueprint})["returnValue"]
    if name not in variables:
        tool(f"{BT}.add_variable", {
            "blueprint": blueprint,
            "name": name,
            "type_name": type_name,
        })


def ensure_function(blueprint, name):
    graphs = tool(f"{BT}.list_graphs", {"blueprint": blueprint})["returnValue"]
    for graph in graphs:
        if graph["refPath"].endswith(":" + name):
            return graph, False
    graph = tool(f"{BT}.add_function_graph", {
        "blueprint": blueprint,
        "graph_name": name,
    })["returnValue"]
    return graph, True


def set_defaults(blueprint, desired):
    cdo = tool(f"{BT}.get_default_object", {"blueprint": blueprint})["returnValue"]
    schema = json.loads(tool(
        "editor_toolset.toolsets.object.ObjectTools.list_properties",
        {"instance": cdo})["returnValue"])
    names = {name.lower(): name for name in schema.keys()}
    values = {names[key.lower()]: value for key, value in desired.items() if key.lower() in names}
    tool(
        "editor_toolset.toolsets.object.ObjectTools.set_properties",
        {"instance": cdo, "values": json.dumps(values)})


def run():
    strategy = {"refPath": "/Game/Core/Camera/BP_RFStrategyCameraPawn.BP_RFStrategyCameraPawn"}
    for name, type_name in [
        ("SimulationClock", "float"),
        ("DayLength", "float"),
        ("RevenueToday", "float"),
        ("ExpensesToday", "float"),
        ("ProfitToday", "float"),
        ("ServerCapacity", "int"),
        ("NetworkLoad", "int"),
        ("Happiness", "float"),
        ("Rating", "float"),
        ("ChurnToday", "int"),
        ("ActivePlayers", "int"),
    ]:
        ensure_variable(strategy, name, type_name)
    tool(f"{BT}.compile_blueprint", {"blueprint": strategy, "warnings_as_errors": True})
    set_defaults(strategy, {
        "simulationClock": 0.0,
        "dayLength": 12.0,
        "revenueToday": 0.0,
        "expensesToday": 0.0,
        "profitToday": 0.0,
        "serverCapacity": 1000,
        "networkLoad": 200,
        "happiness": 72.0,
        "rating": 4.0,
        "churnToday": 0,
        "activePlayers": 186,
    })

    graph, created = ensure_function(strategy, "ProcessEconomy")
    if created:
        tool(f"{BT}.add_function_param", {
            "graph": graph,
            "param_name": "DeltaSeconds",
            "param_type": "float",
            "input_param": True,
        })
    code = r'''
(fn ProcessEconomy (DeltaSeconds)
  (Variables|Default|SetSimulationClock (+ (Variables|Default|GetSimulationClock) DeltaSeconds))
  (if (>= (Variables|Default|GetSimulationClock) (Variables|Default|GetDayLength))
    (Variables|Default|SetSimulationClock 0.0)
    (Variables|Default|SetCurrentDay (+ (Variables|Default|GetCurrentDay) 1))
    (Variables|Default|SetServerCapacity (+ 1000 (* (Variables|Default|GetBuildCount) 600)))
    (Variables|Default|SetNetworkLoad (Math|Float|Truncate (* (Variables|Default|GetSubscribers) 0.80)))
    (Variables|Default|SetActivePlayers (Math|Float|Truncate (* (Variables|Default|GetSubscribers) 0.72)))
    (bind revenue (+ (* (Variables|Default|GetSubscribers) (Variables|Default|GetPriceSubscription)) (* (Variables|Default|GetBuildCount) 350.0)))
    (bind expenses (+ (* (Variables|Default|GetSubscribers) 0.35) (* (Variables|Default|GetBuildCount) 240.0)))
    (Variables|Default|SetRevenueToday revenue)
    (Variables|Default|SetExpensesToday expenses)
    (Variables|Default|SetProfitToday (- revenue expenses))
    (Variables|Default|SetCash (+ (Variables|Default|GetCash) (- revenue expenses)))
    (if (> (Variables|Default|GetNetworkLoad) (Variables|Default|GetServerCapacity))
      (Variables|Default|SetChurnToday 15)
      (Variables|Default|SetSubscribers (- (Variables|Default|GetSubscribers) 15))
      (Variables|Default|SetHappiness (- (Variables|Default|GetHappiness) 3.0))
      (Variables|Default|SetLastNotification "Capacity exceeded: congestion caused 15 cancellations")
      (else
        (Variables|Default|SetChurnToday 0)
        (Variables|Default|SetSubscribers (+ (Variables|Default|GetSubscribers) (+ 10 (* (Variables|Default|GetBuildCount) 3))))
        (Variables|Default|SetHappiness (+ (Variables|Default|GetHappiness) 0.5))
        (Variables|Default|SetLastNotification "Daily close complete: subscribers and treasury updated")))
    (Variables|Default|SetRating (+ 3.0 (* (Variables|Default|GetHappiness) 0.015)))
    (Development|PrintString "DAILY CLOSE // REVENUE, EXPENSES, GROWTH, CAPACITY AND CHURN RESOLVED" true true "(R=0.180000,G=0.850000,B=1.000000,A=1.000000)" 4.0)))
'''
    tool(f"{BT}.write_graph_dsl", {"graph": graph, "code": code})
    tool(f"{BT}.compile_blueprint", {"blueprint": strategy, "warnings_as_errors": True})
    tool("editor_toolset.toolsets.asset.AssetTools.save_assets", {"asset_paths": []})
    return {
        "strategy": strategy["refPath"],
        "status": "daily economy, capacity, growth and churn simulation compiled",
    }
