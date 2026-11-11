# Seven-operation contract in the Linux 3.04 Torque executor

## Exact input and evidence boundary

[bin] This is an offline static contract for the archive-labelled Linux 3.04 fixed x86 analysis executable, SHA-256 `6e9e35a3ef1320e9705db382ea3184cec07cfce5cac9fb2a550d79fe41931e86`. That analysis ELF is an unpacked derivative of the original packed executable, SHA-256 `7901897411ffcee7b72806d5d021d0b42f5670739ad2ed97467fc86bc75690d0`. The two hashes identify different artifacts. This note does not transfer the static contract to another platform or authenticate a release label beyond the owner collection.

[bin] The source is the sanitized owner consultation listed under Evidence lineage. Its private native review covers seven selected operations. The editor can match that document's digest; the underlying native observations remain researcher-supplied. No raw native text, addresses, original script or asset bytes are published here.

## Operations and their limits

[bin] Immediate load, selector 65, consumes its following operand word and pushes that word's exact 32-bit payload. Discard, selector 64, consumes one integer stack entry. Preserving the immediate's bits is separate from interpreting those bits when formatting a number.

[bin] Conditional selectors 7 and 9 consume their condition. Selector 7 takes its branch when the condition is zero; selector 9 takes its branch for any nonzero payload. A taken branch sets the next position to an absolute index in the code-word array. That target is neither a relative distance nor a byte position. Selector 12 is an unconditional absolute jump and does not consume an integer stack entry.

[bin] Integer-to-string selector 63 formats the 32-bit payload as a signed decimal value, then consumes it. Consequently the payloads 2147483648 and 4294967295 format as `-2147483648` and `-1`, respectively. Loading those values need not change the stored bit pattern.

[bin] Return, selector 13, exits through cleanup and returns the current string position. It does not implicitly convert or pop an integer. Explicit conversion followed by return is supported by this path. Plain return does not establish an initially empty string, a fresh invocation state or ownership of the returned storage.

## Independently authored expectations

[inf] The adjacent [conformance vectors](linux-304-seven-operation-vectors.json) contain seven independently authored word sequences. Three distinguish signed formatting, one tests discarding exactly one entry, two exercise taken conditional branches and condition consumption, and one exercises an unconditional absolute jump. These are static-derived acceptance expectations, not recordings of original-client execution. They are not native failure-handling or malformed-input specifications.

[bin] At the separately identified [reproduction snapshot](https://github.com/squirelworks/graal-client-repro/tree/25a3a19668ae112eef73a10ba1d0df2972e997b5/common/torque/console/vm), the inspected branch/stack behavior agreed with this subset, while unsigned integer formatting disagreed for high-bit-set payloads. This comparison concerns that snapshot; it does not assert the present implementation still has the mismatch. Its validation, execution budgets, errors, initial state and instruction-count conventions are implementation policies, not demonstrated original-client behavior.

## Relationship to earlier Linux work

[cap] The earlier [startup and reader note](../client-internals/linux-304-startup-reader.md) established a successful original-client compiled read. A later bounded observation links reading to first-handler entry, but does not supply completion results for these seven test sequences. Neither observation is an oracle for a whole Torque VM. The [packaged-stream round trips](../formats/linux-torque-resource-scope.md) establish serialization identity, not semantic equivalence of execution.

[bin] Before this consultation, formatting, stack consumption and return details in the implementation slice were provisional. The researcher inspected retained native evidence offline and reported the bounded contract above. No client, debugger or server was launched to prepare this publication. Server and server commit: none. This work does not settle Windows-specific Appendix E#503.

- [x] ~~Record the selected static operation contract and independent vectors.~~
- [ ] Execute independently authored vectors on the exact original input with qualified result observations.
- [ ] Determine invocation state, string lifetime and exceptional-input behavior separately.

## Native-call evidence beyond the seven operations

[bin] The separately retained static execution-chain review identifies function/namespace lookup, an object-call branch, recursive executor entry for script-defined functions, and dispatch through registered native callbacks with argument-count checks. It also reports a path that rewrites a resolved-call word or operand into a cached form. These are selected static paths in the exact analysis input identified above, not observed native callback invocations. Several namespace/registry helpers lie outside that selected export, so their internal policies remain unresolved.

[doc] The existing [registrar argument-count study](engine-304.md#argument-counts) supplies inclusive counts: the command name counts, methods also count the object as the second value, and maximum zero means no upper bound. Those published facts are not rediscovered here. They specify logical argument accounting, not the memory representation, allocation, lifetime or native calling convention of a callback's argument array. Maximum zero is not evidence of a C variadic calling convention. The older registrar note does not itself provide a full input digest; shared version labels alone do not independently authenticate its linkage to this review's exact bytes.

[inf] The seven-operation return result above belongs to the script executor. Returning the current string position does not establish a registered native callback's result type, conversion, storage ownership or lifetime. This review does not supply a complete argument/result adapter or a native builtin execution oracle.

[bin] Exact case handling, namespace inheritance/package precedence, duplicate registration, argument coercions, arity-failure behavior and cached-call invalidation remain unqualified by these selected paths. No retained behavioral contract for the builtin echo is established here. Implementations may choose explicit API policies for those unknowns, but passing policy tests is not evidence of original-client fidelity. Later Graal-variable or event-name rules must not be transferred into this older console registry.

The added source key `LNX304-NATIVE-CALL-REVIEW-DOC` identifies the actual retained review document in [the source index](../docs/evidence-index.tsv). Its document digest is checked during publication preparation; the underlying native findings remain researcher-supplied. No decompiled function or assembly was newly inspected, and no client, debugger, provider or build was started for this document review. The earlier first-handler observation is not a native-call argument/result oracle.

- [x] ~~Separate the selected static native-call paths from complete argument/result fidelity.~~
- [ ] Obtain a separately qualified retained contract before asserting callback representation/results, registry policy or builtin behavior.

## Evidence lineage

The exact sanitized handoff digest and vector-document digest are registered in `docs/evidence-index.tsv` under `LNX304-SEVEN-OP-HANDOFF` and `LNX304-SEVEN-OP-VECTORS`. They identify owner-held editorial inputs, not invented raw evidence carriers. Exact executable identities are supplied by the sanitized input identity record under `LNX304-SEVEN-OP-IDENTITIES`.
