# The 5.12-class client draws textures up to 8192 px and crashes silently past ~10240 (T3D-118, Linux 4.20r6)

Date: 2026-11-26. Single-client renderer lab on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route), software GL (Mesa llvmpipe, LLVM 19.1.7, OpenGL 4.5 compat). Observation only. Board row: [T3D-118](3d-capability-board.tsv). Builds on [T3D-090](3d-shape-textures-420r6-2026-11-25.md) (texture caching/naming) and [T3D-077](3d-texture-formats-420r6-2026-11-25.md) (texture formats).

## Headline

**The largest texture that draws is 8192×8192.** Everything from 256 up to and including 8192 px renders at full fidelity; by 10240 px the client **crashes silently on texture load** — no downscale, no white fallback, no error line. **Non-power-of-two textures are accepted and drawn like PoT.** The ceiling is **client-imposed (32-bit process memory), not the GL driver limit** (llvmpipe reports `GL_MAX_TEXTURE_SIZE = 16384`, higher than where the client dies).

## Setup

One GameObject shape (a simple textured `.3ds` cube, the [T3D-090](3d-shape-textures-420r6-2026-11-25.md) layout) whose material names one texture, pre-placed on the client's disk **with its extension** before launch (a server-delivered texture caches without an extension and is never applied, [T3D-090](3d-shape-textures-420r6-2026-11-25.md)/[T3D-077](3d-texture-formats-420r6-2026-11-25.md)). The texture is a 4-quadrant colour pattern with a border, so "draws" shows the quadrants, "not applied" shows white, "failed" shows nothing. One run per size, fixed camera, no movement, console captured.

## Size → outcome **[lab]**

| texture | PoT? | outcome |
| --- | --- | --- |
| 256×256 | yes | draws — full quadrant texture |
| 512×512 | yes | draws |
| 1024×1024 | yes | draws |
| 2048×2048 | yes | draws |
| 4096×4096 | yes | draws |
| 8192×8192 | yes | **draws — largest that draws** |
| 1000×1000 | no | draws — textured identically |
| 1024×768 | no | draws — textured, crisp |
| 10240×10240 | no | **client crashes** on texture load |
| 12288×12288 | no | **client crashes** |
| 16384×16384 | yes | **client crashes** |

## Ceiling and failure mode

- **Ceiling: 8192×8192** is the largest that draws; failure sets in by 10240.
- **Failure mode is a silent client crash**, not a downscale or white fallback. On an oversized texture the client completes the Phase-1 shape download, then the process **terminates** while loading/binding the texture — no `image too large`, no `GL_MAX…`, no downscale notice, no console error, and the frame goes black. It is **not** a kernel OOM-kill: the VM had >1.6 GB free throughout and nothing was killed by the OS; the client aborts itself. It never downscales and never drops to white — it attempts the full-size load and dies.

## PoT vs non-PoT

**Non-power-of-two textures are accepted and drawn exactly like PoT** — 1000×1000 and 1024×768 both textured the cube correctly, no rejection, no padding-to-white, no "must be power of two". Size, not NPoT-ness, sets the ceiling.

## Client-imposed vs GL/driver-imposed

**The ceiling is client-imposed (the 32-bit client's process memory), not the GL texture-size limit.**

- llvmpipe reports `GL_MAX_TEXTURE_SIZE = 16384` (and `GL_MAX_RECTANGLE_TEXTURE_SIZE = 16384`) — the driver would accept a single texture up to 16384.
- Yet the client dies at 10240 and 12288, both well **under** 16384 and fully GL-legal. If the limit were the GL clamp, those would load. So the failure is upstream of GL, in the client.
- Consistent mechanism: the client is a **32-bit** process and decodes the whole image in-process (10240² ≈ 300 MB for the decode) while software GL (llvmpipe) keeps a **system-memory copy** of the texture (10240² RGBA ≈ 400 MB) plus mipmaps — together exhausting the 32-bit address space during upload, below the GL ceiling and without touching host RAM.
- **Software-GL caveat:** because llvmpipe holds the texture in system memory, software GL tightens this ceiling. On a real GPU the texture lives in VRAM, so the in-process pressure is mainly the decode buffer and the same 32-bit client might push the draw ceiling somewhat higher (toward 16384) — but the 32-bit in-process decode keeps it bounded well under a 64-bit build. The measured **~8192 safe ceiling is a software-GL + 32-bit-client figure**; treat 16384 as the hard engine/GL ceiling a 64-bit/real-GPU path would approach, not what this client reaches.

## For a server

Keep GameObject shape textures at **≤ 8192×8192** (power-of-two preferred, though NPoT is accepted). Larger textures crash the 5.12-class client **silently on load with no error**, so a server must not ship very large textures to these clients.
