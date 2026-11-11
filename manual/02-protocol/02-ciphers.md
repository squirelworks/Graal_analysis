<!-- manual: kind=reference status=draft -->
# 2.2 Ciphers and compression

Frame layouts are in → §2.1.4. Which build uses which generation is in → §1.4.

## 2.2.1 Encryption generations

The numbering is GServer-v2's (→ §0.9).

| Gen | Selected by | Users | Scheme | Source |
| ---: | --- | --- | --- | --- |
| 1 | web client | web client; the 1998 relay builds have the same "no compression" property | none, uncompressed | [srv] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering); [bin] (protocol/relay-1998.md) |
| 2 | client type 0 whose first 8 login bytes are a known token | 1.21 to 1.39 | zlib, no cipher | [srv] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering); [bin] (protocol/gserv-1999.md#gen-1-to-gen-2-in-one-table) |
| 3 | client type 0 whose first 8 bytes are not a known token (the key byte comes first) | 1.41 rev1 to 2.17; RC, NC and NPC-server connections in the server's numbering | zlib frame; one junk byte inserted into each client-to-server message (→ §2.2.2) | [srv][2.05] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering); [bin] (protocol/client-versions.md#game-server-login) |
| 4 | client type 4 | 2.19 to 2.21, 3.0, 3.01 | bz2, then partial XOR (→ §2.2.3) | [srv] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering) |
| 5 | client type 5; RC2 (type 6) | 2.22, 2.31, 3.04, 3.153, 4.x, 5.x, 6.01, 6.03, Delphi RemoteControl | compression byte, then partial XOR (→ §2.2.3, → §2.2.4) | [srv] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering); [bin] (protocol/v3x-clients.md#game-server-login-and-cipher); [bin] (protocol/v4x-clients.md#cipher-and-framing); [cap] (protocol/v5v6-windows-unpacked.md); [bin] (protocol/v6x-clients.md#cipher-and-framing-classic-mode) |
| 6 | v6 | unmeasured | not implemented in the server source the notes summarise (→ §2.2.5) | [srv] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering) |

The table above says which generation each build uses. The rules below add what it leaves out: the remote-control socket, which uses no cipher, the fact that generation 2 encrypts nothing, and the random-number step that generations 3 to 5 share [bin] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering).

| Rule | Builds | Source |
| --- | --- | --- |
| The NC socket logs in as type 3 and stays zlib with no cipher | Delphi RemoteControl | [bin] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering) |
| Nothing in generation 2 is encrypted; the DES code in those clients is used only for local files | 1.21 to 1.32 | [bin] (protocol/gserv-1999.md#gen-1-to-gen-2-in-one-table) |
| All 2.x clients share one LCG, `it = it * 0x08088405 + key`, seed `0x04A80B38`; the multiplier is Borland's `Random` constant, but the key is added where Borland adds 1 | 2.05, 2.17, 2.22, 2.31 | [bin] (protocol/client-versions.md) |
| The shared multiplier with the RTL `Random` is a toolchain coincidence, not shared state | 2.05 | [2.05] (protocol/codec-and-framing.md#corrections-to-earlier-notes) |
| The same seed is also used for web-level cache file encryption from 1.3 on; that use is not the connection cipher (→ §3.8) | 1.3 test and later | [bin] (client-internals/build-catalogue.md#how-each-column-was-read) |

## 2.2.2 Generation 3 insertion

Client to server only. Server-to-client traffic for a gen-3 client is plain zlib [srv][cap] (protocol/codec-and-framing.md#gen-3-205).

**State.** `it` is a u32 seeded `0x04A80B38` when the connection object is created. The key `k` is `Random & 0x7F`, sent once as a GCHAR in the login message (→ §2.3.3) [2.05] (protocol/codec-and-framing.md#gen-3-205); [bin] (version-profiles/gen3-insertion-200-205.tsv).

**Per message**, starting with the second message of the session (the login message is sent clean; the messages that follow it in the same first frame, such as `PLI_LANGUAGE`, already carry the byte) [2.05][cap] (protocol/codec-and-framing.md#gen-3-205):

| Step | Operation | Source |
| ---: | --- | --- |
| 1 | `it = it * 0x08088405 + k` (mod 2^32) | [2.05] (protocol/codec-and-framing.md#gen-3-205) |
| 2 | `len` = message length including the trailing `\n`; `pos0 = (it & 0xFFFF) mod len` (0-based) | [2.05] (protocol/codec-and-framing.md#gen-3-205); [bin] (version-profiles/gen3-insertion-200-205.tsv) |
| 3 | insert the byte `((it >> 16) & 0x7F) + 0x20` at 0-based index `pos0`, before compression | [2.05] (protocol/codec-and-framing.md#gen-3-205) |

The steps above are the whole algorithm. The properties below are what a decoder needs to get right in practice, and what the lab sessions confirmed [2.05][cap] (protocol/codec-and-framing.md#gen-3-205).

| Property | Source |
| --- | --- |
| `pos0` can be 0, which puts the junk byte before the id byte; a decoder must not take offset 0 as the id until the byte is removed | [2.05][cap] (protocol/codec-and-framing.md#gen-3-205) |
| The inserted byte is never `\n` and never lands after the terminating `\n` | [2.05][cap] (protocol/codec-and-framing.md#gen-3-205) |
| Insertion is per message, after the receiver's decompression, not over the whole frame | [srv] (protocol/codec-and-framing.md#gen-3-205) |
| The server mirrors the step and deletes the byte at 0-based `(it & 0xFFFF) mod len`, where `len` is the split-off line without `\n` but with the junk byte, which equals the client's length | [srv][2.05] (protocol/codec-and-framing.md#gen-3-205) |
| The server's own gen-3 encoder always inserts `)` instead of an iterator-derived byte; harmless, because the receiver discards it | [srv] (protocol/codec-and-framing.md#gen-3-205) |
| Three lab 2.05 sessions: every message after the login had the predicted byte at the predicted index, several at index 0, no mismatches | [cap] (protocol/codec-and-framing.md#gen-3-205) |

Generation 3 starts somewhere between 1.39 and 1.41. The table pins that boundary and records which later builds were checked against the formula [bin] (client-internals/build-catalogue.md#patterns-worth-knowing).

| Builds | Insertion | Source |
| --- | --- | --- |
| 1.39 | absent | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| 1.41 rev1, NewMain 1.42 | present (seed and 7-bit key in the connection initialiser) | [bin] (client-internals/build-catalogue.md#patterns-worth-knowing) |
| 2.00 | the formula above, read byte for byte | [bin] (version-profiles/gen3-insertion-200-205.tsv) |
| 2.01 to 2.04 | same call structure and endpoints as 2.00 and 2.05 | [bin] (version-profiles/gen3-insertion-200-205.tsv) |
| 2.05, 2.05 rev2 | the formula above | [2.05] (protocol/codec-and-framing.md#gen-3-205) |
| 2.17 | the same gen-3 send code | [bin] (protocol/client-versions.md#game-server-login) |

## 2.2.3 Generation 4 and 5 partial XOR

The server/2.22 contract below is not universal across later receivers; the independently inspected Mac PowerPC qualification follows the table. Same LCG and key as generation 3, with one iterator per direction, both seeded `0x04A80B38` [srv][2.22] (protocol/codec-and-framing.md#gen-45-partial-xor); [bin] (protocol/client-versions.md#gen-5-send-on-the-client-222-231-remotecontrol-bin).

| Step | Operation | Source |
| ---: | --- | --- |
| 1 | on send, compress the body first (→ §2.2.4) | [srv][2.22] (protocol/codec-and-framing.md#gen-45-partial-xor) |
| 2 | `groups = min(ceil(len / 4), limit)`, with `limit` 12 for an uncompressed body (`0x02`) and 4 for zlib or bz2 (`0x04`, `0x06`) | [srv][2.22][cap] (protocol/codec-and-framing.md#gen-45-partial-xor) |
| 3 | for each group: advance `it` once, XOR the 4 body bytes with the little-endian bytes of `it` | [srv][2.22] (protocol/codec-and-framing.md#gen-45-partial-xor) |
| 4 | a short last group still advances `it` and is XORed byte by byte with the low bytes of `it` | [srv][2.22][cap] (protocol/codec-and-framing.md#gen-45-partial-xor) ; [cap] (protocol/lab-checks-2026-10-24.md#gen-5-xor-confirmation) |
| 5 | on receive, undo the XOR first, then decompress | [srv] (protocol/codec-and-framing.md#gen-45-partial-xor) |

The step count above is not taken on trust. Each row is one body of evidence that the rule holds, and the last row shows the alternative reading failing [cap] (protocol/codec-and-framing.md#gen-45-partial-xor).

| Evidence for the step rule | Source |
| --- | --- |
| 27 of 27 server-to-client frames from four public 2.22 game servers and both listserver frames, including zlib and bz2 bodies with a partial last group | [cap] (protocol/codec-and-framing.md#gen-45-partial-xor) |
| 610 lab frames, both directions | [cap] (protocol/codec-and-framing.md#gen-45-partial-xor) |
| a real 2.22 client sent 580 uncompressed and 17 zlib frames; all 17 compressed bodies had a length that was not a multiple of 4 and decode only under this rule | [cap] (protocol/codec-and-framing.md#gen-45-partial-xor) |
| ten 5.x and 6.x Windows captures decode with this rule | [cap] (protocol/v5v6-windows-unpacked.md) |
| for these 2.22 captures, `floor(len / 4)` groups for compressed bodies is wrong and leaves the iterator one step behind | [cap] (protocol/codec-and-framing.md#gen-45-partial-xor) |

Builds agree on the cap but not always on rounding. The table gives the number of iterator steps each build takes for a compressed body. A row that differs from `ceil(len / 4)` needs a server that steps the same way [2.22][cap] (protocol/codec-and-framing.md#gen-45-partial-xor).

| Builds | Step count for zlib and bz2 bodies | Source |
| --- | --- | --- |
| 2.22, 2.31 | `ceil(len / 4)`, capped at 4 | [2.22][cap] (protocol/codec-and-framing.md#gen-45-partial-xor) |
| 3.04, 3.153 | `ceil(len / 4)`, capped at 4 | [bin] (protocol/v3x-clients.md#game-server-login-and-cipher) |
| 4.04r2, 4.20r6, 4.20r8 | cap 4; rounding unmeasured | [bin] (protocol/v4x-clients.md#cipher-and-framing) |
| 5.12 | disputed → App. E#2 | [bin][wire] (protocol/v5v6-lab-play.md#512s-cipher-step-count); [cap] (protocol/v5v6-windows-unpacked.md) |
| 5.24r3 and later 5.x, 6.00 to 6.03r7 | `ceil(len / 4)`, capped at 4 | [cap] (protocol/v5v6-windows-unpacked.md); [bin][wire] (protocol/v5v6-lab-play.md#512s-cipher-step-count) |

### 2.2.3.1 Exact-input Mac PowerPC receive qualification

For the four exact Mac inputs identified by digest in the source note, let n be body length after any mode selector is removed, before decompression. Raw mode 2 processes min(ceil(n / 4), 12) groups, including a partial final group. Compressed modes 4/6 process min(floor(n / 4), 4) groups; an incomplete tail is unchanged and advances no state. Before each processed group, state is multiplied by 134775813 and increased by an additive object word, retaining the low 32 bits. Its bytes are XORed least-significant first despite the big-endian target. State persists through the inspected receiver's iterations. [bin] (protocol/macos-ppc-receive-framing.md)

Initial seed, additive-word provenance, reset/rekey writers, negotiation and outgoing symmetry remain untraced. No live frame result or Windows 5.12 capture resolution follows; E#2 remains open. [bin] (protocol/macos-ppc-receive-framing.md)

## 2.2.4 Compression choice

The type byte of a generation-5 frame (→ §2.1.4):

| Code | Body | XORed | Source |
| ---: | --- | --- | --- |
| 1, 2 | raw | only 2 | [bin] (protocol/client-versions.md#gen-5-send-on-the-client-222-231-remotecontrol-bin) |
| 3, 4 | zlib | only 4; 3 is the fixed "zlib, no cipher" mode of the login frame and of the whole NC session | [bin] (protocol/client-versions.md#gen-5-send-on-the-client-222-231-remotecontrol-bin) |
| 5, 6 | bz2 | only 6 | [bin] (protocol/client-versions.md#gen-5-send-on-the-client-222-231-remotecontrol-bin) |

Which code a client picks for each flush of `n` bytes:

| Builds | `n < 0x30` | `0x30 ≤ n < 0x1000` | `n ≥ 0x1000` | Source |
| --- | --- | --- | --- | --- |
| 2.22, 2.31, RemoteControl | `0x04` if zlib is actually shorter, otherwise `0x02` | `0x04` | `0x06` | [bin] (protocol/client-versions.md#gen-5-send-on-the-client-222-231-remotecontrol-bin); [2.22][cap] (protocol/codec-and-framing.md#gen-45-partial-xor) |
| 3.04, 3.153 | `0x02` or `0x04` | `0x04` | `0x06` | [bin] (protocol/v3x-clients.md#game-server-login-and-cipher) |
| 4.x | `0x02` | `0x04` | `0x06` | [bin] (protocol/v4x-clients.md#cipher-and-framing) |
| 5.12 | `0x04` even for short bodies | `0x04` | unmeasured | [cap] (protocol/v5v6-windows-unpacked.md) |
| 5.24r3 and later | `0x02`, like 2.22 | unmeasured | unmeasured | [cap] (protocol/v5v6-windows-unpacked.md) |
| 6.01r1, 6.03r7 | `0x02` | `0x04` | `0x06` | [bin] (protocol/v6x-clients.md#cipher-and-framing-classic-mode) |

The rules below complete the frame layout: what the length counts, why the login frame is different, what has not been seen, and how the older generations choose [2.22][cap] (protocol/codec-and-framing.md#gen-45-partial-xor).

| Rule | Source |
| --- | --- |
| The `u16be` length counts the type byte | [2.22][cap] (protocol/codec-and-framing.md#gen-45-partial-xor) |
| The login frame carries no type byte and no XOR, because the key travels inside it; the socket switches to dynamic mode after it is flushed | [2.22][cap] (protocol/codec-and-framing.md#gen-45-partial-xor); [bin] (protocol/client-versions.md#game-server-login) |
| No client-originated bz2 frame has been captured | [cap] (protocol/codec-and-framing.md#gen-45-partial-xor) |
| Generations 2 and 3 compress every flush with zlib | [bin] (protocol/gserv-1999.md#framing); [2.05] (protocol/codec-and-framing.md#frame) |

## 2.2.5 Generation 6 and script-defined transports

Generation 6 exists only as a name. The rules say what the late clients actually use, and how a script sent by the server can swap the transport out [srv] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering).

| Rule | Builds | Source |
| --- | --- | --- |
| Generation 6 is named in the server source but not implemented there | server | [srv] (protocol/codec-and-framing.md#encryption-generations-gs2lib-numbering) |
| The classic transport of 6.01 and 6.03 is generation 5, unchanged | 6.01r1, 6.03r7 | [bin] (protocol/v6x-clients.md#cipher-and-framing-classic-mode) |
| A server-sent connector script can replace the framing, the cipher (RC4, AES or TLS) and both id tables; generation 5 stays the default until the script switches protocol (→ §2.10) | 6.11 Mac | [bin] (protocol/login-session-known.md); [bin][cap][doc] (version-profiles/matrix/README.md#thinks-wire-and-scripting) |
