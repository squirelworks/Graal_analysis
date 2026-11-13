# Quattro renderer surface (build 614)

File: `WorldsSetup64-614/Dumped_GameAssembly/dump.cs`.

There is no undecorated `class QuattroC2DRenderer` or `class QuattroObjectRenderer`. Those names survive as nested types and as mis-applied field types. Confidence on the nested method names: medium. Confidence that a parent renderer class body was recovered: low (it was not).

`QuattroObjectRendererActor*` and `QuattroObjectRendererSpriteDraw*` in this dump are X509 / PKCS / Backtrace (`Send`, `SendMinidump`, `ContentInfo`, `DeriveBytes`). They are Il2CppDumper misnames, not renderer APIs. Omitted from the groups below.

## QuattroC2DRenderer nested types

| Group | Type | Public methods (ctors omitted) |
| --- | --- | --- |
| tile | `TileLightParameters` (two copies, TypeDefIndex 25431 and 25436) | `DoSetEnabled`, `DoSetRange`, `DoSetIntensity`, `DoSetColorR/G/B`, `DoSetGradient`, `DoSetGradientRange`, `DoSetGradientA`, `Init`. The 25431 copy also has `DoSetSpotAngle`, `DoSetDirectionX`, `DoSetDirectionY`. |
| particle | `TileParticlesParameters` | `DoSetParticlesPrefabs`, `Init` |
| warp | `TileWarpParameters` | `DoSetScaleX/Y/Z`, `DoSetOutPositionX/Y/Z`, `DoSetOutLevel`, `DoSetOutDirection`, `Init`, `CopyParametersTo`, `Update`, `RecalculateDynamicBounds` |
| tile / UI | `OpenTileParametersInterface` | `Invoke(bool open, tile, a, b)` |
| tile / UI | `RegisterTileForUI` | `Invoke(tile)` |
| tile / UI | `UnregisterTileForUI` | `Invoke(tile)` |
| other | `<>c__DisplayClass12_0`, `13_0`, `27_0` | compiler closures; skipped |

## QuattroObjectRenderer nested types

These sit next to `UnityEngine.Event`, `UnityEngine.GUI`, and `GUILayoutUtility`. Parameter names on two marshallers are `guiStyleState` and `guiStyle`. Treat them as Unity IMGUI types that inherited the Quattro name. Confidence they are a Graal object renderer: low.

| Group | Type | Public methods |
| --- | --- | --- |
| window | `WindowFunction` | `Invoke(int id)` |
| layout | `LayoutCache` | `ResetCursor` (field `id` setter is private) |
| other | `SkinChangedDelegate` | `Invoke()` |
| other | `BindingsMarshaller` (three copies) | `ConvertToNative(QuattroObjectRenderer) -> IntPtr` |

`ConvertToNative` is the only method here that looks like a native marshal. It does not name `Graal3DEngine`. See `native-bridge-stubs.md`.

## Close siblings — `UnityEngine.Quattro3D.Tiles`

Present in 613, 614, and 71243. Shared public shape: `TypeInit`, `ReadParameters`, `WriteParameters`. Extra methods called out.

| Class | Extra public methods | Group |
| --- | --- | --- |
| `TileParameters` | `DoSetHideWithCamera`, `RecalculateDynamicBounds`, `Update` | tile |
| `TileNameParameters` | setters for the name parameter | tile |
| `Tile` | `BindTilesParameters` | tile |
| `TileAmbientLight` | `BindTileAmbientLightParameters` | tile |
| `TileAmbientSound` | bind ambient sound | tile |
| `TileBackGround` | bind background | tile |
| `TileCamera` | bind camera | tile |
| `TileComposite` | `BindTilesParameters` | tile |
| `TileDecal` | bind decal | tile |
| `TileDirectionalLight` | `BindTileLightParameters` | tile |
| `TileDoor` | `GetDoorParameters`, `BindTilesParameters` | tile |
| `TileFlower` | bind flower | tile |
| `TileHouse` | `BindTilesParameters` | tile |
| `TileLight` | `BindTileLightParameters` | tile |
| `TileParticles` | (shared trio only) | particle |
| `TileSpawn` | `GetSpawnParameters`, `BindTilesParameters` | other |
| `TileSpotLight` | `BindTileLightParameters` | tile |
| `TileTestSpawn` | (shared trio only) | other |
| `TileTree` | (shared trio only) | tile |
| `TileWarp` | (shared trio only) | warp |

Nearby, still in the same dump region: `PartitionSystem`, `EraEditorObject`, `Era3DMapFileUtils`, `ProTilePropertiesManager`, `BuildTilesToMap`. Field types on those classes are scrambled (`QuattroC2DRenderer` used as a field type). Not listed as renderer methods.

`UnityEngine.Tilemaps.Tile` / `Tilemap` in the same file are Unity tilemap APIs, not Quattro.

## Native-looking methods on this surface

| Method | Call-into-native? | Confidence |
| --- | --- | --- |
| `BindingsMarshaller.ConvertToNative` | Looks like an il2cpp bindings marshaller. No `DllImport`, no `Graal3DEngine`. | medium that it is Unity marshalling; low that it is the Graal3DEngine bridge |
| Delegate `.ctor(object, IntPtr)` on `WindowFunction`, `OpenTileParametersInterface`, `RegisterTileForUI`, `UnregisterTileForUI` | Standard delegate constructor | high that this is not a native export |
| `DoSet*` / `ReadParameters` / `WriteParameters` | Empty stubs in the dump (`{ }`). No native attribute | high that the dump does not show a native call |
