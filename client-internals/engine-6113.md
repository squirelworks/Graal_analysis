# Windows 6.1.1.3 is still the packer stub

Date: 2026-11-07. Static read of the upload `Graal 6.1.1.3.exe`. Nothing was run. Tags: **[bin]**.

The earlier passes on this same listing are `packed-6113.md` and `skipped-v6-read.md`. This note is the identification after the 2026-11-07 gap archive was opened. The wire neighbour-diff is `protocol/v6113-wire.md`. The GS2 neighbour-diff is `protocol/gs2-6113.md`.

## Still no engine image

The gap archive (`cursor-gap/`, seven members) is cleaned notes only: a short readme and the four protocol notes `v5x-clients.md`, `v6x-clients.md`, `v5v6-windows-unpacked.md` and `v5v6-lab-play.md`. Each of those four is byte-identical to the copy already on main. It does not contain an unpacked executable, a `Graal.exe` engine, or a memory dump.

The project upload folder that holds the 6.x archives has the same four zips as the local set: packed 6.037, packed 6.113, and the unpacked Windows 6.00r2 and 6.00r4 listings. There is no separate 6.113 engine image.

The 6.113 decompile text is 227,199 bytes, the same stub listing those earlier notes read. The paired HTML listing is the same image, not a second program. **[bin]**

## What this file is

One 32-bit Windows GUI executable. It is not a DLL. The characteristics are a normal executable image with relocations, line numbers and local symbols stripped. The linker major version in the header is 9; that is the wrapper's header, not a recovered compiler date for a game engine. The virtual image is 6,504,448 bytes, of which 2,623,488 are code and 696,832 are initialized data, and the headers are 1,024 bytes. Six sections: two with blank names, `.rsrc`, `.idata`, and two 8-letter names (`fbndyrix`, `tlrwuvpz`). That is the same wrapper shape as packed 6.037, not the single readable `quattro_lib` program in `engine-600r2.md`. **[bin]**

The version resource, US English Unicode string table:

| Field | Value |
| --- | --- |
| File description | Graal |
| Internal name | Graal |
| Original file name | `Graal.exe` |
| Company | Eurocenter Games |
| Copyright | 2014 |
| File version string | `6.113` |
| Product version string | `6.113` |

The fixed version words are major 6, minor 1, build 1, revision 3, for both the file version and the product version. That is 6.1.1.3, the same release the string table shortens to 6.113. There is no `G3D` token and no compiler date string of the kind unpacked 6.00 carries (`Jun 12 2011`). The image timestamp is 8 August 2014, 13:19:46 UTC, which agrees with the copyright year and is later than Mac 6.11's 25 March 2014 stamp. **[bin]**

## The one import and the entry

The import directory names one DLL, `KERNEL32.DLL`, and one function, `SetCurrentDirectoryA`. The recovered stub does not call it.

Entry calls one helper and then executes a breakpoint. The helper looks at the byte at its return address. When that byte is the breakpoint opcode, it clears the byte and walks four kilobytes, a dword at a time, xoring each dword and then adding a second constant. It does not allocate memory, change page protection, or jump to another entry. No second image is recovered past that breakpoint. **[bin]**

## The export surface

The export directory is named `QPlay.exe`. The version resource in the same image still calls the file `Graal.exe`. The names are a TLS and compression surface, not Graal classes. They are C++ under a `CyaInt` namespace, with a few cipher calls left unmangled.

The decompiler annotated 117 of those exports, ordinals 1 through 136 with gaps. The names cover a CyaSSL client: SSLv3, SSLv23, TLS 1.0, TLS 1.1 and TLS 1.2 client methods; DTLS peer, timeout and handshake calls; OCSP options and an override URL; connect, read, write, peek, shutdown, session and certificate calls; a nonblocking flag. Cipher and hash names beside that are AES-CBC (set key, set IV, encrypt, decrypt), ARC4, HMAC, MD5, SHA, SHA-256, RSA (public encrypt, private decrypt, SSL sign and verify, key decode) and a random generator.

The listing continues with zlib from ordinal 138 through 177, two ordinals unused. Those names include `inflate`, `deflate`, `inflateUndermine`, `inflateReset2`, `crc32_combine64`, `get_crc_table` and `zlibVersion`.

The bytes at those exports are not that library. Bodies that decompiled are broken instructions, an empty return, or a breakpoint. `CyaSSL_Debugging_OFF` did not decompile: the flow was longer than the decompiler allows. An export ordinal on this directory is not a GS2 opcode. Ordinal 121 here is `Md5Update`. **[bin]**

## Subsystem map

| Piece | In this image |
| --- | --- |
| Connection and framing | No socket, no login builder, no frame type, no cipher seed |
| GS2 VM | No segment walker, no opcode switch, no builtin table |
| Property parsers | No player, NPC or baddy property stream |
| File and cache | No `GRESCR01`, no `.code`, no package or level magic |
| GUI | No control class and no script shell. The PE subsystem is the Windows GUI subsystem, which only says the wrapper is not a console program |
| What is present | The stub above, and the `QPlay.exe` export names |

A search of the listing finds none of the unpacked 6.00 markers `quattro_lib`, `Quattro_Play`, `TSocket`, `GuiGraalCtrl`, `TServerPlayer`, `StartScript`, `OpenGL`, `FMOD`, `SimObject` or `GameConnection`. **[bin]**

## Diff against the nearest 6.x builds

| | 6.1.1.3 (this file) | Packed 6.037 | Unpacked 6.00r4 | Mac 6.11 |
| --- | --- | --- | --- | --- |
| What was read | Packer stub | Packer stub | `quattro_lib` engine | Native Mach-O |
| Version | String `6.113`, words 6.1.1.3 | String `6.037` | Product `6.004` | Bundle `6.111` |
| Publisher / year | Eurocenter Games, 2014 | Linux Cyberjoueurs, 2012 | Linux Cyberjoueurs, 2011 | Eurocenter, 2014 |
| Stamp | 8 August 2014, 13:19:46 UTC | 16 November 2012, 18:05:43 UTC | Compiler string 26 June 2011, 18:32:49 | 25 March 2014 |
| Shape | 32-bit GUI exe, six sections, virtual image 6,504,448 bytes | Same wrapper shape, virtual image 6,217,728 bytes, section names `yfnbwito` and `recqxwzm` | One readable exe | One signed app |
| Import | `SetCurrentDirectoryA` only, not called | `DebugBreak` only | The engine's own imports | Not this file |
| Exports | `QPlay.exe`: CyaSSL through TLS 1.2, DTLS, AES-CBC, HMAC, SHA-256, zlib | `QPlay.exe`: smaller CyaSSL and zlib surface (`skipped-v6-read.md`) | No such directory; the engine is in the image | Not this file |
| Token | None in the image | None in the stub | `G3D26090` on the wire (`v5v6-windows-unpacked.md`) | Set by the connector script |

The 6.00 betas are not this file either. They are January 2010 MoleBox wrappers, older than 5.24r3, and they send `G3D03048` (beta1) and `G3D15010` (beta2). **[bin]** (`protocol/v5v6-windows-unpacked.md`)

The string lists of unpacked 6.00r2 and 6.00r4 still differ only by the two-week delta in `engine-600r4.md`: r4 adds `resolveHost` and the HTTP keep-alive headers; r2 alone names `rsa.c`, `sha1.c`, `truetype`, `type1` and `Server List`. None of those strings are in the 6.113 listing. **[bin]**

## What is gone by 6.1.1.3

The readable post-Torque engine is unpacked Windows 6.00 (`engine-600r2.md`, `engine-600r4.md`). This 6.113 listing is the stub in the sections above, so the absence below is the 6.00 image plus a search of the 6.113 listing. **[bin]**

Already gone in unpacked 6.00, and absent as names from 6.113 as well: the Torque console, `SimObject`, `GameConnection`, `ShapeBase`, Torque's `Player`, `graal_set`, `TAdventure`, `GuiTilesCtrl`, and the Torque GUI fields `horizSizing`, `vertSizing`, `minExtent`, `fontType`, `fillColor`, `makeFirstResponder` and `pushToBack`. Tiles in 6.00 are the `Draw_Tiles` pass. **[bin]** (`client-internals/engine-600r2.md#no-torque-3d`, `client-internals/engine-600r2.md#gui-and-script-objects`, `client-internals/engine-6113.md#subsystem-map`)

What still hooks the session in unpacked 6.00, and what 6.113 does not reintroduce: `GuiGraalCtrl` and `GuiGraal3DCtrl` are the playfield. The GUI walk compares a control's type with both names and drops either one when a flag on the parent is clear. There is no scene graph behind `GuiGraal3DCtrl`, and neither name is a `graal_set` slot. No Torque field name survives beside them to change layout or movement. The lab timings for 6.00 and 6.03 match 2.05: walk a half tile per 50 ms tick. This 6.113 file has neither control name and no movement constant. **[bin]** (`client-internals/engine-600r2.md#no-torque-3d`) **[cap]** (`protocol/v5v6-lab-play.md#play-what-the-client-does`)

`MissionGroup` in 6.00 is a script object looked up by name. `onMouseYawPitch` and a builtin described as recolouring 3D terrain are script text. `levels3d` is a content folder. `graal3://` is an option-list string with no recovered call. None of those are in the 6.113 listing, and none of them is a Torque UDP connection. **[bin]** (`client-internals/engine-600r2.md#what-torque-names-remain`)

### Ato and Issho

Seihai issue 377 asks for mae, ato and issho crates, and its text puts 7.x in issho with 6.x. The cut this reading supports is narrower. Ato is v3–v5: `graal_set`, `TAdventure`, and, where the 3D DLL is loaded, the mission. Issho is v6: the quattro program, `TSocket`, gen-5 framing, the GS2 VM and `GRESCR01`. By unpacked 6.00 that Torque list is already gone. Windows 6.113, image timestamp 8 August 2014, still has no readable replacement and no Unity bridge. v7 Unity is not a supported profile. This pass does not implement Issho, and it does not fill the crate. A readable engine for the packed 6.113 executable is still open. **[bin]**

## For graal-client-repro

`gh issue comment` was not sent. The text that would have been posted:

Windows 6.1.1.3 in the current upload is the `QPlay.exe` packer stub, not a profile to copy. Version string `6.113`, fixed version 6.1.1.3, Eurocenter Games, image timestamp 8 August 2014, one import `SetCurrentDirectoryA`, export names for CyaSSL (through TLS 1.2, DTLS, AES-CBC, HMAC, SHA-256) and zlib, bodies not the library. No login token, no GS2 VM, no property parser, no `graal_set`, no `GuiGraalCtrl`. The post-Torque shape to follow is unpacked 6.00 (`client-internals/engine-600r2.md` in Graal_analysis). Do not point the Torque module at this file. Do not treat the export ordinals as GS2 opcodes.

## For seihai 377

`gh issue comment` was not sent. The text that would have been posted:

Issho is v6. Ato is v3–v5. v7 Unity is not a supported profile, and this Windows 6.113 file does not put a Unity bridge or a 7.x property layout into Issho. The readable v6 engine is unpacked 6.00: `TSocket`, gen-5 framing, GS2 with cases 54 and 121 and folds 234–242, `GRESCR01` on `.code`, playfield types `GuiGraalCtrl` and `GuiGraal3DCtrl`. The packed 6.113 executable is still a stub, so it does not add a packet id, a property encoding or an opcode. Please leave the 7.x sentence in the issue out of the crate boundary. This pass does not add the crate.
