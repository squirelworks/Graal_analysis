# GS2 compilers compared: Preagonal `dev`, gs2-parser and Seihai (2026-11-26)

Question: is Preagonal's GS2 compiler on its `dev` branch newer than what this project
already uses, is it the same thing the GServer-v2 ("Preagonal GS2Emu") server uses, and
what would Seihai gain or risk by leaning on it?

Method: all four compilers were built in a cloud container and run as black boxes on the
same inputs. Nothing was run against a client or a game server. No code from any of them
is quoted here or copied into a Seihai repository; this note gives counts and behaviour.
Tags: **[test]** for the runs in this note, **[doc]** for what the Preagonal tree says
about itself, **[src]** for build files read, **[cap]** for our earlier official-body notes.

## What each compiler is

| Compiler | Commit | Licence | Where we use it |
| --- | --- | --- | --- |
| Seihai GS2 compiler, `seihai-core` `scripting::gs2::compile` | `848323b` (main, 2026-11-25) | MIT OR Apache-2.0, our own code | the Seihai client and the MIT servers. Written from `documentation/gs2-opcodes.md`, the gs2-parser fixtures, and black-box probes of the two open compilers ([gs2-strict-probes-2026-11-13.md](gs2-strict-probes-2026-11-13.md)) |
| gs2-parser (`xtjoeytx/gs2-parser`) | `73e7ea8` (2026-02-07) | GPL-3.0 | compiled into `seihai-gserver-v2` (`server/CMakeLists.txt` pins `73e7ea8`), the same pin as upstream GServer-v2 `beta4` **[src]**. This is "the compiler from the Preagonal server" we have been running. The strict-mode probes used gs2-parser main `4fa0a26` |
| Preagonal.Scripting.GS2Compiler `main` | `7878bc5` (2026-06-29) | MPL-2.0 | read in [preagonal-gs2.md](preagonal-gs2.md) and used as the second black box for the strict-mode probes. Still the `main` tip today |
| Preagonal.Scripting.GS2Compiler `dev` | `3568f38` (2026-11-20) | MPL-2.0 (same `LICENSE` blob as `main`) | not used by us before this note |

`seihai-gs2lib` is the GPL fork of gs2lib, the server's utility library (strings, files,
encryption, version tables). It has no GS2 compiler in it.

`dev` is 36 commits ahead of `main` and `main` has nothing `dev` lacks: about 16 000 lines
added, mostly tests and evidence files **[src]**. It targets .NET 11, takes its shared
syntax tree and ANTLR grammars from a `Preagonal.Scripting.GSAst` 0.0.5 package on
Preagonal's own NuGet feed (the package states no licence, and its source repository is
not public), and adds a NativeAOT library with a C++ header whose `GS2Context::compile`
mirrors gs2-parser's call so a gserver can link it in place of gs2-parser **[src]**.

Upstream GServer-v2 has a `feature/new-gs2-compiler` branch (2026-11-22) whose vcpkg port
builds exactly Preagonal `dev` `3568f38` **[src]**. Its `beta4` and `master` branches, and
our fork, still use gs2-parser. So the Preagonal server is moving to this compiler, but
nothing we have built or run so far used it.

## What changed on `dev`

The large change is the reference. `main` was tuned to match gs2-parser's output (its
`CORRECTNESS.md` scores against "copied C++ baselines"). `dev` was re-tuned against fresh
output of the official server-side compiler, captured through a headless tool that
uploads a weapon script to an official server and reads back the bytecode **[doc]**
(`PARITY.md`, `tests/official-baselines/README.md`). The tree holds 151 usable official
captures with their sources (99 fixture scripts, 52 focused probes and the feature script)
**[test]**. `PARITY.md` also claims GS1-to-GS2 parity with the official compiler on 270 GS1
weapons and several whole GS1 levels; those GS1 fixtures are kept private, so that claim
was not re-run here **[doc]**.

Behaviour `dev` adds that `main` and gs2-parser do not have **[doc][test]**:

- the variable cache: opcodes 45, 46 and 47, which store, load and resolve a per-function
  slot. 78 of the 151 official bodies use them. This is the trio our official 6.113
  bodies already showed and that no open compiler emitted
  ([gs2-official-varcache-functable-partial-2026-11-16.md](../protocol/gs2-official-varcache-functable-partial-2026-11-16.md) **[cap]**);
- `params` as opcode 190 (14 of the 151 bodies), which `main` never emitted;
- no extra `OP_RET` at the end of a script that has no top-level code, and the narrowest
  operand width for jump targets;
- GS1 source as input (`ScriptGrammar.GS1`), compiled to GS2 bytecode;
- `goto` and labels, which the official compiler rejects; Preagonal marks them as its own
  extension **[doc]**;
- the response lists the classes a script `join`s, which a server needs.

## Runs

Each compiler got the client-side part of the source (the text after `//#CLIENTSIDE`).
"Exact" is byte-for-byte equal to the official capture. "Same shape" ignores operand
widths, string-table numbering and one trailing `OP_RET`, and compares the instruction
list and function table.

### 151 official captures from the Preagonal tree

| Compiler | Exact | Same shape | Different | Rejected |
| --- | ---: | ---: | ---: | ---: |
| Preagonal `dev` | 146 | 5 more (only generated lambda names differ) | 0 | 0 |
| Preagonal `main` | 0 | 13 | 119 | 5 |
| gs2-parser `73e7ea8` | 0 | 13 | 117 | 7 |
| Seihai, legacy mode | 0 | 21 | 116 | 7 |
| Seihai, strict mode | 0 | 21 | 111 | 13 |

**[test]**. These fixtures were collected and fixed by Preagonal against this same oracle,
so `dev`'s score is expected; it shows the shape of the official output, not how `dev` does
on scripts it has never seen.

None of the older compilers produces an exact official body. The first difference is
usually the variable cache (official loads a slot where we push the name again), then the
extra final `OP_RET` and the 16-bit jump placeholder, then `temp`/`params` handling and
some `makevar`/conversion choices **[test]**. Seihai's output is closer to the official
shape than gs2-parser's on this set (21 against 13), and agrees with gs2-parser far more
than with `dev`.

Seihai's reader refused 8 of the 151 official bodies: every one has `OP_IN_RANGE` (80)
with an integer operand, and `Script::parse`'s validator only accepts it with no operand.
Our own capture note already says 80 carries an integer operand
([gs2-official-bytecode-6113.md](../protocol/gs2-official-bytecode-6113.md) **[cap]**), so
this is a Seihai reader bug, not a Preagonal oddity **[test]**. Seihai's VM already runs
45–47; only its compiler does not emit them.

### Scripts with no official capture

| Corpus | Files | Accepted (dev / gs2-parser / Seihai legacy) | Same shape: dev=gs2-parser, dev=Seihai, gs2-parser=Seihai |
| --- | ---: | --- | --- |
| Seihai `tests/fixtures/gs2` | 12 | 12 / 12 / 12 | 4, 4, 10 |
| Preagonal `tests/scripts` (not error cases) | 176 | 176 / 175 / 175 | 31, 34, 69 |
| Preagonal `tests/scripts/error_cases` | 3 | 0 / 0 / 3 | — |
| Graal_analysis `torque/conformance/scripts` (3D probes) | 7 | 7 / 7 / 7 | — |

**[test]**. Everything except the error cases compiles with all three. Seihai's legacy mode
takes the three error cases on purpose (it reads old-server quirks). Seihai and gs2-parser
are still one family; `dev` has moved away from both, towards the official output.

## Client builds and the 5.12 3D surface

The compilers do not know game commands. `GameObject`, `Sky`, `findobject` and the other
names in the typed 5.12 surface ([gs2-3d-typed-surface-512-2026-11-26.md](../torque/gs2-3d-typed-surface-512-2026-11-26.md))
are calls by name, so all three compile the 3D probes, and the client build decides what
runs **[test]**. The relevant client question is only whether every GS2 client runs what
`dev` emits: our VM-by-version note has 45, 46 and 47 in every client build read, and 190 is
there from 3.153 on ([gs2-vm-by-version.md](../client-internals/gs2-vm-by-version.md) **[bin]**).
The official captures come from today's server, so they show what a current client gets,
not what a 4.x-era server sent. No 4.x or 5.x client ran any of this output.

## Answer

- **Newer?** Yes. `dev` (`3568f38`, 2026-11-20) is four and a half months past the `main`
  tip we studied and black-boxed, and it is the only open compiler checked against the
  official compiler rather than against gs2-parser.
- **Same as the Preagonal server's?** No, not yet. Our `seihai-gserver-v2` and upstream
  `beta4` compile with gs2-parser `73e7ea8`. Upstream's `feature/new-gs2-compiler` branch
  switches to exactly this `dev` commit, so it will be the server's compiler once that
  branch lands.
- **Licence.** MPL-2.0, file-level copyleft. Compare behaviour and output; do not copy,
  port or translate it into `seihai-core`, `seihai-gserver` or any MIT/Apache repository.
  Its GSAst dependency has no stated licence and no public source.

What we would gain by using it as a reference (black box only):

- an oracle much closer to official output: the variable cache, `params`/`temp` opcodes,
  narrow jumps and no trailing `OP_RET`, all of which our official 6.113 captures showed;
- a way to check Seihai's GS1-to-GS2 lowering against something tuned to official GS1
  output, which we do not have today;
- if the GPL fork follows upstream, `seihai-gserver-v2` would send official-shaped
  bytecode to v4+ clients, which makes lab runs more like the real server.

What we would risk:

- `dev` builds only with .NET 11 and a package from Preagonal's own feed with no stated
  licence; a lab or CI step that needs it depends on that feed staying up;
- 146 of 151 is on Preagonal's own fixtures; on scripts it was not tuned on it may still
  differ from official, and it includes `goto`, which official rejects;
- copying any of its choices as code, rather than re-deriving them from our captures and
  tests, would put MPL-2.0 text into MIT/Apache trees.

Follow-ups for `seihai-core` (not done in this note):

- [ ] accept `OP_IN_RANGE` with its integer operand in `Script::parse` (8 official bodies
  refused);
- [ ] emit the 45/46/47 variable cache, drop the extra final `OP_RET` and use the narrowest
  jump operand, each re-derived from our own official captures and checked against `dev`
  as a black box;
- [ ] compare Seihai's GS1 lowering with `dev`'s GS1 front end on the owner-held world corpora.
