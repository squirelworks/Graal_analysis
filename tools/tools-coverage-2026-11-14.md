# Tool coverage: research, teardown, Rust (2026-11-14)

Date: 2026-11-14. Scope: every tool we hold, deduplicated (the same tree
catalogued in `../recovered-drive-tools/INVENTORY.md`), checked against three questions:

1. **Researched**: is the tool described anywhere in this repo (purpose,
   era, what it reads and writes)?
2. **Teardown**: is there a static teardown, either a hand-written
   `../recovered-drive-tools/ghidra-analysis/<tool>/SUMMARY.md` or a
   behaviour note with measured contracts (`classic-tools/`,
   `generators-222/`, `graalshop.md`, ...)? Tools that ship with source
   need no teardown; the column says "source".
3. **Rust**: is the job done in the Seihai Rust stack (`seihai`,
   `seihai-core`, `seihai-servertools`, `seihai-rc`, `seihai-gserver`,
   `seihai-listserver`, `seihai-npcserver`)? Python references in this
   repo do not count; AGENTS.md keeps them out of the Rust repos.

Static reads only. No tool was run for this note. Client builds held
alongside them (1.x to 6.x, Java, GameBoy, Zelda Online) are clients, not tools, and are covered by the
client notes (`../client-internals/build-catalogue.md`). Tutorials,
PSP/PSD art, gani and NPC sample packs and the GS2 syntax files are
material, not tools, and are left out.

## Answer

Not yet, and this note starts that work. Of 54 tools: 42 are researched, 32 have a teardown
or a measured behaviour note (or ship with source), and 18 have a Rust
equivalent for the job (before the pull requests below). The servers, RC/NC, the gani and level editors,
GS2 compilation and the asset formats are done in Rust. The offline
**LAT tool chain** is the big gap: level conversion, level and gmap
rendering, the three generators and gif2mng all have Python references
and measured notes here, and nothing in Rust.

## Gaps, ranked

Rank weighs what a Seihai server operator or LAT needs against how ready
the evidence is (a measured note or a format spec beats a bare catalogue
line).

| Rank | Gap | Tools it covers | Evidence ready | Rust home | State |
|---|---|---|---|---|---|
| 1 | Level conversion across generations (`.zelda`, `.graal` to `.nw`), and a gmap from a folder of levels | TextConvert / GRAALtoNWconverter, nw-converter, Graal Map Maker, MapGenerator | `formats/level-binary.md`, `classic-tools/text-convert.md`, `level-convert/README.md`; `seihai-core` already reads all three level formats and `GRMAP001` | `seihai-servertools level convert`, `gmap make` (lat-core) | in review: servertools #73; `.graal`/`.zelda` output needs seihai-core #58 |
| 2 | Render a level or a whole gmap to PNG | NW2PNG 1.3 to 2.1, graalmapview, Graal-Level-Viewer, PHP level viewer, Bruges' levelviewer, GraalMap Live View (static part) | `seihai-draw` paints tiles; `lat-core::preview` paints one level | `seihai-servertools level render`, `gmap render` | in review: servertools #73 |
| 3 | Terrain, dungeon and image-to-level generators | TerrainGenerator (2001, 2002), NW Dungeon Generator (2003), GraalLevelGen / GraalLevelGenNW, Emera's and the Python gmap generators | `generators-222/README.md` (gmap keys, level layout, Delphi LCG, 12-colour table, 8 by 11 dungeon blocks); `classic-tools/graal-level-gen.md` | `seihai-servertools gen terrain\|dungeon\|image` | in review: servertools #73 (maze and layout dungeons; other styles open) |
| 4 | gif2mng and GIF/PNG batch conversion | gif2mng, Assimilator GIF2PNG | `gif2mng.md` (one frame PNG, more MNG, `-b`), Assimilator SUMMARY; `seihai-core` reads GIF, PNG and MNG | lat-core (`check --make-gif` already writes GIF copies) | MNG/PNG writer in review: seihai-core #58; the command follows its tag |
| 5 | LevelFiller (theme fill of a level from tile groups) | LevelFiller + LFThemeMaker (2001), two copies | `levelfiller.md` (themes, quantities, placement, object language, `.tm` corner masks) | lat-core `level fill`, `theme make` | open: servertools #77 |
| 6 | GraalShop movie mode and shop pages | GraalShop 2002 builds, Graal Shop Preview | `graalshop.md` (movie grammar and keys), `graaleditor-vs-205.md` | lat-core gani editor (sprite frames already edit) | open: servertools #78 |
| 7 | Server stat pages | gserverstat, gserverstat2, GServer Stats (2004), player-count PHP | `classic-tools/gserverstat.md`, two SUMMARYs, `account13.py` | servertools, from seihai-gserver's account store | open, low |
| 8 | Character files (`CHR:1.00`) | Graal Character Designer 1.2.7, Character Generator 1.0, BinaryCrash Character / Head Viewer | `classic-tools/character-designer.md`, GCD and GChar SUMMARYs | `seihai` client (looks), not servertools | open, low |
| 9 | Small utilities | Graal Messenger, Graal Sound Fix, the two 1999 icon DLLs, apcalc, Guild Manager, guildcode, START-HUB | `small-utilities-2026-11-14.md` | none, except `.code` files (seihai-core #63) | done |
| 10 | DClient | DClientSetup 1198 (VB6) | DClient_setup SUMMARY: bootstrapper only; the CAB in this copy is a stub | none | blocked on a full copy |

## Every tool

`R` researched, `T` teardown or measured note, `Rust` the Rust equivalent.
"cat." means a catalogue line in `../recovered-drive-tools/INVENTORY.md`
or `manual/11-tools.md` and nothing more.

### Official generators, converters and viewers

| Tool | R | T | Rust |
|---|---|---|---|
| Graal Level Generator (2000-12, 2001-05) | yes | `classic-tools/graal-level-gen.md` | no (gap 3) |
| Graal Level Generator NW (2001-10) | yes | GraalLevelGenNW SUMMARY, `generators-222/` | no (gap 3) |
| Terrain Generator (2001, 2002) | yes | `generators-222/` | no (gap 3) |
| NW Dungeon Generator (2003-05) | yes | `generators-222/` (static read of the Linux build) | no (gap 3) |
| TextConvert / GRAALtoNWconverter | yes | TextConvert SUMMARY, `classic-tools/text-convert.md` | partial: lat-core reads `.graal` and writes `.nw`; no command (gap 1) |
| LevelFiller + levelviewer + LFThemeMaker | yes | `levelfiller.md` (v0.6 exe; the v0.7 exe is zero-filled) | no (gap 5, servertools #77) |
| PNGView | yes | PNGView SUMMARY | not needed (an image viewer) |
| Greaditor (NW level editor) | yes | `level-editor/version-deltas.md` (UPX, not unpacked) | yes: `seihai` level editor, servertools LAT level editor |
| GraalShop (gani / shop editor, 2002) | yes | `graalshop.md`, `graaleditor-vs-205.md` | partial: servertools gani editor (gap 6, #78) |
| Graal Character Designer 1.2.7 | yes | GCD SUMMARY, `classic-tools/character-designer.md` | no (gap 8) |
| Graal Character Generator 1.0 | yes | GChar SUMMARY, same note | no (gap 8) |
| Graal Clock 1.2.7 | yes | `client-internals/gserv-125-127-builds.md` item 8 (an offline launcher: clock, `.chr` load/save, starts `Graal.exe`; no socket) | yes for the job: `seihai-launcher` |
| Default characters and theme icon DLLs (1999) | yes | `small-utilities-2026-11-14.md` (16-bit NE icon libraries) | not needed |
| DClient | yes | DClient_setup SUMMARY | blocked (gap 10) |
| Script function list, client 6.0.0.7 | yes | reference text | used by `seihai-core` GS2 work |

### Servers, RC and NC

| Tool | R | T | Rust |
|---|---|---|---|
| GServer 1.19, 1.31, 1.34, 1.39, NW GServer, source archives | yes | gserver13, gserver-linux, gserver-win, Matriark SUMMARYs; source | yes: `seihai-gserver`, `seihai-gserver-v2` (GPL fork) |
| Server Lister / classic listserver | yes | serverlist3, ListServer SUMMARYs, `classic-tools/serverlist3.md` | yes: `seihai-listserver` |
| RemoteControl (classic, NW, custom, 2010, rc3 beta) | yes | four RC SUMMARYs, `remotecontrol.md`, `remotecontrol-lineage.md` | yes: `seihai-rc` |
| NPC Control (nc7132001, NPCControl 1.3) and the NPC server document | yes | NPCControl SUMMARY, `npc-control.md`, `npcserver-2001.md` | yes: `seihai-rc` NC, `seihai-npcserver` |
| Account creator (web, PHP) | cat. | source | partial: listserver accounts (`setup host-listserver`) |
| Secure login sample (GraalReborn) | cat. | source | yes: `seihai-core` secure login |
| GServer Stats, gserverstat, gserverstat2 | yes | two SUMMARYs, `classic-tools/gserverstat.md` | no (gap 7) |
| Guild Maker, guildcode, Guild Manager | yes | `server-tools-2001.md` (`.code` format), `small-utilities-2026-11-14.md` | `.code` files: seihai-core #63; guilds are a gserver feature |

### LAT (levels and maps)

| Tool | R | T | Rust |
|---|---|---|---|
| Graal Map Maker (2000) / MapGenerator / graalmapmaker | cat. | no | no (gap 1, gmap from a folder) |
| graalmapview (2001, with source) | cat. | source | no (gap 2) |
| NW2PNG 1.3 to 2.1 (Java, with source) | cat. | source | no (gap 2) |
| NW2TMX, nw-converter (GitHub) | cat. | source | no (gap 1) |
| Graal-Level-Viewer, PHP level viewer, Bruges' levelviewer | cat. | source / levelviewer = the NW one | no (gap 2) |
| Live map of players, GraalMap Live View | cat. | source | no; needs RC player positions (`seihai-rc`) |
| Gonstruct, GraalEditorW10, Graal Suits, OpenGraal LevelEditor | cat. | source | yes for the job: `seihai` level editor |
| TilesEditor / Graal Editor (39ster), Tiled 1.2.4 | yes | TilesEditor SUMMARY | yes for the job: `seihai` level editor |
| TilesetEditor (BinaryCrash) | cat. | no | partial: `seihai-core` tiledefs |
| TileDef scripts | yes | many notes on tile types | yes: `seihai-core` `TileTypes` |
| Emera's map generators (2013 to 2024), Python and PHP gmap generators | cat. | source | no (gap 3) |
| START-HUB (a GS1 level, not a launcher) | yes | `small-utilities-2026-11-14.md` | not needed |

### NAT (scripts)

| Tool | R | T | Rust |
|---|---|---|---|
| Script Editor 2.53 | yes | scripteditor SUMMARY | yes for the job: servertools NPC editor with the GS1 check |
| GS2 Compiler and BytecodeViewer | yes | BytecodeViewer SUMMARY, source | yes: `seihai-core` GS2 compiler and VM |
| BinaryCrash script engine | cat. | no | not needed |
| gs2-beautify | cat. | source | no; low |
| discord-gs2 | no | source | not needed |

### GAT and gani

| Tool | R | T | Rust |
|---|---|---|---|
| Assimilator GIF2PNG | yes | Assimilator SUMMARY | partial (gap 4) |
| gif2mng (client tree) | yes | `gif2mng.md` | no (gap 4) |
| GraalImageSearch | no | source | not needed |
| GraalViewer 2 / Rev2 / Rev5 / 2.1, GraalAnimViewer2 (with source) | cat. | source | yes: servertools gani editor preview, `seihai-core` gani |
| Gani-Edit web, Emera GaniEditor, GViewer, GraalImagePreviewer | cat. | source | yes for the job: servertools gani editor |
| Graal Character Viewer, Local Head Viewer (BinaryCrash) | no | no | partial: client looks (gap 8) |

### Website and misc

| Tool | R | T | Rust |
|---|---|---|---|
| WebRc (RC chat to a page) | no | source | no; would sit on `seihai-rc` |
| Server player count PHP + NPC | cat. | source | no (gap 7) |
| Graal Messenger | yes | `small-utilities-2026-11-14.md` (two logins, buddy `lister` commands) | optional, low: a `seihai-rc` mode |
| Graal Sound Fix | yes | source; `small-utilities-2026-11-14.md` | not needed |
| apcalc | yes | `small-utilities-2026-11-14.md` (AP bands, unpacked in a lab VM) | not needed |

## What is being built

Gaps 1 to 3 are in seihai-servertools #73 (`level convert|render`,
`gmap make|render`, `gen terrain|image|dungeon`), written from the format
and behaviour notes and `seihai-core`'s readers, not from the Python
here. The writers they and gap 4 need (`.graal`/`.zelda` levels, MNG) are
in seihai-core #58. Gap 5 (LevelFiller) and gap 6 (movie mode) now have teardowns and port
issues (servertools #77, #78); gap 9 is closed by `small-utilities-2026-11-14.md`. Progress is tracked in seihai-servertools issue #50
("Later") and its `docs/NEXT.md`.
