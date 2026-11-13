# The gserver's unknown ids: what the clients do with them

Date: 2026-11-06

Covers the ids that the open-source gserver and gs2lib leave as `UNKNOWN`: client → server
(PLI) 25 and 162, and server → client (PLO) 60, 81, 83, 104, 108, 109, 110, 124, 132, 133,
168, 181, 193 and 194. (132 and 133 were added on 2026-11-12, issue #254.) Every game client in the version chain (1.21 to 6.03r7) was checked, and so
was every staff client in the materials, from the 1999 GServer2 RCs to RC3 and the
standalone NPC Control.

Tags: **[bin]** read from a client binary · **[cap]** seen on the wire in a lab capture ·
**[srv]** only the gserver or gs2lib source says it · **[inf]** inferred.

Confidence: **high** = handler read in at least one binary and the meaning follows from it ·
**medium** = layout read, purpose inferred · **low** = gserver comment only · **none** =
nothing in the materials.

Field notation as in `packet-ids.md`: `c` = GCHAR (byte + 32), `s` = GSHORT (two 7-bit
groups + 32), `i5` = GINT5 (five 7-bit groups, high first, each + 32), `str` = a `c` length
and then that many bytes.

The disassembly excerpts behind this note stay in the project's handoff files, not here.

## Summary

| Id | Proposed name | Layout | Clients that handle it | Confidence |
|---|---|---|---|---|
| PLI 25 | `PLI_WEAPONUPLOAD` | as `PLO_NPCWEAPONADD`: name, image, script | sent by 1.21 to 1.37 | high |
| PLI 162 | `PLI_PING` (6.11 slot `onSendPingAnswer`) | game clients: `!` + `s value`; RC3: empty | 4.20r6, 4.20r8 and 6.x send it as the answer to PLO 108; RC3 sends it empty every 60 s | high |
| PLO 60 | — | — | no client, staff clients included | none |
| PLO 81 | — | — | no client, staff clients included | none |
| PLO 83 | — | — | no client, staff clients included | none |
| PLO 104 | `PLO_FILEKEY` (or `PLO_PACKAGEKEY`) | `str file`, `c a`, `i5 lo`, `i5 hi` | 3.153 to 6.03r7 | high (DES key); `a` partly known |
| PLO 108 | `PLO_PING` | `c sub`, `s value` | 4.20r6, 4.20r8, 6.01r1, 6.03r7 (before the main switch); not 5.00r7 to 5.31r4 | high (sub 0, seen on the wire with 6.03r7); none (what reads the sub 1 value) |
| PLO 109 | `PLO_DOWNLOADURL` (file redirect) | `i5 time`, `str localname`, `str url` | 5.24r4 to 6.03r7 | high (layout); medium (role of the first string) |
| PLO 110 | — | — | no client, staff clients included | none |
| PLO 124 | `PLO_RC_PLAYERFLAGS` (from RC3's own log text) | not read | RC3 only: logs "received player flags" | medium (name); none (payload) |
| PLO 132 | `PLO_WEAPONBYTECODE` (GServer-v2 beta4 name) | `str name`, rest = compiled weapon script | 3.153 to 5.12; not 5.24r4 or later | high |
| PLO 133 | `PLO_CLASSBYTECODE` (GServer-v2 beta4 name) | `str name`, rest = compiled class script | 3.153 to 5.12; not 5.24r4 or later | high |
| PLO 168 | `PLO_LOGGEDIN` | empty | 2.05 to 6.03r7 | high (what it does); medium (what the flag means) |
| PLO 181 | "no peer UDP to this player" (GServer-v2 beta4 name `PLO_PLAYERNOUDP`) | `s player id`, `c toggle` | 2.17 to 5.24r4 | high (layout); medium (meaning) |
| PLO 193 | `PLO_WEAPONCRC` | `i5 crc32`, rest = weapon name | 4.04r2 to 5.12 | high |
| PLO 194 | `PLO_CLEARWEAPONS` (already named) | empty | 4.04r2 to 6.03r7 | high |

## Upstream names (added 2026-11-11)

On 2026-11-11 the project moved to upstream gs2lib's packet names. The code repos (the Seihai gs2lib, gserver forks and the Rust servers) use the upstream name now; the names proposed above are kept as written and stay searchable. Only the label changes: no finding in this note does.

| Id | Proposed here | Upstream gs2lib name (used now) |
|---|---|---|
| PLI 25 | `PLI_WEAPONUPLOAD` | `PLI_TOWEAPON` |
| PLI 162 | `PLI_PING` | `PLI_PONG` |
| PLO 104 | `PLO_FILEKEY` | `PLO_FILEDECRYPTKEY` |
| PLO 108 | `PLO_PING` | `PLO_PING` |
| PLO 109 | `PLO_DOWNLOADURL` | `PLO_HTTPDOWNLOAD` |
| PLO 124 | `PLO_RC_PLAYERFLAGS` | `PLO_RC_UNKNOWN124` |
| PLO 132 | — | `PLO_UNKNOWN132` (GServer-v2 beta4 and pyReborn: `PLO_WEAPONBYTECODE`) |
| PLO 133 | — | `PLO_UNKNOWN133` (GServer-v2 beta4 and pyReborn: `PLO_CLASSBYTECODE`) |
| PLO 181 | — | `PLO_UNKNOWN181` (GServer-v2 beta4 and pyReborn: `PLO_PLAYERNOUDP`) |
| PLO 168 | `PLO_LOGGEDIN` | `PLO_ONLINEMODE` |
| PLO 193 | `PLO_WEAPONCRC` | `PLO_WEAPONHASH` |
| PLO 194 | `PLO_CLEARWEAPONS` | `PLO_RESETCLIENT` |

## Where the gserver's comments were wrong

| Id | gserver / gs2lib comment | What the clients show |
|---|---|---|
| PLO 60 | none; our tables said "client 5.07+ ignores it" | no client of any age handles it. In the 1.33-era RC, 60 was the RC's own **outgoing** "edit player: Apply" (later `PLI_RC_PLAYERPROPSSET`), never something it received **[bin]** |
| PLO 81 | "probably NC related" | not an NC id: neither the NC socket of RC3 nor the standalone NPC Control (`NCL15031`) has a case for it. The player prop 81 is unrelated and only shares the number **[bin]** |
| PLO 104 | `{GSTRING data}` holding `{GCHAR a}{GINT5 x1}{GINT5 x2}` | the leading string is the **file name**; the 8-byte value is a DES key for an encrypted package (`formats/gpak.md`) **[bin]** |
| PLO 109 | `{GINT5 modTime}{GSTRING url}` | one string short: a local name comes before the URL **[bin]** |
| PLO 124 | "RC3 receives this, only hint I seen was regarding receiving player flags" | right, and that is all there is: RC3 prints `received player flags` and reads nothing from the body **[bin]** |
| PLI 162 | "Blank packet, sent by RC3 beta" | right for RC3, but it is also the game clients' answer to PLO 108. Both are one ping / keepalive message **[bin]** |
| PLO 193 | `{GINT5 ?}{?}` | the `i5` is a zlib CRC32 of the cached weapon script, not a mod time **[bin]** |

## Staff clients checked

| Build | Login tokens | RC ids handled | NC ids handled | 60, 81, 83, 110 | 124 | 104, 181 |
|---|---|---|---|---|---|---|
| GServer2 RC, 1.33 era | `GSERV014` | 50–59 only | — | no | no | no |
| GServer2 RC 2000/8/19 (also shipped as "Graal v1.39 - RC") | `GSERV019` | 8 13 16 35 37 55–59 61 70–74 | — | no | no | no |
| GServer2 RC 2000/10/25 | `GSERV020` | as 2000/8/19 | — | no | no | no |
| GServer2 RC 2001/01/27 | `GSERV021` | 8 13 16 35 37 55–59 61 70 72–74 | — | no | no | no |
| GServer2 RC 2001/08/20 and 2002/01/04 | `GSERV022` | 8 13 16 35 37 55–59 61–64 70 72–74 | — | no | no | no |
| GServer2 RC 2002/05/02 ("rc141") | `GSERV023`, `NCL11012` | 8 13 16 30 35 37 55–59 61–70 72–74 76 77 79 180 | not traced | no | no | no |
| Graal Remote Control 2004/01/17 (Delphi; three copies, one a 2005 community mod) | `GSERV024`, `NCL11012` | 8 13 16 30 35 37 55–59 61–70 72–74 76 77 79 103 180 | 16 33 80 157–164 167 188 | no | no | no |
| NPC Control (standalone, Delphi) | `NCL15031` | — | 16 33 61 74 157–164 167 | no | no | no |
| Remote Control Linux 2005/01/24 (i386, GCC 2.96, GTK2; UPX 1.90, unpacked 2026-11-13) | `GSERV024`, `NCL11012` | 8 13 16 30 35 37 47 55 56 58 59 61–70 72–74 76 77 79 100 102 103 180 | 16 33 74 80 100 157–164 167 188 | no | no | no |
| Remote Control 2006/12/20, `RC2_2.05.exe` (MSVC) | `GSERV025`, `NCL21075` | as 2010 (`rc-list-online.md`) | 16 33 74 80 100 157–164 167 188 192 | NC: no | NC: no | NC: no |
| Remote Control 2010/03/29, Linux x86-64 (GCC 4.4.1) | `GSERV025`, `NCL21075` | 8 13 16 30 35 37 47 55 56 58 59 61–70 72–77 79 82 100 102 103 180 190 | 16 33 74 80 100 157–164 167 188 192 | no | no | no |
| RC3 `RemoteControl3.exe` (MinGW, file date 2015) | `GSERV025` | the 2010 set **plus 124** | as 2010 | no | **yes** (log line only) | no |

The Linux i386 RC from January 2005 (build string "Remote Control Linux 2005/01/24") was unpacked on 2026-11-13 and read statically. **[bin]** Its UPX 1.90 checksums all verify, and a byte-exact unpack (NRV2E blocks plus UPX filter 0x49) succeeds. The earlier "damaged header" reading was wrong: the stock unpacker probably refused it over a version mismatch, which was not checked. It handles none of 60, 81, 83, 110 or 124, and has no "received player flags" text. Next to the 2010 build it lacks RC ids 57, 75, 82 and 190. Limit: its two parsers were identified by their switch ranges and where they sit, not by tracing the call that subtracts 32. A later 2005 build and a 2006 build were not read. The RC-side switch of `RC2_2.05.exe` was located later and
matches the 2010 set (`rc-list-online.md`). So 124 first appears in RC3, after the 2010 build. Both the 2010 build and
RC3 send an empty 162 from a timer. Lineage of the older builds: `tools/remotecontrol-lineage.md`,
`tools/npc-control.md`.

## Per id

### PLI 25: weapon upload (1.21 to 1.37)

- **[bin][cap]** 1.21 to 1.37 upload every weapon they hold with id 25, in the same layout as
  `PLO_NPCWEAPONADD` (name, image, the full script text). 1.38 drops 25 and sends 33
  `PLI_WEAPONADD` (`chr(0)` + default-weapon id) instead, and the server answers default
  weapons with 43 `PLO_DEFAULTWEAPON`. No 2.x to 6.x client sends 25.
- **[cap]** 1.33 against GServer-v2 beta4 was kicked with "Unknown Player Packet: 25". A proxy
  that dropped 25 let it play (beta4 then warned about the packet count).
- The Seihai GPL fork (`seihai-gserver-v2`) already maps it to `msgPLI_WEAPONUPLOAD`, which
  accepts it and stores nothing.
- See also `client-internals/versions-133-139.md`, `client-internals/version-profiles/v133-v139.toml`.
- **Confidence:** high.

### PLI 162 and PLO 108: ping

- **PLO 108 layout [bin]:** at least 3 bytes: `c sub`, then `s value`.
  - `sub` 0: the client answers PLI 162 with `!` + `s min(value, 0x6FFF)`.
  - `sub` 1: the client stores `value` on the connection object. Nothing that reads it back
    was traced. It may be a ping interval or a timeout.
  - **2026-11-12 re-check (Windows 6.03r7) [bin]:** the pre-switch test sends 100 and 108 to
    their own handlers there too. Sub 0 answers 162 with the value as above; sub 1 only
    stores it in one field of the connection object. In the connection's own code the field
    is written three times (cleared when the object is set up and on reset, and by this
    handler) and never read. A reader elsewhere that goes through a pointer to the
    connection cannot be ruled out from a static scan, so this stays open. The beta4
    gserver's comment ("type 1 is stored") says no more. **[bin][srv]**
- **Game clients [bin]:** 4.20r6 (Mac), 4.20r8 (Windows), 6.01r1 and 6.03r7 (Linux) send 162
  **only** from their 108 handler. The handler is the same in 4.20r8 and 6.03r7. 5.00r7 to
  5.31r4 neither handle 108 nor send 162; it came back in 6.x. 6.11's named send slots
  include `onSendPingAnswer` (slot 55, `v6x-clients.md`).
- **Where 108 is handled [bin]:** in 4.20r6, 4.20r8, 6.01r1 and 6.03r7, ids 100 and 108 are
  taken **before** the main switch (100 sets the raw-data length, 108 goes to the ping
  handler). The 6.x PLO lists in `v6x-clients.md` left both out because they were read
  from the switch alone; they are added there now.
- **RC3 [bin]:** the RC's ping check sends 162 with an **empty** body once every 60 s (also
  from its main timer). RC3 has no 108 handler. The 2010 Linux RC does the same.
- **So:** one message, a ping or keepalive. Game clients send it as an answer that echoes the
  server's value; RCs send it blank on a timer. The gserver stub that accepts it and does
  nothing is correct for RCs. A server can measure a game client's round trip by sending
  `{108}{c 0}{s seq}` and timing the matching 162.
- **[cap] (2026-11-13):** the unmodified Linux 6.03r7 client, against seihai-gserver `main` (commit `9063b53`) on loopback in a sealed network namespace, answered all 30 of 30 `{108}{c 0}{s seq}` with 162 `!` + `s seq`, echoing each value. Median round trip 3 ms. Capture `t1-sub0` (owner-held). This is the first wire evidence of the 108 → 162 exchange. A sub-1 probe was started but produced no valid run (the lab server sent sub 0), so the sub-1 value's use is still open.
- **6.11 [lab] (2026-11-13):** the live 6.111 connector script maps wire 108 to an ordinary native slot (94) and sends ping answers on wire 162 from send slot 55. 6.11 takes 108 through the script-loaded table, not ahead of the main switch (`v611-id-tables.md`). What sub 1 does there was not traced.
- **Confidence:** high (layout and reply, for game clients and RC3); medium that it is a ping
  (supported by the 6.11 slot name). This settles manual App. E#5.

### PLO 104: per-file DES key for encrypted packages

- **Layout [bin]:** body over 8 bytes: `str filename`, `c a`, `i5 lo`, `i5 hi`. `lo` and
  `hi` are joined little-endian into 8 bytes. Same parse in 4.20r8 and 6.03r7. This is the
  gserver's `{GCHAR a}{GINT5 x1}{GINT5 x2}` once the leading `str filename` is counted.
- **Where it goes [bin] (4.20r8):** into a hash table keyed by the lower-cased file name
  (with extension, without path). When the client creates a file resource whose extension is
  `.gpake` (or `.enc`), it is marked encrypted and attaches the record for its name. An
  encrypted resource can't be loaded until its record is switched on, and the handlers of
  PLO 45, 69 and 102 switch it on for that file name. On load, the bytes are DES-ECB
  decrypted with the record's 8 bytes (libtomcrypt `des_setup` with an 8-byte key). That DES
  reads each key byte bit-reversed, as in 2.05 (`client-internals/saved-passwords.md`).
- **[lab]** The real 6.03r7 client loaded an encrypted package keyed this way and refused a
  wrong key (`formats/gpak.md`).
- 6.03r7 keeps the same table, links it from the file layer, and also stores a timestamp in
  the record.
- **`a` [bin]:** in 6.03r7 a loose `.enc` file decrypts only when `a` is 1. Packages don't
  check it, and 4.20r8 doesn't check it anywhere. Other values are not understood.
- **Handled by:** 3.153 (Mac) onward, every 4.x, 5.x and 6.x build. Not 3.04 and not 2.x.
  RC3 and NPC Control have no 104 handler (staff clients don't load packages).
- The package format, the order a server must send things in, and the client test results
  are in `formats/gpak.md`.
- **Confidence:** high that it is the DES key for an encrypted package. Open: the full
  meaning of `a`, and which server feature sent it.

### PLO 109: download a file from a URL (5.24 and later)

- **Layout [bin] (6.03r7):** `i5 time`, `str A`, `str B`.
- **[bin]** B is parsed as a URL (`http://` or `https://`, then host and path). The client
  finds or creates an HTTP connection object named `HTTP_<host>_<port>_<path>` and starts
  the fetch. It marks the download, stores A and the time, and tells the file manager. So B
  is the URL, A is the file name it is stored under (or redirected from), and the time is
  the mod time. This fits 6.11's native `setfileredirect(u,s,s)`.
- **Handled by:** 5.24r4 to 6.03r7. Not 5.12 or older.
- **Confidence:** high (layout, and that B is fetched over HTTP); medium (what A is used for).

### PLO 168: "logged in" flag

- **[bin]** No payload is read. 2.05 to 2.31 call a local-player routine with flag 1. 4.20r8,
  Mac 4.20r6 and 6.03r7 each set one byte on their player object. Every client from 2.05 on
  handles it.
- **[srv]** The gserver sends it right after the login burst ("This seems to inform the
  client that they have logged in"; "Login server sends this").
- **[cap]** Empty 168 then 194 from GServer-v2 to 5.x and to 4.04r2 in our lab logs. Those
  came from the lab server, so they show the gserver's habit, not a real server's.
- **Confidence:** high (empty, sets a one-shot flag); medium (that the flag means "login done").

### PLO 181: no peer-to-peer UDP to this player

- **Layout [bin]:** at least 3 bytes: `s player id`, `c toggle`. The client looks up the
  player and sets a bool to `toggle > 0` (4.20r8 and Mac 4.20r6 alike).
- **Handled by:** 2.17 to 5.24r4. Dropped in 5.30r3.
- **Reader [bin] (Windows 4.04r2, read 2026-11-12):** the flag has exactly one reader. It sits
  in the routine that collects the players near the local player (within 16 units on each
  axis, the level's players or, on a gmap, the players of the neighbouring boards). A
  player with the 181 flag set is left out of that list, as are players with either of two
  neighbouring flags whose writers were not traced. The only user of the list is the
  peer-to-peer UDP send: it runs only when the client's own UDP socket is open, and it sends
  the message to each listed player directly (`udp-p2p.md`). So a set flag means "do not
  send peer-to-peer UDP to this player"; the server's copy still goes over TCP.
- **[srv]** This matches the name GServer-v2's beta4 branch gives the id, `PLO_PLAYERNOUDP`
  (as quoted by pyReborn, `client-internals/pyreborn-study/`). A server would send it for a
  player whose UDP port is unusable (behind NAT, or `noudp` set), so that peers stop
  sending datagrams that never arrive.
- **Open:** which of the three neighbouring flags the server sets for which reason; no
  capture of a real server sending 181.
- **Confidence:** high (layout, and that it removes the player from peer UDP sends);
  medium (why a server sends it).

### PLO 132 and 133: compiled weapon and class scripts (3.153 to 5.12)

Read 2026-11-12 (issue #254). The handlers were found through the receive switch's jump
table in Windows 4.04r2 and 5.12 and compared with the 3.153 Mac handlers.

- **Layout [bin]:** both are `str name` (a `c` length and that many bytes), then the rest of
  the packet is the compiled script. The body must be at least the name length + 1 bytes or
  the packet is dropped. This is the `{GCHAR name_len}{name}{bytecode}` that GServer-v2's
  beta4 branch sends (`Weapon.cpp` and `ScriptClass.cpp` there, as cited by pyReborn).
- **132, weapon [bin]:**
  - Raises the client's script level to at least 3, as 193 does.
  - Looks the weapon up by exact name in the local player's weapon list. If the player does
    not hold that weapon, the packet does nothing. So the server must send the weapon
    itself first (`PLO_NPCWEAPONADD`, 33).
  - In 4.04r2 it writes the bytes to the weapon cache, `<user folder>weblevels/weapons/<name>.code`
    (the file 193 checks by CRC later), then installs them as the weapon's script and
    restarts it.
  - It marks the weapon when the current server's name starts with `login` (the `Login`
    server of 4.x), the same test the client uses to keep Login-server update packages
    apart. **[bin][inf: that the tested name is the server name]**
  - It is skipped while a client state flag is set (not identified).
- **133, class [bin]:**
  - No script-level change.
  - Adds the name to the client's list of class names if it is new, finds or creates the
    class object of that name, and loads the bytecode into it. The loader reads the
    class's function table and marks functions whose names start with `public.` as callable
    from outside. The class object holds a `joinedclasses` variable, which is what
    `v3x-clients.md` saw.
  - A body that is only the name gives an empty class. The beta4 gserver sends exactly
    that for a class it doesn't have.
- **Handled by:** 3.153 (Mac), 4.04r2, 4.20r6, 4.20r8, 5.00r7 and 5.12. **Not** 5.24r4 or
  later: 5.24r4's switch has no case for either, together with 193. From 5.24 on, compiled
  scripts arrive through 197 `PLO_LOADSCRIPT` and the `GRESCR01` cache
  (`formats/gwebl001-cache.md`). The earlier line "6.x drops both" is right but late: the
  drop is at 5.24.
- **Not read:** the 5.00r7 handlers themselves (its switch lists both ids; the 4.04r2 and
  5.12 handlers on either side agree), and whether 3.153 also writes the `.code` file.
- **Confidence:** high (layout, what each does, and the build range).

### PLO 193: weapon script by CRC from the local cache

- **Layout [bin] (4.20r8):** body over 5 bytes: `i5 crc`, then the rest is a weapon name.
  The client raises the script level to at least 3 and finds the weapon by name. It builds
  `<user folder>weblevels/weapons/<name>.code`, and if the file exists it computes a zlib
  `crc32` over its content. If that equals `crc`, it loads the cached script. Otherwise it
  asks for the weapon with PLI 158 (`PLI_UPDATESCRIPT`), or the `getweapon` script call.
- **So:** "you hold weapon X, and its current script has CRC Y; use your cache if it
  matches." The earlier "mod time, then CRC" reading in `v4x-clients.md` is corrected.
- **Handled by:** 4.04r2 to 5.12 (5.00r7 routes it the same way). Dropped in 5.24r4, where
  197 `PLO_LOADSCRIPT` with the `GRESCR01` cache takes over (`formats/gwebl001-cache.md`).
- **Confidence:** high.

### PLO 194: clear weapons

- **[bin]** 4.20r8 clears its weapon and class script lists and their name index. 5.00r7
  clears every loaded level and the level caches. 6.03r7 resets state on its main game
  object, deletes the objects in two global lists (probably weapons and classes), and
  empties two more containers.
- **Handled by:** 4.04r2 to 6.03r7.
- **[srv][cap]** The gserver sends it empty before the weapon list, and also to RCs
  (`rc-capture-2026-11-04.md`: 25, 194, 74, …). Again the lab server's own habit.
- **Confidence:** high. How much it clears differs by version.

### PLO 124: "received player flags" (RC3 only)

- **[bin]** Neither the 2004 Delphi RC nor the 2010 Linux RC has a 124 case, so it is new in
  RC3. RC3's RC parser has a case that writes `received player flags` to stdout (a debug
  line) and reads nothing from the payload. No game client from 1.21 to 6.03r7 handles 124.
- **Open:** the layout. RC3 throws the body away. Most likely it carries the flags of a player
  the RC asked about, but nothing in RC3 asks for them.
- **Confidence:** medium (purpose, from the client's own text); none (layout).

### PLO 60, 81, 83, 110: not resolved

- **Game clients [bin]:** none of the 26 builds in the version chain (1.21 to 6.03r7) has a
  case for any of the four. The live 6.11 connector script maps 110 to the one empty native slot, so 6.11 ignores it
  too, and it clears 60, 81 and 83 (`v611-id-tables.md`) **[lab]**. Checked directly in the dispatchers of 4.20r8, Mac 4.20r6 and
  Linux 6.03r7, and in the handled-id sets of every other build
  (`client-internals/decomp-findings-2026-10-24-c/plo_handled_ids_by_build.tsv`,
  `client-internals/version-profiles/`).
- **Staff clients [bin]:** none of the builds in the table above. RC3's RC parser handles 8,
  13, 16, 30, 35, 37, 47, 55, 56, 58, 59, 61–70, 72–77, 79, 82, 100, 102, 103, 124, 180 and
  190, so 60 sits between 59 and 61 with no case. Its NC parser checks 16, 33, 74, 80, 100,
  157–164, 167, 188 and 192. Its serverlist parser checks only 1, 2 and 4. The standalone
  NPC Control's one receive dispatcher handles 16, 33, 61 (`PLO_RC_SERVERFLAGSGET`; it has a
  "Server flags" window), 74 and 157–164, 167.
- **Per id:**
  - **60:** client → server "edit player: Apply" in the 1.33 RC (later
    `PLI_RC_PLAYERPROPSSET`), so an old server → RC reply on 60 is plausible. Unverified.
  - **81:** the player prop 81 is a different thing that shares the number.
  - **83:** the gserver's player-prop table also has a prop `UNKNOWN83`. That is the prop,
    not this packet.
  - **110:** falls between 109 and 111, which 6.03 handles; 6.03 has no 110 case.
- **[cap]** none of the four appears in any project capture.
- **Confidence:** none for meaning; high that no client in the materials handles them. Most
  likely they were never used, or used only between servers.
- **Settles it:** only a capture from a real (non-lab) server that sends one.

## What to change downstream

Superseded for names on 2026-11-11: see "Upstream names" above.

- **gs2lib / gserver names (GPL fork only):** 25 → `PLI_WEAPONUPLOAD` (the Seihai fork already
  does this), 162 → `PLI_PING`, 108 → `PLO_PING`, 124 → `PLO_RC_PLAYERFLAGS`,
  104 → `PLO_FILEKEY`, 109 → `PLO_DOWNLOADURL`, 193 → `PLO_WEAPONCRC`, 168 → `PLO_LOGGEDIN`.
- **This repo:** done in the same change as this note: `packet-ids.md`, `v4x-clients.md`
  (193), `v6x-clients.md` (100 and 108 before the switch, 162, 109), and the manual's
  §2.4.9, §2.5 tables and App. E#5.
- **Seihai client (clean-room, from its own docs):** 108 can be answered with 162 for the 4.20
  and 6.x profiles. 104 matters only if encrypted packages are ever served.
