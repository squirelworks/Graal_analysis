# Generators

Three writers emit `GLEVNW01` / `GRMAP001`. They do not emit the same file.
The Graal 2.22 programs are reimplemented in `generators-222/`.

## TerrainGenerator

Plasma midpoint displacement. Writes:

- `GRMAP001` with `GENERATED`, `GENSEED`, `GENBASE`, `HEIGHTMAP`, `RANDOMSEEDS`, and per-level `HEIGHTS` blocks (9×9).
- `GLEVNW01` levels that are 64 rows of tile 0 plus a `HEIGHTS` overlay and edge `LINK` lines. No NPC section.

## DungeonGenerator

8×11 stamp layout (hand-drawn, style, or DungeonMaker 0.9). Writes:

- One base64 `BOARD` of 64×64, edge `LINK`s, and `NPC` blocks.
- Stamp id 0 is replaced by a 4×4 ground fill before storage. Stamp id 1 is a hole and is not written.
- Short-form `GRMAP001`: `WIDTH`, `HEIGHT`, `GENERATED` (last level name).

## GraalLevelGen

Image-to-linked-levels pipeline. Emits `LEVELNAMES` links. A third writer of the same signatures.

The 2004 graal-txt build and the 2001 nw-txt build write `bigmap.txt` instead of that gmap. Their file names and level containers are in `level-tools-gaps/`. The March 2003 manual does not name water, mountain or sand edge tiles, and `docu_dungeongenerator.txt` does not give DungeonMaker 0.9's crawler steps. Both limits are in that note.

Do not feed one writer’s output to another’s loader and expect a playable board.
