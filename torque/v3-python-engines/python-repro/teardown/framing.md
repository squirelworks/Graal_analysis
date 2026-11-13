# Framing

Image: Mac PowerPC `Graal` in project `MacGraal_v304`. Addresses are Ghidra VAs. `__TEXT` file offset is VA minus `0x1000`.

Two layers. The Graal record is a text line. The socket flush may wrap one or more lines in a length header and a short XOR.

## Inner record · high

a client routine at an address.

| connection+0x18 | bytes appended to the pending buffer at connection+0x3c |
| --- | --- |
| non-zero | `(id + 0x20)`, `(byte at connection+0x13 + 0x20)`, payload, `0x0A`. Then `+0x18` is cleared |
| zero | `(id + 0x20)`, payload, `0x0A` |

a client routine sets `+0x18` to 1 before the TCP open, so the first record of a session carries the extra byte. The constructor zero-fills the object (a client routine at the start of a client routine). If nothing else writes `+0x13` before that first send, the extra byte is `0x20`. Confidence medium on that byte staying zero. The flag rule itself is high.

If the pending buffer length reaches `0x1000`, a client routine calls the flush a client routine immediately.

a client routine appends exactly one byte. A call with an address stores `0xFF`.

## GCHAR · high

| kind | rule | where |
| --- | --- | --- |
| small | one byte `value + 0x20` | property codec and the record id |
| short string | if `len < 0xE0`: byte `len + 0x20`, then `len` bytes | a client routine cases and a client routine |
| long string | if `len >= 0xE0`: byte `0xFF`, then the first `0xDF` bytes | same |
| 14-bit | if `value > 0x6FFF`, clamp to `0x6FFF`. Then `(value >> 7) + 0x20` and `(value & 0x7F) + 0x20` | cases `0x4E`, `0x4F`, `0x50` of a client routine |
| 21-bit | if `value > 0x37FFFF`, clamp to `0x37FFFF`. Then `(value >> 14) + 0x20`, `((value >> 7) & 0x7F) + 0x20`, `(value & 0x7F) + 0x20` | cases `3`, `0x1F`, `0x4C` |

There is no `0xFE` remapper and no `onSend*` name.

## Inbound consume · high

a client routine at an address walks a buffer while its length is greater than 1.

1. First byte `b`. Logical id is `b - 0x20`.
2. The switch handles ids 0 through 10. Any other id returns and leaves the rest of the buffer.
3. After a handled id, it drops `consumed + 1` bytes.

String fields in cases 8, 9, and 10: the second byte `n` is a length `n - 0x20`, and the slice runs from index 2 through `n - 0x1E` (that is, `length + 2`).

## Outer flush · high on the header, medium on the two transform calls

a client routine at an address. Field `connection+0x14` is the codec mode.

If that field is 0, the mode is chosen from the pending length:

| pending length | mode |
| --- | --- |
| `< 0x30` | 2 |
| `< 0x1000` | 4 |
| otherwise | 6 |

| mode | body |
| --- | --- |
| 1, 2 | copy the pending bytes (mode 1 and 2 share the copy; a cap at a client global applies) |
| 3, 4 | a client routine |
| 5, 6 | a client routine |

a client routine and a client routine were not decompiled. The file contains the literal `inflate 1.1.3 Copyright 1995-1998 Mark Adler` at file offset an address. That string has no code reference. It is not proof that those two calls are inflate.

After the body is built, modes 2, 4, and 6 XOR it:

```
state = state_at_+0x8 * 0x8088405 + word_at_+0x10
```

The 4 key bytes are walked backward from `connection+0x0B`. Mode 2 mixes at most 12 groups of 4 bytes. Modes 4 and 6 mix at most 4 groups.

Then a binary header, not GCHAR:

| `+0x14` before the call | header |
| --- | --- |
| 0 | big-endian `uint16` of `body_size + 1`, then one mode byte, then the body |
| anything else | big-endian `uint16` of `body_size`, then the body |

The header-plus-body is queued in slices of at most 1000 bytes on the list at `connection+0x44`. a client routine writes that list when the socket state at `connection+0x1c + 0x90` equals 2. If `+0x14` was 3, the flush sets it back to 0.

`crypto/packet.c` and `crypto/des.c` (a client routine and the two neighbors) are short null-check paths. They are not this XOR.
