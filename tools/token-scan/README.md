# token-scan

Static login-token readers for the G3D clients (3.x to 6.01). The method, its limits and the builds it was checked on are in [protocol/login-tokens-3x-7x.md](../../protocol/login-tokens-3x-7x.md#reading-the-token-from-a-file).

- `conntok.py`: Linux ELF clients (32-bit and 64-bit). It reads the eight one-character strings after the "Connecting to the game server" reference. Run it as `python3 -I conntok.py <files>`.
- `machotok.py`: Mac OS X clients (Mach-O, thin or universal; PPC, i386, x86_64). The same connect-routine read. On PPC it follows the register pairs that build each address. For 6.x universal files use the x86_64 slice. It falls back to the 6.03 scramble. Run it as `python3 -I machotok.py <files>`.
- `g3dref.py`: Windows engine DLLs (`GraalEngine.dll`, `Graal3DEngine.dll`) and 32-bit ELF. It looks for runs of references to one-character strings that spell `G3D` + `DDMMY`. It needs `pefile` for PE files. Run it as `python3 -I g3dref.py <files>`. For the unpacked single-exe Windows 5.30r3, 6.00r2 and 6.00r4 images, add `--all-sections`: those dumps flag their code section as data. All three read `G3D26090`.

- `iostok.py`: 32-bit ARM iPhone clients (decrypted Mach-O from an IPA's `Payload/*.app`). The same connect-routine read in ARM mode, following literal-pool string addresses and the stack slots that hold repeated characters. It reports App Store-encrypted files and skips them. It needs `capstone`. Run it as `python3 -I iostok.py <files>`. Belote 1.2 and 1.50 read `G3D04048`, and Classic+ 1.13 reads `G3D0208A` ([note](../../client-internals/iphone-version-tokens.md)).

Keep the scripts and the binaries in separate folders, and run them with `-I`.
