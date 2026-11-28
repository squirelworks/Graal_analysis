# Exact-input movement geometry in 1st Graal

## Input and evidence boundary

The Windows x86 input is 654,336 bytes, with researcher-supplied SHA-256 `03d8121711f41ac7b5a6e3fe549145d8fdfd44d22040f6706329ae83c6a1a37b` and MD5 `07452f8941fdfcdce878b035156e701c`. Evidence ID `GRAAL-FIRST-MOVEMENT-20261109-01` is registered in [the evidence index](../docs/evidence-index.tsv). Its retained-record digest and all binary observations are researcher-supplied. The editor reviewed only the sanitized prose handoff; original instructions, executable and tables were not inspected.

## Coordinates and candidate step

`[bin]` Facing order is up, left, down, right. The candidate displacements are (0, −0.5), (−0.5, 0), (0, +0.5), (+0.5, 0). Separate little-endian doubles hold world X/Y. Board lookup uses integer coordinate parts on a 64×64 grid, supporting tile units rather than screen-pixel displacements.

`[bin]` Coordinate setters also update the camera. For the ordinary 640-pixel-wide viewport, the horizontal expression is x + 1.5 − 20 and the vertical expression is y + 2 − 14, clamped to the board. The restart/new-game path sets (24.5, 30) through those setters; the second local player adds 12 to X. Scrolling can keep the player near screen center while world position changes.

## Ordered probes

`[bin]` These offsets are measured from the already-stepped candidate position. The point test returns true for blocked. Each row lists probes 0 through 5 in order.

| Facing | Offsets |
| --- | --- |
| Up | (0.6, 1.05), (1.4, 1.05), (1.6, 1.05), (2.4, 1.05), (2.525, 1.05), (0.475, 1.05) |
| Left | (0.55, 1.1), (0.55, 1.9), (0.55, 2.1), (0.55, 2.9), (0.55, 3.025), (0.55, 0.975) |
| Down | (0.6, 2.95), (1.4, 2.95), (1.6, 2.95), (2.4, 2.95), (2.525, 2.95), (0.475, 2.95) |
| Right | (2.45, 1.1), (2.45, 1.9), (2.45, 2.1), (2.45, 2.9), (2.45, 3.025), (2.45, 0.975) |

## Refusal and sideways movement

`[bin]` Up/down nudges add +0.125 or −0.125 to X; left/right nudges add those values to Y. Select the positive nudge when probe 0 blocks and probes 2, 3, 4 are clear. Otherwise select the negative nudge when probes 0 and 1 are clear, probe 3 blocks, and probe 5 is clear. These predicates do not require all six results, and the routine does not gather a fresh probe set after the nudge.

`[bin]` Any blocked probe among 0–3 selects pushing and cancels the original facing displacement on the stepped axis. A selected sideways nudge survives and clears the push count; an ordinary blocked attempt increments it. Therefore sideways motion on a refused attempt does not imply a successful forward half-tile move.

`[bin]` For nonnegative coordinates, let trunc mean truncation toward zero. On refusal, up changes fractional Y to trunc(Y); down changes fractional Y to trunc(Y + 1). Left, when X + 0.5 has a positive fractional part, sets X to trunc(X + 0.5) − 0.5; right uses trunc(X + 1.5) − 0.5 under that same predicate. This snaps the stepped axis, correcting the earlier free-axis description. The rounding helpers explicitly select truncation.

`[bin]` Push counts of 38 or more become 18. At 18 a passing ledge predicate selects an eight-tick hop. The count-28 helper can suppress the caller's normal position commits, but the [selected helper path below](#selected-count-28-grid-transition) performs its own coordinate updates; suppression does not mean no movement.

## Selected count-28 grid transition

`[bin]` A later instruction read checked the selected executable against the identity above and followed this helper and its caller directly. It is separate from the original editor's prose-only review. Owner-held evidence: `FIRST-GRID-TRANSITION-20261129`. No original client was run.

At the selected blocked-movement gate, when the current count is 28 and the sideways-nudge flag is clear, the caller invokes the helper and saves its return byte. A nonzero return skips the caller's later normal X/Y setter calls.

The helper converts a facing-dependent sample point to an integer grid query, rejects that point outside 0–63 on either axis, and reads indexed storage using a 64-column stride. It searches a nested 2×2 pattern for a match to that one sampled value; this is not a check that the whole original 2×2 region matches a pattern. Two further point-test calls must both return false to reach the selected success path.

On that path, let `a` be the anchor derived from the matched pattern position and `d` the facing vector: up (0, −1), left (−1, 0), down (0, 1), right (1, 0). In the first nested 2×2 loop, the helper saves each old cell value at `a` and immediately replaces that cell with the value read at the corresponding position at `a + 2d`. A second nested loop writes the saved values at `a + d`. It also calls another helper whose effects are not fully traced here. The accessors read and write a 32-bit field in selected records; this does not identify the pattern or storage object's class.

The same success path calls both coordinate setters with the current coordinates plus `d`, then returns 1. Thus the caller omits its normal coordinate commits after the helper has performed its own. This is a normal-path static result, not a runtime observation or a complete account of all callee effects, exceptional state gates, object identities or input-to-update cadence. G064 remains partial.

## Verification and limits

`[bin]` The researcher asserted the executable digest before reading, decoded the referenced step/probe/nudge values as little-endian IEEE-754 doubles, and checked their consuming instructions. Candidate construction, branch conditions, counters and setters were reviewed against x86 instructions independently of recovered pseudocode. No client or server ran for this inspection.

- [x] ~~Recover the exact 1st Graal step, probe and corner-nudge constants.~~
- [x] ~~Recover the 1.39 tables separately.~~ The [later published comparison](static-reads-appendix-e-2026-11-20-b.md#139-movement-tables-e307) supplies the 1.39 step, probe and nudge tables separately; this earlier exact-input read did not establish them. The later comparison does not compare the 1.39 branch code instruction by instruction.
- [ ] The selected count-28 helper/caller path is followed above; complete exceptional state gates, object-list identities and input-to-update cadence remain open.

The same retained record also contains a death-counter observation. That independent finding is outside this movement note; it must not be inferred from the geometry or converted to a wall-clock death duration.
