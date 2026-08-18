# Future Agent Handoff

## Current state

RealmFoundry is a concluded, playable Unreal Engine 5.8.1 Blueprint-only vertical slice. The source project lives at `D:\CodexGames\RealmFoundry\RealmFoundry.uproject`. The authoritative Blender generator is `ExternalAssets/Scripts/generate_realmfoundry_assets.py`; generated sources and exchange files are under `ExternalAssets/MasterLibrary`.

The Windows package was created successfully under `Packaged/Windows` but is ignored by Git. Rebuild it with the command in `README.md`.

## Runtime architecture

- `/Game/Core/BP_RFSimulationManager`: six-zone onboarding/release loop and top-level KPIs.
- `/Game/Core/Systems/BP_RFWorldDirector`: regions, districts, waterways, construction and obstruction state.
- `/Game/Core/Systems/BP_RFSubscriberDirector`: individual customer, schedule, social, spending and behavior simulation.
- `/Game/Core/Systems/BP_RFCombatDirector`: classes, weapon permissions, abilities, effects, roles and tactical decisions.
- `/Game/Core/Systems/BP_RFDungeonDirector`: rooms, locks, loot, instances and phased boss simulation.
- `/Game/Core/Systems/BP_RFEconomyDirector`: business models, prices, routes, budgets, revenue and loan state.
- `/Game/Core/Systems/BP_RFLiveOpsDirector`: staff, research, bugs, maintenance, releases, marketing and moderation.
- `/Game/Core/Save/BP_RFSaveDirector`: real five-second `SaveGameToSlot` persistence.
- `/Game/UI/WBP_RFOperatorHUD`: operator-facing objective and KPI HUD.
- `/Game/Maps/W_RealmFoundry`: complete authored showcase and playable acceptance path.

## Known boundaries

The project deliberately implements the requested catalog as a breadth-complete vertical slice: some editor-heavy systems are represented by live data and simulation instead of production-scale authoring UIs. The explicitly unreleased roadmap features remain out of scope: factions/unrestricted world PvP, world raids, disasters, Twitch, Workshop, full in-game Codex, additional creativity spikes, and version 1.0.

The project includes Epic Third Person template content for the inherited movement/controller foundation. All RealmFoundry-specific meshes, weapons, monsters, buildings, dungeon pieces, subscriber rig/animations, and operator drone are original generated assets.

## Verification

Read `TEST_LEDGER.md` before changing runtime logic. The final baseline passes Blueprint compilation, 9/9 automation smoke tests, map PIE, six-zone gameplay acceptance, editor and packaged autosave, BuildCookRun, and a 15-second archived-executable runtime audit.
