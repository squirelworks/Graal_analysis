# Packets

Wire byte = `id + 0x20`, then the payload, then `0x0A`, with the first-record exception in `framing.md`. Ids below are the values passed to the sender, not the wire byte.

## Outbound · high where an immediate was recovered

Direct calls of a client routine, plus vtable `+0x0C` calls whose id is an immediate in the decompiler.

| id | wire | site | payload | confidence |
| --- | --- | --- | --- | --- |
| 5 | `0x25` | a client routine an address | `G3D28015`, then string A at a client field, then string B at a client global. Both strings use the short length prefix | high |
| 37 (`0x25`) | `0x45` | a client routine an address | the string at a client global | high on the id, low on the contents |
| 7 | `0x27` | a client routine an address | `G3D30123newmain` on the lister connection | high |
| 1 | `0x21` | a client routine an address | string C at a client global, then string B | high |
| 23 (`0x17`) | `0x37` | a client routine an address | one filename. The name is skipped when it ends in `.gft`. At most four names from each of two lists | medium |
| 34 (`0x22`) | `0x42` | a client routine | a transformed buffer concatenated with the filename | medium |
| 93 (`0x5D`) | `0x7D` | a client routine an address | if the name length is `< 0xE0`: `gchar(len) + name + chunk`. Else `0xFF` and the first `0xDF` name bytes, then the chunk. Chunks are capped near `0x7D00` | medium |
| 155 (`0x9B`) | `0xBB` | a client routine | fired once when a file object starts, before the `0x5D` chunks | low (the object is passed through, layout not walked) |
| 156 (`0x9C`) | `0xBC` | a client routine | fired when that file object finishes | low |

One call of a client routine at an address does not use `li r4`. Its id was not read.

## Inbound, player buffer · high for ids 0–10

a client routine at an address. Logical id = first byte minus `0x20`. Anything else stops the parse.

| id | wire | layout | effect seen in the function |
| --- | --- | --- | --- |
| 0 | `0x20` | one more byte, minus `0x20` | stored at `player+0x40` |
| 1 | `0x21` | one byte, minus `0x20`, scaled through a double | stored as a double at `player+0x45` via vtable `+0x88` |
| 2 | `0x22` | same scale | double at `player+0x47` via vtable `+0x90` |
| 3 | `0x23` | one byte | stored at `+0x3A`. Value 4 sets `+0x39` to 2. Value 6 sets `+0x39` to 4. Value 3 or 4 also loads the image `wbow1.png` |
| 4 | `0x24` | one byte, then an optional string whose length is the next byte minus `0x20` | byte at `+0x3B`. Empty string selects a default from a table indexed by `+0x3A`. The string is passed to a client routine |
| 5 | `0x25` | one byte | value 9 plays `compudead.wav` and sets `player+0x6` to 1. Values 2 and 3 copy neighboring strings and set a counter to `0x14` |
| 6 | `0x26` | one byte | stored at `+0x3D` |
| 7 | `0x27` | one byte | `>> 2` stored at `+0x37`. Low 2 bits stored at `+0x38` |
| 8 | `0x28` | length byte, then that many characters | string copied to `player+0x4F` |
| 9 | `0x29` | same | string copied to `player+0x51` |
| 10 | `0x2A` | same | string copied to `player+0x53` |

Ids 1 and 2 are scaled. The scale constants were not reduced to a plain unit. Do not treat them as tile coordinates.

## Not in this image

No `onSend*` table. No `tclient_` names. `onPlayerLogin` and `onPlayerLogout` exist as strings and have no code references.
