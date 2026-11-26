# `.ifl`, `.dml`, `.dsq` and `.gft` are all unreachable on a 5.12-class client: animation/material lists ignored, no standalone `.dsq`, text draws via `showtext` not a `.gft` shape (T3D-034/035/036, Linux 4.20r6)

Date: 2026-11-26. Single-client lab on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route), software GL; file-request + console + screenshot capture. Observation only. Board rows: [T3D-034](3d-capability-board.tsv) (`.ifl`/`.dml`), [T3D-035](3d-capability-board.tsv) (`.dsq`), [T3D-036](3d-capability-board.tsv) (`.gft`/GameShapeFT). Shares the content-format run of [T3D-011](3d-content-format-requests-420r6-2026-11-26.md); font resolution per [T3D-120](3d-font-handling-420r6-2026-11-26.md).

## Headline

The three legacy Torque animation/material/font-shape formats are **all unreachable** on the 5.12-class route, each for its own reason — confirming they are 4.04r2-era features. 3D text has a working path, but it is **GS2 `showtext` + a GUI `.ttf`**, not a `.gft` shape.

## T3D-034 — `.ifl` / `.dml`: ignored **[lab]**

Used as a **material texture**, the client **strips the extension and requests the bare name** (`anim`, `mat`) as a plain texture — it never fetches or parses the `.ifl` frame list or `.dml` detail-list, and the shape drew plain (no animation, no material effect). Used as a **shape**, neither is requested at all. Confirms `.ifl`/`.dml` are 4.04r2-only.

**For a server:** don't use `.ifl`/`.dml` on a 5.12-class client; do frame animation with a GS2 / texture-swap instead.

## T3D-035 — `.dsq`: not loaded, no animation **[lab]**

A GameObject shape named `a.dsq` produced **no file request** (it isn't a shape to the loader), and there is **no datablock path on proto-24** to attach a standalone `.dsq` sequence (the datablock phase is 4.04r2's — cf. [T3D-052](3d-lighting-phase-timing-404r2-420r6-2026-11-26.md)). `.dsq` appears in the engine's format strings but is unreachable on this route.

**For a server:** you cannot deliver a standalone `.dsq` to a 5.12-class GameObject; animation must be **embedded in the `.dts`/`.3ds`** or driven from GS2.

## T3D-036 — `.gft` / GameShapeFT label: text is a `showtext` path, not a shape **[lab]**

A `.gft` placed as a GameObject shape is **not requested or loaded** (confirming the earlier partial: a `.ft` GameObject never draws). The working 3D-text path is **GS2 `showtext` + a GUI font**: the weapon's `showtext("Arial","lb",…)` drew its label and requested the bold font `arialbd.ttf` (lowercase family + `bd` + `.ttf`, per [T3D-120](3d-font-handling-420r6-2026-11-26.md)); the font wasn't served, so it fell back to default Arial and the label still drew. So a 3D label comes from the `showtext`/font path with a resolved `.ttf`, not from loading a `.gft` shape.

**For a server:** draw 3D text via `showtext` (ship the resolved `.ttf` on disk to apply from first use — [T3D-120](3d-font-handling-420r6-2026-11-26.md)); a `.gft` placed as a shape renders nothing.

## Net

All three legacy formats are dead ends on the 5.12-class route: `.ifl`/`.dml` degrade to a bare plain-texture name, `.dsq` has no attach path without datablocks, and `.gft`-as-shape is never loaded. The only live text path is `showtext` + `.ttf`. Each is consistent with the per-extension request map in [T3D-011](3d-content-format-requests-420r6-2026-11-26.md): none of `.ifl`/`.dml`/`.dsq`/`.gft` is ever fetched as a shape.

## Method caveat

Single client, loopback server, software GL. Negatives rest on the gserver file-request trace (the client never asked for the format) plus the drawn result (plain shape / nothing / default-font label), which together show the format is not parsed on this route — not merely unserved.
