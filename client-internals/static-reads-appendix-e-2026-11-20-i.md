# Static reads for Appendix E, tenth batch (2026-11-20)

Date: 2026-11-20. Evidence: **[bin]** (a decompiler read of the Linux 6.01r1 x64 client on the
GwenTea2 lab, the existing decompiler output of the Linux 6.03r7 x64 client, and a linear
disassembly of the unpacked Windows 6.00r2, 6.00r4 and 6.03r7 executables; no client run). Only
behaviour is given here. Covers App. E#211.

Builds read: Windows 6.00r2 and 6.00r4 (unpacked images), Linux 6.01r1 x64 (build stamp
Sep 18 2011), Linux 6.03r7 x64, and Windows 6.03r7 (unpacked image).

## Which names make fold 241 (E#211)

### The test

After decoding, the 6.x fusion pass looks at each name load (22). When the next instruction is a
call (6), `setreg` (45) or `makeprop` (47), it looks the loaded name up in the client's **global
builtin registry**. If the name is there and that registry entry's flag is set, the name load
becomes 241 and the entry is kept on the instruction. Otherwise nothing changes. This is the only
place that reads the flag.

The registry is one global table, created on first use, that holds the built-in functions the
client registers at start-up. Objects of a script (weapons, NPCs, the player, GUI controls) are not
in it, so they never make 241.

### Where the flag comes from

Built-ins are registered from static tables by two routines:

- The first takes rows of name, return type, parameter signature, handler and description. It
  always sets the flag to 0.
- The second takes the same row with one more field, and copies that field into the flag. A row
  name may be stored scrambled; the row says so, and the name is unscrambled when registered.

Only the global table registered through the second routine has rows with the field set. In every
build read, the same **17 functions** carry it:

| Kind | Names |
| --- | --- |
| Turning default features off | `disabledefmovement`, `disablemap`, `disablepause`, `disableselectweapons`, `disableweapons` |
| Turning them back on | `enabledefmovement`, `enablefeatures`, `enablemap`, `enablepause`, `enableselectweapons`, `enableweapons` |
| Player state | `freezeplayer`, `noplayerkilling` |
| Tile tests | `onwall`, `onwall2`, `onwater`, `onwater2` |

Every other row of that table has the field at 0, and so does every row of the other global tables that the 6.01 scan found.
Examples with 0 are `setani`, `findweapon`, `findlevel`, `triggerserver`, `say2` and `keydown`.

### By build

| Build | How the table is held | Rows with the flag |
| --- | --- | --- |
| 6.00r2, 6.00r4 (Windows) | Each built-in is constructed in code, one call per row; the flag is the last argument: 1 for the 17, and 0 for the other 300-odd calls (a register cleared to 0 in each function) | the 17 |
| 6.01r1 (Linux x64) | Static table of 135 rows, plus a 54-row table through the first routine | the 17 |
| 6.03r7 (Linux x64) | The same two registration calls, with 132 rows and 53 rows; the table contents were not read in this build | not read; the Windows 6.03r7 row stands for it |
| 6.03r7 (Windows) | Static table, 24-byte rows | the 17 |

So the set did not change from 6.00 to 6.03.

### What 241 does

The executor case for 241 (→ `protocol/gs2-client-only-opcodes.md`) pushes the stored entry as a
resolved value, without a name lookup at run time. So the fold binds one of these 17 built-ins at
load time instead of resolving the name each time the instruction runs.

### What this settles

- Fold 241 is made only for the 17 global built-ins above, and only when a call, `setreg` or
  `makeprop` follows the name load. The earlier guess (weapons and other globals that resolve once)
  was wrong: no script object is in the registry.
- A clean-room VM can reproduce the fold with a fixed list of these 17 names.

## Not covered

- Why these 17 are marked. They are all commands or tests that GS1 scripts already used under the
  same names, but no reason is stated in the code.
- Whether anything changes the flag after start-up. No other writer was looked for; the fusion pass
  is the only reader found.
- Whether resolving these names unfused could ever reach a different object (for example a script
  function of the same name). The fold would skip that lookup, so the two could differ in that case.
