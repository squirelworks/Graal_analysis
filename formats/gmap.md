# GMAP (GRMAP001) as read by servers and clients

Date: 2026-10-21

Sources: GServer-v2 `TMap.cpp` (GPLv3, summarized); 2.05 string table; `grmap001.txt` (writer side). Tags as elsewhere.

`grmap001.txt` covers the three **writers** (dungeon generator, terrain generator, GraalLevelGen). This note covers the **reader** keys.

## Keys read by GServer **[srv]**

| Key | Args | Meaning |
|-----|------|---------|
| `GRMAP001` | — | signature (first line) |
| `WIDTH` / `HEIGHT` | n | grid size in levels |
| `GENERATED` | 1 arg | read and stored. Not used to rebuild names on the server side |
| `LEVELNAMES` … `LEVELNAMESEND` | one row per line, quoted, comma-separated names | grid fill, row-major. Names are lowercased for lookup |
| `MAPIMG` | file | overview image |
| `MINIMAPIMG` | file | minimap image |
| `NOAUTOMAPPING` | — | flag |
| `LOADFULLMAP` | — | flag: preload every level |
| `LOADATSTART` … `LOADATSTARTEND` | name list | levels to preload |

Each line is tokenized on whitespace after stripping `\r`. Lines inside the `LEVELNAMES` block are gs-untokenized (quoted CSV). **[srv]**

## On the wire

A player on a gmap has `PLPROP_CURLEVEL` = the gmap name and `PLPROP_GMAPLEVELX`/`Y` = the grid cell. `PLO_PLAYERWARP2` (49) carries x, y, z, then the gmap cell x and y. `PLI_ADJACENTLEVEL` (35) preloads neighbors. **[srv]**

## 2.05

2.05 contains a `GRMAP001` reader (it knows `WIDTH`, `HEIGHT`, `GENERATED`, `GENSEED`, `HEIGHTMAP`, `RANDOMSEEDS` and the rest), but no caller for it was found, so it is probably dormant. **[2.05]** In practice 2.05 uses `bigmap.txt`/`minimap.txt`. It has no `PLO_PLAYERWARP2` handler (49 is missing from its jump table), and no `gmaplevelx` prop name. It does reference `bigmap.txt` and `minimap.txt`, has the GS1 commands `setmap`/`setminimap`, and has a `TGraalMap` class (probably the big-map overlay). So 2.05 does not play gmaps and uses the older text big-map and minimap overlays instead. **[2.05][inf]** The `bigmap.txt`/`minimap.txt` format is described below. GServer's `PLO_BIGMAP` (171) and `PLO_MINIMAP` (172, e.g. `zodiacminimap.txt,zodiacworldminimap3.png,10,10`) are the later server-pushed versions.

## 2.05 big map and minimap text files **[2.05]**

**Defaults:**
- Big map: `bigmap.txt` with image `map.png`.
- Minimap: `minimap.txt` with image `map2.png`.
- Each map also has a few built-in integers. For the big map they are 10, 16, 1688 and 1024; for the minimap they are 664 and 896.
- In training (offline tutorial) mode the client switches to `tutorialmap.txt` and `tutorialmap.png`, with 3, 4, 192 and 486.

**Format:** plain text, one map row per line.
- Each line is parsed as a comma-separated list (Delphi `CommaText`, so quoting is allowed).
- Each cell is normalised and appended to one flat list.
- The column count is the number of cells on the **first** line, and the row count is total cells ÷ columns.
- A cell is a level file name; `x` marks an empty cell.
- The shipped `bigmap.txt` is 20 columns × 21 rows of quoted level names. The loader builds a map object of that grid with the image file name attached.

**Per-server override:** a server-list entry with more than the usual 8 fields can replace these settings.
- Field 8 is the big-map file and field 9 its image. Fields 10 and 11 are two integers.
- Field 12 is the minimap file and field 13 its image. Fields 14 and 15 are two integers.
- The integers become points in the player object. They are probably image offsets or scale, which fits the default values above, but their use is not traced. **[inf]**

The GS1 commands `setmap` and `setminimap` load the same kind of file from a script.
