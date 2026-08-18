# Test Ledger

Final corrected verification date: August 18, 2026. Engine: Unreal Engine 5.8.1. DCC: Blender 5.2.

## Active release expansion gates

These tests describe the current expanded source. The `v0.3.0` package evidence below remains historical and must not be used as proof for the next executable.

| Gate | Evidence | Result |
|---|---|---|
| Visible population | PIE spawned 36 animated representatives for 10,000 logical subscribers; sampled actors moved 377–490 cm over 1.5 seconds | pass |
| Live management HUD | Slate screenshot shows live treasury, subscriber, technology, economy, capacity/load, research, selection, and six-button action bar | pass |
| Timed technology | `T` changed cash `$28,000 -> $23,000` and tier `0 -> 1` only after research duration elapsed | pass |
| Technology rejection | Tier-2 Smithy selected at tier 1; placement left cash `$23,000` and build count `0`, with technology rejection notification | pass |
| Disk save/load | Saved tier 1 / `$23,000`, advanced to tier 2 / `$14,500`, loaded back to tier 1 / `$23,000` | pass |
| Daily economy | Price `12.99 -> 13.49`; day close recalculated revenue, expenses, profit, capacity/load, active players, happiness, cash, and subscribers | pass |
| Runtime errors | Latest validated PIE economy session had no Blueprint runtime error, `Accessed None`, ensure failure, or fatal error | pass |
| Current packaged executable | Expanded source has not yet been cooked and packaged | pending |

## Art and import gates

| Gate | Evidence | Result |
|---|---|---|
| Original top-down world | `ExternalAssets/DioramaV2/RF_DioramaV2.blend`; 523 objects, 22 materials | pass |
| Blender render | `RF_DioramaV2_Preview.png`, 1920x1080 | pass |
| Unreal import | combined town plus six modular building FBXs imported under `/Game/Environment/DioramaV2` | pass |
| Import commandlet | completed with 0 errors; one standard MCP EULA warning | pass |
| Legacy showroom removal | 49 slab/showroom actors and six objective-trigger actors removed from the release world | pass |

## Editor and gameplay gates

| Gate | Evidence | Result |
|---|---|---|
| Blueprint compile | GameMode, strategy pawn/controller, six buildables, HUD, and simulation manager compiled with warnings treated as errors | pass |
| Strategy presentation | elevated top-down camera, cursor input, WASD pan, no third-person operator pawn | pass |
| One-building transaction | Inn spawned at cursor; cash `28000 -> 25500`, subscribers `250 -> 650`, hype `8 -> 15`, progress `0 -> 1` | pass |
| Full construction loop | all six service categories placed in one PIE session | pass |
| Major update | `ReleaseComplete=true`, `CurrentDay=31`, `Cash=28000`, `Subscribers=6650`, `Hype=75`, `BuildCount=6`, `ProgressStep=6` | pass |
| Runtime confirmation | Development package visibly reported `BUILT: GRAND INN // HOME + RESPAWN SERVICES` after keyboard selection and cursor placement | pass |

## Package gates

| Gate | Evidence | Result |
|---|---|---|
| Windows Shipping cook/archive | 555 packages, PAK + IoStore, 0 errors, 1 standard EULA warning | pass |
| Shipping executable smoke | launched into the corrected top-down HUD and authored world | pass |
| Windows Development cook/archive | `BuildCookRun` ExitCode 0 | pass |
| Development executable smoke | keyboard/mouse construction input and spawned building verified | pass |
| Public ZIP structure | archive listing includes root `RealmFoundry.exe` plus PAK/UTOC/UCAS payload | pass |

## Published Windows artifact

```text
RealmFoundry-Tycoon-v0.3.0-Windows.zip
Size: 525,888,846 bytes
SHA256: 2EBEA02D92673BADB8CCBF8A9F69D1BEFB9A2D585F1DAAFCF7DFF86CCD005AAE
```

Development package contents: 55 files, 1,022,279,252 bytes.

```text
5A48C76C8B6DAA31309A915EEC6A47BFE434CAEA9B9DEC859F07066D43722630  RealmFoundry.exe
A40EA770025BAB301C17CA1803F23AD21AA9353550BC2AD717B1DD46B8EADD6E  RealmFoundry-Windows.pak
72E20D3B2C04B0A6E11F9F6B914012890C4183D72A7A4450BADB4ECD98D77871  RealmFoundry-Windows.utoc
7CB01D9CF80533E956A396BD9B9FA007EC034C318DF5D8D93DC141BF659FD9F9  RealmFoundry-Windows.ucas
```

`Packaged/`, `Releases/`, `Saved/`, `Intermediate/`, and derived caches are excluded from source control. The ZIP is distributed through the GitHub release.
