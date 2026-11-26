# The networked terrain/water/replicator/sun-flag layer is unreachable over our lab-server route: no emit path, GS2 terrain hooks are no-ops (T3D-042/045/050/078; T3D-047/048 blocked), Linux 4.20r6 + 4.04r2

Date: 2026-11-26. Single-client lab on native Linux, 4.20r6 (5.12-class, protocol 24, g3d420 route) and 4.04r2 (protocol 19, g3d404 route), software GL; our own loopback gserver. Observation only. Board rows: [T3D-042](3d-capability-board.tsv), [T3D-045](3d-capability-board.tsv), [T3D-050](3d-capability-board.tsv), [T3D-078](3d-capability-board.tsv) (closed here), and the blockers on [T3D-047](3d-capability-board.tsv) and [T3D-048](3d-capability-board.tsv). Builds on [T3D-092](3d-capability-board.tsv) (near-empty handshake), [live-512-sun-replicators](live-512-sun-replicators-2026-11-25.md), [live-512-lighting-and-sky](live-512-lighting-and-sky-2026-11-25.md), and the no-terrain-path static read ([T3D-121](3d-v6-quattro-vs-512-2026-11-26.md)).

## Headline (the shared blocker)

The lab gserver's 3D scene grammar has **no terrain / heights / gmap / water / replicator keyword** — only `object`, `sun`, `sky`, `skyoptions`, `playershape`, `spawn`, `camera`, `tgecontrol`, `tgeplayershape`, `weapon3d`. The **Sun ghost carries only direction + colour + ambient** (no flag bitfield), and the **GameObject ghost has no liquid/terrain/className fields**. So a `TerrainBlock`, `WaterBlock`, replicator, or `fxSunLight` flag bitfield **cannot be ghosted on either protocol** — the client registers these classes but nothing on this route instantiates them (consistent with [T3D-121](3d-v6-quattro-vs-512-2026-11-26.md)/[T3D-092](3d-capability-board.tsv)). That single blocker shapes every row below.

## T3D-042 — terrain on 5.12: no path **[lab]**

No keyword ghosts a `TerrainBlock`/heights. GS2 `setterrain(int)` is callable on 5.12 but a **silent no-op** without a `TerrainBlock`: a weapon called `setterrain(0/1/2)` + `updateterrain` → no file requested, no terrain drawn, no cache, no error, client stayed up. `TerrainBlock` is a registered class but nothing instantiates one here.

**For a server:** you cannot give a 5.12 client terrain over this protocol; `setterrain` does nothing without a `TerrainBlock` emit path the engine doesn't expose.

## T3D-045 — WaterBlock + liquid* on a GameObject: no path, no-op **[lab]**

No keyword ghosts a `WaterBlock` → no water surface, no water-fog. Setting `player.liquidtype="water"` via GS2 changed nothing visible (nothing to drive without a `WaterBlock`). (The `WaterBlock` surface look itself — a single ±0.5× oscillation at 6.0 s — is the earlier [live-512-sun-replicators](live-512-sun-replicators-2026-11-25.md) correction.)

**For a server:** you cannot deliver water (surface/fog) over this route; `liquidtype`/`liquidheight` on a GameObject have no effect without a `WaterBlock`.

## T3D-050 — does setTerrain write a heights cache? No, on either build **[lab]**

- **5.12:** `setterrain` is callable but a no-op (no `TerrainBlock`) → only the normal session write set, **no heights/`.ter`/terrain cache** (cf. the file-footprint set in [3d-session-file-footprint](3d-session-file-footprint-420r6-2026-11-26.md)).
- **4.04r2:** `setterrain` is **not client-callable from a weapon** — console `Function setterrain not found in script` (same shape as `playaudio`, [T3D-061](3d-capability-board.tsv)) — so it did nothing.

**For a server:** `setterrain` produces no on-disk heights cache on either build; don't expect one from script.

## T3D-078 — heightmap formats/sizes on 4.04r2: no load path **[lab]**

Proto-19 ghosts only `Sky` + TGE `Player`/`Camera` (no `TerrainBlock`/heights), and `setterrain` isn't client-callable on 4.04r2, so the client **never requests a heightmap** regardless of what is served — formats/sizes are moot until a terrain-emit path exists. (The 5.12 half is already done; the 4.20r8 half is Windows and waits on [T3D-079](3d-capability-board.tsv), out of this single-client-Linux scope.)

**For a server:** a 4.04r2 client won't fetch/load a heightmap over this protocol; heightmap format/size choices are irrelevant without a terrain-emit path.

## Still blocked (not closed here)

- **T3D-047 (fxSunLight flag-bit count, 14 vs 16):** **not resolvable by lab bisect on this route.** The Sun ghost has no flag field, and no GS2 API sets `fxSunLight` flags, so there is no way to drive one bit at a time. The two disputed static reads ([fxsunlight-512](fxsunlight-512.md) counts 14; a second read counts 16) can only be settled by a **static read of the `fxSunLight` ghost-unpack against the decompile source** (owner-held — AGENTS.md keeps raw decompiles out of the repo), not by this lab. The networked sun on this route is just direction + colour + ambient; the flag bits are not a server-tunable surface here.
- **T3D-048 (replicators with a ghosted TerrainBlock):** **cannot be exercised** — the gserver emits only a plain GameObject (fixed class name) and can't ghost a `TerrainBlock` for replicators to scatter onto, and there is no placeable replicator class on this path. No scatter observed (same blocker as the earlier [live-512-sun-replicators](live-512-sun-replicators-2026-11-25.md) run). Closing it needs both a ghosted `TerrainBlock` and a placeable replicator class, neither of which exists on this route.

## For a server (summary)

Beyond `GameObject` + `Sky` + `Camera`, the 5.12-class / 4.04r2 **networked 3D-world object layer is not reachable over this gserver route**: no `TerrainBlock`, `WaterBlock`, or replicator can be ghosted, and the GS2 terrain hooks are inert (`setterrain` no-op on 5.12, absent on 4.04r2). A server built on this route delivers shapes, sky and a camera, not terrain or water.

## Method caveat

Single client, our own loopback gserver, software GL. The negatives are specifically about **this server/protocol route** — they confirm the static "no emit path" reads ([T3D-121](3d-v6-quattro-vs-512-2026-11-26.md)) rather than proving the client's registered `TerrainBlock`/`WaterBlock` classes could never draw if some other server ghosted them in the exact wire shape their readers expect. T3D-047's bit count and T3D-048's scatter both need capabilities this route does not provide (decompile source; a TerrainBlock emit path) and remain open.
