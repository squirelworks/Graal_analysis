# Bound Linux 3.04 startup and successful compiled-script reading

The editor reviewed only the sanitized 2026-11-09 Linux cross-version handoff and matched its supplied SHA-256. Observations and original private-carrier digests are researcher-supplied, not independently re-run or authenticated by the editor. No raw code, capture text, script body or client asset was inspected for publication. Evidence keys below resolve via [the source index](../docs/evidence-index.tsv). They identify actual owner-held carriers; proposed key-based JSON aliases are not materialized records or new Evidence IDs.

Runtime observations use owned isolated Linux guest/process workflows with no server or server commit, no online login/gameplay and ordinary debugger breakpoints. New probes patch neither executable/signature checks nor script input. Bounded termination and owned-group cleanup do not assert that every system process was inspectable; separately identified unreadable kernel workers are outside the owned client/debugger group.

## Exact executable inputs

[bin] Source `LNX-INPUT-IDENTITIES-20261109` is a materialized sanitized identity record whose digest the editor matched. Its executable identities were rechecked by the researcher. Release names remain owner-held labels; executable-byte hashes are not installer-container hashes. Later analysis copies are byte-identical to their original executables. For 3.04, original packed and UPX-decompressed analysis bytes are separate identities.

- 3.04-fixed-x86 (i386, ELF32): original executable SHA-256 `7901897411ffcee7b72806d5d021d0b42f5670739ad2ed97467fc86bc75690d0`; derived analysis ELF SHA-256 `6e9e35a3ef1320e9705db382ea3184cec07cfce5cac9fb2a550d79fe41931e86`.
- 3.04-obsolete-x86 (i386, ELF32): original executable SHA-256 `7901897411ffcee7b72806d5d021d0b42f5670739ad2ed97467fc86bc75690d0`; derived analysis ELF SHA-256 `6e9e35a3ef1320e9705db382ea3184cec07cfce5cac9fb2a550d79fe41931e86`.

## Artifact identity and startup boundary

[bin] The fixed and obsolete 3.04-labelled prepared unpacked trees match across 528 regular files each (including generated launchers), including their executable. They are duplicate package labels, not independent implementations. The original packed executable is a separately identified input.

[cap] The unpacked input reaches platform initialization, then returns false from Graal initialization after its first observed signature check returns false. The second check is not reached. Focused captures support that boundary; an earlier truncated capture is excluded. License-resource presence and graphics fallback do not identify every verification input or establish the failure's cause.

[cap] The unchanged original packed loader first fails when it attempts to use a temporary location beneath the read-only sandbox root. With an owned writable temporary area and read-only display-socket access, it passes both observed checks, returns success from initialization and opens its startup script. Both the artifact and environment differ from the unpacked case; packing is not isolated as the sole cause. The owned inferior is terminated at the declared boundary.

## Successful compiled-script read

[cap] A separate unchanged-original launch reaches the compiled Torque reader for `common/main.cs` and returns true. The boolean is the low return byte; unspecified upper bits in a displayed machine word do not reverse that result. Post-read state contains 474 numeric code words and 39 line pairs, matching the packaged `common/main.cs.dso` structure: version word 33 and 1,903 bytes. The packaged-file hash is retained, but the runtime memory payload was not hashed.

[cap] Termination follows the reader return; the capture is untruncated and owned-group cleanup is verified. This proves a successful read, without proving instruction execution, script completion, an offline game or recovered source. It is Linux evidence and does not resolve the Windows 4.04r2 plug-in question in E#503.

- [x] ~~Locate the tested legacy startup and compiled-reader boundaries.~~
- [ ] Isolate signature-helper inputs and measure subsequent script execution separately.

## Later relocation-aware first-handler checkpoint

[cap] A later bounded probe on the unchanged original packed Linux 3.04 client links successful compiled reading to the same program object entering its executor, fetching its first code word and reaching the corresponding native handler in one thread. The next word index is one. Of 474 input code words, 401 nonrelocation positions match; 73 identifier-relocation positions are explicitly excluded from equality. This is relocation-aware linkage rather than full runtime-array byte identity. The owned inferior was terminated at handler entry. No handler completion, script completion, GUI or gameplay is claimed.

[cap] The retained handoff reports unchanged input hashes, untruncated output, owned cleanup and host verification of 28 transferred artifacts. Three unsuccessful instrumentation attempts remain separate historical records. Server and server commit: none. The earlier reader-only observation keeps its original stopping point and missing runtime-payload hash; this later probe does not retroactively amend it. Windows E503 remains unresolved.

The actual sanitized incremental handoff is registered as `LNX304-FIRST-HANDLER-HANDOFF-20261109`, SHA-256 `48e450392de8790557ca17b72c64332170d36fbb0241ae597784d11cc6625c72`. The publisher matched that document and the existing identity record; the original runtime carrier and its observations remain researcher-supplied. The original packed executable and unpacked static derivative retain their separate identities above. The brief later-entry mention in the [seven-operation contract](../torque/linux-304-seven-operation-contract.md) does not provide these quantified checkpoint details or original-client vector completion.

## Evidence provenance

- `LNX304-IDENTITY` — researcher-supplied original private-carrier SHA-256 `1cc39d0a609b2a7f87dea26f2dd2310328ccc9cdbdd680ce641012acfcb826b6`.
- `LNX304-UNPACKED-INIT` — researcher-supplied original private-carrier SHA-256 `2588e929ad1e5bae6cdf41d1ec4a6b700cdb45c1918ad83f20630264dba732d8`.
- `LNX304-UNPACKED-CHECK` — researcher-supplied original private-carrier SHA-256 `20ced1dbc25566b991665e7373626b24089eb14903bf6c3c101462d8b4117d1b`.
- `LNX304-LOADER-FAIL` — researcher-supplied original private-carrier SHA-256 `eec533bff226a4ff7dda1cc9b070f8bdc0fa6ca4e9b7eec6e7635173fdd585b1`.
- `LNX304-ORIGINAL-INIT` — researcher-supplied original private-carrier SHA-256 `de612402d9c539395446778d0e1a1f5a92e53f476e0455917ae298581cb78915`.
- `LNX304-COMPILED-READ` — researcher-supplied original private-carrier SHA-256 `58c2bf475122294ddf25b4fd6d8d7c8dee0c7eb3f29177ac106193bbae3e25d5`.
- `LNX304-VALIDATION` — researcher-supplied original private-carrier SHA-256 `82fbd40db3ea7f98eb7ea9fc199439ff008a24e4e6e85a1b0e81f939388d637c`.

- `LNX-INPUT-IDENTITIES-20261109` — materialized sanitized identity-record SHA-256 `7ce8a1cf7fb492f7a263b3c02c3cadb2c2ce25b9b2bc6135dff7335481504318`; executable hashes remain researcher-supplied.
