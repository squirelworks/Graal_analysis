<!-- manual: kind=reference status=draft -->
# 6 Listserver

The listserver gives a client the list of game servers and, from 2.22, checks its account. Two links exist: client ↔ listserver (§6.1 to §6.4) and game server ↔ listserver (§6.5) [srv] (protocol/listserver.md#listserver-protocol). Framing and ciphers are in → §2.1 and → §2.2. From 4.x the first connection goes to a game server named `Login` instead (→ §2.3.5).

> Status: draft. Real-client captures exist for 2.00, 2.05, 2.17.1, 2.22 and 2.31 against a lab listserver only; the public-service runs used a reimplementation's frames. No 2000–2002 listserver binary or capture exists.

## 6.1 Requests

### 6.1.1 Where each build looks for the list

Each build finds its server list in its own way. The table gives the host and port each group of builds uses, and the list name it asks for [bin] (protocol/login-frames-by-version-2026-10-25.md#real-versus-seihai-per-profile-seihai-main-21a37a5).

| Builds | Host and port | List name | Source |
| --- | --- | --- | --- |
| 1.33 to 1.39 | no listserver; the player types a game-server address | n/a | [bin] (protocol/login-frames-by-version-2026-10-25.md#real-versus-seihai-per-profile-seihai-main-21a37a5); [lab] (tools/lab-servers/README.md#133-to-139-on-beta4-2026-10-30) |
| 1.41 | only a patched copy survives (`<list-host-reborn>`:14923) | none sent: the client connects and waits for the list | [bin] (protocol/listserver.md#141-rev1-no-login-the-server-speaks-first-binlab); [bin] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes) |
| 1.42 | `<listserver-host>` built in, port 14921 | `newmain` | [bin] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes) |
| 2.00 to 2.05 | built in as a DES-hidden string assembled one character at a time, port 14921; `arrays2.dat` is not read | `newmain` | [2.05] (protocol/listserver.md#205-specifics-205); [bin] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes) |
| 2.1 test builds | port 14922 built in | unmeasured | [bin] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes) |
| 2.17 to 2.31 | `arrays2.dat`, checked against `arrays2.sig`: line 0 host, line 1 port (14922), lines 5 and 6 fallback hosts, tried in order (→ §3.5) | `newmain` | [bin] (protocol/listserver.md#217-list-host-bin); [2.22][cap] (protocol/listserver.md#222-specifics-222cap) |
| RC 1.41 (2002) | a DES-hidden host to which the code appends the top-level domain, port 14922 | `rc` | [bin] (tools/npc-control.md#listserver-login-new-in-141-bin) |

The 2.22 client keeps the hosts from `arrays2.dat` in memory under a one-byte transform, so a plain memory search misses them [2.22] (protocol/listserver.md#222-specifics-222cap).

### 6.1.2 Client → listserver ids

These are the messages a client sends to the listserver. Each row gives the id, its name and its layout [srv] (protocol/listserver.md#client--listserver-1).

| Id | Name | Layout | Source |
| ---: | --- | --- | --- |
| 0 | V1VER | `rest` = list name, such as `newmain` (RC 1.41: `rc`) | [srv] (protocol/listserver.md#client--listserver-1); [bin] (tools/npc-control.md#listserver-login-new-in-141-bin) |
| 1 | SERVERLIST | `str account`, `str password` | [srv] (protocol/listserver.md#client--listserver-1) |
| 4 | V2VER | `c key` + `newmain`; selects the 2.2 bz2 mode | [srv] (protocol/listserver.md#client--listserver-1) |
| 5 | V2SERVERLISTRC | `c key` (RC) | [srv] (protocol/listserver.md#client--listserver-1) |
| 7 | V2ENCRYPTKEYCL | `c key` + `GNW30123` + `newmain` | [bin] (protocol/listserver.md#client--listserver-1) |
| 223 | GRSECURELOGIN | a Graal Reborn extension | [srv] (protocol/listserver.md#client--listserver-1) |

### 6.1.3 Login shapes

The listserver login differs by client generation, not by build; inside a generation every observed build sends the same bytes [cap] (protocol/login-frames-by-version-2026-10-25.md#short-answer).

| Shape | Builds seen with a real client | Client → listserver | Source |
| --- | --- | --- | --- |
| A: list name only | 2.00 (client side), 2.05 (port 14921) | one plain zlib frame: id 0 + `newmain` + `\n` (9 bytes decoded, 17 on the wire); no account, password, token or key; the client then closes | [cap] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes) |
| B: id 0 then id 1 | 2.17.1 (port 14922 from its signed `arrays2.dat`) | one plain zlib frame holding id 0 `newmain` and id 1 (`str account`, `str password`); no token, key or cipher | [cap] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes); [cap] (protocol/listserver.md#217-list-host-bin) |
| C: id 7, then generation 5 | 2.22, 2.31 (port 14922) | frame 1, plain zlib, 18 bytes decoded: id 7, one key byte, `GNW30123`, `newmain`, `\n`; frame 2, generation 5 with compression byte `0x02`: id 1, XORed with the key | [cap] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes) |
| D: 6.113 on port 14900 | Windows 6.113, one owner-supplied capture | not a list frame: token `GNP1905C`, then ciphertext; no id 0, 1 or 7 and no `newmain` | [cap] (protocol/v6113-list-capture.md#against-the-listserver-note) |
| E: 6.113 full capture | Windows 6.113, the full capture the same day | the same hello on TCP 14900 and on TCP 14882; still no clear list id. The hosts that answer send no UDP | [cap] (protocol/v6113-udp.md#graal-tcp) |
| none: the server speaks first | 1.41 rev1 | the client sends nothing; it reads plain zlib frames, takes id 0 (the list, then it closes) and id 1 (one more entry), and ignores the rest | [bin] (protocol/listserver.md#141-rev1-no-login-the-server-speaks-first-binlab) |
| generation 4 | 2.19 to 2.21 | id 4 `c key` + token, then bz2 frames with partial XOR (limit 4) | [srv] (protocol/listserver.md#client--listserver); [lab] (tools/lab-servers/README.md#our-listserver-version-2) |
| RC 1.41 | RC 1.41 (2002) | id 0 `rc`, then id 1 `str account`, `str password` | [bin] (tools/npc-control.md#listserver-login-new-in-141-bin) |

The rules below say which tokens go to the listserver and which go to a game server, and what the classic frames can tell about the build [bin][cap] (protocol/listserver.md#222-specifics-222cap).

| Rule | Source |
| --- | --- |
| `GNW30123` is the listserver token of 2.22 and 2.31, shared by both; it is not a game build token (2.22 logs in to a game server as `GNW03014`, 2.31 as `GNW28015`) | [bin][cap] (protocol/listserver.md#222-specifics-222cap); [cap] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes) |
| Per-build tokens such as `GNW24011` (2.00), `GNW03081` (2.05) and `GNW22122` (2.17.1) go to the game server, never to the listserver | [cap] (protocol/login-frames-by-version-2026-10-25.md#the-three-real-shapes) |
| The classic frames (A and B) carry no field that could name a build | [cap] (protocol/login-frames-by-version-2026-10-25.md#does-the-evidence-support-classic-logins-look-fake) |
| The real clients compress at zlib's best level (stream starts `78 DA`); a `78 9C` stream with the same deflate body is answered by the public service for shape C | [cap] (protocol/login-frames-by-version-2026-10-25.md#one-byte-level-difference-that-applies-to-every-seihai-frame) |
| The 2.05 list connection derives from the game connection's base class and keeps its base send path, which has no generation-3 insertion | [2.05] (protocol/listserver.md#205-specifics-205) |
| A real 2.00 sends one frame (id 0 + `newmain`), makes no second listserver connection, and accepts a 2.17-style two-frame reply from a lab forwarder | [lab] (protocol/listserver.md#205-specifics-205); [cap] (client-internals/decomp-findings-2026-10-24-b/07-lab-findings-46-186-200.md#200-listserver-handshake-client-side-observed-list-reply-synthetic); [cap] (version-profiles/lab-200-listserver-handshake.tsv) |
| After the list, 2.17 logs in to the game server as type 0 with a key, `GNW22122`, account and password, in generation 3 | [cap] (protocol/listserver.md#217-list-host-bin) |
| What 1.42, 2.01 to 2.04 and 2.1 to 2.16 send is unmeasured (1.41 rev1 sends nothing, see above); 1.42 and 2.01 to 2.04 share 2.00's built-in list data and are expected to send shape A | [inf] (protocol/login-frames-by-version-2026-10-25.md#real-versus-seihai-per-profile-seihai-main-21a37a5) |

## 6.2 Replies

### 6.2.1 Listserver → client ids

These are the listserver's replies. Each row gives the id, its name and its layout; two are disputed and point to App. E [srv][cap] (protocol/listserver.md#listserver--client).

| Id | Name | Layout | Source |
| ---: | --- | --- | --- |
| 0 | SVRLIST | `c count`, then one record per server (→ §6.4) | [srv][cap] (protocol/listserver.md#listserver--client) |
| 1 | NULL | disputed → App. E#401 | [srv] (protocol/listserver.md#listserver--client); [bin] (tools/npc-control.md#listserver-login-new-in-141-bin) |
| 2 | STATUS | disputed → App. E#401 | [srv] (protocol/listserver.md#listserver--client); [bin] (tools/npc-control.md#listserver-login-new-in-141-bin) |
| 3 | SITEURL | URL | [srv] (protocol/listserver.md#listserver--client) |
| 4 | ERROR | text; the connection closes | [srv] (protocol/listserver.md#listserver--client); [bin] (tools/npc-control.md#listserver-login-new-in-141-bin) |
| 5 | UPGURL | donate or upgrade URL | [srv] (protocol/listserver.md#listserver--client) |

The rules below give how 2.05 handles those replies and fills its server window [2.05] (protocol/listserver.md#205-specifics-205).

| Rule | Builds | Source |
| --- | --- | --- |
| The receive handler switches on ids 0 and 1 only | 2.05 | [2.05] (protocol/listserver.md#205-specifics-205); [2.05] (client-internals/client-architecture-205.md#networking-classes) |
| A client fills the list as soon as id 0 arrives after its id 0 `newmain`; it does not wait for id 1, and closes the socket about 2 s after it gets the list | 2.05 | [cap] (protocol/listserver.md#205-specifics-205) |
| The window shows the fields in record order: name, language, description, URL, version, players, address, port | 2.05 | [cap] (protocol/listserver.md#205-specifics-205) |
| The list client acts on ids 0 and 1 only; any other id, including 2, 3 and 5, is ignored | 2.00 | [bin] (client-internals/v2.00-connect-path.md#list-reply-bin) |
| Id 1 carries one server record in the id 0 record layout and appends it to the list; when it is then the only row, it is selected | 2.00 | [bin] (client-internals/v2.00-connect-path.md#list-reply-bin) |
| After id 0 the client fills the list and closes the list socket; a row is drawn only with at least 6 fields, and the detail view needs at least 8 | 2.00 | [bin] (client-internals/v2.00-connect-path.md#list-reply-bin) |
| RC 1.41 reads 0 (server list), 1 (one more server entry), 2 (end, disconnect) and 4 (error text, disconnect), and shows name and player count | RC 1.41 | [bin] (tools/npc-control.md#listserver-login-new-in-141-bin) |
| The 2004 RC logs in with client id 5, an empty token and an empty list name, then `str account`, `str password`; it shows name and player count from an id 0 list, and id 4 text in a message box | RC 2004 | [cap] (protocol/rc-capture-2026-11-04.md#rc-list-from-the-listserver) |
| 2.22 shows the status lines and the Show More and Donations buttons, and files tagged servers under tabs (→ §6.4) | 2.22 | [lab] (tools/lab-servers/README.md#tests-run-2026-10-30) |

### 6.2.2 Reply frames seen

Replies were captured from three kinds of login. Each row gives one login shape and the frames that came back [cap] (protocol/listserver.md#217-list-host-bin).

| Login | Reply | Source |
| --- | --- | --- |
| shape B from a real 2.17, lab listserver | two plain zlib frames: id 0 (the list); then id 2 status, id 3 site URL, id 5 donation URL | [cap] (protocol/listserver.md#217-list-host-bin) |
| shape C, port 14922 of the public service | two generation-5 frames with compression byte `0x04` (zlib): id 0 list; then id 2 status, id 3 site URL, id 5 upgrade URL | [cap] (protocol/public-listserver-2026-10-25.md#what-the-runs-settle) |
| shape C, port 14923 of the public service | three generation-5 frames: the legacy list first, sent straight after the id 7 frame before the client's id 1, then the two frames above | [cap] (protocol/public-listserver-2026-10-25.md#what-the-runs-settle) |
| classic (shape B frame), port 14923 of the public service | one plain zlib frame, id 0 only, no status, site or upgrade lines, no trailing NUL bytes; the server then waits | [cap] (protocol/public-listserver-2026-10-25.md#what-the-runs-settle) |

The table gives details of those reply frames that a decoder must match: trailing bytes, the status frame and its count [cap] (protocol/public-listserver-2026-10-25.md#frame-and-field-layout-derived).

| Detail | Value | Source |
| --- | --- | --- |
| trailing bytes | generation-5 frames end with two `0x00` bytes after the last `\n`; the plain legacy frame does not | [cap] (protocol/public-listserver-2026-10-25.md#frame-and-field-layout-derived) |
| status frame | id 2 text of two lines joined by CR (a welcome line and "N server(s) online"), id 3 site URL, id 5 upgrade URL, `\n` after each | [cap] (protocol/public-listserver-2026-10-25.md#frame-and-field-layout-derived) |
| status count | the number in the status text is the server's own text and need not match the row count | [cap] (protocol/public-listserver-2026-10-25.md#what-the-runs-settle) |
| timing, port 14922 | both frames about 0.4 s after the client's second frame, on a link with a 0.2 s round trip | [cap] (protocol/public-listserver-2026-10-25.md#timing-users-link-round-trip-about-02-s) |
| timing, port 14923, shape C | the legacy list within a few ms of the handshake; the two current frames about 0.35 s after the client's id 1 | [cap] (protocol/public-listserver-2026-10-25.md#timing-users-link-round-trip-about-02-s) |
| timing, port 14923, classic | about 0.2 s after the login | [cap] (protocol/public-listserver-2026-10-25.md#timing-users-link-round-trip-about-02-s) |

### 6.2.3 The classic `serverlist3` listserver

The classic `serverlist3` listserver survives as source. The rules below give its ports, framing and how it filters the list [bin] (tools/classic-tools/serverlist3.md#start-and-config).

| Rule | Source |
| --- | --- |
| One process with two listen ports, one for clients and one for game servers, set by `clientsport` and `serversport` in a `key=value` config; also `playerlimit`, `databaseserver` and `showmore` | [bin] (tools/classic-tools/serverlist3.md#start-and-config) |
| Frame: `u16be` length + zlib; lines start with `id + 32`; strings are `count + 32` and the bytes; an inflated buffer past 16383 bytes or an outgoing buffer past 4095 bytes counts as a broken link | [bin] (tools/classic-tools/serverlist3.md#frame) |
| Client id 0 is the edition text, which filters the directory to rows whose edition contains it and that were written in the last 10 minutes; id 1 is account and password; other ids are ignored; there is no key, token or cipher | [bin] (tools/classic-tools/serverlist3.md#what-a-client-sends) |
| Passwords are checked locally against a `crypt` hash of the first 8 characters with a two-character salt | [bin] (tools/classic-tools/serverlist3.md#what-a-client-sends) |
| A hard failure (unknown account, wrong password, ban) is id 4 with the text, then the link closes | [bin] (tools/classic-tools/serverlist3.md#what-the-client-is-shown) |
| A success is id 0 (the directory) and id 2 (status text), then the link closes; the trial and free-server texts also send id 3 first with the `showmore` URL | [bin] (tools/classic-tools/serverlist3.md#what-the-client-is-shown) |
| Status texts: a welcome line, a staff sentence, a remaining-time sentence, the trial sentence or the free-server sentence | [bin] (tools/classic-tools/serverlist3.md#what-the-client-is-shown) |

## 6.3 Login-type matrix

On 2026-10-25 the public listserver was asked for its list 38 times, once per port for 19 version profiles of a reimplementation, with no game-server login [cap] (protocol/listserver-login-type-matrix-2026-10-25.md). The service chooses its reply by **login type**, not by version or token [cap] (protocol/listserver-login-type-matrix-2026-10-25.md#result).

| Login sent | Profiles | Port 14922 | Port 14923 | Source |
| --- | --- | --- | --- | --- |
| classic: one plain zlib frame with id 0 `newmain` and id 1 | 1.41, 1.42, 2.00, 2.01, 2.02, 2.02 rev 2, 2.03, 2.04, 2.1, 2.12 to 2.17 | connection accepted, no reply and no close for the 5 s timeout, in all 15 | legacy list in all 15: one plain zlib id 0 frame, 2 or 4 rows | [cap] (protocol/listserver-login-type-matrix-2026-10-25.tsv); [cap] (protocol/listserver-login-type-matrix-2026-10-25.md#result) |
| generation 5: id 7 + `GNW30123` + `newmain`, then id 1 | 2.22, 2.3, 2.31, and the 2.05 profile of the run | modern list (8 rows) with status, site and upgrade lines | the legacy list first, then the modern list (12 or 17 rows in all) with the status lines | [cap] (protocol/listserver-login-type-matrix-2026-10-25.tsv); [cap] (protocol/listserver-login-type-matrix-2026-10-25.md#result) |
| any | 2.05 profile | port 14921: connection refused at once | n/a | [cap] (protocol/public-listserver-2026-10-25.tsv); [cap] (protocol/public-listserver-2026-10-25.md#what-the-runs-settle) |

The public service was tested with each login type. The rules below say which port gives a list and what varied between runs [cap] (protocol/listserver-login-type-matrix-2026-10-25.md#result).

| Rule | Source |
| --- | --- |
| A port that gets a list: a classic login on 14923; a generation-5 login on 14922 (14923 also answers it) | [cap] (protocol/listserver-login-type-matrix-2026-10-25.md#result) |
| The legacy list's row count varied between runs (2 or 4) with no link to the version; the 2-row form carried `P ` and `H ` prefixes and the 4-row form none | [cap] (protocol/listserver-login-type-matrix-2026-10-25.md#result); [cap] (protocol/login-frames-by-version-2026-10-25.md#what-the-matrix-shows-public-service-seihai-only) |
| The 2.05 rows of the matrix are a generation-5 login, not a classic 2.05 login; a classic 2.05 login was not run | [cap] (protocol/login-frames-by-version-2026-10-25.md#problem-in-the-matrix-data-the-205-rows-are-not-a-classic-205-login) |
| No real client of these versions was captured against the public service; the runs say which login type the service answers on which port, not what a real 1.41 to 2.17 client sends | [cap] (protocol/listserver-login-type-matrix-2026-10-25.md#what-this-does-not-show) |
| The 2001-era server tools list clients on 14922 and older clients on 14923 (`clientPortOld`) | [src] (tools/server-tools-2001.md#gs2emu-serverlist-thedgtl-snapshot-de66a3f) |

Why the public 14922 ignores a classic login, and what it does with a real 2.17.1, is open (→ App. E#403). Whether the 14923 legacy list is a real 2000-era reply is disputed (→ App. E#402).

## 6.4 Server-list records

Each server in the list is one record of eight fields. The table gives each field's content in order [cap] (protocol/public-listserver-2026-10-25.md#frame-and-field-layout-derived).

| Field | Content | Source |
| ---: | --- | --- |
| — | each record starts with `c` field count, 8 in every capture | [cap] (protocol/public-listserver-2026-10-25.md#frame-and-field-layout-derived) |
| 1 | type prefix and name | [srv][cap] (protocol/listserver.md#listserver--client) |
| 2 | language | [srv][cap] (protocol/listserver.md#listserver--client) |
| 3 | description | [srv][cap] (protocol/listserver.md#listserver--client) |
| 4 | URL | [srv][cap] (protocol/listserver.md#listserver--client) |
| 5 | version text | [srv][cap] (protocol/listserver.md#listserver--client) |
| 6 | player count, as text | [srv][cap] (protocol/listserver.md#listserver--client) |
| 7 | address, as text | [srv][cap] (protocol/listserver.md#listserver--client) |
| 8 | port, as text | [srv][cap] (protocol/listserver.md#listserver--client) |

Every field is a `str` [cap] (protocol/public-listserver-2026-10-25.md#frame-and-field-layout-derived). The list body ends with `\n` after the last record [cap] (protocol/public-listserver-2026-10-25.md#frame-and-field-layout-derived).

| Type prefix | Tier or tab | HQ level in the lab listserver | Source |
| --- | --- | ---: | --- |
| `U ` | hidden | 0 | [srv] (protocol/listserver.md#listserver--client); [lab] (tools/lab-servers/README.md#our-listserver-version-2) |
| `H ` | bronze (hosted) | 1 | [srv] (protocol/listserver.md#listserver--client); [lab] (tools/lab-servers/README.md#our-listserver-version-2) |
| none | silver, shown as "Classic" by 2.17.1 | 2 | [srv] (protocol/listserver.md#listserver--client); [lab] (tools/lab-servers/README.md#tests-run-2026-10-30) |
| `P ` | gold | 3 | [srv] (protocol/listserver.md#listserver--client); [lab] (tools/lab-servers/README.md#our-listserver-version-2) |
| `3 ` | 3D | 4 | [srv] (protocol/listserver.md#listserver--client); [lab] (tools/lab-servers/README.md#our-listserver-version-2) |

The rules below give how prefixes appear, how a client uses a record to connect and one asset check that blocks it [srv] (protocol/listserver.md#listserver--client).

| Rule | Source |
| --- | --- |
| Pre-2.2 clients get no prefix for bronze | [srv] (protocol/listserver.md#listserver--client) |
| Connect needs a selected record with at least 8 fields and takes the address and port from fields 7 and 8; with either empty it shows "The connection could not be established!" without dialling (2.00) | [bin] (client-internals/v2.00-connect-path.md#connect-bin) |
| A missing core asset (`objects.dat`, `arrays.dat` or one of the main images) sets a fatal flag at Start that is never cleared; the server list still works, but Connect then returns before creating the player, leaving a grey game window with no socket (2.00) | [bin] (client-internals/v2.00-connect-path.md#the-fatal-flag); [cap] (client-internals/v2.00-connect-path.md#lab-rule-for-200) |
| The public 14923 legacy list sent untagged rows in its 4-row form; 3 of 4 rows also appear in the current list with the same address, port and version text | [cap] (protocol/public-listserver-2026-10-25.md#frame-and-field-layout-derived) |
| A 2003 fan listserver sets the `P ` prefix for a server marked `Favorite=Yes`, so the client files it under Gold | [bin] (tools/server-tools-2001.md#win32-listserver-by-rick-2003--contains-a-password-stealer-bin) |
| Field bytes are passed through as sent: a captured address field had lost its leading characters, and a name carried three literal `0x3F` bytes | [cap] (protocol/public-listserver-2026-10-25.md#what-the-runs-settle) |

## 6.5 Game server link

Game servers talk to the listserver over a separate link. The rules below give its framing, port and opening lines [src] (server-notes/03-protocol.md#protocol).

| Rule | Source |
| --- | --- |
| Listserver packets on this link have no length prefix: `id + payload + \n` | [src] (server-notes/03-protocol.md#protocol) |
| Game servers register on port 14900 in the Reborn listserver | [src] (tools/server-tools-2001.md#gs2emu-serverlist-thedgtl-snapshot-de66a3f) |
| A GServer-v2 opens with a plain `REGISTERV3` line, then zlib frames: `NEWSERVER`, `SERVERHQPASS` / `SERVERHQLEVEL`, `SETPLYR` and `PLYRADD` per player, `VERIACC2` per login, and `SENDTEXT` with its allowed versions; the older master never pings | [src] (server-notes/lab-servers-2026-10-30.md#what-our-gserver-does-with-each-client-generation-src) |
| The newer GServer-v2 sends `SETIP` every 60 s as a keep-alive, and its `VERIACC2` carries a `s` identity length | [src] (server-notes/lab-servers-2026-10-30.md#2-gserver-v2-beta4-against-our-build) |
| Id 16 from a GServer-v2 is a pong and 99 is the listserver's ping | [src] (tools/lab-servers/README.md#what-changed-from-the-stub-of-2026-10-22) |

The table gives the ids on that link, in each direction [src] (server-notes/03-protocol.md#listserver-ids).

| Direction | Id | Name | Source |
| --- | ---: | --- | --- |
| server → list | 0 | SETNAME | [src] (server-notes/03-protocol.md#listserver-ids) |
| server → list | 7 | SETPLYR | [src] (server-notes/03-protocol.md#listserver-ids) |
| server → list | 14 | PLYRADD | [src] (server-notes/03-protocol.md#listserver-ids) |
| server → list | 15 | PLYRREM | [src] (server-notes/03-protocol.md#listserver-ids) |
| server → list | 16 | PING | [src] (server-notes/03-protocol.md#listserver-ids) |
| server → list | 17 | VERIACC2 | [src] (server-notes/03-protocol.md#listserver-ids) |
| server → list | 22 | NEWSERVER | [src] (server-notes/03-protocol.md#listserver-ids) |
| server → list | 23 | SERVERHQPASS | [src] (server-notes/03-protocol.md#listserver-ids) |
| server → list | 24 | SERVERHQLEVEL | [src] (server-notes/03-protocol.md#listserver-ids) |
| list → server | 8 | ERRMSG | [src] (server-notes/03-protocol.md#listserver-ids) |
| list → server | 11 | VERIACC2 | [src] (server-notes/03-protocol.md#listserver-ids) |
| list → server | 15 to 17 | FILESTART3, FILEDATA3, FILEEND3 | [src] (server-notes/03-protocol.md#listserver-ids) |
| list → server | 19, 20 | request and send text | [srv] (protocol/listserver.md#game-server--listserver-summary-srv) |
| list → server | 29 | PM player | [srv] (protocol/listserver.md#game-server--listserver-summary-srv) |
| list → server | 30 | assign PC id | [srv] (protocol/listserver.md#game-server--listserver-summary-srv) |
| list → server | 99 | PING | [src] (server-notes/03-protocol.md#listserver-ids) |
| list → server | 100 | RAWDATA | [src] (server-notes/03-protocol.md#listserver-ids) |

The other server-to-list ids (0 to 31) set description, language, version, URL, address, port and player count, verify guilds, get and set profiles, request files, the list, server info and buddies, and PM a player [srv] (protocol/listserver.md#game-server--listserver-summary-srv). No open listserver serves files to a game server [src] (server-notes/lab-servers-2026-10-30.md#3-listservers).

| Classic `serverlist3` game-server link | Source |
| --- | --- |
| The first line is the login: kind 0 or 1, then `GLSER001` or `GLSER002`, then the world name; the socket address must match the address stored for that world | [bin] (tools/classic-tools/serverlist3.md#what-a-game-server-sends) |
| Id 4: player add or update (2-byte id, a flag byte, `c` length, name); with flag bit 1 set and kind 0 the listserver answers id 7 with the player id and, when queued, "N ghost(s) before you" | [bin] (tools/classic-tools/serverlist3.md#what-a-game-server-sends) |
| Id 5: player leave (2-byte id) | [bin] (tools/classic-tools/serverlist3.md#what-a-game-server-sends) |
| The public directory is a database table, not built from these messages; the link carries presence, the ghost queue and the address check | [bin] (tools/classic-tools/serverlist3.md#what-a-game-server-sends) |

The Reborn listserver keeps its data in tables. The rows below give what it stores and how it hashes passwords [src] (tools/server-tools-2001.md#gs2emu-serverlist-thedgtl-snapshot-de66a3f).

| Reborn listserver data | Source |
| --- | --- |
| Tables for users (account, password, salt, activation, ban, profile fields), servers (name, address, port, players, description, URL, language, a two-character type, version, uptime), per-server HQ password and level, IP bans, guilds and guild members | [src] (tools/server-tools-2001.md#gs2emu-serverlist-thedgtl-snapshot-de66a3f) |
| Account passwords are `md5(md5(password) + salt)` with a three-character salt | [src] (tools/server-tools-2001.md#gs2emu-serverlist-thedgtl-snapshot-de66a3f) |

### 6.5.1 PC ids (`VERIACC2` and `ASSIGNPCID`)

A PC id is a number the listserver hands to a game server for each login. Neither the game server nor the client computes it [src][bin][inf] (protocol/pcid.md#pcid-where-the-pc-id-comes-from).

| Rule | Source |
| --- | --- |
| GServer-v2 added PC-id support on 2022-09-04; its login parser keeps everything after the password as one identity string, logs it, and takes only the first token (`win`, `mac`, `linux`) as the player's OS | [src] (protocol/pcid.md#game-server-to-listserver-veriacc2-and-assignpcid) |
| The game server forwards the identity unchanged at the end of `SVO_VERIACC2` (17): account, password, player id, player type, then a two-byte length and the string | [src] (protocol/pcid.md#game-server-to-listserver-veriacc2-and-assignpcid) |
| The listserver answers `SVI_ASSIGNPCID` (30): `s player id`, `c player type`, then a `c`-length string holding the PC id in decimal, parsed with `std::stoll` into a signed 64-bit id; a non-numeric string would throw | [src][inf] (protocol/pcid.md#game-server-to-listserver-veriacc2-and-assignpcid) |
| GServer-v2 drops 30 for a player who is already loaded, so the listserver must send it before the `VERIACC2` reply | [src][inf] (protocol/pcid.md#game-server-to-listserver-veriacc2-and-assignpcid) |
| The PC id lives in memory only, and is 0 for a player the listserver gave none | [src] (protocol/pcid.md#game-server-to-listserver-veriacc2-and-assignpcid) |
| RC `/openaccess <account>` makes GServer-v2 send `PLO_SERVERTEXT` `GraalEngine,lister,ban,<account>,<pcid>`, which opens the scripted ban window; `lister getbanhistory` and `lister getbanbyid` are answered by the listserver | [src] (protocol/pcid.md#where-the-pcid-is-used) |
| The 6.03r7 Login session's server-list weapon asks `getlockcomputer`; what it compares was not seen | [cap][inf] (protocol/pcid.md#where-the-pcid-is-used) |
| The 1.25 and 1.27 GServers and RemoteControl 1.33 to 2.01 have no machine id; their ban window bans an account | [bin] (protocol/pcid.md#where-the-pcid-is-used) |
| How the official listserver derives the number (lookup table or hash, which fields) is not in any binary or source held; an MD5 is 128 bits and the id is 64-bit decimal, so it is not one of the sent digests → App. E#406 | [src][inf] (protocol/pcid.md#can-a-pcid-be-derived-from-the-login-fields) |
