# NPC library

Scraped from 1,420 GR-V1 `.graal` levels in `/recycler/trash/Levels/`.

- `npcs.json` — 3,115 unique NPC scripts, sorted by frequency. Each entry has `image`, `script`, `count`, and up to 3 source filenames.
- `tile-patterns.md` — most common horizontal and vertical tile-neighbor pairs from the same levels.

Scripts are the text after `image.gif#` in the binary level. Control characters were stripped. Deduped by script body.

The source levels were discarded after extraction.
