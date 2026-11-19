# Gen-3 probe: the 2.0x-era Windows clients (2026-11-19)

`[lab]` The `wine-core.plan` server→client row set that run `w205-b` used on 2.05 rev 2 under Wine, replayed through
`tools/probe/gen5probe.py` (gen-3 mode) against every other gen-3 Windows build we hold. Rows are in
`probe-results.tsv` with run tags `w200` … `wnwb2`. Captures, screenshots and logs stay with the owner.

## Setup

- **Clients ran natively on Windows 10** (a lab clone, one client at a time), not under Wine. The probe lab VM that ran
  `w205-b` was fully loaded by other jobs, so this set moved to a Windows guest. Each build's exe was verified against
  the MD5 in `client-internals/build-catalogue.md` before use.
- Data folder: the 2.05 rev 2 data tree for every build, plus `objects.dat` (taken from the 1.41 rev 1 folder; 2.03 and
  older refuse to start without it), `zlib.dll` from the 2.02 folders. The NewWorld betas ran from their own folders (they need `arraysnw.dat` and their own data layout).
- Server: the GServer-v2 Windows build (`gs2emu`, classic `gs1classic`-based world, every 2.0x token, 1.41 rev 1's `GNW13110` and the NewWorld `G2N15041` added to
  the newmain line of `allowedversions.txt`) behind `gen5probe.py` on loopback; `seihai-listserver` for the list. The guest reached only
  those ports.
- Canary: bombs reset to 1 before each probe, then `c:5 c:99` after the probed prop (or in a separate message for the
  unknown-PLO probes). The bomb counter was read from the screenshot against two reference shots (count 1, count 99).
  Every run gave a clean two-way split (no "unclear" shot).
- Load guard: a run starts only when the guest's own load (CPU × vCPUs + queue length) is ≤ 4 and the host has spare
  memory. No run needed the load > 6 fallback, so no row carries the fallback note.

## Results

| Build | Token | Run | Rows | Alive | Outcome vs `w205-b` |
| --- | --- | --- | --- | --- | --- |
| 2.05 rev 1 | GNW03081 | `w205r1` | 32 | all | identical |
| 2.05 | GNW03081 | `w205` | 32 | all | identical |
| 2.04 | GNW24061 | `w204` | 32 | all | identical |
| 2.03 | GNW06051 | `w203` | 32 | all | identical |
| 2.02, 2.02 rev 1, 2.02 rev 2 | GNW15041 / GNW20041 | — | 0 | — | crash on Start, before any packet (below) |
| 2.01 rev 1 | GNW23021 | `w201r1` | 32 | all | identical |
| 2.01 | GNW23021 | `w201` | 32 | all | identical |
| GraalX | GNW23021 | `wgx` | 32 | all | identical |
| 2.00 rev 3, rev 2, rev 1, 2.00 | GNW24011 | `w200r3` … `w200` | 4 × 32 | all | identical |
| NewMain 24, NewMain 26 | GNW08011 | `wnm24`, `wnm26` | 2 × 32 | all | identical |
| 1.41 rev 1 | GNW13110 | `w141r1` | 32 | all | identical |
| 2.1 test 2, test 3 | GNW03081 | `w21t2`, `w21t3` | 2 × 32 | all | identical |
| NewWorld beta 1, beta 2 | G2N15041 | `wnwb1`, `wnwb2` | 2 × 32 | all | identical (rupee canary, see below) |

"Identical" means every one of the 32 rows has the same canary and alive outcome as the `w205-b` row with the same
payload. In every build that logged in:

- Own-prop probes (`PLO_PLAYERPROPS` 9): prop 3 at its documented width keeps the stream in step; props 77–83 and 90
  at the probed widths lose the canary, as on 2.05 rev 2. None of these builds knows those props.
- Unknown PLO ids 60, 78, 81, 83, 110: an empty body, one byte, or a text body is skipped to the end of its message
  and the canary in the same frame lands. The `ff00ff00` body loses the same-frame canary, as on 2.05 rev 2.
- No client closed the connection, crashed or answered any probe.

So the gen-3 client parser did not change in these respects from 1.41 rev 1 (November 2000) through the 2.1 test
builds and the second NewWorld beta (October 2001). The native runs of 2.05 and 2.05 rev 1 give the same rows as the Wine run of 2.05 rev 2, so the `w205-b` result
is not a Wine artefact.

The NewWorld betas' HUD shows no bomb count, so their runs used `tools/probe/lab/wine-core-nw.plan`: the same probes
with the rupee count (prop 3, GINT3) as the canary (reset to 1, canary 99). Every shot got the same verdict as the
matching 2.05 rev 1 shot.

## 2.02, 2.02 rev 1, 2.02 rev 2: local crash on Start

All three are the only 2.0x builds that load `zlib.dll` dynamically. With it in place they reach the start window,
then crash the moment Start is pressed, before the list connection opens: an access violation inside the client's
MNG image loader (the routine that raises "MNG loading failed!"). The crash is the same with every `.mng` file removed
from the data tree, and under Wine.
This is a client start-up problem in our setup, not a protocol finding. These builds have no rows.

## Server-side consequences

None new. Nothing in this set crashed or disconnected on any probe, so there is no new "the server must never
send X" rule for 2.0x clients beyond what `w205-b` already showed.
