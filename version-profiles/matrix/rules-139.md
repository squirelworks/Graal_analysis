# 1.39 death, hurt, knockback, sword reach and wall test

Date: 2026-10-31. Closes matrix unknown #1 for **1.39** (era C). Tags: **[bin]** from the 1.39 client (plain behaviour only; no addresses), **[lab]** / **[1.39]** from the offline Wine mannerisms run already in `../../client-internals/player-mannerisms-live.md`. Tick = 50 ms.

Compared with the 2.05 rules in `../../client-internals/decomp-findings-2026-10-24/01-death-respawn.md`, `../../client-internals/decomp-findings-2026-10-24-d/01-sword-damage.md` and `../../client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md`.

## Summary table

| Rule | 1.39 | 2.05 (for contrast) | Tag |
|---|---|---|---|
| Hurt mode length | 40 ticks; cannot be hurt again while in mode 3 | same | **[bin]** **[lab]** |
| Knockback | 1 tile per tick while the hurt counter reads 39 down to 35 (five steps); zero vector becomes one tile east; twelve body-box probes; blocked step undone | same five steps | **[bin]** (earlier live table said four tiles; see below) |
| Hurt pose / blink | pose ~10 ticks then normal; blink starts after the pose, every other tick to 40 | `hurt` gani 31 ticks; blink from the hit | **[lab]** |
| Sword reach | 0–4 tiles ahead of the attacker in the facing; sideways offset under 2 tiles | same | **[bin]** |
| Sword swing length | counter 1→6 (5 ticks); cuts bush | 5 ticks (`sword.gani`) | **[lab]** |
| Death timer | counts 0→30 and stops at 30 | same | **[bin]** |
| Input while dead | any movement/action key respawns once the timer is above 27 | same (after 27) | **[bin]** |
| STATUS dead bit (0x08) | set only when life-state is dead **and** the timer is above 27 | same (≥ 28) | **[bin]** |
| Online default respawn spot | x 30.5, y 30.0 in the current level when no saved entry | same | **[bin]** |
| Respawn hearts | shared heart-write used on respawn restores to **max hearts**; no AP-band test in this path (1.39 has no AP HUD; bands arrive with 1.41) | AP bands (3 / 5 / max) | **[bin]** |
| Wall / walk test | six probe offsets per facing step; blocked count pushes at 18 and wraps 38→18; walk 0.5 tile/tick | six probes; same push counters; same speed | **[bin]** **[lab]** |
| Baddy touch power | 0.5 hearts (1.0 for type 7); within 1 tile on both axes of the baddy centre | same family of powers in 2.05 | **[bin]** |

## Hurt and knockback **[bin]**

A hit is refused when the player is already in hurt mode (mode 3), in mode 7, or not in the playing life-state. An accepted hit:

1. Clears the current pose sprite.
2. Sets mode 3 and the hurt counter to **40**.
3. Applies the power to hearts (negative power heals; hearts stop at max).
4. Stores a knockback unit vector. A zero vector becomes **one tile east**.
5. If the player was carrying something, may force a drop when the power is positive.

Each playing tick while in mode 3: the counter drops by one; at 0 the mode returns to normal. While the counter is **strictly greater than 34** after that drop (readings 39…35), the player moves one tile along the stored vector, then twelve body-box points (four edges × three) are tested; if any is blocked the step is undone for that tick.

The offline Wine run (`player-mannerisms-live.md`) measured a **40-tick** no-rehit, a ~10-tick hurt pose, blink after the pose, and **four** tiles of knockback on the touch-NPC test. The binary’s counter window is the same five-step window as 2.05; the four-tile live figure is kept as a lab observation that may have lost a step to collision or ±1 tick video error. Prefer the binary’s five steps for a faithful profile unless a re-run shows otherwise.

## Sword reach **[bin]** **[lab]**

When another player’s swing is judged against the local player, a hit counts only if the victim lies in a facing-relative box: **0 to 4 tiles** ahead of the attacker’s centre, and **strictly under 2 tiles** of sideways offset. Power and knockback then go through the shared hurt routine. Offline, S runs a 5-tick sword counter and cuts a bush in front on the first frames (`player-mannerisms-live.md`).

## Death and respawn **[bin]**

When hearts fall to 0 or below:

1. Hearts are clamped to 0; the hurt counter is set to **0**; mode returns to normal; life-state becomes **dead** (value 2).
2. `dead.wav` plays; inventory is partly spilled as floor items (rupees in 100/30/5/1 bands, arrows and bombs similarly).
3. Each tick while dead: if the counter is under **30** it increments by one (so it stops at 30). Between counters **4 and 27** the client cycles death sprites. Above **29** a cleanup helper runs.
4. **STATUS bit 0x08** is included in the prop encoding only when life-state is dead **and** the counter is above **27**.
5. A movement or action key while dead with counter above **27** (or while in life-state 4) runs the respawn routine.

Respawn clears the hurt counter and modes, restores the shared heart field through the same write used when filling hearts to max, warps to the last saved level entry when one exists, and otherwise (online, no saved name) places the player at **x 30.5, y 30.0**. Offline without a saved entry uses the built-in start-level table. No separate “respawn” packet exists on this path.

## Wall / walk test **[bin]** **[lab]**

Ordinary walking uses a facing step scaled by the move speed (0.5 tile per tick when unburdened; 0.2 when hidden; other multipliers for horse/shield). The candidate position is tested with **six** probe offsets from a facing table against the tile/NPC block test. A failed probe refuses that step. The blocked-step counter that drives the push pose still uses the **18 / wrap-at-38→18** rule already measured live for 1.39. Sliding along a blocking NPC at 0.125 tile/tick was seen live; it is a consequence of the same probe path, not a separate rule.

Knockback reuses the block test with its own twelve-point body box (centre near X+1.5, Y+2.0), matching the later 2.05 layout in spirit.

## What Seihai should change

See `seihai-gaps.md` (updated in the same change): for a 1.39 profile, use the 2.05 death timer and sword box, keep hurt lock-out at 40, prefer **five** knockback steps from the binary (not the earlier four-tile live cell), restore hearts to **max** on respawn (no AP bands), and keep the six-probe walk / 18–38 push counters already shared with later builds.

## Still open

- Exact numeric contents of the six walk-probe and twelve knockback-probe tables (offsets only; behaviour above does not need them for Seihai’s current box tests).
- A fresh Wine knockback distance re-measure to reconcile the five-step binary with the four-tile live cell.
- 1.32 and 1st Graal (next rows of matrix unknown #1).
- Online GServer13 capture of STATUS bit timing and CLAIMPKER (id 14) on a real death; not required to tag the client-side rules above.
