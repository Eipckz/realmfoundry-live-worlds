# RealmFoundry v0.4.0 — Living Worlds

This release expands the playable MMORPG-management loop and ships the matching Unreal Engine 5.8.1 project source.

## Highlights

- 10,000 logical subscribers represented by 36 visible animated inhabitants with names, classes, levels, activity labels, XP, gold, and lifetime-spending state.
- Four named visible staff members: two realm developers and two game masters with role-specific live activities.
- Eight timed, cash-gated technology tiers and six prerequisite-gated construction categories.
- Grid-snapped building placement with 45-degree rotation, undo/redo history, and save/load restoration of active building transforms.
- Four-stage campaign from founding through live operations, with a continuing sandbox after victory and a recoverable crisis state.
- Player-triggered service, network, quest/social, combat/PvP, dungeon, maintenance, moderation, and named-release operations.
- Live economy, server load/capacity/coverage/congestion, pricing, churn, happiness, rating, competitor, bug, and release metrics.
- Nineteen mouse controls across construction, research, subscriber inspection/follow, live operations, pricing, undo/redo, save, and load.

## Controls

- `WASD`: pan the strategy camera.
- Mouse action bars: select build cards and management actions.
- World click: place the selected snapped building or inspect a subscriber.
- `Q` / `E`: rotate construction by 45 degrees.
- `U` / `I` (also `Z` / `Y`): undo / redo the last construction.
- `T`: research the next technology tier.
- `F`: follow the selected subscriber; `Esc`: return to strategy view.
- `-` / `+`: adjust subscription price.
- `F5` / `F9`: save / load `RealmFoundry_Auto`.
- `R`: publish the original six-building major update.

## Build provenance

The Windows archive is produced by `Tools/Package-RealmFoundry-Windows.cmd` from the tagged source. `TEST_LEDGER.md` records the final cook, package, runtime, archive, and clean-clone verification for the downloadable artifact.
