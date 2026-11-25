# GameObject shape textures and cache naming in 3D mode (T3D-090, Linux 4.20r6)

Date: 2026-11-25. Loopback lab of the Linux 4.20r6 client against our own 3D lab server, with the 2D link decoded (runs `tex420-a1` to `tex420-c`; no movement input). Linux 4.20r6 is 3D-equal to Windows 4.20r8 ([T3D-004](3d-engines-5007-512-and-403-411-2026-11-25.md#t3d-004-linux-and-mac-against-their-windows-twins)). Board row: [T3D-090](3d-capability-board.tsv). Builds on [T3D-107](3d-file-preference-420r6-2026-11-25.md) (downloads go under `levels3d/images/`).

A served GameObject named one textured `.3ds` cube; only the texture name in the material was varied. Server textures were flat 16×16 PNGs so a drawn texture is obvious.

## Results **[lab]**

| Run | Texture in the material | On the server | Cube | Texture request | Cached as |
| --- | --- | --- | --- | --- | --- |
| tex420-a1 | `labtex` | `labtex.png` | white | `labtex` (no extension), once | `images/labtex` (no extension) |
| tex420-a1b | `labtex.png` | `labtex.png` | white | `labtex` (the `.png` stripped) | `images/labtex` |
| tex420-a2 | `misstx` | absent | white | `misstx` once; server answered `PLO_FILESENDFAILED` (30); no retry | nothing |
| tex420-b1 | `sub/subtex` | `subtex` | white | `subtex` (the `sub/` stripped) | `images/subtex` (flat) |
| tex420-c | `labtex`, with `labtex.png` already on the client | `labtex.png` | **green (textured)** | checked the local copy (up to date); no download | the local `labtex.png` is used |

## Naming rules **[lab]**

- **Request name.** The client takes the material's texture name, strips any directory to the leaf (`sub/subtex` → `subtex`) and strips a `.png` extension (`labtex.png` → `labtex`), then asks for that bare name once (`PLI_WANTFILE` 23, or `PLI_UPDATEFILE` 34 for one it has). On a failure it does not re-ask within the session.
- **Cache path**, under the user folder's `levels3d/images/`: the part of the name before the first `_` becomes a subfolder (`tc_labtex.3ds` → `images/tc/tc_labtex.3ds`, `sky_fr` → `images/sky/sky_fr`); a name with no `_` stays flat. The filename is saved exactly as requested, so a texture asked for without an extension is saved without one. Shapes keep their `.3ds`. Casing was not tested.

## Does the shape draw, and does the texture apply?

- **The shape always draws.** A missing or unapplied texture leaves it white, never invisible or a placeholder.
- **A server-delivered texture is not applied this session.** The download is saved as `images/<name>` with no extension, but the material loader looks for `<name>.png`. tex420-c confirms the cause: with a real `labtex.png` on disk the same material drew the cube green. So a texture renders only when a file named `<texture>.png` is already on disk (shipped with the client, in a mounted zip ([T3D-012](3d-archives-404r2-512-2026-11-25.md)), or from an earlier session ([T3D-107](3d-file-preference-420r6-2026-11-25.md))). A fresh on-demand download, cached without the extension, is not matched. Whether a later re-bind would ever pick it up was not seen in 55 s.

**For a server:** to show a texture on a GameObject shape, the texture must be on disk as `<name>.png` before the shape binds — ship it, mount it in a zip, or rely on a prior session's copy. A texture named only in the material and delivered on demand caches without the `.png` and the shape stays white.
