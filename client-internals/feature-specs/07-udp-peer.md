# 07 UDP peer channel

Snapshots read: Graal_analysis `8da6800` (`protocol/udp-p2p.md`, `packet-layouts.md`, `tools/lab-setup.md`), Seihai `06aacfd` (`net/udp.rs`).
Folded here from the public-server report: **PLO_HASNPCSERVER 44**, **PLO_ISLEADER 10** (as it relates to TCP fallback).

## What it is
A client-to-client UDP channel in 2.05. The **server never sees it** (GServer-v2 has no implementation); the gserver only relays each player's address (props 30 IPADDR i5 and 31 UDPPORT i3) in `PLO_OTHERPLPROPS`. Layout: datagram = `seq` byte + GCHAR UDP id + fields, all XORed with `recipientId XOR 1`. No zlib, no length prefix. Receiver accepts only from a known peer ip:port, drops duplicate seq. Ids: 0 move, 10/11 bomb add/del, 12/13 arrow/fire spy, 14 explosion, 15 showimg, 16/17 horse, 18 throw carried, 19/20 item add/del, 21 remote hit, 22 chat, 23 level name (receive only), 24 entered-level (x*2, y*2, level) to the 3x3 gmap neighbourhood, 25 hit objects, 26 trigger action. Payloads for 0, 15, 21, 23, 24 are in the note.

## Routing rule **[2.05]**
A level action goes UDP-only when every other player in the level has a UDP port; otherwise it goes by UDP to peers that have one **and** by TCP to the server. Player props still go over TCP. **GServer-v2's `PLO_HASNPCSERVER` (44)**: if sent, 2.05 sends the TCP copy too.

**Consequence for Seihai: UDP is optional.** If Seihai advertises no UDP port (prop 31 = 0 or absent), 2.05 peers send every combat/object message over TCP, and Seihai receives them as normal PLO packets. UDP only saves latency. Seihai's profile has `udp` and `udp_off_by_default` flags already.

## Seihai today
- `net/udp.rs`: `encode_udp`, `decode_udp`, `udp_key`, id constants, socket bind helper; lab-verified with 2- and 3-player pcaps (`examples/udp_replay`).
- Not wired into the session loop: no socket is polled, no props 30/31 are sent, UDP id handlers do not exist.
- PLO 44 and 10 are unhandled.

## Steps for Claude
1. Keep UDP off by default for all profiles (document that peers fall back to TCP). Do **not** send prop 31 unless the user enables it.
2. Optional path, only when enabled: bind (`fixedudpport` or ephemeral), send props 30/31 once after login, poll the socket every frame. The XOR key is `recipientId XOR 1`: to send to peer P use `udp_key(P)`; on receive, use `udp_key(own player id)`.
3. Map each UDP id to the same internal event as its TCP twin (bomb 10 = PLO 11, etc., see 02) so there is one code path.
4. Send id 0 movement only when the position changed; fields X*2, Y*2, SPRITE, STATUS, CARRYSPRITE, animation letter (first letter of the gani name, upper or lower case as seen: `W`, `I`, `S`). Do not send id 23.
5. Store HASNPCSERVER (44) and ISLEADER (10) flags.

## How to test
- `examples/udp_replay` against the existing pcaps (private, never committed; they contain the lab password in plaintext).
- Lab: two Wine 2.05 clients plus Seihai with UDP disabled; confirm bombs arrive over TCP at Seihai. Then enable UDP in Seihai and confirm datagrams decode.

## NEEDS
nothing to implement. Open questions that do not block: which client version sends UDP id 23, and the meaning of the last byte in id 0 beyond "first letter of the animation" (needs a 2.22/2.31 UDP capture if those versions are to be supported; 2.22 defaults to `noudp=true`).
