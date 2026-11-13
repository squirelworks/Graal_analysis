# Graal3D later beta (`GR3DV003`): the Genesis3D rebuild

Date: 2026-11-13

A second standalone Graal3D client turned up in the 2026-11-13 client hunt as "New Graal 3D Beta Version" (a RAR with one `Graal3D.exe`, 630,272 bytes). It logs in with `GR3DV003`. These notes compare it with the February 2000 client (`GR3DV002`, 605,184 bytes) described in the rest of this folder. Static reads only (imports, strings, the login builder, the packet and property dispatchers); the beta was not run.

## Summary

The beta keeps the network side of the February 2000 client and replaces the renderer. Direct3D Retained Mode and DelphiX `TDXDraw` are gone. The beta draws with **Genesis3D** (`genesis.dll`) and reads its world from a local Genesis3D BSP. This is why the exe asks for `genesis.dll` when it starts: the RAR ships only the exe, not the engine DLL or the art.

## What stays the same

- **Login.** The login line is built by the same code as in `GR3DV002`: `c(0)` + version + `str(account)` + `str(password)`. Only the version string changes (it is a global string constant in both builds).
- **Port and transport.** TCP 14901, the same frame and text codec, the same `noudp` / `fixedudpport` options and the "Don't use UDP for data packages" option text.
- **Server → client packet ids.** The receive switch is identical: it acts on ids 0, 1, 2, 3, 4, 5, 6, 8 and 100. Every other id goes to the default branch, as before.
- **Player property ids.** The props parser is a jump table over 0 to 51 in both builds, and the same ids reach a handler: 0 to 17, 50 and 51.
- **Version stamp.** Both exes carry the same Delphi linker stamp, so the PE header does not date the beta.

## What changes

| Area | February 2000 (`GR3DV002`) | Later beta (`GR3DV003`) |
|---|---|---|
| Renderer | Direct3D RM (`d3drm.dll`), DirectDraw, DelphiX `TDXDraw` | Genesis3D (`genesis.dll`, created with `geEngine_CreateWithVersion`); a driver and mode picker form (`DriversForm`, `DrvList`) |
| World | The server's packet 0 carries the level as `.x` mesh text; the client saves and loads it | Packet 0 only clears the "leader" flag and ignores the text. The world is a local BSP, `genvs.bsp`, loaded at start ("Loading starting level...", "Unable to load / create the starting level!") |
| Players | `.x` meshes (`body.x`, `head.x`, arm, hand and foot meshes) | A Genesis3D actor, `dema.act`, plus `shadow.bmp` / `shadowalpha.bmp` blob shadows. `body.x` and `head.x` remain only as config defaults |
| Level entities | none | Reads the BSP's entity set; the class names `MovingPlat` and `DeathMatchStart` appear |
| Collision | Per-face test on the RM mesh (see [collision.md](collision.md)) | Genesis3D world collision (`geWorld_Collision`, `geWorld_TestModelMove`) |
| Input | Keyboard (DelphiX) | DelphiX `TDXInput`: DirectInput keyboard and joystick, force feedback effects, `joyGetPosEx` |
| HUD art | `logo.bmp` | `font.bmp`, `chatbar.bmp`, `corona.bmp`, `corona_a.bmp` |
| `graal3dconfig.txt` | `serveraddr`, `serverport`, `accountname`, `password`, `fixedport`, `fixedudpport`, `noudp`, `bodyx`, `headx`, `bodytex`, `armcolor`, `shoecolor`, `handcolor`, `nickname` | The same keys plus `RUN_SPEED`, `WALK_SPEED`, `PLAYER_GROUND_FRICTION`, `PLAYER_AIR_FRICTION`, `PLAYER_GRAVITY`, `PLAYER_JUMP_THRUST`, `CAMERA_DISTANCE`, `CAMERA_PLAYERCENTERY`, `CAMERA_DISTANCEY` and `playerscale` |
| Default server | none built in | A built-in default host name (not reproduced here) |

`genvs.bsp`, `dema.act`, `MovingPlat` and `DeathMatchStart` match the names used by the sample level and actor of the public Genesis3D SDK demo. **[inf]** The beta looks like a port of the Graal3D client onto that demo's world and actor, with the movement and camera numbers moved into the config file for tuning.

## Does the archived server accept it?

No. The only Graal3D server we have (`GServer.exe` from `graal3d.7z`) sets a version level of 0, then 1 for `GR3DV001` and 2 for `GR3DV002`. A player login with a level below 2 gets packet 5 "You need at least Graal3D beta2 to play on this server." and is closed. `GR3DV003` therefore gets that text. No server that knows `GR3DV003` is in the archives. [reference-server/](reference-server/) mirrors the archived server and rejects it too ("Wrong client version.").

Since packet ids, props and the login layout did not change, a server that accepted `GR3DV003` as well as `GR3DV002` should be enough to log the beta in. It would no longer need to send level text, because the beta ignores it.

## Open points

- A lab run needs `genesis.dll` and the beta's art (`genvs.bsp`, `dema.act`, the bitmaps). None of them are in the RAR. The DLL from the public Genesis3D 1.x SDK may load if its version matches what `geEngine_CreateWithVersion` asks for; the art may also come from that SDK. Not tried.
- The new physics keys have no defaults recorded yet. They are read from the config at start; the built-in defaults are float constants that this note did not read.
- The beta's UDP datagram layout was not compared byte for byte with `GR3DV002`.
