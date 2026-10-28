# Extra gates on a hit, and open points

## Gates
Beyond the swing sprite (S 6..10), the reach box, the victim's state (not dead, not in hurt mode, not swimming) and AP not 100, the client's shared hit-judging routine also requires:
- the current level has not run the script command `noplayerkilling` (a per-level flag, cleared when a level is created; the client prints the text `nopkzone` when its own attack is refused by it);
- the attacker has not already been judged in the current second of the day: the routine keeps a per-attacker last-second stamp and drops a second judgement in the same second. The stamp is set before the guild and box tests;
- the attacker's `(tag)` is not in the victim's nickname: the attacker's nickname is searched for its first `(`, then the first `)` after it with at least one character between them, and that bracketed text is searched in the victim's nickname (case-sensitive, anywhere). Nicknames are kept obfuscated in memory;
- (swing path) the attacker's STATUS has neither bit 0x02 (hidden) nor bit 0x20, and the attacker is not in the kick animation (2.05 by animation name; 2.17.1 and later by an object id of 3).
The hurt packet (40) handler checks the no-kill level flag, a per-player field that must be equal for attacker and victim, the 10-tile range, and caps the power at one heart.

## Level flags seen
- `noplayerkilling` (script command) sets the no-kill flag.
- `sparringzone` (NPC script command) sets a second level flag that lets a player in the editor or paused state be hurt; the "can be hurt" check is: not in hurt mode, not dead, not swimming, hearts above 0, and (normal play or that flag).

## Open
See open-questions.tsv. Main ones: the per-player field in the hurt-packet path; bit 0x20's meaning; knockback of the sword path; which other callers (bombs, arrows, baddies) use the hurt routine with which power; whether the guild test also applies to the hurt packet; the gmap list's order and the timing of its update against the entry save; the end-of-respawn save; the entry rule in the 2.1 test builds; no lab confirmation.
