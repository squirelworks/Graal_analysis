# Four stored GS1 signatures in Windows 2.05 rev 2

## Scope and provenance

`[bin]` The exact Windows x86 executable is identified by researcher-supplied MD5 `f3fdf54d943fa91c89acba5bb695db99` and SHA-256 `b0e39a04ca0891d0f02282a113a1cd80ddf7a1880a786c5831f26a452e8cbb08`. These findings apply to this 2.05 rev 2 input only.

The editor reviewed the sanitized handoff for evidence ID `GRAAL-E201-20261109-01`, registered in [the evidence index](../docs/evidence-index.tsv). Artifact and private-record hashes and static observations are researcher-supplied; the editor did not inspect the executable or underlying raw proof.

## Stored letters

`[bin]` The bounded static record search found one matching record for each command, with a reference to its terminated signature. The stored argument-letter sequences are:

| Command | Stored signature |
| --- | --- |
| `toinventory` | `S` |
| `puthorse` | `MRR` |
| `showimg` | `RMRR` |
| `replaceani` | `MM` |

`[bin]` These agree with the literal-letter entries in [the earlier GS1 reference](gs1-reference-205.md#commands-161-205). The alternative letters formerly printed in [the command reference](gs1-command-reference-205.md#commands) do not describe these four stored sequences and are corrected there.

## Checks and limits

`[bin]` The researcher extracted the original ZIP, hashed the executable, checked command-name references against the static record layout, and checked the referenced signatures and their terminators. No runtime code was executed.

- [x] ~~Resolve which literal letters the four records store.~~ The table above records the bounded static result.
- [ ] Determine whether differing argument descriptions in the older notes express equivalent runtime behavior.
- [ ] Check argument conversion and coercion at runtime.

The correction changes literal signatures only. Existing independently supported command descriptions remain in place; it does not settle string-expression parsing, conversion rules or equivalent naming conventions. Appendix E#201 retains those semantic questions.
