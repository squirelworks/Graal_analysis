# v7 Worlds: the unpacked GameAssembly (IL2CPP) images, builds 548–71243

Date: 2026-11-13. Static read only. Nothing was run. No addresses, no decompiled code. Tags: **[bin]** read from the unpacked `GameAssembly.dll` images or their shipped IL2CPP metadata; **[inf]** inference.

The six Worlds builds each ship two Themida-wrapped native modules: the Graal engine plugin `Graal3DEngine.dll` and Unity's IL2CPP `GameAssembly.dll`. The engine plugin is covered by the `protocol/v7-graal3d-*.md` notes and [v7-graal3d-unity-bridge.md](v7-graal3d-unity-bridge.md). Owner-held unpacked copies of all six `GameAssembly.dll` images exist next to those engine dumps, but until now the repo only listed them ("GameAssembly inventory" in [v7-graal3d-identity-and-builds.md](../protocol/v7-graal3d-identity-and-builds.md)). This note is that missing read. It covers the managed side: what the C# layer is, how it hosts the Graal engine, and what changed between builds.

The Graal network protocol, cipher, packet tables, GS2 VM and script builtins are **not** in GameAssembly. They are all in the engine plugin (see the bridge note: GameAssembly "does not reimplement PLI/PLO"). This read confirms that from the managed side: none of the six images contains a Graal login token, a `Graal/6.7x` user-agent string, a packet-id table or a GS2 opcode name. **[bin]**

## The six images

| Build | PE stamp | Unity player (`Worlds.exe` version) | Packed → unpacked size | Metadata version | Types | String literals |
|---|---|---|---|---|---|---|
| 548 | 2022-12-17 | 2021.3.8 | 23 MB → 72 MB | 29 | 25,820 | 17,969 |
| 610 | 2023-10-06 | 2022.3.9 | 25 MB → 77 MB | 29 | 27,078 | 19,199 |
| 612 | 2024-01-12 | 2023.2.3 | 27 MB → 83 MB | 29 | 28,062 | 20,108 |
| 613 | 2024-04-15 | 2023.2.13 | 27 MB → 84 MB | 29 | 27,939 | 20,265 |
| 614 | 2024-04-21 | 2023.2.13 | 27 MB → 83 MB | 29 | 27,823 | 20,089 |
| 71243 | 2024-10-15 | 2023.2.20 | 26 MB → 80 MB | 29 | 27,010 | 19,731 |

**[bin]** Each GameAssembly has the same PE stamp as the `Graal3DEngine.dll` of its build, so both modules were built together. Neither carries a version resource. The packed images have blank section names plus `.themida`/`.boot`; the unpacked images add a `.text` and an `.SCY` section and keep the Themida residue (`.themida`, `.boot`) as dead sections, the same shape as the unpacked 6.x Windows exes ([themida-pack.md](themida-pack.md)). The current installed Worlds client (Unity 6000.0, 2026) is packed only and was not read.

**Is the code really there?** **[bin]** Yes. In every build the unpacked image has 20,000–30,000 more printable strings than the packed one, and the 43–52 names of the native callback table (below) appear as C strings in each unpacked image and in none of the packed images. Both forms export the same 236–241 `il2cpp_*` API names, so the export table survives packing; the code and data behind it do not.

**Metadata.** **[bin]** Each build's `global-metadata.dat` (shipped in the clear beside the app, not inside the packer) is a plain IL2CPP version-29 file with the normal magic. It is not encrypted or renamed. Type, method and field names and all string literals read directly from it. That is where the class and method names in this note come from; the unpacked GameAssembly supplies the native side (the strings and the callback names).

## What the managed layer is

**[bin]** Own assemblies (all others are Unity, .NET and third-party packages):

| Assembly | Role | 548 | 610 | 612 | 613 | 614 | 71243 |
|---|---|---|---|---|---|---|---|
| `Assemblies-Quattro` | Unity host for the engine, plus the generated binding layer | 14,390 | 15,921 | 15,759 | 15,762 | 15,761 | 15,117 |
| `Assemblies-quattroplugins` | bundled third-party code: LiteNetLib, MLAPI, NativeWebSocket, Funly SkyStudio, RuntimeInspector, DynamicPanels, a BMP loader, an OBJ loader | 616 | 613 | 613 | 530 | 511 | 511 |
| `Assemblies-Quattroshared` | `Era3D.*` tile/level build types and `UnityEngine.Quattro3D.Tiles` | 187 | 192 | 192 | 153 | 153 | 153 |
| `Assemblies-quattrosharedlowlevel` | small `Scripting.Engine` / `Scripting.File` helpers | 98 | 102 | 103 | 28 | 24 | 25 |
| `Assemblies-graalunity` | the `Quattro.Graal` data hand-off types (and, in 548, a full PlayMaker action set) | 1,101 | 14 | 14 | 4 | 4 | 4 |
| `Assemblies-playmaker` | PlayMaker UI event proxies | – | 15 | 15 | 14 | 14 | 14 |
| `Assembly-CSharp` | almost empty (5–11 types) | 6 | 11 | 11 | 7 | 6 | 5 |

(Numbers are type counts.)

**The bulk is a generated binding layer, not game code.** **[bin]** In every build about 14,000–15,500 of the `Assemblies-Quattro` types are delegate types with generated names that spell out a Unity API member, for example a `UnityEngine.GameObject` property getter or a Cinemachine field setter. The matching `NativeScript.Bindings` and `BindingsPart0`…`BindingsPart17` classes hold 14,108 (548), 15,622 (610), 15,466 (612–614) and 14,819 (71243) binding methods. Their names and shape (`Box…`/`Unbox…`/`Release…` helpers, an object store with handles, a `_SetCsharpException` path, an `Init` that receives function pointers) are those of a C++-scripting-for-Unity binding generator: C++ code calls Unity's C# API through function pointers that the C# side registers at start-up. **[bin][inf]** So in v7 the **native Graal engine drives Unity**, not the other way round. The C# layer is a host and an API exporter; the Unity objects the engine creates and moves (game objects, meshes, textures, cameras, particles, UI, PlayMaker FSM variables, LiteNetLib/MLAPI objects) are all reached through these bindings.

The bound API surface is the set of Unity types the engine is allowed to touch. It covers core objects and transforms, rendering (command buffers, meshes, render textures, URP and post-processing), physics 2D/3D, particles, animation, audio, UI and event systems, Cinemachine, PlayMaker, LiteNetLib and MLAPI, NativeWebSocket, and the Quattro rendering helpers (`Quattro.Rendering.TMeshWrapperManager`, `Texture2DWrapper`, `TileRenderer`, `Quattro2D`). **[bin]** In 71243 the generated delegate-type names change their suffix from `DelegateType` to `DT` and one binding part (`BindingsPart17`) is folded away; the bound set is about 4% smaller.

## How the engine is hosted

**[bin]** Start-up is in `NativeScript.BootScript` (`Awake`, `DoAwake`, `OpenBindings`, `CloseBindings`, `OnApplicationQuit`; fields `loaded`, `MemorySize`, `debugLibraryLoad`). The literals `OpenPlugin Init curMemory=` and `OpenPlugin OUT` are the log lines written around plugin load. The plugin is opened by module name `Graal3DEngine`, stored as a UTF-16 string in all six unpacked images; there is no narrow-string DLL import of the engine. **[bin][inf]** That is why 71243 still loads a file named `Graal3DEngine.dll` even though its export-directory name is `Graal3DEngineFlavor0.dll`.

**The callback table.** **[bin]** `NativeScript.NativeTypedDelegates` is the set of native entry points the C# side calls. It matches the engine export list in the bridge note. Per build:

| Build | Count | Change against the previous build |
|---|---|---|
| 548 | 45 | baseline: frame ticks (`QuattroUpdate`, `QuattroFixedUpdate`, `SetFrameTick`), render events, mesh/UV/texture push, file probes (`AskFileExists`, `FillPointerWithFile`, `SendFileToCpp`, `SendFileToHttpRequest`), the native download object (`TFileDownload_*`), 3D level and player hooks, focus/pause/low-memory, `DoQuit`, `SetStartServerClassicReloaded` |
| 610 | 44 | `SetStartServerClassicReloaded` removed |
| 612 | 46 | `OnTouchEvent`, `ManageMultiTouch` added |
| 613 | 45 | `FillPointerWithTexture2`, `GetTextureSize`, `onDeeplink` and two Firebase push callbacks added; `TFileDownload_CanDownload/_Download/_Update`, `GetCurrentWrappersLength/CurrentDone` and the first key-event entry removed |
| 614 | 43 | the two Firebase push callbacks removed again |
| 71243 | 52 | tile-atlas path added: `LoadTilesTexture`, `UnloadTilesTexture`, `PrepareTilesAtlas`, `CopyTilesPixels`, `SendTileAtlasToUnity`, `GetBitmapWidth/Height`, `GetFileSize`, `SendTexturesWithOpenGLESAndroid` |

**[inf]** From 613 on, file download is no longer a native object that C# polls; the C# side only answers file and texture requests. 71243 moves tile-sheet atlas building into the engine and hands the finished atlas to Unity.

**The reverse direction** (engine calls into C#) is `Quattro.UQuattroUnityBridge`: paths (streaming assets, persistent data, temporary cache), pinned buffers and stream hand-off, clipboard, keyboard request, log, quit, target frame rate, a JavaScript command hook for the WebGL build, and three launch inputs. **[bin]** In 548 the launch input is `GetGameFromUnity`. From 610 it is `GetGameToConnectIfLogin` plus `GetPremium`.

## Launch inputs

[v7-connector-live-20261111.md](../protocol/v7-connector-live-20261111.md) covers why a stock v7 client cannot go online against a lab server. Whether a standalone start reaches the connector at all also depends on what the Unity host hands the engine at start. `DoQuit` is one of the native callbacks above. The managed metadata names what the C# host can hand the engine at start. **[bin]**

- `Quattro.UnityMain` fields: `gameToConnectIfLogin`, `premium`, `SteamAppId`, `forceIsSteam`, `steamWorkManagerGo`, `deepLinkData`, `exitPopupGo`, `WillQuit`, `leavingApplication`.
- `UnityMain` methods added by build: 610 `isSteam`, `GetSteamId`, `GetPersonaName`, `GetEnteredGamepadTextInput` (Steamworks.NET assembly first appears in 610; the literal `notsteam` from 610); 613 `WantsToQuit`, `Quitting`, `onDeepLinkActivated`; 614 `GetDeepLinkDatas`, `clearDeepLinkData`.
- `Quattro.SecureIds` holds three Discord application/bot id fields and `authenticate`; it is gone from 71243.

**[inf]** The start-up inputs the engine can query are therefore: which game to connect to, a premium flag, a Steam identity (or "not Steam"), and from 613/614 a deep-link payload. They are Unity-side state, read through the bridge, not command-line strings in the engine. An empty game, Steam or deep-link input is therefore a candidate reason for a standalone start to stop early, beside a missing launcher argument. It is not proven; the C# method bodies were not read.

## Other notable content

- **[bin]** `Quattro.Graal.DatasFromGraal` (fields `playerPosition`, `level`, `map`, `sentFromGraal`, `serverPlayers`, `npcs`) and `Quattro.Graal.Actor` (`position`, `name`, `type`) are the only managed types named after Graal. In 548–612 PlayMaker actions (`GetFromGraal`, `SendToGraal`, `DistanceFromPlayer`, `DistanceFromPlayerTo1`, `PlayerPosition`) expose them to PlayMaker FSMs; from 613 the first four are methods on `DatasFromGraal` and `PlayerPosition` is gone.
- **[bin]** `Quattro3D.UQuattro3DBridge` / `Quattro3DBridge` / `UServerPlayer3D` / `UServerNPC3D` / `MapLoadingManager` / `SimpleLoadMap` are the 3D-level side (load level asset bundles, spawn and move server players and NPCs). `GraalPackageNamer.GetFileNameForDownload` names downloaded packages. The tile kinds in `UnityEngine.Quattro3D.Tiles` (house, door, warp, spawn, light, particles, tree, flower, decal, camera, ambient sound) are present in all six builds.
- **[bin]** `SprinterPublishing.*` is an MNG/PNG chunk reader (MHDR, FRAM, BACK, TERM chunks), used for animated images.
- **[bin]** Literals present in every build: `C:\Graal2\levels\`, `emptylevel.nw`, `.nw`, `.gmap`, `CONNECTED TO SERVER`, `DISCONNECTED FROM SERVER`, `PLAYER CONNECTED`, `Quattro c# exception report`, `TryCatchOnQuattro`. `HOME.graal` is in 548–612 only. `worlds` and `testingworlds` are in 548–614 and gone from 71243. Build 548 alone carries a vendor build-machine path to a self-signed HTTPS certificate and key for a small local test server (`SmallServerSSL`).
- **[bin]** Telemetry and store SDKs: Backtrace crash reporting and Unity Services/Analytics and Unity Purchasing in all six; Steamworks.NET from 610; Firebase App/Messaging only in 613; IronSource ads only in 613; Unity LevelPlay (ads) from 614.

## What changed between neighbouring builds

Counts are own-assembly types excluding the generated binding delegate types. **[bin]**

| From → to | Added | Removed | Main change |
|---|---|---|---|
| 548 → 610 | 59 | 1,093 | the full PlayMaker action library leaves `Assemblies-graalunity` (a separate `Assemblies-playmaker` keeps 15 UI proxies); Steamworks added; launch input becomes game-to-connect + premium; Android memory-advice types added |
| 610 → 612 | 3 | 8 | touch input callbacks; Android memory-advice types removed again |
| 612 → 613 | 22 | 219 | `Era3D.Editor` / build-time JSON types and most of `quattrosharedlowlevel` dropped from the shipped build; Firebase and IronSource added; deep-link and quit-request handling added; native download object retired |
| 613 → 614 | 1 | 25 | IronSource and Firebase removed again; LevelPlay added; `Scripting.Engine.THashList` removed |
| 614 → 71243 | binding rename only | 7 | delegate suffix `DT`; one binding part folded; `SecureIds` removed; tile-atlas callbacks added |

## Relation to the other v7 notes

- Engine side, identity, token absence, packet tables: [v7-graal3d-identity-and-builds.md](../protocol/v7-graal3d-identity-and-builds.md) and the other `protocol/v7-graal3d-*.md` notes.
- Engine exports seen from the native side: [v7-graal3d-unity-bridge.md](v7-graal3d-unity-bridge.md). The C# callback table above is the same contract read from the other end.
- The supplied 701750 images: [v7-701750-bridge-clock.md](v7-701750-bridge-clock.md). Not compared here.
- Coverage of every unpacked client image in the archive: [unpacked-images-coverage.md](unpacked-images-coverage.md).
