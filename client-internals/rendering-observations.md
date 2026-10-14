# Rendering observations

Date: 2026-10-14

Derived from observed client behavior and the public DirectX notes. No decompile material.

## Frame loop

The client runs an idle handler that gates on a 50 ms timer, then a frame function that handles clock skew, network, and draw. A stall is one frame; there is no catch-up burst.

## Draw path

- The frame function calls a draw routine that uses the current tile sheet.
- The device object exposes viewport, material, projection transform, and ambient render state.
- Supported drop suffixes for images include `.txt`, `.gif`, `.png`, and `.mng`.

## Tile sheet

The active sheet is selected from the loaded list (default `pics1.png`, type 0). An offline session that already draws an ASCII or PPM view of the board can replace that view with a blit of the selected sheet once the type-0 allow lists and the stamp vocabulary are applied.

## Offline implication

The next useful increment remains small: blit one stamp from `pics1` using the sheet that the client would have selected, then wire `playertouchsme` to actually hide or warp. After that the offline session starts to look like a level instead of a parser.
