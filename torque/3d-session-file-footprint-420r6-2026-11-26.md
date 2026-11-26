# What a 5.12-class 3D session writes to disk: the `.graal/` cache tree, no screenshot from a script key, no heights/lightmap cache (T3D-053, T3D-100; Linux 4.20r6)

Date: 2026-11-26. Single-client lab on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route), software GL; full-session file read/write trace. Observation only. Board rows: [T3D-053](3d-capability-board.tsv) (session files/screenshots/caches) and [T3D-100](3d-capability-board.tsv) (which files the client writes by itself) — one run answers both. Extends the static reads in [3d-formats-renderer-camera-by-build](3d-formats-renderer-camera-by-build.md) and [3d-engine-static-reads](3d-engine-static-reads-2026-11-25.md); sky/texture naming per [T3D-090](3d-capability-board.tsv).

## Headline

A normal 4.20r6 3D session (login → sky+shape scene → idle → quit) writes a **predictable `.graal/` cache tree** and nothing else of the client's own. **No screenshot file is written** even when the engine's screenshot path is invoked from a script or by the F-keys; **no `heights`, terrain or interior lightmap cache** appears (that content belongs to terrain/interior data the lab server doesn't emit).

## Files written, under the client dir **[lab]**

- `.graal/.registry`; `.graal/graal4/console.log`
- `.graal/graal4/levels3d/images/` — the **3D content cache**: shapes keep their extension (`…/images/redcube.3ds`); **sky** textures land under `…/images/sky/` **without** an extension (`sky_fr`, `sky_rt`, …), exactly the [T3D-090](3d-capability-board.tsv) naming.
- `.graal/graal4/global/` — shared assets (e.g. the player shape).
- `.graal/graal4/updatepackages/<server>/basepackage.gupd` — the per-server update package.
- `.graal/graal4/weblevels/weapons/<server>/<WeaponName>.code` — cached client-side GS2 weapon bytecode.

Not the client's own content, but present in the headless lab: a Mesa/llvmpipe shader cache under `.cache/mesa_shader_cache_db/` — a software-GL artifact of this environment, not something the client writes.

## Not written in this scene

- **No screenshot file.** The engine exposes a screenshot path (GS2 `makescreenshot2(…)` with `$pref::video::screenshotformat`), but calling `makescreenshot2` from a script produced **no file** — script capture appears gated (`$pref::capture::allowbyscript` reads as read-only) — and the F-keys pressed wrote nothing (one only changed the resolution). The capability exists in-engine; no on-disk screenshot was produced here.
- **No `heights`**, no interior/terrain lightmap cache (`*_lm_*.png`), no `FILENAMECACHE`. Those belong to terrain/interior content the lab server does not emit, so they never appear in a sky+shape scene.

## For a server

A 3D session's on-disk footprint stays in the user's `.graal/` tree: the content cache under `levels3d/images/` (shapes with their extension, sky textures without), shared shapes under `global/`, the per-server `updatepackages/<server>/basepackage.gupd`, cached weapon `.code` under `weblevels/weapons/<server>/`, plus `console.log` and `.registry`. A server cannot rely on the client writing a screenshot on a script trigger (capture is gated to user action).

## Method caveat

Single client, loopback server, software GL, one representative sky+shape scene. The "not written" set is scoped to that scene — terrain/interior caches (`heights`, lightmaps, `FILENAMECACHE`) need content this lab server doesn't serve, so their absence here is expected, not a proof the client never writes them for terrain worlds. The screenshot negative is from a script call plus F-key presses; a user-driven capture binding was not exercised.
