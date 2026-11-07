# Skipped v6 listings: a QPlay export directory, not the engine

Date: 2026-11-07. Static read of the packed uploads `Graal 6.0.3.7.exe` and `Graal 6.1.1.3.exe`. The unpacked Windows 6.00 engine is `engine-600r2.md` and `engine-600r4.md`. An earlier pass on these two files is `packed-6037.md` and `packed-6113.md`. Nothing was run. Tags: **[bin]**.

The two files are distinct. They share a stub shape. They do not share an import, and the later file's export list is larger.

## The stub

Entry calls one helper and then executes a breakpoint. The helper looks at the byte at its return address. When that byte is the breakpoint opcode, it clears the byte and walks four kilobytes, a dword at a time, xoring each dword and then adding a second constant. The helper does not allocate memory, change page protection, or jump to another entry. The decompiler does not show a second image past that breakpoint.

The file labeled 6.037 imports `DebugBreak` and nothing else. The file labeled 6.113 imports `SetCurrentDirectoryA` and nothing else, and the recovered stub does not call it.

The section names are not `UPX0` and not `.text`. Each image has two scrambled section names plus `.rsrc` and `.idata`.

## The export directory

Both export directories are named `QPlay.exe`. The version resource in the same image still calls the file `Graal.exe`. The directory is a TLS and compression surface. It is not a list of Graal classes.

The 6.037 names are C. They cover a CyaSSL context, certificates and keys, an SSLv3 client method, connect, read, write and shutdown, plus RSA, ARC4, MD5, SHA, a random generator, and zlib's inflate and deflate.

The 6.113 names are C++, under a `CyaInt` namespace, with a few cipher calls left unmangled. The surface adds TLS 1.0, TLS 1.1 and TLS 1.2 client methods, an SSLv23 client method, DTLS peer and timeout calls, OCSP, AES-CBC, HMAC, SHA-256, and a nonblocking read. Its zlib names include `inflateUndermine`, `inflateReset2` and a 64-bit CRC combine, which the 6.037 list does not.

The bytes at those exports are not that library. Bodies that decompiled are broken instructions, an empty return, or a breakpoint. One 6.113 name, the debugging-off entry, did not decompile: the flow was longer than the decompiler allows. A Windows assembly manifest is present. Its requested execution level is not recovered as text.

## Absent from both

No `quattro_lib` path, no `Quattro_Play` string, no OpenGL or Direct3D import, no FMOD, no GS2 control name, no `TSocket`, no Torque class, no Delphi form, and no protocol id. The engine of the unpacked 6.00 builds is not in these two listings.
