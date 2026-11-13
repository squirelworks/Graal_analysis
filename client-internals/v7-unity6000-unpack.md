# v7 Worlds, Unity 6000 build: the native unpack and why IL2CPP names don't come out yet

Date: 2026-11-14. Tags: **[bin]** read from the original or unpacked file · **[cap]** produced by an earlier run in an isolated lab VM (no network, no game start; the tools were run against the DLLs, `Worlds.exe` was not launched) · **[inf]** inferred.

[v7-gameassembly-il2cpp.md](v7-gameassembly-il2cpp.md) (added in squirelworks/Graal_analysis#463) reads builds 548–71243 and notes that the current installed Worlds client "is packed only and was not read". This note covers that client: how its two Themida-wrapped modules were unpacked, what the result is, and where reading the IL2CPP names stopped.

## The build

**[bin]**
- The unpacked GameAssembly carries the Unity version string `6000.0.63f1`.
- Both PE stamps are from April 2026: GameAssembly on 3 April, `Graal3DEngine.dll` on 7 April. Earlier builds share one stamp across both modules; this build does not.
- The engine plugin's export-directory name is `Graal3DEngineFlavor0.dll`, as in 71243, and it is still loaded under the file name `Graal3DEngine.dll`.

## Unpacking

**[cap]** Both modules were unpacked with the public Unlicense 0.4.0 tool (Themida/WinLicense 3.x support), one DLL at a time. It ran with a 60-second dump timeout and no forced entry point, patch or manual repair. The tool reported Themida 3.x on both, resolved the imports and rebuilt each PE.

**[bin]** What the outputs look like, compared with the originals:

| | GameAssembly packed → unpacked | Graal3DEngine packed → unpacked |
|---|---|---|
| Size | 25.7 MB → 77.9 MB | 8.0 MB → 26.7 MB |
| Sections | blank-named sections plus `.exports`, `.imports`, `.tls`, `.themida`, `.boot`, `.reloc` → the same plus a leading `.text` and a trailing `.SCY` | the same pattern (with `.rsrc`) |
| Named exports | 371 → 371 (241 `il2cpp_*`) | 309 → 309 (no `il2cpp_*`) |
| Import descriptors | 15 → 15 | 21 → 29 |
| Relocation directory | 16 bytes → 16 bytes | 16 bytes → 16 bytes |
| Printable strings (8+ chars) | 7,174 → 35,765 | 2,139 → 21,021 |

- **The section shape matches older builds.** The unpacked shape (added `.text` and `.SCY`, with the Themida sections left as dead weight) is the same as the 548–71243 images in #463 and the 6.x exes in [themida-pack.md](themida-pack.md). **[bin]**
- **The code really came out.** String content multiplies by five to ten times. The unpacked engine holds the Graal world types (26 `TServer…` names such as `TServerBomb`, `TServerChest`, `TServerCarry`) and the `Quattro.Graal` binding names. **[bin]**
- **Not proven runnable.** The relocation directory is only 16 bytes in both the packed and the unpacked files, so the dumps are fixed to the base they were dumped at. Unlicense also logged two invalid-memory-read errors per module during import emulation. Treat both outputs as analysis images, not runnable replacements, and do not assume every import is recovered. **[bin][cap]**
- **The engine has more import descriptors after unpacking (21 → 29).** That is expected: the packer hides part of the real import table. **[inf]**

## IL2CPP metadata: version 31

**[bin]** The client's `global-metadata.dat` is in the clear, with the normal magic. It is **version 31**. All six builds read in #463 are version 29; the 71243 file was rechecked here and is 29.

**[cap]** Il2CppDumper 6.7.46, whose source accepts versions up to 31, was run on the unpacked GameAssembly with that exact metadata file, without forcing a version. It recognized version 31 and found registration candidates. It then failed in generic-type resolution and did not write `script.json`, `il2cpp.h` or the dummy DLLs.

**[bin]** The partial `dump.cs` it left is 3.55 MB, with 2,543 type entries and 16 `NullReferenceException` markers. Do not use it as a type hierarchy.

So the Unity 6000 client is unpacked, but its C# names are not readable with current public tooling. The open question is whether the cause is:
- a Unity 6 / metadata-31 layout that Il2CppDumper doesn't fully handle,
- damage in the recovered image, or
- a mistake in locating the registration structures.

This run does not decide between them. **[inf]**

## What still holds from #463

GameAssembly still exports the 241 `il2cpp_*` API names, and the engine plugin is still a separate native module with its own 309 exports. That is consistent with #463's picture of the native engine driving Unity through generated bindings. **[bin]** **[inf]** None of the 6000-build specifics (callback table, binding counts) were checked here.

## How this was checked

Static read with a small PE32+ reader (section names, export and import tables, relocation directory, printable-string counts, string searches) of the original installed `GameAssembly.dll`, engine plugin and `global-metadata.dat`, and of the two unpacked outputs of an earlier isolated lab-VM run in which only the unpacker and the IL2CPP dumper ran (`Worlds.exe` was not launched, no network). The partial dump was only counted. The tools were not re-run for this note.

## Still open

- **Registration check.** Validate the code- and metadata-registration arrays (pointers and counts) in the unpacked GameAssembly against the version-31 metadata, before changing any parser.
- **Names in the clear.** Search the unpacked engine for the login token and user-agent. A plain-string search found no `Graal/…` user-agent and no `onSend…` names, so they may be built at run time or obfuscated.
- **Callback table.** Compare this build's callback table and exports with 71243 once the names can be read.
