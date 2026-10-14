# Session receive opcodes (cleaned)

Date: 2026-10-14

Derived from observed packet shapes and the public opcode tables. No decompile material.

## Framing reminder

Length-prefixed (u16be) + zlib. After the first login line, most frames are scrambled with the Borland LCG once the session flag is set. The client inserts one scramble byte; the modern server generation-3 codec deletes one byte with the same multiplier.

## Common server → client meanings

| First byte | Meaning |
|------------|---------|
| 0x20 | Level body |
| 0x21 | Link record |
| 0x22 | Computer / NPC-like object |
| 0x24 | Chest |
| 0x25 | Sign (payload then decoded) |
| 0x26 | Set current level name |
| 0x27 | Tile rectangle |
| 0x28 | Other player |
| 0x2E | Spawn (coordinates are (byte-0x20)/2) |
| 0x85 | Level load (raw path) |
| 0x86 | Stream data (raw path, length > 6) |

Many other bytes exist (property updates, combat, flags, file requests). The list above covers the records an offline session already parses from a GLEVNW01 file.

## Login

Selector 0 carries the random prefix + version token + length-biased account and password. Selector 0x25 carries the language string. The version token is eight character immediates, not a string literal.

## Offline implication

An offline session does not need these opcodes. It already loads levels from disk. The table is useful when online mode returns, because the same records (LINK, SIGN, CHEST, level name, tile rectangle) arrive on the wire under these bytes.
