# Pre-gmap clients in a gmap world

Date: 2026-11-16. Research-gaps / research-list rank **#12** (focus 1.39; 1.411 if it cannot play gmaps).

**Question:** how did an original server present a gmap world to a build that cannot load gmaps — separate linked levels, a refusal, or something else?

**Answer so far:** the **client-side limits** are settled for 1.39 and for the 2.00–2.04 gap. What a **period production server** actually sent a pre-gmap client on a gmap world is still **unobserved**. seihai-gserver does not yet emit the “gmap as linked single levels” fallback.

Tags: **[bin]** catalogue and format notes; **[doc]** cross-links; **[inf]** where behaviour is only inferred. No new binary or lab session in this pass.

## What each focus-era client can load

| Build | Board forms (catalogue) | Gmap / continuous overworld | Evidence |
|---|---|---|---|
| 1.39 (and 1.33–1.38) | `GR-V1.00`–`1.03` (+ offline `.zelda`). **No** `GLEVNW01`, **no** `GRMAP001`. | None. Connect dialog only; levels are single boards. | `versions-133-139.md`; `build-catalogue.md` **[bin]** |
| 1.41 rev 1 | `GR-V1.00`–`1.03`, **`GLEVNW01`** (string). Catalogue row has **no** `GRMAP001`. | No continuous gmap path recorded. Whether a real 1.41r1 loads `.nw` is still open (research-list **#11**). | `build-catalogue.md` **[bin]**; profile-audit gap for live `.nw` |
| 2.00–2.04 | `GR-V1` only (no `GLEVNW01` / `GRMAP001` strings). | None. | `build-catalogue.md` (“`.nw` support is not monotonic”) **[bin]** |
| 2.05 | `GR-V1`, `GLEVNW01`, **`GRMAP001`**. | Reader present; no static caller found; **no** `PLAYERWARP2` (49). Active map path is `bigmap.txt` / minimap overlays, not continuous gmap walk. | `formats/gmap.md` **[2.05][bin]** |
| 2.1+ / 2.22 | Full gmap file + wire path. | `PLAYERWARP2` (49), `PLI_ADJACENTLEVEL` (35), cell props 43/44. | `formats/gmap.md`; `feature-specs/06-gmap-overworld.md` **[bin][cap]** |

So for the focus build **1.39**, a server that only speaks “gmap as gmap” (warp into a `.gmap` name, neighbour boards without ordinary level links) has **nothing that client can consume**.

## What held original servers do

| Server | Gmaps? | Note |
|---|---|---|
| GServer 1.28 beta 2 / 1.3 (1999) | No | Predate `.nw` / `.gmap`. Single levels and ordinary warps only (`seihai-gserver` `ORIGINAL-SERVERS.md`; `server-notes/gserver-1999-rules.md`). **[bin]** |
| GServer-v2 / modern forks | Yes, for capable clients | Continuous gmap path for gen-5 style clients; classic-login neighbour framing is a separate open (`gmap-adjacent-level-target.md`). **[srv]** |

Gmaps as a client feature land with **2.05** (Aug 2001) and become the continuous overworld path in the **2.1** era. Asking what a 1999 binary did with gmaps is a category error: those builds never saw the format.

## Hypotheses for a mixed world (none proven for period servers)

When a later original list/gserver hosted both old and new clients on one world that *staff* thought of as a gmap:

1. **Version gate / separate start level** — old clients never receive a `.gmap` warp; they play a non-gmap hub or are refused. **[inf]**
2. **Expand to linked single levels** — server sends ordinary `LEVELNAME` + board + edge `LEVELLINK` warps instead of 49 / adjacent-level neighbour fills. This is what seihai-gserver’s profile row calls “gmaps as linked single levels”, and it is **not written yet**. **[doc]**
3. **Same gmap packets anyway** — old client ignores unknown ids / hangs on loading. Observed failure modes on modern labs for missing `.gmap` on disk (`gmap-file-on-warp.md`) are about **gmap-capable** clients, not 1.39. **[inf]**

No archive capture of an original 2001–2005 list+gserver serving **1.39** (or another pre-`GRMAP001` build) into a staff gmap world is in the notes. That is what would settle the question.

## Seihai today

- Profile / `GmapRules`: capable builds get gmap play; pre-gmap builds do not get an automatic single-level expansion (`CLIENT-PROFILES.md` Levels row; PARITY “Gmaps as linked single levels … not written”).
- Closing that row is **server design + lab**, not more 1.39 static: once a linked-level emitter exists, lab 1.39 against a gmap-shaped world on loopback.

## Open after this note

| Item | Status |
|---|---|
| 1.39 cannot load gmaps / `.nw` | **Settled** **[bin]** |
| Original-server presentation to pre-gmap clients | **Open** (needs period capture or server binary of the gmap era) |
| 1.41r1 `.nw` / gmap live load | **Open** (#11) |
| seihai single-level gmap output | **Open** (implementation) |
