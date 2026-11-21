# Static reads for Appendix E (2026-11-20)

Date: 2026-11-20. Evidence: **[bin]** (a disassembler read of the real client executables on the
lab host B, with no client run). Only behaviour is given here. Covers App. E#1, E#6, E#215, E#321,
E#328, E#502, E#503 and E#602. It follows
[static-reads-appendix-e-2026-11-19.md](static-reads-appendix-e-2026-11-19.md).

Builds read: 1st Graal to 15th Graal and 1.1 to 1.1.9 (early Delphi builds), 1.21 (the file the
version profile names by digest), 1.32, 2.05 rev 2 `Graal.exe`, the 2.1 test 2 image, Windows 2.22
(`Graal_222.exe`), 2.31, every other Windows client exe held from 1.28 beta 2 to 6.00r4 for E#602,
the GS2 engine DLLs of 4.20 (linked January 2007), 5.00r7 and 5.12, the dumped 5.24r3 to 5.31r4
exes, 6.00r2 and 6.03r7, and a memory image of the Windows 4.04r2 3D plug-in.

## What drives the 2.22 tick (E#328)

- The step runs from the DelphiX timer component, which 2.22 creates in code when its main form
  starts, not from a form resource. That is why a scan of the form resources finds no timer.
- The creating code sets the interval to 50 ms and the maximum lag count to 10, and binds the
  component's timer event to the game step. Claim A's "resolution of 10" is this lag count; there
  is no multimedia timer.
- The component works from the application's idle event. Each time the application goes idle it
  reads `timeGetTime`; when 50 ms or more have passed since the last step it records the current
  time as the new start and calls the step once. It also tells the application it is not done
  idling, so the idle event comes round again at once.
- Because the start is reset to the current time rather than moved on by 50 ms, a late step is not
  made up: there is no catch-up, and late steps push every later step back. The step routine does
  not read the lag count the component passes it.
- So Claim B (idle handler behind a 50 ms gate) describes the mechanism, and Claim A's timer is the
  same component seen from its creation code. The window timer that 2.22 imports belongs to other
  timers, not to the step.
- 2.05 rev 2 creates the same component the same way, with interval 50 and lag 10, unless a start-up
  option is set, in which case the interval is 0 (no gate). The class is also in 1.39, the 2.1 test 2
  image and 2.31; their creation code was not read.

## Compiler of the early Delphi builds (E#1)

- 1st Graal, 3rd Graal to 15th Graal, 1.1 and 1.1.9 all keep the class self pointer 64 bytes before
  the class table. 2nd Graal, 1.3 beta, 1.28 beta 2, 1.31, 1.39 and 2.05 keep it 76 bytes before, as
  shipped Delphi 3 does.
- All of the early builds carry the `SysInit` unit, interface support (`TInterfacedObject`,
  `IUnknown`) and a package-information resource that lists their units. Those are Delphi 3
  features. Delphi 2 has no `SysInit` unit and no language interfaces.
- None of them carries the C++ start-up code or C++ runtime hooks that a C++Builder project links
  in. A C++Builder 1 project cannot be built without its C++ start-up, so C++Builder 1 is ruled out.
- So the builds come from a Delphi 3 generation compiler whose class table is 12 bytes shorter than
  the shipping Delphi 3's, with the "1983,97" runtime library. A pre-release Delphi 3 fits all of
  this. 2nd Graal was built with the shipping layout between them. Which pre-release it was cannot
  be named without that compiler's own library to compare against.
- The 1.21 profile's "Delphi 2 level" label rests on the same 64-byte offset; the read above says
  that offset does not mean Delphi 2.

## Client-to-server ids of 1.21 and 1.32 (E#6)

- Both builds have one send routine for the game connection. It writes the id as one character
  (id + 32) in front of the body and queues the line.
- In 1.21 every call to it passes the id as a constant, at 27 sites. The ids are 0 to 13 and 15 to
  26. There is no 14.
- In 1.32 every call passes a constant too, at 33 sites. The ids are 0 to 30, so 1.32 sends both 14
  and 22. Its 22 comes from a routine that first looks for a matching entry in a list, sends 29 if
  one is found and sends 22 otherwise. Its 14 is sent from a small routine whose body is a single
  id character supplied by the caller.
- 1.32 also has a second, shorter send routine for the peer (UDP) channel, called with 10 to 14 and
  16 to 20.
- So the 1.21 profile is right (no 14) and the 1.32 profile missed 22. No register-passed id exists
  in either build's main send routine, so the "floor" caveat does not apply to these two lists.
- The profile lists also leave out 1 to 9, which both builds send as constants through the same
  routine.

## The 2.31 window blacklist (E#321)

- The scan belongs to a third-party Delphi anti-debugging component on the main form. Its four
  switches (kill debuggers, stop execution, anti-procdump, kill monitors) are all set on in the
  form resource, and none of its two events is bound.
- For each top-level window it reads the title and the class name, pads the title to at least 20
  characters and looks for each list entry anywhere in it. The match is case-sensitive. The class
  name is read but not compared in this path.
- The list is stored scrambled; each entry is XORed with a stream from the Delphi random-number
  generator seeded with a fixed value. Decoded, it names 20 tools, two of them twice: ExeSpy, wxr95,
  Regmon, File Monitor, RegMonEx, Window Detective, DebugView, ResSpy, Advanced Registry Tracer,
  regsnap, MEMSPY, Memory Doctor, ProcDump32, Memory Editor, FrogsICE, SMU Winspector, Memory Dumper,
  MemoryMonitor, DeDe and OpenTrap. The list holds monitors, dumpers and decompilers of the time,
  not game trainers or speed hacks.
- On a match it posts a quit message to the matching window (the "kill monitors" switch) and, with
  "stop execution" on, ends the client at once. It sends nothing to the server.
- The server-driven window-title list (S→C 182, answered on 44, and 183) is a separate path in the
  receive dispatcher, as already recorded in [the 4.x client note](../protocol/v4x-clients.md).

## GS2-only names in the engines (E#215)

The engine DLLs of 4.20 (linked January 2007), 5.00r7 and 5.12, and the dumped 5.24r3, 5.24r4 and
5.30r3 exes, each hold all eight names as plain strings: `triggerserver`, `scheduleevent`, `findimg`,
`findweapon`, `md5`, `cancelevents`, `keydown2` and `onwall2`. 6.00r2 and 6.03r7 show only
`scheduleevent` and `md5` in plain text because their name strings are scrambled, so they were not
counted. The packed Windows 4.04r2 exe gives no plain names and was not read. So every name is in
the January 2007 4.20 engine; the earliest 4.x build that has each is still open for 4.04r2 and
4.11. What a client does with a missing name still needs the lab.

## `.mis` and `.dso` in the 4.04r2 3D plug-in (E#502, E#503)

- The plug-in's console function table keeps `eval`, `echo`, `schedule`, `activatePackage`,
  `findFirstFile`, `setLogMode`, `dumpConsoleClasses`, `getRealTime` and `strlen`, but has no `exec`
  and no `compile`. In the Torque base those two are how a script file (a `.cs`, a `.dso` or a `.mis`
  mission) is read from disk.
- No `.mis` literal exists in the image, and none of the base engine's "compiling", "loading
  compiled script" or "missing file" console messages does, though many other engine messages are
  kept.
- `.dso` and `.cs` appear only in the download filter already described in
  [404r2-resource-filter.md](../torque/404r2-resource-filter.md).
- So no script path loads a local mission or compiled script; the mission arrives over the network.
  `eval` keeps a compiler for strings, so the script compiler itself is present. Whether a file-reading
  routine for compiled code is still linked in but uncalled cannot be told from the stripped image.

## `Z3-V1.02` in the Graal clients (E#602)

Every Windows client exe held from 1st Graal to 6.00r4, including 1.39, 2.05 rev 2, the 2.1 tests,
2.17.1, 2.22 and 2.31, lists only `Z3-V1.03` and `Z3-V1.04` among its `Z3` magics. None holds
`Z3-V1.02`. (The 4.04r2, 5.12 and 6.03r7 exes held are packed or dumped without these strings.) So no
Graal client reads `.02`, and the 12-bit readers never meet it.
