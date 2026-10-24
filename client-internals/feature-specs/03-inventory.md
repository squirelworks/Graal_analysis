# 03 Inventory

Snapshots read: Graal_analysis `8da6800`, Seihai `06aacfd`, GServer-v2 (`TLevelItem.cpp`, `TPlayerProps.cpp`, `TPlayer.cpp`).

## What it is
The player's counts and gear are **player props sent by the client**. The server clips and stores them. Items on the floor are `PLO_ITEMADD/ITEMDEL`; chests are `PLO_LEVELCHEST`.

### Item index table (0-24) **[srv]**, used by ITEMADD, ITEMTAKE, chests, DEFAULTWEAPON, WEAPONADD
0 greenrupee (+1 gralat), 1 bluerupee (+5), 2 redrupee (+30), 3 bombs (+5, max 99), 4 darts (+5 arrows, max 99), 5 heart (+1 heart), 6 glove1 (glove power at least 2), 7 bow, 8 bomb, 9 shield (power 1), 10 sword (power at least 1), 11 fullheart (+1 max hearts, hard cap 20, and heals fully), 12 superbomb, 13 battleaxe (sword at least 2), 14 goldensword (sword 4), 15 mirrorshield (2), 16 glove2 (3), 17 lizardshield (3), 18 lizardsword (sword at least 3), 19 goldrupee (+100), 20 fireball, 21 fireblast, 22 nukeshot, 23 joltbomb, 24 spinattack (sets the has-spin status bit). Items 7-8 and 12 and 20-23 become weapons (`addWeapon`). Shields and swords never downgrade. Rupees cap at 9,999,999.

### Props involved (self stream, PLPROP ids) **[srv]**
1 MAXPOWER (hearts), 2 CURPOWER (half-hearts), 3 RUPEESCOUNT (i3), 4 ARROWSCOUNT, 5 BOMBSCOUNT, 6 GLOVEPOWER, 7 BOMBPOWER, 8 SWORDPOWER (`c(power+30)` + image, or a plain power 0-4 for `swordN.png`), 9 SHIELDPOWER (`c(power+10)` + image, or plain 0-3), 18 STATUS bits (`0x40` has spin).
Server clipping when the client sets them (`setProps`): arrows and bombs 0..99; rupees at most 9,999,999; sword and shield power clipped to `swordlimit`/`shieldlimit` (3 in the lab); bomb power 0..3; glove max 3; **CURPOWER cannot rise for players under 40 AP**. With V8NPCSERVER some of these become server-only; the lab server is built without it.

### Item pickup and chests **[srv][cap]**
- Floor item pickup: the client sends `PLI_ITEMDEL` (13) `c x*2, c y*2`. The server relays `PLO_ITEMDEL` (23) to everyone else and removes it from the level. It does **not** give the item on 13. `PLI_ITEMTAKE` (32) does the same removal and also applies the item to the player's props (via the table above) and echoes the prop change to the player and the level. 2.05 used 13 in the capture (client then edits its own props). **[cap]**
- Dropping an item: `PLI_ITEMADD` (12) `c x*2, c y*2, c item`; the server relays `PLO_ITEMADD` (22), adding a player id for dropped swords and shields.
- Chest open: `PLI_OPENCHEST` (20) `c x, c y` (whole tiles). If the account has not opened it (`chestList` in the save), the server applies the chest item with the same table, answers `PLO_LEVELCHEST` (4) `c 1, c x, c y`, and records the chest. Level entry sends one LEVELCHEST per chest (`c opened, c x, c y` + `c item, c signindex` if closed). The account's opened-chest list persists (see 05).
- Drops: bushes/vases with `bushitems`, baddies with `baddyitems`, and deaths (`dropitemsdead`, `mindeathgralats`..`maxdeathgralats`, `dropItemsOnDeath`) create ITEMADD packets from the server.
- Weapon list display is in 02.

## Seihai today
- `send_open_chest` exists; `main.rs` sends it on A/Space near a chest and takes the reply (`opened_chests`) into the session. The item itself is not applied: the chest item index is printed to stderr only.
- HUD draws `player_health` and `rupees` (`render/tiles.rs draw_hud`). Bombs, arrows, sword, shield, glove, MAXPOWER, AP, status are not displayed or sent.
- ITEMADD/ITEMDEL (22, 23) are unhandled. Own-prop sending is limited to position/sprite/chat.
- Offline mode has its own item model (`offline/mod.rs give_item`) that is not the GServer table.

## Steps for Claude
1. Add an `Inventory` struct to `SessionState` filled from the self prop stream: maxpower, curpower, rupees, arrows, bombs, glove, bombpower, sword (power+image), shield (power+image), status bits. Fix decode for both prop forms (see `protocol/props.rs`).
2. Parse PLO 22/23 into a per-level list of floor items (x,y,item); parse PLO 4 chests; draw both.
3. Pickup: when the player's feet overlap a floor item, send `PLI_ITEMTAKE` (32) if the version profile has it (2.05 lists 32), and let the server echo the new props; fall back to 13 plus local prop edits if a server ignores 32.
4. Chest: after the server's LEVELCHEST (opened=1), show the item name from the table and update the inventory locally only if no echo arrives within one tick (the lab echoes via `setProps`).
5. HUD: hearts (CURPOWER/2 of MAXPOWER), rupees, bombs, arrows, selected weapon.
6. Implement an item key (`Q` in the original) to select among default weapons and named weapons; sending a use event is 02's job.
7. Add a unit test per table row (item index to prop change) and a replay test using the lab chest/bush captures.

## How to test
- Lab, one Seihai: log in, walk to a bush, bomb it, take the drop, and verify the prop echo. Chest in `onlinestartlocal.nw` if present; otherwise use the RC-free approach of adding a chest to the lab level file (Seihai supports `.nw` reading, the editor in `tools/level-editor` can place one).
- Check server saved state afterwards in the lab account file (`servers/lab/accounts/<name>.txt`): RUPEES, BOMBS, ARROWS, SWORDP, CHEST lines.

## NEEDS
nothing blocking. Optional: "the 2.05 item/weapon list window (Q key) layout" for a faithful HUD; not needed for interoperability.
