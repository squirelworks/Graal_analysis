# Torque surface the Mac v3 client references

Image: Mac PowerPC `Graal`, Ghidra project `MacGraal_v304`. A name is “referenced” when a code instruction points at that exact C string. Class strings were taken from `__TEXT`. Xref counts are from one pass over `MacGraal_v304` on 2026-11-08.

## Gui classes · high that the string exists

Controls, not profiles and not error sentences:

| class | code refs | notes |
| --- | --- | --- |
| `GuiCanvas` | 3 | methods registered in a client routine |
| `GuiGraalCtrl` | registered | methods in a client routine |
| `GuiGraal3DCtrl` | 1 | a client routine, about 500 bytes, no method pairs extracted |
| `GuiTSCtrl` | 1 | a client routine, 285 bytes, no method pairs |
| `GuiControl` | 29 | base control. Two opened functions did not list methods |
| `GuiConsole` | 1 | same function as the big canvas registrar a client routine |

Also present as their own strings. No per-class method list was extracted, so they are registered names, not walked call sites. Confidence high on the string, medium that each has a `ConcreteClassRep`:

`GuiArrayCtrl`, `GuiAviBitmapCtrl`, `GuiBackgroundCtrl`, `GuiBitmapBorderCtrl`, `GuiBitmapButtonCtrl`, `GuiBitmapCtrl`, `GuiBorderButtonCtrl`, `GuiBubbleTextCtrl`, `GuiButtonBaseCtrl`, `GuiButtonCtrl`, `GuiCheckBoxCtrl`, `GuiChunkedBitmapCtrl`, `GuiClockHud`, `GuiConsoleEditCtrl`, `GuiConsoleTextCtrl`, `GuiContextMenuCtrl`, `GuiCrossHairHud`, `GuiCursor`, `GuiDrawingPanel`, `GuiEditCtrl`, `GuiFadeinBitmapCtrl`, `GuiFilterCtrl`, `GuiFrameSetCtrl`, `GuiHealthBarHud`, `GuiInputCtrl`, `GuiInspector`, `GuiMLTextCtrl`, `GuiMLTextEditCtrl`, `GuiMapOverviewCtrl`, `GuiMenuBar`, `GuiMessageVectorCtrl`, `GuiMouseEventCtrl`, `GuiNoMouseCtrl`, `GuiPMCtrl`, `GuiPMEditCtrl`, `GuiPMHistoryCtrl`, `GuiPlayerView`, `GuiPopUpMenuCtrl`, `GuiProgressCtrl`, `GuiRadioCtrl`, `GuiScrollCtrl`, `GuiShapeNameHud`, `GuiShowImgCtrl`, `GuiSliderCtrl`, `GuiSpeedometerHud`, `GuiTerrPreviewCtrl`, `GuiTextCtrl`, `GuiTextEditCtrl`, `GuiTextEditSliderCtrl`, `GuiTextListCtrl`, `GuiTreeViewCtrl`, `GuiWindowCtrl`.

Profiles (`GuiControlProfile`, `GuiDefaultProfile`, `GuiTextProfile`, and the other `*Profile` strings) and the format strings `GuiControl::awaken…`, `GuiMessageVectorCtrl::attach…`, `GuiPlayerView::mountShape…` are data, not controls.

## Console methods that were read out of a registrar · high

`GuiCanvas` at a client routine: `renderFront`, `setContent`, `getContent`, `pushDialog`, `popDialog`, `popLayer`, `cursorOn`, `cursorOff`, `setCursor`, `hideCursor`, `showCursor`, `repaint`, `reset`, `isCursorOn`, `getCursorPos`, `setCursorPos`, `setFilterState`, `setFilterColor`, `setFilterMask`.

`GuiGraalCtrl` at a client routine: `moveUp`, `moveLeft`, `moveDown`, `moveRight`, `doA`, `doS`, `doD`, `doQ`, `doP`, `doM`, `doMicro`, `setChat`, `retrieveAccountFields`, `setNickName`, `setAccountName`, `setPassWord`, `setLanguage`, `openServerList`, `selectServer`, `selectServerCategory`, `startOfflineMode`, `connectToSelectedServer`, `serverDirectConnect`, `updateLoadLevelFields`, `loadLevel`, `updatePlayerProfile`, `updatePlayerMuted`, `updateMidiVolume`, `updateMp3Volume`, `updateRadioVolume`, `updateMicroActivationLevel`, `updateGraalOptions`.

Global console, a client routine: `lockMouse`, `setNetPort`, `createCanvas`, `saveJournal`, `playJournal`, `getVersionNumber`, `getVersionString`, `getCompileTimeString`, `getBuildString`, `getSimTime`, `getRealTime`.

`SimObject` / `SimSet`, a client routine: `save`, `setName`, `getName`, `getClassName`, `getId`, `getGroup`, `delete`, `schedule`, `dump`, `getType`, and `SimSet` `listObjects`, `add`, `remove`, `clear`, `getCount`, `getObject`, `isMember`, `bringToFront`, `pushToBack`. Bare names in that function include `nameToID`, `isObject`, `cancel`, `isEventPending`, `deleteDataBlocks`.

`NetConnection`, a client routine: `transmitPaths`, `clearPaths`, `getAddress`, `setSimulatedNetParams`, `getPing`, `getPacketLoss`, `checkMaxRate`, `connect`, `connectLocal`.

`GameConnection`, a client routine: `activateGhosting`, `resetGhosting`, `setControlObject`, `getControlObject`, `isAIControlled`, `play2D`, `play3D`, `chaseCam`, `setControlCameraFov`, `getControlCameraFov`, `setBlackOut`, `delete`, `startRecording`, `stopRecording`, `playDemo`, `isDemoPlaying`, `isDemoRecording`.

String helpers in a client routine, which also references `echo`, `exec`, and `eval`: `ExpandFilename`, `strcmp`, `stricmp`, `strlen`, `strstr`, `strpos`, `ltrim`, `rtrim`, `trim`, `stripChars`, `strlwr`, `strupr`. The word `echo` itself was not in the first bare-name slice. Confidence medium that this function is the `echo` builtin.

`ShapeBase` has 8 code refs. The two functions opened register `Camera` and `AdvancedCamera`, not a `ShapeBase::` method list. `Player\0` at an address has no code reference. `PlayerData` and `ShapeBaseData` are separate strings.

## Console lines the client evals · high

Passed to a client routine:

| line | site |
| --- | --- |
| `Canvas.setContent(MainMenuGui2D);` | a client routine |
| `Canvas.pushDialog(ServerListGui);` | a client routine |
| `Canvas.popDialog(ServerListGui);` | same |
| `Canvas.pushDialog(LoadLevelGui);` | string only, site not opened |
| `Canvas.pushDialog(PlayerProfileGui);` | string only |
| `start2D();` | a client routine |
| `resetCanvas();` | string only |

Prefs the options object binds, a client routine: `$pref::Graal::fixedport`, `fixedudpport`, `noudp`, `dontsavepasswords`, `automapping`, `nomassmessages`, `notoalls`, `dontloadlistheads`, `dontconnectlevels`, `limitnicknames`, `nicknamelimit`, `defaultfontsize`, and the `$pref::Audio::*` volume names. `$pref::Video::*` and `$pref::OpenGL::*` are strings. Their stores were not walked.

## What each job needs

| job | required | confidence |
| --- | --- | --- |
| window | `createCanvas`, `GuiCanvas` `setContent` / `repaint` / `reset`, `$pref::Video::resolution` | high |
| input | `GuiGraalCtrl` `moveUp` `moveLeft` `moveDown` `moveRight`, `GuiInputCtrl` as the control that exists for keys, `lockMouse`, cursor methods | high on the move methods, medium on `GuiInputCtrl` |
| 2D draw | `start2D();`, `GuiGraalCtrl`, `GuiBitmapCtrl`, `GuiShowImgCtrl` | high on `start2D` and `GuiGraalCtrl`. The bitmap controls are the blit surface by name |
| level load | `GuiGraalCtrl.loadLevel`, `updateLoadLevelFields`, `Canvas.pushDialog(LoadLevelGui)`, magic `GLEVNW01` in a client routine | high |
| player move | the four `move*` methods. Animation names `walk` and `walkslow` are stored in a client routine | high on the methods, low on a real step size |
| network | `NetConnection.connect` and `getAddress`. The Graal bytes are not these Torque calls. They are a client routine / a client routine in the v3 teardown | high |

## What can be stubbed

| piece | why |
| --- | --- |
| `GuiTSCtrl`, `GuiGraal3DCtrl`, `Camera`, `AdvancedCamera`, `GameConnection` ghosting and demo recording | 3D / demo path. The offline line is `start2D()` |
| `GuiPM*`, huds, `GuiInspector`, `GuiTreeViewCtrl`, `GuiTerrPreviewCtrl`, every `*Profile` | present as strings, not on the 2D login or walk path that was read |
| `ShapeBase` physics, `InteriorInstance`, `TerrainBlock`, `TerrainEditor` | engine strings. No Graal walk uses them |
| `transmitPaths`, `setSimulatedNetParams`, `getPing`, `getPacketLoss` | Torque net stats. The v3 line protocol does not call them |
| OpenGL prefs | video backend. A terminal grid does not read them |
