# Asset Manifest

All RealmFoundry-specific presentation assets are original and were authored procedurally in Blender for this project. The `.blend` sources remain authoritative outside Unreal `Content`.

## Corrected v0.3.0 presentation set

| ID | Blender source | Exchange asset | Unreal destination | Validation | Status |
|---|---|---|---|---|---|
| TD-001 | `ExternalAssets/DioramaV2/RF_DioramaV2.blend` | `RF_TownDiorama_V2.fbx` | `/Game/Environment/DioramaV2/SM_RF_TownDioramaV2` | 523 authored objects, 22 materials, rendered 1920x1080 preview | verified |
| BLD-001 | same source | `RF_Building_Inn_V2.fbx` | `SM_RF_InnV2`, `BP_RFBuildable_InnV2` | origin-centered runtime building | verified |
| BLD-002 | same source | `RF_Building_Smithy_V2.fbx` | `SM_RF_SmithyV2`, `BP_RFBuildable_SmithyV2` | origin-centered runtime building | verified |
| BLD-003 | same source | `RF_Building_Uplink_V2.fbx` | `SM_RF_UplinkV2`, `BP_RFBuildable_UplinkV2` | origin-centered runtime building | verified |
| BLD-004 | same source | `RF_Building_GuildHall_V2.fbx` | `SM_RF_GuildHallV2`, `BP_RFBuildable_GuildHallV2` | origin-centered runtime building | verified |
| BLD-005 | same source | `RF_Building_DungeonGate_V2.fbx` | `SM_RF_DungeonGateV2`, `BP_RFBuildable_DungeonGateV2` | origin-centered runtime building | verified |
| BLD-006 | same source | `RF_Building_TravelDock_V2.fbx` | `SM_RF_TravelDockV2`, `BP_RFBuildable_TravelDockV2` | origin-centered runtime building | verified |

Preview: `ExternalAssets/DioramaV2/RF_DioramaV2_Preview.png`.

Generation is deterministic through `ExternalAssets/Scripts/generate_realmfoundry_diorama_v2.py`; modular exports are produced by `ExternalAssets/Scripts/export_realmfoundry_buildings_v2.py`.

## Supplementary legacy simulation library

`ExternalAssets/MasterLibrary/RF_MasterLibrary.blend` remains available for the broader simulation layer. It contains 56 named meshes, a weighted 18-bone subscriber rig with 15 isolated animation clips, service props, dungeon pieces, creatures, and 15 weapon-category representatives. These assets support design coverage but are not used as the corrected release's main town presentation.
