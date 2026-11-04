# gs1-table-scan

Reads the GS1 command list out of a Graal client binary, so the command set of every client can be compared without relying on
release notes. Results and the write-up: [`npc-library/gs1-commands-by-version.md`](../../npc-library/gs1-commands-by-version.md).

- `gs1scan.py <mode> <binary>` prints `{"count": n, "commands": [...]}`. Modes: `table` (Delphi 2nd Graal to the 2.1 tests and
  NewWorld betas), `init` (Delphi 2.17.1 to 2.31), `x86` (C++ engine: Linux 3.04 ELF, `GraalEngine.dll` 4.x and 5.x), `ppc`
  (the engine on Mac OS X PowerPC). The docstring says what each mode looks for.
- `builds.tsv` lists the 61 builds in order: key, label, line (`delphi` or `engine`), date, which binary was scanned, its MD5, and
  the mode.
- `matrix.py <dir>` reads `<dir>/<key>.json` for every build in `builds.tsv` and prints the matrix TSV
  (`npc-library/gs1-commands-by-version.tsv`). With `--changes` it prints the change-by-build table of the note.

Only command names come out; no addresses are printed or stored. Needs `pefile`, `capstone` and `pyelftools`. The client
binaries are not in this repo: get them from the project files (`graal clients.zip`, the 2.2x Drive folder, the 3.x–5.x
uploads; see the Sources table of the note), unpack 3.04 with `upx -d` first, and run the scanner with `python -I` from a
directory outside the extracted archives. It reads the files only and never runs them.

Re-running on the binaries listed in `builds.tsv` gives the same 61 lists as the committed TSV.
