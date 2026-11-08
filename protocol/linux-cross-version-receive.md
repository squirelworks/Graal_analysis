# Compare Linux receive cases and the 4.20r6 compiled-input chain

The editor reviewed only the sanitized 2026-11-09 Linux cross-version handoff and matched its supplied SHA-256. Observations and original private-carrier digests are researcher-supplied, not independently re-run or authenticated by the editor. No raw code, capture text, script body or client asset was inspected for publication. Evidence keys below resolve via [the source index](../workingpapers/sources.tsv). They identify actual owner-held carriers; proposed key-based JSON aliases are not materialized records or new Evidence IDs.

Runtime observations use owned isolated Linux guest/process workflows with no server or server commit, no online login/gameplay and ordinary debugger breakpoints. New probes patch neither executable/signature checks nor script input. Bounded termination and owned-group cleanup do not assert that every system process was inspectable; separately identified unreadable kernel workers are outside the owned client/debugger group.

[bin] The new selected 4.20r6 native package is researcher-reported host-verified: 316 unique selected C-export entries and 2,929 manifest files, five repaired retained-dossier deliveries and zero unresolved requested facets. This is selected recovery coverage, not complete source/semantics. At the cited handoff revision, five expanded native jobs were pending; their completion is not asserted here.

## Exact executable inputs

[bin] Source `LNX-INPUT-IDENTITIES-20261109` is a materialized sanitized identity record whose digest the editor matched. Its executable identities were rechecked by the researcher. Release names remain owner-held labels; executable-byte hashes are not installer-container hashes. Later analysis copies are byte-identical to their original executables. For 3.04, original packed and UPX-decompressed analysis bytes are separate identities.

- 4.20r6-x86 (i386, ELF32): original executable SHA-256 `a994afd24f5ebdcf73647ffe8b6752274a6c874058cb0db05c525bab060224d0`; analysis ELF has the same hash.
- 4.20r8-x86 (i386, ELF32): original executable SHA-256 `566cd371464568436265c32976babf2faa95b5fc71cce1f26cbd860b406c2a91`; analysis ELF has the same hash.
- 6.01r1-x86 (i386, ELF32): original executable SHA-256 `9a2cd037cd3de2ed1dcfc6e9665f5d11854862ef521397f593fa7dd8ffd64a3d`; analysis ELF has the same hash.
- 6.01r1-x64 (x86_64, ELF64): original executable SHA-256 `3f4fbb802fe5e99fd235833e45f509257e3930295a96288343f0e6ec08a141c1`; analysis ELF has the same hash.
- 6.03r7-x64 (x86_64, ELF64): original executable SHA-256 `ceeaefeb2df0668c9de921d4b967c511f85b235b25a18563534eb2f09b619c50`; analysis ELF has the same hash.

## Numbering and exact receive paths

[bin] The inspected packet splitters zero-extend the packet tag, subtract 32 and pass that argument to a virtual receive entry. The client receiver handles two special arguments separately, then chooses immediate dispatch or mutex/queue machinery. The queue branch is not a separately established protocol switch. Immediate tables index the argument without another adjustment.

[bin] Both 4.20 revisions have distinct paths for arguments 131 and 193; 140 takes fallback and 197 lies outside the guard. In both 6.01r1 architectures and 6.03r7 x64, 131, 140 and 197 have distinct handlers while 193 takes fallback. These exact-path results do not prove universal retirement across modes/server generations. The 140/197 field grammar and cache behavior remain acquisition leads.

## Completed 4.20r6 native chain

[bin] Case 131 checks for three payload bytes, calls an unreviewed helper and rechecks length. It derives a positive identifier using three unsigned byte getters, removes the three-byte prefix, chooses lookup sources around the 1000 boundary and passes the remainder to an associated context/program loader and segment reader. This does not separately prove canonical validation of all seven-bit groups. The lookup sources' gameplay types remain inferred.

[bin] A nonempty remainder also reaches an indirect object callback; neither its event name nor complete signature follows from that call. The reader parses compiled segments/numeric records. This is a static compiled-input path, not an identified source compiler. The unreviewed helper is not identified as decryption/decompression. Loader mask binding and linked-program aggregation do not settle joined-class or cancellation semantics.

[bin] Native bodies, exact arithmetic and raw corroboration were reviewed offline. No wire fixture, cache hit/miss, server session or script completion was observed. Server and commit are none; process cleanup is not applicable. E#202 stays partial for body/descriptor/cache relationships across server versions.

- [x] ~~Follow normalized receive numbering and the r6 case-131 compiled-input chain.~~
- [ ] Capture delivery envelopes, descriptors, cache outcomes and callback behavior.

## Evidence provenance

- `LNX420-R6-PACKET-PATHS` — researcher-supplied original private-carrier SHA-256 `5f266b4f41ad69464b38fcbb4cbb2be27a011716c330b4d8b622f36d46935cc3`.
- `LNX420-R8-PACKET-PATHS` — researcher-supplied original private-carrier SHA-256 `22a86ea02140174b73338e80b8fce236b16e2d3a88fd9f5c66e9240d83128501`.
- `LNX601-X86-PACKET-PATHS` — researcher-supplied original private-carrier SHA-256 `9ee7c162b42f84eed2999614f05ce6d4eeff7136701e8b2a06c78253057f93eb`.
- `LNX601-X64-PACKET-PATHS` — researcher-supplied original private-carrier SHA-256 `b147f3fce78898fd440bcb116284cd30c602f645668939276b39190b0210fce2`.
- `LNX603-X64-PACKET-PATHS` — researcher-supplied original private-carrier SHA-256 `e5136c5ddf2f6e931bd124b122c9ea744412a5aa0977271fefcc55985413b1e1`.
- `LNX420-R6-RECEIVE131` — researcher-supplied original private-carrier SHA-256 `80e8402039ae725663801487f9eb36abe1c9330114bf5c9800b3b9356280f306`.
- `LNX420-R6-SCRIPT-ASSOCIATION` — researcher-supplied original private-carrier SHA-256 `30aebd746468370cfa1f38b07f58e8c9325ed8999bc4b720f591d03a08371426`.
- `LNX420-R6-PROGRAM-LOAD` — researcher-supplied original private-carrier SHA-256 `928a5cef2c02749faa81a8175b57042da3a9b084614b33ce4d0cb44d77e7969c`.
- `LNX420-R6-SEGMENT-READER` — researcher-supplied original private-carrier SHA-256 `9746a62d22632ddd16a594eebcf2c2be826345bf15e25c6d5d5f36d985220b61`.
- `LNX420-R6-PACKET-NUMBERING` — researcher-supplied original private-carrier SHA-256 `6552147c77cd657c487c48ea8e640c0d1a4faf54fad4991617b45ca767b2d221`.
- `LNX420-R8-PACKET-NUMBERING` — researcher-supplied original private-carrier SHA-256 `182ba87231d65a29cafd6faf9f1e352b3d4afc7bdedcda217d142fa0541ea897`.
- `LNX601-X86-PACKET-NUMBERING` — researcher-supplied original private-carrier SHA-256 `24a9d4e6a44ed403c85a8bf3939e6e4a91beab6485541fc05ffed2a366bab7ef`.
- `LNX601-X64-PACKET-NUMBERING` — researcher-supplied original private-carrier SHA-256 `1895247dc9d885427d3ea99cfd31439be3085c6eaefdf35afecf10c5af4581af`.
- `LNX603-X64-PACKET-NUMBERING` — researcher-supplied original private-carrier SHA-256 `c80927c73d15416cc05373dae498e6770dd6ccac8f046d22f8942cd43c1bb720`.
- `LNX420-R6-NATIVE-BUNDLE` — researcher-supplied original private-carrier SHA-256 `6c3c5ee9e6af833de92a35f8587f2b05225a73915c5fe770b2c2e0334eac0737`.
- `LNX420-R6-NATIVE-VERIFICATION` — researcher-supplied original private-carrier SHA-256 `cbe17bddafcca4999b35d9813b105133e96cb9dbdf3512b35daa9420765d1f0c`.
- `LNX420-R6-NATIVE-VALIDATION` — researcher-supplied original private-carrier SHA-256 `47c6c4025b054ff9fbbe5449ee155c0b4ab6f3d427d87d12fd81548bfd2d347a`.
- `LNX420-R6-NATIVE-RECOVERY` — researcher-supplied original private-carrier SHA-256 `e97acd04552728f6b1cf9a38f67da78bec800f7793c86476fe98bbe512743804`.

- `LNX-INPUT-IDENTITIES-20261109` — materialized sanitized identity-record SHA-256 `7ce8a1cf7fb492f7a263b3c02c3cadb2c2ce25b9b2bc6135dff7335481504318`; executable hashes remain researcher-supplied.
