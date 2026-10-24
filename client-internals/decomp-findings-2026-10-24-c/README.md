# Decompile mining, batch c: Graal 2.00 - 2.1 test, NewWorld, NewMain (Ghidra + IDR), 2026-10-24 (Asia/Tokyo)

Derived facts only. No raw decompile text, no addresses, no generated function names, no code. Raw exports are private (outside every repo). Nothing was pushed, no public server was contacted, the lab was not touched.

Scope: 20 Drive builds decompiled with Ghidra 12.2 and named with IDR under Wine. Supersedes the 2.00/2.05 parts of batch b where they conflict (see 10).

## Files
| file | content |
|---|---|
| 01-toolchain-and-coverage.md | what was decompiled, Delphi/dispatcher fix, IDR, method, limits |
| 02-login-token-and-version.md | tokens per build, date reading, login shape, language packet |
| 03-framing-and-encryption.md | framing, zlib.dll in the 2.02 family, junk-byte status |
| 04-plo-server-to-client.md | handled ids per build, adds/removes, 26 history, layouts |
| 05-pli-client-to-server.md | sent ids per build, meaning of 35-38, id 6 |
| 06-handler-changes-by-build.md | behaviour changes 2.00 -> 2.1 and revision differences |
| 07-udp-channel.md | UDP channel in 2.0x, ids per build |
| 08-test-builds-newworld-newmain.md | 2.1 test2/test3, NewWorld, NewMain |
| 09-features-classes-vocabulary.md | vendor changelog vs binary evidence, classes, script strings |
| 10-open-questions-and-corrections.md | corrections to earlier notes, open items, Seihai implications |
| coverage_by_build.tsv | per build: size, function count, IDR, id counts |
| plo_handled_ids_by_build.tsv | server-to-client ids handled |
| pli_sent_ids_by_build.tsv | client-to-server ids with a send |
| id_changes_between_builds.tsv | adds/removes per step |
| version_tokens.tsv | login token and post-login send |
| plo_decode_signatures.tsv | heuristic field layouts per id (not authoritative for long handlers) |
| handler_shape_changes.tsv | per id, per step: similarity of normalized handler body |
| classes_by_build.tsv | class counts and class changes |
| script_vocab_deltas.tsv | script/identifier string changes |

## Top facts
1. Tokens: 2.00 GNW24011, 2.01 GNW23021, 2.02 GNW15041, 2.02 rev2 GNW20041, 2.03 GNW06051, 2.04 GNW24061, 2.05 and 2.1 test GNW03081, NewWorld G2N15041, NewMain GNW08011.
2. PLO sets: 53 (2.00) -> 55 (2.01: +46, +156) -> 56 (2.02: +47) -> 58 (2.03: +48, +165) -> 58 (2.04: +166, -26) -> 59 (2.05: +168) -> 61 (2.1 test: +49, +169).
3. PLI sets: 35 (2.00) -> 37 (2.01: +35, +36) -> 38 (2.02 rev2: +37 language) -> 39 (2.03: +38). No id removed. Id 6 is a real sender.
4. Revisions of one version are identical in game logic. 2.02 rev2 is the exception (new token + language packet).
5. 2.02, rev1 and rev2 import zlib.dll; all other builds carry zlib inside the exe.
6. UDP ids: 2.00 already sends 10-14, 16-20; 25 from 2.01, 26 from 2.03; PLI 36/38 are their TCP twins.
7. 2.1 test2/3: same PLI as 2.05, new PLO 49 PLAYERWARP2 and 169 UPGRADEURL. NewWorld beta1 follows the 2.05 line, beta2 the 2.1 line; NewMain is an older separate branch (2.00 minus freeze).
8. The 2.1 test2/test3 decompiles are lossy (the decompiler drops some arguments and calls). Treat every 2.1 test fact here as structure only (ids, field counts, which handler changed), not argument-level.
