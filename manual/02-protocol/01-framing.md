<!-- manual: kind=reference status=draft -->
# 2.1 Framing and encodings

Notation is fixed in → §0.5 to → §0.7. Ciphers that act on messages or frames are in → §2.2; the 1998 text relay, which has no binary framing, is in → §2.3.1.

## 2.1.1 Integer and string encodings

Graal's own types add `0x20` to every 7-bit group, so an encoded value is printable and never contains `\n` [srv][2.05] (protocol/codec-and-framing.md#graal-integer-types).

| Type | Short | Bytes | Encoding, first byte first | Range | Source |
| --- | --- | ---: | --- | --- | --- |
| GCHAR | `c` | 1 | `v + 0x20` | 0–223 | [srv][2.05] (protocol/codec-and-framing.md#graal-integer-types) |
| GSHORT | `s` | 2 | `(v >> 7) + 0x20`, `(v & 0x7F) + 0x20` | 0–28767 | [srv] (protocol/codec-and-framing.md#graal-integer-types) |
| GINT (GINT3) | `i3` | 3 | three 7-bit groups, high first, each `+ 0x20` | 0–3682399 | [srv] (protocol/codec-and-framing.md#graal-integer-types) |
| GINT4 | `i4` | 4 | four 7-bit groups, high first, each `+ 0x20` | unmeasured | [srv] (protocol/codec-and-framing.md#graal-integer-types) |
| GINT5 | `i5` | 5 | first group 4 bits (`v >> 28`), then four 7-bit groups, each `+ 0x20` | 32-bit | [srv] (protocol/codec-and-framing.md#graal-integer-types) |
| GSTRING | `str` | 1 + n | GCHAR length, then n bytes | n ≤ 223 | [srv][2.05] (protocol/codec-and-framing.md#graal-integer-types) |

| Rule | Builds | Source |
| --- | --- | --- |
| On overflow the server clamps rather than wraps (a GSHORT high byte is at most 223) | server | [srv] (protocol/codec-and-framing.md#graal-integer-types) |
| A signed value is sent as its unsigned bit pattern | server | [srv] (protocol/codec-and-framing.md#graal-integer-types) |
| In the login message, an account or password of 224 bytes or more is sent as length byte `0xFF` followed by its first 223 bytes | 4.20r6, 4.20r8, 5.00r7, 6.01r1, 6.03r7 | [bin] (protocol/v4x-clients.md#login-packet); [bin] (protocol/v5x-clients.md#login); [bin] (protocol/v6x-clients.md#login-message-601-and-603) |
| Numbers in 1998 relay payloads use the same `+32` single-character encoding as GCHAR | 1st Graal to 1.1.9 | [bin] (protocol/relay-1998.md#d-payloads) |

## 2.1.2 Messages and terminators

| Rule | Builds | Source |
| --- | --- | --- |
| A message is `GCHAR(id)`, the payload, then `\n` | 1.21 to 6.x | [bin] (protocol/gserv-1999.md#framing); [srv][2.05] (protocol/codec-and-framing.md#messages); [bin] (protocol/v6x-clients.md#cipher-and-framing-classic-mode) |
| Several messages are concatenated in one frame | 1.21 to 6.x | [srv][2.05] (protocol/codec-and-framing.md#messages); [bin] (protocol/gserv-1999.md#framing) |
| The wire byte of the id is the logical id + `0x20`; an id above 223 cannot be sent as one GCHAR | all binary generations | [srv] (protocol/packet-ids.md) |
| The sender refuses a payload that already contains `\n`; binary payloads use the raw-data escape (→ §2.1.3) | 2.05 | [2.05] (protocol/codec-and-framing.md#messages) |
| An outgoing message containing `\n` is refused with "Illegal characters in the outgoing data" | 6.01r1, 6.03r7 | [bin] (protocol/v6x-clients.md#cipher-and-framing-classic-mode) |
| The receiver splits an inflated frame on `\n` | 1.21 to 2.05 | [bin] (protocol/gserv-1999.md#framing); [2.05] (protocol/codec-and-framing.md#205-send-pipeline-update-2026-10-21-205) |
| An id the receive dispatcher has no case for is ignored silently; 2.05 has 59 cases | 2.05 | [2.05] (protocol/codec-and-framing.md#205-send-pipeline-update-2026-10-21-205) |
| Every 2.05 handler checks a minimum length first and drops a short message silently | 2.05 | [2.05] (protocol/packet-layouts.md#how-205-reads-a-message-205) |

## 2.1.3 The raw-data escape

| Rule | Builds | Source |
| --- | --- | --- |
| `PLO_RAWDATA` (100, wire `0x84`) carries an `i3` length; the next *length* bytes are read as one message, newline or not | server; 1.21 to 6.x clients | [srv] (protocol/codec-and-framing.md#raw-data-escape); [bin] (protocol/gserv-1999.md#framing); [bin] (protocol/v4x-clients.md#cipher-and-framing) |
| The server sends 100 in front of `PLO_BOARDPACKET` (101) and `PLO_FILE` (102) | server | [srv] (protocol/codec-and-framing.md#raw-data-escape) |
| 2.05 has a case for 100 in its main dispatch but none for 101 or 102, consistent with 101 and 102 only arriving behind 100 | 2.05 | [2.05][inf] (protocol/codec-and-framing.md#raw-data-escape) |
| In the other direction, before a payload sent as id 93 the client sends id 50 with an `i3` length, capped at `0x37FFFF` | 4.20r8, 5.00r7 | [bin] (protocol/v4x-clients.md#cipher-and-framing); [bin] (protocol/v5x-clients.md#login) |

The board and file layouts behind 100 are in → §2.5 and → §2.7.

## 2.1.4 Frames by generation

Encryption generations are defined in → §2.2.1; builds per generation are in → §1.4.

| Generation | Builds | Client → server frame | Server → client frame | Source |
| --- | --- | --- | --- | --- |
| 1 | 1st Graal to 1.1.9 | text lines ending in `\n`, no length (→ §2.3.1) | same | [bin] (protocol/relay-1998.md#summary) |
| 2 | 1.21 to 1.39 | `u16be length`, then a zlib stream of that length; every flush is compressed, with no size threshold; zlib 1.0.4 | same | [bin] (protocol/gserv-1999.md#framing) |
| 3 | 1.41 rev1 to 2.17 | `u16be length` + zlib stream of the whole out buffer; gen-3 insertion applied per message before compression (→ §2.2.2) | `u16be length` + zlib, no extra byte, no cipher | [2.05] (protocol/codec-and-framing.md#frame); [bin] (protocol/client-versions.md#game-server-login); [srv][cap] (protocol/codec-and-framing.md#frame) |
| 4 | client type 4 (2.19 to 2.21, 3.0, 3.01) | `u16be length` + bz2 body, then partial XOR (→ §2.2.3) | same | [srv] (protocol/codec-and-framing.md#frame) |
| 5 | 2.22 and later; RemoteControl type 6 | login frame: `u16be length` + zlib, no type byte, no XOR (fixed mode 3); later frames: `u16be (len + 1)`, a type byte, the body (→ §2.2.4) | same layout, type byte present from the first frame | [srv] (protocol/codec-and-framing.md#frame); [bin] (protocol/client-versions.md#gen-5-send-on-the-client-222-231-remotecontrol-bin); [2.22][cap] (protocol/codec-and-framing.md#gen-45-partial-xor) |
| 5, long frames | 6.01r1, 6.03r7 | a frame of `0xFFFF` bytes or more is sent as length `0xFFFF` followed by a 4-byte big-endian length | unmeasured | [bin] (protocol/v6x-clients.md#cipher-and-framing-classic-mode) |
| own | Graal3D | → §9 | → §9 | [bin] (client-internals/build-catalogue.md#catalogue) |

### 2.1.4.1 Flush and buffer limits

| Rule | Builds | Source |
| --- | --- | --- |
| Messages collect in an out buffer, compressed and flushed at `0x1000` bytes or at the end of the tick | 2.00 to 2.05, 2.17 | [2.05] (protocol/codec-and-framing.md#205-send-pipeline-update-2026-10-21-205); [bin] (version-profiles/gen3-insertion-200-205.tsv); [bin] (protocol/client-versions.md#game-server-login) |
| The link is dropped when more than `0x40000` bytes are queued unsent | 2.00 to 2.05, 2.17, 2.22, 2.31 | [2.05] (protocol/codec-and-framing.md#205-send-pipeline-update-2026-10-21-205); [bin] (version-profiles/gen3-insertion-200-205.tsv); [bin] (protocol/client-versions.md#gen-5-send-on-the-client-222-231-remotecontrol-bin) |
| The same limit is `0x800000` bytes | RemoteControl (gen 5) | [bin] (protocol/client-versions.md#gen-5-send-on-the-client-222-231-remotecontrol-bin) |
| Buffers flush at `0x1000` | 6.01r1, 6.03r7 | [bin] (protocol/v6x-clients.md#cipher-and-framing-classic-mode) |
| The client links zlib 1.1.2 (Delphi ZLib unit) | 2.05 | [2.05] (protocol/codec-and-framing.md#frame) |
| zlib is a compiled-in unit in 2.00 to 2.01 rev1 and from 2.03 on; 2.02, 2.02 rev1 and 2.02 rev2 import an external `zlib.dll` and need it beside the program; the wire format is the same | 2.00 to 2.1 test | [bin] (client-internals/decomp-findings-2026-10-24-c/03-framing-and-encryption.md#where-zlib-comes-from-the-one-real-difference) |
| The NewWorld betas and NewMain 24 and 26 use the same transport and login shape as 2.00 to 2.05 | NewWorld, NewMain | [bin] (client-internals/decomp-findings-2026-10-24-c/03-framing-and-encryption.md#encryption-generations) |
| The 1998 relay read buffer is 1 KB | 1st Graal to 1.1.9 | [bin] (protocol/relay-1998.md#summary) |
| A UDP peer message is not framed this way (→ §2.9) | 1.28 beta 2 and later | [2.05] (protocol/codec-and-framing.md#205-send-pipeline-update-2026-10-21-205) |

### 2.1.4.2 zlib stream header

| Rule | Builds | Source |
| --- | --- | --- |
| Real clients compress at the best zlib level: the stream starts `78 DA` | 2.05, 2.17.1, 2.22, 2.31 | [cap] (protocol/login-frames-by-version-2026-10-25.md#one-byte-level-difference-that-applies-to-every-seihai-frame) |
| A listserver accepts gen-5 frames that start `78 9C` (default level); whether a classic frame with that header is accepted is unmeasured | public listserver | [cap] (protocol/login-frames-by-version-2026-10-25.md#one-byte-level-difference-that-applies-to-every-seihai-frame) |
