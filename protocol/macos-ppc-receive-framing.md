# PowerPC receive framing and partial-group advancement

[bin] Focused static review on 2026-11-09 inspected four distinct Mac PowerPC
executables independently, checking decompilation against assembly. This is a
receiver contract, not a live traffic result or a send-path specification.

## Exact input scope

The archive groups and owner-held main-executable identities are:

- Shared v3: `owner-held SHA-256 (not published)`.
- Label 4.04r2: `owner-held SHA-256 (not published)`.
- Label 4.20r6: `owner-held SHA-256 (not published)`.
- Shared v5, including a copy labelled 5.12:
  `owner-held SHA-256 (not published)`.

Matching executable bytes do not authenticate release labels or whole bundles.
The findings below were obtained for each input, rather than transferred from
another platform by analogy.

## Frame boundary and mode

[bin] Each receiver reads a two-byte unsigned big-endian body length, excluding
the prefix, and waits for the whole frame. When the object's configured mode is
zero, the first body byte selects the mode and is removed from the transform
length. A nonzero configured mode applies directly. Mode 1 is raw, 3 follows
the zlib route and 5 the bzip2-linked route; 2, 4 and 6 apply XOR before the
corresponding raw/decompression route.

## Group count and state

[bin] Let n be the body byte count after any selector is removed and before
decompression. Raw mode 2 processes min(ceil(n / 4), 12) groups: an incomplete
last group is transformed and advances state. Modes 4 and 6 process
min(floor(n / 4), 4) groups: an incomplete last group is left unchanged and
does not advance state. The transform limits are respectively 48 and 16 bytes.

[bin] Before each processed group, the state becomes the low 32 bits of its
previous value multiplied by 134775813, plus an additive object word. The
updated state's bytes are applied least-significant first, despite the
big-endian PowerPC target. State persists through group/frame iterations in
the opened receiver; initialization and reset writers were not traced.

[inf] Consequently a five-byte body advances twice in raw mode and once in
either compressed mode. This arithmetic consequence is not a wire capture,
and arbitrary bytes tagged as compressed data are not valid compressed members.

## Correction boundary and remaining work

The earlier blanket partial-group sentence in
[the v3 overview](v3x-clients.md) needs this Mac qualification.
It does not establish a Linux correction. These Mac static results do not
settle the Windows 5.12 capture disagreement in
[Appendix E#2](../manual/app-e-open-questions.md).

- [ ] Observe an unchanged Mac receiver consume one valid original local frame,
  with explicit mode/state and a raw-mode positive control.
- [ ] Trace seed, additive-word provenance, mode negotiation and reset/rekey sites.
- [ ] Establish outgoing behavior independently; receive/send symmetry is unproven.

No packet-specific PLO/PLI semantics, successful login, rendering or v6 behavior
is established here. Decompression workspace policies differ between inputs
and are outside this deliberately shared framing contract; they are in
[the decompression companion](macos-ppc-receive-decompression.md).

## Evidence

The four FRAME-STATIC records below are sanitized researcher-held static
summaries, indexed by public evidence identifiers in
[the evidence registry](../docs/evidence-index.tsv). Exact digests and raw exports remain owner-held.

- `MAC-PPC-V3-FRAME-STATIC-20261109-R1`.

- `MAC-PPC-404-FRAME-STATIC-20261109-R1`.

- `MAC-PPC-420-FRAME-STATIC-20261109-R1`.

- `MAC-PPC-V5-FRAME-STATIC-20261109-R1`.
