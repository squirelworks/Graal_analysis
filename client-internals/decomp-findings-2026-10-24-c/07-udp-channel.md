# 07 UDP peer channel in 2.0x

Compare with `Graal_analysis_draft/protocol/udp-p2p.md` (2.05 rev2).

- Every one of the 20 builds imports the same socket calls (socket, bind, sendto, recvfrom, ioctlsocket, getsockname, inet_addr, gethostbyname). The UDP channel therefore exists from 2.00 on, in NewWorld and NewMain too.
- Per build there is one send wrapper and one receive wrapper. The send wrapper has the same shape (about 40 normalized statements) in every build. The receive wrapper has the same shape (about 82 statements) from 2.00 to 2.04 and NewMain, shrinks to 74 in 2.05 and NewWorld beta1, and to 72 in 2.1 test2/test3 and NewWorld beta2.
- The 2.05 change is a removed bit-test on a length value (alignment or sanity step, purpose unresolved) and a field offset; nothing about the datagram layout changes. Datagram shape in 2.00-2.04 is still seq byte + XORed payload [structure confirmed on 2.00-2.04 by the same call structure, not by per-id decode].
## UDP ids sent per build (constant-id call sites of the peer-send wrapper)
| build | ids found |
|---|---|
| 2.00 (and revs) | 10, 11, 12, 13, 14, 16, 17, 18, 19, 20 |
| 2.01 | + 25 (hit objects) |
| 2.03 | + 26 (trigger action) |
| 2.04 | 11, 16, 17, 19, 20, 25, 26 found (other call sites go through a changed wrapper form; not recovered) |
| 2.05 | the 2.05 rev2 set from `udp-p2p.md`; the scan found only the movement sender (id 0) |

- These were partial in the first scan: ids 0 (movement), 15 (showimg) and 22 (chat) use a broadcast helper (prepend GCHAR id, send to every peer with a UDP port) rather than a naked constant at sendto. Manual read recovered them for 2.00 and 2.05; see `version-profiles/udp-ids-200-204.tsv`. Receive switch cases are wire bytes 0x20 / 0x2f / 0x36.
- The additions match the TCP ids: UDP 25/26 appear in the same builds as PLI 36 (2.01) and PLI 38 (2.03), which supports the "UDP + TCP twin" reading in `05`.
- So the 2.00 client has movement, showimg, chat, bomb, arrow, firespy, explosion, horse, throw and item UDP messages (ids 0, 10-20, 22); hit objects arrive in 2.01 and trigger action in 2.03.
- A 2.00 client has no hit-objects message on either channel.
