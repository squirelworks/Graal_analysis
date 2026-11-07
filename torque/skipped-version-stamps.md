# Version stamps on the skipped v4, v5 and v6 exports

Date: 2026-11-07. Tags as in `README.md`. Static read of decompile exports. Nothing was run. **[bin]**

These are the uploads earlier passes left as packer stubs or broken exports. The modules already read in full (the 4.2.0.8 launcher, `GraalEngine.dll` and `Graal3DEngine.dll`; the 5.0.0.7 launcher, engine, 3D engine and FreeType; the unpacked 5.30r3 and 5.31r4 programs) are not opened again here. The unpacked 6.00r2 and 6.00r4 programs are full engines, not stubs, and are not opened here either. The FreeType decompile in the 4.2.0.8 archive is the same file as the 5.0.0.7 FreeType decompile, so it has no second stamp. **[bin]**

The decompiled C of each stub below has no string literals. The version resource is still in the listing, as a string table plus the four fixed version words. Those words are read major, minor, build, revision: that order matches the four-part file-version string wherever the string itself is four-part. A missing string is recorded as absent from the decompile, which is not a claim that some other copy of the client has no version. **[bin]**

## What was skipped

| Upload | Code | File version string | Fixed words | Product version string | Original file | Company | Year |
|---|---|---|---|---|---|---|---|
| `Graal 4.04r2.exe` and `Graal v4.20r8[Windows].exe` (one decompile) | stub | `4.0.4.2` | `4.0.4.2` | `4` | `Graal.exe` | `Linux Cyberjoueur` | none |
| `Graal 5.12.exe` | stub | `5.1.2.0` | `5.1.2.0` | `5` | `Graal.exe` | `Linux Cyberjoueur` | none |
| `Graal 5.2.4.3.exe` | stub | `5.243` | `5.2.4.3` | `5.243` | `Graal.exe` | `Linux Cyberjoueurs` | `2010` |
| `Graal v5.24r4.exe` | stub | `5.244` | `5.2.4.4` | `5.244` | `Graal.exe` | `Linux Cyberjoueurs` | `2010` |
| `fmod.dll` in the 4.2.0.8 and 5.0.0.7 archives (one decompile) | stub | `3.75` | `3.7.5.0` | `3.75` | `fmod.dll` | Firelight Technologies Pty, Ltd | `1994-2005` |
| `Graal 6.0.3.7.exe` | stub | `6.037` | `6.0.3.7` | `6.037` | `Graal.exe` | `Linux Cyberjoueurs` | `2012` |
| `Graal 6.1.1.3.exe` | stub | `6.113` | `6.1.1.3` | `6.113` | `Graal.exe` | `Eurocenter Games` | `2014` |

## Two layouts

The `4.0.4.2` exe stub and the `5.1.2.0` stub share one string table. The file version is four-part, the product version string is a single digit (`4` or `5`), the description is `Graal Online client`, the internal name is `Graal client`, and the company and the copyright string are both `Linux Cyberjoueur`, with no year. **[bin]**

From the `5.243` stub onward the Graal stubs share a second table. The file version string and the product version string are the same collapsed form (`5.243`, `5.244`, `6.037`, `6.113`). The fixed words stay four-part and match the dotted archive name (`5.2.4.3`, `5.2.4.4`, `6.0.3.7`, `6.1.1.3`). The description is Graal, the original file is `Graal.exe`, and the copyright string is a year: `2010`, `2012` or `2014`. The company is `Linux Cyberjoueurs` except on the `6.113` stub, where it is `Eurocenter Games`. **[bin]**

## v4 exe pair

The archives named `Graal 4.04r2.exe` and `Graal v4.20r8[Windows].exe` are one decompile, byte for byte, listing included. The recovered code is a packer stub: the entry allocates and protects memory and resolves imports, and it never reaches a game. There is no Graal class and no Torque class. **[bin]**

The version resource does not follow the archive names. Both copies say file version `4.0.4.2` (string and fixed words), product version `4`, product name Graal, description `Graal Online client`, internal name `Graal client`, original file `Graal.exe`, company `Linux Cyberjoueur`. There is no year. The zip labelled 4.20r8 is not a 4.2.0.8 binary. The file-version 4.2.0.8 launcher and engines are a different export and were already read. **[bin]**

## Graal 5.12

`Graal 5.12.exe` is a packer stub. The entry is overlapping instructions and stops. No game class is recovered. The archive holds that executable only. **[bin]**

File version string and fixed words are both `5.1.2.0`. The product version string is `5`, not `5.1.2.0`. Description `Graal Online client`, internal name `Graal client`, original file `Graal.exe`, company `Linux Cyberjoueur`, no year. **[bin]**

## Graal 5.2.4.3

`Graal 5.2.4.3.exe` is a packer stub. The entry is overlapping instructions and stops. No game class is recovered. **[bin]**

The file version string and the product version string are `5.243`. The fixed words are `5.2.4.3`, which is the archive name and not the string. Description Graal, original file `Graal.exe`, company `Linux Cyberjoueurs`, copyright year `2010`. **[bin]**

## Graal 5.24r4

`Graal v5.24r4.exe` is a packer stub. The entry is overlapping instructions and does not reach game code. **[bin]**

The file version string and the product version string are `5.244`. The fixed words are `5.2.4.4`. Description Graal, original file `Graal.exe`, company `Linux Cyberjoueurs`, copyright year `2010`. This is a different decompile from the 5.2.4.3 stub. **[bin]**

## fmod

`fmod.dll` in the 4.2.0.8 archive and `fmod.dll` in the 5.0.0.7 archive are one decompile. The recovered code is a packer stub: the entry loads libraries, resolves imports, and stops on a bad instruction. No sound API is recovered from that code. **[bin]**

The resource says this file is FMOD, not Graal. File version string and product version string are `3.75`. Fixed words are `3.7.5.0`. Description FMOD, product FMOD, original file `fmod.dll`, company Firelight Technologies Pty, Ltd, copyright years `1994-2005`. **[bin]**

## Graal 6.0.3.7

`Graal 6.0.3.7.exe` is a packer stub. The entry runs a short unpack step and then stops. Names on the image do not decompile into a library or a game. There is no Graal class. **[bin]**

The file version string and the product version string are `6.037`. The fixed words are `6.0.3.7`. Description Graal, original file `Graal.exe`, company `Linux Cyberjoueurs`, copyright year `2012`. **[bin]**

## Graal 6.1.1.3

`Graal 6.1.1.3.exe` is the same kind of stub, with a larger broken export. The entry runs a short unpack step and then stops. Three named routines did not decompile; the bodies that did are not a game. There is no Graal class. It is not the same file as the 6.0.3.7 stub. **[bin]**

The file version string and the product version string are `6.113`. The fixed words are `6.1.1.3`. Description Graal, original file `Graal.exe`, company `Eurocenter Games`, copyright year `2014`. **[bin]**
