# Properties

The outbound codec is a client routine at an address. It switches on a numeric property id and appends GCHAR to a buffer. This is not the inbound switch in `packets.md`. Those two functions do not share a case list.

a client routine calls the codec in a loop. When `player+0x194` and `player+0x74` are both zero it walks five ids from the table at a client global, then one more. Otherwise it walks eight ids from a client global. The table slots are pointers in a zero-filled data segment here, so the id numbers in those tables were not read. Confidence high that the loop exists, low on which ids it emits at runtime.

## Ids with a name in the function · high

| id | encoding | what the case does |
| --- | --- | --- |
| 0 | string, capped at 200, then `len + 0x20` and the bytes | field at `player+0xB1` |
| 8 | one byte, or a long image name | sword. Image names `sword1.` `sword2.` `sword3.` `sword4.` become 1–4. The raw field is biased by `+0x1E`, clamped to 10–`0x32`, and `0x1E` becomes 0. A value `>= 10` appends the image string under the `0xE0` rule |
| 9 | one byte, or a long image name | shield. `shield1.` `shield2.` `shield3.` become 1–3. Bias `+10`, clamp 10–`0x0D`, and 10 becomes 0 |
| 11 (`0x0B`) | one byte, or a name | head. The literal `head` is searched inside the image name. A long name uses length byte `len - 0x7C` (the decompiler writes `cVar8 + -0x7c`) and caps the name at 100 |

## Ids whose encoding is visible and whose field is not named · high on the encoding

| ids | encoding |
| --- | --- |
| 1, 4, 5, 6 | one byte `field + 0x20` |
| 2 | one byte from a client routine |
| 3 | 21-bit, clamp `0x37FFFF`, field `player+0xA9` |
| 7 | the constant `0x2A` is fed to the one-byte writer |
| 10, 12 (`0x0C`) | string, `0xE0` rule. Case 10 joins two fields with a comma when both are non-empty. Case 12 caps at 200 |
| 13 (`0x0D`) | a run of one-byte values |
| `0x1F`, `0x4C` | 21-bit |
| `0x2A` | a flag byte `(field == 0) + 0x20`, then a 21-bit value |
| `0x4E`, `0x4F`, `0x50` | 14-bit, clamp `0x6FFF` |
| `0x20`, `0x21`, `0x23`, `0x25`–`0x29`, `0x2B`, `0x2E`–`0x31`, `0x34`, `0x35`–`0x4A`, `0x4B` | one-byte or short-string cases are present. Individual fields were not named |

Case labels that are absent, so those ids are not encoded here: `0x19`, `0x1B`–`0x1E`, `0x22`, `0x24`, `0x32`, `0x33`, `0x4D`.

## NPC and baddy · medium

The level loader a client routine has section names `NPC` and `BADDY` and allocates an object for each (`0xC0` bytes for one of them, `0x90` for the other). It does not show a property-id stream for those objects. Script names that sit in the GS1 function include `hurt`, `carryobject`, `canbepushed`, `canbepulled`. Those are script words, not wire ids.

No `account,alpha,ani` registry is in this image.
