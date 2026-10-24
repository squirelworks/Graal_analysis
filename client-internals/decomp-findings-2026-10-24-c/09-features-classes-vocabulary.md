# 09 Features, classes, vocabulary

Tables: `classes_by_build.tsv`, `script_vocab_deltas.tsv`. Vendor source: `newfeatures2001.txt` in each version folder (2.01-2.05 and the 2.1 tests). The 2.00 builds and NewWorld/NewMain have no changelog.

## What each step adds (vendor text + binary evidence)
| step | feature | binary evidence |
|---|---|---|
| 2.01 | levels preloaded when walking on the map; map-reading animation; showimg artefact fixes; chat text from `setplayerprop #c` stays 3 s | PLI 35 and PLO 156 appear; warp/board handlers simplified; script strings bomy_walk/bomy_idle, maps1-3, hitobjects, playerreading, playerdies/hurt |
| 2.01 | `hitobjects` | PLI 36, PLO 46, UDP 25 |
| 2.02 | hats via gani attributes (5 attributes read from the player account), `#i()` images in signs, string parsing (strlen, startswith, indexof, `#e`, `#T`, tokenize/tokenize2/tokenscount/`#t`), `local.` flags are not sent to the server, flags issparringzone/nopkzone, free-server restrictions, HTML window navigation buttons, staff-guild list editable by server owners | PLO 47; new strings for heads/bodies/shields/hats directories, `local.`, webgifs, weblevels, profiles; zlib.dll import (see 03) |
| 2.02 rev1 | speed-cheat check fix, history without web bar, better hacking protection, server learns the client's language | server language is sent starting rev2 (PLI 37) |
| 2.03 | `triggeraction`, `actionpushed/actionpulled`, `move dx,dy,time,options` | PLO 48 and 165, PLI 38, UDP 26, NPCMOVED handler grows; strings pushed/pulled/vecx/vecy/triggeraction/paramscount/movementfinished/onmapx/onmapy |
| 2.04 | `replacegani`, `addtiledef`, `addtiledef2`, `removetiledefs`, `setshape`, `setshape2`, `attachplayertoobj`/`detachplayer` with playerattachid/type and levelorgx/levelorgy, showimg text and server-side showimg, weaponscount/`#w`/`#W`, enable/disableselectweapons, bomy_kick | PLO 166, 26 removed; strings tiledefs, tileobjects, shapetiletypes, playerattached |
| 2.05 | maps via `setmap` applied at once, window title with server name, script-editor format button, `.nw` text level format (GLEVNW01), array tiletypes for setshape2 | PLO 168; strings updateterrain, loadmap, getz/playerz, setbacktile2 |
| 2.1 test | new tile art, new start/server-list window (F8), new image engine, `ascii()`, `tiles[x,y]`, predefined-npc editor with `#COMMENTS`/`#EDIT`, smilies in PMs, tabbed editor | PLO 49 and 169; TPageControl/TTabSheet/TMemo added, person/show-code windows removed |

## Classes
- 186 classes in 2.00 through 2.03. +1 in 2.04 (an object-set class; matches "support for object sets"). +1 in 2.05 (class TADP; purpose not identified). 2.1 test swaps 4 editor classes for 4 tabbed ones (188 total).
- NewWorld beta1 = 186 classes, the same set as the 2.0x line (without the 2.04 and 2.05 additions); beta2 changes the editor windows like 2.1 test. NewMain has 193 (adds DDE classes, chest/baddy editors).

## Vocabulary (script/identifier strings, resources excluded)
See `script_vocab_deltas.tsv` for exact lists. Takeaways:
- Everything the changelog calls a new script command or variable appears in the binary's string table in the same build, with no extra undocumented identifier in 2.01-2.05 other than `actionplayer`, `lighteffectsenabled` (2.03) and `bomy_*` animation names.
- 2.01 drops `openurl` from the string list and 2.02 drops `error`/`z_stream8` (then 2.03 brings them back and drops the zlib.dll strings). These are string-table moves, not feature removals: the 2.02 changelog still describes `openurl`/`openurl2`.
