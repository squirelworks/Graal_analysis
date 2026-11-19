# GS2 opcode table: every byte, every readable client VM

Date: 2026-11-18. Static read only; nothing was run. Tags as in `README.md`: **[bin]** the client binaries below, **[doc]** the MPL-2.0 Preagonal compiler at `7878bc5` (`npc-library/preagonal-gs2.md`), **[cap]** the 19 official 6.113-era bodies (`gs2-official-bytecode-6113.md`), **[inf]** inference. Evidence IDs `GS2-OPTABLE-WIN-20261118`, `GS2-OPTABLE-LNX-20261118`, `GS2-OPTABLE-ANDROID-20261118` (`docs/evidence-index.tsv`).

This is the one table that `#370` item 3 (App. E#202, E#207) asks for: which byte each client dispatches, the name the client itself gives it, and whether the third-party compiler emits it. The effect of each opcode stays in the notes that already describe it: `gs2-client-vm.md` (4.2.0.8 dispatcher, peephole folds), `gs2-client-only-opcodes.md` (43, 45–49, 54, 66, 67, 104, 121, 190, 200–242), `gs2-unpacked-6113.md` (6.1.1.3, folds 234–242) and `gs2-android-classic-18.md`. Where this note disagrees with them, it says so below.

## What was read

| Build | Image | How the case set was taken |
| --- | --- | --- |
| 4.03r3, 4.04r2, 4.11 | Windows `GraalEngine.dll` | two-level MSVC switch (byte index table, then jump table) over opcodes 1–190 |
| 4.20r8 | Windows `GraalEngine.dll` (two copies, same table) | the same switch shape, opcodes 1–233; also the opcode **name table** |
| 5.00r7, 5.12 | — | not re-read here: the DLL copies held show no readable strings (packed). The 5.0.0.7 row is the earlier export reading in `gs2-client-vm.md` |
| 5.30r3, 6.00r2, 6.00r4, 6.0.3.7, 6.1.1.3 | unpacked Windows executables | two-level switch over opcodes 1–242 |
| Linux x64: a June 2011 6.x beta, a November 2011 build, and 6.03r7 | x64 ELF | a 243-entry handler-pointer table (see "Linux uses threaded dispatch") |
| 7.12.43 | unpacked x64 `Graal3DEngine.dll` (v7 Worlds) | two-level switch over opcodes 1–242 |
| Android Classic 1.8 and 2.2 | x86_64 `libqplay.so` | the `TScriptMachine::executeScript` jump table (1.8 keeps that symbol; 2.2 was found by the same switch shape) |

Not resolved: the Linux 6.x **x86** builds (their handler table was not found by the x64 pattern), and the ARM-only Android APKs (Classic 1.6, 1.7, the 2014 Classic build, Era 1.7 and 2.0). **[bin]**

## The client's own names

4.03r3 to 4.20r8 fill a table of opcode names, one string per byte, at start-up. 5.x and later images carry no such strings. The table is complete: every slot that has a name is in the table below, including the ones `gs2-client-vm.md` called "short symbols". They are ordinary words (`add`, `sin`, `less`, `app` and so on), not operator spellings. **[bin]**

4.03r3, 4.04r2 and 4.11 have the same table as 4.20r8 with two differences: slot 11 is empty (no `waitfor`), and the table stops at 190 (no names for the folds 200–233). **[bin]**

The table names seven bytes that no dispatcher runs: `goto` (160), `break` (161), `continue` (162), `loadserver` (185), `loadserverr` (186), `loadclient` (187), `loadclientr` (188). `noop` (0) is named; only the Linux builds give it a handler (see below). **[bin]**

## Case sets

| Build | Cases | Change from the row above |
| --- | ---: | --- |
| 4.03r3, 4.04r2, 4.11 | 119 | base set: 1–10, 20–27, 30–47, 50–53, 60–104, 110–120, 130–142, 150, 151, 163, 180–184, 189, 190 |
| 4.20r8 | 154 | adds 11 (`waitfor`) and the folds 200–233 |
| 5.00r7, 5.12 | 158 | adds 48, 49, 54, 121 (`gs2-client-vm.md`) |
| 5.30r3 to 6.1.1.3, 7.12.43, Android 1.8 and 2.2 | 165 | drops 48 and 49; adds the folds 234–242 |
| Linux 6.x x64 (all three builds) | 167 | the 165 above, plus 0 and 164 |

So the dispatcher stopped changing at 5.30r3. 6.00r2, 6.00r4, 6.0.3.7, 6.1.1.3, the 2019+ v7 engine and both Android builds run the same 165 bytes. Android adds no opcode. **[bin]**

This corrects two readings. `gs2-client-vm.md` says the 4.2.0.8 name table leaves the arithmetic and comparison slots as short symbols; it does not. And the 5.30r3 row is new: the 234–242 folds are already in 5.30r3, so they are not a 6.00 addition. **[bin]**

Footnotes in the table: ¹ unnamed and not dispatched on 4.03r3–4.11. ² named in 4.20r8 only; these are folds, made after decode, and never appear in a byte stream (`gs2-client-vm.md#peephole-after-decode`). 234–242 have no name in any table. **[bin]**

The compiler column: **yes** where `npc-library/preagonal-gs2.md` or `gs2-client-vm.md` records an emitter, **no** where those notes record that the enum has no member, **?** where neither note settles it. The official 6.113 compiler differs from Preagonal at least on 190 (it emits `loadparams`), and none of 48, 49, 54, 121 or anything at 200 or above appears in its 19 bodies. **[doc][cap]**

## The table

A byte is listed when any client names it or dispatches it. "yes" means the build has a case (or a Linux handler) for that byte; "·" means it does not. **[bin]**

| Byte | Client name | 4.03r3–4.11 | 4.20r8 | 5.00r7, 5.12 | 5.30r3–6.113, 7.12.43, Android | Linux 6.x x64 | Preagonal compiler |
| ---: | --- | :-: | :-: | :-: | :-: | :-: | :-: |
| 0 | `noop` | · | · | · | · | yes | ? |
| 1 | `jump` | yes | yes | yes | yes | yes | yes |
| 2 | `jumptrue` | yes | yes | yes | yes | yes | yes |
| 3 | `sjumptrue` | yes | yes | yes | yes | yes | yes |
| 4 | `jumpfalse` | yes | yes | yes | yes | yes | yes |
| 5 | `sjumpfalse` | yes | yes | yes | yes | yes | yes |
| 6 | `call` | yes | yes | yes | yes | yes | yes |
| 7 | `return` | yes | yes | yes | yes | yes | yes |
| 8 | `sleep` | yes | yes | yes | yes | yes | yes |
| 9 | `loopcheck` | yes | yes | yes | yes | yes | yes |
| 10 | `savestackpos` | yes | yes | yes | yes | yes | yes |
| 11 | `waitfor` ¹ | · | yes | yes | yes | yes | yes |
| 20 | `loadfloat` | yes | yes | yes | yes | yes | yes |
| 21 | `loadstring` | yes | yes | yes | yes | yes | yes |
| 22 | `loadmember` | yes | yes | yes | yes | yes | yes |
| 23 | `stackmark` | yes | yes | yes | yes | yes | yes |
| 24 | `loadtrue` | yes | yes | yes | yes | yes | yes |
| 25 | `loadfalse` | yes | yes | yes | yes | yes | yes |
| 26 | `loadnull` | yes | yes | yes | yes | yes | yes |
| 27 | `loadpi` | yes | yes | yes | yes | yes | yes |
| 30 | `dupe` | yes | yes | yes | yes | yes | yes |
| 31 | `swap` | yes | yes | yes | yes | yes | yes |
| 32 | `pop` | yes | yes | yes | yes | yes | yes |
| 33 | `makefloat` | yes | yes | yes | yes | yes | yes |
| 34 | `makestring` | yes | yes | yes | yes | yes | yes |
| 35 | `makemember` | yes | yes | yes | yes | yes | yes |
| 36 | `makeobject` | yes | yes | yes | yes | yes | yes |
| 37 | `makearray` | yes | yes | yes | yes | yes | yes |
| 38 | `initarray` | yes | yes | yes | yes | yes | yes |
| 39 | `setarray` | yes | yes | yes | yes | yes | yes |
| 40 | `setmember` | yes | yes | yes | yes | yes | yes |
| 41 | `makevar` | yes | yes | yes | yes | yes | yes |
| 42 | `createobject` | yes | yes | yes | yes | yes | yes |
| 43 | `makeoldscriptvar` | yes | yes | yes | yes | yes | no |
| 44 | `convertbool` | yes | yes | yes | yes | yes | yes |
| 45 | `setreg` | yes | yes | yes | yes | yes | no |
| 46 | `getreg` | yes | yes | yes | yes | yes | no |
| 47 | `makeprop` | yes | yes | yes | yes | yes | no |
| 48 | (none) | · | · | yes | · | · | no |
| 49 | (none) | · | · | yes | · | · | no |
| 50 | `assign` | yes | yes | yes | yes | yes | yes |
| 51 | `massassign` | yes | yes | yes | yes | yes | yes |
| 52 | `inc` | yes | yes | yes | yes | yes | yes |
| 53 | `dec` | yes | yes | yes | yes | yes | yes |
| 54 | (none) | · | · | yes | yes | yes | no |
| 60 | `add` | yes | yes | yes | yes | yes | yes |
| 61 | `sub` | yes | yes | yes | yes | yes | yes |
| 62 | `mul` | yes | yes | yes | yes | yes | yes |
| 63 | `div` | yes | yes | yes | yes | yes | yes |
| 64 | `mod` | yes | yes | yes | yes | yes | yes |
| 65 | `pow` | yes | yes | yes | yes | yes | yes |
| 66 | `and` | yes | yes | yes | yes | yes | no |
| 67 | `or` | yes | yes | yes | yes | yes | no |
| 68 | `not` | yes | yes | yes | yes | yes | yes |
| 69 | `negative` | yes | yes | yes | yes | yes | yes |
| 70 | `equal` | yes | yes | yes | yes | yes | yes |
| 71 | `nequal` | yes | yes | yes | yes | yes | yes |
| 72 | `less` | yes | yes | yes | yes | yes | yes |
| 73 | `greater` | yes | yes | yes | yes | yes | yes |
| 74 | `lessequal` | yes | yes | yes | yes | yes | yes |
| 75 | `greaterequal` | yes | yes | yes | yes | yes | yes |
| 76 | `bitor` | yes | yes | yes | yes | yes | yes |
| 77 | `bitand` | yes | yes | yes | yes | yes | yes |
| 78 | `bitxor` | yes | yes | yes | yes | yes | yes |
| 79 | `bitinvert` | yes | yes | yes | yes | yes | yes |
| 80 | `inrange` | yes | yes | yes | yes | yes | ? |
| 81 | `inarray` | yes | yes | yes | yes | yes | ? |
| 82 | `indexof` | yes | yes | yes | yes | yes | yes |
| 83 | `type` | yes | yes | yes | yes | yes | yes |
| 84 | `format` | yes | yes | yes | yes | yes | yes |
| 85 | `int` | yes | yes | yes | yes | yes | yes |
| 86 | `abs` | yes | yes | yes | yes | yes | yes |
| 87 | `random` | yes | yes | yes | yes | yes | yes |
| 88 | `sin` | yes | yes | yes | yes | yes | yes |
| 89 | `cos` | yes | yes | yes | yes | yes | yes |
| 90 | `arctan` | yes | yes | yes | yes | yes | yes |
| 91 | `exp` | yes | yes | yes | yes | yes | yes |
| 92 | `log` | yes | yes | yes | yes | yes | yes |
| 93 | `min` | yes | yes | yes | yes | yes | yes |
| 94 | `max` | yes | yes | yes | yes | yes | yes |
| 95 | `getangle` | yes | yes | yes | yes | yes | yes |
| 96 | `getdir` | yes | yes | yes | yes | yes | yes |
| 97 | `vecx` | yes | yes | yes | yes | yes | yes |
| 98 | `vecy` | yes | yes | yes | yes | yes | yes |
| 99 | `indicesof` | yes | yes | yes | yes | yes | yes |
| 100 | `link` | yes | yes | yes | yes | yes | yes |
| 101 | `shl` | yes | yes | yes | yes | yes | yes |
| 102 | `shr` | yes | yes | yes | yes | yes | yes |
| 103 | `char` | yes | yes | yes | yes | yes | yes |
| 104 | `compare` | yes | yes | yes | yes | yes | no |
| 110 | `trim` | yes | yes | yes | yes | yes | yes |
| 111 | `length` | yes | yes | yes | yes | yes | yes |
| 112 | `pos` | yes | yes | yes | yes | yes | yes |
| 113 | `app` | yes | yes | yes | yes | yes | yes |
| 114 | `charat` | yes | yes | yes | yes | yes | yes |
| 115 | `substring` | yes | yes | yes | yes | yes | yes |
| 116 | `beginswith` | yes | yes | yes | yes | yes | yes |
| 117 | `endson` | yes | yes | yes | yes | yes | yes |
| 118 | `tokenize` | yes | yes | yes | yes | yes | yes |
| 119 | `translate` | yes | yes | yes | yes | yes | yes |
| 120 | `positions` | yes | yes | yes | yes | yes | yes |
| 121 | (none) | · | · | yes | yes | yes | no |
| 130 | `arraysize` | yes | yes | yes | yes | yes | yes |
| 131 | `getarraycell` | yes | yes | yes | yes | yes | ? |
| 132 | `setarraycell` | yes | yes | yes | yes | yes | ? |
| 133 | `getarraycell2` | yes | yes | yes | yes | yes | ? |
| 134 | `setarraycell2` | yes | yes | yes | yes | yes | ? |
| 135 | `subarray` | yes | yes | yes | yes | yes | yes |
| 136 | `arrayadd` | yes | yes | yes | yes | yes | yes |
| 137 | `arraydelete` | yes | yes | yes | yes | yes | yes |
| 138 | `arrayremove` | yes | yes | yes | yes | yes | yes |
| 139 | `arrayreplace` | yes | yes | yes | yes | yes | yes |
| 140 | `arrayinsert` | yes | yes | yes | yes | yes | yes |
| 141 | `arrayclear` | yes | yes | yes | yes | yes | yes |
| 142 | `expandarray` | yes | yes | yes | yes | yes | ? |
| 150 | `with` | yes | yes | yes | yes | yes | yes |
| 151 | `popwith` | yes | yes | yes | yes | yes | yes |
| 160 | `goto` | · | · | · | · | · | ? |
| 161 | `break` | · | · | · | · | · | no |
| 162 | `continue` | · | · | · | · | · | no |
| 163 | `foreach` | yes | yes | yes | yes | yes | yes |
| 164 | (none) | · | · | · | · | yes | ? |
| 180 | `loadthis` | yes | yes | yes | yes | yes | yes |
| 181 | `loadthiso` | yes | yes | yes | yes | yes | yes |
| 182 | `loadplayer` | yes | yes | yes | yes | yes | yes |
| 183 | `loadplayero` | yes | yes | yes | yes | yes | yes |
| 184 | `loadlevel` | yes | yes | yes | yes | yes | yes |
| 185 | `loadserver` | · | · | · | · | · | no |
| 186 | `loadserverr` | · | · | · | · | · | no |
| 187 | `loadclient` | · | · | · | · | · | no |
| 188 | `loadclientr` | · | · | · | · | · | no |
| 189 | `loadtemp` | yes | yes | yes | yes | yes | yes |
| 190 | `loadparams` | yes | yes | yes | yes | yes | no |
| 200 | `addfloat` ² | · | yes | yes | yes | yes | no |
| 201 | `subfloat` ² | · | yes | yes | yes | yes | no |
| 202 | `mulfloat` ² | · | yes | yes | yes | yes | no |
| 203 | `divfloat` ² | · | yes | yes | yes | yes | no |
| 204 | `modfloat` ² | · | yes | yes | yes | yes | no |
| 205 | `powfloat` ² | · | yes | yes | yes | yes | no |
| 206 | `andfloat` ² | · | yes | yes | yes | yes | no |
| 207 | `orfloat` ² | · | yes | yes | yes | yes | no |
| 208 | `addassign` ² | · | yes | yes | yes | yes | no |
| 209 | `subassign` ² | · | yes | yes | yes | yes | no |
| 210 | `mulassign` ² | · | yes | yes | yes | yes | no |
| 211 | `divassign` ² | · | yes | yes | yes | yes | no |
| 212 | `modassign` ² | · | yes | yes | yes | yes | no |
| 213 | `powassign` ² | · | yes | yes | yes | yes | no |
| 214 | `andassign` ² | · | yes | yes | yes | yes | no |
| 215 | `orassign` ² | · | yes | yes | yes | yes | no |
| 216 | `addfloatassign` ² | · | yes | yes | yes | yes | no |
| 217 | `subfloatassign` ² | · | yes | yes | yes | yes | no |
| 218 | `mulfloatassign` ² | · | yes | yes | yes | yes | no |
| 219 | `divfloatassign` ² | · | yes | yes | yes | yes | no |
| 220 | `modfloatassign` ² | · | yes | yes | yes | yes | no |
| 221 | `powfloatassign` ² | · | yes | yes | yes | yes | no |
| 222 | `andfloatassign` ² | · | yes | yes | yes | yes | no |
| 223 | `orfloatassign` ² | · | yes | yes | yes | yes | no |
| 224 | `lessfloat` ² | · | yes | yes | yes | yes | no |
| 225 | `greatorfloat` ² | · | yes | yes | yes | yes | no |
| 226 | `lessequalfloat` ² | · | yes | yes | yes | yes | no |
| 227 | `greaterequalfloat` ² | · | yes | yes | yes | yes | no |
| 228 | `getregfloat` ² | · | yes | yes | yes | yes | no |
| 229 | `getregstring` ² | · | yes | yes | yes | yes | no |
| 230 | `getregobject` ² | · | yes | yes | yes | yes | no |
| 231 | `getregincpop` ² | · | yes | yes | yes | yes | no |
| 232 | `getregdecpop` ² | · | yes | yes | yes | yes | no |
| 233 | `getregdupe` ² | · | yes | yes | yes | yes | no |
| 234 | (none) | · | · | · | yes | yes | no |
| 235 | (none) | · | · | · | yes | yes | no |
| 236 | (none) | · | · | · | yes | yes | no |
| 237 | (none) | · | · | · | yes | yes | no |
| 238 | (none) | · | · | · | yes | yes | no |
| 239 | (none) | · | · | · | yes | yes | no |
| 240 | (none) | · | · | · | yes | yes | no |
| 241 | (none) | · | · | · | yes | yes | no |
| 242 | (none) | · | · | · | yes | yes | no |

## Linux uses threaded dispatch

The Windows, v7 and Android images step the instruction list with a `switch` on the opcode byte. The Linux x64 builds do not. When a script is loaded, a pass over the decoded instructions looks each opcode up in a 243-entry table of handler addresses and stores the address in the instruction itself. Each handler ends by loading the next instruction's stored address and jumping to it. An opcode whose table entry is empty stores a null address; this read did not find a guard in front of that jump, so a byte outside the 167 is unsafe on Linux rather than a silent skip. **[bin][inf]**

The same three-build table also gives the decoded record size. **[bin]**

| Image | Decoded instruction |
| --- | --- |
| Windows 4.2.0.8 to 6.1.1.3 | 24 bytes (`gs2-client-vm.md`) |
| Linux 6.x x64 | 40 bytes, with the handler address in the last 8 |
| 7.12.43 x64 | 40 bytes |
| Android 1.8 x86 | 20 bytes (`gs2-android-classic-18.md`) |
| Android 1.8 x86_64 | 32 bytes |
| Android 2.2 x86_64 | 40 bytes |

None of these sizes is part of the bytecode. The byte stream is the same four-segment container on every build.

### Opcode 0 on Linux

Its handler moves to the next instruction and does nothing else. On the Windows, v7 and Android switches, 0 is outside the switch's range and takes the same default path as any undispatched byte, which is not a plain no-op (`gs2-client-vm.md`, `gs2-unpacked-6113.md`). No compiler is known to emit 0. **[bin][doc]**

### Opcode 164 on Linux

Unnamed in 4.20r8's table and absent from every Windows, v7 and Android switch. The Linux handler sets a flag on the running script, then looks for the running script in its owner's list of scripts and takes the first later entry that has instructions. If there is one, it switches the machine to that script, sets the program counter to 0 and bumps a 16-bit counter on it. If there is none, it backs the program counter up by one and leaves the run loop. **[bin]**

That reads as "continue in the next joined script" **[inf]**. No compiler is known to emit 164; whether the 19 official bodies contain it was not checked. A portable VM can treat it as Linux-only and refuse it elsewhere.

## Method

1. Find the dispatcher. On Windows, search the code for a compare of the opcode against 189, 232 or 241 (after a decrement) followed by a byte-indexed table and a jump table. On Linux x64, follow the reference to the `Loop limit exceeded` string to the run loop, then the table load in the decode pass. On Android 1.8, the exported `executeScript` symbol.
2. Read the tables. Two-level switch: an opcode's case is the jump-table entry its byte-table slot selects; the default is the entry the out-of-range branch uses. Linux: a non-null entry is a handler. Android: the most common target is the default.
3. Read the name table on 4.x by following the string `jumptrue` to the start-up routine that stores one string per slot.
4. Cross-check: the 6.00r2 and 6.1.1.3 sets equal what `gs2-unpacked-6113.md` and `gs2-client-only-opcodes.md` list from the Ghidra listings, and the 4.20r8 set equals what `gs2-client-vm.md` lists.

No addresses are given here, by the repository rule. The scripts were throwaway and are not committed. **[bin]**

## For a compiler and a VM

- A compiler that targets every client from 4.03r3 should not emit 11. It is not dispatched before 4.20r8. **[bin]**
- 48 and 49 run only on 5.00r7 and 5.12; 54 and 121 only from 5.00r7. Emitting any of them breaks 4.x clients. **[bin]**
- Emitting 0, 160–162, 164 or 185–188 is never portable. **[bin]**
- The folds (200–242) are made by each client after decode. A compiler never writes them. **[bin][cap]**

## Delteria 2019 features, by opcode

The project's Delteria 2019 server backup excerpt (`server-notes/hubserver-037-and-delteria-2026-11-18.md`) counts the GS2 features in use. This maps each counted feature to the opcodes it compiles to and the oldest client whose switch has all of them. Counts are uses / files from that excerpt. The opcode for each feature is from the compiler notes; for `switch` and the ternary the comparison-and-jump shape is inferred. **[doc][bin][inf]**

| Feature (uses / files) | Opcodes | Runs from |
| --- | --- | --- |
| `temp.` locals (2,500 / 24) | 189, and on the official compiler 45–47 for cached locals | 4.03r3 |
| `this.` vars (896 / 33) | 180, 35 | 4.03r3 |
| `function onX()` handlers (140 / 33) | segment 2, 6, 7 | 4.03r3 |
| `with (obj)` (45 / 5) | 150, 151 | 4.03r3 |
| `for (x : list)` (74 / 16) | 163 | 4.03r3 |
| `in \|a, b\|` (22 / 11) | 80 | 4.03r3 |
| `in {list}` (5 / 3) | 81 | 4.03r3 |
| `switch` / `case` (29 / 8) | 70, 2–5 (no switch opcode) | 4.03r3 |
| ternary (68 / 10) | 44, 2–5 | 4.03r3 |
| `@` (130 uses), `SPC` `NL` `TAB` (90 uses) | 113 | 4.03r3 |
| `format(` (22 / 6) | 84 | 4.03r3 |
| array literal `{…}` (88 / 13) | 23, 37 | 4.03r3 |
| `.size()` `.add(` `.starts(` `.substring(` | 130, 136, 116, 115 | 4.03r3 |
| `.pos(` `.tokenize(` `.insert(` `.index(` `.length()` `.delete(` `.subarray(` `.remove(` | 112, 118, 140, 82, 111, 137, 135, 138 | 4.03r3 |
| `.type()` / `makevar` | 83 / 41 | 4.03r3 |
| `sleep` (39 / 18) | 8 | 4.03r3 |
| `waitfor` (6 / 4) | 11 | **4.20r8** |
| `scheduleevent`, `settimer`, `trigger*`, `find*`, `new Gui…Ctrl` | 6 (call by name), 42 | 4.03r3 for the opcode; the command itself is the client's |

Only `waitfor` needs a newer VM than the oldest 4.x. Everything else in the Delteria scripts is in the 119-case base set. What limits those scripts on old clients is the command and object library behind opcode 6, not the opcode set. **[bin][inf]**

## Still open

- The Linux 6.x x86 dispatcher, and the ARM-only Android builds.
- Who emits 164, if anyone, and a live run that reaches it.
- Each handler's effect on 5.30r3 and 7.12.43 (only the case set was read). The 6.1.1.3 effects are in `gs2-unpacked-6113.md`.
- 5.00r7 and 5.12 from the shipped DLLs rather than the earlier export.
- Live runs of every undispatched byte, the raw fold bytes and opcodes 45–54, 66, 67, 104 and 121 on 6.03r7, 5.24r4 and 4.20r8 are in `script-fuzz-2026-11-19.md`. 48 and 49 still need a build that dispatches them.
