# Terrain after a world switch: a 5.12 lights only at phase 2, and takes a second one (T3D-162 follow-up)

Date: 2026-11-26. Lab: a real 5.12 under Wine with the full OpenGL renderer (Mesa llvmpipe)
in a headless lab VM. It ran against seihai-gserver on the VM's own loopback, with trace on,
`graal3d_pushterrain = true`, a fresh server each run, and a screenshot about every second.
Three server heads were used:

- the #223 head (126f946), which holds `MissionStartPhase2` until the terrain is in;
- a lab-only patch of that head, used for the probes;
- seihai-gserver #224 (1cb2362), the fix.

Only behaviour is recorded here. Captures, logs and shots stay in the lab kit. **[lab]**

This builds on [terrain-512.md](terrain-512.md), which covers the drawing and the fixed-light
shading rule, and on [the level-warp note](3d-level-warp-per-player-replicator-208-512-2026-11-26.md),
which covers the `g3dworld` switch and the world files.

## Setup

- **Default world:** the T3D-162 20° cone (square size 4), a `Sun`, and the camera straight
  down.
- **Second world:** `config/graal3dworlds/cave.txt`, the same lines but `terrain cave_terrain 4`,
  a 45° cone. Nine chunks differ from the default world.
  - Each `terrain` line names its own chunk folder, and the server serves that world's chunks.
  - Both worlds share one `heights.info`.
- **The 5.12 keeps one chunk cache slot per server name**, so switching between two different
  terrains always resends their nine chunks. A true 0-chunk switch needed a control world whose
  two terrains are identical.

### The weapon fixture

The fixture is a `weapon3d WarpW weapons/warpw.gs2` line in both worlds. `triggerserver`
from a weapon3d goes over UDP, as BigData. `MODE` and `LS` are filled in per run:

- `MODE` 1 switches to the cave only; `MODE` 2 also goes back later.
- `LS` is the number of ticks after each switch before `lightscene()` runs; 0 means never.

```
//#CLIENTSIDE
function onCreated() { this.n = 0; this.mode = MODE; this.ls = LS; echo("WSLAB created mode=" @ this.mode); setTimer(0.2); }
function onTimeout() {
  this.n++;
  if (this.n == 75) { triggerserver("gui", "WarpW", "g3dworld", "cave"); echo("WSLAB switch cave"); }
  if (this.mode == 2 && this.n == 225) { triggerserver("gui", "WarpW", "g3dworld", "default"); echo("WSLAB switch default"); }
  if (this.ls > 0 && (this.n == 75 + this.ls || (this.mode == 2 && this.n == 225 + this.ls))) { lightscene(); echo("WSLAB lightscene n=" @ this.n); }
  if (this.w != clientr.g3dworld) { this.w = clientr.g3dworld; echo("WSLAB world=" @ this.w @ " n=" @ this.n); }
  showtext(210, 4, 4, "Arial", "l", "n=" @ this.n @ " w=" @ clientr.g3dworld);
  setTimer(0.2);
}
```

The tick counter `n` keeps counting across switches, so the weapon is not restarted by a
switch.

## Before the fix: the new terrain is never shaded

These runs used the #223 head. The table gives the share of pixels differing by more than 8
from a first link to the same world.

| Case | Chunks after the switch | Lighting line after the switch | At +5 s / +20 s | Pixels differing |
|---|---|---|---|---|
| Cold | 9 | none | unshaded / unshaded | 97.8% |
| Warm (the cold run's cache kept) | 9 (one cache slot) | none | unshaded / unshaded | 97.8% |
| True warm (identical chunks) | 0 | none | unshaded / unshaded | 97.8% |
| Round trip, default → cave | 9 | none | unshaded / unshaded | 97.8% |
| Round trip, cave → default | 9 | none | unshaded / unshaded | 98.1% |
| Control: the cave as the first link | 9 or 0 at link | "Terrain lit" | lit | reference |

- **"Unshaded"** means the whole view is the flat texel cap (grey 198), so the cone can't be
  seen from above. It is not partly lit from the old heights, as in the T3D-162 cold-cache gap.
- **After every switch the client asks for terrain again.** It logs "Loading terrain from
  terrain chunks." and sends a new `TerrainRequestUpdates` 0.16 to 1.2 s later. The server
  answers it after the new TerrainBlock is created.
- **No lighting happens after a switch.** No "Phase 2: Mission Lighting" or "Terrain lit" line
  appears. A switch doesn't relink, and nothing sends a phase 2.
- **The initial link is unaffected.** Phase 1 ack to phase 2 ack took 242 to 449 ms over 15
  runs, with no warning line, and every first link drew lit.

**Conclusion.** A 5.12 lights terrain, water and Sun only at `MissionStartPhase2`. A
TerrainBlock it gets later, at a world switch or otherwise, stays unshaded for the session.
**[lab]**

## What relights it

These probes used lab-only changes. "Pixel-identical" means 0.00% of pixels differ.

- **`lightscene()` from the weapon, 3 s after the switch.** The view was pixel-identical to a
  first link about 1 s after the call. This held cold, warm, and on both legs of a round trip.
  The console printed "Terrain lit" after only one of the four calls, so the screenshots are
  the evidence. **[lab]**
- **A second `MissionStartPhase2` from the server.** A 5.12 accepts a second, third and fourth
  phase 2.
  - Each time it logs "Phase 2: Mission Lighting" and "Terrain lit", and acks it.
  - It keeps the link, the 3D view and the running weapon.
  - No GUI reset, link drop, black frame or flicker was seen at 1 s sampling.
  - **Timing decides the result.** Phase 2 sent before the new TerrainBlock existed left the
    terrain unshaded. Waiting also for the client's new terrain request and the acks of those
    chunks drew it correctly.
  - Sending phase 1 and then phase 2, with the initial-link hold, works too. **[lab]**

## The fix: seihai-gserver #224, validated

After a switch that brings a new TerrainBlock, WaterBlock or Sun, the server holds a second
phase 2 with the start's own wait:

- the new lighting ghosts are created;
- with a new TerrainBlock, the chunks the client then asks for are acked;
- the wait is capped at 15 s.

A switch with nothing new to light sends none. These runs used 1cb2362, built clean, with no
`lightscene()` in the fixture:

| Case | Chunks | Switch → new terrain request | Switch → second phase 2 ack | +2 s | +5 s | +20 s |
|---|---|---|---|---|---|---|
| Cold | 9 | 1154 ms | 1378 ms | 0.00% | 0.00% | 0.00% |
| Cold, repeat | 9 | 1227 ms | 1502 ms | 0.00% | 0.00% | 0.00% |
| True warm | 0 | 153 ms | 272 ms | 0.00% | 0.00% | 0.00% |
| Round trip, default → cave | 9 | 187 ms | 433 ms | 0.00% | 0.00% | 0.00% |
| Round trip, cave → default | 9 | 171 ms | 405 ms | 0.00% | 0.00% | 0.00% |

- **For scale:** the lit old world 2 s before a switch differs by 2.50%.
- **One unshaded frame** was seen, the round trip's first shot at +0 s. Every frame from +1 or
  +2 s on is lit.
- **Order:** after every switch the client logs:
  1. "Loading terrain from terrain chunks.";
  2. every "received terrain chunk" line (none in the warm case);
  3. "Phase 2: Mission Lighting" and "Terrain lit".

  All the post-switch chunks arrive before the second phase 2.
- **No side effects:**
  - every link held;
  - the weapon was not restarted (`world=cave n=76`, and `world=default n=226` on the return);
  - no "phase 2 sent with" or "no terrain request answered yet" line;
  - no GUI reset and no black frame.
- **The initial link still holds.** Phase 1 ack to phase 2 ack took 285 to 416 ms over 5 runs:
  416 ms with 9 chunks at link, 285 to 312 ms with none.

All of this is **[lab]**.

## Open: a switch to a world with no terrain, water or Sun stalls a 5.12

As a control, a switch went to a world with only a sky and one marker object. The server
correctly sent no second phase 2. The 5.12 then stayed on a sky-only frame:

- the marker never drew;
- the weapon's echoes and the client events stopped.

The #223 head, without the fix, does exactly the same, so this is an older problem. The lab did
not separate whether the missing terrain or the missing `Sun` triggers it. **[lab]**

## Summary

| Row | Finding |
|---|---|
| T3D-162 (world switch) | A 5.12 lights terrain, water and Sun only at `MissionStartPhase2`. After a no-relink world switch, the new world's terrain draws flat and unshaded for the session: cold, warm, and both ways. It accepts a second phase 2 (relights, acks, keeps the link, view and weapons) and `lightscene()` also relights. The phase 2 must come after the new TerrainBlock is created and its re-requested chunks are acked. seihai-gserver #224 does that and draws every switch pixel-identical to a first link by +2 s. Open: a switch to a world with no terrain, water or Sun stalls the client on a sky-only frame, on both server heads. **[lab]** |
