# Sign text decoding

Date: 2026-10-14

Two distinct alphabets exist. Neither is plain Latin-1 for binary signs. GLEVNW01 text signs are plain.

## Network / session sign payload

When a sign arrives on the wire, the payload is decoded by indexing `byte - 0x20` into a fixed alphabet string. The alphabet is long enough to cover the printable range. A `#` character triggers a secondary 14-slot lookup that emits `#` plus one character from the set `ABXYudlrhxyz4`. Bytes under 32 are treated as controls and are not displayed.

This path is used for signs that arrive after a successful world login. An offline session that only loads files never sees it.

## File alphabet (GR-V / Ash)

> **Superseded** by `level-binary-client.md` (Sign text in files): the 2.05 client decodes file signs with the same alphabet as wire signs, and `v*eUWf` + high byte is `#K(13)` plus a newline, not a space. The steps below are kept for history.

Binary sign text stored inside a `.graal` or `.zelda` file is not Latin-1.

Encoding steps observed in the file:

1. The x and y coordinates are each stored as `value + 0x20`.
2. Each subsequent text byte is stored as `char + 89`.
3. Decode: `(b - 89) & 0x7f`, then subtract 6 from A–Z.
4. The six-character token `v*eUWf` followed by a byte with the high bit set is a space.
5. Bytes under 32 are controls.

Viewers that drop non-ASCII characters produce the garbled appearance seen on many house-outside signs. The same file contains NPC scripts that are plain Latin-1 with 0xA7 used as a newline.

## Drop-in decoder

A small decoder exists for the file alphabet:

- `decodeSignRecord(line)` — takes a raw sign line and returns the decoded text.
- `decodeSignText(payload)` — takes the payload after the coordinates.

It is not for GLEVNW01 text signs and not for NPC scripts.

## GLEVNW01 signs

Text signs in a `.nw` file are plain. The SIGN record is `SIGN x y / text / SIGNEND`. The body may be empty. No alphabet transform is required.

## Offline implication

An offline session that already parses SIGN records can display text correctly by:

- Leaving GLEVNW01 signs as plain text.
- Applying the file alphabet to binary signs loaded from `.graal` or `.zelda` files.
- Ignoring the network alphabet unless online mode is later added.

This is sufficient for the offline slice. The network alphabet becomes relevant only when signs arrive on the wire.
