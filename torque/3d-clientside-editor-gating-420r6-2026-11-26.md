# The in-client 3D editors and script file-saves are gated off from a clientside weapon — editing/saving 3D content is server-side (T3D-020, Linux 4.20r6)

Date: 2026-11-26. Single-client lab on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route), software GL; a GS2 weapon tried to open the editors and write files, with a file trace. Observation only. Board row: [T3D-020](3d-capability-board.tsv). Same gating pattern as the screenshot/file-write no-ops in [3d-session-file-footprint](3d-session-file-footprint-420r6-2026-11-26.md). Typed editor member lists are in [gs2-3d-typed-surface-512](gs2-3d-typed-surface-512-2026-11-26.md).

## Headline

`WorldEditor`, `TerrainEditor` and `EditManager` **do not open from a clientside weapon**, and the generic script save function **writes nothing** — a **gated no-op**. Privileged file-writing/editing from a clientside weapon is disabled on our server; editing and saving 3D content is staff / NPC-server-side.

## What happened **[lab]**

A GS2 weapon referenced `WorldEditor` / `TerrainEditor` / `EditManager` (all registered as GuiControls) and called `savestring(…)`:

- **Referencing the editors did nothing** — no instance was created, no editor GUI appeared, and no error was logged.
- **`savestring` produced no file anywhere** and no error — a silent gated no-op, the same pattern as `makescreenshot2` (gated script capture, [3d-session-file-footprint](3d-session-file-footprint-420r6-2026-11-26.md)) and `setterrain` ([3d-terrain-water-sun-route](3d-terrain-water-sun-route-420r6-2026-11-26.md)).

So although the editor classes and the save builtins are present in the engine's typed surface ([gs2-3d-typed-surface-512](gs2-3d-typed-surface-512-2026-11-26.md)), a **clientside weapon cannot instantiate an editor or write a file** — the privileged paths are disabled for client scripts.

## For a server

You cannot drive the world/terrain editors or do script file-saves from a **clientside** weapon; editing and saving 3D content is a staff / NPC-server-side capability. A client script gets the editor class names and save builtins but they are inert from that context.

## Method caveat

Single client, loopback server, software GL. The result is a trace of a clientside weapon's attempts (reference + `savestring`) plus a file trace showing nothing written; it does not test a server-side / NPC-server or staff-privileged context, where these paths may be enabled. "Gated no-op" means disabled for a client script, not absent from the engine.
