# Windows carrier identity and the imported v4.20r8 alias

## What the imported report actually records

[doc] The imported report is titled as a Windows v4.20r8 teardown. Its identity
section records a carrier digest and PE file-version resource `4.0.4.2`. Its own
naming-mismatch paragraph says that v4.20r8 came from supplied naming and that no
installer/build manifest or second input reconciled those labels. This caveat
is part of the report, not a new discovery about executed client behavior.

[doc] The editor checked the report's document identity in owner-held records
and reviewed its identity/caveat prose, without executing the imported Python
prototype or opening raw native exports. The separate retained-carrier checkpoint
is researcher-supplied and reports matching identity/resource fields; these
checks do not authenticate a vendor release.

## Keep the provenance fields separate

- Supplied alias: v4.20r8, from the imported folder/executable naming.
- Reported resource version: `4.0.4.2`, a component metadata value.
- Existing research collection label: Windows 4.04r2 for the retained carrier
  identified by the same owner-held digest.
- Official release authentication: unresolved without an independently traced
  package/build provenance chain.

[file] A completed 2026-11-09 Windows checkpoint reports that the retained carrier has the same identity and PE resource values `4.0.4.2`, `4` and `Graal`. This corroborates the report's bounded resource claim but remains researcher-supplied, not a fresh publisher binary scan. No original release manifest or signature provenance was established. The exact checkpoint identifier and digest remain owner-held.

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
