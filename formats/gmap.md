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

2.05 has **no** `GRMAP001` string, no `PLO_PLAYERWARP2` handler (49 is missing from its jump table), and no `gmaplevelx` prop name. It does reference `bigmap.txt` and `minimap.txt`, has the GS1 commands `setmap`/`setminimap`, and has a `TGraalMap` class (probably the big-map overlay). So 2.05 predates gmaps and uses the older text big-map and minimap overlays instead. **[2.05][inf]** The format of `bigmap.txt`/`minimap.txt` is still open. GServer's `PLO_BIGMAP` (171) and `PLO_MINIMAP` (172, e.g. `zodiacminimap.txt,zodiacworldminimap3.png,10,10`) are the later server-pushed versions.
