# Unpacked Windows 6.1.1.3

Date: 2026-11-07. Static read of the upload `unpacked_Graal 6.1.1.3.exe.zip`. Nothing was run. The archive was not committed. Tags: **[bin]**.

The packed listing of this same release is `packed-6113.md`, `skipped-v6-read.md`, `engine-6113.md` and `decompile-6113.md`. Those notes describe a packer stub. This note is the later listing in which the engine body is readable.

## What was supplied

One zip, 42,380,990 bytes. It holds two Ghidra listings and no executable: a C listing of 11,559,691 bytes and an HTML listing of 535,686,460 bytes. Both name the image `unpacked_Graal 6.1.1.3.exe`. There is no second file, no `GraalEngine.dll`, and no companion DLL in the archive. **[bin]**

## What the image is

One 32-bit Windows GUI program. The header characteristics are a normal executable with relocations, line numbers and local symbols stripped. The optional header says subsystem Windows, operating system 5.0, subsystem 5.0. The linker field is major 9, minor 0. The virtual image is 6,504,448 bytes, of which the code field is 2,623,488 and the initialized-data field is 696,832, and the headers are 1,024 bytes. Seven sections: `.text` (virtual 3,403,776, raw 3,318,784), `.rsrc` (4,096), `.idata` (virtual 4,096, raw 512), one blank name (virtual 1,662,976, raw 1,658,368), `fbndyrix` (virtual 1,425,408, raw 1,417,728), `tlrwuvpz` (virtual 4,096, raw 1,024) and `.SCY` (virtual 8,192, raw 7,680). The header marks `.text` as initialized data and marks `.SCY` as code. **[bin]**

The version resource, US English Unicode string table:

| Field | Value |
| --- | --- |
| File description | Graal |
| Internal name | Graal |
| Product name | Graal |
| Original file name | `Graal.exe` |
| Company | Eurocenter Games |
| Copyright | 2014 |
| File version string | `6.113` |
| Product version string | `6.113` |

The fixed version words are major 6, minor 1, build 1, revision 3, for both the file version and the product version. That is 6.1.1.3, the same release the string table shortens to `6.113`. **[bin]**

Two compiler strings sit with the draw-profiler names: `Aug 8 2014` and `17:16:33`. The image timestamp is 8 August 2014, 13:19:46 UTC. The recovered runtime helpers are labelled as the Visual Studio 2008 release library; the same comments also name the 2005 release, and the exception prolog is the helper shared by Visual Studio 2005 through 2012. **[bin]**

The header entry is the Visual C++ security-cookie initializer. It reads the system time, the process id, the thread id, the tick count and a performance counter, mixes them into the cookie, and returns. It does not clear a breakpoint or walk four kilobytes. The listing recovers about 9,300 functions and fails to decompile two. **[bin]**

## Same stamp as the packed stub

The packed 6.113 listing and this one share the version resource, the 8 August 2014 timestamp, the virtual image size 6,504,448, the code field 2,623,488, the initialized-data field 696,832, the 1,024-byte headers and linker major 9. The packed note counted six sections and no readable engine. This listing has seven: `.text` and `.SCY` are named as well as the blank section, `.rsrc`, `.idata`, `fbndyrix` and `tlrwuvpz`. **[bin]** (`client-internals/engine-6113.md#what-this-file-is`)

| | Packed 6.113 listing | This listing |
| --- | --- | --- |
| What was read | Packer stub, 106 functions | Engine body, about 9,300 functions |
| Entry | Clears a breakpoint byte, mixes four kilobytes, then breakpoints | Security-cookie initializer, then returns |
| Version | `6.113`, words 6.1.1.3, Eurocenter Games, 2014 | The same resource |
| Stamp | 8 August 2014, 13:19:46 UTC | The same timestamp, plus compiler strings `Aug 8 2014` and `17:16:33` |
| Shape | Six sections, no named `.text` | Seven sections, `.text` and `.SCY` named |

## The engine is visible

This is not a second program and not a DLL split. The original file name is `Graal.exe`. The body is the `quattro_lib` program already described for unpacked 6.00: source paths under `quattro_lib`, the name `Quattro Play`, `TSocket`, `TServerPlayer` and the other `TServer*` world objects, `GuiGraalCtrl`, `StartScript_GraalGui`, OpenGL startup text, an FMOD open-failure string, and `d3d9.dll` loaded by name. The script cache magic `GRESCR01` is present. A CyaSSL cipher-name function decompiles here; in the packed listing those export names did not have library bodies. **[bin]** (`client-internals/engine-600r2.md#what-the-export-is`)

The connection, the GS2 dispatcher and the Torque-name diff are the later notes on this same image. **[bin]**

## Packer names that remain

The image is not a clean rebuild. The export directory is still named `QPlay.exe`, and that directory sits in the section `fbndyrix`. The import directory sits in `.SCY`, not in the short `.idata` section. No product string `Themida` appears among the `quattro_lib` type names. The blank section still holds packer strings: `Themida`, `WinLicense`, a WinLicense registry key, and Oreans driver names (`oreans32.sys`, `oreansx64.sys`, `oreans.vxd`). **[bin]**
