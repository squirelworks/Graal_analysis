# Minigames

Part of the [original NPC library](../README.md). No single category of [`behaviours.md`](../../behaviours.md) holds minigames, but the archived catalogue counts 59 (manual §8.1.10). These are built from the same parts as the other families: timers, flags, strings and rupees.

Every game runs its clock with `timereverywhere`, so it works for a player who is not the level leader. Scores and records that must outlast the visit are kept in player strings (`setstring`) and read back with `strtofloat(#s(...))`.

| File | What it does |
| --- | --- |
| `race-start.gs1` | Start post: touch to start a clock in tenths of a second. It keeps the best time in `race_best` and pays for a record. |
| `race-finish.gs1` | Finish line: stops the clock by swapping `race_running` for `race_finished`. |
| `target-range.gs1` | Paid 30 s round. The target hops between five spots, and arrow hits score and pay out. |
| `whack-a-mole.gs1` | 20 moles across six holes, getting faster. Sword hits pay, with a bonus for a perfect round. |
| `coin-toss.gs1` | Dealer: say "heads" or "tails" to bet, with a pause before the result. Pays double. |
| `three-chests.gs1` | Three copies of one script. Pick a chest for 5 rupees, and all of them open to show where the prize was. |
