# v3 builds (inventory)

Date: 2026-11-08 · Tags: **[bin]**

Primary (clear ELF, analyzed):

| File | Role |
|---|---|
| `older/v3/…/release/graalexe 3.0.4` | ELF32 i386 client, ~6.9 MB, stripped, GCC 2.96. **Protocol surface.** |
| `release/main.cs` | Torque startup: mods `common;graaldata` |
| `release/graaldata/languages/*.cs` | UI strings (version, fixed UDP port) |
| `release/levels`, `maps`, `sounds` | shipped content (`offlinetutorial.gmap`, swords, …) |

Skipped:

| File | Why |
|---|---|
| `setup.data/bin/.../glibc-2.0/graal` | installer helper, not the client |
| `release/graal` | 12-byte shell launcher |
| `Graal v3.04[Linux][Obsolete].sh`, `3.15r1[Linux][Broken].sh` | Makeself installers |
| `3.04` / `3.15r2` Mac `.dmg.gz` | not a clear ELF sibling; not opened this pass |

No `3.153` image was in `older/v3`. The readable client for this pass is **3.0.4**.
