# Item drops from bushes, pots and stones, per client version

Date: 2026-10-30

What a cut or lifted bush, a lifted pot and a stone leave, who rolls it, and what the client sends about items on the floor. Covers every build from the 4th alpha to 2.31, read in the binaries and checked in the lab with real 1.39, 2.05 rev 2 and 2.22 clients. This corrects parts of `board-respawn.md` (see the end).

Tags: **[bin]** read from the binary · **[live]** seen in the lab with the real client under Wine · **[cap]** read from a lab capture · **[src]** GServer-v2 source · **[doc]** `newfeatures*.txt` · **[inf]** inferred.

The captures, their decoded message lists and screenshots are in the project files under `graal-decompile/live-trace/item-drops/`.

## Summary

| Builds | Who drops | What the client sends |
|---|---|---|
| 4th alpha to 1.37 | The client rolls **[bin]** | Roll: UDP 19 to the other players only. Pickup: applied locally, UDP 20 and TCP `PLI_ITEMDEL` (13). Timeout: nothing **[bin]** |
| 1.38 to 1.41 | The client rolls **[bin]** | Roll: UDP 19 and TCP `PLI_ITEMADD` (12). Pickup online: `PLI_ITEMTAKE` (32), and the server gives the item with props. Timeout online: `PLI_ITEMDEL` (13) **[bin][cap]** for 1.39; 1.41 read for the roll only |
| 1.42 (NewMain) to 2.31 | The server (`PLO_ITEMADD`, 22). Offline nothing drops **[bin][doc]** | Pickup: `PLI_ITEMTAKE` (32). Timeout: `PLI_ITEMDEL` (13) **[bin][cap]** |

- **The change is at 1.42, not 2.00.** NewMain 1.42's `newfeatures142.txt` says "bush rupees and pot hearts are server-side", and the roll is gone from NewMain 24 and 26 **[doc][bin]**. 1.41 (graal_gr1411) still has it **[bin]**.
- **No client ever rolls arrows**, and no client drops anything for a stone **[bin]**. Arrows from a bush come only from a server that has them in its table (GServer-v2: `rand() % 6` includes darts **[src]**).
- **Stones.** The only client path that touches a stone is the bomb blast, which destroys a sign, pot or stone and gives a heart only for the pot **[bin]**. "Something with rocks" is most likely bombs breaking them.

## The 1.x roll **[bin]**

One `Random(100)` per drop, with Delphi's `Random` (`seed = seed * 0x08088405 + 1`, result `(seed * range) >> 32`):

| Roll | Item |
|---|---|
| 0 to 24 | green rupee (25 %) |
| 25, 26 | blue rupee (2 %) |
| 27 to 31 | heart (5 %) |
| 32 to 36 | bombs (5 %) |
| 37 to 99 | nothing (63 %) |

- The same table is in every build from the 4th alpha to 1.41. From 1.38 the code picks the item by its number in the item table (0, 1, 5, 3) instead of by name.
- **Sword cut:** every entry of the cut table rolls, tall grass too (1.3 and 1.41 read). `board-respawn.md` said bush only.
- **Lift:** lift entry 0 (bush) rolls; entry 2 (pot) always leaves a heart; sign and stones leave nothing.
- **Bomb blast** (`TAdventureExplosion`, four test points): cut entry 0 rolls; lift entries 1 to 3 (sign, pot, stone) are destroyed, and the pot leaves a heart.
- The item lies at the object's top-left tile (1.39 capture: the bush at 31, 34 sent `^d `).
- A new item gets life 164 and the "announce" flag.
- `bushitems` in GServer-v2 beta4's `serveroptions.txt` says the same thing from the server side: "If making a 1.41 server, set bushitems, vasesdrop, and baddyitems to false as the 1.41 client generates items."

## Items on the floor (2.05 rev 2) **[bin]**

The item object (`TAdventureExtra`) and the level's item tick:

- **Life.** Every 50 ms tick the life goes down by 1, from 164. Below 0 the item goes; online the client sends `PLI_ITEMDEL`. Lab: 8.20 s from the drop to the 13 **[cap]**.
- **Pickup** when all hold: the item is not permanent (life below 100 at creation, such as a chest's display item with life 24), the life is below 160 (so not in the first four ticks), and `|px + 1.5 - (ix + 1)| < 2` and `|py + 2 - (iy + 1)| < 2`.
- At life 140 the `playerlaysitem` event fires.
- **Blink:** not drawn while the life is below 37 and odd.
- **Bounce:** raised by `|sin(life / 3)| · (life / 164)^16 · 3` tiles while the life is at least `164 - 7π`.
- **Draw:** the shadow, sprite 42, at `(x + 0.5, y + 1 + h / 2 - 0.5)` for an item `h` tiles high; the item centred on `(x + 1, y + 1)`.
- **Sprites by item number:** 136, 137, 138, 67, 143, 139, 145, 351, 65, 350, 314, 315, 321, 323, 322, 324, 325, 328, 329, 330, 331, 332, 333, 334, 349.
- **Floor items** (the announce flag; `PLO_ITEMADD` makes an item only for these): 0 to 5, 7, 8, 19 and 24 (rupees, bombs, darts, heart, bow, bomb, gold rupee, spin attack).
- **What a pickup gives offline:** green 1, blue 5, red 30, gold 100 rupees (up to 9,999,999); bombs and darts 5 each (up to 99); a heart one whole heart. Sound `extra.wav` (1.3 and 1.39: `sounds\extra.wav`).

1.3 differs **[bin]**: the pickup test is an overlap of pixel boxes, and a timeout is silent. Whether 1.3's life count stops behind a flag (offset 0x74) was not settled.

## Lab runs **[live][cap]**

| Client and server | What happened |
|---|---|
| 2.05 rev 2, old lab pack (2.05 in the 2.1 slot, `tiledroprate` 100) | Cut: C>S 1, then S>C 7 and S>C 22 `^d"` (red rupee at 31, 34). Left alone: C>S 13 `^d` 8.20 s later. Picked up: C>S 32 `^d!`, then S>C 9 RUPEESCOUNT 5, and the HUD showed 5. A lifted pot: S>C 22 heart |
| 2.22, beta4 | The same: 22, then 13 after about 8.7 s; pickup 32, then props 9 |
| 2.05 rev 2, beta4 | No drops: beta4 counts 2.05 as `CLVER_2_052`, below 2.1, and GServer-v2 gives no drops below 2.1 **[src]** |
| 1.39, beta4 (`generation = classic`) | The client rolled: C>S 1, then C>S 12 `^d ` in the same frame. Picked up: C>S 32 `^d `. The server did not echo 22 to the sender. Four of the next five cuts dropped nothing |

## Seihai against the same servers (2026-10-30) **[cap]**

- **2.05:** cut, S>C 22 bombs, drawn with its shadow and bounce; C>S 13 8.39 s later. A heart: picked up after 1.09 s with C>S 32, S>C 9 CURPOWER.
- **1.39:** lift, C>S 1 and C>S 12 `^\x82 ` (green rupee) in the same frame; C>S 32 on pickup; S>C 9 RUPEESCOUNT, and the HUD count went up.

## Corrections to `board-respawn.md`

- Drops became server-side at **1.42**, not 2.00.
- The 1.x cut roll is for every cut entry, not the bush alone.
- From 1.38 the roll also goes to the server (`PLI_ITEMADD`), not only to peers.
- The drop tables of 1.39 to 1.41 were read: the same as 1.3.

## Open

- 1.41's pickup and timeout path is assumed to be 1.39's.
- 1.x pickup box in tiles (only 1.3's pixel overlap was read).
- Whether items are drawn under or over players (Seihai draws them under, inferred).
