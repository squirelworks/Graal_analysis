# GS1 and GS2 script fuzzing on real clients

Date: 2026-11-19. Evidence is **[lab]** unless a line says otherwise. All runs were in the Debian lab VM, under Xvfb, in a bwrap namespace with only loopback. Each real client talked to a lab gserver through `tools/probe/gen5probe.py`. Nothing was sent to any public server. Raw logs, pcaps and screenshots stay in the VM, and this note keeps only derived results.

## Method

The cases come from seihai-core's generators (`examples/gs2_fuzzcases.rs` and `examples/gs1_fuzzcases.rs`, seed 1). Each case comes with what Seihai's own GS2 VM, run per version profile, or its GS1 engine predicts the client will do. `tools/probe/scriptfuzz.py plan` turns a case file into a probe plan. For each case the plan:

- creates a fresh NPC with PLO_NPCPROPS (3);
- delivers the script:
  - **GS2:** PLO_RAWDATA (100) followed by PLO_NPCBYTECODE (131) in one inject.
  - **GS1:** the script text as NPC prop 1 (a GSHORT length, then the text). Clients never receive GS1 as bytecode.
- waits, then deletes the NPC with PLO_NPCDEL (29).

Every script sets `player.chat` to `FZ<id>a`, waits, computes one value, and sets `player.chat` to `FZ<id>:<value>`. The client sends both chats back to the server as player props, and `scriptfuzz.py score` reads them from the proxy log.

| Verdict | Meaning |
| --- | --- |
| `match` | The client sent exactly what Seihai predicts. |
| `differs` | Both chats came, but the value is different. |
| `stopped` | Only `FZ<id>a` came, so the script halted partway. |
| `silent` | Nothing came. |
| `ran-past` | Seihai predicts a stop or rejects the file, but the client finished. |

The case families are:

- **GS2:**
  - `control`;
  - `op`: every byte that no compiler emits, tested with no operand, with 0 and with 5; opcodes 45–49, 54, 66, 67, 104, 121, 0, 164 and `waitfor`; the fold bytes 200–242 written raw;
  - `limit`: stack depth, loop passes, `maxlooplimit` and call depth;
  - `container`: damaged segments, damaged references, operand markers and byte flips;
  - `expr`: random expressions over edge values.
- **GS1:**
  - `code`: message codes;
  - `cond`: conditions;
  - `limit`: loop limits;
  - `text`: damaged scripts;
  - `expr`: random expressions.

**Harness lessons.**

- **Canary after every case (`plan --canary`).** Some cases leave the client connected but stop its script engine for good. Every later case then reads `silent`. So every case is followed by a copy of the control script under a fresh id, and when two canaries in a row are silent, the case before them is marked `dead`.
- **Crash resume.** When the client disconnects, the case of the last `CASE` mark is marked `crash`. The run then restarts on a fresh client from the next case.
- **Longer gaps on the Wine clients.** Under VM load, the Wine clients' chat reports arrive up to about 1 s late, so those runs used a 2.0 s gap per case and a 1.5 s gap for canaries.
- **Re-check of `stopped` cases.** Every `stopped` case was run again with a 4 s gap. 11 of about 260 changed verdict, so `stopped` almost always means a real halt.
- **Large frames in the proxy.** A case with 80 KB of bytecode overflowed the proxy's uncompressed u16 frame length. The proxy now sends payloads over 60 KB as gen-5 type 4 (zlib). This was a limit of our proxy, not a client finding.
- **6.03r7 kept one variant per undispatched byte.** It used only the no-operand case for each undispatched byte, because every one of them crashes. Bytes 0 and 164 kept all three variants.

## Tallies

| Client | Cases | match | differs | stopped | silent | ran-past | crash | dead |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 6.03r7 Linux (GS2) | 603 | 270 | 130 | 152 | 7 | 26 | 109 | 1 |
| 5.24r4 (GS2, Wine) | 849 | 497 | 185 | 96 | 7 | 36 | 0 | 6 |
| 4.20r8 (GS2, Wine) | 849 | 486 | 225 | 74 | 7 | 34 | 0 | 1 |
| 2.22 (GS1) | 267 | 142 | 113 | 4 | 0 | 7 | 0 | 0 |
| 2.31 (GS1) | 267 | 153 | 95 | 11 | 0 | 7 | 0 | 0 |
| 2.05 (GS1) | 267 | 156 | 93 | 9 | 1 | 7 | 0 | 1 |

Both controls matched on 6.03r7, 4.20r8 and every GS1 client. On 5.24r4, control 30001 matched, while 30000 reads `stopped` in the scored table; the canaries (copies of the control) reported through the whole run. Delivery by RAWDATA + NPCBYTECODE (3.153 on) and by NPC prop 1 (2.x) worked as written, with no image or level step needed.

## GS2: what each undispatched byte does

**6.03r7 Linux.** Bytes with no handler crash the client: it disconnects about 0.2 s after `FZ<id>a`. The crashing bytes are 12–19, 28, 29, 48, 49, 55–59, 105–109, 122–129, 143–149, 152–162, 165–179, 185–188 and 191–199. This confirms live that the threaded dispatch has no guard in front of a null handler slot (`gs2-opcode-table.md`, "Linux uses threaded dispatch"). Byte 0 runs as a no-op, even with an operand, which Seihai's reader rejects (`ran-past`). Byte 164 halts the script, as "continue in the next script" would when there is no next script.

**5.24r4 and 4.20r8.** No byte disconnects. An undispatched byte takes the switch default and runs as a no-op: the 7 pushed before it survives, as Seihai predicts. After a lone 7, only these differ:

| Byte after a lone 7 | 5.24r4 | 4.20r8 |
| --- | --- | --- |
| 46 (slot load) | empty value | empty value |
| 47 | 0 | 0 |
| 200–207, 224–230, 233–235 | runs, empty value | runs, empty value |
| 208–223, 231, 232 | halts | halts |
| 236–239 | halts | runs, empty value |
| 240, 242 | halts | halts |
| 241 | runs, empty value | runs, empty value |

## GS2: the fold bytes written raw

Compilers never write 200–242: each client creates them after decoding. Written straight into the stream after pushes of 3 and 4, with a numeric operand of 2, they behave as follows:

| Bytes | 6.03r7 | 5.24r4 | 4.20r8 |
| --- | --- | --- | --- |
| 200–207 | runs, empty value | same | same |
| 208 | 7 (add) | 7 | 7 |
| 209 | −1 (sub) | −1 | −1 |
| 210 | 12 (mul) | 12 | 12 |
| 211 | 0.75 (div) | 0.75 | 0.75 |
| 212 | 3 (mod) | 3 | 3 |
| 213 | 81 (pow) | 81 | 81 |
| 214, 215 | 1 | 1 | 1 |
| 216–223 | halts | halts | halts |
| 224–230 | runs, empty value | same | same |
| 231 | **crash** | engine **dead** | halts |
| 232 | halts; crashed once on the re-check | halts | halts |
| 233–235 | runs, empty value | same | same |
| 236–240 | halts | halts | 236–239 empty, 240 halts |
| 241 | runs, empty value | same | same |
| 242 | **crash** | engine **dead** | halts |

So 208–215, which fuse arithmetic with assign, run as plain binary operations on the two stack values when they arrive raw. **[lab][inf]** Seihai predicts an empty value for all of them. 4.20r8 has folds only up to 233, so 231 and 242 written raw only halt there.

## GS2: crashes and dead engines outside the opcode sweep

**6.03r7 crashes:**
- An operand marker 0xf7–0xff where a second operand would be. 5.24r4 and 4.20r8 run these with an empty value. Markers 0xf3–0xf5 there give an empty value on all three.
- A slot store (45) into slot 1024, 4000 or −1.
- Opcodes 48 and 49, which 6.03r7 does not dispatch.
- Six single-byte flips in the code segment.
- One random expression (case 30789) that combines `getangle`, `^` with a tiny exponent, and `substring` with a huge length.

**Engine stops and stays dead, no crash:**

| Case | 6.03r7 | 5.24r4 | 4.20r8 |
| --- | --- | --- | --- |
| The code segment twice | dead | silent | dead |
| Slot store (45) into slot 1024, 4000 or −1, then a load (46) | crash | **dead** | matches Seihai (0) |
| Object literal (48) with n = 1, value-then-name order (case 30395) | crash | **dead** | empty value |
| Raw fold bytes 231 and 242 | crash | **dead** | halts |

**Silent on all three clients** (Seihai runs them): an unknown segment type placed first, the segments in reverse order, and the code segment twice.

### Why case 30789 crashes 6.03r7 (static read, 2026-11-25)

The expression is `(((2 in |"  pad  ", -0.0001|) + (-0.0001 >= 0.00011)) * getangle((-2147483649 ^ 0.000000001), ("a").substring(2.00001, 2147483647)))`. The fault is in **`substring` (opcode 115)**, not in `getangle` or `^`. GS2 is a stack machine, so `getangle`'s second argument — the `substring` — is evaluated first and faults before the `getangle` opcode runs. `-2147483649 ^ 0.000000001` is a negative base to a non-integer exponent, so `pow` returns NaN, which is only a pushed value (6.03r7 prints it as `0.-000000000`); the range test and `>=` just produce 0. **[bin]**

`("a").substring(2.00001, 2147483647)` on a one-character string hits a signed-overflow bug that all three builds share. The start `2.00001` becomes `floor(x + 0.0001)` = 2, clamped down to the length (1). The length 2147483647 (INT_MAX) is not re-clamped, because the bound test is signed: `start + length` = 1 + 2147483647, which wraps to −2147483648, the most-negative int, so the signed `≤ strlen` test passes and the "length = strlen − start" fixup is skipped. The copy count handed to the string-grow helper is then `end − start` ≈ 2.1 billion.

The builds differ only in that terminal grow/append helper:

| Build | Grow/append helper | Result |
|---|---|---|
| 6.03r7 | no length cap and no allocation-success check: requests ~2 GB and writes through the result unconditionally | **faults** — access violation on Windows; on Linux the ~2 GB libstdc++ resize throws with no catch around the VM, so the client terminates |
| 4.20r8 | caps the copy at 1,000,000 bytes (it skips the copy when the count is larger) | empty string (the "substring with a huge length → empty" row above) |
| 5.12 | no cap, but tests the ~2 GB allocation result and bails on failure | empty string |

So 6.03r7 is the odd one out: it carries the same signed-overflow length bug as 4.20r8 and 5.12 but dropped both guards (the million-byte cap and the allocation-null check). Seihai's own VM predicts the script completes with value 0, so a server's own run of this script would not reproduce the client crash.

Caveats: the lab crash was on **Linux** 6.03r7 while the static target was the **Windows** 6.0.3.7 unpack (same C++ handlers; only the fault flavour differs), and 5.24r4 was not located, so 5.12 stood in for 5.x. Confidence is high on the dispatch, handler and guard reads, and medium-high (from the libstdc++ contract) on the exact Linux fault type.


## GS2: limits

- **Loop passes.** A `while` loop of 10001 passes finishes on 6.03r7 (`ran-past`). 5.24r4 and 4.20r8 stop it, as Seihai predicts.
- **`maxlooplimit`.** Setting it to 50 reads back as 100, so the value is clamped from below, and a loop of 120 passes then finishes on 6.03r7 and 5.24r4. With `maxlooplimit` 2000000, a loop of 20000 passes stops.
- **Call depth.** Recursion 9999, 10000 and 10001 deep finishes with the value 0 on all three clients. Seihai predicts a call-stack overrun.

## GS2: damaged containers

- Cutting 1 or 5 bytes off a segment still runs the script.
- A jump target of 9999 or −1 runs on, and the script reports 7.
- A string index past the end of the string table gives an empty value.
- **F6 decimal text** is read like C `atof`/`strtol`: `"0x10"` is 16, `"12abc"` is 12, `"1,5"` is 1, `"  3"` is 3 and `""` is 0. `-0`, `nan` and `1e-400` load as −1, and on 5.24r4 so does `inf`.
- **4.20r8 clamps big numbers to 4294967295:** `"1e400"`, a long run of 9s, `99999999999` and `2147483647*1e9` all give 4294967295, while `-2147483649` stays as it is.
- 6.03r7 prints NaN as `0.-000000000`.

## GS2: which texts read as −1

A follow-up run (`numtext`, 94 cases on 4.20r8, 5.24r4 and 6.03r7) put 23 texts through `+ 0`, `!`, `== 0` and `== -1`. The 6.03r7 Linux client's text-to-number routine was also read. **[bin][lab]** It works in this order:

1. `""` is 0, `"true"` is 1 and `"false"` is 0.
2. A text that starts with `0x` is read as hex (`strtoul`, base 16). Any other text goes through `strtod`.
3. A zero result stands only when the text is exactly `"0"` or `"0x0"`, or `"0.0"` on 6.03r7. Anything else that reads as zero returns −1, the client's "not a number".

| Text | 4.20r8 | 5.24r4 | 6.03r7 |
| --- | ---: | ---: | ---: |
| `"0"`, `"0x0"`, `""`, `"false"` | 0 | 0 | 0 |
| `"0.0"` | −1 | −1 | 0 |
| `"00"`, `" 0"`, `"0 "`, `"+0"`, `"-0"`, `".0"`, `"0."`, `"0e5"`, `"0abc"` | −1 | −1 | −1 |
| `"abc"`, `"a1"`, `" "`, `"null"` | −1 | −1 | −1 |
| `"true"`, `"1"`, `"000001"`, `"1abc"` | 1 | 1 | 1 |
| `"-1"` | −1 | −1 | −1 |

So `!` of any text in the −1 rows is 0, `== 0` is false and `== -1` is true. A script notices this when a variable holds a name or a word: `this.mode == 0` is false for a name, and a text flag `"true"` equals 1. The 4.20r8 and 5.24r4 routines were not read, and their rule is inferred from the run. Seihai's GS2 VM follows the rule from seihai-core PR #120 on; GS1 keeps 0, because GS1 reads a text in `#v` as 0.

## GS2: value rules that differ from Seihai's VM

Unless a line names one client, these hold on 4.20r8, 5.24r4 and 6.03r7.

- **A string that is not a number converts to −1, not 0.** So `min(1000000000, "\"q\"")` is −1, `arctan("a")` is −0.785398…, and `format("<%5.2f>", "  pad  ")` is `<-1.00>`. `"1e3"` reads as 1000.
- **`!` of a non-empty string that is not a number is 0.** Seihai gives 1.
- **Opcodes 66 and 67 treat any string operand as true**, so 66 on `""` and `""` gives 1.
- **`tokenize().size()` of a single value is 1**, and of `"a,b,c"` it is 3. Seihai gives 0.
- **`%f` and `%5.2f` follow C printf.** For example, `<%5.2f>` of 31 is `<31.00>`.
- **`substring` with a string as its length returns the rest of the string.** Seihai returns an empty string.
- **`in |…|` with string members differs**: `("abc" in |"a,b,c", "1.00000"|)` is 0.
- **Opcode 104 (object compare) on strings:**
  - 6.03r7 returns a byte difference, like `strcmp`: `""` vs `"x"` is −120, `"x"` vs `"3"` is 69, and `"3"` vs `""` is 51.
  - 5.24r4 mostly matches Seihai.
  - 4.20r8 gives 0.05 for any string, and 2 against 0 or 2 gives 2.
- **Opcode 121 is a numeric add on 6.03r7 and 5.24r4**, with a non-number counted as −1: `"x"+0` is −1, `"x"+2` is 1 and `"3"+2` is 5. It does not join strings. 4.20r8 does not dispatch it and gives an empty value.
- **Opcode 54.** On 6.03r7 and 5.24r4 every push order matches Seihai's prediction: `this.k` reads back 0, so nothing lands in `this.k`. 4.20r8 does not dispatch it and gives an empty value.
- **Opcodes 48 and 49** give an empty value on 5.24r4 and 4.20r8 and crash 6.03r7, so their operand order is still not settled: the 5.00r7 and 5.12 builds, which dispatch them, were not run.
- **5.24r4 does its maths in single precision.** `3.14159265358979` prints as 3.141592656 and `0.123456789999` as 0.123456792, and `getangle` and `arctan` values differ in the last digits.
- **Integer edges differ by build**:
  - `(-1 & -2147483649)` gives 2147483647 on 6.03r7.
  - `x >> "a,b,c"` gives −1 on 6.03r7 and 0 on 5.24r4.
  - `-2147483648 % -1` gives −2147483647 on 5.24r4.
- **A slot store (45) of 9, then a pop, then a slot load (46) reads back 0** for slots 0, 1, 5 and 1023. Seihai gives 9. One likely reason is that a function's slots exist only once its own code sets them up, and the spliced sequence never did that. **[inf]**

## GS1: 2.05, 2.22 and 2.31

No GS1 case crashed a client. 2.05's engine stopped for good after one damaged script, `fzr = ();` (empty parentheses), which 2.22 and 2.31 run without trouble.

- **Message codes read the live player and world.** Seihai leaves these literal or empty.
  - `#L` gives the level, `#a` the account, `#n` the nick and `#m` the gani.
  - `#w` gives the weapon, `#W` its image, and `#k(0)` gives `Up`.
  - `#1`, `#2`, `#3` and `#8` give the sword, shield, head and body images, and `#C0`–`#C2` give the colours.
  - `#g`, `#f`, `#S` and `#D` are empty, and `##` gives `#`. On 2.05, `#P1` and `#P1(-1)` are empty.
  - `#c` gives the current chat, so the player's chat is sent twice.
- **Other message-code results:**
  - `#e(2,-1,abcdef)` is `cdef`, so a negative length means "to the end".
  - `#e(1,2)` stays literal on 2.22 and 2.31.
  - `#t(-1)`, `#s()` and `#s(nosuch)` are empty, except that `#s()` on 2.05 returned the tail of an unrelated string (`lient.gs1ok`), which looks like a read from a stale buffer. **[inf]**
  - An unclosed code such as `#v(` stays literal on 2.22 and 2.31; 2.05 drops the `#` and the letter and keeps `(`.
  - `#v()` and `#v(#v(2))` are 0, so `#v` does not nest.
  - `#I(fzs,0)` gives the first token, `hello`, not `hello world`.
- **Fuzzy equality arrived after 2.05.**
  - On 2.22 and 2.31, `1 == 1.00001`, `1 == 1.0001` and `0.1+0.2 == 0.3` are true, and `1 < 1.00001` is false.
  - On 2.05 all four are exact, matching Seihai's 2.05 column.
  - `#s(fzs) == hello` is true on all three, because it compares the first token, and `1 && 0 || 1` is 0.
- **String functions on 2.22 and 2.31** (2.05 matches Seihai here): `strcontains(#s(fzs),ll)`, `strcontains(abc,)` and `lindexof(b,a,b,c)` are 0, and `3 in <1,3>` is 0. On all three, `indexof(,abc)` is 1, and `strlen(x,y)` is 0; `ascii(x,y)` is 0 on 2.22 and 2.31.
- **The loop limit caps a loop and the script carries on.** `while` and `for` loops stop at 10000 passes and the script finishes, where Seihai predicts a stop. Nested loops count toward the same limit: 100 × 100 gives 9901.
- **Number text:**
  - 2.05 and 2.22 compute and print in single precision: `2147483647` prints as `2.147484E9`, `99999999999` as `1E11`, and tiny values such as `-0.000000001` as 0. 2.31 prints nine decimals in double precision.
  - `1e3` is 1000 on all three. Seihai reads it as 0.
  - `31 % 0.00009` is 0 on 2.05 and 2.22, and `(-32 % -1e3)` is −32 on 2.05.
- **Overflow differs by build.** An overflowing `^` (such as `33 ^ 2147483647`) gives `INF` on 2.22 and halts the script on 2.31; on 2.05 some halt and some give a value. `int()` of a value past 32 bits halts on 2.31, prints `-2.147484E9` on 2.22, and wraps on 2.05 (`int(4294967296)` is 0, and `int(-2147483649 * 10)` is −10).
- **Unary minus.** `--int(3)` is −3 and `(cos(1.5) / --7)` is −7, where Seihai gives an empty value; `((0.5 - -1) - (0.5 * -1))` is 0, where Seihai gives 2; and `-(-0.5 ^ 2) * cos(-3.14159)` is −0.25. So `- -` and a leading minus do not parse as Seihai parses them.
- **Script errors stop the script.** A missing `;`, an unknown command or a command with no arguments halts the script. Seihai continues past all three. A `with` with no target halts on 2.05 and gives 4 on 2.22 and 2.31.
- **Damaged scripts:** `1.2.3` is 0, while Seihai gives 1.2. A doubled operator gives 0, a string variable in `#v` gives 0, and a string with high bytes has length 7 where Seihai counts 4.

## For Seihai

Each `differs` row above is a candidate fix for seihai-core's GS2 VM or GS1 engine. The rules seen on all clients come first: −1 for a string that is not a number, `!` of a string, single-value `tokenize`, printf formatting, F6 text read like `atof`, call depth past 10000, the live GS1 message codes, the GS1 loop cap, `1e3` in GS1, and stopping on GS1 script errors. The per-build rules come next: fuzzy equality from 2.1, single precision on 2.05, 2.22 and 5.24r4, the 4.20r8 clamp at 4294967295, opcodes 104 and 121, and the integer edges. Seihai should also refuse undispatched bytes for 6.x Linux, as the opcode table already advises.

## Still open

- [ ] Runtime behavior of opcodes 48 and 49 on a build that dispatches them (5.00r7 or 5.12). The [retained 5.00r7 backup-engine handler read](gs2-client-only-opcodes.md#48-and-49-retained-500r7-backup-engine) supplies a bounded static contract; genuine 5.12 and runtime validation remain open.
- [ ] The value `waitfor` gives when its time runs out. The three cases did not settle it. A separate [static follow-up](../client-internals/gs2-wait-results-2026-11-22.md) binds saved-one preparation, deadline payload zeroing and conditional restoration in two selected inputs; it does not supply a new native timeout experiment.
- [x] ~~Why the expression in case 30789 crashes 6.03r7.~~ [Answered 2026-11-25](#why-case-30789-crashes-603r7-static-read-2026-11-25): a shared signed-overflow in `substring`, with both of 6.03r7's length guards dropped. **[bin]**
- [ ] Why control 30000 reads `stopped` on 5.24r4 while 30001 and every canary reported.
