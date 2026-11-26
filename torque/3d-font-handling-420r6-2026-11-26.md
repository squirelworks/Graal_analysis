# showtext fonts on the 5.12-class client: lowercase(family)+style+.ttf, TrueType only, missing→default, must be pre-placed to apply (T3D-120, Linux 4.20r6)

Date: 2026-11-26. Single-client lab on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route), software GL (llvmpipe). Observation only; only valid or validly-absent fonts used (per the [T3D-119](3d-file-loader-errors-420r6-2026-11-26.md) crash finding). Board row: [T3D-120](3d-capability-board.tsv). Builds on [T3D-058](3d-gui-overlay-420r6-2026-11-25.md) (showtext/GUI overlay) and [T3D-090](3d-shape-textures-420r6-2026-11-25.md) (on-demand asset caching).

## Headline

`showtext` resolves a font to **`lowercase(family)` + a weight/slant suffix + `.ttf`**, fetched over the Graal file protocol. **Only TrueType is accepted.** A font that is merely **absent falls back to a default (shipped Arial) and the text still draws** — no crash (the graceful counterpart to the malformed-font startup crash in [T3D-119](3d-file-loader-errors-420r6-2026-11-26.md)). A font must be **pre-placed on disk to apply**; a first-time on-demand fetch caches it but the triggering draw still falls back to default — the same "too late this session" behaviour as textures.

## 1. Name resolution & fetch **[lab]**

The client lowercases the family name and appends a style suffix + `.ttf`:

| `showtext` font, style | requested file |
| --- | --- |
| `"Arial"`, plain | `arial.ttf` — shipped, resolved locally (no request) |
| `"Arial"`, bold (`b`) | `arialbd.ttf` |
| `"Arial"`, bold+italic (`bi`) | `arialbi.ttf` |
| `"Arial"`, italic (`i`) | `ariali.ttf`, then `arialit.ttf` (second italic-name try) |
| `"Times"`, plain | `times.ttf` |
| `"Verdana"`, plain | `verdana.ttf` |
| `"arial.ttf"`, plain | `arial.ttf.ttf` — **`.ttf` is always appended**; passing an extension is wrong |
| `"Zzqqxx"`, plain | `zzqqxx.ttf` |

Rule: `lowercase(family)` + weight/slant suffix (`bd` bold, `i` italic with `it` fallback, `bi` bold-italic, none for plain) + `.ttf`. Alignment letters (`l`/`c`/`r`) in the style arg don't change the filename. **Do not pass an extension** in the font name — it is appended, producing `name.ttf.ttf`.

## 2. Formats

**TrueType (`.ttf`) only.** The client ships one font (`arial.ttf`); resolution always appends `.ttf`. There is no bitmap/other font format in the 3D `showtext` path.

## 3. Missing-font fallback

**A font that can't be found or fetched falls back to a default font and the text still draws** — not nothing, not a crash. Every styled / other-family / garbage-name line (including the deliberately absent `Zzqqxx`) rendered in the default (shipped Arial) when its file was "not found", and the client stayed up. This is the graceful counterpart to [T3D-119](3d-file-loader-errors-420r6-2026-11-26.md): a **validly-absent** font → default draw; a **malformed present** font → startup crash. **Absence is safe; corruption is not.**

## 4. Present-on-disk vs fetched (and cache naming)

A font must be on disk to render in that font; a first-time fetch caches it but doesn't apply it to the triggering call. Tested by serving a visibly distinct serif as `arialbd.ttf`:

- **Pre-placed before the call:** the bold line rendered **in the served serif** — pre-placed fonts are used.
- **Served on demand:** the client **downloaded** `arialbd.ttf` and cached it at **`levels/fonts/arialbd.ttf` — with its extension** (a dedicated fonts cache dir, unlike textures which cache under `levels3d/images/` *without* extension, [T3D-090](3d-shape-textures-420r6-2026-11-25.md)). But the triggering `showtext` **fell back to default** (plain sans, not the serif). The fetched file is cached for later, not applied to the in-flight draw.

So fonts are **fetched-on-demand for caching** but must be **pre-placed** (shipped, mounted zip, or cached from a prior session) to be used in the draw that needs them — the "too late this session" pattern textures also show.

## For a server

- Ship the exact resolved filenames the client requests — `lowercase(family)` + style suffix + `.ttf` (`arial.ttf`, `arialbd.ttf`, `arialbi.ttf`, `ariali.ttf`, `times.ttf`, `verdana.ttf`, …) — so the font is on disk before first use. A first-time fetch caches to `levels/fonts/<name>.ttf`, but that first draw falls back to default Arial.
- Only TrueType is accepted. Don't pass an extension in the `showtext` font name (it becomes `name.ttf.ttf`).
- **Never send a corrupt font** ([T3D-119](3d-file-loader-errors-420r6-2026-11-26.md): a malformed `.ttf` crashes the client at startup). A validly-missing font is safe (default fallback); a broken one is not.
