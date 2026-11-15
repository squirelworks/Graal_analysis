# 1.41 rev 1 `.nw` / gmap load status

Date: 2026-11-16. Research-gaps / research-list rank **#11** (focus 1.411).

**Question:** does a real 1.41 rev 1 load `.nw` levels, gmaps, cached links and heights?

**Answer so far (static only):** the catalogued binary **carries a `GLEVNW01` (`.nw`) loader string** and **does not carry `GRMAP001`**. A live `.nw` (or gmap) load against a gserver has **not** been recorded. Cached links / heights for this build stay profile-audit unknowns until that lab (or a deeper static of those paths) runs.

Tags: **[bin]** string / catalogue; **[doc]** cross-links. No new binary session in this pass.

## Settled from the catalogue

| Feature | 1.41 rev 1 (`graal_gr1411`) | Evidence |
|---|---|---|
| `GR-V1.00`–`1.03` | Yes | `build-catalogue.md` levels column **[bin]** |
| `GLEVNW01` (`.nw`) | **String present** (loader listed with GR-V1) | same **[bin]** |
| `GRMAP001` (`.gmap`) | **Absent** from the catalogue row (unlike 2.05+) | same **[bin]** |
| Continuous gmap wire (`PLAYERWARP2` 49, cell props) | Not attributed to 1.41; gmap era is 2.05+ / 2.1+ | `formats/gmap.md`; `pre-gmap-in-gmap-world.md` **[bin]** |
| Live `.nw` load | **Unobserved** (“no `.nw` level was loaded in a real 1.41” in profile-audit) | research-list / profile-audit **[doc]** |

Related: `.nw` support is **not monotonic** across early 2.x — 1.41r1 and NewMain 1.42 have `GLEVNW01`, 2.00–2.04 drop it, 2.05 restores it with gmaps (`build-catalogue.md`). That strengthens the string finding but still does not replace a live load.

## What a lab must show

Loopback only. Suggested minimum:

1. seihai-gserver (or lab classic pack) with a small **`.nw`** start level the 1.41r1 account can reach.
2. Real 1.41r1 through list (shape S / `silent_list_after_ms`) then connect; confirm board draw and that the level on disk / on the wire is GLEVNW01.
3. Optional second world: a tiny **`.gmap`**. Expect failure or ignore (no `GRMAP001` in the catalogue); record the actual client behaviour.
4. If `.nw` draws: note whether cached links / heights messages appear (or are absent) for the open profile-audit rows.

Until that run, treat “1.41r1 plays `.nw` online” as **[inf]** from strings only.

## Open after this note

| Item | Status |
|---|---|
| String-level `.nw` loader present | **Settled** **[bin]** |
| No `GRMAP001` in catalogue | **Settled** **[bin]** |
| Live `.nw` load / play | **Open** (lab) |
| Live gmap behaviour | **Open** (expect none; confirm in lab) |
| `cached_links` / `heights` profile rows | **Open** |
