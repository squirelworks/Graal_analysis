# 3D scale II: what a 5.12 can draw, and how replicators scale (T3D-149/153)

Date: 2026-11-26. Lab: a real 5.12 in a Windows 10 VM (QEMU std VGA, i.e. the VM's
software/GDI render path) against seihai-gserver main (5cd9c15) on the loopback, driven by a
small GS2 frame-rate probe. Behaviour only; lab tooling stays in the lab kit, off every PR.
**[lab]**

Two rows that extend [the ghost-capacity / asset / world-parse note](3d-scale-assets-worldparse-147-154-155-512-2026-11-26.md)
(T3D-147/154/155): the client's draw-rate ceiling, which T3D-147 pointed to (no ghost cap, the
limit is draw time), and how replicators scale against it.

**Numbers caveat up front:** this is the VM's *software* renderer, so the absolute frame
rates are VM-bound — a real GPU would shift the whole curve up. The *shape* of the curve
(roughly linear per drawn object, a fixed terrain cost, a cap set by the OS tick) is what
carries over.

## T3D-149 — frame rate vs scene complexity

**Measuring FPS without a visible counter.** The 5.12 GUI exposes no reachable Torque
metrics/console, so a `weapon3d` probe re-arms `setTimer(0.001)` and counts callbacks per
wall-clock second, reporting the count once a second through a `triggerserver` `g3dpos` call
(the trace logs it as the client's position). Two checks confirm the count is frames, not a
fixed tick: it falls as objects are added, and it drops to ~7–10 the instant another window
takes focus (Torque's background-window frame throttle). The values are quantized to 64/k
(64, 32, 21.3, 12.8, 7.9), i.e. frames paced to Windows' 15.6 ms tick, so **64 fps is this
client's cap here** and each step is a whole number of ticks per frame.

Sustained rate (steady-state; opening/closing seconds dropped):

| scene | sustained fps |
| --- | --- |
| empty (Sun, Sky, avatar) | 64 (cap) |
| 100 GameObjects | 64 (cap, unaffected) |
| 500 | 32 |
| 1000 | ~21 |
| 2000 | ~13 |
| 4000 | ~7.9 (after the ~28 s black-screen wait from T3D-147) |

Streamed terrain alone (a TerrainBlock, no objects) costs a **fixed chunk** that is largely
independent of extent: square size 1 (256 units) ~21 fps, size 4 (1024) ~17, size 16 (4096)
~21 — the engine's terrain LOD caps the work. On this VM: the first drop below the 64 cap is
between 100 and 500 objects; below ~30 fps ("not smooth") from ~500 objects or any streamed
terrain; unusable (<10) at ~4000 objects. Cost is roughly linear in object count — each cube
is a separate draw.

## T3D-153 — replicator autoload: one ghost per line, copies are the client's cost

A level autoloads its replicators from the world file. Set A raised the number of replicator
*lines* (each 1 cube per cell, radius 4 → 81 cells); set B held one line and grew its radius.

**Server side: flat and cheap.** Each replicator line becomes exactly **one ghost**; the
scattered copies are built client-side and never ghosted. 10/100/200/500 lines gave
10/100/200/500 ghosts, all accepted and delivered with no cap, warning or slowdown, down the
same ~140 creates/s pipe as T3D-147 (the control object arrived at server packet 8/54/104/254,
the last ≈ 12.7 s, and the Camera/control-last ordering applies here too). **So T3D-147's
network cost scales with replicator lines, not with placed copies.**

**Client side: the placed-copy count sets the frame rate,** exactly as T3D-149's per-object
cost predicts:

| set A (lines × ~81 cells) | ≈ copies | fps |
| --- | --- | --- |
| 10 lines | ~810 | ~12.8 |
| 100 lines | ~8,100 | ~3.5 |
| 200 lines | ~16,200 | ~1.5 |
| 500 lines | ~40,500 | ~0.2 (effectively frozen; no crash/drop, left only on close) |

Set B (one line, 5 per cell, growing radius): radius 8 (~1,445 copies) ~9.4 fps, radius 16
(~5,400) ~8.1, radius 32 ~8.1, radius 64 ~8.1 — the rate **plateaus from radius 16** because
cover only grows where its placement rays hit terrain, and the terrain here is ~16 cells
either side of the avatar, so a larger radius adds no copies past the terrain edge.

## Verdict

Replicators are the **network-efficient** way to fill a world — one ghost per line however
many copies it scatters — but every copy still costs client **draw time**, roughly in line
with a hand-placed GameObject. On this VM's software renderer, ~800 placed copies already halve
the frame rate, ~8,000 make it unplayable, and ~40,000 freeze the client (while the server
never feels it). Practical limits for authors targeting low-end clients: keep total placed
copies (replicator copies + GameObjects) under ~500–800 for a smooth game, treat ~5,000 as the
unusable line, and remember a replicator radius only matters up to the terrain's extent and
that streamed terrain alone already takes roughly two-thirds of the frame budget. Because a
world can freeze a client while costing the server nothing, a **server-side sanity cap or
warning on the total expected copy count** (lines × cells × max-per-cell) would be a cheap
guard — optional, but it is the only place the cost is visible before a client hits it.

## Summary

| row | verdict |
| --- | --- |
| T3D-149 | A real 5.12 (VM software renderer) caps at 64 fps (frames paced to the 15.6 ms Windows tick, quantized 64/k) and falls roughly linearly with drawn-object count: 100 obj = 64, 500 = 32, 1000 = ~21, 2000 = ~13, 4000 = ~7.9; streamed terrain costs a fixed ~21-fps chunk largely independent of extent (LOD-capped); below ~30 fps from ~500 objects or any terrain, unusable (<10) at ~4000. Absolute numbers are VM-bound (software render); the linear-per-object + fixed-terrain shape carries over. Measured with a setTimer-callback frame probe. **[lab]** |
| T3D-153 | Replicator autoload is flat and cheap server-side — each line is one ghost (scattered copies built client-side, never ghosted), so network cost scales with lines not copies and rides the same ~140 creates/s pipe as T3D-147 — but the client's frame rate is set by the placed-copy count per T3D-149: ~810 copies ~12.8 fps, ~8,100 ~3.5, ~16,200 ~1.5, ~40,500 frozen (no crash); radius plateaus once cover fills the terrain extent (~radius 16 here). A server-side sanity cap/warning on total expected copies would protect clients, since the server never feels the cost. **[lab]** |
