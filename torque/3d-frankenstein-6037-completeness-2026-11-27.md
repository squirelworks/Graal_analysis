# How complete the Frankenstein 6.037 is against what we know of the 5.12 3D client (2026-11-27)

Date: 2026-11-27. An audit of our own Frankenstein 6.037 client (graal-client-repro
`frankenstein-6037`, with `common/cpp/graal3dengine`) against every 5.12 behaviour the
[capability board](3d-capability-board.tsv) and the [conformance suite](conformance/README.md)
have settled, and against the Seihai server features a 3D client meets (big worlds,
interiors, world switches, staff editing, `seihai3d`). "Complete enough for what we know",
not complete in theory. Gaps closed in graal-client-repro #477. Tags as in `README.md`.

## Verdict

**Before #477: about 60%** (19 of the 36 rows below work, 5 partly). The wire (protocol 24 from connect to step 6, ghosts,
control object and movetypes, terrain, water, sky, cover, files) and the renderer were
done and lab-run; what was missing was nearly all on the script side: the 5.12's GS2 3D
objects read 0, `timevar3` was absent, GS2 GUIs drew only in the 6.x inset, a server move
of the player was never reported back, and 3D files were asked for by the wrong names.
Scored against the **5.12** expectations (not the all-`?` 6.037F column, which made
every run read PASS), its last lab runs matched the 5.12 in **23 of 36** cases run.

**After #477: about 80%** (27 work, 3 partly) by code and unit test. The C030 probe now gives back every
value the real 5.12 gave; C009, C010, C011, C006 and C007 are fixed in code; `seihai3d`
v1 is in on the client side. The lab rerun on #477 is the check (below). What remains
is mostly look (terrain near band, Sun flare, lightmaps, animation), input (mouse-look,
the 5.12's own keys), the rest of the GS2 surface, and the `seihai3d` bits that need the
server half.

The percentages weight each row below equally, a partial counting half.

## Gap table

Status: **works** (does what the 5.12 does, or better where the 5.12 is broken), **partial**,
**missing**. "Verified" says how: **[lab]** a lab run of the Frankenstein (conformance
6.037F rows, `docs/lab/frankenstein-6037-lab-2026-11-26.md` in graal-client-repro),
**[test]** a unit or loopback test in graal-client-repro, **[code]** read in the source only.

| # | Feature | What 5.12 does | Frankenstein before → after #477 | Verified |
|---|---|---|---|---|
| 1 | `3 ` entry, TCP login + UDP on port + 1, protocol 24 to step 6 | links, control object, mission phases (C001, T3D-164) | works | [lab] C001, C002, C029, C040 |
| 2 | Survives junk, floods, server drop, reconnect churn | survives (C015, C025, C027, C038–C040) | works | [lab] |
| 3 | Ghosts: create, update, delete; class table by name; 4096 slots | T3D-160, T3D-166 | works (deletes free the slot; scope give/destroy is ordinary ghost traffic) | [lab] C023, C024; [code] |
| 4 | Several players see each other | C020 | works | [lab] C020 |
| 5 | Control object movetypes (interpolate, list, rigid) | E#505 | works | [test], [lab] |
| 6 | Server move of the own object reported back (doors, same-world warps) | reports the new place (C011) | missing → **works** | [test] `testServerMoveReported`; lab rerun |
| 7 | Camera follows a server move | the server re-sends the Camera; the view follows | works (the view draws from the named Camera ghost) | [lab] 2026-11-26 run; [code] |
| 8 | Interiors in the same world, door links, portal prefetch (T3D-167) | `player.position` move from a script, no relink | works (a script's `player.position` moves the object; prefetched ghosts are ordinary ghosts) | [lab] lab #458 for `player.position`; interiors world not run on our client |
| 9 | Interiors: own Sky and Sun | not possible (outdoor sky serves inside) | missing on both (proposed `seihai3d` spaces bit) | — |
| 10 | Streamed terrain, chunk decode, heights.info, textures | C018, terrain-512 | works (our C018 passes where the 5.12's white-terrain check fails) | [lab] C018 |
| 11 | Big worlds: sliding terrain window, chunks overwritten mod 16 (T3D-166, seihai-gserver #227) | redraws a re-sent chunk | works by code: a re-sent chunk replaces its slot and the terrain is decoded again | [code]; not lab-run on our client |
| 12 | Relight after a world switch or window swap | lights only at Phase 2 (T3D-162) | works, better: our terrain is shaded whenever drawn, Phase 2 or not | [code] |
| 13 | World switch (`g3dworld`) | relinks or re-ghosts; terrain resent | works (ghosts replaced); no terrain cache, so every join and switch downloads all chunks | [lab] C029 (relinks); [code] |
| 14 | Terrain cache per server with stamps | caches per server name | missing (stamps computed, 256 zero stamps sent) | [code] |
| 15 | Near-camera terrain band, 75–150 unit fade, `TilesControl.getTilesForSpot` | first material near the camera unless a `TilesControl` weapon answers | partial: always the blended terrain (what the 5.12 draws with seihai-gserver's `TilesControl`); no band, no hook | [code] |
| 16 | Terrain material blending | bilinear corner blend, slope light (T3D-162) | partial: primary material per square only | [code] |
| 17 | Water | surface texture fetched and drawn (C019) | works (flat, no reflection) | [lab] C019 |
| 18 | Sky box, six faces, face order, options | C003, C004, T3D-046 | works (C004 face order; the 5.12 itself fails C004's front face) | [lab] C003, C004 |
| 19 | Sun lighting and `fxSunLight` flare | flare as a screen-filling quad (T3D-047) | Sun: rebuild's fixed light; flare: missing | [code] |
| 20 | Grass and shape replicators, origin-cell rule | cover around the avatar, none in the origin cell (C031–C037, C047) | partial: shapes and the origin-cell rule work; grass cards too small to pass the C035–C037 diff check | [lab] C035–C037 (grass_drawn = no on the last runs) |
| 21 | Shapes: `.3ds`, `.dts` 19–24, `.dif` 44, `.ft` off | C005, C006, C016, C017 | works (no animation threads, no `.dif` lightmaps) | [lab] C005, C006; [test] |
| 22 | Draw horizon `visibledistance3D` (1000, max 2400) | T3D-075 | works | [test] |
| 23 | File requests: shapes each visit, images by bare name, never `.cs`/`.ter` | C005, C006, C007, C028, T3D-033 | partial → **works** | [test] `request_name_3d`; lab rerun |
| 24 | weapon3d GS2 runs, triggers go back as `events` | C008 | works | [lab] C008 |
| 25 | `timevar3` | advances, server-synced (C009, T3D-024) | missing → **works** | [test]; lab rerun |
| 26 | GS2 GUI over the 3D view (`showimg`, `showtext`) | draws over the scene (C010, T3D-058) | partial (inset only; `showtext` never showed, T3D-152) → **works** | [code], lab rerun |
| 27 | `GameObject`/`SceneObject` members, formats, rotation rules | C026, C030 | missing (all read 0) → **works** for the core set | [test] the C030 probe gives every 5.12 value |
| 28 | `player.camera` live pose | readable (T3D-140) | missing → **works** (read only) | [code] |
| 29 | No `findobject` in weapon3d, server flags not delivered | C012, C013 (5.12: both absent) | works (absent, as 5.12) | [lab] |
| 30 | Rest of the GS2 3D surface: `castRay`, `get3Dobjects`, `getz`, Sky/Sun setters, mounts, `ActionMap`, editors (`WorldEditor`, `TerrainEditor`) | T3D-096, T3D-125, T3D-126, C042, C043 | missing | — |
| 31 | Staff in-game world editing (seihai-gserver `g3dedit`, #217/#225) | a staff weapon's triggers; the server re-ghosts | works by code: the triggers ride the `events` lines like any weapon's; not run on our client | [code] |
| 32 | Chat in the 3D view | none: 2D chat only (T3D-069) | missing → **works** on `seihai3d` `chat_3d` (lines bottom right; no bubbles); none against a stock server, as 5.12 | [test] `testSeihai3d`; needs the server half |
| 33 | `seihai3d/1` hello, reply, fallback (seihai-core #169) | n/a (ours) | missing → **works** client side (`frame_stats`, `chat_3d`); the other six bits missing | [test]; seihai-gserver does not answer yet |
| 34 | OpenGL renderer, software fallback, frame counter (#475) | OpenGL only | works | [test]; lab frame rates pending in #475 |
| 35 | Mouse-look and the 5.12's own 3D keys | mouse-look, `graalkeypressed` | missing (arrow keys walk the 6.x player and the 3D object follows) | [lab] |
| 36 | Animation threads (`GameObject` section 8) | animates | missing | [code] |

## Conformance: our client against the 5.12

Real 5.12 (Windows): **37 of 40** judged cases pass ([RESULTS.md](conformance/RESULTS.md); it
fails C004's front face, C018's ground checks and C036 on its own expectations).

Frankenstein 6.037, last runs before #477 (seihai-gserver 5cd9c15 / 833faba, gcr
ca85053a / be493cb6), each run's observed values judged against the **5.12's** expected
values, 36 cases run:

| Result | Cases |
|---|---|
| Behaves like the 5.12 (23) | C001–C003, C008, C012–C015, C018–C022, C025, C027–C030, C038–C040, C045, C046 |
| Differs (13) | C004 (asks_bare), C005, C023, C024 (asks_shape, first batch only), C006 (bare name), C007 (asks .cs/.ter), C009 (timevar3), C010 (overlay), C011 (moved), C026 (typed members), C035–C037 (grass) |

C005/C023/C024's `asks_shape` and C012/C013 are from the first batch (gcr ca85053a), before
the shape and probe fixes; the second batch did not rerun them. Of the 13, #477 closes C006,
C007, C009, C010, C011 and C026 in code and test; C004/C005/C023/C024 need only a rerun; the
grass cases (C035–C037) remain.

The rerun of 6.037F on #477 is below when it is in.

## What remains, by how much it matters for what we know

1. **Grass draws too little** to show in C035–C037: the 5.12's pieces are about a metre
   across at scale 1 and cover the ground at 40–60 a cell; ours are 0.6 a side.
2. **The server half of `seihai3d` v1** (seihai-gserver): until it answers, chat in 3D and
   frame stats do nothing; then the `world_terrain_cache` and `chunk_relight` bits.
3. **Terrain cache** with the 5.12's stamps (a warm join in about 0.5 s instead of about 8 s).
4. **The rest of the GS2 3D surface**, most used first: `castRay`, `getz`, `get3Dobjects`,
   Sky/Sun setters, mounts, `ActionMap`; the editor classes last.
5. **Look**: terrain material blending and the near band, the Sun flare quad, `.dif`
   lightmaps, animation threads.
6. **Input**: mouse-look and the 5.12's 3D keys.
7. **Lab runs on our client** of the big-world sliding window, the interiors world and staff
   editing, which are correct by code only.
