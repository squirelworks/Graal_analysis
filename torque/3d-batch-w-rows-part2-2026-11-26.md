# Batch W, third pass: 5.12 TorqueScript markers and more (2026-11-26)

Date: 2026-11-26. Follows [3d-batch-w-rows-2026-11-26.md](3d-batch-w-rows-2026-11-26.md), same lab
setup: headless Windows 10 lab clone on a VM-internal network with no other member, server and
clients in that guest over `<lan-host>`, **seihai-gserver main at `8800c2b`** (lobby 14900, TCP
14802, Graal3D UDP 14803). Captures stay in the owner-held lab kit. **[lab]**

## T3D-006 (5.12 half): does 5.12 run TorqueScript it is given?

Client: real 5.12 Windows (`G3D14097`). Two 60 s runs: markers local, and markers served.

Each marker `.cs` echoes a `MARKER006 <where>` line and writes a `marker006_<where>.txt` through a
`FileObject`, so a run that executed it would leave both a console line and a file.

- **Beside the client:** `main.cs`, `autoexec.cs`, `prefs.cs`, `client.cs`, `marker006.cs`,
  `main.cs.dso` and `marker006.dso` (placeholder bytes, since there is no compiler to make a real
  `.dso`), and `marker006.mis` (a MissionGroup stub plus an echo).
- **Under `levels3d\`:** `main.cs`, `mission.cs`, `marker006.cs`, `marker006.dso`,
  `marker006.mis`, `lab.mis`.
- **Served:** `marker006srv.cs`, `.mis` and `.dso` in the server's file folder, named as `object`
  shapes in the 3D world. A `weapon3d` probe also called `exec(...)` on three paths, `eval(...)`,
  `loadMission(...)`, and `isfile()` on two marker paths.

File trace: NTFS last-access tracking turned on in the guest, with every marker's access time preset
to a fixed old date, plus a file-system watcher over the whole system drive for each run.

| What | Result |
|---|---|
| Console marker line, marker `.txt` anywhere | **none**, in either run |
| Files beside the client | access time set to the client's start second, the same as every other file there; all listed in `FILENAMECACHE.txt`. That is the start-up folder scan for the file-name cache; nothing touched them afterwards |
| Files under `levels3d\` | access time unchanged: **never opened** (listed in `FILENAMECACHE.txt` too) |
| Served `.cs`/`.mis`/`.dso` named as shapes | the three GameObjects were ghosted, but 5.12 **never requested** the files; it fetched the world's `.3ds` and sky files as usual |
| `exec`, `eval`, `loadMission` from `weapon3d` | "GraalScript: Function exec not found in script of Weapon …" (same for `eval` and `loadMission`); each returned 0 |
| `isfile()` on the marker paths | 0 for both, although the root file exists |

**Answer for 5.12: it runs no `.cs`, `.dso` or `.mis` it is given**, whether beside the client,
under `levels3d`, or named by the server. Local files are only indexed into the file-name cache,
served script names are not fetched as shapes, and GS2 has no `exec`, `eval` or `loadMission` to
reach them. This fits the static read that 5.12 ships no TorqueScript compiler. The 3.153 half
of T3D-006 (Tiger VM) stays open.

## T3D-071 (Windows half): 5.12 and 4.20r8 in one world

Clients: real 5.12 Windows (`G3D14097`) on GDI GL, and 4.20r8 Windows (`G3D20126`) on a local
32-bit Mesa `opengl32.dll` (llvmpipe), chosen to avoid the GDI near-terrain crash (T3D-079); the
world has no terrain anyway. World: sky, a red world cube, and a green textured `playershape` so
each player's object is visible; spawn 0 0 1, the second player on the ring point 2 units out.
Four runs, both launch orders.

- **Both link as protocol 24 in one world.** Neither client logged a ghost error, an unknown class
  or a drop, and each link held to the end of the run.
- **Each gets the other's `G3DPlayer_<acct>` ghost** once the other's 3D link is up (in one run:
  5.12's player reached 4.20r8 as ghost 6, 4.20r8's reached 5.12 as ghost 3).
- **Before the other's 3D link is up, it appears as a `G2DPlayer_<acct>` GameObject** (seen on
  4.20r8 while 5.12 was still at the lobby/TCP stage). That stand-in is deleted when the 3D link
  replaces it with the `G3DPlayer`.
- **What each draws:** 5.12 draws both player objects as the green textured cube at the right
  offsets. 4.20r8 draws both in the right places but **white** (untextured), its usual GameObject
  drawing (now seen under Mesa too), not a cross-build effect.
- So 5.12 and 4.20r8 share a world cleanly and differ only in texture drawing. The 4.20r6 and
  4.04r2 legs (Wine) and the 3.153 leg were not run in this pass.

## T3D-133, T3D-069, T3D-110: a 2D 5.24r4 and a 3D 5.12 in one world

Clients: real 5.24r4 Windows (`G3D15010`, 2D) in a second Win10 lab VM with its clock at 2012, and
real 5.12 Windows (3D) in the first, clock at 2007; both on the same VM-only network.
`serverflags.txt` holds `server.labflag=on` and `server.confflag=on`. The start level holds one
clientside level NPC that, every 4 s, reads `server.`/`serverr.labflag` into its chat, changes
head, body, colours, ani, nick and chat, fires `putexplosion2` and `triggeraction`, then reads the
flag again. Two runs; the server logged every TCP body and UDP datagram.

### T3D-133: why the server flag reads empty

- The server sends PLO_FLAGSET `server.labflag=on` and `server.confflag=on` over TCP to **both**
  clients at login (to 5.12 before it opens its 3D link).
- **The 2D 5.24r4 reads it empty too.** Its own level-NPC script reads `server.labflag` and
  `serverr.labflag` as empty, both 4 s and about 40 s after login.
- So **the gap is not the 3D plug-in**: the 2D client receives the FLAGSET and its GS2 still reads
  nothing. The cause is in how the flag is named or stored, not in 5.12's 3D side. The 5.12
  `weapon3d` reads `server.confflag` empty as before.
- 5.12 never runs the 2D level NPC's clientside script while in 3D, so a "pre-3D" read is not
  possible that way (it would need a 2D weapon, which guest accounts do not hold).

### T3D-069: 2D look props as seen from the 3D client

- Body (`body2.png`), ani (`sit`) and chat set by the 5.24r4 script reach the server as
  PLI_PLAYERPROPS and go to 5.12 as PLO_OTHERPLPROPS for its `G2DPlayer_<acct>` ghost (in one run
  the `sit` ani was not seen going out).
- **Head, colours and nick set by the script never leave 5.24r4** (it fetched `head2.png` but sent
  no head prop), so there is nothing for 5.12 to show.
- The 2D player is a `G2DPlayer_<acct>` GameObject ghost on 5.12, re-created when the 2D player
  relogs. A per-prop screenshot of the 3D view was not captured (window capture), so the visual
  half stays open.

### T3D-110: game logic across 2D and 3D

- The 5.24r4's `putexplosion2` and `triggeraction` go out over TCP (it also hurt itself, fetching
  `bomb.wav`/`hurt.gani` and sending a hurt prop).
- **The 3D 5.12 shows none of it**: 2D level NPCs are not ghosted to 3D (no GameObject for the
  NPC) and the explosion has no 3D effect. The server forwards this 2D traffic on TCP only.
- Flags behave as in T3D-133. 3D-to-2D weapon fire and 3D-side triggers were not exercised.
