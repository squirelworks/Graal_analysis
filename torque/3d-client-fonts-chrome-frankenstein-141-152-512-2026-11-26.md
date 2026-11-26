# What a 3D client brings on its own: 5.12 fonts and chrome, and the Frankenstein 6.037 rendering the real world live (T3D-141/152)

Date: 2026-11-26. Lab: a real 5.12 in a Windows 10 VM and our own-build "Frankenstein 6.037"
(from-source hybrid, sha256 `ccc57f5f…0756`) against seihai-gserver main (5cd9c15) on the
loopback. Behaviour only; lab tooling stays in the lab kit, off every PR. **[lab]**

Two rows on what a client supplies for itself, separate from what the server ghosts: what a
5.12 fetches and draws with no world content (fonts, 2D art, UI chrome — T3D-141), and whether
our Frankenstein 6.037 build can run a full live 3D session and what it now draws (T3D-152).

## T3D-141 — default fetches, on-demand fonts, and no UI chrome in the 3D view

**The default 3D session's own fetches** (identical across 71 prior 5.12 session traces plus a
fresh run): the only font requested is `arial.ttf`, which the server does not have ("not sent"),
so the client falls back to its **built-in Arial**. Alongside the world's own assets (shapes,
sky, terrain textures, `lightfalloffmono` with terrain) the client also fetches its 2D-side
player/HUD art at login — `head0.png`, `head26.png` (sometimes `head25`), `idle.gani`,
`wbowi1.png`, `wbomb1.png` — but **none of it is drawn in the 3D view**. No `.gft`, no GUI
profiles, no other fonts are requested.

**Fonts are fetched on demand, and the list is not fixed.** Served a `labfont.ttf` and a
`showtext` line in several font names, the 5.12 **does** fetch TTFs from the server on demand,
addressed by **family name, lowercased** (plus `bd` for bold), via Windows' font-file mapping:
Arial → `arial.ttf`, bold → `arialbd.ttf`, Verdana → `verdana.ttf`/`verdanabd.ttf`,
"Courier New" → `cour.ttf`, "DejaVu Serif" → `dejavu serif.ttf` (+`bd`), `labfont` →
`labfont.ttf`, and the literal `"labfont.ttf"` → `labfont.ttf.ttf`. The served `labfont.ttf`
(356 668 bytes) was sent and **rendered** — the line redraws in its bold serif once the file
arrives, Arial until then — and a missing font gives a quiet "not found" and an Arial fallback
with no error. So the shipped font set is not a fixed table; a world can serve its own TTFs.

**No Era-A UI chrome in the 3D view.** The 3D view draws **none** of the 2D HUD furniture — no
hearts, no AP/MP bars, no rupee or weapon boxes, no chat bar, no player list. The 2D HUD art
fetched at login is simply not drawn here. The only non-world element is the launcher's
"Starting 3D mode…" box (a documented Wine leftover). **The 3D HUD is a separate, script-drawn
layer** — nothing chrome-like is built in.

Not tested: a `.gft` (GameShapeFT label, the T3D-036 path) — no world syntax to emit one was to
hand and none of the 72 sessions requested one, so it stays an open item under T3D-036, not here.

## T3D-152 — the Frankenstein 6.037 runs a full live session and now renders the real world

Our Frankenstein 6.037 (build sha256 `ccc57f5f…0756`) ran a complete multi-step 3D session
against the live gserver, `--account guest`, assets at `C:\g512`:

- **Link and login.** The server logged it in as 6.03r7 (`G3D0311C`), linked proto 24, finished
  mission start, ghosted the whole world (Sun, Sky, RED, RED2, avatar, Camera, TerrainBlock) and
  delivered the control object at seq 4. **0 moves received** — like the 5.12, it sends no 3D
  movement of its own (the position lives in the game section). The client console walked the
  full ladder: UDP connect → established → Phase 1 download-ghosts/login step 2 → weapon loaded →
  Phase 2 mission lighting/step 3 → lighting done/step 4 → initial control object/step 5 → step 6
  → asking for `bigred.3ds` → got (505 bytes) → "3D yes, login step 6".
- **Server-text → 6.x GS2 bridge works for execution.** The seihai-core-compiled GS2 `weapon3d`
  loaded and ran: `triggerserver`s moved the player and drove **both** world switches (to a cave
  with fresh Sky/BIG/MARK creates, and back to the default with Sky/RED/RED2), including the
  on-demand fetch of the cave's `bigred.3ds`. **But the script's `showtext` line never appeared**
  — so script *drawing* (showtext) is either not bridged or hidden, while script *execution* is.
- **It renders the real world live.** The view is the real Torque scene with **textured terrain**
  (blue water and sand — where a 5.12's GDI/software path draws plain white), sky, the cubes, the
  cave's fog sky and BIG block, plus a 2D "GRAAL" inset bottom-left. It also showed the T3D-155
  stale-cache effect (orange sky / green cubes left in the `C:\g512` cache), so that caching
  behaviour applies to the Frankenstein too.
- **Clean quit.** A plain `taskkill` produced a real disconnect ("link closed (client
  disconnected)", then "pc:1 left (client closed)") — no half-open link left behind.

**This updates the static Frankenstein note.** The static read
([T3D-122](3d-frankenstein-6037-vs-600-2026-11-26.md)) recorded that the build "renders only a
stand-in box/grid view, not the real Torque 3D scene (that renderer is future work)." The build
has advanced since that read: run live, **build `ccc57f5f…0756` renders the real textured world**,
not a box/grid. The box-view renderer that the static note called future work is now wired in.
What that note listed as still missing holds only in part — the real renderer works; `showtext`
(script-drawn text) is the piece that does not yet appear, and interactive keyboard movement was
not exercised here.

## Verdict

A 3D client brings very little of its own. A 5.12 ships one fallback (built-in Arial) and
otherwise pulls every asset from the server — including fonts, on demand and by lowercased family
name, so a world can serve its own TTFs — and draws **no** built-in UI chrome in the 3D view;
the 3D HUD is entirely a script-drawn layer (T3D-141). Our Frankenstein 6.037 build is now a
fully working proto-24 3D client: it runs the complete link/login/ghost/control-object ladder,
bridges server text into its 6.x GS2 machine to execute scripts, switches worlds with fresh
creates and on-demand fetches, sends no movement of its own (like the 5.12), and — the headline —
**renders the real textured Torque world live**, superseding the static note's box-view claim.
The one remaining gap on the Frankenstein is script-drawn `showtext`, which does not appear
(T3D-152).

## Summary

| row | verdict |
| --- | --- |
| T3D-141 | A default 5.12 3D session requests only `arial.ttf` (server lacks it → built-in Arial) plus the world's own assets; it also fetches 2D player/HUD art at login (`head0/head26.png`, `idle.gani`, `wbowi1/wbomb1.png`) that is **never drawn in 3D**. Fonts are fetched on demand by lowercased family name (+`bd` bold) via Windows file mapping (Arial→`arial.ttf`, "Courier New"→`cour.ttf`, etc.) and rendered when present (served `labfont.ttf` drew in bold serif), missing→Arial fallback, so the font set is not fixed. No Era-A UI chrome renders in the 3D view (no hearts/bars/boxes/chat/player-list); the 3D HUD is a separate script-drawn layer. `.gft` untested (belongs to T3D-036). **[lab]** |
| T3D-152 | Our Frankenstein 6.037 (sha256 `ccc57f5f…0756`) runs a full live 3D session vs seihai-gserver: links proto 24 as 6.03r7, finishes mission start, ghosts the world + control object at seq 4, and — like the 5.12 — sends **0 moves** (position in the game section). Its server-text→6.x GS2 bridge executes scripts: a seihai-core GS2 weapon moved the player and drove two world switches with fresh creates and an on-demand `bigred.3ds` fetch; a clean `taskkill` gave a real disconnect. **Renders the real textured Torque world live** (blue water + sand terrain, not a box/grid), which **updates** the static note's "stand-in box/grid only, real renderer future work" claim ([T3D-122](3d-frankenstein-6037-vs-600-2026-11-26.md)) — the renderer is now wired in. Only gap: script-drawn `showtext` does not appear (execution bridged, drawing not). **[lab]** |
