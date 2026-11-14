# Laying items and hiding under a carried object (2.05, 2.22, 3.04, 3.153)

Date: 2026-11-14. Static read only; no lab run yet.

The "lay-down mode" in `decomp-findings-2026-10-28/01-sword-while-carrying.md` is two different things that the old notes ran together:

1. **D while carrying** a bush, a light stone, a black stone or an NPC is **hiding** (mode 14), already described for 2.05 in `carry-hide-and-glove.md`. Nothing is put down.
2. **Laying an item** (putting a rupee, bombs, a heart, a sword and so on on the floor) is **S held + A**, a separate mode 9. The 1.21 readme names it: "Laying Items: Select Item: hold Attack Button (S) + press Action Button (A); Lay Item: Action Button (A)". This is how a player drops a rupee.

Both work the same way in 2.05, 2.22, 3.04 (Linux) and 3.153 (Mac). 3.x adds one gate: the `enablefeatures` flags.

Tags: **[2.05]** read in the 2.05 rev 2 binary · **[2.22]** / **[3.153]** the same tables found in that binary · **[3.04]** read in the unpacked 3.04 Linux binary · **[doc]** readme · **[inf]** inferred.

## Keys

The game keys are A (action), S (sword) and D (weapon); the 3.x key binds send `doA`, `doS`, `doD` to the 2D game **[3.04]**.

| State | A | S | D |
|---|---|---|---|
| Empty hands, S not held | grab or lift | swing | fire the selected weapon |
| Empty hands, **S held** | **pick an item to lay** (enters mode 9) | – | **select the next weapon** |
| Carrying | throw | throw | **hide** if the carried thing allows it, else nothing |
| Hidden (mode 14) | come out | throw | come out |
| Laying (mode 9) | with S held: next item; alone: **lay** | leave mode 9 | leave mode 9 |

## Hiding (D while carrying)

Same in 2.05 and 3.04 **[2.05][3.04]**; the hide table is in 2.22 and 3.153 too **[2.22][3.153]**.

- **Enters** when the carry sprite is 261 (bush), 263 (light stone) or 239 (black stone), or when the player carries an NPC (any NPC, no sprite test). A pot (265) or a sign (267): D does nothing.
- **Mode 14**, STATUS bit 0x02. Gani `hiddenstill` standing, `hidden` walking; walking uses a speed factor of 0.2 (0.1 tile per tick, seen live on 2.05; see `carry-hide-and-glove.md`).
- **D again or A** comes out: back to carrying (`carrystill`). If the carried thing is the bush (sprite 261, not an NPC), break effect 0 (the leaves) starts at `(x + 0.5, y + 1)`.
- **S** throws from hiding as from carrying, and the mode goes back to idle.
- The carry sprite prop does not change. Wire: STATUS (0x02) goes out with the normal own-props send; `hiddenstill` is animation step 24, `hidden` steps 25 to 28 on the pre-gani wire.

## Laying items (S held + A)

### Picking

- A with S held, when A has nothing else to do (not carrying, nothing to grab or lift), and the point in front of the player is neither blocking nor water (tile type 11). The test point by facing is `(x + 1.5, y)` north, `(x - 0.5, y + 2)` west, `(x + 1.5, y + 4)` south, `(x + 3.5, y + 2)` east **[2.05][2.22][3.153]**.
- **3.x only:** also needs `enablefeatures` bit 0x10 **[3.04]**. The flags start at 0xFFFF (all on) and reset to that with the player, so this only matters when a script turns it off. `enablefeatures` exists from 2.17.1 (`version-profiles/141-217.toml` lists "S+A"), so 2.22 likely has the same gate **[inf]**; 2.05 has no such flag.
- The first item the player has, in the **lay order**, is picked. None: nothing happens.
- The player enters **mode 9** with the `idle` gani (in 3.x the replaceable `idle` slot, so a `replaceani` of idle applies), and `item2.wav` plays at `(x + 1.5, y + 2)`.

**Lay order** (item numbers, `feature-specs/03-inventory.md` table): 0, 1, 2, 19, 3, 4, 5, 6, 16, 8, 12, 23, 7, 20, 21, 22, 9, 15, 17, 10, 13, 18, 14, 24. Identical in 2.05, 2.22 and 3.153; 3.04 walks a list built from it **[2.05][2.22][3.153][3.04]**. The heart container (11) is not in it.

### In mode 9

- **A with S held** picks the next item the player has, after the current one and wrapping round, and plays `item2.wav`.
- **A alone lays** the item (below) and goes back to mode 0.
- **Any other game key** (an arrow, S, D) goes back to mode 0 and idle without laying.
- **Drawn:** the picked item's sprite above the head, centred on `(x + 1.5, y)`, one tile higher on a horse. 3.x draws it only while `enablefeatures` 0x10 is on and hides the AP/status line over the head meanwhile **[3.04]**.

### What can be laid and what it costs **[2.05]**

| Item | Can lay when | Taken from the player |
|---|---|---|
| green / blue / red / gold rupee (0, 1, 2, 19) | rupees ≥ 1 / 5 / 30 / 100 | that many rupees |
| bombs (3), darts (4) | count ≥ 5 | 5 |
| heart (5) | hearts ≥ 1.5 | one heart |
| glove1 (6), glove2 (16) | glove power 2 / 3 | glove power drops to 1 / 2 |
| sword (10), battleaxe (13), lizardsword (18), goldensword (14) | sword power 1 / 2 / 3 / 4 with the stock image | sword power drops to 0 / 1 / 2 / 3 |
| shield (9), mirrorshield (15), lizardshield (17) | shield power 1 / 2 / 3 with the stock image | shield power drops to 0 / 1 / 2 |
| spinattack (24) | the spin is allowed | the spin |
| 7, 8, 11, 12, 20 to 23 | never | – |

A custom sword or shield image can be laid as item 10 or 9 at any power; the floor item then carries the picture **[2.05]**. 3.04 does the same when it creates the item (it copies the player's own sword or shield image) **[3.04]**.

### Laying

- The cost is checked again; if the player no longer has the item, nothing is laid.
- The item is added at `(x + 0.5 + dx, y + 1 + dy)`, with `(dx, dy)` by facing north `(0, -3)`, west `(-2, 0)`, south `(0, 2)`, east `(2, 0)` **[2.05][2.22][3.153]**, with **life 164** and the announce flag; then the cost is taken; then `item.wav` at `(x + 1.5, y + 2)`.
- From there it is an ordinary floor item (`item-drops.md`): it loses one life per 50 ms tick, cannot be picked up for the first four ticks (life ≥ 160), fires `playerlaysitem` at life 140 (1.2 s after laying), blinks below 37 and goes at 0 (8.2 s), sending `PLI_ITEMDEL` (13) online.

### Wire

- When an announced item is added online, the client sends **`PLI_ITEMADD` (12)**: `GCHAR round(x × 2)`, `GCHAR round(y × 2)`, `GCHAR item` (each byte + 32) **[2.05][3.04]**, and UDP 19 to peers in builds that still have UDP **[2.05]**.
- **Only floor items are sent**: 0 to 5, 7, 8, 19, 24 (the 25-entry floor table, identical in 2.05, 2.22 and 3.153) **[2.05][2.22][3.153]**; 3.04 checks the same table before the send **[3.04]**. A laid glove, sword, shield or spin stays local: other players never see it, and picking it up again sends nothing (it is applied locally), but its timeout still sends `PLI_ITEMDEL`.
- The server relays `PLO_ITEMADD` (22) to the others (`protocol/packet-layouts.md`).
- The taken counts (rupees, bombs, darts, hearts, sword or shield power) change the player's own props, which go out with the client's normal own-props send **[inf]**: not captured.
- In 3.04 the packet id is passed through an indirect call, so 12 is read from the 2.05 path and the identical 3.04 sibling for pickup (which sends 20 and 32) **[3.04][inf]**.

## S held + D: next weapon

With S held and empty hands, D selects the next weapon (the one after the selected, wrapping) instead of firing **[3.04]**. 3.x needs `enablefeatures` bit 0x20 ("S+D"). Not read in 2.05.

## Open

- [ ] A lab run on 2.05 rev 2 and 2.22 (hold S, press A, A) to capture the `PLI_ITEMADD` bytes and see which props follow.
- [ ] Whether 2.22's lay and S+D paths check `enablefeatures` (2.22 has the command; the check was read in 3.04 only).
- [ ] 3.04's cost table was not read line by line; its pick, lay and send paths match 2.05's, and its tables match 2.22 and 3.153.
