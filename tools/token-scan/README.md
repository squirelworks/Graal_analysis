# token-scan

Static login-token readers for the G3D clients (3.x to 6.01). The method, its limits and the builds it was checked on are in [protocol/login-tokens-3x-7x.md](../../protocol/login-tokens-3x-7x.md#reading-the-token-from-a-file).

- `conntok.py`: Linux ELF clients (32-bit and 64-bit). It reads the eight one-character strings after the "Connecting to the game server" reference. Run it as `python3 -I conntok.py <files>`.
- `g3dref.py`: Windows engine DLLs (`GraalEngine.dll`, `Graal3DEngine.dll`) and 32-bit ELF. It looks for runs of references to one-character strings that spell `G3D` + `DDMMY`. It needs `pefile` for PE files. Run it as `python3 -I g3dref.py <files>`.

Keep the scripts and the binaries in separate folders, and run them with `-I`.
