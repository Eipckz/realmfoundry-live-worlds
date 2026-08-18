# Feature Matrix

Status values: `verified-slice`, `implemented-sim`, `represented-data`, `deferred-roadmap`.

| Area | Status | Primary system | Verification |
|---|---|---|---|
| MMO definition/business model/setup/seed | verified-slice | `BP_RFSimulationManager`, economy data | Loan start, name, paid + subscription + F2P flags and seed state |
| Regions/terrain/settlements/districts/water | implemented-sim | `BP_RFWorldDirector` | Two regions, six districts, flat/lake/waterway/weather state advances live |
| Advanced construction/brush/groups/undo | implemented-sim | `BP_RFWorldDirector` | Brush/group/duplication state and 20-action undo depth |
| Functional buildings/services | verified-slice | World set + economy data | Inn, tavern, shops, market, graveyard, quest hall, portal, dungeon, travel |
| Network/server infrastructure | verified-slice | Simulation + world directors | Uplink objective reaches 100 coverage and 250 capacity |
| Player class design | represented-data | `BP_RFCombatDirector` | Five role classes, resources, category permissions, ability parameters |
| Monster/NPC design and zones | verified-slice | Combat director + world set | Slime, golem, elite/boss, quest representative, painted-zone state |
| Weapons/abilities | verified-slice | Combat director + asset displays | Fifteen categories (14 core + ray gun), status effects, ranged/melee/cast |
| Quests/progression | verified-slice | Simulation + subscriber directors | Quest zone, progression state, party quest and abandonment decisions |
| Friends/parties/social | implemented-sim | `BP_RFSubscriberDirector` | Friends, messages, social circles, four-player parties, shared state |
| Tactical PvE/PvP duels | verified-slice | `BP_RFCombatDirector` | Pulls, target selection, role logic, AoE count, status effects, boss phases |
| Editable dungeons | verified-slice | `BP_RFDungeonDirector` + vignette | Rooms, corridors, locks, key, chest, loot, fog, dynamic light, phased boss |
| Transportation/routes | verified-slice | World set + economy data | Boat, flight point, vehicle, teleporter, bridge, paid per-route state |
| Individual subscriber simulation | verified-slice | `BP_RFSubscriberDirector` | Profiles, schedules, budgets, bank, spending, activity, addiction, cheating |
| Monetization/economy | verified-slice | `BP_RFEconomyDirector` | Loan, service/route pricing, daily income, budgets, cashflow and graphs data |
| Development/technology/bugs | implemented-sim | `BP_RFLiveOpsDirector` | Developers, research, repair, severity queues, policies, debugging/anti-cheat |
| Updates/maintenance/live service | verified-slice | Simulation + live-ops directors | Changelog, named releases, hype, shutdown/maintenance data; playable `0.2` gate |
| Advertising/reception/competition/awards | implemented-sim | `BP_RFLiveOpsDirector` | Impressions, rating, streamer influence, campaigns, awards state |
| Moderation/cheating/Game Masters | implemented-sim | Subscriber + live-ops directors | Reports, suspicion, evidence, warning/ban policies, anti-cheat research |
| Art packs/themes | represented-data | Original master asset library | Feudal/fantasy base plus ruins, pulp sci-fi, confection, eldritch palette data |
| Save/settings/QoL/localization/mod listing | verified-slice | `BP_RFSaveDirector`, HUD, live ops | Real five-second autosave, settings data, five locales, active-mod listing |
| Factions/unrestricted PvP/raids/disasters/Twitch/Workshop/full Codex | deferred-roadmap | None | Explicit non-goal |
