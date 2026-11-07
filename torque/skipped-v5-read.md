# Skipped v5 listings: forms, a packer entry, and FMOD's exports

Date: 2026-11-07. Static read of `Graal 5.12.exe`, `Graal 5.2.4.3.exe`, `Graal v5.24r4.exe`, and `fmod.dll` inside the 5.0.0.7 archive. The 5.0.0.7 engine DLLs and the unpacked 5.30 and 5.31 exes are other notes. Nothing was run. Tags: **[bin]**.

The three executables are three programs. Each recovered entry is overlapping instructions that the decompiler cuts on a bad instruction. Each import directory binds only `LoadLibraryA` and `VirtualAlloc`, and the recovered body never reaches either call. Past that, the listings diverge.

## The 5.12 resource directory

`Graal 5.12.exe` is distinct from the other two. The code that decompiled is the overlapping entry and two helpers that fall into the same bad instruction. There is no second image and no jump to an unpacked entry in the recovered functions.

The resource directory is in the clear, and it is a Delphi executable's. The named resources include the forms `TGRAALWINDOW`, `TPLAYERLIST`, `TPLAYERLISTOPTIONS`, `TOPTIONS`, `TPROFILEEDIT`, `TOPENURL`, `TCONTROLSFRAME` and `TSHORTMESSAGE`, plus Delphi's `DVCLAL` license block and `PACKAGEINFO`. The usual dialog resources are there too: the button ids and the drive-type names. Two resource strings at high ids are not readable text.

No Torque class, no `graal_set`, no Winsock import, no DirectDraw or OpenGL import, and no protocol id. This zip has no engine DLL. The listing does not name MoleBox, and it does not show the file-hook layer.

## The later packed exes

`Graal 5.2.4.3.exe` and `Graal v5.24r4.exe` are distinct from each other and from 5.12. Both keep the same two kernel32 imports. Both entries are overlapping instructions and stop on a bad instruction, so the decompiler never shows an allocate or a jump.

The 5.24r4 entry is the larger of the two. It keeps a stack temporary of about twelve thousand slots, chains calls into the middle of its own bytes, and still does not call `LoadLibraryA` or `VirtualAlloc`. The 5.2.4.3 entry is a shorter chain of the same kind and stops the same way.

Neither resource directory names a form, a Delphi unit, a Torque class, a socket, or a protocol id. The version block is present. Nothing else of the client is.

## fmod

The `fmod.dll` listing in the 5.0.0.7 archive is the same bytes as the `fmod.dll` listing in the 4.2.0.8 archive, both the decompiled C and the HTML. One program, described once.

The section names are `UPX0`, `UPX1` and `.rsrc`. On process attach, the entry is an UPX decompressor. It expands a bitstream of literal bytes and matches into the unpacked image, rewrites call and jump slots so they point into that image, walks a name table with `LoadLibraryA` and `GetProcAddress`, and applies relocations. If `GetProcAddress` fails it returns without finishing. The decompiler then stops on a bad instruction, before the original entry.

Imports left in the clear, besides `LoadLibraryA` and `GetProcAddress`, are `mixerOpen`, `acmStreamOpen`, `CoInitialize`, `ShowWindow`, `RegCloseKey`, `abs`, and one WinSock import by ordinal. That is a sound library that also opens a mixer, the audio-compression manager, COM, a window, the registry and a socket.

The export names are FMOD's API: samples and channels, streams, a 3D listener, DSP and effects, CD audio, recording, and module music. The stream exports include net-stream calls (a proxy, a timeout, server status, a metadata callback). The version resource names the file `fmod.dll` and the product FMOD, from Firelight. The bodies of those exports are not in the decompile.

No Graal class, no Torque name, and no Graal protocol id.
