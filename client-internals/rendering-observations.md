# Rendering observations

Date: 2026-10-14

Derived from observed client behavior and public DirectX notes. No decompile material.

## Frame loop

The client runs an idle handler that gates on a 50 ms timer, then a frame function that handles clock skew, network traffic, and draw. A stall is one frame; there is no catch-up burst. The frame function ignores the step count that the pacer may supply.

## Draw path

The frame function calls a draw routine that uses the currently selected tile sheet. The device object exposes:

- viewport
- material
- projection transform
- ambient render state (set to white)

Supported image suffixes observed in the drop path are `.txt`, `.gif`, `.png`, and `.mng`. The default sheet is `pics1.png`.

## Tile sheet and blit

The active sheet is selected from the loaded definition list when the level is entered. An offline session that already draws an ASCII or PPM view of the board can replace that view with a blit of the selected sheet once:

1. The sheet is chosen (default `pics1.png`, type 0).
2. The type-0 allow lists are applied so only walkable tiles are treated as open.
3. The stamp vocabulary is used so a named stamp expands to the correct tile ids.

A single stamp blit (for example the 2×2 Bush) is enough to prove the path. After that, the full board can be blitted from the same sheet.

## Offline implication

The next useful increment remains small:

1. Blit one stamp from `pics1` using the sheet the original client would have selected.
2. Wire `playertouchsme` so that a touch actually hides the NPC or warps the player.

After those two changes the offline session starts to look like a level instead of a parser. Both steps use data and rules already documented in `formats/tile-walk.md` and `npc-library/gs1-commands.md`.
