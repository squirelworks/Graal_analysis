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

## Default list port

`listserver` carries the endpoint a reimplementation should dial first: `host`, `port`, `kind` (`legacy` or `supported`) and `port_status` (`confirmed` or `assumed`). It is not the value the binary carries: that is kept as history in `built_in_host` and `built_in_port`.

- Host is always `listserver.graal.in`.
- 14921 is dead (the public service resets it) and is nobody's default.
- The default follows the login type the profile sends (the public listserver answers by login type, not by version or token): legacy = classic login (1.41 to 2.17, including 2.05) defaults to 14923; supported = gen-5 login (2.22, 2.3, 2.31) defaults to 14922.
- Every profile is `confirmed` except 2.05: Seihai's own login for it was run on its port in the matrix of 2026-10-25 (a real client was not captured). 2.05 is `assumed`: its classic login was not run.

The per-profile table and the evidence behind each status are in `list-ports.md`. `python3 list_ports.py --check` fails when a profile breaks the rule. Rule text: Seihai `documentation/port-rule.md`; public results: `../../protocol/public-listserver-2026-10-25.md` and `../../protocol/listserver-login-type-matrix-2026-10-25.md`.

## 1998 to 1.32 (added 2026-10-30)

Two more files cover the clients before 1.33. They use the flat layout of `v133-v139.toml`: each `[[version]]` holds every value, with no `base`.

- `v1998-v11.toml`: 20 builds from 1st Graal (Sept 1998) to 1.1 (Feb 1999). Generation 1, the text relay in `../../protocol/relay-1998.md`. There is no token, login or account, so `token` and `pli_sent` are replaced by `relay_game` (the game name sent with `N`) and `d_types_sent` (the relay `D` type letters). It also gives the dialog host, the level and save magics, and the config keys.
- `v121-v132.toml`: 1.21, 1.28 beta 2, 1.3 test, 1.31 and 1.32. Generation 2, GSERV tokens, see `../../protocol/gserv-1999.md`. Same keys as the 1.33 file, plus `plprops_sent` (the prop writer's table) and `bundled_servers`.

How the gen-2 sets were read: the same switch-table and send-site method as above, with each table found in 1.32 and then matched in the older builds by function shape. `pli_sent` is a lower bound here. 1.28 beta 2 and 1.3 test pass more ids in a register, which is why they list fewer ids than 1.21.

| | 1.21 | 1.28 b2 | 1.3 test | 1.31 | 1.32 |
|---|---|---|---|---|---|
| Server ids | 0–34 except 30, 100 | 0–38, 100 | 0–39, 100 | 0–40, 100 | 0–41, 100 |
| Player props parsed | 0–24 | 0–31 | 0–32 | 0–32 | 0–33 |
| Player props sent | 0–24 | 0–24, 26, 31 | 0–24, 26, 31, 32 | same as 1.3 | 0–24, 26, 31–33 |
| NPC props | 0–17 | 0–32 | 0–34 | 0–34 | 0–34 |
| UDP ids | none | 0, 10–22 | 0, 10–22 | 0, 10–23 | 0, 10–23 |
| GS1 commands | 71 | 84 | 85 | 85 | 85 |

1.32's sets match the 1.33 profile, except that 1.33 adds three GS1 commands (`setbody`, `setfocus`, `resetfocus`).

Correction to `v133-v139.toml`: `save_format` said `Graalsav9`. These builds write `Graalsv11`. The three save magics are referenced the same way as in 1.32, where the writer was traced (see `../../formats/graalsav.md`).

No build in this range was run. Every value comes from the binaries and the shipped notes. The features tagged `doc` come only from the release notes.
