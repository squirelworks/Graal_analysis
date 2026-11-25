# 3D engine static reads: sky functions, name tags, protocol, loaders, input (2026-11-25)

Static reads of the 5.00r7 3D engine, used in place of 5.12's, whose engine
is packed inside its exe. Behaviour only; no addresses or code. Board rows:
T3D-057, T3D-063, T3D-065, T3D-072, T3D-080, T3D-098. **[bin 5.00r7]**

## Sky, fog and view functions (T3D-063)

- `setSunColors`, `setSkyBandColors`, `setFogColors` and `setSkyBandSizes`
  each take one list. They fill a client-side day and night keyframe table.
  They do not touch the ghosted Sky or Sun. This explains why the live 5.12
  probe saw no change (live-512-gs2-3d-probe-2026-11-25.md).
- `syncTimeOfDay` takes two numbers.
- `updateVisibleDistance` takes no argument. It re-reads
  `$pref::Video::visibleDistance` (`visibledistance3D`).
- There is no `updateFogDistance` function.
- `lightScene` does a full relight.

## Name tags (T3D-065)

`GuiShapeNameHud` has `nameMaxDistance` and `nameDistanceFade`. It reads the
GameObject fields `nickname`, `nickcolor`, `movetype` and `liquidtype`.
Whether it skips the control object is still open.

## Protocol check (T3D-072, T3D-080)

- The connect reject has separate texts for a protocol that is too old, a
  protocol that is too new, and a wrong game.
- The 3D protocol numbers in the held builds are 19, 21 and 24.

## Loaders (T3D-098)

- `.3ds`, `.dts` and `.dif` loaders are registered.
- The DIF and ForceField readers check their version numbers.
- 4.03r3 and 4.11 could not be read: each is a single packed client.

## Input (T3D-057)

The engine binds the `moveMap2D` move commands itself. `getAllowCursorOff`
is a callback into the client exe, not a GS2 function. The full list of
default binds is still open.

## The engine DLL as a whole (T3D-093 to T3D-104) **[bin 4.20r8, 5.00r7]**

Read from the 4.20r8 and 5.00r7 `Graal3DEngine.dll`. 5.12's engine is packed
inside its exe, and no separate 4.04r2 DLL was at hand for this read.

**Exports and loading (T3D-093).**

- 4.20r8 exports about 200 names, including the 76 `graal_set*` callback
  setters.
- 5.00r7 exports only five: load, run, end, resize and toggleFullScreen.
- Both import most of their runtime from `GraalEngine.dll`: strings, file
  streams, the GS2 variable and object types, and in 5.x the maths types
  too.
- The 5.00r7 exe loads `GRAAL3DENGINE.DLL` by name and resolves the load, run
  and end entry points. No version check between the exe and the DLL was
  found.

**Client-to-engine interface (T3D-094).** In 5.x the 78 `graal_set*` names
still exist but are not exported, so the callbacks must be passed in through
the load entry point. Compared with 4.20r8:

- added: ScreenCapture, ForceTextureTransparency, PushColorMatrix and
  PopColorMatrix;
- dropped: MakeGraalScreenshot and DrawGraphicsStretched.

**Torque version (T3D-095).** Neither DLL carries a TGE version banner.
4.20r8 still holds its build source paths; 5.00r7 holds none. Neither can
exec TorqueScript, and 5.00r7 has no SimDataBlockEvent, so no datablocks.

**Loaders (T3D-098).** The terrain loader requires 256x256 24-bit textures
("must be 256x256x24"). The DIF and ForceField readers check the file
version.

**Logs and files (T3D-099, T3D-100).** The engine logs to `console.log` in
the client folder and saves terrain under `levels3d/terrain/`.

**Threads and input (T3D-101, T3D-102).**

- The engine creates no threads and imports no DirectInput. It is
  single-threaded and ticked by the client.
- Input reaches it through the client's action names.

**Still open:**

- the full console function table with argument ranges (T3D-096);
- the NetEvent id order per protocol (T3D-097);
- how protocol-24 moves are packed.
