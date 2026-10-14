# Offline play notes

Date: 2026-10-14

## Requirement
Seihai must support playing levels offline (no listserver / gserver connection).

## Observations from original client
- Tutorial levels are embedded in the executable (not loaded from disk).
- `2dadventureclient` already demonstrates local player + level simulation using the shared game object model.
- Level files, GANIs, NPCs, and links can be loaded from a local `levels/` tree.
- The original client’s editor (F4) and snapshot features operate on local level data.

## Current status
- `.nw` parser + board-modify applicator (`Level::apply_board_modify`).
- `OfflineSession` can load a level and apply `BoardModify` updates.
- GANI parser extracts SPRITE defs, ANI frames (placements), and DEFAULT* fields.

## Remaining for offline play
1. Tile collision using the parsed boards.
2. NPC script execution (seihaiscript).
3. Rendering the tile data.
