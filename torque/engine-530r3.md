# Graal.exe 5.30r3 (file version 5.303)

Date: 2026-11-07. Static read of the unpacked executable in the v5 export. Nothing was run. **[bin]**

## What the decompile is

One executable. The version resource strings are file version `5.303`, original filename `Graal.exe`, copyright 2010. A compile-date string in the binary is `Oct 18 2010`. Source paths are `..\quattro_lib\` (crypto `sha1.c`, `des.c`, `rsa.c`, and jpeg2000). The named exports in the listing are zlib's (`crc32`, `deflate`, `inflate`, and the rest), not `graal_set`. **[bin]**

`graal_set` is absent. The Delphi launcher and the separate engine DLL of 5.0.0.7 are not in this file. **[bin]**

## Torque

Absent: `GuiCanvas`, `SimObject`, `GameConnection`, `GameObject`, `ShapeBase`, `ActionMap`, `.dso`, `TAdventure`, `TScriptExecutionSpace`, `TerrainChunk`, `datablock`, mission-phase logs. **[bin]**

Still present as GUI names: `GuiControl`, `GuiGraalCtrl`, `GuiGraal3DCtrl`, `GuiShowImgCtrl`, `GuiControlProfile`, `horizSizing`, `vertSizing`, `fillColor`, `makeFirstResponder`, `pushToBack`. `MissionGroup` is a string. `$pref::Graal::` keys are present, including `fixedudpport`. **[bin]**

## Graal's game

`TGraalVar`, `TShowImg`, `TGraalAni`, `TPlayer`, `TServerPlayer`, `TScriptFunction`, `TScriptUniverse`. Script methods are named `Adventure …`, including `Adventure getBuildTime`. Drawing is OpenGL (`Initialized OpenGL.` and `TWindowOpenGL::setScreenMode` messages). The string `Direct3DCreate9` is present. `DirectDraw` is absent. **[bin]**

Level magics `GR-V1.00` through `GR-V1.05` are present, as are `GRESCR` and `GRPKG` hits in the same way as 5.31. FMOD is still named (`Failed to open fmod audio`). **[bin]**

## Differences from 5.31r4

The two unpacked exes are the same program a few months apart, not copies. Only this build logs that Graal has been activated, names a quit-dialog start script, and lists the extensions zip, gpak, app, nw, graal, gmap and gxml. Its compile banner is 18 October 2010. What only 5.31r4 has is in [engine-531r4.md](engine-531r4.md#differences-from-530r3). Both still have a separate `.gxml` string. **[bin]**

## Native window and object-message boundary

2026-11-15 addition: bounded instruction read of a retained reconstructed
5.30r3 image, with its reconstructed import table. Evidence ID
`WIN-530R3-WINDOW-20261115` in the [evidence index](../docs/evidence-index.tsv).
The protected original and reconstructed input were distinguished before this
read. Their unpacking lineage and original loader state are not authenticated
by this comparison. Nothing was executed. **[bin]**

A window method calls a registration helper. On its once-flag path, the helper
prepares a native window-class record containing a procedure pointer and calls
the slot named `RegisterClassA`. The window method computes a rectangle,
conditionally adjusts it for the selected style, calls the slot named
`CreateWindowExW` and stores the returned window handle in its object. It then
calls the file-drop acceptance slot with that handle and an enabled flag.
These are decoded call instructions and object stores, not just API-name
presence. **[bin]**

The registered procedure searches a window-object collection for the incoming
handle. A matching object receives the message and its parameters through an
object handler. An unmatched handle, or the ordinary unhandled-result path,
calls the slot named `DefWindowProcA`. A separate close-message path for an
object other than the distinguished window returns directly; the complete
lifecycle semantics and object handler were not traced. This is a concrete
handle-to-object dispatch boundary within this reconstructed program. **[bin]**

The reconstructed import names mix ANSI and Unicode variants. The instruction
read identifies calls through those slots; it does not independently verify
their original bindings or character-width behavior. No silent correction of
the API names is assumed. Two direct callers of the window method were
decoded, but their complete purposes and connection to startup remain open.
**[bin]**

This supports a native window implementation in the inspected image. It does
not connect the protected original's entry to engine initialization or the
play loop, establish the absence of dynamically loaded engine modules, or
prove that the reconstruction preserves original startup behavior. It does
not extend this method to 5.31r4, 6.x or another platform. **[inf]**

## Open points

- [x] ~~Read the inspected 5.30r3 native window creation and handle-to-object
  message boundary.~~ [Bounded finding](#native-window-and-object-message-boundary).
- [ ] Authenticate original-to-reconstructed lineage and connect the window
  method's callers to engine initialization and the play loop.
- [ ] Independently verify the reconstructed API bindings before specifying
  character-width behavior.
- [ ] Establish original startup and dynamic-module behavior through the
  coordinated isolated runtime route; static window code alone is insufficient.
