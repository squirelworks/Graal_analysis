# Lab findings: PLI 46 on level changes, PLI 24, PLO 178 (batch c, 2026-10-24)

Derived facts only. Lab-only runs: real 2.22 and 2.31 clients against the stock open-source game server and listserver, on a loopback-only lab network, with placeholder accounts. No public server was contacted. Follows `07-lab-findings-46-186-200.md` (batch b2). Tables are under `version-profiles/`:

| Table | Content |
|---|---|
| `lab-levelchange-46-222-231.tsv` | 18 level changes (door or edge link, server-side warp) on 2.31 and 2.22: whether PLI 46 and PLI 39 went out, and where |
| `lab-showimg24-relay.tsv` | PLI 24 payloads (the real 9 and eight injected ones) and how the server relayed them |
| `lab-serverwarp178.tsv` | PLO 178 tests: the real chain and five injected field-order cases |

## How to read the provenance
- **Observed**: a real client and a real lab server, nothing altered.
- **Synthetic**: a lab-only re-encoding proxy rewrote or injected a message. The client's or server's reaction is what was observed. It says nothing about what a real public service sends.
- **Unresolved**: not answered by this run.
- In the 178 table, `<name>`, `<lab host>` and `<port>` are placeholders for the lab server's name, a loopback address and its port.

## A. PLI_ENTERLEVEL (46) on doors, edge links and server warps
Table: `version-profiles/lab-levelchange-46-222-231.tsv`. 2.31: 2 sessions, 10 transitions. 2.22: 1 session, 8 transitions. Both mix first visits and cached visits.

**2.31 [observed]**
- Sends `46 = GCHAR 1` on **every** level entry, not only on a gmap crossing: a level link (a door or an edge strip) and a server-side warp (the chat command `warpto`). The payload never changes.
- The position depends on who starts the change and on whether the client has the level cached:
  - **Level link, level not cached.** The client sends `PLI_LEVELWARP` (0) with x, y and the level name. The server answers (ids 14, 6, 100, 101, 39, 1, 0, 174, 10, 42, 156). Then the client sends one frame: `46`, then the props. So 46 comes **after** the server's answer.
  - **Level link, level cached.** The client sends `PLI_LEVELWARPMOD` (30), which adds the level's mod time before x, y and the name. The 46 is in the **same frame** as the 30, right after it and before the props, so before the server's answer. That answer has no id 14, and no 100/101 when the board is cached too.
  - **Server-side warp.** The server sends 14, 6 and the level data. The client then replies with a frame whose first message is 46. The props follow in the same frame only if the position changed; a warp to the same x, y gives `46` alone.
  - **Gmap crossing** (batch b2): 46, then the props, in one frame before the server's answer.
- One rule covers all four: 46 goes out when the client has the level and is about to send the first props of it. At login it is in the login frame after the `PLI 35` messages and before `PLI 44` and the props.
- **2.31 does not re-send the tamper check (39) on a door, a link or a warp.** Its 39 stays on the 3.2 s timer.

**2.22 [observed]**
- **Never sends 46**: 0 of 8 transitions, and not at login.
- It does send the tamper check (39, the same 10 bytes) in the same frame as every **client-initiated** level-link request (`0` or `30`, then `39`), as it does at a gmap crossing. It does not send 39 after a server-side warp.

**Not done / unresolved**
- A level change started by a level NPC script (`setlevel2`). The lab's level scripts never ran, so there is no capture of a script warp. Whether it looks like a link on the wire is unresolved.
- Separate lab observation, not investigated: an NPC whose image was a large sprite sheet made the 2.31 client stop sending anything (no heartbeat) for over a minute.

## B. PLI_SHOWIMGPLAYER (24)
Table: `version-profiles/lab-showimg24-relay.tsv`.

**What the real clients send [observed]**
- **2.31** sends `24 = GCHAR 9` in its first frame after login (after 46 and 44, with the props) and again every 5.11 to 5.17 s (median 5.13 s; one gap of 5.5 s), idle or walking, in every level used. 48 messages in two solo sessions. The value never changed. A level change neither triggers nor resets it.
- **2.22 also sends `24 = 9`**, at login and then every 5.1 s, **but only while another player is in the same level**: 0 messages in 3 solo sessions of 70 to 100 s each. Earlier notes calling 24 "2.31 only" are wrong for 2.22 with two players. The exact condition (another player present, their props received, or the same level) was not isolated. **Unresolved.**

**Server reaction [observed in the source and on the wire]**
- The stock server relays 24 unchanged as `PLO_SHOWIMGPLAYER` (32) = `GSHORT sender id` + the client's payload, to every other player in the level area (not back to the sender). Both real clients were seen receiving the other's 9 every 5 s.

**Injected payloads [synthetic]**
- A lab-only proxy replaced the payload of each client 24 with `GCHAR 0`, `1`, `5`, `14`, `58`, `95`, the six bytes `xx.png`, and an empty payload. The server relayed each one verbatim as 32. No disconnect, no invalid-packet entry in the server log, no error. Neither 2.31 nor 2.22 showed any visible reaction: screenshots matched the baseline apart from an animated status bar. The lab had no player sprites or emoticon files, so a drawn image could not have shown anyway.

**Conclusion**
- The stock server treats 24 as an opaque payload to relay. The 2.31 form is a single byte 9, unlike the four-field emote form (index, x, y, name length and name) that the 2.05 notes describe. What the 9 means, and what a receiving client does with a one-byte payload, is **unresolved**. An emote-form payload with a real image file in the receiver's folder was not tried. (Later read: 2.05 does not use a four-field form; it sends the same tagged image list, see `../id24-205.md`.)

## C. PLO_SERVERWARP (178)
Table: `version-profiles/lab-serverwarp178.tsv`. Real 2.31 client only.

**The chain [request synthetic, rest real]**
- A client `PLI_SERVERWARP` (41) carrying the target server's name was injected on the 2.31 connection. The real game server passed the name to the real lab listserver, which answered. The game server wrapped the answer as 178 for the client. The wire text had four comma fields: `<name>,<name>,<host>,<port>`.
- That answer comes from the **open-source listserver reimplementation**. What a real service sends is **unobserved**, although the 2.31 client accepted this one.

**What the client does on 178 [observed]**
- It closes the connection to the current game server (FIN). A few milliseconds later (2 to 3 ms) it opens a TCP connection to the host in field 2 and the port in field 3, and logs in again by itself: login frame type 5, a new random key, its normal version token, the same account and the same stored password.
- There is **no new listserver connection** and no server-list screen. The second game server accepted the login and sent its usual login sequence.

**Field order [synthetic 178 frames]**
| Fields sent (field 0 first) | Client reaction |
|---|---|
| decoy host, name, host, port | connected to the host in field 2 and the port in field 3; no attempt to the decoy. **Field 0 is unused.** |
| any, host, port, name | no TCP connection; old connection closed; "The connection couldn't be established!" with Reconnect and Open serverlist |
| any, name, port, host (port and host swapped) | same failure |
| any, a bogus name, host, port | connected normally. **Field 1 is a name and is not needed to connect.** |
| any, name, host (three fields) | ignored: connection stays, nothing happens. Consistent with "at least 4 fields". |

- So on the wire: **field 0 unused, field 1 = server name, field 2 = host, field 3 = port.** This matches the decompile reading in `02-server-to-client-layouts.md`.
- **Unresolved:** whether field 1 is used for anything else (a title text, say). Not tried: 2.22, a host name instead of an IP in field 2, a port above 65535, extra trailing fields. A script-initiated `serverwarp` did not run in the lab (see A), which is why the request was injected.

## What to implement (Seihai, 2.31 and 2.22 profiles)
1. **2.31:** send `46 = GCHAR 1` once per level entry, immediately before the first props frame of the new level. In the same frame as the warp request when the level is cached; in the first client frame after the server's level answer (6 or 14) otherwise; at login, after the `PLI 35` messages and before `PLI 44`. Drop the "login one-shot" idea.
2. **2.22:** do not send 46. If the tamper check is enabled, send 39 in the same frame right after each client-initiated `PLI_LEVELWARP` or `PLI_LEVELWARPMOD`, not after a server-side warp.
3. **178:** parse four comma fields, use fields 2 and 3, close the connection, reconnect to that host and port with a fresh login (new key, same credentials). Ignore the message with fewer than four fields. No listserver step.
4. **24 and 32:** treat 32 as `GSHORT id` + opaque bytes. Do not crash on a one-byte or empty payload. 2.31 sends 24 = 9 always; 2.22 was seen sending it only while another player was in the level (condition not isolated).
