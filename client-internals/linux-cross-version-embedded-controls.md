# Compare bounded Linux embedded-script corpora across builds

The editor reviewed only the sanitized 2026-11-09 Linux cross-version handoff and matched its supplied SHA-256. Observations and original private-carrier digests are researcher-supplied, not independently re-run or authenticated by the editor. No raw code, capture text, script body or client asset was inspected for publication. Evidence keys below resolve via [the source index](../workingpapers/sources.tsv). They identify actual owner-held carriers; proposed key-based JSON aliases are not materialized records or new Evidence IDs.

Runtime observations use owned isolated Linux guest/process workflows with no server or server commit, no online login/gameplay and ordinary debugger breakpoints. New probes patch neither executable/signature checks nor script input. Bounded termination and owned-group cleanup do not assert that every system process was inspectable; separately identified unreadable kernel workers are outside the owned client/debugger group.

## Exact executable inputs

[bin] Source `LNX-INPUT-IDENTITIES-20261109` is a materialized sanitized identity record whose digest the editor matched. Its executable identities were rechecked by the researcher. Release names remain owner-held labels; executable-byte hashes are not installer-container hashes. Later analysis copies are byte-identical to their original executables. For 3.04, original packed and UPX-decompressed analysis bytes are separate identities.

- 3.04-fixed-x86 (i386, ELF32): original executable SHA-256 `7901897411ffcee7b72806d5d021d0b42f5670739ad2ed97467fc86bc75690d0`; derived analysis ELF SHA-256 `6e9e35a3ef1320e9705db382ea3184cec07cfce5cac9fb2a550d79fe41931e86`.
- 3.04-obsolete-x86 (i386, ELF32): original executable SHA-256 `7901897411ffcee7b72806d5d021d0b42f5670739ad2ed97467fc86bc75690d0`; derived analysis ELF SHA-256 `6e9e35a3ef1320e9705db382ea3184cec07cfce5cac9fb2a550d79fe41931e86`.
- 4.04r2-x86 (i386, ELF32): original executable SHA-256 `50f2057117cfafd5a1151d6e6fdd1413095fa71445ff274bf923ce7dc04198aa`; analysis ELF has the same hash.
- 4.20r6-x86 (i386, ELF32): original executable SHA-256 `a994afd24f5ebdcf73647ffe8b6752274a6c874058cb0db05c525bab060224d0`; analysis ELF has the same hash.
- 4.20r8-x86 (i386, ELF32): original executable SHA-256 `566cd371464568436265c32976babf2faa95b5fc71cce1f26cbd860b406c2a91`; analysis ELF has the same hash.
- 6.01r1-x86 (i386, ELF32): original executable SHA-256 `9a2cd037cd3de2ed1dcfc6e9665f5d11854862ef521397f593fa7dd8ffd64a3d`; analysis ELF has the same hash.
- 6.01r1-x64 (x86_64, ELF64): original executable SHA-256 `3f4fbb802fe5e99fd235833e45f509257e3930295a96288343f0e6ec08a141c1`; analysis ELF has the same hash.
- 6.03r7-x64 (x86_64, ELF64): original executable SHA-256 `ceeaefeb2df0668c9de921d4b967c511f85b235b25a18563534eb2f09b619c50`; analysis ELF has the same hash.

## Exact payload controls

[bin] Bounded extraction recovers 14 four-segment containers in 4.04r2, 13 in each 4.20 revision, 13 in each 6.01 architecture and 12 in 6.03r7 x64. All 13 inflated payloads match between 4.20r6 and r8; all 13 match between 6.01r1 x86 and x64. The recovered 6.03 corpus is an exact byte subset of 6.01's. The unmatched 6.01 payload has nine declared entries and 247 numeric instructions; scan absence does not prove removal of a client feature.

[bin] Each 4.20 corpus has 119 declared entries and 15,208 numeric instructions. Each 6.01 corpus has 55 and 5,053; 6.03 has 46 and 4,806. All 78 container occurrences have four unique segments numbered 1–4, valid candidate entry/string bounds and exact instruction-byte reconstruction. The maximum observed numeric tag is 189. Five whole payloads also match between 4.04 and 4.20. Roster alignment is only a candidate relationship; it is weaker than whole-payload equality.

## Extractor and interpretation limits

[bin] Neither duplicate 3.04 executable yields an accepted bounded zlib stream. Other compression, external resources and the older format remain outside this negative result. Original ELF bytes are scanned under explicit candidate input/output limits; accepted payloads are decoded and re-encoded with hashes retained. No client/server runs for extraction; cleanup is not applicable.

[bin] Structural equality supplies cross-version controls for E#207. It does not prove native handler equivalence, execution, a complete language, event behavior or complete malformed-input handling.

- [x] ~~Compare accepted payload bytes and validate bounded corpus reconstruction.~~
- [ ] Connect further payloads to live execution and establish native semantic equivalence.

## Evidence provenance

- `LNX-EMBEDDED-CORPUS` — researcher-supplied original private-carrier SHA-256 `187a68d118bfb9e8455f1d59a4d796b0ed9ee88e80e51d5b50c0f45a21248c45`.
- `LNX-EMBEDDED-PAIRS` — researcher-supplied original private-carrier SHA-256 `5af56c42b118192cba728927a58ac57c83a3628881c5d891b4991d5814ea90f6`.
- `LNX-EMBEDDED-ROSTER-CANDIDATES` — researcher-supplied original private-carrier SHA-256 `bf17f7eb8b0c239f50ad24a15101a37457dd3aaa6c95d632ee82a6fa81a244de`.

- `LNX-INPUT-IDENTITIES-20261109` — materialized sanitized identity-record SHA-256 `7ce8a1cf7fb492f7a263b3c02c3cadb2c2ce25b9b2bc6135dff7335481504318`; executable hashes remain researcher-supplied.
