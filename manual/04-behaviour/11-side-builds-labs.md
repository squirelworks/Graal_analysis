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

## 4.11.6 2.04 to 2.05 rev 2: what changed in the code

The three builds closest to 2.05 rev 2 were matched function by function on address-free instruction streams; unmatched counts are an upper bound on real churn [bin] (client-internals/build-diff-204-205.md#how-the-matching-works).

| Pair | Functions (old / new) | Identical | Changed | Only old | Only new | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 2.05 rev1 → rev2 | 6522 / 6529 | 6345 | 94 | 83 | 90 | [bin] (client-internals/build-diff-204-205.md#how-the-matching-works) |
| 2.04 → 2.05 rev2 | 6471 / 6529 | 5799 | 558 | 114 | 172 | [bin] (client-internals/build-diff-204-205.md#how-the-matching-works) |

| Rule | Source |
| --- | --- |
| 2.05 rev1 to rev2 moves about 20 game functions with identical class layouts and GS1 table: player counting reads both tests through one object (the "playerscount is fixed" note), the tutorial no longer creates a map object at start-up, one level-reset path drops a game-mode-5 flag and takes a loop bound from the main form instead of 632, and one of three `§`-to-CR/LF helpers is dropped | [bin][doc] (client-internals/build-diff-204-205.md#205-rev1--rev2) |
| rev2 is linked against a rebuilt VCL: its library units differ in shape from rev1's, while rev1's library matches 2.04's | [bin] (client-internals/build-diff-204-205.md#205-rev1--rev2) |
| 2.05 adds the classes `TGraalMap` (gmaps) and `TADP`, and drops `TEditorBaddy` and `TEditorLevel` | [bin] (client-internals/build-diff-204-205.md#204--205) |
| `TDrawableObject` gains a virtual method in 2.05, so every level-object class's slot numbers move by one: 2.04 `X.virt_N` is 2.05 `X.virt_(N+1)` | [bin] (client-internals/build-diff-204-205.md#204--205) |
| `TAdventureLevel` grows from 96 to 184 bytes (gmap and `.nw` state), `TAdventureCommand` from 68 to 76, and `TServerPlayer`, `TPlayer` and `TEditorNPC` shrink by 4 | [bin] (client-internals/build-diff-204-205.md#204--205) |
| The `GLEVNW01` reader and writer are new code beside the binary reader; the writer emits one `BOARD 0 <y> 64 0 <tiles>` line per row, and a new chest-line parser reports "Wrong chest data!" (→ §3.1) | [bin] (client-internals/build-diff-204-205.md#204--205) |
| New GS1 in 2.05: `loadmap`, `setz`, `updateterrain`, `setbacktile2` and an argument form of `setbacktile`; the table holds 161 commands, and only `loadmap` has an executor case (→ §8.2) | [bin] (client-internals/build-diff-204-205.md#204--205) |
| 2.05 writes PMs to `pms\messages_<name>.txt`, adds a `drawaslight` draw check, a script-editor button that handles `/* */` comments and tabs, and an editor routine clamping `playerx`/`playery` to 0–61; 2.04's `tempsitc.ttf` installer is left uncalled and the `Courier New` default is gone | [bin] (client-internals/build-diff-204-205.md#204--205) |
| Anti-debug: 2.05, its revisions, the 2.1 test builds and both NewWorld betas link the third-party `TADP` component with `Kill_Debugers`, `Stop_Execution`, `Anti_Procdump` and `Kill_Monitors` all on; it walks processes, modules and heaps and stops the client when it finds a debugger, loader or monitor (names such as `FPLOADER.EXE`). Builds up to 2.04 do not have it (→ §4.10.1) | [bin] (client-internals/build-diff-204-205.md#anti-debug-component-adp-new-in-205) |

## 4.11.7 The 2.05 rev 2 client's parts

2.05 rev 2 (`GNW03081`) is a Delphi build on DelphiX (DirectDraw, DirectSound, DirectInput) with zlib 1.1.2; its classes are named by RTTI [2.05] (client-internals/client-architecture-205.md#client-205-rev-2-architecture).

| Area | Classes and role | Source |
| --- | --- | --- |
| network | `TGraalClient` (socket, out buffer, zlib flush, `u16be` frame); `TServerListClient` (listserver link, no cipher, handles ids 0 and 1); `TAdventureClient` (game link, gen-3 send, a receive jump table of 59 ids, the login builder); `TWebClient` (HTTP for web levels and `openurl`); `TAdventureServer` (offline stand-in) | [2.05][inf] (client-internals/client-architecture-205.md#networking-classes) |
| socket rules | the game socket keeps the gen-3 iterator, the key and a first-message flag; disconnecting renames the server `Offline`; messages flush at 0x1000 bytes and the link drops at 256 KB queued | [2.05] (client-internals/client-architecture-205.md#networking-classes) |
| game model | `TAdventure` (main window and loop); `TAdventureLevel`, `TBoard`, `TBoardModify`; `TLevelObject` and its extras, leaps, bombs, explosions, balls, flying objects and carried objects; `TServerPlayer` with `TPlayer` and `TEditorNPC`; `TComputer` (baddy); `TAdventureHorse`; `TDisplayedNPCImg`, `TTempWeaponImg`; `TAdventureWeapon`; `TTileDef`, `TTempTile`; `TGraalMap`; the `TGraalAni*` gani model; `TCachedStream` | [2.05][inf] (client-internals/client-architecture-205.md#game-model) |
| script engine | `TAdventureCommand`, `TAdventureOperation` and `TAdventureVariable` parse-tree nodes with `TArray`, `TInteger`, `TDouble` and `TStringPosList` values, run by a recursive tree walk (→ §8.1) | [2.05] (client-internals/client-architecture-205.md#script-engine) |
| forms | connect, reconnect, server list, load level, server message, short message, player list and its options, profile, options, more options, links, sign codes, `TPersonAction` (the NPC "Set Npc's Action" editor, not a player menu), chest editor, debugger; editor and client are one executable until 2.3 (→ §4.9) | [2.05] (client-internals/client-architecture-205.md#ui-forms) |
| other code | a Delphi DES class (`UDesCipher`) for saved passwords, the hidden listserver host and the web cache, not the wire; GIF, MNG and JPEG decoders | [2.05] (client-internals/client-architecture-205.md#other-formats-seen-in-205) |

| Rule | Source |
| --- | --- |
| 2.05 hides the listserver host as a DES ciphertext and key built one `Chr()` at a time, and the port and `newmain` as plain characters built the same way; a hosts entry for the host is enough to redirect it | [2.05][cap] (client-internals/des-and-hidden-strings.md#hidden-strings); [2.05] (client-internals/des-and-hidden-strings.md#notes-for-tool-writers) |
| 2.22 keeps its in-memory copies of the three listserver hosts and port, and the account name in the config and before login, through `dec(b) = (NOT b − 10) & 0xFF`; the plain values come from `arrays2.dat`, so a memory search for the names finds nothing | [2.22][cap] (client-internals/des-and-hidden-strings.md#hidden-strings) |
| 2.22 saved passwords: a 49-character value starting with a marker is decrypted with a second key held by the options form, anything else with the first, so old saves still load; new saves use the second key (→ §3.7) | [2.22] (client-internals/des-and-hidden-strings.md#des-saved-passwords-and-the-web-cache-pointers) |
| None of these schemes protect anything; they keep strings out of a casual `strings` dump | [inf] (client-internals/des-and-hidden-strings.md#notes-for-tool-writers) |

## 4.11.8 Client features 2.00 to 2.31 by release notes

The shipped `newfeatures2001.txt` to `newfeatures2005.txt` are named by release year: 2001 covers 2.00–2.12, 2002 2.13–2.17, 2003 2.18–2.21, 2004 2.22 and 2005 2.3–2.31 [doc] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231).

| Version | Release-note highlights | On the wire | Source |
| --- | --- | --- | --- |
| 2.00 | online only: 2/3/4-player mode and save games removed; bush rupees and pot hearts go server-side; `warpto <account>` for GPs | | [doc] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.01 | level preloading on maps; `hitobjects` as the fair replacement for `hitplayer`; `openurl2` | 36/46 | [doc] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.02 | hats and signs with images; string parsing; free-server limits on light effects and complex ganis | | [doc] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.03 | `triggeraction`; `/` chat commands in RC and NC; the built-in zlib.dll replaced by in-game code "because it has been abused" | 38/48 | [doc] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.04 | gani `PLAYSOUND PARAM1`, `replacegani`, sound and animation changes | | [doc] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.05, 2.05 rev 2 | mostly bug fixes; server name in the window title | type 0, gen 3, 59 S→C ids | [doc][bin] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.1 | new start window and server list with account info; an image engine without GDI; gani scripts (`SCRIPT … SCRIPTEND`); string arrays; `play2`; auto-mapping; big map and minimap set by the game server (`bigmap=`, `minimap=`); ghost mode for free players; Alt+0 log window; `graalversion` | 170–174 | [doc][bin] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.12 | Graal2001/Graal2002 client compatibility; multi-level editing; `wraptext`, `wraptext2` | | [doc] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.13 | editor control-NPCs; a new RC with file browser and server list, RC and NC in one program (→ §7) | | [doc] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.14 | two server-list tabs; voice chat; player-list status icons (`playerlisticons=`); `serverwarp <world>`; files over 64 KB (`downloadpos`); gmaps auto-download | 180, 178, 68/69 | [doc][bin] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.15 | bug fixes, "enabling Graal2002"; `showimg2` | | [doc] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.16 | real transparency (`seteffectmode`); gani attributes `#P10`–`#P30`; a UDP check with a warning when UDP is blocked | props 54–74 | [doc] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.17 | Graal Kingdoms speed-ups; level heights stored in level files instead of the gmap | 185; adds 39 and the signed `arrays2.dat` | [doc][bin] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.18 | "new password encryption" for stored passwords; preloaded levels on entering a server | | [doc] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.19 | released alongside v3; new start screen and server list; "better compression" (bz2); `this.` strings on the client; on NPC-server servers the client stops sending non-`client.` strings | `GNW15053`, gen 4 | [doc][srv] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.2 | multi-byte sign text (Korean, Chinese, Japanese); server-side tile changes on gmaps via `updateboard2` | 186 | [doc][bin] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.21 | "network traffic reduced drastically"; `triggeraction 0,0,clientside,…` reaches a weapon's client-side part | `GNW01113`, compression byte | [doc][srv] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.22 | a third server-list tab for playerworlds under construction (gold and VIP only); `gravity`; `downloadsize` | gen 5, `GNW03014` | [doc][bin] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.3 | editor and online client split; `FILENAMECACHE.txt`; a new timer; B-tree NPC lookup; classic client-side mode removed; Graal3D tab; `graal://` with `serverstartparams`; full-precision positions; `timevar2`; more hacking checks | 44 dropped; 189 and 84 in 2.31 | [doc][bin] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |
| 2.31 | float-to-string fix, keyboard config saved, gmap NPC border crossing fixed | `GNW28015` | [doc][bin] (client-internals/feature-timeline.md#client-feature-timeline-200-to-231) |

A feature announced as "enabled later" often shows in a client's receive switch one or more versions before servers used it (full-precision moves in 2.3, level heights in 2.17), so a handled id does not prove servers of that era sent it [bin][inf] (client-internals/feature-timeline.md#reading-the-timeline-against-the-binaries).

## 4.11.9 Crossing gmap edges (2.22, 2.31)

A real 2.22 client walked east, south, west and north across a 2×2 gmap of open-grass levels on a lab server; the gmap file format is in → §3.2 [cap] (client-internals/feature-specs/06-gmap-overworld.md#lab-capture-of-a-real-222-client-crossing-gmap-edges-2026-10-24-cap).

| Rule | Source |
| --- | --- |
| Three different "maps" must not be mixed: level links (S→C 1, walking into one sends 0 or 30); bigmap-style server maps (`maps =`, a text grid the server alone uses to know which levels are adjacent); and gmaps (`gmaps =`, `GRMAP001`), where the client walks continuously. The `bigmap =` and `minimap =` options are a fourth thing: overlay settings sent as S→C 171 and 172 at login, and setting `bigmap` breaks gmaps | [srv] (client-internals/feature-specs/06-gmap-overworld.md#three-different-maps-do-not-mix) |
| At login the server sends S→C 49 (x×2, y×2, z+50, cell x, cell y, then the gmap name), `LEVELNAME` (6) with the level and again with the gmap name, 174, 10 and 156 with the gmap name; the client fetches the `.gmap` itself and sends 35 (`i5` modtime + name, 0 on a cold cache) for the three neighbour levels | [cap] (client-internals/feature-specs/06-gmap-overworld.md#lab-capture-of-a-real-222-client-crossing-gmap-edges-2026-10-24-cap) |
| A crossing uses only ordinary props, with no level-warp message: the cell prop (43 or 44) changes in the same props message as the wrapped coordinate (local = global − 64 × cell), and position props go out only on whole-tile steps | [cap] (client-internals/feature-specs/06-gmap-overworld.md#lab-capture-of-a-real-222-client-crossing-gmap-edges-2026-10-24-cap) |
| 2.22 sends flag sets `gr.x` and `gr.y` on every half-tile step carrying the global position (past 63.5) from the server's movement weapon, and re-sends 39 on each crossing; going west, 39 goes at global x 63.5 and the next props carry X = 63.0 and cell 0 | [cap] (client-internals/feature-specs/06-gmap-overworld.md#lab-capture-of-a-real-222-client-crossing-gmap-edges-2026-10-24-cap) |
| The server answers each crossing in one frame: 6 with the new level, 39 (level modtime, only when not cached), 0 (an empty board), 6 with the gmap name, 174, 10, 156 | [cap] (client-internals/feature-specs/06-gmap-overworld.md#lab-capture-of-a-real-222-client-crossing-gmap-edges-2026-10-24-cap) |
| 2.31 sends 46 (`GCHAR 1`) first, then the props with the cell prop and wrapped coordinate, and does not re-send 39 at the crossing (→ §2.4) | [cap] (client-internals/feature-specs/06-gmap-overworld.md#needs) |
| UDP id 24 ("entered level") goes to peers in the 3×3 neighbourhood; the server keeps 39 per level so the next entry can use 30 or 35 with a cached board | [srv] (client-internals/feature-specs/06-gmap-overworld.md#gmap-wire-behaviour-srv) |

## 4.11.10 What each executable names, 1998 to 2.31

A static survey lists, per build in link order, what each executable adds (+) or drops (−) against the one before. From 1.38 some config keys are built one character at a time, so a key can be read while missing from the list; garbled three-letter keys (`ekv`, `u5j`, `d4n`, `kxs`, `azg`) are such fragments [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys).

| Build | `graalconfig.txt` keys | Source |
| --- | --- | --- |
| 6th Graal (beta5) | + `joystickon`, `musicon`, `reversestereo`, `soundfxon`, `waitvertical` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 8th Graal (beta8) | + `saveimages` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.1 | + `editnickname`, `gamemode` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.21 | + `accountname`, `loadcolorsfromserver`, `password`, `serveraddr`, `serverport` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.28 beta2 | + `compabilitydraw`, `externalchat`, `language`, `nodecompressionerror` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.3 test | + `font`, `fontsize`; − `accountname`, `password` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.31 | + `fixedport`, `fixedudpport`, `noudp`; − `editnickname` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.32 | + `nomassmessages` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.33 | + `nodirectinput` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.35 | + `nohtmlinpms` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.36 | + `limitnicknames`, `nicknamelimit`; − `serverport` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.38 | − `externalchat` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.39 | + `dontconnectlevels`, `dontloadlistheads`, `nohtmlimages`, `notoalls`, `sortplayersbyname` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 1.41 rev1 | + `dontsavepasswords`, `fullscreenmode`, `usewinamp`; − `serveraddr` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| NewMain 1.42 | + `dontsavepms`, `dontusedirectx7`, `head`, `joyselected`; − `gamemode` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 2.00 | − `loadcolorsfromserver` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 2.1 test 2 | + `startinfullscreen` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 2.17.1 | + `automapping`, `microactivatebyvolume`, `microactivatekey`, `microactivationlevel`, `microinputdevice`, `microon`, `midivolume`, `mp3volume`, `quickplayerworlds`, `radiovolume`, `sfxvolume`, `voicecodec`, `voicevolume`; − `musicon`, `soundfxon`, `usewinamp` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| 2.31 | + `cachefilenames` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |
| Graal3D | `bodytex`, `bodyx`, `fixedport`, `fixedudpport`, `headx`, `noudp`, `serveraddr`, `serverport` | [bin] (version-profiles/matrix/builds-deltas.md#graalconfigtxt-keys) |

| Build | Delphi forms (windows) | Source |
| --- | --- | --- |
| 1st Graal | + `TADVENTURE`, `TCONNECTFRAME`, `TEDITBADDY`, `TEDITSIGNS`, `TLINKLIST`, `TLINKOPTIONS`, `TLOADLEVEL`, `TOBJECTNAME`, `TOPTIONS`, `TSHOWCODES` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| 2nd Graal | + `TCHESTEDIT`, `TEDITPERSON`, `TPERSONACTION` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| 3rd Graal | + `TEDITFLAGS` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| 5th Graal | + `TMOREOPTIONS` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| 6th Graal (beta5) | + `TOPENURL` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| 9th Graal alpha | + `TRECONNECTFRAME` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| 1.1 | + `TCONTROLSFRAME` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| 1.21 | + `TDEBUGGERFRAME` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| 1.28 beta2 | + `TEDITCHARACTER`, `TMESSAGEEDITOR`, `TPLAYERLIST` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| 1.32 | + `TRTFMESSAGE` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| 1.39 | + `TPLAYERLISTOPTIONS`, `TPROFILEEDIT` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| 1.41 rev1 | + `TSERVERLISTFRAME`, `TSERVERMESSAGE`, `TSHORTMESSAGE`, `TWAABOUT`; − `TRTFMESSAGE` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| 2.04 | + `TOBJECTSET` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| NewWorld betas | − `TCHESTEDIT`, `TEDITBADDY` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| 2.1 test 2 | + `TEDITNPC`; − `TEDITPERSON`, `TOBJECTSET`, `TPERSONACTION`, `TSHOWCODES` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| 2.17.1 | + `TABOUTDLG`, `TLOGFRAME`, `TRPGFRAME`, `TTILESARRAYFRAME`; − `TWAABOUT` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| 2.31 | − `TCHESTEDIT`, `TDEBUGGERFRAME`, `TEDITBADDY`, `TEDITCHARACTER`, `TEDITFLAGS`, `TEDITNPC`, `TEDITSIGNS`, `TLINKLIST`, `TLINKOPTIONS`, `TOBJECTNAME`, `TTILESARRAYFRAME` (the editor leaves the client) | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |
| Graal3D | `TADVENTURE`, `TCONNECTFRAME`, `TEDITLOOK`, `TMOREOPTIONS` | [bin] (version-profiles/matrix/builds-deltas.md#delphi-forms-windows) |

| Rule | Source |
| --- | --- |
| Sound names in the executable: 4th Graal alpha has `arrow`, `axe`, `bomb`, `chest`, `crush`, `dead`, `extra`, `frog`, `lift`, `put`, `sword`, `swordon`; 7th adds `water`; 8th adds `arrowon`, `compudead`, `fire`, `goal`, `horse`, `horse2`, `item`, `item2`, `jump`, `lift2`, `nextpage`, `sign`, `steps`, `steps2`, `stonemove`, `thunder`; 1.1.9 Gold drops `horse`, `horse2`, `steps2`; 1.34 brings back `horse2`; NewMain 1.42 drops `dead`, `goal`, `sign` (→ §4.7) | [bin] (version-profiles/matrix/builds-deltas.md#sound-effect-names-wav) |
| The NewWorld betas drop `chest`, `compudead`, `frog`, `item2`, `jump`, `stonemove` and `swordon`, which 2.05 rev2 and 2.17.1 carry | [bin] (version-profiles/matrix/builds-deltas.md#sound-effect-names-wav) |
| Images: 1st Graal names `letters`, `link`, `map`, `opps`, `pics1`, `state` (`.gif`); 3rd adds `heads.gif`; 5th adds `sprites.gif`; 1.21 brings the baddy, head, shield, sword, bomb and bow images; 1.33 moves the core sheets from `.gif` to `.png`; 2.00 adds lights, gates, doors and the tutorial maps; the NewWorld betas swap to `bodynw.png`, `pics1nw.png`, `spritesnw.png`, `newsword.png`; 2.17.1 moves the remaining item images to `.png` and adds the Kingdoms body parts, `picso.png` and `graal2002letters.png`; 2.31 drops `graalmap.png`, `shield1.gif`, `ss_arrow.png`, `ss_bomb.png` (→ §3.10) | [bin] (version-profiles/matrix/builds-deltas.md#image-names-the-executable-refers-to) |
| Fonts named: `Courier`, `MS Sans Serif`, `System` from 1st Graal; `Courier` dropped in 6th; `Courier` and `Courier New` from 1.34; `Arial` from 2.17.1 | [bin] (version-profiles/matrix/builds-deltas.md#font-names-in-the-executable) |
| In the shared Drive archive (73 exes in 55 folders) every PE timestamp is the same dummy 1992 date, so only file-version strings date the builds; it holds 2.00 and its revisions 1 to 3 but no 2.1.x release, 2.17, 2.22 or 2.31 (→ §1.1.1) | [file] (client-internals/drive-clients-inventory.md#drive-clients-set-what-it-contains-2026-10-24); [file] (client-internals/drive-clients-inventory.md#versions-present) |
| Under Wine the 2.0x exes from that archive stop at "Cannot open file … commands.rtf" until another build's data files are put beside them | [cap] (client-internals/drive-clients-inventory.md#running-them-wine) |
