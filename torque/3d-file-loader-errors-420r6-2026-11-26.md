# 5.12-class file-loader error paths: a malformed font crashes the client at startup; textures and sounds are robust (T3D-119, Linux 4.20r6)

Date: 2026-11-26. Single-client lab on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route), software GL (llvmpipe). This is the **on-disk file-loader** error path (distinct from the net/ghost fuzz tier, [T3D-105](3d-fuzz-net-tier1-2026-11-25.md)/[T3D-114](3d-capability-board.tsv)). Observation only. Board row: [T3D-119](3d-capability-board.tsv). Builds on [T3D-118](3d-texture-size-limit-420r6-2026-11-26.md) (texture size), [T3D-090](3d-shape-textures-420r6-2026-11-25.md)/[T3D-077](3d-texture-formats-420r6-2026-11-25.md) (textures), [T3D-058](3d-gui-overlay-420r6-2026-11-25.md) (fonts), [T3D-084](3d-sound-paths-2026-11-25.md) (sound).

## Headline

**Only the font loader crashes — and it takes the client down at startup, before it connects.** A malformed `.ttf` (truncated, zero-byte, or not a font) aborts the process right after GL init, before login. The **texture** and **sound** loaders are robust: a malformed texture draws white or garbled and the scene survives; a malformed sound is a silent no-op.

## Setup

One deliberately broken file per run, placed where a valid asset lives on the client disk (with its extension), then the client driven to the scene that uses it. Texture: a GameObject cube whose material names one texture ([T3D-118](3d-texture-size-limit-420r6-2026-11-26.md)/[T3D-090](3d-shape-textures-420r6-2026-11-25.md)). Font: the `.ttf` that `showtext` uses, at the client root. Sound: the `.wav` for `play`/`play2` via a `weapon3d` script. Audio not verifiable headless — judged by console / crash / client survival.

## Matrix: asset × malformation → outcome **[lab]**

| asset | malformation | outcome | client |
| --- | --- | --- | --- |
| **Texture** (.png) | truncated (header + partial body) | garbled — black cube with faint colour scanlines (valid rows decode); applied | alive, scene survives |
| | zero-byte | white — untextured fallback (as missing) | alive, scene survives |
| | wrong magic (text as `.png`) | white — magic check rejects, untextured fallback | alive, scene survives |
| | valid header + corrupt body / bad CRC | garbled — black cube (broken stream decodes to black); applied | alive, scene survives |
| **Font** (.ttf) | truncated | **CRASH** | **dies at startup, before login** |
| | zero-byte | **CRASH** | **dies at startup, before login** |
| | wrong magic (text as `.ttf`) | **CRASH** | **dies at startup, before login** |
| **Sound** (.wav) | truncated | graceful no-op — FMOD inits, `play`/`play2` run, no error | alive, scene survives |
| | zero-byte | graceful no-op | alive, scene survives |
| | wrong magic (non-RIFF text as `.wav`) | graceful no-op | alive, scene survives |

## Which crash vs which are handled

- **Only the font loader crashes — the worst kind.** All three malformed `.ttf` take the client down **at startup, before it connects**: it stops right after GL init and never reaches activation or login (client log halts at the GL-extension step, ~48 vs ~84 lines for a good run). The client loads the on-disk font **eagerly at startup**, and a present-but-broken font (truncated, empty, or not a font) aborts the process there. Even a **zero-byte** `.ttf` crashes it — no guard against empty/short input.
- **The texture loader is robust.** Bad magic or empty → untextured white cube; truncated or CRC-broken → partially decoded black/garbled cube, drawn anyway; the rest of the scene always renders. Contrast [T3D-118](3d-texture-size-limit-420r6-2026-11-26.md): there an *oversized* valid texture crashed on memory; here *malformed* small textures are graceful — the crash risk is size, not corruption.
- **The sound loader is robust.** A broken `.wav` (truncated/empty/non-RIFF) doesn't crash or stall: FMOD inits, the `play` call runs, the mission completes, the scene draws. The bad sound is silently a no-op.

## For a server

**Never let a malformed or corrupt font file reach the client's font location** — a broken `.ttf` on disk crashes the 5.12-class client at startup, before it even connects (the one hard failure here). Malformed textures and sounds are handled gracefully (white/garbled cube, or a silent no-op) and are low-risk. Combined with [T3D-118](3d-texture-size-limit-420r6-2026-11-26.md): the two file-level ways to crash this client are an **oversized** texture (>~8192 px) and a **broken font** — both worth validating server-side before shipping assets.
