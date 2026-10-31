# Lab servers: our gserver and listserver

Date: 2026-10-30. These are the two servers the offline lab runs (see `../lab-setup.md`). The prebuilt packs live in the project files at `seihai-lab/servers/`: `seihai-lab-servers.tar.gz` (GServer master `efb5b90`) and `seihai-lab-servers-beta4.tar.gz` (GServer beta4 with our patch); this folder versions the parts we wrote ourselves.

| File | What it is |
|---|---|
| `listserver.py` | Our lab listserver, version 2 (2026-10-30). Python 3, standard library only. |
| `test_listserver.py` | Drives a running listserver with every login shape and a fake gserver. Exit 0 when all checks pass. |
| `run-lab.sh` | Starts the listserver and the prebuilt GServer on loopback; `stop` stops both. |
| `gs2lib-GNW03081.patch` | The one-line gs2lib change our efb5b90 gserver build carries (2.05 token in the 2.1 slot). |
| `gserver-beta4-lab.patch` | Our fixes to GServer-v2 beta4 `365bbd2`: three for real 2.05 and 2.17.1, one for a saved hidden state, three for 1.33 to 1.39 (apply in `server/`). |
| `gs2lib-CLVER_5_24.patch` | Adds 5.24 (`G3D15010`) to gs2lib as its own slot, `CLVER_5_24`, between 5.12 and 5.31x. Against gs2lib `5c36ab8` (what beta4 fetches). |
| `gs2lib-CLVER_5_24-b839106.patch` | The same change against gs2lib `b839106` (our efb5b90 build). Applies with or without `gs2lib-GNW03081.patch`. |
| `test_clver_5_24.cpp` | Checks the token → id → name lookups and the order 5.12 < 5.24 < 5.31x < 6.015 against a built gs2lib. |
| `clver-5-24-lab/` | The 2026-10-31 lab run of real 5.24r4 on stock and patched gs2lib: screenshots, client consoles, proxy lines for the file messages. |
| `run-lab-beta4.sh` | The beta4 pack's start script: listserver, the 2.x server on 14802 and the classic server on 14803. |

Background on what each server is, and how they compare with GServer-v2 beta4 and the other open-source servers, is in `../../server-notes/lab-servers-2026-10-30.md`.

## Our gserver

GServer-v2 **master at `efb5b90` (2025-01-07)**, built without the V8 NPC server and without UPnP, linked against gs2lib `b839106` with `gs2lib-GNW03081.patch`. The binary reports itself as `3.0.9-beta`. It is not beta4: the beta4 branch is 807 commits ahead of it.

The patch puts `GNW03081` (2.05) in gs2lib's 2.1 slot. Real 2.05 needs it on this build: in a pre-2.1 slot this build's pre-2.1 level sequence never sends `PLO_SETACTIVELEVEL` (156), and 2.05 waits on the loading screen for it. The patch drops 2.1's own token `GNW31101`, so a real 2.1 client cannot log in to this build; `lib-stock/` has the unpatched library.

## Our beta4 gserver (2026-10-30)

GServer-v2 **beta4 `365bbd2`**, built here with GCC 14 (no V8, no UPnP), with beta4's own gs2lib `5c36ab8` unpatched. It reports `4.0.0-beta`. beta4 knows 2.05r2 (`GNW03081`) natively as `CLVER_2_052`, so 2.1 keeps its token. Stock beta4 refuses 2.05 and 2.17 at login because its `allowedversions.txt` only accepts 1.41r1 and 2.22 to 2.31; the pack widens that in config. With the versions accepted, beta4 still did not get real gen-3 clients into the game, and none of the causes is reachable from config (the player class comes from the login type byte). `gserver-beta4-lab.patch` fixes three things for them, plus one account-save fix:

1. **Login bundle remainder.** 2.05 and 2.17 send the login line and `PLI_LANGUAGE` in one frame. beta4's `parseLoginPacket` dropped the rest of that frame, so the gen-3 decrypt iterator ran one step behind for the whole session: 2.17.1 failed with "Invalid PlayerProp" and 2.05 never sent valid packets. The patch keeps the remainder and hands it to the new player.
2. **`PLO_SETACTIVELEVEL` (156)** is now sent to Original clients from 2.01 up, before the NPCs. 2.05 waits for it on the loading screen.
3. **`PLO_LEVELNAME` before the board** on the first load, as efb5b90 and the live-trace stub send it. After the board, 2.05 stays on the loading screen.

All three copy a packet order real 2.05 was already seen to accept; none adds behaviour.

4. **Never log in hidden.** The account loader clears the hidden bit (`STATUS` 0x02). From the v4 lab: a client that closed while hiding under a carried object was saved hidden and came back invisible until its first step. Not reproducible with 2.17.1, which sends its own status at login (an account saved with `STATUS 22` loads visible on both builds and is saved back as 20). Build steps are in the pack's `README.md`.

### 1.33 to 1.39 on beta4 (2026-10-30)

beta4's `generation` is server-wide and 1.x clients need `classic`, so the beta4 pack runs a second server folder, `servers/classic` ("Lab Classic", port 14803), beside the 2.x one. 1.33 to 1.39 have no listserver; they connect straight to `127.0.0.1:14803` ("One Player Online"). Starting from the `../../client-internals/versions-133-139.md` live check, four more problems turned up:

5. **Id 25 kicked 1.33 to 1.37** (their weapon upload). Code: accepted and ignored; the weapon stays on the client.
6. **Prop 10 sent as a gani.** Code: a classic server sends the bow form.
7. **Kicked after about 30 s, all of 1.33 to 1.39.** beta4 took "packet count is 0" to mean "the next frame is a login", and `PLI_PACKETCOUNT` (31) resets the count. These clients send a lone id 31 every 10 s, so the next frame was parsed as a login and counted as invalid; the third one kicked them. Code: a login-done flag. This fits #119's "invalid packet count" warning and also covers any 2.x client that sends 31 alone.
8. **Zero max hearts.** Stock `(defaultaccount).txt` has `MAXHP 3.00`, which the loader reads as 0, on both servers. Config: `MAXHP 3`. The classic folder's default account also uses `head0.gif`, `sword1.gif` and `shield1.gif`, since the stock world has no images and these clients carry them only as `.gif`, and turns off the 2.x `-gr_movement` helper weapon.

Real clients: 1.33, 1.34, 1.35, 1.36, 1.37, 1.38 and 1.39 log in, show the right player and HUD, walk, and stay connected (no kicks or unknown packets); 2.05r2, 2.17.1 and 2.22 rechecked on the 2.x server. Under Wine these clients need `nodirectinput=true` in `graalconfig.txt` for keyboard input, and often start on their own pause menu (Continue/End), which P closes.

## 5.24 in gs2lib's version table (2026-10-31)

Stock gs2lib has no entry for `G3D15010` (5.24r3, 5.24r4, and 6.00 beta2, which sends the same token). GServer then gives 5.24 `CLVER_UNKNOWN` (0) and serves it every pre-2.1 file path, so the client saves PNG data as a file name and never gets files over 64000 bytes (`../../protocol/file-transfer.md`). Until now the lab got around this by renaming another build's table entry to `G3D15010`, which took that build off the table.

`gs2lib-CLVER_5_24.patch` gives 5.24 its own slot instead. It adds three lines: `CLVER_5_24` in the enum (`include/IUtil.h`), and `G3D15010` / `"5.24"` in `clientVersions[]` and `clientVersionString[]` (`src/IUtil.cpp`), all right after 5.12. The array index is the version id, so the enum and both arrays move together.

**Version ranges.** Every later id goes up by one, and 5.24 sorts between 5.12 and 5.31x. Every test above 2.31 in GServer efb5b90 and beta4 `365bbd2` compares against `CLVER_4_0211`, `CLVER_5_07`, `CLVER_5_12` or `CLVER_6_015`, so 5.24 takes the same branch in each as 5.30/5.31 do, and no other build changes branch. beta4's stock `allowedversions.txt` has `modern = G3D14097:G3D0511C` (5.12 to 6.037), compared by id, so 5.24 is now inside the stock modern range. Before the patch it was id 0 and outside it. A side effect of the stock check (`PlayerClient.cpp`, about line 396): a single entry that gs2lib does not know, such as a bare `G3D15010`, also resolves to 0, so it lets in every client whose token is unknown, not only 5.24. **[src]**

**Rebuild GServer too.** The `CLVER_*` constants are compiled into GServer, so a new `libgs2lib.so` under an old `gs2emu` shifts every comparison above 5.12 by one. For example, the old binary would treat 5.31x as 6.015. Always rebuild both together. For beta4 that happens anyway, because gs2lib is linked in statically.

**Build and checks.**

    # efb5b90 (the lab pack): gs2lib b839106 + this patch (+ gs2lib-GNW03081.patch if 2.05 is wanted)
    git -C dependencies/gs2lib apply gs2lib-CLVER_5_24-b839106.patch
    cmake .. -DTESTS=OFF -DUPNP=OFF -DV8NPCSERVER=OFF -DSTATIC=OFF -DCMAKE_BUILD_TYPE=Release && make -j8
    # beta4: apply gs2lib-CLVER_5_24.patch to the fetched gs2lib 5c36ab8 before building
    g++ -std=c++23 -I<gs2lib>/include test_clver_5_24.cpp <gs2lib>/lib/libgs2lib.a -lz -lbz2 && ./a.out   # prints OK

Both gs2lib versions built, and `test_clver_5_24.cpp` printed OK on both. On `b839106` the program needs the `CLVER_WORLDS` line swapped for `CLVER_IPHONE_BELOTE_1_5`, because that version has no Worlds entry.

**Lab run (real 5.24r4, GServer efb5b90, Wine 9.0, loopback-only namespace).** This used the same server config twice, with `G3D15010` allowed and the S→C 178 warp from `v5x/lab/rules.py`. The only difference was the library and the binary. **[cap]**

| | stock gs2lib `b839106`, prebuilt gs2emu | `b839106` + `gs2lib-CLVER_5_24-b839106.patch`, rebuilt gs2emu |
|---|---|---|
| `PLO_FILE` for `sword1.png` | `\x86*sword1.png‰PNG…` (no modtime) | `\x86&w6u\x84*sword1.png‰PNG…` (GINT5 modtime) |
| client console | `File download: 1.png‰PNG`, then `Couldn't open …/downloads/1.png‰png` | `File download: sword1.png (size: 7143) done`, same for `sprites.png`, `body.png`, `head0.png`, `shield1.png`, `idle.gani` |
| `pics1.png` (216,002 B) | S→C 30 `FILESENDFAILED` (over 64000 B for a "pre-2.14" client) | 68 `LARGEFILESTART`, 84 size, seven 32000-B chunks, 69 `LARGEFILEEND`, "done" |
| screen after the warp | black: no tiles, no player | level drawn, player drawn with the downloaded head, body, sword and shield |

Every file the patched run saved is byte-identical to the server's copy. Files under `clver-5-24-lab/`.

Not covered: 6.00 beta2 (same token, so it gets the 5.24 slot; not run) and 6.00 beta1 (`G3D03048`, still unknown to gs2lib). The beta4 build with the master patch was compiled and unit-checked but not run against a client.

## Our listserver (version 2)

```sh
python3 listserver.py [LOGFILE] [--accounts FILE] [--name TEXT] [--host 127.0.0.1]
```

Ports: 14900 for gservers, 14921, 14922 and 14923 for clients. Every client port accepts every login shape; the shape is read from the first message, not from the port.

| Client sends | Clients | Reply |
|---|---|---|
| id 0 list name only, plain zlib (shape A) | 2.00, 2.05 | id 0 list, id 2 status, one plain zlib frame |
| id 0 + id 1 account/password, plain zlib (shape B) | 2.17.1 | the same, once |
| id 4 key + token, then bz2 frames (gen 4) | 2.19 to 2.21 | id 0 + id 2 in one gen-4 frame |
| id 7 key + token + list name, then gen-5 frames (shape C) | 2.22, 2.31 | two zlib (ctype 4) frames: id 0 list, then id 2 status + id 3 site URL + id 5 upgrade URL |
| id 5 key + token (RC list) | RC | as shape C, every server |
| a refused account (with `--accounts`) | any | id 4 with the error text, then the link closes |

The gen-5 reply follows the public listserver's 14922 reply (`../../protocol/public-listserver-2026-10-25.md`), except that we do not add the two trailing NUL bytes the public server leaves after the last line.

Server names carry the list tag only for gen-4/gen-5 clients, from the gserver's `SERVERHQLEVEL`: 0 `U ` (hidden), 1 `H ` (bronze, the GServer default), 2 none (classic), 3 `P ` (gold), 4 `3 `. Classic clients always get the bare name, as on the public 14923 list.

Gserver side: `REGISTERV3`, `NEWSERVER`, `SERVERHQLEVEL`, `SETPLYR`/`PLYRADD`/`PLYRREM` (the players column is live), `VERIACC2` (answered `SUCCESS`, or the account error with `--accounts`), `SETIP` (beta4's 60-second keep-alive), `SENDTEXT` (logged), `PING` (a pong in GServer's naming; never answered). A gserver's row is dropped when its link closes.

### What changed from the stub of 2026-10-22

The stub shipped in the lab pack (`listserver.py`, 119 lines) differed from the one that made the 2026-10-21 captures:

1. **No gen-5 login.** It handled id 4 (gen 4) but not id 7, so real 2.22/2.31 and Seihai's 2.22/2.31 profiles got no list: Seihai reported "the listserver sent no reply within 5 s". Fixed.
2. Shape B got the list twice (once for id 0, once for id 1). Fixed: once, after the account.
3. Rows were never removed, so a stopped gserver stayed listed. Fixed.
4. The players column was always 0. Fixed (PLYRADD/PLYRREM).
5. It answered gserver id 16 with id 99. Id 16 from GServer is a pong, and 99 is the listserver's ping, so a beta4 gserver would answer with another 16. GServer efb5b90 never sends 16 on its own, so this never looped in practice. Removed.
6. No RC (id 5) list, no account check, no site/upgrade URLs. Added.

## Tests run (2026-10-30)

* `test_listserver.py` against version 2: all checks pass (shapes A, B, gen 4, gen 5, RC, gserver VERIACC2, player count, row dropped on disconnect, refused password with `--bad-login`). Against the old stub: 5 failures (gen 5, RC, duplicate reply, player count, stale row).
* Seihai `--list-only`, profiles 2.00, 2.05, 2.17, 2.22, 2.31: every profile lists the server with version 2. With the old stub, 2.22 and 2.31 fail.
* **Real clients under Wine** (loopback namespace, our gserver build), list then game login:
  * 2.05 rev 2: list on 14921 (shape A), in game on `onlinestartlocal.nw`.
  * 2.17.1: list on **14922** with shape B (its built-in port), "Classic" tab, in game.
  * 2.22: list on 14922 (shape C), "Bronze" tab, the two status lines, the Show More and Donations buttons; in game.

* **Real clients on patched beta4** (same namespace, listserver version 2, and again from the packed tarball for 2.17.1): 2.05 rev 2 (`GNW03081 (2.05r2)`), 2.17.1 (`GNW22122`) and 2.22 (`GNW03014`, logged as "New Client (2.22+)") each list the server, reach the game and walk; the gserver log shows no unknown or invalid packets. Unpatched beta4 with the widened `allowedversions.txt`: 2.05 stuck on loading, 2.17.1 "Invalid PlayerProp" on the first step. beta4 has no legacy port or old-client option (one listener, `serverport`); `generation = classic` makes 2.17.1 fail at login instead.
* `test_listserver.py` expects to be the only gserver on the listserver. Run it with GServer stopped; with GServer connected the row and tag checks fail because GServer's row comes first.

## Notes for the other threads

* A v5/v6 client logs in to a gserver named "Login" on port 14900, which here is the listserver's gserver port. To use our gserver as that login server, move the listserver's gserver port (the `14900` in `main()` and `listport` in `serveroptions.txt`) and set GServer's `serverport=14900`.
* GServer knows `G3D22067` (5.07), `G3D14097` (5.12) and `G3D26090` (5.31x), not `G3D15010` (5.24); add unknown tokens to `config/allowedversions.txt`.
* `xtjoeytx/glauncher` redirects the official v4+ client by hooking `gethostbyname` and `connect`: `license.graal` line 1 is the host for `loginserver.graalonline.com`, line 2 the port that replaces 14900, line 3 the host for `Graalonline.com`, lines 6 and 7 `loginserver2`/`loginserver3`. In the lab a hosts file does the same job without a DLL.
