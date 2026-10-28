# Decompile mining, batch d: sword damage and the respawn entry save, 2026-10-25 (Asia/Tokyo)

Derived facts only. No raw decompile text, no addresses, no generated function names, no code, no paths. The raw exports stay private. Nothing was pushed to Graal_analysis, no public server was contacted, the lab was not touched. Nothing here was seen on a wire.

Scope: the two rules that Seihai's combat and health/death work had left as placeholders. Read in the 2.05 rev 2, 2.17.1, 2.22 and 2.31 clients, with the 2.1 test builds and all other builds checked only for one constant (see 02).

## Files
| file | content |
|---|---|
| 01-sword-damage.md | how the victim's client turns a hit into hearts, the sword-power byte, heal rule, hurt mode |
| 02-respawn-entry-save.md | which level entry is saved as the respawn point, the gmap-list test, the name group (2.00 to 2.05) |
| 03-hit-gates-and-open-points.md | extra gates on a hit (no-kill level, guild tag, attacker status, per-second limit), and what is still open |
| damage-rules.tsv | the damage rules, one row each, with the builds they were read in |
| hit-gates.tsv | every gate a hit must pass, in the order the client checks, per path |
| entry-save-rule.tsv | the save-entry decision table |
| name-group-constant-by-build.tsv | which builds contain the name-group delimiter constant |
| open-questions.tsv | what was not resolved |

## Top facts
1. A sword hit takes the attacker's sword power in half hearts, limited to -20..20. Shield, item levels and the attacker's AP are not read. Same in 2.05 rev 2, 2.17.1, 2.22, 2.31.
2. A negative power heals only a victim with AP 40 or more; below that it changes no hearts. Hurt mode (mode 3, 40 ticks) starts for every accepted hit, including power 0.
3. The sword-power byte on the wire is 0..4 for the default swords 1..4, and power + 30 (10..50) plus an image name otherwise.
4. A hit is dropped when the level ran the script command `noplayerkilling`, when the attacker's `(tag)` is in the victim's nickname, when the attacker's STATUS has bit 0x02 or 0x20, and when the same attacker was judged earlier in the same second of the day. The hurt packet (40) is stopped by the no-kill level too.
5. The respawn point is the last *saved* level entry. An entry is saved when there is no previous level, or when exactly one of {old level, new level} is in the current gmap's level list (the client multiplies the two list indices with -1 for "absent", so index 0 behaves like "absent": a quirk).
6. In 2.00 to 2.05, an entry that fails that test is still saved when the old and new levels are in different name groups. The name group is the file name without its folder, lower-cased, up to and including the last `§` or `$`; with neither, the group is empty. 2.17.1, 2.22 and 2.31 have no group test; the 2.1 test builds do not contain the delimiter constant.
7. With plain level names, the respawn point is therefore the login spot or the last gmap boundary crossing.
