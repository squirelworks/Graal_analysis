# Baddies in the 2.22 client

Date: 2026-11-04

How the 2.22 client runs the ten built-in baddies: the types and what each one reads from `arrays.dat`, the AI state machine step by step, what blocks and what a baddy can see, sword, shield, projectile and touch damage, drops, sounds, and the baddy messages (who decides what, online). The goal is a serverside script that behaves like the real thing; `server-notes/baddies-serverside.md` is the guide for that, and `server-notes/baddies/graysoldier-222.gs1` is a worked type 0.

Tags: **[2.22]** read in the 2.22 client binary · **[cap]** read from a real 2.22 lab capture · **[srv]** GServer-v2 source · **[doc]** shipped docs and earlier notes · **[inf]** inferred.

Evidence. The rules were read from the 2.22 binary. The step counters, speeds, knockback lengths and the hurt message were then checked against existing captures of the real 2.22 client on a lab server (`lan-222kill-baddy.txt`, `lan-222d-baddyprops.txt` and the two-client hurt run in `lab-baddies-v3.md`, in the project files): `tools/baddy-222/check_capture.py` passes 5,971 checks with no failure (see "Lab check"). No new lab run was made for this note. The 2.05-derived rebuild (`graal-delphi`) was used as a cross-check; the 2.22 differences from it are listed at the end.

## Summary

- **One AI step every 100 ms** (every second 50 ms game tick). Counters below are in steps **[2.22][cap]**.
- **Online, one client thinks for each level: the leader.** It runs the AI and sends the baddy's changed props to the server every step; every other client only draws what the server relays. Every client tests its own player for touch damage and every player it sees swinging a sword **[2.22][cap]**.
- **The server owns three things:** the baddy's id and creation, the switch from dying (mode 5) to dead (mode 9) after 2 s, and the respawn and drops **[srv]**. The 2.22 client drops nothing **[2.22]**.
- **The state machine has 10 modes:** walk 0, look about 1, hunt 2, hurt 3, bumped by a shield 4, dying 5, swamp soldier 6, frog 7, octopus ink 8, dead 9 **[2.22]**.
- **The frog uses the hare image.** Type 5 (`frog` in GS1) draws `baddyhare.png` and plays `frog.wav`. That settles App. E#205 **[2.22][doc]**.
- **BDPROP 6 is the step counter, not an animation frame,** and BDPROP 7 is `dir × 4 + head` (body direction high, head low) **[2.22][cap]**.

## Types **[2.22]**

| Type | GS1 name | Image | Power | Shield | Walk / hunt step (tiles) | Hunts with | Starts in |
| ---: | --- | --- | ---: | :---: | --- | --- | --- |
| 0 | graysoldier | baddygray.png | 2 | yes | 0.25 / 0.5 | melee | walk |
| 1 | bluesoldier | baddyblue.png | 3 | yes | 0.25 / 0.5 | melee | walk |
| 2 | redsoldier | baddyred.png | 4 | yes | 0.25 / 0.5 | melee | walk |
| 3 | shootingsoldier | baddyblue.png + wbow1.png | 3 | no | 0.25 / 0.5 | arrows | walk |
| 4 | swampsoldier | baddygray.png + wbow1.png | 2 | no | does not move | arrows from the swamp | mode 6 |
| 5 | frog | baddyhare.png | 1 | no | jumps | — | mode 7 |
| 6 | octopus | baddyoctopus.png | 1 | no | 0.5 / — | ink | walk |
| 7 | goldenwarrior | baddygold.png | 6 | yes | 0.25 / 0.5 | melee | walk |
| 8 | lizardon | baddylizardon.png | 12 | no | 0.5 / 0.75 | melee | walk |
| 9 | dragon | baddydragon.png | 8 | no | 0.25 / 0.5 | fire (arrow kind 2) | walk |

- "Power" is the hit points at creation. A sword hit takes the swinging player's sword power **[2.22]**.
- A baddy touching the player takes half a heart, or a whole heart for type 7 **[2.22]**.
- The octopus does not hunt and never enters the sight check; it walks and stops to shoot ink. Types 4 to 6 do not talk; the level editor saves empty verses for them **[2.22][doc]**.
- The baddy is a 2 × 2 tile body. Its x, y is the top-left corner; its centre is (x + 1, y + 1). A player's centre is (x + 1.5, y + 2) **[2.22]**.

### Creation **[2.22]**

- Default: mode 0, direction and head down (2), counter `Random(20) + 40`.
- Type 4: mode 6, ani 2. Type 5: mode 7. Type 6: facing right (3), ani 4, counter `Random(10) + 20`.
- Offline only: the frog is moved 4 tiles from its level position in a random direction (one of four cases; two of them both move it right). The first direction faces the player — the opposite of the player's direction — when the player is within 30 tiles (|dx| + |dy|) or for type 1, otherwise up or down toward the player.
- GS1 `putnewcomp` (and `putcomp`): offline the client creates the baddy, and types other than 4 to 6 start in hunt with counter 12; online it sends `PLI_BADDYADD` and the server creates it.

## What it reads from `arrays.dat` **[2.22]**

`arrays.dat` holds 25 integer arrays. Baddies draw from four of them. The values are not reproduced here; `tools/baddy-222/gen_ganis.py` reads them from your own install.

| Array | Used for | Shape |
| ---: | --- | --- |
| 20 | the baddy body | 32 entries, index `ani × 4 + dir`; each entry is a list of sprites, each packed as `sprite << 16 \| dx << 8 \| dy` with dx and dy signed bytes in eighths of a tile from the baddy's x, y |
| 22 | the puff of smoke when a baddy dies | 5 entries of the same packed sprites |
| 23 | the swamp soldier (type 4), in place of array 20 | same shape as array 20 |
| 24 | the sprite rectangles | one value per sprite: `x = v >> 23`, `y = ((v >> 12) & 1023) × 2`, `w = ((v >> 6) & 63) × 2`, `h = (v & 63) × 2` |

Which sheet a sprite comes from:

- sprites 48 to 63, 104 to 106 and 117 to 130: the baddy's own image;
- sprites 111 to 114: `wbow1.png` (types 3 and 4 only);
- every other sprite: `sprites.png`.

Sprites 48 to 51 are the head. The client draws `48 + head` in their place, so the head can face another way than the body.

The ani values are 0 and 1 for walking (the two leg frames), 2 for the bow drawn (types 3, 4, 9), 4 to 7 for the octopus, and 2 or 3 for the archer types while hunting (`(ani & 1) + 2`) **[2.22]**.

### Drawing **[2.22]**

- **Body:** array 20 (array 23 for type 4) at `ani × 4 + dir`.
- **Dying (mode 5):** the body while the counter is above 3, and the puff (array 22, entry `4 − counter div 2`) while the counter is below 10.
- **Hurt blink:** in modes 3 and 4 the hurt flag hides sprites 1 to 106 on odd frames, so only the shadow and the effects stay.
- **Ground:** on some kinds of ground the baddy draws a ground overlay in place of its shadow (which sprite for which ground is not mapped here).

## The AI step **[2.22]**

Every second game tick (100 ms), for every baddy in the current level:

1. **Think** — the mode logic below — runs only offline or on the level's leader.
2. **Touch** — runs on every client, against the local player only (see "Damage").
3. **Animation fixups** on every client: type 3 always draws `ani = (ani & 1) + 2`; type 6 with ani below 2 draws `(ani & 1) + 4`.
4. **Dead:** a baddy in mode 5 whose counter has gone below 0 switches to mode 9. Removing a baddy plays `compudead.wav`. When the last baddy of the current level is gone, the level gets the `compusdied` event.
5. **Verse time** counts down (a verse shows for 20 steps).
6. **Online:** the client compares the 11 props with the last snapshot and sends the ones that changed (`PLI_BADDYPROPS`, 15). Props that came from the server go into the snapshot, so they are not echoed back.

### The counter

Each baddy has one step counter, `c`. It is BDPROP 6 on the wire. Every mode uses it differently **[2.22][cap]**.

### Mode 0: walk **[2.22]**

- **Head and body agree** (head = dir):
  - `c` falls by 1. Every 5th step plays `steps.wav` (not the octopus).
  - When `c` goes below 0: the octopus goes to mode 8 with `c = 13`; any other type goes to mode 1 with `c = 44`.
  - Otherwise ani = `(c & 3) div 2` (plus 4 for the octopus): the legs change every second step.
  - **Blocked test:** three points 0.5 tile ahead of the body edge in the walking direction (at 0.1, 1 and 1.9 along the edge). If any is blocked, the head turns back (`head = dir + 2`), the body turns right (`dir = dir + 3`; the octopus turns its body with the head), and an even `c` is made odd.
  - Not blocked: move 0.25 tile in `dir` (0.5 for types 6 and 8).
- **Head and body disagree:** on an even `c` the body turns to the head; on an odd `c`, `c` falls by 1. So a baddy that bumped into a wall looks back for one step, then walks the new way.
- **Sight check** (not the octopus): see "Sight". If it sees its target it goes to hunt.

### Mode 1: look about **[2.22][cap]**

- `c` falls by 1. When it goes below 0: a random direction, mode 0, `c = Random(20) + 40`.
- Otherwise the head turns by the table `{1, 1, 0, −1, −1, 0, 1, 1, 0, −1, −1}` at index `c div 4`: `head = (turn + dir + 4) & 3`. The body stays.
- Sight check, as in mode 0.

44 steps is 4.4 s of looking about **[cap]**.

### Mode 2: hunt **[2.22][cap]**

- **The pause:** while `c ≥ 6`, `c` falls by 1 and ani = `c & 1` (unless hurt). A baddy that just saw its target enters with `c = 16`, so it stands 1 s before it chases; after a hit it enters with 12, a 0.6 s pause.
- **Chasing** (`c < 6`): the hurt flag is cleared. Types 3 and 9 run the archer step; every other type runs the melee step.

**Melee step:**

1. `c = (c + 3) & 3` — it cycles 0, 3, 2, 1 — and ani = `c div 2`. `steps.wav` when `c` is 0.
2. Pick the target (see "Target") and test sight in the current direction. Not seen: `lost` rises by 1; above 40 (4 s) the baddy gives up and goes to mode 1 with `c = 44`. Seen: `lost` = 0.
3. Main and side axis: the axis with the larger distance to the target is the main one, the other the side, and `ratio` = smaller / larger. If both distances are under 2 tiles and the target is not seen, the main direction stays the current one.
4. Probe the main direction 0.5 tile ahead and the side direction 0.1 tile outside the body (three points each). If the main direction is not the wanted one and it is blocked, retry with the wanted one.
5. Move, with speed 0.5 tile (0.75 for type 8): main free and side blocked → main only; both free → main plus side × ratio; main blocked and side free → side only; both blocked → no move.
6. **Unstick** when the main direction was blocked: round x and y to the half-tile grid, then for each side whose three inner points (0.1 inside the body edge) are in a wall, push 0.5 tile away from that side.
7. Body and head face the main direction.

**Archer step** (types 3 and 9):

- Ani: the dragon cycles `c` and draws `c div 2`; the shooting soldier keeps ani 2.
- If `lost > 0` it is the cool-down after a shot: `lost` falls by 1; at 0, `c = 12`.
- Otherwise it walks to a firing spot 11 tiles from the target in line with the way it faces: spot = target + `{(−1, 11), (11, 1), (0, −11), (11, 1)}` by target direction (up, left, down, right; left and right share one entry in the table, and the distances are compared as absolute values) **[2.22]**.
  - If it was aiming and sees the target, it stops to look about (mode 1, `c = 44`).
  - It shoots when it is within 1 tile of the spot, or after more than 40 steps of trying. Otherwise it steps 0.5 tile on each axis where it is still 1 tile or more away, with `steps.wav`, then unsticks as above.
  - It also shoots when stuck, or when it is in line with the target and 11 tiles or more away.
- **Shoot:** `lost = 15` (1.5 s cool-down), aiming on. An arrow with sprite `107 + dir` (kind 2, fire, for the dragon; kind 0 otherwise) starts from the baddy's x, y plus `{(12, −12), (−10, 0), (4, 3), (11, 0)}` eighths by direction, and goes out as `PLI_ARROWADD`.

### Modes 3 and 4: hurt and shield bump **[2.22][cap]**

- While `c > 2`: add the knock vector to the position; if any of the 12 inner points is in a wall, undo the move. Then `c` falls by 1. With `c = 8` at the hit this moves for 6 steps.
- When `c` goes below 1:
  - power below 1 → mode 5 with `c = 14`;
  - otherwise: the hurt verse, once per baddy, for a mode 3 hit; then mode 2 with `c = 12`, head toward the target, `lost = 0`.
- The octopus: when `c` falls below 4 it goes to mode 5 with `c = 9`.

### Mode 5: dying, and mode 9: dead **[2.22][srv]**

- Mode 5: `c` counts down to −1 (1.5 s for `c = 14`), drawing the body, then the puff.
- Offline, the client then removes the baddy (`compudead.wav`).
- Online, the server waits 2 s from mode 5 and sends mode 9 to every client; mode 9 removes the baddy on the client **[srv]**. The server then respawns it (see "Respawn and drops").

### Mode 6: swamp soldier (type 4) **[2.22]**

- `c` cycles `(c + 1) mod 43` (4.3 s).
- At 11: face down. At 17: it leaps out of the swamp (the splash effect, `crush.wav`). At 22: face the target. At 25: shoot an arrow (as above). At 33: face down, aiming off. The head follows the body.
- A hit does not knock it back: it sets `lost = 8`. While `lost` counts down it blinks; at 0 the hurt flag is cleared, and with power below 1 it goes to mode 5 with `c = 14`.
- It can be hit, and can hurt by touch, only while `lost < 1` and `21 < c < 37` (out of the swamp).

### Mode 7: frog (type 5) **[2.22]**

- `c` cycles `(c + 1) mod 46` (4.6 s). At 0, `lost` rises by 1, and on even values the frog jumps back to its start position ±4 tiles at random. `frog.wav` at 16.
- It can be hit, and can hurt by touch, only while `16 < c < 38`.
- A hit kills it at once: mode 5, `c = 9`, and it moves up one tile.

### Mode 8: octopus ink (type 6) **[2.22]**

- `c` falls by 1 from 13. At 10: ani 6. At 6: ani 7 and an ink shot (sprite 131) from the baddy's x, y plus `{(4, −3), (−8, 5), (4, 12), (17, 5)}` eighths by direction. At 2: ani 4. At 0: a random direction, mode 0, `c = Random(10) + 20`.

### When a baddy can hit and be hit **[2.22]**

"Active" means not in modes 3, 4 or 5 (or 9), with the two extra conditions above for modes 6 and 7. Only an active baddy can be hit by a sword, arrow, bomb or thrown object, and only an active baddy hurts by touch.

## Target **[2.22]**

- Candidates: every player in the level plus the local player (online), or the local player (offline).
- Distance is `max(|dx|, |dy|)` from the baddy's centre to the player's centre. The best starts at 1000.
- The first candidate is taken without a sight test; every closer one after it must be in sight. So with one player in the level, that player is always the target, seen or not.
- The local player is skipped while a flag on it is set (the same flag that hides it from NPC tests; not traced further).
- The target's direction from the baddy (up, left, down, right) is the axis with the larger distance, and its sign.

## Sight **[2.22]**

A baddy sees a point when all of these hold:

1. **Cone:** the point is strictly on the facing side (above for up, and so on), and the distance along the facing axis is at least the distance across it — a 90° cone.
2. **Range:** within 20 tiles (the larger of the two distances).
3. **Line:** stepping from the baddy's centre to the point one tile at a time, no step lands on a wall, on water, a chair or the bottom of a bed, on another player, an NPC, a horse or another 2 × 2 object.
4. **Hidden:** a target that is hidden needs an extra flag (not traced).

Walk and look about test with the head's direction; the hunt tests with the body's direction.

## What blocks a baddy **[2.22]**

A point blocks when it is off the board (outside 0 to 64), on a wall tile, on water (tile type 11), a chair (3) or the bottom half of a bed (5), inside another player's body (x + 0.5 to 2.5, y + 1 to 3; online only), or inside an NPC, a horse or another 2 × 2 object.

The probes, from the baddy's x, y, three per side at 0.1, 1 and 1.9 along the edge:

| Probe | Up | Left | Down | Right | Used by |
| --- | --- | --- | --- | --- | --- |
| ahead | y − 0.5 | x − 0.5 | y + 2.5 | x + 2.5 | walk, hunt main axis |
| just outside | y − 0.1 | x − 0.1 | y + 2.1 | x + 2.1 | hunt side axis |
| inside | y + 0.1 | x + 0.1 | y + 1.9 | x + 1.9 | unstick, knockback |

## Damage

### Sword **[2.22][cap]**

Every tick, for every player whose gani is the sword (the local player and every other player the client draws), against every active baddy. With the player's centre P = (px + 1.5, py + 2), the baddy's centre B = (x + 1, y + 1), ADX = |Px − Bx| and ADY = |Py − By|:

**Shield block** — types 0, 1, 2 and 7, when the baddy faces the player (`dir = (player dir + 2) & 3`). It blocks when, by the player's facing:

| Player faces | Blocks unless |
| --- | --- |
| up | By + 5 < Py, or Py ≤ By + 2, or ADX > 2, or Bx + 0.5 ≤ Px |
| left | Bx + 5 < Px, or Px ≤ Bx + 2, or ADY > 2, or Py ≤ By − 0.5 |
| down | Py < By − 5, or By − 2 ≤ Py, or ADX > 2, or Px ≤ Bx − 0.5 |
| right | Px < Bx − 5, or Bx − 2 ≤ Px, or ADY > 2, or Py ≤ By − 0.5 |

**Hit** — when there is no block:

| Player faces | Hits unless |
| --- | --- |
| up | By + 4 < Py, or Py < By, or ADX ≥ 2 |
| left | Bx + 4 < Px, or Px < Bx, or ADY ≥ 2 |
| down | Py < By − 4, or By < Py, or ADX > 2 |
| right | Px < Bx − 4, or Bx < Px, or ADY > 2 |

The power is the swinging player's sword power.

### The hurt routine **[2.22][cap]**

On the leader (or offline):

- **Hit:** the hurt flag is set and power falls by the hit's power. Then by type: the swamp soldier sets `lost = 8` and stops here; the frog dies at once (mode 5, `c = 9`, one tile up); any other type goes to mode 3 with knock length 2.0.
- **Shield block:** mode 4, knock length 0.8, `swordon.wav`, and the player is pushed back (the player's own pushed state).
- Then `c = 8` and the knock vector is `−(P − B) × 2`, scaled to the knock length. A zero vector becomes (−length, 0).

On a client that is not the leader, a hit takes the power locally, sets mode 3 and a pending flag (so the next relayed mode does not undo it), and sends `PLI_BADDYHURT` (16) for the leader to apply:

| Byte | Value |
| --- | --- |
| id | the baddy id |
| dx | `round((Px − Bx + 4) × 16)`, with Px − Bx clamped to ±4 |
| dy | `round((Py − By + 4) × 16)`, same clamp |
| power | the hit's power, as is (a sword power of 1 sends 1) |

The server passes it on as `PLO_BADDYHURT` (27) to the leader, which decodes `d = (byte − 32 − 64) / 16` (the `−32` undoes the wire's byte offset) and runs the hurt routine. The leader applies it only when it is the leader and the baddy is in its current level **[2.22][srv]**. The two-client capture shows one such message from a 2.22 client that was not the leader, facing right with sword power 1: id 1, dx −3.5, dy 0, power 1. In the same step that client also sent its own `PLI_BADDYPROPS` with power 1 and mode 3, and the server relayed those bytes to the other client 6 ms later **[cap]**.

### Arrows, bombs and thrown objects **[2.22]**

- A projectile point hits an active baddy when it is within Bx ± 1 and By − 2 to By + 1. The knock direction is the projectile's direction.
- The hit-objects message (`PLO_HITOBJECTS`, as sent by `hitobjects`) hurts an active baddy within 2 tiles of the point on both axes.
- An arrow a baddy shoots belongs to no player, so it hurts any player it reaches, even in a no-killing level **[doc]** (`damage-sources.md`).

### Touch **[2.22][cap]**

- Each client tests only its own player: the player's centre within 1 tile of the baddy's centre on both axes hurts it by half a heart (a whole heart for type 7).
- The player's hurt lock-out (40 ticks, 2 s) stops repeats: in the captures, touches land 2.0 s apart and each costs one half-heart **[cap]**.
- If the baddy already used its sight verse and has not used its attack verse, it says the attack verse.

### Verses **[2.22]**

Each baddy has three verses: sight (BDPROP 8), hurt (9) and attack (10). Each is said once in the baddy's life, for 20 steps (2 s): the sight verse on first entering hunt from walk or look about, the hurt verse after the first knockback that does not kill it, the attack verse on the first touch after the sight verse.

## Drops **[2.22][srv]**

The 2.22 client drops nothing when a baddy dies. GServer-v2 drops on mode 9 when the server option `baddyitems` is on, rolling `Random(12)`:

| Roll | Item | Odds |
| --- | --- | --- |
| 0, 6 to 9 | green rupee | 5/12 |
| 1 | blue rupee | 1/12 |
| 2 | red rupee | 1/12 |
| 3 | bombs | 1/12 |
| 4 | darts | 1/12 |
| 5 | heart | 1/12 |
| 10, 11 | nothing | 2/12 |

Whether the original GServer dropped items, and with what odds, is not known **[inf]**.

### 1.x clients roll the drop themselves **[bin]**

Before NewMain 1.42 the drop is not the server's: the client rolls it when a baddy dies. One `Random(100)` per death, the item lands on the baddy's position, and online the client announces it the same way as a bush drop (see `item-drops.md`):

| Roll | Item | Gray, blue, red soldier, frog, octopus, golden warrior, lizardon | Shooting soldier (3), swamp soldier (4), dragon (9) |
| --- | --- | --- | --- |
| 0 to 9 | green rupee | 10 % | 10 % |
| 10 to 14 | blue rupee | 5 % | 5 % |
| 15 to 29 | heart | 15 % | 15 % |
| 30 to 74 | darts | – | 45 % |
| the rest | nothing | 70 % | 25 % |

- A baddy never drops a red or gold rupee, bombs or anything else, and drops at most one item.
- The roll runs when a baddy goes to dying (mode 5): when its hurt time ends with power below 1; at once for a frog on any hit; after a short delay for a swamp soldier; and for an octopus a few steps into any hurt, whatever its power.
- Online, only the client that runs the level's baddies (the leader) is expected to reach the death code; another client only lowers the power and sends `PLI_BADDYHURT` **[inf]**.
- **Builds.** The same odds and types in every client from 7th Graal (beta 7, 1998-12) to 1.41 (graal_gr1411): 1.0, 1.1, 1.1.9, 1.21, 1.28 beta 2, 1.3 beta, 1.31 to 1.39 and 1.41 were all read. From 1.38 the code picks the item by its number (0, 1, 5, 4) instead of its name. 1st Graal to 6th Graal give darts to types 3 and 4 only, and 1st to 4th Graal roll the heart before the blue rupee (heart 10 to 24, blue rupee 25 to 29), so the odds are the same. NewMain 24/26 and the NewWorld betas have no client roll.
- So a 1.x-compatible server should leave `baddyitems` off for 1.x clients, as it does for `bushitems`.

## Respawn **[srv]**

GServer-v2 waits `baddyrespawntime` seconds (default 60) after mode 9, then resets the baddy to its start position, its start power, the start mode for its type, and BDPROP 7 = `(2 << 2) | 2` (body and head down), and sends it to the level.

## Messages

| Message | Way | Content |
| --- | --- | --- |
| `PLO_BADDYPROPS` (2) | S→C | baddy id, then props |
| `PLO_BADDYHURT` (27) | S→C | a hurt from another client, for the leader |
| `PLO_ISLEADER` (10) | S→C | this client is the level's leader and runs the AI |
| `PLI_BADDYPROPS` (15) | C→S | from the leader: the props that changed in the last step |
| `PLI_BADDYHURT` (16) | C→S | a hit seen by a client that is not the leader |
| `PLI_BADDYADD` (17) | C→S | `putnewcomp` online: ask the server to create a baddy |

### The props **[2.22][cap]**

| Id | Prop | Wire | What the client does with it |
| ---: | --- | --- | --- |
| 1, 2 | X, Y | `c(tiles × 2)` | position, clamped to 0 to 63; also becomes the start position (used by the frog's jumps) |
| 3 | type | `c` | type 4 sets ani 2, type 6 ani 4; types 3 and 4 load `wbow1.png` |
| 4 | power and image | `c(power)` + string | an empty image means the type's default; the client sends an empty image when it uses the default |
| 5 | mode | `c` | 3 sets the hurt flag and clears pending; the mode is applied only when no hit is pending; 2 shows the sight verse once, 3 the hurt verse once; 9 removes the baddy |
| 6 | counter | `c` | the step counter `c` |
| 7 | directions | `c(dir × 4 + head)` | body direction high, head low |
| 8, 9, 10 | verses | string each | sight, hurt, attack |

An unknown id in `PLO_BADDYPROPS` creates the baddy, with the leap effect and `crush.wav` when it is in the current level **[2.22]**. The leader sends only what changed, so a step with no change sends nothing **[cap]**.

### Who owns what

| Owned by | What |
| --- | --- |
| server | ids (from 1), creation from the level and `PLI_BADDYADD`, mode 5 → 9 after 2 s, respawn, drops, choosing the leader [srv] |
| leader's client | all AI: mode, counter, position, directions, power after hits, arrows and ink it shoots [2.22][cap] |
| every client | drawing, touch damage to its own player, sword hits it sees (reported with `PLI_BADDYHURT` unless it is the leader), arrow, bomb and thrown hits it judges [2.22] |

A serverside script that recreates a baddy takes over the leader's part as well; see `server-notes/baddies-serverside.md`.

## Sounds **[2.22]**

`steps.wav` (walking, hunting, the archer's steps), `frog.wav` (the frog), `swordon.wav` (a shield block), `crush.wav` (leaping out of the swamp, or a baddy appearing; `water.wav` instead on water), `compudead.wav` (a baddy removed).

## Lab check **[cap]**

`tools/baddy-222/check_capture.py` follows every baddy through the 2.22 captures and checks the leader's updates step by step. On `lan-222kill-baddy.txt` and `lan-222d-baddyprops.txt` (the format of the third capture does not parse):

| Rule | Pass | Fail |
| --- | ---: | ---: |
| frog counter rises by one, modulo 46 | 515 | 0 |
| hunt cycle 0, 3, 2, 1 | 2512 | 0 |
| counter falls by one in mode 1 / 2 (the pause) / 3 / 5 | 71 / 268 / 18 / 28 | 0 |
| entering mode 1 with 44 | 15 | 0 |
| entering mode 2 with 16 or 12 | 17 | 0 |
| entering mode 3 with 8 (7 after the step) | 3 | 0 |
| entering mode 5 with 14 or 9 | 2 | 0 |
| hunt step at most 0.5 per axis | 2512 | 0 |
| knock step of length 2.0 or 0.8 | 10 | 0 |

The two-client hurt run (`lab-baddies-v3.md` in the project files) gave one `PLI_BADDYHURT`, decoded above.

## Differences from the 2.05-based rebuild

The `graal-delphi` rebuild's 2.22 baddy unit is still the 2.05 code. 2.22 differs in:

- the hunt's side probe is 0.1 tile outside the body, not 0.5;
- unsticking tests the inner probes;
- targets are chosen among all players in the level, not only the local player;
- the sounds above;
- a shield block pushes the player back;
- the ground overlays (water, grass, lava) instead of the shadow.

## Open points

- Online with more than one player: whether a client that is not the leader also reports sword hits by *other* players it sees (it runs the test for them) — the two-client run only had the swinging client report its own hit. In that run later swings sent nothing more and the baddy stopped being drawn on that client, which the pending flag alone does not explain.
- The archer's and the swamp soldier's timings, and the shield bump, were read but not seen in a capture.
- The flags that skip the local player as a target and that let a baddy see a hidden player are not traced.
