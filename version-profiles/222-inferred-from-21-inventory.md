# 2.22 profile rows: what is still “from 2.1 / inferred”

Date: 2026-11-16. Research-list rank **#9** (focus 2.220, carry 2.310). Inventory only — **no new binary read** this pass. Points at work still needed to replace era-default / inferred cells with 2.22-tagged evidence.

Tags: **[bin]** / **[cap]** already in `2.22-2.31.toml` and `2.22-2.31.md`; **[inf]** remaining; **[doc]** Seihai `documentation/version-profiles.md`.

## Scope

Seihai marks whole **2.1–2.16** profiles `Basis::Inferred` (no binary). **2.22** has a binary and is mostly `Basis::Binary`, but some fields still ride on **gen-5 era defaults** shared with 2.1+ or are explicitly incomplete. This note lists those cells so a later **S** pass can tick them without re-deriving settled rows.

## Already settled for Windows 2.22 (do not re-open)

| Area | Value / rule | Src |
|---|---|---|
| Token | `GNW03014` | **[bin][cap]** |
| Framing / gen-5 | u16be + ctype; raw&lt;0x30 / zlib&lt;0x1000 / bz2≥0x1000; XOR caps 12/4/4 | **[bin][cap]** |
| Login layout | type, key, token[8], account, password | **[bin][cap]** |
| PLO known set | 80 ids (no 84 / 189) | **[bin]** |
| PLI send sites | listed set; complete=false | **[bin]** (+ **[cap]** for 44) |
| Tampercheck 39 | 10 raw bytes; lab hex; resend on gmap edge | **[bin][cap]** |
| Large files | 68/69 receive cases; 32000-byte server chunks | cases **[bin]**; chunk size / era ≥2.14 **[srv]** |
| File modtime on 102 | true | era ≥2.1 **[srv]** + profile |
| Precise move | false | **[srv][bin]** |
| Feature UI (F1, start buttons, tabs) | as in TOML / live note | **[bin][cap]** |

Companion prose: `2.22-2.31.md`. Machine row: `2.22-2.31.toml` `[[version]] label = "2.22"`.

## Still open or era-carried (replace or re-tag)

| Cell / question | Why it is open | Suggested **S** (then optional **L**) |
|---|---|---|
| **PLI 36, 42, 45** | Send-helper sites unmatched; `pli_sent_complete = false`. Seihai: 2.22 does **not** send 36 or 45. | Confirm absence of call sites; keep complete=false until done |
| **Shared default provenance** | `defaults.gen5` is a local block used directly by 2.22/2.31; inferred 2.3 inherits 2.31, not a 2.1 profile. Server version gates are separate from exact-client reads | [Provenance pass](../protocol/file-profile-evidence-2026-11-21.md) separates existing per-build support and the remaining native reads |
| **List host / port built-in vs Seihai dial** | Profile records Reborn-era list endpoint; Seihai dials placeholders / defaults separately | Out of scope for binary protocol; keep as config history |
| **Community-edit caveat** | 2009 file date on `Graal_222.exe`; tabs/hosts may be patched | Document once; do not treat UI strings as protocol proof |
| **2.31 carry** | Separate binary; mostly settled. Residual: PLI 44 send policy in Seihai vs real client | Own row in TOML; not “from 2.1” |
| **2.3 (no binary)** | Entire row `inferred = true` from 2.31 + release notes | Needs a binary or stays inferred |

## Not this track

The [provenance reconciliation](../protocol/file-profile-evidence-2026-11-21.md)
links existing per-build framing, queue and UDP evidence, separates server chunk
size from receive cases, and preserves directional capture limits. It changes
TOML comments only: no value or generated consumer fixture changes. The remaining
native modtime/default-extension and numeric fixed-port questions stay open.

- **2.1–2.16** inferred profiles (no focus binary) — leave as Seihai `Basis::Inferred`.
- Gmap warp re-send / neighbour framing — assigned leads / ranks **#14/#15**, not profile TOML cells.
- Gen-5 **cipher step** short-compressed rule — that is 5.12 E#2 / research **#4**, not 2.22.

## Open checklist

- [ ] Static pass on Windows 2.22: unmatched PLI 36/42/45.
- [x] ~~Separate the historical server ≥2.1 file-default comments from exact-client evidence.~~ [Provenance pass](../protocol/file-profile-evidence-2026-11-21.md).
- [ ] Complete the remaining `defaults.gen5` native-field footnotes identified by that pass.
- [ ] After **S**, regenerate Seihai `profile_toml.tsv` if any TOML cell changes (Seihai `rows_match_version_profile_toml`).
