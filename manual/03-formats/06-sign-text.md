<!-- manual: kind=reference status=complete -->
# 3.6 Sign text alphabets

Binary sign text uses one packed alphabet. The same encoding is used in the sign sections of `.graal` and `.zelda` files (→ §3.1.2.6) and on the wire in `PLO_LEVELSIGN`; GLEVNW01 text signs are plain text [2.05][srv] (formats/sign-text.md).

## 3.6.1 Encoding

Sign text is stored and sent in Graal's own alphabet, not in ASCII. The rules below give the record and the alphabet, code range by code range [2.05][srv] (formats/sign-text.md#encoding).

| Rule | Detail | Source |
| --- | --- | --- |
| record | `GCHAR x`, `GCHAR y`, then the text bytes | [2.05][srv] (formats/sign-text.md#encoding) |
| text byte | a GCHAR: `byte - 32` indexes a fixed 97-entry alphabet, the same string in the 2.05 client and in GServer-v2 | [2.05][srv] (formats/sign-text.md#encoding) |
| codes 0 to 61 | `A`–`Z`, `a`–`z`, `0`–`9` | [2.05][srv] (formats/sign-text.md#encoding) |
| codes 62 to 96 | punctuation, space (code 89, byte `0x79`) and newline (code 96, byte `0x80`); several slots are `#` placeholders | [2.05][srv] (formats/sign-text.md#encoding) |
| glyph codes | one or two codes stand for `#` plus a symbol: `#A` `#B` `#X` `#Y` (button icons), `#u` `#d` `#l` `#r` (arrows), `#x` `#y` `#z`, `#h` and `#4` (two codes each), and `#.`; code 86 is a literal `#` | [2.05][srv] (formats/sign-text.md#encoding) |
| other characters | written as the escape `#K(n)`, with `n` the decimal character code spelled in alphabet codes | [2.05][srv] (formats/sign-text.md#encoding) |
| controls | bytes under 32 are controls and are not shown | [2.05][srv] (formats/sign-text.md#encoding) |
| line break | the editor writes CRLF as `#K(13)` and the newline code; in a raw dump that is the bytes `v*eUWf` and a byte with the high bit set | [test] (formats/sign-text.md#encoding) |
| in the corpus | 2,381 signs in 808 levels, 684 of them at (0, 0) (text kept by index); 498 `#K(n)` escapes with n other than 13, most often 95 (`_`), 164, 61 (`=`), 42 (`*`), 36 (`$`), 64 (`@`), 94 (`^`), 124 (`\|`), 134, 233, 169 and 43 (`+`) | [test] (client-internals/decomp-findings-2026-10-25-f/04-sign-and-chest-details.md) |

The alphabet, from code 0 [2.05] (formats/level-binary-client.md#sign-text-in-files):

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!?-.,#>()#####"####':/~&### <####;\n
```

## 3.6.2 Corrections to earlier notes

Earlier notes decoded signs wrongly. Each row pairs an earlier claim with its correction, so a reader who meets the old reading knows what replaced it [test] (formats/sign-text.md#correction).

| Earlier claim | Correction | Source |
| --- | --- | --- |
| two alphabets, one for files and one for the wire | one alphabet indexed by `byte - 32` | [test] (formats/sign-text.md#correction) |
| a `char + 89` file rule with "subtract 6 from A–Z" | it only looked right for some characters | [test] (formats/sign-text.md#correction) |
| `v*eUWf` + high byte = space | it is `#K(13)` + newline, a line break | [test] (formats/sign-text.md#correction) |
| garbled house-outside signs | viewers that drop non-ASCII bytes produce that appearance | [test] (formats/sign-text.md#correction) |

NPC scripts in the same file are plain Latin-1 with `0xA7` as the newline, not sign-encoded [test] (formats/sign-text.md#correction).

## 3.6.3 GLEVNW01 signs

Signs in a `.nw` level do not use the alphabet. The two rules give the record and its plain text [srv] (formats/sign-text.md#glevnw01-signs).

| Rule | Detail | Source |
| --- | --- | --- |
| record | `SIGN x y`, the text, `SIGNEND`; the body may be empty (→ §3.1.3.3) | [srv] (formats/sign-text.md#glevnw01-signs) |
| text | plain; no alphabet transform | [srv] (formats/sign-text.md#glevnw01-signs) |

## 3.6.4 Reference decoder

The repository has a decoder for the alphabet. The table lists its functions and the test vectors it was checked against [src] (formats/sign-text.md#drop-in-decoder).

| Function | Use | Source |
| --- | --- | --- |
| `decodeSignRecord(line)` | a raw sign line or a `PLO_LEVELSIGN` payload → `{ x, y, text }` | [src] (formats/sign-text.md#drop-in-decoder) |
| `decodeSignText(payload)` | the payload after the coordinates; by default the CR from `#K(13)` is dropped | [src] (formats/sign-text.md#drop-in-decoder) |
| `encodeSignText`, `encodeSignRecord` | the reverse | [src] (formats/sign-text.md#drop-in-decoder) |
| tests | `formats/sign-decoder/test.js` and `vectors.json`, from 11 real signs in GR-V1.03 levels | [test] (formats/sign-text.md#drop-in-decoder) |
