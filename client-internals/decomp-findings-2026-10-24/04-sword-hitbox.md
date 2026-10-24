# 2.05 rev2: sword swing and hit box (derived)

## Starting a swing
Preconditions: weapons allowed by the level or server, sword power not 0, not swimming without a horse, and not already in the charged-spin mode.
- Normal swing: mode 6. Charged spin: mode 13 (0xd); needs the has-spin flag.
- Plays the sword, ridesword or spin gani and a sound, then checks for a cuttable bush at the sword tip.
- The sprite sent to others follows steps 9 to 13 (sprites 6 to 10) of the swing; see `02-sprites-poses-emotes.md`.

## Who decides a hit
The **victim's client** evaluates the hit and applies damage. The attacker only broadcasts its position, direction and sprite.
A hit counts when all of these hold:
- the attacker is on step 9 to 13 (sprites 6 to 10);
- the victim is 0 to 4 tiles ahead of the attacker in the facing direction;
- the sideways offset is under 2 tiles;
- the victim's AP is not exactly 100 (such players cannot be hit);
- the victim is currently hurtable (not in mode 3, mode 10, dead or editor).

## Damage
Inferred: sword power divided by 2 in hearts. Not confirmed from a capture.

## Explosions
A bomb hit needs the victim within 1 tile on both axes of the blast, with knockback of 0.5 or 1.0 tile.

## Gaps
- Exact damage formula and the timing of the swing frames in milliseconds are not confirmed; frame durations come from the gani files, not the client.
