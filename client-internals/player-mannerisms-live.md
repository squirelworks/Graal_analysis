# Player mannerisms seen in real clients (2.05 rev 2 and 1.39)

Date: 2026-10-30. What the player does, tick by tick, in two real clients run under Wine with no network.

* **2.05 rev 2.** The player state was read every 3 ms from outside the process while xdotool held keys, and the screen was recorded at 60 fps. Tag **[live]**. The test level is `lab1.nw` (described below).
* **1.39.** This client was run in its own One Player mode on its built-in start level. It was measured from 60 fps screen video only, with no memory read. Tag **[video]**. Its counts are good to ±1 tick.
* **The gani files.** These are the files that the timings come from. Tag **[gani]**.

A tick is the 50 ms game tick. Speeds are in tiles. This note has no addresses and no decompiler text. The harness, the level, the raw traces and the gani comparison script are in the project files under `graal-decompile/live-trace/mannerisms/`. Stills are in `mannerisms-shots/`.

## Summary table (2.05 rev 2)

| action | what the client does | timing |
|---|---|---|
| walk | `walk`, 0.5 tile per tick, one gani frame per tick (8 frames) | 8-tick cycle |
| key released | `idle` in the same tick, frame 0 | 0 ticks |
| run into a wall | `walk` keeps cycling in place; `push` on the **18th** blocked tick | 0.9 s |
| push pose | 5 frames × 4 ticks; restarts at frame 0 each time the 20-step push cycle wraps | 20-tick loop |
| slide along a wall | holding Down into a wall and adding Right walks right at full speed with `walk`. The blocked count drops to 1 and stays there. | — |
| lift (A) | `lift` for **6 ticks**, then `carrystill`. The object counts as carried from the 5th tick. | 0.3 s |
| carry walk | `carry`, still 0.5 tile per tick, 8 frames × 1 tick | — |
| hide (D while carrying) | `hiddenstill` / `hidden`; walking is **0.1 tile per tick**; only the object is drawn | — |
| throw (A, or S from hiding) | `idle` in the same tick | 0 ticks |
| sword (S) | `sword` 5 frames × 1 tick, then `idle`. The player stops while it plays. | 5 ticks |
| hurt | `hurt` for 31 ticks; knockback 1 tile per tick for 5 ticks; blinking and no further hits for 40 ticks | 1.55 s / 2.0 s |
| swim | `swim` from the first tick the point (x + 1.5, y + 2) is on water; 0.5 tile per tick; 8 frames × 2 ticks; **keeps animating when standing still** | 16-tick cycle |
| grab / pull | `grab` on A at a wall. `pull` starts on the arrow away from the wall: 3 frames × 2 ticks, with a pull try every 18 ticks. | — |

## Walking, idle and running in place **[live]**

* Each walk tick moves 0.5 tiles and advances the `walk` frame by one (0 to 7, then 0). The first tick after the key goes down already moves the player.
* Letting go of the arrow switches to `idle` frame 0 in the next tick. There is no slow-down and no finishing step. In `idle` nothing in the player state changes from tick to tick.
* **Against a wall.** A refused step still advances the walk frame, so the player runs in place. The blocked-step count goes 1, 2, …, 17, and `push` replaces `walk` on the 18th. This is the same count as the ledge jump (`ledges-push-pull.md`). Deep water (tile 3644) counts as a wall.
* **The push pose.** Each push frame lasts 4 ticks (`push.gani`: 5 frames, each `WAIT 3`). When the count reaches 38 it goes back to 18, and the gani starts again from frame 0. Five frames of 4 ticks make exactly that 20-tick cycle, so the pose loops seamlessly.
* **Sliding along a wall.** Still holding Down into the wall, add Right. The player walks right at the full 0.5 tile per tick in `walk`, and the push pose is gone in that tick. Let go of Right and the player runs in place again from walk frame 0. The blocked count goes on from where it had dropped to (1), so the full 18 ticks have to pass again before `push`.
* Pressing the arrow again into the wall after letting go starts the count at 1, with no push straight away.

## Lifting, carrying, hiding and throwing **[live]**

Test objects: a bush, a pot, a light stone, a black stone and a sign in a row (`lab1.nw`, y = 20).

* **Lift.** A at the bush (or the pot) plays `lift` at once. A five-step counter runs 4 down to 0, and the carried flag is set on the 5th tick. `carrystill` follows on the **7th tick** (6 ticks of `lift`, as `lift.gani` = 1 frame with `WAIT 5`). The bush tile turns into its stump at once (`arrays.dat` array 12).
* **Carry.** Walking while carrying plays `carry` (8 frames, one per tick) at the normal 0.5 tile per tick. There is no slow-down. Stopping plays `carrystill`. The object is drawn over the head. In the video the head and arms are hidden behind it (`205-pot-throw.png`, first frame).
* **Hide** (D while carrying a bush). In the same tick the pose becomes `hiddenstill`, and the player's "hidden" flag (STATUS bit 0x02, see `carry-hide-and-glove.md`) is set. Only the bush is drawn, where the player stands. Body, head and shadow are all gone (`205-hidden-under-bush.png`).
  * Walking while hidden plays `hidden` at **0.1 tile per tick**. That is a fifth of the walk speed, which confirms the 0.2 factor in `carry-hide-and-glove.md`. The gani frame does not advance: `hidden.gani` is one frame with `WAIT 4` and a step sound.
  * Stopping goes back to `hiddenstill`.
  * D again leaves the hiding place, back to `carrystill` in the same tick.
  * S while hidden throws the bush. The player is in `idle` in that tick, with the hidden flag cleared and the carried flag cleared.
* **Throw** (A while carrying). The player is in `idle` in the same tick. Video of a pot thrown upwards (`205-pot-throw.png`, one frame per tick):
  * The object flies about 6 tiles in 9 ticks. Its shadow moves along the ground while the object itself is drawn rising and then falling back onto the shadow.
  * It breaks into four pieces that spread out over 4 ticks and then vanish.
  * The pot's base tile (the grey plinth) stays where it was lifted.
* A at a black stone with glove 1 does nothing: no lift and no grab. The stone is not a wall tile.

## Sword **[live]**

* S plays `sword` in the next tick. Five frames of one tick each, then `idle` (`sword.gani`: 5 frames, `SETBACKTO idle`).
  * The player does not move while it plays, even with an arrow held.
  * With the arrow still held, walking resumes in the tick after the swing, from walk frame 0.
  * Holding S does not swing again. Every swing needs a new press.
  * Holding S for 2.5 s without the spin item gives no charge and no spin.
* **What it looks like** (facing up, `205-sword-up-bush-cut.png`):
  * The blade sweeps from the right side over the head to the left.
  * The bush in front is cut on the **first** swing frame. The leaves fly up and out for about 8 ticks, and the stump is left behind.
  * The shield stays drawn on the right during the swing.
* **Offline editor play with no sword.** A player started from the editor has sword power 0. S still plays the full `sword` gani and sound, but no blade is drawn and nothing is cut. Give the player a sword (`setsword sword1.gif,1` in a level NPC) to test cutting.

## Hurt, knockback and blinking **[live]**

The test NPC runs `if (playertouchsme) { hurt 1; }`.

* Touching it plays `hurt` in the same tick and takes half a heart (3 → 2.5).
* **Knockback.** The player moves **1 tile per tick for 5 ticks**, along the direction from the NPC's image centre to the player's centre. In the run it went from (29.5, 48) to (28.79, 52.95), which is 5.0 tiles. This is exactly the decompile's description (`decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md`).
  * If the player is inside a blocking NPC's image, every knock step is refused and the player does not move. A large image, such as `bomb1.png` at 128 × 320, makes this happen.
* **Pose.** `hurt` is shown for **31 ticks** (`hurt.gani`: 1 frame, `WAIT 30`), then `idle`. The hurt pose keeps the facing.
* **Can't be hurt again** for 40 ticks (2 s) from the hit. The second touch in the run came only after that.
* **Blinking.** For the whole 40 ticks the player's body is drawn in one tick and left out in the next: only the shadow shows on the "off" ticks (`205-hurt-knockback-blink.png`). It goes on after `hurt` has given way to `idle`.
* Keys are not read for walking during `hurt`: an arrow held through the hit did not move the player.

## Swimming **[live]**

Water tile 461 (passable, liquid); the pool starts at x = 40.

* The switch to `swim` happens on the tick where x + 1.5 reaches 40 (x = 38.5). Leaving the water happens where x + 1.5 drops below 40 (x = 37.5). In that tick `walk` comes back, at frame 0.
* Swimming speed is the same 0.5 tile per tick as walking.
* `swim` steps one frame every **2 ticks** (8 frames, `WAIT 1`), so the stroke takes 0.8 s.
* **It keeps animating while the player is not moving.** It does not reset when the player turns.
* The splash at entry and exit is in `water-and-ganis.md`.

## Grab and pull **[live]**

At a wall of deep-water tiles, facing down:

* A at the wall plays `grab` at once and holds it.
* Holding the arrow away from the wall (Up) plays `pull`: 3 frames of 2 ticks each (`pull.gani`, `WAIT 1`). The pull cycle counter goes 2 … 19 and back to 2, so it repeats every 18 ticks, as in `ledges-push-pull.md`. Nothing moves against a wall.
* **Letting go of the arrow while still holding A.** The cycle counter drops to 1, but the pose stays `pull` and keeps animating. It does not go back to `grab`.
* **Letting go of A as well.** The pose still stays `pull`, animating in place, until the next key moves the player. This answers the open question in `ledges-push-pull.md`: nothing sets `idle` there, and the stale pull loop is what is drawn.

## 1.39, before ganis existed **[video]**

1.39 is the last client before the first gani build (`graalnm24`, January 2001). Its player animation is built into the executable.

* **Input under Wine.** 1.39 ignores xdotool keys until `nodirectinput=true` and `joystickon=false` are set in its `graalconfig.txt`. 2.05 needs neither.
* **Walk.** 0.5 tile per tick (8 px per tick) with an 8-tick frame cycle, the same as 2.05.
* **Idle.** The sprite does not change.
* **Against a wall.** The walk cycle runs in place, and the push pose replaces it about **18 ticks** after the key went down, the same as 2.05.
  * The push pose (`139-push-left.png`) drops the shield and puts both hands on the wall.
  * Unlike 2.05, its frames change about every **2 ticks**, not every 4.
  * The pose sequence restarts on the same 20-tick cycle, though which frame restarts it could not be told from video.
* **Sword.** About 5 ticks, then idle, the same as 2.05. Facing left, the blade sweeps from above the head down to the lower left. The shield is hidden for the swing (`139-sword-left.png`).
* Not checked in 1.39: lift, carry, hide, throw, hurt and swim. The built-in start level has none of the objects, and a `.graal` test level was not built.

## The built-in ganis across the gani sets **[gani]**

The 2.0x archives in the project hold only the executables, and the 2.05 client fetches its ganis from the server. The gani sets on hand are:

* NewMain 2.4 and 2.6, the first gani clients (December 2000 files);
* NewWorld beta 1 (August 2001);
* the Graal Reborn 2.22 pack.

NewMain 2.4 and 2.6 are identical. In the table below, frames × ticks gives the ticks per frame (1 + WAIT); ">x" is SETBACKTO x; L means LOOP.

| gani | NewMain 2.4 / 2.6 | NW beta 1 | 2.22 pack |
|---|---|---|---|
| idle | 1 | 1 | 1 |
| walk | 8 × 1, L | 8 × 1, L | 8 × 1, L |
| walkslow | 8 × 2, L | – | 8 × 2, L |
| sword | 5 × 1, >idle | 5 × 1 | 5 × 1, >idle |
| spin | 13 × 1, >idle | – | 13 × 1, >idle |
| push | 5 × 4, L | **3 × 4**, L | 5 × 4, L |
| pull | 3 × 2, L | 3 × 2, L | 3 × 2, L |
| grab | 1 | 1 | 1 |
| lift | 1 × 6, >carrystill | **6 × 1** | 1 × 6, >carrystill |
| carry | 8 × 1, L | 8 × 1, L | 8 × 1, L |
| hidden | 1 × 5, L, single direction | (no frames) | 1 × 5, L, single direction |
| kick | 1 × 5, >idle | 1 × 5 | **1 × 11**, >idle |
| shoot | 1 × 11, >idle | 1 × 11 | 1 × 11, >idle |
| hurt | 1 × 31, >idle | 31 frames (10 × 2 then 21 × 1) | 1 × 31, >idle |
| dead | **13 × 4** (52 ticks) | 5 frames, >gameover | **15 frames** (3 × 7 + 2 × 8 = 37 ticks) |
| swim / lava | 8 × 2, L | 8 frames (6 × 2 + 2 × 1) | 8 × 2, L |
| ride | 4 × 2, L | 4 × 2, L | 4 × 2, L |
| sleep | 1 | **2 × 19**, L | 1 |

* Every 2.05 live timing above matches the NewMain / 2.22 column: walk, push, pull, lift, carry, sword, hurt and swim.
* **The hidden ganis.** In NewMain, `hidden` and `hiddenstill` draw only a shadow, and the client itself draws the carried object. The 2.22 pack adds the object to the gani as an `ATTR3` sprite (`bushitem.png`). A 2.22 server's ganis drawn by the 2.05 client would therefore show the bush twice.
* Every set keeps the same sounds on the same frames: `steps2.wav` on walk frames 0 and 4, `sword.wav` on frame 0, `lift.wav` on lift and hurt, and `water.wav` / `water2.wav` on swim / lava.
* The full per-file output, with frame-content hashes, is `gani-compare.txt` in the project folder.

## Asset gotcha: 2.05 loads only GIF heads, bodies and swords **[live]**

Given the 2.22 folder, where heads, bodies, swords and shields are PNG, 2.05 rev 2 looks only for `head0.gif` and the like. It finds nothing and draws the player with no body. That is the "missing body" in `live-trace-205.md`, and it is not a Wine bug. Converting `levels/{heads,bodies,swords,shields}/*.png` to `.gif` next to them fixes it. A Seihai 2.05 profile that resolves player images should try `.gif` only.

## What Seihai does differently (from its `client/src/pose.rs`, 2026-10-30)

Seihai was not changed here. These are what a 2.05 profile would need:

1. **Push.** Seihai shows `push` after 17 blocked steps and advances it one frame per blocked step. The real client shows it on the 18th and holds each frame for 4 ticks (it honours `WAIT`).
2. **Pull.** Seihai steps `pull` once per tick; the real client steps it once every 2 ticks. Seihai drops the pose on release; the real client leaves `pull` looping.
3. **Gani WAIT.** Seihai does not read per-frame `WAIT`. The real hurt pose is 31 ticks, not Seihai's 500 ms minimum. Lift is 6 ticks. Swim is 2 ticks per frame, which Seihai already uses.
4. **Swim while still.** Seihai steps `swim` per step taken. The real client keeps it animating when the player stands still in water.
5. **Hurt blink.** There is no blink in Seihai. The real client draws the body on alternate ticks for 40 ticks.
6. **Hide.** There is no `hiddenstill` / `hidden`, no 0.1 tile per tick walk and no hidden flag in Seihai.
7. **Lift pose.** Seihai goes straight to `carrystill`. The real client plays `lift` for 6 ticks first.

## Harness

* `act.py <name> "<keys>"` runs a key script, for example `down:Up w:0.6 up:Up tap:a`. It records the player state (gani, frame, position, every changed field) and 60 fps video at the same time. A `tap` holds the key for 120 ms: shorter taps are lost between ticks. `NOMEM=1` records video only, for builds whose player record has not been mapped.
* `sh.py` prints a trace, with the key presses interleaved.
* `mklevel.py` writes `lab1.nw`:
  * five liftable objects in a row at y = 20;
  * a pool of water tile 461 at x 40 to 55, y 10 to 30;
  * a deep-water wall at y = 40;
  * four bushes at y = 50;
  * a `setsword` NPC, a touch-to-hurt NPC at (30, 44) and a `lay spinattack` NPC.
* `gani.py` summarises and compares gani folders.

## Open

* **The spin attack.** It needs the spin item, and walking over the item laid by `lay spinattack` did not pick it up offline. Not seen.
* **The 1.39 timings by memory read.** Its player record has not been mapped. The same goes for lift, carry, hurt and swim in 1.39, which need a `.graal` test level.
* **The first gani client.** NewMain 1.41.1 (`graalnm24`) was not run. It would show whether gani timing behaved as in 2.05 from the start.
