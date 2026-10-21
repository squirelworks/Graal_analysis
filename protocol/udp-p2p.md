# UDP peer-to-peer channel (2.05)

Date: 2026-10-21

All facts here are from client 2.05 rev 2. **[2.05]** No open-source server implements this channel, because the server never sees it.

## Setup
- At connect the client binds a UDP socket on `fixedudpport` if `fixedport` is set, otherwise on an ephemeral port. Config `noudp` turns the channel off.
- It sends its own port to the server as `PLPROP_UDPPORT` (31, GINT3). The server relays this to other players.
- A peer's address is `PLPROP_IPADDR` (30, GINT5 = 32-bit IP) plus `PLPROP_UDPPORT` (31). Both arrive through `PLO_OTHERPLPROPS`.

## Datagram
`seq` (1 byte) + payload. The whole datagram is XORed with the low byte of `peerId XOR ownId`.

In code, the key is the low byte of the recipient player's id field XOR the same field on the local player object. In practice the local object's field reads **1**, so the effective key is `recipientId XOR 1`. In the lab, player 2 sent with key 3 and player 3 sent with key 2, and every datagram decoded with `seq` counting up from 0. The local player apparently never stores its own server id in that field. **[2.05][cap]**

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
- **Id 0 movement:** six GCHARs: X×2, Y×2, SPRITE (direction), STATUS (20 in the lab), CARRYSPRITE (−1 = none), and one more value (seen 41, 51 and 55; meaning not traced). It is sent about every 100 ms while moving, then less often.
- **Id 15 showimg:** four GCHARs (index, x, y, name length) followed by the image name, e.g. the AFK emoticon `emoticon_afk_stay.mng`, then a few trailing bytes. It is re-sent every ~3 s while shown.
- **TCP too:** while UDP was active, both clients still sent `PLI_PLAYERPROPS` X/Y/sprite updates over TCP. When the server is in the level, the "UDP only" routing rule does not stop the TCP copy. Exactly which condition picks TCP is not traced. **[inf]**

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
- Whether 2.1+ clients kept this channel. In 2.22, `noudp=true` is the default, and voice chat also used UDP.
