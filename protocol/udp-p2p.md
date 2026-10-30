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

## Open
- Which client sends id 23 (2.05 only receives it).
- Whether 2.1 to 2.31 kept this channel on the wire (3.04 did, see above). In 2.22, `noudp=true` is the default, and voice chat also used UDP.
