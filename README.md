# RealmFoundry: Live Worlds

RealmFoundry is an original 3D, top-down MMORPG management simulator built in Unreal Engine 5. You operate a living fantasy service from a strategy camera: research technology, tune pricing, watch visible subscribers, expand capacity, place services, manage daily cash flow, inspect inhabitants, and publish updates.

![RealmFoundry top-down tycoon](Evidence/RealmFoundry_Tycoon_Shipping.png)

The repository is actively expanding beyond the historical `v0.3.0` construction slice. Current validated gameplay includes a 36-character visible population representing 10,000 logical subscribers, timed/costed technology research with enforced build prerequisites, a mouse action bar, daily revenue/expense/capacity/growth simulation, pricing controls, and disk-backed save/load. `FEATURE_MATRIX.md` distinguishes playable systems from director-only representations and remaining release work.

See [GAME_CONTRACT.md](GAME_CONTRACT.md) for the frozen product contract, [FEATURE_MATRIX.md](FEATURE_MATRIX.md) for implementation depth, [ASSET_MANIFEST.md](ASSET_MANIFEST.md) for asset provenance, and [TEST_LEDGER.md](TEST_LEDGER.md) for reproducible verification.

## Play the management loop

1. Use `W`, `A`, `S`, and `D` to pan the top-down camera.
2. Press `T` to research the next technology tier. Press `1` through `6` to select an Inn, Smithy, Uplink, Guild Hall, Dungeon Gate, or Travel Dock; locked categories reject placement until their prerequisite tier completes.
3. Left-click the world to place the selected service on the 250 cm construction grid.
4. Watch treasury, price, subscribers, active players, happiness, revenue, profit, capacity, load, and research update in the live HUD.
5. After all six service categories have been established, press `R` to publish the major update.

Additional controls: `0` enters subscriber inspection mode, `F` follows the selected subscriber, `Esc` returns to strategy view, `-`/`+` change subscription price, `F5` saves, and `F9` loads. The HUD action bar exposes the main inspect, build, research, follow, and release actions by mouse.

Each building costs `$2,500`, adds `400` subscribers and `7` hype, and contributes one changelog item. The major release adds `$15,000`, `4,000` subscribers, `25` hype, and advances the simulation by 30 days.

## Original 3D art

The primary town is a 523-object Blender scene with 22 authored materials, layered terrain, water, roads, bridges, trees, walls, market details, and fantasy service buildings. Six gameplay buildings are also exported as origin-centered modular assets for runtime placement. The authoritative source is `ExternalAssets/DioramaV2/RF_DioramaV2.blend`; the scene-generation and export scripts are stored beside the project.

The legacy master library remains in the repository as supplementary simulation content for classes, subscribers, monsters, weapons, dungeon props, and themed service data. It is not the presentation layer used by the corrected tycoon release.

## Run or rebuild

The next Windows release is being rebuilt after the active feature expansion. Until the new verified release artifact is published, run the project from source in Unreal Engine 5.8.1; do not treat the historical package as evidence for the current source state.

To work from source, open `RealmFoundry.uproject` in Unreal Engine 5.8.1. The project uses Epic's Model Context Protocol plugin and a Blueprint-only runtime architecture.

Useful scripts:

- `Tools/Launch-RealmFoundry-Editor.cmd` opens the project in the configured engine.
- `Tools/Package-RealmFoundry-Tycoon.cmd` cooks and archives the Windows Development build.
- `ExternalAssets/Scripts/generate_realmfoundry_diorama_v2.py` regenerates the Blender town.
- `ExternalAssets/Scripts/export_realmfoundry_buildings_v2.py` exports the six modular gameplay buildings.
- `Design/Programmatic/compile_tycoon_blueprints.py` compiles all corrected gameplay Blueprints with warnings treated as errors.

## Release status

The historical `v0.3.0` package passed its documented construction-slice gates. The active release goal is not complete: the expanded source must finish its remaining gameplay slices, then pass Blueprint compilation, PIE acceptance, persistence, automation, cook, Windows packaging, exact executable smoke tests, archive hashing, GitHub source push, and GitHub Release publication. See `FUTURE_AGENT_HANDOFF.md` and `TEST_LEDGER.md` for evidence and remaining work.
