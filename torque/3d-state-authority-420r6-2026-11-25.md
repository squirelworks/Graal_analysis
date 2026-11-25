# Which 3D state is server-authoritative and what the client trusts from itself (T3D-111, Linux 4.20r6)

Date: 2026-11-25. Loopback lab of the Linux 4.20r6 client (5.12-class, protocol 24) against our own 3D lab server, 3D leg through a UDP relay (runs `auth420-*`; no movement input). Linux 4.20r6 is 3D-equal to Windows 4.20r8 ([T3D-004](3d-engines-5007-512-and-403-411-2026-11-25.md)). Board row: [T3D-111](3d-capability-board.tsv). Builds on [T3D-018](3d-client-events-420r6-2026-11-25.md) (client events / `g3dpos`), [T3D-027](3d-link-drop-420r6-2026-11-25.md) (self-report cadence), [T3D-090](3d-shape-textures-420r6-2026-11-25.md)/[T3D-091](3d-world-limits-420r6-2026-11-25.md) (ghost positions) and [T3D-109](3d-shared-world-subset-2026-11-25.md) (Sun ghost).

## Table **[lab]**

| State kind | Authority | Evidence |
| --- | --- | --- |
| Sky | server-authoritative | the server sends a `Sky` ghost every run; the client renders what it's given (its default gradient here, since face textures don't apply — [T3D-077](3d-texture-formats-420r6-2026-11-25.md)). No `sky` line → no Sky. |
| Sun / lighting | server-authoritative | **new, direct:** a world with a `sun` line sends a `Sun` ghost and the shape is brightly lit with per-face shading; the identical world with **no `sun` line sends no Sun ghost and the shape is near-black**. The client supplies no meaningful default light — it takes directional lighting from the Sun ghost. |
| Other-ghost (GameObject) positions | server-authoritative | GameObjects draw exactly where the server's create/update places them ([T3D-090](3d-shape-textures-420r6-2026-11-25.md)/[T3D-091](3d-world-limits-420r6-2026-11-25.md)); the client sends nothing about another ghost and never moves one. |
| Control-object (own player) position | client-trusts-self by default; server can override | the client continuously reports its own control-object state to the 3D server (~2.5 UDP updates/s, 107 over ~41 s, as in [T3D-027](3d-link-drop-420r6-2026-11-25.md)). With no input it reports the spawn position. The server can override via a script `triggerserver(…, "g3dpos", x, y, z)`, which moves the object server-side, ghosts it back, and makes the client ignore its own reports for ~2 s ([T3D-018](3d-client-events-420r6-2026-11-25.md)). Between overrides the client holds and trusts its own position; an override snaps it. |
| Physics / collision | mostly server-side here; not fully testable on this route | with no terrain and no movement keys the client runs no observable local physics — the control object sits at spawn and is drawn there. On the protocol-19 path the server runs the walk sim (plain walk, no gravity/collision, no terrain); the 5.12 client predicts its own camera motion. Gravity/collision couldn't be exercised. **[route limit: no terrain, no movement]** |
| Animation | not driven on this route | only static `.3ds` shapes; no sequence was sent, so whether sequence state is a server field or client-run was not observable. **[not testable here]** |

## What the client trusts from itself

- **Its own control-object position** (and the state it packs into its update): computed and held locally and **reported** to the server (the steady ~2.5/s UDP updates). With no input it trusts the spawn position and keeps reporting it; the server does not continuously correct it. The only time the client yields is an explicit `g3dpos` move, after which it ignores its own reports for ~2 s then resumes self-reporting.
- **Its own camera prediction** (protocol 24): the client moves/predicts its camera locally; the server sends the initial Camera and the client drives it.
- **Everything about other objects** (other ghosts' positions, the Sky, the Sun/lighting) it takes from the server and does not second-guess.

## Summary

- **Server-authoritative:** Sky, Sun/lighting, every other ghost's position and content, the existence and identity of the control object, and (on demand) the control object's position via `g3dpos`.
- **Client-trusts-self (reported, not corrected by default):** the client's own control-object position/state and its camera prediction.
- **Shared:** the control object — the server owns its creation and can assert its position, but the client owns it moment-to-moment and reports it back.
- **Not observable on this route:** local physics/collision (no terrain, no movement) and animation (no sequence sent).

## Limits

- A fresh `g3dpos` override run this session didn't produce an observable move (the script weapon's trigger rides the encrypted 3D UDP channel this route can't decode), so the override point rests on the earlier [T3D-018](3d-client-events-420r6-2026-11-25.md) evidence, not a new capture.
- No terrain and no movement on this route, so physics, collision and gravity are structurally untestable here; a terrain-capable server or a movement-driving harness would be needed.
