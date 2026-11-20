# Static reads for Appendix E, fifteenth batch (2026-11-20)

Date: 2026-11-20. Evidence: **[bin]** (linear disassemblies of the native engine library in the
Android packages Classic 1.8, Classic 2.2, Era 1.7 and Era 2.0, compared function by function; no
client run). Only behaviour is given here. Covers App. E#209, the Android rows of
[gs2-vm-loader-diff.md](gs2-vm-loader-diff.md#android).

## What each package holds

| Package | Engine builds | Engine names |
| --- | --- | --- |
| Classic 1.8 | ARM, ARM64, x86, x86-64 | exported in plain C++ form |
| Classic 2.2 | ARM, ARM64, x86, x86-64 | exported, but every engine class and method name is replaced by random letters; the argument structure of each name is kept |
| Era 2.0 | ARM, ARM64 | the same kind of renaming, with different random names from Classic 2.2 |
| Era 1.7 | ARM only | stripped (188 exported names, none of them engine names) |

Library code (zlib, bzip2, FreeType, the image decoders and the TLS library) keeps its names in
every package.

## How the later builds were matched to Classic 1.8

Each function was reduced to its instruction sequence with addresses and constants masked, and the
sequences were compared between builds. A renamed name keeps its argument types, so a match can
also be checked against the signature.

| Comparison | Functions of 20 or more instructions | Identical after masking |
| --- | ---: | ---: |
| Era 2.0 against Classic 2.2 (ARM64) | 3,475 | 99.5% |
| Classic 2.2 against Classic 1.8 (ARM64) | 3,402 | 84.6% |
| Classic 2.2 against Classic 1.8 (x86-64) | 3,347 | 78.5% |

**Era 2.0 and Classic 2.2 have the same engine.** Every script-machine function checked below is
identical between them, including the main execution loop (3,922 instructions on ARM64). So what
follows for Classic 2.2 holds for Era 2.0.

## Classic 2.2 against Classic 1.8

- **Opcode dispatch.** Both main loops switch on the decoded opcode byte through a 243-entry table
  (0 to 242), and the same 165 opcode numbers have their own handler in both. The other numbers
  take the no-handler path.
- **Which of 48, 49, 54, 121 and 164 exist.** In both builds 54 and 121 have handlers, and 48, 49
  and 164 do not. The fold pass rewrites only fused groups, to ids of 200 and above, and leaves other
  instructions under their file numbers; it tests file numbers such as 50 directly. So 48, 49 and
  164 in a script continue without popping on Android. The loader that fills the decoded table
  was not followed, so this rests on the fold pass keeping file numbers.
- **The execution loop changed little.** The x86-64 loop grew from 4,140 to 4,202 instructions,
  89% alike. The differences seen are a changed string layout and a 40-byte decoded instruction
  in place of 32 (both x86-64 sizes, not file format), and one case that now picks a constant by
  comparison where 1.8 read it from a table. No change of behaviour was found in the parts
  compared, but the loop was not read case by case.
- **Unchanged functions.** The stack setup and growth (by 100), the array size cap of 10000, the
  call-stack refusal at 10000, the event-queue refusal at 1000, the
  loop-limit getter and setter, and the event-function lookup are instruction-identical, or differ
  only by string layout while keeping the same limits.

## Event names ignore case (1.8, 2.2 and Era 2.0)

To find the function for a fired event, the engine puts `on` in front of the event name and looks
it up in the script's function list with a case-ignoring lookup. If it is not found, it asks each
joined class in turn.

- The list's hash folds `A` to `Z` to lower case before mixing each byte, so names that differ
  only in case land in the same bucket.
- The comparison also folds `A` to `Z`.

So `onTimeout` and `onTimeOut` select the same function in Classic 1.8, Classic 2.2 and Era 2.0.
This matches 6.03r7 ([static-reads-appendix-e-2026-11-20-j.md](static-reads-appendix-e-2026-11-20-j.md#event-names-and-the-function-table-603r7)).

## The loop limit on Android

- The per-script loop budget is a field of the script space, set to 10000 when the space is made
  and read into the loop counter each time the machine starts.
- Its setter clamps the value to 100 to 1,000,000; its getter returns 10000 when there is no
  script space. This matches the desktop fuzz result where 50 read back as 100.
- The property is registered under a scrambled name. Decoding it with the engine's own lookup rule
  gives `ma`, a zero byte, then `looplimit`, the same oddity the 6.x read found
  ([static-reads-appendix-e-2026-11-20-j.md](static-reads-appendix-e-2026-11-20-j.md#the-6x-loop-limit-name)).
  The same stored bytes are in all four Android packages.
- Under that rule the stored third character does not equal `x`, so a lookup of `maxlooplimit` by
  the routine as read would miss it. On 6.03r7 a script run did reach the property by that name.
  Which is right for Android needs a run; this read does not settle it.

## What this settles

- Android Era 2.0 is the same engine as Classic 2.2, and Classic 2.2's script machine has the same
  opcode set as Classic 1.8.
- On Android, opcodes 54 and 121 exist and 48, 49 and 164 do not.
- Event-function lookup ignores case on Classic 1.8, Classic 2.2 and Era 2.0.

## Not covered

- Era 1.7 (stripped, ARM only). It holds the same scrambled loop-limit name, and nothing else was
  compared.
- Classic 1.6, 1.7 and 2.0. They are held but were not read for this batch.
- The loader that turns file bytes into the decoded table.
- Whether `maxlooplimit` is reachable by name on Android.
- The 2.2 execution loop case by case.
