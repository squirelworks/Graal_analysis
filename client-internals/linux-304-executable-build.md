# Linux 3.04: how the executable was packed, built and linked

Date: 2026-11-14. Static read of the 3.04 Linux client (the "revision 1" package, `graalexe`) and the installer files shipped with it. Nothing was run. Tags: **[bin]** executable bytes · **[file]** shipped installer or data file · **[inf]** inferred.

This adds build and link facts to the existing 3.04 notes. Engine version, compile time and the package layout are already in `torque/study-torque-clients.md` and `torque/engine-and-formats.md`. Startup behaviour is in `linux-304-startup-reader.md`. Protocol is in `../protocol/v3x-clients.md`.

## Packing

- `graalexe` ships compressed with **UPX 1.24** (pack-header format 10, UPX's `linux/386` format rather than the later `linux/elf386`; method 5, NRV2D; level 10, `--best`). The packed file is 2,506,953 bytes; the pack header records an original size of 6,963,812 bytes. **[bin]**
- `upx -d` restores a file whose size and Adler-32 checksum match the values stored in that pack header. The unpacked file is therefore exactly what the packer compressed, not an approximation. **[bin]**

## Toolchain

- The `.comment` section has 478 entries:
  - 473 read `GCC: (GNU) 2.96 20000731 (Red Hat Linux 7.3 2.96-110)`.
  - 5 read `The Netwide Assembler 0.98.22`.
  
  So nearly all of the engine was compiled with Red Hat's GCC 2.96, and five objects were assembled with NASM. Torque ships a few hand-written assembly files; NASM objects are expected there. **[bin]** **[inf]**
- The C++ ABI is the pre-GCC-3 one. Exported runtime symbols use the old `__ti…`, `__tf…` and `__vt_…` type-info and vtable names, and class names in the string table use 2.x mangling (for example `t16ConcreteClassRep1Z8AIPlayer`). GCC 3+ demanglers and RTTI tools will not read these names as they are. **[bin]**
- The executable is stripped: there is no `.symtab`, only the dynamic symbol table. **[bin]**
- The compile-time string `Jan  3 2004 at 22:32:08` (already published) sits beside a second build stamp, `Dec 14 2003, 21:07:09`. That second stamp belongs to the embedded GIFLIB 4.0 banner, so the GIF library was compiled about three weeks before the engine. **[bin]**

## Linkage

ELF32, Intel 80386, executable type, 26 sections. The `.text` section is about 3.9 MB, and the `.eh_frame` and `.gcc_except_table` sections are about 2.5 MB together. **[bin]**

Dynamically linked libraries, in `DT_NEEDED` order: **[bin]**

| Library | Notes |
|---|---|
| `libfmod-3.70.so` | Shipped in the package's `lib/`. 30 imports (24 `FSOUND_*`, 6 `FMUSIC_*`) |
| `libSDL-1.2.so.0` | Shipped in `lib/`. 48 `SDL_*` imports, including `SDL_GL_LoadLibrary` |
| `libpthread.so.0`, `libc.so.6`, `libdl.so.2`, `libm.so.6` | System |
| `libX11.so.6` | System. 39 `X*` imports |

- **OpenGL is not linked.** There are no `gl*` imports. The binary holds the names `libGL.so.1` and `libGL.so`, the message `Error loading GL library: %s`, and the imported `SDL_GL_LoadLibrary`, so GL is opened at run time and its functions are looked up by name. **[bin]**
- **No OpenAL library is linked or named.** Torque's OpenAL driver layer is compiled in (its console functions such as `OpenALInitDriver` are present), but no `libopenal` name appears anywhere in the binary, and no `al*` import exists. Sound and music go through FMOD 3.70. This corrects the "SDL, OpenAL" wording in the build tables (`torque/README.md`, `manual/10-torque.md`). The 2026-10-30 lab installed an OpenAL package for this client; going by this read, that package is not needed. **[bin]**
- **The C++ runtime is static.** Neither `libstdc++` nor `libgcc_s` appears in `DT_NEEDED`. The executable itself defines and exports the GCC 2.96 runtime pieces: type-info objects, `__register_frame_info`, `__divdi3`/`__udivdi3`/`__umoddi3`, and its own `stdin`/`stdout`/`stderr` and `_IO_*` objects. It needs no 2001-era libstdc++ on the target system. **[bin]**
- The dynamic symbol table has 396 named entries: 310 imports and 86 definitions. All 86 definitions are C++ runtime, libgcc or stdio objects; no Graal or Torque function is exported. **[bin]**
- Required glibc symbol versions top out at `GLIBC_2.2` (libc), `GLIBC_2.1.1` (libpthread) and `GLIBC_2.1` (libm). Any glibc from 2.2 onward satisfies the version check. **[bin]**
- Libraries compiled in, confirmed by their own banners: zlib 1.1.3 (`inflate 1.1.3`, `deflate 1.1.3`), libmng 1.0.5, GIFLIB 4.0, and the IJG JPEG decoder (its error strings). **[bin]**

## Installer and launcher

- The package is a **Loki Setup** installer. `setup.xml` names the product "Graalonline for Linux", version 3.04, installs to `/usr/bin` with a `graal` symlink, and points its update check at a `linux_updates.txt` on the 2001-era official update host (`<public-host>`). **[file]**
- The post-install script writes the launcher. It changes to the install folder, appends `lib` to `LD_LIBRARY_PATH` and runs `./graalexe`. That is how the shipped `libfmod` and `libSDL` are found; nothing is set for GL or X11. **[file]**
- The readme calls this "Graal Linux version 3.04 revision 1", credits the Linux Cyberjoueurs Team (Paris), and notes that the temporary files folder `~/.garagegames` is not removed on uninstall. **[file]**

## How this was checked

Static read only; nothing was run. The packed executable's UPX pack header was read directly, and the `upx -d` output was checked against the original size and Adler-32 stored in that header. ELF headers, sections, the dynamic table and symbol-version requirements were read with `readelf`; the `.comment` section, the dynamic symbols and string context were read with small scripts. Shipped installer files were read as text.

## Still open

- **Voice codec.** `librariesinfo.txt` lists "hvdi 0.9 - voice packaging" **[file]**, and the binary has the microphone preferences (`microon`, `microactivationlevel`, `choosenvoicecodec`, `microinputdevice`), `doMicro`, and Torque's `setVoiceDecodingMask`/`setVoiceEncodingLevel`. Yet no `hvdi`, `GSM` or `LPC` string appears in the unpacked executable. `torque/study-torque-clients.md` currently tags the GSM/LPC codecs **[bin]** for this client. Either the codec is present without identifying strings, or 3.04 has the voice controls without the codec. The first is quite possible. In the Windows 4.04r2 engine, HawkVoice is compiled in and visible only through its exported `hvdi*` function names (see `windows-404r2-components.md`). This Linux binary exports nothing of its own, so stripping would remove those names too. A code-level check of the `choosenvoicecodec` consumer would settle it.
- **OpenAL path.** Whether Torque's OpenAL driver can be reached at all, or is dead code beside FMOD, is not established by a static string read.
