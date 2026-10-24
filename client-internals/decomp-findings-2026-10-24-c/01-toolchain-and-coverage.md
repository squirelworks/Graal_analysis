# 01 Toolchain and coverage

Derived facts only. No raw decompile text, addresses or generated function names are in this folder. Raw exports are kept private and are not in any repo. Run date: 2026-10-24 (Asia/Tokyo).

## Result
- All 20 requested builds were decompiled with Ghidra 12.2 headless (JDK 25), at most 2 jobs at a time. No job hit the 7200 s limit and no job failed. Per-build table: `coverage_by_build.tsv`.
- Builds: 2.00 (main) and revs 1-3; 2.01 and rev1; 2.02, rev1, rev2; 2.03; 2.04; 2.05, rev1, rev2; 2.1 test2 and test3; NewWorld beta1/beta2; NewMain 24/26.
- 2.05 rev2 and 2.00 main already had decompiles. They were re-run only as a diff baseline (same pipeline, so differences are not tool artefacts).
- Each export holds about 5,480-5,720 functions. Most are VCL/RTL, JPEG library and DirectX wrappers. About 100 are game classes.

## Why plain Ghidra output was not enough (Delphi finding)
- Every build is a Delphi 3/4/5-era PE (CODE/DATA/BSS sections, VCL RTTI). Plain auto-analysis missed about 520 functions per build, including the whole server-to-client packet switch and some real senders.
- Fix, in two Ghidra scripts run per build before export:
  1. Create functions at standard Delphi prologue sites that analysis skipped.
  2. Rebuild the packet dispatcher as one function from its jump table plus the byte index table in front of it. The table is indexed by `id` and has 0x9b..0xa9 entries depending on the build.
- Without step 2 the handled-id set per build cannot be read from the decompile at all. With it, the sets in `plo_handled_ids_by_build.tsv` match the 2.05 set already documented in the repo (59 ids), which is the check that the method is sound.
- Lesson for any later pass on another Delphi build: always check that the dispatcher exists as a function and that the jump-table size matches the "last index" in `plo_handled_ids_by_build.tsv`.

## IDR (Interactive Delphi Reconstructor) status
- IDR 2.x runs under Wine 10 on a private virtual display, driven by xdotool. It works for every build. The first attempt on 2.1 test2 failed (a stray click opened a form preview) and the retry succeeded.
- 20 of 20 IDC name tables were produced (about 6,590-6,730 names each: RTTI classes, RTL, VCL and the application's own methods). They were substituted into the Ghidra C export. About 27-29k substitutions per build.
- Value: the dispatcher cases, the login function and the senders become identifiable. Method names of the game's own classes (TAdventureClient, TPlayer, TAdventureLevel, ...) are the only game-specific names IDR can recover. Packet handlers themselves are anonymous bodies in one switch, so their names come from gs2lib (`PLO_*` by id) and not from IDR.

## Method for the tables
- PLO ids handled: dispatcher jump table minus the shared default arm.
- PLI ids sent: the union of (a) constant-id send calls found in the decompile and (b) an assembly scan for the same call pattern. The union is needed because one 2.03 sender (id 80) is missing from the decompile but present in the assembly. Id 6 (chat/TOALL) is a real sender in every build. The earlier "may be a false positive" remark in batch b was wrong.
- Handler layouts: heuristic scan of how a handler reads the payload (GCHAR/GINT2/GINT3 reads, rest-of-string copies, length guards). It is exact for simple handlers and incomplete for long ones. `plo_decode_signatures.tsv` records the result and is not authoritative for long handlers.
- Handler change detection: normalized statement shapes (names, big numbers and casts removed), compared with a sequence-similarity ratio. See `handler_shape_changes.tsv`. Small bodies (4-12 statements) change shape from compiler noise, so only large drops in similarity count.

## Limits
- The 2.1 test decompiles drop some arguments and calls (the Ghidra decompiler loses some register arguments in that compiler version). Structural facts (ids, field counts, which handler changes) are reliable. Exact argument values are not.
- The raw exports are private. Re-running needs the lab's private tool folder (Ghidra, IDR; not in a repo).
