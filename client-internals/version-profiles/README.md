# Version profiles, 1.41 to 2.17

Date: 2026-10-23

`141-217.toml` describes each client release from 1.41 rev1 to 2.17 well enough for a reimplementation to *be* that version. That covers what it sends and understands on the wire, and also what the player sees and can do.
`resolve.py` flattens the inheritance (`base`, `_add`, `_remove`) and prints JSON or one markdown block per version, with a source tag on every value:

```
python3 resolve.py 141-217.toml          # JSON
python3 resolve.py 141-217.toml --md     # markdown
```

Field names follow the Seihai profile schema: `token`, `listserver`, `client_type`, `generation`, `login_key_byte`, `compression`, `cipher`, `pli_sent`, `plo_known`, `props_max`, `prop_diffs`, `login_props`, `level_formats`, `file`, `tampercheck`, `udp`, and `features`.

## Sources

| Tag | Meaning |
|---|---|
| bin | Read from that build: switch tables, send sites, DFM forms, strings, shipped images. 24 executables were scanned (1.41 rev1, NewMain 24/26, 2.0 r0–r3, 2.01 r0–r1, 2.02 r0–r2, 2.03, 2.04, 2.05 r0–r2, 2.1 test 2/3, NewWorld betas 1/2, 2.1.7.1) |
| doc | The release notes shipped with the clients (`newfeatures141/142/2001/2002.txt`) |
| srv | GServer-v2 source: what a server does differently per version |
| forms | The DFM resources: start window, options, controls, server list, player list |
| inf | Not checked in that build. Either the value is carried from the nearest scanned build, or it is placed at the release that introduced the feature |

No binaries of 2.1 release, 2.12, 2.13, 2.14, 2.15 or 2.16 are in the archive. Their entries are release notes plus server source, and every value they inherit from a scanned build is tagged `inf`.

## How the packet sets were read

- **Server → client:** the receive dispatcher is a `case` on `id` with a jump table. The ids with a non-default arm are the ids the build handles. The results match `cross-version-timeline.md` except for one correction (below).
- **Client → server:** every packet goes out through one virtual send method that takes the id as a byte argument. Scanning each build for constant ids passed to that call reproduces the known 2.05 set exactly (`packet-ids.md`), so the same scan was used for the other builds. Id 0 is sent through a computed path and is present in all of them.
- **Props:** each prop parser and the prop writer are `case` tables too. The writer's table is the list of props the client can send. In 2.05 it matches the "sent by the client" list in `player-props.md`.

## Wire boundaries

| Change | First build | Tag |
|---|---|---|
| gen 3 (key byte + LCG insertion), server list window | 1.41 | bin |
| `.gani`, light effects, PLO 42, 44, 45, 150, 151, 153; **UPDATEFILE (34) sent** | 1.42 | bin |
| `.nw` loader dropped (until 2.05; GraalX keeps it), listserver host DES-hidden, PLO 154, 155 | 2.00 | bin |
| ADJACENTLEVEL (35), HITOBJECTS (36) sent; PLO 46, 156 | 2.01 | bin |
| PLO 47; player props 37–41 (`#P1`–`#P5`) parsed and sent; NPC props to 40 | **2.02** | bin |
| LANGUAGE (37) sent after login | 2.02 rev2 | bin |
| TRIGGERACTION (38) sent; PLO 48, 165 | 2.03 | bin |
| PLO 166, PLO 26 dropped; prop 42 | 2.04 | bin |
| `.nw` + `.gmap`; PLO 168 | 2.05 | bin |
| Bow slot → GANI string, `.png` defaults, PLO_FILE modtime, FILEUPTODATE, `sprite % 4` for NPCs, prop caps lifted | 2.1 (GNW31101) | srv |
| Large files (LARGEFILESTART/END) | 2.14 | srv, doc |
| TAMPERCHECK (39), SHOOT (40), SERVERWARP (41), MUTEPLAYER (43), PROCESSLIST (44/45); signed `arrays2.dat` listserver; account and password sent to the listserver | 2.17 (checked); some may be earlier | bin |

Corrections to earlier notes:

- **PLO 47 and props 37–41 are already in 2.02**, not first in 2.02 rev2 as `cross-version-timeline.md` says. That note skipped the 2.02 base build.
- **1.41 has no UPDATEFILE sender.** It never revalidates a cached file. 1.42 adds it, which matches the 2.00 note "files are now automatically downloaded again from the server when they have been updated".
- The 2.02 rev1 notes say the client language is sent to the server. No LANGUAGE send site exists in rev1, though. The first one is in rev2.
- The 2.1 test builds still send 2.05's token (GNW03081), so a server cannot tell them apart from 2.05 and uses the pre-2.1 paths for them.

## What the player sees

These are the `features` keys, which matter most for making the client look and behave like the chosen version.

- **1.41.** The start window lists game modes (One Player, One Player Online, Two/Three/Four Players) beside character heads. Local 2–4 player split screen and save games (F2/F3) still exist. There are no ganis, so animation runs on sprite numbers only. The HUD gets its AP bar under the ASD box this version, plus a "sparring" label and the R key for ratings. Right-clicking a player opens their profile. The options window has a Save games page. The HUD sheet has two chat-bubble colours and no gralat bag, clock or day/night icons.
- **1.42 / 2.00.** The game becomes online-only. The start window shows a character with Training (built-in tutorial levels) and Start buttons. The 2.00 start window is titled "Graal 2001". Keys are rebindable in the Controls window. Ganis and light effects arrive, with a "Don't use DirectX7" option. The HUD sheet adds admin, guild and mass chat-bubble colours, a gralat bag, a clock and day/night icons. The player list gets a "Staff" section (from 2.00).
- **2.01–2.04.** Levels preload on the map, and a map-reading animation plays. 2.02 adds hats (`#P1`–`#P5`), images in signs and HTML-window navigation. 2.04 adds `replacegani`, tile replacement, attaching the player to an object and a weapon-select toggle.
- **2.05.** The server name appears in the title bar. `.nw` and `.gmap` levels load. The shipped HUD sheet adds the "PK off" sword icon (identical to the 2.1 test sheet), although the notes date that feature to 2.1.
- **2.1.** A new start window and server list show account info. The options window gets tabs (General, Video, Audio, Controls) and a Direct3D toggle. Ghost mode, auto-mapping, map and minimap set by the gserver, the Alt+0 log, smilies in PMs and gani scripts all arrive, and default images switch from GIF to PNG/MNG.
- **2.12–2.16.** The editor gains multi-level editing (2.12). Gani attributes grow to `#P9` (2.13) and then `#P30` (2.16). The server list splits into two tabs (2.14), which also bring voice chat, OGG/MP3/MOD music, volume sliders, player status and `serverwarp`. 2.16 adds transparency modes, `enablefeatures` and `showani`/`showpoly`/`showtext`.
- **2.17.** The start window gains payment buttons and a "Private Server List". The options window gains Audio and Microphone tabs and an Automapping toggle. The player list gets status (Online/Away/DND) and Mute. The client handles the RPG window, Kingdoms and New World modes, and level heights.

## Open

- 2.1–2.16 packet and prop sets are inferred from neighbours. A binary of any of them would pin them down.
- The original 1.41 listserver host and port: the only surviving 1.41 copy is patched for graal.in.
- Whether 1.41 and 1.42 send the account to the listserver, or only to the game server.
- The props each version sends at login are only verified for 2.05.
- The 2.17 other-player prop parser and its GS1 command count were not read.

## Default list endpoint

Every profile with a listserver points at **`listserver.graal.in`** and carries a `class`:

- **legacy** = port **14923**: the classic single-frame login (plain zlib frame with id 0 and id 1). Every build up to and including 2.17 sends it.
- **supported** = port **14922**: the gen-5 handshake (id 7 with the `GNW30123` token, then gen-5 frames). 2.22, 2.3 and 2.31.

`class_status` says how sure that is: **confirmed** (seen on the public service) or **assumed** (placed by the rule above). Port 14921 is refused by the public service and is no profile's default; the old host and 14921 that some builds carry are noted in comments only. 1.33 to 1.39 have no listserver in their build (they use 2.05's, so legacy 14923, when a list is wanted).

| Build | Host | Port | Class | Status | Evidence |
|---|---|---|---|---|---|
| 1.33 to 1.39 | none in the build | borrow 2.05's | legacy | assumed | no listserver code |
| 1.41 | listserver.graal.in | 14923 | legacy | assumed | the graal.in-patched copy carries host and port; not run |
| 1.42 | listserver.graal.in | 14923 | legacy | assumed | classic login; build's own host and 14921 not used |
| 2.00 | listserver.graal.in | 14923 | legacy | **confirmed** | classic login on 14923 got a plain zlib id-0 list (2 of 2 runs) |
| 2.01 to 2.05 (rev2), GraalX | listserver.graal.in | 14923 | legacy | assumed | same classic login as 2.00; 2.05 with another binary's gen-5 login also got a list on 14923 (and on 14922); a classic 2.05 login was not run |
| 2.1 test to 2.16 | listserver.graal.in | 14923 | legacy | assumed | classic login; the 2.1 test builds carry 14922 but a classic login got no reply there (2.17 run) |
| 2.17 | listserver.graal.in | 14923 | legacy | assumed | classic login got no reply on 14922 twice; not tried on 14923 |
| 2.22, 2.31 | listserver.graal.in | 14922 | supported | **confirmed** | gen-5 login: list and status frames on 14922 (2 of 2 runs each) |
| 2.3 | listserver.graal.in | 14922 | supported | assumed | no binary; carried from 2.31 |

Public-service facts are in `../../protocol/public-listserver-2026-10-25.md`.
