# A better 3D client and server: what 5.12 limits, what we can lift, and in what order (2026-11-27)

Date: 2026-11-27. Planning note, no new lab run. It reads the 5.12 findings already on the
capability board, the state of our two 3D code bases (graal-client-repro
`common/cpp/graal3dengine` with the Frankenstein 6.037 host, and seihai-gserver `src/graal3d`),
and the big-world measurements of [T3D-166](3d-big-world-streaming-512-2026-11-27.md). Tags as in
`README.md`; every limit below links the note that measured or read it.

Question from the owner: can Seihai 3D be upgraded so a 3D Enigma-scale world runs better, and can
we build a better 3D client to pair with an improved 3D server? Follow-up: the new protocol has to
be version controlled, because original Graal3D clients cannot run the new features.

## Short answer

- **Yes, and it does not have to cost the real clients anything.** Everything new goes behind an
  opt-in extension, `seihai3d` version 1 ([seihai3d-ext-v1.md](seihai3d-ext-v1.md)). A real 5.12
  never asks for it, so the server keeps serving it the stock protocol byte for byte; our client
  asks for it and falls back to stock on a server that does not answer. The wire contract is
  written and tested (seihai-core `protocol::three_d_ext`).
- **The 5.12's ceilings are in its binary** (4096 ghosts, one wrapped 256 by 256 terrain grid,
  lighting only at Phase 2, a terrain cache per server, a ~1000-unit draw horizon). The server can
  work around them, as T3D-166 shows, but only a new client removes them.
- **Our client is not yet faster than 5.12; it is slower.** Its renderer is software only, and the
  Frankenstein host draws the 3D frame "at most about half the time" of its 50 ms tick
  (`frankenstein-6037/README.md`). The biggest "runs better" win is a GPU renderer, and it needs
  no protocol change at all.
- **Recommended first build step:** a GPU (OpenGL) back end for `graal3dengine/render` behind the
  same `graal3dengine_renderFrame` call, with a frame-time counter built in. Detail in §6.

## 1. What the stock 5.12 client limits

| Limit | Value on 5.12 | Evidence | Server-side workaround today |
|---|---|---|---|
| Ghost table | 4096 slots; ≥ 4094 world objects black out the view for the whole session | [T3D-166](3d-big-world-streaming-512-2026-11-27.md) §3 **[lab]** | Distance scoping (seihai-gserver `graal3d/scope.rs`), ~1400 slots for a 20 000-object world |
| Terrain | One `TerrainBlock`, one 256 by 256 grid (16 by 16 chunks), repeat or not; square size only stretches it | [terrain-512.md](terrain-512.md), T3D-166 §1 **[lab]** | Sliding window: chunks overwritten mod 16 as the player moves (T3D-166 §6B, lab patch) |
| Terrain request | Once, when the block is added; never again while walking | T3D-166 §2 **[lab]** | Server pushes chunks unasked |
| Terrain cache | Keyed by server name, not world: every world switch resends all 256 chunks (~45 KB, ~7 s) | T3D-166 §5 **[lab]** | None; use separate worlds only behind warps |
| Lighting | Terrain, water and Sun lit only at `MissionStartPhase2` | [T3D-162](3d-worldswitch-terrain-lighting-512-2026-11-26.md) **[lab]** | Send Phase 2 again after each window swap (0.04 s relight; script side effects not checked) |
| Draw horizon | ~1000 units by default, `visibledistance3D` at most 2400 | [T3D-075](3d-capability-board.tsv), [scoping note](3d-scoping-interiors-limits-512-2026-11-26.md) | Scope radius 1100 matches it |
| Join pacing | Our server sends one ~400-byte packet per 50 ms (~8 KB/s); 4000 objects took 31 s | T3D-166 §4 **[lab]** | 10 ms worked with no loss on 5.12 |
| Chat | No chat line in the 3D view; 3D players get 2D chat only | [T3D-069](3d-2d3d-crossview-flags-movetype-512-2026-11-26.md) and the GUI overlay note **[lab]** | None |
| Script-made objects | GS2-made 3D objects do not draw; sky and fog functions change nothing | [live GS2 probe](live-512-gs2-3d-probe-2026-11-25.md) **[lab]** | Server-side objects only |
| Shapes and textures | DTS ≤ 24; textures ≤ 1024 a side; a per-shape draw ceiling ~265k to 400k vertices | [texture limit](3d-texture-size-limit-420r6-2026-11-26.md), [mesh limit](3d-mesh-size-limit-420r6-2026-11-26.md) **[lab]** | Author within them |
| Frame rate | Not measured on 5.12 yet. On the 4.20r6 software floor: inverse-linear in ghosts, steeper in triangles | [T3D-113](3d-frame-rate-scaling-420r6-2026-11-25.md) **[lab]** | Being measured in the big-world work (below) |

## 2. What our client already does, and its gaps

The Frankenstein 6.037 client is the 6.03r7 Quattro host with the 5.12 repro's 3D side linked in
(`frankenstein-6037/README.md`; [T3D-122](3d-frankenstein-6037-vs-600-2026-11-26.md),
[T3D-132](3d-frankenstein-6037-vs-retail-6037-2026-11-26.md)). The 3D side is
`common/cpp/graal3dengine`, shared with the 4.x and 5.x folders.

**Has:** the protocol-24 link from connect to login step 6 (handshake, acks, events, ghosts,
mission start, control object and its three movetypes), checked against the recorded real 5.12
session and a third-party server's capture; a software renderer for `.3ds`, `.dts` 19 to 24,
`.dif` 44, `.ft` trees (off by default as on 5.12), streamed terrain, water, sky box, fog,
replicator ground cover, name tags; GS2 weapon scripts on the 6.x machine; Windows, Linux and
macOS builds.

**Gaps, roughly by how much they hold a player back:**

| Gap | Effect | Where |
|---|---|---|
| Software rasteriser only | Slower than 5.12; the 3D frame is drawn at most every other tick | `render/raster.*` |
| No terrain cache in the link (stamps computed, 256 zero stamps sent) | Every join and world switch downloads all terrain (5.12 at least caches per server) | `src/link.*` terrain |
| The 5.12 GS2 3D surface: 35 classes, 418 members, none bound | Clientside 3D scripts (cameras, `castRay`, `get3Dobjects`, `getz`, sky setters, `ActionMap`, `GameObject`'s 23 properties and 26 methods) do nothing | [typed surface](gs2-3d-typed-surface-512-2026-11-26.md); no binding in the client tree |
| Animation threads (`GameObject` section 8) | Shapes do not animate | `render/README.md` "Not yet" |
| Terrain material blending, texture scale, water reflection | Flatter look than 5.12 | same |
| `.dif` lightmaps and other detail levels; `.dts` 17 and 18, IFL | Interiors flat-lit; some shapes refused | same |
| Lighting not checked against 5.12 side by side | The Sun's colour and ambient do nothing yet | same |
| No chat in 3D, no frame stats | Same as 5.12 | — |

## 3. What a new client can lift

Two kinds of improvement, and they need different things from the server:

**Client-only (works against any server, stock or ours):** a GPU renderer; frustum and distance
culling per object; vertex buffers per shape loaded once; mipmaps; instanced ground cover; LOD
from `.dts` detail levels; a terrain cache with the 5.12's own stamps, so a warm join is ~0.5 s
instead of ~8 s (T3D-166 §1); frame-time statistics on screen and to a log. None of this changes a
byte on the wire.

**Needs the server to agree (the extension, §4):** more than 4096 ghosts; terrain past one wrapped
16 by 16 grid; a terrain cache per world; chunk relight without a second Phase 2; a draw distance
past 2400 with a matching scope radius; faster pacing; chat in the 3D view; the client reporting
its frame rate to the server.

## 4. Version control: how old and new clients share one server

The rule the owner set is that original Graal3D clients must keep working. That is easy to break
by accident: a 5.12 drops its link on an unknown ghost class (T3D-099 and the recovery note), and it
cannot be told about new classes. So the extension is never offered, only asked for.

Three numbers identify a 3D client, and only the last one is new:

| Number | Where | Who sets it |
|---|---|---|
| TCP login token (`G3D14097`, `G3D0311C`, …) | gen-5 login | The host build. Our client keeps a stock token, so any server lets it in |
| Torque protocol (24) | UDP connect request, twice | Stays 24, so a server without the extension accepts the request |
| `seihai3d` extension version (1) | A third connect argument, `seihai3d/1/<caps>` | Our client only |

The handshake, in full in [seihai3d-ext-v1.md](seihai3d-ext-v1.md):

1. Our client adds `seihai3d/<version>/<caps hex>` after the account and the nickname.
2. A server that speaks the extension sends one guaranteed `RemoteCommandEvent` `seihai3d
   <version> <caps>` before `MissionStartPhase1`, with the intersection of both sides' caps.
3. Our client that sees `MissionStartPhase1` with no reply is on a server without the extension
   and runs as a plain 5.12. A server that gets no hello serves the stock protocol and sends
   nothing new. The server keeps choosing the client's capability row by token and protocol as it
   does now (`graal3d/caps.rs`); the extension mode is one more field beside that row.

The version lives in seihai-core (`protocol::three_d_ext::EXT_VERSION`), so the gserver and the
client read the same constant. A bit's meaning never changes once released; a new capability is a
new bit and a version bump. A newer client and an older server (or the other way round) agree on
the lower version and its bits.

## 5. Roadmap

Effort is rough agent working time, each stage one PR per repo where possible.

| Stage | What | Repos | Effort | Depends on |
|---|---|---|---|---|
| 0 (done here) | The `seihai3d` v1 wire contract and its tests; this plan and the spec | seihai-core, Graal_analysis | — | — |
| 1 | **Client runs better on any server.** OpenGL back end for `render/` behind `graal3dengine_renderFrame` (software path kept for headless tests); per-object culling; shape buffers; mipmaps; frame-time overlay and `--fps-log`. Then the terrain cache in the link with the 5.12's stamps | graal-client-repro | 1 to 2 weeks | — |
| 2 | **Server speaks v1.** Read the hello in the connect request, send the reply, keep a per-link `Mode`; a `graal3d_ext` switch (on by default, since a stock client can never trigger it). First caps: `frame_stats`, `view_distance`, `fast_pacing`, `world_terrain_cache`, `chunk_relight`, `chat_3d`. Client side of the same six. Conformance: a stock-5.12 regression case against an extension-enabled server (must be identical), and our client against a server without the extension (must fall back) | seihai-gserver, graal-client-repro, Graal_analysis conformance | 3 to 5 days | 0; 1 for `frame_stats` |
| 3 | **Lift the hard limits for our client.** `wide_ghosts` (14-bit indices, 16 384 slots), `world_chunks` (world chunk coordinates, no mod-16 wrap), LOD and impostors for far objects; a draw distance past 2400 | both | 1 to 2 weeks | 2 |
| 4 | **The GS2 3D surface.** Bind the 35 classes in the client's GS2 machine, most used first: `GameObject`, `Camera`, the global `castRay`/`get3Dobjects`/`getz`, `Sky`/`Sun` setters, `ActionMap`; the editor classes last. Each behaves as 5.12's where 5.12 works, and our own way only behind an extension bit | graal-client-repro | 2 to 3 weeks | 1 |
| 5 | **Look parity and past it.** Animation threads, terrain blending, `.dif` lightmaps, water, side-by-side lighting checks with a real 5.12 in the lab | graal-client-repro | ongoing | 1 |

## What this plan does not repeat

The thread building a large world from chunks owns: how a big world is authored as a grid of chunk
files, per-chunk object budgets for dense towns under the 4096 cap, chunk-split towns against warped
interiors, and the frame rate, CPU, GPU and memory of the **real 5.12** walking that world. This plan
uses its results and does not measure them again. Where its workarounds exist only because of 5.12
(the extra Phase 2, the 1100 scope radius, the mod-16 window), the extension bits
`chunk_relight`, `view_distance` and `world_chunks` are how our client stops needing them; the
server keeps the workarounds for real clients.

## 6. First build step

**OpenGL back end for `graal3dengine/render`, with frame timing, in graal-client-repro.**

- It is the main reason our client is slower than the real one, and it helps on every server
  (ours, a stock-protocol server, a third-party one) with no protocol change and no risk to real
  clients.
- It gives the frame-rate instrument for our own client that stage 2's `frame_stats` reports, and
  that the big-world thread's 5.12 numbers can be compared with.
- It is self-contained: the scene, readers and resolver stay; only the rasteriser is replaced, and
  the software path stays for headless tests and the conformance screenshots.
- Lab check when it lands: the same world on the real 5.12 and on our client in the lab's Linux and
  Windows 10 VMs, frame time and pixels side by side (the conformance suite already drives both).

Stage 2's server half is small and can run beside it.

## Open

- Whether a third-party 5.12-protocol server (SharpServer) accepts a connect request with a third
  argument **[inf]**: stock Torque passes extra arguments to script, but this is unchecked. The
  client keeps an option to send no hello.
- Frame rate on the real 5.12 under a GPU (only the software floor is measured).
