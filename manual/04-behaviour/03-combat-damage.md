<!-- manual: kind=reference status=draft -->
# 4.3 Combat, damage, hurt and knockback

This chapter gives the sword swing and the spin, who judges a hit, the gates a hit must pass, the damage each source takes, the shared hurt routine, hurt mode, knockback and the hurt pose. The combat messages themselves are in → §2.4 and → §2.5.5; the STATUS bits are in → §2.6.2.1. Death is → §4.4.

> Status: draft. Read in full for 2.00 to 2.05 rev 2, 2.17.1, 2.22 and 2.31; 1st Graal and 1.39 for the main rules; 3.x to 6.x only as timed on the wire. E#309 to E#315 are settled in the chapters (→ §4.3.3, §4.3.5.2, §4.3.7.2, §4.4.4).

## 4.3.1 Who judges a hit

In Graal the victim's client, not the server, decides whether it was hit. The rules below set out that model and the units hearts are counted in [2.05] (client-internals/decomp-findings-2026-10-24/04-sword-hitbox.md#who-decides-a-hit).

| Rule | Detail | Source |
| --- | --- | --- |
| the victim decides | the victim's own client judges another player's swing from that player's props (position, direction, sprite) and applies the damage; the attacker only broadcasts its props | [2.05] (client-internals/decomp-findings-2026-10-24/04-sword-hitbox.md#who-decides-a-hit); [2.00] (client-internals/combat-200-204.md#the-same-in-every-build-200-to-205-rev-2) |
| bombs and arrows | the victim's client also judges a server-sent bomb (`PLO_BOMBADD`, 11), explosion (36) or shot (`PLO_ARROWADD`, 19), whoever owns it; no hit message is sent, only the victim's props message (CURPOWER and the `hurt` gani) and the knockback positions; a client's own bomb hurts its owner | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#b-bombs-arrows-baddies-who-owns-the-damage-part-2-fresh-runs); [2.05] (client-internals/damage-sources.md#other-players-bombs-blasts-and-shots) |
| hearts on the wire | the victim reports its own hearts: in the hit's tick one props message with CURPOWER, the `hurt` gani and one more prop; nothing from the server asks for it, and the server's own CURPOWER is not echoed | [cap][2.05] (client-internals/live-trace-205.md#hearts-are-reported-by-the-client); [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#c-curpower-semantics-settled-for-222) |
| units | CURPOWER is in half-hearts, MAXPOWER in hearts; the client clamps CURPOWER to MAXPOWER × 2 before subtracting | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#c-curpower-semantics-settled-for-222) |
| killer report | when a hit by another player's sword, piece or shot, or a UDP hurt, leaves the hearts at 0 or below, the victim sends `PLI_CLAIMPKER` (14) with the attacker's id (→ §2.4) | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#damage-rules-that-feed-this); [2.05] (client-internals/damage-sources.md#who-can-hurt-whom) |
| integrity | hearts, AP and the heart cap are stored obfuscated twice and cross-checked; a mismatch raises a "memory problems" error (→ §4.10) | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#anti-cheat-note) |

## 4.3.2 The sword swing

The sword swing is a mode with its own gani and timing. The rules below give when it can start, where the tip probe lies, and how long it lasts [2.05] (client-internals/decomp-findings-2026-10-24/04-sword-hitbox.md#starting-a-swing).

| Rule | Detail | Source |
| --- | --- | --- |
| preconditions | weapons allowed by the level or server, sword power not 0, not swimming without a horse, not already in the spin mode | [2.05] (client-internals/decomp-findings-2026-10-24/04-sword-hitbox.md#starting-a-swing) |
| mode and gani | mode 6; plays `sword` (`ridesword` on a horse) and the sword sound, then checks for a cuttable bush at the sword tip | [2.05] (client-internals/decomp-findings-2026-10-24/04-sword-hitbox.md#starting-a-swing); [2.05] (client-internals/water-and-ganis.md#built-in-animations) |
| tip probe | one tile beyond the middle of the leading edge: up (x + 1.5, y), left (x - 0.5, y + 2), down (x + 1.5, y + 4), right (x + 3.5, y + 2) | [2.05] (client-internals/decomp-findings-2026-10-25-l/01-walking-body-box.md#other-probes-same-routine-family) |
| timing | `sword` in the next tick, 5 frames of one tick, then `idle`; the bush is cut on the first swing frame; the player does not move while it plays, even with an arrow held; walking resumes the tick after, from walk frame 0 | [live][2.05] (client-internals/player-mannerisms-live.md#sword-live) |
| repeat | holding S does not swing again; each swing needs a new press; holding S gives no charge | [live][2.05] (client-internals/player-mannerisms-live.md#sword-live) |
| on the wire | the swing's sprite steps are 9 to 13 (SPRITE 6 to 10) | [2.05] (client-internals/decomp-findings-2026-10-24/04-sword-hitbox.md#starting-a-swing) |
| no sword | a player with sword power 0 started from the editor still plays `sword` and its sound, but no blade is drawn and nothing is cut | [live][2.05] (client-internals/player-mannerisms-live.md#sword-live) |
| carrying | the sword key with an object carried throws it instead (the same throw as the action key, → §4.5); no swing precondition is checked on that path | [2.05] (client-internals/decomp-findings-2026-10-28/01-sword-while-carrying.md); [live][2.22] (client-internals/player-mannerisms-live.md#notes-per-build) |
| `hidesword n` | sets a counter of `n` seconds (clamped 0 to 30, × 20 ticks) that counts down each tick; while it is 0 or more STATUS carries bit 0x20; it does not stop the local swing, only refuses the hit at the victim's end | [2.05] (client-internals/status-bit-0x20.md) |
| `hideplayer n` | the same clamp and scale on its own counter, which drives STATUS bit 0x02 (hidden) | [2.05] (client-internals/status-bit-0x20.md#how-the-bit-is-set) |

By build:

| Build | Swing | Cut | Source |
| --- | --- | --- | --- |
| 1st Graal | hit frames 6 to 10 | unmeasured | [bin] (version-profiles/matrix/rules-1st-graal.md#sword-reach-bin) |
| 1.39 | counter 1 to 6 (5 ticks), no gani | cuts the bush | [live][1.39] (client-internals/player-mannerisms-live.md#cross-version-table) |
| 1.41 | `sword` 5 ticks | on the first frame | [live][1.41] (client-internals/player-mannerisms-live.md#cross-version-table) |
| 2.05 rev 2 | `sword` 5 × 1 tick | on the first frame | [live][2.05] (client-internals/player-mannerisms-live.md#sword-live) |
| 2.22 | `sword` | the 2 × 2 leaves board change goes to the server in the same frame as the sword gani; idle follows 240 ms later | [cap] (live-runs/2gta-222-2026-10-30/README.md#what-the-client-sends-while-walking-and-cutting) |
| 5.24r4, 5.30r3, 6.03r7 | `sword` 5 ticks, `idle` 0.25 s later | the cut (board change) in the same tick as the swing starts | [wire] (protocol/v5v6-lab-play.md) |

### 4.3.2.1 The spin attack

A second press during a swing turns it into a spin. The rules below give the timing window, the length of the spin, and what it ignores [live][2.05] (client-internals/player-mannerisms-live.md#spin-attack-live-online).

| Rule | Detail | Source |
| --- | --- | --- |
| start | a second S press while `sword` is still playing, with the has-spin status (STATUS bit 0x40); not a hold-to-charge | [live][2.05] (client-internals/player-mannerisms-live.md#spin-attack-live-online); [2.05] (client-internals/feature-specs/02-weapons-combat.md#205-sword-swing-and-hit-box-205dec) |
| new press | S must be up for at least one tick in between; a press on swing frame 2, 3 or 4 works; a press after the swing has ended starts a normal swing | [live][2.05] (client-internals/player-mannerisms-live.md#spin-attack-live-online) |
| timing | the swing is cut off: `spin` frame 0 shows in the tick after the second press; 13 frames of one tick (650 ms), then `idle`; the facing at the start is stored | [live][2.05] (client-internals/player-mannerisms-live.md#spin-attack-live-online) |
| mode | mode 13; a press during the spin is ignored and queues nothing | [live][2.05] (client-internals/player-mannerisms-live.md#spin-attack-live-online); [2.05] (client-internals/decomp-findings-2026-10-24/player-modes.tsv) |
| wire | the client sends `GANI=spin` once at the start and `GANI=idle` at the end, and asks for `spin.gani` the first time | [live][2.05] (client-internals/player-mannerisms-live.md#spin-attack-live-online) |
| 2.22 | the same: a second press on frame 3 cut the swing off, `spin` ran 13 × 1 tick, a third press was ignored | [live][2.22] (client-internals/player-mannerisms-live.md#spin-attack-live-online) |
| 1.39, 1.41 | no spin: 1.39 given STATUS bit 0x20 never spun from a second S press (0/6); 1.41r1 given bits 0x20 and 0x40 never spun from a second press or a hold (0/9) | [lab][1.39][1.41r1] (live-runs/client-harness-2026-11-13/README.md#findings) |
| 2.22, 2.31 input | double-tap S spins (3/3 each) and so does tap-then-hold S (3/3 each); holding S alone does not (0/3 on 2.22, 1/3 on 2.31) | [lab][2.22][2.31] (live-runs/client-harness-2026-11-13/README.md#findings) |
| what it hits | which bushes the spin cuts and whether it hits players or NPCs: unmeasured | [live] (client-internals/player-mannerisms-live.md#spin-attack-live-online) |

## 4.3.3 The sword hit test (victim's side)

A swing hits the local player only when every gate passes. In 2.05 rev 2 order:

| # | Gate | Source |
| --- | --- | --- |
| 1 | the attacker's player id is known | [2.05][2.22] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#gates-shared-by-the-sword-and-the-packets) |
| 2 | the attacker is on sprite steps 9 to 13 (SPRITE 6 to 10) | [2.05] (client-internals/decomp-findings-2026-10-24-d/hit-gates.tsv) |
| 3 | the victim can be hurt: not in hurt mode, not dead, not swimming, hearts above 0, and normal play or a sparring-zone level | [2.05] (client-internals/decomp-findings-2026-10-24-d/03-hit-gates-and-open-points.md#level-flags-seen) |
| 4 | the victim's AP is not exactly 100 | [2.05] (client-internals/decomp-findings-2026-10-24-d/hit-gates.tsv) |
| 5 | the level has not run `noplayerkilling`; when the local player's own attack is refused by it, the client prints `nopkzone` | [2.05] (client-internals/decomp-findings-2026-10-24-d/03-hit-gates-and-open-points.md#gates) |
| 6 | the attacker has not already been judged in this second of the day (a per-attacker stamp, stored before the guild test); on 2.05 rev 2 this gate is on the hurt-message path only: the sword judge neither checks nor stores the stamp (→ §4.3.3) | [2.05][2.22] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#gates-shared-by-the-sword-and-the-packets); [lab] (protocol/lab-appe-hostb-2026-11-20.md#once-per-second-hit-stamp-on-205-e310) |
| 7 | guild: the first bracketed text in the attacker's nickname (a `(`, then the first `)` after it with at least one character between) does not occur anywhere in the victim's nickname, case-sensitive | [2.05] (client-internals/decomp-findings-2026-10-24-d/03-hit-gates-and-open-points.md#gates) |
| 8 | the attacker's STATUS has neither 0x02 (hidden) nor 0x20 (sword hidden) | [2.05] (client-internals/decomp-findings-2026-10-24-d/03-hit-gates-and-open-points.md#gates) |
| 9 | the attacker is not kicking: 2.05 by the animation name `kick`, 2.17.1 and later by an object id of 3 | [2.05][2.17.1] (client-internals/decomp-findings-2026-10-24-d/hit-gates.tsv) |
| 10 | reach box: the victim's centre 0 to 4 tiles ahead of the attacker's centre along its facing (both ends count) and at most 2 tiles to the side, the 2-tile edge included (every build 1.21 to 2.31; earlier readings said strictly under 2) [bin] (client-internals/combat-baddy-tile-by-version.md#the-sword-box-the-victim-judging-another-players-swing); two live 1.35 clients confirm the edge: a victim 2 tiles to either side is hit, 2.5 tiles is missed [lab] (live-runs/sword-edge-2026-11-18/README.md#result); centres are (x + 1.5, y + 2); skipped while the victim is in hurt mode | [2.05] (client-internals/decomp-findings-2026-10-24/04-sword-hitbox.md#who-decides-a-hit); [2.00] (client-internals/combat-200-204.md#the-same-in-every-build-200-to-205-rev-2) |

**Settled question, formerly E#310: Where the once-per-second hit stamp sits.** Which hit paths share the per-attacker once-per-second stamp was open between two reads; a two-client lab on 2.05 settled it [lab] (protocol/lab-appe-hostb-2026-11-20.md#once-per-second-hit-stamp-on-205-e310).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: the sword and both hit messages share the stamp, stored before the guild test. B: in 2.00 to 2.05 rev 2 the stamp is on the hurt-message path only | [2.05][2.22] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#gates-shared-by-the-sword-and-the-packets); [2.00][2.05] (client-internals/combat-200-204.md#what-changes-by-build) |
| Settled | On 2.05 rev 2 a guild-rejected hurt message blocks a clean one from the same attacker in the same second, so that path stores the stamp before the guild test; a real swing is not blocked by that stamp and stores none of its own | [lab] (protocol/lab-appe-hostb-2026-11-20.md#once-per-second-hit-stamp-on-205-e310) |
| Verdict | Verified on 2.05 rev 2: Claim B holds | [lab] (protocol/lab-appe-hostb-2026-11-20.md#once-per-second-hit-stamp-on-205-e310) |
| Left over | 2.22, which Claim A also covers | [lab] (protocol/lab-appe-hostb-2026-11-20.md#once-per-second-hit-stamp-on-205-e310) |

By build:

| Rule | 1st Graal | 1.39 | 2.00 | 2.01 | 2.02 | 2.03 | 2.04 = 2.05 rev 2; 2.17.1, 2.22, 2.31 | Source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| reach box | up to 4 ahead, sideways under 2; the 0 and 4 edges unread | 0 to 4 ahead, sideways up to 2 inclusive | 0 to 4, both ends; sideways up to 2 inclusive | = | = | = | = | [bin] (version-profiles/matrix/rules-1st-graal.md#sword-reach-bin); [1.39] (version-profiles/matrix/rules-139.md#sword-reach-bin-lab); [2.00] (client-internals/combat-200-204.md#the-same-in-every-build-200-to-205-rev-2) |
| tested only in | the normal life-state | unmeasured | play state exactly 0 (its own victim test; no paused/editor test) | the shared can-be-hurt test | shared | shared | shared | [bin] (version-profiles/matrix/rules-1st-graal.md#sword-reach-bin); [2.00][2.01] (client-internals/combat-200-204.md#what-changes-by-build) |
| kick test | unmeasured | unmeasured | absent | by animation name | = | = | by name (2.05); object id 3 (2.17.1 on) | [2.00][2.01] (client-internals/combat-200-204.md#what-changes-by-build); [2.17.1] (client-internals/decomp-findings-2026-10-24-d/hit-gates.tsv) |
| no-kill flag | unmeasured | unmeasured | on the player, cleared on level load | on the player | on the player | on the player | on the level, read through a tamper-checked byte | [2.00][2.03][2.04] (client-internals/combat-200-204.md#what-changes-by-build) |
| `playerhurt` event on a hit | n/a | unmeasured | absent | present | present | present | present | [2.00][2.01] (client-internals/combat-200-204.md#what-changes-by-build) |
| props path: per-player link field equal | n/a | unmeasured | no | no | no | no | yes (→ §4.3.6) | [2.00][2.04] (client-internals/combat-200-204.md#what-changes-by-build) |

## 4.3.4 Sword damage

Sword damage comes from one prop. The rules below give the formula, how the prop is encoded and what the formula leaves out [2.05][2.17.1][2.22][2.31] (client-internals/decomp-findings-2026-10-24-d/01-sword-damage.md#the-formula).

| Rule | Detail | Source |
| --- | --- | --- |
| formula | half-hearts taken = the attacker's sword power as the victim last received it in SWORDPOWER (prop 8), limited to -20 to 20; a power-3 sword takes 1.5 hearts | [2.05][2.17.1][2.22][2.31] (client-internals/decomp-findings-2026-10-24-d/01-sword-damage.md#the-formula) |
| prop 8 on the wire | power 0 sends byte 0 (no image); power 1 to 4 with the matching default image (`sword1` to `sword4`) sends the power itself; anything else sends power + 30 (10 to 50) followed by the image name; the receiver reads a byte below 10 as the power and otherwise byte - 30 (→ §2.6) | [2.05] (client-internals/decomp-findings-2026-10-24-d/01-sword-damage.md#the-sword-power-byte-prop-8) |
| negative power | heals, but only at AP 40 or more; hearts stop at the maximum | [2.05] (client-internals/decomp-findings-2026-10-24-d/01-sword-damage.md#what-happens-to-the-hearts) |
| not in the formula | the victim's shield power, item levels and the attacker's AP were not read into it | [2.05] (client-internals/decomp-findings-2026-10-24-d/damage-rules.tsv) |

The damage store changed twice. Each row gives a group of builds, how they store the received power and what a negative power does [bin] (version-profiles/matrix/rules-1st-graal.md#sword-reach-bin).

| Build | Sword power store | Negative power | Source |
| --- | --- | --- | --- |
| 1st Graal | fixed half a heart; the sword does not grow | n/a | [bin] (version-profiles/matrix/rules-1st-graal.md#sword-reach-bin) |
| 2.00, 2.01, 2.02 | the received power as is, in a 6-bit slot (0 to 63) | cannot occur: it wraps in the store (inferred from the mask) | [2.00][2.01][2.02][inf] (client-internals/combat-200-204.md#what-changes-by-build) |
| 2.03 to 2.31 | power + 20, limited to -20 to 20 | heals at AP 40 or more | [2.03] (client-internals/combat-200-204.md#what-changes-by-build); [2.05] (client-internals/decomp-findings-2026-10-24-d/01-sword-damage.md) |

## 4.3.5 Other damage sources (2.05)

Every source calls the same hurt routine (→ §4.3.7) with a power in hearts and a knockback direction.

| Source | Hearts | Hit test | Source |
| --- | --- | --- | --- |
| explosion piece, type 1 (`putbomb 1`, `putexplosion`, the blast of a fireblast or nuke) | 0.5 | the piece's centre, offset by one tile, less than one tile from the player's centre (x + 1.5, y + 2) on both axes; the 2.22 lab pattern follows the 2-tile piece spacing (settled below) | [2.05] (client-internals/damage-sources.md#bombs-and-explosions) |
| explosion piece, type 2 (`putbomb 2`, the super bomb) | 0.5 | as type 1 | [2.05] (client-internals/damage-sources.md#powers) |
| explosion piece, type 3 (`putbomb 3`, the jolt bomb) | 1 | as type 1 | [2.05] (client-internals/damage-sources.md#powers) |
| arrow (`shootarrow`) | 0.5 | the shot box against the player's box (→ §4.3.5.2) | [2.05] (client-internals/damage-sources.md#powers) |
| fireball (`shootfireball`) | 1 | as an arrow | [2.05] (client-internals/damage-sources.md#powers) |
| fireblast (`shootfireblast`) | 0.5, then a blast of reach 2, type 1 | as an arrow | [2.05] (client-internals/damage-sources.md#projectiles) |
| nuke (`shootnuke`) | 1, then a blast of reach 2, type 1 | as an arrow | [2.05] (client-internals/damage-sources.md#projectiles) |
| thrown object (`waspelt`) | 1, or 0.5 when the player has exactly 1 heart | lands within 2 tiles of (x + 0.5, y + 1) on both axes | [2.05] (client-internals/damage-sources.md#thrown-objects) |
| baddy touch | 0.5, or 1 for the golden warrior (type 7) | the player's centre within one tile of the baddy's point on both axes; the baddy may say its "hurts the player" verse | [2.05] (client-internals/damage-sources.md#baddies) |
| lava | 0.5 every 101 ticks (→ §4.2.10.1) | the point (x + 1.5, y + 2) on lava | [live][2.05] (client-internals/live-trace-205.md#water-and-lava-live-new4nw) |
| `PLO_HURTPLAYER` (40) | its power byte - 32 in half-hearts, capped at one heart; 0 gives hurt mode and knockback with no hearts | → §4.3.6 | [2.05] (client-internals/decomp-findings-2026-10-24-d/01-sword-damage.md#the-hurt-packet-id-40-and-its-power); [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#b-packet-40-hurt-player-real-client-as-victim-settled-for-the-cases-below) |

**Settled question, formerly E#311: Blast hit zone and the occasional full-heart hit.** Why the blast zone read from code did not seem to match the hits measured on 2.22, and why some trials took a full heart, was open. A read of the 2.22 explosion routine settled it [bin] (client-internals/static-reads-appendix-e-2026-11-20-d.md#explosions-on-222-e311).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | An explosion is a centre piece and four arms, with a piece every 2 tiles out to twice the power; each piece hurts under the strict "less than 1 tile" windows of Claim A, so hits fall on the rows and columns the 2-tile spacing reaches | [bin] (client-internals/static-reads-appendix-e-2026-11-20-d.md#explosions-on-222-e311) |
| Settled | A full heart comes from an explosion made with kind 3 (on 2.05 the jolt bomb, `putbomb 3`), not from two pieces overlapping; shots make kind 1 | [bin] (client-internals/static-reads-appendix-e-2026-11-20-d.md#explosions-on-222-e311); [2.05] (client-internals/damage-sources.md#powers) |
| Verdict | Verified by read on 2.22: Claim A holds for each piece and explains Claim B's pattern; the best guess about overlap is refuted | [bin] (client-internals/static-reads-appendix-e-2026-11-20-d.md#explosions-on-222-e311) |
| Left over | Which bomb sources make kind 3 on 2.22, whether a second piece in the same tick can add damage, and the one-bomb-per-trial sweep | [bin] (client-internals/static-reads-appendix-e-2026-11-20-d.md#explosions-on-222-e311) |

Swords are not the only source of damage. The rules below cover ownership, overlapping hits, and baddy touch damage [2.05] (client-internals/damage-sources.md#who-can-hurt-whom).

| Rule | Detail | Source |
| --- | --- | --- |
| ownership | a bomb, blast, arrow or thrown object can belong to another player; online, a piece counts as a player's when it has an owner still in the player list; a player's source does not hurt in a level that ran `noplayerkilling`; a source with no owner (a baddy's, the level's, or one whose owner has left) always hurts | [2.05] (client-internals/damage-sources.md#who-can-hurt-whom); [2.05] (client-internals/damage-sources.md#when-a-piece-hurts-the-local-player) |
| one blast, one hit | overlapping pieces take hearts once, because the second finds the player in hurt mode | [2.05] (client-internals/damage-sources.md) |
| 1.39 baddy touch | 0.5 hearts (1 for type 7), within 1 tile on both axes of the baddy centre | [1.39] (version-profiles/matrix/rules-139.md#summary-table) |
| 1.32 baddy touch | within 1 tile on both axes, baddy centre (x+1, y+1) to player centre (x+1.5, y+2); 0.5 hearts, 1 for one type not mapped to 1.39's numbering; one standing pose heals and one tile condition hurts (forced) half a heart every 100 ticks | [bin] (version-profiles/matrix/rules-132.md#baddy-touch-bin) |
| 2.22 baddies | touch as above, judged by each client for its own player only, with the 2 s hurt lock-out spacing the hits; a player's sword hits a baddy inside a box that depends on the player's facing, and types 0, 1, 2 and 7 block with a shield when they face the swing (knockback 0.8 instead of 2.0); online, a client that is not the leader reports its hit with `PLI_BADDYHURT` (16) | [2.22][cap] (client-internals/baddies-222.md#damage) |
| 1st Graal | sword and baddy touch half a heart; baddy centre (x + 1, y + 1); two projectile types (sprites 65 and 261) half a heart, the others one heart; an arrow (sprites 107 to 110) flying opposite the player's facing, with the player's sprite index below 6, is blocked | [bin] (version-profiles/matrix/rules-1st-graal.md#hurt-and-knockback-bin) |

### 4.3.5.1 Bombs and blasts

Bombs and blasts are built from one command and a cross-shaped blast. The rules below give the powers, the shape and the explosion command [2.05][inf] (client-internals/damage-sources.md#bombs-and-explosions).

| Rule | Detail | Source |
| --- | --- | --- |
| `putbomb power,x,y` | powers 1 to 3 are the bomb, super bomb and jolt bomb of the built-in weapons (inferred from the weapon scripts); a local fuse is 60 ticks; water under (x + 1, y + 1) makes a splash and no bomb | [2.05][inf] (client-internals/damage-sources.md#bombs-and-explosions); [2.05] (client-internals/damage-sources.md#bomb-11) |
| going off | power 3 plays `thunder.wav`, any other `bomb.wav`; power 2 makes five type-2 blasts (four of reach 2 at the diagonal corners 2 tiles out, one of reach 4 in the middle); any other power one blast of reach 2 with the bomb's power as its type | [2.05] (client-internals/damage-sources.md#bombs-and-explosions) |
| blast shape | a cross: a centre piece and `n` pieces in each direction (`n` at most 15); the last piece of an arm uses the end picture; each piece lives 11 ticks and may hit on any of them | [2.05] (client-internals/damage-sources.md#bombs-and-explosions); [2.05] (client-internals/damage-sources.md#when-a-piece-hurts-the-local-player) |
| `putexplosion radius,x,y` | one blast of type 1 with that reach | [2.05] (client-internals/damage-sources.md#bombs-and-explosions) |
| knockback | along the piece's arm | [2.05] (client-internals/damage-sources.md#when-a-piece-hurts-the-local-player) |
| another player's bomb (11) | at least 4 bytes; power `v & 7`, bit 8 marks it as the sender's; the fuse byte is in ticks (the sender's copy is 5 ticks shorter than a local `putbomb`); put in the sender's level; nothing is sent back | [2.05] (client-internals/damage-sources.md#bomb-11) |
| another player's explosion (36) | at least 4 bytes; power `v & 7`, 0 read as 1 and above 3 read as 3; one cross, never the super-bomb split; one of two sounds by whether the power is 3 (that they are `thunder.wav` and `bomb.wav` is inferred) | [2.05][inf] (client-internals/damage-sources.md#explosion-36) |

### 4.3.5.2 Shots

Shots fly one tile per tick. The rules below cover local and remote shots, their flight and their hit box [2.05] (client-internals/damage-sources.md#projectiles).

| Rule | Detail | Source |
| --- | --- | --- |
| local shots | the four shoot commands make a flying object of type 0 (arrow), 1 (fireball), 2 (fireblast) or 3 (nuke) at speed 1 and play `arrow.wav` | [2.05] (client-internals/damage-sources.md#projectiles) |
| another player's shot (19) | at least 5 bytes: `x×2`, `y×2`, flags, sprite, type (`byte - 33`); flags `& 3` direction, 4 first removes a matching shot already held, 8 marks it as the sender's; arrows use sprites 107 + direction | [2.05] (client-internals/damage-sources.md#shot-19) |
| flight | 1 tile per tick; past -2 or at 64 and beyond it moves to the neighbouring level of the loaded gmap block, or is gone | [2.05] (client-internals/damage-sources.md#when-a-shot-hurts-the-local-player) |
| hit box | size from the sprite table entry `v` (array 24): width `((v >> 6) & 63) / 16`, height `(v & 63) / 16`; hits when `x + w > px + 0.5`, `x < px + 2.5`, `y + h > py + 1`, `y < py + 3` | [2.05] (client-internals/damage-sources.md#when-a-shot-hurts-the-local-player) |
| skipped | while the shot bounces back, for a player's shot (one's own, or one received in a `noplayerkilling` level), or when the player cannot be hurt | [2.05] (client-internals/damage-sources.md#when-a-shot-hurts-the-local-player) |
| shield | the player faces the shot, shield power above 0, the shot is type 0 or 1, and the animation is one of two built-in names (inferred `idle` and `walk`); power 1: an arrow turns back for 3 ticks with a sound, any other sprite is gone; power 2 or more: the shot is sent back the other way and re-sent as a new shot | [2.05][inf] (client-internals/damage-sources.md#when-a-shot-hurts-the-local-player) |
| walls | arrows (type 0) and fireballs (type 1) pass walls; types 2 to 4 burst on them, measured on 2.05 rev 2 (→ §4.3.5.2) | [2.05] (client-internals/damage-sources.md#open); [lab] (protocol/lab-appe-hosta-2026-11-20.md#arrows-and-fireballs-at-a-wall-on-205-e313) |
| lab | an injected shot hurt only when its last byte was `0x23` or more; the byte is the shot type, and low types do hurt (settled below) | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#b-bombs-arrows-baddies-who-owns-the-damage-part-2-fresh-runs) |

**Settled question, formerly E#312: The last byte of a shot.** What the last byte of `PLO_ARROWADD` (19) does was open, because an earlier 2.22 lab saw only bytes 35 and up hurt. A read of the 2.22 receiver and a lab sweep settled it [bin] (client-internals/static-reads-appendix-e-2026-11-20-d.md#the-shot-message-on-222-e312); [lab] (protocol/lab-appe-hostb-2026-11-20d.md#shot-types-0-and-1-on-222-e312).

| Part | Discussion | Source |
| --- | --- | --- |
| Settled | The last byte less 33 is the shot type. On 2.22, types 0 and 1 hurt a receiving client directly, half a heart and one heart, linked to an owner or not; type 2 hurts half a heart. A `noplayerkilling` level stops every shot | [bin] (client-internals/static-reads-appendix-e-2026-11-20-d.md#the-shot-message-on-222-e312); [lab] (protocol/lab-appe-hostb-2026-11-20d.md#shot-types-0-and-1-on-222-e312) |
| Verdict | Verified on 2.22: Claim A holds. Claim B's no-hit results came from the setup (placement, level flags or the owner field), not from the byte | [lab] (protocol/lab-appe-hostb-2026-11-20d.md#shot-types-0-and-1-on-222-e312) |
| Left over | Which owner field the client compares, and why the 2026-10-25 and 2026-11-20 lab host A sweeps saw no hits | [bin] (client-internals/static-reads-appendix-e-2026-11-20-d.md#the-shot-message-on-222-e312) |

**Settled question, formerly E#313: Do arrows and fireballs pass walls.** Whether arrows and fireballs fly through walls in 2.05 was open from a code read; a lab shot at a wall settled it [lab] (protocol/lab-appe-hosta-2026-11-20.md#arrows-and-fireballs-at-a-wall-on-205-e313).

| Part | Discussion | Source |
| --- | --- | --- |
| Before | In the 2.05 shot flow, types 0 and 1 skip the blocking test that stops types 2 and 3 | [2.05] (client-internals/damage-sources.md#open) |
| Settled | On 2.05 rev 2 an arrow (type 0) and a fireball (type 1) cross a wall row and keep going; types 2 to 4 burst on the wall | [lab] (protocol/lab-appe-hosta-2026-11-20.md#arrows-and-fireballs-at-a-wall-on-205-e313) |
| Verdict | Verified: the code read holds | [lab] (protocol/lab-appe-hosta-2026-11-20.md#arrows-and-fireballs-at-a-wall-on-205-e313) |

## 4.3.6 Hits by message

Two server messages deliver hits. The table compares them rule by rule: their payload, the gates they pass and the range they use [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#bc-addendum-fresh-runs-2310-2330-jst-packet-40-distance-gate).

| Rule | `PLO_HURTPLAYER` (40) | `PLO_HITOBJECTS` (46) | Source |
| --- | --- | --- | --- |
| payload | attacker id, dx, dy, power; an optional trailing GINT3 NPC id | power, then the hit point's two bytes (half-tiles) | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#bc-addendum-fresh-runs-2310-2330-jst-packet-40-distance-gate); [2.05][2.22] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#packet-46-box) |
| gates 1 to 6 of §4.3.3 | yes, without the attacker status test | yes | [2.05][2.22] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#gates-shared-by-the-sword-and-the-packets) |
| link field | the attacker's layer/parent link integer equals the victim's (new players start at 0; a horse does not change it) | as 40 | [2.22] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#the-per-player-field-of-packet-40); [2.05][2.22] (client-internals/decomp-findings-2026-10-25-e/04-name-index-case-link.md#packet-40-link) |
| range | squared distance between the two X/Y positions at most 100 (lab: hits at 100.0, none at 110.25) | the player's centre (x + 1.5, y + 2) strictly under 2 tiles from the hit point on each axis | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#bc-addendum-fresh-runs-2310-2330-jst-packet-40-distance-gate); [2.05][2.22] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#packet-46-box) |
| power | `byte - 32` half-hearts, capped at 2 | capped at one heart | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#b-packet-40-hurt-player-real-client-as-victim-settled-for-the-cases-below) |
| knockback | `(byte - 0x60) / 16` per axis, normalised to the 5-tile push; a zero vector goes 5 tiles east | the victim's centre minus the hit point | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#bc-addendum-fresh-runs-2310-2330-jst-packet-40-distance-gate); [2.05][2.22] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#knockback-of-a-hit) |
| NPC id present | the hit is refused completely (no damage, no knockback); with only 2 trailing bytes it still hits | unmeasured | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#bc-addendum-fresh-runs-2310-2330-jst-packet-40-distance-gate) |
| unknown attacker | refused | refused | [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#b-packet-40-hurt-player-real-client-as-victim-settled-for-the-cases-below) |

Many of the hit gates arrived in 2.01. Each row gives one gate and whether each group of builds has it [2.00][2.01] (client-internals/combat-200-204.md#what-changes-by-build).

| Gate | 2.00 | 2.01, 2.02, 2.03 | 2.04 = 2.05 rev 2 | Source |
| --- | --- | --- | --- | --- |
| id 46 handled | no | yes | yes | [2.00][2.01] (client-internals/combat-200-204.md#what-changes-by-build) |
| AP 100 immune | no | yes | yes | [2.00][2.01] (client-internals/combat-200-204.md#what-changes-by-build) |
| no-kill flag | no | yes | yes | [2.00][2.01] (client-internals/combat-200-204.md#what-changes-by-build) |
| once per attacker per second | no | yes | yes | [2.00][2.01] (client-internals/combat-200-204.md#what-changes-by-build) |
| guild test | yes | yes | yes | [2.00][2.01] (client-internals/combat-200-204.md#what-changes-by-build) |
| link field equal | no | no | yes | [2.00][2.04] (client-internals/combat-200-204.md#what-changes-by-build) |
| range and power cap | 10 tiles, one heart | = | = | [2.00] (client-internals/combat-200-204.md#the-same-in-every-build-200-to-205-rev-2) |

## 4.3.7 The hurt routine and hurt mode

Every accepted hit goes through one hurt routine. The rules below give its input, when it refuses, what happens to hearts and the mode it sets [2.05] (client-internals/decomp-findings-2026-10-24-d/01-sword-damage.md#what-happens-to-the-hearts).

| Rule | Detail | Source |
| --- | --- | --- |
| input | a power in hearts and a knockback vector | [2.05] (client-internals/decomp-findings-2026-10-24-d/01-sword-damage.md#what-happens-to-the-hearts) |
| refused | while the player cannot be hurt: in hurt mode (3), swimming (10), dead, or in the editor or paused outside a sparring zone; lava's call skips these checks | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#damage-rules-that-feed-this); [2.05][inf] (client-internals/decomp-findings-2026-10-28-b/01-tile-type-tests.md#the-default-tileset) |
| hearts | the heart change is minus the power; a heal (negative power) applies only at AP 40 or more; hearts at 0 or below start the death (→ §4.4) | [2.05] (client-internals/decomp-findings-2026-10-24-d/01-sword-damage.md#what-happens-to-the-hearts) |
| mode | hurt mode (3) with the counter at 40, for every accepted hit, including power 0 and an ignored heal | [2.05][2.17.1][2.22][2.31] (client-internals/decomp-findings-2026-10-24-d/damage-rules.tsv) |
| event | the script event `playerhurt` fires | [2.05] (client-internals/decomp-findings-2026-10-24/01-death-respawn.md#damage-rules-that-feed-this) |
| countdown | each tick the counter drops by one; at 0 the mode returns to normal; no new hit for the whole 40 ticks (2 s) | [2.05] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#knockback-of-a-hit); [live][2.05] (client-internals/player-mannerisms-live.md#hurt-knockback-and-blinking-live) |
| arrows during hurt | held arrows are ignored while the counter is above 29; from the 12th tick after the hit (counter 28) a held arrow walks again and `walk` replaces `hurt` | [live][2.05] (client-internals/player-mannerisms-live.md#hurt-knockback-and-blinking-live) |
| carrying | 1.39: a positive-power hit may force a drop of the carried object; 1st Graal: the carry is dropped | [1.39] (version-profiles/matrix/rules-139.md#hurt-and-knockback-bin); [bin] (version-profiles/matrix/rules-1st-graal.md#hurt-and-knockback-bin) |

### 4.3.7.1 Knockback

A hit pushes the player back. The rules below give the vector, the steps and what happens when the way is blocked [2.05][2.17.1][2.22][2.31] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#knockback-of-a-hit).

| Rule | Detail | Source |
| --- | --- | --- |
| vector | stored scaled to one tile; a zero vector becomes one tile east | [2.05][2.17.1][2.22][2.31] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#knockback-of-a-hit) |
| steps | while the counter reads 39 down to 35 after its decrement, the player moves one tile per tick along the vector: five tiles in 250 ms on open ground | [2.05][2.17.1][2.22][2.31] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#knockback-of-a-hit) |
| blocked | after each step twelve body-box points are tested with the walking rules (→ §4.2.3); if any is blocked the step is undone and tried again the next tick | [2.05][2.17.1][2.22][2.31] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#knockback-of-a-hit) |
| inside a blocking NPC | every step is refused and the player does not move | [live][2.05] (client-internals/player-mannerisms-live.md#hurt-knockback-and-blinking-live) |
| sword direction | the victim's centre minus the attacker's point (halved before normalising, where 2.00 and 2.02 keep it) | [2.05] (client-internals/decomp-findings-2026-10-25-k/01-knockback-and-packet-hits.md#knockback-of-a-hit); [2.00][2.02] (client-internals/combat-200-204.md#the-same-in-every-build-200-to-205-rev-2) |
| live | a touch NPC moved the player from (29.5, 48) to (28.79, 52.95), 5.0 tiles, along the line from the NPC image centre to the player's centre | [live][2.05] (client-internals/player-mannerisms-live.md#hurt-knockback-and-blinking-live) |

The twelve points, offsets from (x, y), three per edge of a box 0.6 to 2.4 across and 1.1 to 2.9 down, centred on (x + 1.5, y + 2):

| Point | x offset | y offset | Source |
| --- | --- | --- | --- |
| 1 | 0.6 | 1.1 | [2.05] (client-internals/decomp-findings-2026-10-25-k/knockback-probes.tsv) |
| 2 | 1.5 | 1.1 | [2.05] (client-internals/decomp-findings-2026-10-25-k/knockback-probes.tsv) |
| 3 | 2.4 | 1.1 | [2.05] (client-internals/decomp-findings-2026-10-25-k/knockback-probes.tsv) |
| 4 | 0.6 | 1.1 | [2.05] (client-internals/decomp-findings-2026-10-25-k/knockback-probes.tsv) |
| 5 | 0.6 | 2.0 | [2.05] (client-internals/decomp-findings-2026-10-25-k/knockback-probes.tsv) |
| 6 | 0.6 | 2.9 | [2.05] (client-internals/decomp-findings-2026-10-25-k/knockback-probes.tsv) |
| 7 | 0.6 | 2.9 | [2.05] (client-internals/decomp-findings-2026-10-25-k/knockback-probes.tsv) |
| 8 | 1.5 | 2.9 | [2.05] (client-internals/decomp-findings-2026-10-25-k/knockback-probes.tsv) |
| 9 | 2.4 | 2.9 | [2.05] (client-internals/decomp-findings-2026-10-25-k/knockback-probes.tsv) |
| 10 | 2.4 | 1.1 | [2.05] (client-internals/decomp-findings-2026-10-25-k/knockback-probes.tsv) |
| 11 | 2.4 | 2.0 | [2.05] (client-internals/decomp-findings-2026-10-25-k/knockback-probes.tsv) |
| 12 | 2.4 | 2.9 | [2.05] (client-internals/decomp-findings-2026-10-25-k/knockback-probes.tsv) |

### 4.3.7.2 Hurt mode by build

Hurt mode was measured across builds. Each row gives one build's lock-out, knockback, pose and blinking. The 1.39 knockback is disputed between the binary and a live run [bin] (version-profiles/matrix/rules-1st-graal.md#hurt-and-knockback-bin).

| Build | Lock-out | Knockback | Hurt pose | Blinking | Source |
| --- | --- | --- | --- | --- | --- |
| 1st Graal | 40 ticks; walking refused while the counter is 30 or more | 5 steps; baddy and projectile hits an axis unit step from the attacker's facing, a sword hit the centre-to-centre delta; no zero-vector rule | the hurt body while the counter is above 30 | odd counters draw a single frame | [bin] (version-profiles/matrix/rules-1st-graal.md#hurt-and-knockback-bin) |
| 1.32 | 40 ticks (mode 3); a new hit refused while it lasts | 5 steps (counter 39 to 35), twelve body probes, a blocked step undone; baddy touch a unit step from the baddy's facing table, a sword hit half the centre-to-centre delta with 1st Graal's broken normalisation; no zero-vector rule | the hurt body while the counter is above 30 | odd counters at 34 or below | [bin] (version-profiles/matrix/rules-132.md#hurt-and-knockback-bin) |
| 1.39 | 40 ticks; a hit is also refused in mode 7 | 5 tiles, from the binary and measured online on open ground (→ §4.3.7.2) | about 10 ticks, the back with the arms out | after the pose, every other tick to 40 | [1.39] (version-profiles/matrix/rules-139.md#hurt-and-knockback-bin); [live][1.39] (client-internals/player-mannerisms-live.md#notes-per-build); [lab] (protocol/lab-appe-hostb-2026-11-20.md#knockback-on-139-e309) |
| 1.41 | 40 | 5 steps | `hurt` 31 ticks | from the hit, every other tick | [live][1.41] (client-internals/player-mannerisms-live.md#cross-version-table) |
| 2.05 rev 2 | 40 | 5 steps | `hurt` 31 ticks (`hurt.gani` 1 frame, WAIT 30), keeping the facing; 12 ticks when an arrow is held | the body drawn on alternate ticks, only the shadow on the off ticks, for all 40 ticks, after `hurt` has given way | [live][2.05] (client-internals/player-mannerisms-live.md#hurt-knockback-and-blinking-live) |
| 2.22 | 40 | 4.9 tiles on the same test | 12 ticks with an arrow held | unmeasured | [live][2.22] (client-internals/player-mannerisms-live.md#cross-version-table) |
| 5.24r4, 5.30r3, 6.03r7 | unmeasured | 5 tiles in 5 ticks | `idle` 1.54 to 1.55 s after the hit | blinks | [wire] (protocol/v5v6-lab-play.md) |

**Settled question, formerly E#309: knockback distance of 1.39.** Whether 1.39 knocks a hurt player back four or five tiles was open between a code read and one offline video; an online run on open ground settled it [lab] (protocol/lab-appe-hostb-2026-11-20.md#knockback-on-139-e309).

| Part | Discussion | Source |
| --- | --- | --- |
| Claims | A: one tile per tick while the hurt counter runs 39 down to 35, five steps. B: four tiles on the offline touch-NPC test | [1.39] (version-profiles/matrix/rules-139.md#hurt-and-knockback-bin); [live][1.39] (client-internals/player-mannerisms-live.md#cross-version-table) |
| Settled | On 1.39 a hurt message on open ground moved the player five tiles east (3 runs), south and north | [lab] (protocol/lab-appe-hostb-2026-11-20.md#knockback-on-139-e309) |
| Verdict | Verified: Claim A holds; the four-tile reading lost a step | [lab] (protocol/lab-appe-hostb-2026-11-20.md#knockback-on-139-e309) |

## 4.3.8 Combat, baddy and lava rules by build, 1.21 to 2.31

A 2026-11 static pass compared the baddy, combat and tile code of 35 Windows builds from 1.21 to 2.31, with one live 1.39 check [bin][live] (client-internals/combat-baddy-tile-by-version.md). The rows give what changes; anything not listed is the same as 2.05 rev 2.

| Rule | Builds | Source |
| --- | --- | --- |
| sideways reach of the sword box includes the 2-tile edge | every build, 1.21 to 2.31 | [bin] (client-internals/combat-baddy-tile-by-version.md#the-sword-box-the-victim-judging-another-players-swing) |
| swing gate | sprite 6 to 10 in 1.21 to 1.33; animation step 9 to 13 from 1.34 (equivalent) | [bin] (client-internals/combat-baddy-tile-by-version.md#the-sword-box-the-victim-judging-another-players-swing) |
| AP 100 immunity | from 1.34; none in 1.21 to 1.33 | [bin] (client-internals/combat-baddy-tile-by-version.md#sword-judge-gates) |
| a victim in player mode 7 (attached to another local player in same-PC play: carried, or a horse passenger) is passed over | 1.34 to 1.41; never applies online | [bin] (client-internals/combat-baddy-tile-by-version.md#the-sword-box-the-victim-judging-another-players-swing) |
| no sword hit on a victim in ghost mode (170), and no sword judging in Kingdoms or New World mode (176, 177) | 2.17.1, 2.22, 2.31 | [bin] (client-internals/combat-baddy-tile-by-version.md#sword-judge-gates) |
| sword power stored raw (6 bits), no ±20 limit | 1.39 to 2.02; the limit from 2.03 | [bin] (client-internals/combat-baddy-tile-by-version.md#sword-power) |
| hits by packet (40, 46): 10-tile range, 1-heart cap, AP 100 check | same handler 2.03 to 2.31; 1.39 has an id 40 handler with the 1-heart cap but no range or AP test | [bin] (client-internals/combat-baddy-tile-by-version.md#hits-by-packet-ids-40-and-46) |
| selected 1.41 rev 1 id 40 extra field | after the attacker prefix, a six-byte body adds one three-byte NPC identifier; missing NPC skips hurt, matched NPC supplies the range centre and skips the attacker kill-credit tail; short and long paths share the squared-distance limit 100 for ordinary finite coordinates | [bin] (client-internals/combat-baddy-tile-by-version.md#selected-141-rev-1-extra-hit-fields) |
| baddy AI tables | byte-identical in all 33 builds with the baddy class; NewWorld betas have none | [bin] (client-internals/combat-baddy-tile-by-version.md#baddy-ai) |
| swamp soldier: the sword's window | counter 17 or more, no upper bound, 1.21 to 2.00; 22 to 36 from 2.01 | [bin] (client-internals/combat-baddy-tile-by-version.md#baddy-ai) |
| a dying baddy drops an item on the client (green rupee under 10, blue under 15, heart under 30, darts under 75 for types 3, 4, 9, out of 100) | 1.21 to 1.41; gone from NewMain 1.42 | [bin][live] (client-internals/combat-baddy-tile-by-version.md#1x-clients-roll-an-item-when-a-baddy-dies) |
| lava burn | none in 1.21; from 1.28 beta 2, half a heart per 101-tick cycle at (x + 1.5, y + 2) | [bin] (client-internals/combat-baddy-tile-by-version.md#lava-and-tile-rules) |
| death | dead-bit threshold 28 and timer cap 30 in every build; respawn AP bands (3 / 5 / max hearts at under 20 / under 40 / 40+ AP) from 1.41 rev 1 | [bin] (client-internals/combat-baddy-tile-by-version.md#death) |
| sword-clash spark: five ticks of `arrays.dat` array 21 | 1.28 beta 2 to 2.31 | [bin] (client-internals/combat-baddy-tile-by-version.md#the-sword-clash-spark) |

Lab runs since the static pass checked three of these rows on real clients [lab] (live-runs/sword-edge-2026-11-18/README.md); [lab] (live-runs/open-issues-2026-11-19/README.md#1-443-item-drops-when-a-baddy-dies).

| Check | Result | Source |
| --- | --- | --- |
| sideways sword edge | two real 1.35 clients: a victim exactly 2 tiles to the side is hit on both sides; 2.5 tiles misses | [lab] (live-runs/sword-edge-2026-11-18/README.md) |
| no client drop roll from 2.0 | 2.05 rev 2 offline: 17 archer and 8 soldier kills, no drop; a 1.39 control on the same levels dropped 9 times in 12 archer kills (8 darts, 1 green gralat), as the 75 % archer roll predicts | [lab] (live-runs/open-issues-2026-11-19/README.md#1-443-item-drops-when-a-baddy-dies) |
| 1.21 kill reward | 12 of 12 archer sword kills raised the gralat count by exactly 1 in the frame of death. Ranged kills settle it: with the player 14 tiles away, explosion kills of boxed archers drew a heart, darts and green gralats at the archer's spot and never changed the counter, so 1.21 rolls a real ground drop and the sword-kill +1 was a dropped gralat picked up at once | [lab] (live-runs/open-issues-2026-11-19/README.md#1-443-item-drops-when-a-baddy-dies); [lab] (live-runs/drops-2026-11-20/README.md#1-121-the-archer-drops-an-item-the-counter-does-not-change) |
| 2.17.1 drops | 4 archers killed at range by explosions in Training: nothing drawn at any spot, as on 2.05 rev 2 | [lab] (live-runs/drops-2026-11-20/README.md#2-2171-no-drop) |
| sword-clash spark | on 1.39, three swings into a rock wall showed the blade from about 25 to 240 ms after key-down and no separate spark | [lab] (live-runs/open-issues-2026-11-19/README.md#2-443-the-sword-spark) |

Open: → App. E#324.

## 4.3.9 Spin and lay on the wire (2.05 rev 2, 2.22)

A loopback capture of the real 2.05 rev 2 and 2.22 clients. The spin window, the `GANI` bytes, and a laid rupee are below. Laying rules already in → §4.5.2.2 stay; this section is what those two clients sent [lab][cap] (client-internals/spin-lay-205-2026-11-14.md).

| What was sent | 2.05 rev 2 | 2.22 | Source |
| --- | --- | --- | --- |
| Second S during the swing | `GANI` `spin` on 18 of 20 tries from +111 ms to +290 ms (about 0.1–0.3 s). Inside that span, +271 ms sent a second `sword` and +131 ms sent nothing. +91 ms and +93 ms stay `sword`. +321 ms and later, on earlier tries, starts a new `sword` | `spin` at +131, +200 and +271 ms (3/3) | [lab][cap] (client-internals/spin-lay-205-2026-11-14.md#spin-a-second-s-during-the-swing) |
| `GANI` on the wire | prop 10 is a length byte equal to the name, then `sword`, `spin` or `idle` | the same names | [lab][cap] (client-internals/spin-lay-205-2026-11-14.md#spin-a-second-s-during-the-swing) |
| End of the swing or spin | no `idle`. `idle` goes out on a walk, or on A with S held | `idle` about 262 ms after `sword`, and 630–680 ms after `spin` | [lab][cap] (client-internals/spin-lay-205-2026-11-14.md#spin-a-second-s-during-the-swing) |
| S held, then A | `idle`, then a held rupee that cycles green, blue, red with no further send; A alone sends `PLI_ITEMADD` then `RUPEESCOUNT` in one frame | the same item frame; the pick asks for `item2.wav` and does not ask for `item.wav` | [lab][cap] (client-internals/spin-lay-205-2026-11-14.md#laying-s-held-then-a) |
| Landing | `(x + 0.5 + dx, y + 1 + dy)`, north `(0, −3)`, west `(−2, 0)`, south `(0, +2)`, east `(+2, 0)` | the south case matches | [lab][cap] (client-internals/spin-lay-205-2026-11-14.md#laying-s-held-then-a) |
| After the lay | `PLI_ITEMDEL` 8.2–8.6 s later; an arrow while the rupee is held sends nothing and leaves the count unchanged | `PLI_ITEMDEL` at 8.45 s | [lab][cap] (client-internals/spin-lay-205-2026-11-14.md#laying-s-held-then-a) |

## 4.3.10 The baddy AI step (2.22)

The 2.22 client runs one AI step every 100 ms, every second 50 ms game tick, and all counters below are in steps. Online, only the level's leader thinks for the baddies and sends their changed props; every client draws what the server relays and judges touch and sword hits for what it sees [2.22][cap] (client-internals/baddies-222.md#summary). The props on the wire are in → §2.6, and the server's share (mode 5 to 9, respawn, drops) in → §5.

Each type has its own hit points, step and way of attacking. The table gives them as the 2.22 client creates them [2.22] (client-internals/baddies-222.md#types-222).

| Type | Name | Power | Shield | Walk / hunt step (tiles) | Attacks with | Starts in | Source |
| ---: | --- | ---: | :---: | --- | --- | --- | --- |
| 0 | graysoldier | 2 | yes | 0.25 / 0.5 | melee | walk | [2.22] (client-internals/baddies-222.md#types-222) |
| 1 | bluesoldier | 3 | yes | 0.25 / 0.5 | melee | walk | [2.22] (client-internals/baddies-222.md#types-222) |
| 2 | redsoldier | 4 | yes | 0.25 / 0.5 | melee | walk | [2.22] (client-internals/baddies-222.md#types-222) |
| 3 | shootingsoldier | 3 | no | 0.25 / 0.5 | arrows | walk | [2.22] (client-internals/baddies-222.md#types-222) |
| 4 | swampsoldier | 2 | no | does not move | arrows from the swamp | mode 6 | [2.22] (client-internals/baddies-222.md#types-222) |
| 5 | frog | 1 | no | jumps | none | mode 7 | [2.22] (client-internals/baddies-222.md#types-222) |
| 6 | octopus | 1 | no | 0.5 / none | ink | walk | [2.22] (client-internals/baddies-222.md#types-222) |
| 7 | goldenwarrior | 6 | yes | 0.25 / 0.5 | melee | walk | [2.22] (client-internals/baddies-222.md#types-222) |
| 8 | lizardon | 12 | no | 0.5 / 0.75 | melee | walk | [2.22] (client-internals/baddies-222.md#types-222) |
| 9 | dragon | 8 | no | 0.25 / 0.5 | fire (arrow kind 2) | walk | [2.22] (client-internals/baddies-222.md#types-222) |

The rules below give what each mode does with the step counter `c` (BDPROP 6) and a second counter, `lost` [2.22][cap] (client-internals/baddies-222.md#the-ai-step-222).

| Rule | Source |
| --- | --- |
| Creation: mode 0, body and head down, `c = Random(20) + 40`. Type 4 starts in mode 6 with ani 2, type 5 in mode 7, type 6 faces right with ani 4 and `c = Random(10) + 20`. Offline, GS1 `putnewcomp` starts types other than 4 to 6 in hunt with `c = 12`; online it sends `PLI_BADDYADD` | [2.22] (client-internals/baddies-222.md#creation-222) |
| Mode 0, walk: when head and body agree, `c` falls by 1, with `steps.wav` every 5th step. Below 0 the octopus goes to mode 8 with `c = 13`, any other type to mode 1 with `c = 44`. Blocked ahead, the head turns back (`head = dir + 2`), the body turns right (`dir = dir + 3`) and an even `c` is made odd; otherwise the baddy moves one walk step. When head and body disagree, an even `c` turns the body to the head | [2.22] (client-internals/baddies-222.md#mode-0-walk-222) |
| Mode 1, look about: `c` falls by 1; the head turns by the table `{1, 1, 0, −1, −1, 0, 1, 1, 0, −1, −1}` at index `c div 4`. Below 0: a random direction, mode 0, `c = Random(20) + 40`. 44 steps is 4.4 s | [2.22][cap] (client-internals/baddies-222.md#mode-1-look-about-222cap) |
| Walk and look about run the sight check with the head's direction; seeing the target starts the hunt with `c = 16`, a 1 s pause before the chase (12, a 0.6 s pause, after a hit) | [2.22][cap] (client-internals/baddies-222.md#mode-2-hunt-222cap) |
| Mode 2, melee chase (`c < 6`): `c = (c + 3) & 3`, so it cycles 0, 3, 2, 1. Out of sight, `lost` rises by 1, and above 40 (4 s) the baddy goes back to look about. It moves on the axis with the larger distance to the target, plus the other axis scaled by the smaller / larger ratio when that side is free, then unsticks to the half-tile grid if blocked | [2.22][cap] (client-internals/baddies-222.md#mode-2-hunt-222cap) |
| Mode 2, archers (types 3 and 9): walk to a spot 11 tiles from the target in line with it, and shoot within 1 tile of it, after 40 steps of trying, when stuck, or when in line 11 tiles or more away. A shot sets `lost = 15`, a 1.5 s cool-down, and goes out as `PLI_ARROWADD` with sprite `107 + dir` | [2.22] (client-internals/baddies-222.md#mode-2-hunt-222cap) |
| Modes 3 and 4, hurt and shield bump: while `c > 2` the knock vector is added unless that puts an inner point in a wall, so `c = 8` at the hit moves it for 6 steps. Below 1, power under 1 means mode 5 with `c = 14`; otherwise mode 2 with `c = 12`, facing the target, `lost = 0` | [2.22][cap] (client-internals/baddies-222.md#modes-3-and-4-hurt-and-shield-bump-222cap) |
| Mode 5, dying: `c` counts down to −1 (1.5 s from 14), then the puff. Offline the client removes the baddy; online the server sends mode 9 after 2 s, and mode 9 removes it | [2.22][srv] (client-internals/baddies-222.md#mode-5-dying-and-mode-9-dead-222srv) |
| Mode 6, swamp soldier: `c` cycles `(c + 1) mod 43`; it leaps out at 17, faces the target at 22, shoots at 25 and faces down at 33. A hit sets `lost = 8` instead of a knockback, and it can be hit or hurt only while `21 < c < 37` | [2.22] (client-internals/baddies-222.md#mode-6-swamp-soldier-type-4-222) |
| Mode 7, frog: `c` cycles `(c + 1) mod 46`, jumps back to its start ±4 tiles on even values of `lost`, and plays `frog.wav` at 16. It can be hit or hurt only while `16 < c < 38`, and one hit kills it | [2.22] (client-internals/baddies-222.md#mode-7-frog-type-5-222) |
| Mode 8, octopus ink: `c` falls from 13; ink (sprite 131) at 6; at 0 a random direction, mode 0, `c = Random(10) + 20` | [2.22] (client-internals/baddies-222.md#mode-8-octopus-ink-type-6-222) |

Targets, sight and walls follow fixed rules. The table gives them [2.22] (client-internals/baddies-222.md#target-222).

| Rule | Source |
| --- | --- |
| Target: the nearest player by `max(|dx|, |dy|)` between centres, where the first candidate is taken without a sight test and every closer one must be seen; so a lone player is always the target | [2.22] (client-internals/baddies-222.md#target-222) |
| Sight: the point is strictly on the facing side within a 90° cone, within 20 tiles, and a one-tile walk from the baddy's centre to it meets no wall, water, chair, bed bottom, player, NPC, horse or other 2 × 2 object | [2.22] (client-internals/baddies-222.md#sight-222) |
| Blocking: off the board (0 to 64), a wall, water (tile type 11), a chair (3), the bottom of a bed (5), another player's body (online only), an NPC, a horse or another 2 × 2 object; three probes per side, at 0.1, 1 and 1.9 along the edge | [2.22] (client-internals/baddies-222.md#what-blocks-a-baddy-222) |

A hit runs the hurt routine on the leader. The rules below give that routine and what a client that is not the leader sends instead [2.22][cap] (client-internals/baddies-222.md#the-hurt-routine-222cap).

| Rule | Source |
| --- | --- |
| A hit takes the hit's power off the baddy's power. The swamp soldier sets `lost = 8`, the frog dies at once, any other type goes to mode 3 with knock length 2.0. A shield block goes to mode 4 with knock length 0.8 and `swordon.wav`, and pushes the player back | [2.22][cap] (client-internals/baddies-222.md#the-hurt-routine-222cap) |
| Then `c = 8`, and the knock vector is `−(P − B) × 2`, from the player's centre P to the baddy's centre B, scaled to the knock length; a zero vector becomes (−length, 0) | [2.22][cap] (client-internals/baddies-222.md#the-hurt-routine-222cap) |
| A client that is not the leader takes the power locally, sets mode 3 and a pending flag, and sends `PLI_BADDYHURT` with dx and dy as `round((Px − Bx + 4) × 16)` and `round((Py − By + 4) × 16)`, each clamped to ±4 tiles, and the power as is. The leader decodes `(byte − 32 − 64) / 16`. A captured hit facing right with sword power 1 carried dx −3.5, dy 0 and power 1 | [2.22][cap] (client-internals/baddies-222.md#the-hurt-routine-222cap) |
| Verses: sight (BDPROP 8), hurt (9) and attack (10) are each said once in a baddy's life, for 20 steps (2 s): on first entering hunt, after the first knockback that does not kill, and on the first touch after the sight verse | [2.22] (client-internals/baddies-222.md#verses-222) |
