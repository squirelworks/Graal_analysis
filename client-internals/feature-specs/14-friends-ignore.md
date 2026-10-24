# 14 Friends (buddies), ignore, mute, status

Snapshots read: Graal_analysis `8da6800` (`versions-133-139.md`, `version-profiles/*.toml`, `protocol/chat-pm-rc.md`, `graalconfig-reference.md`), Seihai `06aacfd`, GServer-v2 (`TPlayerRequestText.cpp`, `TPlayerProps.cpp` status message, `TPlayerLogin.cpp`), graal-serverlist (`TServer.cpp` `msgSVI_REQUESTBUDDIES`).
Folded here from the public-server report: **PLO_STATUSLIST 180**.

## What it is
Four separate features.

| Feature | Version | Where it lives |
|---|---|---|
| Ignore a player | 1.33; by account name from 1.34 (`ignoredaccounts.txt`) | client-local; ignored players shown red and their chat/PMs dropped |
| Buddy | 1.35 local `buddyaccounts.txt`; 2.17+ also through the listserver | local in 2.05; listserver in later builds |
| Mute | 2.17+ | `PLI_MUTEPLAYER` (43): `s playerId, c 1/0` (from the playerlist Mute item) |
| Status (Online/Away/DND/...) | 2.14+ | `PLO_STATUSLIST` (180) list, `PLPROP_PSTATUSMSG` (53) index |
Additional ignore switches: `nomassmessages`/`notoalls` options and the ADDITFLAGS prop bits (`0x01` no mass message, `0x04` no toall, `0x08` voice off) (09).

### Server behaviour **[srv]**
- **Ignore**: none. The server never learns about it.
- **Mute (43)**: GServer-v2 defines `PLI_MUTEPLAYER` in the enum but registers **no handler**. It falls to `msgPLI_NULL`, which counts as an invalid packet: **after more than 5 such packets the server disconnects the client**. A real 2.22 client does send it (see lab findings below), and two sends in a lab session did not disconnect.
- **Buddies (2.17+)**: the client sends `PLI_SENDTEXT` (the generic text packet) with tokens `GraalEngine, lister, verifybuddies | addbuddy | deletebuddy` (+ account list). `msgPLI_SENDTEXT` forwards those three options (not for guest accounts) to the **listserver**; graal-serverlist answers `msgSVI_REQUESTBUDDIES` with a `PLO_SERVERTEXT` (82) whose tokens are `weapon, lister, buddylist, <comma list>` built from a database query. GServer itself stores nothing.
- **Status**: `PLO_STATUSLIST` (180) at login (2.1+/RC): comma list from `playerlisticons` (lab: Online, Away, DND, Eating, Hiding, No PMs, RPing, Sparring, PKing). The client sets its own index with `PLPROP_PSTATUSMSG` (53); the server validates it against the list length and rebroadcasts it to everyone (`PLO_OTHERPLPROPS`).
- **Player list pulls**: `PLI_REQUESTTEXT` types `pmservers`, `pmserverplayers <server>`, `pmunmapserver`, `pmguilds` go to the listserver for cross-server and guild tabs. **PM** (`PLI_PRIVATEMESSAGE` 28) is already implemented.

## Lab findings from a real 2.22 client, 2026-10-24 **[cap]**
- Player-list window sections: Staff, Buddies, Guild, Normal, Ignore. Right-click on a player gives: Message, History, Buddy (check mark when set), Ignore, Mute, Profile. (This is the 2.22 popup; the 2.05 popup is a different, shorter menu, see 10.)
- **Buddy add and delete send nothing** on the game-server or listserver connection. The client writes `buddyaccounts.txt` locally and deletes the file when it becomes empty. The `verifybuddies`, `addbuddy` and `deletebuddy` requests were **not** sent in this lab, so their token layout is still unseen. The assumption above that 2.17+ buddies go through the listserver is not supported by this client in this setup; it may only trigger for accounts the listserver knows (a database-backed listserver) or at some other moment.
- **Ignore** is local too: it writes `ignoredaccounts.txt`, one account per line, and sends no packet.
- **Mute** sends `PLI 43`: `GSHORT playerId` + `GCHAR 1` (mute) or `GCHAR 0` (unmute), one message per click. The list entry does not move on Mute, unlike Buddy and Ignore, which move it.
- Not captured: the listserver-side buddy list reply and any status change.

## Seihai today
- PM and toall send/receive (`send_pm`, `send_toall`); chat shows. No ignore filter, no buddy list, no status UI. 180 is unhandled. `send_text` helpers for `PLI_SENDTEXT`/`REQUESTTEXT` do not exist.

## Steps for Claude
1. **Ignore (all versions)**: `ignored: HashSet<String>` loaded from `ignoredaccounts.txt` (one account per line, lower-case compare), applied to chat bubbles, `PLO_PRIVATEMESSAGE` (37), toall. Needs the account name prop (34) for each player; show tinted in the F7 list (10).
2. **Buddy (2.05)**: `buddyaccounts.txt` the same way; mark buddies in the list and print a login notice when a buddy appears (`PLO_ADDPLAYER`/`OTHERPLPROPS` with PCONNECTED). Local only.
3. **Buddy (2.17+, lab)**: implement `send_text(weapon, type, option, args)` using the tokenized form from `TPlayerRequestText.cpp`; send `GraalEngine, lister, addbuddy, <acct>`; parse PLO 82 `buddylist`. Behind a flag until captured.
4. **Status**: parse 180 into the list; send `PLPROP_PSTATUSMSG` (53) when the user picks one (Away on a timer is original behaviour, off by default); show others' status icon index in the list.
5. **Mute (2.17+)**: client-local mute set (same filter as ignore). Optionally also send `PLI 43` (`GSHORT playerId`, `GCHAR 1/0`) as the real client does, but GServer-v2 counts it as an invalid packet, so keep it off by default against that server.
6. Tests: ignore filter on a scripted chat stream; buddy file parse; status prop round trip; assert no `PLI 43` is emitted.

## How to test
- Unit tests for the filters (no network).
- Lab: two sessions, ignore one account locally and send chat from it (the second Seihai or the Wine client); status: set a status index and check the other client receives prop 53. Buddy via listserver: the lab stub has no buddy table, so extend the stub to answer `addbuddy`/`verifybuddies` with a `buddylist` text, or run graal-serverlist with its database.

## NEEDS
the mute payload is now known (see the lab findings). Still open: a capture of the buddy requests (`verifybuddies`, `addbuddy`, `deletebuddy`) and the listserver's `buddylist` reply, which the real client did not send in the 2026-10-24 lab. That needs a database-backed listserver or another trigger. No decompile needed; 2.05 needs nothing (local files).
