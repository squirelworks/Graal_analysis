# Client cross-version timeline, 1.33 → 2.1 tests

Date: 2026-10-21

This note follows the Delphi client across twenty builds: 1.33 to 1.39, 1.41 rev1, NewMain 1.42, 2.0, 2.01, 2.02 rev2, 2.03, 2.04, 2.05 rev1, 2.05 rev2, the two 2.1 test builds and the two NewWorld betas.
Builds are identified by MD5 in `build-catalogue.md`. Function data come from the same Ghidra pipeline as `build-diff-204-205.md`. All facts here come from RTTI, the GS1 command table and the packet switch tables, read the same way in every build.
It is cleaned: no addresses, no decompiler output.

## How it was read

- **Classes.** Class names, parents, instance sizes and virtual-slot counts come from the Delphi VMTs.
- **GS1 commands.** The script executor matches commands against one table of fixed-size records, each holding a pointer to the command text. The table was found by its first entry (`say`) and read to the end. Records are 16 bytes in 1.33 and 12 bytes from 1.34 on.
  Trailing spaces in a command (`say `, `setshape `) are part of the match text and mean the command takes arguments.
- **Packet ids.** Each packet and prop parser is a Delphi `case` on the first byte minus 32, compiled as a jump table (two-level in most parsers: a byte index table, then a pointer table).
  The ids that reach a real handler, not the default branch, are the ids the build handles. Ids are listed after the minus-32 step, so they are protocol ids.

## Function maps onto 2.05 rev2

Every build was matched function by function onto 2.05 rev2 (6529 functions) with the matcher described in `build-diff-204-205.md`, applying the 2.05 virtual-slot shift for the level-object classes.
The per-build maps (old function, rev2 function, name, identical or changed) are kept outside the repo with the lab files, since they carry addresses.

| Build | Functions | Identical to 2.05 rev2 | Changed | Only in this build | Only in 2.05 rev2 |
|---|---|---|---|---|---|
| 1.33 | 5228 | 4312 | 345 | 571 | 1872 |
| 1.34 | 5240 | 4299 | 388 | 553 | 1842 |
| 1.35 | 5435 | 4479 | 383 | 573 | 1667 |
| 1.36 | 5437 | 4477 | 385 | 575 | 1667 |
| 1.37 | 5459 | 4494 | 395 | 570 | 1640 |
| 1.38 | 5546 | 4534 | 439 | 573 | 1556 |
| 1.39 | 5593 | 4550 | 470 | 573 | 1509 |
| 1.41 rev1 | 5675 | 4783 | 419 | 473 | 1327 |
| NewMain 1.42 | 6468 | 5592 | 507 | 369 | 430 |
| 2.0 | 6396 | 5637 | 515 | 244 | 377 |
| 2.01 | 6412 | 5663 | 528 | 221 | 338 |
| 2.02 rev2 | 6350 | 5678 | 484 | 188 | 367 |
| 2.03 | 6428 | 5754 | 479 | 195 | 296 |
| 2.04 | 6471 | 5799 | 558 | 114 | 172 |
| 2.05 rev1 | 6522 | 6345 | 94 | 83 | 90 |
| NewWorld beta 1 | 6381 | 5810 | 405 | 166 | 314 |
| 2.1 test (first) | 6598 | 5774 | 611 | 213 | 144 |
| 2.1 test (second) | 6595 | 5762 | 619 | 214 | 148 |
| NewWorld beta 2 | 6484 | 5668 | 489 | 327 | 372 |

Most of the identical count for the 1.3x builds is shared Delphi library code. The largest single step is 1.41 rev1 to NewMain 1.42, about 800 more functions, part of which is the new DirectDraw 7 and grid library code.
The 2.1 tests have more functions than 2.05 but fewer that are unique to rev2, which fits them being a later branch of the 2.05 code.

## Classes

| Build | Added | Removed |
|---|---|---|
| 1.34 | `TServerPlayer`, `TEditorBaddy` | `TOtherClient`, `TEditorOpponent`, the OLE classes (the new names look like renames of the removed ones) |
| 1.35 | `TWebBrowser` and the OLE control classes | — |
| 1.36 to 1.38 | — | — |
| 1.39 | `TPlayerListOptions`, `TProfileEdit` | — |
| 1.41 rev1 | `TGraalClient`, `TServerListClient`, `TServerListFrame`, `TServerMessage`, `TShortMessage`, `TWinamp` | `TAdventureBoolOperation`, `TRTFMessage` |
| NewMain 1.42 | `TGraalAni` (+ `Part`, `Sound`, `Sprite`, `Step`), `TGraalImage`, the DelphiX DirectDraw 7 classes, string and draw grids, `TClipboard` | `TAdventureSign` |
| 2.0 | — | the DDE client/server classes |
| 2.01 | — | — |
| 2.02 rev2 | — | the zlib error classes (back in 2.03) |
| 2.03 | `TNPCMove` | — |
| 2.04 | `TLevelObject`, `TObjectSet`, `TTempTile`, `TTileDef` | — |
| 2.05 rev1 | `TGraalMap`, `TADP` (anti-debug) | `TEditorBaddy`, `TEditorLevel` |
| 2.05 rev2 | — | — |

Against 2.05 rev2:

| Build | Added | Removed |
|---|---|---|
| NewWorld beta 1 | `TLevelHeights`, `TAdventureBacktileArea`, `TDrawText` | horse, ball and carry objects, `TComputer`, `TEditorChest`, `TChestEdit`, `TEditBaddy`, `TPos`, `TWebClient` |
| 2.1 test (both) | `TEditNPC`, `TEditVariable`, `TEditorDefNPC`, `TPageControl` / `TTabSheet`, `TMemo`; the second test adds `TSmilie` | `TPersonAction`, `TEditPerson`, `TShowCodes`, `TObjectSet` |
| NewWorld beta 2 | both lists above, including `TSmilie` | both lists above |

So **NewWorld beta 1 was cut from the 2.05 code base and beta 2 from the 2.1 test code base.** Beta 2 carries every 2.1-test class change on top of the NewWorld removals.

### Sizes of the main game classes (bytes, virtual slots)

| Class | 1.33 | 1.34 | 1.38 | 1.39 | 1.41 | NM 1.42 | 2.0 | 2.01 | 2.02r2 | 2.03 | 2.04 | 2.05 | NW b1 | 2.1 test | NW b2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `TAdventure` (main form) | 3268 | 3240 | 3244 | 3256 | 3268 | 1864 | 1864 | 1860 | 1860 | 1860 | 1084 | 1084 | 1084 | 1108 | 1108 |
| `TAdventureLevel` | 56 | 84 | 84 | 84 | 84 | 84 | 88 | 88 | 88 | 88 | 96 | 184 | 33968 | 184 | 33968 |
| `TAdventureCommand` | 64 | 68 | 76 | 76 | 68 | 68 | 68 | 68 | 68 | 68 | 68 | 76 | 76 | 76 | 76 |
| `TDrawableObject` | 20 | 20 | 20 | 20 / 2 | 28 / 2 | 28 / 2 | 28 / 2 | 28 / 2 | 28 / 2 | 28 / 2 | 32 / 2 | 32 / 3 | 32 / 3 | 44 / 3 | 44 / 3 |
| `TServerPlayer` | — | 220 | 224 | 240 / 2 | 272 / 2 | 272 / 2 | 272 / 2 | 280 / 2 | 288 / 2 | 288 / 2 | 340 / 7 | 336 / 8 | 320 / 8 | 364 / 9 | 348 / 11 |
| `TPlayer` | 1516 | 1512 | 1524 | 1544 | 1564 | 1496 | 1500 | 1516 | 1528 | 1528 | 804 | 800 | 760 | 832 / 836 | 792 |
| `TEditorNPC` | 208 | 220 | 228 | 224 | 244 | 476 | 476 | 488 | 496 | 508 | 568 | 564 | 548 | 592 | 572 |
| `TGraalMap` | — | — | — | — | — | — | — | — | — | — | — | 76 | 96 | 256 | 34060 |

Two points for anyone carrying names between builds by virtual-slot number:

- **2.04 puts `TLevelObject` under the player and NPC classes**, which is why `TServerPlayer` jumps from 2 to 7 slots. Slot numbers from 2.03 and earlier do not line up with 2.04 for these classes.
- **2.05 adds a slot to `TDrawableObject`**, shifting every descendant by one (see `build-diff-204-205.md`). The 2.1 tests and NewWorld beta 2 add more slots to the player classes again.

The NewWorld `TAdventureLevel` (33968 bytes) and beta 2 `TGraalMap` (34060 bytes) are large enough to hold tile arrays inline, which fits the NewWorld level heights and back-tile layers.

## GS1 commands

Count of commands in the table, and what each build adds over the previous one.
The table is followed directly by a short direction table (`up`, `right`), and in some builds by other keyword lists (`*=`, `:=`, the 1.33 soldier names, and `nwweek` / `nwmonth` / `nwmin` in the NewWorld betas).
Those entries are not counted. In 2.05 this gives 161 commands, matching the earlier count on main.

| Build | Count | Added |
|---|---|---|
| 1.33 | 88 | — |
| 1.34 | 93 | `dontblocklocal`, `blockagainlocal`, `showlocal`, `hidelocal`, `carryobject`, `throwcarry`, `setbacktile`; `seteffect` and `unseteffect` leave the table (`seteffect` returns in NewMain 1.42) |
| 1.35 | 93 | same table as 1.34 |
| 1.36 | 104 | `lay2`, `take2`, `takehorse`, `takeplayerhorse`, `removebomb`, `removearrow`, `removeitem`, `removeexplo`, `removehorse`, `explodebomb`, `reflectarrow`; `lay` now takes arguments |
| 1.37 | 106 | `playlooped`, `stopsound` |
| 1.38 | 109 | `setlevel2`, `changeimgpart`, `hitnpc`; `setlevel` now takes arguments |
| 1.39 | 111 | `setani`, `setcharani` |
| 1.41 rev1 | 126 | `canwarp`, `callnpc`, `say2`, `break`, `continue`, `callweapon`, `spyfire`, `function`, `return`, `changeimgvis`, `setimg`, `setimgpart`, `drawovertrees`, `putexplosion2`, `showstats`; `putexplosion` now takes arguments |
| NewMain 1.42 | 134 | `canwarp2`, `setshape`, `seteffect`, `setcoloreffect`, `setzoomeffect`, `drawaslight`, `changeimgcolors`, `changeimgzoom` |
| 2.0 | 142 | `setgender`, `setchargender`, `join`, `freezeplayer2`, `unfreezeplayer`, `enabledefmovement`, `disabledefmovement`, `setmusicvolume` |
| 2.01 | 144 | `openurl2`, `hitobjects`; `openurl` now takes arguments |
| 2.02 rev2 | 146 | `tokenize`, `tokenize2` |
| 2.03 | 148 | `triggeraction`, `move` |
| 2.04 | 157 | `addtiledef`, `addtiledef2`, `removetiledefs`, `replaceani`, `attachplayertoobj`, `detachplayer`, `setshape2`, `enableselectweapons`, `disableselectweapons`; `setshape` now takes arguments |
| 2.05 rev1 / rev2 | 161 | `setbacktile2`, `setz`, `updateterrain`, `loadmap`; `setbacktile` now takes arguments |
| 2.1 tests | 161 | same table as 2.05 |
| NewWorld beta 1 | 161 | same table as 2.05 |
| NewWorld beta 2 | 165 | `addstring`, `insertstring`, `removestring`, `deletestring` |

A command being in the table does not mean it does anything. #4 found that in 2.05 `setz`, `updateterrain` and `setbacktile2` have no executor case, so they parse and are ignored. This note has not checked executor cases in the other builds.

New commands are inserted in the middle of the table, not appended. So the internal index of a command changes between builds, and an executor decompiled in one build cannot reuse another build's case numbers.

## Packet ids handled by the client

### Server → client packets

| Build | Change |
|---|---|
| 1.33 to 1.37 | 43 ids: 0–41, 100 |
| 1.38 | + 43 |
| 1.39 | + 75 (45 ids: 0–41, 43, 75, 100) |
| 1.41 rev1 | same set |
| NewMain 1.42 | + 42, 44, 45, 150, 151, 153 |
| 2.0 | + 154, 155 |
| 2.01 | + 46, 156 |
| 2.02 rev2 | + 47 |
| 2.03 | + 48, 165 |
| 2.04 | + 166; − 26 |
| 2.05 rev1 / rev2 | + 168 |
| NewWorld betas | 2.05 minus 2, 4, 17, 18, 154, 155 |
| 2.1 tests | 2.05 plus 49, 169 |

Id 42 is not handled until NewMain 1.42, although 43 is handled from 1.38 on. NewWorld drops six ids at once, alongside the removed baddy, horse and chest classes.

### Prop parsers

Each prop switch reads a run of `(prop id, value)` pairs. Ids handled:

| Parser | 1.33 | Added later |
|---|---|---|
| Player props | 0–33 | 34 (1.39); 35, 36 (1.41); 37–41 (2.02 rev2); 42 (2.04); 43–45 (2.1 tests) |
| NPC props | 0–33 | 34 (1.34); 35 (1.41); 36–40 (2.02 rev2); 41–43 (2.1 tests) |
| Baddy props | 0–10 | none; the switch is gone in both NewWorld betas |

The player switch was told apart from the NPC switch by its callers: the player prop parser is the one that calls the sparse switch described below.
That holds in every build from 1.34 on. In 1.33 neither switch calls it within its own body, so the 1.33 row assumes the same split as 1.34 (one switch is 0–33, the other 0–34).
So NPC prop 34 arrives in 1.34, five builds before player prop 34.

The five ids added together in 2.02 rev2 (player 37–41, NPC 36–40) sit at the same place in both lists, so they are probably one feature added to players and NPCs at once.
This is consistent with the public prop numbering used by open-source server work, where both lists gain five attribute props at these positions.

The player prop parser also calls a second, sparse switch with ids up to 51 (21 ids in 1.33, 23 in 1.39 and 31 in 2.05). It handles a subset of player props and grows in step with the player prop list.
Its role (likely props of other players) has not been confirmed.

### UDP packets

The UDP parser handles ids 0 and 10–23 in 1.33 to 1.37. 1.38 adds 24, 2.01 adds 25, 2.03 adds 26 and the 2.1 tests add 27. The NewWorld betas drop 16 and 17.
