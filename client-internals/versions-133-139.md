# Client versions 1.33 to 1.39

Date: 2026-10-23, live check 2026-10-30

This note covers what makes each of the seven gen-2 GNW clients different, both on the wire and for the player.
It is the writeup for `version-profiles/v133-v139.toml`, the machine-readable table that a client such as Seihai can load to behave as one exact build.
The table gives every key in full for every version. This note only describes changes.

It is cleaned: no addresses, function names or decompiler output.
The builds are the ones in `build-catalogue.md`, identified by MD5 there, and every shipped `Graal.exe` matched its catalogued hash.

## Sources and method

| What | How it was read | Confidence |
|---|---|---|
| Server → client ids, prop ids, UDP ids, GS1 command tables | Jump tables and the command table, as described in `cross-version-timeline.md` | confirmed |
| Client → server ids | Every call to the TCP send helper with a constant id. The helper is the one that prefixes `chr(id+32)`, appends `\n` and flushes at 4096 bytes. | confirmed for constant ids. A few call sites pass the id in a register and are not counted. |
| Login | The code that builds the first message after connect, read in 1.33 and 1.39 | confirmed in 1.33 and 1.39. 1.34 to 1.38 are assumed to be the same. |
| Windows, options, menus | The Delphi form resources (captions and components) | confirmed |
| `graalconfig.txt` keys | Plain strings ending in `=` | confirmed. From 1.38 on some strings are built one character at a time, so those lists may be short. |
| HUD and tiles | `state.png`, `sprites.png` and `pics1.png` shipped beside each exe, compared tile by tile | confirmed |
| Player-facing behaviour | The shipped `newfeaturesNNN.txt` and `readme.txt` | confirmed as release notes, not checked in code |
| Server behaviour | GServer-v2 source (public). Its version checks only distinguish 1.41 and 2.1+, so it treats all of 1.33–1.39 the same. Checked live against GServer-v2 beta4, see "Live check". | confirmed live for 1.33 and 1.39 |
| Live capture | 1.33 and 1.39 run under Wine against a local GServer-v2 beta4, with the traffic captured and decoded. See "Live check" below. | confirmed for 1.33 and 1.39 |

## What is the same in all seven

- **Wire.** Gen 2: every flush is one `u16be length` + zlib stream, with no size threshold, no cipher and no key byte. See `protocol/gserv-1999.md`.
- **Login.** Login is message id 0, which is `chr(32)` and also marks the client type as player. It carries the 8-byte token, then `chr(len+32)` + account, then `chr(len+32)` + password.
- **Server.** There is no listserver. The connect dialog is pre-filled with `www.graalonline.com:14900` and the `guest`/`guest` account. There is no server list window.
- **Levels.** Only GR-V1.00 to 1.03 load (`.graal`, plus `.zelda` Z3-V1 for the offline levels). There is no `.nw` and no `.gmap`. The board does arrive as `RAWDATA` (100, with an i3 length) followed by `BOARDPACKET` (101) in its own frame (confirmed live). Saves are written as `Graalsv11` (the reader also takes `Graalsav9` and `Graalsv10`; see `../formats/graalsav.md`).
- **Files.** The client asks for files with `WANTFILE` (23) and never sends `UPDATEFILE` (34). It handles no large-file ids. The reply is `RAWDATA` (100, i3 length) then `PLO_FILE` (102): `chr(len+32)` + name, then the file bytes, with no modtime (confirmed live in 1.39). For clients before 2.1, the server adds `.gif` to image names that have no extension.
- **No tampercheck** (39).
- **UDP.** There is a peer UDP channel for "data packages", with `noudp=` and `fixedudpport=` (default 14899).
- **Game modes.** One Player, One Player Online, and Two, Three or Four Players on one machine. Local multiplayer goes away in 2.0.
- **Window.** The window is 640×480 (648×508 outer). Alt+Enter switches to fullscreen.
- **Keys.** F1 opens options, F2/F3 load and save, F4 opens the editor, F5 loads a level, F6 opens the debugger, F7 opens the player list, and Alt+1 to Alt+7 take screenshots, show the minimap, show the bytes counter, take a snapshot and record.
- **Prop encodings.** These are not traced per build. Live, the server-sent forms of props 1–9, 11 and 13 parsed in 1.33 and 1.39 as the pre-2.1 forms in `protocol/player-props.md`. The rest are assumed (*inferred*). The forms are: sword `c(power+30)+str`, shield `c(power+10)+str`, bow `c(10+len)+image` or `c(power)`, head `c(len+100)+image`, and X/Y in half-tiles. No build in this range has X2/Y2. Prop 10 must be the bow form; a server that sends a gani string there (GServer-v2 beta4 does) is misread, and the rest of that prop stream is lost.

## Protocol changes

| Build | Client → server | Server → client | Player props | Other-player props | NPC props | UDP |
|---|---|---|---|---|---|---|
| 1.33 | 0–31 | 0–41, 100 | 0–33 *[inf]* | 0, 2, 8–13, 15–21, 24, 30–32, 50, 51 | 0–34 *[inf]* | 0, 10–23 |
| 1.34 | same | same | 0–33 | + 34 | 0–34 | same |
| 1.35–1.37 | same | same | same | same | same | same |
| 1.38 | + 32 `ITEMTAKE`, 33 `WEAPONADD`; − 25 | + 43 `DEFAULTWEAPON` | same | same | same | + 24 |
| 1.39 | + 80 `PROFILEGET`, 81 `PROFILESET` | + 75 `PROFILE` | + 34 `ACCOUNTNAME` | + 33 | same | same |

Some of these protocol steps line up with release notes.

- **1.34 adds other-player prop 34 (account name).** The same release saves ignores by account name (`ignoredaccounts.txt`).
- **1.38 adds `ITEMTAKE`.** The 1.38 notes say "when you get the item then the server increases your rupee count", which is the anti-dupe change.
- **1.38 changes how weapons are registered.** Up to 1.37 the client uploads each weapon it holds with id 25 (name, image and the full script, in the same layout as `PLO_NPCWEAPONADD`). From 1.38 it sends id 33 as `chr(0)` + `chr(default weapon id)` instead, and the server answers default weapons with 43 `DEFAULTWEAPON`. Both confirmed live (25 in 1.33, 33 in 1.39).
- **1.39 adds the profile window**, with request (80), set (81) and reply (75).

So a server can only tell 1.38 and 1.39 apart from the earlier builds by these ids or by the token.
gs2lib also knows `GNW02070` (1.38 rev1) and `GNW12080` (1.39 rev1). Neither build is in the archive.

## What the player sees change

### HUD art (`state.png`, `sprites.png`)

- **1.33 and 1.34.** `state.png` is 224×81, and the three item buttons carry the letters **A**, **S** and **D**. The HUD digits 0–9 sit at the bottom of `sprites.png` (128×484).
- **1.35.** A small **CHAT** label is added to `state.png`. It marks the focused player in 2/3/4-player mode, a feature the 1.34 notes describe.
- **1.38.** The button letters are removed from the art, because keys became configurable in that release. The client still draws A/S/D on the buttons itself (seen live in 1.39). The digits move from `sprites.png` (now 128×452) into `state.png` (now 224×97).

A client that copies these looks needs the A/S/D button art up to 1.37, and blank button art with the letters drawn on top from 1.38. It also has to read the digits from the right sheet.

### Tiles (`pics1.png`, always 1856×512)

The tileset is unchanged from 1.33 to 1.37. 1.38 changes 81 tiles ("some new tiles in pics1.png") and 1.39 changes 7 ("added some tiles and corrected the tile type for the dirty water").

### Windows and options

| Build | Change |
|---|---|
| 1.33 | Player list (F7) with four sections (GPs, Guild, Normal, Ignore). Its popup menu has Message, Ignore and History. More Options has 13 checkboxes: vsync, joystick, music, sound, reverse stereo, save downloaded images, external chat, compatibility draw, hide decompression errors, fixed UDP port, no UDP, ignore mass messages, no DirectInput. |
| 1.34 | The F6 debugger is rebuilt with Next, Run, Stop next call and Stop next script, plus panes for this.vars, vars, flags and NPC attributes. It only works offline. |
| 1.35 | Player list popup gains **Buddy** (`buddyaccounts.txt`). More Options gains "Don't use HTML for PMs". PMs render as HTML. The editor gains "Generate map" *[inf]*. A "(Senior GP)" tag string appears. |
| 1.36 | More Options gains "Limit the length of nicknames to [50]". An "(RC)" tag string appears. |
| 1.38 | The editor gains a "Show blocking tiles" checkbox. "Support for external chat programs" and its in/out message files are removed. |
| 1.39 | Player list gains **Profile** and **Options** buttons and a Profile popup item. There is a new Player List Options window (ignore mass messages, no HTML, no images in PMs, sort by nickname). There is a new Profile window (real name, age, sex, country, ICQ, e-mail, homepage, favourite hangout, favourite quote). More Options swaps the moved PM options for "Don't connect levels", "Ignore toalls" and "Don't load heads for the playerlist / map". |

### Controls

- **Up to 1.37** the keys are fixed: arrows or IJKL, D item, S or Space attack, A action, M map, Q item list, P pause, Tab chat.
- **From 1.38** each action can have up to three keys, set in `graalconfig.txt`. The actions are `up`, `down`, `left`, `right`, `item`, `attack`, `action`, `map`, `switchtochat`, `itemlist` and `pause`. The usable key names are A–Z, 0–9, Tab, Enter, Shift, Space, P_Up, P_Down, the arrows, N0–N9, Add, Sub, Mul, Div, Dec, and F9–F15.
- **1.38** adds Alt+8 and Alt+9 for zoom, and Ctrl+letter emotion icons from `levels/emotions` for A, B, D, E, F, G, H, L, M, O, P, R, S, T, W, X and Z. AFK, BRB and Zzz stay until the player moves.
- **1.39** adds Ctrl+C, K and Y. It also adds chat-line history on Up and Down (100 lines), and lets the player click the weapon list to select.

### Gameplay and rules (release notes)

- **1.34.** Hitting a mounted player costs their horse one bush, and at zero bushes the rider is pushed off. Two players can share a horse offline. Sounds are limited to one per type per frame and eight at once. `canbepulled` is separate from `canbepushed`.
- **1.36.** The server cap rises from 220 to 28000 players. Scripts can read the level object arrays (`bombs[]`, `arrows[]`, `items[]`, `explos[]`, `horses[]`).
- **1.37.** Sound volume falls off with distance. `showimg` works on normal NPCs. `playlooped` and `stopsound` are added. Arrays can be initialised as literals, and `true`, `false` and `hasweapon()` are added.
- **1.38.** A nickname equal to the account name shows as `*nick`. Item pickup is checked by the server. A laid-down shield is visible to others. Scripts can read and write `npcs[]`, and `hitnpc`, `setlevel2`, `changeimgpart` and the `test*()` functions are added. Explosions are capped at 1024. The `gotbow`/`gotsword` flags are dropped. PMs are saved to `pms/`.
- **1.39.** Head images are handled differently. Dead players don't block. Weapon-list and M-map fixes. In the editor, tiles can be painted by dragging, and an image dropped on the level becomes an NPC.

### Script commands

The GS1 command table grows from 88 to 93, 93, 104, 106, 109 and 111 commands. The full lists are in the TOML, and the per-build additions are in `cross-version-timeline.md`.
Two of the 1.34 additions, `carryobject` and `throwcarry`, are only announced in the 1.37 notes. So being in the table does not prove a command works in that build.

### Other shipped files

- **Languages.** English, Deutsch and Portugues up to 1.36. Español and Italiano are added in 1.37, Swedish in 1.38 and Français in 1.39.
- **World maps.** The world map image grows from 616×784 (1.33) to 952×952 (1.36) and 1008×952 (1.37). `mappw` is added in 1.35 and `mapmantara` in 1.37. These are server content, not client features.
- **gif2mng** ships from 1.38.

## Using the table

- `[[version]]` holds the full values for one build. `[version.features]` holds that build's on/off flags, and `[version.assets]` describes which HUD and tileset revision it ships.
- The top-level `[features]` table gives each flag's first build, its confidence and a one-line note. `[confidence]` gives one line per key on how sure each value is.
- To pick ids, use `pli_sent` for what the client may send, and `plo_known`, `plprops_known` and `npcprops_known` for what it parses.
  A server that sends anything else to one of these builds hits the default branch, and the client ignores it. Confirmed live in 1.33 and 1.39 for ids 47, 82, 156, 168, 190 and 194.

## Live check (2026-10-30)

1.33 and 1.39 were run under Wine against a local GServer-v2 beta4 with a local listserver copy, on loopback only, and the traffic was decoded.

- **Login props.** After the level loads, the first id 2 carries props 0 (nick), 11 (head), 13 (colours), 18 (status), 31 (UDP port) and 33 (additional flags), the same in both builds. The head goes as `chr(head number)` when it is a numbered default head. 1.34 to 1.38 are assumed to match.
- **Steady traffic.** Id 31 `PACKETCOUNT` goes about every 10 s. Id 3 NPC props go for each level NPC after the load, and level scripts cause id 18 and 7.
- **Board and files.** As described under "What is the same in all seven". For a name sent without an extension the server adds `.gif`. Downloaded images were not written to disk in this setup, and the level was cached under `weblevels/<server>/`.
- **Server message.** 1.33 shows the server message (41) as raw HTML text.

### Server compatibility (GServer-v2 beta4)

- It needs `generation = classic`, with the GNW tokens listed in `allowedversions.txt`. Otherwise it refuses the client with "Allowed: 2.0 - 2.31".
- The server checks the account with a listserver, even though the client connects directly. Without one the client is told "The login server is offline".
- It kicks 1.33 for id 25 ("Unknown Player Packet: 25"). 1.34 to 1.37 send the same id (*inferred* to be kicked too). A proxy that drops id 25 lets 1.33 play, though beta4 then warns about an invalid packet count, because the dropped messages are missing from the count.
- 1.39 logs in and plays. 1.38 has the same send set apart from profiles (*inferred* to work).
- It sends prop 10 as a gani string, which these clients misread (see "Prop encodings").

## Open

- Login props in 1.34 to 1.38 (seen live only in 1.33 and 1.39).
- Per-prop byte layouts for props not seen live (assumed above).
- The client → server UDP id set. The receive set is confirmed.
- The exact letter-to-icon mapping for emotions. The names are built at run time, and only AFK (A), BRB (B) and Zzz (Z) are given in the notes.
