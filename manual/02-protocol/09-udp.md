<!-- manual: kind=reference status=draft -->
# 2.9 UDP peer-to-peer

A channel between clients that the game server never sees; the server only relays each player's address. The ids handled per build are in → App. C.4; the TCP twins of the level-object messages are in → §2.4.5.

> Status: draft.

## 2.9.1 Setup and addressing

| Rule | Builds | Source |
| --- | --- | --- |
| No open-source server implements this channel, because the server never sees it | server | [2.05] (protocol/udp-p2p.md) |
| The first build that links `bind`, `sendto` and `recvfrom`, and calls the feature "direct data packages", is 1.28 beta 2 | 1.28 beta 2 | [bin] (protocol/gserv-1999.md#udp-128-beta-2-on) |
| Every 2.0x build, NewWorld and NewMain included, imports the same socket calls and has one send and one receive wrapper | 2.00 to 2.1 tests | [bin] (client-internals/decomp-findings-2026-10-24-c/07-udp-channel.md) |
| At connect the client binds a UDP socket on `fixedudpport` when `fixedport` is set, otherwise on an ephemeral port; `noudp` turns the channel off | 2.05 | [2.05] (protocol/udp-p2p.md#setup) |
| 1.31 adds `noudp=` and `fixedudpport=` to the client config; the catalogue gives 14899 as the fixed-port default | 1.31 | [bin] (protocol/gserv-1999.md#udp-128-beta-2-on) |
| `noudp` defaults to on | 2.22, 2.31 | [bin] (version-profiles/2.22-2.31.md#wire-protocol) |
| The client sends its own port as PLPROP UDPPORT (31, `i3`); a peer's address is PLPROP IPADDR (30, `i5`, a 32-bit address) plus UDPPORT, both arriving in `PLO_OTHERPLPROPS` | 2.05 | [2.05] (protocol/udp-p2p.md#setup) |
| A datagram is accepted only from the address and port of a known player | 2.05 | [2.05] (protocol/udp-p2p.md#datagram) |

## 2.9.2 Datagram

| Rule | Builds | Source |
| --- | --- | --- |
| A datagram is `seq` (1 byte), then `c` UDP id and the fields, in the same G-type encodings as TCP; no zlib, no length prefix, no gen-3 insertion | 2.05 | [2.05] (protocol/udp-p2p.md#datagram) |
| The whole datagram is XORed with one key byte: `recipientId XOR 1` | 2.05, 3.04 | [2.05][cap] (protocol/udp-p2p.md#datagram) |
| In code the key is the low byte of the recipient's id field XOR the same field of the local player object, which reads 1 in practice | 2.05 | [2.05][cap] (protocol/udp-p2p.md#datagram) |
| In a three-player capture (ids 2, 3, 4) every datagram to player 2 used key 3, to player 3 key 2 and to player 4 key 5, whoever sent it | 2.05 | [cap] (protocol/udp-p2p.md#datagram) |
| `seq` counts from 0 per sender–recipient pair and wraps mod 256; a duplicate `seq` is dropped | 2.05, 3.04 | [2.05][cap] (protocol/udp-p2p.md#datagram) |
| 1.28 beta 2 sends single, uncompressed, unframed messages straight to another player's address and port | 1.28 beta 2 | [cap] (protocol/gserv-1999.md#udp-128-beta-2-on) |
| The 2.05 receive wrapper drops a bit test on a length value and moves a field offset compared with 2.00–2.04; the datagram layout does not change | 2.00 to 2.05 | [bin] (client-internals/decomp-findings-2026-10-24-c/07-udp-channel.md) |

## 2.9.3 Routing

| Rule | Builds | Source |
| --- | --- | --- |
| A level-local action goes over UDP only when every other player in the level has a UDP port; otherwise it goes over UDP to the peers that have one and over TCP to the server | 2.05 | [2.05] (protocol/udp-p2p.md#routing) |
| The TCP copy is also sent when the server has an NPC server (`PLO_HASNPCSERVER`) | 2.05 | [2.05] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| This rule covers the level-object messages only; player props stay on TCP | 2.05 | [cap] (protocol/packet-layouts.md#combat-and-objects-both-directions) |
| With UDP active, both clients still sent X, Y and sprite props over TCP; which condition picks the TCP copy when the server is in the level is not traced | 2.05 | [cap][inf] (protocol/udp-p2p.md#observed-on-the-wire-cap) |
| One player per level, the level leader picked with `PLO_ISLEADER` (10), sends the level NPCs' arrows to the others | 1.28 beta 2 | [cap] (protocol/gserv-1999.md#udp-128-beta-2-on) |

## 2.9.4 UDP ids

The ids are their own space, not PLI or PLO numbers; the wire byte is again the id + `0x20` [2.05] (protocol/udp-p2p.md#udp-ids-own-dispatcher-not-plipl-numbering); [bin] (version-profiles/udp-ids-200-204.tsv).

| Id | Meaning | Payload | TCP twin | Source |
| ---: | --- | --- | --- | --- |
| 0 | movement | six GCHARs: X × 2, Y × 2, SPRITE, STATUS, CARRYSPRITE (−1 none), and a letter that follows the animation | props 15–19 | [2.05][cap] (protocol/udp-p2p.md#observed-on-the-wire-cap) |
| 10, 11 | bomb add, bomb delete | unmeasured beyond the TCP twins | PLI 4, 5 | [2.05] (protocol/udp-p2p.md#udp-ids-own-dispatcher-not-plipl-numbering) |
| 12 | arrow add | the 5 bytes of relay `A` in 1.28 beta 2 | PLI 9 | [2.05] (protocol/udp-p2p.md#udp-ids-own-dispatcher-not-plipl-numbering); [cap] (protocol/gserv-1999.md#udp-128-beta-2-on) |
| 13 | fire spy | unmeasured | PLI 10 | [2.05] (protocol/udp-p2p.md#udp-ids-own-dispatcher-not-plipl-numbering) |
| 14 | explosion | unmeasured | PLI 27 | [2.05] (protocol/udp-p2p.md#udp-ids-own-dispatcher-not-plipl-numbering) |
| 15 | showimg | four GCHARs (index, x, y, name length), the image name, then a few trailing bytes; 3.04 sends one byte 9 about every 5.1 s per peer | PLI 24 | [cap] (protocol/udp-p2p.md#observed-on-the-wire-cap); [cap] (protocol/udp-p2p.md#304-linux-lab-2026-10-30-cap) |
| 16, 17 | horse add, horse delete | unmeasured | PLI 7, 8 | [2.05] (protocol/udp-p2p.md#udp-ids-own-dispatcher-not-plipl-numbering) |
| 18 | throw carried | unmeasured | PLI 11 | [2.05] (protocol/udp-p2p.md#udp-ids-own-dispatcher-not-plipl-numbering) |
| 19, 20 | item add, item delete | unmeasured | PLI 12, 13 | [2.05] (protocol/udp-p2p.md#udp-ids-own-dispatcher-not-plipl-numbering) |
| 21 | remote hit from GS1 `hitplayer`, sent only to the victim | `c (dx + 4) × 16, c (dy + 4) × 16, c halfhearts`, optional attacker-object bytes | PLO 40 shape | [2.05] (protocol/udp-p2p.md#payloads-of-ids-21-23-24) |
| 22 | chat | text, at most 253 bytes | CURCHAT prop | [2.05] (protocol/udp-p2p.md#udp-ids-own-dispatcher-not-plipl-numbering) |
| 23 | level name | raw level name, no length byte; applied as CURLEVEL (20); no 2.05 sender | prop 20 | [2.05][inf] (protocol/udp-p2p.md#payloads-of-ids-21-23-24) |
| 24 | entered level | `c x × 2, c y × 2`, raw level name; sent to peers in the 3 × 3 gmap neighbourhood | props 15, 16, 20 | [2.05] (protocol/udp-p2p.md#payloads-of-ids-21-23-24) |
| 25 | hit objects | unmeasured | PLI 36 | [2.05] (protocol/udp-p2p.md#udp-ids-own-dispatcher-not-plipl-numbering) |
| 26 | trigger action | for example NPC id 0, x × 2, y × 2, `leftmouse` | PLI 38 | [cap] (protocol/udp-p2p.md#304-linux-lab-2026-10-30-cap) |

| Rule | Builds | Source |
| --- | --- | --- |
| Movement goes out about every 100 ms while moving, then less often | 2.05, 1.28 beta 2 | [cap] (protocol/udp-p2p.md#observed-on-the-wire-cap); [cap] (protocol/gserv-1999.md#udp-128-beta-2-on) |
| The last movement byte was 55, 41 and 51 (`W`, `I`, `S` as characters) for walk, idle and sword, so it looks like the first letter of the gani name | 2.05, 3.04 | [cap][inf] (protocol/udp-p2p.md#observed-on-the-wire-cap) |
| Showimg is re-sent about every 3 s while shown | 2.05 | [cap] (protocol/udp-p2p.md#observed-on-the-wire-cap) |
| 21's `dx`, `dy` is the direction from the script's `fromx, fromy` to the victim, clamped to −4..4; the receiver decodes `(b − 0x60) / 16` and damage `(b − 0x20) / 2` capped at 1.0; it is sent only when the victim is in the same level | 2.05 | [2.05] (protocol/udp-p2p.md#payloads-of-ids-21-23-24) |
| A newcomer sends one empty id 22 to each player already in the level | 1.28 beta 2 to 1.32 | [cap] (protocol/gserv-1999.md#udp-128-beta-2-on) |
| Ids 0, 15 and 22 go through a broadcast helper (prepend the id, send to every peer with a UDP port); the other ids through a peer-send wrapper | 2.00, 2.05 | [bin] (version-profiles/udp-ids-200-204.tsv) |
| UDP 25 and 26 first appear in the same builds as their TCP twins, PLI 36 (2.01) and PLI 38 (2.03) | 2.01, 2.03 | [bin] (version-profiles/udp-ids-200-204.tsv); [bin] (client-internals/decomp-findings-2026-10-24-c/07-udp-channel.md) |
| The Torque-era 3.04 client kept the channel byte for byte | 3.04 | [cap] (protocol/udp-p2p.md#304-linux-lab-2026-10-30-cap) |
| Whether 2.1 to 2.31 used the channel on the wire is unmeasured; 2.22 also used UDP for voice chat | 2.1 to 2.31 | [doc] (protocol/udp-p2p.md#open) |

## 2.9.5 Unpacked Windows 6.1.1.3

| Rule | Builds | Source |
| --- | --- | --- |
| A datagram socket opener is present. The game connect path does not call it. Script can, through the method that reports "Binding of port" | 6.1.1.3 | [bin] (protocol/v6113-udp-code.md#what-is-in-the-image) |
| The 6.113 captures have no client datagram on the TCP 14900 remotes. That matches the connect path, and it leaves the script opener in the image | 6.1.1.3 | [bin][cap] (protocol/v6113-udp-code.md#against-the-captures) |
