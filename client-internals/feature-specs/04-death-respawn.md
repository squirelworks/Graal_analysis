# 04 Death, respawn and health regeneration

Snapshots read: Graal_analysis `8da6800`, Seihai `06aacfd`, GServer-v2 `TPlayerProps.cpp`, `TPlayer.cpp`, `TAccount.cpp`.

## What it is
Death is **client-driven**. When hearts reach zero the client sets the DEAD bit in its STATUS prop (bit `0x08` of prop 18), sends the prop, and (if a killer is known) sends `PLI_CLAIMPKER` (14) `s killer id`. The server reacts to the bit transitions; it does not move the player or heal gradually.

## Exact server behaviour (`TPlayerProps.cpp`, STATUS case) **[srv]**
- **Dies** (bit goes 0 to 1): unless the level is a sparring zone, `deaths` increases and `dropItemsOnDeath` runs (random gralats between `mindeathgralats` and `maxdeathgralats` as a floor item, plus items if `dropitemsdead`). If the dead player was level leader and others are present, leadership passes to the next player and that player gets `PLO_ISLEADER` (10).
- **Revives** (bit goes 1 to 0): the server sets hearts by AP: AP under 20 gives 3 hearts, under 40 gives 5, otherwise the full MAXPOWER; at least 0.5. It pushes `PLPROP_CURPOWER` to the player and the level, and re-sends `ISLEADER` if the player is leader. **There is no warp**: where the player respawns is a client decision.
- AP (the "alignment" prop 32): with `apsystem` on, `TPlayer::doTimedEvents` counts `apCounter` down once a second (not while paused or in a sparring zone). At zero AP goes up by 1 (max 100), the server pushes `PLPROP_ALIGNMENT` to the player and the level, and reloads the counter from `aptime0..4` (30/90/300/600/1200 s in the lab, by AP band 0-19, 20-39, 40-59, 60-79, 80+). Entering a sparring zone at 100 AP drops it to 99.
- `PLI_CLAIMPKER` (`msgPLI_CLAIMPKER`): ignored for self-kills or an unknown killer. In a sparring zone a Glicko-style rating update runs for both players (skipped if both share an IP) and `lastspartime` is set. Elsewhere the killer gets +1 kills (unless `dontchangekills`), and if `apsystem` is on and the victim has 20+ AP and the killer has any AP, the killer loses AP by a formula based on both AP bands and the killer's counter is reloaded.
- Heart regeneration is not periodic on the server. Hearts come from heart items (03), `healswords`, the revive rule above, or script/NPC props. A client-sent CURPOWER above the server value is refused while AP is under 40.
- Login saves/loads HP (`HP`, `MAXHP`, `AP`, `APCOUNTER`, `KILLS`, `DEATHS`) in the account file (05).
- Idle: `disconnectifnotmoved` + `maxnomovement` (1200 s in the lab) kicks idle players with a disconnect message (see 13).
- Baddy death timers are in 02 (2 s to dead, `baddyrespawntime` 60 s).

## What 2.05 does on the client side **[2.05][dec]**
From the 2.05 rev2 decompile (2026-10-24). Tick = 50 ms. Behaviour only; tables are in `../decomp-findings-2026-10-24/` (`01-death-respawn.md`, `constants-205.tsv`, `life-states.tsv`, `player-modes.tsv`).

**Trigger.** Any change that leaves hearts at 0 or below starts the death sequence once. A per-frame safety net also forces the dead life-state whenever hearts are 0 or below.

**Sequence on the dying client**
1. A death timer starts at 0 and counts up each tick; it **stops at 30 (1.5 s)**.
2. Life-state becomes dead, mode returns to 0 (normal) and the player faces down.
3. The local `dead` gani plays and the script event `playerdies` fires.
4. **Controls are ignored until the timer passes 27 (1.35 s)**, so input works from timer 28.
5. The STATUS prop (18) gets the dead bit (0x08) **only when life-state is dead and the timer is at least 28** (about 1.4 s after death). Other players therefore see the death about 1.4 s late.
6. No dead sprite goes on the wire: prop 17 shows idle plus direction (see 11). The dead state is carried by the status bit only.

**Respawn**
- After the timer passes 27, any movement or action key respawns the player. **There is no respawn packet and no server permission step** on this path. After respawn the client clears the status bit 0x08 when life-state returns to playing, and the server's revive rule (above) sets hearts and pushes CURPOWER.
- Hearts the client sets, by AP: below 20 gives 3; 20 to 39 gives min(5, max hearts); 40 or more gives max hearts. (Same bands as the server's revive rule.)
- **Destination** = the last saved level-entry point (level, x, y, direction). It is updated on every level entry (unless the old and new levels share the same "name group", see open items) and at login. If nothing was saved and the client is online: x 30.5, y 30.0, facing down, in the current level. Offline: the default start level `tutorial_b-4.graal`.
- When the online flag is set the client **re-sends the current level at the current x/y**, so the server sees an ordinary level warp (`PLI_LEVELWARP` route), not a "died" message.

**CLAIMPKER.** The *victim's* client sends `PLI_CLAIMPKER` (14) with the attacker's player id when a sword hit, an explosion hit or a UDP hurt leaves hearts at 0 or below. The server's reaction is in `TPlayerProps.cpp`/`TPlayer.cpp` (above); it is not in the client binary.

**Damage rules that feed this**
- Healing only happens at AP 40 or above.
- No damage in swim mode (10) or in the editor/pause state unless forced. Hurt state: mode 3 for 40 ticks, `hurt` gani, knockback, script event `playerhurt`. A player already in mode 3, mode 10 or dead cannot be hurt.
- Hearts, AP and max-power sit in an attribute array the client stores obfuscated twice and cross-checks; a mismatch raises "memory problems error 1/2". Editing hearts from outside the client is detected by the client itself. A Seihai that holds hearts in plain fields has no such check (fine, the server stays authoritative).

**Open**
- The exact "same name group" rule for *not* updating the saved entry point was only partly traced. Until it is known, update the saved point on every level entry and treat a warp inside one map or group as a Seihai choice.
- The server-side reaction to CLAIMPKER is described above from GServer-v2, not from the client.
- The `0x20` STATUS bit and a few mode values are unlabelled (see 11).
- 1.39 and 1st Graal death handling was not read.

## Seihai today
- Reads `player_health` for the HUD. Does not send STATUS, does not track the dead bit, does not send CLAIMPKER, and treats `ISLEADER` (10) as unhandled.
- Offline: the web-Seihai design (`formats/seihai-systems.md`) has its own death panel and revive (85% of rupees kept, spawn at level start). Seihai's own invention, fine for offline.

## Steps for Claude
1. Track CURPOWER from the server. Add `dead: bool` and a death tick counter (50 ms ticks, capped at 30). When hearts become 0 or below after a hit (02), start the timer, play `dead`, and send CLAIMPKER (14) when the hit has an attacker id. Set the DEAD bit (0x08) in STATUS and send it only once the timer reaches 28 (2.05 behaviour).
2. While dead: show the `dead` gani frame (or a placeholder), block movement and weapons until the timer passes 27. Send prop 17 as idle plus direction.
3. Respawn on any movement or action key once the timer has passed 27 (the 2.05 rule, no timer-only respawn): clear the bit, send STATUS, accept the server's CURPOWER push (hearts by AP, as in the table above). Respawn location: the last saved level-entry point (level, x, y, direction), updated on every level entry; if none, x 30.5, y 30.0 facing down in the current level. Re-send the current level at that x/y as an ordinary level warp. No respawn packet exists. Keep the saved point configurable only for the open "same name group" case.
4. Show gralat loss from the floor item the server drops (ITEMADD from 03).
5. Handle `PLO_ISLEADER` (10) by storing `is_leader` (needed for 02 baddies).
6. Show an HP regen hint only if the server pushes CURPOWER; do not simulate regen.

## How to test
- Lab: Seihai sends the dead bit (STATUS prop with bit 0x08) and then clears it. Check the lab account file: `DEATHS` increments, and the server pushes CURPOWER = full hearts (the default account has AP 50, so the rule gives MAXPOWER, 3 hearts). Set AP under 40 in a copy of the account to see the 5-heart and 3-heart bands.
- Second client observes `PLO_OTHERPLPROPS` with the STATUS dead bit.

## NEEDS
Filled by the 2026-10-24 2.05 decompile: timings, input lock, status-bit delay, hearts by AP, destination rule, and that no respawn packet exists. Server side was already known.

Still open: the "same name group" rule for the saved respawn point, the unlabelled STATUS bit 0x20 and a few mode values, and the 1.39 / 1st Graal death handler. A lab capture of a real 2.05 client dying twice would confirm the sequence on the wire (status bit timing, the warp frame after respawn).
