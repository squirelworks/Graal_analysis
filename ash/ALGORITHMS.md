# 39ster 2.1 — algorithms and pseudocode

All numeric fields that go through `CBuffer::writebyte` / `readbyte` / `writebyteN` / `readbyteN` use GCHAR. Frame lengths and the raw tile blob do not.

Integer types below are the C types in the 2006 source (`int` iterator, `char` for many coords). Treat iterator as 32-bit wrapping on `*=` if you port; the original multiplies a signed `int`.

---

## A1 — GCHAR numeric codec

Purpose: keep packet bytes in the printable range (`value + 32` → starts at ASCII space). Multi-byte integers are 7-bit big-endian groups, each biased by +32.

```
function enc1(v):                # writebyte
    emit byte (v + 32) & 0xFF

function dec1(b):                # readbyte
    return (signed char)(b - 32)

function encN(v, n):             # writebyte2/3/4/5
    for i from n-1 down to 0:
        emit byte (((v >> (7*i)) & 0x7F) + 32)

function decN(bytes, n):         # readbyte2/3/4/5
    acc = 0
    for i in 0 .. n-1:
        acc = (acc << 7) + (bytes[i] - 32)
    return acc
```

Widths actually used:

| Helper | Bytes | Shift start | Used for |
|---|---|---|---|
| writebyte | 1 | — | opcodes, most props, coords*2 |
| writebyte2 | 2 | 7 | player id, AP counter, script length |
| writebyte3 | 3 | 14 | rupees, kills, deaths, npc id |
| writebyte4 | 4 | 21 | effect colors (inbound only) |
| writebyte5 | 5 | 28 | file mtime, last-ip, mod-warp mtime |

`writechar` / `readchar` / `addBuffer` write raw octets. Frame length is raw BE u16 (not GCHAR).

Strings are raw: `len = enc1(n); emit n bytes`. Head GIF is special: `enc1(100 + n)` then n bytes of filename. If inbound head length `< 100`, treat it as a classic head index and format `head{n}.gif`.

---

## A4 — PLAYER descramble (drop-one LCG)

Iterator is initialized in `CPlayer::CPlayer` to `0x04A80B38`. `key` is the second GCHAR of the login line.

```
# parseMessage, CLIENTPLAYER only
function descramble(line, iterator, key) -> payload:
    iterator = iterator * 0x8088405 + key
    pos = ((iterator & 0xFFFF) % line.count) + 1     # 1-based
    # drop the byte at index pos-1
    return line[0 .. pos-2] + line[pos .. end]

# CLIENTRC: payload = line unchanged
```

Then `opcode = readbyte(payload)` (GCHAR) and `msgFuncs[opcode](rest)`.

---

## A8 — GR-V1 tile bitstream

Maps are 64×64 tiles. Magic: `"GR-V1.01"` / `"GR-V1.02"` / `"GR-V1.03"`.

- 01 uses 12-bit codes; 02/03 use 13-bit.
- Bitstream decoder with run-length and double-repeat modes.

Full pseudocode and remaining algorithms (outbound/inbound zlib frames, ID generation, board-change persistence notes, etc.) are in the Drive archive `Graal 39sters gServer.zip` under `Ash/ALGORITHMS.md`.

This file captures the critical wire-format and codec details needed to understand or reimplement the 2006 server behavior.
