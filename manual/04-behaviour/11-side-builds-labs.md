<!-- manual: kind=reference status=draft -->
# 4.11 Precursors, side builds and the 4.x clients in play

This chapter covers how the builds outside the 2.x Delphi line behave: the Java precursors, the relay room bridge, the Game Boy Color demo, the 39ster fan client, and the 4.04r2 and 4.20r8 clients run live. Their place in the build list is in → §1.7 and → §1.8.

## 4.11.1 Zelda Online and Java Graal

| Rule | Source |
| --- | --- |
| Zelda Online 1 (class files dated 16 May 1998) runs at scale 2 in a 512×448 box and fetches levels, `arrays.dat`, images and sound relative to its codebase. The rar ships 36 `Z3-V1.03` levels | [bin] (client-internals/precursors-and-fan-builds.md#zelda-online-1-may-1998) |
| Zelda Online 1 hard-codes its story per level name: people on `level13`, `level28`, `level22` and `cave2`, chests on `level21`, `level24`, `village3`, `level16` and `level29`, gated by progress flags | [bin] (client-internals/precursors-and-fan-builds.md#zelda-online-1-may-1998) |
| Zelda Online 1 already holds the sign glyph-code list `A B X Y u d l r h x y z 1 2 3 4 .` beside the 97-entry alphabet (→ §3.6) | [bin] (client-internals/precursors-and-fan-builds.md#zelda-online-1-may-1998) |
| Zelda Online 2 (files dated 18–26 July 1998) opens a start window with One-Player and Multiplayer modes and a server field defaulting to loopback, refuses to run on Java 1.0, and reads files from the working folder | [src] (client-internals/precursors-and-fan-builds.md#zelda-online-2-local-version-july-1998) |
| A second `ZeldaMain (1).class` differs from the shipped one only in the "free stone" tile left by a lifted stone: 1023 instead of 584. The readme warns that the local version's tile indexes differ from the online server's | [bin][doc] (client-internals/precursors-and-fan-builds.md#zelda-online-2-local-version-july-1998) |
| The Zelda Online 2 options hold a nickname, a show-own-name option, cap, cap-edge, belt and coat colours and the 10-character save code; the save code packs x and y (6 bits each), level index (9), rupees (10), darts (6), power in half hearts (5), four ability bits, four story-chest bits and a 6-bit set-bit count (→ §1.7) | [src] (client-internals/precursors-and-fan-builds.md#password-saves) |
| The Zelda Online 2 copy in the "very first graal" zip carries a player's edits of 13–15 February 2002: four new levels, four changed ones, and an `objects.dat` with 109 stamps | [file] (client-internals/precursors-and-fan-builds.md#zelda-online-2-in-the-very-first-graal-zip) |
| ZeldaEditor (Delphi 3, linked around 25 July 1998) has a toolbar with New, Open, Save, Save As, Undo, Cut, Copy, Paste, Delete, "Turn Selection Into A Warp Field", Edit Links, Edit Baddies and Edit Signs, a stamp palette, and keeps window positions in `ZeldaEditor.ini` as `Name:left,top,width,height` | [bin] (client-internals/precursors-and-fan-builds.md#zeldaeditor-july-1998) |
| GServ Standalone ("(C) Stefan Knorr 1997, based on JccVsd") is a game-neutral lobby on 14801: ids are `0000` plus a counter that wraps at 9999, the log is `GServProto.txt`, and a `ChessSync` thread sends every "Chess" player a one-character timer line each second (→ §2.3.1) | [src] (client-internals/precursors-and-fan-builds.md#network-gserv-standalone-and-the-java-clients) |
| The Zelda Online 2 client joins `Z` + level base + `1.6`, sends `C` and `-` on a level change and joins the new room as `def`; the real nickname follows in `D`. It answers the first `+` with `P` and pushes its state | [src][live] (client-internals/precursors-and-fan-builds.md#zelda-online-2-client); [live] (client-internals/precursor-runs-2026-10-30.md#what-the-wire-showed) |
| The client clamps baddy knock-back to ±4 before encoding, but one of the four clamps writes the wrong axis, so a large positive vertical knock-back overwrites the horizontal value | [src] (client-internals/precursors-and-fan-builds.md#zelda-online-2-client) |
| When two clients see each other at once both send `P`, GServ links the pair twice, and every later `D` line arrives twice (1144 relayed lines for 572 sent); a server that emulates GServ need not copy this | [live] (client-internals/precursor-runs-2026-10-30.md#what-the-wire-showed) |
| Java Graal: five classes in `Graal.jar`, all dated 2 July 2000 and signed; a 512×418 Java 1.1 applet on a Cyberjoueur page beside Bomberman, chess, Reversi and Tetris; starts on `level13.graal`; has a `nickname:` chat command; the 2002 rip holds 180 readable levels and 25 damaged ones, many `.zelda` files carrying `GR-V` headers | [bin][file] (client-internals/precursors-and-fan-builds.md#java-graal-july-2000) |
| Java Graal sends the Zelda Online 2 `D` types without `S` (colours) and with `L` (level name), so Java players show in default colours to others | [bin][src] (client-internals/precursors-and-fan-builds.md#java-graal-client) |

Constants of the shared Java engine, beyond those in → §1.7.1 [src] (client-internals/precursor-runs-2026-10-30.md#behaviour-constants-zelda-online-2-and-java-graal):

| What | Value | Source |
| --- | --- | --- |
| shield bump | 4 ticks | [src] (client-internals/precursor-runs-2026-10-30.md#behaviour-constants-zelda-online-2-and-java-graal) |
| lifting | 5 ticks | [src] (client-internals/precursor-runs-2026-10-30.md#behaviour-constants-zelda-online-2-and-java-graal) |
| baddy moves | sent by the level leader every 2 ticks (100 ms) | [src] (client-internals/precursor-runs-2026-10-30.md#behaviour-constants-zelda-online-2-and-java-graal) |
| push frames | advance every 4 ticks; letting go or turning resets the counter to 0 | [src] (client-internals/precursor-runs-2026-10-30.md#walking-into-a-wall) |
| liftable kinds | four; kinds 0 to 2 always liftable, kind 3 (heavy stone) needs the stronger glove; kind 2 always leaves a heart | [src] (client-internals/precursor-runs-2026-10-30.md#bushes-stones-and-pots) |
| board changes | each relayed as a `B` line; the level leader sends all current changes to every newcomer | [src] (client-internals/precursor-runs-2026-10-30.md#bushes-stones-and-pots) |
| chat font | TimesRoman bold 20 pt, black over a white copy one pixel right and down, centred at the player's x + 12 pixels times the zoom; the nickname is drawn the same way three tiles lower | [src] (client-internals/precursor-runs-2026-10-30.md#chat) |

## 4.11.2 The relay room bridge

Java Graal (2000) and the Delphi betas talk to the same GServ lobby but join different rooms. Run live against Knorr's own GServ [live] (client-internals/relay-room-bridge.md#result):

| Pair | Relay | Meet | What went across | Source |
| --- | --- | --- | --- | --- |
| Java Graal + 4th Graal alpha | stock GServ | yes | both drawn, nicknames, chat both ways | [live] (client-internals/relay-room-bridge.md#run-2-java-graal-and-4th-graal-alpha-no-rename) |
| Java Graal + 5th Graal | stock GServ | no | different rooms (`G2<level>` and `G3<level>`) | [bin][live] (client-internals/relay-room-bridge.md#result) |
| Java Graal + 5th Graal | GServ behind a bridge that renames `G2` to `G3` | yes | both drawn, nicknames, walking and chat both ways, a level change and back | [live] (client-internals/relay-room-bridge.md#run-1-java-graal-and-5th-graal-through-the-bridge) |

| Rule | Source |
| --- | --- |
| Every Delphi beta opens two relay connections, one to a room per level and one to a fixed game-wide room; the Java builds open one. Room names per build are in → §2.3.1 | [live][bin] (client-internals/relay-room-bridge.md#rooms-each-build-joins) |
| The bridge passes every line unchanged except the room in `N<room>#<name>` and `O<room>#<name>`; the rename must keep the level part, or players on different levels share a room | [live] (client-internals/relay-room-bridge.md#what-this-means) |
| 5th Graal sends `D` types `T P Y C N S`, Java Graal `T P C N D`; each ignores the types it does not know, so the `D` dialect lines up from Zelda Online 2 to 1.1.9 | [live] (client-internals/relay-room-bridge.md#run-1-java-graal-and-5th-graal-through-the-bridge); [live] (client-internals/relay-room-bridge.md#what-this-means) |
| Under Wine the betas lose the arrow keys, because DelphiX's DirectInput keyboard format lists one object and Wine fills only listed objects; with `WINEDLLOVERRIDES="dinput=d"` DelphiX falls back to `GetKeyboardState` and walking sends a `D #P…` line every 100 ms while a key is held | [live] (client-internals/relay-room-bridge.md#run-4-5th-graal-walks-in-the-shared-room) |
| From 3rd Graal the server box is greyed out at Cyberjoueur's fixed address on 14802; 4th alpha and 1st Graal keep an editable address on 14801 | [live] (client-internals/relay-room-bridge.md#how-it-was-run) |

## 4.11.3 The Game Boy Color demo

`Graal V1.1 Adventure Demo (PD) [C].gbc` is 262,144 bytes; its sources reassemble to a byte-identical ROM [bin] (client-internals/gameboy-demo.md#graal-game-boy-color-demo-1999).

| Rule | Source |
| --- | --- |
| Built with GBDK 2.x and LCC: 161 functions, of which 41 are GBDK library or crt0 routines | [bin] (client-internals/gameboy-demo.md#what-it-is-built-with) |
| Everything runs in the VBlank interrupt: OAM DMA, scrolling, the window slide and music every VBlank, game logic every second one (about 30 Hz); `main` switches the CGB to double speed and returns | [bin][live] (client-internals/gameboy-demo.md#what-it-is-built-with) |
| Cartridge type `$02` (MBC1+RAM) with RAM size 0; CGB flag `$80` (runs on both models); banks 6 to 15 are all `$FF` | [bin] (client-internals/gameboy-demo.md#header-and-bank-map) |
| Bank 0 core game; bank 1 entities, AI, lifting, camera, music; bank 2 graphics (two 256-tile sets, an 82-tile font, walk bitmaps, five BG palette sets, 172 sprite tiles); bank 3 objects, effects, the character table; banks 4 and 5 rooms | [bin] (client-internals/gameboy-demo.md#header-and-bank-map) |
| A room is one 32×32-tile BG map (256×256 pixels), written whole to VRAM; positions are 16-bit half pixels, a tile is 16 units; directions are 0 up, 1 left, 2 down, 3 right, as on the PC; sprites are 8×16, sorted by Y each tick | [bin] (client-internals/gameboy-demo.md#screen-and-coordinates) |
| Room header (13 bytes): map pointer, tileset (0 outdoor, 1 indoor), BG palette set, then count and pointer for links, texts and NPCs; the bank is room / 5 + 4 | [bin] (client-internals/gameboy-demo.md#room-format) |
| Map: 1,024 tile ids then 1,024 CGB attribute bytes; collision reads a second WRAM copy that changes when things are lifted | [bin] (client-internals/gameboy-demo.md#room-format) |
| Link (8 bytes): x, y, width, height, new x, new y (−1 keeps a coordinate), then the target room as 16 bits | [bin] (client-internals/gameboy-demo.md#room-format) |
| Text (4 bytes): x, y and a string pointer; a text at (0, 0) is shown only by index; signs are read only while facing up into a solid tile | [bin] (client-internals/gameboy-demo.md#room-format) |
| NPC (16 bytes): x, y, direction, character type, two unknown bytes, text index, five movement bytes (mode and patrol bounds), a 16-bit flag word (bit 0: turn and chase once lined up) and a 16-bit event number. Event 1, on the captive in room 4, is the only event | [bin] (client-internals/gameboy-demo.md#room-format) |
| Each tileset has a 256-bit walkable bitmap and a second 256-bit set read when something is put down; its meaning is open | [bin] (client-internals/gameboy-demo.md#room-format) |
| Seven rooms: six outdoor rooms in a 2×3 grid (0 start, 2, 3 with two chasers, 4 the captive, 5 "Hello!", 6 the house) and room 1, the house inside; room 0's sign reads "Welcome to Graal! Demo version by Stefan Knorr" | [bin][live] (client-internals/gameboy-demo.md#the-seven-rooms) |
| The text box is three lines of 18 characters, padded so words break right; in play only a d-pad direction other than the facing one turns the page; capitals are drawn red | [bin][live] (client-internals/gameboy-demo.md#text); [live] (client-internals/gameboy-demo.md#seen-in-an-emulator) |
| 31 character types, each with a name, three OBJ palettes and a two-frame 16×16 head (Fung Si Yun, Pach Soldier, Ninji, Lunar, Squall, Vincent, Mandi, Ryu, Zoraas, Mad Max, Pachukite, Matt, Brandon, Bob, Athena, Lizardon, Oldman and recoloured Gold, Red, Green, Blue, Fire, Silver, Theif and Water variants); NPCs and the player pick one by number | [bin] (client-internals/gameboy-demo.md#characters) |
| At most eight 50-byte entities, entity 0 the player; states 0 idle, 1 walking, 2 reading, 3 sword, 4 knocked back, 5 chasing, 8 carrying, 9 lifting; movement mode 1 is a random walk, 2 to 4 patrol | [bin] (client-internals/gameboy-demo.md#entities) |
| Controls: d-pad walks, B swings the sword (every character, three colours), A is the character's item (lift and throw for Fung Si Yun, a bomb for Ninji, a boomerang for Ryu, nothing else), Select opens the carousel, Start toggles music | [bin][live] (client-internals/gameboy-demo.md#player-controls); [live] (client-internals/gameboy-demo.md#seen-in-an-emulator) |
| Lifting compares the top two tile ids two tiles ahead with four liftable kinds (three kinds of bush and stone, and a dropped object never seen in play) | [bin] (client-internals/gameboy-demo.md#player-controls) |
| Eight one-shot sound effects on the pulse and noise channels, skipped during music; the music player reads its song from `$A000` in cartridge RAM, which the ROM never writes, so Start mutes the game until reset | [bin][live] (client-internals/gameboy-demo.md#sound); [live] (client-internals/gameboy-demo.md#seen-in-an-emulator) |

Seen in an emulator (PyBoy, CGB mode, 60 Hz frames) [live] (client-internals/gameboy-demo.md#seen-in-an-emulator):

| What | Value | Source |
| --- | --- | --- |
| walk | 4 pixels per logic tick, 2 per frame, 120 per second; a room takes about 2 s to cross | [live] (client-internals/gameboy-demo.md#seen-in-an-emulator) |
| against a wall | the walk cycle keeps running in place; no push pose | [live] (client-internals/gameboy-demo.md#seen-in-an-emulator) |
| sword | an arc from one side to the front, about 24 frames; hits knock back and blink; nothing dies, no damage, no game over | [live] (client-internals/gameboy-demo.md#seen-in-an-emulator) |
| lift | the object becomes its lifted tiles at once, is drawn where it stood for 10 ticks, then over the player's head; the carrier faces the screen with arms up and the object hides the head | [live] (client-internals/gameboy-demo.md#seen-in-an-emulator) |
| throw | flies about 6 ticks, breaks into four leaf pieces for about 8 ticks; nothing is written back to the map | [live] (client-internals/gameboy-demo.md#seen-in-an-emulator) |
| respawn | none while in the room (a stump stayed two minutes); the room reloads from ROM on re-entry | [live] (client-internals/gameboy-demo.md#seen-in-an-emulator) |
| Ninji's bomb | sits about 110 frames, flashes about 70, then a plus-shaped blast about three tiles each way | [live] (client-internals/gameboy-demo.md#seen-in-an-emulator) |
| Ryu's boomerang | about four tiles out and back, about one second | [live] (client-internals/gameboy-demo.md#seen-in-an-emulator) |
| NPCs | room 3's first soldier patrols the top at 1 pixel a frame; both soldiers chase at a little over 1 pixel a frame once lined up; Vincent and Squall wander in room 6 | [live] (client-internals/gameboy-demo.md#seen-in-an-emulator) |
| the captive | after its first text it walks two tiles left, lifts and throws the bush, and the second text opens; the player also starts as Fung Si Yun, so the text reads as if the player was meant to start as someone else | [live] (client-internals/gameboy-demo.md#seen-in-an-emulator) |

## 4.11.4 The 39ster client and GraalX

| Rule | Source |
| --- | --- |
| 39ster's client 1.00 (23 April 2014): `GameMaker.exe` is a small C++ engine on SDL 1.2 with zlib and stb_image, unrelated to YoYo's GameMaker; all Graal logic is about 1,500 lines of GameMonkey script in `main.gm` | [bin] (client-internals/precursors-and-fan-builds.md#39sters-graal-client-100-2014) |
| It reads `.nw` and `GR-V1.00` to `1.03` levels and `.gani` files, converts tile ids into the 2.x `pics1.png` layout, starts on `level13.nw`, has no socket code, and shows NPC images without running their scripts; it bundles 1,733 `.nw` levels and 1,321 GIFs from community worlds. Its `arrays.dat` is a plain-text tile-type table | [bin] (client-internals/precursors-and-fan-builds.md#39sters-graal-client-100-2014); [bin] (client-internals/precursors-and-fan-builds.md#shared-java-game-data) |
| GraalX has the same 28 forms as 2.0 rev3 and 2.01 and differs from 2.01 only in two control positions on the main form | [bin] (client-internals/precursors-and-fan-builds.md#graalx) |

## 4.11.5 4.04r2 and 4.20r8 live

The real 4.04r2 client (token `G3D17026`, reported by GServer-v2 as 4.042) and a restored 4.20r8 engine were run under Wine against GServer-v2 through a gen-5 logging proxy. Ganis and art came from the lab server, so anything a gani draws is the server's look [live] (client-internals/live-behaviour-404.md#graal-404r2-live-the-login-server-chat-movement-carrying-and-respawn).

| Rule | Source |
| --- | --- |
| The draw-layer mask is 0 while the lowercase server name starts with `login` and all layers (0x7ff) otherwise; ghost mode (S→C 170) forces 0x500. A 178 warp to `x,<name>,<host>,<port>` (field 0 unused, fewer than 4 fields ignored) ends the lobby (→ §1.8.6) | [bin][live] (client-internals/live-behaviour-404.md#the-login-server-never-draws-players) |
| In the Login session the game still runs: walking, chat and the sword send as normal; only drawing is cut | [live] (client-internals/live-behaviour-404.md#live-run-2026-10-31-404r2-and-420r8-next-to-seihai) |
| Tab opens a dark red chat bar at the bottom of the view and Enter sends (prop 12); the bar stays open after Enter, Tab closes it and sends an empty prop 12, Esc asks to quit. Letter keys without Tab are game keys | [live] (client-internals/live-behaviour-404.md#chat); [live] (client-internals/live-behaviour-404.md#live-run-2026-10-31-404r2-and-420r8-next-to-seihai) |
| Chat is white bold sans above the head with a pure blue (#0000FF) copy 1 px down and right; no bubble | [live] (client-internals/live-behaviour-404.md#chat) |
| Walking sends X2/Y2 (78/79) every 50 ms in half-pixels with the sign in the low bit, 16 half-pixels (half a tile) per tick; the first step carries GANI `walk` and SPRITE; each tick sends only the axes that moved; `idle` goes alone one tick after the last step; X/Y (15/16) are never sent | [live] (client-internals/live-behaviour-404.md#walking-and-pushing-against-a-wall); [live] (client-internals/live-behaviour-404.md#third-run-2026-10-31-update-packages-frames-focus-and-the-walk-in-detail) |
| Push starts about 0.9 s after the player stops (4.20r8: 0.85 s); `pushed,0` follows 0.55 s later and then once a second; a click sends `leftmouse` at the clicked point | [live] (client-internals/live-behaviour-404.md#walking-and-pushing-against-a-wall); [live] (client-internals/live-behaviour-404.md#420r8-the-packet-logger-build) |
| A on something that cannot be lifted plays `grab`; S sends 34 `sword.gani`, 157 `sword`, prop 10 `sword`, `sword.wav`, back to `idle` about 250 ms later; D with the bow sends 157 `shoot`, prop 10 `shoot,wbow1.png`, `arrow.wav` and C→S 9; with bombs C→S 4 | [live] (client-internals/live-behaviour-404.md#action-key-a-sword-s-item-d); [live] (client-internals/live-behaviour-404.md#live-run-2026-10-31-404r2-and-420r8-next-to-seihai) |
| A cut sends C→S 1 with the 2×2 stump tiles and `crush.wav`; a lift sends the same, then `lift` with `item.wav` and `lift.wav`, `carrystill` and carry sprite 1 about 300 ms later. The client keeps no respawn timer | [live] (client-internals/live-behaviour-404.md#cutting-and-lifting-a-bush-and-respawn) |
| The carried object is the gani's `ATTR3` sprite, drawn last 22 px above the body, so it covers the top of the head. D hides the player (status 0x16, `hiddenstill`, `hidden`), hidden walking averages 1.6 px per tick; A throws with C→S 11 and an empty payload | [live] (client-internals/live-behaviour-404.md#carrying-hiding-and-throwing) |
| Coming out of hiding with A sends `carrystill` and status 0x14; a second A throws; S throws straight from hiding. A thrown object breaks 250 to 350 ms after the throw, with no packet marking where it landed | [live] (client-internals/live-behaviour-404.md#pots-stones-and-black-stones) |
| After a reconnect while hidden the server had saved `hiddenstill` and status 22 with nothing carried; only the shadow drew until the first step. A server should clear the hidden bit and gani when it saves or loads an account | [live] (client-internals/live-behaviour-404.md#hidden-state-survives-a-reconnect) |
| The client runs GS1 weapon scripts but sends only `client.` string flags to the server: a probe that set `gr.probe`, `client.probe` and `probeflag` sent only C→S 18 `client.probe=2` | [live] (client-internals/live-behaviour-404.md#live-run-2026-10-31-404r2-and-420r8-next-to-seihai) |
| After login both builds send 37, 23 `basepackage.gupd` twice, 23 `bigmap.txt` (Login session only), 157 `idle`, 152 `GraalEngine,pmguilds` and `pmservers`, 154 `GraalEngine,lister,options,…` and `verifybuddies`, 46, 44, then 2 | [live] (client-internals/live-behaviour-404.md#live-run-2026-10-31-404r2-and-420r8-next-to-seihai) |
| Update packages: with no copy the client asks `basepackage.gupd` with 23 twice and saves it in `updatepackages/` (and per server in `updatepackages/<server, space as %032>/`); on the next run it sends C→S 47 with the file's CRC-32, while within one run it keeps asking with 23. `bigmap.txt` is asked once per run | [live] (client-internals/live-behaviour-404.md#third-run-2026-10-31-update-packages-frames-focus-and-the-walk-in-detail) |
| Prop 0 in the own props is the start screen's Nickname field, not the account; losing focus sends status 21 and regaining it 20; 24 is `GCHAR 9` every 5.142 to 5.151 s | [live] (client-internals/live-behaviour-404.md#third-run-2026-10-31-update-packages-frames-focus-and-the-walk-in-detail) |
| 4.20r8 survives only in the packet-logger build; putting back the 8 original bytes at the hook's call site gives a plain engine, which GServer-v2 accepts with `G3D20126` and which behaves as 4.04r2 for chat, walking, pushing, sword and items | [live][bin] (client-internals/live-behaviour-404.md#420r8-the-packet-logger-build) |

Lifting with glove power 3 on the lab level [live] (client-internals/live-behaviour-404.md#pots-stones-and-black-stones):

| Object | Glove | Board after lifting | Carry sprite | Item drop (GServer-v2) | D hides | Back after | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bush (2) | 1 | 677 678 / 693 694 | 1 | sometimes | yes | 14.2 to 14.5 s | [live] (client-internals/live-behaviour-404.md#pots-stones-and-black-stones) |
| pot (684) | 1 | 1770 1771 / 1786 1787 | 5 | a heart, every time | no | 15.0 s | [live] (client-internals/live-behaviour-404.md#pots-stones-and-black-stones) |
| stone (34) | 2 | 1834 1835 / 1850 1851 | 3 | none | yes | 15.0 s | [live] (client-internals/live-behaviour-404.md#pots-stones-and-black-stones) |
| black stone (990) | 3 | 1834 1835 / 1850 1851 | byte 0xe9 (201), not decoded | none | yes | 14.3 s | [live] (client-internals/live-behaviour-404.md#pots-stones-and-black-stones) |

The respawn times are GServer-v2's 15 s timer checked once a second, not the client's (→ §4.5.7) [live][src] (client-internals/live-behaviour-404.md#pots-stones-and-black-stones).
