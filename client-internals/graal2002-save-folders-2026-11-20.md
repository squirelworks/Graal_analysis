# Save and maps folders in the Graal 2002 builds (2.1.0.0 to 2.1.0.4)

Date: 2026-11-20. Tracker: [#245](https://github.com/squirelworks/Graal_analysis/issues/245); App. E#10. Tags: **[bin]** (static read of the six Windows images in `graal2002-and-140-builds.md`: ver7, ver8, ver9, ver10, ver13 and v22; no run).

## Where a downloaded file is saved

All six builds use one save routine with the same shape. **[bin]**

1. Nothing is written unless the stream exists and is not empty. This is the same guard as in 1.39 to 2.31 (`decomp-findings-2026-10-25-k/02-save-folders-by-build.md#the-guard`).
2. If the name already resolves to a file on disk through the client's name index, that file is replaced where it is.
3. Otherwise a folder is chosen by name, compared without case:
   - `.wav` goes to `sounds`.
   - **ver9 onward only:** `.gmap` goes to `maps`, and so does a name that contains `map` and ends `.txt`, `.gif`, `.png` or `.mng`.
   - Everything else goes under `levels`:
     - `bomys` for names starting `bomy` or `b_`;
     - `ganis` for `.gani`;
     - `emoticons`;
     - `hats` for `hat` with a digit as the fourth character;
     - then `heads`, `bodies`, `swords` and `shields` for names containing the word;
     - anything left goes to `webgifs`.
4. The folder chain is created if it is missing and an existing file there is deleted. The stream is written, the file time is set when the reply carried one, and the file is announced to the name index.

| Build | Shipped | Token | `maps` rule |
| --- | --- | --- | --- |
| ver7 | 2001-10-09 | `GNW03081` | no: a downloaded `.gmap` lands in `levels\webgifs`, as in 2.05 rev 2 and the 2.1 test builds |
| ver8 | 2001-10-19 | `GNW03081` | no |
| ver9 (2.1.0.0) | 2001-10-30 | `GNW03081` | yes, already in the 2.17.1 to 2.31 form |
| ver10, ver13, v22 | later | see `graal2002-and-140-builds.md` | yes, the same rule |

So the `maps` save rule first appears in ver9. It comes before the gmap loader: the gmap code and `loadgmaps.txt` are absent from all of 2.1.0.0 to 2.1.0.4 (`static-reads-appendix-e-2026-11-19.md`). 2.12 to 2.16 have no binary (#439). Every 2.1.0.x from ver9 on and every client from 2.17.1 on carries the rule, so those builds very probably have it too. **[inf]**

## When folders are made

No folder is made at start-up. Each one is created on its first write, just before the write. **[bin]** The writers are:

- the download save routine above: `sounds`, `maps` and `levels\…`;
- the web-level cache, `weblevels\<host>\<level>-<port>.code`. It starts with `GWEBL001` and then holds the level as `GR-V1.03` text;
- the PM log, `pms\messages_<name>.txt`;
- `profiles\profile_<name>.txt`;
- `levels\tiledefs\<name>.txt`;
- `tileobjects\objects….txt`.

## Reads

- Before asking for a level, the client tries `weblevels\<host>\<level>-<port>.code`, then the same name without the port. **[bin]**
- A `maps\parts\<name>\<file>.png` path builder for map-part images is already in ver7, before the save rule. **[bin]**
- `bigmap.txt`, `minimap.txt`, `map.png` and `map2.png` appear only as default names in a table: one set in ver7 and ver8, two from ver9. They are found by bare name through the file index, not at a fixed `maps\` path. **[bin]**
- The start-up file index walks the game folder recursively but skips any folder named in the list `+pms+profiles+weblevels+`. The list is in all six builds, so PM logs, profiles and cached web levels are never treated as game files. `maps` is indexed. **[bin]**

## Not read

- The `saveimages` gate in the caller was not re-read in these images. It is read in 2.05 rev 2 to 2.31 (`decomp-findings-2026-10-25-e/02-save-rules.md`).
