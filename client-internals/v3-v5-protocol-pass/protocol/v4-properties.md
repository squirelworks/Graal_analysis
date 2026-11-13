# v4 — properties

Date: 2026-11-08 · Tags: **[bin]**

## Script-facing player fields · **high** (names)

Engine exposes many `player*` accessors (`playerhp`, hearts, rupees, bombs, powers, dir, sprite, gender flags, map, …) plus `setplayerprop` / `setcharprop` / `makeprop`. RTTI: `TPlayer`, `TServerPlayer`, `TServerNPC`, `TBaddy`.

No cleartext `account,alpha,ani,…` comma registry (that lands later).

## Wire property ids · **high** (partial)

Numeric prop codec (get/set) and other-player applicator share the classic GCHAR space:

| id | Meaning (from string/normalize paths) |
|---|---|
| 0 | nickname / account-like |
| 8 | sword (`sword1`…`sword4`) |
| 9 | shield (`shield1`…`shield3`) |
| 11 | head (`head0` / gif) |
| 12 | chat text (fires `onRemotePlayerChats`) |

Other ids exist as numeric cases without friendly names in-image. On the wire, property bytes often appear as `id + 0x20` inside a props blob (after a 2-byte player id for remote players).

## showimg · **high**

GS1 `showimg` / `showimg2`; `TShowImg::getNetProperty` encodes attach fields with length-prefixed GCHAR strings.

## Diff vs v5 / v6

Late-5 similarly lacks a clear comma registry. v6.113 adds named lists + FE player-props bridge.
