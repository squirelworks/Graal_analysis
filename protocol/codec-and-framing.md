# Codec, framing, and encryption generations

Date: 2026-10-21

Sources: gs2lib `CEncryption`, `CFileQueue`, `CString` (GPLv3, summarized); GServer-v2 `TPlayer` receive path; client 2.05 rev 2 (`GNW03081`) send path; 2026-10-04 captures.

Confidence tags: **[2.05]** confirmed in the 2.05 binary · **[srv]** server source only · **[cap]** seen in captures · **[inf]** inferred.

## Graal integer types

All "G" types offset each 7-bit group by 0x20 so the stream stays printable and never contains `\n`.

| Type | Bytes | Encode | Range | Tag |
|------|------:|--------|-------|-----|
| GCHAR | 1 | `v + 0x20` | 0–223 | [srv][2.05] |
| GSHORT | 2 | `(v >> 7) + 0x20`, `(v & 0x7F) + 0x20` | 0–28767 | [srv] |
| GINT (GINT3) | 3 | 7-bit groups, high first, each `+ 0x20` | 0–3682399 | [srv] |
| GINT4 | 4 | same, four groups | — | [srv] |
| GINT5 | 5 | first group 4 bits (`>> 28`), then four 7-bit groups | 32-bit | [srv] |
| GSTRING | 1 + n | GCHAR length then bytes | ≤ 223 bytes | [srv][2.05] |

The server clamps rather than wraps on overflow (GSHORT high byte ≤ 223). Signed values are sent as their unsigned bit pattern.

## Messages

One message = `GCHAR(id)` + payload + `\n`. Several messages are concatenated into one frame. **[srv][2.05]**

The 2.05 sender refuses a payload that already contains `\n`. Binary payloads (board, files) use the raw-data escape below. **[2.05]**

### Raw-data escape

`PLO_RAWDATA` (100, wire `0x84`) carries a GINT3 length. The next *length* bytes are read as one message, newline or not. The server uses it in front of `PLO_BOARDPACKET` (101) and `PLO_FILE` (102). **[srv]** 2.05 handles 100 in its main dispatch table but not 101 or 102. That fits with 101/102 only ever arriving behind 100. **[2.05][inf]**

## Frame

```
u16be length | body
```

- Client to server in 2.05: the body is zlib-deflated. Messages collect in an out buffer, which is compressed and flushed at 0x1000 bytes or on an explicit flush. The 2.05 client links zlib 1.1.2 (Delphi ZLib unit). If more than 256 KB is queued unsent, the client drops the connection. **[2.05]**
- Server to client (gen 2/3): zlib body, no extra byte. **[srv][cap]**
- Gen 4: bz2 body. Gen 5: one compression byte after the length (`0x02` none, `0x04` zlib, `0x06` bz2), then the body. **[srv]**

## Encryption generations (gs2lib numbering)

| Gen | Enum | Used by | Scheme | Tag |
|----:|------|---------|--------|-----|
| 1 | `ENCRYPT_GEN_1` | web client | none, uncompressed | [srv] |
| 2 | `ENCRYPT_GEN_2` | client type 0 with a known token in the first 8 bytes | zlib, no cipher | [srv] |
| 3 | `ENCRYPT_GEN_3` | **2.05**, RC, NC, NPC-server, any type-0 client whose first 8 bytes are not a known token | zlib frame; one junk byte inserted into each message | [srv][2.05] |
| 4 | `ENCRYPT_GEN_4` | client type 4 (2.19–2.21, 3.0–3.01) | bz2, then XOR of the first *limit* dwords | [srv] |
| 5 | `ENCRYPT_GEN_5` | client type 5 (2.22+), RC2 (type 6) | compression byte, then the same partial XOR | [srv] |
| 6 | `ENCRYPT_GEN_6` | v6 | unknown, not implemented | [srv] |

Client-side check (2026-10-21) **[bin]**: 2.17 also sends type 0 with gen-3 insertion, like 2.05. 2.22 and 2.31 send type 5 and use gen 5. The Delphi RemoteControl logs in as type 6 (gen 5), and its NC socket as type 3, which stays zlib with no cipher. The client-side gen-5 send rules (when each compression byte is chosen, XOR word counts) are in `client-versions.md`.

### Gen 3 (2.05)

State: `it` (u32), seeded `0x04A80B38`. Key `k` = 7-bit random value, sent once in the login line. **[2.05]**

Per outgoing message, starting with the **second** message of the session. Only the login line itself is sent clean. The messages that follow it in the same first frame (such as `PLI_LANGUAGE`) already carry the byte. **[2.05][cap]**

1. `it = it * 0x08088405 + k` (mod 2^32).
2. `pos = (it & 0xFFFF) mod len + 1` (1-based; `len` includes the trailing `\n`). `pos` can be 1, which puts the junk byte **before the id byte**, so a decoder must not assume the id is at offset 0 until the byte is removed. **[2.05][cap]**
3. Insert one byte `((it >> 16) & 0x7F) + 0x20` before the 1-based position `pos`.

`pos` can be 1, which puts the junk byte **before the id byte**. A decoder that skips the first byte as "the id" before looking for the junk byte gets that case wrong. Because the inserted byte is never `\n` and `pos` is at most `len`, the byte never lands after the terminating `\n`. **[2.05][cap]**

The server mirrors this: same LCG step, deletes the byte at 0-based `(it & 0xFFFF) mod len`. **[srv]** Here `len` is the line the server split off, which drops the `\n` and keeps the junk byte. That is the same length the client used, so the server's 0-based index is exactly where the client put the byte. GServer-v2 therefore decodes 2.05 correctly, with no tolerance tricks. **[srv][2.05]**

Wire check (lab, three 2.05 sessions): every client→server message after the login line had the expected byte `((it >> 16) & 0x7F) + 0x20` at the predicted index. Several messages had it at index 0, before the id. There were no mismatches. **[cap]** The server's own gen-3 encoder always inserts `)` instead of an iterator-derived byte. That is harmless because the receiver throws the byte away. **[srv]** Gen 3 runs per message *after* decompression, not over the whole frame. **[srv]**

Gen 3 is client→server only. Server→client traffic for a gen-3 client is plain zlib. **[srv][cap]** The 14842/14912 captures stay clear zlib, which matches this.

### Gen 4/5 partial XOR

Same LCG and key. For each 4-byte group, advance `it` and XOR the group with the little-endian bytes of `it`. Stop after *limit* groups: 12 groups for uncompressed bodies, 4 for zlib or bz2. On send the body is compressed first and the XOR is applied to the compressed bytes. On receive the XOR is undone first, then the body is decompressed. **[srv][2.22]**

2.22 client side **[2.22][cap]**:
- **Login frame:** `u16be len` + zlib, with no compression byte and no XOR. The key travels inside it, so it has to be readable.
- **Compression choice for later frames:**
  - Bodies of 0x1000 bytes or more use bz2 (`0x06`).
  - Bodies from 0x30 bytes up use zlib (`0x04`).
  - Bodies under 0x30 bytes are zlib-compressed only when that makes them smaller; otherwise they go uncompressed (`0x02`).
- **Lengths:** the `u16be` length counts the compression byte.
- **Group counting:** a partial last group is XORed byte by byte. For `0x02` the count is `ceil(len/4)` capped at 12. For `0x04`/`0x06` it is `floor(len/4)` capped at 4.
- **Wire check:** a lab 2.22 session decoded completely in both directions with this rule. This is the cipher that makes the 14801 sessions stop inflating after the first frame (2.22/2.31 clients). **[cap][inf]**

## Corrections to earlier notes

- "Some post-login frames are encrypted (Borland LCG)" in CONSOLIDATED.md is gen 4/5. It does not apply to 2.05. 2.05 uses gen 3 (insertion only).
- "First line of a session inserts one extra LCG byte" (crosscheck note): the first line carries the **key**. Insertion starts with the second message.
- The "random prefix" in the login line is the gen-3 key. See `login-and-walk.md`.
- The 0x8088405 / 0x08088405 multiplier is the Borland `Random` LCG constant. 2.05 also uses it in its RTL `Random`. That is a coincidence of the toolchain, not a shared state.

## 2.05 send pipeline (update 2026-10-21) **[2.05]**

1. Build each message as GCHAR id + data + `\n`.
2. From the second message on (every message after the login line, including the rest of the first frame), apply the gen-3 insertion to **this message**, before compression. The byte may land at position 1, before the id.
3. Append it to the out buffer.
4. Flush: zlib-compress the whole buffer (several messages) into one block and prefix it with u16be length. A flush happens at 0x1000 bytes or at the end of the tick. The link is dropped if more than 0x40000 bytes are queued.

Receive is the reverse, with no cipher: u16be → inflate → split on `\n`, with the RAWDATA escape. The receive dispatcher handles 59 ids. Every other id, including 26 and 49–59, hits a silent default.

A separate UDP peer channel is not framed this way; see `udp-p2p.md`.
