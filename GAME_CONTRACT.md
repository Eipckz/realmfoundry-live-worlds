# RealmFoundry: Live Worlds

Contract revision: 1.0 — frozen vertical slice  
Target project: `D:\CodexGames\RealmFoundry\RealmFoundry.uproject`

## Product

- One-sentence fantasy: Design, launch, monetize, and operate a living 3D MMORPG whose individually simulated customers visibly inhabit the world you build.
- Player verbs: inspect, orbit, sculpt, buy, place, connect, price, configure, hire, research, design, publish, moderate, repair, pause, accelerate, and analyze.
- Core loop: acquire a region → build a playable MMO destination → connect infrastructure → attract subscribers → satisfy needs and earn revenue → research features → ship named updates → expand while controlling bugs, congestion, cheating, and debt.
- Session length: 30–90 minutes per campaign; unlimited sandbox continuation after victory.
- Target platform and input: Windows 64-bit packaged build; keyboard/mouse primary and gamepad-compatible camera/UI navigation. Project content is platform-neutral for native macOS/Linux builds.
- Camera and movement model: 3D strategy camera with pan, edge/keyboard movement, orbit, zoom, focus, and construction-mode raycasts.
- Win state: reach MMO rating 4.5, 5,000 active subscribers, positive 30-day cash flow, and release a named Major Update without unresolved crash-level bugs.
- Loss state: cash remains below the loan limit for 30 simulated days, or reputation reaches zero with no active subscribers. The player can restart or continue in recovery mode.

## Vertical slice

- Start state: loan-backed company setup creates a named MMO, logo seed, business model, target appeals, world seed, and first owned region.
- Traversable space: one stylized 3D valley region with a buildable settlement, lake, bridge, road, server coverage, and a small dungeon entrance.
- Objective: place an inn, quest NPC, uplink, monster zone, and paid travel stop; connect coverage; launch version 0.1; satisfy 25 simulated subscribers; publish version 0.2.
- Required interaction: construction preview and placement, service pricing, quest generation, update changelog selection, and release while servers are offline.
- Feedback/UI: build palette, placement validity, region/network overlays, subscriber bubbles, finance/appeal HUD, objective tracker, release dialog, pause/speed controls, and explicit failure reasons.
- End-state transition: a successful release celebration, rating/subscriber increase, and unlocked world-expansion screen; failure displays recovery actions.
- Restart behavior: new campaign clears runtime systems and widgets, reloads seed/setup data, and creates one copy of every manager.

## Content matrix

| ID | Type | Source | Required states/animations | Unreal destination | Acceptance check |
|---|---|---|---|---|---|
| CH-001 | Operator drone/cursor | Original Blender | idle hover, select pulse, invalid shake | `/Game/Characters/Operator` | Visible, animated, selects and places objects |
| CH-002 | Modular subscriber | Original Blender | idle, walk, run, talk, cheer, melee, ranged, cast, hit, death, ghost, sit | `/Game/Characters/Subscribers` | AI changes activity and animation without errors |
| CH-003 | Developer/GM staff | Original Blender variants | idle, walk, type, repair, inspect, celebrate | `/Game/Characters/Staff` | Staff travel to work and complete tasks |
| CR-001 | Monster family | Original Blender | idle, patrol, attack, hit, death, boss phase | `/Game/Characters/Monsters` | Zone spawn and tactical combat pass |
| IT-001 | Weapon kit | Original Blender | 14 readable category silhouettes plus ray gun | `/Game/Items/Weapons` | Class permissions, visuals, price, and item level work |
| IT-002 | Loot/consumable kit | Original Blender | closed/open, pickup, active | `/Game/Items/Loot` | Chest, key, potion, trinket, and visible loot work |
| ENV-001 | Feudal town kit | Original Blender | doors/openable parts | `/Game/Environment/Architecture/Feudal` | Validation building snaps with no gaps |
| ENV-002 | Ruins/wild-west/scifi/confection/eldritch variants | Original Blender/material variants | optional emissive/animated parts | `/Game/Environment/Themes` | Each theme has functional building/readable scenery coverage |
| ENV-003 | Infrastructure/transport kit | Original Blender | uplink pulse, vehicle/boat/teleporter motion | `/Game/Environment/Infrastructure` | Coverage and independent route pricing work |
| ENV-004 | Dungeon kit | Original Blender | doors, locks, keys, chests, traps, boss props | `/Game/Environment/Dungeons` | Editable room/corridor/key/boss loop completes |
| FX-001 | Weather/water/combat/update effects | Unreal procedural materials/Niagara | rain, fog, waterfall, hit, heal, release celebration | `/Game/FX` | Effects respond to configuration and settings |
| UI-001 | Management interface | Unreal UMG/vector shapes | all management states | `/Game/UI` | 1280×720 through 4K, keyboard/gamepad focus, no stale widgets |

## Art and technical direction

- Shape language and palette: readable stylized diorama realism; chunky modular silhouettes, warm settlement lighting, cool network overlays, saturated service accents, and restrained UI panels.
- Realism/stylization: stylized proportions with physically plausible materials and lighting; no copied commercial-game assets or logos.
- Unreal units and Blender units: 1 Unreal unit = 1 cm; 1 Blender unit = 1 meter; Z-up handoff verified on import.
- Texture/material budgets: 1K repeated props, 2K characters/building atlases, 4K only for shared terrain/theme atlases; bounded master materials with instances; ORM packing.
- Triangle/LOD budgets: subscriber 18k/9k/3k; monster 25k/12k/4k; building module 15k with Nanite eligibility; prop 1k–12k; three LODs for repeated non-Nanite meshes.
- Skeleton and retarget target: one original humanoid root skeleton for subscribers/staff; separate quadruped/monster skeleton where needed; Unreal retarget assets documented.
- Root-motion policy: in-place locomotion driven by AI/camera-safe movement; bounded boss attacks may use root motion.
- Modular building grid: 100 cm base grid, 300 cm floor height, 20 cm wall thickness, snap-corner pivots.
- Collision policy: simple convex/box collision for buildings/props, capsules for characters, query channels for placement/interactions, complex collision only for justified static terrain.
- Performance target: 60 FPS at 1920×1080 on RTX 3060-class hardware; 10,000 logical subscribers in background simulation with no more than 150 representative 3D agents active; <6 GB VRAM and <10 GB RAM in the release map.

## Architecture

- Maps and game mode: `W_MainMenu`, `W_RealmFoundry`, `W_DungeonPreview`, `W_Automation`; `BP_RFGameMode`, `BP_RFGameState`, `BP_RFPlayerController`, strategy-camera pawn.
- Player/NPC/item responsibilities: camera pawn owns navigation/selection; controller owns input/mode; game state exposes time/company totals; simulation subsystem owns logical subscribers; representatives mirror logical state; services and items are data-driven actors.
- Interfaces, components, data assets, and tags: interaction/placeable/service/priceable/damageable interfaces; construction, network, service, inventory, needs, combat, and animation components; primary data assets for buildings, technology, class, weapon, monster, quest, update, art pack, and subscriber archetype; gameplay tags for states/actions/effects.
- Save/progression needs: manual save, autosave rotation, seed/setup, owned regions, constructions, districts/water, prices/routes, research, bugs, releases, staff, subscribers, economy history, moderation actions, and settings.
- Folder and naming convention: `/Game/Core`, `/Game/Data`, `/Game/Characters`, `/Game/Items`, `/Game/Environment`, `/Game/Maps`, `/Game/UI`, `/Game/FX`, `/Game/Audio`, `/Game/Tests`; `SK_`, `SM_`, `T_`, `M_`, `MI_`, `A_`, `ABP_`, `BP_`, `DA_`, `W_`, `UI_` prefixes.

## Acceptance tests

1. Packaged executable launches into `W_MainMenu`, starts a seeded campaign, loads `W_RealmFoundry`, and exits cleanly.
2. Strategy camera pans, orbits, zooms, focuses, and selects with keyboard/mouse; gamepad equivalents retain UI focus.
3. The vertical-slice objective can be completed from a clean campaign and produces the version 0.2 celebration.
4. Valid placement deducts cost and creates one saved building; invalid/obstructed placement explains why and creates nothing.
5. Undo/redo restores the last 20 construction mutations, including group duplication.
6. District, lake, water elevation, waterfall, bridge, obstruction, entrance, and impassable-state interactions update traversal/placement validity.
7. Network coverage, bandwidth, region capacity, congestion, and server strain change from buildings and subscriber load.
8. A class, monster, weapon permission, ability, and quest can be configured and used by a representative subscriber.
9. A four-member party forms, shares a quest/loot, travels, and uses tank/healer/damage tactics in combat.
10. A dungeon contains rooms, doors, keyed locks, visible loot, dungeon-only monsters, and a two-phase boss; parallel logical instances do not pause the main world.
11. Every functional building exposes its supported services, separate prices, availability/maintenance state, use count, and income.
12. Paid, subscription, free-to-play, and hybrid campaigns calculate acquisition, recurring revenue, and microtransaction spending from private budgets.
13. Staff research technology, repair a building, debug a bug under policy, investigate a report, and warn/ban a subscriber.
14. Named releases require changelog content and downtime, pay marketing cost, generate hype, and preserve release history.
15. Manual save and autosave restore the same seed, constructions, economy, research, subscribers, and release history without duplicate managers/widgets.
16. Finance, subscribers, active players, spending, advertising conversion, happiness, rating, competition, streamer/VIP, and awards views update from simulation data.
17. At least 10,000 logical subscribers simulate while no more than the representative-agent cap is rendered; performance target is measured in the stress map.
18. Blueprint/map/asset validation, focused automation, two clean PIE runs, standalone play, cook, package, and packaged smoke tests pass with no new fatal/error sequence.

## Explicit non-goals

- Real online multiplayer or external MMO servers; subscribers are autonomous simulated customers inside a single-player management game.
- Unreleased roadmap features: factions and unrestricted world PvP, world raid bosses, disasters, Twitch integration, Steam Workshop integration, the future full in-game Codex, and claims of version 1.0.
- The documented pre-spawn charging exploit is not implemented as a dependable feature.
- Licensed or copied art, names, logos, music, or code from the referenced commercial game.

