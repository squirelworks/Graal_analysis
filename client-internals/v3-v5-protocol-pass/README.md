# graal_analysis3 — cleaned v3–v5 notes

Date: 2026-11-08

Source: owner-held Windows, Mac and Linux v3–v5 client images; static read with Ghidra.  

Cleaned rules: no addresses, no `FUN_` names, no raw decompiler paste. Tables preferred.

## Status

| Topic | State |
|---|---|
| Inventory | `client-internals/older-v3-v5-inventory.md` |
| Late 5.x identity + framing | `protocol/v5-late-identity.md`, `protocol/v5-late-framing.md` |
| Remaining v5 / v4 / v3 | pending |
| `manual/sources.tsv` | started |

## Relation to 6.x

Late Quattro 5.30/5.31 sits **before** the 6.11 connector / AES / `onSend*` FE cut. Closest cleaned 6.x sibling is 6.037 (classic framing, no connector).
