# Session receive opcodes (cleaned)

Date: 2026-10-14, revised 2026-10-21

Derived from observed packet shapes, public opcode tables, and capture notes. No decompile material.

## Framing

Every frame is a 16-bit big-endian length followed by that many bytes. Zlib bodies begin with `78 9c` or `78 da`. For 2.05 (gen 3), the **client** inserts one junk byte into each message after the login line, and server→client messages are plain zlib. The insertion rule is in `codec-and-framing.md`. Full-frame XOR applies only to gen 4/5 clients (2.19+).

The list client and the world client share the same zlib flush path. Only the world client adds the gen-3 insertion. **[2.05]**

## Common server → client meanings

| First byte | Meaning | Offline equivalent |
|------------|---------|-------------------|
| 0x20 | `PLO_LEVELBOARD` (0): cached-board marker or board changes | BOARD data |
| 0x21 | `PLO_LEVELLINK` (1) | LINK |
| 0x22 | `PLO_BADDYPROPS` (2), a "compu" (baddy) | BADDY |
| 0x23 | `PLO_NPCPROPS` (3) | NPC |
| 0x24 | `PLO_LEVELCHEST` (4) | CHEST |
| 0x25 | `PLO_LEVELSIGN` (5): x, y, then sign alphabet | SIGN |
| 0x26 | `PLO_LEVELNAME` (6) | level filename |
| 0x27 | `PLO_BOARDMODIFY` (7): GCHAR x/y/w/h + GSHORT tiles | BOARD modify |
| 0x28 | `PLO_OTHERPLPROPS` (8) | — |
| 0x2E | `PLO_PLAYERWARP` (14): x×2, y×2, level | player start |
| 0x84 | `PLO_RAWDATA` (100): GINT3 length of the next raw message | — |
| 0x85 | `PLO_BOARDPACKET` (101), behind 0x84: 8192 bytes of raw LE u16 tiles | full level load |
| 0x86 | `PLO_FILE` (102), behind 0x84: name + bytes | file or cache stream |

Many other bytes exist. The full table, with 2.05 coverage, is in `packet-ids.md`, and layouts are in `packet-layouts.md`. The list above covers the records an offline session already parses from a GLEVNW01 file.

Coordinates on the wire are frequently stored as `byte - 0x20`. Spawn uses `(byte - 0x20) / 2`.

## Login

The first message is GCHAR client type 0, GCHAR key (`rand & 0x7F`), the eight-character token `GNW03081`, then the account and password as GSTRINGs. The "random printable prefix" is the gen-3 key. The next message is `PLI_LANGUAGE` (37, wire 0x45), carrying the language string. Details are in `login-and-walk.md`.

The token is built from eight character immediates, not a string literal. Current gs2lib maps `GNW03081` to `CLVER_2_052`, which sorts below `CLVER_2_1`.

## Offline implication

An offline session does not need these opcodes. It already loads levels from disk and applies the same records. The table is useful when online mode returns, because the same LINK, SIGN, CHEST, level name, and tile rectangle records arrive on the wire under these bytes. Wiring the offline parsers to also accept the wire form is then a thin adapter.
