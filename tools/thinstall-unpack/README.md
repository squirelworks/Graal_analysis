# thinstall-unpack

Unpacks the Thinstall 2.x packages that Graal 4.x was shipped in (the Windows 4.03r3, 4.04r2 and 4.11 `Graal4Setup.exe` downloads) **without running them**. Results and checks: [protocol/v4x-windows-403r3-411.md](../../protocol/v4x-windows-403r3-411.md).

- `unpack.py <packed.exe> <workdir> <outdir> [name-substring ...]` runs the three steps below in order.
- `emu.py` emulates the package in unicorn. On the first run it stops when the stub hands over to the Thinstall runtime it has unpacked, and saves `<prefix>.snap`. On the second run it continues the runtime with stubbed Windows calls and stops at the first instruction of the virtual program, which never runs, and saves `<prefix>.snap3`.
- `vfsx.py` reads the runtime's file directory out of `.snap3` and decodes each file's 64 KiB blocks by calling the runtime's own block decoder in the emulator.
- `argtab.py <wine-i386-windows-dir> kernel32 user32 …` writes `argtab.json`: the stdcall argument count of each export, read from Wine's i386 PE DLLs (`ret imm16`). `emu.py` uses it for Windows calls it has no stub for. The JSON is not committed.

Needs `pefile`, `capstone` and `unicorn` 2.x. Keep the packages, the work folder and the output outside this repo, and run the scripts with `python3 -I`. The unpacked files are the vendor's and are never committed.
