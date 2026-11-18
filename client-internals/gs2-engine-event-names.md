# GS2 engine event names by client build

Date: 2026-11-18. Static read of strings only; nothing was run. Tags as in `README.md`. Evidence ID `GS2-EVENTNAMES-20261118` (`docs/evidence-index.tsv`). Companion to [`../protocol/gs2-opcode-table.md`](../protocol/gs2-opcode-table.md).

## What this list is

Every literal string of the form `on` + capital letter + word that the engine image holds, for nine builds. These are the event names the engine passes to a script by name: GUI control callbacks (`onMouseDown`, `onSelect`), engine and network hooks (`onPlayerLogin`, `onReceiveData`), store and platform hooks on Android, and the packet-send hooks on 6.1.1.3. **[bin]**

What it is not:

- **Not the GS1-mask events.** `created`, `timeout`, `playerenters` and the rest of the `script_event` list are built at run time from the bare name (`client-internals/gs2-vm-from-engines.md#events`), so most of them never appear as an `on…` literal. `onCreated` shows up only where some code also spells it out. **[bin]**
- **Not proof of firing.** A literal can be dead text. Which call site fires each name needs a cross-reference read per event. **[inf]**
- **A floor for 7.12.43 and Android 2.2.** Those two images hold far fewer `on…` literals than their neighbours (40 and 36). They probably build or encode most names differently; the gap is not evidence that the events were removed. **[inf]**

## Counts

| Build | `on…` names |
| --- | ---: |
| 4.04r2 (`GraalEngine.dll`) | 76 |
| 4.20r8 (`GraalEngine.dll`) | 81 |
| 5.30r3 (unpacked) | 107 |
| 6.00r2 (unpacked) | 111 |
| 6.1.1.3 (unpacked) | 170 |
| Linux 6.03r7 x64 | 106 |
| Android Classic 1.8 (x86_64) | 157 |
| Android Classic 2.2 (x86_64) | 36 |
| 7.12.43 (`Graal3DEngine.dll`) | 40 |

221 distinct names across the nine. **[bin]**

## What changes between builds

- **6.1.1.3 adds 55 `onSend…` hooks**, one per outgoing message (`onSendPlayerProperties`, `onSendWantClassScript`, `onSendTriggerAction` and so on); that is the same count as the fifty-five script-filled send slots in [`../protocol/v6113-pli.md`](../protocol/v6113-pli.md). Android 1.8 has 51 of them plus `onSendNPCProperties`, which 6.1.1.3 lacks. Linux 6.03r7 and 6.00r2 have none. These are the hooks a connector script uses to take over the client's own sends, which bears on `#397`. **[bin]**
- **6.1.1.3 adds the queue and connection names** `onCreated`, `onAllRCChat`, `onReconnect`, `onDisconnected`, `onServerWarp` and `onFileRequests`. Android 1.8 has all six; Android 2.2 and 7.12.43 show `onCreated` and `onAllRCChat`. **[bin]**
- **4.04r2 and 4.20r8 have names later builds drop:** `onInitialize`, `onKeyPress`, `onLoad`, `onUnload`, and (4.20r8 only) `onGraal3DConnectionEstablished`. `onOpenHelpWindow`, `onOpenLogWindow` and `onOpenOptionsWindow` last until 6.00r2. **[bin]**
- **5.30r3 adds the Flash-style and connection names** `onRollOver`, `onRollOut`, `onCall`, `onConnect`, `onBind`, `onHandShake`, `onMetaData`, `onAnimationStart` and the style/responder group. **[bin]**
- **Android-only:** store and platform hooks (`onGooglePlayPurchase`, `onAmazon…`, `onMobiroo…`, `onDeviceBackButton`, `onAppEnterBackground`, `onVideoLoaded`, `onScriptFunctionCall`, `onStartedWithURL`). **[bin]**
- **7.12.43-only:** Unity-era hooks (`onUpdate`, `onFixedUpdate`, `onLevel3DEnter`, `onLevel3DLoaded`, `onQuattro3DLoaded`, `onChangeMode3D`, `onServerSetPlayerX/Y/Z`, the push-notification group, `onDeeplink`, `onLowMemory`). **[bin]**

## How events reach a script

Recorded elsewhere, gathered here so the table has its context. **[bin]**

- An event is a call of the function of that name. Segment 2 lists the functions; a name with `public.` is also callable from other scripts (`protocol/gs2-client-vm.md`).
- Segment 1 is the GS1 event mask; joined classes OR theirs in. Official bodies always write 0 (`protocol/gs2-seg1-event-mask-2026-11-16.md`).
- 4.2.0.8 drops an event once the list passes 9,999 (`Events number overrun`); the installed 5.00 queue has a 1,000-action gate (`client-internals/windows-500-event-queue.md`); Android 1.8 refuses new events at 1,000 and puts `istimeout`, `created` and `initialized` at the front (`protocol/gs2-android-classic-18.md`). Linux 6.03r7 keeps the same `Events number overrun` text. **[bin]**
- `waitfor` registers a catch for a named event; a leading `on` is stripped (`manual/08-scripting/03-gs2-language.md`).

## The table

`x` means the image holds that literal; `·` means it does not.

| Event | 4.04r2 | 4.20r8 | 5.30r3 | 6.00r2 | 6.1.1.3 | Linux 6.03r7 | Android 1.8 | Android 2.2 | 7.12.43 |
| --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| `onAction` | x | x | x | x | x | x | x | · | · |
| `onAdd` | x | x | x | x | x | x | x | · | · |
| `onAllRCChat` | · | · | · | · | x | · | x | x | x |
| `onAmazonHistory` | · | · | · | · | · | · | x | x | · |
| `onAmazonHistoryDone` | · | · | · | · | · | · | x | x | · |
| `onAmazonPurchase` | · | · | · | · | · | · | x | x | · |
| `onAmazonUser` | · | · | · | · | · | · | x | x | · |
| `onAnimationEnd` | · | · | x | x | x | x | · | · | · |
| `onAnimationFinished` | · | · | x | x | x | x | x | · | · |
| `onAnimationStart` | · | · | x | x | x | x | · | · | · |
| `onAppActive` | · | · | · | · | · | · | · | · | x |
| `onAppEnterBackground` | · | · | · | · | · | · | x | x | x |
| `onAppInactive` | · | · | · | · | · | · | · | · | x |
| `onAppLeaveBackground` | · | · | · | · | · | · | x | x | x |
| `onAppResume` | · | · | · | · | · | · | · | x | · |
| `onAssetBundleDownloaded` | · | · | · | · | · | · | · | · | x |
| `onBecomeFirstResponder` | · | · | x | x | x | x | x | · | · |
| `onBind` | · | · | x | x | x | x | x | · | · |
| `onBindFailed` | · | · | x | x | x | x | x | · | · |
| `onCall` | · | · | x | x | x | x | · | · | · |
| `onCancel` | x | x | x | x | x | x | x | · | · |
| `onChangeMode3D` | · | · | · | · | · | · | · | · | x |
| `onClassesDownloaded` | · | · | x | x | x | x | x | x | x |
| `onClassLoaded` | · | · | x | x | x | x | x | x | x |
| `onClose` | · | · | x | x | x | x | x | x | x |
| `onCloseQuery` | x | x | x | x | x | x | · | · | · |
| `onConnect` | · | · | x | x | x | x | x | · | · |
| `onConnectFailed` | · | · | x | x | x | x | x | · | · |
| `onConnectingToServer` | · | · | x | x | x | x | · | · | · |
| `onControlKeyDown` | · | · | · | x | · | x | x | · | · |
| `onControlKeyUp` | · | · | · | x | x | x | x | · | · |
| `onCreated` | · | · | · | · | x | · | x | x | x |
| `onCursorLineChanged` | x | x | x | x | x | x | x | · | · |
| `onData` | x | x | · | · | x | · | x | · | · |
| `onDblClick` | x | x | x | x | x | x | x | · | · |
| `onDeeplink` | · | · | · | · | · | · | · | · | x |
| `onDefaultStyleChanges` | · | · | x | x | x | x | x | · | · |
| `onDeleteKey` | x | x | x | x | x | x | x | · | · |
| `onDeselect` | x | x | x | x | x | x | · | · | · |
| `onDeviceBackButton` | · | · | · | · | · | · | x | x | · |
| `onDialogPop` | x | x | x | x | x | x | x | · | · |
| `onDialogPush` | x | x | x | x | x | x | x | · | · |
| `onDisconnected` | · | · | · | · | x | · | x | · | · |
| `onDropFiles` | · | · | x | x | x | x | x | · | · |
| `onEnterFrame` | x | x | x | x | x | x | · | · | · |
| `onExpand` | x | x | x | x | x | x | · | · | · |
| `onExternalStyleChanges` | · | · | · | · | x | x | x | · | · |
| `onFileChunkReceived` | x | x | x | x | x | x | x | · | · |
| `onFileDownloaded` | x | x | x | x | x | x | x | · | · |
| `onFileRequests` | · | · | · | · | x | · | x | · | · |
| `onFilesUploaded` | · | · | x | x | x | x | x | · | · |
| `onFirstResponderChanges` | · | · | x | x | x | x | x | · | · |
| `onFixedUpdate` | · | · | · | · | · | · | · | · | x |
| `onFold` | x | x | x | x | x | x | · | · | · |
| `onFolderLog` | x | x | x | x | x | x | x | · | · |
| `onGeneratedThumbnail` | · | · | x | x | x | x | · | · | · |
| `onGooglePlayInitialized` | · | · | · | · | · | · | x | x | · |
| `onGooglePlayPurchase` | · | · | · | · | · | · | x | x | · |
| `onGraal3DConnectionEstablished` | · | x | · | · | · | · | · | · | · |
| `onHandShake` | · | · | x | x | x | x | · | · | · |
| `onHide` | x | x | x | x | x | x | x | · | · |
| `onIconResized` | x | x | x | x | x | x | x | · | · |
| `onInitFrame` | · | · | x | x | x | x | x | x | x |
| `onInitialize` | x | x | · | · | · | · | · | · | · |
| `onKeyDown` | x | x | x | x | x | x | x | · | · |
| `onKeyEvent` | · | · | · | · | · | · | · | x | x |
| `onKeyPress` | x | x | · | · | · | · | · | · | · |
| `onKeyUp` | x | x | x | x | x | x | x | · | · |
| `onLevel3DEnter` | · | · | · | · | · | · | · | · | x |
| `onLevel3DLoaded` | · | · | · | · | · | · | · | · | x |
| `onLevelFileUpdated` | · | x | x | x | x | x | x | · | · |
| `onLoad` | x | x | · | · | · | · | · | · | · |
| `onLogMessage` | x | x | x | x | x | x | · | · | · |
| `onLoseFirstResponder` | · | · | x | x | x | x | x | · | · |
| `onLowMemory` | · | · | · | · | · | · | · | · | x |
| `onMapClick` | x | x | x | x | x | x | · | · | · |
| `onMetaData` | · | · | x | x | x | x | · | · | · |
| `onMobirooInAppItems` | · | · | · | · | · | · | x | x | · |
| `onMobirooPurchase` | · | · | · | · | · | · | x | x | · |
| `onMobirooPurchaseUpdate` | · | · | · | · | · | · | x | x | · |
| `onMobirooUser` | · | · | · | · | · | · | x | x | · |
| `onMouseDown` | x | x | x | x | x | x | x | x | x |
| `onMouseDragged` | x | x | x | x | x | x | x | x | x |
| `onMouseEnter` | x | x | x | x | x | x | x | x | x |
| `onMouseLeave` | x | x | · | · | x | x | x | x | x |
| `onMouseMove` | x | x | · | · | · | x | x | x | x |
| `onMouseOverCell` | · | x | x | x | x | x | x | · | · |
| `onMouseUp` | x | x | x | x | x | x | x | x | x |
| `onMouseWheelDown` | x | x | x | x | x | x | x | x | x |
| `onMouseWheelUp` | x | x | x | x | x | x | x | x | x |
| `onMouseYawPitch` | x | x | x | x | x | x | · | · | · |
| `onMove` | x | x | x | x | x | x | x | · | · |
| `onMusicDataReceived` | x | x | x | x | x | · | · | · | · |
| `onNewClient` | · | · | x | x | x | x | x | · | · |
| `onOpenHelpWindow` | x | x | x | x | · | · | · | · | · |
| `onOpenLogWindow` | x | x | x | x | · | · | · | · | · |
| `onOpenMenu` | x | x | x | x | x | x | x | · | · |
| `onOpenOptionsWindow` | x | x | x | x | · | · | · | · | · |
| `onOpenPlayerList` | · | · | x | x | · | · | · | · | · |
| `onOpenPlayerPositionWindow` | x | x | x | x | x | x | · | · | · |
| `onOpenProfileWindow` | · | · | x | x | x | x | x | · | · |
| `onOpenServerList` | x | x | x | x | x | x | x | · | · |
| `onPackagesDownloadComplete` | x | x | x | x | x | x | x | · | · |
| `onPackagesDownloaded` | x | x | x | x | x | x | x | · | · |
| `onPf` | · | · | x | x | x | · | · | · | · |
| `onPlayerChanges` | x | x | x | x | x | x | x | · | · |
| `onPlayerLanguageChanges` | · | · | x | x | x | x | x | · | · |
| `onPlayerLogin` | x | x | x | x | x | x | x | · | · |
| `onPlayerLogout` | x | x | x | x | x | x | x | · | · |
| `onPM` | x | x | x | x | x | x | · | · | · |
| `onPress` | x | x | x | x | x | x | · | · | · |
| `onPushNotification` | · | · | · | · | · | · | · | · | x |
| `onPushNotificationFireBase` | · | · | · | · | · | · | · | · | x |
| `onQuattro3DLoaded` | · | · | · | · | · | · | · | · | x |
| `onRCChat` | x | x | x | x | x | x | x | · | · |
| `onReceiveData` | x | x | x | x | x | x | x | · | · |
| `onReceiveDataPackage` | · | · | x | x | x | x | x | · | · |
| `onReceiveUDPData` | · | · | x | x | x | x | x | · | · |
| `onReconnect` | · | · | · | · | x | · | x | · | · |
| `onReflow` | x | x | x | x | x | x | x | · | · |
| `onRegisterPushNotifications` | · | · | · | · | · | · | · | · | x |
| `onRegisterPushNotificationsFireBase` | · | · | · | · | · | · | · | · | x |
| `onRelease` | x | x | x | x | x | x | · | · | · |
| `onReleaseSlider` | x | x | x | x | x | · | · | · | · |
| `onRemotePlayerChats` | x | x | · | x | x | · | x | · | · |
| `onRemove` | x | x | x | x | x | x | x | · | · |
| `onResize` | x | x | x | x | x | x | x | · | · |
| `onRightMouseDown` | x | x | x | x | x | x | x | x | x |
| `onRightMouseDragged` | x | x | x | x | x | x | x | x | x |
| `onRightMouseUp` | x | x | x | x | x | x | x | x | x |
| `onRightSelectTag` | · | · | x | x | x | x | x | · | · |
| `onRollOut` | · | · | x | x | x | x | · | · | · |
| `onRollOver` | · | · | x | x | x | x | · | · | · |
| `onRotationChanged` | · | · | · | · | · | · | · | · | x |
| `onScriptFunctionCall` | · | · | · | · | · | · | x | x | · |
| `onScrolled` | x | x | x | x | x | x | x | · | · |
| `onSelect` | x | x | x | x | x | x | x | · | · |
| `onSelectedFileForUpload` | · | · | x | x | x | x | · | · | · |
| `onSelectedPath` | x | x | x | x | x | x | · | · | · |
| `onSelectTag` | x | x | x | x | x | x | x | · | · |
| `onSendAddBomb` | · | · | · | · | x | · | x | · | · |
| `onSendAddHorse` | · | · | · | · | x | · | · | · | · |
| `onSendBaddyHurt` | · | · | · | · | x | · | · | · | · |
| `onSendBaddyProperties` | · | · | · | · | x | · | · | · | · |
| `onSendBoardModify` | · | · | · | · | x | · | x | · | · |
| `onSendBoardModify2` | · | · | · | · | x | · | x | · | · |
| `onSendCarryThrown` | · | · | · | · | x | · | x | · | · |
| `onSendDelBomb` | · | · | · | · | x | · | x | · | · |
| `onSendDeleteNPC` | · | · | · | · | x | · | x | · | · |
| `onSendDeleteWeapon` | · | · | · | · | x | · | x | · | · |
| `onSendDelHorse` | · | · | · | · | x | · | · | · | · |
| `onSendDownloadFile` | · | · | · | · | x | · | x | · | · |
| `onSendEnterLevel` | · | · | · | · | x | · | x | · | · |
| `onSendExplosion` | · | · | · | · | x | · | x | · | · |
| `onSendExtra` | · | · | · | · | x | · | x | · | · |
| `onSendFileDeletion` | · | · | · | · | x | · | x | · | · |
| `onSendFileRename` | · | · | · | · | x | · | x | · | · |
| `onSendFilesMove` | · | · | · | · | x | · | x | · | · |
| `onSendFireSpying` | · | · | · | · | x | · | x | · | · |
| `onSendFlag` | · | · | · | · | x | · | x | · | · |
| `onSendFolderDeletion` | · | · | · | · | x | · | x | · | · |
| `onSendHaveWindow` | · | · | · | · | x | · | x | · | · |
| `onSendImageUpdate` | · | · | · | · | x | · | x | · | · |
| `onSendImageUpdateCRC` | · | · | · | · | x | · | x | · | · |
| `onSendIsPKer` | · | · | · | · | x | · | x | · | · |
| `onSendLevelWarp` | · | · | · | · | x | · | x | · | · |
| `onSendLevelWarpModtime` | · | · | · | · | x | · | x | · | · |
| `onSendNPCProperties` | · | · | · | · | · | · | x | · | · |
| `onSendOpenChest` | · | · | · | · | x | · | x | · | · |
| `onSendPingAnswer` | · | · | · | · | x | · | x | · | · |
| `onSendPlayerHurt` | · | · | · | · | x | · | x | · | · |
| `onSendPlayerProperties` | · | · | · | · | x | · | x | · | · |
| `onSendPreloadLevel` | · | · | · | · | x | · | x | · | · |
| `onSendPrivateMessage` | · | · | · | · | x | · | · | · | · |
| `onSendProjectile` | · | · | · | · | x | · | x | · | · |
| `onSendRCChat` | · | · | · | · | x | · | x | · | · |
| `onSendRemoveExtra` | · | · | · | · | x | · | x | · | · |
| `onSendRequestText` | · | · | · | · | x | · | x | · | · |
| `onSendSaveFile` | · | · | · | · | x | · | x | · | · |
| `onSendServerWarp` | · | · | · | · | x | · | x | · | · |
| `onSendSetText` | · | · | · | · | x | · | x | · | · |
| `onSendShot` | · | · | · | · | x | · | x | · | · |
| `onSendTakeExtra` | · | · | · | · | x | · | x | · | · |
| `onSendToAllChat` | · | · | · | · | x | · | x | · | · |
| `onSendTriggerAction` | · | · | · | · | x | · | x | · | · |
| `onSendUnsetFlag` | · | · | · | · | x | · | x | · | · |
| `onSendUpdatePackage` | · | · | · | · | x | · | x | · | · |
| `onSendUploadEnd` | · | · | · | · | x | · | x | · | · |
| `onSendUploadStart` | · | · | · | · | x | · | x | · | · |
| `onSendWantClassScript` | · | · | · | · | x | · | x | · | · |
| `onSendWantGaniScript` | · | · | · | · | x | · | x | · | · |
| `onSendWantImage` | · | · | · | · | x | · | x | · | · |
| `onSendWantWeaponScript` | · | · | · | · | x | · | x | · | · |
| `onSendWeaponHit` | · | · | · | · | x | · | x | · | · |
| `onSendWeaponImage` | · | · | · | · | x | · | x | · | · |
| `onSendWindowList` | · | · | · | · | x | · | x | · | · |
| `onServerListerConnect` | x | x | x | x | x | x | x | · | · |
| `onServerLogin` | x | x | x | x | x | x | x | · | · |
| `onServerSetPlayerX` | · | · | · | · | · | · | · | · | x |
| `onServerSetPlayerY` | · | · | · | · | · | · | · | · | x |
| `onServerSetPlayerZ` | · | · | · | · | · | · | · | · | x |
| `onServerWarp` | · | · | · | · | x | · | x | · | · |
| `onShow` | x | x | x | x | x | x | x | · | · |
| `onSleep` | x | x | x | x | x | x | x | · | · |
| `onStartDrag` | · | x | x | x | x | x | x | · | · |
| `onStartedWithURL` | · | · | · | · | · | · | x | x | · |
| `onStopDrag` | · | x | x | x | x | x | x | · | · |
| `onStyleChanges` | · | · | x | x | x | x | x | · | · |
| `onTabComplete` | x | x | x | x | x | x | · | · | · |
| `onTextChanged` | x | x | x | x | x | x | x | · | · |
| `onTextEditStart` | · | · | · | x | x | x | x | · | · |
| `onTFontOptionsProblem` | · | · | · | · | · | · | · | · | x |
| `onToall` | x | x | x | x | x | x | · | · | · |
| `onTranslationUpdated` | · | · | x | x | x | x | x | · | · |
| `onUnload` | x | x | · | · | · | · | · | · | · |
| `onUpdate` | · | · | · | · | · | · | · | · | x |
| `onUpdatePackageDownloaded` | x | x | x | x | x | x | x | · | · |
| `onURL` | x | x | x | x | x | x | x | · | · |
| `onVideoFinished` | · | · | · | · | · | · | x | x | · |
| `onVideoLoaded` | · | · | · | · | · | · | x | x | · |
| `onWake` | x | x | x | x | x | x | x | · | · |

## Still open

- The call site that fires each name, per build, starting with the 6.1.1.3 `onSend…` group for `#397`.
- How 7.12.43 and Android 2.2 store the names this list misses.
- The run-time names of the GS1-mask events on 6.x (whether `onPlayerEnters` is built from `playerenters`).
