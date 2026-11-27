# gserver-v2's phase 2 hold on a real 5.12: Wine/Mesa and Windows 10 (T3D-162 follow-up)

Date: 2026-11-27. This is a lab retest of seihai-gserver-v2 #182, which ports seihai-gserver #223.
After phase 1 is acked, #182 holds `MissionStartPhase2` until the client has done two things:

- acked the creates of every TerrainBlock, WaterBlock and Sun ghost;
- had its terrain request answered and every `TerrainChunkEvent` in that answer acked.

The hold is capped at 15 s. #182 was merged with unit tests only. This note records how it behaves
on a real 5.12. **[lab]**

Builds (gserver-v2 branch `seihai`):

- **A** = `bd1aec1` (with #182)
- **B** = `d273525` (its parent, without #182) as the control

The fixture is the T3D-162 one from [the world-switch note](3d-worldswitch-terrain-lighting-512-2026-11-26.md):

- a 20° cone and a 45° cone, square size 4, 256 streamed chunks;
- a WaterBlock under the ground;
- a Sun and a Sky.

Only behaviour is recorded here. Captures, logs and shots stay in the lab kit.

## The two labs

| | Wine + Mesa | Windows 10 |
|---|---|---|
| Client | real 5.12 under Wine 10, Mesa llvmpipe, Xvfb | real 5.12, 32-bit Mesa llvmpipe |
| Server | A/B built in the VM; a log-only patch added ms timestamps | gs2emu Windows CI builds of A/B, no patch (no MSVC on the host) |
| Network | VM loopback | guest loopback (server, lobby and client in one throwaway VM clone) |
| Reference frame | A warm, which matches the #223 lab's lit first-link frame at 0.00% | A warm at +20 s |
| Runs | 57 | about 20 |

Pixel diffs count pixels that differ by more than 8 from the reference. The times run from the phase 1 ack.

## Cold and warm terrain cache

| Run | Wine/Mesa +2 / +5 / +20 s | Windows +2 / +5 / +20 s | Terrain lit |
|---|---|---|---|
| A cold (256 chunks) | unshaded on 3 of 4 runs, 0.00% on 1 / 0.00% / 0.00% | still loading / 0.00% / 0.00% | yes |
| A warm (0 chunks) | 0.00% / 0.00% / 0.00% | 0.00% / 0.00% / 0.00% | yes |
| B cold | 98.12% throughout | loading / 95.63–100% / 95.63% | no |
| B warm | 98.12% throughout | 95.63% throughout | no |

- **B fails the same way on both platforms.** Its TerrainBlock is created after phase 2, so the
  whole terrain stays unshaded for the session. The client logs "Mission lighting done" but never
  "Terrain lit". B's score is 95.63% on Windows against 98.12% under Wine only because the
  Windows camera frames the cone differently.
- **A cold under Wine:** the terrain is unshaded for about 1 s while chunks stream and phase 2
  is held. It then relights once and is lit by +2.0 to +2.9 s.
- **A cold on Windows:** the client shows black or white loading frames, and its first drawn
  frame, at +3.7 to +4.3 s, is usually lit already. One unshaded frame (under 0.5 s) appeared
  in 2 of 6 cold or restart runs.
- **No hard-edged dark patch** appeared on any run. That patch is the other T3D-162 failure mode,
  where chunks are lit from stale heights.

## Phase 2 timing

All times are in ms from the phase 1 ack.

| Case | Wine/Mesa A: sent / acked | Windows A: acked | B: acked |
|---|---|---|---|
| Cold, 256 chunks | +1075–1152 / +1208–1299 | +2311–4158 (+8668 on the first run after boot) | Wine +119–202 (sent +0); Windows +390–967 |
| 9 chunks (restart onto the 45° world) | +291 / +407 | +1922 | Windows +361 |
| Warm, 0 chunks | +156–227 / +277–443 (just after the Sky ack) | +1077–1451 | Windows +422–513 |
| No terrain, water or Sun | +0 / +36–102 | +248 | +0 sent; Windows +171 |

- **Under Wine, A sends phase 2 in the same ms as the last chunk ack.** Every "received terrain
  chunk" line comes before "Phase 2: Mission Lighting" and before "Terrain lit in 0.03–0.05 s".
- **On B, the chunks are acked about 1.1 s after phase 2** with a cold cache.
- **On Windows, A's phase 2 comes later on a cold cache** (+2.3 to +4.2 s against about +1.2 s
  under Wine). The delay is on the client side: the 5.12 is slow to take in 256 chunks, and one
  run logged "send window full". The hold stays well inside the 15 s cap.
- **No "phase 2 sent with … not yet created" line** appeared on any run on either platform.

## World switch

gserver-v2 has no runtime world switch. `config/graal3dworld.txt` is read only in `Addon::start`,
once at server start, and nothing else calls `Service::setWorld`. There is no reload path and no
`g3dworld` trigger. The second phase 2 that seihai-gserver #224 sends after a switch therefore has
no counterpart to port. **[static + lab]**

The nearest case is to stop the server, change to the 45° world (9 chunks differ) and relog with
the 20° cache still warm:

| | Wine/Mesa | Windows |
|---|---|---|
| A | lit; 0.00% against #223's lit 45° control at +2/+5/+20 s | one unshaded frame at +1.4 s, lit from +2.9 s; 0.00% at +5 and +20 s |
| B | 97.77% unshaded throughout | 98.43% unshaded throughout |

A world with no terrain, water or Sun sends phase 2 at once on A, as on B. The sky draws, the link
holds and nothing freezes. Note that seihai-gserver's sky-only freeze is a switch *into* such a
world, and v2 cannot reach that case.

## Grass (v2 specifics only)

The rule for which cell grass grows from is covered in T3D-048 (#1012). This section records only
what gserver-v2 does.

| Line | Wine/Mesa first visit | Windows first visit | Shaded by mission lighting? |
|---|---|---|---|
| radius 8, A | draws | draws (empty cache) | no |
| radius 4, A | draws | nothing (one warm run) | no |
| radius 4 and 8, B | draws | radius 8 draws | no |

- **gserver-v2's login push of grass textures works.** Grass draws on the first visit with an
  empty client cache.
- **Grass colour does not follow terrain lighting.** Under Wine, the grass was 59,148,50 over lit
  ground (174) and the same over unshaded ground (200). On Windows, a 255,0,255 texel drew as
  243,20,243 on lit A and 248,25,248 on unshaded B.
- **The Windows radius-4 blank is one run only.** It fits T3D-048's origin-cell rule better than
  any radius threshold, but it was not rerun here.

## Side effects

- **The link held on both platforms** on every run, until the harness closed the client. No
  crashes occurred, and no black frame appeared after the first terrain frame.
- **Movement works on Windows (A as on B).** Keys reached the client and the position changed in
  the trace: 107 position reports on A, with x 97..123 and y 99..125. Only the script's
  `keydown2` saw the keys; the client's own 3D bindings (`moveForward2` and the others) never
  fired.
- **Movement was not checked under Wine.** xdotool keys never reached the 5.12 window under Xvfb.
- **Harness pitfall:** focusing the 5.12 by its window menu pauses the game, and the link then
  times out on A and B alike. This is a problem in the harness, not in the server.

## Result

#182 does what #223 does, on both platforms. With it, the terrain is lit and matches the
reference cold, warm and after a restart onto a new world. Without it, the terrain stays unshaded
all session. gserver-v2 needs no further change for T3D-162.
