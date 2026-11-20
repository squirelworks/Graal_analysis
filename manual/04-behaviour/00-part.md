<!-- manual: kind=reference status=draft -->
# 4 Client behaviour by version

> Status: draft. Each chapter carries its own status line.

## 4.0 Reading this Part

Graal's game rules run on the client, and they run on one clock. One game tick is 50 ms, and the static survey of every Delphi executable finds that interval wherever a frame timer is present. [bin] (version-profiles/matrix/README.md#acts-timing-movement-and-rules); [bin] (version-profiles/matrix/builds-static-survey.tsv) This Part therefore states durations in ticks, and §4.1 fixes how each build drives the tick before any later chapter counts with it. The 5.x and 6.x clients measured on the wire keep 2.05's walk, push, lift and sword timings in ticks, so the counts carry well beyond the Delphi line. [wire] (protocol/v5v6-lab-play.md)

**The client is the referee.** A victim's own client judges another player's sword from that player's props, applies the damage, and reports its own hearts; the attacker only broadcasts its props. [2.05] (client-internals/decomp-findings-2026-10-24/04-sword-hitbox.md#who-decides-a-hit) The same holds for bombs and arrows the server relays. [lab][2.22] (client-internals/lab-captures-2026-10-25/01-damage-chest-respawn-weapons.md#c-curpower-semantics-settled-for-222) A server that wants to reproduce a build's play does not compute combat; it relays the messages each build expects and leaves the rules to the client. Where the authority did move, the move is dated: item drops are rolled by the client up to 1.41 and by the server from NewMain 1.42. [bin] (client-internals/item-drops.md#summary)

**2.05 rev 2 is the reference build.** Most rules here were read in full in 2.05 rev 2, then checked against 2.17.1, 2.22 and 2.31, and against 1st Graal and 1.39 where those builds were read. [2.05] (client-internals/decomp-findings-2026-10-24/constants-205.tsv) A row names the builds it covers. A rule given for 2.05 is not assumed for 1.39 or for 3.x, and the chapters' status lines say which builds are read in full and which only as timed on the wire. The Torque-era 3.x and 4.x frame loops and 6.03r7's were measured in 2026-11: 50 ms steps, as in 1.x and 2.x (→ §4.1.7, §4.1.7). [lab] (client-internals/update-cadence-3x-6x.md)

**How the Part is laid out.** §4.1 gives the tick and the periodic work. §4.2 to §4.5 follow a player through movement, combat, death and the items on the board. §4.6 to §4.9 cover what the player sees and hears, offline play and the editor, and §4.10 the remaining client features, including the integrity checks. §4.11 covers the builds outside the 2.x Delphi line, the code changes inside it, and the windows each build opens around play. §4.12 gives what each key and mouse action does, from a sweep of eight real clients. [live][2.05] (client-internals/player-mannerisms-live.md)

**What is still open.** The open behaviour points are collected in App. E.6 (→ App. E#300), each with the evidence so far, a best guess and the scene that would settle it. Three kinds stand out. The frame driver of three 1998 betas and of 2.22 is read two ways (→ App. E#300, §4.6.10). Several combat and item rules were read statically but not yet seen in a controlled scene (→ App. E#324). And the 6.03r7 HUD and item runs left measurements a script-free lab world could not give (→ App. E#326, §4.5.8). Most of these are settled by one lab scene on the exact build; App. E.11 lists the few that may never be.

## Chapters

- → §4.1 Frame loop and timing (`01-loop-timing.md`)
- → §4.2 Movement and collision (`02-movement-collision.md`)
- → §4.3 Combat, damage, hurt and knockback (`03-combat-damage.md`)
- → §4.4 Death clocks and respawn (`04-death-respawn.md`)
- → §4.5 Items, drops and board respawn (`05-items-board.md`)
- → §4.6 HUD, sign panel, chat text and options (`06-hud-ui.md`)
- → §4.7 Sound (`07-sound.md`)
- → §4.8 Offline and training mode (`08-offline.md`)
- → §4.9 The built-in editor (`09-editor.md`)
- → §4.10 Other client features (`10-feature-specs.md`)
- → §4.11 Precursors, side builds and the 4.x clients in play (`11-side-builds-labs.md`)
- → §4.12 Input: keys and mouse (`12-input.md`)
