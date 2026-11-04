<!-- manual: kind=reference status=draft -->
# 4.4 Death clocks and respawn

This chapter gives what the client does when its hearts reach zero, the death timer, the dead bit on the wire, the respawn key, the hearts and the destination after respawn, and the level-entry save that picks the destination. What the server does on the dead bit is in → §5. Damage is in → §4.3.

> Status: draft. Read for 1st Graal, 1.39, 2.00 to 2.05 rev 2, 2.17.1, 2.22 and 2.31; timed live for 2.05 and 2.22. Open points are App. E#314 and E#315.

## 4.4.1 Life-states

| Value | Life-state | Source |
| --- | --- | --- |
| 0 | playing | [2.05] (client-internals/decomp-findings-2026-10-24/life-states.tsv) |
| 1 | editor or pause | [2.05] (client-internals/decomp-findings-2026-10-24/life-states.tsv) |
| 2 | dead | [2.05] (client-internals/decomp-findings-2026-10-24/life-states.tsv); [1.39] (version-profiles/matrix/rules-139.md#death-and-respawn-bin) |
| 4 | a state in which any key restarts, with no timer test (1st Graal, 1.39); not named | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [1.39] (version-profiles/matrix/rules-139.md#death-and-respawn-bin) |

## 4.4.2 The death sequence (2.05)

| Step | Rule | Source |
| --- | --- | --- |
| trigger | any change that leaves hearts at 0 or below starts the sequence once; a per-frame check also forces the dead state whenever hearts are 0 or below | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#trigger) |
| 1 | the death timer starts at 0 and counts up one per tick; it stops at 30 (1.5 s) | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#sequence-on-the-dying-client) |
| 2 | the life-state becomes dead, the mode returns to 0 and the player faces down | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#sequence-on-the-dying-client) |
| 3 | the `dead` gani plays and the script event `playerdies` fires | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#sequence-on-the-dying-client) |
| 4 | controls are ignored until the timer passes 27 (1.35 s) | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#sequence-on-the-dying-client) |
| 5 | STATUS (prop 18) carries the dead bit 0x08 only while the life-state is dead and the timer is at least 28, so other players see the death about 1.4 s late | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#sequence-on-the-dying-client) |
| 6 | no dead sprite goes on the wire: SPRITE shows idle plus direction | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#sequence-on-the-dying-client) |

On the wire:

| Rule | Detail | Source |
| --- | --- | --- |
| server CURPOWER 0 | the client at once sends the `dead` gani and no CURPOWER; 27 ticks later STATUS 0x1C (dead bit set) | [live][cap][2.05] (client-internals/live-trace-205.md#server-curpower-0-death-and-respawn-live-online-2026-10-29) |
| 2.22 | `dead` gani and one more prop, no CURPOWER; then STATUS 28; the board goes black and an "End" scroll in the sign style appears under the player | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#c-curpower-semantics-settled-for-222); [cap] (live-runs/2gta-222-2026-10-30/README.md#baddies-death-and-respawn-2118-to-2121) |
| offline | burning to 0 hearts offline shows the `End` death scroll | [live][2.05] (client-internals/live-trace-205.md#water-and-lava-live-new4nw) |
| baddies | a leader client stops sending baddy props the moment it dies | [cap] (live-runs/2gta-222-2026-10-30/README.md#baddies-death-and-respawn-2118-to-2121) |

## 4.4.3 Respawn

| Rule | Detail | Source |
| --- | --- | --- |
| key | once the timer has passed 27, any movement or action key respawns the player; there is no timer-only respawn, no respawn message and no server permission step | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#respawn); [cap] (live-runs/2gta-222-2026-10-30/README.md#baddies-death-and-respawn-2118-to-2121) |
| destination | the last saved level-entry point (level, x, y, direction; → §4.4.4) | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#respawn) |
| nothing saved, online | x 30.5, y 30.0, facing down, in the current level | [2.05] (client-internals/decomp-findings-2026-10-24/constants-205.tsv); [1.39] (version-profiles/matrix/rules-139.md#death-and-respawn-bin) |
| nothing saved, offline | the default start level `tutorial_b-4.graal` (axes of its start position unread) | [2.05] (client-internals/decomp-findings-2026-10-24/constants-205.tsv); [2.05] (client-internals/decomp-findings-2026-10-24-d/open-questions.tsv) |
| online warp | the client re-sends the level at the destination, so the server sees an ordinary level warp, not a "died" message; it does not wait for a reply | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#respawn); [live][cap][2.05] (client-internals/live-trace-205.md#server-curpower-0-death-and-respawn-live-online-2026-10-29) |
| 2.05 frame | `PLI_LEVELWARP` (0) to the same level at the login point, and in the same frame CURPOWER, GANI `idle`, X, Y and STATUS with the dead bit cleared | [live][cap][2.05] (client-internals/live-trace-205.md#server-curpower-0-death-and-respawn-live-online-2026-10-29) |
| 2.22 frame | the level warp, `PLI_TAMPERCHECK`, any script flags, then props with CURPOWER (full hearts), GANI `idle`, X, Y, SPRITE and STATUS; the server echoes the position and the hearts | [cap] (live-runs/2gta-222-2026-10-30/README.md#baddies-death-and-respawn-2118-to-2121) |
| dead bit | cleared when the life-state returns to playing | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#respawn) |
| repeat | a server that answers every respawn with CURPOWER 0 puts the client into a death loop | [live][2.05] (client-internals/live-trace-205.md#server-curpower-0-death-and-respawn-live-online-2026-10-29) |

### 4.4.3.1 Hearts after respawn

| AP | Hearts (2.05, 2.22) | Source |
| --- | --- | --- |
| below 20 | 3 | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#respawn); [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#c-curpower-semantics-settled-for-222) |
| 20 to 39 | min(5, max hearts) | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#respawn); [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#c-curpower-semantics-settled-for-222) |
| 40 or more | max hearts | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#respawn); [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#c-curpower-semantics-settled-for-222) |
| MAXPOWER 0 | 2.05 still reports CURPOWER 6 (3 hearts): the respawn hearts are not capped at a MAXPOWER of 0 | [live][2.05] (client-internals/live-trace-205.md#server-curpower-0-death-and-respawn-live-online-2026-10-29) |

### 4.4.3.2 By build

| Rule | 1st Graal | 1.39 | 2.05 rev 2 | 2.22 | Source |
| --- | --- | --- | --- | --- | --- |
| on death | hearts clamped to 0, counter and mode cleared, dead state; the relay object is notified; no inventory spill, no sound | hearts clamped to 0, counter 0, mode normal, dead state; `dead.wav`; the inventory partly spilled as floor items (rupees in 100/30/5/1 bands, arrows and bombs alike) | → §4.4.2 | → §4.4.2 | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [1.39] (version-profiles/matrix/rules-139.md#death-and-respawn-bin) |
| timer | the up-count loop not found; the dead sprite and the key wait for a reading above 27 | counts 0 to 30 and stops | 0 to 30 | unmeasured | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [1.39] (version-profiles/matrix/rules-139.md#death-and-respawn-bin) |
| drawing | the board replaced by a filled rectangle and a text panel; the body uses sprite 157 once the counter is above 27 | death sprites cycle between counters 4 and 27; a cleanup runs above 29 | the `dead` gani | the "End" scroll | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [1.39] (version-profiles/matrix/rules-139.md#death-and-respawn-bin) |
| dead bit 0x08 | n/a (no STATUS prop) | only while dead and the counter is above 27 | at 28 or more | sent | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [1.39] (version-profiles/matrix/rules-139.md#summary-table) |
| key | above 27 (one key index does not restart) | above 27 | above 27 | a key, after 34 s in the run | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [1.39] (version-profiles/matrix/rules-139.md#summary-table); [cap] (live-runs/2gta-222-2026-10-30/README.md#baddies-death-and-respawn-2118-to-2121) |
| destination | the new-game setup: `house1.graal` at (24.5, 30), facing 2; a second local player 12 tiles to the east | the saved entry, else (30.5, 30.0) online, else the built-in start-level table offline | → §4.4.3 | the level's entry point | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [1.39] (version-profiles/matrix/rules-139.md#death-and-respawn-bin); [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#d-end-of-respawn-save-settled-for-222-same-level-respawn) |
| hearts | 3, and the heart cap set to 3 | max hearts, no AP bands (1.39 has no AP display; the bands arrive with 1.41) | by AP | by AP | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [1.39] (version-profiles/matrix/rules-139.md#summary-table) |

## 4.4.4 The level-entry save

Run after every level entry, and at login; saving stores the new level's name, the player's x and y, and the direction as it is [2.05] (client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md#the-decision-run-after-every-level-entry).

| Step | Condition | Result | Builds | Source |
| --- | --- | --- | --- | --- |
| 1 | the level left is empty (login) | save | all read | [2.05] (client-internals/decomp-findings-2026-10-24-d/entry-save-rule.tsv) |
| 2 | index(new) × index(old) in the current gmap's level list is negative (-1 = absent; an index of 0 gives 0, so the first list entry behaves like "absent") | save | all read | [2.05] (client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md#the-decision-run-after-every-level-entry) |
| 3 | the name groups differ | save | 2.00 (all revisions) to 2.05 rev 2 | [2.05] (client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md#which-builds-have-the-group-test) |
| 4 | otherwise | do not save | all read | [2.05] (client-internals/decomp-findings-2026-10-24-d/entry-save-rule.tsv) |

| Rule | Detail | Source |
| --- | --- | --- |
| name group | drop everything up to the last path delimiter, lower-case, then take the text up to and including the last `§` (byte 0xA7) or `$`; with neither, the group is empty, and two empty groups are equal; the extension stays | [2.05] (client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md#the-name-group-200-to-205) |
| effect | plain names such as `a.nw` and `b.nw` are always the same group; the test only separates names that use the delimiters | [2.05] (client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md#the-name-group-200-to-205) |
| no gmap | 2.05 returns -1 for both indices when there is no current gmap; 2.00 to 2.04 take the list straight from the client's state, which is inferred to give the same result | [2.05][inf] (client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md#which-builds-have-the-group-test) |
| 2.17.1, 2.22, 2.31 | no group test (step 3 absent) | [2.17.1][2.22][2.31] (client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md#which-builds-have-the-group-test) |
| end-of-respawn save | the respawn routine calls the save once more, unconditionally; in the 2.22 lab, dying again before the server's warp reply still respawned at the entry point, not the death spot | [2.05] (client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md#after-the-respawn); [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#d-end-of-respawn-save-settled-for-222-same-level-respawn) |
| gmap list order | the list's order and the timing of its update against the save are open (→ App. E#314) | [2.05] (client-internals/decomp-findings-2026-10-24-d/open-questions.tsv) |

Builds that carry the group test's delimiter set, by a constant scan, with the rule itself read only where marked:

| Builds | Delimiter constant | Source |
| --- | --- | --- |
| 1.1 to 1.36 | absent | [bin] (client-internals/decomp-findings-2026-10-24-d/name-group-constant-by-build.tsv) |
| 1.37, 1.38, 1.39, 1.41 | present | [bin] (client-internals/decomp-findings-2026-10-24-d/name-group-constant-by-build.tsv) |
| 2.00 to 2.05 rev 2, NewMain 24 and 26, NewWorld beta 1 | present (rule read in all 2.00 to 2.05 builds) | [bin] (client-internals/decomp-findings-2026-10-24-d/name-group-constant-by-build.tsv) |
| 2.1 test 2 and 3, NewWorld beta 2 | absent; their entry code not read (→ App. E#315) | [bin] (client-internals/decomp-findings-2026-10-24-d/name-group-constant-by-build.tsv) |
| 2.17.1, 2.22, 2.31 | absent; entry code read, no group test | [bin] (client-internals/decomp-findings-2026-10-24-d/name-group-constant-by-build.tsv) |
