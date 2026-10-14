# Tile walk and collision

Date: 2026-10-14

Derived from observed client behavior and format documentation. No decompile material.

## Sheet selection

The client loads tile sheets from lines of the form `image,prefix,type[,x,y]`. The default sheet is `pics1.png` with type 0. A type-0 sheet is the primary walk surface. Type 1 and type 2 sheets use a different grid.

## Collision rules

- Wall tiles block movement. In the observed type tables, wall is type ≥ 20.
- Water does not block movement. Water is type == 11. It changes display and may affect swimming state.
- Type 0 tiles are walkable only if their id appears in one of two internal allow lists (the “nowall” lists). Tiles absent from both lists are treated as blocking.
- Type 1 and type 2 tiles use a fixed grid: one extraction counted 1,725 blocking and 2,371 walkable cells.
- Throw skip is type 0x14. Shapes above type 19 block.

## Offline implication

An offline session that already rejects moves onto wall tiles and tracks water is exercising the same rules the original client uses. The remaining work is selecting the correct sheet for the current level and applying the type-0 allow lists when the sheet is type 0.

## Stamp notes

Stamp id 0 is a 4×4 ground fill. Stamp id 1 is a hole and is not written. The 2×2 Bush stamp writes ids 2, 3, 18, 19. These are the same ids that appear in the type-0 walk tables.
