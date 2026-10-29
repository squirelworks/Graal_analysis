# Live traces of the 2.05 rev 2 client

Date: 2026-10-29. These are behaviours seen in the running 2.05 rev 2 client: in Wine, offline with no network, with the player state read every 50 ms tick from outside the process. Hearts reports come from the 2.05 lab capture (`tools/lab-setup.md`, run 1). Tags: **[live]** seen in the running client, **[cap]** seen in a lab capture. This note has no addresses and no decompiler text. The harness, its scripts and the raw traces are in the project files under `graal-decompile/live-trace/`.

## Hearts are reported by the client

* **On a hit, the client sends its own CURPOWER.** **[cap]**
  * In run 1, the player's own bomb hit them. In the same tick as the hit, the client sent one `PLI_PLAYERPROPS` message with CURPOWER = 5 half-hearts (down from 6), GANI `hurt` and SPRITE. Its knockback position updates followed.
  * Nothing from the server asked for it, and the server did not echo CURPOWER back.
  * The 2.22 lab shows the same thing (`lab-captures-2026-10-25/`): a hit sends CURPOWER + `hurt`; death sends the `dead` gani + STATUS; respawn sends CURPOWER by AP bracket.
* A client that applies damage locally but never sends CURPOWER leaves the server holding stale (full) hearts for that player.
* Not yet captured for 2.05: lava burns, heart pickups and respawn.
* Hearts are stored obfuscated in the client (`feature-specs/04-death-respawn.md`). A memory scan does not find them as a plain value. **[live]**

## Ledge jump and running in place **[live]** (`new3.nw`)

* Walking up into the up-ledge at y = 14: the refused steps are counted 1 to 17, and the jump starts on the 18th.
* Jump y values from y0 = 14: 12.5, 11.3, 10.2, 9.5, 9.0, 8.8, 8.8, 9.0. This is exactly the curve in `ledges-push-pull.md`.
* **Running in place.** On every refused step the walk animation frame keeps advancing, and the gani stays `walk`. It changes only when the push gani takes over (at 18, against a wall) or the jump starts (at 18, at a ledge).
* While jumping the gani stays `walk`, and the blocked-step counter counts down 7 to 0 as the jump timer.

## Water and lava **[live]** (`new4.nw`)

| tile | what the client does |
|---|---|
| 3644, dark-blue deep water | Blocks like a wall. `push` comes at the 18th refused step. |
| 2882, bright-red lava | Swim: the gani becomes `lava`. Burns. |
| 2958, dark-red lava floor | Walkable: the gani stays `walk` / `idle`. Burns. |

* **Burn timing.** On either red tile a per-player counter runs 0 to 100 and wraps to 0 on the next tick. One cycle is therefore **101 ticks**, and each wrap costs half a heart. Three wraps took 3 → 1.5 hearts.
* Stepping onto grass resets the counter to 0.
* The liquid test uses the point (x + 1.5, y + 2).
* Burning to 0 hearts offline shows the `End` death scroll.
