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
