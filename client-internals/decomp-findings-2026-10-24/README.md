# Decompile findings, 2026-10-24 (derived facts only)

Built from three Ghidra decompiles (2.05 rev2, Graal 1.39, 1st Graal). Nothing here quotes code or addresses.

| File | Topic |
|---|---|
| 01-death-respawn.md | zero-hearts handler, respawn, damage rules |
| 02-sprites-poses-emotes.md | sprite prop, poses, swim, emotes |
| 03-player-list-popup.md | F7 list, popup, PM recipients, TPersonAction |
| 04-sword-hitbox.md | sword swing and hit evaluation |
| 05-205-props-misc.md | other 2.05 facts |
| 06-first-graal.md | 1st Graal protocol summary |
| 07-graal-139.md | 1.39 protocol summary |
| 08-contradictions.md | new facts and contradictions |

Tables (TSV): sprite-step-table, gani-to-step, gani-name-table, gani-short-codes, status-bits-prop18, player-modes, life-states, constants-205.

## Gaps still open
- Wire representation of swim (none found) and how others see emotes.
- Damage formula (inferred sword power / 2).
- Meaning of a few unlabelled mode values. (Status bit 0x20 is now answered: `../status-bit-0x20.md`.)
- Exact "same name group" rule for the saved respawn point.
- 1st Graal room-name branch selection; 1.39 popup, death and sword.
