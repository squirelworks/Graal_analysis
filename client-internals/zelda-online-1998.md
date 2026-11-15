# Zelda Online (1997–98) — precursor analysis

Date: 2026-10-14
Author: Stefan Knorr (knorr@informatik.uni-rostock.de)
Copyright: GServ Standalone (C) Stefan Knorr 1997; Zelda Client for GServer (C) Stefan Knorr 1998

## What this is

The Java Zelda Online 2 local version that predates the Delphi Graal client. The server is a text-line lobby; the client is a full Zelda-style game that loads `.zelda` levels and optionally joins multiplayer on port 14801. Zelda Online 1 is a separate single-player applet with no socket code. [src][bin]

For build-by-build transport, rooms, native-run interventions and consumer
limits, use the [canonical earliest-network capability map](../protocol/relay-1998.md#earliest-networking-capability-map).

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

`ZeldaClient` connects to host:14801. On enter it sends `N` + level-prefix + `#def`. Subsequent `D` packets carry position, chat, nickname, sprite colors, computer moves, board modifies, extras, carries, shots. Leadership uses timestamp comparisons with the local login time, not a general global-minimum algorithm; see the source qualifications below. [src]

## Board changes and a joining player's state

This selected retained-author-source review is cited as
`ZELDA2-BOARD-SOURCE-REVIEW` in the [evidence index](../docs/evidence-index.tsv).
It is source-derived behavior, not an observation of the compiled client.
The [historical run](precursor-runs-2026-10-30.md#bushes-stones-and-pots)
captured no board mutation while both clients shared a room. Native board
packets, replay order and restoration on re-entry therefore remain
unobserved here. The package's author-source versus decompiler-source
distinction is in [the source inventory](precursors-and-fan-builds.md#what-the-uploads-are). [src][live]

After the sender's two-character identity, relay type `B` carries whole-tile
rectangle x/y, packed dimensions and two-base-128-character tile values,
with the high component first and the usual 32 bias. Width occupies the
dimension value above its low three bits; height occupies those three bits.
Traversal is x-major: for each x offset, all y offsets follow. A non-square
rectangle distinguishes that order from row-major. These whole-tile board
coordinates must not inherit a player-position scale from another dialect.
[src]

The relay forwards data to party opponents without maintaining a board.
The selected client receiver requires a known peer, applies the rectangle
and records it in the current visit's ordered board history without echoing
the remote change. Local sword-cut and lift paths mutate and send through
the same route; a receive-only decoder does not implement local mutation.
[src]

Pairing pushes timestamp, position, chat, nickname, colours and carried
object. Board replay is triggered by a known peer's `T` timestamp: after
storing it and recalculating the leader, the current leader broadcasts its
retained board history and dead-baddy state to the party. It is not targeted
only at the newcomer, so existing party members can receive it again. The
selected source compares each peer timestamp against the local login time,
not the best timestamp found so far. Equal-local-time comparisons use
lexical identity ordering against the retained candidate; negative-time
handling is conditional, not a blanket earliest-nonnegative filter.
Iteration order can change the retained candidate identity, and the exposed
result is whether that identity is the local player. This agrees with the
[existing source/bytecode qualification](precursor-mechanics-2026-11-09.md#relay);
it must not be simplified to a global earliest-peer election. Level entry starts a fresh timestamp; successful level
loading clears the history and dead-baddy list. These are visit-local client
records, not persistent server world state. [src]

The selected mutation routine has a static quirk: its change detector
compares replacement values with the rectangle's top-left board entry as
mutation proceeds, rather than comparing each destination cell. Native
confirmation and a fidelity decision remain open. The selected receiver
also does not establish safe handling of truncated or out-of-board
rectangles. Defensive validation is independent implementation behavior,
not a historically captured rule. [src]

## Relation to later Graal

| Zelda Online | Later Graal |
|--------------|-------------|
| port 14801 | listserver / world ports evolve |
| text-line lobby | binary framed protocol with version token |
| `.zelda` RLE board | `.nw` GLEVNW01 text board |
| `arrays.dat` tile tables | `tiledefs.txt` / pics1.png |
| Java application (Zelda Online 2); Zelda Online 1 is an applet | Delphi client |

This is a relay precursor to the Delphi clients. The Delphi relay builds
remain tokenless through 1.1.9; central GSERV accounts/zlib begin later,
as separated in the canonical capability map. [bin][src]

## See also

`precursors-and-fan-builds.md` (2026-10-29) covers both Java versions from the uploads in more depth. Zelda Online 1 is a single-player applet with no network code. Zelda Online 2 ships 51 levels. It also covers the 11-bit `Z3-V1.02` code width, the full GServ line set, password saves, the ZeldaEditor and how its dialogs became 1st Graal's editor, and Java Graal.
