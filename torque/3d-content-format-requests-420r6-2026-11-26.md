# What a 5.12-class client actually requests per extension: shapes `.3ds`/`.dts`(/`.dif`) with extension, textures bare-named, `.wav`/`.ttf` with extension, the rest never fetched (T3D-011, Linux 4.20r6)

Date: 2026-11-26. Single-client lab on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route), software GL; one scene placing a GameObject per extension plus textured shapes and a sound/label weapon, with all gserver file requests traced. Observation only. Board row: [T3D-011](3d-capability-board.tsv). Confirms and narrows the static read (requests every missing resource except `.dso`/`.cs`/`.ter`); texture naming per [T3D-090](3d-capability-board.tsv), interior-loader vestige per [T3D-121](3d-v6-quattro-vs-512-2026-11-26.md).

## Headline

The client only asks the gserver for the extensions its **loaders recognise**. Shapes are fetched **with** their extension (`.3ds`, `.dts`, and — via a lingering interior loader — `.dif`); **material textures are requested bare-named** (extension stripped); `.wav` and `.ttf` are fetched **with** extension; **everything else used as a shape is silently never requested**.

## Per-extension request map **[lab]**

**Requested over the file protocol:**

- `.3ds` shape — requested with extension, draws (white here; texture not applied this session, cf. [T3D-090](3d-capability-board.tsv)).
- a shape ending `.dif` — requested with extension; the client runs its **interior loader** on it (`InteriorResource::read: incompatible file version found`) then draws nothing on the stub — a lingering interior path (cf. [T3D-121](3d-v6-quattro-vs-512-2026-11-26.md)).
- material textures (`plain.png`, `anim.ifl`, `mat.dml`) — **requested bare, extension stripped** (`plain`, `anim`, `mat`): always a plain texture name.
- sky textures; the player shape `.3ds`.
- `.wav` sound — requested **with** extension.
- `.ttf` font (`arialbd.ttf`) — requested **with** extension.
- `basepackage.gupd`.

**Never requested** (as a GameObject shape): `.dsq`, `.gft`, `.ter`, `.ifl`, `.dml`, `.png`, `.jpg`, `.gif` — the shape loader doesn't recognise them, so it never asks for them.

## Reading

- The **shape loader** recognises `.3ds`/`.dts` (and `.dif` through the vestigial interior loader, which then can't draw it). A raster image, `.ter`, or an animation/material-list extension placed **as a shape** is not a shape to the loader, so no request goes out.
- **Textures** are always requested bare-named — the on-disk `<name>.png` is what applies ([T3D-090](3d-capability-board.tsv)); handing a texture an `.ifl`/`.dml` name just strips the extension to a plain texture name.
- **Sounds and fonts** keep their extension (`.wav`, `.ttf`).
- There is **no interior/terrain scene keyword**, so `.dif`/`.ter` can only be named as a shape — and only `.dif` is even recognised there (and fails to draw); `.ter` is not recognised at all.

## For a server

Ship only what the client asks for: `.3ds`/`.dts` shapes (extension kept), **bare-named** textures (put `<name>.png` on disk to apply), sky textures, `.wav`, `.ttf`. Do not ship `.dsq`/`.gft`/`.ter`/`.ifl`/`.dml` as shapes — they are never fetched and are wasted. A `.dif` named as a shape is fetched but fails the interior-version check and draws nothing.

## Method caveat

Single client, loopback server, software GL, one scene per extension. The map is what the client **requested**, which is a reliable read of its loader table; "never requested" means the shape loader rejected the name before any fetch. Draw results are the stub's (white `.3ds`, nothing for `.dif`), consistent with the renderer notes.
