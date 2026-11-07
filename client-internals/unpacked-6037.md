# Unpacked Windows 6.037

Date: 2026-11-07. Static read of the Ghidra listing of `unpacked_Graal 6.0.3.7.exe` (the C listing and the HTML listing). Nothing was run. Tags: **[bin]**.

The packed executable of this version is `packed-6037.md`. That file is a Themida shell: no code section, and CyaSSL labels on bodies that do not implement the calls. This listing is not that shell. The code section is present, `quattro_lib` and `TSocket` are in it, and the GS2 switch is in it.

Unpacked 6.00r2 and 6.00r4 are `engine-600r2.md` and `engine-600r4.md`. Protocol for this generation stays in `protocol/v6x-clients.md`.

## What this file is

One native Windows GUI image. The version resource says product Graal, file description Graal, internal name Graal, original file name `Graal.exe`, company Linux Cyberjoueurs, copyright 2012. The file-version and product-version strings are `6.037`. The fixed version words are 6, 0, 3 and 7. The image timestamp is 16 November 2012, 18:05:43 UTC. A banner joins the compiler strings `Nov 16 2012` and `18:58:51`. **[bin]**

The code section holds `quattro_lib` (DES, JPEG 2000 / JasPer) and the play name `Quattro_Play`. The entry is the Visual C++ security-cookie setup. It is not the packer loop that clears a byte, mixes a block and breakpoints. **[bin]**

Packer residue remains: seven sections. The code, resources and imports have ordinary names. One name is blank, two names are eight letters, and one is `.SCY`. The export directory is still named `QPlay.exe`. The strings `qplay` and `qplay_debug` are also present. **[bin]**

CyaSSL in this image has real bodies: context allocation, free, and connect. PEM armour is present for certificates and for RSA, DSA and EC private keys. The program calls `CyaSSL_library_init`, asks for the SSLv3 client method, and on failure reports "Error when creating SSL context" (the stored characters begin with `@`, and the report starts at the second character). The linked `zlibVersion` returns `1.2.3`. **[bin]**

## One program

No Delphi launcher, no `GraalEngine.dll`, no `Graal3DEngine.dll`, and no SDL. `GraalEngine` and `QEngine` are names compared when a three-field script record is loaded, beside `getstats` and `receivetext`. They are not a second module. `ExeReplacer.exe` and `ExeReplacer_temp.exe` are still launched. The updater path also names `Graal6.exe`. **[bin]**

Drawing, GUI, script and the socket still split as in unpacked 6.00. Direct3D 9 is created from `d3d9.dll` (`Direct3DCreate9`, "Failed to create DirectX9 device", "DirectX9 capabilities:"). The frame is OpenGL ("Initialized OpenGL.", and a failure to set the pixel format). World passes include `Game_Draw`, `Game_Draw_GetDrawObjects`, `Game_Draw_Player`, `Game_Draw_Texts`, `Draw_Tiles`, `Draw_ShowImg` and `Draw_Particles`. Sound failure text is "Failed to open fmod audio". Video is optional FFMPEG (`avcodec-51.dll`, `avformat-51.dll`, `avutil-49.dll`, "Couldn't load the FFMPEG library") plus `TRTMPClient`. **[bin]**

## Connection

The game session is `TSocket`. Script events include `onConnectingToServer`, `onConnect`, `onConnectFailed`, `onServerLogin`, `onPlayerLogin`, `onServerListerConnect` and `onReceiveData`. Status text includes "Connecting to the login server..." and "Connecting to the game server...". Outgoing data that contains a newline is still "Illegal characters in the outgoing data". Incoming data can be "Received illegal data (1)" or "Received illegal data (2)". Winsock startup failure is "winsocket startup failed". **[bin]**

The cipher object is initialised with the gen-3/5 LCG seed in two slots, a key byte masked to seven bits, and 3 in the next field. `MRandomLCG` is registered. No eight-character `G3D` token, and no port number, is stored as plaintext. **[bin]**

The incoming game-message switch has exactly the 92 ids already listed for Linux 6.03r7. **[bin]** (`protocol/v6x-clients.md#server--client-ids-601-603`)

HTTP still sends `Connection: Keep-Alive` and `connection: keep-alive`. There is no `resolveHost` name. An SSL context is created separately from `TSocket`, with the SSLv3 client method. Callers of inflate pass the version text `1.2.5`, while `zlibVersion` returns `1.2.3`. **[bin]**

## GS2

The script switch runs cases through 242. It includes 54 and 121 and every case from 200 through 242. It has no case 48 or 49, and no case above 242. That is the same addition, and the same absence, as unpacked 6.00r2 and 6.00r4. **[bin]** (`protocol/gs2-client-vm.md#opcodes-added-after-4208`)

Case 54 drops two values and writes type tag 4. Case 121 requires two values: a string tag on either value takes the string helper, and otherwise the numbers are added. Case 234 sets type tag 4 and skips the next instruction. The fold pairing that produces 234–242 was not re-derived in this read. **[bin]**

A `.code` file shorter than eight bytes is rejected. A longer file is compared with `GRESCR01` (the stored characters are `AGRESCR01`, and the compare starts at the second character) and the CRC32 is taken over the bytes after those eight. **[bin]**

## GUI

`GuiGraalCtrl` is still the type the GUI walk drops. `GuiGraal3DCtrl` is not a string in this image. The shell looks up `GraalControl` and `GraalControl3D` as children of `GUIContainer`. `GuiTilesCtrl` is constructed, with `GuiControl` as the name beside it. **[bin]**

`horizSizing`, `vertSizing`, `minExtent`, `fontType`, `fillColor`, `makeFirstResponder` and `pushToBack` are absent. **[bin]**

`ChatBar` and `ChatBar3D` are both looked up. The shell scripts are `StartScript_Profiles`, `StartScript_GraalGui`, `StartScript_MessageBoxDialog`, `StartScript_SetupDialog`, `StartScript_SelectFileDialog` and `StartConnectMessage` ("Connecting to %s...", with a German line and a French line of the same shape). There is no `StartScript_FileScanDialog`. **[bin]**

`onMouseYawPitch` is still described as the mouse moving in 3D mode, with yaw. `levels3d` is still a content folder beside `levels/` and `translations/`. `graal3://` is still an option-list string. `MissionGroup` is not in this image. The 6.00 description of a builtin that changes the colour of the 3D terrain is not among these strings. The names `TilesBuffer_Draw3DArea` and `Use3DText` are present; their call sites were not read. **[bin]**

## Torque names that remain

No `GameConnection`, `TerrainBlock`, `Interior`, DTS, `SimObject`, `SimGroup`, `.mis`, `.ter`, `.dts`, `.dso`, Torque console, `TAdventure`, `graal_set`, `ShapeBase` or SDL. **[bin]**

The Torque control names that 6.00 still implements are still here (`GuiControlProfile`, `GuiWindowCtrl`, `GuiScrollCtrl`, `GuiMLTextCtrl`, and the show-image, PM, start-menu and account-password controls), each as a Graal control. **[bin]**

`new t2dImageMapDatablock(`, `new t2dAnimationDatablock(`, `new t2dStaticSprite(` and `new t2dTileLayer(` are text the `-printmap` path writes. The usage line is `-printmap datablockfile levelfile`. That writer is not a Torque module. **[bin]**

## Against unpacked 6.00

Shared with both June 2011 images: one `quattro_lib` program, OpenGL after a Direct3D 9 capability check, FMOD, FFMPEG 51/49, the `TServer*` set (player, NPC, level, link, weapon, bomb, carry, chest, horse, sign, leap, flying, extra), `TSocket`, the newline refusal, `GRESCR01` on `.code`, GS2 cases 54 and 121 and 200–242, no cases 48 or 49, no Torque field names, `GuiGraalCtrl` as the playfield type, `levels3d`, `graal3://`, `onMouseYawPitch`, `ExeReplacer.exe`, bzip2 1.0.4 (20 December 2006), JasPer inside `quattro_lib`, and `des.c` as the named crypto source under `quattro_lib`. Level packages are still `GRPKG001`. **[bin]**

| What changed | 6.037 | 6.00r2 and 6.00r4 |
|---|---|---|
| Version and date | `6.037`, fixed words 6.0.3.7, compiler banner 16 November 2012 18:58:51, image timestamp the same day at 18:05:43 UTC | 6.002 on 12 June 2011, and 6.004 on 26 June 2011 |
| `GuiTilesCtrl` | constructed | absent |
| Playfield object names | `GraalControl` and `GraalControl3D` on `GUIContainer`. No `GuiGraal3DCtrl` string | `GuiGraal3DCtrl` is a type beside `GuiGraalCtrl` |
| Chat control | `ChatBar` and `ChatBar3D` | `ChatBar` |
| `MissionGroup` | absent | a script object looked up by name |
| `resolveHost` | absent, as in 6.00r2 | present only in 6.00r4 |
| Keep-Alive | both header spellings, as in 6.00r4 | 6.00r2 does not have those two headers |
| `creationtime.dat` | present | absent in 6.00r2; the 6.03 Linux note already records the addition |
| Level magics, as strings | `GR-V1.03`, `GR-V1.04`, `GR-V1.05`. No `GR-V1.00` through `GR-V1.02`, and no `GLEVNW01` | `GR-V1.00` through `GR-V1.05` |
| zlib text | `zlibVersion` returns `1.2.3`; inflate callers pass `1.2.5` | not separated in the 6.00 notes |
| TLS | CyaSSL is called, SSLv3 client method | no CyaSSL name. 6.00r2 also names `rsa.c` and `sha1.c`; this image names `des.c` only, plus the PEM set |
| Incoming game ids | the 92-id Linux 6.03r7 set | not re-counted in the 6.00 engine notes |
| Version token | not plaintext | not claimed as a string in the 6.00 engine notes |
| File-scan dialog | no `StartScript_FileScanDialog` | 6.00 builds that dialog |
| `-printmap` | writes Torque 2D datablock and sprite text | not in the 6.00 engine notes |

**[bin]**

`truetype`, `type1` and a "Server List" title stay absent, as in 6.00r4. `1024x768` and `Tempus Sans ITC` are present. **[bin]**
