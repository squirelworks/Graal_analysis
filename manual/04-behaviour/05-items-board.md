<!-- manual: kind=reference status=draft -->
# 4.5 Items, drops and board respawn

This chapter gives the client's side of lifting, carrying, hiding and throwing, the sword cut, chests, items on the floor, who rolls item drops in each build, and what the client does (and does not do) about board respawn. The `arrays.dat` tables named here are defined in → §3.5.3; the server's respawn timers and drop tables are in → §5.

> Status: draft. Read for 1.3, 1.38 to 1.41 and 2.05 rev 2; lab-checked on 1.39, 2.05 rev 2 and 2.22. Open points are App. E#316 to E#318.

## 4.5.1 Matching a 2 × 2 object

Cutting and lifting both work by matching a 2 × 2 object in the board. The rules below give the match, the probe, a change made in 2.04 and how the result is written [2.05] (client-internals/decomp-findings-2026-10-25-l/03-cut-lift-chest.md#matching-a-2-x-2-object).

| Rule | Detail | Source |
| --- | --- | --- |
| match | take the tile under the probe point; for each table entry in order, for each of its four tiles equal to that tile, the object's top-left is the point minus that tile's column and row; the four board tiles there must equal the entry's four, all on the board; the first full match wins | [2.05] (client-internals/decomp-findings-2026-10-25-l/03-cut-lift-chest.md#matching-a-2-x-2-object) |
| probe | one tile beyond the middle of the leading edge (→ §4.3.2) | [2.05] (client-internals/decomp-findings-2026-10-25-l/01-walking-body-box.md#other-probes-same-routine-family) |
| 2.04 change | from 2.04 the whole 2 × 2 must match before anything happens; 1.3 matched only the single tile under the probe and wrote the leftover block at the derived corner | [bin][doc] (client-internals/board-respawn.md#sending-the-change) |
| writing | cut and lift share one routine: it writes the leftover tiles, then, only online, sends `PLI_BOARDMODIFY` (1) with the 2 × 2; nothing is sent if the tiles were already equal | [2.05] (client-internals/board-respawn.md#sending-the-change) |
| Windows 4.04r2, static | the attack-linked tile edit requires a complete two-by-two pattern; its first pattern and replacement also occur in pickup, whose category is tested by the bush property; no successful cut was captured | [bin] (client-internals/404r2-carry-state.md#board-matching) |

The objects (`arrays.dat`; the same in 1.21, 1.3 test and the 2.22 install, one index lower in 1.21):

| Table | # | Object | Tiles (top row / bottom row) | Leaves | Carry sprite | Source |
| --- | --- | --- | --- | --- | --- | --- |
| cut | 0 | bush | 2 3 / 18 19 | 677 678 / 693 694 | n/a | [bin] (client-internals/board-respawn.md#the-objects) |
| cut | 1 | tall grass | 420 421 / 436 437 | 679 680 / 695 696 | n/a | [bin] (client-internals/board-respawn.md#the-objects) |
| lift | 0 | bush | 2 3 / 18 19 | 677 678 / 693 694 | 261 | [bin] (client-internals/board-respawn.md#the-objects); [2.05] (client-internals/carry-hide-and-glove.md#glove-power-and-the-lift-table) |
| lift | 1 | sign | 512 513 / 528 529 | 1802 1803 / 1818 1819 | 267 | [bin] (client-internals/board-respawn.md#the-objects); [2.05] (client-internals/carry-hide-and-glove.md#glove-power-and-the-lift-table) |
| lift | 2 | pot (`vase`) | 684 685 / 700 701 | 1770 1771 / 1786 1787 | 265 | [bin] (client-internals/board-respawn.md#the-objects); [2.05] (client-internals/carry-hide-and-glove.md#glove-power-and-the-lift-table) |
| lift | 3 | light stone | 34 35 / 50 51 | 1834 1835 / 1850 1851 | 263 | [bin] (client-internals/board-respawn.md#the-objects); [2.05] (client-internals/carry-hide-and-glove.md#glove-power-and-the-lift-table) |
| lift | 4 | black stone | 990 991 / 1006 1007 | 1834 1835 / 1850 1851 | 239 | [bin] (client-internals/board-respawn.md#the-objects); [2.05] (client-internals/carry-hide-and-glove.md#glove-power-and-the-lift-table) |

## 4.5.2 Lift, carry, hide and throw

The A key lifts, carries and throws. The rules below give the key order, the glove rule, NPCs that can be carried, and the timing of a lift [2.05] (client-internals/ledges-push-pull.md#grabbing-and-pulling).

| Rule | Detail | Source |
| --- | --- | --- |
| A key order | throw what is carried; else lift; else grab (→ §4.2.8) | [2.05] (client-internals/ledges-push-pull.md#grabbing-and-pulling) |
| glove | glove power `g` allows the first `g + 2` lift entries; every player starts at glove 1 (bush, sign, pot); `glove1` raises it to at least 2 (light stone), `glove2` to at least 3 (black stone); online the power is player prop 6; the cut-and-lift note words the steps differently: `disputed → App. E#316` | [2.05] (client-internals/carry-hide-and-glove.md#glove-power-and-the-lift-table); [2.05] (client-internals/decomp-findings-2026-10-25-l/03-cut-lift-chest.md#lift-a-key) |
| NPCs | an NPC is lifted only when its script set `canbecarried` (command 41, cleared by 42), at the same point, with no glove check; it leaves the level's NPC list and nothing is sent | [2.05] (client-internals/carry-hide-and-glove.md#glove-power-and-the-lift-table) |
| lift | `lift` plays at once and the board tile becomes its leftover at once; a counter runs 4 down to 0 and the carried flag is set on the 5th tick; `carrystill` follows on the 7th tick (6 ticks of `lift`) | [live][2.05] (client-internals/player-mannerisms-live.md#lifting-carrying-hiding-and-throwing-live) |
| carry | `carry` (8 frames, one per tick) at the normal 0.5 tile per tick; the object is drawn over the head, the head and arms hidden behind it | [live][2.05] (client-internals/player-mannerisms-live.md#lifting-carrying-hiding-and-throwing-live) |
| carried image | the carried bush is the plain bush sprite, not the board's tiles (a bluish board bush is carried green) | [shot] (live-runs/2gta-222-2026-10-30/README.md#lift-hide-under-it-throw) |
| hide | D while carrying a bush, light stone, black stone or NPC hides the player under it (mode 14); D with a pot or sign does nothing; STATUS gets bit 0x02; the carry sprite prop does not change; only the object is drawn, where the player stands | [2.05] (client-internals/carry-hide-and-glove.md#hiding-mode-14); [live][2.05] (client-internals/player-mannerisms-live.md#lifting-carrying-hiding-and-throwing-live) |
| hidden walk | `hiddenstill` standing, `hidden` walking at 0.1 tile per tick (→ §4.2.1.1); `hidden.gani` is one frame, so the frame does not advance | [live][2.05] (client-internals/player-mannerisms-live.md#lifting-carrying-hiding-and-throwing-live) |
| hidden on the wire | `hiddenstill` is step 24, sprite 18 (as `carrystill`); `hidden` steps 25 to 28, sprites 19, 20, 19, 18 | [2.05] (client-internals/carry-hide-and-glove.md#hiding-mode-14) |
| hits while hidden | the hit gate refuses hits on a hidden player unless a player byte that was not traced is set | [2.05] (client-internals/carry-hide-and-glove.md#hiding-mode-14) |
| leaving | D again, or A, goes back to `carrystill` in the same tick; out from under a bush (not an NPC) the client starts break effect 0 (the leaves) at (x + 0.5, y + 1) | [2.05] (client-internals/carry-hide-and-glove.md#hiding-mode-14) |
| throw | A, or S (also from hiding): `idle` in the same tick, the carried and hidden flags cleared, the carry sprite back to -1 | [live][2.05] (client-internals/player-mannerisms-live.md#lifting-carrying-hiding-and-throwing-live); [2.05] (client-internals/decomp-findings-2026-10-28/01-sword-while-carrying.md) |
| flight | a thrown pot flies about 6 tiles in 9 ticks, its shadow along the ground; it breaks into four pieces that spread over 4 ticks; a landing does not touch the board, it only breaks into leaves (`crush.wav`, or `water.wav` for the water leap) | [live][2.05] (client-internals/player-mannerisms-live.md#lifting-carrying-hiding-and-throwing-live); [bin] (client-internals/board-respawn.md#the-objects) |
| D key while carrying | does not throw; with carry sprite 239, 261 or 263 it hides (above) | [2.05] (client-internals/decomp-findings-2026-10-28/01-sword-while-carrying.md) |
| stone without glove | A at a black stone with glove 1 does nothing: no lift and no grab | [live][2.05] (client-internals/player-mannerisms-live.md#lifting-carrying-hiding-and-throwing-live) |

By build:

| Build | Lift | Hide | Source |
| --- | --- | --- | --- |
| 1.39 | counter 4 to 0, carried on the 5th tick; no lift pose; carried bush id 261 | hidden flag; walk 0.1 per tick | [live][1.39] (client-internals/player-mannerisms-live.md#cross-version-table) |
| 1.41 | `lift` 6 ticks, then `carrystill` | hidden flag, but the pose stays `carrystill` / `carry`, the legs cycling at 0.1 per tick; `hidden.gani` is shipped but not played | [live][1.41] (client-internals/player-mannerisms-live.md#notes-per-build) |
| 2.05 rev 2, 2.22 | as above | `hiddenstill` / `hidden`; D toggles | [live][2.05][2.22] (client-internals/player-mannerisms-live.md#cross-version-table); [shot] (live-runs/2gta-222-2026-10-30/README.md#lift-hide-under-it-throw) |
| Windows 4.04r2, static | static sequence → §4.5.2.1; elapsed duration unmeasured | state relationships → §4.5.2.1; captured behavior unmeasured | [bin] (client-internals/404r2-carry-state.md#pickup-carrying-and-hiding) |
| 5.24r4, 5.30r3, 6.03r7 | `lift` and the board change in the key's tick, `carrystill` 0.30 s later; a throw sends id 11 and `idle` in the same tick | hidden at about 1.5 px per tick; D with a pot does nothing | [wire] (protocol/v5v6-lab-play.md) |

### 4.5.2.1 Windows 4.04r2 static transition limits

Windows 4.04r2 was read statically for the same actions. Each row gives one relationship, what was seen and the limit on what that proves [bin] (client-internals/404r2-carry-state.md#pickup-carrying-and-hiding).

| Relationship | Static observation | Limit | Source |
| --- | --- | --- | --- |
| Pickup | Transitional action and countdown initialization precede a later update setting the carrying flag; the carried category and boolean carrying property read different state | Countdown initial value five does not establish total frames or elapsed duration; glove-bound semantics remain unmeasured | [bin] (client-internals/404r2-carry-state.md#pickup-carrying-and-hiding); [bin] (client-internals/404r2-carry-state.md#timing-and-input-limits) |
| Hiding | Bush and two stone categories, or a carried-object pointer, permit selection of a hiding-related state and animation; its movement branch starts with a smaller magnitude | Physical keys, distance per real-time tick and captured hiding behavior remain unmeasured | [bin] (client-internals/404r2-carry-state.md#pickup-carrying-and-hiding) |
| Release | Creates a level carry entity and clears player carry fields under animation-dependent conditions | Separate exit-helper conditions remain untraced; no universal drop/unhide rule established | [bin] (client-internals/404r2-carry-state.md#pickup-carrying-and-hiding) |

These are static findings, not gameplay confirmation; older and later lab timings remain version-specific. Open questions: → App. E#611. [bin][cap] (client-internals/404r2-carry-state.md#timing-and-input-limits)

### 4.5.2.2 Laying items (S held + A) and S held + D

"Laying an item" is a separate mode 9 entered with S held + A, distinct from hiding (D while carrying, mode 14); the 1.21 readme names it. The rules are the same in 2.05, 2.22, 3.04 Linux and 3.153 Mac [2.05][3.04][doc] (client-internals/laying-items-and-hiding.md#laying-items-and-hiding-under-a-carried-object-205-222-304-3153).

| Rule | Builds | Source |
| --- | --- | --- |
| Hiding: D while carrying a bush (261), light stone (263), black stone (239) or any NPC enters mode 14 (STATUS 0x02); a pot (265) or sign (267) does nothing; D again or A comes out, and a bush starts break effect 0 at `(x + 0.5, y + 1)`; S throws | 2.05, 3.04 (tables in 2.22, 3.153) | [2.05][3.04] (client-internals/laying-items-and-hiding.md#hiding-d-while-carrying) |
| Picking: A with S held, when A has nothing else to do and the point in front is neither blocking nor water; test point `(x + 1.5, y)` north, `(x − 0.5, y + 2)` west, `(x + 1.5, y + 4)` south, `(x + 3.5, y + 2)` east | 2.05, 2.22, 3.153 | [2.05][2.22][3.153] (client-internals/laying-items-and-hiding.md#picking) |
| 3.x also needs `enablefeatures` bit 0x10 (default 0xFFFF); 2.05 has no such flag; whether 2.22 checks it is unread | 3.04 | [3.04][inf] (client-internals/laying-items-and-hiding.md#picking) |
| The first item the player has in the lay order 0, 1, 2, 19, 3, 4, 5, 6, 16, 8, 12, 23, 7, 20, 21, 22, 9, 15, 17, 10, 13, 18, 14, 24 is picked (no heart container 11); the player enters mode 9 with `idle` and `item2.wav` plays at `(x + 1.5, y + 2)` | 2.05, 2.22, 3.153, 3.04 | [2.05][2.22][3.153][3.04] (client-internals/laying-items-and-hiding.md#picking) |
| In mode 9, A with S held picks the next item the player has (wrapping) and plays `item2.wav`; A alone lays it; any other game key leaves mode 9 without laying; the item is drawn above the head at `(x + 1.5, y)`, a tile higher on a horse (3.x: only with bit 0x10, hiding the AP line) | 2.05; 3.04 | [2.05][3.04] (client-internals/laying-items-and-hiding.md#in-mode-9) |
| Cost: rupees 0/1/2/19 need 1/5/30/100 and take that many; bombs 3 and darts 4 need 5 and take 5; heart 5 needs 1.5 hearts and takes one; glove1 6 / glove2 16 need power 2 / 3 and drop it by one; swords 10/13/18/14 need power 1–4 with the stock image, shields 9/15/17 power 1–3, each dropping by one; spinattack 24 takes the spin; 7, 8, 11, 12 and 20–23 never | 2.05 | [2.05] (client-internals/laying-items-and-hiding.md#what-can-be-laid-and-what-it-costs-205) |
| A custom sword or shield image lays as item 10 or 9 at any power and the floor item carries the picture | 2.05, 3.04 | [2.05][3.04] (client-internals/laying-items-and-hiding.md#what-can-be-laid-and-what-it-costs-205) |
| Laying re-checks the cost, then adds the item at `(x + 0.5 + dx, y + 1 + dy)` with `(dx, dy)` north (0, −3), west (−2, 0), south (0, 2), east (2, 0), life 164 and the announce flag, takes the cost and plays `item.wav`; from there it is an ordinary floor item (→ §4.5.6) | 2.05, 2.22, 3.153 | [2.05][2.22][3.153] (client-internals/laying-items-and-hiding.md#laying) |
| Online the client sends `PLI_ITEMADD` (12) `c round(2x)`, `c round(2y)`, `c item` (UDP 19 to peers where UDP exists), only for floor items 0–5, 7, 8, 19 and 24; a laid glove, sword, shield or spin stays local, but its timeout still sends `PLI_ITEMDEL` (13) | 2.05, 3.04 | [2.05][3.04] (client-internals/laying-items-and-hiding.md#wire) |
| S held + D with empty hands selects the next weapon instead of firing; 3.x needs `enablefeatures` bit 0x20 | 3.04 | [3.04] (client-internals/laying-items-and-hiding.md#s-held--d-next-weapon) |
| Open: a lab capture of the 12 bytes and following props on 2.05 and 2.22, the 2.22 `enablefeatures` check, and 3.04's cost table line by line | — | [inf] (client-internals/laying-items-and-hiding.md#open) |

## 4.5.3 Sword cut

A sword swing cuts what is at its tip. The rules below give when that happens, what is left behind and how bombs differ [2.05] (client-internals/decomp-findings-2026-10-25-l/03-cut-lift-chest.md#sword-cut).

| Rule | Detail | Source |
| --- | --- | --- |
| when | at the start of a swing, at the probe point, against the whole cut table with no glove | [2.05] (client-internals/decomp-findings-2026-10-25-l/03-cut-lift-chest.md#sword-cut) |
| effect | the four tiles become the entry's leftover tiles (array 10) through the shared write routine, then the leaves effect; the leaves fly up and out for about 8 ticks | [2.05] (client-internals/decomp-findings-2026-10-25-l/03-cut-lift-chest.md#sword-cut); [live][2.05] (client-internals/player-mannerisms-live.md#sword-live) |
| bombs | "bombs don't destroy half bushes" (2.05) | [doc] (client-internals/board-respawn.md#sending-the-change) |
| bomb blast, 1.x | the blast's four test points cut cut-entry 0 and destroy lift entries 1 to 3 (sign, pot, stone) | [bin] (client-internals/item-drops.md#the-1x-roll-bin) |

## 4.5.4 Chests

Chests are records in the level, not tiles. The rules below give how they look, how they block and how they are opened [2.05] (client-internals/decomp-findings-2026-10-25-l/03-cut-lift-chest.md#chests).

| Rule | Detail | Source |
| --- | --- | --- |
| look | a chest record has no draw code in 2.05: a chest looks like its board tiles; the record adds the open action and a solid 2 × 2 footprint, opened or not | [2.05] (client-internals/decomp-findings-2026-10-25-l/03-cut-lift-chest.md#chests) |
| 2.22 drawing | the full (closed) form of `PLO_LEVELCHEST` (4) is drawn as a closed chest and the short form as an open one, each a 2 × 2 block over the board with no board tile needed | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#part-1-fresh-runs-2026-10-25-22502310-jst-a-chests-real-222-client-labm-lab-plo_levelchest-id-4-injected) |
| solid | a closed chest stops the player when the body probes touch its 2 × 2 box; pushing against it plays `push` | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#part-1-fresh-runs-2026-10-25-22502310-jst-a-chests-real-222-client-labm-lab-plo_levelchest-id-4-injected) |
| opening | only facing up, from below, with the action key; facing down, left or right nothing is sent | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#part-1-fresh-runs-2026-10-25-22502310-jst-a-chests-real-222-client-labm-lab-plo_levelchest-id-4-injected) |
| on opening | at once: asks for `chest.wav`, sends `PLI_OPENCHEST` (20) with the chest's top-left in whole tiles, draws the chest open locally without waiting; about 1.2 s later sends message 13 with the point one tile above the chest | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#part-1-fresh-runs-2026-10-25-22502310-jst-a-chests-real-222-client-labm-lab-plo_levelchest-id-4-injected) |
| sound | `chest.wav`, also when the chest has a sign; no item sound follows | [live][2.05] (client-internals/live-checks-editor-offline-sound.md#sound-205) |
| record bytes | each + 32: opened flag, x, y, and only if not opened the item index and the sign index (→ §3.1) | [2.05] (client-internals/decomp-findings-2026-10-25-l/03-cut-lift-chest.md#chests) |
| the reward | what the server sends back for a known chest is unmeasured | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#part-1-fresh-runs-2026-10-25-22502310-jst-a-chests-real-222-client-labm-lab-plo_levelchest-id-4-injected) |
| 2.05 opening sides | as 2.22: only from below, facing up (6/6; 0/6 from each other side); the chest opens as the player walks into it, without the action key | [lab] (client-internals/lab-cells-200-205-2026-11-13.md#205-rev2-which-sides-open-a-chest) |

## 4.5.5 Item drops: who rolls

Who rolls a dropped item moved from the client to the server at 1.42. Each row gives a group of builds, who drops, and what the client sends [bin] (client-internals/item-drops.md#summary).

| Builds | Who drops | What the client sends | Source |
| --- | --- | --- | --- |
| 4th Graal alpha to 1.37 | the client rolls | the roll as UDP 19 to the other players only; a pickup is applied locally, with UDP 20 and `PLI_ITEMDEL` (13); a timeout sends nothing | [bin] (client-internals/item-drops.md#summary) |
| 1.38 to 1.41 | the client rolls | the roll as UDP 19 and `PLI_ITEMADD` (12); online a pickup sends `PLI_ITEMTAKE` (32) and the server gives the item with props; a timeout sends `PLI_ITEMDEL` (13) (1.39 read and captured; 1.41 read for the roll only) | [bin][cap] (client-internals/item-drops.md#summary) |
| NewMain 1.42 to 2.31 | the server (`PLO_ITEMADD`, 22); offline nothing drops | pickup `PLI_ITEMTAKE` (32); timeout `PLI_ITEMDEL` (13) | [bin][doc] (client-internals/item-drops.md#summary) |

The rules below give the evidence for that change and what follows from it, offline and online [doc][bin] (client-internals/item-drops.md#summary).

| Rule | Detail | Source |
| --- | --- | --- |
| the change | at 1.42: "bush rupees and pot hearts are server-side"; the roll is gone from NewMain 24 and 26 and still in 1.41 | [doc][bin] (client-internals/item-drops.md#summary) |
| arrows and stones | no client ever rolls arrows, and no client drops anything for a stone | [bin] (client-internals/item-drops.md#summary) |
| 2.05 offline | the cut routine makes only the leaves and the lift routine only the carried object, so an offline 2.05 bush or pot gives nothing | [bin] (client-internals/board-respawn.md#item-drops-from-142-on-server-side) |
| server drop timing | on a 2.22 server with pot drops on, the heart arrived in the same frame as the lift, at the pot's spot, and stayed when the pot was thrown | [cap] (live-runs/2gta-222-2026-10-30/README.md#pots) |

### 4.5.5.1 The 1.x roll

One `Random(100)` per drop, with the Delphi generator `seed = seed × 134775813 + 1`, result `(seed × range) >> 32`:

| Roll | Item | Source |
| --- | --- | --- |
| 0 to 24 | green rupee (25 %) | [bin] (client-internals/item-drops.md#the-1x-roll-bin) |
| 25, 26 | blue rupee (2 %) | [bin] (client-internals/item-drops.md#the-1x-roll-bin) |
| 27 to 31 | heart (5 %) | [bin] (client-internals/item-drops.md#the-1x-roll-bin) |
| 32 to 36 | bombs (5 %) | [bin] (client-internals/item-drops.md#the-1x-roll-bin) |
| 37 to 99 | nothing (63 %) | [bin] (client-internals/item-drops.md#the-1x-roll-bin) |

Before 1.42 the client rolled the drop itself. The rules below give the table it used, what rolls, when and where [bin] (client-internals/item-drops.md#the-1x-roll-bin).

| Rule | Detail | Source |
| --- | --- | --- |
| same table | in every build from 4th Graal alpha to 1.41; from 1.38 the item is picked by its number in the item table (0, 1, 5, 3) instead of by name | [bin] (client-internals/item-drops.md#the-1x-roll-bin) |
| what rolls | every cut entry (tall grass too); a lifted bush (lift entry 0); a bush destroyed by a blast; a pot (lift entry 2) always leaves a heart, lifted or blasted; sign and stones nothing | [bin] (client-internals/item-drops.md#the-1x-roll-bin) |
| when | at the lift, not when the thrown pot breaks | [bin] (client-internals/board-respawn.md#item-drops-in-13-client-side) |
| where | at the object's top-left tile | [cap] (client-internals/item-drops.md#the-1x-roll-bin) |
| new item | life 164 and the announce flag | [bin] (client-internals/item-drops.md#the-1x-roll-bin) |
| 1.3 to peers | UDP id 19, `chr(x·2+32) chr(y·2+32) chr(item+32)`, sent straight to each peer, only for item kinds marked in a per-item table; the board change still goes to the server over TCP | [bin] (client-internals/board-respawn.md#item-drops-in-13-client-side) |

## 4.5.6 Items on the floor (2.05 rev 2)

An item on the floor has a life that counts down. The rules below give that life, when it can be picked up, the event it fires and how it blinks [bin][cap] (client-internals/item-drops.md#items-on-the-floor-205-rev-2-bin).

| Rule | Detail | Source |
| --- | --- | --- |
| life | from 164, down 1 per tick; below 0 the item goes and, online, the client sends `PLI_ITEMDEL`; lab: 8.20 s from the drop | [bin][cap] (client-internals/item-drops.md#items-on-the-floor-205-rev-2-bin) |
| pickup | the item is not permanent (life below 100 at creation, such as a chest's display item with life 24), its life is below 160 (not in its first four ticks), and `|px + 1.5 - (ix + 1)| < 2` and `|py + 2 - (iy + 1)| < 2` | [bin] (client-internals/item-drops.md#items-on-the-floor-205-rev-2-bin) |
| event | at life 140 `playerlaysitem` fires | [bin] (client-internals/item-drops.md#items-on-the-floor-205-rev-2-bin) |
| blink | not drawn while the life is below 37 and odd | [bin] (client-internals/item-drops.md#items-on-the-floor-205-rev-2-bin) |
| bounce | raised by `|sin(life / 3)| · (life / 164)^16 · 3` tiles while the life is at least `164 - 7π` | [bin] (client-internals/item-drops.md#items-on-the-floor-205-rev-2-bin) |
| draw | the shadow, sprite 42, at (x + 0.5, y + 1 + h / 2 - 0.5) for an item `h` tiles high; the item centred on (x + 1, y + 1) | [bin] (client-internals/item-drops.md#items-on-the-floor-205-rev-2-bin) |
| sprites by item number | 136, 137, 138, 67, 143, 139, 145, 351, 65, 350, 314, 315, 321, 323, 322, 324, 325, 328, 329, 330, 331, 332, 333, 334, 349 | [bin] (client-internals/item-drops.md#items-on-the-floor-205-rev-2-bin) |
| floor items | `PLO_ITEMADD` makes an item only for the announce-flag items: 0 to 5, 7, 8, 19 and 24 (rupees, bombs, darts, heart, bow, bomb, gold rupee, spin attack) | [bin] (client-internals/item-drops.md#items-on-the-floor-205-rev-2-bin) |
| offline value | green 1, blue 5, red 30, gold 100 rupees (up to 9,999,999); bombs and darts 5 each (up to 99); a heart one whole heart; sound `extra.wav` | [bin] (client-internals/item-drops.md#items-on-the-floor-205-rev-2-bin) |
| online pickup | `PLI_ITEMTAKE` (32) with the item's three bytes; the server answers with props (for example RUPEESCOUNT) | [cap] (client-internals/item-drops.md#lab-runs-livecap) |
| 1.3 | the pickup test is an overlap of pixel boxes, and a timeout is silent | [bin] (client-internals/item-drops.md#items-on-the-floor-205-rev-2-bin) |
| 1.x pickup box in tiles, draw order against players | unmeasured (→ App. E#317) | [bin] (client-internals/item-drops.md#open) |

## 4.5.7 Board respawn on the client

Cut and lifted objects come back only when the server says so. The rules below give how the client handles a restore and what it sends after a push [bin][live] (client-internals/board-respawn.md#no-client-side-respawn).

| Rule | Detail | Source |
| --- | --- | --- |
| no client regrowth | no client regrows a cut or lifted object; the 1.3 and 2.05 board-modify record is built to send one change and has no timer; an offline 2.05 board polled for 633 s after a lift never changed back | [bin][live] (client-internals/board-respawn.md#no-client-side-respawn) |
| restore | a restore arrives as `PLO_BOARDMODIFY` (7) and is handled as any board modify; the timers and the echo rules are the server's (→ §5) | [bin] (client-internals/board-respawn.md#summary) |
| where | the restore puts the object back where it was lifted, since the board changed only at the lift | [bin] (client-internals/board-respawn.md#the-objects) |
| push and pull blocks | the 2.05 client sends the 4 × 4 area round the old spot (→ §4.2.7) | [2.05] (client-internals/ledges-push-pull.md#pushing) |
| re-entry offline | 2.05 rev2 does not reload a level from disk on re-entry: a cut or thrown bush stays gone for the session (3/3; also after loading the level again with F5, 2/2); settled → App. E#318 | [lab] (client-internals/lab-cells-200-205-2026-11-13.md#205-rev2-offline-re-entering-a-level) |
