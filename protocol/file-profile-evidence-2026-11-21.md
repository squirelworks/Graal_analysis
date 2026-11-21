# File defaults and receive-case evidence

Date: 2026-11-21. Reconciliation of existing published reads, profile data and
captures; no new binary read or experiment. This separates client receive cases,
server version gates and the provenance of shared defaults. **[bin][srv][cap]**

## The recorded 1.41r1 input

The [catalogue](../client-internals/build-catalogue.md) identifies the canonical
patched 1.41r1 input as generation 3, with token `GNW13110`, rather than generation 2.
Its [profile](../client-internals/version-profiles/141-217.toml) records 45 direct
receive cases: 0–41, 43, 75 and 100. The newer
[build comparison](../client-internals/graal2002-and-140-builds.md) also records the
unchanged direct dispatcher from 1.39 to 1.41. Thus 68 and 69 are absent from this
recorded direct switch. This is an exact-input result, not a claim about every
copy labelled 1.41r1 or a pristine vendor specimen. **[bin]**

That set does not establish the FILE body or absence of file transfer. The
[file-transfer note](file-transfer.md#replies-server--client) distinguishes direct
message 100 from the FILE message 102 carried behind it. An exact-bound read of
the 1.41r1 raw/file subpath remains needed; neither a direct-switch omission nor
the server's pre-2.1 reply branch supplies that receiver contract. **[bin][srv]**

## Shared 2.22 and 2.31 defaults

The [TOML](../version-profiles/2.22-2.31.toml) defines a local shared
`defaults.gen5` block. Both 2.22 and 2.31 use it directly; inferred 2.3 inherits
2.31. This is not literal inheritance from a 2.1 profile. Historical version-gate
comments describe a different evidence dimension. No profile values change in
this reconciliation. **[doc]**

- `file_modtime`: the ≥2.1 reply-layout gate is server evidence; it does not by
  itself establish the exact 2.22 receiver's metadata handling. **[srv]**
- `image_ext_default`: the server stops appending `.gif` at that gate. This does
  not independently recover the native client's default-extension algorithm. **[srv]**
- `large_files`: the recorded 2.22/2.31 direct receive cases include 68 and 69.
  The 32000-byte chunk size and ≥2.14 gate describe the server sender, not a new
  per-client size-limit measurement. **[bin][srv]**

The [per-build profile prose](../version-profiles/2.22-2.31.md#wire-protocol)
already attributes framing, compression thresholds, XOR limits and the send queue
cap to the inspected builds. It also records UDP presence, the `noudp` and
`fixedudpport` keys and default-off behavior in both builds. That does not alone
establish the numeric fixed-port default. The same source separates the
`zlib_fix_npc` server workaround from inferred native bug equivalence. **[bin][srv][inf]**

## Captures remain directional

The [codec evidence](codec-and-framing.md#gen-45-partial-xor) records real 2.22
client-originated raw and zlib frames, including partial compressed groups. It
does not record client-originated bz2. Server-originated bz2 observations and a
profile's combined `compression_src` label must not turn that missing direction
into captured behavior. The client send helper was not newly re-read here. **[cap]**

## Remaining reads

- [ ] Trace the exact 1.41r1 raw/file subpath and FILE body.
- [ ] Establish exact native modtime/default-extension semantics and the numeric
  fixed UDP default before upgrading the remaining profile evidence.
- [ ] Audit the remaining shared-default cells, including the full level-format
  list; this provenance pass does not settle every inherited value.

G264 and G375 remain partial. G374's unmatched outgoing sites and the focus
4.x–6.x receive-limit questions are unchanged.
