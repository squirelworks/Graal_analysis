# Packed Windows Graal 6.037 is a stub

Date: 2026-11-07. Static read of the upload `Graal 6.0.3.7.exe`. Nothing was run. Tags: **[bin]**.

## What this file is

The version resource says product Graal, file version and product version 6.037, original file name `Graal.exe`, company Linux Cyberjoueurs, copyright year 2012. That is the 6.03r7 Windows build already identified in `protocol/v6x-clients.md`. **[bin]**

The decompile is not that client. The entry clears one byte, runs a dword xor-and-add over a fixed block, then breakpoints. The functions named from that image are a CyaSSL and CTaoCrypt surface (context setup, certificates, RSA, MD5, ARC4, SHA, a random generator). Their bodies are broken instructions, empty returns or infinite loops, not the library and not `quattro_lib`. No Graal class, no OpenGL, no GUI, no Torque name. **[bin]**

The engine of this generation was read from the Linux 6.03 build in `protocol/v6x-clients.md`, not from this export. **[bin]**
