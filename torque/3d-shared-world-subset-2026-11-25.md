# The common 3D content subset across builds: one world, two protocol encodings (T3D-109)

Date: 2026-11-25. Lab of one world file served to protocol-24 and protocol-19 clients from our own 3D lab server, plus the class-table facts from [T3D-081](3d-object-classes-by-build-2026-11-25.md) and [T3D-004](3d-engines-5007-512-and-403-411-2026-11-25.md). Board row: [T3D-109](3d-capability-board.tsv).

## Runs

| Build | Protocol | This session | Result |
| --- | --- | --- | --- |
| 4.20r6 (5.12-class) | 24 | run (g3d420 route) | drew Sky + Sun-lit GameObject shape + Camera |
| 4.04r2 | 19 | run (native Linux, g3d404 route) | drew Sky + loaded a TGE Player (datablock + Player ghost); world shape not self-visible (route reason, below) |
| 5.00r7 | 24 | relied on prior note | class-equal to 5.12 ([T3D-004](3d-engines-5007-512-and-403-411-2026-11-25.md)), protocol 24 → same wire path and result as 4.20r6 |

Both clients were driven from **one and the same world file** (`sun`, `sky`, an `object` GameObject shape, `tgeplayershape`, Camera); the server chose what to send per client.

## The common drawable subset (as content)

**Sky + Sun lighting + a shape + a Camera.** That is what every build can show. Everything else — Items, StaticShapes, interiors, markers, triggers, particles, etc. — is 4.04r2-only and can't be sent to a 5.12-class client at all ([T3D-081](3d-object-classes-by-build-2026-11-25.md)).

## One byte stream, or a split at protocol 19/24?

**It splits at the 19/24 boundary — there is no single byte stream that serves all three.** Serving the one world file, the gserver produced two wire encodings, confirmed on the wire:

| | 4.20r6 / 5.12 family (protocol 24) | 4.04r2 (protocol 19) |
| --- | --- | --- |
| login detected as | protocol 24, 4.20r8, 5.x | protocol 19, 3.153, 4.04r2 |
| mission start | **2 phases** (Download Ghost Objects → Mission Lighting) | **3 phases** (Download Datablocks → Download Ghost Objects → Mission Lighting) |
| datablocks | none sent | a PlayerData datablock sent first (DataBlocksDone) before any ghost |
| ghosts sent | Sun, Sky, GameObject (shape), GameObject (player control), Camera | Sky, Player (stock TGE, from `tgeplayershape`) — no GameObject, no Sun ghost |
| the shape is a | GameObject | stock Player / TGE shape |
| sun lighting carried by | a Sun ghost | the Mission-Lighting phase (no Sun ghost) |

The same *content* is encoded with **different classes and different framing** per protocol. The gserver already branches on the protocol detected at login and emits the right encoding for each — which is what makes one world usable, but it is **one content design served through two protocol encodings, not one packet stream**.

## What each build drew

- **4.20r6 (protocol 24):** Sky gradient box, the red GameObject cube with Sun shading, through the Camera. All three common elements visibly rendered.
- **4.04r2 (protocol 19):** the Sky rendered, and the client loaded the PlayerData datablock and accepted the Player ghost (its octahedron), reaching Mission Lighting and the control object. The world shape was **not visible to the lone connected client**, for a route reason, not an engine one:
  - in Player-control mode the client views first-person from its own Player, so it never sees its own avatar;
  - in fly mode the gserver ghosts only a Camera, so there's nothing to look at;
  - the gserver does **not** ghost the world's GameObjects (nor a StaticShape or a second Player) to a protocol-19 client, so a single 4.04r2 client has no third-party shape to see.
  - That 4.04r2 *does* render a TGE Player shape is established from the g3d175 lab ([T3D-004](3d-engines-5007-512-and-403-411-2026-11-25.md) context). This run re-confirms the loading path; the missing visible shape is the single-client / server-emit limit.

## Bottom line / for a server

- **Common drawable content:** Sky + Sun lighting + a shape + a Camera.
- **Wire:** no single byte stream — it splits cleanly at protocol 19 vs 24. Protocol 19 = TGE datablocks + stock Player/Camera + 3-phase start; protocol 24 = GameObject + Sun ghost + 2-phase start. One authored world, two server-side encodings (which the gserver already does by detecting the client's protocol).
- **Caveat:** a shape is directly visible to a lone protocol-24 client (as a GameObject); for a lone protocol-19 client the only shape is its own first-person avatar, so to show world shapes to 4.04r2 the server would have to ghost them as stock Players/StaticShapes (which it doesn't today). The *content* is common; the *visible-to-one-client* result differs by how each protocol carries a world shape.
