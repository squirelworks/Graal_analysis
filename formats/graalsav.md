# Save games: Graalsav1 to Graalsv11, and the DES-wrapped `.code` / `.gsave` files

Date: 2026-10-21

Covers the clients from 1st Graal (Sept 1998) to 1.32 (Jan 2000).
The notes come from static analysis of the shipped executables. No decompiler output is reproduced.
Field names come from the 13th Graal script variables (`playerrupees`, `playerdarts` …), whose storage lines up with the save record of the same build. Earlier and later builds are matched by position. Names that rest only on position or defaults are marked *inferred*.

## Container

Every version is a Delphi `TWriter` value stream, not a hand-made binary layout.
Each value starts with a one-byte `TValueType` tag:

| Tag | Type | Body |
|---|---|---|
| 2 | Int8 | 1 byte |
| 3 | Int16 | 2 bytes LE |
| 4 | Int32 | 4 bytes LE |
| 5 | Extended | 10-byte x87 float |
| 6 | String | 1-byte length and chars |
| 12 | LString | 4-byte length and chars (strings of 256 bytes or more) |
| 8 / 9 | False / True | none |

`WriteInteger` picks the smallest of Int8, Int16 and Int32, so a reader has to go by the tag.
The first value is always the magic string (`Graalsav1` … `Graalsav9`, `Graalsv10`, `Graalsv11`).

## Versions by build

| Magic | Written by | Read by | Extension | Wrapped |
|---|---|---|---|---|
| Graalsav1 | 1st, 2nd | same | `.save` | no |
| Graalsav2 | 4th alpha, 5th, 5th alpha | same | `.save` | no |
| Graalsav3 | 6th | same | `.save` | no |
| Graalsav4 | 7th, 8th | same | `.save` | no |
| Graalsav5 | 9th alpha to 12th | same | `.save` | no |
| Graalsav6 | 13th | same | `.save` | no |
| Graalsav7 | 14th, 15th | same | `.save` (14th), `.gsave` (15th) | 15th on |
| Graalsav8 | 1.1, 1.1.9 | 7 and 8 | `.gsave` | yes |
| Graalsv11 | 1.21 to 1.41 rev1 (writer traced in 1.21 and 1.32; later builds by string references) | 9, 10 and 11 | `.gsave` | yes |

3rd and 4th Graal reuse Graalsav1 (the 4th alpha was built later than 4th, as the build catalogue notes).
Earlier catalogue rows listed 1.21 to 1.39 as "Graalsav9". Those builds read 9 too, but they write `Graalsv11` and also read `Graalsv10`, and a search for `Graalsav` misses both. The record layout was read from 1.21 and 1.32. In 1.33 to 1.41 rev1 the three magics are referenced the same way as in 1.32 (two references to `Graalsv11`, one each to the readers' `Graalsav9` and `Graalsv10`), so they write `Graalsv11` too, but the record itself was not re-read.
No build in the set writes `Graalsav9` or `Graalsv10`. The v9 and v10 layouts below come only from the 1.21 to 1.32 readers, so they presumably match saves from a 1.2x build that isn't in the archive.
From 15th Graal saving only works on a level from the Cyberjoueur server or on the online start level. From 1.21 the client refuses to save in online mode: "The server saves your game if you have an own account."

## File layout

```
magic                      String
mode                       Integer   0 = one player, 1 = two players, 2 = online, 3/4 = three/four players (14th on)
[mode 2]      String, String         two online-session strings (*inferred*: nickname and server)
player record × n          n = 1, 2, or the player count in 3/4-player modes
[Graalsav2+]  flag list    Integer count, then count × String
```

From `Graalsv11` the header is just `magic`, then `Integer players-1`, then the records and the flag list.

## Player record

### Graalsav1

```
String  level
String  nickname
Float   x
Float   y
Integer dir                    (*inferred*)
Integer fullhearts             (*inferred*)
Float   hearts
Integer rupees
Integer darts                  (default 5)
Integer bombs                  (default 10)
Integer glovepower             (*inferred*, default 2)
4 × Boolean                    (flags; the first defaults to true)
4 × Boolean
4 × Integer colours            (the same four values the relay `S` message sends)
```

### Graalsav2 to Graalsav6

The same start (level, nickname, x, y, dir, fullhearts, hearts, rupees, darts, bombs), and then:

| Field | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| glovepower | ✓ | ✓ | ✓ | ✓ | ✓ |
| shieldpower, swordpower | ✓ | ✓ | ✓ | ✓ | ✓ |
| shootpower | | | ✓ | ✓ | ✓ |
| one Boolean | ✓ | ✓ | | | |
| 5 × Integer colours | ✓ | ✓ | ✓ | ✓ | ✓ |
| Integer headset | ✓ | ✓ | ✓ | ✓ | ✓ |
| horse: String image, Integer bushes | | | | ✓ | ✓ |
| carried NPCs: Integer n, then n × (String image, String script) | | | | ✓ | ✓ |
| trailing Boolean | | | | | ✓ |

The power order in the file is glove, shield, sword, then shoot. The colour count goes from 4 to 5 between Graalsav1 and Graalsav2.

### Graalsav7 and Graalsav8

The same record as Graalsav6. Graalsav8 adds one trailing Integer, and the 1.1.9 loader reads it only when the magic is 8 or above.
The change from 6 to 7 is in the file header (the four-player mode).

### Graalsav9 to Graalsv11 (1.21 to 1.32)

`Graalsv11` is taken from the writer. The `[v9]` / `[v11]` conditions come from the reader.

The player is no longer a list of typed fields. It is one string in the network player-props encoding:

```
String  props          concatenation over prop index i: chr(i+32) + the prop's encoded value
[v9]    String horse image, Integer bushes
Integer n, then n × (String image, String script)        carried / inventory NPCs
[v11]   Integer w, then w × String                        NPC weapon names
[v11]   Integer selected weapon index
```

So the save uses the same props codec as the GServer protocol (`protocol/gserv-1999.md`). A props decoder written for gen-2 packets can read these saves.

## DES-wrapped files

From 5th Graal the client carries a small DES class and two 8-byte keys, `AXBORG15` and `VERGRAAL`.
They protect local files against editing. Nothing on the network is encrypted in these builds.

### `.code` files (5th Graal on)

These are `guildname.code` (behind the `playeringuild` script check) and, in 15th Graal to 1.1.9, `reg.code` (the registration key).

```
24 bytes  DES-ECB(AXBORG15, P)
24 bytes  DES-ECB(VERGRAAL, P)
```

`P` is a 24-byte buffer that holds a Pascal short string (length byte, then up to 23 characters).
The reader decrypts both halves, requires them to be equal, and returns the string. Anything else (a file too short or halves that differ) reads as `###`.
In 15th Graal to 1.1.9 the registration key is also broadcast as relay type `8`, so two players with the same key are noticed.

### `.gsave` (15th Graal on)

```
u32 LE    n = length of the padded plaintext
n bytes   DES-ECB(AXBORG15, plaintext)
n bytes   DES-ECB(VERGRAAL, plaintext)
```

The plaintext is the `TWriter` stream described above, padded to a multiple of 8 with random bytes.
The loader decrypts both copies, compares them byte for byte, and parses the result only if they match.

The DES class takes a second constructor argument (7) whose role hasn't been pinned down. `client-internals/saved-passwords.md` (PR #6, not yet merged; summarised in `client-internals/des-and-hidden-strings.md`) found that the 2.05 DES is textbook DES-ECB with each key byte bit-reversed. The same class name and key handling are probably at work here, so a round-trip test should try `AXBORG15` and `VERGRAAL` bit-reversed first. Before anyone writes a tool for these files, one real save should be round-tripped.
