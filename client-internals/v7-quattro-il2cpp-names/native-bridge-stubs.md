# Native bridge stubs in the C# dumps

Searched all six `Dumped_GameAssembly/dump.cs` files. The native DLL was not reopened. Export names used as search keys come from the existing note `unpacked_Graal3DEngine_exports.txt` (`QuattroFixedUpdate`, `QuattroUpdate`, `QuattroInitializedReturn`, and the 71243 DLL name `Graal3DEngineFlavor0.dll`).

Confidence: high that no clean Graal3DEngine call site is in these dumps.

## Counts

| Token | 548 | 610 | 612 | 613 | 614 | 71243 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `DllImport` | 0 | 0 | 0 | 0 | 0 | 0 |
| `Graal3DEngine` | 0 | 0 | 0 | 0 | 0 | 0 |
| `Flavor0` | 0 | 0 | 0 | 0 | 0 | 0 |
| `QuattroFixedUpdate` | 0 | 0 | 0 | 0 | 0 | 0 |
| `QuattroUpdate` | 0 | 0 | 0 | 0 | 0 | 0 |
| `QuattroInitializedReturn` | 0 | 0 | 0 | 0 | 0 | 0 |
| `MonoPInvokeCallback` | 1 | 1 | 1 | 19 | 1 | 0 |
| `static extern` | 40 | 40 | 40 | 49 | 40 | 40 |

## What those hits actually are

No `DllImport` attribute survived in any dump.

`static extern` methods are Win32-shaped: `LoadLibraryEx`, `FreeLibrary`, `CreateFilePrivate`, `GetFileAttributesExPrivate`, `BCryptGenRandom`, and similar. They are not Quattro or Graal3DEngine exports. Confidence: high.

`MonoPInvokeCallback` sites:

| Build | Site | Confidence |
| --- | --- | --- |
| 614 (and the single hit in 548, 610, 612) | `MessageCallback` next to `OnPurchaseSucceeded` / `OnAppReceiptRetrieved` (Unity IAP) | high that this is store code |
| 613 extra hits | `SWIGRegisterExceptionCallbacks_FirebaseMessaging` and `SetPending*Exception` | high that this is Firebase SWIG |
| 71243 | none | high |

`ConvertToNative` appears on `QuattroObjectRenderer.BindingsMarshaller` in 614, and again on types the dumper named `TTempTile`, `TMeshWrapper`, and `TMeshWrapperManager` (Unity web request, text, XR, VFX, hierarchy). None of those methods name a Graal3DEngine export.

## Result

There is no clean C# call site for `Graal3DEngine.dll` or `Graal3DEngineFlavor0.dll` in these dumps. The 71243 export-name change is recorded only in the native notes. This C# pass does not show that DLL name.
