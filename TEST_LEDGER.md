# Test Ledger

Final autonomous verification date: August 18, 2026. Engine: Unreal Engine 5.8.1. DCC: Blender 5.2 LTS.

## Blender asset gates

| Gate | Evidence | Result |
|---|---|---|
| Mesh topology/normals | `RF_Inn` report `e37185c8-3190-4010-a247-e3408623fe1e`; boss report `edabcd1a-b1b5-4b9b-9956-d930284b687a` | pass |
| Character/rig | report `e1b17192-cc69-43f5-aff1-5901efb05113`; 18 bones, one root, weighted subscriber | pass |
| Materials | report `af05e47a-2568-40f2-8be4-6bb680de0357` | pass |
| Animation isolation | report `7aea2b56-00dd-425c-b172-01ae06f34da4`; 15 in-place clips | pass |
| Static GLB export | report `4118b18a-ee05-4302-ae1c-4fc560648499` | pass |
| Static FBX export | report `a4ea187f-ee2b-45dc-8bc6-ccd16b66b5d2` | pass |
| Rigged FBX export | report `b264f4fa-2231-423d-bf78-0d223d0a2347` | pass |

## Unreal editor gates

| Gate | Evidence | Result |
|---|---|---|
| Blueprint compile | All project-authored Blueprints compiled with warnings treated as errors | pass |
| Automation smoke | 9/9 CoreUObject/PCG/container/structured-log/color/tuple/typed-element tests | pass |
| Map PIE | `Project.Maps.PIE` 1/1; only host audio raw-mode warning | pass |
| Full gameplay acceptance | Traversed all six construction zones in one PIE session | pass |
| Acceptance state | `ProgressStep=6`, `Subscribers=25`, `ActivePlayers=13`, `Version=0.2`, `ObjectiveComplete=true`, `Cash=264250`, `Rating=4.5`, `Hype=80`, `NetworkCoverage=100`, `ServerCapacity=250` | pass |
| Persistence | Editor autosave `RealmFoundry_Autosave.sav`, successful five-second save cycle | pass |
| Live simulation sample | World revision 40; subscriber day 80; dungeon instances 2; economy revenue 2625; research 95; minor bugs 0 | pass |

## Package gates

| Gate | Evidence | Result |
|---|---|---|
| Windows cook/stage/archive | 631 packages; PAK + IoStore; `BuildCookRun` ExitCode 0 | pass |
| Archived executable | Process remained stable through 15-second smoke window | pass |
| Runtime world | Mounted containers, loaded `/Game/Maps/W_RealmFoundry`, brought world up for play, printed operator objective | pass |
| Runtime persistence | Packaged `RealmFoundry_Autosave.sav` created (1,980 bytes) | pass |
| Runtime log audit | 0 fatal errors, ensures, Blueprint errors, script errors, or `/Game` load failures | pass |

## Package fingerprints

```text
5A48C76C8B6DAA31309A915EEC6A47BFE434CAEA9B9DEC859F07066D43722630  RealmFoundry.exe
0C750B1A013B2FC988F8AA932D97CAFD62C5109DB15CC2A595F3CE66C2DA61A7  RealmFoundry-Windows.pak
D9725CDBCBD71E7CBB65AD304B1CD6CEE545382E9270E036D4CD4D0752EC0E72  RealmFoundry-Windows.utoc
2654CF00B7D7383CA794DCF655CC7A34BA7B0AD629E306BE89FA701347BA1C95  RealmFoundry-Windows.ucas
```

The archived Windows folder contains 52 files and 998,958,827 bytes. `Packaged/`, `Saved/`, `Intermediate/`, and derived caches are excluded from source control.
