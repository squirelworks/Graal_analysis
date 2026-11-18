# v7 Worlds, Unity 6000 build: IL2CPP names recovered, and the startup/date gate read from the unpacked modules

Date: 2026-11-18. Tags: **[bin]** read from the original or unpacked file · **[cap]** produced by an earlier run in an isolated lab VM (no network, no game start; the tools were run against the DLLs, `Worlds.exe` was not launched) · **[inf]** inferred.

This note continues [v7-unity6000-unpack.md](v7-unity6000-unpack.md). That note unpacked the two Themida-wrapped modules of the current installed Worlds client but reported that the IL2CPP C# names "are not readable with current public tooling": Il2CppDumper recognized metadata version 31, then failed in generic-type resolution and wrote only a 3.55 MB partial `dump.cs`. It left three hypotheses open (a Unity 6 / metadata-31 layout the dumper mishandles, damage in the recovered image, or a mistake in locating the registration structures) and did not decide between them.

That open item is now resolved, and the readable names let the startup-quit path, the launch inputs and the date gate be read directly from the unpacked modules instead of chased in a running client. The point of this note: **once the modules are unpacked, v7 is a static problem, not a runtime one.**

## The IL2CPP names come out after all

**[cap]** The failure was the third hypothesis — the dumper's interpretation of the registration structures, not image damage and not an inherent metadata-31 limit. The registration arrays in the recovered image carry **static metadata indices** (the values are fixed at the image base they were dumped at), but the public dumper's heuristic reads them as **runtime handles**. Correcting that one interpretation lets the same Il2CppDumper 6.7.46 run to completion on the same unpacked GameAssembly and the same unmodified version-31 `global-metadata.dat`, with no `ForceIl2CppVersion` and no `ForceDump`.

**[bin]** With the correction, the dumper writes the full set, not a partial:

| | partial (first run, unpack note) | corrected run |
|---|---|---|
| `dump.cs` | 3.55 MB, 2,543 type entries, 16 `NullReferenceException` markers | ~32 MB, **15,546 types**, no embedded exception markers |
| `il2cpp.h` | not written | written (~49 MB) |
| `script.json` | not written | written (~104 MB) |
| `DummyDll` | not written | written; all generated assemblies parse |

**[bin]** The recovered surface is **15,546 types, 112,435 methods, 58,791 fields, 16,296 properties, 230 events**. All generated assemblies parse under a Cecil read, and the framework/Unity inheritance checks pass. The same static-index correction was applied to the six older builds (548, 610, 612, 613, 614, 71243); each reconstructs with zero missing or duplicated type-definition markers and independent metadata member counts that match the generated assemblies. So the names are readable for **all seven builds**, latest included.

**[inf]** This recovers declarations, signatures and the static method→RVA map. It does **not** recover original C# method bodies, and it is not a runnable client. Treat `dump.cs`/`il2cpp.h`/`script.json` as a type-and-symbol index over the unpacked image, nothing more.

## The startup-quit path, in managed names

The older runtime work ([v7-connector-live-20261111.md](../protocol/v7-connector-live-20261111.md) and the lab notes behind it) established from `Player.log` that a **standalone** launch draws exactly one frame and then quits before login: `OpenPlugin(InitMode)` → one URP render loop → `Quit` → `Quattro->Do Quit` → `NativeScript.NativeTypedDelegates:DoQuit()` → clean `OnApplicationQuit`. The native plugin calls quit on itself; it is not a crash and not a user close.

**[bin]** The recovered names put concrete managed symbols on that boundary:

- `UQuattroUnityBridge.Quit(string reason)` (TypeDefIndex 121) — a managed quit entry that takes a **reason** string. There is also `UQuattroUnityBridge` `ForceQuit()` and `QuattroUnityMainMethodForceQuit()`.
- `Connection.OnApplicationQuit` is an `async void` state machine (`AsyncVoidMethodBuilder.Start<Connection.<OnApplicationQuit>d__4>`), i.e. shutdown has an awaited network/teardown step — consistent with the clean `Bindings.Close`/`OnApplicationQuit` tail in the log.

**[inf]** The `DoQuit` seen in the log is the **native** side (`NativeTypedDelegates:DoQuit`) calling across the bridge; `UQuattroUnityBridge.Quit(string reason)` is the matching **managed** entry. The decision to quit is taken in the native engine at boot, before the login scene, and is then driven into managed through the bridge. The reason-string argument is the obvious next read: recover the literal(s) passed at the one-frame boot quit from the engine's `.text`.

## The launch inputs the boot path reads

**[bin]** `UnityMain : MonoBehaviour` (TypeDefIndex 114) holds exactly the inputs the earlier IL2CPP read ([v7-gameassembly-il2cpp.md](v7-gameassembly-il2cpp.md)) flagged as boot candidates, now confirmed as managed fields with native getters on the Quattro bridge:

| field (on `UnityMain`) | type | bridge getter |
|---|---|---|
| `gameToConnectIfLogin` | string | `QuattroUQuattroUnityBridgeMethodGetGameToConnectIfLogin` |
| `premium` | string | `QuattroUQuattroUnityBridgeMethodGetPremium` |
| `deepLinkData` | string (613+) | `QuattroUnityMainMethodGetDeepLinkDatas` / `clearDeepLinkData` |
| `forceIsSteam` | bool | — |

**[bin]** There is also `Environment.GetCommandLineArgs()` in the recovered surface, so command-line arguments are reachable to the boot path.

**[inf]** On a standalone double-click (no GraalOnline launcher/updater handoff), none of `gameToConnectIfLogin`, `premium` or `deepLinkData` is populated, and `forceIsSteam` is false. The native boot path finds no game to connect to and no session, which is the most likely trigger for the one-frame `DoQuit`. The realistic way past it is to supply those inputs the way the launcher does (argument, deep link, or the session file/registry value the updater writes), not to patch the quit out blind.

## The date/version gate is native, not managed

The runtime lab established a **clock gate** empirically ([the 701750 bridge/clock checkpoint](v7-701750-bridge-clock.md) and the clock-test lab): with the guest clock at the build date, the packed client reaches the connector dial (TLS 443, then `GET /conf.gs?p=` on :80); at the real 2026 clock it stalls with no dial. The unpacked modules show **where that gate is**:

**[bin]** In the recovered IL2CPP there is **no client date/version gate**. The only "expired" symbols are TLS certificate checks (`UNITYTLS_X509VERIFY_FLAG_EXPIRED`, `CERT_HAS_EXPIRED`, `X509FindType.FindByTimeExpired`). The one `buildDate` field is on `Reporter : MonoBehaviour` (TypeDefIndex 50) — the Backtrace crash reporter's metadata, not a gate. `DateTime.get_Now` exists but is the ordinary framework accessor.

**[bin]** The **unpacked engine** (`Graal3DEngine.dll`), by contrast, imports wall-clock APIs that the packed original hid behind Themida: `GetSystemTime`, `GetSystemTimeAsFileTime`, `_time64` and — the telling one — `_mktime64`, which turns a broken-down calendar date into a timestamp for comparison. (The engine also uses `GetTickCount`/`QueryPerformanceCounter`, but those are the frame clock in `QuattroUpdate`, a separate thing.)

**[inf]** So the version/date gate lives in the **native engine**, reading the system wall clock and comparing against a baked date, which is exactly consistent with the empirical clock gate. This is why holding the guest clock at the build date is what lets the connector fire. Reading the baked date and the comparison out of the engine's `.text` (now that it is unpacked and `_mktime64`'s caller is locatable) would turn the empirical gate into an exact, documented check.

## A better method for analyzing v7 clients

The runtime track spent many sessions failing to drive the stock client to a capture (headless renders black; the connector gates behind Unity cloud services; the engine's bundled curl uses c-ares DNS that bypasses the loopback redirect; Themida blocks inline hooks; and the standalone boot `DoQuit`s before login). The unpacked modules make almost all of that unnecessary:

1. **Unpack both Themida modules with the 64-bit Unlicense, one at a time.** Both `GameAssembly.dll` and `Graal3DEngine.dll` are **x64** (`.themida` + `.boot` sections), so the tool must be the **x64** Unlicense 0.4.0 build (Themida/WinLicense 3.x support); the Unlicense binary's own PE machine must read as AMD64. A 32-bit Unlicense (a `...-x86`/`unlicense-32` build) is the wrong bitness and cannot dump an x64 target — match the tool to the target. Run `<tool> <dll> --timeout=60 --verbose=True`, no forced OEP or patch, in an isolated headless Win10 lab clone (no NIC, no shared folders); the unpacker runs the DLL through its own loader, so the client never starts and never phones home. The outputs gain a leading `.text` (the recovered code) and a trailing `.SCY` (the rebuilt IAT); the dead `.themida`/`.boot` sections stay as weight. These are base-fixed analysis images, not runnable replacements.
2. **Recover IL2CPP names with the static-index correction**, then read declarations/signatures/RVAs from `dump.cs`/`il2cpp.h`/`script.json` — don't try to read names out of a live process.
3. **Read the gates statically:** launch inputs on `UnityMain`, the quit boundary on `UQuattroUnityBridge`, the native date gate via the engine's `_mktime64` caller.
4. **Use the runtime only for the one thing static can't give cheaply:** the connector's signed reply. Capture it with the guest clock held at the build date (the only reliable way to make the stock client dial), and keep the capture and any replay material private.

In short: unpack → static-index IL2CPP recovery → static read of the three gates, with a single clock-gated capture as the only runtime step. That is the better v7 method, and it is reproducible from public tooling.

## The date gate and the quit reason, read by static disassembly

Two of the open items below are now answered by disassembling the unpacked modules directly — Capstone over the engine's recovered `.text`, with the managed side cross-checked in the Il2CppDumper `script.json`. Nothing was run.

### The date gate is an "N days after a reference date" check, wired to the boot quit

**[bin]** The engine has a single `_mktime64` call path. A small helper takes the current local time (`_time64` → `_localtime64`), then overwrites three `struct tm` fields from three 32-bit globals — `tm_mday` (tm offset `0x0c`), `tm_mon = month − 1` (offset `0x10`) and `tm_year = year − 1900` (offset `0x14`; the literal `0x76c` = 1900) — and calls `_mktime64`, yielding a `time_t` for that (year, month, day).

**[bin]** Its only caller is the gate itself: it reads `_time64(NULL)` for the current time, calls the helper for the reference `time_t`, then `difftime(now, reference)` and compares the result against `N × 60 × 60 × 24`. The two `60.0` and the `24.0` are `.rdata` doubles, so the threshold is **N days**; if `now − reference > N days` the gate returns true. Two one-byte enable flags guard it — if either is clear the gate returns false (check disabled).

**[bin]** The inputs are **initialised data in the image**, and the gate is **active**. (An earlier revision of this note read the wrong addresses — an off-by-`0x34000` slip in the rip-relative arithmetic landed in an uninitialised pointer region and wrongly suggested the gate might be dormant. The correct addresses were pinned by the v7 runtime-dump thread's read of the live data and then re-confirmed against this static image.) At the right globals:

| global | address (RVA) | value |
|---|---|---|
| enable flag A | `0xC03E7B` | `1` |
| enable flag B | `0xC03E90` | `1` |
| window `N` | `0xC03E80` | `180` (days) |
| reference year | `0xC03E84` | `2026` |
| reference month | `0xC03E88` | `4` |
| reference day | `0xC03E8C` | `7` |

Three neighbouring bytes (`0xC03E78`/`79`/`7A`) are also `1`. Nothing in the code writes these — the only write anywhere near them is the gate clearing flag B (`0xC03E90`) after a pass.

**[bin][inf]** So this build's reference date is **2026-04-07** (its engine build date) and the window is **180 days**, i.e. it is valid until **2026-10-04**. Both enable flags are set, so the check runs. At any clock past 2026-10-04 — today included — `now − reference > 180 days`, the gate returns true, and its caller skips the normal boot init toward the one-frame quit. This **is** the empirically observed clock gate: holding the guest clock on or before 2026-10-04 lets boot proceed (and the connector dial); at the real clock the engine date gate trips and the client quits after one frame. It is a native, self-contained check — no connector or certificate involved — which settles the earlier TLS-versus-engine ambiguity in favour of the engine gate. Source: confirmed by the v7 runtime-dump thread's read of the data, re-verified here against the unpacked image.

### The same gate across all seven builds

The v7 runtime-dump thread read the gate's globals for every build. The same `now − reference > N days` check is present in each; the reference is each build's own engine date, and one build ships with the gate disabled:

| build | reference date | state |
|---|---|---|
| 548 | 2022-10-17 | active |
| 610 | 2022-04-22 | **dormant** (enable byte 0) |
| 612 | 2023-10-17 | active |
| 613 | 2024-04-15 | active |
| 614 | 2024-04-15 | active (`N = 180` → valid to 2024-10-12) |
| 71243 | 2024-10-15 | active |
| latest (Unity 6000) | 2026-04-07 | active (`N = 180` → valid to 2026-10-04) |

Where `N` is reported it is **180 days**. Build 614 gives the sharpest black-box check: with `N = 180`, `reference + 180 days = 2024-10-12`, and the test is strict (`>`), so a guest clock of **2024-10-12 boots** and **2024-10-13 skips init and quits**. That one-day flip is the cleanest confirmation available if a lab clock test is ever run (headroom permitting). Source: v7 runtime-dump thread; the latest-build values re-verified here.

### The quit reason is native, and the instant-quit literal is `QuitInstant`

**[bin]** `Quattro.UQuattroUnityBridge.Quit(string reason)` resolves to a known method in the unpacked GameAssembly (`script.json` signature `void …Quit(System.String* reason, const MethodInfo*)`), but it has **no callers in managed `.text`**. It is invoked by the native engine across the bridge, so the `reason` is engine-supplied, not a managed literal.

**[bin][inf]** The engine's quit handler logs `Do Quit` and assembles a `reason=` string; the concrete instant-quit reason literal is **`QuitInstant`** (the string `reason=QuitInstant` is appended at the quit site), paired with the GS2 script event name `Adventure_quit_Instant`. So the one-frame boot teardown is the engine's own `DoQuit`, and `QuitInstant` is the reason value it carries across the bridge.

### For a live debugger: where to break and what to read

The one thing static analysis can't give — the runtime values of the gate's inputs — is a few breakpoints away for anyone with a live v7 session (Bochs/QEMU, or the unpacked engine substituted in). RVAs below are in the unpacked `Graal3DEngine.dll` analysis image; rebase to the loaded engine's base at run time, or locate the routines by their landmarks (the `_time64`/`_localtime64`/`_mktime64` CRT-thunk cluster, and the `difftime` result compared to a `.rdata` `60.0/60.0/24.0` product). **[bin]**

- **Gate function — RVA `0x36878`** (the call site) into the gate body at **`0xb29b0`**. The return value (AL) is the expired/true verdict.
- **Reference-date builder — RVA `0xb24c0`.** The `tm` fields come from globals **`year @0xC03E84`**, **`month @0xC03E88`**, **`day @0xC03E8C`** (as written: `tm_year = year − 1900`, `tm_mon = month − 1`, `tm_mday = day`). `_mktime64`'s return is the reference `time_t`.
- **Window `N` — global `@0xC03E80`** (the `difftime` threshold is `N × 86400 s`). **Enable flags — `@0xC03E7B` and `@0xC03E90`**; if either is zero at the gate, the check is disabled.

These globals are initialised data, and their values for this build are read out above (reference `2026-04-07`, `N = 180`, both flags `1`). A clock test (boot at either side of `reference + N days`, read `Player.log` for boot-proceeds vs the one-frame `DoQuit`) is the black-box cross-check of the same thing.

## How this was checked

**[bin]** Static read with a small PE32+ reader (section names and entropy, import/export directories, string searches) of the two unpacked modules of the latest Unity 6000 build, and symbol/context reads of the corrected-run `dump.cs` (class and `TypeDefIndex` for each cited field/method). **[cap]** The unpack, the IL2CPP reconstruction and the member-count validation were produced by earlier isolated lab-VM runs (unpacker and dumper only; `Worlds.exe` was not launched; no network). The tools were not re-run for this note, and no raw dump, private hash or lab path is reproduced here.

## Still open

- **The quit reason string** — *answered above:* `Quit(string reason)` has no managed callers, so the reason is native; the instant-quit literal is `QuitInstant` (`reason=QuitInstant`), paired with the GS2 event `Adventure_quit_Instant`. Residual: confirm the exact reason the expiry path itself passes, versus the script-driven `QuitInstant`.
- **The native date comparison** — *answered:* `now − reference > N days`, with the inputs recovered as initialised data — reference **2026-04-07**, `N = 180` days (valid until **2026-10-04**), both enable flags set, so the gate is **active** and trips at any clock past 2026-10-04. Confirmed by the v7 runtime-dump thread and re-verified here.
- **The connector signing key.** Still the gating secret for an online repro; unchanged by this note. The signed-reply capture remains the one runtime step, and the key swap stays a private, owner-run task.
