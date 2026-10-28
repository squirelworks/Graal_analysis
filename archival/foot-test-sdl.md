# Foot test (SDL reimplementation)

Date: 2026-10-14 (archived 2026-10-28)

Derived from the SDL reimplementation of the client movement loop and the type table. This is **not** the real client's walking test.

The real clients (2.05 through 2.31) use a six-probe body-box routine with corner nudges and flush snaps. See Seihai `documentation/walking-collision.md` for the current description.

## Single-point test (SDL)

Arrow keys set a pixel step of `16 * 0.30` and a sprite direction (0 up, 1 left, 2 down, 3 right). The wall test is a single point:

```
testx = (pixelX + moveX + 32) / 16
testy = (pixelY + moveY + 44) / 16
```

If `isOnWall(testx, testy)` is false, the new position is accepted. If true, the step is rejected. There is no slide, no corner resolution, and no water slowdown in this loop.

## Predicates used by the SDL path

- Outside the board on x or y: wall.
- Inside: type byte at `levelTiles[round(y)*64 + round(x)]` ≥ 20 is wall; type == 11 is water (does not block).
- Chair, bed, swamp, and lava types are stored and ignored by this path.

The 2×2 Bush stamp writes ids 2, 3, 18, 19. Those type bytes are 20/22, so the bush is wall under this path.
