# Asset Manifest

All RealmFoundry-specific visual assets are original and generated for this project. Blender source remains authoritative outside Unreal `Content`; standard Unreal Engine Third Person template content supplies the inherited movement/controller foundation.

| ID | Blender source | Exchange | Preview | Unreal destination | Validation | Status |
|---|---|---|---|---|---|---|
| ML-001 | `ExternalAssets/MasterLibrary/RF_MasterLibrary.blend` | `RF_StaticLibrary.glb`, `RF_StaticLibrary.fbx` | `RF_MasterLibrary_Preview.png` | `/Game/Environment/RealmFoundryKit` | 56 stable named meshes; 17 key meshes with generated convex collision | verified |
| CH-001 | `ExternalAssets/MasterLibrary/RF_MasterLibrary.blend` | `SK_RFSubscriber.fbx` | master preview | `/Game/Characters/Subscriber` | 18-bone single-root rig, weighted mesh, physics asset | verified |
| AN-001 | subscriber actions in master `.blend` | `SK_RFSubscriber.fbx` | live world representatives | `/Game/Characters/Subscriber` | 15 isolated in-place clips: Idle, Walk, Run, Talk, Cheer, Melee, Ranged, Cast, Hit, Death, Ghost, Sit, Type, Repair, Inspect | verified |
| ENV-001 | master `.blend` | static GLB/FBX | master preview | `/Game/Environment/RealmFoundryKit` | 12 functional buildings and service props | verified |
| ENV-002 | master `.blend` | static GLB/FBX | master preview | `/Game/Environment/RealmFoundryKit` | 18 infrastructure/modular/dungeon construction pieces | verified |
| CR-001 | master `.blend` | static GLB/FBX | master preview | `/Game/Environment/RealmFoundryKit` | slime, golem, eldritch multi-phase boss | verified |
| IT-001 | master `.blend` | static GLB/FBX | master preview | `/Game/Environment/RealmFoundryKit` | 15 weapon-category display models | verified |
| PROP-001 | master `.blend` | static GLB/FBX | master preview | `/Game/Environment/RealmFoundryKit` | chest, key, potion, trinket, respawn stone, operator drone | verified |

Generation is deterministic and rerunnable through `ExternalAssets/Scripts/generate_realmfoundry_assets.py`. Blender validation completed with zero reported topology, rig, animation, material, or export errors.
