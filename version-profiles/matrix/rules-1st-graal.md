# 1st Graal death, hurt, knockback, sword reach and wall test

Date: 2026-11-01. Closes matrix unknown #1 for **1st Graal** (era A). **1.32 stays open** (no decompile; see the end).

Tags: **[bin]** from a static read of the 1st Graal client export (plain behaviour only). The export is the VCL-lossy one already noted in `../../client-internals/early-clients.md`: a few hundred functions, most of them the Delphi library, with the player rules recovered from the routines at the end. Counters are in the 50 ms tick already surveyed for every Delphi build. Where the export's comparisons disagree with themselves, that is called out and not tagged as a number.

Compared with `rules-139.md`. 1st Graal has no AP bar, no ganis, and no later STATUS property.

## Summary

| Rule | 1st Graal | 1.39 (for contrast) | Tag |
|---|---|---|---|
| Hurt lock-out | action mode 3 for 40 ticks; a new hit is refused while that mode lasts | same 40 | **[bin]** |
| Knockback steps | one step per tick while the shared counter reads 39 down to 35 (five steps); twelve probes; a blocked step is undone | same five steps | **[bin]** |
| Knockback direction | baddy and projectile hits store an axis unit step from the attacker's facing; a sword hit stores the centre-to-centre delta | unit vector; a zero vector becomes one tile east | **[bin]** |
| Hurt drawing | full hurt body while the counter is above 30; odd counters blink to a single frame | pose ~10 ticks, then blink **[lab]** | **[bin]** |
| Sword reach | swing frames 6 to 10; ahead by up to 4 tiles; sideways strictly under 2 | 0–4 ahead, sideways under 2 | **[bin]** |
| Sword power | half a heart, fixed | not a fixed half heart in the later profile | **[bin]** |
| Death | hearts at or below 0: clamp to 0, clear the counter and the action mode, life-state becomes dead | same clamp; then a 30-tick timer | **[bin]** |
| Restart after death | a key, once the shared counter is above 27, reloads `house1.graal` at x 24.5, y 30 with hearts and the heart cap both set to 3 | saved entry, or (30.5, 30) online; hearts to max | **[bin]** |
| Wall test | six probes; a blocked step uses the push counter, which wraps from above 37 back to 18; at 18 a ledge test starts an 8-tick hop | six probes; same 18 / wrap-at-38 push counters | **[bin]** |

## Hurt and knockback **[bin]**

A hit is refused while the action mode is already 3. Sword hits, baddy touches and the projectile hits below all use one entry:

1. If the player is carrying something, that carry is dropped.
2. Action mode becomes 3 and the shared counter becomes 40.
3. Hearts change by the hit's power (negative hurts). Hearts are a fractional count. They do not rise above the integer heart cap. At or below 0, the death path below runs, and it clears the mode and the counter that this entry just set.
4. A knockback step is stored.

The hurt tick then drops the counter by one. At 0 the action mode returns to normal. While the counter is still above 34 after that drop (readings 39 down to 35), the player moves by the stored step. Twelve points, four groups of three, are tested against the block test; if any is blocked, that tick's step is undone.

Walking is also refused during hurt while the counter is still at least 30. Below that, and until the counter hits 0, walking is allowed again but a new hit is still refused.

Drawing, while the counter is above 30, uses the hurt body. An even counter, or any counter still above 34, draws the full hurt frame list; an odd counter at or below 34 draws a single frame. Once the counter is 30 or below and the mode is still hurt, the normal body is drawn, and odd counters again draw only one frame.

Baddy touch and the common projectile hit store an axis-aligned step of length 1 from the attacker's facing: facing 0 decreases Y, facing 1 decreases X, facing 2 increases Y, facing 3 increases X. A sword hit instead stores the delta between centres (victim minus attacker). The export then scales that delta by its length, but the length adjustment is applied twice to the horizontal component and the vertical component is left at the half-delta, which is the same class of bad assignment this export shows elsewhere. Direction "away from the attacker" is tagged. Unit length for a sword knockback is not.

There is no "zero step becomes one tile east" in these stores.

Powers that reach this entry:

- Sword, and a baddy touch: half a heart.
- A baddy touch counts when both axes are within 1 tile of the body centres (player centre at x+1.5, y+2; baddy centre at x+1, y+1).
- Two projectile types (sprites 65 and 261) hurt by half a heart; the other types in that list hurt by one heart. The same 40-tick mode is used.
- An arrow whose sprite is 107 to 110 is blocked, instead of hurting, when its direction is the opposite of the player's facing and the player's sprite index is below 6. Otherwise an arrow hurts by half a heart.

## Sword reach **[bin]**

Another player's swing is tested only while the local life-state is the normal value. The other player's packed sprite keeps the facing in the low two bits and the frame above that. A hit is possible only on frames 6, 7, 8, 9 and 10.

The box is facing-relative, measured between centres (each centre is x+1.5, y+2). The victim must sit ahead of the attacker, by a span of 4 tiles, and the sideways distance must be strictly under 2. On two facings the export includes both ends of the 4-tile span; on the other two the ends are exclusive. That split is treated as decompiler noise. The tagged reach is "up to 4 tiles ahead, sideways strictly under 2", the same shape as 1.39, and the exact 0 and 4 edges are not tagged.

Power is half a heart, not a sword-power scale. 1st Graal's sword does not grow.

## Death and the restart **[bin]**

When hearts fall to 0 or below, the heart write:

1. Clamps hearts to 0.
2. Clears the shared counter and the action mode.
3. Sets the life-state to dead.
4. Notifies the relay object when one exists. The payload was not read. There is no later-style STATUS property on this client, and this path does not spill the inventory.

The dead life-state changes drawing: the tile buffer is replaced by a filled rectangle, and a text panel is drawn. The body uses one fixed sprite (index 157) only once the shared counter is above 27. Before that, with the action mode already cleared, the normal body is drawn.

A keypress while dead restarts the player once that counter is above 27. The same restart also runs for one other life-state (value 4), with no counter test. The key index handled before this test does not restart; the other indexes do. The restart is the new-game setup, not a saved `Graalsav1` entry:

- Level `house1.graal`.
- Position x 24.5, y 30. The second local player is shifted 12 tiles toward increasing X (x 36.5, same y).
- Facing 2 (increasing Y).
- Hearts set to 3, and the heart cap set to 3, whatever the cap was before.
- Carry, counter and action mode cleared.

The loop that advances the shared counter while dead was not found in this export. Death itself sets the counter to 0, and both the dead sprite and the restart key wait for a reading above 27. A 30-tick cap, of the kind 1.39 has, is therefore not tagged. No death sound is on this path; this build has no sound engine.

## Wall and walk test **[bin]**

The step added for a facing comes from a per-facing table. The length is not an immediate in the routine. The offline run already measured 0.5 tile per tick (`live-runs-2026-10-30.md`); that measurement is not re-done here.

The candidate point is tested with six probes. The block test fails closed: a point is blocked when an object's box contains it, when it lies outside the 64 by 64 board, when either coordinate is below half a tile, or when the tile is not on the passable-tile list. The list itself was not copied out.

If any of the first four probes is blocked, the action mode becomes the push mode and the stepped axis is undone. A fractional part on the free axis is snapped (facings 0 and 2 snap Y down; facings 1 and 3 snap X onto a half-tile). A particular pattern of the six probes instead adds a nudge from a second per-facing table; the nudge offsets were not read. A nudged step clears the push counter. A plain blocked step increments it.

The push counter wraps: a reading above 37 is set back to 18. When the counter is 18 and a ledge-tile test passes, the action mode becomes the hop and the counter becomes 8. The hop then follows a facing table for those 8 ticks and returns to the normal mode. While pushing, once the counter is above 17 and the player is not carrying, the body sprite steps through the push frames.

## What Seihai should change

See `seihai-gaps.md`. Seihai has no era A profile. When one is added, the 1.39 / 2.05 combat row is the wrong default: sword power is a fixed half heart, hurt is 40 ticks with five knockback steps, a killing blow goes straight to the dead life-state, and the death key restarts `house1.graal` at (24.5, 30) with 3 hearts rather than restoring a saved cap. The walk test is already the six-probe, push-counter family.

## 1.32

Not tagged: a listing of the Decompile folder on 2026-11-01, client exports and the Accessories folder, still has no 1.32 export, so no death, hurt or wall number is added.

## Still open

- The routine that counts the shared counter up while dead, and whether it stops at 30.
- Exact inclusion of the 0-tile and 4-tile edges of the sword box, and unit length of a sword knockback.
- The six walk-probe offsets, the corner-nudge offsets, and the numeric walk-step table (the 0.5 tile step is the live measurement only).
- 1.32 for all five rules, and the rest of eras A and B.
