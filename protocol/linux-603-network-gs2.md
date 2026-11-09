# Observe Linux 6.03 network GS2 execution and continuation

[lab] Exact runtime subject: archive-labelled Linux 6.03r7 x64, executable SHA-256 ceeaefeb2df0668c9de921d4b967c511f85b235b25a18563534eb2f09b619c50. This matches the approved sanitized input identity record; it is distinct from the pinned lab server binary.

Publication prose is derived only from the sanitized owner handoffs listed below. Their file hashes were independently computed during preparation; underlying native observations and original-carrier identities are researcher-supplied. Raw code, native addresses, client assets and private capture payloads are excluded. These source IDs identify handoff documents, not newly materialized raw captures.

[lab][cap] The exact Linux 6.03r7 x64 client accepted independently authored GS2 through a state-aware local proxy. Three probes establish class parsing, weapon instruction dispatch/return, and later continuation after a sleep handler. These are new runtime results for this build only, extending the static [6.x architecture](https://github.com/squirelworks/Graal_analysis/blob/main/protocol/v6x-clients.md) and [GS2 VM notes](https://github.com/squirelworks/Graal_analysis/blob/main/protocol/gs2-client-vm.md).

The class probe delivered a 42-byte body through packet 140. The reader received those exact bytes and returned two instruction records, selectors 20 and 7. No class execution was observed or claimed.

The weapon probe first sent explicit packet 33 registration, then packet 140 with a 42-byte body containing an authored numeric 42 operand. The reader returned two records. The executor's program identity matched that reader object; it entered at instruction 0, reached 20 with next position 1, reached 7 with next position 2, and returned. This sequence occurred twice. The native return register was 3; its meaning remains opaque and it is **not evidence that the script returned 42**. The triggering event and universal invocation count remain unknown.

The sleep probe registered another owned weapon and delivered a 50-byte body with selectors 20, 8, 20, 7 and authored numeric operands 0.15 and 42. It observed two initial entries at position 0 reaching the sleep handler, then a later entry for the same owned program at position 2, followed by 20, 7 and native return 3. This establishes an observed continuation position. It does not establish snapshot representation, complete sleep semantics or exact timer accuracy. The measured interval from the second initial executor return to continuation was about 86 ms, not a verified 150 ms wall-clock delay. Debugger instrumentation affects timing.

[lab] An independent read-only review reassembled recorded server-to-client stream fragments, advanced cipher state over complete preceding frames, and decoded each inserted frame exactly to the authored packet. Raw 100 lengths 85, 87, 94 matched the selected packet 140 packets. Descriptor lengths 39, 41, 40 selected exact body boundaries 41, 43, 42 within the packet 140 payloads: the transmitted length counts descriptor bytes; the native boundary adds the two prefix bytes. Body hashes and reader bytes matched exactly. This independently supports the corrected length contract rather than the earlier absolute-boundary interpretation.

These fixtures came from the proxy, not from an unmodified server's compiler or script-delivery path. After insertion, later upstream frames were deliberately withheld because the server's cipher state had not advanced for the injected frame. Login compatibility, normal compiled GS2 distribution, uninterrupted sessions, graphical UI and a reconstructed client are separate gates. No disk-cache hit, checksum-domain contract or header-only acceptance was tested.

For Appendix E, E202 is narrowed by exact network-to-reader delivery and corrected descriptor framing; cache validation and normal server-produced delivery remain open. E207 gains an exact-build handler/continuation observation; event identity, full suspension/wakeup semantics and other selectors remain open. This does not resolve the Windows-specific E503 question or prove other Linux versions share these runtime results.

Before: static parsing/executor routes were known, but independently authored network delivery had no positive runtime chain. Action: ordinary local authentication followed by one proxy-origin fixture per probe, observed with passive GDB breakpoints and return breakpoints. After: the three bounded chains above were recorded. The original executable file hash was unchanged; ordinary debugger breakpoint instrumentation was used. All captures reported no truncation. Actual owned child processes were audited absent and the unique executable path had no active process; separate process-environment inspection omissions were followed up without assuming those sampled processes were owned. No public service was contacted.

Server: isolated lab GServer source pin 1b0a6e15641aa542168d5fd0878517d15d990adc with recorded lab compatibility changes. Server binary SHA-256 97d891fda061811af625c7b2d28b3d55c83c125b1dc23e97f9d6c973041c3743. This identifies the bootstrap server, not the origin of the authored GS2 body. Private source captures, helper scripts, input hashes, packet bytes, ownership checks and transfer verification remain in owner-held workingpapers. Some inherited helper comments still say reader-only or two instructions; actual frozen hooks, bytes and event sequences define the scope described here.

For the reviewed Linux 6.01 x86/x64 and 6.03 x64 clients, the two-byte field encodes

the descriptor's byte length, excluding the two-byte field itself. The receiver

adds two when computing the following body boundary.

If H is the decoded descriptor length, the descriptor occupies [2, H+2) and the

body begins at H+2 within the handler payload. The earlier instruction to encode

H+2 was incorrect: it would move that boundary two bytes too far. A sender that

already encodes H should retain that value.

This correction comes from an independent arithmetic and substring-argument

audit. It does not establish malformed-input rules, complete transport behavior,

metadata/cipher compatibility or script execution, and it does not generalize

the result to other client builds.

## Evidence lineage

- `LNX-POS-603-NETWORK-POSITIVE-1`: sanitized handoff `linux-603-network-gs2-execution-handoff-20261109.md`, SHA-256 `3d0b03438457d8d2c63180d47408f0abd2370ed9707d970da92a387f7137a900`.
- `LNX-POS-603-NETWORK-POSITIVE-2`: sanitized handoff `linux-packet140-length-erratum-20261109.md`, SHA-256 `bee30f870b25181cc069ae1d5a15b51abd3fd181fffe936eb25ec7f296e8952f`.

- [x] ~~Publish these bounded observations and their exact scope.~~
- [ ] Measure the remaining delivery, parser, event and cache gates separately.
