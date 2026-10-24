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

## What 2.05 does on the client side **[inf]**
Not traced. The 2.05 string table has the `dead` and `hurt` animations, the `compudead` sound, and "Respawn" in the NPC editor templates (`this.mode = 5; // RESPAWN`, `setcharani dead`), which are baddy scripts, not the player. The player respawn trigger, destination and delay are not documented in the notes.

## Seihai today
- Reads `player_health` for the HUD. Does not send STATUS, does not track the dead bit, does not send CLAIMPKER, and treats `ISLEADER` (10) as unhandled.
- Offline: the web-Seihai design (`formats/seihai-systems.md`) has its own death panel and revive (85% of rupees kept, spawn at level start). Seihai's own invention, fine for offline.

## Steps for Claude
1. Track CURPOWER from the server. Add `dead: bool` and a `died_at` timestamp. When hearts become 0 after a hit (02), set the DEAD bit in STATUS and send it with the next prop update, then send CLAIMPKER when a hit has an attacker id.
2. While dead: show the `dead` gani frame (or a placeholder), block movement, block weapons.
3. Respawn on a key or after a timer (choose 3 s as a placeholder, mark it as Seihai's choice): clear the bit, send STATUS, and accept the server's CURPOWER push. Respawn location: stay in place first. Make the location a config until NEEDS is answered.
4. Show gralat loss from the floor item the server drops (ITEMADD from 03).
5. Handle `PLO_ISLEADER` (10) by storing `is_leader` (needed for 02 baddies).
6. Show an HP regen hint only if the server pushes CURPOWER; do not simulate regen.

## How to test
- Lab: Seihai sends the dead bit (STATUS prop with bit 0x08) and then clears it. Check the lab account file: `DEATHS` increments, and the server pushes CURPOWER = full hearts (the default account has AP 50, so the rule gives MAXPOWER, 3 hearts). Set AP under 40 in a copy of the account to see the 5-heart and 3-heart bands.
- Second client observes `PLO_OTHERPLPROPS` with the STATUS dead bit.

## NEEDS
"the 2.05 death handler": what the client does when hearts hit zero (input lock, dead animation length, respawn key or timer, respawn destination and the hearts it sets) and what it sends. A decompile of the 2.05 hurt/dead routine, or a lab capture of a 2.05 client dying twice, would settle it. Everything server-side is known.
