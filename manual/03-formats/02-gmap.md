<!-- manual: kind=reference status=draft -->
# 3.2 GRMAP001 and gmaps

A gmap is a grid of levels that the client walks across without a level warp. Its file is `GRMAP001` text. The 2.05-era text big map and minimap, which name a grid of levels for the map screen only, are a different format and are in → §3.2.4. How a client crosses a gmap edge on the wire is in → §4.10.

> Status: draft. The server reader and three tool writers are summarised; the 2.05 reader is read statically and may be dormant; how 2.17 and later clients lay out the gmap overview is unmeasured.

## 3.2.1 Three kinds of map

| Kind | File | Server option | Effect | Source |
| --- | --- | --- | --- | --- |
| level links | none; links inside each level (→ §3.1.2.3) | none | walking into a link rectangle makes the client ask for a level warp | [srv] (client-internals/feature-specs/06-gmap-overworld.md#three-different-maps-do-not-mix) |
| server big map | `bigmap.txt`-style text grid | `maps =` | tells the server which levels are adjacent, so players see and chat across edges; the client does nothing special | [srv] (client-internals/feature-specs/06-gmap-overworld.md#three-different-maps-do-not-mix) |
| gmap | `GRMAP001` | `gmaps =` | the client walks continuously across level borders | [srv] (client-internals/feature-specs/06-gmap-overworld.md#three-different-maps-do-not-mix) |
| map-screen overlays | text grid and image | `bigmap =`, `minimap =` (four comma fields `text,image,x,y`) | the server sends the overlay settings at login to 2.1 and later clients; the notes warn that setting `bigmap` breaks gmaps | [srv] (client-internals/feature-specs/06-gmap-overworld.md#three-different-maps-do-not-mix) |

## 3.2.2 GRMAP001 as the server reads it

| Key | Arguments | Meaning | Source |
| --- | --- | --- | --- |
| `GRMAP001` | none | signature, first line | [srv] (formats/gmap.md#keys-read-by-gserver-srv) |
| `WIDTH`, `HEIGHT` | n | grid size in levels | [srv] (formats/gmap.md#keys-read-by-gserver-srv) |
| `GENERATED` | one argument | read and stored; not used to rebuild names on the server side | [srv] (formats/gmap.md#keys-read-by-gserver-srv) |
| `LEVELNAMES` … `LEVELNAMESEND` | one grid row per line, quoted, comma-separated names | fills the grid row-major; names are lowercased for lookup | [srv] (formats/gmap.md#keys-read-by-gserver-srv) |
| `MAPIMG` | file | overview image | [srv] (formats/gmap.md#keys-read-by-gserver-srv) |
| `MINIMAPIMG` | file | minimap image | [srv] (formats/gmap.md#keys-read-by-gserver-srv) |
| `NOAUTOMAPPING` | none | flag | [srv] (formats/gmap.md#keys-read-by-gserver-srv) |
| `LOADFULLMAP` | none | flag: preload every level | [srv] (formats/gmap.md#keys-read-by-gserver-srv) |
| `LOADATSTART` … `LOADATSTARTEND` | name list | levels to preload | [srv] (formats/gmap.md#keys-read-by-gserver-srv) |

| Rule | Detail | Source |
| --- | --- | --- |
| tokens | each line is split on whitespace after `\r` is stripped | [srv] (formats/gmap.md#keys-read-by-gserver-srv) |
| name rows | lines inside the `LEVELNAMES` block are parsed as quoted CSV | [srv] (formats/gmap.md#keys-read-by-gserver-srv) |
| coordinates | position in the world is `cell*64 + local`; local = global − 64 × cell | [cap] (client-internals/feature-specs/06-gmap-overworld.md#lab-capture-of-a-real-222-client-crossing-gmap-edges-2026-10-24-cap) |
| transfer | a client fetches the `.gmap` file itself as a file transfer when it does not have it | [cap] (client-internals/feature-specs/06-gmap-overworld.md#lab-capture-of-a-real-222-client-crossing-gmap-edges-2026-10-24-cap) |

## 3.2.3 GRMAP001 as the tools write it

Three writers emit the signature, each with a different set of keys; `GENERATED` does not mean the same thing in all three [bin] (formats/grmap001.txt).

| Writer | Keys in order | Level names | Source |
| --- | --- | --- | --- |
| DungeonGenerator (short form) | `GRMAP001`, `WIDTH`, `HEIGHT`, `GENERATED <bottom-right level name>`; no `LEVELNAMES` block | `LEVELSTART`, a column letter and a 1-based row; the grid is rebuilt from the last level's name in `GENERATED` | [bin] (formats/grmap001.txt) |
| TerrainGenerator (generator form) | `GRMAP001`, `WIDTH`, `HEIGHT`, `GENERATED 1`, `GENSEED`, `GENBASE`, `GENEVENBORDERS` (0 or 1), `GENHEIGHT`, `GENCHAOS`, `LEVHEIGHT`, `LEVCHAOS`, `MAPIMG <basename>.png`, one level name per row, `HEIGHTMAP` … `HEIGHTMAPEND`, `RANDOMSEEDS` … `RANDOMSEEDSEND` (one seed per level, when present) | basename, a column `A` then `AA`, a zero-padded row, and `.nw`; `GENERATED 1` is a flag here | [bin] (formats/grmap001.txt) |
| GraalLevelGen | `GRMAP001`, `WIDTH`, `HEIGHT`, then a `LEVELNAMES` list of quoted, comma-separated file names | as listed | [bin] (formats/grmap001.txt) |

| Rule | Detail | Source |
| --- | --- | --- |
| `MAPIMG` | the overview the client shows on the map list; the PNG TerrainGenerator saves from its preview dialog is a separate file | [bin] (formats/grmap001.txt) |
| `HEIGHTMAP` | the height field; a sibling `_heights.txt` holds the same numbers without the gmap wrapper | [bin] (formats/grmap001.txt) |
| per-level heights | each level file then carries a 9 by 9 `HEIGHTS` block (→ §3.1.2.7) | [bin] (formats/grmap001.txt) |

## 3.2.4 Client readers by build

| Build | Gmap reader | Map path in use | Source |
| --- | --- | --- | --- |
| 2.05 rev 2 | has the `GRMAP001` string, a reader that knows `WIDTH`, `HEIGHT`, `GENERATED`, `GENSEED`, `GENBASE`, `GENEVENBORDERS`, `GENHEIGHT`, `GENCHAOS`, `LEVHEIGHT`, `LEVCHAOS`, `MAPIMG`, `HEIGHTMAP` … `HEIGHTMAPEND`, `RANDOMSEEDS` … `RANDOMSEEDSEND` and `HEIGHTS`, and a map class; no static caller of the reader was found, so it may be dormant | the text big map and minimap below; no gmap warp handler and no gmap cell prop name | [2.05] (formats/gmap.md#205) |
| 2.22 | unmeasured | gmap crossing captured in the lab (→ §4.11.9) | [cap] (client-internals/feature-specs/06-gmap-overworld.md#lab-capture-of-a-real-222-client-crossing-gmap-edges-2026-10-24-cap) |
| 2.31 | unmeasured | gmap crossing captured in the lab (→ §4.11.9) | [cap] (client-internals/feature-specs/06-gmap-overworld.md#needs) |

An earlier version of the gmap note said 2.05 had no `GRMAP001` string; that was wrong, and the build catalogue also lists it for 2.05 [2.05] (formats/gmap.md#205).

## 3.2.5 Text big map and minimap (2.05)

2.05 reads the big map and minimap as text grids; the GS1 commands `setmap` and `setminimap` load the same kind of file from a script [2.05] (formats/gmap.md#205-big-map-and-minimap-text-files-205).

| Map | File | Image | Built-in integers | Source |
| --- | --- | --- | --- | --- |
| big map | `bigmap.txt` | `map.png` | 10, 16, 1688, 1024 | [2.05] (formats/gmap.md#205-big-map-and-minimap-text-files-205) |
| minimap | `minimap.txt` | `map2.png` | 664, 896 | [2.05] (formats/gmap.md#205-big-map-and-minimap-text-files-205) |
| tutorial (offline) | `tutorialmap.txt` | `tutorialmap.png` | 3, 4, 192, 486 | [2.05] (formats/gmap.md#205-big-map-and-minimap-text-files-205) |

| Rule | Detail | Source |
| --- | --- | --- |
| lines | plain text, one map row per line, each parsed as a comma-separated list with quoting allowed | [2.05] (formats/gmap.md#205-big-map-and-minimap-text-files-205) |
| cells | each cell is normalised and appended to one flat list; a cell is a level file name, and `x` marks an empty cell | [2.05] (formats/gmap.md#205-big-map-and-minimap-text-files-205) |
| shape | the column count is the number of cells on the first line; the row count is total cells ÷ columns | [2.05] (formats/gmap.md#205-big-map-and-minimap-text-files-205) |
| shipped file | the shipped `bigmap.txt` is 20 columns × 21 rows of quoted level names | [file] (formats/gmap.md#205-big-map-and-minimap-text-files-205) |
| server-list override | an entry with more than the usual 8 fields replaces these: field 8 big-map file, 9 its image, 10 and 11 two integers, 12 minimap file, 13 its image, 14 and 15 two integers | [2.05] (formats/gmap.md#205-big-map-and-minimap-text-files-205) |
| integers | stored as points in the player object; probably image offsets or scale, which fits the defaults, but their use is not traced | [inf] (formats/gmap.md#205-big-map-and-minimap-text-files-205) |
| later builds | the server-pushed forms `PLO_BIGMAP` (171) and `PLO_MINIMAP` (172, for example `zodiacminimap.txt,zodiacworldminimap3.png,10,10`) replace this; they carry file names plus a default x,y for heads of players off the map | [srv] (formats/gmap.md#205); [srv] (client-internals/feature-specs/06-gmap-overworld.md#three-different-maps-do-not-mix) |

The server-list entry layout is in → §6.
