# Prop parsers in 5.x, and where 6.x parses its prop strings

Static read, 2026-11-13. Nothing was sent to these clients. **[bin]**

Builds read:

| Build | Image | How it was obtained |
| --- | --- | --- |
| 5.00r7 (`G3D22067`) | `GraalEngine.dll` from the unpacked 5.0.0.7 archive (the unpatched `.bak` copy; the "CRC patch" changes 8 bytes elsewhere, a license-file check bypass, see [launcher note](../client-internals/launchers-420r8-500r7-512.md#its-engine-is-the-500r7-engine-patched)) | as archived |
| 5.12 (`G3D14097`) | the engine DLL that the packed `Graal 5.12.exe` maps at run time (PE date 2007-10-19) | the exe was started under Wine in a network namespace with no outside link, and the mapped image was copied out of the process. The packer leaves only a 2 KB header stub on disk. **[lab]** |
| 5.30r3, 5.31r4 | the unpacked single exes | as archived |
| 6.0.3.7, 6.1.1.3 | the unpacked exes | as archived |

Method: every jump-table switch in the image whose bound is 10, 77, 82 or 83 and whose index is a received id byte minus 32, with the case list split into ids that reach a handler and ids that fall to the switch's default. As a control, the same script on the unpacked 4.20r8 `GraalEngine.dll` gives exactly the four rows already in [v4x-clients.md](v4x-clients.md#prop-parsers).

A "5.12 untouched" copy found in 2026-11 is not a second 5.12 source: its launcher and engine are 5.00r7's, re-versioned and patched ([launcher note](../client-internals/launchers-420r8-500r7-512.md)). The genuine 5.12 engine is `Graal3DEngine.dll` (5.12 ships no `GraalEngine.dll`). Its on-disk file, taken from the MoleBox bundle, gives the same four case sets as the run-time image read here ([launcher note](../client-internals/launchers-420r8-500r7-512.md#the-genuine-512-engine)). **[bin]**

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
- **83 is new, and it is the gralat count in five bytes.** The self parser reads five bytes as one 5-byte number and, when it is at most 999,999,999, passes it to the same player setter that 3 (`RUPEESCOUNT`, three bytes) calls. See [83: a wide gralat count](#83-a-wide-gralat-count). GServer-v2 has no 83. **[bin]**
- **7 lost its case in 6.1.1.3.** It is still skipped as one byte, which is its width, so a stream with 7 in it stays in step. 6.0.3.7 still applies it (values 1 to 3 set bomb-power flags).
- The self default is the same as in 4.x and 5.x: skip the id plus the current width (one byte unless the case changed it) and go on.

### 83: a wide gralat count

Date: 2026-11-18. Static read of unpacked Windows 6.03r7 and the Linux x86-64 6.03 build. Nothing was run. **[bin]**

- **Same setter as 3.** In both builds the self parser's case for 3 reads a three-byte number and the case for 83 reads a five-byte number. Each one calls the same virtual method on the local player, with the same "below 1,000,000,000" test in front of it. No other self-prop case calls that method. **[bin]**
- **That method is the gralat setter.** The item pickup routine uses the same getter and setter pair for item 19 (`goldrupee`): it reads the value, adds 100 and writes it back. Right after any pickup it clamps that value to 999,999,999, beside the 99 caps on arrows (4) and bombs (5). The symbol table of the Mac 6.11 build names the getter on the player class `getGralats`. **[bin]**
- **So 83 sets the player's gralats.** It carries the same value as 3 in a wider encoding: three 7-bit groups hold at most 2,097,151, and five hold the full 999,999,999 the client allows. The 999,999,999 test is the client's gralat ceiling, the same one pickups clamp to, not a separate field. **[bin][inf]**
- **Receive-only.** The outgoing player encoder has no case for 83 (nor for 3), the other-player parser stops at it, and NPC and baddy streams do not use it. A server sets a player's own gralats with 83; other players never see it. **[bin]**
- **Name.** No server header in the materials names it. The gserver prop table that lists it calls it `UNKNOWN83` ([unknown-ids-2026-11-06.md](unknown-ids-2026-11-06.md)). A working name is `RUPEESCOUNT2`, following `ONLINESECS2` (77), the five-byte form of an older counter. **[inf]**
- **Other builds.** 6.1.1.3 has the same case set (above); its setter was not re-traced in this pass. 4.x and 5.x skip 83 as one byte, so a server should send gralats above 2,097,151 to them as 3, clamped. No mobile prop parser has been read, so whether iPhone or Android clients parse 83 is open. **[bin][inf]**
- **Checked at runtime (2026-11-18):** a lab server sent 83 to a Linux 6.03r7 client: 1234 and 999,999,999 set the gralat counter, 1,000,000,000 was ignored, and the next prop parsed after five bytes ([probe-targets-2026-11-18.md](probe-targets-2026-11-18.md)). **[lab]**

## Open items

- [x] ~~What 83 sets on the player.~~ The gralat count, as a five-byte value ([above](#83-a-wide-gralat-count)), lab-confirmed on 6.03r7 ([probe-targets-2026-11-18.md](probe-targets-2026-11-18.md)). Which real server sent it is still unknown.
- Whether iPhone or Android clients parse own prop 83.
- ~~Whether a real 5.x or 6.x client accepts a long value at an unknown own id without desync.~~ 6.03r7 does not: a three-byte value at an unknown id loses the rest of that message, and the next message parses normally (lab, 2026-11-18). 5.x is not checked yet.
- 6.03r7 lab widths (2026-11-18): 77 five bytes, 78–80 two bytes (`X2`, `Y2`, `Z2`), 81 one byte, 82 string, 83 five bytes.
- The per-id value widths of the 5.x parsers. ~~6.x~~: on 6.03r7 every id with a case reads at the width `player-props.md` gives (lab, 2026-11-18, run `cwid-b` in [probe-targets-2026-11-18.md](probe-targets-2026-11-18.md)).
