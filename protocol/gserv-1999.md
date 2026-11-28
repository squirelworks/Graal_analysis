# GSERV-token protocol, 1.21 to 1.32 (May 1999 to January 2000)

Date: 2026-10-21

This covers the clients from 1.21 to 1.32 (1.25 and 1.27 from [`client-internals/gserv-125-127-builds.md`](../client-internals/gserv-125-127-builds.md)) and the GServer and RemoteControl builds shipped with 1.21, 1.28 beta 2 and 1.3 test.
It is the first central-server protocol: accounts, a login token, and zlib on every frame.
In the GServer-v2 numbering this is encryption generation 2, the same one 1.33 to 1.39 use with GNW tokens.
The base contracts come from static analysis; linked original-program captures add the qualified login, bootstrap and UDP observations. No decompiler output is reproduced. The [canonical earliest-network capability map](relay-1998.md#earliest-networking-capability-map) separates relay and central-server builds, run interventions and reproduction status.

## Gen 1 to gen 2 in one table

| | Gen 1 (1st Graal to 1.1.9) | Gen 2 (1.21 on) |
|---|---|---|
| Server | Lobby/relay, no game logic | GServer: accounts, levels, NPCs, flags, weapons |
| Port | 14801 local default, 14802 Cyberjoueur | 14804 (`<list-host-classic>`) for 1.21 to 1.3 test, 14900 from 1.31 |
| Framing | Text lines | `u16` big-endian length, then a zlib stream |
| Message ids | One letter (`D` plus a type letter) | `chr(id+32)` as the first byte of each line |
| Identity | Server-given 8-character id, nickname sent as data | Account and password at login |
| Levels | HTTP from the level server | Sent by the GServer |

Nothing in gen 2 is encrypted. The DES code in these clients is only used for local files (see `formats/graalsav.md`).

## Framing

Sending: messages queue in one buffer as `chr(id+32) + data + "\n"`.
On flush the whole buffer is deflated with zlib 1.0.4 and written as:

```
[len_hi][len_lo][zlib stream of len bytes]
```

There is no size threshold. Every flush is compressed.

Receiving: frames are read the same way, inflated, and split on `\n`.
Server id 100 (`chr(132)`) puts the reader into a raw mode that takes a given byte count instead of a line, for file data.
`nodecompressionerror=` in `graalconfig.txt` (from 1.27) hides the inflate error message.

## Login

The first message after `connect` is a normal id-0 line:

```
' '                    type: chr(0+32) = player. The GServer treats '!' (type 1) as RemoteControl
"GSERVnnn"             8 bytes
chr(len(account)+32) account
chr(len(password)+32) password
```

The connect dialog's defaults are `guest` / `guest`.
This is the same shape the later gen-3 login uses, minus the key byte and with GSERV instead of GNW.

| Client | Token |
|---|---|
| 1.21, RemoteControl 1.21 | `GSERV007` |
| 1.25 | `GSERV009` |
| RemoteControl shipped with 1.25 | `GSERV010` |
| 1.27 | `GSERV011` |
| RemoteControl 1.27 (shipped again as RC 1.28), RemoteControl 1.3 | `GSERV011` |
| 1.28 beta 2 | `GSERV013` |
| 1.3 test | `GSERV014` |
| 1.31 | `GSERV016` |
| 1.32 | `GSERV018` |

The tokens are a protocol revision and not a date. GNW tokens, which are dates, start with 1.33.

### What the GServers accept

From 1.27 the server compares the token against a fixed list and stores the matching number (7 to 14) on the connection. 1.25 has no stored number yet: it tests the token against a short list for each connection type.
Then it checks the minimum for the connection type.

| GServer | Accepts | Player minimum and refusal text |
|---|---|---|
| 1.21 (May 1999) | `GSERV007` | "You need Graal version 1.2 rev1 to play on this server." |
| 1.25 (Aug 1999) | `GSERV007` to `GSERV010` | no numeric minimum: a player must send exactly `GSERV007`, `GSERV008` or `GSERV009`, anything else gets the 1.21 text. RemoteControl must send `GSERV009` or `GSERV010` and is dropped without a message otherwise **[bin]** |
| 1.27 (Oct 1999) | `GSERV007` to `GSERV011` | 11: "You need at least Graal version 1.27 to play on this server." RemoteControl needs 9 or more **[bin]** |
| 1.28 (Nov 1999) | `GSERV007` to `GSERV013` | 13: "You need at least Graal version 1.28beta2 to play on this server." |
| 1.3 (Nov 1999) | `GSERV007` to `GSERV014` | 14: "You need at least Graal version 1.3 to play on this server." |

The older tokens stay on the list so that RemoteControl (GSERV011) can still log in.
Refusals and login errors ("The account has been disabled by an admin.", "The account is already in use.", "An account with the name and password you typed in doesn't exist.") go out as server id 16, which is DISCMESSAGE in the later numbering.
Captured under Wine (`client-internals/live-trace-early.md`): after a good player login GServer13 sends 9 (own props), 28 (flags, only if the account has any), 14 (warp), 100 followed by a separate frame holding 101 and the board, 6 (level name), 1 (links), 5 (signs), 39 (level modification time), 3 (NPC props with scripts), and 10. GServer 1.28 sends the same sequence without 39, which arrives with the 1.3 level cache. GServer 1.21 also sends no 39, and it packs the whole reply (9, 14, 100, 101 with the board, 6, 1, 10) into a single zlib frame. When another player is already on the level, the newcomer gets an 8 (other player's props) right after its own 9.
A token newer than the server's list is refused like an old one: GServer13 answers GSERV016 (1.31) and GSERV018 (1.32) with id 16 "You need at least Graal version 1.3 to play on this server." **[cap]**

### Client→server packet fuzz (lab)

The standalone C→S fuzzer ([`../tools/srvfuzz/`](../tools/srvfuzz/)) ran 292 gen-2 cases
(malformed framing, malformed login, the empty id sweep 0–223, and malformed bodies)
against four original GServers on a loopback lab port, one case per fresh connection with a
clean-guest-login canary after each. **No crash, hang or canary drop in any case on any
build** — GServer 1.28 beta 2 (`GSERV013`), 1.3 test (`GSERV014`), 1.25 (`GSERV009`) and
1.27 (`GSERV011`). The capped 8 MiB-inflate-ratio probe and the 500-packet in-frame flood
caused no slowdown; the 1.x servers do not inflate unboundedly. **[lab]** These add to the
capture facts above:

- **Login refusal is clean and the version-gate text is per-build**, confirmed live: wrong
  or old token → id 8 then id 16 DISCMESSAGE and close, with "You need Graal version 1.2
  rev1 to play on this server." (1.25), "…at least Graal version 1.27…" (1.27) and "…at
  least Graal version 1.3…" (1.3). Empty account+password, a 250-byte account and a
  250-byte password each draw id 16 "An account with the name and password you typed in
  doesn't exist." then close (a genuine auth failure; the built-in guest exists). **[lab]**
- **Odd login types.** Type 1 (RemoteControl) and a non-login first packet get id 8 then a
  close with no further reply; login types 2, 5, 64 and 127 leave the socket half-open with
  id 8 and no login. Short/truncated/zero tokens and account/password length-prefix overruns
  also land in the same id-8-only half-open state. **[lab]**
- **Double login.** Two valid login lines in one frame: 1.25, 1.27, 1.3 test, and **1.28
  beta 2** (re-checked 2026-11-24) all complete a normal login (login stream `9,14,100,…`).
  The earlier 1.28b2 “half-open, id 8 only” note was incomplete. Held completed sessions
  occupy ordinary player slots until the TCP close; see
  [`server-fuzz-c2s-targets.md`](server-fuzz-c2s-targets.md). **[lab]**
- **No `WANTFILE` path traversal.** Id 23 with `../`, Windows `..\`, an absolute path, an
  empty name and a 250-byte name each returned id 30 (FILESENDFAILED) with no file bytes, on
  every build. **[lab]**
- **Post-login id sweep.** After a clean login, id 23 (WANTFILE) → id 30 is the only reliable
  dedicated reply; every other client→server id with an empty body drew no dedicated reply.
  (The 1.2x servers stream the whole start level on login — id 9 props, 14 warp, 100 RAWDATA
  + board, 6 level name, 1 links, optional 5 signs, 10 ISLEADER — so a post-login reply capture
  must drain that stream first, which the fuzzer does.) Empty id 17 (BADDYADD) does **not**
  crash the server — note it crashes the 6.03r7 *client*, the opposite direction. **[lab]**
- An S→C id 8 (`OTHERPLPROPS`) on some pre-auth sockets is a **canary artifact**, not a reply
  to the malformed input. Confirmed 2026-11-24 on 1.28b2: solo frame/login with no canary
  and no other guest → no id 8; the same build under the normal canary harness → id 8 on
  every frame case (body `0x21 0x53`, player index 1). Earlier “id 8 then …” observations on
  pre-auth sockets should be read with that in mind. **[lab]**
- Sticky `NPCWEAPONADD` (id 33) on the shared `guest` account across post-login cases is
  **cumulative state**, not a per-case reply. Confirmed 2026-11-24 on 1.28b2: `idsweep`+`body`
  with a per-case restore of the pristine guest account file → no canary and no case reply
  carried id 33; empty `id-40`/`id-222` reply `none` when the account is clean. The held
  2026-11-19 cumulative `results.tsv` first shows a dirty canary after empty `id-25`.
  GServer 1.21 (`GSERV007`) has the same big level-stream login but its fuzz run is pending
  a redo on a quiet host (a loaded host produced false canary timeouts). Per-build run
  status and the full taxonomy are in
  [`server-fuzz-c2s-targets.md`](server-fuzz-c2s-targets.md). **[lab]**

## Message ids

The server-to-client numbering used through 2.x is already in place in 1.21.
The 1.21 handlers line up with the later names: 1 links (`TEditorLink`), 2 baddy props (`TComputer`), 3 NPC props (`TEditorNPC`), 4 chest, 5 sign (`TAdventureSign`), 7 board modify, 8 other player props (`TOtherClient`), 21 throw carried (`TAdventureCarry`), 22 item add (`fullheart`, `sword`, `shield`), 23 item delete (`extra.wav`).

| Client | Server-to-client ids handled |
|---|---|
| 1.21 | 0 to 34 except 30, plus 100 |
| 1.25, 1.27 | 0 to 38, plus 100 |
| 1.28 beta 2 | 0 to 38, plus 100 |
| 1.3 test | 0 to 39, plus 100 |
| 1.31 | 0 to 40, plus 100 |
| 1.32 | 0 to 41, plus 100 |

The client-to-server ids visible as constants are 0 and 10 to 26 in 1.21, and 0 and 10 to 30 in 1.32. Other sends pass the id in a register, so these lists are not complete.

The [selected 1.25/1.27 follow-up](../client-internals/gserv-125-127-builds.md#selected-receive-handlers-35-to-38) describes four normal receive branches: administrator text (35), an effect helper plus bomb sound (36), player-keyed incoming text (37), and paired numeric components (38). It records the early guards and fields without assigning recovered native enum names or transferring later layouts. Full consumers, runtime effects and the remaining ids stay open. **[bin]**

## Props by build

| | 1.21 | 1.28 b2 | 1.3 test | 1.31 | 1.32 |
|---|---|---|---|---|---|
| Player props the client parses | 0–24 | 0–31 | 0–32 | 0–32 | 0–33 |
| Player props the client sends | 0–24 | 0–24, 26, 31 | 0–24, 26, 31, 32 | same as 1.3 | 0–24, 26, 31–33 |
| NPC props | 0–17 | 0–32 | 0–34 | 0–34 | 0–34 |
| Baddy props | 0–10 | 0–10 | 0–10 | 0–10 | 0–10 |

The prop numbers grow at the end, so a decoder can use the later tables (`player-props.md`) and stop at the build's last id.
Per-build values, and the client-to-server ids, are in `client-internals/version-profiles/v121-v132.toml`.

## UDP (1.28 beta 2 on)

The 1.28 beta 2 notes call this "direct data packages", and it is the first build that links `bind`, `sendto` and `recvfrom`.
The client binds a UDP socket and sends single, uncompressed, unframed messages (anything without a `\n`) straight to another player's address and port. In 1.28 beta 2 captures, a walking client sent id 0 to the other player every 100 ms, while the server got only the changed props over TCP and forwarded nothing. Id 0 carries X, Y, SPRITE, STATUS and CARRYSPRITE (props 15 to 19; `0x1F` is −1, nothing carried), the same fields that 2.05 sends in UDP id 0. Id 12 is arrow add, with the same 5 bytes as relay `A`. One player per level sends the level NPCs' arrows to the others: the level leader, picked by the server with id 10 (`ISLEADER`, empty). The server sends 10 at the end of the first player's login reply, and to the next player when the leader leaves. **[cap]** The address and port are stored on the other player's record, so they most likely come from the server (*inferred*).
The client reports its own UDP port to the server as player prop 31 (GINT3) in its first `PLI_PLAYERPROPS`: on 1.28 beta 2 to 1.39 under Wine the value matched the bound UDP socket ([lab results](early-clients-probe-2026-11-19.md#what-the-clients-send-unprompted)). **[lab]**
The main loop reads TCP and UDP separately ("tcp read", "udp read" in the 1.32 profiler labels).
1.31 adds `noudp=` and `fixedudpport=` to `graalconfig.txt` (the catalogue gives 14899 as the fixed-port default).
The client handles UDP ids 0 and 10 to 22 in 1.28 beta 2 and 1.3 test, and 0 and 10 to 23 from 1.31. These are the same ids, with the same +32 offset, that 1.33 handles. Ids 0 (movement) and 12 (arrow add) match 2.05 on the wire. A newcomer sends one empty id 22 to each player already in the level; 2.05 uses 22 for chat. The other ids have not been mapped yet. `protocol/udp-p2p.md` covers the 2.05 UDP ids and is the closest reference.

## Lab results (2026-11-19)

Real 1.28 beta 2, 1.3 test and 1.31–1.39 behind the probe proxy: how unknown props, NUL bytes and empty lines are parsed, the own-prop width table per build, and the 10.2 s `PLI_PACKETCOUNT` from 1.33 on are in [`early-clients-probe-2026-11-19.md`](early-clients-probe-2026-11-19.md).

## Open questions

- Finish the meanings of ids 35 to 41 and the full client-to-server list. Selected 1.25/1.27 normal branches for 35–38 are compared above; original names, full consumers and the remaining ids stay open.
- Whether RemoteControl uses the same framing. It probably does, since the server code path is shared, but it hasn't been checked.
