# Zelda Online (1997–98) — precursor analysis

Date: 2026-10-14
Author: Stefan Knorr (knorr@informatik.uni-rostock.de)
Copyright: GServ Standalone (C) Stefan Knorr 1997; Zelda Client for GServer (C) Stefan Knorr 1998

## What this is

The Java Zelda Online local version that predates the Delphi Graal client. The server is a text-line lobby; the client is a full Zelda-style game that loads `.zelda` levels and optionally joins multiplayer on port 14801.

## Layout (promoted to shanalysis/zelda-online-1998)

| Path | Contents |
|------|----------|
| `server/` | `GServer.java`, `Player.java` — lobby server |
| `game/` | `Zelda.java`, `ZeldaMain.java`, `ZeldaClient.java`, `MapPanel.java`, `Computer.java`, `FileLink.java` |
| `programming/` | `makeArrays.java`, `addSprites.java` — generate `arrays.dat` |
| `readme.txt`, `readme-2.txt` | original notes |

Levels (51 `.zelda`) and binaries (class, gif, arrays.dat, audio, bat) moved to `/recycler/trash/`.

## Server protocol (text lines, port 14801)

| Prefix | Meaning |
|--------|---------|
| `N` / `O` / `S` | game#name (normal / observer / super) |
| `I` + 8-char id | server assigns id |
| `+` / `-` | enter / leave available list |
| `P` + id | play against |
| `C` + id | disconnect from party |
| `D` + data | game data relay |
| `V` + id | observe |

Player ids are 8-char (`0000` + 4-digit). Game data is relayed between opponents; no binary framing.

## Level format (`.zelda`)

Header: `Z3-V1.02` or `Z3-V1.03` (8 bytes).

Board: 64×64 tiles, RLE. Code bits = 11 (v1.02) or 12 (v1.03). High bit set means count; otherwise tile id. Double-repeat flag for alternating pairs.

After board:
- text lines of `FileLink` records (`filename x y w h newx newy`) until `#`
- binary computer records (4 bytes each: x, y, type, stop)
- text sign records (`signx-32`, `signy-32`, coded text)

## Tile / sprite tables

`makeArrays.java` writes `arrays.dat` with:
- `nowall` (passable tile ids)
- `swamp`, `jumpstone`, `bushobj` / replace, `liftobj` / replace, `chestfields` / replace, `movestone`
- sprite placement tables (`spritevalues`, `hurtsprites`, `compusprites`, etc.)

`addSprites.java` appends the sprite crop table (x, y, w, h packed into ints).

## Client connection

`ZeldaClient` connects to host:14801. On enter it sends `N` + level-prefix + `#def`. Subsequent `D` packets carry position, chat, nickname, sprite colors, computer moves, board modifies, extras, carries, shots. Leader election is by earliest login time.

## Relation to later Graal

| Zelda Online | Later Graal |
|--------------|-------------|
| port 14801 | listserver / world ports evolve |
| text-line lobby | binary framed protocol with version token |
| `.zelda` RLE board | `.nw` GLEVNW01 text board |
| `arrays.dat` tile tables | `tiledefs.txt` / pics1.png |
| Java applet | Delphi client |

This is the last point before the version-token and binary-packet era.
