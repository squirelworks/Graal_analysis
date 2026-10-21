# Offline training levels

Date: 2026-10-14

Derived from observed client behavior. No decompile material.

## Observation

Tutorial levels are embedded in the executable. They can be drawn and walked without a network connection. The client does not require a listserver or gserver to enter them.

## Difference from session levels

The global that holds the current level name is set only by the session “set level” message (the byte that arrives after a successful world login). Offline training levels never set that global. A debugger session that shows a training level drawn while the level pointer remains null is expected and correct.

## Enter path

Entering a training level stores the level name on the player object and the arrival coordinates. Nearby links (for example to a house interior) are present in the embedded data. The same collision and script paths used by disk levels are used here.

## Offline implication

An offline session that loads a GLEVNW01 file from disk is already past the embedded-tutorial case. The same collision, sign, and script paths apply. The only difference is the source of the level data (disk versus embedded).

The offline slice therefore does not need to special-case training levels. It only needs to:

1. Load a level from disk (already done).
2. Apply the tile walk rules (see `formats/tile-walk.md`).
3. Execute the common GS1 commands on touch (see `npc-library/gs1-commands.md`).
4. Blit the selected sheet (see `rendering-observations.md`).

Once those four are in place, both embedded training levels and disk levels will behave the same way.


See `offline-tutorial-205.md` for the 2.05 details: the *Play offline* path, the resource lookup, and the level-by-level contents.
