# pyReborn study

Date: 2026-11-12. Issue #244, `docs/NEXT.md` task 4.

A read of hosler's pyReborn and its two sibling repositories, compared with this repo's
own client reads. It says what pyReborn covers, where its facts come from, where it agrees
or disagrees with us, and which of its findings are worth checking in our clients.

Tags as elsewhere in this repo: **[bin]** read from a client binary · **[srv]** a server's
source says it · **[lab]** · **[inf]**. pyReborn's own claims are not tagged **[bin]**
here, even when they cite a client: see "Where its facts come from".

## Source and licence

| Repository | Commit read | Licence |
|---|---|---|
| `hosler/pyreborn` (the client) | `340d789` (2026-11-11) | MIT, `LICENSE` file ("Copyright (c) 2024 PyReborn Contributors") |
| `hosler/reborn-protocol` (codec, GS1 interpreter, GS2 VM, packet ids) | `f6b36d9` (2026-11-11) | MIT, declared in `pyproject.toml`; no `LICENSE` file |
| `hosler/pygserver` (a Python gserver and listserver link) | `58fb4a4` (2026-11-11) | MIT, declared in `pyproject.toml`; no `LICENSE` file |

Every `file:line` below refers to those commits. Per `AGENTS.md`, this note summarises and
cites; it quotes no pyReborn code. Seihai's clean-room repos may link to this note but must
not copy from it.

An earlier, owner-held study of an older pyReborn commit (2026-10-31) ranked these
findings against the Seihai client of that date. It is not reproduced here; its lasting
points are folded into the sections below and re-checked against the current commits.

## What it is

- **pyReborn** is a pure-Python client: socket and cipher (`pyreborn/protocol.py`), one
  handler module per packet domain (`pyreborn/handlers/`, registered with a decorator,
  `handlers/registry.py`), a GS1 host (`pyreborn/gs1_client/`), a GS2 host
  (`pyreborn/gs2_client/`), RC and NC clients (`rc_client.py`, `nc_client.py`), a
  listserver client (`listserver.py`) and an optional pygame front end (`pygame_game.py`,
  `pyreborn/game/`). About 135,000 lines of Python with its tests and tools.
- **reborn-protocol** holds the parts shared with the server: the packet-id enums and
  their layout comments (`reborn_protocol/constants.py`), the property tables
  (`props.py`), the gen-5 cipher and compression (`encryption.py`), a GS1 interpreter
  and a GS2 compiler and VM (`gs1/`, `gs2/`).
- **pygserver** is a Python game server and listserver link built on the same library.
- `game_tester/` in pyReborn holds live-play tools: behaviour fingerprints, a content
  crawler, conformance checks and bots.

## Where its facts come from

This decides how much weight any pyReborn claim can carry here.

1. **GServer-v2's source**, mostly its `beta4` branch. The layout comments in
   `reborn_protocol/constants.py` cite `IEnums.h`, `Player.cpp`, `PlayerClient.cpp`,
   `Weapon.cpp` and `ScriptClass.cpp` line by line (for example `constants.py:255-319`),
   and the codec cites `origin/beta4` paths (`pyreborn/packet_codec/files.py:322-336`).
   These are server-side facts, our **[srv]** grade.
2. **A "reversed official client"** in a repository we cannot see. 236 comments across
   pyReborn and reborn-protocol cite it by file and line. Treat each one as a hint until a
   client read here or a lab run agrees.
3. **Live play against public servers.** Most of the GS1/GS2 script behaviour comes from
   playing one public server's content and fixing what broke. That is real-client
   *content*, not a real client: it shows what scripts expect, not what the original
   client does. We do not repeat that method (`AGENTS.md`: no public servers without the
   owner's written OK).
4. **Scripting docs** shipped with the server projects (`scripting-gs1-commands.md` and
   others, cited in `pyreborn/gs1_client/host_commands_layer.py:41-50`).

So pyReborn is a good map of what GServer-v2 sends and what live content uses. It is not
evidence of what any original client build does.

## Protocol coverage

| Area | pyReborn | Our notes | Agree? |
|---|---|---|---|
| Login tokens | 1.411 `GNW13110` (type 0, gen 3), 2.17 `GNW22122` (gen 3), 2.21 `GNW01113` (type 4, gen 4), 2.22 `GNW03014` with build string `356` (type 5, gen 5), 6.037 `G3D0311C` (Windows) and `G3D0511C` (Linux) (`pyreborn/protocol.py:89-136`) | same tokens and client types (`protocol/login-tokens-3x-7x.md`, `client-internals/version-tokens.md`) | yes. Nothing before 1.411, nothing from 3.x to 5.x, no 6.11 |
| Server's allowed tokens | pygserver offers 13 tokens from `GNW22122` to `G3D0511C` (`pygserver/listserver.py:293-298`) | — | a convenient list of what a GServer-v2-style server expects |
| Gen-5 cipher | seed `0x4A80B38`, multiplier `0x8088405`, limit 12 groups for raw, 4 for zlib and bz2 (`reborn_protocol/encryption.py:40-87`) | same constants and limits (`protocol/codec-and-framing.md`) | yes |
| Cipher step count | a final partial 4-byte group counts as a step, always (`encryption.py:88-132`) | 5.12 steps zlib and bz2 frames rounded **down** (`protocol/v5v6-lab-play.md`) | no for 5.12. pyReborn, like stock GServer-v2, would drift against a real 5.12 client |
| Send compression | at most 55 bytes raw, then zlib up to 0x2000 bytes, then bz2, as a per-session policy (`encryption.py:170-200`) | the clients pick raw below 0x30 and zlib below 0x1000 (`protocol/v3x-clients.md`) | different thresholds, both legal. The idea of a per-session "which types may be sent" policy is worth keeping |
| Listserver | one shape, the 5.x/6.x one (`pyreborn/listserver.py:238-356`) | 1.x to 6.x shapes (`protocol/listserver.md`) | ours is wider |
| RC and NC | full RC (type 6) and NC (type 3) clients (`pyreborn/rc_client.py`, `nc_client.py`) | `tools/remotecontrol.md`, `protocol/npc-control.md` | not compared id by id here |

## The ids our notes call unknown

reborn-protocol names most of the ids that the 2026-11-06 note
(`protocol/unknown-ids-2026-11-06.md`) read in the clients. Its names come from the beta4
gserver, so they tell us what the server meant to send, which the client reads cannot.

| Id | reborn-protocol (`constants.py`) | Our client reads | Verdict |
|---|---|---|---|
| PLO 60, 81, 83 | "Unhandled by 5.07+" (`:226`, `:247`, `:249`) | no client of any age handles them, staff clients included | its comment understates it |
| PLO 104 | `FILEDECRYPTKEY`: file name, a "key purpose" byte, two `i5` halves of a DES key; purpose 0 = `.gpake`, 1 = `.enc` (`:255`) | same layout; 6.03r7 decrypts a loose `.enc` only when the byte is 1 | agrees, and names the byte: it says what kind of file the key is for. **[srv]** |
| PLO 108 | `PING`: type 0 is answered by `PLI_PONG`, type 1 is stored (`:259`) | same; nothing reads the stored value back | agrees; no more on sub 1. pyReborn has no 108 handler, so it never answers a ping |
| PLO 109 | `HTTPDOWNLOAD`: mod time, local file, URL; "download url, save as localfile" (`:260`) | `i5 time`, `str A`, `str B`; B is fetched over HTTP | agrees, and says A is the name to save as. **[srv]** |
| PLO 124 | `RC_UNKNOWN124`, "RC3 receives this" (`:263`) | RC3 logs "received player flags" and reads nothing | agrees |
| PLO 132, 133 | `WEAPONBYTECODE`, `CLASSBYTECODE`: name length, name, bytecode (`:265-266`) | same layout, 3.153 to 5.12 (read 2026-11-12, PR #412) | agrees. One difference in use: pyReborn stores a 132 script under any name (`pyreborn/handlers/scripts.py:86-108`), but the real client ignores 132 for a weapon the player doesn't hold |
| PLO 168 | `ONLINEMODE`, blank login-complete marker (`:286`) | empty; sets a one-shot flag | agrees |
| PLO 181 | `PLAYERNOUDP`: player id, toggle (`:303`) | the flag keeps the player out of peer-to-peer UDP sends (PR #412) | agrees |
| PLO 190 | `SERVERLISTCONNECTED`: the listserver link is up, the client may log into IRC (`:312`) | 6.x raises `onServerListerConnect` | agrees |
| PLO 193 | `WEAPONHASH`: checksum, name (`:315`) | zlib CRC32 of the cached weapon script, then the name | agrees |
| PLO 194 | `RESETCLIENT`, sent before the weapon list (`:316`); pyReborn clears only its weapon list (`handlers/scripts.py:164-167`) | 4.20r8 clears weapons and classes; 5.00r7 clears levels and level caches; 6.03r7 resets more | pyReborn does less than any real client |
| PLO 82 | `SERVERTEXT`, stored (`handlers/chat.py:78-81`) | 3.153 raises the `receivetext` event (`protocol/v3x-clients.md`) | agrees on purpose |

## GS2 VM

reborn-protocol's VM names opcodes 45, 46 and 47 as register store, register load and
"convert to property" (`reborn_protocol/gs2/opcodes.py:67-82`), and treats 66 and 67 as
non-short-circuit and/or that push 1 or 0 (`opcodes.py:96-102`, which cites the
"reversed official client"). Our VM note has the same three as `setreg`, `getreg` and
`makeprop`, and 66/67 as `andfloat`/`orfloat`, all present in the client and never emitted
by the compiler (`protocol/gs2-client-vm.md`). The two reads agree. Its `waitfor` pops
object, event and timeout and pushes the host's answer, or 0 without a host
(`reborn_protocol/gs2/vm.py:796-804`). `tests/test_gs2_vm.py` and the other `test_gs2_*`
files are a large source of hand-written cases.

## Client-side script behaviour (hints to check)

Each of these was settled by playing live content, not by reading a client. Check each
one against the 2.x and later client reads before relying on it.

| Behaviour | pyReborn | Status here |
|---|---|---|
| `keydown(i)` reads a fixed control table: 0 up, 1 left, 2 down, 3 right, 4 weapon (D), 5 sword (S), 6 grab (A), 7 map (M), 8 chat (Tab), 9 inventory (Q) | `pyreborn/gs1_client/runtime.py:93-97` (from the server's GS1 docs) | not checked in a client |
| Scripts still read keys while the player is frozen (a splash menu does `freezeplayer` and then polls `keydown`) | `runtime.py:93-97`, `gs1_client/host_functions.py:144-146` | not checked |
| `keydown2(code, edge)`: a raw key code, plus an optional "pressed this frame" flag | `host_functions.py:147-155` | not checked |
| `keypressed` fires on every script with `#p(0)` = key code and `#p(1)` = the character | `runtime.py:1168-1173` | not checked |
| `hasweapon` matches names case-insensitively | `host_functions.py:156-161`, which cites the server's account code, not a client | server semantics only |
| `statsoff` reads true while `showstats` hides the HUD | `gs1_client/host_builtins.py:276-299` | not checked |
| `selectedweapon` is the equipped weapon's index, or -1 | `host_builtins.py:301-308` | not checked |
| `showimg2` and `showtext2` take a z coordinate, not a zoom, and draw in screen space; `showani2` adds z but stays in level space | `gs1_client/host_commands_layer.py:17-60`, `:181-200` | not checked |
| `hideimgs start,end` is an inclusive range | `host_commands_layer.py:209-220` | not checked |
| A weapon resent under the same name with a new script runs `created` again | `runtime.py:379-392` | not checked |
| GANI keywords beyond the 2.x set: `CONTINUOUS` (resume where left), `PARAMn` and `DEFAULTPARAMn` (also inside `PLAYSOUND`), `SCRIPT … SCRIPTEND`, `MOVIE … MOVIEEND` with `ACTOR` | `pyreborn/gani.py:281-320`, `:349`, `:577-620`, `:668` | compare with `formats/` gani notes before use; `MOVIE` is probably v5/v6 |

## Test and tooling ideas

- **Behaviour fingerprints** (`game_tester/behaviour_fingerprint.py:1-20`): log in, record
  the *shape* of what scripts built (counts in bands, sets) and compare it with a
  checked-in baseline. This catches a script that silently takes the wrong branch. It
  fits our loopback lab servers as is.
- **GS1 oracle corpus** (`reborn-protocol/tests/test_gs1_oracle.py`,
  `tests/gs1_oracle_corpus.cases`): the same GS1 cases run through GServer-v2's own C++
  engine and compared by variable store. A cheap semantic check for any GS1 interpreter,
  as long as the known upstream bugs are kept in mind.
- **Parser recovery cases** (`reborn-protocol/tests/test_gs1_parser_recovery.py`):
  malformed GS1 lifted from live content (a `*`-prefixed block, `:=` assignment, arrays
  with empty slots, stray top-level `}`). The owner's 2026-10-31 run found that two of
  them made the Seihai parser run code that should not run.
- **Conformance table** (`game_tester/gs1_client_conformance.py`): one test row per cited
  reference line, so a regression contradicts a citation rather than a guess.
- **Content crawler** (`game_tester/server_crawl.py:1`): a bounded, read-only crawl of a
  public server's scripts. Not usable here without the owner's written OK, because it
  talks to public servers.

## What it cannot help with

- Anything before 1.411, including 1.39's poses without ganis.
- The 5.12 round-down cipher and the 6.036 and later logins.
- 3.x to 5.x client behaviour: it speaks no token between 2.22 and 6.037.
- Mac and Linux client differences.

## Leads for Seihai

Seihai's repos may link here. The behaviours most likely to matter for the Seihai client,
each to be confirmed from our own client notes before use: reading keys while frozen
(`keydown`, `keydown2`, `keypressed`), `statsoff` and `selectedweapon`, the z argument of
`showimg2`/`showtext2`, the GANI keywords above, and the parser recovery cases. For the
Seihai gserver: 132 must follow the weapon itself (the client drops it otherwise), 194 is
sent before the weapon list, and 181 should be sent for a player whose UDP port is
unusable.
