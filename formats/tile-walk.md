# Tile walk and collision

Date: 2026-10-14

Derived from observed client behavior, public tiletype tables, and format documentation. No decompile material.

## Sheet loading

The client reads a tile definition list. Each entry is `image,prefix,type` with optional `x,y` offsets. The default sheet is `pics1.png` of type 0. Type 0 is the primary walk surface used by most classic levels. Type 1 and type 2 sheets use a separate rectangular grid for collision.

A level may reference multiple sheets. The active sheet is selected when the level is entered. Offline sessions that already load a GLEVNW01 board can select the same default sheet.

## Collision rules

Observed type meanings:

- Type ≥ 20 blocks movement (wall).
- Type == 11 does not block movement (water). It changes the displayed tile and may set a swimming flag.
- Type 0 tiles are walkable only when their 12-bit id appears in one of two internal allow lists (commonly called the “nowall” lists). An id absent from both lists is treated as blocking even if the sheet is type 0.
- Type 1 and type 2 tiles consult a fixed grid. One extraction of that grid counted 1,725 blocking cells and 2,371 walkable cells.
- Throw skip is type 0x14. Objects whose shape type is above 19 block.

These rules match the offline session’s existing behavior of rejecting moves onto wall tiles and tracking water without blocking.

## Type-0 allow lists

The two allow lists are populated when the sheet is loaded. They contain the tile ids that the original client treats as non-blocking on a type-0 sheet. The lists are not stored in `tiledefs.txt`; that file only names the sheet, prefix, and type. An offline session that wants exact classic walk behavior must either embed the same allow lists or derive them from a known-good `pics1` extraction.

One exported type-0 mask counted 3,195 non-blocking tiles and 682 blocking tiles. The type 1/2 grid counts above are independent of that mask.

## Stamp vocabulary

Stamp id 0 is a 4×4 ground fill. Stamp id 1 is a hole and is never written. The 2×2 Bush stamp writes the four ids 2, 3, 18, 19. These ids appear in the type-0 walk tables and are therefore walkable when the sheet is type 0. A generator or editor that places stamps by name can emit the same ids without inventing tile codes.

## Offline next step

The offline session already rejects wall tiles and tracks water. The remaining collision work is:

1. Select the sheet the original client would have selected (default `pics1.png` type 0).
2. Apply the type-0 allow lists when the sheet is type 0.
3. Fall back to the type 1/2 grid for other sheets.

Once that is done, walking an offline level exercises the same collision path the online client uses.
