# Transport: warps, lifts, teleporters

Part of the [original NPC library](../README.md). Covers the `transport / level-warps` and `transport / local-warps` categories of [`behaviours.md`](../../behaviours.md). The warp ring weapon is in `items/`.

Warps use `setlevel2` (level, x, y) between levels and an assignment to `playerx` / `playery` inside a level. `warp` and `jump` are not 2.05 commands (manual §8.1.8). Scripts whose timer guards one player's state call `timereverywhere`, because otherwise only the level leader gets the timeout (§8.1.4).

| File | What it does |
| --- | --- |
| `warp-basic.gs1` | Non-blocking warp to a fixed spot in another level. |
| `warp-guarded.gs1` | Warps only with a flag. Otherwise steps the player back a tile and explains, at most every 2 s. |
| `warp-random.gs1` | Sends the player to one of three levels at random. |
| `lift-panel.gs1` | Panel that steps through floors 1–3 and keeps exactly one `lift_floor_N` flag set. |
| `lift-cabin.gs1` | Cabin plate that rides to the floor the panel chose, or says you are already there. |
| `ferry.gs1` | Character NPC that names the fare. Saying "yes" nearby pays and crosses, or says how much is missing. |
| `teleporter-pad.gs1` | Paired in-level pads. A shared one-second cool-down flag stops the player bouncing back. |
| `teleporter-keyed.gs1` | Pad that only works for an owner of the `Warpstone` weapon. |
| `warp-stand.gs1` | Pedestal that says whether the player owns the warp stone. |
