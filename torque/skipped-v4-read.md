# The two skipped v4 exe listings are one Thinstall loader

Date: 2026-11-07. Static read of the uploads labeled `Graal 4.04r2.exe` and `Graal v4.20r8[Windows].exe`. Nothing was run. Tags: **[bin]**.

The 4.04r2 engine, the Delphi launcher and `Graal3DEngine.dll` stay the reads in `protocol/v4x-clients.md` and `graal3d/torque-engine-4x.md`. This note is the program inside these two listings.

## One listing

The decompiled C files are the same bytes: 102,537 bytes, 3,706 lines. The HTML listings are the same bytes as well. The two labels are one program. Nothing in either listing distinguishes them.

## What the loader does

It is the outer loader of a Thinstall bundle, the same layer the 4.04r2 installer note describes. **[bin]** (`protocol/v4x-clients.md`)

The entry asks for the module handle and calls the loader. The loader builds an eight-character environment name, `TS_LOADER`, from immediate bytes. When that variable is set, it opens the path the variable holds. Otherwise it opens its own module path. A failure formats the system message, shows it in a message box titled with that path, and exits the process.

It reads the DOS header, seeks to the optional header, and treats `LoaderFlags` as a file offset. From there it reads a 56-byte table. The first dword has to be the Thinstall package magic `0x82D0B188`. A short read or any other value takes the same message-box exit.

The table's first record is one payload: a file offset, an unpacked size and a packed size. The loader allocates an executable image for the unpacked size and a scratch buffer, then decodes. A leading `0xD9` copies the bytes through. Any other tag runs the range-coded decoder: tagged blocks, a probability model that refills its range, and filters that classify rising and falling runs of bytes and of words. The scratch buffer is released afterwards.

The decoded image is relocated (high half, low half, and the full 32-bit relocation). Each imported DLL is loaded, the import slots are made writable, and each procedure is resolved by name or by ordinal. A missing DLL or a missing named procedure is the message-box exit. The loader then calls the unpacked image's entry point.

## What is in the clear

The import directory is the loader's own kernel32 and user32 calls, plus one import from each DLL of the wrapped program. Those extra DLLs are the registry (`RegQueryValueExA`, `RegSetValueExA`), the shell (a special-folder lookup and `ShellExecuteA`), the save-file dialog, an image list, an OLE stream and OLE variants, the joystick (`joyGetPosEx`), the printer spooler and GDI. Winsock, DirectDraw and OpenGL are not among them.

The version resource names the file `Graal.exe`, the product Graal, and the description a Graal Online client, with company Linux Cyberjoueur. That is the wrapped program's identity sitting in the stub. It is not a class list.

## What this listing does not contain

No Delphi method, no `TForm`, no Torque class, no `graal_set`, no protocol id, no `GraalEngine.dll`, no `Graal3DEngine.dll`, and no file directory. The inner stub, the bundled files and `thinstall.log` are not plaintext here. The compressed payload was not decoded; this pass did not run the decoder.
