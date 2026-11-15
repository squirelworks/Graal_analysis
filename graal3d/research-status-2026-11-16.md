# Graal3D research status (2026-11-16)

Date: 2026-11-16. Resume pass for the February 2000 side project and its later beta (research-track avenue **#5** / Part IX). Own notes only: static and lab evidence already in this folder. No new binary session in this pass (client archives are not in the checkout; Wine needs native `d3drm.dll` for draw-time checks).

Tags: **[bin]** **[cap]** **[doc]** **[lab]** **[inf]** as in the linked notes. No hosts, machine names, drive paths, secrets or binary addresses here.

## Scope

| Line | Notes | Status index |
|---|---|---|
| February 2000 client + its `GServer` (`GR3DV002`) | `README.md`, `protocol.md`, `formats.md`, `client-behaviour.md`, `collision.md`, `camera.md`, `lab-2026-10-30.md` | this page §Settled / §Open |
| Later Genesis3D beta (`GR3DV003`) | `beta3-genesis.md` | App. E#504; this page §Beta |
| 4.x Torque plug-in (`Graal3DEngine.dll`) | `torque-engine-4x.md` + `torque/` | **Out of this resume** (Part X / avenue #4); listed only to keep the two programs apart |

## Settled (do not re-open without new evidence)

| Topic | Result | Evidence |
|---|---|---|
| Archive identity | Client + own server, resource stamps 2000-02-05, between 1.32 and 1.33 | `README.md` **[bin][file]** |
| Wire codec | 2D text codec, no key/scramble; version `GR3DV002`; peer UDP for props 1–5 and chat | `protocol.md` **[bin][cap]** |
| Login / level / props / admin | Lab-confirmed TCP order and layouts | `lab-2026-10-30.md`, `protocol.md` **[cap]** |
| Packet 4 (leader) | Server sends to the sole player in a level; client sets a flag that packet 0 clears; **nothing reads the flag** | `protocol.md` **[bin][cap]** |
| Packet 6 (session) | Server sends `c(0)` on accept; client stores a value **nothing reads** | `protocol.md` **[bin][cap]** |
| Walk / run / jump / chat log | Speeds, run after 25 ticks, jump table, world ±4000, chat log rules | `client-behaviour.md` **[bin]** |
| Collision (G3D-1) | Radius 5, step height 30, slope/wall/probe rules | `collision.md` **[bin]** |
| Follow camera (G3D-2) | Distance 220, look height +80, turn ±5°/tick, pitch −0.15 rad | `camera.md` **[bin]** |
| Field of view | Library field **0.5**; opening ≈ 53.13° on the square window; exe does not set field | `camera.md` **[doc][bin][inf]** |
| Back clipping plane (E#500) | `SetBack(5000)` right after `CreateViewport` | `camera.md` **[bin]** (re-read 2026-11-13); App. E#500 settled row |
| TCP lab | Real client logs in, receives props and level text under Wine | `lab-2026-10-30.md` **[lab][cap]** |

Stale index lines that still said the far / back plane was open are corrected in the folder and root contents lists in the same PR as this note. The value at **draw time** with native retained-mode remains open (below).

## Open (February 2000)

| Item | Why open | What settles it |
|---|---|---|
| Live camera follow numbers + FOV/back at draw time | Wine RM stubs break camera frames | Loopback lab with native `d3drm.dll`; record follow geometry and viewport back plane while walking |
| Live collision | Same RM stub (`GetFaces`) | Same lab: walk into known faces; compare to `collision.md` |
| Peer UDP between two real clients | Needs working player meshes / positions | Two real clients + native `d3drm.dll` on loopback; scripted peers already match TCP relay rules |
| Admin client | None in the archives; admin protocol is server-side only | Archive find, or keep as server-only **[bin]** |
| Animation counter advance while standing | Not traced; freeze while idle is **[inf]** | Static re-read of prop-5 tick path, or lab with native RM |

## Beta (`GR3DV003`) — still static-only

| Item | Status |
|---|---|
| Network side matches `GR3DV002` ids/props/login layout | Settled **[bin]** (`beta3-genesis.md`) |
| Archived server rejects `GR3DV003` | Settled **[bin]** |
| Genesis3D DLL + art load | Open (E#504) |
| Physics / camera config defaults | Open (float constants not read) |
| UDP bytes vs `GR3DV002` | Open |

A lab needs the public Genesis3D 1.x SDK pieces the RAR omitted, plus a server that accepts `GR3DV003`. No such run is claimed here.

## Lab blockers (no new run this pass)

1. **Native Direct3D Retained Mode** for the February 2000 client under Wine (or a real Windows guest). Without it: no walk, no collision live check, no peer UDP with real clients, no draw-time back plane.
2. **Client + art archives** available to the lab worker (not in this checkout).
3. **Beta:** `genesis.dll` + BSP/actor/bitmaps; server accept for `GR3DV003`.

Loopback only. Placeholders for any host field. No public servers.

## Hypotheses from outside leads

Outside reimplementation write-ups are **leads only**. Nothing in this pass promotes an outside claim into a settled row. Confirm later against our binaries or a loopback lab, in our own words.

## Not in scope here

- Torque / 4.x–5.12 3D plug-in open items (E#501–E#503, avenue #4).
- v7 Worlds / Unity bridge notes under `protocol/v7-graal3d-*`.
- Changes to the Python reference server beyond what the notes already require.
