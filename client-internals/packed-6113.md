# Packed Windows Graal 6.113 is a stub

Date: 2026-11-07. Static read of the upload `Graal 6.1.1.3.exe`. Nothing was run. Tags: **[bin]**.

## What this file is

The version resource says product Graal, file version and product version 6.113, original file name `Graal.exe`, company Eurocenter Games, copyright year 2014. **[bin]** Mac 6.11 in `protocol/v6x-clients.md` is bundle version 6.111, same publisher and year. This file's version is 6.113.

The decompile is the same kind of packer stub as `packed-6037.md`: the entry runs a dword xor-and-add over a fixed block, then breakpoints. The names on that stub are a larger CyaSSL and CTaoCrypt surface than 6.037, including AES-CBC, SHA-256 and HMAC, plus mangled CyaSSL C++ entry points. Bodies that decompiled are broken instructions or empty returns; one did not decompile. There is no `quattro_lib`, no GUI, no OpenGL draw path and no Torque name. **[bin]**

This export does not show how the 6.113 engine is split. The Mac 6.11 connector in `protocol/v6x-clients.md` is a different binary. **[bin]**

A later read of the same listing, after the 2026-11-07 gap archive, is `engine-6113.md`. The archive did not add an unpacked image.
