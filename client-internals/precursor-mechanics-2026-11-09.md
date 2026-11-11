# Precursor mechanics: Zelda Online 1 and 2, 39ster, GraalX and the Zelda editor

Findings from the November 2026 research campaign on the programs described in [precursors-and-fan-builds.md](precursors-and-fan-builds.md). Each section names its evidence and how strong it is. Zelda Online 1 (here "Java1") and the 39ster client are read from code with thin runtime checks. Zelda Online 2 ("Java2") is read mostly from the author's own source and was **not** run. Evidence IDs resolve in [the evidence index](../docs/evidence-index.tsv).

## Zelda Online 1 input (Java1)

Evidence `VX-JAVA1-INPUT-20261109-01`. Input: `Zelda.class`, SHA-256 `86ef5832c200ba2dfcb29e27c210bf3ea9cccac0da002bd6b4ddc129439d0ce4` (34,148 bytes). A decompiled source was cross-checked against the key-down, key-up and worker bytecode. **[bin]**

### Walking is event-driven

- Each direction key-down callback makes **one** half-tile attempt. There is no pressed-key array and the worker does not poll keys.
- Each callback tests collision, then updates facing, position, pose, the swamp frame and the camera, repaints, and checks links.
- A held key repeats only through the operating system's key repeat. Worker ticks never repeat walking or add push progress.

### Key-down order

1. Input is rejected while the injury counter is 30 or more, during a jump or a lift, and after the game has ended.
2. With a sign open: up-arrow, `i` and `8` are swallowed without paging. Any other key shows the next 3 lines if there are more; otherwise it closes the sign and the **same** key is processed further, so the closing key can also move or attack.
3. On the start screen any key enters the game, and nothing else happens.
4. Once the ending counter reaches 28, any key reloads the start level.

### Keys

| Action | Keys |
| --- | --- |
| Up, left, down, right | arrows, `i` `j` `k` `l`, `8` `4` `2` `6` |
| Sword | space, `s`, `5` |
| Lift / grab | `a`, `1` |
| Bow | `d` |

Uppercase letters are not mapped. There is no pause key and no rule for two directions at once.

### Facing, collision and pushing

- Facing changes before the wall test, so a blocked attempt still turns the player.
- An active sword or bow animation skips the movement step but keeps the new facing. A pending grab blocks the facing change; pressing away from the facing during the first grab starts pulling.
- Collision uses 6 probes on the leading edge, with a corner correction of 1/8 tile.
- The wall-push count goes up by 1 for each blocked event without a correction and resets to 0 when a correction happens or the move is free.
- A stone is tried when the count before the event is 28, that is on the 29th blocked event. At 38 the count wraps to 18. At 18, if the jump test passes, an 8-update jump is armed.
- The walking pose advances one of 8 frames per event. From a count of 18 the push frames advance in groups of 4.
- An up attempt reads a sign and then tries to open a chest, even when blocked. The link test runs on every movement event, blocked or not, and never on a worker tick.

### Actions

- Sword throws a carried object. Otherwise it attacks, but only while the sword latch is clear. Enemy hits are resolved in the worker.
- Lift/grab throws a carried object. Otherwise it tries to lift (5 updates), or grabs if a wall is in front.
- Bow needs bow permission, at least one arrow, no bow animation in progress and nothing carried.

### Key-up

Every key-up clears the sword latch, the swamp frame, the wall-push count and grab or pull progress. If the player is not attacking, shooting or lifting it restores the standing pose. It does not cancel animations already running. So releasing any other key lets the sword start again, and a down/up pair resets pushing.

### Worker

- A fixed 50 ms sleep, with no allowance for the time the work took and no catch-up.
- During scrolling or loading, outside the game, or with a sign open it skips gameplay, but the tick count and the ending checks still run.
- Update order: sword frames (with enemy hits mid-swing), jump, pulling, lifting, carried and thrown objects, debris, projectiles, bow, periodic swamp effect, enemies (every second tick), injury movement, bump, pickups, camera, then a repaint when needed.

**[lab]** One Java 21 run on a modern host: a half-second hold moved the player half a tile. That fits the reading above but says nothing about key-repeat timing.

## Zelda Online 2 rules (Java2), from source

Read from the author's Java2 source (`ZeldaMain.java`, `Computer.java`, `ZeldaClient.java`) and the relay's `Player.java`. **Nothing in this section was run**; multiplayer was never exercised. Where bytecode was checked it is said so. **[src]**

### Start and input

- Java1 and Java2 both start at (22.5, 36) facing down, with 3 hearts and 5 arrows.
- Java2 keys: arrows, `I` `J` `K` `L` and `8` `4` `2` `6` move; `S`, space or `5` swing the sword; `A` or `1` is the action key; `D` fires the bow; `P` pauses. Letters are case-insensitive.
- Unlike Java1, held keys are polled on worker ticks. The 50 ms loop subtracts the time the work took, with no catch-up. An accepted tick moves half a tile. The sword is latched until the key is released.

### World and drawing

- The view is 32 × 28 tiles in Java2 and 32 × 24 in Java Graal. The camera is clamped to x 0–32 and y 0–36.
- Paint order: background, pickups, specials below the player, debris, enemies, other players, the player, thrown objects, the bump effect, projectiles, specials above the player, signs, the pause overlay, the status bar.
- Collision is the Java1 scheme: 6 foot-area probes on the leading edge, a 1/8-tile corner correction, and anything outside the 64 × 64 board blocks. Pushing: a stone at 28, the count loops 38 → 18, an 8-step jump at 18.
- Links use inclusive horizontal end points and an exclusive bottom edge. A negative destination keeps that axis.

### Combat

- The sword has 6 counter positions and 5 poses; hits are checked on the middle 3.
- Cutting a bush: green currency if a random draw is below 25 %, a heart below 30 %, blue currency below 32 %, otherwise nothing.
- Lifting: 3 object kinds with the starting glove, 4 with the better glove; a pot gives a heart; a lift takes 5 updates. Thrown objects fly 9 steps; a bush does 1 damage and heavier objects 10.
- The bow fires late in a 16-count animation and takes the arrow on launch.
- Enemies update every second tick. Hit points: green and swamp 2, blue and shooting 3, red 4, octopus 1. They move 1/4 tile per update; the octopus moves 1/2.
- Facing and the shield can turn a sword hit into a bump. Damage: sword 1, the player's arrow 3, touching an enemy 0.5. Contact injury runs a 40-count timer, and its knock-back vector is the raw position difference, not normalized.

### Pickups and progress

- Currency is capped at 999 and arrows at 30. Pickups vanish after 164 updates and blink from 128.
- Progress is hard-coded per level: the glove upgrade, bow permission, chests, rescuing the brother, and a 50-currency trade.

### Level resources

- The recursive array resource starts with a big-endian 32-bit header: the high half says flat or nested, the low half is the count. Java1 has 17 arrays, Java2 18 and Java Graal 19.
- The board codec is least-significant-bit first: 11-bit codes for Zelda 1.02, 12-bit for Z1.03, Z1.04, GR1.00 and GR1.01, and 13-bit for GR1.02 and GR1.03. The top bit marks a run, the low 8 bits are its count, and a flag selects runs that alternate between two tiles. 399 files (counting duplicates) decoded to exactly 4,096 tiles each.

### Relay

- A fixed TCP port, newline-framed, which mostly forwards; the relay does not simulate the game.
- The room name is a prefix, the level's base name and a fixed suffix (see the client sections of `precursors-and-fan-builds.md`).
- An 8-digit text id is packed into two 7-bit characters. Text is sent as the low byte of each Java `char`, not UTF-8.
- Submessages carry position, enemies, chat, nickname, colours, enemy injury, board edits, login time, dead enemy ids, extras, carried and thrown objects, and projectiles. Player positions are cut to whole tiles. Board edits are column-major two-character tile words. Login time is sent as 10 little-ordered 7-bit groups.
- One peer, the leader, drives the shared enemies. **Leader selection compares every peer with the local login time, not with the best candidate found so far**, so the order of the peer list can change who leads. The bytecode agrees on this.
- The source also shows a duplicated horizontal component in the hurt vector and an uneven clamp; these are source-only and need the bytecode to confirm.

An alternative Java2 main class differs only in the starting value of a free-stone variable: 1023 instead of 584.

## 39ster's client mechanics

Evidence `GRAAL39STER-ENGINE-20261109-01`. Input SHA-256 `ab47332b27479aa8c586da8daeaab0065a8adca80271de30a5d4fe694b3826cf`. The rules come from its game script (`main.gm`) and the engine; the only runtime check was rendering the town and pausing with `P`. The numbers below were not tested at run time. **[src][run]**

### Start and drawing

- It starts in `level13.nw` at pixel (512, 512), facing down, in a 640 × 480 view with 16-pixel tiles.
- The camera centres on a 16-pixel anchor and is clamped to the level; a level smaller than the window is centred.
- Player sprites are drawn as separate body, head, shield, sword and attribute pieces.

### Tiles

- An NW tile is a base64 pair giving a 12-bit id. The tile sheet is 128 × 32 cells; each block of 512 ids moves 16 columns across, the 2.x `pics1` layout.
- A category file holds one entry per sheet cell. Internally a tile packs 10 bits of column, 10 of row and 12 of category. The category is an index that is turned into a bit later, not a collision mask.
- Categories: ground, blocking, throw-through, water, chair, jump, swamp and shallow water. Lava is named but not used in the table. Blocking, jump and throw-through tiles count as walls.

### Collision and movement

- A rectangle outside the level is blocked.
- Edge scan: left and top edges truncate, right and bottom edges round up, and the end is exclusive. A zero-width edge is a real case and should be kept.
- Movement is 3 pixels per nominal update (2 when getting up from sitting). Diagonal components are multiplied by 0.75. The time factor is the previous frame time in ms ÷ (1000/60), capped at 4.
- The vertical move is resolved before the horizontal one. A blocked component shrinks 1 unit at a time.
- With only one axis pressed, a blocked move slides at 1.5 × the time factor, with a preferred direction and snapping at 16-pixel boundaries.

### Controls and animation

- Facing order is up, left, down, right. Arrows move while held. Space is a 5-frame sword. `A` grabs; pressing away pulls; releasing `A` stands; releasing the away key returns to the grab. `P` pauses. Signs page 3 lines on any key except Up, which scrolls back.
- Eight GANIs: idle, walk, sword, swim, sit, grab, pull, push, with 1, 8, 5, 8, 1, 1, 3 and 5 frames.
- The frame position advances by 0.35 × the time factor. An animation loops, switches to its return animation, or holds its last frame. Frame commands such as wait and sound are skipped.
- The freeze counter drops by 60 × the time factor each update, so a value of 1000 lasts about 17 updates, not one second.

### Links and NPCs

- Links are tested against the predicted rectangle (floor and ceiling). Special destination values keep an axis.
- A latch stops repeated warps and clears only once the player has left the link area. A successful warp resets movement but keeps the latch; a failed load also sets it.
- The NPC execute call is disabled, as `precursors-and-fan-builds.md` says, and the timer update was never seen being called.

## GraalX keeps an unchanged level byte-identical

Evidence `VX-GRAALX-NW-SAVE-20261109-01`. GraalX SHA-256 `155111950ac69bbae5add23b7c78e731ed4ca65b5d928ada76272a61687dfd74`. **[run]** A synthetic `GLEVNW01` level was loaded, F4 opened the editor and Save reported "Level saved". The file's time stamp changed but its 10,319 bytes stayed identical. This is one case with no edits; it says nothing about how edited levels are written. GraalX's stale version resource does not make it a 2.0 rev 3 profile.

## The Zelda editor writes an empty board

**[run]** One run of the July 1998 Zelda editor saved a new, empty board as a 206-byte `Z3-V1.03` file in which all 4,096 tiles are 1023. This is a single case. An earlier internal note said the editor had never been run; that note was wrong, since this run and its saved file exist.
