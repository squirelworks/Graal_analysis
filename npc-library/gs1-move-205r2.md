# GS1 queued movement in exact Windows 2.05 rev 2

## Evidence and limits

This static result covers the Windows 2.05 rev 2 executable with researcher-supplied SHA-256 `b0e39a04ca0891d0f02282a113a1cd80ddf7a1880a786c5831f26a452e8cbb08`. Evidence `GS1-MOVE-205R2-20261109-05` is registered in [the evidence index](../docs/evidence-index.tsv). The editor matched the sanitized publication document against its supplied digest; the private nine-file manifest, original instructions and executable were not independently inspected. Their verification is researcher-reported.

`[2.05][bin]` The researcher freshly crosschecked selected original instruction regions and reports nine frozen private files verified. No new client execution occurred. Scheduling frequency, catch-up, complete collision eligibility, nonfinite/overflow inputs, later event execution and bits outside this consumer remain unmeasured.

## Queue construction

`[2.05][bin]` A move record is relative to an endpoint accumulated from the actor's current position and prior queued displacements. The low two option bits choose replacement: 0 clears; 1 clears when the queued endpoint is more than five Manhattan units from the actor; 2 and 3 retain the queue. At least 100 existing records forces clearing. Start calculation precedes clearing, so clearing can reposition the actor to that calculated start.

## Consumer progression

`[2.05][bin]` The first consumer update places the actor at the recorded start. For a movement calculation, remaining duration divided by 0.05 is converted with biased floor: floor(value + 0.0001) for ordinary finite in-range values. Each remaining displacement is divided by that integer, then the applied displacement and 0.05 are subtracted from the record. This does not measure a 20 Hz scheduler.

`[2.05][bin]` A nonpositive integer bypasses the normal collision probes and takes completion. Remaining duration below 0.0001 also completes: set the recorded endpoint and remove the record. A sub-step duration can therefore bypass those probes on its first consumer update; the command itself does not synchronously finish it.

## Options and collision

| Option | Observed consumer behavior |
| --- | --- |
| 16 | Face the dominant displacement axis; ties choose vertical. Probes use the resulting facing. |
| 4 | Invoke broad blocking, temporarily making the moving NPC nonblocking to exclude itself. The query includes remote players, NPCs, bombs, an unidentified object collection, tiles and a conditional local-player body test. Eligibility remains partial. |
| 32 | Use the terrain-category predicate also reached by the `onwater` expression, corroborated by its name record and evaluator instructions. Classic-board tile IDs from 64 up to but not including 288 (64 ≤ id < 288) qualify; another board path uses a membership table. This is not a generic wall query. |
| 8 | Queue `movementfinished` on normal completion or collision cancellation, without directly running its body. |
| 64 | Select automatic character animation as described below. |

`[2.05][bin]` Character probes are direction-specific points at the body edge. Other actors derive a point from image/shape dimensions converted from pixels to tiles. This is one facing-dependent point test rather than swept-box collision. A collision discards the whole queue and leaves the attempted displacement unapplied.

`[2.05][bin]` For option 64, water chooses water animation. Otherwise an empty queue or displacement below the comparison tolerance on both axes selects idle. Displacement at least half a tile on either axis selects walking; smaller movement selects the slower variant. A special character profile supplies its own animation names. Asset availability and playback timing were not checked.

- [x] ~~Decode the bounded 2.05r2 move queue and option consumer.~~
- [ ] Measure caller scheduling frequency/catch-up and later event execution.
- [ ] Complete collision eligibility, unidentified collection and remaining option/state coverage.
- [ ] Establish overflow/nonfinite behavior and animation timing.
