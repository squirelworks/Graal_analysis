# Bound Linux 4.20r6 clock updates and advertised 3D-state predicate

The editor reviewed only the sanitized 2026-11-09 Linux cross-version handoff and matched its supplied SHA-256. Observations and original private-carrier digests are researcher-supplied, not independently re-run or authenticated by the editor. No raw code, capture text, script body or client asset was inspected for publication. Evidence keys below resolve via [the source index](../workingpapers/sources.tsv). They identify actual owner-held carriers; proposed key-based JSON aliases are not materialized records or new Evidence IDs.

Runtime observations use owned isolated Linux guest/process workflows with no server or server commit, no online login/gameplay and ordinary debugger breakpoints. New probes patch neither executable/signature checks nor script input. Bounded termination and owned-group cleanup do not assert that every system process was inspectable; separately identified unreadable kernel workers are outside the owned client/debugger group.

[bin] The new selected 4.20r6 native package is researcher-reported host-verified: 316 unique selected C-export entries and 2,929 manifest files, five repaired retained-dossier deliveries and zero unresolved requested facets. This is selected recovery coverage, not complete source/semantics. At the cited handoff revision, five expanded native jobs were pending; their completion is not asserted here.

## Exact executable inputs

[bin] Source `LNX-INPUT-IDENTITIES-20261109` is a materialized sanitized identity record whose digest the editor matched. Its executable identities were rechecked by the researcher. Release names remain owner-held labels; executable-byte hashes are not installer-container hashes. Later analysis copies are byte-identical to their original executables. For 3.04, original packed and UPX-decompressed analysis bytes are separate identities.

- 4.20r6-x86 (i386, ELF32): original executable SHA-256 `a994afd24f5ebdcf73647ffe8b6752274a6c874058cb0db05c525bab060224d0`; analysis ELF has the same hash.

## Six observed updates

[cap] Unchanged 4.20r6 startup reaches the clock updater at entry/return six times with its branch byte zero. The initially zero clock is seeded within the observer's wall-clock interval. Each of the next five stored values equals the binary-double expression previous value plus 0.05. These are per-invocation state changes. Debugger pauses prevent interpreting them as a measured 50 ms frame period, 20 Hz rendering, movement-send rate, walk duration or sleep latency.

## Directly registered predicate

[bin] Raw property registration binds the advertised global read-only boolean `isgraal3d` to a small getter returning the same byte that the clock predicate reads. The byte defaults to zero in a zero-filled ELF section. Bounded direct-address references identify three writer owners; the observed set-to-one branch follows an input-prefix test for `3 `. The property name follows the registration binding rather than an analyst label. Registration/raw bytes support the callable getter entry, without asserting a standalone decompiled getter boundary.

[bin] With the byte zero and the clock nonzero, it adds 0.05 per call; if the clock is zero, or the byte is nonzero, it refreshes from the wall-clock helper. The probe observed one seed and five increments; it does not prove that the clock can never be reset or reseeded. Direct encoded-reference scans do not exclude alias, indirect or module writes. No nonzero live branch, successful 3D connection or rendering is observed; E#301's frame-driver and timed-walk questions remain open.

## Capture and optional bridge boundary

[cap] Ordinary breakpoints record the six updater returns, followed by explicit inferior termination. Mode byte, executable, signatures and script input are unchanged. The capture is untruncated, exits normally, retains canonical/runtime executable equality and verifies owned cleanup. Server and commit are none.

[bin][inf] A separate bounded static record identifies initialization of two callbacks used by guarded adapters. One adapter restores its own frame and jumps directly to a callback while leaving the caller's stack arguments in place. A short decompiler prototype is not an ABI signature. This establishes no module activation, complete callback contract or Windows plug-in reader.

- [x] ~~Observe six updates and identify the advertised property through direct binding.~~
- [ ] Measure frame drivers, movement timing and the live nonzero branch separately.

## Evidence provenance

- `LNX420-R6-CLOCK-CAPTURE` — researcher-supplied original private-carrier SHA-256 `288a046598aafa82b87f54fce832a527119f98ef5c500bfc41ff48d81e1759e0`.
- `LNX420-R6-CLOCK-OBSERVATIONS` — researcher-supplied original private-carrier SHA-256 `b4f6b9fc93501a161ddda0a6b813c9017252d1f214a4f3e7a8c4c1125ec16977`.
- `LNX420-R6-CLOCK-VALIDATION` — researcher-supplied original private-carrier SHA-256 `69f77af01d3d8d3b6fa7a9e60fcbb729589bdaae3980b6a9a102056702d89856`.
- `LNX420-R6-CLOCK-UPDATER` — researcher-supplied original private-carrier SHA-256 `25bb4c471a9fc1786c40b15662a2f0ddba1bdc20b8af39e11ddaaa713d514e02`.
- `LNX420-R6-CLOCK-PREDICATE` — researcher-supplied original private-carrier SHA-256 `2c3108bfcdf8efab593d6506de40ee1820da200343a15d6488d1083fe1c9ce38`.
- `LNX420-R6-MODE-BINDING` — researcher-supplied original private-carrier SHA-256 `285a24427b3918e039f16aec947a6bd02c1ccf83fb62349b7e4da2b8b3afe608`.
- `LNX420-R6-MODE-DEFAULT` — researcher-supplied original private-carrier SHA-256 `5d49152f240e638a1a4b10cfeecfc2804ed3017b8a580ea5e42b3614cdc58e88`.
- `LNX420-R6-MODE-WRITERS` — researcher-supplied original private-carrier SHA-256 `71cd4885af4a6cff8f571be0ad1396739942e4b6e2cac90db9e146f24356e608`.
- `LNX420-R6-MODE-CONDITION` — researcher-supplied original private-carrier SHA-256 `9ce1adecb3cbc8268088979209be17b7ede0ccdd0b8b67fc33fdecb7f1787ebe`.
- `LNX420-R6-BRIDGE-REGISTRATION` — researcher-supplied original private-carrier SHA-256 `b3f9577e26cc27caf6c89eb145e0373a4fc1b7bd1ab9e7b40351e972b5683eb2`.
- `LNX420-R6-BRIDGE-ADAPTER` — researcher-supplied original private-carrier SHA-256 `44ade8cd9c47f9bbbcaf77c7c9a8d05e04ebe458dc96ec61ef5374b2a3f46322`.
- `LNX420-R6-BRIDGE-INITIALIZER` — researcher-supplied original private-carrier SHA-256 `1082f48ba6ca4bbfe6e8354bb682f535466e5e4a75b3e8cf2a6fa68e2b55c87f`.
- `LNX420-R6-NATIVE-BUNDLE` — researcher-supplied original private-carrier SHA-256 `6c3c5ee9e6af833de92a35f8587f2b05225a73915c5fe770b2c2e0334eac0737`.
- `LNX420-R6-NATIVE-VERIFICATION` — researcher-supplied original private-carrier SHA-256 `cbe17bddafcca4999b35d9813b105133e96cb9dbdf3512b35daa9420765d1f0c`.
- `LNX420-R6-NATIVE-VALIDATION` — researcher-supplied original private-carrier SHA-256 `47c6c4025b054ff9fbbe5449ee155c0b4ab6f3d427d87d12fd81548bfd2d347a`.
- `LNX420-R6-NATIVE-RECOVERY` — researcher-supplied original private-carrier SHA-256 `e97acd04552728f6b1cf9a38f67da78bec800f7793c86476fe98bbe512743804`.

- `LNX-INPUT-IDENTITIES-20261109` — materialized sanitized identity-record SHA-256 `7ce8a1cf7fb492f7a263b3c02c3cadb2c2ce25b9b2bc6135dff7335481504318`; executable hashes remain researcher-supplied.
