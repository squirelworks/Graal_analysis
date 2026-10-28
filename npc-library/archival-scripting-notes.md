# Archival Scripting Notes

This note records prior analysis of Classic Graal NPC scripting systems, performed outside this repository and archived on decommissioning of the analysis project (2026-10-28).

## Source Archive

A full dump of extracted, catalogued, and documented NPC scripts plus architecture notes was packaged as **Graal Scripting.zip** (24 MB, ~3,900 files) and uploaded to Google Drive under `/[Grok/[Projects/`.

Direct link: https://drive.google.com/file/d/1WDbffUEHO-rwa6FcVSXYG7KfSr1SKxVu/view

The archive contains:

- **Grokd extract** — cleaned unique script bodies (1,520 unique from 6,275 placements), `CATALOG.tsv` with body-hashes, packs concatenated per system.
- **Phoenix documented copies** — same scripts with analysis headers (source path, classification, events hooked, functions, `toweapons` names, `client.*` / `save[]` usage, timeout rates, gotchas).
- **Ash architecture docs** — runtime model of the Classic client NPC engine (events, timeout scheduler, weapon-bar persistence, image ID bands), plus per-pack blueprints, flowcharts, algorithms, and pseudocode for larency HUD/inventory, Phoenix quests/farm, Meh weapons/smartbaddy, Ultimate NPC Pack minigames, and standalones.
- Original pack folders and assets (larency, ultimatenpcpack1, etc.).

## Classification Summary (from Ash)

Across ~1,519 documented scripts:

| Class | Approx. count | Typical home |
|-------|---------------|--------------|
| quest / dialogue | 516 | Phoenix |
| level prop / trigger | 390 | UNP + Phoenix |
| farm / planting | 136 | Phoenix |
| player weapon / projectile | 135 | Meh + UNP |
| shop / merchant | 111 | UNP + larency |
| minigame | 59 | UNP + Phoenix |
| enemy / baddy AI | 44 | Meh + Phoenix |
| inventory / equipment UI | 37 | larency |
| HUD / stats overlay | 20 | larency |

Dominant author tags: tricxta (HUD/inventory/shop), Ace2896 (weapons + smartbaddy), Agret (UNP houses/minigames), plus community.

## Runtime Model Highlights (Classic client)

- Pure client-side NPCs. No separate server VM visible in the dump.
- Level NPC vs weapon NPC (`toweapons -Name`) vs putnpc children.
- Tick model is `timeout = N` (seconds) → `if (timeout)` wake; common rates 0.05 (AI/HUD), 0.1–0.2 (menus), 0.5–1.0 (idle).
- Persistence: `toweapons`, `save[n]`, `client.*` flags.
- Image ID collisions common in the ~300+ band used by HUDs and shops.

These notes are complementary to the existing `npc-library/` unique scripts and `gs1-reference-205.md`. They emphasize control flow, host effects, and real-world patterns useful for offline script engines.

## Boundary

No raw decompiles or proprietary client code. All material is derived from public level dumps, observed script behavior, and open documentation. The archive is for reference only; it is not a playable server or complete asset set.
