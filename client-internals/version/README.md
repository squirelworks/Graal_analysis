# Seihai — Version ID Recovery

How the project recovers version identifiers from Graal classic binaries and their decompiles. Packaged for the Seihai project.

## Contents

- `VERSION.md` — consolidated notes on the methods used.
- `docs/` — supporting documentation:
  - `GraalEditor-README.md`, `GraalEditor-architecture.md`
  - `graaleditor.txt`, `graal.txt` (LinuxMan 2 man pages)

## Quick reference

| Binary | Version signal | Value |
|--------|----------------|-------|
| GraalEditor.exe | PE version resource (FileVersion) | 2.3.1.1 |
| Graal_2171.exe | Filename | 2.171 |
| Graal_222.exe | Filename | 2.22 |
| Graal_231.exe | Filename | 2.31 |
| gif2mng.exe | Banner string | 2004-06-03 |

The PE version resource is the reliable source for FileVersion / CompanyName / ProductName. It is present even in the Thinstall stub of GraalEditor. Client builds are identified by filename encoding.
