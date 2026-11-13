# Windows 4.04r2: the five modules and what each one holds

Date: 2026-11-14. Tags: **[bin]** file on disk · **[cap]** raw mapped module image from a controlled load-only capture of the original packed client (no server, no login; see `../version-profiles/windows-404r2-teardown.md`) · **[inf]** inferred.

4.04r2 ships as one packed `Graal4.exe`. At run time the carrier maps four modules out of itself, and a separate updater sits beside it. The published notes describe the launcher/engine split for 4.2.0.8 and 5.0.0.7 (`../manual/10-torque.md`, `../torque/5007-engine.md`) and the 3D DLL interface (`../graal3d/torque-engine-4x.md`). This note gives the same picture for the 4.04r2 carrier itself, one module at a time.

| Module (as named in its own headers) | Built with | Header date | Size mapped | What it is |
|---|---|---|---|---|
| `Graal4.exe` carrier | MSVC linker 6.0, one section | 2003-07-03 | 3.9 MB on disk | Packed carrier. Its version resource matches the shell's (below). **[bin]** |
| Shell (`Graal.exe`) | Delphi (linker 2.25; the header date is Delphi's fixed 1992 stamp) | — | 1.0 MB | Delphi/VCL client UI. FileVersion `4.0.4.2`, ProductName `Graal`, company `Linux Cyberjoueur`, description "Graal Online client". **[cap]** |
| `GraalEngine.dll` | MSVC linker 6.0 | 2006-03-03 | 3.8 MB | Combined Graal/Torque-derived engine. Source root `K:\src\graalv4\`. **[cap]** |
| `Graal3DEngine.dll` | MSVC linker 6.0 | 2006-03-03 | 2.6 MB | Torque 3D engine. 3 exports: `loadGraal3DEngine`, `runGraal3DEngine`, `endGraal3DEngine`. **[cap]** |
| `fmod.dll` | MSVC linker 6.0, itself UPX-packed (`UPX0` section) | 2003-09-16 | 0.6 MB | FMOD 3.7 (Firelight). Built from a Firelight `PC\SRC` tree with `fmod/src`, `vorbis/lib` and `ogg/src` objects. 222 exports. **[cap]** |
| `ExeReplacer.exe` | MSVC linker 6.0, 4 sections | 2005-08-23 | 60 KB | Updater helper; imports only KERNEL32 and SHELL32. **[bin]** |

## GraalEngine.dll exports

The engine exports **1,651 named symbols**: **[cap]**
- 980 C++ methods
- 443 C++ constructors, destructors and operators
- 228 plain C names

The C++ exports belong to 52 classes. Grouped:
- **Torque GUI and math:** `GuiControl` (102), `GuiCanvas` (56), `GBitmap` (41), `MatrixF` (35), `Stream` (33), `PlaneF`, `QuatF`, `Point3F`, `Box3F`, `GPalette`, `RectI`, `ColorI`, `FileStream`, `MemStream`, `GuiBitmapCtrl`, `GuiControlProfile`, `MRandomLCG`, `MRandomGenerator`.
- **Graal script and world:** `TGraalVar` (86), `TAdventure` (30), `TGraalClientVar` (14), `TGraalVarProperty`, `TDoubleArrayVar`.
- **Graal containers and strings:** `TJStringList`, `JString`, `THashList`, `TList`, `TStream`.

**[cap]** This export surface is what `Graal3DEngine.dll` links against. The published 4.x note counts 623 imports from the engine (`../graal3d/torque-engine-4x.md`). **[inf]**

The 228 plain exports include:
- **HawkVoice, compiled in.** 17 `_hvdi*` functions (VOX, AGC, codec selection, packet encode/decode, mixing) and 8 `_hcrypt*` functions (key, salt, packet and stream encrypt/decrypt). In 4.04r2, voice packaging is part of `GraalEngine.dll`, not a separate `hvdi.dll` as described for later clients in `sound-and-music.md`. **[cap]**
- **The launcher interface.** `graal_engineInitialize` and 100 `graal_set*` exports. The 5.0.0.7 launcher is published as resolving 95 of these names. **[cap]**
- **Direct entry points.** Examples are `connectToGraalServer`, `getGraalLoginInfo`, `getGraalMicroInputDevices`, `getGraalMicroGain`, `getGraalScriptFunctions`, `decryptGraalMemoryDES`, and the drawing-panel and tile-buffer setters. **[cap]**

## Source areas visible in the engines

- **GraalEngine.dll:**
  - 79 embedded source paths under a `lib/crypto` tree, the crypto layer already identified as libtomcrypt in `../protocol/v4x-clients.md`.
  - JasPer JPEG 2000 paths (`jpc`, `base`, `jp2`, `ras`, `pnm`, `mif`).
  - 242 MSVC RTTI class names. **[cap]**
- **Graal3DEngine.dll:**
  - Torque source paths under `engine/interior`, `engine/core`, `engine/sim`, `engine/terrain`, `engine/console`, `engine/sceneGraph`, `engine/dgl`, `engine/ts`, `engine/platformWin32`, `game/net`, `game/fx` and `editor`.
  - 338 MSVC RTTI class names. **[cap]**

## Notes on dating

The engine DLLs' header dates (March 2006) are almost three years later than the carrier's (July 2003). FMOD's header date (September 2003) sits between them. So the 4.04r2 carrier in this archive holds engines built long after the carrier stub itself. Whether that reflects a re-pack of the same release, or a later 4.04r2 build, is not established. **[inf]**

## How this was checked

Static read with a small PE reader (headers, export tables, version resources, embedded source-path strings, MSVC RTTI names). Inputs: the original packed carrier, the updater beside it, and the raw mapped images of the carrier's four modules from an earlier controlled load-only capture (no server, no login). Header values are as found in the mapped images. Nothing was run for this note.

## Still open

- **Engine date vs release date.** Date the 4.04r2 release independently (installer, update server or archive dates) to decide between the two readings above.
- **RTTI class map.** Map the 242 and 338 RTTI class names onto the published Torque class lists, separating stock TGE classes from Graal additions.
- **Shell forms.** Identify the Delphi shell's forms and event handlers from its own resources. This read covered only the shell's version resource.
