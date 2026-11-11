<!-- manual: kind=reference status=draft -->
# 3.7 Save games (graalsav)

Clients from 1st Graal (September 1998) to the 1.4x builds write offline save games; from 2.00 the server owns the save [bin] (formats/graalsav.md); [2.05] (client-internals/feature-specs/05-save-load.md#what-it-is). This chapter gives the save container, its revisions, the DES-wrapped local files and the server's account file.

> Status: draft. Field names rest on 13th Graal's script variables; the Graalsav9 and Graalsv10 layouts come only from readers; the DES wrapping has not been round-tripped on a real save.

## 3.7.1 Container

Every revision is a Delphi `TWriter` value stream, not a hand-made binary layout. Each value starts with a one-byte type tag [bin] (formats/graalsav.md#container):

| Tag | Type | Body | Source |
| --- | --- | --- | --- |
| 2 | Int8 | 1 byte | [bin] (formats/graalsav.md#container) |
| 3 | Int16 | 2 bytes, little-endian | [bin] (formats/graalsav.md#container) |
| 4 | Int32 | 4 bytes, little-endian | [bin] (formats/graalsav.md#container) |
| 5 | Extended | 10-byte x87 float | [bin] (formats/graalsav.md#container) |
| 6 | String | 1-byte length and the characters | [bin] (formats/graalsav.md#container) |
| 12 | LString | 4-byte length and the characters; strings of 256 bytes or more | [bin] (formats/graalsav.md#container) |
| 8, 9 | False, True | none | [bin] (formats/graalsav.md#container) |

A save file is a list of tagged values. The rules below say how to read the tags and where the field names come from [bin] (formats/graalsav.md#container).

| Rule | Detail | Source |
| --- | --- | --- |
| integer width | the writer picks the smallest of Int8, Int16 and Int32, so a reader must go by the tag | [bin] (formats/graalsav.md#container) |
| first value | always the magic string: `Graalsav1` to `Graalsav9`, `Graalsv10`, `Graalsv11` | [bin] (formats/graalsav.md#container) |
| field names | taken from 13th Graal's script variables (`playerrupees`, `playerdarts` …), whose storage lines up with that build's save record; other builds are matched by position | [bin] (formats/graalsav.md) |

## 3.7.2 Revisions by build

The save format was revised many times. Each row gives one magic, the builds that write and read it, the file extension, and whether it is DES-wrapped [bin] (formats/graalsav.md#versions-by-build).

| Magic | Written by | Read by | Extension | DES-wrapped | Source |
| --- | --- | --- | --- | --- | --- |
| Graalsav1 | 1st, 2nd, 3rd, 4th | same | `.save` | no | [bin] (formats/graalsav.md#versions-by-build) |
| Graalsav2 | 4th alpha, 5th, 5th alpha | same | `.save` | no | [bin] (formats/graalsav.md#versions-by-build) |
| Graalsav3 | 6th | same | `.save` | no | [bin] (formats/graalsav.md#versions-by-build) |
| Graalsav4 | 7th, 8th | same | `.save` | no | [bin] (formats/graalsav.md#versions-by-build) |
| Graalsav5 | 9th alpha to 12th | same | `.save` | no | [bin] (formats/graalsav.md#versions-by-build) |
| Graalsav6 | 13th | same | `.save` | no | [bin] (formats/graalsav.md#versions-by-build) |
| Graalsav7 | 14th, 15th | same | `.save` (14th), `.gsave` (15th) | from 15th | [bin] (formats/graalsav.md#versions-by-build) |
| Graalsav8 | 1.1, 1.1.9 | 7 and 8 | `.gsave` | yes | [bin] (formats/graalsav.md#versions-by-build) |
| Graalsav9, Graalsv10 | no build in the set | 1.21 to 1.32 readers | `.gsave` | yes | [bin] (formats/graalsav.md#versions-by-build) |
| Graalsv11 | 1.21 to 1.41 rev 1; writer traced in 1.21 and 1.32, later builds by string references | 9, 10 and 11 | `.gsave` | yes | [bin] (formats/graalsav.md#versions-by-build) |

The rules below explain the odd steps in that table and correct an earlier catalogue entry [bin] (formats/graalsav.md#versions-by-build).

| Rule | Detail | Source |
| --- | --- | --- |
| 4th alpha | built later than 4th, which is why it writes the newer revision | [bin] (formats/graalsav.md#versions-by-build) |
| 1.33 to 1.41 rev 1 | reference the three magics as 1.32 does (two references to `Graalsv11`, one each to `Graalsav9` and `Graalsv10`), so they write `Graalsv11`; the record itself was not re-read | [bin] (formats/graalsav.md#versions-by-build) |
| catalogue correction | earlier catalogue rows listed 1.21 to 1.39 as "Graalsav9"; a search for `Graalsav` misses `Graalsv10` and `Graalsv11` | [bin] (formats/graalsav.md#versions-by-build) |
| v9 and v10 | presumably match saves from a 1.2x build that is not in the archive | [inf] (formats/graalsav.md#versions-by-build) |
| 15th Graal | saving only works on a level from one named community server or on the online start level | [bin] (formats/graalsav.md#versions-by-build) |
| 1.21 on | the client refuses to save online: "The server saves your game if you have an own account." | [bin] (formats/graalsav.md#versions-by-build) |
| 2.00 on | the server owns the save; 2.05 contains "Save games are not supported anymore", and the offline F2/F3 save games ended with 1.41 | [2.05] (client-internals/feature-specs/05-save-load.md#what-it-is) |

## 3.7.3 File layout

```
magic                      String
mode                       Integer   0 one player, 1 two players, 2 online, 3/4 three/four players (14th on)
[mode 2]      String, String         two online-session strings
player record × n          n = 1, 2, or the player count in 3/4-player modes
[Graalsav2+]  flag list    Integer count, then count × String
```

| Rule | Detail | Source |
| --- | --- | --- |
| layout | as above | [bin] (formats/graalsav.md#file-layout) |
| online strings | nickname and server | [inf] (formats/graalsav.md#file-layout) |
| Graalsv11 header | `magic`, then `Integer players-1`, then the records and the flag list | [bin] (formats/graalsav.md#file-layout) |
| 6 to 7 | the change is in the header: the four-player mode | [bin] (formats/graalsav.md#graalsav7-and-graalsav8) |

## 3.7.4 Player record

### 3.7.4.1 Graalsav1

The first revision is the simplest. The table gives its fields in file order with their types. Rows tagged as inferred have a field whose meaning is not read directly [bin] (formats/graalsav.md#graalsav1).

| Order | Type | Field | Source |
| --- | --- | --- | --- |
| 1 | String | level | [bin] (formats/graalsav.md#graalsav1) |
| 2 | String | nickname | [bin] (formats/graalsav.md#graalsav1) |
| 3, 4 | Float | x, y | [bin] (formats/graalsav.md#graalsav1) |
| 5 | Integer | dir | [inf] (formats/graalsav.md#graalsav1) |
| 6 | Integer | fullhearts | [inf] (formats/graalsav.md#graalsav1) |
| 7 | Float | hearts | [bin] (formats/graalsav.md#graalsav1) |
| 8 | Integer | rupees | [bin] (formats/graalsav.md#graalsav1) |
| 9 | Integer | darts, default 5 | [bin] (formats/graalsav.md#graalsav1) |
| 10 | Integer | bombs, default 10 | [bin] (formats/graalsav.md#graalsav1) |
| 11 | Integer | glovepower, default 2 | [inf] (formats/graalsav.md#graalsav1) |
| 12 | 4 × Boolean | flags; the first defaults to true | [bin] (formats/graalsav.md#graalsav1) |
| 13 | 4 × Boolean | flags | [bin] (formats/graalsav.md#graalsav1) |
| 14 | 4 × Integer | colours, the same four values the relay `S` message sends (→ §2.3.1) | [bin] (formats/graalsav.md#graalsav1) |

### 3.7.4.2 Graalsav2 to Graalsav8

The record starts as Graalsav1 (level, nickname, x, y, dir, fullhearts, hearts, rupees, darts, bombs), then [bin] (formats/graalsav.md#graalsav2-to-graalsav6):

| Field | 2 | 3 | 4 | 5 | 6, 7, 8 | Source |
| --- | --- | --- | --- | --- | --- | --- |
| Integer glovepower | yes | yes | yes | yes | yes | [bin] (formats/graalsav.md#graalsav2-to-graalsav6) |
| Integer shieldpower, swordpower | yes | yes | yes | yes | yes | [bin] (formats/graalsav.md#graalsav2-to-graalsav6) |
| Integer shootpower | n/a | n/a | yes | yes | yes | [bin] (formats/graalsav.md#graalsav2-to-graalsav6) |
| one Boolean | yes | yes | n/a | n/a | n/a | [bin] (formats/graalsav.md#graalsav2-to-graalsav6) |
| 5 × Integer colours | yes | yes | yes | yes | yes | [bin] (formats/graalsav.md#graalsav2-to-graalsav6) |
| Integer headset | yes | yes | yes | yes | yes | [bin] (formats/graalsav.md#graalsav2-to-graalsav6) |
| horse: String image, Integer bushes | n/a | n/a | n/a | yes | yes | [bin] (formats/graalsav.md#graalsav2-to-graalsav6) |
| carried NPCs: Integer n, then n × (String image, String script) | n/a | n/a | n/a | yes | yes | [bin] (formats/graalsav.md#graalsav2-to-graalsav6) |
| trailing Boolean | n/a | n/a | n/a | n/a | yes | [bin] (formats/graalsav.md#graalsav2-to-graalsav6) |
| trailing Integer | n/a | n/a | n/a | n/a | 8 only; the 1.1.9 loader reads it only when the magic is 8 or above | [bin] (formats/graalsav.md#graalsav7-and-graalsav8) |

The power order in the file is glove, shield, sword, then shoot; the colour count goes from 4 to 5 between Graalsav1 and Graalsav2 [bin] (formats/graalsav.md#graalsav2-to-graalsav6).

### 3.7.4.3 Graalsav9 to Graalsv11

The player is one string in the network player-props encoding [bin] (formats/graalsav.md#graalsav9-to-graalsv11-121-to-132):

```
String  props          concatenation over prop index i: chr(i+32) + the prop's encoded value
[v9]    String horse image, Integer bushes
Integer n, then n × (String image, String script)        carried and inventory NPCs
[v11]   Integer w, then w × String                        NPC weapon names
[v11]   Integer selected weapon index
```

| Rule | Detail | Source |
| --- | --- | --- |
| sources | `Graalsv11` is from the writer; the `[v9]` and `[v11]` conditions are from the reader | [bin] (formats/graalsav.md#graalsav9-to-graalsv11-121-to-132) |
| props codec | the same as the generation 2 protocol (→ App. B); a props decoder for generation 2 messages reads these saves | [bin] (formats/graalsav.md#graalsav9-to-graalsv11-121-to-132) |

## 3.7.5 DES-wrapped local files

From 5th Graal the client carries a small DES class and two 8-byte keys, `AXBORG15` and `VERGRAAL`. They protect local files against editing; nothing on the network is encrypted in these builds [bin] (formats/graalsav.md#des-wrapped-files).

### 3.7.5.1 `.code` files (5th Graal on)

```
24 bytes  DES-ECB(AXBORG15, P)
24 bytes  DES-ECB(VERGRAAL, P)
```

| Rule | Detail | Source |
| --- | --- | --- |
| files | `guildname.code` (behind the `playeringuild` script check); in 15th Graal to 1.1.9 also `reg.code`, the registration key | [bin] (formats/graalsav.md#code-files-5th-graal-on) |
| `P` | a 24-byte buffer holding a Pascal short string: a length byte, then up to 23 characters | [bin] (formats/graalsav.md#code-files-5th-graal-on) |
| reader | decrypts both halves, requires them to be equal, and returns the string; a short file or differing halves read as `###` | [bin] (formats/graalsav.md#code-files-5th-graal-on) |
| key broadcast | in 15th Graal to 1.1.9 the registration key is also sent as relay type `8`, so two players with the same key are noticed (→ §2.3.1) | [bin] (formats/graalsav.md#code-files-5th-graal-on) |

### 3.7.5.2 `.gsave` (15th Graal on)

```
u32le     n = length of the padded plaintext
n bytes   DES-ECB(AXBORG15, plaintext)
n bytes   DES-ECB(VERGRAAL, plaintext)
```

| Rule | Detail | Source |
| --- | --- | --- |
| plaintext | the `TWriter` stream of §3.7.1, padded to a multiple of 8 with random bytes | [bin] (formats/graalsav.md#gsave-15th-graal-on) |
| loader | decrypts both copies, compares them byte for byte, and parses only if they match | [bin] (formats/graalsav.md#gsave-15th-graal-on) |
| DES variant | the class takes a second constructor argument (7) whose role is not pinned down; the 2.05 DES is textbook DES-ECB with each key byte bit-reversed, and the same handling is probably at work here, so a round trip should try the keys bit-reversed first | [inf] (formats/graalsav.md#gsave-15th-graal-on) |
| open | no real save has been round-tripped | [bin] (formats/graalsav.md#gsave-15th-graal-on) |

### 3.7.5.3 Saved passwords (1.3 test to 2.22)

The client saves account passwords in the registry under `HKEY_CURRENT_USER\Software\Graal\Client`, as `password` and as `<account>:pass` per account [2.05] (client-internals/saved-passwords.md#warning-for-anyone-holding-old-installs).

| Rule | Detail | Source |
| --- | --- | --- |
| cipher | DES-ECB with standard tables, each key byte bit-reversed before the key schedule; the same routine as the `.gsave` DES | [2.05][test] (client-internals/saved-passwords.md#cipher) |
| key | one fixed 8-byte key, the same in every copy of the client, so a saved value is as good as plain text to anyone who can read the registry or an export of it | [2.05] (client-internals/saved-passwords.md#warning-for-anyone-holding-old-installs) |
| builds | the same key and form from 1.3 test (Nov 1999) to 2.05; a value saved by 1.31 or 1.32 in the lab decrypts the same way | [test] (client-internals/saved-passwords.md#warning-for-anyone-holding-old-installs) |
| encrypt | cut the plaintext to 23 bytes; build 24 bytes: the length, the text, random padding; encrypt as three DES blocks; write each byte as two characters `(b >> 4) + 0x20`, `(b & 0x0F) + 0x20` | [2.05] (client-internals/saved-passwords.md#string-format-48-characters) |
| decrypt | input under 48 characters, or a first decrypted byte of 0 or 24 and above, gives an empty string | [2.05] (client-internals/saved-passwords.md#string-format-48-characters) |
| same text, new value | the random padding makes every save of the same password differ | [2.05] (client-internals/saved-passwords.md#string-format-48-characters) |
| opting out | "Don't save the passwords" in More Options deletes the values when the client closes | [2.05] (client-internals/saved-passwords.md#warning-for-anyone-holding-old-installs) |
| 2.22 | a 49-character value that starts with a marker character is decrypted with a second key held by the options form; any other value with the first key, so old saves still load; new saves use the marker and the second key | [2.22] (client-internals/des-and-hidden-strings.md#des-saved-passwords-and-the-web-cache-pointers) |
| 2.22 account name | stored with the byte transform of the login (→ §2.3.3) | [2.22] (client-internals/des-and-hidden-strings.md#des-saved-passwords-and-the-web-cache-pointers) |
| other uses | 2.05 builds its hidden listserver host the same way, from a key and a 48-character text assembled one character at a time (→ §6.1.1); the web-level cache uses the same DES with per-block keys (→ §3.8) | [2.05][cap] (client-internals/des-and-hidden-strings.md#hidden-strings); [2.05] (client-internals/saved-passwords.md#other-uses-of-the-same-cipher) |
| what it protects | nothing; these schemes only keep the strings out of a casual string dump | [inf] (client-internals/des-and-hidden-strings.md#notes-for-tool-writers) |

## 3.7.6 Server account file (GRACC001)

From 2.00 the save is the server's account file; the client receives it as its login burst (→ §2.3) [srv] (client-internals/feature-specs/05-save-load.md#what-it-is).

| Rule | Detail | Source |
| --- | --- | --- |
| file | `accounts/<name>.txt`; text, first line `GRACC001`, then `KEY value` lines, CRLF on write | [srv] (client-internals/feature-specs/05-save-load.md#server-file-gracc001-accountsnametxt-srv) |
| player keys | NAME, NICK (at most 223 characters), COMMUNITYNAME, LEVEL, X, Y, Z, MAXHP, HP, RUPEES, ANI, ARROWS, BOMBS, GLOVEP, SHIELDP, SWORDP, BOWP, BOW, HEAD, BODY, SWORD, SHIELD, COLORS (5 comma-separated), SPRITE, STATUS, MP, AP, APCOUNTER, ONSECS, IP, LANGUAGE, KILLS, DEATHS, RATING, DEVIATION, LASTSPARTIME | [srv] (client-internals/feature-specs/05-save-load.md#server-file-gracc001-accountsnametxt-srv) |
| repeated keys | FLAG (`name=value`), ATTR1 to ATTR30, WEAPON, CHEST (an `x:y:level` style string) | [srv] (client-internals/feature-specs/05-save-load.md#server-file-gracc001-accountsnametxt-srv) |
| admin keys | BANNED, BANREASON, BANLENGTH, COMMENTS, EMAIL, LOCALRIGHTS, IPRANGE, LOADONLY, FOLDERRIGHT (repeated), LASTFOLDER | [srv] (client-internals/feature-specs/05-save-load.md#server-file-gracc001-accountsnametxt-srv) |
| new account | the server clones `accounts/defaultaccount.txt`, applies `startlevel`, `startx` and `starty` from the server options if set, and saves the new file | [srv] (client-internals/feature-specs/05-save-load.md#server-file-gracc001-accountsnametxt-srv) |
| guest | load-only, with a random `pc:` community name | [srv] (client-internals/feature-specs/05-save-load.md#server-file-gracc001-accountsnametxt-srv) |
| saving | on disconnect for accounts that are not load-only, and every 300 s while connected; not saved if the listserver login failed | [srv] (client-internals/feature-specs/05-save-load.md#server-file-gracc001-accountsnametxt-srv) |

The client's other local files from 2.00 on are its config files (→ §3.9) and the web-level cache (→ §3.8) [2.05] (client-internals/feature-specs/05-save-load.md#what-it-is).
