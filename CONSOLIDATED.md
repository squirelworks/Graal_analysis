# Graal Analysis — consolidated notes

Date: 2026-10-14

Cleaned notes derived from public server sources, observed packet shapes, and format documentation. No decompile material.

## Formats

### Levels
- **GLEVNW01** (`.nw`) — text format. Header, `BOARD x y width layer tiledata` (2-char base64 tiles), `NPC` blocks, `LINK`/`SIGN`/`CHEST`/`BADDY` records.
- **GR-V1** (`.graal`) — binary format. 8-byte magic, 64×64 board of 2-byte tiles, embedded `image.gif#script` NPC records.
- **Z3-V1** (`.zelda`) — earlier binary. RLE board, `FileLink` records terminated by `#`.

### Tiles
- Tile id is a 12-bit value decoded from the 2-char base64 encoding into `pics1`.
- Collision table is 4096 bytes. Wall is `>= 20` (blocks). Water is `== 11` (does not block, changes display).
- `arrays.dat` first array is the passable-tile list (`nowall`). Tiles in that list get type 0; everything else gets type 22.
- Stamp id 0 is a 4×4 ground fill. Stamp id 1 is a hole and is not written. The 2×2 Bush stamp writes ids 2, 3, 18, 19.

### GANI
- `SPRITE`/`ANI`/`ANIEND`/`PLAYSOUND`/`DEFAULTATTR` blocks.
- `ANI` carries placements. A stepper advances the frame index.

### Maps
- **GRMAP001** (`.gmap`) — world map linking levels.

## Protocol

### Framing
- Length-prefixed (u16be) + zlib. Some post-login frames are encrypted (Borland LCG).

### Login
- Classic line: random prefix `(rand & 0x7F) + 0x20` + `GNW#####` version token + length-biased account/password.
- Observed tokens: `GNW28015`, `GNW22122`, `GNW03014`, `GNW07080`, `GNW30123`.
- `GNW07080` = 1.39. `GNW03081` = 2.05.

### Movement
- Short char-encoded frames headed `0x02` (wire `"`). Not f32.
- Position codecs: classic ×2, precise ×16.
- Directions: 0 south, 1 west, 2 east, 3 north.

### Board
- `BoardModify` carries x, y, width, layer, and tile data.
- Packet ids remain provisional.

## NPC scripting

3,172 unique scripts scraped from 1,420 GR-V1 levels. Stored in `npc-library/npcs.json`. The scrape reported 3,187; 15 records were lost to truncated source pages (see `partial_pages` in `npcs.json` meta).

### Common events (by frequency)
| Event | Scripts |
|-------|--------:|
| `playerenters` | 2,268 |
| `playertouchsme` | 1,986 |
| `timeout` | 1,456 |
| `playerendsreading` | 1,123 |
| `compusdied` | 1,122 |
| `playertouchsother` | 1,074 |
| `wasshot` | 728 |
| `playersays` | 43 |

### Script shape
Scripts follow `image.gif#if (event) { body }`. Common commands: `hide`, `show`, `set`, `unset`, `say`, `setlevel`, `warp`, `hurt`.

### GS1 bytecode
Opcodes match OpenGS1: Push, Assign, ArrSet/Get, Add/Sub/Mul/Div/Mod/Pow, Inc/Dec, Call/CmdCall, Jmp/Jal/Ret, Eq/Lt/Gt/Lte/Gte, Not/And/Or, Jez/Jnz, Stop, DbgOut. Arithmetic, comparison, and jump execute. Call and array ops are no-ops until the command set is wired.

## Offline play

A local session can:
1. Load a GLEVNW01 `.nw`.
2. Decode tile ids and apply board modifies.
3. Reject moves onto wall tiles. Track water without blocking.
4. Parse LINK/SIGN/BADDY/CHEST. Decode binary sign text.
5. Step an optional walk GANI on every successful move.
6. Draw an ASCII or PPM view of the board and player.

## Version map

| Token | Build |
|-------|-------|
| `GNW07080` | 1.39 |
| `GNW03081` | 2.05 |
| `GNW22122` | (from capture) |
| `GNW28015` | (from capture) |
| `GNW30123` | (from capture, listserver) |

Filename builds: `Graal_2171` = 2.171, `Graal_222` = 2.22, `Graal_231` = 2.31. PE FileVersion is authoritative for editors.

## Precursor

Zelda Online (1997–98, Stefan Knorr) is the Java precursor. AWT applet client/server on port 14801, text-line lobby protocol, `.zelda` levels. Source is archived separately. Levels were analyzed and discarded.
