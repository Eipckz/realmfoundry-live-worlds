# Future Agent Handoff

## Active release objective

RealmFoundry is under active expansion from the historical `v0.3.0` construction slice into a release-ready MMORPG management simulator. Do not describe the overall goal as complete until a newly packaged Windows executable has been launched outside Unreal, smoke-tested, pushed with the full source/content update, and attached to a GitHub Release.

The source project is `D:\CodexGames\RealmFoundry\RealmFoundry.uproject`. Use Unreal Engine 5.8.1 and keep the runtime Blueprint-only unless a working C++ toolchain is independently confirmed.

## Validated current systems

- `/Game/Characters/Subscribers/BP_RFSubscriberSpawner` creates 36 visible representatives for 10,000 logical subscribers.
- `/Game/Characters/Subscribers/BP_RFSubscriberRepresentative` runs animated world-space activity movement and owns a third-person follow camera.
- `/Game/Data/Technology` contains eight real technology definition data assets with prerequisite, cost, duration, tier, build unlock, and feature fields.
- `/Game/Core/Camera/BP_RFStrategyCameraPawn` enforces technology-tier build prerequisites, supports research, inspection/follow, daily economy simulation, pricing, and disk-backed save/load.
- `/Game/UI/WBP_RFOperatorHUD` reports live treasury, subscribers, price, daily economy, capacity/load, research, build prerequisite, and selected-subscriber state. It also contains a six-button mouse action bar.
- `F5` saves to `RealmFoundry_Auto`; `F9` restores the saved realm state.

## Reproducible evidence

- Research test: `$28,000 -> $23,000`, tier `0 -> 1` after timed completion.
- Technology rejection: selecting the tier-2 Smithy at tier 1 left cash and build count unchanged and set the rejection notification.
- Persistence test: saved tier 1 / `$23,000`, advanced to tier 2 / `$14,500`, then restored tier 1 / `$23,000` from disk.
- Economy test: price `12.99 -> 13.49`; daily close advanced the day, recalculated revenue/expenses/profit/capacity/load, and grew subscribers.
- Current-session PIE logs contained no Blueprint runtime error, `Accessed None`, ensure failure, or fatal error during the validated economy run.
- Visual evidence is generated under ignored `Saved/Validation/`.

## Authoring workflow

- Use `Tools/Invoke-UnrealMcp.ps1` for Unreal MCP calls.
- Reusable authoring scripts live under `Design/Programmatic/`.
- Use the project skill at `.codex/skills/realmfoundry-feature-studio/` and read its Unreal MCP reference before structural Blueprint or UMG edits.
- Stop PIE before structural edits, compile with warnings as errors, save all assets, and validate both a success and a rejected path.

## Still required for the release goal

- Persist placed-building classes and transforms, not only aggregate construction state.
- Complete subscriber inspection data, social behavior, quests, combat, progression, inventory, and churn reasons as observable gameplay.
- Replace director-only representations with playable building/service, infrastructure, dungeon, live-ops, moderation, campaign, and settings interactions.
- Add construction obstruction/rotation/undo and fuller mouse-first management panels.
- Run automation, performance, cook, packaging, and exact packaged-executable tests.
- Update GitHub source/content and publish the verified Windows package through GitHub Releases.
