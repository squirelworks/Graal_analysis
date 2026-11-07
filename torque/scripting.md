# TorqueScript in Graal 3.x: the `.dso` format and the shipped scripts

Date: 2026-10-30. Tags as in `README.md`.

Graal 3.x keeps its menus, options, key binds, message boxes and the 3D mission-loading flow in TorqueScript. **[file]**

- 3.04 Linux ships 39 compiled scripts in the TGE starter layout (`common/client`, `common/ui`, `graaldata/client`, `graaldata/languages`, `graaldata/main.cs.dso`). It has a private-message window and a player list in script, and no 3D scripts.
- 3.153 Mac ships 44 compiled scripts (`scripts/`, `scripts2D/`, `scriptsgui/`) and 13 plain `.cs` files (prefs, key configs, nine language tables). It adds the 3D client scripts.
- From 4.x on, the menus are native or GS2 and no `.dso` files ship.

All 83 files decode with the table below.

## File format (version 33)

All integers little-endian. **[file]**

| Field | Notes |
|---|---|
| U32 version | 33 |
| U32 size, bytes | global string table (NUL-separated) |
| U32 count, count × F64 | global float table |
| U32 size, bytes | function string table |
| U32 count, count × F64 | function float table |
| U32 codeLength, U32 lineBreakPairCount | |
| code | `codeLength` words; each is one byte, or `0xFF` followed by a U32 |
| lineBreakPairCount × 2 × U32 | line/ip pairs |
| U32 identCount, then per ident: U32 string offset, U32 count, count × U32 ip | patches identifier words in the code with global-string entries |

Code inside a function body uses the function tables; code outside uses the global tables.

**Mac quirk:** the PPC build writes the F64 tables **big-endian** while everything else stays little-endian (1.0 is stored `3F F0 00 …`). The decoder detects this per file. The 3.04 Linux files are little-endian throughout.

**Unused parameters:** a function argument that the body never uses gets an ident offset just past the end of the global string table, so its name is lost. The decoder prints `%unusedN`.

## Graal's opcode table

The numbering differs from stock TGE 1.x: two unused opcodes follow `CREATE_OBJECT`, and one follows `CALLFUNC`. Worked out from the scripts (every file decodes cleanly with this table and no others) **[file]**:

| # | Opcode | # | Opcode | # | Opcode |
|---|---|---|---|---|---|
| 0 | FUNC_DECL | 28 | SHL | 56 | STR_TO_UINT |
| 1 | CREATE_OBJECT | 29 | AND | 57 | STR_TO_FLT |
| 2 | (unused) | 30 | OR | 58 | STR_TO_NONE |
| 3 | (unused) | 31 | ADD | 59 | FLT_TO_UINT |
| 4 | ADD_OBJECT | 32 | SUB | 60 | FLT_TO_STR |
| 5 | END_OBJECT | 33 | MUL | 61 | FLT_TO_NONE |
| 6 | JMPIFFNOT | 34 | DIV | 62 | UINT_TO_FLT |
| 7 | JMPIFNOT | 35 | NEG | 63 | UINT_TO_STR |
| 8 | JMPIFF | 36 | SETCURVAR | 64 | UINT_TO_NONE |
| 9 | JMPIF | 37 | SETCURVAR_CREATE | 65 | LOADIMMED_UINT |
| 10 | JMPIFNOT_NP | 38 | SETCURVAR_ARRAY | 66 | LOADIMMED_FLT |
| 11 | JMPIF_NP | 39 | SETCURVAR_ARRAY_CREATE | 67 | TAG_TO_STR |
| 12 | JMP | 40 | LOADVAR_UINT | 68 | LOADIMMED_STR |
| 13 | RETURN | 41 | LOADVAR_FLT | 69 | LOADIMMED_IDENT |
| 14 | CMPEQ | 42 | LOADVAR_STR | 70 | CALLFUNC_RESOLVE |
| 15 | CMPGR | 43 | SAVEVAR_UINT | 71 | CALLFUNC |
| 16 | CMPGE | 44 | SAVEVAR_FLT | 72 | (unused) |
| 17 | CMPLT | 45 | SAVEVAR_STR | 73 | ADVANCE_STR |
| 18 | CMPLE | 46 | SETCUROBJECT | 74 | ADVANCE_STR_APPENDCHAR |
| 19 | CMPNE | 47 | SETCUROBJECT_NEW | 75 | ADVANCE_STR_COMMA |
| 20 | XOR | 48 | SETCURFIELD | 76 | ADVANCE_STR_NUL |
| 21 | MOD | 49 | SETCURFIELD_ARRAY | 77 | REWIND_STR |
| 22 | BITAND | 50 | LOADFIELD_UINT | 78 | TERMINATE_REWIND_STR |
| 23 | BITOR | 51 | LOADFIELD_FLT | 79 | COMPARE_STR |
| 24 | NOT | 52 | LOADFIELD_STR | 80 | PUSH |
| 25 | NOTF | 53 | SAVEFIELD_UINT | 81 | PUSH_FRAME |
| 26 | ONESCOMPLEMENT | 54 | SAVEFIELD_FLT | 82 | BREAK |
| 27 | SHR | 55 | SAVEFIELD_STR | | |

Operands: `FUNC_DECL` name, namespace, package, hasBody, end ip, argc, argc arg idents; `CREATE_OBJECT` parent ident, isDatablock, fail ip; `ADD_OBJECT` and `END_OBJECT` one flag; jumps one target; `SETCURVAR`, `SETCURVAR_CREATE`, `SETCURFIELD`, `LOADIMMED_*`, `TAG_TO_STR`, `ADVANCE_STR_APPENDCHAR` one; `CALLFUNC(_RESOLVE)` name, namespace, call type (0 function, 1 method, 2 parent). Everything else has none. This is the same operand shape as stock TGE 1.x. Opcodes 2, 3 and 72 never occur in the shipped files, so what they were is unknown.

## The decoder

`tools/dsodis.py file.dso` prints a disassembly. `tools/dsodec.py file.dso` prints TorqueScript-like source: calls, assignments, `new` blocks with their fields, `@`/`SPC`/`TAB`/`NL` concatenation, array variables, and `&&`/`||` chains. Other control flow stays as `if (!cond) goto Lnn;` with labels, and `?:` expressions are not rebuilt (they show as an empty `goto`). Run Python with `-I` on untrusted files.

## What the 3.153 scripts do

The decompiled sources are in the project folder (`graal-decompile/torque/dec3153/`, and `dec304/` for 3.04). 3.04's key map is the same as 3.153's 2D map, under the name `moveMap`, with F3 bound in the map instead of globally. Highlights **[file]**:

- **Start-up.** `main.cs` sets log mode 6, opens the console, runs `main2D.cs` and writes default prefs (`$pref::Graal::fixedudpport = 14899`, `$pref::Graal::defaultfontsize = 22`, OpenAL audio). `main2D.cs` (package `graal`) loads the GUI files and key binds and shows `MainMenuGui2D`. The 2D game itself is a native GUI control named `Adventure` (`GuiGraalCtrl`), shown by `start2D()`.
- **Menus call into native code** through `Adventure.*`: `setNickName`, `setAccountName`, `setPassWord`, `setLanguage`, `openServerList`, `startOfflineMode`, `selectServer`, `serverDirectConnect` (the "direct connect" box on the server list), `connectToSelectedServer`, `retrieveAccountFields`. If `$serverstartconnect` is set and account and password are filled in, the main menu goes straight to the server list (this is how `-connect` / `graal://name` auto-join works).
- **2D keys** (`default.bind2D.cs`, map `moveMap2D`): arrows move, A/S/D actions (Space = `doS2`), Q, P, M, T = microphone, F5 load level, F7 player list, F8 server list. Global: F1 help, F2 console, F3 options, Alt+Enter full screen, Esc `escapeFromGame2D()`.
- **3D keys** (`default.bind3D.cs`, map `moveMap`): WASD and arrows move (each also calls the 2D move function, so the Graal player is driven too), mouse look with `getMouseAdjustAmount` (sensitivity clamped to 0.05–2.0, scaled by FOV/90), Space jump (`$mvTriggerCount2`), left mouse fire, right mouse first person, E free look.
- **3D start** (`main3D.cs`, package `graal3D`): runs prefs and canvas scripts, maps nine terrain textures to detail textures and footstep sounds (`addMaterialMapping("grass.jpg", "detail: terraindetail_grass", "sound: 1", …)`; sand, grass, patchy, cobbles, two desert, three snow), loads `PlayGui`, `LoadingGui`, the mission-download and connection scripts, sets net port 0, then `new GameConnection(ServerConnection)` and `connect()`.
- **Connection errors** (`serverConnection.cs`): maps every Torque reject code to a message box, including the Graal ones for `CHR_PROTOCOL_LESS` / `_GREATER`.
- **Chat over Torque** (`message.cs`): stock `clientCmdChatMessage` / `clientCmdServerMessage` with `addMessageCallback`, ending in native `onChatMessage` / `onServerMessage`.
- **Loading screen** (`missionDownload2.cs`): a snowball rolls across the screen and grows (`g3d_splashsnow1-3.png`), the player picture changes with progress (`g3d_playersnow1-5.png`), and the hair image marks the phase (`g3d_hairsnow1/3/4.png`). These are the Christmas 2004 3D assets in `scripts2D/`.
