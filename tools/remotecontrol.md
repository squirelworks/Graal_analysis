# RemoteControl

Delphi staff client, predecessor of the GTK `RC2_2.05`. One process, 25 auto-created forms. Combined RC + NC in one program ("new RC version with file browser, server list and RC+NC in one program", v2.13). The live console holds two `TGraalClient` sockets:

- RC / game-server socket.
- NPC-server (NC) socket, opened when the RC connects to the NPC server.

Revised 2026-10-21 from a static read of `RemoteControl.exe` (Graal Reborn 2.2.2.0 folder). Tags: **[bin]** read from the binary · **[srv]** gs2lib/GServer only.

## Logins **[bin]**

| Socket | First message | Mode during login | Mode after |
|---|---|---|---|
| RC | type **6**, GCHAR key (`rand & 0x7F`), `GSERV024`, `str account`, `str password` | fixed zlib, no cipher, no type byte | **gen 5** (type byte + partial XOR) |
| NC | type **3**, `NCL11012`, `str account`, `str password` (no key byte) | fixed zlib, no cipher, no type byte | unchanged for the whole session |

- Right after the RC login the client sends a short `PLI_PLAYERPROPS` (2). Its prop list is not traced.
- Type 6 is what gs2lib calls "RC2". This Delphi RC already uses it, so "RC2 = type 6" in the server tables means the gen-5 RC login, not the GTK program. **[bin][srv]**
- `GSERV024` and `NCL11012` are plain string constants here, unlike the game clients' char-by-char tokens. Default NC address fields are the loopback address and `14804`. The live address arrives in `PLO_NPCSERVERADDR` (79), which the RC handles. **[bin]**
- The default account and password fields hold `super` / `super`. **[bin]**

## Codec

Classic Graal text messages (`GCHAR id` + payload + `\n`, G-integers with `+0x20`), batched and flushed at 0x1000 bytes. Framing and cipher are the client-side gen 5 described in `protocol/client-versions.md`: in dynamic mode each flush picks raw/zlib/bz2 by size, writes a type byte, and XORs the first 12 or 4 dwords (one LCG step per 4-byte group present, a partial last group included) with the `0x04A80B38`-seeded cipher LCG (Borland multiplier, `+ key`). Send and receive keep separate iterators with the same key. The NC socket never leaves the fixed zlib mode, so NC traffic has no cipher and no type byte. **[bin]**

Correction: the earlier note "compression mode chosen once" is wrong for the RC socket. After login the mode is chosen per flush. **[bin]**

## Ids

Server → client, RC socket: 13, 16, 30, 35, 37, 55–59, 61–70, 72–74, 76, 77, 79, 100, 103, 180. **[bin]**
Server → client, NC socket: 16, 33, 80, 157–164, 167, 188. **[bin]**

Client → server with a constant id at the call site **[bin]** (a few more are sent with a computed id):
- RC socket: 2, 6, 28, 51–54, 61–64, 68–76, 78, 79, 82, 84, 86, 88–92, 94, 96–98.
- NC socket: 3, 79, 103–119, 150, 151.

Names for all of these are in `protocol/packet-ids.md`. The NC set lines up with gs2lib's `PLI_NC_*` (103–119) and `PLI_NC_LEVELLIST*` (150/151).

## Player list

Packet 0x37 creates or updates a `TServerPlayer`. The body is a property stream walked by the property parser. Id is a 14-bit integer. Constructor defaults include hearts = 3, sword = `sword1.gif`, body = `body.png`, level = `onlinestartlocal.graal`.

## File and account operations

- Folder change: 0x5a.
- Upload framed by 0x9b / 0x5d / 0x9c.
- Delete requires the rights string to contain `w`.
- Account list and property get/set use the matching PLI_RC_* ids from gs2lib.

Local settings live in `controlconfig.txt`. RC2 later wrote the same family to `control2config.txt`.
