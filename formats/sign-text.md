# Sign text decoding

Date: 2026-10-14

Two distinct alphabets exist. Neither is plain Latin-1 for binary signs.

## Network / session sign payload

When a sign arrives on the wire, the payload is indexed by `byte - 0x20` into a fixed alphabet string. A `#` character triggers a secondary lookup that emits `#` plus one of `ABXYudlrhxyz4`. Bytes under 32 are controls.

## File alphabet (GR-V / Ash)

Binary sign text stored inside a `.graal` or `.zelda` file is not Latin-1.

- After the x,y pair (each already minus 0x20), each byte is `char + 89`.
- Decode: `(b - 89) & 0x7f`, then A–Z minus 6.
- The token `v*eUWf` plus 0x80 is a space.
- Bytes under 32 are controls.
- Viewers that drop non-ASCII produce the garbled appearance seen on many house-outside signs.
- NPC scripts in the same file are plain Latin-1 with 0xA7 newlines.

## Drop-in

A small decoder (`decodeSignRecord` / `decodeSignText`) exists for the file alphabet. It is not for GLEVNW01 text signs or for NPC scripts.

## Offline implication

An offline session that already parses SIGN records can display the text correctly once it applies the file alphabet to binary signs and leaves GLEVNW01 signs as plain text.
