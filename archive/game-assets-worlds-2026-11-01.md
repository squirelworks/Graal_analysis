# Worlds and level dumps (2026-11-01)

Follows `archive/game-assets-2026-11-01.md`. That note opened one level dump
(alkaren) and one world archive (Andor, 21 July 2002). This note opens the
other level-dump archives, the three Zelda Online rars, `Zone_GMAP.rar`, and
a sample of the 87 archived server folders. Nothing from the folder is
committed: no archives, levels, images, or scripts.

Static read only. No binary was run. A level magic is the first 8 bytes.
`GR-V1` and `Z3-V1` files were accepted by `formats/grv1-decoder/grv1.py`
(`load`, the existing header check). Every one of those files reported below
loaded. `GLEVNW01` is the text magic and is not passed to that decoder.
AppleDouble files (`._` names, a Mac resource fork) are left out of the counts.

## Baseline, not re-counted

From the earlier note: the alkaren dump has 29 `.nw` files whose magic is
`GLEVNW01`, 5 `.nw` files whose magic is `GR-V1.03`, and 16 `.graal` files
whose magic is `GR-V1.03`. Andor 2002 is one flat directory of 409 `.graal`
and 93 `.nw`, plus one `GRMAP001` gmap. Those two archives are the baseline
only.

## Other level dumps

Both dump folders were opened: 19 rars under "Graal - Level Dumps" (alkaren
left as the baseline) and all 17 under "Graal New World - Level Dumps".
Nested rars and zips inside those archives were opened too, and so was the
zip inside the police dump. Totals for that set:

| Magic | Where | Count |
| --- | --- | --- |
| `GLEVNW01` | `.nw` | 330 |
| `GR-V1.03` | `.nw` | 5 |
| `GLEVNW01` | `.graal` | 2 |
| `GR-V1.03` | `.graal` | 305 |
| `GR-V1.02` | `.graal` | 1 |
| `GR-V1.01` | `.lost` | 1 |
| `GR-V1.02` | `.zelda` | 1 |
| `GR-V1.03` | `.zelda` | 1 |
| `GR-V1.03` | no extension | 13 |
| `GR-V1.03` | `.shop` | 1 |
| `GR-V1.03` | `.nw-notused` | 1 |

So among files whose name ends in `.nw`, 330 are `GLEVNW01` and 5 are
`GR-V1.03`. The five are all in `Snapshots of chicks.rar`:
`snapshot_worldg-18.nw`, `snapshot_worldv-20.nw`,
`snapshot_worldw-13_hatshop.nw`, `snapshot_stefquest-1.nw`, and
`snapshot_worldi-17.nw`. The same dump also has 95 `GLEVNW01` `.nw` files
and 16 `GR-V1.03` `.graal` files. That is the same mismatch the alkaren dump
showed (the extension is not the magic), and it is the only dump in this set
where a `.nw` name carries `GR-V1.03`.

The other direction shows up twice, both inside nested rars in the Agret
dump: `snapshot_mdgquest11.graal` and `snapshot_onlinestartlocal2.graal` are
`GLEVNW01` text. `Jesters house 2.rar` has `bab_e-11.nw-notused`, which
`grv1.py` reads as `GR-V1.03`; the suffix is not `.nw`, so it is not in the
330 / 5 split.

Older magics are rare and sit in `graalnew.rar`: `level6.graal` and
`vampgrave2.zelda` are `GR-V1.02`, and `level7.lost` is `GR-V1.01`.
`levelscrappy.rar` has one `.zelda` name whose magic is `GR-V1.03`. No
`Z3-V1` magic turned up in these two dump folders.

Per archive, level magics only (images and scripts omitted). Agret's outer
rar is the row below; its nine nested rars are the next row. Graal Kingdoms'
outer rar is two zips; their levels are the row after that. The police row
includes three `GLEVNW01` files inside `Mt. Antora Station.zip`.

| Archive | Level magics |
| --- | --- |
| `9-06-2000.rar` | 8 `.graal` `GR-V1.03` |
| `antglobe.rar` | 1 `.graal` `GR-V1.03` |
| `aod-town-brett.rar` | 16 `.graal` `GR-V1.03`, 11 extensionless `GR-V1.03`, 1 `.shop` `GR-V1.03` |
| `Brett's--lvls.rar` | 97 `.graal` `GR-V1.03`, 2 extensionless `GR-V1.03` |
| `elftown.rar` | 27 `.nw` `GLEVNW01`, 23 `.graal` `GR-V1.03` |
| `fishhouse-2.rar` | 6 `.graal` `GR-V1.03` |
| ghost pirate rar | 12 `.graal` `GR-V1.03` |
| `graalnew.rar` | 1 `.graal` `GR-V1.02`, 1 `.zelda` `GR-V1.02`, 1 `.lost` `GR-V1.01` |
| `levelscrappy.rar` | 3 `.graal` `GR-V1.03`, 1 `.zelda` `GR-V1.03` |
| `partyhall.rar` | 1 `.graal` `GR-V1.03` |
| `personalhouse9.rar` | 1 `.graal` `GR-V1.03` |
| pikachu mix rar | 8 `.nw` `GLEVNW01`, 19 `.graal` `GR-V1.03` |
| `Set Stuff.rar` | 1 `.graal` `GR-V1.03` |
| `sk-staffroom.rar` | 1 `.graal` `GR-V1.03` |
| `Staff Room.rar` | 1 `.graal` `GR-V1.03` |
| `suck.rar` | 6 `.graal` `GR-V1.03` |
| `supermegaland.rar` | 1 `.graal` `GR-V1.03` |
| `warcaptainmagfill.rar` | 1 `.graal` `GR-V1.03` |
| `xitami preview.rar` | 5 `.graal` `GR-V1.03` |
| `3dcube.rar` | 1 `.nw` `GLEVNW01` |
| `Agret Levels and scripts.rar` | 23 `.nw` `GLEVNW01`, 1 `.graal` `GR-V1.03` |
| Agret nested rars | 31 `.nw` `GLEVNW01`, 74 `.graal` `GR-V1.03`, 2 `.graal` `GLEVNW01` |
| `Asylum Levels.rar` | 4 `.nw` `GLEVNW01` |
| Avalon rar (2005-05-10) | 28 `.nw` `GLEVNW01`, 11 `.graal` `GR-V1.03` |
| `brandon_u_arse.rar` | 1 `.nw` `GLEVNW01` |
| `classiclevel.rar` | 1 `.nw` `GLEVNW01` |
| `Events.rar` | 10 `.nw` `GLEVNW01` |
| `GraalKingdoms.rar` | no level magic in the outer rar |
| Graal Kingdoms zips | 5 `.nw` `GLEVNW01` |
| `Intro Levels.rar` | 23 `.nw` `GLEVNW01` |
| `Jesters house 2.rar` | 23 `.nw` `GLEVNW01`, 1 `.nw-notused` `GR-V1.03` |
| `Kakariko.rar` | 4 `.nw` `GLEVNW01` |
| `Police.rar` | 24 `.nw` `GLEVNW01` |
| `School.rar` | 1 `.nw` `GLEVNW01` |
| `Snapshots of chicks.rar` | 95 `.nw` `GLEVNW01`, 5 `.nw` `GR-V1.03`, 16 `.graal` `GR-V1.03` |
| `twintowers.rar` | 1 `.nw` `GLEVNW01` |
| `Zippys soda factory.rar` | 6 `.nw` `GLEVNW01` |
| Zol's pub rar | 14 `.nw` `GLEVNW01` |

`Kakariko.rar` also has `village.gmap` (see below). Several dumps mix in
png, gif, and gani files. Those were not measured.

## Zelda Online's three rars

`Zelda Online.rar` (50 KB) and `zolevels.rar` (49 KB) are the same 36
`.zelda` files. Byte for byte, each pair matches. Every file is `Z3-V1.03`
and `grv1.py` reads it. Names: `cave1`, `cave2`, `level1` through `level29`,
`linkshouse`, and `village1` through `village4`. Archive dates on the files
are April–May 1998. `Zelda Online.rar` nests them one directory deeper; the
timestamps differ by an hour.

`Zelda.rar` (948 KB) is a later mix, not a third copy. It has 34 `.zelda`
names. `level6.zelda`, `level10.zelda`, and `level27.zelda` are still the
`Z3-V1.03` bytes from the small rars. The other 31 `.zelda` names are
`GR-V1.03` and are not the same bytes. `linkshouse.zelda` and
`village4.zelda` are absent. Beside those levels: two identical `GLEVNW01`
files (`metro_starthouse.nw` and `onlinestartlocal.nw`, same hash), one
`GR-V1.03` `.graal` (`onlinestartlocal.graal`), gif and jpeg pictures, two
short letters (they name an official host; the host is left out), and a
nested zip of a 1.39-era server tree (22 entries, including two executables,
which were not run).

## Zone gmaps

`Zone_GMAP.rar` (2 KB) is 19 text gmaps, dated 2008 through 2014 in the
archive listing. Every file starts `GRMAP001`, then `WIDTH` and `HEIGHT`,
then a `LEVELNAMES` block of one row per line and `LEVELNAMESEND`. None has
`GENERATED`. Sixteen also have `NOAUTOMAPPING` (`zone_alien.gmap`,
`zone_monsters9.gmap`, and `zone_monsters9_inst224.gmap` do not).

| File | Grid |
| --- | --- |
| `zone_ad.gmap` | 9 × 5 |
| `zone_alien.gmap` | 3 × 3 |
| `zone_arctic.gmap` | 8 × 6 |
| `zone_arctic_final.gmap` | 2 × 2 |
| `zone_conquest.gmap` | 5 × 5 |
| `zone_conquest_final.gmap` | 2 × 2 |
| `zone_green.gmap` | 8 × 6 |
| `zone_green_final.gmap` | 2 × 2 |
| `zone_jumprace.gmap` | 1 × 6 |
| `zone_mission1.gmap` | 1 × 10 |
| `zone_monsters1.gmap` and three `inst` copies | 6 × 5 |
| `zone_monsters2.gmap`, `zone_monsters3.gmap` | 6 × 5 |
| `zone_monsters9.gmap` and `zone_monsters9_inst224.gmap` | 2 × 2 |
| `zone_platform.gmap` | 4 × 2 |

A row is quoted names separated by commas. `zone_ad.gmap` row 1 is
`"zone_ad-a1.nw","zone_ad-b1.nw",…` through `i`. `zone_platform.gmap` is the
same grid with the quotes left off
(`zone_platform-a1.nw,zone_platform-b1.nw,zone_platform-c1.nw,zone_platform-d1.nw`).
`Kakariko.rar`'s `village.gmap` is the same shape at 2 × 2, plus a `MAPIMG`
line before `LEVELNAMES`.

## Archived server folders

`# Archived Servers #` is 87 folders, one listing, no further page. Full
downloads of all 87 do not fit (several single rars are tens or hundreds of
megabytes). All 87 names are below. Thirteen were opened, spread from 1999
file dates through a 2020 folder name. The other 74 were listed only.

Opened:

| Folder | What was opened | Levels, gmap, gani, scripts |
| --- | --- | --- |
| Chaos Continuum | `cc12-04` rar, 376 KB. File dates in the listing are 1999 | 219 `.graal` `GR-V1.03`, plus one `.old` file with the same magic. Image files and an html website folder. `maps/` is directories of those levels. No `.nw`, no `.gmap`, no gani, no npc tree |
| Zelda Link to The Past | rar dated 2003-03-24, 178 KB | 65 `.nw` `GLEVNW01`, images, one text file. No gmap, gani, or npc tree |
| Aleria | rar dated 2004-07-02, 262 KB | 571 `.nw` `GLEVNW01`. `levels/al.gmap` is `GRMAP001`, `WIDTH 23`, `HEIGHT 24`, `LEVELNAMES` of quoted `.nw` names. Text scripts: `NPCs` 1, `Weapons` 15, `Classes` 2. No gani |
| Eternal | rar dated 2004-12-17, 321 KB | 824 `.nw` `GLEVNW01`. `overworld/eternal.gmap` is `LEVELNAMES`, 27 × 30. Text under `NPCs`, `classes`, and `guilds`. No gani |
| Niromia | the 2006-12-11 rar, 436 KB. A 2007 rar in the same folder was listed only | 411 `.nw` `GLEVNW01` (one of them sits in `Classes`). No gmap and no gani. Text under `NPCS` (89), `Weapons` (32), `Classes` (8) |
| Horizon | rar dated 2006-11-24, 335 KB | 390 `.nw` `GLEVNW01`. One further `.nw` does not start with a level magic. No gmap. 86 `.gani`: 46 start at `SPRITE`, 34 at `GANI0001`, 1 at `GANI0002`. Text: `npcs` 772, `weapons` 88, `guilds` 53 |
| Zerati | rar dated 2006-10-26, 1.1 MB | 889 `.nw` `GLEVNW01`, 5 `.gani`, no gmap. Text under `npcs` (1979), `weapons`, `guilds`, and `scripts` |
| Graal Legacy | rar dated 2006-10-26, 2.3 MB | 234 `.nw` `GLEVNW01`, 7 `.gani`, no gmap. Almost the whole archive is `npcs/*.txt` (4583) |
| Aevum | outer rar dated 2009-08-03 is two inner rars; both were unpacked | The 2009-08-03 inner rar: 35 `.nw` `GLEVNW01`, 1 `.graal` `GR-V1.03`, and `maps/aev.gmap` (`LEVELNAMES`, 4 × 4, quoted `.nw` names). The converted inner rar: 56 `.nw` `GLEVNW01`, 1 `.graal` `GR-V1.03`, images, no second gmap |
| Flower World | rar dated 2012-10-13, 284 KB | 32 `.nw` `GLEVNW01`, 1 `.graal` `GR-V1.03`, 12 `.gani`. `levels/fern_main.gmap` is `LEVELNAMES`, 5 × 5. Text under `npcs`, `weapons`, `scripts` |
| GrimeCraft | rar dated 2012-02-17, 1.0 MB | 101 `.nw` `GLEVNW01`, 7 `.gani`. `Levels/grimecraft.gmap` is `LEVELNAMES`, 10 × 10. Text under `NPC's`, `Weapons`, `Classes` |
| Frolic | `Frolic.rar`, 5 KB, no date in the name | 4 `.nw` `GLEVNW01` and nothing else |
| Graal Development Studio | starter pack in the folder whose name includes 2020-08-10, 41 KB | 16 `.nw` `GLEVNW01`. `levels/overworld/playerworld.gmap` is `LEVELNAMES`, 3 × 3. A few `.txt` scripts and one weapons file |

A typical opened folder is one dated rar. Inside it: level files (`.nw`
`GLEVNW01`, and `.graal` `GR-V1.03` when the archive is older or mixed),
often images, and text scripts in `npcs` / `weapons` / `classes` when the
world has them. A gmap, when present, is one `GRMAP001` file with `WIDTH`,
`HEIGHT`, and a `LEVELNAMES` block. Ganis show up in the larger 2006 packs
and in the 2012 packs, not in Chaos, Aleria, or Eternal.

None of the thirteen is script-only in the way the Era pack from the earlier
note is. Frolic is levels alone. The Development Studio starter pack has
scripts and also 16 levels plus a gmap. Graal Legacy is mostly npc text and
still has 234 levels.

Listed only (74), under the folder names they have on Drive: `## Offline
Playerworlds Games ##`, Alvadore, Alzar, Andora Planet, `Anystria - PW65
[German]`, Archaic, Arynala, Atrian City, Azura, BlackPoint, Circuits, Cora,
Corinthia, Coronia, Cythus Med, Dargaro, Dark Ages, Dark Diamond, Dark
Horizon, Dark Nations, Dev_LifeInGraal, Dragandia, Dragon Tri-jer, `Dual
Ortus Dominion [DOD]`, Elemental Kingdoms, Endora, `Extreme Power Wrestling
[EPW_Graal]`, `Fallen Lands [FL Development]`, FastLane, Firebrand Kingdom,
Galactic Nations, Galrovik, Graal Realms, Griffin, Hyroko, Infection, Jedi,
Kuburiki, Life Bound, Lost Empire, `Lumina [2011-16-07] [GServer-2.3.1]`,
`Magonia [Mag]`, Malhangaia, Mantara, Mario Theme Game PW, Midwinter Nights,
Millenium, Mystic Nations, Nagorias, Outworld, Paradox, Phoenix, Playerworld
WanDaMan, Rastafaria, Renegade, Revenge Online, Roak, Rudora, Sands of Glory,
Seilius, Server Interface Test, `Shaded Angel Isles [S.A.I] AKA [Graal East]`,
Shangri-La, Shogun Online, Silver Dreams, Sparitoria, `Spawn [Genesis]`,
Stonehenge, Sumbria, Trabiac, Twisted, Unix Graal, Utheril, Vesporia. Dark
Ages, Lumina, and Shangri-La are single rars of about 17 MB, 61 MB, and 30
MB. Server Interface Test is two rars (about 8 MB and 6 MB); the larger
fetch came back as an HTML page, so it was not opened. Niromia's 2007 rar
was listed and not opened.

## Gmap text shapes

Two shapes were read from real files. Cells were not rebuilt.

**Dungeon, `GENERATED` only.** In the 2002 client zip already listed in the
earlier note (`levels/maps/`, nine `GRMAP001` files), two files are only the
signature, the grid, and one generated name:

```
GRMAP001
WIDTH 16
HEIGHT 16
GENERATED caverns_p-16.nw
```

```
GRMAP001
WIDTH 2
HEIGHT 2
GENERATED mines_b-2.nw
```

There is no `LEVELNAMES` block and no generator key after `GENERATED`.

**Terrain generator files in that same zip are not bare name rows.** Seven
maps (`main` 40 × 40, `start` 16 × 16, and `forest`, `samurai`, `pirates`,
`dustari`, `zormite` at 32 × 32) start `GRMAP001`, `WIDTH`, `HEIGHT`, then
`GENERATED` plus one `.nw` name (the corner name, such as
`GENERATED main_bn-40.nw`), then `GENSEED`, `GENBASE`, `GENEVENBORDERS`,
`GENHEIGHT`, `GENCHAOS`, `LEVHEIGHT`, `LEVCHAOS`, and a minimap image line.
`MAPIMG` is present and empty on `main`. A `HEIGHTMAP` block follows: rows
of comma-separated integers, closed by `HEIGHTMAPEND`. Some of those files
also contain `HEIGHTS` blocks (`HEIGHTS`, a level name, `8 8`, later
`HEIGHTSEND`). A Loriel leak rar in the Graal2002
folder has `forest.gmap` in the same shape (32 × 32, `GENERATED
forest_bf-32.nw`, two `HEIGHTS` blocks) plus 690 `GLEVNW01` `.nw` files and
one empty `.nw`.

No opened gmap uses `GENERATED 1` as a flag followed by one bare level name
per row. The gmaps in Zone, Kakariko, Aleria, Eternal, Aevum, Flower World,
GrimeCraft, and the Development Studio pack are the `LEVELNAMES` shape
above: quoted (or, once, unquoted) names inside the block, one grid row per
line.
