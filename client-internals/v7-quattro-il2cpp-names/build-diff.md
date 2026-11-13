# Quattro / Graal type names, 548 through 71243

Declared names only (`class` / `enum` lines). Token counts are separate because Il2CppDumper pastes `QuattroC2DRenderer` onto unrelated types.

Confidence: high for presence/absence of a literal declaration. Low for treating a missing nested name as a removed game API — the dumper rebinds names between builds, and `UnityEngine.Quattro3D.Tiles` stays present after the nested `QuattroC2DRenderer.Tile*` names vanish.

## Names that still read as game types

| Declaration or namespace | 548 | 610 | 612 | 613 | 614 | 71243 |
| --- | --- | --- | --- | --- | --- | --- |
| `Quattro.Graal.DatasFromGraal` | no | yes | yes | yes | yes | yes |
| `Quattro.Graal.Actor` / `ActorType` | no | yes | yes | yes | yes | yes |
| `UnityEngine.Quattro3D.Tiles` | no | no | no | yes | yes | yes |
| `Quattro3D` namespace | no | no | no | yes | yes | yes |
| `QuattroC2DRenderer.TileLightParameters` | no | no | no | no | yes | no |
| `QuattroC2DRenderer.TileParticlesParameters` | no | no | no | no | yes | no |
| `QuattroC2DRenderer.TileWarpParameters` | no | no | no | no | yes | no |
| `QuattroC2DRenderer.OpenTileParametersInterface` | no | no | no | no | yes | no |
| `QuattroC2DRenderer.MousePositionRttReceiver` | no | no | no | no | no | no (yes in 612 only) |
| `Quattro3DText.EasingFunction` | yes | no | no | no | no | no |

548's only clean Quattro declarations are `Quattro3DText.EasingFunction` and `Quattro3DTextType.Function`. The identifier `QuattroC2DRenderer` still occurs 47 times in 548 as a substituted type, not as its own class.

612 is the only build that declares `QuattroC2DRenderer.MousePositionRttReceiver` and `QuattroC2DRenderer.<_Batch>d__6`, plus `Quattro2D` dropdown/button nested types and `Quattro2DOptimisedRenderingOption` (Cinemachine-shaped names: `VcamActivatedEvent`, `BrainFrame`). Those names do not return in 614.

614 is the only build that declares the tile/particle/warp parameter nested types listed in `quattro-renderer-surface.md`.

## 548 vs 71243 declared `Quattro*` / `Graal*` class names

Shared declared names: none.

548-only clean names: `Quattro3DText.EasingFunction`, `Quattro3DTextType.Function`.

71243-only names that are not X509/PKCS noise:

| Name | Reading |
| --- | --- |
| `QuattroObjectRendererType.FileSystemEntryFilter`, `Filter`, `InputProperties`, `OnCancel`, `OnSuccess` | file-dialog shaped |
| `QuattroObjectRendererType.<WaitForLoadDialog>`, `<WaitForSaveDialog>`, `<CreateNewFolderCoroutine>` | file-dialog coroutines |
| `QuattroObjectRendererActor.ZipEntryEnumerator`, `PartialInputStream`, `KeysRequiredEventHandler` | zip-library shaped, not a renderer |

71243 still has `DatasFromGraal`, `Actor`, `ActorType`, and `UnityEngine.Quattro3D.Tiles`. The nested `QuattroC2DRenderer.Tile*` class names from 614 are absent. `QuattroC2DRenderer` as a token drops to 2 hits in 71243, both as a base type on unrelated visitors (`BinaryReaderWrapper.CastDataSourceVisitor`, `GetPropertyVisitor`).

## 71243 and `Graal3DEngineFlavor0.dll`

The native export list for 71243 starts `dll_name=Graal3DEngineFlavor0.dll`. That string, and `Graal3DEngine`, are absent from the 71243 `dump.cs` (and from the other five). The C# dump does not record the DLL rename. Confidence: high.

Do not read the empty overlap of declared class names as “the renderer was deleted.” The dumper’s name substitution moves between builds, and the tile namespace is still there in 71243.
