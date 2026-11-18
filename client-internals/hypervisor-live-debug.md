# Live-debugging the Themida-protected clients from outside the guest (Bochs vs QEMU/KVM vs in-guest tools)

Date: 2026-11-18. Tags: **[lab]** done in an isolated, headless lab VM (no network card, files moved in on CD images) · **[cap]** read from that lab's logs and debugger output · **[doc]** tool documentation · **[inf]** inferred, not tested.

Question: can Bochs be used to live-debug v7 Worlds (Unity 6000, x64, Themida on `GameAssembly.dll` and `Graal3DEngine.dll`) and 6.113 (32-bit, Themida/WinLicense), and if not, what should be used instead?

## Short answer

**Use QEMU with KVM and its built-in gdb server (gdbstub), and set hardware breakpoints and watchpoints from the host.** That gives what Bochs promises (a debugger the guest cannot see) at near-native speed, and it was proven on v7 here: the engine's date gate was stopped at entry in a running client and its inputs and result read live, with no debugger, driver or hook inside the guest. **[lab]**

Bochs is not worth setting up for these targets. Its only advantage over KVM is full-system instruction tracing, which these questions do not need, and it costs one to two orders of magnitude in speed on a target that has to boot Windows 10 x64, run Themida's unpacker and start Unity. On the lab host the distribution's Bochs 2.8 package did not even get through its BIOS (details below). **[lab]**

| Target | Recommended | Fallback | Not recommended |
|---|---|---|---|
| v7 Worlds, x64 Unity 6000 | QEMU/KVM gdbstub, hardware breakpoints from the host, plus guest memory snapshots | QEMU TCG with the same gdbstub (no KVM), if a step needs instruction-level tracing | Bochs (too slow, no GPU, package broken on the host); in-guest x64dbg (an arms race with Themida's anti-debug) |
| 6.113, Win32 under WOW64 | Same as v7 (the 32-bit process runs in the same 64-bit guest) **[inf]** | An XP guest under QEMU/KVM if the client needs XP-era behaviour | Bochs, for the same reasons; Frida inline hooks (Themida checks its code) |

## What was done on v7 **[lab]**

Setup: a copy-on-write overlay of the existing Windows 10 (19045) lab disk, 2 vCPUs, 3 GB RAM, standard VGA, no network card, KVM on, and QEMU's gdb server on a loopback port. The v7 build went in on a CD image and was copied to the guest disk. The guest clock was set inside Windows.

1. **The build needs the VC++ 2019 x64 runtime.** On a bare Windows 10 the engine plugin fails with `DllNotFoundException ... Graal3DEngine` (the loader cannot find `VCRUNTIME140_1.dll`), and the Backtrace crash-reporter plugin fails the same way. The redistributable shipped inside the official Worlds installer fixes both. Without it the run looks like an early quit, and that is misleading.
2. **Finding the engine at run time.** Windows places the engine DLL at a different base on each launch in this guest, so fixed addresses are useless. The method that worked:
   - take one guest memory snapshot (`dump-guest-memory` over QMP, about 15 s for 3 GB) and run Volatility 3 on it to get `ntdll`'s base and exports. `ntdll` is at the same address in every process for the whole boot;
   - set a hardware breakpoint on `ntdll!LdrLoadDll`. On each stop, read the current thread's TEB from the `gs_base` register that QEMU exposes, follow the PEB to the loader's module list, and check for `Worlds.exe` and `Graal3DEngine.dll`. Once the engine shows up, its base is known, and the real breakpoints can be armed. In practice this takes a few hundred `LdrLoadDll` stops, a few seconds in all.
3. **Reading the date gate.** With the base known, a hardware breakpoint on the gate routine (found from its landmarks in [the startup-gate note](v7-il2cpp-names-and-startup-gate.md)) stopped the client before the check ran. The breakpoint then moved to the return address to read the verdict, and the six input values were read before and after the check. The values and the two clock runs are recorded in that note's "Live confirmation" section: both flags 1, `N` = 180 days, reference 2026-04-07; a pass returns 0 and disarms the second flag, and an expired clock returns 1.
4. **What the watchpoints showed about Themida.** Read/write watchpoints placed on the same data bytes fire first inside the `.themida` section, while the bytes still hold ciphertext. The packer's decrypt loop restores them, and only then does the engine's own code read them. This is the "writer" that a static scan of `.text` cannot find, and it is invisible to anything that only reads the unpacked file.
5. **Nothing in the guest noticed.** No debugger process, driver or hook was present in the guest, and the client behaved the same with and without the breakpoints. On the April clock it crashed at the first render frame both with and without them (see the D3D section below). KVM handles the hardware breakpoints in the host, and the guest does not see them in its own debug registers. **[inf]** That last point is from how KVM guest debugging works; it was not checked separately against Themida's debug-register checks.

Limits met:

- **Four hardware slots.** x86 has four debug-address registers, so at most four breakpoints and watchpoints can be armed at once. Plan the stops in phases, and swap the set between phases.
- **Watchpoints stop on every access.** A watchpoint armed from process start also stops on each step of Themida's decrypt loop. That is slow (one host round trip per stop) but finite. Arming the watchpoints after the engine has loaded avoids it.
- **Virtual addresses belong to the current process.** gdb reads memory through whatever page tables are active when the guest stops. Check that the stop is in the target process (via the TEB/PEB) before trusting a read.
- **Snapshots are big.** A 3 GB guest gives a 3 GB snapshot. Keep snapshots private and delete them after use.

## Why not Bochs **[lab]** **[doc]**

- **The package on the lab host is broken.** The distribution's Bochs 2.8 with its bundled BIOS image triple-faults inside the BIOS's 32-bit setup stage, before anything appears on screen and before the disk is read. This happens with a 64-bit CPU model and 2 GB, with 1.5 GB, with the default CPU and 64 MB, and with the SeaBIOS image that ships alongside. Working around it means building Bochs and its BIOS from upstream source. That is possible, but it was not worth doing given the next points.
- **Speed.** Bochs interprets every instruction. Its status bar showed single-digit millions of instructions per second in the BIOS on a loaded host. Even at the tens of millions per second it reaches on an idle modern CPU, booting Windows 10 x64 (well over 10^11 instructions) takes hours. Themida's unpacker and Unity's start-up then add a large multiple of that before the date gate runs. **[inf]**
- **No GPU, and software D3D does not save v7.** See the next section. Bochs's VGA/VBE device would give Windows the same Basic Render Driver as QEMU's standard VGA, with the same first-frame crash, only much slower.
- **What it would add.** An instruction-level debugger and tracer that the guest cannot see. For these targets, KVM's hardware breakpoints cover the same need, and QEMU TCG (QEMU's own CPU emulator, with the same gdbstub) is the step to take if instruction-level single-stepping across protection code is ever needed.
- **Operational gotchas, for the record.** This build of Bochs starts at its internal debugger prompt, so it needs `c` on standard input to run headless. Its RFB/VNC display binds on all interfaces, not loopback, so the X display under Xvfb is the safer headless choice. Bochs cannot read qcow2 images; convert to a sparse raw image and use `volatile` mode so the conversion is not modified.

## Software D3D (WARP) for v7 **[lab]**

Windows in a VM without a GPU driver uses the Microsoft Basic Render Driver. That driver provides Direct3D 11 (feature level 11.1) through WARP, and Unity reports it as the active device.

- **Up to the gate:** fine. Plugin load, `OpenPlugin`, and the engine's start-up, including the date gate, all happen before any frame is rendered.
- **Inside the date window:** the build crashes in the URP render pipeline's first frame (`RenderPipelineManager.DoRenderLoop_Internal` → Unity crash handler), with or without `-batchmode -nographics`. So a full software-rendered session of the latest v7 is not available in this setup.
- **After expiry:** the client never builds the render pipeline. It sits on a black window, so there is no crash.

So software D3D is good enough for any start-up or connector-side question, but not for anything that needs v7 to actually draw. For that, use a guest with a real or paravirtual GPU (or a native Windows run), not Bochs.

## In-guest alternatives

- **x64dbg with ScyllaHide (user mode) or TitanHide (kernel driver).** These work, but they are an arms race. Themida checks for debuggers in many ways, and TitanHide needs a test-signed driver loaded in the guest. They are worth it only when you need an interactive debugger UI on code that the hypervisor method already located. **[doc]** **[inf]**
- **Frida.** Useful for read-only memory scans and for hooking non-protected modules (the Unity runtime, the C runtime). Inline hooks inside the Themida-protected modules are detected, as recorded in earlier v7 lab notes. **[cap]** (from earlier notes)
- **Static first.** Both protected v7 modules and 6.113 have already been unpacked for analysis, so most questions are static ones. The hypervisor method is for the few values that only exist at run time, or for confirming a static reading.

## Moving files in and out

- **In:** build a CD image on the host (`genisoimage -J -R`), attach it at boot, or swap it live from the QEMU monitor (`change <cd-device> <file>`), then copy it inside the guest. No network card and no shared folders are needed.
- **Out:** read results from the host side (gdb output, memory snapshots). For guest files such as `Player.log`, print them in a guest console and take a screen dump, or write them to a second, writable disk image.
- **Keep the base disk read-only.** Do all runs in a copy-on-write overlay, so the shared lab image is never touched.

## 6.113 notes **[inf]**

The same method applies unchanged, with one difference: 6.113 is a 32-bit process under WOW64. Its 32-bit TEB and PEB sit next to the 64-bit ones (the 32-bit TEB is a fixed distance after the 64-bit TEB), and its modules are listed in the 32-bit loader list. The other route is to break on the 64-bit `ntdll` loader routine, which still sees every load. Hardware breakpoints compare linear addresses, so they behave the same for 32-bit code. This was not run in this pass. The connector decision point is already documented statically ([connector script](../protocol/connector-script.md), [unpacked 6.1.1.3](unpacked-6113.md)), and the live confirmation there is a follow-up.

## Not settled here

- A from-source Bochs build was not attempted, so the true time for Bochs to reach the v7 gate is an estimate, not a measurement.
- Whether Themida's debug-register checks could ever see KVM guest-debug breakpoints is inferred from KVM's design. The live runs showed no behaviour change, but no targeted test was made.
- 6.113 under this method is untested.
