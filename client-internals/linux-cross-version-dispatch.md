# Bound later Linux dispatch ranges and observed cached jumps

The editor reviewed only the sanitized 2026-11-09 Linux cross-version handoff and matched its supplied SHA-256. Observations and original private-carrier digests are researcher-supplied, not independently re-run or authenticated by the editor. No raw code, capture text, script body or client asset was inspected for publication. Evidence keys below resolve via [the source index](../workingpapers/sources.tsv). They identify actual owner-held carriers; proposed key-based JSON aliases are not materialized records or new Evidence IDs.

Runtime observations use owned isolated Linux guest/process workflows with no server or server commit, no online login/gameplay and ordinary debugger breakpoints. New probes patch neither executable/signature checks nor script input. Bounded termination and owned-group cleanup do not assert that every system process was inspectable; separately identified unreadable kernel workers are outside the owned client/debugger group.

## Exact executable inputs

[bin] Source `LNX-INPUT-IDENTITIES-20261109` is a materialized sanitized identity record whose digest the editor matched. Its executable identities were rechecked by the researcher. Release names remain owner-held labels; executable-byte hashes are not installer-container hashes. Later analysis copies are byte-identical to their original executables. For 3.04, original packed and UPX-decompressed analysis bytes are separate identities.

- 4.04r2-x86 (i386, ELF32): original executable SHA-256 `50f2057117cfafd5a1151d6e6fdd1413095fa71445ff274bf923ce7dc04198aa`; analysis ELF has the same hash.
- 4.20r6-x86 (i386, ELF32): original executable SHA-256 `a994afd24f5ebdcf73647ffe8b6752274a6c874058cb0db05c525bab060224d0`; analysis ELF has the same hash.
- 4.20r8-x86 (i386, ELF32): original executable SHA-256 `566cd371464568436265c32976babf2faa95b5fc71cce1f26cbd860b406c2a91`; analysis ELF has the same hash.
- 6.01r1-x86 (i386, ELF32): original executable SHA-256 `9a2cd037cd3de2ed1dcfc6e9665f5d11854862ef521397f593fa7dd8ffd64a3d`; analysis ELF has the same hash.
- 6.01r1-x64 (x86_64, ELF64): original executable SHA-256 `3f4fbb802fe5e99fd235833e45f509257e3930295a96288343f0e6ec08a141c1`; analysis ELF has the same hash.
- 6.03r7-x64 (x86_64, ELF64): original executable SHA-256 `ceeaefeb2df0668c9de921d4b967c511f85b235b25a18563534eb2f09b619c50`; analysis ELF has the same hash.

## Static dispatch classification

[bin] Both 4.20 executors guard an unsigned range ending at internal selector 233: 234 indexed positions, 80 common-fallback targets and 154 other targets. The classifications agree between revisions. The earlier 4.04 range ends at 190. Positions are not a count of distinct language operations.

[bin] The three 6.x executors cache a native destination in decoded instruction records. Their executable-target selector sets agree. A zero-extended byte allows inspection of 256 positions. The prefix through 242 contains 167 executable-mapping pointers and 76 zeros, followed by adjacent non-code data. A 243-entry table is inferred rather than a recovered declaration. Zero entries and subsequent data are not safe no-op handlers. Internal selectors are not automatically serialized wire values.

## Observed startup boundaries

[cap] Five unchanged startups reach the chosen executor entry: both 4.20 revisions, both 6.01r1 architectures and 6.03r7 x64. These are entry stops. New frame candidates are not hit, so this cohort supplies no new live frame-layout verification.

[cap] Three additional captures, one per 6.x build, compare decoded selector 23's cached target, static lookup and jump register. In each, one indirect jump is single-stepped to their shared destination, then the inferior is killed. This observes a cached jump for one startup record per build, without observing handler completion, all selectors or scheduling.

[cap] All eight captures are untruncated, exit normally, retain executable identity and verify owned-group cleanup after explicit termination. Server and commit are none. E#207 remains partial.

- [x] ~~Classify the bounded dispatch ranges and observe one cached jump per 6.x input.~~
- [ ] Measure handler completion, frame layouts and broader selector semantics independently.

## Evidence provenance

- `LNX420-R6-DISPATCH` — researcher-supplied original private-carrier SHA-256 `e9f6f1f8dc8fd698f9dab25916e60215edc2458639c16e0fdf854c35d2133f48`.
- `LNX420-R8-DISPATCH` — researcher-supplied original private-carrier SHA-256 `9da5e61594d7aff77d96a7ead17f35f62006bfc77e96befc87a2c9066c31afc4`.
- `LNX601-X86-DISPATCH` — researcher-supplied original private-carrier SHA-256 `36c65aa51a8a3fcedf494bf26c6f1292a491c96e30d6cf41badb23580f08f66d`.
- `LNX601-X64-DISPATCH` — researcher-supplied original private-carrier SHA-256 `230540ea0dd373bc90c0a29a66efbf6c061598d22ead46206e2b71df464c7108`.
- `LNX603-X64-DISPATCH` — researcher-supplied original private-carrier SHA-256 `53e64c6e50e133140a3d64d843eb467ef9ee6bf88e47dcd9a801e53bfd4aa8be`.
- `LNX-SELECTOR-CLASSIFICATIONS` — researcher-supplied original private-carrier SHA-256 `da3b8a9d31b62b07ffac6d401aba8ef23299d38cb83b6277045174d15ed4b701`.
- `LNX420-R6-ENTRY` — researcher-supplied original private-carrier SHA-256 `8cd25bc489a843d48b11e916073b56f83ec81932b1d99e2bd24152e2e5e7f05e`.
- `LNX420-R8-ENTRY` — researcher-supplied original private-carrier SHA-256 `2a540865210b0daa2e8d86a8d24943a59d80cdb9928246b82cd6a58a705038e9`.
- `LNX601-X86-ENTRY` — researcher-supplied original private-carrier SHA-256 `716fa393c2e6691580f7c1fd847fcbe0f23cae262b13018413f0e297333c4f88`.
- `LNX601-X64-ENTRY` — researcher-supplied original private-carrier SHA-256 `a03f97e96ef1d7d2e81530ad1b89e341b48233c788c2f061ede41337f4db9161`.
- `LNX603-X64-ENTRY` — researcher-supplied original private-carrier SHA-256 `011c93c2946c4f13b7ffcfa955f637693f2e927f5fc7ed50a297e796ab674ccf`.
- `LNX601-X86-CACHED-JUMP` — researcher-supplied original private-carrier SHA-256 `df1fb5dd613d065ec1c83c042fbbab14371b94dc710b17afb35a86930b8c629d`.
- `LNX601-X64-CACHED-JUMP` — researcher-supplied original private-carrier SHA-256 `06d4cb52acaa99149e2ad877fefda4ddeff862b84ae259de73b5115ddb19e56d`.
- `LNX603-X64-CACHED-JUMP` — researcher-supplied original private-carrier SHA-256 `2435f52c40e79fd59408c02802ff2f01fdb5817a1b15994290f985684987141c`.
- `LNX-RUNTIME-VALIDATION` — researcher-supplied original private-carrier SHA-256 `bbd4076a963b027897ee2646e6eef5bbb255c6d6ce624c295caa3a932577444f`.
- `LNX-RUNTIME-KERNEL-OMISSIONS` — researcher-supplied original private-carrier SHA-256 `8795d516c1d6bcbf1600c221ac061c119cc943953d0c6f8db69593da96820b20`.

- `LNX-INPUT-IDENTITIES-20261109` — materialized sanitized identity-record SHA-256 `7ce8a1cf7fb492f7a263b3c02c3cadb2c2ce25b9b2bc6135dff7335481504318`; executable hashes remain researcher-supplied.
