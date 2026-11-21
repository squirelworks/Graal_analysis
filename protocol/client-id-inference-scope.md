# Client-id sets: inference limits for 2.14–2.16 and Windows 6.00–6.015

Date: 2026-11-21. This is a reconciliation of published per-build notes and
profile metadata, not a new binary read or lab run. A token association, a
receive-switch read and a client-to-server send set are separate claims.

## 2.14–2.16: retain the send-set hypothesis

`[inf]` The [profile inheritance](../client-internals/version-profiles/141-217.toml)
for 2.14 adds client-to-server id 41 to the inherited 2.1-line set; 2.15 and
2.16 inherit it. No exact 2.14–2.16 executable or complete send-site read is
cited for these rows. Keep the proposed set inferred and incomplete as evidence.
Do not turn documentary feature dates or server version branches into an
observed client send set.

`[bin]` The [send-site survey](../version-profiles/pli-send-sites-141-217.md#result)
establishes the sets of its named inputs, including 2.1 test 2/test 3 and
2.17.1. It has no 2.14–2.16 input. Its completeness finding does not bridge
that gap. The [token catalogue](../client-internals/version-token-catalogue.md#21231-gen-3-to-gen-5)
keeps 2.14, 2.15.0, 2.15.1/2.15.2 and 2.16 as documentary associations,
not exact-build binary or runtime confirmation. A later release sharing a
token or accepting id 41 does not establish these releases' sends.

## Windows 6.00r2/r4: receive reads do not settle outgoing ids

`[bin]` The [Windows per-build receive tables](v5v6-windows-unpacked.md#server--client-ids)
give 93 main-switch ids for each of 6.00r2 and 6.00r4. That is a server-to-client
result, not a count of outgoing ids. The [profile](../version-profiles/5.00-6.03.toml)
marks each proposed outgoing set as `pli_sent_src = "inf"` and
`pli_sent_complete = false`: it borrows the Linux 6.01r1 set, itself described
as the Linux 6.03r7 set without 160. Preserve those direction and platform limits.

`[cap][bin]` The Windows [login observations](v5v6-windows-unpacked.md#tokens)
and [connect-routine recovery](login-tokens-3x-7x.md#reading-the-token-from-a-file)
associate both builds with `G3D26090`. The [earlier lab](v5v6-lab-play.md#600r2-and-600r4-on-real-windows)
records login and selected play observations, not a complete outgoing-id sweep.
Neither token recovery, a visible scene nor the reconstructed lifecycle
boundaries in [6.00r2](../client-internals/engine-600r2.md) and
[6.00r4](../client-internals/engine-600r4.md) settles the full send set.

## Windows 6.007/6.015 and Mac 6.015: separate the identities

`[cap]` The [canonical catalogue](../client-internals/version-token-catalogue.md)
records Windows FileVersion 6.007 and 6.015 sending `G3D3007A` in their
first login frames in the 2026-11-13 lab. The profile's old description of
that association as never captured is superseded. The `6.015` row in
`5.00-6.03.toml` is the Windows protocol-profile label associated with
these two Windows builds; this is not a complete behavioral equivalence claim.

`[inf]` That Windows row still borrows the Linux 6.01r1 receive and send
sets. The capture establishes the token association, not the borrowed sets,
own-property rules or every login field. Retain `inferred = true`, both
packet-set inference tags and the incomplete-send flag. Do not copy the
6.03r7 profile or switch an engine default on this basis.

`[bin][lab]` Mac 6.015 is separately catalogued with `G3D3107A`, from a
selected-slice token read; its [Mac probe](probe-mac-6015-2026-11-19.md)
has its own runtime scope. Neither is the Windows `G3D3007A` profile,
and neither establishes a complete Windows outgoing-id set.

## What remains to measure

- [ ] Establish exact 2.14–2.16 client send sites, or a qualified per-build
  outgoing capture; the present documentary associations cannot supply them.
- [ ] Read or measure each Windows 6.00r2/r4 outgoing set independently of
  the already published receive-switch and login-token evidence.
- [ ] Establish the Windows 6.007/6.015 packet sets independently of the
  captured token association and Linux sibling profiles.

The manual's inference ledger intentionally retains these packet-set rows.
Relabelling their evidence limits completes the reconciliation, not the
underlying client-behavior research.
