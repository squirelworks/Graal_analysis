# Classic+ 1.13 login-construction boundary

Date: 2026-11-15. Static observations from one selected iOS Classic+ 1.13 input; caller evidence `IOS-CLASSIC-LOGIN-STATIC-20261115-02` and prefix/copy follow-up `IOS-CLASSIC-PREFIX-STATIC-20261115-03` ([index](../docs/evidence-index.tsv)). No app, device, VM or server session was run for these studies. **[bin]**

## Scope and prior work

The [earlier token study](iphone-version-tokens.md#the-binaries-bin) already identifies `G3D0208A` in Classic+ 1.13. This pass follows a selected constructor and one directly relevant forwarding helper using stock Ghidra's ARMv6 Mach-O support. The constructor entry was analyst-seeded from a candidate register-save sequence; its reconstructed body and static pseudocode do not authenticate an original source-function boundary or establish complete teardown coverage. **[bin]**

Eight append-call arguments resolve the same `G3D0208A` token through the original segment mappings. This corroborates the prior reading; it does not establish a desktop-compatible mobile profile or a captured login frame. **[bin]**

## Caller observations

After the token buffer, the selected caller combines two string-related values. For each selected branch, a comparison uses threshold 223. The short branch derives a prefix-helper argument from length plus 32; the longer branch supplies an all-bits-set prefix argument and passes 223 to a copy helper. Empty/null cases are present separately. The initial caller pass did not independently validate the helper bodies; the follow-up below narrows the prefix/copy behavior while leaving the short-path object append and complete field codec unresolved. **[bin]**

The first value comes through a getter and is stored on the connection object; a second getter supplies the other value. Their semantic identities are unresolved. Neither is identified here as an account, password or device name. **[bin]**

A vector-related construction invokes a helper with index arguments 0 through 3 and appends a serializer-helper result after the two string-related values. Element meanings, delimiters, encoding and whether this supplies a complete identity trailer remain unknown. **[bin]**

## Prefix and copy helper follow-up

Two selected direct-call targets were inspected in a later static pass using the existing stock Ghidra ARMv6 project. Their entries were analyst-seeded; successful reconstruction of these bodies does not authenticate source-function boundaries or whole-program coverage. This is a separate helper follow-up, not a new token discovery or native experiment. **[bin]**

The prefix helper stores its argument's low eight bits in a temporary byte and passes that byte's address to the inspected copy helper with count 1, then returns the destination. On the ordinary positive-count append path it therefore appends one byte. The caller's all-bits-set argument supplies byte 255; the argument derived from length plus 32 supplies its low byte. These are constructed buffer bytes, not an observed network frame. **[bin]**

The copy helper returns without appending for a null source, zero count or negative signed count. Its positive-count path copies the requested byte count at the destination's previous end, writes a trailing NUL and updates stored length. A shared-storage branch copies the storage before resizing/appending. These are static control/data-flow observations; allocation failure and runtime behavior were not executed or broadly validated. **[bin]**

The selected caller's long-path argument 223 is thus a byte-copy count for this helper. It is not proof of a server-accepted maximum field size or a complete string codec. The short-path object-to-object append helper remains unread, so complete short-field bytes and multibyte/character behavior remain unresolved. **[bin]**

## Forwarding boundary

The selected result is passed to the forwarding helper with selector 5. That path bypasses two special cases and chooses between two lower send paths using a global flag. The lower senders were not validated here. Selector 5 is not established as an on-wire client type, packet opcode, cipher generation, PLI 5 or PLAYERPROPS selector. The constructor trigger and receiver property mapping were not established. **[bin]**

## Use and remaining questions

The token remains a build-catalogue fact. The caller observations identify bounded helper/getter questions; they do not yet define an implementable mobile-login frame or a native accepted-frame fixture. A desktop capture or synthetic mobile-shaped fixture does not supply the missing iOS evidence. The prior note's PLI 161 description is a server-source lead, not an observed iOS packet layout. **[bin][doc]**

- [x] ~~Corroborate the already published token in the selected constructor and record the caller/forwarding boundary.~~ Static result above; no runtime acceptance claim.
- [x] ~~Independently inspect the selected prefix and direct copy helpers.~~ One-byte prefix and selected positive byte-count append are established statically; no runtime acceptance claim.
- [ ] Inspect the short-path object append and remaining field-codec cases before describing complete bytes, character semantics or accepted limits.
- [ ] Establish the getter identities and vector-serializer format before naming fields or an identity trailer.
- [ ] Follow the selected lower sender and constructor trigger before assigning wire framing, a client type or cipher semantics.
- [ ] Establish the exact-input receive-property mapping and native acceptance separately; neither follows from the token or caller selector.
