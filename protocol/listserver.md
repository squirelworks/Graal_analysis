# Listserver protocol

Date: 2026-10-21

Sources: graal-serverlist (xtjoeytx, 2019) `TPlayer`, `TServer`, `main.cpp`; gs2lib `IEnums.h` SVO/SVI enums; 2.05 `TServerListClient` class. Tags: **[srv]** · **[2.05]** · **[cap]** · **[inf]**.

Two separate links exist:

1. **Client ↔ listserver**: login and the server list. This is what the game client talks to.
2. **Game server ↔ listserver**: registration, account verification, and profiles (SVO_*/SVI_*). Only servers use it.

## Client ↔ listserver

Framing depends on the client generation. **[srv]**

| Gen | Detected by | Frame |
|-----|-------------|-------|
| pre-2.2 (2.05) | default | `u16be len` + zlib. No cipher |
| 2.2 | id 4 `V2VER` | `u16be len` + bz2, partial XOR (limit 4) |
| post-2.2 | id 5 or 7 | `u16be len` + compression byte + body, partial XOR |

### Client → listserver

| Id | Name | Layout |
|---:|------|--------|
| 0 | V1VER | rest = version string (e.g. `newmain`) |
| 1 | SERVERLIST | `str account`, `str password` |
| 4 | V2VER | `c key` + `newmain` (selects 2.2 bz2 mode) |
| 5 | V2SERVERLISTRC | `c key` (RC) |
| 7 | V2ENCRYPTKEYCL | `c key` + `GNW30123newmain` (2.22 and 2.31 clients) **[bin]** |
| 223 | GRSECURELOGIN | Graal Reborn extension |

### Listserver → client

| Id | Name | Layout |
|---:|------|--------|
| 0 | SVRLIST | `c count`, then per server: `c 8` (field count) and 8 GSTRINGs: `type+name`, language, description, url, version, player count, ip, port |
| 1 | NULL | — |
| 2 | STATUS | text (`\r` = line break) |
| 3 | SITEURL | url |
| 4 | ERROR | text; the connection closes |
| 5 | UPGURL | donate / upgrade url |

The `type` prefix on a server name comes from the server's HQ level: `3 ` 3D, `P ` gold, `H ` bronze (hosted), `U ` hidden, empty for silver. Pre-2.2 clients get no prefix for bronze. **[srv]**

### 2.05 specifics **[2.05]**
- `TServerListClient` derives from the same `TGraalClient` base as the game connection. It overrides only the receive handler. Its **send path is the base one, with no gen-3 insertion**, which fits a cipher-free pre-2.2 list link.
- Its receive handler switches on two ids only: 0 (server list: count followed by length-prefixed fields) and 1.
- The list host and port are not in the string table as plain text. The host is a DES-encrypted string that the server-list form builds one character at a time, together with its key. It decrypts to `www.graalonline.com`. The port is `14921`, and the first packet is id 0 with `newmain`. See `client-internals/des-and-hidden-strings.md`. **[2.05]**
- The lab run confirms the whole exchange (`tools/lab-setup.md`). **[cap]**
  1. The client sends id 0 `newmain` as soon as the list window opens.
  2. A listserver that answers with id 0 at that point fills the list. The client does not wait for id 1.
  3. The client closes the socket about two seconds after it gets the list.
  4. The field order shown in the window is name, language, description, url, version, players, ip, port, which matches the table above.
- 2.00 uses the same built-in, DES-hidden host and port as 2.05 and does not read `arrays2.dat`. In the lab a real 2.00 client sent one plain zlib frame, `GCHAR 0` + `newmain` + LF (no account or password), made no second listserver connection, and accepted a 2.17-style two-frame list reply, but that reply was synthetic (a lab-only forwarder translated the request), so what a real 2.00-era listserver sends is still unobserved and the repo's "2.05-style" list format stays unverified for 2.00 (`client-internals/decomp-findings-2026-10-24-b/07-lab-findings-46-186-200.md`) (`client-internals/decomp-findings-2026-10-24-b/04-v2.00-client.md`).
- To point a stock 2.05 at another listserver, redirect `www.graalonline.com` in the hosts file and listen on 14921. Patching the encrypted string in memory also works.
- The captures show later listservers on ports 14922/14923 (`GNW30123` login, `GNW07080` guest). **[cap]** On the public service the reply depends on the login type (matrix of 2026-10-25, `listserver-login-type-matrix-2026-10-25.md`): a classic login gets a list on 14923 and no reply on 14922; a gen-5 login gets a list on both. **[cap]**

### 2.22 specifics **[2.22][cap]**
- The host list is not built in. It comes from `arrays2.dat` in the game folder, in clear text, checked against `arrays2.sig`: line 0 `listserver.graal.in`, line 1 port `14922`, lines 5 and 6 the fallbacks `listserver.graal.cc` and `listserver.graalonline.biz`. They are tried in that order until one connects. Once loaded, the client keeps them in memory under the one-byte transform described in `client-internals/des-and-hidden-strings.md`, which is why a plain memory search misses them. The same file layout applies from 2.17 on (see `client-versions.md` and the 2.17+ section below).
- First packet: id 7 `V2ENCRYPTKEYCL` = `GCHAR key` + `GNW30123` + `newmain`. This frame is plain zlib. Every later frame in both directions is post-2.2 framing (compression byte + partial XOR) keyed with that key.
- Then id 1 `SERVERLIST` = account + password. The list reply is the same id 0 layout as for 2.05.

`GNW30123` (seen on 14922) is the 2.22/2.31 listserver token. Both clients send listserver id 7 as `c key` + `GNW30123` + `newmain`, then switch to gen 5 and send id 1 with the account and password. It is a listserver protocol token, not a game build, so the game-version tables do not list it. **[bin]** The lab confirmed this for 2.22. **[cap]** (See `client-versions.md`.)

### 2.17+ list host **[bin]**
From 2.17 the list host and port are not built in. They are read from `arrays2.dat` (line 0 host, line 1 port, lines 5 and 6 fallback hosts), which must match the signature in `arrays2.sig`. 2.17 still logs in pre-2.2 style (id 0 `newmain`, then id 1) with no cipher.

**2.17 flow, seen from a real client in the lab** **[cap]**: one TCP connection to port 14922 (host and port read from `arrays2.dat`), plain zlib framing (`u16be len` + zlib body), no gen-5, no version token. The client sends **one frame holding two messages**: `GCHAR 0` + `newmain`, then `GCHAR 1` + GSTRING account + GSTRING password. The server answers with **two plain zlib frames**: frame 1 is id 0 (the server list); frame 2 holds id 2 (status text), id 3 (site URL) and id 5 (donation URL). The client then closes the connection (FIN). Compare 2.22 and 2.31: they open with `GCHAR 7` + key + `GNW30123` + `newmain` and use gen-5 for everything after, with the same list and status ids (0, 2, 3, 5). After the list, the 2.17 game-server login is type 0, key, `GNW22122`, account, password, then gen-3 framing; the junk-byte rule in `codec-and-framing.md` decoded every 2.17 message in the capture.

## Game server ↔ listserver (summary) **[srv]**

Server → list (`SVO_*`, 0–31): set name, description, language, version, url, ip, port, player count; verify account (`VERIACC2`) and guild; get/set profile; player add/remove; ping; file get (v3); serverHQ password and level; request list, server info, and buddies; PM a player; register v3; send text.

List → server (`SVI_*`): verify-account results (`VERIACC2` 11), guild verification, file start/data/end (v3 15–17), profile, error message, server info, request/send text (19/20), PM player (29), assign PC id (30), ping (99), rawdata (100).

Only needed if Seihai ever hosts its own listserver. The client only needs ids 0–5 above.
