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

2.05 rev 2 **does** contain the `GRMAP001` string and a reader for it that knows `WIDTH`, `HEIGHT`, `GENERATED`, `GENSEED`, `GENBASE`, `GENEVENBORDERS`, `GENHEIGHT`, `GENCHAOS`, `LEVHEIGHT`, `LEVCHAOS`, `MAPIMG`, `HEIGHTMAP`…`HEIGHTMAPEND`, `RANDOMSEEDS`…`RANDOMSEEDSEND` and `HEIGHTS`, plus a `TGraalMap` class. No static caller of that reader was found, so it may be dormant. 2.05 has no `PLO_PLAYERWARP2` handler (49 is missing from its jump table) and no `gmaplevelx` prop name. It references `bigmap.txt` and `minimap.txt` and has the GS1 commands `setmap`/`setminimap`/`loadmap`, so the text big-map and minimap overlays are the active path in 2.05. **[2.05]** (An earlier version of this note said 2.05 had no `GRMAP001` string; that was wrong. `client-internals/build-catalogue.md` also lists GRMAP001 for 2.05.) The format of `bigmap.txt`/`minimap.txt` is still open. GServer's `PLO_BIGMAP` (171) and `PLO_MINIMAP` (172, e.g. `zodiacminimap.txt,zodiacworldminimap3.png,10,10`) are the later server-pushed versions.
