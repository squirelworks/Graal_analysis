# UDP peer-to-peer channel (2.05)

Date: 2026-10-21

All facts here are from client 2.05 rev 2. **[2.05]** No open-source server implements this channel, because the server never sees it.

## Setup
- At connect the client binds a UDP socket on `fixedudpport` if `fixedport` is set, otherwise on an ephemeral port. Config `noudp` turns the channel off.
- It sends its own port to the server as `PLPROP_UDPPORT` (31, GINT3). The server relays this to other players.
- A peer's address is `PLPROP_IPADDR` (30, GINT5 = 32-bit IP) plus `PLPROP_UDPPORT` (31). Both arrive through `PLO_OTHERPLPROPS`.

## Datagram
`seq` (1 byte) + payload. The whole datagram is XORed with the low byte of `peerId XOR ownId`.

In code, the key is the low byte of the recipient player's id field XOR the same field on the local player object. In practice the local object's field reads **1**, so the effective key is `recipientId XOR 1`. A three-player lab capture settles this on the wire. With players 2, 3 and 4 all sending to each other, the key depended only on the destination: every datagram to player 2 used key 3, to player 3 key 2, and to player 4 key 5, whoever sent it. That is `recipientId XOR 1`, and key 5 rules out `senderId`. Every datagram decoded with `seq` counting up from 0 per sender–recipient pair. **[cap]** (An earlier two-player capture could not tell `recipientId XOR 1` from `senderId`, because with ids 2 and 3 they give the same keys.) The local player apparently never stores its own server id in that field. **[2.05][cap]**

- `seq` is per peer and wraps mod 256. A duplicate `seq` is dropped.
- There is no zlib, no length prefix, and no gen-3 insertion.
- Payload = GCHAR UDP id + fields, in the same G-type encodings as TCP.
- A datagram is accepted only from the ip:port of a known player.

## Routing
A level-local action goes **UDP only** when every other player in the level has a UDP port. Otherwise it goes over UDP to the peers that have one **and** over TCP to the server.

## UDP ids (own dispatcher, not PLI/PLO numbering)

| Id | Meaning | Dir |
|----|---------|-----|
| 0 | movement: X, Y, SPRITE, STATUS, CARRYSPRITE, bow | send/recv |
| 10 / 11 | bomb add / del | send/recv |
| 12 / 13 | arrow add / fire spy | send/recv |
| 14 | explosion | send/recv |
| 15 | showimg | send/recv |
| 16 / 17 | horse add / del | send/recv |
| 18 | throw carried | send/recv |
| 19 / 20 | item add / del | send/recv |
| 21 | remote hit from GS1 `hitplayer`, sent only to the victim: knockback dx, dy and half-hearts | send/recv |
| 22 | chat (≤ 253 bytes) | send/recv |
| 23 | level name only; rewritten on receive as `PLPROP_CURLEVEL` (20). No 2.05 sender | recv |
| 24 | "entered level": X, Y, level name; sent to players in the 3×3 gmap neighbourhood | send/recv |
| 25 | hit objects | send/recv |
| 26 | trigger action | send/recv |
| 28 | 5.0.0.7: shot, the PLI_SHOOT body (`shoot-5007.md`) | send/recv |
| 30 | 5.0.0.7: shot, the PLO_SHOOT2 body (`shoot-5007.md`); no 5.0.0.7 sender seen | recv |

The ids 10–20 and 25–26 line up with the matching TCP PLI meanings (`PLI_BOMBADD` 4 …), but the numbers differ. The movement fields reuse PLPROP encodings [inf: field order not documented here].

## Observed on the wire **[cap]**

Lab, two 2.05 clients on one level, both with `noudp=false`:
- **Id 0 movement:** six GCHARs: X×2, Y×2, SPRITE (direction: 0 up, 2 down and 3 right were seen), STATUS (20 in the lab), CARRYSPRITE (−1 = none), and one more GCHAR that follows the current animation. It was 55 while walking, 41 on the datagram where the player stopped, and 51 on the datagram sent at the same instant as a `sword.gani` change. As characters (+0x20) those are `W`, `I` and `S`, so the value looks like the first letter of the gani name: walk, idle, sword. **[cap][inf]** The "bow" label in the table above comes from the code reading and does not match these values. It is sent about every 100 ms while moving, then less often.
- **Id 15 showimg:** four GCHARs (index, x, y, name length) followed by the image name, e.g. the AFK emoticon `emoticon_afk_stay.mng`, then a few trailing bytes. It is re-sent every ~3 s while shown.
- **TCP too:** while UDP was active, both clients still sent `PLI_PLAYERPROPS` X/Y/sprite updates over TCP. When the server is in the level, the "UDP only" routing rule does not stop the TCP copy. Exactly which condition picks TCP is not traced. **[inf]**

## 3.04 Linux (lab, 2026-10-30) **[cap]**

The 3.x Torque client kept this channel byte for byte. Two 3.04 clients exchanged id 0 (movement, same seven fields and gani letter), id 22 (chat), id 26 (trigger action, e.g. a mouse click as NPC id 0, x×2, y×2, `leftmouse`, UDP only) and id 15 with a single byte 9 about every 5.1 s per peer. That last one is the periodic message 2.31 sends to the server as TCP 24. Key `recipientId XOR 1` and `seq` from 0 held for every datagram. Details: `version-profiles/lab-304-linux-2026-10-30.md`.

## Payloads of ids 21, 23, 24

- **21** (hit): `GCHAR((dx+4)*16)`, `GCHAR((dy+4)*16)`, `GCHAR(halfhearts)`, then optional attacker-object bytes.
  `dx`/`dy` is the direction from the script's `fromx, fromy` to the victim, each component clamped to −4..4. The receiver decodes it as
  `(b-0x60)/16`, and the damage as `(b-0x20)/2` capped at 1.0. The sender only fires when the victim is in the same level as the local player (it compares their level objects).
- **23**: level name (raw, no length byte). The receiver adds the prop id and length itself (`chr(20+32) + chr(len+32) + name`) and applies it as prop 20 (CURLEVEL). No sender was found in 2.05: no constant id,
  no literal, and no computed id feeds a send helper. A later or earlier client may send it. **[inf]**
- **24**: `GCHAR(x*2)`, `GCHAR(y*2)`, level name (raw, no length byte; the receiver adds it). It is sent when the player enters a level, to peers in the surrounding
  gmap levels. The receiver applies it as props 15, 16 and 20 (X, Y, CURLEVEL).

## Receive cases 10–20 and 25 in 2.05r2 **[bin]**

Added 2026-11-12, from a static read of the 2.05r2 UDP dispatcher. In each case the payload is the matching TCP `PLI_*` body with no player id in front, because the peer that sent the datagram is the sender.

**Shared gate.** For every id below except 18, the handler runs only when the sending peer is in the local player's current level, meaning that level's player list holds the peer. Datagrams from other peers are dropped.

| Id | Payload read | What the receiver does |
| ---: | --- | --- |
| 10 bomb add | `c x×2, c y×2, c power (+8 = sender's bomb), c fuse` (PLI 4); at least 4 bytes | Ignores an exact repeat of the last 10 from the same peer, which is a per-peer dedupe of re-sent datagrams. Otherwise it adds the bomb in the sender's level, with power `v & 7`. With bit 8 set, the sender is the owner. |
| 11 bomb delete | at least 2 bytes (PLI 5) | Removes the bomb from the local player's level, and from the second level the player object holds when that one differs. |
| 13 fire spy | `c` (PLI 10); the sender must be known | Uses the byte divided by 8 (the `a` part, as for TCP) to start the fire effect at the sender's position and direction. |
| 14 explosion | `c radius, c x×2, c y×2, c power (+8 = sender's)` (PLI 27); at least 4 bytes | Power is `v & 7`, clamped to 1–3, and bit 8 makes the sender the owner. It plays the explosion sound, then adds the explosion in the sender's level. |
| 16 horse add | `c x×2, c y×2, c (dir & 3) + 4 × bushes`, `rest` = image (PLI 7); at least 3 bytes | The same per-peer repeat dedupe as 10. It adds the horse in the local player's level, with bushes capped at 6. An empty image name is replaced by a fixed default. |
| 17 horse delete | at least 2 bytes (PLI 8) | Removes the horse, using the same two-level pattern as 11. |
| 18 throw carried | nothing is read (PLI 11) | The sender's carried object is released as thrown, with the sender recorded as its thrower. This case does not check the level. |
| 19 item add | `c x×2, c y×2, c item` (PLI 12); at least 3 bytes | Item 0–24, and only types that are enabled. It adds the item in the sender's level and plays the drop sound. A `sword` or `shield` item copies the sender's current sword or shield image onto the dropped item. |
| 20 item delete | `c x×2, c y×2` (PLI 13); at least 2 bytes | Removes the item using the same two-level pattern, and plays a sound. |
| 25 hit objects | `c power×2, c x×2, c y×2` [+ `i3 npc`] (PLI 36); at least 3 bytes | Runs the remote-hit routine that 21 uses, in its "hit objects" mode. Power is `(b0 − 32) / 2`, capped at 1 heart. With 6 or more bytes, the source is that NPC's centre; otherwise it is the sender's position. The local player is hurt only within 10 tiles of the source, and only when (x, y) lies within 2 tiles of the player's body centre on both axes. The same dedupe and same-level checks as 21 apply. |

Limits: the position arguments of the delete routines (11, 17, 20) are passed in registers that the export loses, so "removes the one at (x, y)" is **[inf]** from the TCP twins. Which sound 14 and 20 play is not named in the export.

## Open
- Which client sends id 23 (2.05 only receives it).
- Whether 2.1 to 2.31 kept this channel on the wire (3.04 did, see above). In 2.22, `noudp=true` is the default, and voice chat also used UDP.
