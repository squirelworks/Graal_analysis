# Bound Linux packaged Torque streams and resource comparisons

The editor reviewed only the sanitized 2026-11-09 Linux cross-version handoff and matched its supplied SHA-256. Observations and original private-carrier digests are researcher-supplied, not independently re-run or authenticated by the editor. No raw code, capture text, script body or client asset was inspected for publication. Evidence keys below resolve via [the source index](../docs/evidence-index.tsv). They identify actual owner-held carriers; proposed key-based JSON aliases are not materialized records or new Evidence IDs.

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

## Preserved compiled streams

[bin] Each duplicate 3.04 label contains the same 39 distinct version-33 compiled streams, totaling 48,310 numeric words and 733 line pairs per label. Parsing follows the recovered reader; independent serialization reconstructs every stream byte-for-byte. Pool bytes, compact words, numeric line pairs and identifier relocations remain separate. Neither line-pair member receives an unproved semantic name.

[bin] Out-of-range identifier-pool selections remain visible in the validation results. The native reader's empty-string fallback is a separate behavior, not a reason to suppress strict corpus diagnostics. No script bodies or raw asset bytes are reproduced.

## Bounded supplied-tree comparison

[bin] The inventory hashes 1,463 regular files across eight prepared canonical trees, including eight generated `run-client.sh` launchers and both duplicate 3.04 labels. This is not a pristine installer file count. The counts are 528/528 for the two 3.04 labels, 133 for 4.04r2, 134 each for 4.20r6/r8, and 2 each for 6.01r1 x86/x64 and 6.03r7 x64. No packaged `.dso` or offset-zero version-33 candidate is found in the six later trees. This excludes neither embedded streams, other containers, downloaded resources nor retained engine/compiler functionality. The three prepared 6.x trees contain the supplied standalone executable plus a generated launcher each; the launcher is not an originally shipped resource. They represent two 6.01r1 architectures and 6.03r7 x64, not three releases.

[bin] All nine supplied localization script resources match by hash across 4.04r2, 4.20r6 and 4.20r8 (all x86). The corresponding older resources differ. These are supplied-tree identities, not authenticated release histories.

[bin] This comparison reads preserved package bytes offline, decodes and reserializes them, then checks source hashes against inventory. It launches no process; server and commit are none, and process cleanup is not applicable. The separate Linux 3.04 live reader observation provides a single reader linkage, without transferring execution coverage to later clients or settling Windows E#503.

- [x] ~~Round-trip the preserved legacy streams and compare the supplied resource trees.~~
- [ ] Trace later embedded/downloaded formats and execution separately.

## Evidence provenance

- `LNX304-COMPILED-READER` — researcher-supplied original private-carrier SHA-256 `cf77c7a48f47f25b4935b10611fc93fd1d44a419864399de6aedff1d9ffadb03`.
- `LNX304-COMPILED-CORPUS` — researcher-supplied original private-carrier SHA-256 `5c513ef546ab318c9155df48f4488aa1a51b6fdfbf1edee52a4b4589c69f42fa`.
- `LNX-TORQUE-RESOURCE-INVENTORY` — researcher-supplied original private-carrier SHA-256 `f23e24adafadea45a0191ad42cc5833d8d49775f5aad3e0c6134fa2da6755719`.
- `LNX-TORQUE-RESOURCE-VALIDATION` — researcher-supplied original private-carrier SHA-256 `7253d1eb9b21a3ce1a41daccf1262bbf7c99476d9995312f35f873fd3674bab7`.
- `LNX-TORQUE-CONTENT-IDENTITIES` — researcher-supplied original private-carrier SHA-256 `e647a5861abad852fa071ad4b95591245813c6194e19c8bcf5db18347543362c`.
- `LNX-TORQUE-LOCALIZATION-COMPARE` — researcher-supplied original private-carrier SHA-256 `91f2d4a7ece031ac0e1cdb5b78c4534c31e24935e93f262c4505c288e13c8c4a`.

- `LNX-INPUT-IDENTITIES-20261109` — materialized sanitized identity-record SHA-256 `7ce8a1cf7fb492f7a263b3c02c3cadb2c2ce25b9b2bc6135dff7335481504318`; executable hashes remain researcher-supplied.
