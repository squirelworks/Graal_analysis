# NRY identity findings F01–F03 — publish status

Date: 2026-11-16. Research-list rank **#53**. Sanitised consolidation of three identity findings already on `main`; **no new binary session**.

Tags: **[bin]** launcher / strings / static walks already published; **[doc]** this index.

## F01 — `5.12-untouched` is 5.00r7

| Claim | Status | Canonical note |
|---|---|---|
| Windows FileVersion 5.1.2.0 “untouched v5” launcher is the **5.00r7** launcher re-versioned + one-byte window-title-scan bypass | **Settled** | [`launchers-420r8-500r7-512.md`](../client-internals/launchers-420r8-500r7-512.md) **[bin]** |
| Engine beside it is the 5.00r7 engine (CRC/license patch + auto-update skips) | **Settled** | same |
| Genuine 5.12 game engine is `Graal3DEngine.dll` (no `GraalEngine.dll` on stock 5.12) | **Settled** | same; [`v5-props.md`](../protocol/v5-props.md) |

Do **not** treat a “5.12 untouched” tree as a second 5.12 source for props, cipher, or weapon paths. Research **#4** / **#5** / **#6** use the genuine 5.12 engine image.

## F02 — 2.1.x GLEVNW01 / PLO 170–177 / controlnpc

| Claim | Status | Canonical note |
|---|---|---|
| Public 2.1.0.0 / Graal 2002 ladder knows `GLEVNW01` (and related level magics) as **level file** magics, not login tokens | **Settled** | [`graal2002-and-140-builds.md`](../client-internals/graal2002-and-140-builds.md); [`nry-coverage-teardown.md`](nry-coverage-teardown.md) **[bin]** |
| Public 171/172 destination and resource guards walked | **Settled** (rounding/display open) | graal2002 note § public 171/172; manual §2.5.2.2 |
| ver10 installs `Control-NPC` from `controlnpc.txt` when a gate byte is clear and the resolved path is nonempty; helper joins lines, does **not** compile/run GS1 | **Settled** (which weapons it replaces / whether text later runs: open) | graal2002 `#local-gmap-preload-and-controlnpc` **[bin]** |
| Public 2.1.0.0 widths for 170–174 and v22 widths for 175–177 | **Carried** in manual §2.5.2.2 | same note |

NRY strings hits on `GLEVNW01` / `GSERVL01` must not be read as connect tokens.

## F03 — 1.x `VERGRAAL` vs listserver path

| Claim | Status | Canonical note |
|---|---|---|
| Early Windows 1.25 / 1.27 installers and 1.3x FileVersion rows carry **`VERGRAAL`** (local DES key family / save wrap), not a listserver login token | **Settled** as strings evidence | [`nry-coverage-teardown.md`](nry-coverage-teardown.md); [`formats/graalsav.md`](../formats/graalsav.md) **[bin]** |
| Focus **1.39** has **no listserver / server-list path** — connect dialog host:port only | **Settled** (research **#8**) | [`build-catalogue.md`](../client-internals/build-catalogue.md) (“1.39 and earlier have no listserver”); [`versions-133-139.md`](../client-internals/versions-133-139.md) **[bin]** |
| seihai-listserver client table correctly starts at **1.41 rev 1** | **Settled** (companion listserver note / #545) | research #8 |

So: 1.x `VERGRAAL` hits are **save/local crypto literals**; getting online on 1.39 is **direct dial**, not list → Login.

## Open after this index

- F02: exact coordinate rounding / original-client display for 171/172; which built-in weapons `Control-NPC` replaces.
- F03: catalogue login-token re-read for FileVersion 1.3.8.0 (1.39) was not part of the NRY strings pass — use the catalogue, not this scan.
- Share Cursor packs 7/8 remain owner-held; this PR only points at already-public Graal_analysis notes.

## Checklist

- [x] Publish F01–F03 as behaviour-only index with links (this note).
- [ ] No further NRY identity publish until a new binary session changes a claim above.
