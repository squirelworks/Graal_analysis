# NPC library

3,172 unique scripts (the scrape reported 3,187, but 15 records were lost to truncated source pages; see `partial_pages` in the `npcs.json` meta), broken into a hierarchy so no single file is large.

**Script bodies are not in this repo.** On 2026-11-04 the `script` field was removed from every record in `page.json` and `npcs.json`, because it was text copied verbatim from the original levels. Page records keep the image name, occurrence count, up to three source level names and `script_chars` (the original body length); `npcs.json` records also keep event and command names and the truncation flag. The full copies are kept outside the repo by the owner (project files, `graal-analysis-audit/moved/npc-library/`, same layout). Notes that need a script should describe it and quote only a short excerpt.

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

`index.json` lists every genre and topic with script and book counts and a short own-words `behaviour` summary; the same summaries are in [behaviours.md](behaviours.md), the spec for rewriting NPCs from scratch.

## Original library

[`scripts/`](scripts/README.md) holds new NPC scripts written from scratch against the behaviour summaries and manual §8, organised by family. None of it comes from the scraped bodies.

## Reference

`reference/` holds the small NPC material from shanalysis:
- `npcControl-NPC.txt` — GServer-v2 control NPC header
- `forcesay.txt` — phoenix execscript

## Tile patterns

`tile-patterns.md` is unchanged.

## Flat file

`npcs.json` is the flat aggregate of the page files (metadata only, as above). The older `npcs.json.bak` flat dump is not tracked.

## GS1 references

- `gs1-commands.md`: cleaned catalog and offline wiring priority.
- `gs1-reference-205.md`: the full 2.05 command and function tables, built-in flags, and constants.
