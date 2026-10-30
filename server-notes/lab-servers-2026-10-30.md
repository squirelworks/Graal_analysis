# Our gserver and listserver, and the open-source servers around them (2026-10-30)

What the project's own servers are, what they do, and how they compare with GServer-v2 beta4, graal-serverlist, glauncher and gs2-parser. The open-source repositories were read, not changed: nothing was pushed, filed or proposed to any repository outside squirelworks. Their code is summarized and cited, not copied. How to run our servers is in `../tools/lab-servers/README.md`.

Tags: **[src]** read in the named source, **[lab]** run in the offline lab today with the real client named, **[inf]** inferred, not run.

## 1. What "our servers" are

There is no squirelworks gserver or listserver repository. The servers the project runs are the **Seihai lab pack** (`seihai-lab/servers/seihai-lab-servers.tar.gz` in the project files, built 2026-10-22):

| Piece | What it is |
|---|---|
| gserver | GServer-v2 **master `efb5b90`** (2025-01-07), built with `V8NPCSERVER=OFF`, `UPNP=OFF`, against gs2lib `b839106` plus a one-line patch that puts the 2.05 token `GNW03081` in the 2.1 slot. Reports `3.0.9-beta`. Ships the stock `default` world with `onlinestartlocal.nw`. **[src]** |
| listserver | `listserver.py`, a Python stub (119 lines) written for the lab. Replaced today by version 2 (`../tools/lab-servers/listserver.py`). |
| sources kept | `seihai-lab/sources/GServer-v2.zip` (the same `efb5b90` tree) and `graal-listserver.zip`, which is **Guthius/graal-listserver** (a C# "2.1.5 list server emulator"), not xtjoeytx/graal-serverlist. |

Older material (the 39ster 2.1 server, Phoenix, Ash) is in `ash/` and `server-notes/01-lineage.md`; none of it runs in the lab.

### What our gserver does with each client generation **[src]**

* The login type byte selects the player type and cipher generation (`../protocol/client-versions.md`); v5's type 5 is `PLTYPE_CLIENT3`. A trailing identity string (`win`, hardware ids, OS) is read and forwarded to the listserver.
* Version comes from the token through gs2lib's table. An unknown token that is in `allowedversions.txt` gets `CLVER_UNKNOWN` (0), which sorts below everything, so the client is served every pre-2.1 code path. This is why 5.24 (`G3D15010`) gets the gani prop in the old form (v5 thread, 2026-10-30).
* Below `CLVER_2_1` the level goes through `sendLevel141`, which never sends `PLO_SETACTIVELEVEL` (156). Real 2.05 waits for 156 (live-trace finding), so unpatched it stalls on the loading screen. Hence the gs2lib patch, which costs real 2.1 its login.
* `PLI_UPDATEFILE` for files on a hard-coded default list (`idle.gani`, `walk.gani`, `sword?.png`, `body.png`, the stock `.wav` set, `pics1.png`, and others) always answers "up to date" without looking at modtimes. `PLI_WANTFILE` has no such check.
* 2.21 to 2.31 get a hidden clientside weapon, `-gr_zlib_fix`, that pads chat to dodge the 2.x clients' zlib bug (see `../version-profiles/2.22-2.31.md`).
* Listserver link: plain `REGISTERV3` line, then zlib frames: `NEWSERVER`, `SERVERHQPASS`/`SERVERHQLEVEL`, `SETPLYR` + `PLYRADD` per player, `VERIACC2` per login, `SENDTEXT Listserver,settings,allowedversions,...`. It never pings on its own.

### Real clients against it today **[lab]**

Loopback namespace, Wine, listserver version 2:

| Client | List | Game |
|---|---|---|
| 2.05 rev 2 | 14921, shape A (`newmain` only) | in game, `onlinestartlocal.nw` |
| 2.17.1 | **14922**, shape B (list name + account, plain zlib); "Classic" tab | in game |
| 2.22 | 14922, gen 5 (id 7); "Bronze" tab, status, Show More and Donations | in game |

2.17.1's choice of 14922 for a plain login is new: the public listserver stays silent to a plain login on 14922 (`../protocol/public-listserver-2026-10-25.md`). So either the 2001-era public server answered plain logins on 14922 too, or 2.17.1 was built against a different list server. Open.

## 2. GServer-v2 beta4 against our build

`beta4` (`365bbd2`, 2026-10-26) is 807 commits ahead of `efb5b90`: 374 files, +79k/-34k lines. It is a rewrite of most of the tree (`TPlayer` → `player/PlayerClient*`, `TLevel` → `level/`), C++23, built with vcpkg, and it fetches gs2lib `5c36ab8` and gs2-parser `73e7ea8` at configure time. **[src]**

What changes for real clients **[src]**:

| Area | efb5b90 (ours) | beta4 |
|---|---|---|
| Classic tokens | 1.33 to 1.411, 2.1 up; nothing for 2.00 to 2.05 | adds GSERV007 to 018 (1.21 to 1.32), 1.38r1/1.39r1, 2.00 `GNW24011`, 2.01, 2.02, 2.02r2, 2.03, 2.04, **2.05r2 `GNW03081` as `CLVER_2_052`**, NewWorld 2.02 `G2N15041`, Graal Worlds. Still no `G3D15010`. |
| Level send | separate `sendLevel141` for < 2.1, no `SETACTIVELEVEL` | one path for every version: `LEVELNAME`, board (blank board first on first load), links, signs, chests, `LEVELMODTIME`, then NPCs and **`SETACTIVELEVEL` for every version** |
| 2.05 | needs our gs2lib patch, which locks out 2.1 | no gs2lib patch needed, but stock beta4 still fails real 2.05 and 2.17.1 (below); with our three-fix patch, in game **[lab]** |
| zlib bug of 2.x clients | `-gr_zlib_fix` clientside weapon for 2.21 to 2.31 | fixed in the receive path: on a zlib data error gs2lib retries as raw DEFLATE and rolls the gen-5 iterator back one step; weapon removed |
| Big packets | manual `PLO_RAWDATA` handling | gs2lib `CFileQueue` rewritten for RAWDATA (2026-10-26) |
| Board changes | lost when a level unloads | kept (`def25322`) |
| Server-side scripts | V8 GS2 NPC server (we build without it) | adds a **GS1 NPC server** (ANTLR grammar), tested on the "newmain" generation; V8 still optional |
| Listserver link | no keep-alive | `SETIP` every 60 s as keep-alive; `VERIACC2` carries a GSHORT identity length; a `localhost` option skips listserver verification |
| Ancient clients | | bow and bomb power for ancient clients, the bow removed for old clients, loading animation and type-1 tileset fixes |

beta4's own notes (`bin/docs/server-unimplemented.md`) say 1.38 to 1.411 and the 2.x/3.x "newmain" era are fully supported client-authoritative, clientside GS1 works up to 5.007, and server-side GS2 is not supported.

### beta4 built and run against real clients **[lab]**

Built here 2026-10-30 (GCC 14, CMake 3.31, system antlr4 4.10 with the Maven Central 4.10.1 jar in place of the pinned 4.13.2 download, `UPNP=OFF`, no V8). Two layers stand between stock beta4 and the old clients.

**Config.** Stock `allowedversions.txt` uses `[generation-range]` with `classic = GNW13110` (1.41r1 only) and `newmain = GNW03014:GNW28015` (2.22 to 2.31), and the stock generation is `newmain`. So out of the box beta4 refuses 2.05 and 2.17 at login. The lab pack widens `newmain` to `GNW24011:GNW28015` (2.00 to 2.31) and `classic` to 1.33 to 1.41r1; the originals are kept as `*.stock.txt`.

**Code.** With the versions accepted, the logs show `New login ... [GNW03081 (2.05r2)]` and `[GNW22122 (2.17)]`, and the clients still fail:


* 2.05r2: logs in as `GNW03081 (2.05r2)` and stays on the loading screen.
* 2.17.1: "Invalid PlayerProp" right after login.

Three causes, found by decoding the pcap and comparing beta4's server-to-client order with efb5b90's:

1. Gen-3 clients (2.05, 2.17) put `PLI_LANGUAGE` in the same frame as the login line. beta4's `IPacketHandler::parseLoginPacket` reads the login line and drops the rest of the frame, so the new player's gen-3 iterator is one step behind for the rest of the session. This is the 2.17.1 error.
2. `PlayerClientOriginal` (login type 0) never sends `PLO_SETACTIVELEVEL` (156). The single level path in the table above is `PlayerClientNew`'s; the Original path has no 156. 2.05 waits for it (live-trace finding).
3. `PlayerClientOriginal` sends the first `PLO_LEVELNAME` after the board. efb5b90 and the live-trace stub send it before, and 2.05 stays on loading otherwise.

`../tools/lab-servers/gserver-beta4-lab.patch` fixes all three (keep and replay the login remainder; send 156 from 2.01 up; LEVELNAME first). With it, real 2.05r2, 2.17.1 and 2.22 each list the server on listserver version 2, reach the game and walk, with no unknown-packet logs. One difference from efb5b90 seen in the trace and left alone: beta4 answers a pre-2.1 client's request for a default file with `PLO_FILESENDFAILED` (30) where efb5b90 sent `PLO_FILEUPTODATE` (45); 2.05 did not mind.

None of the three can be done in config. The player class comes from the login type byte (`PlayerLogin::msgLoginPacket`: type 0 is `PlayerClientOriginal`, which 2.05 and 2.17 send), not from `generation` or `allowedversions.txt`; `PlayerClientOriginal`'s level send has no generation or option check; and fix 1 is in the shared login parser. The `generation` setting changes props, baddies, items and NPC details, not these paths.

Checked again with a stock beta4 build (2026-10-30, widened `allowedversions.txt`) because a "legacy port" or old-client toggle would make the patch unnecessary. There is none: beta4 opens one client listener (`serverport`), and its options list has no old-client or encryption switch. The one related knob is `generation`:

* `generation = newmain` (stock): 2.17.1 draws the level, then on the first step the server logs `Unknown Player Packet: 55` and the client shows "Invalid PlayerProp type in constructPropFor" and drops. This is fix 1's iterator desync.
* `generation = classic` with 2.17's token added to the classic range: worse; the login bundle is read as garbage (`Unknown Player Packet: 112`, "sending invalid packets") and the client is dropped before a player exists. beta4's own `docs/start-here.md` warns that 2.x clients on a classic server get mangled packets.

For 1.33 to 1.39 (`generation = classic`, so a second server folder on port 14803) the patch adds three more fixes, and the pack two config changes; details in `../tools/lab-servers/README.md`. The one that matters beyond 1.x: beta4 treats "packet count is 0" as "the next frame is a login" while `PLI_PACKETCOUNT` resets the count, so any client that sends id 31 alone in a frame is misparsed on its next frame and kicked after three. The others: id 25 (1.33 to 1.37 weapon upload) accepted; prop 10 in the bow form on classic; the stock default account's `MAXHP 3.00` loads as 0 hearts (config `MAXHP 3`). Real 1.33 to 1.39 now play on it.

The patch also carries a fourth, smaller fix from the v4 lab: the account loader clears the hidden bit (`STATUS` 0x02), so a player who quit while hiding under a carried object does not log in invisible.

These are bugs against the real clients, not lab choices, so they would be worth upstream; under the project rule nothing was sent outside squirelworks.

## 3. Listservers

| | Our stub (10-22) | Our v2 (10-30) | graal-serverlist `feature/revamp` (2022) | Guthius graal-listserver (2025) |
|---|---|---|---|---|
| Plain login (id 0 / id 0+1) | yes (list twice for 0+1) | yes, once | yes (needs id 1) | yes, needs `newmain` |
| Gen 4 (id 4) | yes | yes | yes | no |
| Gen 5 (id 7, 2.22/2.31) | **no** | yes, two zlib frames as the public 14922 | yes | no |
| RC list (id 5) | no | yes | yes | no |
| Gserver link | register, VERIACC2 | + players, HQ level tag, drop on disconnect | full (MySQL accounts, profiles, PM, buddies, file serving stubbed out, IRC) | none (static `servers.json`) |
| Accounts | any | any, or a file | MySQL | JSON files |

graal-serverlist is the protocol reference our v2 follows for ids and the HQ-level tags (`U`, `H`, none, `P`, `3`). Its `GETFILE3` file serving is commented out, so no open listserver serves files to a gserver. Guthius's server names the listserver ids by their buttons: 3 "Show More", 5 "pay by credit card" (the 2.22 Donations button), 6 "pay by phone".

## 4. glauncher and gs2-parser

* **glauncher** (2022) is a Detours DLL plus launcher for the official v4+ client. It hooks `gethostbyname` (maps `loginserver.graalonline.com`, `Graalonline.com`, `loginserver2/3`) and `connect` (rewrites port 14900) from a line-based `license.graal`. It changes nothing in the protocol. In the lab a bind-mounted hosts file does the same, so we do not need it.
* **gs2-parser** compiles GS2 to the bytecode that v4+ clients and the V8-less beta4 load. GS2 is post-2.x; the 2.x clients this project targets run GS1 text (`../CONSOLIDATED.md`: no GS1 bytecode in 2.05). Useful later only for comparing GS2 bytecode or if Seihai ever runs v4+ worlds.

## 5. What was changed, and what was not

Changed (lab only, our files):

1. Listserver version 2, with tests. It fixes the missing gen-5 login, the duplicate reply, the stale rows and the dead player count, and adds RC lists, an account file and the site/upgrade URLs. Checked against real 2.05, 2.17.1 and 2.22 and against Seihai 2.00 to 2.31.
2. `run-lab.sh` passes `accounts.txt` to the listserver when it exists.
3. A second gserver pack, `seihai-lab-servers-beta4.tar.gz`: beta4 `365bbd2` with `gserver-beta4-lab.patch`, beside the efb5b90 pack. It runs 2.05 without a gs2lib patch, so 2.1 keeps its token (no 2.1 client was run), the receive-side zlib fix and the GS1 NPC server.

Not changed:

* The efb5b90 pack. It stays the default until other threads have used the beta4 one; both run the same listserver and world.

### Real client or invented?

Everything changed today copies a real reply or a behaviour a real client was seen to accept: the gen-5 two-frame reply is the public server's, the plain reply is the one real 2.05 accepted in the 10-21 captures, the tags are what 2.22 draws as tabs. Two things are deliberately lab-only and differ from the public service: our listserver answers a plain login on 14922 (the public one does not, but real 2.17.1 sends exactly that), and it accepts any account unless an account file is given.
