# Windows 4.03r3 and 4.11: the Thinstall packages unpacked, and what changed around 4.04r2

Date: 2026-11-13. Evidence ID `BATCH1-THINSTALL-20261113` ([evidence index](../docs/evidence-index.tsv)). Static read only: no client was run, and nothing here was seen on the wire. Tags: **[bin]** read from the unpacked binaries, **[file]** read from shipped data files, **[inf]** inferred.

## The packages

The Windows 4.03r3 and 4.11 downloads are single `Graal4Setup.exe` files (copies of the official downloads, the same bytes as the 2006-01-12 and 2006-11-03 copies of the auto-updater). The 4.04r2 installer already in the archive is the same kind of file. All three are **Thinstall 2.x** packages: a small stub, then one archive that holds the Thinstall runtime and a virtual file system with the whole client. [bin]

Until now the only way into them was to start the package under Wine and copy the engine out of memory. They can now be unpacked without running anything, with [tools/thinstall-unpack](../tools/thinstall-unpack/):

1. The stub is emulated until it has unpacked the runtime into memory and jumps to it.
2. The runtime's start-up is emulated, with stubbed Windows calls, until it reaches the virtual program's entry point. Nothing past that point runs. The runtime has by then read and decompressed its file directory.
3. Each file is cut into 64 KiB blocks, each compressed on its own. Every block is decoded by calling the runtime's own block decoder in the emulator.

The unpacked files are exact: [bin]

- All nine RSA signatures in the three `license/` folders (`sig.graal` over `Graal4.exe`, `sig.graallib` over `GraalEngine.dll`, `sig.license` over `license.graal`) verify against the key in each build's engine.
- The 4.04r2 `GraalEngine.dll` has the same MD5 as the one unpacked earlier and listed in [`tools/gs1-table-scan/builds.tsv`](../tools/gs1-table-scan/builds.tsv).
- `g3dref.py` on the unpacked engines gives 4.03r3 `G3D09125`, 4.04r2 `G3D17026` and 4.11 `G3D26076`. These are the memory-image tokens, and 4.04r2's is the token seen on the wire ([token note](login-tokens-3x-7x.md#reading-the-token-from-a-file)).

| Build | Files | `Graal4.exe` FileVersion | `GraalEngine.dll` link date | `Graal3DEngine.dll` link date |
|---|---|---|---|---|
| 4.03r3 | 135 | 4.0.3.3 | 2006-01-06 | 2006-01-06 |
| 4.04r2 | 137 | 4.0.4.2 | 2006-03-03 | 2006-03-03 |
| 4.11 | 142 | 4.1.1.0 | 2006-09-15 | 2006-09-15 |

All three ship the same `license.graal`, `sig.license`, `fmod.dll` 3.7 and `ExeReplacer_temp.exe`. 4.11 adds `freetype6.dll` 2.1.10, `zlib1.dll` 1.2.3 and a TrueType font, `tempsitc.ttf`. Its install list (`graalv4_installfiles.txt`) also adds three GUI images and the tutorial gani `tutorial_touch.gani`. [file]

None of the other Windows installers in the archive (5.x, 6.x, the 2.x setups) starts with this packer's archive header. Graal 2.31 was also shipped as a Thinstall package, but the archive already holds it unpacked.

## Server messages the client handles

Read with [tools/switch-scan](../tools/switch-scan/). It reproduces the published sets for 2.05 and for 4.20r8 exactly. The 4.20r8 engine read here is the stock one, not the packet-logger copy. The full lists are in [`plo-handled-ids-by-build.tsv`](../version-profiles/plo-handled-ids-by-build.tsv). [bin]

| Build | Handled ids | Change |
|---|---|---|
| 4.03r3 | 98 | Same set as 4.04r2 |
| 4.04r2 | 98 | 100 is a case in the packet switch; 107 and 108 are not handled |
| 4.11 | 100 | Adds **107** (board change on a tile layer) and **108** (the probe that 4.11 answers with id 162). 100 and 108 are now tested before the switch, as in 4.20r8 |
| 4.20r8 | 101 | Adds **196** |

So the layered board change (107) and the 108/162 exchange first appear in 4.11, between March and September 2006, and 196 between September 2006 and January 2007. 4.03r3 and 4.04r2 handle exactly the same ids.

The prop parsers did not change. The four large prop switches (self, other players, NPC and the shared parser) have the same case sets in 4.03r3, 4.04r2, 4.11 and 4.20r8. This extends the 4.04r2/4.20r8 match in [v4x-clients.md](v4x-clients.md#prop-parsers) to 4.03r3 and 4.11. [bin]

## Login and identity

4.03r3 already carries everything the 4.x login identity needs: the `DigitalProductId` read, `UuidCreateSequential`/`UuidCreate` for the MAC address, and `GetVolumeInformationA` for the volume serial. All three builds also have the gen-5 cipher seed and multiplier. So the comma-separated machine identity after the password ([v4x-clients.md](v4x-clients.md#login-packet)) most likely starts with the first Windows 4.x build in the archive. The fields themselves were not re-traced in 4.03r3. [bin][inf]

The login host file is the same in all three builds. It names the 4.x login host on port 14900, then two fallback hosts. [file]

## What the engine gained

`GraalEngine.dll` exports 1,638 symbols in 4.03r3, 1,651 in 4.04r2, 1,961 in 4.11 and 2,009 in 4.20r8. The `graal_set…` callbacks, through which the Delphi launcher gives the engine its drawing and window functions, show where the work went. [bin]

- **4.03r3 to 4.04r2** adds two callbacks, `graal_setClear2DTile` and `graal_setGetDatablockProperties`. The engine strings add tile layers (`TTilesLayer`, `tilelayers`, `tilelayercount`, `layerindex`), so layered tiles are in the 4.04r2 engine before the client handles packet 107. They also add music status and tags (`getMusicStatus`, `getMusicTags`, `onMusicDataReceived`), `findnpcbyid`, `getimgpixel`, `isimgpixeltransparent`, `isimgrectangletransparent`, `savevarstoarray`/`loadvarsfromarray`, `isblocking`/`isblockingprojectiles`, `actionclientside`, `playlooped2`, the `particleeffectsenabled` and `weathereffectsenabled` options, and a file-select dialog for the 3D start script. `onKeyRepeat` is gone. [bin]
- **4.04r2 to 4.11** adds 21 callbacks and drops 7:
  - **A Flash panel.** Eleven callbacks create, size, show, fill and drive a Flash panel (`graal_setCreateFlashPanel`, `…SetFlashPanelFile`, `…PlayFlashPanelMovie`, `…GetFlashPanelVar`, `…SetFlashPanelGraalVar`, `…CallFlashPanelFunction` and so on). The 4.11 launcher hosts the Shockwave Flash ActiveX control (`IShockwaveFlash`, `EmbedMovie`, `AllowScriptAccess`, and the error "Error when loading Flash ActiveX control: found version …"). The 4.11 engine also has a table of SWF ActionScript action names (`gotoframe`, `waitforframe`, `pushdata`, `storeregister`, `declarefunction2`, `extends`, `instanceof`, `throw`, …). What the engine does with that table was not traced. [bin][inf]
  - **2D drawing.** It adds a 2D matrix stack (`graal_setPushGraal2DMatrix`, `…PopGraal2DMatrix`, `…IsGraal2DMatrixActivated`), `graal_setDrawLine2`, `graal_setDrawPolygonEx` and `graal_setIsOpenGLEnvironment`. It drops `graal_setDrawPolygon`, `graal_setDrawTriangleStrip` and the three `GraalRotation` callbacks. [bin]
  - **3D.** It adds `graal_setCreateGraal3DGameObject`, `…DeleteGraal3DLightInfo` and `…GetGraal3DTerrainHeight`, and drops `…GetDatablockProperties` and `…RemoveGraal3DDatablocks`. [bin]
  - **Script and UI words** that are new in the 4.11 engine: player rotation, stretch and zoom (`playerrotation`, `playerstretchx`, `playerstretchy`, `playerzoom`), `mouseyaw`/`mousepitch`, the global mouse buttons, drag and drop (`startdrag`, `onStartDrag`, `onStopDrag`), multibyte string helpers (`multibytelength`, `multibytesubstring`, …), `textshadow`, `truetypefonts`, `isbuddy`/`isignored`, `geturl2`, `togglequality`, and two new start-menu entries, `Adventure_startBilliard` and `Adventure_startFairyland`. Terrain detail (`enableterraindetails`) and the `getObjectAt…` picking calls are gone. [bin]
- **Obfuscated values.** 4.11 adds a small value holder that keeps a 4-byte value in a separately allocated block, XORed with a byte from its own generator. The generator steps with the gen-5 cipher's multiplier (`x = x * 0x08088405 + 1`), and the block size comes from that state as well. The multiplier constant appears 4 times in the 4.04r2 engine and 88 times in 4.11 (89 in 4.20r8), so the holder is inlined in many places. This adds to the random start-up allocations 4.x already uses against memory scanners ([v4x-clients.md](v4x-clients.md#what-these-clients-are)). Which game values use it was not traced. [bin][inf]

The GS1 command table did not change. [`gs1scan.py`](../tools/gs1-table-scan/) `x86` reads 191 commands in each of the three engines. [bin]

## The 3D engine became a library in 4.11

`Graal3DEngine.dll` exports three functions in 4.03r3 and 4.04r2 (`loadGraal3DEngine`, `runGraal3DEngine`, `endGraal3DEngine`). In 4.11 it exports 206, among them `resizeGraal3DWindow` and `toggleGraal3DFullScreen`, and it imports `freetype6.dll`. With the new 3D callbacks in the 2D engine, this reads as the 3D side moving from a separately started engine to a library that the 2D engine calls into. [bin][inf]

## The public 2.1.0.0, for comparison

The public Windows 2.1.0.0 (FileVersion 2.1.0.0, built 2001-11-13, token `GNW31101`) was read the same way. It is the exe in the 2001 auto-updater pack ([token catalogue](../client-internals/version-token-catalogue.md)). [bin]

- **66 server ids, bound 174**: 0–25, 27–49, 75, 100, 150–151, 153–156, 165–166, 168–174. This is the Graal 2002 ver10 set plus the six ids (2, 4, 17, 18, 154, 155) that ver7 to ver13 send to the default branch ([Graal 2002 note](../client-internals/graal2002-and-140-builds.md)). So the main-world release has the baddy, chest and horse handlers that the Graal 2002 world builds of the same weeks leave out.
- **168 GS1 commands.** That is one fewer than ver10. It has `play2`, `shoot` and `replacestring` but not `savelog`, which ver10 (shipped two days later) adds. None of the v22 additions are in it.

## Open points

- [ ] Compare the Batch-1 `2.1.0.0-win`, `4.03r3-win` and `4.11-win` uploads with the files read here, once they are on the analysis machine. Only the copies of the official downloads were read.
- [ ] Trace the 108 probe and the value that 4.11 answers in 162.
- [ ] Find which game values the 4.11 value holder protects.
- [ ] Find what the 4.11 engine does with the SWF action-name table.
