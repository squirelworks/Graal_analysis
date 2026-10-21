# Sign text decoding

Date: 2026-10-14

Binary sign text uses **one** packed alphabet. The same encoding is used in `.graal` / `.zelda` sign sections and on the wire (`PLO_LEVELSIGN`). GLEVNW01 text signs are plain text. (An earlier version of this note described a separate "file alphabet" with `char + 89`. That was wrong; see "Correction" below.)

## Encoding

A sign record is `GCHAR x`, `GCHAR y`, then the text bytes. Each text byte is a GCHAR: `byte - 32` is an index into a fixed 97-entry alphabet. The alphabet is the same string in the 2.05 client and in GServer-v2 (`TLevelSign`).

- Codes 0–61: `A`–`Z`, `a`–`z`, `0`–`9`.
- Codes 62–96: punctuation, space (code 89, byte `0x79`) and newline (code 96, byte `0x80`). Several slots in this range are `#` placeholders.
- `#` slots are glyph codes. One or two codes stand for `#` plus a symbol: `#A` `#B` `#X` `#Y` (button icons), `#u` `#d` `#l` `#r` (arrows), `#x` `#y` `#z`, `#h` and `#4` (two codes each), and `#.`. Code 86 is a literal `#`.
- Characters outside the alphabet are written as the escape `#K(n)`, with `n` the decimal character code, spelled out in alphabet codes.
- Bytes under 32 are controls and are not shown.

The editor writes a line break as CRLF: the escape `#K(13)` followed by the newline code (byte `0x80`). In a raw dump, the escape `#K(13)` appears as the bytes `v*eUWf`, followed by a byte with the high bit set. That is why it looked like a "space token". It is a line break.

## Correction

The old notes claimed two alphabets, a `char + 89` file rule with "subtract 6 from A–Z", and `v*eUWf` + high byte = space. All three were wrong. There is one alphabet indexed by `byte - 32`. `+ 89` only looked right for some characters. `v*eUWf` + `0x80` is `#K(13)` + newline. Viewers that drop non-ASCII bytes produce the garbled appearance seen on many house-outside signs. NPC scripts in the same file are plain Latin-1 with `0xA7` as the newline, not sign-encoded.

## Drop-in decoder

`formats/sign-decoder/signText.js` (no dependencies; tests in `test.js` and `vectors.json`, from 11 real signs in GR-V1.03 levels):

- `decodeSignRecord(line)`: takes a raw sign line or a `PLO_LEVELSIGN` payload and returns `{ x, y, text }`.
- `decodeSignText(payload)`: takes the payload after the coordinates. By default the CR from `#K(13)` is dropped.
- `encodeSignText` / `encodeSignRecord`: the reverse.

It is not for GLEVNW01 text signs and not for NPC scripts.

## GLEVNW01 signs

Text signs in a `.nw` file are plain. The SIGN record is `SIGN x y / text / SIGNEND`. The body may be empty. No alphabet transform is required.

## Offline implication

An offline session that already parses SIGN records can display text correctly by:

- Leaving GLEVNW01 signs as plain text.
- Decoding binary signs from `.graal` or `.zelda` files with the alphabet above.

The same decoder covers `PLO_LEVELSIGN` if online mode is added later.
