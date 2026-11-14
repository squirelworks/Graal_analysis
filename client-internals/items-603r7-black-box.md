# 6.03r7 item keys and item drawing, measured from the wire and the screen

Date: 2026-11-13 to 2026-11-14. Black-box lab only: nothing was disassembled. The real Linux 6.03r7
x64 client (`G3D0511C`) in a headless Debian lab VM, in a network namespace that reaches only the
loopback address, with the same login-server → world-server setup as
[hud-603r7-black-box.md](hud-603r7-black-box.md). The world level is plain grass with test objects
written into the board (bush, pot, rock, sign with a `SIGN` record, `CHEST … greenrupee`), no NPCs
and no scripts. Account: sword 1, glove 1, shield 1, 5 bombs, 10 arrows, 3 hearts. Server options
`bushitems = true`, `vasesdrop = true`, `respawntime = 15`. Keys were sent with `xdotool`; frames
were captured every 45–55 ms (one client tick is about 50 ms). Times in the second round were
measured with the VM idle; the first round's times were approximate and are not used here.
**[lab][cap][shot]**

"PTL" below is the player's top-left (the gani origin). Sprite rects are in `sprites.png`
(x, y, w, h). Logs, frames and scripts are owner-held. For the 2.x rules see
[carry-hide-and-glove.md](carry-hide-and-glove.md), [laying-items-and-hiding.md](laying-items-and-hiding.md)
and [board-respawn.md](board-respawn.md).

## Packets the keys produce

- **C→S 2** carries prop 10 GANI, 17 SPRITE (0 up, 1 left, 2 down, 3 right), 18 STATUS, 19
  CARRYSPRITE (−1 none) and 78/79 X2/Y2. **[cap]**
- **C→S 157** (`UPDATEGANI`) is sent twice, about 50 ms apart, the first time the client uses each
  gani. The server answers each with S→C 195 naming the gani's `SETBACKTO`: `sword` → idle, `lift` →
  carrystill; `walk`, `push` and `carrystill` have none. **[cap]**
- Every 5 s the server sends 42 (world time) and the client answers with 24 about 0.3–0.5 s later.
  **[cap]**

## S (sword)

| Situation | What happens | Tag |
| --- | --- | --- |
| open grass, any facing | `GANI sword` with the SPRITE, then `idle` **0.25 s** later. Nothing else: no hit packet, no board change. The first swing of a session waits for the `sword.gani` download (the player is not drawn for about 150 ms) | [cap][shot] |
| S held for 2 s | one swing only; holding does not repeat and shows no spin charge (the account has none) | [cap][shot] |
| facing a bush | `1 BOARDMODIFY` to the cut-stump tiles (677, 678 / 693, 694, the "left" tiles of the 2.22 table) in the same millisecond as the gani. The server put the bush back with S→C 7 about 15.4 s later | [cap] |
| facing a sign or an open chest | a plain swing; nothing opens | [cap] |

**Bush leaves.** Four leaves, using (44, 0, 15, 16) and (60, 0, 16, 16) swapped per tick, appear
0.21 s after the key and drift down and out for 6 ticks (gone at +0.50 s). With `bushitems` the
server dropped nothing on one cut and answered another with `ITEMADD` (a green gralat), as a random
drop would; the gralat (0, 144, 16, 28), with a second
frame (0, 136, 16, 36), bounces from PTL + (24, 9) to rest at PTL + (24, 46) in about 1 s, with its
shadow (65, 162, 14, 7). **[cap][shot]**

## A (lift, throw, grab) with glove 1

| Situation | Wire | Screen |
| --- | --- | --- |
| bush, pot or sign | `1 BOARDMODIFY` (to the "left" tiles: bush 677…, pot 1770…, sign 1802…) and `GANI lift CARRYSPRITE -1` within 22 ms; `CARRYSPRITE` 1 (bush), 5 (pot) or 7 (sign) at +0.29–0.31 s; `carrystill` at +0.38–0.41 s | the object stays at the tile for 3–4 ticks, then rises in about 4 ticks to its carried place at about +0.44 s |
| pot lifted | the server answered the board change with `ITEMADD` (a heart, from `vasesdrop`) at the pot's spot; the client sent `ITEMDEL` when it timed out unpicked | the heart shows on the emptied tile |
| **sign** | lifted like a bush; **no sign text opens**. The server restored it about 15.7 s later | |
| A again while carrying (throw) | `11 THROWCARRIED` (empty body) and `GANI idle CARRYSPRITE -1` in the same millisecond. **No throw gani, and nothing is sent for the landing** | flight and break below |
| rock (too heavy at glove 1) | `GANI grab` on the press, which stays; only SPRITE on release; with Up held, `GANI pull`. No board change | the grab or pull pose stays on screen after the keys are released, until the next move |

**Carried object.** A 32 × 32 cell of `sprites.png` at **PTL + (8, −22)** in every facing (the gani
`carry` / `carrystill` item sprite): bush cell (0, 338), sign (32, 338), pot (64, 338). Walking with
a load uses gani `carry`, and the item bobs with the head at base, −2 and −4 px. Standing objects
on the board are drawn from the same cells. **[shot]**

**Flight.** 8 ticks of 16 px, **128 px (8 tiles)** in the facing direction from the carried place.
The item drops 3 px per tick (1 on the first). The shadow (0, 0, 24, 12) runs on the ground at
PTL + 34, 16 px per tick, hidden behind the player for the first tick or two. The first moved frame
is about 50 ms after THROWCARRIED and the break frame at +0.42–0.45 s. **[shot]**

**Break.** Four pieces, each a quadrant of a 32 × 32 cluster, moving ±4 px per tick diagonally
outward. **[shot]**

| Object | Pieces | Flip | Lifetime |
| --- | --- | --- | --- |
| sign | (56..88, 82..110), 16 × 14 quadrants | left and right halves swap every tick | 4 ticks |
| pot | (24..56, 82..114), 16 × 16 quadrants | every tick | 4 ticks |
| bush | the two leaf images | about every 2 ticks, out of phase | 6 ticks (about 0.3 s) |

Nothing on the wire marks the break, and the server does nothing after it. **[cap]**

## Signs and chests

- **Sign.** Walking or pushing into a sign from below opens nothing, though the server sent both
  `LEVELSIGN` records. Pushing plays `push` after about 0.85 s and sends 38 (TRIGGERACTION
  `pushed`) once a second, with the probe point in front of the body. With no script the 6.03r7
  client has **no built-in sign reader**; A then lifts the sign. **[cap][shot]**
- **Chest.** It opens **on contact, with no key**: in the tick the walk is blocked the client sends
  20 (OPENCHEST); the server answers PLO 9 gralats and PLO 4 (chest now open). The green gralat
  (0, 144, 16, 28) shows one tile above the chest, centred, without moving, and the client sends
  13 (ITEMDEL) about 1.2–1.35 s later. The HUD count goes up by one. A on an open chest does
  nothing. **[cap][shot]**
- **The chest itself is not drawn**: only grass shows at its spot, open or closed, though it blocks
  and opens. In 2.x the client draws the chest tiles itself; 6.03r7 seems to need them in the board
  or a file this server did not send. **[shot][inf]**

## D, Q, Tab and Esc

All four toggle the same state, STATUS bit 0x01 (the pause / menu bit). While it is set the client
draws only a 10 × 15 orange rectangle at (58, 112). With no server GUI images or scripts this is
most likely a weapon or menu window drawn without its skin. D did not place a bomb or show a
D-slot icon. **[cap][shot][inf]**

## Walking into objects

Bush, pot, rock and sign all block: walking down stops with the body's bottom edge on the object's
top row, and after about 0.85–1.0 s the gani becomes `push`. No board change is sent. The client
never asked for `arrays.dat`, so the 6.x tile tables are built in; every cut and lift wrote the
same tiles as the 2.22 tables. The walk sends one X2/Y2 update every 50 ms, 0.5 tile per step.
**[cap]**

## Open

- Where the 6.x chest art comes from.
- Whether a GUI skin from the server turns the orange rectangle into a weapon window.
