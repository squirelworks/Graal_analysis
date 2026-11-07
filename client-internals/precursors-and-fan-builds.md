# Precursors and fan builds

Date: 2026-10-29

This note covers a set of uploads that sit around the Delphi client line:

- the Zelda Online Java versions (1998)
- Stefan Knorr's Zelda level editor (1998)
- Java Graal (2000)
- the Graal Game Boy Color demo (1999)
- 39ster's Graal client 1.00 (2014)
- GraalX (2001)

The sources were read where they exist and the class files and binaries were read statically where they don't. Nothing was run.
No code is reproduced here. Two of the "source" archives turned out to be decompiler output and are treated that way (see below).

## What the uploads are

There are 14 uploads but only 9 distinct items. They were compared by content hash.

| Upload(s) | Same as | What it is |
|---|---|---|
| `zeldaonline.zip`, `zeldaonline1.rar` | each other, except that the rar adds 36 levels | Zelda Online 1: a single-player Java applet |
| `zeldaonline1_src.zip` | – | Decompiler output for the Zelda Online 1 classes, made in 2003, not the author's source |
| `zeldaonline2.zip`, `zeldaonline2.rar` | each other, byte for byte. The zip is also the copy in `zeldaonline2.7z` in the project files | Zelda Online 2 "local version": game, server and the author's commented source |
| `zeldaonlineeditor.zip`, `zeldaonlineeditor.rar` | each other. The exe is also in the next item | The Zelda level editor (`ZeldaEditor.exe`) |
| `ZeldaOnline_aka_very_first_graal.zip` | – | The editor, the untouched `zeldaonline2.zip`, and an unpacked Zelda Online 2 that a player edited in February 2002 |
| `javagraal_rip.rar` | – | Java Graal as served by Cyberjoueur: `Graal.jar`, loose classes, art and 261 level and asset files. The archive is damaged: 26 files (10 `.graal`, 15 `.zelda`, 1 more) fail extraction |
| `javagraal_src.zip` | – | Decompiler output for the five classes in `Graal.jar` (2003). Its class and method set matches the jar exactly |
| `graalgb.rar`, `Graal v1.10 - Adventure Demo (PD) [C].zip` | each other: the same 256 KB ROM | The Graal Game Boy Color demo |
| `GraalX.rar` | – | A 2.01-era Delphi client. Already in `build-catalogue.md` |
| `39ster Graal v1.00.7z` | – | A 2014 fan remake. It is not the 39ster 2.1 GServer covered in `ash/` |

## How they relate

```
1998-05  Zelda Online 1      Java 1.0 applet, single player, Z3-V1.02/1.03 levels
1998-07  Zelda Online 2      Java 1.1 app, adds multiplayer through GServ on 14801
1998-07  ZeldaEditor         Delphi 3, writes Z3-V1.03; its dialogs become 1st Graal's editor
1998-09  1st Graal           Delphi; reuses the editor forms and the relay lobby
1999-09  Graal GB demo       Game Boy Color homebrew by Knorr ("Graal v1.10 Adventure Demo")
2000-07  Java Graal          Zelda Online 2's client with Graal art, reading GR-V levels, relay on 14802
2001-03  GraalX              2.01 pre-release that keeps the .nw loader
2014-04  39ster client 1.00  offline fan remake on an SDL/GameMonkey engine
```

### Zelda Online 1 (May 1998)

- A Java 1.0 applet (`Zelda` class, class file version 45). The page runs it at scale 2 in a 512×448 box. The class files are dated 16 May 1998.
- **Single player only.** There is no socket code, and levels, `arrays.dat`, images and sound are all fetched relative to the applet's codebase.
- The start level is `level1.zelda`. The rar ships 36 levels, all `Z3-V1.03`. The loader also accepts `Z3-V1.02`.
- The story is hard-coded per level name: people placed on `level13`, `level28`, `level22` and `cave2`, and chests on `level21`, `level24`, `village3`, `level16` and `level29`, all gated by progress flags.
- The class already holds the text alphabet that later Graal uses for sign text (the 97-entry string documented in `formats/sign-text.md`), together with the glyph-code list `A B X Y u d l r h x y z 1 2 3 4 .`. So the Graal sign alphabet goes back to the first Java applet.

### Zelda Online 2 "local version" (July 1998)

- A Java 1.1 *application*, not an applet. It opens a start window with "One-Player mode" and "Multiplayer mode" and a server address field that defaults to the loopback address. It refuses to run on Java 1.0.
- Files are read from the working directory, not over HTTP.
- The package has `game/`, `server/` and `programming/` folders, and the author's real source is included, with comments. The files are dated 18–26 July 1998.
- It ships 51 `Z3-V1.03` levels. `level1.zelda` is again the start level.
- There is an extra `ZeldaMain (1).class` at the top level. It differs from `game/ZeldaMain.class` in one constant only: the tile index of the "free stone" (the tile left behind when a stone is lifted) is 1023 instead of 584.
- The options window has a nickname field, an option to show your own name, sprite colours for cap, cap edge, belt and coat, and a **password**. The password is a 10-character save code (see below).
- The readme warns that the local version uses different tile indexes from the online server, so bushes and stones look wrong when the two are mixed.

#### Password saves

The save code is 10 characters from a 64-character alphabet, so it holds 60 bits. Packed into it are:

| Field | Bits |
|---|---|
| player x (0–63) | 6 |
| player y (0–63) | 6 |
| level index (from a fixed level list) | 9 |
| rupees | 10 |
| darts | 6 |
| power, in half hearts | 5 |
| glove level 2, can shoot, has map, found brother | 1 each |
| the four story chests opened | 1 each |
| checksum: the number of set bits in the payload | 6 (lowest) |

The 60 bits are then XORed with a fixed mask and their positions transposed (bit *i* moves to `(i mod 10)·6 + i div 10`) before being written out six bits per character.
Reading a code reverses those steps, checks the bit count, and fails on a wrong length or an unknown character.

#### Zelda Online 2 in the "very first graal" zip

The `ZeldaOnline2` folder in `ZeldaOnline_aka_very_first_graal.zip` is the stock release plus a player's edits from 13–15 February 2002:

- 4 new levels (`agrethouse1`, `agretweapons1`, `eggsecretroom1`, `gameover`)
- 4 changed levels (`level1`, `level11`, `level29`, `house15`)
- an `objects.dat` with 4 more stamps (109 instead of 105): "Chest - Red Rupee", "Blackness", "Big Blackness" and "Breakaway Wall Part"
- a `GServProto.txt` log line from one server start

None of this is from 1998.

### ZeldaEditor (July 1998)

- Built with Delphi 3 (Borland RTL, "Copyright (c) 1983,97"). Linked around 25 July 1998.
- Main window `TZeldaFrame`, titled "Zelda Editor". It has a toolbar with New, Open, Save, Save As, Undo, Cut, Copy, Paste, Delete, "Turn Selection Into A Warp Field", Edit Links, Edit Baddies and Edit Signs. A stamp ("object") palette sits on the right with add, save and delete buttons.
- Dialogs: `TLinkList`, `TLinkOptions`, `TNewOpponent`, `TEditSigns`, `TObjectName` and `TShowCodes` (the sign glyph codes).
- It saves only `Z3-V1.03`. Window positions are kept in `ZeldaEditor.ini`, one `Name:left,top,width,height` line per window.

**1st Graal grew out of this editor.** The 1st Graal client (Sept 1998) carries `TEditSigns`, `TLinkList`, `TLinkOptions`, `TObjectName` and `TShowCodes` under the same names. `TEditSigns` differs only by a few pixels plus `KeyPreview` and a key handler. `TNewOpponent` became `TEditBaddy`, and the main form became `TAdventure`.
So the Delphi Graal client started as the level editor with a game added, not the other way round. This fits Graal shipping with an editor built in.

#### `objects.dat` (stamps)

The editor's stamp list is a flat sequence of records:

- the name, ended by `\n`
- one byte for the width and one byte for the height
- width × height 32-bit little-endian tile ids, row by row

Tile id 2047 (`0x7FF`) is a transparent cell.
The 1998 file has 105 stamps, from "Bush", "Sign", "Stone" and "PushStone" up to whole houses, bridges and a cathedral. The same format is still used by the `objects.dat` shipped with Graal 1.21.

### Shared Java game data

**`arrays.dat`** is built by the `makeArrays` and `addSprites` tools in `programming/`. It is a list of typed integer arrays. Each array starts with a 32-bit big-endian header: the high 16 bits give the kind (0 for a flat int array, 1 for an array of arrays) and the low 16 bits the count. The values that follow are big-endian 32-bit ints.

The game reads these arrays in this fixed order:

1. non-wall tiles
2. swamp tiles
3. jump stones
4. bush objects and their replacements
5. liftable objects and their replacements
6. chest tiles and their replacements
7. movable stone
8. sprite crop table
9. hurt sprites
10. leap animation
11. baddy sprites
12. bumped sprites
13. explosion frames
14. swamp-soldier frames

Java Graal and 39ster's client also ship an `arrays.dat`. 39ster's is a plain-text tile-type table instead.

### Level format as the Java code reads it

This confirms and extends `formats/level-binary.md`:

| Magic | Code width | Read by |
|---|---|---|
| `Z3-V1.02` | **11 bits** | Zelda Online 1 and 2 only |
| `Z3-V1.03` | 12 | Zelda Online 1 and 2, ZeldaEditor (writes it), Java Graal |
| `Z3-V1.04` | 12 | Java Graal |
| `GR-V1.00`, `GR-V1.01` | 12 | Java Graal, 39ster |
| `GR-V1.02`, `GR-V1.03` | 13 | Java Graal, 39ster |

- The run-length rules are the ones already in `level-binary.md` (control flag in the top bit, count in the low byte, `0x100` for a double run). A decoder that follows them reads all 271 levels in these uploads with no errors.
- In `Z3-V1.02` and `Z3-V1.03` the Java games read each baddy as a fixed 4-byte record: x, y, type, then a byte that is always `\n`. That is the same thing as "3 bytes plus an empty verse line". The list ends at a record whose first byte is `0xFF`.
- Link lines are `file x y w h newx newy`. A negative `newx` or `newy` means that coordinate is kept when warping.
- Sign lines are x+32, y+32, then text in the sign alphabet.
- Java Graal reads GR-V NPC lines but only shows the image: the script after `#` is dropped, and a missing `.gif` suffix is added. It skips the GR-V1.01+ chest section.

## Network: GServ Standalone and the Java clients

Zelda Online 2's `server/` holds "GServ Standalone (C) Stefan Knorr 1997, based on JccVsd (C) Stephan Kulow". It is a game-neutral lobby that Knorr also used for chess (a `ChessSync` thread sends every "Chess" player a one-character timer line every second).
It listens on **14801**, gives out ids `0000` plus a 4-digit counter that wraps at 9999, and logs to `GServProto.txt`. This is the lobby that `protocol/relay-1998.md` describes from the Delphi side. The source adds:

| Line | Direction | Meaning |
|---|---|---|
| `N<game>#<name>` | C→S | Join as a player (state "waits") and get `I<id>` |
| `O<game>#<name>` | C→S | Join as an observer. You see players in that game who are already in a party |
| `S<name>` | C→S | Super user: sees every player in every game, listed as `name (game)` |
| `+` | C→S | Available again (after `-`) |
| `-` | C→S | Not available. Your id is withdrawn from the other players' lists |
| `P<id8>` | C→S | Join that player's party. You are linked to them and to everyone already in their party |
| `C` | C→S | Leave the party |
| `V<id8>` | C→S | Watch a player: you receive their party's `D` traffic |
| `D<data>` | C→S | Relay to everyone in your party |
| `H<score>` | C→S | High score. The client sends it and this server ignores it |
| `I<id8>` | S→C | Your id |
| `+<id8><name>` | S→C | A player in your game is available. The name follows the id directly |
| `-<id8>` | S→C | That player left or became unavailable |
| `P<id8>` | S→C | That player is now in your party |
| `C<id8>` | S→C | That player left your party |
| `D<data>` | S→C | Relayed data, unchanged. The server does not add the sender |

### Zelda Online 2 client

- Connects to the typed address on 14801.
- Room name: `Z` + level file name without extension + `1.6`, for example `Zlevel11.6`. Every level is its own room. On a level change the client sends `C` and `-`, then joins the new room with the name `def`. The real nickname is sent in `D` later.
- When the first `+` arrives it sends `P` for that player straight away. On `P` it pushes its state: login time, position, chat, nickname, colours and carried object.
- `D` payload types: `P C N S M H B T D E O W A`. Their layouts are the ones in `relay-1998.md`, and the 1st Graal kept them. The level-leader rule (earliest login time, ties broken by the lower id) also comes from here.
- The client clamps baddy knock-back to ±4 before encoding. One of the four clamps writes the wrong axis, so a large positive vertical knock-back overwrites the horizontal value.

### Java Graal client

- Connects to **its own codebase host on 14802**, the Cyberjoueur relay port that the Delphi betas also used.
- Room name: `G2` + level file name. A second "fixed room `Graal2`" mode exists in the class but the applet never selects it.
- `D` types: the Zelda Online 2 set without `S` (colours) and with `L` (level name) added.
- Without `S`, Java players appear with default colours. Delphi clients of the same period send types the applet ignores (`F`, `G`, `I`, `Q`, `R`, `U`, `X` to `Z`, `0` to `8`). So mixed sessions would only share movement, chat, board changes, baddies, items and arrows. This is *inferred*, not observed.
- **The `G2` prefix and the `Graal2` fallback are exactly what 4th Graal alpha (October 1998) uses.** The room prefixes and fallback names were read from the string tables of all 18 betas. 1st and 2nd use `Zelda2`, 3rd and 4th use `Graal` with a bare `G` prefix, and 4th alpha alone uses `G2` / `Graal2`. From 5th Graal on (`G3` / `Graal3` up to `G8` / `Graal8`) the rooms no longer match.
- So Java Graal speaks the relay dialect of 4th Graal alpha. Its `D` types are all ones that 4th alpha also sends or handles, and 4th alpha's extra types (`I`, `U`, `X`, `Y`, `Z`, `Q`, `F`, `G`, `R`) are ones the applet ignores. A Java player and a 4th alpha player on the same level file were in the same room. Later betas were not. This is read from the binaries and the Java source, not from a capture. The only open point is whether 4th alpha appends the bare file name for a local level, as the applet does. **Run live on 2026-10-31:** it does (`G2level13.graal`), and a Java Graal and a 4th alpha player met and chatted on Knorr's GServ. Java Graal and 5th Graal met through a room-renaming proxy (`relay-room-bridge.md`).
- The applet was built in July 2000, 20 months after 4th alpha, so its dialect was already long out of date. It only made sense on a relay that still had 4th alpha clients, or Java players alone.

## Java Graal (July 2000)

- `Graal.jar` holds 5 classes (`Graal`, `GraalClient`, `Computer`, `FileLink`, `ServerPlayer`), all dated 2 July 2000 and signed (SHA and MD5 digests in the manifest). The rip's loose copies are identical to the jar's.
- It is a Java 1.1 applet (512×418) embedded in a Cyberjoueur page next to their Bomberman, chess, Reversi and Tetris applets, with the Flycast ad block from 1999. The rip itself was taken on 23 February 2002.
- In code terms it is Zelda Online 2's game and client with Graal art (`pics1.gif`, `sprites.gif`, `letters.gif`) and Graal levels. It starts on `level13.graal` and has a `nickname:` chat command.
- `levels/` holds 180 readable levels (plus 25 damaged ones), NPC images and a few WAV files. Many `.zelda` files actually carry `GR-V` headers. The level names (`ebon*`, `mod*`, `sominside*`, `dungeona*`) look like player-made Cyberjoueur web levels.

## Graal Game Boy Color demo (1999)

The full disassembly is written up in `gameboy-demo.md`. In short:

- The ROM header has the title `GRAAL`. It is dual-mode (it runs on both Game Boy and Game Boy Color) on an MBC1 cartridge with 256 KB of ROM. Only banks 0 to 5 are used. The header checksum is valid and the file is dated 29 September 1999.
- It is a C program built with GBDK 2.x and LCC. The whole game runs in the VBlank interrupt.
- "Welcome to Graal / Demo version by Stefan Knorr" is a sign in the first room; there is no title screen. So this is Knorr's own port, not a fan project. The "(PD)" in the dump name marks it as public-domain homebrew.
- There are seven rooms of 32×32 tiles. Their links use the PC client's link record, with a room number in place of the file name.
- Gameplay text includes a captive you free, who shows you how to lift and throw stones and then tells you to press Select and switch to "Fung Si Yun".
- Names in the ROM such as Lizardon, Pachukite, Pach Soldier, Gold Soldier, Water Athena and Red Squall belong to a table of 31 character types, not only to baddies. The Select menu lets the player switch to any of them.
- The text font is ordered space, A–Z, a–z, 0–9, then punctuation, starting at byte `0x20`. This is not the PC sign alphabet.

## 39ster's Graal client 1.00 (2014)

- All files are dated 23 April 2014. `GameMaker.exe` is a small C++ engine on SDL 1.2 (plus zlib and stb_image), unrelated to YoYo's GameMaker. It embeds the GameMonkey scripting language, and all of the Graal logic is in `main.gm`, about 1,500 lines of script.
- It reads `GLEVNW01` `.nw` levels and `GR-V1.00`–`1.03` levels with the same 12- and 13-bit rule, plus `.gani` animations. It converts tile ids into the 2.x `pics1.png` layout and starts on `level13.nw`.
- **Offline only.** It has no socket code, and NPC scripts are not run: the NPC object has an execute hook with the call commented out, so NPCs only show their images.
- It bundles 1,733 `.nw` levels and 1,321 GIFs collected from community worlds.

## GraalX

GraalX is already in `build-catalogue.md`: a pre-release of 2.01, linked 17 hours before it, with 2.01's token, list port and DES-hidden list host, which keeps the `GLEVNW01` reader and writer.
A form-by-form comparison adds one more check. GraalX has the same 28 forms as 2.0 rev3 and 2.01, and differs from 2.01 only in two control positions on the main form.

## Open

- ~~Whether a Delphi beta ever used the `G2` room prefix.~~ Answered above: 4th Graal alpha did, and no other beta.
- ~~The GB demo's full script and map format.~~ Answered in `gameboy-demo.md`.
- Who made the February 2002 Zelda Online 2 edits.
