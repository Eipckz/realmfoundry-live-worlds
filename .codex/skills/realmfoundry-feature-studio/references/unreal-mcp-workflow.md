# Unreal MCP workflow

## Connection

- Launch `D:\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe` with the project and `-ModelContextProtocolStartServer`.
- Use `Tools/Invoke-UnrealMcp.ps1`; the endpoint is `http://127.0.0.1:8000/mcp`.
- Use ProgrammaticToolset scripts for multi-step authoring. Define `run()` and call tools through `execute_tool(name, json.dumps(args))`.

## Blueprint graphs

1. Call `get_graph_dsl_docs` once per conversation before authoring.
2. Call `read_graph_dsl` before replacing a graph.
3. Use `find_node_types` and `get_node_type_pins` for every unfamiliar node.
4. Prefer discovered type IDs exactly; capitalization and punctuation vary across editor sessions.
5. Use `(bind (a b c) expression)` for multiple data outputs.
6. Use named pins for ambiguous calls and custom function parameters.
7. Compile with `warnings_as_errors: true` after the graph is complete.

## UMG

1. Call `GetWidgets` to recover the actual tree and variable flags.
2. For every returned widget and slot, call `ObjectTools.list_properties` before setting values.
3. Toggle runtime references with `ToggleWidgetAsVariable`, compile the widget, and restart the editor if the Blueprint action database does not expose the new getter nodes.
4. Bind buttons with `BindToEventProperty`, read the resulting event graph, then add logic to the generated `OnClicked(WidgetName)` events.
5. Validate UMG with a Slate screenshot because a raw viewport capture omits game UI.

## Runtime tests

- Start PIE in-process with `warmupSeconds: 0`, then wait briefly before inspection.
- Use Slate `PressKey` to exercise hotkeys against the focused PIE viewport.
- Find the runtime pawn with `SceneTools.find_actors` and read exact state using `ObjectTools.get_properties`.
- Test one allowed path and one rejected path.
- Capture the 3D world with `CaptureViewport`; capture the full HUD with `SlateInspectorToolset.Screenshot`.
- Stop PIE before editing assets.

## Known recovery hazards

- A failed idempotency check can add duplicate components on every retry. Detect generated component paths and remove extras before compiling.
- Multiple editors can lock `.uasset` files. Confirm one process and close stale instances normally before saving.
- World Partition actors save as external actor packages; save all assets after adding them.
- Authoring-time DSL errors remain in the session log. Compare timestamps and distinguish them from current PIE runtime errors.
