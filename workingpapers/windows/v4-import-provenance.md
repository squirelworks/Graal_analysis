# Windows carrier identity and the imported v4.20r8 alias

## What the imported report actually records

[doc] The imported report is titled as a Windows v4.20r8 teardown. Its identity
section gives carrier SHA-256
`71378394469bcf16038ee3b335da786afcdf357fe4e8dd6329a05ba926a5e4bf`
and reports PE file-version resource `4.0.4.2`. Its own naming-mismatch paragraph
says that v4.20r8 came from the supplied folder and executable name, and that no
installer/build manifest or second input reconciled those labels. This caveat
is part of the report, not a new discovery about executed client behavior.

[doc] The report's SHA-256 is
`19a7154a4e66f720af3413f1fbd8aa9b888cfdbd32fe4161a8c19ca6d19da7b7`.
The editor matched the document bytes and reviewed its identity/caveat prose,
without executing the imported Python prototype or opening raw native exports.
This verifies the report identity and what it says. The separate retained-carrier checkpoint below corroborates the input hash and resource fields; neither check authenticates a vendor release.

## Keep the provenance fields separate

- Supplied alias: v4.20r8, from the imported folder/executable naming.
- Reported resource version: `4.0.4.2`, a component metadata value.
- Existing research collection label: Windows 4.04r2 for the retained carrier
  identified by that same digest in the owner's Windows recovery records.
- Official release authentication: unresolved without an independently traced
  package/build provenance chain.

[file] The completed 2026-11-09 Windows checkpoint independently reports that the retained carrier hashes to the same SHA-256 and its PE resource reads FileVersion `4.0.4.2`, ProductVersion `4`, OriginalFilename `Graal.exe` and ProductName `Graal`. This corroborates the exact retained byte identity and the report’s resource claim. It does not authenticate the supplied `4.20r8` alias or collection `4.04r2` label as an official release.

Source `WIN-V4-IDENTITY-CHECKPOINT-20261109` identifies the sanitized checkpoint, SHA-256 `1404c7e44d0fa5d43535b0aea0f6461c1d985a97417bdf218775b98cc3e49efa`. The publisher matched its document digest and reviewed the bounded findings; the underlying carrier/resource check remains researcher-supplied, not a fresh publisher binary scan. No original release manifest or signature provenance was established.

## Packed carrier and recovered components

[doc] The imported report says that native function bodies were not recovered
from its sole supplied carrier. Its Python prototype explicitly omits actual
GS1/GS2, Torque APIs and other engine behavior. Those prototype results are not
an original-client execution oracle.

The [earlier packed-carrier export](../../torque/v4-404r2-exe.md) and the
[later Windows recovery collection](README.md) retain different artifact and
measurement scopes. A label on the original carrier does not relabel a later
reconstructed component, turn a packer export into an engine export, or transfer
another build's runtime behavior.

- [x] ~~Verify the imported document identity and preserve its existing caveat.~~
- [x] ~~Corroborate exact retained carrier hash and reported resource fields.~~ The completed Windows checkpoint supplies that bounded comparison.
- [ ] Resolve package provenance before authenticating a vendor release label.
- [x] ~~Carry the corroborated identity qualification into the build catalogue and evidence index.~~

This is a completed bounded identity/provenance comparison, not an original-client behavior result.
No client, server, debugger or imported script was launched for its preparation.
