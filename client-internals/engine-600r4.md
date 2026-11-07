# Windows 6.00r4: the same Quattro engine, two weeks later

Date: 2026-11-07. Static read of the unpacked `GraalSetup` export whose version resource says product Graal, product version 6.004, company Linux Cyberjoueurs. The image carries the compiler date 26 June 2011 and the time 18:32:49. Nothing was run. Tags: **[bin]**.

This is the same program as `engine-600r2.md` (12 June 2011, product version 6.002). The decompiles are not the same file. What follows is the shared shape, then the differences that show up in this image.

## What the export is

One native Windows executable, source tree `quattro_lib`, play name `Quattro_Play`, `ExeReplacer.exe` still launched for packages. The dump still ends in the packer's dword loop; that loop is not the engine. **[bin]**

## Same engine as 6.00r2

No Torque 3D. No `GameConnection`, `TerrainBlock`, `Interior`, DTS, `SimObject`, mission or terrain files, Torque console or SDL. **[bin]**

Drawing, GUI, script and the network client split the same way. Direct3D 9 is created from `d3d9.dll` for adapter capabilities (`TWindow` reports them). The frame is OpenGL (`TWindowOpenGL::setScreenMode`, "Initialized OpenGL.", ARB shaders, `.vert` / `.frag`). World passes are `Game_Draw`, `Game_Draw_GetDrawObjects`, `Game_Draw_Player`, `Game_Draw_Texts`, then `Draw_Tiles`, `Draw_ShowImg`, `Draw_Particles`. `RenderGUI` and a `Draw_*` routine per control follow. Sound is FMOD. Video is optional FFMPEG (`avcodec-51` and the matching format and util libraries) plus `TRTMPClient`. **[bin]**

The shell is GS2: `StartScript_GraalGui` and the profile, connect, message-box, setup and file dialogs. `ChatBar` is the chat control name. World script types are the `TServer*` set (player, NPC, level, link, weapon, bomb, carry, chest, horse, sign, leap, flying, extra), plus `TBaddy`, `TGaniObject` and `TGraalAni`. Values are `TGraalVar`. The game connection is `TSocket`, with `onServerListerConnect`, `onConnectingToServer` and the login-server status text. Outgoing newlines are still "Illegal characters in the outgoing data". **[bin]**

`GuiGraal3DCtrl` is handled in the GUI walk beside `GuiGraalCtrl`. `GuiTilesCtrl` is absent. Torque field names (`horizSizing`, `vertSizing`, `minExtent`, `fontType`, `fillColor`, `makeFirstResponder`, `pushToBack`) are absent. `MissionGroup` is a script-object name. `onMouseYawPitch` is still described as 3D-mode mouse movement. `levels3d` is still a content folder. `graal3://` is still only an option-list string. **[bin]**

JPEG 2000 is still JasPer inside `quattro_lib`. DES is still `quattro_lib` `des.c`. bzip2's banner is still 1.0.4. Level magics still run `GR-V1.00` through `GR-V1.05`. **[bin]**

## What changed in two weeks

- A script builtin `resolveHost` is registered, described as a DNS lookup that resolves the host name. 6.00r2 has no such name. **[bin]**
- The HTTP layer carries the header `Connection: Keep-Alive` and the lowercase `connection: keep-alive`. 6.00r2 instead has a "connection could not be established" string and not those two headers. **[bin]**
- 6.00r2 names crypto sources `des.c`, `rsa.c` and `sha1.c`. This image names `des.c` only. That is the source-path strings, not a proof the RSA routines were deleted. **[bin]**
- 6.00r2 names font kinds `truetype` and `type1`, and has a "Server List" string beside the `1024x768` mode. This image keeps `1024x768` and has neither the font-kind names nor that title. **[bin]**
