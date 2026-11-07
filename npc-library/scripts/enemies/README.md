# Enemies: baddies, AI, bosses, waves

Part of the [original NPC library](../README.md). Covers `combat / baddies` and the AI half of `combat / weapons` in [`behaviours.md`](../../behaviours.md). Traps and turrets are in `hazards/`, and respawning and timed spawners are in `spawners/`.

All moving enemies run a 0.05 s timer, the AI rate the manual reports for the archived corpus (§8.1.4). They move by assigning `x` and `y` and test walls with `onwall`. Only the level leader gets these timeouts (no `timereverywhere`), so one client drives the enemy for everyone in the level. Defeated enemies `hide` rather than `destroy`, so they come back on the next visit. Online, `destroy` would delete the NPC from the server (§8.2.3).

Hit handling: `washit` (sword, damage = `playerswordpower`), `wasshot` (arrow) and `exploded` (bomb). Touch damage uses `hurt`, which knocks the player away from the NPC.

| File | What it does |
| --- | --- |
| `lunger.gs1` | Waits at home, charges along a row or column when the player lines up, stops at the wall, walks back. |
| `wanderer.gs1` | Roams a rectangle, picks a random direction and speed every 1–3 s, turns at walls and edges. |
| `chaser.gs1` | Character that chases within 7 tiles, gives up past 11, slides along walls, is knocked back on hits. |
| `archer.gs1` | Keeps 4–9 tiles away and fires an arrow whenever the player is in line, every 1.5 s at most. |
| `guard-patrol.gs1` | Walks a square route with a view strip ahead. Shouts and chases intruders without a pass, then rejoins at the nearest corner. Out for 20 s after 5 hits. |
| `burrower.gs1` | A harmless mound that drifts toward the player and bursts out for 1.5 s when close. It can only be hit while out. |
| `blocker.gs1` | Mirrors the player's sideways position along a lane. Swords bounce off and an arrow stuns it for 2 s. |
| `bat-swoop.gs1` | Circles its roost and swoops at the player's position when they come within five tiles, then flies back. Two-frame flap (bat sheet, wings up at x 0 and down at x 32, 32x32). One hit kills. Events: playerenters, playertouchsme, washit, wasshot, timeout. The file has no comments, because `spawners/spawner-npc.gs1` places it with `putnpc` (see that folder's README). |
| `boss-golem.gs1` | Two-phase boss: a fireball ring, then faster with charges. Invulnerable flash after each hit. Defeat sets a flag and drops a heart container. |
| `wave-controller.gs1` | Invisible arena controller: three waves of built-in baddies (`putcomp`), each started by `compusdied`, then a reward. |
| `baddy-reset.gs1` | Clears the built-in baddies on entry and places a fresh set with `putnewcomp`, or none once a flag is set. |
