# UDP peer-to-peer channel (2.05)

Date: 2026-10-21

All facts here are from client 2.05 rev 2. **[2.05]** No open-source server implements this channel, because the server never sees it.

## Setup
- At connect the client binds a UDP socket on `fixedudpport` if `fixedport` is set, otherwise on an ephemeral port. Config `noudp` turns the channel off.
- It sends its own port to the server as `PLPROP_UDPPORT` (31, GINT3). The server relays this to other players.
- A peer's address is `PLPROP_IPADDR` (30, GINT5 = 32-bit IP) plus `PLPROP_UDPPORT` (31). Both arrive through `PLO_OTHERPLPROPS`.

## Datagram
`seq` (1 byte) + payload. The whole datagram is XORed with the low byte of `peerId XOR ownId`.

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
| 21, 23, 24 | handled on receive; no 2.05 sender found | recv |
| 22 | chat (≤ 253 bytes) | send/recv |
| 25 | hit objects | send/recv |
| 26 | trigger action | send/recv |

The ids 10–20 and 25–26 line up with the matching TCP PLI meanings (`PLI_BOMBADD` 4 …), but the numbers differ. The movement fields reuse PLPROP encodings [inf: field order not documented here].

## Open
- What ids 21, 23, and 24 carry.
- Whether 2.1+ clients kept this channel. In 2.22, `noudp=true` is the default, and voice chat also used UDP.
