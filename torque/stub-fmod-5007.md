# fmod.dll beside Graal 5.0.0.7

Date: 2026-11-07. Static read. Nothing was run. **[bin]**

## What the decompile is

The version resource says this file is FMOD: file version `3.75`, description `FMOD Sound and Music System`, product `FMOD`, original filename `fmod.dll`, copyright 1994–2005. **[bin]**

The code the decompiler recovered is a packer stub. `entry` walks an import list with `LoadLibraryA` and `GetProcAddress`, then stops on a bad instruction. There are no string literals and no FMOD API names in the recovered code. `GraalEngine.dll` still looks for FMOD by name (`Failed to open fmod audio`); that call is not satisfied by anything readable in this decompile. **[bin]**
