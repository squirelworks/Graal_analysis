# Prop parsers in 5.x, and where 6.x parses its prop strings

Static read, 2026-11-13. Nothing was sent to these clients. **[bin]**

Builds read:

| Build | Image | How it was obtained |
| --- | --- | --- |
| 5.00r7 (`G3D22067`) | `GraalEngine.dll` from the unpacked 5.0.0.7 archive (the unpatched `.bak` copy; the CRC patch changes 8 bytes elsewhere) | as archived |
| 5.12 (`G3D14097`) | the engine DLL that the packed `Graal 5.12.exe` maps at run time (PE date 2007-10-19) | the exe was started under Wine in a network namespace with no outside link, and the mapped image was copied out of the process. The packer leaves only a 2 KB header stub on disk. **[lab]** |
| 5.30r3, 5.31r4 | the unpacked single exes | as archived |
| 6.0.3.7, 6.1.1.3 | the unpacked exes | as archived |

Method: every jump-table switch in the image whose bound is 10, 77, 82 or 83 and whose index is a received id byte minus 32, with the case list split into ids that reach a handler and ids that fall to the switch's default. As a control, the same script on the unpacked 4.20r8 `GraalEngine.dll` gives exactly the four rows already in [v4x-clients.md](v4x-clients.md#prop-parsers).

A "5.12 untouched" copy found in 2026-11 is not a second 5.12 source: its launcher and engine are 5.00r7's, re-versioned and patched ([launcher note](../client-internals/launchers-420r8-500r7-512.md)). The 5.12 row above still rests on the Wine dump alone.

## 5.x: one parser set for the whole era

5.00r7, 5.12, 5.30r3 and 5.31r4 have the same four case sets.

| Stream | Ids with a case | No case | At an id with no case |
| --- | --- | --- | --- |
| self (`PLO_PLAYERPROPS`, 9) | 0–32, 34–49, 52, 54–74, 78–82 | 33, 50, 51, 53, 75–77, and 83 and up | skipped as a one-byte prop (id byte plus one value byte), and parsing goes on, as in 4.x |
| other players (`PLO_OTHERPLPROPS`, 8) | 0, 2, 8–13, 15–21, 23, 24, 30–76, 78–82 | 1, 3–7, 14, 22, 25–29, 77, and 83 and up | the rest of the message is dropped, as in 4.x |
| NPC (`PLO_NPCPROPS`, 3) | 0–47, 53–77 | 48–52, and 78 and up | the rest of the message is dropped |
| baddy (`PLO_BADDYPROPS`, 2) | 0–10 | 11 and up | the rest of the message is dropped |

- **The one change from 4.x is id 82.** Both player streams now accept it. The other-player parser reads one length byte (minus 32) and then that many bytes, and stores the text as a string on the player. The self parser hands 82 to the other-player parser, as it does for the other shared ids. The server header calls 82 `COMMUNITYNAME`; that name is **[srv]**, the string read is **[bin]**.
- **The self parser's default path is the 4.20r8 one.** Its first 120 instructions match 4.20r8's one for one, so an unknown own id is still skipped as one byte, and an unknown id that carries a longer value still desyncs the rest of the message. **[bin][inf]**
- **77 is still not parsed** in 5.x: it ends an other-player stream and is skipped as one byte in self props.
- 5.30r3 and 5.31r4 also hold a 0–82 player-id switch with no received byte behind it. Its no-case list is the 6.x outgoing encoder's in [v6-props.md](v6-props.md#player) except that 3 has a case and the loop ends at 82, so it is read as the 5.3x send side, not a parser. **[bin][inf]**

## 6.x: the parsers are still native

[v6-props.md](v6-props.md) read the four `tclient_set*props` script methods in 6.1.1.3 as storing a string and found no id switch. The switch is one call further in. Each method calls a native parser of the same shape as the 4.x and 5.x ones:

| Script method (6.1.1.3) | Arguments | Calls |
| --- | --- | --- |
| `tclient_setplayerprops` | string | the self parser, on the local player |
| `tclient_setotherplayerprops` | id, string | the other-player parser, on the player with that id |
| `tclient_setnpcprops` (and `tclient_setnpcmove`, same native) | id, string | the NPC parser |
| `tclient_setbaddyprops` | id, string | the baddy parser |

The method names come from the native registration table. Its names are stored scrambled with the length-and-position decoder that [v6x-clients.md](v6x-clients.md) describes: rotate the byte right by two after adding the length and subtracting 246, add the position, and invert. Each entry gives the name, an argument signature (`s`, `is`, …) and the native. **[bin]**

6.0.3.7 has no `tclient_` names. There the native packet switch sends ids 9, 8, 3 and 2 straight to the same four parsers. So 6.0.3.7 parses props natively on receipt, and 6.1.1.3 parses them when the server-defined protocol script passes the prop string to a `tclient_set*props` method. **[bin]**

Case sets in 6.x:

| Stream | 6.0.3.7 | 6.1.1.3 |
| --- | --- | --- |
| self | 0–32, 34–49, 52, 54–74, 77–83; no case for 33, 50, 51, 53, 75, 76 | as 6.0.3.7, but 7 (`BOMBPOWER`) has no case either |
| other players | as 5.x (to 82, no 77) | as 5.x |
| NPC | as 5.x (0–47, 53–77) | as 5.x |
| baddy | 0–10 | 0–10 |

- **77 is parsed in 6.x self props as five bytes.** The handler only sets the value width to 5; nothing is stored. The server header calls 77 `ONLINESECS2`, a five-byte value, so a 6.x client skips it cleanly where 2.x ends the stream. **[bin][srv]**
- **83 is new.** The self parser reads five bytes as one 5-byte number and passes it to a player setter when it is at most 999,999,999. GServer-v2 has no 83. Its meaning is not traced. **[bin]**
- **7 lost its case in 6.1.1.3.** It is still skipped as one byte, which is its width, so a stream with 7 in it stays in step. 6.0.3.7 still applies it (values 1 to 3 set bomb-power flags).
- The self default is the same as in 4.x and 5.x: skip the id plus the current width (one byte unless the case changed it) and go on.

## Open items

- What 83 sets on the player, and which server sends it.
- Whether a real 5.x or 6.x client accepts a long value at an unknown own id without desync (the skip is one byte, so it should not). A lab check needs a 5.x or 6.x client on the wire.
- The per-id value widths of the 5.x and 6.x parsers, beyond the ids named above.
