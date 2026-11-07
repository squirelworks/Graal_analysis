# Foot test (movement collision)

Date: 2026-10-14

**Superseded.** This note records the single-point wall test recovered from the SDL reimplementation (2dadventureclient). The real clients (2.05 through 2.31) use a six-probe body-box routine with corner nudges and flush snaps. See Seihai `documentation/walking-collision.md` for the current description, and `archival/foot-test-sdl.md` for the preserved SDL snapshot.

The original content is retained below for reference.

---

Derived from the SDL reimplementation of the client movement loop and the type table. No decompile material.

## Single-point test

Arrow keys set a pixel step of `16 * 0.30` and a sprite direction (0 up, 1 left, 2 down, 3 right). The wall test is a single point, not a box or a sweep:

```
testx = (pixelX + moveX + 32) / 16
testy = (pixelY + moveY + 44) / 16
```

If `isOnWall(testx, testy)` is false, the new position is accepted. If true, the step is rejected. There is no slide, no corner resolution, and no water slowdown in this loop. `isOnWater` exists but is not consulted by the keyboard path.

## Predicates

- Outside the board on x or y: wall (edge is solid until a LINK says otherwise).
- Inside: type byte at `levelTiles[round(y)*64 + round(x)]` ≥ 20 is wall; type == 11 is water (does not block).
- Chair, bed, swamp, and lava types are stored and ignored by this path. Type 12 (old note: lava) is walkable here.

## Stamp consequence

The 2×2 Bush stamp writes ids 2, 3, 18, 19. Those type bytes are 20/22, so the bush is wall. The stamp file itself carries no collision column; the foot test decides after the ids are written.

Official ~2.05 used a different body-block mask and type-0 allow lists. The measured path above keeps only the two predicates.
