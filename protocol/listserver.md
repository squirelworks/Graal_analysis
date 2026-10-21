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
| 7 | V2ENCRYPTKEYCL | `c key` (2.22+ client) |
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
- To point a stock 2.05 at another listserver, redirect `www.graalonline.com` in the hosts file and listen on 14921. Patching the encrypted string in memory also works.

### 2.22 specifics **[2.22][cap]**
- The host list is three strings hidden with a one-byte transform: `listserver.graal.in`, `listserver.graal.cc` and `listserver.graalonline.biz`, all on port `14922`. They are tried in that order until one connects. They were read from a running client's memory, and the transform is described in `client-internals/des-and-hidden-strings.md`.
- First packet: id 7 `V2ENCRYPTKEYCL` = `GCHAR key` + `GNW30123` + `newmain`. This frame is plain zlib. Every later frame in both directions is post-2.2 framing (compression byte + partial XOR) keyed with that key.
- Then id 1 `SERVERLIST` = account + password. The list reply is the same id 0 layout as for 2.05.

`GNW30123` is therefore the 2.22 client's **listserver protocol token**. It is not a game build token, which is why it is missing from the gs2lib client tables. The same 2.22 binary sends `GNW03014` to the game server. **[2.22][cap]**

## Game server ↔ listserver (summary) **[srv]**

Server → list (`SVO_*`, 0–31): set name, description, language, version, url, ip, port, player count; verify account (`VERIACC2`) and guild; get/set profile; player add/remove; ping; file get (v3); serverHQ password and level; request list, server info, and buddies; PM a player; register v3; send text.

List → server (`SVI_*`): verify-account results (`VERIACC2` 11), guild verification, file start/data/end (v3 15–17), profile, error message, server info, request/send text (19/20), PM player (29), assign PC id (30), ping (99), rawdata (100).

Only needed if Seihai ever hosts its own listserver. The client only needs ids 0–5 above.
