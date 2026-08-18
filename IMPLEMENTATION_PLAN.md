# RealmFoundry: Live Worlds — Autonomous Implementation Plan

This plan is executable by a future Codex agent using `$autonomous-unreal-game-studio`, `$blender-game-asset-pipeline`, and `$unreal-mcp-game-builder`. Every phase ends in saved evidence and a testable gate.

## 0. Environment and repository

1. Run the studio health script and save JSON to `Evidence/StudioHealth.json`.
2. Start/reuse Blender gateway, Blender, and Unreal; prove ports 9765 and 8000.
3. Create a Blueprint-only UE 5.8 project, editor-only MCP plugins, project-local Codex config, source-art folders, and Git LFS rules for large binary sources.
4. Record engine/add-on/CLI versions and package prerequisites.

Exit: project opens, MCP tool search works, empty map saves, and source control has deterministic ignores.

## 1. Vertical slice greybox

1. Create strategy camera, selection trace, build mode, time controls, game state, and objective tracker.
2. Greybox one valley region, lake, road, bridge, settlement pad, dungeon entrance, and obstruction.
3. Implement placeable/service base data and five required slice objects: inn, quest NPC, uplink, monster zone, travel stop.
4. Implement minimal subscriber planner, network coverage, service use, revenue, satisfaction, changelog, downtime, and version release.
5. Add win/failure states and clean restart.

Exit: acceptance tests 1–4 pass twice in PIE with zero Blueprint errors.

## 2. Original asset production

Produce deterministic Blender collections and scripts for:

- operator drone;
- modular humanoid subscribers/staff with animation coverage;
- monster and boss family;
- 14 weapon silhouettes plus optional ray gun;
- loot, keys, chests, potions, trinkets;
- 100 cm-grid town kit and validation building;
- functional building silhouettes and infrastructure/transport kit;
- dungeon kit;
- six material/theme families.

For each batch: save `.blend`, render preview, validate, export FBX/GLB, hash outputs, update `ASSET_MANIFEST.md`, import to deterministic Unreal destinations, verify scale/material/collision/source path.

Exit: no unresolved Blender validation errors and Unreal asset validation passes.

## 3. World and construction

1. Generated seed preview and reproducible world initialization.
2. Region ownership, names, levels, settlements, terrain color/grass/weather/light controls.
3. Normal, flat, and lake districts; elevation, climbability, water color, impassability, connected rivers/waterfalls.
4. Object transform/duplicate, box selection, groups/constructions, precise duplicate, 20-action undo/redo, scenery brush, obstruction/entrance overlays, automatic maintenance.
5. Roads, walls, paths, bridges, landmarks, screenshot overlay toggle.

Exit: construction suite and save/load mutation tests pass.

## 4. Services, infrastructure, and transport

1. Multi-service buildings with per-service price/use/income and maintenance availability.
2. Inns, taverns, blacksmiths, potion shops, markets, trinket carts, graveyards, quest NPCs, starts, landmarks, dungeon entrances, and travel buildings.
3. Uplink nodes, cables/fibers, coverage, bandwidth, capacity, congestion, strain, network overlay, remote starts, and load migration.
4. Boats, flight, vehicles, teleporters, bridges, multi-route connections, route price/use/affordability.

Exit: acceptance tests 6, 7, and 11 pass.

## 5. Content authoring and tactical play

1. Data-driven class editor: appearance preset, stats/resources, permitted weapons, ability list, level gates, progression rate, unlock slots.
2. Monster/NPC editor: visual preset, stats, levels, abilities, weapons, elite/dungeon/boss flags, painted zones, scaling, slot unlocks.
3. Weapon catalog and visual item-level tiers; projectile definitions; combat animation mapping.
4. Quest generator for fetch, buy/equip, travel, scenery, hunt, building/service direction, reward/progression, party choice, and abandonment.
5. Friends, messaging, social circles, parties of four, shared quests/loot, tavern formation, group travel, leaderboards, and PvP duels.
6. Tactical combat: basic/custom abilities, targeting, effects, AoE, taunt/pull, tank/healer roles, potions, accidental-pull avoidance, obstacle recovery, combat shouts.

Exit: acceptance tests 8 and 9 pass with deterministic fixtures.

## 6. Dungeons

1. Flexible room/corridor floor-paint layout with animated material options.
2. Doors, keyed locks, containers/chests, visible loot, scenery, dynamic light, fog/ground fog.
3. Dungeon-exclusive monsters, configurable two-phase boss, boss abilities/loot/key-gated treasure.
4. Parallel logical instances and a focused view that leaves world simulation running.
5. Entry price and server-load relief.

Exit: acceptance test 10 passes from entry through boss loot.

## 7. Subscriber simulation and economy

1. Stable logical identity/profile, schedule, interest, expertise, budget, bank, happiness, addiction, home, quest, party/social graph, inventory/equipment, playtime, activity, travel/purchase propensities, toxicity/cheat traits, churn reason.
2. Background planning with remaining-session-time awareness and representative 3D-agent pooling.
3. Paid/subscription/F2P/hybrid acquisition and pricing; purchase, subscription, weapon, potion, home, resurrection, dungeon, travel, trinket, and service transactions.
4. Economy history, individual building income, daily microtransactions, revenue/expense graphs, active/subscriber/spending trends, live pricing changes.

Exit: acceptance tests 12 and 17 pass under fixed seeds.

## 8. Development, operations, release, reception, moderation

1. Staff hiring/travel/workplaces; research tree for features, capacity, debugging, art packs, and content slots.
2. Bugs by severity, priority policies, manual fixes, building repairs, offline speed bonus, forced-online cancellation.
3. Changelog tracking, excitement, release types/names/notes, marketing, hype, warnings, immediate/scheduled downtime, forced logout, publish, celebration, release history.
4. Advertising impressions/conversion, buzz/reviews/reports, rating/happiness, competitors, streamers/VIPs, expos/promotions, awards.
5. Suspected cheating, gold-farm/toxic evidence, reports, warning/ban policy, searchable logs, anti-cheat, GM investigations.

Exit: acceptance tests 13, 14, and 16 pass.

## 9. UX, persistence, settings, and platform readiness

1. Manual save, rotating autosaves, detailed listing, typed numeric inputs, borderless/exclusive fullscreen, monitor/resolution/refresh choices, notification/combat-shout filters, active-mod listing.
2. Versioned save schema and migration hooks; asynchronous/background-safe serialization where Blueprint facilities allow.
3. Localization-ready text tables for English plus four additional language slots.
4. Platform-neutral content/config and documented native build commands for Windows/macOS/Linux.

Exit: acceptance test 15 and UI scaling/focus tests pass.

## 10. Release and GitHub

1. Compile/save/validate all Blueprints and imported assets; fix first root error.
2. Run focused automation, map tests, two clean PIE loops, standalone loop, save/load, stress/performance, cook/package, and packaged executable smoke.
3. Capture logs, screenshots, hashes, size, version, feature matrix, test ledger, known limits, and future-agent handoff.
4. Initialize git, configure LFS guidance, commit source and reproducible scripts while excluding DerivedDataCache/Intermediate/Saved/package bulk, create GitHub repository, push default branch, and verify remote contents.

Exit: packaged executable repeats the vertical slice and the remote repository contains all reproducible project/source/documentation files.

