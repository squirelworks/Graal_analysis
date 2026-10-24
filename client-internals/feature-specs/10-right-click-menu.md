# 10 Right-click context menu (player list popup, profile)

Snapshots read: Graal_analysis `8da6800` (`versions-133-139.md`, `version-profiles/141-217.toml`, `protocol/chat-pm-rc.md`, `client-architecture-205.md`), Seihai `06aacfd`, GServer-v2 (`TPlayerRequestText.cpp`, `TPlayer.cpp` PM/profile handlers).
Folded here from the public-server report: **PLO_STAFFGUILDS 47** (player-list "Staff" section).

## What is known **[2.05][inf]**
- There is no context menu on the wire. It is client UI. The 2.05 client has a `TPlayerList` form (F7) with a popup menu whose item names in the string table are **Ignore, History, Buddy, Profile** (click handlers for each). The 1.33 build had Message, Ignore, History; Buddy came in 1.35 (`buddyaccounts.txt`); Profile and the Player List Options window came in 1.39. A `TPersonAction` form exists in 2.05 (purpose not traced). "Right-click profile" is a listed feature in the 2.17 profile.
- Actions behind the items, with what is known:
  - **Message**: opens the PM box; sends `PLI_PRIVATEMESSAGE` (28) `s count, s player...` + text. Done in Seihai (`send_pm`).
  - **Profile**: sends `PLI_PROFILEGET` (80) with the account; the listserver answers `PLO_PROFILE` (75) with 10 length-prefixed fields; fields 1-9 are saved locally. Edit own profile with `PLI_PROFILESET` (81). GServer-v2 does **not** answer profile requests; the listserver does.
  - **Ignore**: local only. Add the account (1.34+: by account name) to `ignoredaccounts.txt`; ignored players are drawn red in the list (1.34+) and their chat and PMs are dropped by the client.
  - **History**: local chat/PM history window.
  - **Buddy**: local `buddyaccounts.txt` in 2.05; see 14 for 2.17+.
- Player list sections: 1.33 had GPs, Guild, Normal, Ignore. 2.14+ lists staff in a section named from `PLO_STAFFGUILDS` (47): a list of guild names that count as staff (GServer `staffguilds` option, sent at login by `sendLogin`).
- Right-click on a player's sprite in the world: not documented for 2.05.

## Seihai today
- `ui.rs draw_player_list` shows the other players; `nearest()` picks the closest. No menu, no mouse handling beyond the egui launcher. `PLO_STAFFGUILDS` (47) and `PLO_PROFILE` (75) are not handled; `send_pm` exists.

## Steps for Claude
1. Add mouse input to the framebuffer loop (minifb gives `get_mouse_pos`, `get_mouse_down`). Right-click inside the F7 list selects a row and opens a small menu drawn with `ui.rs` primitives: Message, Profile, Ignore, Buddy, History (hide History until it exists).
2. Message: open the existing chat input in PM mode with the target prefilled.
3. Profile: send `PLI_PROFILEGET` (80) and render the reply when PLO 75 arrives (implement the 10-field parser from `chat-pm-rc.md`; drop field 0).
4. Ignore: keep a set of account names, saved to `ignoredaccounts.txt` next to the settings (one account per line). Filter chat/PM/toall/bubbles for them and tint the row.
5. Buddy: see 14.
6. Store 47 and draw a "Staff" section label for players whose guild matches.
7. Do not add a menu for a world click until NEEDS is answered.

## How to test
- Headless unit tests on the menu model (selection, ignore filter). Visual check under Xvfb on display :9 only.
- Lab: with a lab account PLI 80 reaches GServer, which sends nothing back (expected); profile display needs a listserver reply, so test with a recorded 10-field PLO 75 frame in `lab_replay`.

## NEEDS
"the 2.05 player-list popup and right-click handler": the exact item order and enable/disable rules, the 'World right-click on a player' behaviour, and what `TPersonAction` is. A decompile or screenshot of the 2.05 F7 list with its popup open. Not needed for a minimal menu.
