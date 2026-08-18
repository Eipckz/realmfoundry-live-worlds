# RealmFoundry: Live Worlds

RealmFoundry is an original playable 3D Unreal Engine 5 management simulation about designing and operating a simulated MMORPG. The operator walks through six glowing construction zones to establish an inn, quest hall, uplink, monster zone, paid flight route, and named `0.2` release while the world, customers, combat, dungeon, economy, and live-service systems continue independently.

The implementation is a breadth-complete, data-driven vertical slice of the frozen game contract. It includes an original 56-mesh Blender kit, an original rigged subscriber with 15 animations, an in-world town/dungeon/transport showcase, an operator HUD, persistent autosave, and six live Blueprint simulation directors.

See [GAME_CONTRACT.md](GAME_CONTRACT.md) for the frozen release contract, [FEATURE_MATRIX.md](FEATURE_MATRIX.md) for implementation depth, and [TEST_LEDGER.md](TEST_LEDGER.md) for reproducible evidence.

## Toolchain

- Unreal Engine 5.8.1 with Epic Model Context Protocol and All Toolsets enabled for editor use
- Blender 5.2 LTS with DCC-MCP Blender
- Blueprint-only runtime architecture for reproducible content-only packaging on the configured machine

## Play

Open `RealmFoundry.uproject` in Unreal Engine 5.8.1 and press Play, or run the archived Windows build from `Packaged/Windows/RealmFoundry.exe` after building locally. Use the standard third-person movement controls and walk through the six numbered cyan zones from west to east. The HUD reports company cash, subscribers, active players, infrastructure, release state, and the current objective.

## Rebuild

Regenerate all original Blender assets by running `ExternalAssets/Scripts/generate_realmfoundry_assets.py` inside Blender 5.2. The deterministic script recreates the authoritative `.blend`, GLB, static FBX, rigged FBX, manifest, and preview.

Create a Windows package with:

```powershell
& 'D:\UE_5.8\Engine\Build\BatchFiles\RunUAT.bat' BuildCookRun -project="$PWD\RealmFoundry.uproject" -noP4 -platform=Win64 -clientconfig=Development -cook -allmaps -build -stage -pak -iostore -archive -archivedirectory="$PWD\Packaged" -utf8output
```

## Status

The autonomous production pass concluded August 18, 2026. Blueprint compilation, PIE acceptance, autosave, cook/package, and archived-executable smoke tests pass. Generated build products are intentionally excluded from Git; reproduce them with the command above.
