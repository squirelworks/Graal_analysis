# NPC library

3,187 unique scripts, broken into a hierarchy so no single file is large.

## Structure

```
genre / topic / book-NN / chapter-NN / page.json
```

- **Genre** — combat, transport, object, dialogue, spawn, interaction, misc
- **Topic** — targets, hazards, baddies, weapons, level-warps, local-warps, signs, doors, chests, blocks, speech, timers, visibility, flags, triggers, other
- **Book** — up to 100 scripts
- **Chapter** — up to 25 scripts
- **Page** — one `page.json` per chapter

## Counts

| Genre | Scripts | Topics |
|-------|--------:|--------|
| combat | 1,400 | targets (728), baddies (452), hazards (192), weapons (28) |
| interaction | 602 | triggers (411), visibility (180), flags (11) |
| dialogue | 373 | speech (373) |
| spawn | 328 | timers (328) |
| misc | 257 | other (257) |
| object | 168 | doors (108), blocks (35), signs (15), chests (10) |
| transport | 59 | local-warps (32), level-warps (27) |

## Index

`index.json` lists every genre and topic with script and book counts.

## Reference

`reference/` holds the small NPC material from shanalysis:
- `npcControl-NPC.txt` — GServer-v2 control NPC header
- `forcesay.txt` — phoenix execscript

## Tile patterns

`tile-patterns.md` is unchanged.

## Flat file

`npcs.json.bak` is the original 1 MB flat dump, kept for reference. Use the hierarchy.

## GS1 references

- `gs1-commands.md`: cleaned catalog and offline wiring priority.
- `gs1-reference-205.md`: the full 2.05 command and function tables, built-in flags, and constants.
