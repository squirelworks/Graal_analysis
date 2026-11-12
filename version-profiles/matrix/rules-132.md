# 1.32 death, hurt, knockback, sword reach and wall test

Date: 2026-11-12. Closes matrix unknown #1 for **1.32** (era B). Before this, 1.32 was marked as having no decompile. A 1.32 client export does exist in the private working set, so this note is a static read of it. No lab run was needed.

Tags: **[bin]** from a static read of the 1.32 client export. Only plain behaviour is given here, with no addresses. Tick = 50 ms, the same as every Delphi build already surveyed. Where the export's numbers cannot be read (values the decompiler leaves on the FPU stack), that is called out and not tagged.

Compared with `rules-139.md` and `rules-1st-graal.md`.

## Summary

| Rule | 1.32 | 1.39 (for contrast) | Tag |
|---|---|---|---|
| Hurt lock-out | action mode 3 for 40 ticks; a new hit is refused while that mode lasts | same | **[bin]** |
| Knockback steps | one step per tick while the counter reads 39 down to 35 (five steps); twelve body probes; a blocked step is undone | same | **[bin]** |
| Knockback direction | baddy touch stores a unit step from the baddy's facing table; a sword hit stores half the centre-to-centre delta, with the same broken normalisation as 1st Graal | unit vector; a zero vector becomes one tile east | **[bin]** |
| Hurt drawing | hurt body while the counter is above 30; odd counters at 34 or below blink | pose ~10 ticks, then blink **[lab]** | **[bin]** |
| Sword reach | swing frames 6 to 10; up to 4 tiles ahead; sideways strictly under 2 | 0–4 ahead, sideways under 2 | **[bin]** |
| Sword power | passed in with the swing (not a fixed half heart) | same | **[bin]** |
| Baddy touch | within 1 tile on both axes; half a heart, one heart for one baddy type | same powers | **[bin]** |
| Death timer | counts 0 → 30 and stops; death sprites cycle between 4 and 27 | same | **[bin]** |
| Input while dead | a movement or action key respawns once the counter is above 27 (or in life-state 4) | same | **[bin]** |
| STATUS dead bit (0x08) | set when dead **and** the counter is above 27 | same | **[bin]** |
| Online default respawn spot | x 30.5, y 30.0 when there is no saved level | same | **[bin]** |
| Respawn hearts | written through the shared heart setter; the value is not readable in the export | max hearts | not tagged |
| Wall test | six probes per facing step | six probes | **[bin]** |
| Push counter | hop check at 18; counter wraps from above 37 back to **28** | wraps 38 → 18 | **[bin]** |
| Walk speed | facing step × 1.0; 0.2 hidden; 0.4 for one carry pose; 1.2 with a high item level; horse 0.8 and up | 0.5 tile/tick; 0.2 hidden | **[bin]**; 0.5 tile/tick **[live]** |

## Hurt and knockback **[bin]**

A hit is refused while the action mode is already 3. An accepted hit sets mode 3 and the counter to **40**, changes hearts by the hit's power, and stores a knockback step.

Each playing tick in mode 3, the counter drops by one. At 0 or below, the mode returns to normal. While the counter is above 34 after that drop (readings 39 down to 35), the player moves one step along the stored vector. Twelve body points (four edges of three) are then tested against the block test, and if any is blocked that tick's step is undone. This is the same five-step window as 1.39 and 1st Graal.

The hurt body is drawn while the mode is 3 and the counter is above 30. At 34 and below, odd counter values blink.

Knockback direction:

- **Baddy touch:** a unit step taken from the baddy's facing table.
- **Sword hit:** half of the centre-to-centre delta (victim minus attacker). The export then divides the horizontal part by the length twice and leaves the vertical part un-normalised. This is the same flaw already seen in the 1st Graal export. "Away from the attacker" is tagged; unit length is not.
- There is no "zero step becomes one tile east" rule on these paths.

## Hearts, damage and death **[bin]**

The heart setter caps hearts at the heart maximum. Damage is refused in life-state 1 and in action mode 13 unless the caller forces it. Healing plays no sound. A hit that is not fatal plays the character's own hurt sound from `sounds\`.

When hearts reach 0 or below:

1. `dead.wav` plays.
2. The counter and the action mode are cleared, and the life-state becomes dead (value 2).
3. Up to 1000 rupees are dropped as floor items in bands of 100, 30, 5 and 1.
4. Darts and bombs are each capped at 95 and dropped in fives. Afterwards the player is left with 5 darts and 10 bombs.

Each dead tick, the counter increases by one while it is under 30. Between counters 4 and 27 the facing spins, which is the death animation. The STATUS dead bit (0x08) is set only when the player is dead and the counter is above 27.

A movement or action key respawns the player once the counter is above 27. Life-state 4 also respawns, with no counter test.

## Respawn **[bin]**

Respawn:

- Resets the heart field through the shared heart setter.
- Clears the counter, carry and action modes.
- Clears the ten-slot flag array.
- Warps to the saved level entry when one exists, keeping the saved position and facing.

With no saved entry:

- **Online:** the player is placed at **x 30.5, y 30.0** in the current level.
- **Offline:** a built-in start-level table is indexed by game mode. If that level file is missing, the start level from the options is used instead. The facing is set from the same table (3, 1 or 2).

Online, or in game mode 0, respawn also shows the player's name for 60 ticks.

The value written to hearts is passed on the FPU stack and is lost in the decompile. The heart-container pickup on this build uses the same setter right after it reads the heart maximum ("fill to max"), and 1.39 fills to max. That points to max hearts here too, but it is not tagged. 1.32 has no AP bar.

## Sword reach **[bin]**

Another player's swing is tested only when the local player is not already in mode 3, and only on swing frames **6 to 10**. The box is facing-relative between centres (each centre is x+1.5, y+2). The victim must be ahead by up to **4 tiles**, and the sideways offset must be strictly under **2**. On two facings the ends of the 4-tile span are inclusive, and on the other two they are exclusive, the same split seen in 1st Graal. The exact 0 and 4 edges are not tagged. Power is the value passed with the swing, so it is not 1st Graal's fixed half heart.

## Baddy touch **[bin]**

A baddy hurts when both axes are within 1 tile, measured from the baddy centre (x+1, y+1) to the player centre (x+1.5, y+2). Power is half a heart, or one heart for one baddy type. The type numbering differs from 1.39's, so that type is not mapped here. The counter becomes 40 and the mode becomes 3.

Two timed effects use the same heart setter:

- One standing pose heals half a heart every 100 ticks.
- One tile condition hurts half a heart every 100 ticks. That hurt is forced, so it ignores the refusals above.

## Wall and walk test **[bin]**

A walking step is the facing step from the step table, scaled by a speed factor:

| Factor | When |
|---|---|
| 1.0 | normal walking |
| 0.2 | hidden mode |
| 0.4 | one carry pose |
| 1.2 | a high item level |
| 0.8 and up | on a horse, rising with the horse's speed |

The live runs measured 0.5 tile per tick in 1.32 (`live-runs-2026-10-30.md`), so the table's base step is half a tile. The candidate position is tested at **six** probe offsets from a per-facing table. Separate probe routines are used on a horse.

A blocked step adds one to the push counter, and a free step resets it to 0. In walking mode:

- At **18**, if the ledge test passes, the player hops: the action mode becomes the hop mode, the counter is set to 8 and `jump.wav` plays.
- Above **37**, the counter goes back to **28**. 1.39 and 1st Graal wrap to 18 instead.
- From 18 on, the push pose is 14 + (counter − 18) / 4. With the wrap to 28, a long push cycles the last three push frames instead of all five.

## What Seihai should change

For a 1.32 row, use the 1.39 rules with these differences:

- The push counter wraps above 37 to **28**, not 18.
- Sword knockback is "away from the attacker" with no zero-vector rule.
- The respawn heart value is unconfirmed; use max hearts, as in 1.39, until it is confirmed.

Seihai has no era B profile yet, so nothing in Seihai changes now.

## Still open

- The value respawn writes to hearts (needs the raw instruction bytes or a Wine run).
- The exact numbers in the six walk probes and twelve knockback probes.
- Which baddy type gets the one-heart touch, and how it maps to 1.39's type 7.
- The rest of eras A–B (1.0, 1.1, 1.21–1.31).
