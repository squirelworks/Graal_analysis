# 05 Player save and load

Snapshots read: Graal_analysis `8da6800`, Seihai `06aacfd`, GServer-v2 `TAccount.cpp`, `TPlayer.cpp` (`cleanup`), `TPlayerLogin.cpp`.

## What it is
For every client from 2.00 on, **the server owns the save**. The 2.05 client contains the string "Save games are not supported anymore", and the offline F2/F3 save games ended with 1.41. The client has nothing to save except its local files (`graalconfig.txt`, `ignoredaccounts.txt`, `buddyaccounts.txt`, per-account profile file, web-level cache `GWEBL001`).

What a client must do is **consume the login burst correctly**, because that burst is the loaded save.

## Server file (GRACC001, `accounts/<name>.txt`) **[srv]**
Text file, first line `GRACC001`, then `KEY value` lines, CRLF on write. Keys read by `TAccount::loadAccount`: NAME, NICK (max 223 chars), COMMUNITYNAME, LEVEL, X, Y, Z, MAXHP, HP, RUPEES, ANI, ARROWS, BOMBS, GLOVEP, SHIELDP, SWORDP, BOWP, BOW, HEAD, BODY, SWORD, SHIELD, COLORS (5 comma-separated), SPRITE, STATUS, MP, AP, APCOUNTER, ONSECS, IP, LANGUAGE, KILLS, DEATHS, RATING, DEVIATION, LASTSPARTIME, FLAG (`name=value`, repeated), ATTR1..ATTR30, WEAPON (repeated), CHEST (repeated: `x:y:level` style string), then the admin block: BANNED, BANREASON, BANLENGTH, COMMENTS, EMAIL, LOCALRIGHTS, IPRANGE, LOADONLY, FOLDERRIGHT (repeated), LASTFOLDER.
- Unknown account: the server clones `accounts/defaultaccount.txt`, applies `startlevel`/`startx`/`starty` from `serveroptions` if set, and saves the new file.
- `guest` accounts are load-only and get a random `pc:` community name.
- Saved on disconnect (`TPlayer::cleanup`, only clients that are not load-only) and every 300 s while connected (`doTimedEvents`). Not saved if the listserver login failed.

## How the save reaches the client (login burst, `sendLogin`) **[srv][cap]**
Order (`TPlayer::sendLogin` then `sendLoginClient`): signature, own props (`PLO_PLAYERPROPS` 9 with the loaded values; no level or position props), `PLO_CLEARWEAPONS`, one `PLO_FLAGSET` (28) per saved player flag, the server flags, `NPCWEAPONDEL` for "Bomb" and "Bow" (the client adds them itself), the account's weapons (`NPCWEAPONADD` 33 and `DEFAULTWEAPON` 43), protected weapons and classes, then the warp: `PLO_PLAYERWARP` (14) to the saved level and x/y followed by the level data. After the level come bigmap/minimap/RPG window (2.1+), `PLO_STARTMESSAGE` (41) and an empty `PLO_SERVERTEXT` (82). Chest open state arrives inside each level's chest packets (03). The saved `LEVEL`, `X`, `Y` therefore arrive as the first warp, not as props.
Level and position are stored, so reconnecting resumes where the player left.

## Seihai today
- Consumes the burst: props (partly), flags (`SessionState.flags`), weapons, default weapons, warp, board, chests list from LEVELCHEST (`opened_chests`).
- No local save. Offline mode in web-Seihai design notes has its own JSON save (`SaveV1` under `formats/seihai-systems.md`), not related to GRACC001.
- Seihai writes only its own `settings.rs` file.

## Steps for Claude
1. Nothing to implement for online play beyond keeping the full self prop stream (03) and flags (done).
2. Keep `login_state` in the session: level, x, y from the first `PLAYERWARP`; log it in `session_probe` output (names only).
3. Optional offline save: keep the existing offline model; do not invent a GRACC001 writer in the client. If a local server is wanted, use GServer-v2 in the lab instead.
4. Add a lab test that logs in twice and asserts the second `PLAYERWARP` equals the position saved at the first logout.

## How to test
- Lab: log in with the placeholder account, move, send a chat, disconnect, then read `servers/lab/accounts/<name>.txt` (X, Y, LEVEL, HP, RUPEES). Reconnect and confirm the warp matches. Never print credentials.
- Or replay a captured login burst through `SessionState`.

## NEEDS
nothing.
