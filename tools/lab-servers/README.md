# Lab servers: our gserver and listserver

Date: 2026-10-30. These are the two servers the offline lab runs (see `../lab-setup.md`). The prebuilt pack lives in the project files at `seihai-lab/servers/seihai-lab-servers.tar.gz`; this folder versions the parts we wrote ourselves.

| File | What it is |
|---|---|
| `listserver.py` | Our lab listserver, version 2 (2026-10-30). Python 3, standard library only. |
| `test_listserver.py` | Drives a running listserver with every login shape and a fake gserver. Exit 0 when all checks pass. |
| `run-lab.sh` | Starts the listserver and the prebuilt GServer on loopback; `stop` stops both. |
| `gs2lib-GNW03081.patch` | The one-line gs2lib change our gserver build carries (2.05 token in the 2.1 slot). |

Background on what each server is, and how they compare with GServer-v2 beta4 and the other open-source servers, is in `../../server-notes/lab-servers-2026-10-30.md`.

## Our gserver

GServer-v2 **master at `efb5b90` (2025-01-07)**, built without the V8 NPC server and without UPnP, linked against gs2lib `b839106` with `gs2lib-GNW03081.patch`. The binary reports itself as `3.0.9-beta`. It is not beta4: the beta4 branch is 807 commits ahead of it.

The patch puts `GNW03081` (2.05) in gs2lib's 2.1 slot. Real 2.05 needs it on this build: in a pre-2.1 slot this build's pre-2.1 level sequence never sends `PLO_SETACTIVELEVEL` (156), and 2.05 waits on the loading screen for it. The patch drops 2.1's own token `GNW31101`, so a real 2.1 client cannot log in to this build; `lib-stock/` has the unpatched library.

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

## Notes for the other threads

* A v5/v6 client logs in to a gserver named "Login" on port 14900, which here is the listserver's gserver port. To use our gserver as that login server, move the listserver's gserver port (the `14900` in `main()` and `listport` in `serveroptions.txt`) and set GServer's `serverport=14900`.
* GServer knows `G3D22067` (5.07), `G3D14097` (5.12) and `G3D26090` (5.31x), not `G3D15010` (5.24); add unknown tokens to `config/allowedversions.txt`.
* `xtjoeytx/glauncher` redirects the official v4+ client by hooking `gethostbyname` and `connect`: `license.graal` line 1 is the host for `loginserver.graalonline.com`, line 2 the port that replaces 14900, line 3 the host for `Graalonline.com`, lines 6 and 7 `loginserver2`/`loginserver3`. In the lab a hosts file does the same job without a DLL.
