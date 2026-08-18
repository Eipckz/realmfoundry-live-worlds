---
name: realmfoundry-feature-studio
description: Build, extend, recover, and validate RealmFoundry Unreal Engine gameplay slices through Unreal MCP and Blueprint graph DSL. Use for RealmFoundry feature implementation, management UI, subscriber simulation, technology gates, construction, economy, combat, quests, dungeons, save/load, campaign, PIE testing, packaging, or release-readiness work in the RealmFoundry project.
---

# RealmFoundry Feature Studio

Implement one end-to-end playable slice at a time and leave every partial run recoverable.

## Start from evidence

1. Inspect `Design/Production-Handoff.md`, `Design/Game-Design-Contract.md`, the current Git status, and the loaded Unreal level.
2. Read the relevant existing Blueprint graphs before replacing them.
3. Treat feature names, counters, static actors, and documentation claims as unverified until exercised in PIE.
4. Preserve unrelated user changes and never introduce a C++ requirement unless a working compiler toolchain is confirmed.

Read [references/unreal-mcp-workflow.md](references/unreal-mcp-workflow.md) before authoring or testing Blueprint assets.

## Build a vertical slice

For each feature:

1. Define its player action, visible state, simulation consequence, failure state, and acceptance test.
2. Put authoritative state on a Blueprint or data asset, not only in HUD copy or debug prints.
3. Enforce prerequisites at the action boundary. Do not rely on disabled-looking UI alone.
4. Expose the result through the strategy HUD and, when applicable, a mouse-driven control.
5. Compile changed Blueprints with warnings treated as errors.
6. Save all assets, run PIE, inspect runtime properties and logs, and capture visual evidence.
7. Update the handoff only after validation passes.

## Keep authoring recovery-safe

- Make ProgrammaticToolset scripts idempotent: check for assets, variables, widgets, actors, and components before adding them.
- Clean artifacts from failed retries before saving.
- Use the project MCP wrapper at `Tools/Invoke-UnrealMcp.ps1` for deterministic calls.
- Store reusable Unreal orchestration scripts under `Design/Programmatic/`.
- Discover exact Blueprint node type IDs and pins before using a new node.
- Call `ObjectTools.list_properties` before setting UMG widget or slot properties.
- Stop PIE before structural asset edits.
- Keep exactly one Unreal Editor instance attached to the project.

## Validate completion

Require all of the following before calling a slice complete:

- The authoritative Blueprint compiles with warnings as errors.
- PIE starts and stays running.
- The positive path changes runtime state.
- At least one negative or locked path rejects the action without charging resources or mutating success counters.
- The player can see the changed state in the HUD or world.
- Current-session logs contain no Blueprint runtime errors, `Accessed None`, fatal errors, or new save failures.
- Changed assets are saved and visible in Git status.

Do not mark the overall release complete until the packaged Windows executable launches outside the editor, the exact release artifact is smoke-tested, source/content is pushed, and the executable is attached to a GitHub Release.
