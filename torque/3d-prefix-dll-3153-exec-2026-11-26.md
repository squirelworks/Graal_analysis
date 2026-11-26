# The "3 " prefix and a missing Graal3DEngine.dll on 4.20r8/5.00r7; 3.153 local .cs execution; batch-W blockers (2026-11-26)

Date: 2026-11-26. Last part of the batch-W labs (parts 1 and 2:
[3d-scoping-interiors-limits-512-2026-11-26.md](3d-scoping-interiors-limits-512-2026-11-26.md),
[3d-win10-sky-prefs-scripting-512-2026-11-26.md](3d-win10-sky-prefs-scripting-512-2026-11-26.md)).
Board rows: T3D-059, T3D-006; blockers recorded for T3D-072, T3D-066, T3D-089, T3D-067.
Captures stay in the owner-held lab kit. **[lab]**

## T3D-059: the "3 " prefix and a missing Graal3DEngine.dll (4.20r8, 5.00r7)

Headless Windows 10 lab VM, no network cable, clock held at 2007-11-19; our own
**seihai-gserver-v2 at `1d74282e`** and the lobby in the same guest on loopback. The lobby
server-warps each client to either "3 Lab 3D" or plain "Lab 3D" (same server, same level).
Clients: unpacked **5.00r7** (`G3D22067`, guest login; its licence-fallback login hosts mapped to
the in-guest lobby) and unpacked **4.20r8** (`G3D20126`). "Missing" = the same folder with
`Graal3DEngine.dll` deleted.

| Build | Server name | DLL | Result |
|---|---|---|---|
| 5.00r7 | "3 Lab 3D" | present | "Graal3D has been activated!"; **links as protocol 24** (server: 5.00r7, GameObject layer); shapes downloaded; 3D drawn |
| 5.00r7 | "Lab 3D" | present | **plays the level in 2D** (tiles, 2D weapons); no UDP link; the 3D GUI weapon fails with "type GuiGraal3DCtrl is not existing" |
| 5.00r7 | "3 Lab 3D" | **missing** | black window at "Connecting to the login server…" **forever**; never reaches the gserver; **no error, no crash** |
| 4.20r8 | "3 Lab 3D" | present | links as protocol 24 (drawn untextured); its weapon3d ran; ground, cube and sky drawn on GDI GL. **A second run crashed** after linking with an access violation in the 3D engine DLL, then the 3D link timed out |
| 4.20r8 | "Lab 3D" | present | **plays the level in 2D** (tiles, player, player list) |
| 4.20r8 | "3 Lab 3D" | **missing** | as 5.00r7: black window, console ends at "Connecting to the game server… Done.", never reaches the gserver, no error, no crash |

- **The "3 " prefix alone decides 2D or 3D** on 4.20r8 and 5.00r7, as on 5.12: with it the 3D
  engine starts and the Torque link opens; without it the same server and level play in 2D.
- **A missing `Graal3DEngine.dll` is never reported.** Both builds stall before the game server,
  and the server sees no login at all. A server cannot detect it; a player sees a black window.
- **4.20r8 on GDI software GL is unstable** (one clean 3D session, one access violation after
  linking); it was stable on Mesa.

## T3D-006: does 3.153 execute a local .cs?

The Mac 3.153 client in the Tiger VM, on a throwaway copy of the lab overlay, with the guest
network set so it could reach nothing; started from Terminal without the render shim.

- At startup it always logs "Compiling clientprefs3D.cs…" and "Compiling keysconfig3D.cs…".
- Statements were appended to those two files and to `main.cs`, plus a new `scripts/t3dmark.cs`:

| Marker | Result |
|---|---|
| `echo` lines | no marker line ever appeared |
| `exec()` of the new file | no "Compiling t3dmark.cs" line |
| `$pref` markers | inconclusive: the client ignored Quit, so prefs were never exported |
| `quit()` | the client kept running |

- No `.dso` was ever rewritten, including in the unmodified control run.
- **Still no evidence that 3.153 runs any `.cs` it didn't ship with**; served `.cs` files are never
  even requested (earlier live runs). Two causes remain: a silent compile failure, or the build
  announcing "Compiling" without running the file. A run with the render shim and a clean prefs
  export would settle it.

## Blocked rows (not run in batch W)

| Row | Why blocked | Needs |
|---|---|---|
| T3D-072 (mixed protocols 19/21/24) | On Windows 10 the packed 4.04r2 and 4.11 exit within 25 s with no window or login, and the unpacked 4.04r2 crashes at start (as in the 2026-11-14 and 2026-11-19 notes). The builds that run there (4.20r8, 5.00r7, 5.12) are all protocol 24 | Wine 4.04r2 and 4.11 in the Linux lab VM |
| T3D-066 (two 4.04r2) | same: 4.04r2 runs only under Wine | the Linux lab VM |
| T3D-089 (datablocks, clientCmds, missions on 3.153) | the 3.153 server stack (listserver, world and 3D server) hosted for the Tiger VM | a hosted 3.153 stack |
| T3D-067 (two 3.153) | as T3D-089, and no world 3.153 draws yet | T3D-089 first |
| T3D-135 / T3D-136 | our server has no second 3D level and no per-client ghosting (part 2) | server work |
