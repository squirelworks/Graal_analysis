# NPC-Control protocol

Date: 2026-10-31

Wire layouts for the NPC-server (NC) socket that staff tools use. Written for
`seihai-rc` stage 5. Sources: static reads already filed as `tools/npc-control.md`
(RC 1.41 / 2002) and `tools/remotecontrol.md` (2004 Delphi `RemoteControl.exe`);
Drive inventory of Squirrel's `NC [NPC Control]` and `RC [Remote Control]`
folders (binaries and docs held outside the repo). Tags: **[bin]** static read ·
**[doc]** 2001 NPCControl text · **[srv]** gs2lib / GServer names · **[inf]**
inferred, needs a loopback check.

Raw decompiles and client binaries stay on Drive. This note has plain behaviour
only.

## Login

| Socket | First message | Framing after login |
|---|---|---|
| NC | type **3**, 8-byte token, `str account`, `str password` (no key byte) | fixed zlib frame (`u16be` length + zlib body), **no** type byte, **no** cipher, for the whole session **[bin]** |

- **Login token is build-dependent.** The standalone NPCControl tools (`nc7132001` = "GServer2 NPC Control 2001/07/13", and the 2001-05-21 build the Jan-2002 leak re-dates) send token `NCL15031`; the NC socket embedded in RC 2002/01/11 sends `NCL11012`. Both are type 3, no key byte, no junk byte after the password; the framing is identical. A loopback run of both standalone builds through `tools/probe/ncprobe.py` confirmed type 3 + `NCL15031` + `str account` + `str password` and the cipher-free zlib stream. **[lab]** This also answers "Check on loopback" item 1 below for the standalone tools.
- Message body: classic Graal text lines (`GCHAR id` + payload + `\n`), G-integers with `+0x20`. Batches flush at 0x1000 bytes. **[bin]**
- Large uploads: id 50 (`PLI_RAWDATA`) with a GINT3 length, then one raw frame; receive id 100 (`PLO_RAWDATA`) switches the reader for the next *length* bytes. **[bin]**
- The NC login did not change between RC 1.41 (2002) and the 2004 RemoteControl. The RC game-server login did (`GSERV023` type 1 → `GSERV024` type 6 / gen 5). **[bin]**
- Default NC host fields in the 2004 binary are the loopback address and `14804` (lab ports; unused leftovers once discovery works). **[bin]**

## Finding the NPC server **[bin]**

The RC does not ask the user for an NC address. It:

1. Treats any player whose nickname contains `(Server)` as an NPC-server player.
2. Sends id **94** (`PLI_NPCSERVERQUERY`): `GSHORT player id` + text `location`.
3. Handles id **79** (`PLO_NPCSERVERADDR`): `GSHORT player id`, then `ip,port`. Opens the NC socket only if that nickname still contains `(Server)` and NC is not already connected.
4. Sends the NC login above. Status: "Connected to NPC-Server".

The 2001 doc (`npccontrol.txt` in the NPCControl 1.3 bundle) says the NewWorld game server exposed NC on port **14950**, with NewWorld accounts allowed and main-server accounts needing admin level ≥ 4. **[doc]** That is the older published port; live discovery uses packet 79.

## NC → client (server ids)

Handled on the NC socket (RC 1.41). Everything else on that socket, including 16, still goes through the normal RC handler. **[bin]**

| Id | gs2lib name | Layout | UI / effect |
|---:|---|---|---|
| 16 | DISCMESSAGE | rest = text | disconnect box |
| 33 | NPCWEAPONADD | `str name`, `str image`, `GSHORT len`, `len` bytes of script | weapon script editor |
| 80 | NC_LEVELLIST | rest = level list, one per line | level list editor |
| 157 | NC_NPCATTRIBUTES | rest = attribute text, one per line | attribute viewer (view-only) |
| 158 | NC_NPCADD | `GINT3 id`, then props: `GCHAR 50` + `str name`, `GCHAR 51` + `str type`, `GCHAR 52` + `str level` (any order, any subset) | add/update NPC list row |
| 159 | NC_NPCDELETE | `GINT3 id` | remove row |
| 160 | NC_NPCSCRIPT | `GINT3 id`, rest = script | script editor |
| 161 | NC_NPCFLAGS | `GINT3 id`, rest = flags, one per line | flag editor |
| 162 | NC_CLASSGET | `str name`, rest = script | class editor |
| 163 | NC_CLASSADD | rest = class name | add to class list |
| 164 | NC_LEVELDUMP | rest = text | dump viewer (view-only) |
| 167 | NC_WEAPONLISTGET | repeated `str name` | weapon list |
| 188 | NC_CLASSDELETE | class name **[inf]** | handled in the 2004 build; not in 2002 **[bin]** |

2004 RemoteControl also lists NC receive ids 16, 33, 80, 157–164, 167, 188. **[bin]**

## Client → NC (client ids)

| Id | gs2lib name | From | Payload |
|---:|---|---|---|
| 3 | (login) | connect | see Login |
| 79 | RC_CHAT | console line typed in NC mode | text |
| 103 | NC_NPCGET | NPC list: open / attributes | `GINT3 id` |
| 104 | NC_NPCDELETE | NPC list: Delete (confirm) | `GINT3 id` |
| 105 | NC_NPCRESET | NPC list: Reset | `GINT3 id` |
| 106 | NC_NPCSCRIPTGET | NPC list: Script | `GINT3 id` |
| 107 | NC_NPCWARP | Quick warp / warp dialog | `GINT3 id`, `GCHAR x*2`, `GCHAR y*2`, level |
| 108 | NC_NPCFLAGSGET | Edit flags | `GINT3 id` |
| 109 | NC_NPCSCRIPTSET | script editor: Save | `GINT3 id`, script |
| 110 | NC_NPCFLAGSSET | flag editor: Save | `GINT3 id`, flags |
| 111 | NC_NPCADD | Add NPC dialog | comma text: name, id, type, scripter, start level, x, y. Type drop-down: `OBJECT`, `ANIMAL`, `POLICE`, `HORSE`, `BOAT`, `HOUSEC` |
| 112 | NC_CLASSEDIT | class list: open | class name |
| 113 | NC_CLASSADD | class editor: Save | `str name`, rest = script |
| 114 | NC_LOCALNPCSGET | Local NPCs dialog | level name |
| 115 | NC_WEAPONLISTGET | console button | — |
| 116 | NC_WEAPONGET | weapon list: open | weapon name |
| 117 | NC_WEAPONADD | weapon editor: Save | `str name`, `str image`, rest = script |
| 118 | NC_WEAPONDELETE | weapon list: Delete | weapon name |
| 119 | NC_CLASSDELETE | class delete | class name — **sent in 2004**; no button in 2002 **[bin]** |
| 150 | NC_LEVELLISTGET | console button | — |
| 151 | NC_LEVELLISTSET | level list editor: Save | level list |

2004 also sends NC ids 3, 79, 103–119, 150, 151. **[bin]**

Shared editor window modes map Save to 109 / 110 / 113 / 117 / 151. Attributes (157) and dumps (164) are view-only (can save as `.rtf` locally). **[bin]**

Id 111 matches the 2001 PM `add npc` field list moved onto its own packet. **[inf][doc]**

## Cross-links

- RC (game-server) staff packets and gen-5 framing: `tools/remotecontrol.md`, `tools/remotecontrol-lineage.md`.
- 2001 NPC-server PM admin channel (older than this socket): `tools/npcserver-2001.md`.
- Packet id names: `protocol/packet-ids.md`. Staff overview: `protocol/chat-pm-rc.md`.

## Drive material (inventory only; not in git)

| Item | Drive id | Role |
|---|---|---|
| Folder `NC [NPC Control]` | `1sABQxJiJ4cwbtfzrB9oqCwNhC5G3Zqsz` | NPCControl1.3 / 13 rars, `nc7132001`, NPC Server Document |
| Folder `RC [Remote Control]` | `1oF6qDwxTMoIqmHIugbx_O72m3B7_Qjih` | RC rars (rc139, rc2, Custom RemoteControl, windows_rc3_beta, …) |
| `RemoteControl.exe` | `1WAoHpifrHvM72aYXVNzkKRJVTkgJNkGH` | 2004 Delphi staff client (~1 MB) |
| `RemoteControl.exe.c` / `.html` | under `Graal Decompiles` / Accessories | decompile; read locally, never commit |
| `RC2_2.05.exe` (+ `.c`) | `1J7Ac-F42R1t8siRcveYO8Np2Il0ebbAP` | GTK RC2 line |

## Check on loopback **[inf]**

Confirm against GServer-v2 lab + Wine `RemoteControl.exe` / RC 1.41 (sandbox, the loopback address, lab ports only):

1. ~~Exact bytes of NC login (type 3 / token / account / password) and whether any junk byte follows.~~ Done for the standalone tools: type 3 + `NCL15031` + `str account` + `str password`, no key byte, no junk byte (see Login, **[lab]**). RC-2002 embedded socket (`NCL11012`) still to confirm live.
2. Packet 79 address string format (`ip,port` vs spaces) when the lab NPC-server player appears.
3. NC_NPCADD (158) property order when the server sends all three props; whether missing props clear or leave the row.
4. NC_CLASSDELETE (188 / client 119): payload is bare class name vs length-prefixed string.
5. Weapon add (33) script length: `GSHORT` vs GINT3 on large scripts; RAWDATA path for big set packets (109 / 113 / 117).
6. Local-NPC list reply id and layout after client 114 (not named in the 2002 handler table above).
7. Whether id 16 on the NC socket really shares the RC disconnect UI when the NPC-server drops the link.

## Receive-handler fuzz (first pass) **[lab]**

A first pass of malformed NC-server→client packets injected through `tools/probe/ncprobe.py`
with `tools/probe/lab/nc-core.plan`, against the standalone NPCControl tools under Wine with a
loopback NC stub as the server (it accepts the `NCL15031` login, logs ids, sends nothing; the
injected packets came from the proxy). Clients: `nc7132001` (2001/07/13) and the 2001-05-21
build (runs `nc713-a`, `nc2002-a`).

- The sweep covered receive ids 16, 33, 80, 157–164, 167, 188 with empty bodies, truncated
  GINT3 ids, `str`/`GSHORT` length-prefix over-reads (up to the 223-byte single-GCHAR max and a
  16000-byte GSHORT claim), oversized bodies and high/NUL bytes.
- **No crash in either build**: 46/46 shots stayed alive, no `CLIENT-GONE`, and no
  frame-decode-error, exception or traceback in the proxy or client logs.
- The clients did *read* the malformed packets rather than ignore them — 167 populated the
  weapon list, 164 opened the dump viewer, and the over-read weapon/name strings were drawn — so
  "alive" means the parsers tolerated the bad input, not that they skipped it.
- **Not yet fuzzed:** client→NC write ops against a server that actually parses them (gap #40,
  `nc-write-ops-status.md`).

### RC-embedded NC socket (second pass) **[lab]**

The NC socket embedded in a staff RC was then fuzzed through the RC's own discovery flow, jointly
with the RC-fuzz lab: RC logs into the game server (gen-2), the server presents the `(Server)`
player, the RC opens its NC socket, and `ncprobe.py` fronts only that NC socket (ns_ip pointed at a
third loopback) so `nc-core.plan` runs on it while the game socket is untouched.

- **Build:** the usable embedded-NC RC is the **2002/05/02** `RemoteControl.exe` (game login
  `GSERV023`, NC login `NCL11012`, both verified in strings). The archived "RC 2 (Jan 2002)" rars
  (`rc2.rar` and its duplicate, 5 copies, one md5) are the **2002/01/04** build, token `GSERV022`,
  with **no** NCL token — i.e. no embedded NC socket. So the Jan-2002 RC does not carry the NC
  client; the May-2002 build is the earliest held RC that does. **[bin][lab]**
- **Result:** the NC login was accepted (`NCL11012`, the server logging `New login: … [NC]
  [NCL11012 (1.1)]`), the server sent Control-NPC 158 + 42, and `nc-core.plan` injected 45 S→C
  packets. The RC stayed alive at all 46 shots — **no crash, no disconnect** — matching the
  standalone NPCControl result. The cipher-free NCL framing decoded and re-framed intact.
- **GServer-v2 discovery bug (server-side, [srv], cause under confirmation):** the RC's
  `PLI_NPCSERVERQUERY` (94) did **not** draw a `PLO_NPCSERVERADDR` (79) back on the lab gserver
  (gs2emu-73/76/101a) despite `serverside = true`, the NPC server loaded, `ns_ip` set, and the
  account holding `NPCCONTROL`. In the seihai-gserver-v2 source `msgPLI_NPCSERVERQUERY` only replies
  with 79 when the query body equals exactly `"location"` (else it logs "unknown"), and there is no
  send-79-at-login path — the three `sendNCLoginToPlayer` callers are this query, an RC
  server-options update, and an `NPCCONTROL` rights change. Whether the real RC's 94 body differs
  from `"location"`, or the lab gserver build diverges from that source, is still being pinned from
  the captured 94 bytes before filing. The lab worked around it by injecting 79 on the game socket
  after connect, which opened the NC socket immediately. Cross-ref: the RC-fuzz thread's rc-fuzz note.
