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
- The 2.05 list host and port are not in the string table as plain text. They are DES-hidden and decode to `www.graalonline.com`, port `14921`. 2.05 sends only id 0 `newmain` on that link. **[2.05]** The captures show later listservers on ports 14922/14923 (`GNW30123` login, `GNW07080` guest). **[cap]**

`GNW30123` (seen on 14922) is the 2.22/2.31 listserver token. Both clients send listserver id 7 as `c key` + `GNW30123` + `newmain`, then switch to gen 5 and send id 1 with the account and password. It is a listserver protocol token, not a game build, so the game-version tables do not list it. **[bin]** (See `client-versions.md`.)

### 2.17+ list host **[bin]**
From 2.17 the list host and port are not built in. They are read from `arrays2.dat` (line 0 host, line 1 port, lines 5 and 6 fallback hosts), which must match the signature in `arrays2.sig`. 2.17 still logs in pre-2.2 style (id 0 `newmain`, then id 1) with no cipher.

## Game server ↔ listserver (summary) **[srv]**

Server → list (`SVO_*`, 0–31): set name, description, language, version, url, ip, port, player count; verify account (`VERIACC2`) and guild; get/set profile; player add/remove; ping; file get (v3); serverHQ password and level; request list, server info, and buddies; PM a player; register v3; send text.

List → server (`SVI_*`): verify-account results (`VERIACC2` 11), guild verification, file start/data/end (v3 15–17), profile, error message, server info, request/send text (19/20), PM player (29), assign PC id (30), ping (99), rawdata (100).

Only needed if Seihai ever hosts its own listserver. The client only needs ids 0–5 above.
