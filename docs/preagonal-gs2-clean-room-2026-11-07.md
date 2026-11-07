# Clean-room GS2: Preagonal survey, 2026-11-07

Static read of the public Preagonal organisation and of the two GS2 repositories on their default branch. No C# was opened, no grammar file was opened, and no bytecode baseline was opened. Nothing was built or run. No Seihai repository was changed.

The Rust compiler stays in `seihai-core`. It is written from Seihai's own grammar, opcode notes and tests. A translation of the C# would stay under MPL-2.0, and the Seihai repositories are MIT OR Apache-2.0, so that translation is not usable there.

## Licence on the default branch

Both default branches are `main`. Both are MPL-2.0 only.

| Repository | `main` | Licence file |
|---|---|---|
| `Preagonal/Preagonal.Scripting.GS2Engine` | `f8b5f131` (2025-01-01, "Add coverage status") | MPL-2.0, the standard text |
| `Preagonal/Preagonal.Scripting.GS2Compiler` | `7878bc50` (2026-06-29, "Unify branch tips after parser parity fix") | the same blob |

GitHub reports SPDX `MPL-2.0` for each. There is one `LICENSE` and no second licence. Source files on `main` do not carry their own licence header, and they do not carry the "Incompatible With Secondary Licenses" notice. That notice appears only as Exhibit B inside the licence text itself. The `dev` branch of each repo still has that same `LICENSE` blob. Other branches were pushed later; their program text was not read.

MPL-2.0 section 3.1 requires source-form distribution of Covered Software, including a modification, to stay under MPL-2.0. A line-by-line translation is that kind of modification. MIT and Apache-2.0 are not MPL secondary licences. The Seihai client and the MIT server repositories (`seihai`, `seihai-gserver`, `seihai-listserver`, `seihai-rc`, `seihai-npcserver`, `seihai-servertools`) therefore cannot vendor, submodule, or translate these trees. GPL code from GServer-v2, gs2lib and gs2-parser stays out of those repositories as well. Packet layouts and opcode numbers already written in our own notes are facts; the C# is not a source of new ones.

## What the organisation publishes

Nine repositories. Two matter for GS2 script.

| Repository | Licence | Language | Role for GS2 |
|---|---|---|---|
| `Preagonal.Scripting.GS2Engine` | MPL-2.0 | C# | The VM. This is the one to keep away from a translation. |
| `Preagonal.Scripting.GS2Compiler` | MPL-2.0 | C# | The compiler. Same rule. |
| `HxDGraal` | MIT | C++ | A hex-editor helper for Graal packed numbers. Not a script compiler or VM. |
| `TilesEditor` | MIT | C++ | A level editor fork (gmap and nw). Not GS2. |
| `Ghidra`, `GhidraMCP` | Apache-2.0 | Java | Forks of reverse-engineering tools. Not a script spec, and not for import. |
| `nx-decomp-tools` | MIT | none on the listing | Decompiler tooling fork. Not a script spec. |
| `libtomcrypt` | no SPDX assertion | C | Cryptography fork. Not GS2. |
| `.github` | MIT | none | An empty organisation profile. |

## Engine

C# library, native project, small test application and unit tests. The readme is two lines: "Geyser II Engine" and "Repository for Geyser II VM". The package metadata names the author Preagonal and the copyright Preagonal 2023–2024. The published docs do not describe a file format, an opcode list, or a parse/compile/execute split. The repository shape is a virtual machine: a script machine, bytecode segments, an opcode file, and tests around that machine. Those files were not opened.

The only behaviour issue on the default branch says their VM runs top-level statements once, at load, and that the author believes the official client runs those statements again before each event, so a top-level assignment would not survive into the next event. That is their claim. Seihai's executor note says a top-level run starts at the first opcode and an event calls a function. It does not say a later event runs the top level again. This note does not adopt their expected result, and it does not change the executor. Confirming it needs a lab of our own.

## Compiler

C# compiler package. The readme says a caller passes source text and receives bytecode bytes, through one compile call. The arguments they document are the source, a script type (they default it to weapon), a script name (they default it to npc), and a flag for whether to include a header (they default it to included). A command-line build, a native library and a browser build are documented. The native exports they name are a context, compile with the header, compile without the header, and delete the context. Their correctness note, dated 2026-06-28, says the unit tests passed and that an advanced corpus was only partly byte-identical to a C++ baseline. Their parity note now says that same advanced corpus matches the C++ baseline byte for byte, and that `setarray` is emitted directly as opcode 39. Opcode 39 is already `OP_SETARRAY` in `squirelworks/seihai` `documentation/gs2-opcodes.md`.

Their contributor notes say to follow the engine's style and not to invent behaviour that is not in "the original". The parity note calls the comparison files copied C++ baselines. So this compiler is a C# reimplementation aimed at another compiler's output. It is not an independent specification.

Their published docs do not describe the segment layout, the operand markers, or the opcode table beyond that one `setarray` line. The header flag is a public switch with no byte layout attached. The tree contains an ANTLR grammar and a large baseline corpus. Neither was read. The corpus is not imported.

## Attribution

The files attribute the work to Preagonal: copyright lines, package author, and the engine name Geyser II. The compiler's package tags include `gs2`, `graal`, `compiler` and `preagonal`. The readmes, the licence and the package metadata do not name the Reborn project. This note does not treat community membership as permission to copy.

## What Seihai already has

On `squirelworks/seihai` `main`, `seihai-core` reads a compiled script (`Script::parse`), prints it (`disassemble`) and runs the part that overlaps GS1 (`gs2::exec`, plus the timer, string and list groups). The layout, the operand markers and the opcode table are `documentation/gs2-opcodes.md`. The language is `documentation/gs2-grammar.md`. Run-time choices and the stubs (real objects, `waitfor`, `link`, `params`) are `documentation/gs2-executor.md` and `documentation/gs2-commands.md`. The fixtures under `crates/seihai-core/tests/fixtures/gs2/` are what those notes are checked against.

Pull request 376 (`cursor/gs1-gs2-front-end-2b09`, not modified here) is the temporary compiler on that same crate. `compile_gs1` lowers GS1 with the existing grammar. `compile_gs2` accepts the small GS2 subset that emitter needs. `Script::write` encodes the four-segment file from the opcode note. The pull request says `shared.gs2` and the matching GS1 script match `shared.gs2bc` byte for byte. That is the clean-room start. It is not reimplemented in this change, and no second compiler crate is added.

`Graal_analysis` already records where GS2 appears on the wire (`manual/08-scripting/03-gs2-language.md`, `04-gs2-bytecode.md`) and says the language and the 4.x bytecode format are still open (Appendix E, item 207). A later properties note (`protocol/v7x-properties-and-gs2.md`) describes fixed-size instruction slots and a peephole range that the opcode note and the fixtures do not use. Those two descriptions are not reconciled here. The compiler spec remains the opcode note and the fixtures, not that later table, and not the Preagonal tree.

## Gaps that need a spec before code

These are not implemented. The first group is already specified in Seihai's notes, so the next code change continues pull request 376's crate from those notes. The second group is not specified there. Filling either group from the C#, the grammar file, or the baselines would be a translation, and it is refused.

Already in our notes, left for a later change on `seihai-core` (not this one, and not a new crate):

- GS2 constructs the opcode note says the compiler emits, and that the temporary front end still rejects: `with`, array literals and indexes, `new`, nested functions, an event test with `else`.
- The stubs the executor note already lists: real objects, `waitfor`, `link`, `params`.

Not in our notes, so not code until a lab or our own write-up specifies them:

- What the compiler's header flag adds or removes. Our file is four segments and one trailing byte. Their docs name the flag and do not give the bytes.
- Whether top-level statements run again before each event. Their issue says the official client does. Our executor note does not.
- Byte-for-byte parity with their C++ baselines. Those files were not read and are not a Seihai oracle.
- Anything on their unmerged branches (parameter passing, bitwise operations on nested arrays, and several compiler parity fixes). The branch names are public. The diffs were not read.

## Rule followed

Learn what the programs do from the readme, the build and parity notes, the package metadata and the issue text. Write Rust only from Seihai's grammar, opcode notes and tests. Opening their source to close a gap blocks implementing that gap in the same change. This change did not open their source, did not vendor it, and did not add a submodule. The gaps above stay uncoded. Pull request 376 remains the compiler, on its own branch.

Evidence: static read of the public docs and of Seihai's notes. No lab. No client.
