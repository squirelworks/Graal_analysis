# Windows 2.22-labelled verifier variants

Date: 2026-11-14. Scope: a static comparison of two retained Windows inputs
reporting version 2.2.2.0, with a separately retained community-distributed
control. The version resource is an observation, not authentication of an
official release. No client was executed for this comparison. **[bin]**

## Evidence and method

Owner-held evidence IDs `WIN222-VERIFIER-A`, `WIN222-VERIFIER-B` and
`WIN222-VERIFIER-CONTROL` are registered in
[`docs/evidence-index.tsv`](../docs/evidence-index.tsv). Private identity
records distinguish the inputs; this note does not distribute them.

The two compared inputs are both 1,991,680 bytes and identify as x86 PE
applications. Their version resources report 2.2.2.0. A complete file-byte
comparison finds four differing bytes, each in the code section. **[bin]**

Ghidra 12.1.4 was used to resolve the affected code in input A. All four
sites belong to one analyzed routine. Its decoded branches and referenced
error messages identify RSA verification and a PKCS1 scheme. The original
files were not modified. **[bin]**

Input B was not separately imported into the deep provider. Its comparison
is based on the complete byte difference against A and the decoded
instruction contexts in A. This distinction matters: the result below is
a static interpretation of those edits, not an independently analyzed
whole-program control-flow result for B. **[bin][inf]**

## What the four edits change

Each edit replaces a conditional branch with an unconditional branch to
the same destination, preserving its displacement. The destinations skip
the associated error paths. The four contexts in A are: **[bin]**

- A minimum RSA key-size guard, with an error referring to the PKCS1 scheme.
- A supplied signature-size guard against the length derived from the key.
- A success/failure guard after a helper in the verification path.
- A final comparison-result guard before error reporting.

The third helper's complete algorithm was not established. The observation
is that its result controls an error path in A and that B removes that
condition. It does not establish cryptographic correctness, acceptance of
any particular signature, or whether a startup caller reaches this routine
in either input. **[bin][inf]**

## Relationship to the earlier signature note

[`arrays-and-signatures.md`](arrays-and-signatures.md#the-graal-reborn-222-exe-has-the-check-disabled)
already reports three conditional-to-unconditional edits in the
community-distributed control. That finding is prior research; the new
observation here is the four-site difference between A and B. These are
different comparisons and must not be treated as competing counts for the
same patch. The control is not authenticated as pristine official code.

Relative to the separately identified control, A differs at 34 bytes in
eight contiguous ranges and B at 30 bytes in four ranges. Those broader
differences have not all been interpreted. The matching file sizes do not
establish a packed/unpacked relationship or a release lineage. **[bin][inf]**

## Coverage and remaining questions

- [x] ~~Establish the bounded A-to-B code difference and its routine context.~~
  Four branch conditions in one RSA-verification routine, as described above.
- [ ] Interpret the remaining control-to-variant differences without assuming
  the control is an official baseline.
- [ ] Trace callers and their error propagation before making any claim about
  startup behavior or accepted inputs.
- [ ] Establish the verification helper's algorithm and signature format;
  this comparison does not resolve the earlier note's key-encoding question.

No protocol, PM-list behavior, GS1 execution or runtime acceptance was
measured. These inputs therefore provide no new evidence for official 2.x
cross-server PM support or for another client's behavior.
