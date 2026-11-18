# Two-player sword edge on 1.35, 2026-11-18 (#443)

Checks the sideways reach rule in
[combat-baddy-tile-by-version.md](../../client-internals/combat-baddy-tile-by-version.md):
`|side| <= 2` tiles, edge included.

## Setup

- Two real 1.35 clients (`GNW13040`, the `graal135` install), one per Xvfb screen, under
  user-space Wine in a loopback-only network namespace (only `lo`).
- Server: seihai-gserver (Rust) in that namespace, behind a logging relay. Plain grass
  level `door45.nw`, anticheat off.
- Placement through the account files before login: attacker at (20, 40) facing down
  (`SPRITE 2`); victim at (20 + dx, 40 + 2), also full hearts (3).
- The attacker swings three times (S held 0.35 s, 1.2 s apart). The victim's client judges
  the hit, so a hit shows as the victim sending its own lower power (prop 2) and a
  knockback.
- Raw relay logs and screenshots are kept privately; this page has the derived result.

## Result

| dx (tiles, sideways) | forward | attacker swings seen | victim power after | verdict |
|---|---|---|---|---|
| +2 | 2 | 3 | 3 → 2.5 hearts, knocked back | **hit** |
| −2 | 2 | 3 | 3 → 2.5 hearts, knocked back | **hit** |
| +2.5 | 2 | 3 | 3 (no prop 2 sent) | miss |
| −2.5 | 2 | 3 | 3 (no prop 2 sent) | miss |

So on 1.35 a victim exactly 2 tiles to the side is hit, on both sides, and half a tile
further is not: the edge is **included**, as the static read says. One hit per round of
three swings (the 40-tick hurt time covers the next swings).

## Not covered

- Other builds (the rule is read from every build 1.21 to 2.31; only 1.35 was run).
- The forward reach (0 to 4 tiles) was not swept.
