# Themida shells in the Windows listings

Date: 2026-11-07. Static read of the Ghidra listings already extracted for these builds. Nothing was run. Tags: **[bin]**.

The 2026-11-07 gap archive is cleaned notes only. It adds no executable and no second copy of these listings.

## The marker

Four unpacked listings carry the same defined strings, in the section whose name is eight spaces:

| String |
| --- |
| `Themida` |
| `Oreans.vxd` |
| `oreans32.sys` |
| `oreansx64.sys` |
| `SecureEngine` (the defined string begins with that word) |
| `Software\WinLicense` |
| `WinLicenseVersion` |
| `WinLicenseDriverVersion` |
| `WinLicenseInstance` |

The four listings are unpacked 5.30r3, unpacked 5.31r4, unpacked 6.00r2 and unpacked 6.00r4. A section named `.themida` is not among them. The decompiled C of those four exes does not repeat the strings. They are defined data in the listing. **[bin]**

The same words, and a section named `.themida`, are absent from the packed `Graal 6.0.3.7.exe` and `Graal 6.1.1.3.exe` listings. The search covered the listing text and the undefined bytes. **[bin]**

## Which listings carry it

| Listing | What is in the file |
| --- | --- |
| Unpacked 5.30r3, 5.31r4, 6.00r2, 6.00r4 | The strings above. The image also has `.text`, and that is the C++ core (`quattro_lib`). The shell names are still in the section table: `.idata` padded with spaces, eight spaces, and two random 8-letter names. A further section is named `.SCY`. |
| Packed 6.0.3.7 and 6.1.1.3 | The same shell shape, with no `.text` and none of the vendor strings. The first section name is three spaces, a zero byte, and four spaces. Then `.rsrc`, `.idata` padded with spaces, eight spaces, and two random 8-letter names: `yfnbwito` and `recqxwzm` on 6.037, `fbndyrix` and `tlrwuvpz` on 6.113. |
| 4.2.0.8 and 5.0.0.7 `GraalEngine.dll`, `Graal3DEngine.dll` and `freetype6.dll`, and both Delphi launchers | None of the vendor words. Ordinary section names (`.text` / `.rdata` / `.data` / `.reloc`, freetype's export section, or Delphi `CODE` / `DATA` / `BSS`). The engine DLLs are the readable core for those builds. |
| `fmod.dll` in the 4.2.0.8 archive and in the 5.0.0.7 archive | Sections `UPX0`, `UPX1` and `.rsrc`. None of the vendor words. |
| `Graal 5.12.exe` | Eleven sections named `.data`. None of the vendor words. |
| `Graal 5.2.4.3.exe` | Eight sections named `.udata`. None of the vendor words. |
| `Graal v5.24r4.exe` | Eight sections named `.CRT$XIA`. None of the vendor words. |
| `Graal 4.04r2.exe` and the Windows `Graal v4.20r8` exe listing | One section, `.text` padded with spaces. None of the vendor words. That file is the Thinstall loader in `torque/skipped-v4-read.md`. |

## What the export cannot show

The packed 6.037 and 6.113 exports are that shell. The C++ core is not in them. `quattro_lib` is in the unpacked 6.00 images. The readable core of 4.2.0.8 and of 5.0.0.7 is in those builds' engine DLLs. **[bin]**
