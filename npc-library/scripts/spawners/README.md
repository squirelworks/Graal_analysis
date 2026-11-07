# Spawners: respawn, spawn, follow, animate

Part of the [original NPC library](../README.md). Covers `spawn / timers` in [`behaviours.md`](../../behaviours.md), and the animated decorations of `misc / other`.

Timers that keep one player's view up to date (regrowing bushes, animations, the day clock, the pet) call `timereverywhere`. Timers that create things for the whole level (dens, hatcheries) leave the level leader in charge, so each object is made once.

| File | What it does |
| --- | --- |
| `respawn-bush.gs1` | Breaks to sword or bomb. Regrows after 8 s, but not on top of the player. It cannot be lifted, because a thrown bush grows back where it landed. |
| `spawner-baddies.gs1` | Den that sends out a frog every 6 s while fewer than 3 baddies live. Can be destroyed. |
| `spawner-npc.gs1` | Hatches an NPC from a script file (`putnpc`) every 10 s, up to 3 per visit. Save `../enemies/bat-swoop.gs1` on the server as `bat-swoop.txt`. |
| `follower.gs1` | Pet that follows the player once found, moving itself (`followplayer` is offline-only). |
| `animation-cycle.gs1` | Steps through a strip of frames (`setimgpart`) on a timer. |
| `day-night.gs1` | A 4 min day, 4 min night clock that sets the `night` flag and tints the screen (`seteffect`). |
| `item-rain.gs1` | Touch the cloud for 10 s of random rupees, then it rests a minute. |
