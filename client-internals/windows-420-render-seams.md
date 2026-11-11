# Windows 4.20: two render entry points, and who owns scripts in v3 to v5

Static reading, November 2026. The first part is a new check on a loose Windows 4.20 engine core. The second part summarizes, from notes already published, which program owns which kind of script in the Windows v3 to v5 clients, so that the render result is not read as more than it is. Evidence `W420-RENDER-SEAMS-20261109`. **[bin]**

## The two render entry points

**[bin]** The input is a loose engine core recovered from an archive labelled 4.20r8, SHA-256 `828e9311c8bddc9324988cb458e30581bb87636cbffdd1874c32ca502a30d337`. It does not inherit the provenance of the packet-logger 4.20r8 build or of the 4.2.0.8 export in [torque/4208-launcher.md](../torque/4208-launcher.md).

- The **adventure** render entry returns without drawing when there is no adventure object. Otherwise it calls the adventure's paint.
- The **canvas** render entry returns without drawing when there is no canvas. Otherwise it asks the canvas for one frame, with its boolean option false.
- The setter for the ordinary drawing callback only stores the callback. Registering it does not draw anything.

These are small dispatch rules. They do not show what paint draws, the callback's argument layout, when the client is ready to draw at start-up, what happens if paint calls itself, or whether a null callback is safe once paint uses it. No client was run.

This fits the 4.04r2 tutorial run in [version-profiles/windows-404r2-teardown.md](../version-profiles/windows-404r2-teardown.md#instrumented-tutorial-run-r01): with an adventure object allocated, the shell kept ticking, but no periodic core update or render hook was seen.

## A test that follows from it

**[inf]** A reproduction can check the same separation with fake renderers and a recording drawing adapter, using its own interface rather than the original binary one:

1. With no adventure and no canvas, call each render entry once. Nothing is recorded.
2. Add a fake adventure only. The adventure entry records one paint; the canvas entry records nothing.
3. Add a fake canvas too. The canvas entry records one frame with option false and no adventure paint.
4. Register drawing adapter A, then B. Registering records nothing. One synthetic draw then goes to B. This last step is a design check for the reproduction; the original draw-call interface was not verified.

The test needs no archived assets, scripts, network or graphics device. It should not advance the simulation or run scripts, and the shell's roughly 50 ms timer should not be taken as the script or simulation clock.

## Who owns scripts in Windows v3 to v5

This is a reading of published notes, kept here so the render result above is placed correctly. **[inf]**

- **Windows 3.x** has no evidence of its own. The compiled TorqueScript menus and native GS1 in [protocol/v3x-clients.md](../protocol/v3x-clients.md) belong to Linux 3.04 and Mac 3.153. They do not say which Windows 3.x program loads which `.dso`, or in what order.
- **Windows 4.04r2** is a Delphi shell with a native C++ core and an optional native 3D module. The shell supplies the window, input and drawing adapters and external dialogs; the core owns game, file, network and script services. Loading the 3D module can replace the drawing adapters. TorqueScript in 4.04r2 is only partly resolved: one resource-miss filter excludes `.dso`, `.cs` and `.ter` (→ [torque/404r2-resource-filter.md](../torque/404r2-resource-filter.md)), which does not prove there is no local reader.
- **Windows 4.20r8** has positive GS2 execution machinery, a container reader and a native dispatcher (→ [protocol/gs2-client-vm.md](../protocol/gs2-client-vm.md)). That is separate from its Torque names and does not show a TorqueScript interpreter.
- **Windows 5.00r7** keeps the shell and core split, with GS2 services in the engine (→ [protocol/v5x-clients.md](../protocol/v5x-clients.md)). Cached scripts in a used install are not evidence of what shipped.
- **5.12 and later 5.x** are not one design. 5.12 is a Delphi launcher plus an engine inside the 3D-named DLL; 5.24r3 and later are one native executable (→ [protocol/v5v6-windows-unpacked.md](../protocol/v5v6-windows-unpacked.md)).

The experiment that would settle the open parts is a per-build trace of start-up file opens and script-reader entry, with one small authored resource, in an isolated guest.
