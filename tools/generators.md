# Generators

Three writers emit `GLEVNW01` / `GRMAP001`. They do not emit the same file.

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

Do not feed one writer’s output to another’s loader and expect a playable board.
