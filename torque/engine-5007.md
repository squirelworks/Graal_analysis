# GraalEngine.dll 5.0.0.7

Date: 2026-11-07. Static read of the decompile in the v5 export. Nothing was run. **[bin]**

The launcher's version resource is `5.0.0.7` ([launcher-5007.md](launcher-5007.md#what-the-decompile-is)). This DLL's decompile has no file-version string. Its source paths are under `F:\graallib\`. **[bin]**

## Graal's game

The DLL defines the Graal types. `TAdventure` has constructors and methods (`localToScreenY`, `getMouseLevelX`, `getMouseLevelY`). Also present: `TGraalVar`, `TScriptExecutionSpace`, `TShowImg` (Flash, gani, image, poly, shape, text), `TGraalAni` and its part, sound, sprite and step types, `TGraalUniverse`, `TPlayer`, `TServerPlayer`, `GuiGraalCtrl`, `GuiGraal3DCtrl`. **[bin]**

Level and cache magics in the string table: `GR-V1.00` through `GR-V1.05`, `Z3-V1.03`, `Z3-V1.04`. License paths: `license/license.graal`, `license/sig.graal`, `license/sig.graallib`, `license/sig.license`. The console log name is `graal4console.log`. FMOD is used by name (`Failed to open fmod audio`); the separate `fmod.dll` in this export is a packer stub ([stub-fmod-5007.md](stub-fmod-5007.md#what-the-decompile-is)). **[bin]**

No `G3D` login-token literal is in the string table. **[bin]**

## Torque that remains

Torque's GUI is compiled in. `GuiCanvas` methods are defined here (`setRenderFront`, `isCursorON`, `setCursorPos`, and others), along with `GuiControl`, `GuiScrollCtrl`, `GuiWindowCtrl`, `GuiControlProfile`, `GBitmap` and `MatrixF`. **[bin]**

Absent from this DLL: `SimObject`, `GameConnection`, `ActionMap`, `.dso`, `OpenGLDevice`, `ShapeBase`. `GameObject` appears only as the `graal_setCreateGraal3DGameObject` setter, not as a Torque class body. The 3D world is the other DLL ([g3d-5007.md](g3d-5007.md#torque-that-is-still-here)). **[bin]**

## Who registers the setters

`graal_engineInitialize` and 118 `graal_set*` functions are defined here. Each setter stores the function pointer it is given. The engine is the registration API. The launcher and `Graal3DEngine.dll` call the setters; they do not define them. **[bin]**

### Who calls the setters

| Who | What it does with `graal_set*` |
|---|---|
| This DLL | Defines all 118 setters and `graal_engineInitialize`. |
| Launcher | Resolves `graal_engineInitialize` and 95 setters by name. |
| `Graal3DEngine.dll` | Calls 78 setters, then calls `graal_engineInitialize`. |

Every name the launcher resolves, and every name the 3D DLL calls, is defined here. **[bin]**

Launcher only (Flash, external windows, login screens, microphone, starting 3D): `graal_setCallFlashPanelFunction`, `graal_setCreateFlashPanel`, `graal_setDeleteFlashPanel`, `graal_setGetFlashPanelVar`, `graal_setPlayFlashPanelMovie`, `graal_setSetFlashPanelClipping`, `graal_setSetFlashPanelFile`, `graal_setSetFlashPanelGraalVar`, `graal_setSetFlashPanelLooping`, `graal_setSetFlashPanelVar`, `graal_setSetFlashPanelVisible`, `graal_setStopFlashPanelMovie`, `graal_setExternalPlayerlistDelete`, `graal_setExternalPlayerlistUpdate`, `graal_setOpenExternalOptions`, `graal_setOpenExternalPlayerlist`, `graal_setOpenExternalProfile`, `graal_setOpenMessageBox`, `graal_setEndTilesDrawing`, `graal_setStartTilesDrawing`, `graal_setGetGraalApplicationActive`, `graal_setGetGraalIsFullscreen`, `graal_setGetMicroInfoRequired`, `graal_setOnServerListerConnect`, `graal_setOnServerLogin`, `graal_setReceiveServerText`, `graal_setSetGraalFullscreen`, `graal_setSetGraalLanguage`, `graal_setSetGraalStatusIcons`, `graal_setSetGraalTranslationURL`, `graal_setSetMicroIsActivated`, `graal_setSetMicroVolume`, `graal_setShowFileScanMessage`, `graal_setShowGraalWindow`, `graal_setShowSelectPathDialog`, `graal_setStartGraal3D`, `graal_setSwitchToSetupMode`. **[bin]**

3D DLL only: `graal_setConnectTo3DServer`, `graal_setCreateGraal3DGameObject`, `graal_setDeleteGraal3DLightInfo`, `graal_setFreeGraalTexture`, `graal_setGetAllowCursorOff`, `graal_setGetGraal3DTerrainHeight`, `graal_setGetGraalPlayerScriptObject`, `graal_setGetHardwareCursorVisible`, `graal_setIsOpenGLEnvironment`, `graal_setLogGraalMessage`, `graal_setOnGraalFileDownloaded`, `graal_setRemoveGraal3DConnection`, `graal_setRemoveGraal3DMissionGroup`, `graal_setSendGraal3DScriptEvent`, `graal_setSendGraal3DScriptEvents`, `graal_setSendGraal3DServerText`, `graal_setSetGraalFullScreenMode`, `graal_setSetGraalWindowLocked`, `graal_setSetGraalWindowMode`, `graal_setSetMinimumFrameTicks`. **[bin]**

Defined here and named by neither host in this export: `graal_setOpenExternalHistory`, `graal_setOpenExternalLogWindow`, `graal_setOpenExternalPM`. **[bin]**

Both hosts name the other 58 setters, the shared draw set: tiles (`graal_setDraw2DTile`, `graal_setDraw3DTile`, `graal_setClear2DTile`, `graal_setClear3DTile`, `graal_setCreateTilesBuffer`, `graal_setScrollTilesBuffer`, `graal_setDrawTilesOnScreen`, and the buffer size, delete and clip helpers), text and graphics, the 2D matrix (`graal_setPushGraal2DMatrix`, `graal_setPopGraal2DMatrix`, `graal_setGetGraal2DMatrix`, `graal_setIsGraal2DMatrixActivated`), colour matrices (`graal_setPushColorMatrix`, `graal_setPopColorMatrix`), panels, clipboard, and `graal_setHomeDirectory`, `graal_setOpenURL`, `graal_setOpenURL2`, `graal_setUpdateGraalFile`, `graal_setShutdownGraal`, `graal_setPrepareShutdownGraal`. **[bin]**
