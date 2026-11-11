<!-- manual: kind=reference status=draft -->
# 11 Tools and the formats they define

The official and community tools around Graal, covered for the files they read and write and the behaviour that bears on those files. The byte-level formats themselves are in Part III; the staff wire protocols are in → §7.

> Status: draft.

## 11.0 Tool map

The table maps each tool to its role, the files it defines or writes, and the section that describes it [2.22] (tools/level-editor/README.md#classic-graal-level-editor-notes-by-version).

| Tool | Role | Files it defines or writes | Section | Source |
| --- | --- | --- | --- | --- |
| Built-in level editor | editor inside each client up to 2.22 | GR-V1.03, GLEVNW01, GOBJSET01 sets, map images | → §11.6 | [2.22] (tools/level-editor/README.md#classic-graal-level-editor-notes-by-version) |
| GraalEditor | standalone level editor from 2.3 | GLEVNW01 with `HEIGHTS`, gmaps | → §11.1 | [GE] (tools/graaleditor-vs-205.md#lineage) |
| GraalShop | GANI editor | `GANI0001`, `GANI0002` | → §11.2 | [bin] (tools/graaleditor-vs-205.md#graalshop-the-gani-editor) |
| TerrainGenerator, DungeonGenerator, GraalLevelGen | world generators | GLEVNW01, GR-V1.03, GRMAP001, `bigmap.txt`, `GDUNG001` options | → §11.3 | [bin][doc] (tools/generators-222/README.md#graal-222-generators) |
| gif2mng | image converter | PNG, MNG | → §11.4 | [bin] (tools/gif2mng.md#gif2mng) |
| RemoteControl, NPC Control | staff clients | — (wire only) | → §11.5, → §7 | [bin] (recovered-drive-tools/ghidra-analysis/RemoteControl_classic/SUMMARY.md) |
| TextConvert, Character Designer, GChar, gserverstat and others | converters, offline editors, server-side helpers | GLEVNW01, `CHR:1.00`, HTML leaderboards | → §11.7 | [bin] (tools/classic-tools/README.md#classic-server-side-tools) |

## 11.1 GraalEditor

### 11.1.1 Lineage and package

The facts below give how the standalone editor came out of the client and what its package holds [GE][2.05] (tools/graaleditor-vs-205.md#lineage).

| Fact | Source |
| --- | --- |
| Up to 2.22 the editor is built into the client (F4, refused online); 2.31 has no editor forms, and its start screen has an Editor button that launches `GraalEditor.exe` from the game folder | [GE][2.05] (tools/graaleditor-vs-205.md#lineage) |
| GraalEditor 2.3.1.1 (2005) is the same `TAdventure` program with the online client removed: the 2.05 main form, tool forms, toolbar hints and even game-only strings remain | [GE] (tools/graaleditor-vs-205.md#lineage) |
| It keeps the whole game model and GS1 interpreter, so Play runs a level locally; it has no network client, list-server host or login token | [GE] (tools/graaleditor-vs-205.md#lineage) |
| The shipped copy is a Thinstall package (magic `0x82D0B188`); the Delphi image is recovered by running the stub decompressor and its block codec | [bin] (tools/graaleditor.md#packing) |
| Version resource: company `Linux Cyberjoueur`, file version 2.3.1.1, internal name `Graal editor`, product `GraalEditor` | [bin] (tools/graaleditor.md#packing) |
| The main form is `TAdventure`, the document `TAdventureLevel`, the unit `UAdventureEditor` | [GE] (tools/graaleditor.md#document-model) |
| `Greaditor.exe` (2001, in the New World beta folders) is a separate UPX-packed editor that was not unpacked | [bin] (tools/level-editor/version-deltas.md#1-the-standalone-editors-one-line-each) |

### 11.1.2 Files

The rules below give which level formats GraalEditor opens and how it saves [GE] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205).

| Rule | Source |
| --- | --- |
| Open: GR-V1.00–1.03, Z3-V1.03/1.04 and GLEVNW01, with the filter `Graal levels (*.graal, *.nw)` | [GE] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205) |
| Save: GLEVNW01 with a new `HEIGHTS` section; the GR-V1 writer strings are still present; "Level(s) saved" means several levels can be saved at once | [GE][inf] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205) |
| The `BOARD 0` layer as GraalEditor writes it | disputed → App. E#600 |
| Heights are a `TLevelHeights` overlay per level, not a second board | [GE] (tools/graaleditor.md#document-model) |
| Sections read and written: `BOARD`, `LINK`, `SIGN`, `CHEST`, `NPC`, `BADDY`, `LEVELNAMES`, in the field order of the dialogs (→ §3.1.3) | [GE] (tools/graaleditor.md#document-model) |
| The editor stores no tile types; collision comes from the 4096-byte type table (→ §3.5.2) | [GE] (tools/graaleditor.md#collision) |
| gmaps are wired in: the `GRMAP001` reader plus `LEVELNAMES`, `MAPIMG`, `MINIMAPIMG`, `NOAUTOMAPPING` and the generator keys (→ §3.2); a `TEditorLevelCache` holds neighbours | [GE] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205) |
| 2.05 already has a dormant `GRMAP001` reader with no caller | [2.05][inf] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205) |
| Offline data: `offlinetutorial_*` (3×3) levels and `tiledefsOffline.txt` | [GE] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205) |

### 11.1.3 Additions over the 2.05 built-in editor

GraalEditor adds features over the 2.05 built-in editor. Each row gives an area and what was added [GE] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205).

| Area | GraalEditor | Source |
| --- | --- | --- |
| terrain | per-level height overlay, "Terrain Height Spot", "Show terrain grid" | [GE] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205) |
| palette | a fourth mode, Predefined NPCs, with a parameter grid | [GE] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205) |
| NPCs | one `TEditNPC` window with image, script, Test, Style and Find; scripts may carry `//#EDIT` and `//#COMMENTS` markers | [GE] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205) |
| character NPC | the same fields on four tabs (Look, Movement, Attack, General) | [GE] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205) |
| tiles | Export Tiles Array: the selection as one line of tile indices and as a script array | [GE] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205) |
| view and log | Hide npcs, Show terrain grid, a log window | [GE] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205) |
| sound | BASS, with the function set the 2.22 client imports | [GE] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205) |
| integrity | the client self-check plus RSA/SHA-1 checks of `GraalEditor.sig` and `arrays2.sig`; live, the editor starts with no `GraalEditor.sig` and with a corrupted `arrays2.sig`, so the check does not gate start-up (→ §3.5.5) | [GE] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205) |
| unchanged | the tile undo model, the link, sign, chest and baddy dialogs, GOBJSET01 sets, right-click copy, Generate map → `graalmap.png` | [GE] (tools/graaleditor-vs-205.md#what-graaleditor-adds-over-205) |

## 11.2 GraalShop

GraalShop is the period gani editor. The facts below say what it is and where its name comes from [bin] (tools/graaleditor-vs-205.md#graalshop-the-gani-editor).

| Fact | Source |
| --- | --- |
| `GraalShop.exe` 1.1.1.0 ("Gani Editor", 2006) and `GraalShop_old.exe` (2002) are Delphi programs with one main form, "Graal Shop - The Graal Animation Editor", and an Add sprite dialog; they edit `.gani` files only | [bin] (tools/graaleditor-vs-205.md#graalshop-the-gani-editor) |
| The name is a pun on Photoshop, not a store | [doc] (tools/graalshop.md#graalshop) |
| The model holds sprites with attachments (`ATTACHSPRITE`, `ATTACHSPRITE2`), frames of placements and sounds, and in movie mode actors and actor modifiers; undo and redo are a list of edit operations | [bin] (tools/graaleditor-vs-205.md#model) |
| Sprite mode (`GANI0001`): direction selector, sprite-definition grid, frame strip and canvas; play, add, delete, copy and insert frames, add sound, add, import or prune sprite definitions, reverse the animation, undo, redo, file actions; selected sprites can be moved, raised, lowered and keyed by x/y | [bin] (tools/graaleditor-vs-205.md#workflow) |
| Movie mode (`GANI0002`): a timeline of CHAR, SPRITE, SOUND and TEXT actors; TEXT has font, zoom, size, alignment, wordwrap and shading; CHAR has ani, dir, head, body, sword, shield, horse, colours, attr and param; options Automatic Gani Setting and Graal2002 ganis | [bin] (tools/graaleditor-vs-205.md#workflow) |
| Header fields are edited in a grid and written as `LOOP`, `BACKCOLOR`, `SETBACKTO`, `DEFAULTHEAD`, `DEFAULTBODY`, `DEFAULTPARAM`, `DEFAULTATTR`, the effect keys and `SCRIPT` … `SCRIPTEND` (→ §3.3.4) | [bin] (tools/graaleditor-vs-205.md#workflow) |
| The script block is copied, not run | [bin] (tools/graalshop.md#contract) |
| Preview uses DirectDraw 7 and plays `PLAYSOUND` steps through DirectSound; default art is `sprites.png`, `body.png`, `head0.png`, `shield1.png`, `ride.png`, `soundicon.png`; the Graal folder is found through `Graal.exe` and `FILENAMECACHE.txt`, and `pms`, `profiles` and `weblevels` are searched | [bin] (tools/graaleditor-vs-205.md#workflow) |
| `GraalShop_old` has sprite mode only: no `GANI0002`, `MOVIE`, `ACTOR`, `ATTACHSPRITE2` or `ROTATEEFFECT` | [bin] (tools/graaleditor-vs-205.md#workflow) |
| 2.05 plays only the sprite-mode subset (`SPRITE`, `ANI` … `ANIEND`, `WAIT`, `PLAYSOUND`, `LOOP`, `CONTINUOUS`, `SETBACKTO`, `SINGLEDIRECTION`, `COLOREFFECT`, `ZOOMEFFECT`), so movie-mode ganis and attachments from the 2006 GraalShop do not play there | [2.05] (tools/graaleditor-vs-205.md#how-this-compares-with-what-205-can-play) |
| The offline tile definition in the client tree is `picso.png,offlinetutorial,1,0,0` | [file] (tools/graalshop.md#contract) |

## 11.3 Generators

Three writers emit `GLEVNW01` and `GRMAP001`, each with a different key set; one writer's output is not a valid input for another's loader (the key sets are → §3.2.3) [bin] (tools/generators.md#generators).

### 11.3.1 Builds

Several level generators survive. Each row gives a program, its date and what it writes [bin] (tools/generators-222/README.md#graal-222-generators).

| Program | Date | Writes | Source |
| --- | --- | --- | --- |
| `TerrainGenerator.exe` | 2003-12-16 | `GRMAP001` generator form and GLEVNW01 levels of tile 0 with a 9×9 `HEIGHTS` block and edge links | [bin] (tools/generators-222/README.md#graal-222-generators) |
| `dungeongen.exe` and the Linux `dungeongen` | 2003-05-23 | GLEVNW01 levels from `GDUNG001` options, short `GRMAP001` | [bin] (tools/generators-222/README.md#graal-222-generators) |
| `GraalLevelGen_nw-gmap.exe` | 2003-03-07 | GLEVNW01 and a `LEVELNAMES` gmap; GR-V1.03 when the output name does not end in `.nw` | [bin] (tools/generators-222/README.md#not-reimplemented) |
| `GraalLevelGen_graal-txt.exe` | 2004-01-18 | GR-V1.03 levels and `bigmap.txt` | [bin] (tools/level-tools-gaps/README.md#graal-txt-and-nw-txt) |
| `GraalLevelGen_nw-txt.exe` | 2001-06-30 | GLEVNW01 levels and `bigmap.txt` | [bin] (tools/level-tools-gaps/README.md#graal-txt-and-nw-txt) |
| `GraalLevelGen.exe` | December 2000 | levels named `.graal` and `bigmap.txt`; the readme says New World format and not for 1.39 or older | [doc][bin] (tools/classic-tools/graal-level-gen.md#graallevelgen-december-2000) |
| `GraalLevelGenNW.exe` | 2001-10-08 | a New World levels tree from a map image, with calendar fields and per-level options such as whether warping is allowed | [bin] (recovered-drive-tools/ghidra-analysis/GraalLevelGenNW/SUMMARY.md) |

No generator imports a socket library; output stays in the chosen folder [bin] (tools/classic-tools/graal-level-gen.md#what-it-never-sends).

### 11.3.2 TerrainGenerator

The rules below give TerrainGenerator's options and how it builds the height field [doc][bin] (tools/generators-222/README.md#terrain).

| Rule | Source |
| --- | --- |
| Dialog fields: grid width and height, base, height, chaos, even borders, an islands preset (even borders, the rim kept at the base) and a seed | [doc][bin] (tools/generators-222/README.md#terrain) |
| The height field is plasma midpoint displacement | [bin] (tools/generators.md#terraingenerator) |
| gmap keys in order: `WIDTH`, `HEIGHT`, `GENERATED 1`, `GENSEED`, `GENBASE`, `GENEVENBORDERS`, `GENHEIGHT`, `GENCHAOS`, `LEVHEIGHT`, `LEVCHAOS`, `MAPIMG`, one level name per line, `HEIGHTMAP`, `RANDOMSEEDS` | [bin] (tools/generators-222/README.md#terrain) |
| Level names: world name, an `A`…`Z`/`AA` column, a zero-padded row, `.nw` | [bin] (tools/generators-222/README.md#terrain) |
| A level is 64 `BOARD` rows of tile 0, a `HEIGHTS` block of nine lines of nine numbers, and a `LINK` on each edge with a neighbour; no NPC section | [bin] (tools/generators-222/README.md#terrain) |
| Edge arrivals: west 61, east 0, north 61, south 0; the other axis is `playerx` or `playery` | [bin] (tools/generators-222/README.md#terrain) |

### 11.3.3 DungeonGenerator

The rules below give DungeonGenerator's options file and how it cuts a layout into levels [file] (tools/generators-222/README.md#dungeon).

| Rule | Source |
| --- | --- |
| `dungeonoptions.txt` starts with `GDUNG001`; a `LAYOUTFILE` of `X` (wall) and `.` (path) wins over `LAYOUTSTYLE` | [file] (tools/generators-222/README.md#dungeon) |
| Each layout cell is 8 tiles wide and 11 tall, cut into 64×64 levels named `LEVELSTART`, a column letter and a 1-based row (`cave_A1.nw`) | [doc][bin] (tools/generators-222/README.md#dungeon) |
| The gmap is three lines after the signature: `WIDTH`, `HEIGHT`, `GENERATED` with the bottom-right name | [bin] (tools/generators-222/README.md#dungeon) |
| Each level is one base64 `BOARD`, edge links and `NPC` blocks; stamp 0 becomes a 4×4 ground fill, stamp 1 is a hole and is not written | [bin] (tools/generators.md#dungeongenerator) |
| Place names for NPCs and 88-id `TILES` blocks: `path`; `walln`/`walls`/`wallw`/`walle` (one open side, wall opposite); `wallnw`/`wallne`/`wallsw`/`wallse` (one open diagonal); the `…2` corner forms (two adjacent open sides); `walld1` (open north and south) and `walld2` (open east and west); `wall` otherwise | [doc][file][bin] (tools/generators-222/README.md#dungeon) |
| `NPC` lines take `image`, `script`, `blocking`, `underplayer`, `dominant`, `chance` (1–100, `%` optional), `place`, `x`, `y`; false `blocking` adds `dontblock`, `underplayer` adds `drawunderplayer` | [bin] (tools/generators-222/README.md#dungeon) |
| `ADDTESTNPCS` adds one test NPC per level running `addtiledef`, `addtiledef2` and `loadmap` | [doc][bin] (tools/generators-222/README.md#dungeon) |
| `LAYOUTSYMMETRY` 1 none, 2 vertical mirror, 3 horizontal mirror, 4 both, 0 picks 1–4 from the seed; `DOUBLE 1` draws at half size and scales up; `LAYOUTORIENTATION` is stored | [doc][bin] (tools/generators-222/README.md#dungeon) |
| The random styles (maze, onion, spiral, rogue, snake, square spiral) come from the linked DungeonMaker 0.9 library, which reads `layouts/rooms*`, `layouts/stats*` and `layouts/constants`; its crawler steps are unmeasured | [bin][doc] (tools/level-tools-gaps/README.md#dungeonmaker-09) |

### 11.3.4 GraalLevelGen

GraalLevelGen builds levels from a picture. The rules below give how the picture is read [doc] (tools/classic-tools/graal-level-gen.md#what-the-operator-does).

| Rule | Source |
| --- | --- |
| The input picture is 64 pixels per level across and down, saved as gif or 8-bit png | [doc] (tools/classic-tools/graal-level-gen.md#what-the-operator-does) |
| The pixel grid is `(width + 5) // 6` by `(height + 5) // 6` cells, each read at `(x × 6, y × 6)`; a colour matches when the sum of absolute channel differences is under 32 | [bin] (tools/generators-222/README.md#level-generator); [bin] (tools/level-tools-gaps/README.md#water-mountain-and-sand-edges) |
| Forest blits a 6×5 stamp of tiles 25–30, 41–46, 57–62, 73–78, 89–94 at `(x × 6, y × 6 + 1)`, shifted 3 tiles left on odd rows | [bin] (tools/generators-222/README.md#level-generator) |
| Other colours write one fill tile: water 12, mountains 80, flowers 4, sand 5, puddle 6, puddle stone 7, small stones 8, big stone 9, swamp 10, bushes 11; grass and unknown colours write nothing | [bin] (tools/generators-222/README.md#level-generator) |
| Water, mountain and sand edges are blitted from neighbour flags; the stamp-to-shore table is unmeasured | [bin] (tools/level-tools-gaps/README.md#water-mountain-and-sand-edges) |
| nw-gmap names are `world_a-01.nw` to `world_z-99.nw`, and the gmap is `WIDTH`, `HEIGHT` and quoted `LEVELNAMES` rows; edge links use the 0/61 arrivals | [doc][bin] (tools/generators-222/README.md#level-generator) |
| graal-txt names are prefix + column + `-` + row + `.graal`; nw-txt names drop the dash and end in `.nw`; column letters are `a` + index mod 26 with a leading letter from 26 levels across; the row is 1-based with leading zeros from 10 and 100 levels down | [bin] (tools/level-tools-gaps/README.md#graal-txt-and-nw-txt) |
| `bigmap.txt` is one row per line of `"name","name"` (the editor's M-key map) | [bin][doc] (tools/level-tools-gaps/README.md#graal-txt-and-nw-txt) |
| A second run on existing levels keeps their links and NPCs and paints only the new non-grass tiles | [doc] (tools/generators-222/README.md#level-generator) |

Colour table, the same in the December 2000 build and the nw-gmap build [doc][bin] (tools/classic-tools/graal-level-gen.md#what-the-operator-does); [doc][bin] (tools/generators-222/README.md#level-generator):

| Index | Meaning | RGB | Source |
| ---: | --- | --- | --- |
| 0 | grass, not drawn | 24, 140, 24 | [doc] (tools/generators-222/README.md#level-generator) |
| 1 | forest | 181, 239, 189 | [doc] (tools/generators-222/README.md#level-generator) |
| 2 | water | 0, 0, 255 | [doc] (tools/generators-222/README.md#level-generator) |
| 3 | mountains | 128, 0, 0 | [doc] (tools/generators-222/README.md#level-generator) |
| 4 | flowers | 255, 0, 0 | [doc] (tools/generators-222/README.md#level-generator) |
| 5 | sand | 150, 110, 0 | [doc] (tools/generators-222/README.md#level-generator) |
| 6 | puddle | 0, 255, 255 | [doc] (tools/generators-222/README.md#level-generator) |
| 7 | puddle stone | 0, 179, 179 | [doc] (tools/generators-222/README.md#level-generator) |
| 8 | small sand stones | 113, 82, 0 | [doc] (tools/generators-222/README.md#level-generator) |
| 9 | big sand stone | 83, 61, 0 | [doc] (tools/generators-222/README.md#level-generator) |
| 10 | swamp | 0, 106, 0 | [doc] (tools/generators-222/README.md#level-generator) |
| 11 | bushes | 0, 66, 0 | [doc] (tools/generators-222/README.md#level-generator) |

## 11.4 gif2mng

gif2mng converts images for the client. The rules below say what it does [bin] (tools/gif2mng.md#gif2mng).

| Rule | Source |
| --- | --- |
| A GIF converter with banner date 2004-06-03, units `UGif` and `UMNG`, zlib linked | [bin] (tools/gif2mng.md#gif2mng) |
| One frame becomes PNG, two or more become MNG | [bin] (tools/gif2mng.md#gif2mng) |
| `-b` rewrites the existing palette to the seven Graal body-colour slots and forces transparent index 2; it does not add a second palette (the slots' draw roles are → §2.6.3) | [bin] (tools/gif2mng.md#gif2mng) |
| The seven slot RGB values and the MNG `TERM` delay fields are unmeasured | [doc] (tools/level-tools-gaps/README.md#gif2mng) |

## 11.5 RemoteControl and NPC Control

The RC and NC wire protocols, logins and commands are → §7; the RC lineage from `GSERV014` to `GSERV023` is → §7.1. This section lists the recovered staff-client binaries and what each shows.

| Binary | Toolkit | Behaviour | Source |
| --- | --- | --- | --- |
| `RemoteControl.exe` (classic `rc.rar` line) | Delphi | server-list connect screen; registry prefs, a local startup script and password fields; NPC attributes, script and flags, NPC level list, local NPCs; player count and NPC-server status; account and player editors; deflate | [bin] (recovered-drive-tools/ghidra-analysis/RemoteControl_classic/SUMMARY.md) |
| custom `remotecontrol.exe` and a UPX `Agret_RC.exe` variant | Delphi | the classic RC role with a blue theme and a text config with nickname and UI-colour keys; the unpacked `Agret_RC.exe` is a different build | [bin] (recovered-drive-tools/ghidra-analysis/remotecontrol_custom/SUMMARY.md) |
| `RemoteControl-NW.exe` (New World packs, NC V2 pack) | Delphi | account and player editors and a database account search by admin level, admin worlds and block state; admin message and broadcast, edit account, update level, disconnect, ban, away-on-close, HTML in PMs | [bin] (recovered-drive-tools/ghidra-analysis/RemoteControl-NW/SUMMARY.md) |
| `RemoteControl3.exe` (RC3 beta, also in a 5.x pack) | GTK on Windows | server list, version and password fields; list-server and separate NPC-server connections; player list with mass PM and admin message, NPC lists, level-NPC dump, folder and config pages, profile, rights, account and access editors; ban with time and reason, warps, disconnect, update level, separate NC chat; bzip2 and zlib; highlighters for Graal script, ini, Pascal and C++ | [bin] (recovered-drive-tools/ghidra-analysis/RemoteControl3/SUMMARY.md) |
| `NPCControl.exe` (`nc7132001`, July 2001) | Delphi | a text config of server name, port and password mirrored in the registry; NPC and weapon management, take a script from a class, edit weapon scripts, local NPCs; deflate | [bin] (recovered-drive-tools/ghidra-analysis/NPCControl/SUMMARY.md) |

## 11.6 Level editor

The built-in editor, with 2.22 as the reference and every other build as a delta. The 2.05-specific in-client behaviour is → §4.9. Formats it reads and writes are → §3.1 [2.22] (tools/level-editor/README.md#classic-graal-level-editor-notes-by-version).

### 11.6.1 Entering, window and modes (2.22)

In 2.22 the editor is a mode of the game window. The rules below give how it is entered and laid out [2.22] (tools/level-editor/222-reference.md#1-entering-and-leaving).

| Rule | Source |
| --- | --- |
| The editor is the `TAdventure` main form in a second mode; the same exe plays and edits | [2.22] (tools/level-editor/222-reference.md#1-entering-and-leaving) |
| F4 opens it and is refused online ("You cannot open the editor in the online mode."); from a tutorial level it opens a new empty level | [2.22] (tools/level-editor/222-reference.md#1-entering-and-leaving) |
| F5 opens Load level; P or Play returns to the game on the current level, saving every modified level first since 2.13 | [2.22] (tools/level-editor/222-reference.md#1-entering-and-leaving) |
| A level path as the first command-line argument skips the login screen and opens it in the editor | [2.22] (tools/level-editor/222-reference.md#1-entering-and-leaving) |
| F10 toggles the window border; Esc warns before leaving; dropping a text file creates an NPC from it | [2.22] (tools/level-editor/222-reference.md#1-entering-and-leaving) |
| Board view: 64 × 64 tiles at 16 px with scroll bars, wheel and arrow-key scrolling | [2.22] (tools/level-editor/222-reference.md#2-window-and-tool-modes) |
| Toolbar order: New, Open, Save, Save as, Undo board copy, Cut, Copy, Paste, Delete, Turn selection into a warp field, Edit links, Edit signs, selection-as-text (2.16), Close, Play | [2.22] (tools/level-editor/222-reference.md#2-window-and-tool-modes) |
| One tab per open level; Close asks about unsaved changes | [2.22] (tools/level-editor/222-reference.md#2-window-and-tool-modes) |
| Palette modes: predefined object (stamp), tile palette, baddies/NPCs/chests, predefined NPCs (`defnpc*.txt` with an `#EDIT` grid) | [2.22] (tools/level-editor/222-reference.md#2-window-and-tool-modes) |
| Blocking, foreground and terrain overlays are computed from the type table, not stored | [2.22] (tools/level-editor/222-reference.md#2-window-and-tool-modes) |
| Editor control-NPCs (2.13): `editnpc<Name>.txt` scripts editor actions with `mousex`, `mousey`, `mousescreenx`, `mousescreeny` and `mousebuttons` (left 1, middle 2, right 4); only tile changes are supported | [2.22] (tools/level-editor/222-reference.md#2-window-and-tool-modes) |
| M builds a PNG map image of the level, and of a gmap from 2.16 rev 7 | [2.22] (tools/level-editor/222-reference.md#2-window-and-tool-modes) |
| The mouse state machine (select, drag, drop, double-click by kind) is known only in outline: left drag selects or paints, right button on an object clones it, right button elsewhere flood-fills, double-click opens an object's dialog or makes a tile the background tile | [2.22] (tools/level-editor/222-reference.md#2-window-and-tool-modes) |

### 11.6.2 Level model (2.22)

The editor holds a level as a set of lists. Each row gives one list and what an element holds [2.22] (tools/level-editor/222-reference.md#3-level-model).

| List | Element | Source |
| --- | --- | --- |
| board | 64 × 64 16-bit tile ids, index y × 64 + x | [2.22] (tools/level-editor/222-reference.md#3-level-model) |
| links | destination, x, y, w, h, new-x text, new-y text | [2.22] (tools/level-editor/222-reference.md#3-level-model) |
| signs | x, y in tiles, text | [2.22] (tools/level-editor/222-reference.md#3-level-model) |
| chests | x, y, item, sign index | [2.22] (tools/level-editor/222-reference.md#3-level-model) |
| NPCs | image or none, x, y in fractional tiles, script | [2.22] (tools/level-editor/222-reference.md#3-level-model) |
| baddies | x, y, type, three verse strings | [2.22] (tools/level-editor/222-reference.md#3-level-model) |
| heights | optional 9 × 9 floats | [2.22] (tools/level-editor/222-reference.md#3-level-model) |
| cache | recently loaded levels, for the link walker and gmaps (2.17 on) | [2.22] (tools/level-editor/222-reference.md#3-level-model) |

### 11.6.3 Open and save (2.22)

The rules below give how the 2.22 editor opens and saves levels [2.22] (tools/level-editor/222-reference.md#open).

| Rule | Source |
| --- | --- |
| The open filter is `Graal levels (*.graal, *.nw)`; several files open in their own tabs | [2.22] (tools/level-editor/222-reference.md#open) |
| The loader branches on the first eight bytes: `GLEVNW01` text; `GR-V1.00`–`1.03` binary (13-bit codes for 1.02/1.03, 12-bit for 1.00/1.01); `Z3-V1.03`/`1.04`; anything else is rejected ("Unsupported file type!", no caller found) | [2.22] (tools/level-editor/222-reference.md#open) |
| `GR-V1.04` is read only by the weblevels cache path, not by the editor | [2.22] (tools/level-editor/222-reference.md#open) |
| The text reader rules (layer field ignored, row skipping, 12-bit tile ids, `LINK` defaults, `BADDY` clamp, `HEIGHTS` only when an overlay exists) are → §3.1.3 | [2.22] (tools/level-editor/222-reference.md#the-glevnw01-text-reader-222) |
| Save (Ctrl+S) is save-all: it commits a floating paste, then saves every modified level with a file name plus the current one, deleting the old file and writing in place; a modified map is saved too; the status bar shows "N Level(s) saved" | [2.22] (tools/level-editor/222-reference.md#save-222) |
| The extension picks the format: `.nw` writes GLEVNW01, anything else GR-V1.03; the editor never writes Z3-V1, GR-V1.00–1.02 or GR-V1.04 | [2.22] (tools/level-editor/222-reference.md#save-222) |
| The text writer emits `HEIGHTS` only when the overlay is marked modified (2.05 never does) | [2.22] (tools/level-editor/222-reference.md#save-222) |
| Chests and baddies are written only when two obfuscated session-mode flags are both clear; otherwise only the terminators; the same flags gate the loaders; that they are a New World mode switch is an inference | [2.22][inf] (tools/level-editor/222-reference.md#save-222) |
| 2.22 deletes before writing, so a crash loses the level; the 2.3 change log says the editor then writes a copy and renames it | [2.22] (tools/level-editor/222-reference.md#safety) |

### 11.6.4 Editing tools (2.22)

The rules below give the editor's tools and how tiles and tile definitions are addressed [2.22] (tools/level-editor/222-reference.md#5-tiles-and-the-sheet).

| Rule | Source |
| --- | --- |
| Tile ids are 0–4095 on the 2048 × 512 sheet; the id → sheet mapping is → §3.5.1 | [2.22] (tools/level-editor/222-reference.md#5-tiles-and-the-sheet) |
| A tile definition line is `image,prefix,type,x,y`; type 0 is the old order and type 1 the new; type 4 and its x offsets are unmeasured | [2.22][inf] (tools/level-editor/222-reference.md#5-tiles-and-the-sheet) |
| Palette: click picks one tile, drag picks a block that pastes as a floating selection; double-click sets the background tile, which fills new levels | [2.22] (tools/level-editor/222-reference.md#5-tiles-and-the-sheet) |
| Undo covers board tiles only: a rectangle snapshot before each write, at most 128 records per tab | [2.22] (tools/level-editor/222-reference.md#6-selection-paste-undo-fill) |
| Draw mode: with one tile selected, left drag paints (1.41); flood fill with the right button (2.00), Shift for complete objects only, and the background tile when nothing is selected | [2.22] (tools/level-editor/222-reference.md#6-selection-paste-undo-fill) |
| Turn selection into a warp field: a link over the selection with new x `playerx` and new y `playery`, then the first matching edge rule: starts in column 63 → new x 0; row 63 → new y 0; column 0 and one wide → new x 61; row 0 and one high → new y 61 | [2.22] (tools/level-editor/222-reference.md#6-selection-paste-undo-fill) |
| Stamps come from `objects<set>.txt` in GOBJSET01 (→ §3.4); add-selection inserts after the chosen stamp and Save objects rewrites the set; placing writes tile ids only; sets arrived in 2.04 | [2.22] (tools/level-editor/222-reference.md#7-stamps-predefined-objects) |
| Edit links (L): Linkfile, X, Y, W, H, New X, New Y; Load opens the destination in a tab; the dialog refuses invalid fields with "Wrong values! Type in a filename…"; arrival text is stored as typed | [2.22] (tools/level-editor/222-reference.md#8-links) |
| Whether the engine evaluates an arrival such as `playery+10` at warp time | disputed → App. E#601 |
| Edit signs (S): X, Y, New, Delete; a (0, 0) sign is not drawn and is used by index from chests and `say n`; text is in the sign alphabet (→ §3.6); trailing empty lines are removed | [2.22] (tools/level-editor/222-reference.md#9-signs) |
| Chest dialog: item, sign index, Sign button; items in index order `greenrupee, bluerupee, redrupee, bombs, darts, heart, glove1, bow, bomb, shield, sword, fullheart, superbomb, battleaxe, goldensword, mirrorshield, glove2, lizardshield, lizardsword, goldrupee, fireball, fireblast, nukeshot, joltbomb, spinattack`; a new chest is item 1, sign −1 | [2.22] (tools/level-editor/222-reference.md#10-chests) |
| Baddy dialog: ten types (Gray, Blue, Red, Shooting and Swamp Soldier, Frog, Spider, Golden Warrior, Lizardon, Dragon) and three verses; types 4–6 disable and save empty verses; a new baddy says "Stop!" and "Ouch!" | [2.22] (tools/level-editor/222-reference.md#11-baddies) |
| NPC dialog: image, script, Test, Style, Find; `//#EDIT name value` and `//#COMMENTS text` markers; predefined NPCs replace each named variable on drop; NPC positions survive a binary save only as whole and half tiles | [2.22][inf] (tools/level-editor/222-reference.md#12-npcs) |
| Multi-level editing (2.12): when an NPC calls `setmap` the neighbours show together; scroll by dragging the player or with arrows; a big cursor on maps (2.13) | [2.22] (tools/level-editor/222-reference.md#14-tabs-maps-and-multi-level-editing) |
| Other dialogs: load by name, log window, `TShowImg` (role unmeasured), variable editor, tile-array window | [2.22] (tools/level-editor/222-reference.md#15-other-dialogs) |

Keys, 2.22 [2.22] (tools/level-editor/222-reference.md#13-keys):

| Key | Action | Source |
| --- | --- | --- |
| Ctrl+N, Ctrl+O, Ctrl+S | New, Open, Save (save-all) | [2.22] (tools/level-editor/222-reference.md#13-keys) |
| Ctrl+Z, Alt+Backspace | Undo board copy | [2.22] (tools/level-editor/222-reference.md#13-keys) |
| Ctrl+X / Shift+Del, Ctrl+C / Ctrl+Ins, Ctrl+V / Shift+Ins, Del | Cut, Copy, Paste, Delete | [2.22] (tools/level-editor/222-reference.md#13-keys) |
| L, S, P, M | Edit links, Edit signs, Play, map image; ignored while a side-panel combo has focus | [2.22] (tools/level-editor/222-reference.md#13-keys) |
| Ctrl+Q | batch re-save of every level named in the loaded map, by extension (2.17.1, 2.22) | [2.22] (tools/level-editor/222-reference.md#13-keys) |
| F10, Esc | border toggle, warning before leaving | [2.22] (tools/level-editor/222-reference.md#13-keys) |

### 11.6.5 Builds as deltas from 2.22

Other builds' editors are described as differences from 2.22. Each row gives a build and its delta [2.17] (tools/level-editor/version-deltas.md#5-deltas-as-a-checklist-per-build-relative-to-222).

| Builds | Delta | Source |
| --- | --- | --- |
| 2.17.1 | none found; same class list | [2.17] (tools/level-editor/version-deltas.md#5-deltas-as-a-checklist-per-build-relative-to-222) |
| 2.05, rev 1, rev 2 | no heights, cache, tiles-array or log windows, no predefined NPCs; separate person-image and script dialogs; a sign-codes window; open filter `*.graal`; the map parser present from rev 1 but dormant; GLEVNW01 first appears; the chest clamp is gone | [2.05] (tools/level-editor/version-deltas.md#3-formats-per-build) |
| 2.0 rev 3 to 2.04 | no GLEVNW01 reader or writer; `.zelda` dropped from the open filter at 2.0 rev 3 (the reader still accepts it); object sets and tile definitions from 2.04; chests clamped to 0–62 and NPCs to 0–63 on load | [2.04][inf] (tools/level-editor/version-deltas.md#3-formats-per-build) |
| 2nd Graal to 2.0 rev 2 | read GR-V1.00–1.03 and Z3-V1.03/1.04, save GR-V1.03; filter `*.graal, *.zelda`; same clamps | [1.39][2.00] (tools/level-editor/version-deltas.md#3-formats-per-build) |
| 1.28b2 to 1.33 | baddy class still named opponent; character NPC dialog present | [bin] (tools/level-editor/version-deltas.md#2-class-timeline-of-the-built-in-editor) |
| before 1.28b2 | no character dialog or level class; 2nd Graal adds chest and person dialogs, 3rd Graal the flags dialog; 1st Graal reads only Z3-V1 and has no chest or NPC dialog | [bin] (tools/level-editor/version-deltas.md#2-class-timeline-of-the-built-in-editor) |
| New World betas | no chest and no baddy editor or class; heights and map in beta 1; text format in the beta's own `levelformat.txt` | [bin] (tools/level-editor/version-deltas.md#2-class-timeline-of-the-built-in-editor) |
| 2.1 test builds | combined NPC dialog, predefined NPCs, no sign-codes window | [bin][doc] (tools/level-editor/version-deltas.md#2-class-timeline-of-the-built-in-editor) |
| 2.31 | no editor dialogs; the level model and GR-V1.04 reader remain for the game; no GLEVNW01 | [2.31] (tools/level-editor/version-deltas.md#3-formats-per-build) |

The rules below give the loader limits that differ between builds [bin] (tools/level-editor/version-deltas.md#3-formats-per-build).

| Rule | Source |
| --- | --- |
| The load clamps are compares against 62 for chests and 63 for NPCs in the 1.39, 2.00 and 2.04 loaders, absent from 2.05 on; a chest at x = 63 loads at 62 up to 2.04 | [bin] (tools/level-editor/version-deltas.md#3-formats-per-build) |
| The baddy section ends at a record shorter than three bytes or whose first byte is 0x80 or more, with no x = 0 test, in 1.39, 2.00, 2.05, 2.17.1 and 2.22 | [bin] (tools/level-editor/formats-crossref.md#batch-f-decomp-findings-2026-10-25-f-pr-39) |
| The editor writes double runs (`ABAB…`, up to 64 pairs) in GR-V1 boards, and a newline after each chest record | [2.22] (tools/level-editor/formats-crossref.md#formatslevel-binarymd-and-level-binary-clientmd) |

Change-log dated editor features, from the shipped `newfeatures` files [doc] (tools/level-editor/version-deltas.md#4-change-log-dated-features):

| Version | Features | Source |
| --- | --- | --- |
| 1.41 | drag painting with one tile, M map PNG, status-bar position and tile, double-click background tile, no selection outside the level, drop a text file to make an NPC, trailing sign lines trimmed, new levels use the background tile | [doc] (tools/level-editor/version-deltas.md#4-change-log-dated-features) |
| 2.00 | flood fill with the right button | [doc] (tools/level-editor/version-deltas.md#4-change-log-dated-features) |
| 2.04 | object sets; `addtiledef`, `addtiledef2`, `removetiledefs` | [doc] (tools/level-editor/version-deltas.md#4-change-log-dated-features) |
| 2.1 | predefined NPCs, merged sign-code and add-NPC windows, multi-tile palette selection, F4 on a tutorial opens an empty level | [doc] (tools/level-editor/version-deltas.md#4-change-log-dated-features) |
| 2.12 | multi-level editing on `setmap`, scrolling by player drag or arrows | [doc] (tools/level-editor/version-deltas.md#4-change-log-dated-features) |
| 2.13 | scrollbars on single levels, big cursor on maps, Play saves all, editor control-NPCs | [doc] (tools/level-editor/version-deltas.md#4-change-log-dated-features) |
| 2.13 rev 3 | dropped objects can be released and moved; caching and Play position fixes | [doc] (tools/level-editor/version-deltas.md#4-change-log-dated-features) |
| 2.15 | wheel scrolling, arrow scrolling on single levels | [doc] (tools/level-editor/version-deltas.md#4-change-log-dated-features) |
| 2.16 | selection-as-text button, `showimg` and `putnpc` in editor NPCs, map-level fixes; M on gmaps from rev 7 | [doc] (tools/level-editor/version-deltas.md#4-change-log-dated-features) |
| 2.3 | editor and client become separate exes; write-copy-and-rename saving; filename cache | [doc] (tools/level-editor/version-deltas.md#4-change-log-dated-features) |

## 11.7 Other tools

Other period tools are listed here. Each row gives a tool, what it does and the files it uses [bin][doc] (tools/classic-tools/text-convert.md#textconvert).

| Tool | What it does | Files | Source |
| --- | --- | --- | --- |
| TextConvert | on start, walks the current folder and subfolders and converts every GR-V1 level to GLEVNW01, links included; no socket | GR-V1.00–1.03 in, GLEVNW01 out; errors `Wrong link data!`, `Wrong chest data!`, `Decompression error!` | [bin][doc] (tools/classic-tools/text-convert.md#textconvert) |
| Graal Character Designer 1.2.7 (Nov 1999) and GChar 1.0 | offline character-look editors; need `headsconfig.txt`, `levels\heads\`, `levels\gifs\`, `levels\webgifs\`; import `*.chi` files and rename them `*.chr`; no socket | `CHR:1.00<name>=<head gif>,<male\|female>,<five colour names>`, one line; GChar keeps `GChar.ini` (`drawmethod`, `headmode`, `graaldir`) | [bin][doc][file] (tools/classic-tools/character-designer.md#graal-character-designer-and-gchar) |
| `gserverstat`, `gserverstat2`, `statmaker` (1999 gserver tree) | HTML leaderboards on standard output, 14 modes (kills default), top 50, load-only accounts and the account named `super` skipped; `statmaker` loops with 10 s and 600 s sleeps; no socket | reads `weapons.txt`, `accountslist.txt`, `accounts/accN.txt` (→ §5.1) | [bin][src][file] (tools/classic-tools/gserverstat.md#gserverstat-and-gserverstat2) |
| Classic listserver `serverlist3` | list server ELF with MySQL; protocol → §6 | config keys `clientsport`, `serversport`, `playerlimit`, `databaseserver`, `showmore`; status files beside the process | [bin] (tools/classic-tools/serverlist3.md#start-and-config) |
| Win32 `ListServer.exe` | Delphi directory helper reading an ini server list (→ §7) | ini, registry | [bin] (recovered-drive-tools/ghidra-analysis/ListServer/SUMMARY.md) |
| Script Editor 2.53 | GS1 NPC and weapon script editor with templates and a find-NPC helper | GS1 scripts | [bin] (recovered-drive-tools/ghidra-analysis/scripteditor/SUMMARY.md) |
| BytecodeViewer | console dump of a GS2 bytecode capture: skips the first byte, then the information section, function names, strings and bytecode, with opcode names from `BytecodeViewer_defs.txt` (GS2 bytecode → §8) | GS2 bytecode | [src] (recovered-drive-tools/ghidra-analysis/BytecodeViewer/SUMMARY.md) |
| Assimilator ("GIF2PNG") | offline batch checker and converter for scripts, levels, text and animations | asset files | [bin] (recovered-drive-tools/ghidra-analysis/Assimilator/SUMMARY.md) |
| PNGView | offline image viewer | PNG | [bin] (recovered-drive-tools/ghidra-analysis/PNGView/SUMMARY.md) |
| TilesEditor (39ster, Reborn line) | offline 64-bit Qt editor for levels, tiles, links, chests and NPCs (anonymous and external classes), layers, grid snap, map export | levels | [bin] (recovered-drive-tools/ghidra-analysis/TilesEditor/SUMMARY.md) |
| Recovered third-party trainers (AutoIt and VB6 macro tools such as AutoD, WaterGet and the AFK bots) | AFK chat bots, input macros and chat or costume spam that act on the stock client's window from outside; read statically, none run; groups and tool-by-tool behaviour → §4.10.1.4 | — | [bin] (recovered-hacks/TRAINER_RE_NOTES.md); [bin] (recovered-hacks/behaviour-models.md); [bin] (recovered-hacks/static-2026-11-01/README.md); [doc] (recovered-hacks/THREAT_TAXONOMY.md) |
| DClient setup | a VB6-era installer bootstrap; its cabinet is truncated, so the client cannot be rebuilt | — | [bin] (recovered-drive-tools/ghidra-analysis/DClient_setup/SUMMARY.md) |

Recovered server binaries, described in Part V [bin] (recovered-drive-tools/ghidra-analysis/gserver13/SUMMARY.md):

| Binary | Notes | Source |
| --- | --- | --- |
| `gserver13` (Linux, Dec 1999) | unstripped; account parse, level enter and update, guild verify, IP bans (→ §5.1) | [bin] (recovered-drive-tools/ghidra-analysis/gserver13/SUMMARY.md) |
| `gserver` (Linux) and `gserver.exe` (Win32), about June 2002 | the same classic server with source beside it: NW level load, RC player props, MySQL accounts | [bin] (recovered-drive-tools/ghidra-analysis/gserver-linux/SUMMARY.md); [bin] (recovered-drive-tools/ghidra-analysis/gserver-win/SUMMARY.md); [bin] (recovered-drive-tools/ghidra-analysis/gserver_pe_GServersource/SUMMARY.md) |
| Matriark `gserver` (pack labelled 1.39) | stripped static build with database accounts, guilds, RC and NC sessions and leaderboard queries; the pack's bug note says head, shield and sword path checks disagree with the paths used when sending level files | [bin][doc] (recovered-drive-tools/ghidra-analysis/Matriark_gserver/SUMMARY.md) |
