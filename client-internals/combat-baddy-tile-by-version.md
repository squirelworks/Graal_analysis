# Combat, baddy and tile rules by client build, 1.21 to 2.31

Date: 2026-11-13. Static reads of 35 Windows executables: 1.21, 1.28 beta 2, 1.3 test, 1.31 to
1.39, 1.41 rev 1, NewMain 24 and 26 (1.42), every 2.00 to 2.05 revision, the 2.1 tests 2 and 3,
2.17.1, 2.22, 2.31, and NewWorld betas 1 and 2. Each build's baddy, combat and tile code was
compared by its constants, and the units that differed were read in full **[bin]**. One live
check ran a real 1.39 offline under Wine **[live][shot]**. The rules are implemented in
squirelworks/seihai-core PRs #28 and #34 (releases 0.0.19 and 0.0.20) **[doc]**. No addresses or
decompiled code are reproduced.

Before this pass the notes took baddy AI from 2.05, combat from 1.42 to 2.04, and tile rules
from 2.05 or 2.22, and applied them to every build. This note says where that holds.

## Baddy AI

| Rule | Builds | Tag |
| --- | --- | --- |
| the AI tables (step, look-ahead, turn, rock, shoot position, arrow, aim, power, hare height) | byte-identical in all 33 builds that have the baddy class | [bin] |
| no built-in baddy class | NewWorld betas 1 and 2 | [bin] |
| the AI code | the same from 2.01 to 2.31, matching 2.05 | [bin] |
| swamp soldier (mode 6), the sword's window | 1.21 to 2.00 (every revision, plus 1.41 and NewMain 1.42): hit when its aux value is under 1 and the counter is 17 or more, with no upper bound. From 2.01: counter 22 to 36, the same window the touch and object tests use in every build | [bin] |
| hare window | 17 to 37 in every build | [bin] |
| other 1.28b2 to 1.39 differences | drawing code only (the sprite composer changed) | [bin] |

### 1.x clients roll an item when a baddy dies

From 1.21 to 1.41, each time a baddy enters mode 5 (dying), the client draws a random number
from 0 to 99 and drops an item at the baddy's top-left corner, as a bush does **[bin]**:

| Roll | Item |
| --- | --- |
| under 10 | green rupee |
| under 15 | blue rupee |
| under 30 | heart |
| under 75, and the baddy is type 3, 4 or 9 | darts (arrows) |

1.21 names the item (`greenrupee`, `bluerupee`, `heart`, `darts`); later builds pass an index
(0, 1, 5, 4) **[bin]**. The roll is gone from NewMain 1.42 and 2.0 on, where the server drops
items **[bin]** (→ [item-drops.md](item-drops.md)).

Live check, 1.39: in One Player mode on a level with eight baddies of types 0 to 3, each baddy
was set to the state a final sword hit leaves. Every baddy went to mode 5 and then 9, and items
appeared where some died: two hearts, and darts where an archer (type 3) stood **[live][shot]**.

## Lava and tile rules

| Rule | Builds | Tag |
| --- | --- | --- |
| no lava burn; its mode-38 counter heals +0.5 instead | 1.21 | [bin] |
| lava burn: test point (x + 1.5, y + 2); the count runs past 100, so one cycle is 101 ticks; half a heart per cycle | 1.28 beta 2 to 2.31 | [bin] |
| which test finds lava | a dedicated lava list in 1.28b2 to 2.03; the generic tile-type test with type 12 from 2.04; same behaviour | [bin] |

## The sword box (the victim judging another player's swing)

| Rule | Builds | Tag |
| --- | --- | --- |
| sideways reach | `\|side\| <= 2` tiles, **edge included**: a target exactly 2 tiles to the side is hit | every build, 1.21 to 2.31 [bin] |
| forward reach | 0 to 4 tiles inclusive | every build [bin] |
| hurt | mode 3 for 40 ticks | every build [bin] |
| swing gate | sprite 6 to 10 directly in 1.21 to 1.33 (1.33 polls the judge every tick); animation step 9 to 13 from 1.34, which is equivalent | [bin] |
| player mode 7 | 1.34 to 1.41 pass over a victim in player mode 7; what mode 7 is was not identified | [bin] |

The earlier reading in → [combat-200-204.md](combat-200-204.md) and manual §4.3.3 treated exactly
2 tiles to the side as a miss; that was wrong for every build.

## Sword judge gates

| Gate | Builds | Tag |
| --- | --- | --- |
| no AP immunity | 1.21 to 1.33 | [bin] |
| AP 100 immunity | from 1.34 | [bin] |
| attacker check | one hidden-flag byte in 1.34; the status bits 2 and 32 from 1.39 | [bin] |
| one more victim test | 2.17.1, 2.22, 2.31; not identified | [bin] |

## Sword power

The ±20 limit on the stored sword power is absent in 1.39, 1.41, NewMain 1.42 and 2.00 to 2.02,
and present from 2.03. So 1.x stores the power as the raw 6 bits it receives **[bin]**.

## Hits by packet (ids 40 and 46)

The handler is the same in 2.03, 2.05, the 2.1 test 3, 2.17.1, 2.22 and 2.31: 10-tile range, a
cap of 1 heart, and the AP 100 check **[bin]**. 2.00 was read earlier (→ [damage-sources.md](damage-sources.md)).
No handler for id 40 was found in any 1.x build, so a 1.x client is taken not to apply hits by
packet **[bin][inf]**.

## Death

The dead-bit threshold of 28 and the death timer cap of 30 hold in every build **[bin]**. The
respawn AP bands were found only in 2.x; 1.39 respawns to full hearts with no AP bands **[bin]**.

## The sword-clash spark

When the local player's sword meets a baddy's sword, the client draws a spark on the sword for
five 50 ms player ticks, one piece of `arrays.dat` array 21 per tick, picked by the player's
facing and the frame. Every build from 1.28 beta 2 to 2.31 does the same **[bin]**. Not yet
watched in the running game.

## Summary of rule groups

| Group | Builds | Combat | World |
| --- | --- | --- | --- |
| 1.21 | 1.21 | no AP immunity, raw sword power, no packet hits | no lava burn; swamp sword from counter 17 |
| 1.28b2–1.33 | 1.28 beta 2 to 1.33 | as 1.21 | lava burns; swamp sword from 17 |
| 1.34–1.41 | 1.34 to 1.41 rev 1 | AP 100 immunity, raw power, no packet hits, mode 7 skipped | as above |
| 1.42 | NewMain 1.42 | the 2.00 judge; no packet hits traced | as above; no client item roll |
| 2.00 | 2.00 to 2.00 r3 | the 2.00 judge | as above |
| 2.01 on | 2.01 to 2.31 | ±20 power limit from 2.03; packet hits | swamp sword 22 to 36 |

## Not known

- The 1.x handler for hit packet 40, if any.
- Player mode 7 in 1.34 to 1.41.
- The extra victim test in 2.17.1, 2.22 and 2.31.
- The respawn AP bands before 2.x.
- Not run live: the 2-tile sideways edge (needs two players), a 2.05 control (expected: no
  client item drops), anything on 1.21, and the sword spark.
