# Decompile findings, batch k: hit knockback, packet-hit gates, save-folder layouts by build, 2026-10-25 (Asia/Tokyo)

Derived facts only. No raw decompile text, no addresses, no generated function names, no code, no paths. The raw exports stay private. No public server was contacted and no lab run was made for these facts.

Scope: the leftovers of batch d (damage and respawn) and batch e (file transfer). Static read of the 2.05 rev 2, 2.17.1, 2.22 and 2.31 clients (hit path), and of the 1.33 to 1.41, 2.00 to 2.05, both 2.1 test builds, 2.17.1, 2.22 and 2.31 clients (save routine).

## Files
| file | content |
|---|---|
| 01-knockback-and-packet-hits.md | the knockback of a hit, the gates of packets 40 and 46, the 46 box, what stays unknown |
| 02-save-folders-by-build.md | the save routine's folder layout in each build, the empty-stream guard |
| 03-open-points.md | what was not resolved and which capture would settle it |
| knockback-probes.tsv | the body-box probe offsets |
| save-folders-by-build.tsv | the folder layouts per build |
| open-questions.tsv | unresolved points |

## Top facts
1. A hit starts hurt mode (40 ticks) and moves the player one tile per tick for the first five ticks along the knockback vector scaled to length one (a zero vector means east). After each step twelve body-box points are tested; if one is blocked the step is undone. Same in 2.05 rev 2, 2.17.1, 2.22, 2.31; the twelve offsets are identical in all four.
2. Packets 40 and 46 go through the sword's gates (attacker known, victim hurtable, AP not 100, level not no-player-killing, the once-a-second stamp per attacker shared with the sword and taken before the guild test, the guild tag test) and then a range test (40) or a box test (46). There is no attacker status test on the packet path. Power is capped at one heart; power 0 is accepted.
3. Packet 46's hit point is (b1/2, b2/2); a player's centre is (X+1.5, Y+2.0); the box is strictly under 2 tiles on each axis. The knockback is centre minus hit point.
4. The per-player field compared in packet 40 is an owner or parent link and is zero for ordinary players, so the comparison is always true for them (inferred from its other uses, not seen on a wire).
5. Save folders: 1.33 to 1.41 save everything in one folder (`levels/webgifs`); 2.00 and 2.01 have the folder list without `hats`; `hats` appears in 2.02; both 2.1 test builds have no `maps` folder rule, which first shows in 2.17.1.
6. Every build from 1.39 to 2.31 returns from the save routine at once for a missing or zero-length stream: nothing written, nothing deleted.
