# 07 UDP peer channel in 2.0x

Compare with `Graal_analysis_draft/protocol/udp-p2p.md` (2.05 rev2).

- Every one of the 20 builds imports the same socket calls (socket, bind, sendto, recvfrom, ioctlsocket, getsockname, inet_addr, gethostbyname). The UDP channel therefore exists from 2.00 on, in NewWorld and NewMain too.
- Per build there is one send wrapper and one receive wrapper. The send wrapper has the same shape (about 40 normalized statements) in every build. The receive wrapper has the same shape (about 82 statements) from 2.00 to 2.04 and NewMain, shrinks to 74 in 2.05 and NewWorld beta1, and to 72 in 2.1 test2/test3 and NewWorld beta2.
- The earlier shape comparison reported a removed test and a field-offset change in 2.05. The selected native follow-up below locates a pre-receive predicate on a stored object field, rather than the current datagram's returned length; its higher-level purpose remains unresolved. The earlier datagram-shape result is separate: seq byte + XORed payload in 2.00-2.04 [structure confirmed by the same call structure, not by per-id decode].

## Selected 2.04/2.05 pre-receive predicate

A 2026-11-28 follow-up read two separately identified retained inputs associated with the published 2.04 and 2.05 tokens. Both report FileVersion 2.0.4.0, so resource version alone does not distinguish them. The selected 2.05 file also matches the earlier [revision-0 identity record](../receive-dispatch-revision-boundaries-2026-11-09.md#distinct-receive-routes). This does not establish stock lineage or identity with every file used in the earlier batch. Evidence: UDP-RECEIVE-PRELUDE-20261128. No client was run. **[file][bin]**

In the selected 2.04 routine, an integer loaded through an existing global object pointer is tested before the UDP guard and before the imported `recvfrom` call. A zero signed remainder modulo 16 selects a helper call. The current receive result is stored separately only after `recvfrom` returns. This predicate therefore does not test that call's returned datagram length; the earlier alignment/sanity interpretation was not established. The selected 2.05 routine proceeds from setup directly to its UDP guard without that prelude. **[bin]**

The earlier helper passes a fixed memory span to another routine and stores its returned value through a global slot. A nearby helper with similar call-and-store structure remains in the selected 2.05 input. Its algorithm, the tested field's meaning and writers, other callers and any relocation of the operation were not established here. Divisibility does not show one call per 16 datagrams, a timer interval or runtime frequency. **[bin]**

G041 remains partial. This corrects the operand and ordering of the selected removed predicate; it does not settle its overall purpose or revalidate the downstream decoder, datagram layout, malformed-input behavior, other revisions or runtime acceptance. **[bin]**

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
