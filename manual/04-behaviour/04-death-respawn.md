<!-- manual: kind=reference status=draft -->
# 4.4 Death clocks and respawn

This chapter gives what the client does when its hearts reach zero, the death timer, the dead bit on the wire, the respawn key, the hearts and the destination after respawn, and the level-entry save that picks the destination. What the server does on the dead bit is in → §5. Damage is in → §4.3.

> Status: draft. Read for 1st Graal, 1.39, 2.00 to 2.05 rev 2, 2.17.1, 2.22 and 2.31; timed live for 2.05 and 2.22. Open points are App. E#314 and E#315.

## 4.4.1 Life-states

The client keeps a life-state alongside its mode. Each row gives one value and what it means; the death and respawn rules below depend on it [2.05] (client-internals/decomp-findings-2026-10-24/life-states.tsv).

| Value | Life-state | Source |
| --- | --- | --- |
| 0 | playing | [2.05] (client-internals/decomp-findings-2026-10-24/life-states.tsv) |
| 1 | editor or pause | [2.05] (client-internals/decomp-findings-2026-10-24/life-states.tsv) |
| 2 | dead | [2.05] (client-internals/decomp-findings-2026-10-24/life-states.tsv); [1.39] (version-profiles/matrix/rules-139.md#death-and-respawn-bin) |
| 4 | a state in which any key restarts, with no timer test (1st Graal, 1.39); not named | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [1.39] (version-profiles/matrix/rules-139.md#death-and-respawn-bin) |

## 4.4.2 The death sequence (2.05)

Death in 2.05 runs as a short fixed sequence. The steps below are in order, from the trigger to the dead pose [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#trigger).

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

There is no automatic respawn. The rules below give the key that ends death and where the player comes back [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#respawn).

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

The hearts a player gets back depend on AP. Each row gives an AP band and the hearts restored, the same in 2.05 and 2.22 [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#respawn).

| AP | Hearts (2.05, 2.22) | Source |
| --- | --- | --- |
| below 20 | 3 | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#respawn); [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#c-curpower-semantics-settled-for-222) |
| 20 to 39 | min(5, max hearts) | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#respawn); [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#c-curpower-semantics-settled-for-222) |
| 40 or more | max hearts | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#respawn); [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#c-curpower-semantics-settled-for-222) |
| MAXPOWER 0 | 2.05 still reports CURPOWER 6 (3 hearts): the respawn hearts are not capped at a MAXPOWER of 0 | [live][2.05] (client-internals/live-trace-205.md#server-curpower-0-death-and-respawn-live-online-2026-10-29) |

### 4.4.3.2 By build

Death was read in four builds. Each row is one part of the sequence, with how each build does it, so the columns can be compared across [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin).

| Rule | 1st Graal | 1.39 | 2.05 rev 2 | 2.22 | Source |
| --- | --- | --- | --- | --- | --- |
| on death | hearts clamped to 0, counter and mode cleared, dead state; the relay object is notified; no inventory spill, no sound | hearts clamped to 0, counter 0, mode normal, dead state; `dead.wav`; the inventory partly spilled as floor items (rupees in 100/30/5/1 bands, arrows and bombs alike) | → §4.4.2 | → §4.4.2 | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [1.39] (version-profiles/matrix/rules-139.md#death-and-respawn-bin) |
| timer | death clears to 0; dead-state updater increments while below 30, then stops; sprite/key predicates remain above 27; elapsed duration not newly measured | counts 0 to 30 and stops | 0 to 30 | unmeasured | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [bin] (client-internals/first-graal-death-counter-2026-11-09.md#counter-transition); [1.39] (version-profiles/matrix/rules-139.md#death-and-respawn-bin) |
| drawing | the board replaced by a filled rectangle and a text panel; the body uses sprite 157 once the counter is above 27 | death sprites cycle between counters 4 and 27; a cleanup runs above 29 | the `dead` gani | the "End" scroll | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [1.39] (version-profiles/matrix/rules-139.md#death-and-respawn-bin) |
| dead bit 0x08 | n/a (no STATUS prop) | only while dead and the counter is above 27 | at 28 or more | sent | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [1.39] (version-profiles/matrix/rules-139.md#summary-table) |
| key | above 27 (one key index does not restart) | above 27 | above 27 | a key, after 34 s in the run | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [1.39] (version-profiles/matrix/rules-139.md#summary-table); [cap] (live-runs/2gta-222-2026-10-30/README.md#baddies-death-and-respawn-2118-to-2121) |
| destination | the new-game setup: `house1.graal` at (24.5, 30), facing 2; a second local player 12 tiles to the east | the saved entry, else (30.5, 30.0) online, else the built-in start-level table offline | → §4.4.3 | the level's entry point | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [1.39] (version-profiles/matrix/rules-139.md#death-and-respawn-bin); [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#d-end-of-respawn-save-settled-for-222-same-level-respawn) |
| hearts | 3, and the heart cap set to 3 | max hearts, no AP bands (1.39 has no AP display; the bands arrive with 1.41) | by AP | by AP | [bin] (version-profiles/matrix/rules-1st-graal.md#death-and-the-restart-bin); [1.39] (version-profiles/matrix/rules-139.md#summary-table) |

1.32 was read on its own (era B); it follows 1.39 except where the rows below say otherwise [bin] (version-profiles/matrix/rules-132.md#summary).

| Rule (1.32) | Source |
| --- | --- |
| On death: `dead.wav`, counter and mode cleared, life-state 2; up to 1000 rupees dropped in bands of 100, 30, 5 and 1; darts and bombs each capped at 95 and dropped in fives, leaving 5 darts and 10 bombs | [bin] (version-profiles/matrix/rules-132.md#hearts-damage-and-death-bin) |
| The counter rises while under 30; the facing spins between counters 4 and 27; the dead bit 0x08 only while dead and the counter is above 27; a movement or action key respawns above 27, and life-state 4 respawns with no test | [bin] (version-profiles/matrix/rules-132.md#hearts-damage-and-death-bin) |
| Damage is refused in life-state 1 and in mode 13 unless forced; healing plays no sound; a non-fatal hit plays the character's hurt sound from `sounds\` | [bin] (version-profiles/matrix/rules-132.md#hearts-damage-and-death-bin) |
| Respawn resets hearts through the shared setter (value unreadable in the export; max hearts by analogy with 1.39), clears counter, carry and action modes and the ten-slot flag array, and warps to the saved entry; with none, (30.5, 30.0) online, or offline the built-in start-level table by game mode (facing 3, 1 or 2), falling back to the options' start level | [bin][inf] (version-profiles/matrix/rules-132.md#respawn-bin) |
| Online or in game mode 0 the name shows for 60 ticks after respawn; 1.32 has no AP bar | [bin] (version-profiles/matrix/rules-132.md#respawn-bin) |
| Sword reach: tested only outside mode 3, on swing frames 6 to 10; up to 4 tiles ahead, sideways strictly under 2, ends inclusive on two facings and exclusive on the other two; power passed with the swing | [bin] (version-profiles/matrix/rules-132.md#sword-reach-bin) |
| Open: the respawn heart value, the probe numbers, the one-heart baddy type, and eras A–B outside 1.32 | [inf] (version-profiles/matrix/rules-132.md#still-open) |

## 4.4.4 The level-entry save

Run after every level entry, and at login; saving stores the new level's name, the player's x and y, and the direction as it is [2.05] (client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md#the-decision-run-after-every-level-entry).

| Step | Condition | Result | Builds | Source |
| --- | --- | --- | --- | --- |
| 1 | the level left is empty (login) | save | all read | [2.05] (client-internals/decomp-findings-2026-10-24-d/entry-save-rule.tsv) |
| 2 | index(new) × index(old) in the current gmap's level list is negative (-1 = absent; an index of 0 gives 0, so the first list entry behaves like "absent") | save | all read | [2.05] (client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md#the-decision-run-after-every-level-entry) |
| 3 | the name groups differ | save | 2.00 (all revisions) to 2.05 rev 2 | [2.05] (client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md#which-builds-have-the-group-test) |
| 4 | otherwise | do not save | all read | [2.05] (client-internals/decomp-findings-2026-10-24-d/entry-save-rule.tsv) |

The respawn point is saved on level entry, but only when the new level is a different group from the old. The rules below give how 2.05 forms that group and which builds skip the test [2.05] (client-internals/decomp-findings-2026-10-24-d/02-respawn-entry-save.md#the-name-group-200-to-205).

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

## 4.4.5 Server side (GServer-v2)

Death is client-driven; the server reacts only to the dead bit of STATUS (prop 18) changing [srv] (client-internals/feature-specs/04-death-respawn.md#what-it-is).

| Event | Server action | Source |
| --- | --- | --- |
| dies (bit 0 → 1) | outside a sparring zone, adds a death and drops random gralats between `mindeathgralats` and `maxdeathgralats` as a floor item, plus items when `dropitemsdead` is set; a dead level leader hands leadership to the next player, who gets `PLO_ISLEADER` (10) | [srv] (client-internals/feature-specs/04-death-respawn.md#exact-server-behaviour-tplayerpropscpp-status-case-srv) |
| revives (bit 1 → 0) | sets hearts by AP (under 20: 3; under 40: 5; else MAXPOWER; at least 0.5), pushes CURPOWER to the player and the level, and re-sends `ISLEADER` to a leader; it does not move the player | [srv] (client-internals/feature-specs/04-death-respawn.md#exact-server-behaviour-tplayerpropscpp-status-case-srv) |
| `PLI_CLAIMPKER` (14) | ignored for a self-kill or an unknown killer; in a sparring zone both players get a rating update (skipped when they share an IP); elsewhere the killer gets a kill and, with the AP system on, can lose AP | [srv] (client-internals/feature-specs/04-death-respawn.md#exact-server-behaviour-tplayerpropscpp-status-case-srv) |
| AP | with `apsystem` on, a per-second countdown raises AP by 1 (to 100) and reloads from `aptime0` to `aptime4` by AP band; it does not run while paused or in a sparring zone | [srv] (client-internals/feature-specs/04-death-respawn.md#exact-server-behaviour-tplayerpropscpp-status-case-srv) |
| hearts | no periodic regeneration; a client CURPOWER above the server's value is refused while AP is under 40 | [srv] (client-internals/feature-specs/04-death-respawn.md#exact-server-behaviour-tplayerpropscpp-status-case-srv) |
| idle | `disconnectifnotmoved` with `maxnomovement` disconnects an idle player with a message | [srv] (client-internals/feature-specs/04-death-respawn.md#exact-server-behaviour-tplayerpropscpp-status-case-srv) |
