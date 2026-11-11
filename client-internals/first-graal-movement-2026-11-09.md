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

`[bin]` Push counts of 38 or more become 18. At 18 a passing ledge predicate selects an eight-tick hop. A helper reached at count 28 can prevent position commits; its complete meaning remains untraced.

## Verification and limits

`[bin]` The researcher asserted the executable digest before reading, decoded the referenced step/probe/nudge values as little-endian IEEE-754 doubles, and checked their consuming instructions. Candidate construction, branch conditions, counters and setters were reviewed against x86 instructions independently of recovered pseudocode. No client or server ran for this inspection.

- [x] ~~Recover the exact 1st Graal step, probe and corner-nudge constants.~~
- [ ] Recover the 1.39 tables separately; these values do not settle that half of E#307.
- [ ] Establish complete exceptional state gates, object-list identities and input-to-update cadence.

The same retained record also contains a death-counter observation. That independent finding is outside this movement note; it must not be inferred from the geometry or converted to a wall-clock death duration.
