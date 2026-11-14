# Classic+ 1.13 login-construction boundary

Date: 2026-11-15. Static observations from one selected iOS Classic+ 1.13 input; evidence `IOS-CLASSIC-LOGIN-STATIC-20261115-02` ([index](../docs/evidence-index.tsv)). No app, device, VM or server session was run for this study. **[bin]**

## Scope and prior work

The [earlier token study](iphone-version-tokens.md#the-binaries-bin) already identifies `G3D0208A` in Classic+ 1.13. This pass follows a selected constructor and one directly relevant forwarding helper using stock Ghidra's ARMv6 Mach-O support. The constructor entry was analyst-seeded from a candidate register-save sequence; its reconstructed body and static pseudocode do not authenticate an original source-function boundary or establish complete teardown coverage. **[bin]**

Eight append-call arguments resolve the same `G3D0208A` token through the original segment mappings. This corroborates the prior reading; it does not establish a desktop-compatible mobile profile or a captured login frame. **[bin]**

## Caller observations

After the token buffer, the selected caller combines two string-related values. For each selected branch, a comparison uses threshold 223. The short branch derives a prefix-helper argument from length plus 32; the longer branch supplies an all-bits-set prefix argument and passes 223 to a copy helper. Empty/null cases are present separately. These are caller arguments: helper bodies were not independently validated here, so exact emitted bytes, accepted field limits, truncation and multibyte behavior remain unknown. **[bin]**

The first value comes through a getter and is stored on the connection object; a second getter supplies the other value. Their semantic identities are unresolved. Neither is identified here as an account, password or device name. **[bin]**

A vector-related construction invokes a helper with index arguments 0 through 3 and appends a serializer-helper result after the two string-related values. Element meanings, delimiters, encoding and whether this supplies a complete identity trailer remain unknown. **[bin]**

## Forwarding boundary

The selected result is passed to the forwarding helper with selector 5. That path bypasses two special cases and chooses between two lower send paths using a global flag. The lower senders were not validated here. Selector 5 is not established as an on-wire client type, packet opcode, cipher generation, PLI 5 or PLAYERPROPS selector. The constructor trigger and receiver property mapping were not established. **[bin]**

## Use and remaining questions

The token remains a build-catalogue fact. The caller observations identify bounded helper/getter questions; they do not yet define an implementable mobile-login frame or a native accepted-frame fixture. A desktop capture or synthetic mobile-shaped fixture does not supply the missing iOS evidence. The prior note's PLI 161 description is a server-source lead, not an observed iOS packet layout. **[bin][doc]**

- [x] ~~Corroborate the already published token in the selected constructor and record the caller/forwarding boundary.~~ Static result above; no runtime acceptance claim.
- [ ] Independently validate the prefix and copy helpers before describing emitted bytes, limits or truncation.
- [ ] Establish the getter identities and vector-serializer format before naming fields or an identity trailer.
- [ ] Follow the selected lower sender and constructor trigger before assigning wire framing, a client type or cipher semantics.
- [ ] Establish the exact-input receive-property mapping and native acceptance separately; neither follows from the token or caller selector.
