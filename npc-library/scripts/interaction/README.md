# Interaction: switches, flags, scenery, breakables, seats

Part of the [original NPC library](../README.md). Covers the `interaction / flags`, `interaction / triggers` and `interaction / visibility` categories of [`behaviours.md`](../../behaviours.md), the switch-like part of `combat / targets`, and the seats from `dialogue / speech`.

Live puzzles (lever and gate, plate, stepping stones) poll on a short timer with `timereverywhere`, so each player's client sees its own flags change at once. `exploded` is used as "caught in an explosion". The manual lists it as a 2.05 event (§8.1.5) but does not describe it, so that reading is an inference.

| File | What it does |
| --- | --- |
| `lever.gs1` | Pull (touch facing up) or hit to flip a flag. Shows on/off frames. |
| `gate-flag.gs1` | Opens and closes live as a flag changes, optionally inverted. |
| `pressure-plate.gs1` | Held while the player or any NPC (a pushed block) stands on it. |
| `step-sequence.gs1` | Invisible controller for three floor stones that must be stepped on in order. A wrong stone resets. |
| `eye-target.gs1` | Closes only when shot with an arrow, and sets a flag. |
| `flag-stone.gs1` | Marks a quest step, but only while the quest is active. |
| `wardrobe.gs1` | Cycles the player through four outfits. |
| `dye-vat.gs1` | Dyes the player's coat for a fee. |
| `scenery-overhang.gs1` | Non-blocking, drawn over the player (tree crowns, arch tops). |
| `scenery-decal.gs1` | Non-blocking, drawn under the player (rugs, puddles). |
| `breakable-pot.gs1` | Liftable pot that breaks on a throw, a hit or an explosion, and sometimes drops a rupee. |
| `cracked-wall.gs1` | Breaks only to an explosion and stays broken. Sounds hollow to the sword. |
| `seat.gs1` | Seats the player facing down with the `sit` gani, and lets them walk off. |
| `freeze-statue.gs1` | Freezes a player who crosses its line of sight, then rests 3 s. |
