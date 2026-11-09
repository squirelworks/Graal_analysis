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

## Evidence lineage

The exact sanitized handoff digest and vector-document digest are registered in `workingpapers/sources.tsv` under `LNX304-SEVEN-OP-HANDOFF` and `LNX304-SEVEN-OP-VECTORS`. They identify owner-held editorial inputs, not invented raw evidence carriers. Exact executable identities are supplied by the sanitized input identity record under `LNX304-SEVEN-OP-IDENTITIES`.
