# Static reads for Appendix E, second batch (2026-11-20)

Date: 2026-11-20. Evidence: **[bin]** (a disassembler read of the real executables on the Mirae
lab, with no client run). Only behaviour is given here. Covers App. E#209, E#307, E#315 and E#421.

Builds read: 1st Graal, 1.39, 2.05 rev 2 `Graal.exe` and 2.22 for the movement tables; 2.1 test 2,
2.1 test 3 and 2.17.1 for the entry save; the 2004 `RemoteControl.exe` (token `GSERV024`) for
RC 76; and the 5.00r7 `GraalEngine.dll` for the GS2 opcodes.

## 1.39 movement tables (E#307)

The movement constants of each build sit together in one block of doubles: the per-facing step,
the six probe points per facing, and the sideways nudge per facing. The 1.39 block, set beside
1st Graal's and 2.05's:

| Table | 1st Graal | 1.39 | 2.05 rev 2 (and 2.22) |
| --- | --- | --- | --- |
| step (up, left, down, right) | (0, −0.5), (−0.5, 0), (0, +0.5), (+0.5, 0) | same | same |
| up probes, y | 1.05 | 1.0 | 1.0 |
| up and down probes, x | 0.6, 1.4, 1.6, 2.4, 2.525, 0.475 | 0.6, 1.4, 1.6, 2.4, 2.525, 0.475 | 0.525, 1.475, 1.525, 2.475, 2.525, 0.475 |
| left probes, x | 0.55 | 0.5 | 0.5 |
| left and right probes, y | 1.1, 1.9, 2.1, 2.9, 3.025, 0.975 | 1.1, 1.9, 2.1, 2.9, 3.025, 0.975 | 1.025, 1.975, 2.025, 2.975, 3.025, 0.975 |
| down probes, y | 2.95 | 3.0 | 3.0 |
| right probes, x | 2.45 | 2.5 | 2.5 |
| nudge | ±0.125 | ±0.125 | ±0.1 |

- So 1.39 is a step between the two. It keeps 1st Graal's four inner probe points along each edge
  (0.6, 1.4, 1.6, 2.4 and 1.1, 1.9, 2.1, 2.9) and its 0.125 nudge, but already uses 2.05's edge lines
  (1.0, 0.5, 3.0 and 2.5, against 1st Graal's 1.05, 0.55, 2.95 and 2.45).
- 2.05 moves the inner points 0.075 outwards (0.525 to 2.475, 1.025 to 2.975) and makes the nudge 0.1.
- The 1.39 nudge of 0.125 agrees with the live 1.39 run, where walking into an NPC's side moved the
  player 0.125 tile per tick.
- The 2.22 block is byte-identical to 2.05's.
- The probe order (0 to 5) is the same in all three builds, so the nudge and refusal rules that use
  the probe numbers read the same way. Their branch code in 1.39 was not compared instruction by
  instruction.

## Level-entry save in the 2.1 test builds (E#315)

- 2.1 test 2 and 2.1 test 3 run the same entry decision as 2.17.1. The point is saved when the level
  left is empty (the login), or when the product of the two levels' indices in the current gmap's
  list is negative. Otherwise it is not saved.
- There is no name-group test. Unlike 2.05, there is no "different groups: save" step after the
  product test.
- With no gmap, both indices read as −1, as in 2.05.
- So the earlier guess that every entry saves is wrong. Moving between two ordinary levels, or between
  two levels of the same gmap, keeps the old respawn point.

## The last byte of RC 76 (E#421)

- The 2004 RC's player-props dialog builds 76 from the account, the world, the props, the two lists
  and the weapon list. It then appends one more length-prefixed string.
- That string is not a dialog field. When the RC parses the server's 72 for the same player, it reads
  one extra length-prefixed string after the weapon list, if any bytes are left, and keeps it. It
  sends that string back unchanged in 76.
- The one capture had a 72 without that extra string, so the RC stored an empty string and wrote its
  length byte, an encoded 0. That is the "last byte".
- The dialog never edits the string. So it is an optional trailing field of 72 that the 2004 RC copies
  back, and the GServer-v2 72, which ends at the weapons, makes it empty. What an older server put
  there is not known.

## GS2 opcodes 48, 49 and 54 on 5.00r7 (E#209)

- **54** needs at least three values on the stack. It takes the object (deepest), the member name
  and the value (on top). It turns the object into an object reference, copies the name onto it, and
  then runs the same store as opcode 50. So on 5.00r7 it consumes three values, pushed in the order
  object, name, value. The 6.1.1.3 form (drop two, convert the value then on top) is the later
  two-value variant.
- **49** takes a count from the top, rounded down and clamped to 0 to 10000. It then pops up to that
  many values, stopping early if the stack runs out, and appends each to a new list in the order
  popped. So the list comes out in reverse push order: element 0 is the value pushed last, just
  under the count. The list replaces the slot of the last value taken.
- **48** takes a count from the top and builds an object from name and value pairs. In each pair the
  name is pushed first and the value second. The pairs are taken from the top down, and a name already
  set is overwritten.
- The loop counter of 48 counts up instead of down. So 48 does not stop after the given number of
  pairs: with a positive count it keeps taking pairs until two or fewer values remain on the stack.
  The object replaces the slot of the last name taken. A compiler that targets 5.00r7 should therefore
  emit 48 only on an otherwise empty stack. This may be why 48 and 49 were dropped after 5.12.
