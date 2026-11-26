# The server time field drives `timevar3`, a synchronized Graal3D clock that animates smoothly (not jumps) and feeds day/night (T3D-024, Linux 4.20r6)

Date: 2026-11-26. Single-client lab on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route), software GL; a weapon read the time vars once a second. Observation only. Board row: [T3D-024](3d-capability-board.tsv). Extends the partial (the visible-distance field does not fog/clip GameObjects — [live-512-lighting-and-sky](live-512-lighting-and-sky-2026-11-25.md)).

## Headline

The server time field drives **`timevar3`** — a **synchronized Graal3D clock** (server+client, ms precision) that **advances continuously (~1/sec) and animates smoothly, it does not jump**. It is the clock that feeds the day/night drawing mode. `timevar` and `timevar2` are different, coarser clocks.

## The three time vars **[lab]**

A weapon read each second (default served time):

| var | what it is | behaviour |
| --- | --- | --- |
| `timevar` | coarse **integer tick** | stepped 2 → 7 → 15 (a counter, not wall-clock) |
| `timevar2` | **UNIX wall-clock** | ~1.7956e9 seconds |
| `timevar3` | **synchronized Graal3D time** (server+client, ms) | advances continuously ~1/sec (~12 → 40 → 80 across the run) — **animates smoothly** |

`timevar3` is the server-synced clock: it runs forward smoothly and feeds the day/night drawing mode, so changing the server time field **re-syncs** `timevar3` (it stays server-driven) rather than letting the client clock free-run.

## For a server

Drive day/night and other timed 3D effects via **`timevar3`**, read continuously from the server time field — it animates smoothly forward and stays server-synced. `timevar2` is the wall clock; `timevar` is a coarse counter. Time runs forward smoothly, so expect animation, not a jump, from a time change.

## Method caveat

Single client, loopback server, software GL, default served time. `timevar3`'s server-sync and smooth advance are read directly from the weapon's per-second samples; a deliberate time-**jump** test (abruptly changing the sent time) would need a gserver patch to the time field and was not run — but the observed behaviour (server-synced, advancing ~1/sec) indicates a changed server time re-syncs `timevar3` rather than stepping it discontinuously on the client.
