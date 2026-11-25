# Image formats, bit depths and sizes accepted for 3D shape and sky textures (T3D-077, Linux 4.20r6)

Date: 2026-11-25. Loopback lab of the Linux 4.20r6 client against our own 3D lab server, with the 2D link decoded (runs `tfmt420-a`, `-b`, `-sky`, `-sky2`; no movement input). Linux 4.20r6 is 3D-equal to Windows 4.20r8 ([T3D-004](3d-engines-5007-512-and-403-411-2026-11-25.md#t3d-004-linux-and-mac-against-their-windows-twins)), so this is the 5.12-class image loader. Board row: [T3D-077](3d-capability-board.tsv). Builds on [T3D-090](3d-shape-textures-420r6-2026-11-25.md): a texture applies only when its file is on disk under the right extension.

One base image — a 2×2 green/magenta checker — was saved in each format/size variant, then **pre-placed on the client with its real extension** (so this measures the image loader, with the file already on disk). A correct load shows the checker; a rejected file leaves the shape **white** (untextured); a wrong decode would show noise or swapped colours. One textured cube per variant, laid out so position maps to variant.

## Formats and bit depths **[lab]**

| Format | Bit depth | Result |
| --- | --- | --- |
| PNG | 8-bit indexed | renders correctly |
| PNG | 24-bit RGB | renders correctly |
| PNG | 32-bit RGBA | renders correctly |
| JPEG | 24-bit | renders correctly (expected JPEG softening) |
| GIF | indexed | renders correctly |
| BMP | 24-bit | renders correctly |
| TGA | 24-bit | renders correctly |
| TGA | 32-bit | renders correctly |
| DDS | BC1/DXT1 | **white — not loaded, silently** |

- PNG/JPEG/GIF/BMP/TGA all drew the checker with correct colours and orientation. No channel swap or wrong-colour: the 32-bit RGBA/TGA cubes matched the 24-bit ones.
- **DDS was the only format rejected.** The cube stayed white — the loader did not decode the `.dds` and the material fell back to untextured — even though the GL driver (Mesa, software GL) advertises S3TC. No error was printed; the failure is silent.
- No crash, no disconnect, and no format error in the console for any variant.

## Sizes **[lab]** (PNG-24 base)

| Size | Result |
| --- | --- |
| 100×100 (non-power-of-two) | renders correctly |
| 2048×2048 | renders correctly — no ceiling hit |
| 1×1 | renders as a single flat colour |
| 32×256 (odd aspect) | renders correctly |

- Non-power-of-two and odd aspect both rendered a correct-looking checker (the engine either handles NPOT or rescales silently; not distinguishable here).
- 2048×2048 loaded and drew with no complaint; no size ceiling was found at that size.
- No crash or disconnect at any size.

## Sky textures

The sky box uses the **same image loader** as shapes. With PNG checker faces pre-placed on disk (with extension), the sky rendered the textured faces (different colours per face). So the format/size table above applies to sky textures too; PNG was verified on the sky directly rather than re-running every format.

When the six sky faces were instead **delivered by the server** (as JPEG), the client downloaded all six but the sky showed its default gradient — the download cached without an extension and was not applied, exactly as for shapes ([T3D-090](3d-shape-textures-420r6-2026-11-25.md)).

## For a server

- **Supported texture formats:** PNG (8/24/32-bit), JPEG (24-bit), GIF, BMP (24-bit), TGA (24/32-bit), on both shapes and sky. **DDS is not** decoded by this client's loader — avoid it. Sizes are flexible: non-power-of-two, odd aspect, 1×1 and 2048×2048 all load with no ceiling found.
- As in [T3D-090](3d-shape-textures-420r6-2026-11-25.md), the file must be on disk under its correct extension before the shape or sky binds (shipped, mounted in a zip, or from a prior session). A texture delivered on demand this session caches without its extension and is not applied, in any format.
