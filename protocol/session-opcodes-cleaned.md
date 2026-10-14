# Session receive opcodes (cleaned)

Date: 2026-10-14

Derived from observed packet shapes, public opcode tables, and capture notes. No decompile material.

## Framing

Every payload is a 16-bit big-endian length followed by that many bytes. Zlib bodies begin with `78 9c` or `78 da`. After the first login line, most frames are scrambled with the Borland LCG once a session flag is set. The client inserts one scramble byte on send; the modern server generation-3 codec deletes one byte with the same multiplier (`0x8088405`).

The list client and the world client share the same flush path for the zlib frame.

## Common server → client meanings

| First byte | Meaning | Offline equivalent |
|------------|---------|-------------------|
| 0x20 | Level body | BOARD data |
| 0x21 | Link record | LINK |
| 0x22 | Computer / NPC-like object | NPC |
| 0x24 | Chest | CHEST |
| 0x25 | Sign (payload then decoded) | SIGN |
| 0x26 | Set current level name | level filename |
| 0x27 | Tile rectangle | BOARD modify |
| 0x28 | Other player | — |
| 0x2E | Spawn (coordinates are (byte-0x20)/2) | player start |
| 0x85 | Level load (raw path) | full level load |
| 0x86 | Stream data (raw path, length > 6) | file or cache stream |

Many other bytes exist (property updates, combat, flags, file requests, RC staff commands). The list above covers the records an offline session already parses from a GLEVNW01 file.

Coordinates on the wire are frequently stored as `byte - 0x20`. Spawn uses `(byte - 0x20) / 2`.

## Login

Selector 0 carries the random printable prefix `(rand & 0x7F) + 0x20`, the eight-character version token, and the length-biased account and password. Selector 0x25 carries the language string (“English” in the observed case).

The version token is built from eight character immediates, not a string literal. `GNW03081` is the v2.05 token. The server maps it to CLVER_2_052.

## Offline implication

An offline session does not need these opcodes. It already loads levels from disk and applies the same records. The table is useful when online mode returns, because the same LINK, SIGN, CHEST, level name, and tile rectangle records arrive on the wire under these bytes. Wiring the offline parsers to also accept the wire form is then a thin adapter.
