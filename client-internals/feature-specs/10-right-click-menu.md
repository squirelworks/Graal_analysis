# 10 Right-click context menu (player list popup, profile)

Snapshots read: Graal_analysis `8da6800` (`versions-133-139.md`, `version-profiles/141-217.toml`, `protocol/chat-pm-rc.md`, `client-architecture-205.md`), Seihai `06aacfd`, GServer-v2 (`TPlayerRequestText.cpp`, `TPlayer.cpp` PM/profile handlers).
Folded here from the public-server report: **PLO_STAFFGUILDS 47** (player-list "Staff" section).

## What is known **[2.05][inf]**
- There is no context menu on the wire. It is client UI. The 2.05 client has a `TPlayerList` form (F7) with a popup menu. **[2.05][dec]** The 2026-10-24 decompile gives the item order: **Message (default item), History, Buddy, Ignore, Profile**. The 1.33 build had Message, Ignore, History; Buddy came in 1.35 (`buddyaccounts.txt`); Profile and the Player List Options window came in 1.39. "Right-click profile" is a listed feature in the 2.17 profile.
- **`TPersonAction` is not a player menu.** It is the level editor's "Set Npc's Action" script editor (opened from the NPC editor, see `level-editor-205.md`). There is no per-player action form (trade, duel and so on) in 2.05. An earlier version of this spec listed it as an unexplained 2.05 form; that is corrected.
- Window facts: the list is a stay-on-top form with a multi-select list view; a panel caption reads "--- N online ---"; buttons Profile and Options. Right-click selects the row under the cursor, then sets the Ignore and Buddy check marks to "checked if every selected player is in that list". Double-click or Enter opens the read-PM window if a PM from that player is pending, otherwise the compose window. PM window titles are "Send Message" and "Read Message". The Options window has 5 check boxes; the profile edit window has 10 fields.
- Actions behind the items, with what is known:
  - **Message**: opens the PM box for **all selected rows** (an existing PM window for the same set is reused); sends `PLI_PRIVATEMESSAGE` (28) `s count, s player...` + text. Recipient encoding in 2.05: a two-byte count, then two bytes per player id, **at most 50 recipients**. Done in Seihai (`send_pm`).
  - **Profile**: uses only the **first** selected player and, when online, sends `PLI_PROFILEGET` (80) with the account; the listserver answers `PLO_PROFILE` (75) with 10 length-prefixed fields; fields 1-9 are saved locally. Edit own profile with `PLI_PROFILESET` (81). GServer-v2 does **not** answer profile requests; the listserver does.
  - **Ignore**: local only. Toggles each selected account in `ignoredaccounts.txt` (1.34+: by account name) and saves the buddy list too; ignored players are drawn red in the list (1.34+) and their chat and PMs are dropped by the client. The client holds an auto-reply string "Your messages are ignored."; the condition under which it is sent was not traced.
  - **History**: opens the message history window (not traced further).
  - **Buddy**: local `buddyaccounts.txt` in 2.05, toggled for each selected account; **Ignore and Buddy are mutually exclusive**; see 14 for 2.17+.
- Player list sections: 1.33 had GPs, Guild, Normal, Ignore. 2.14+ lists staff in a section named from `PLO_STAFFGUILDS` (47): a list of guild names that count as staff (GServer `staffguilds` option, sent at login by `sendLogin`).
- Right-click on a player's sprite in the world: **no such handler was found in the 2.05 decompile**. The only player popup is the F7 list's.

## Seihai today
- `ui.rs draw_player_list` shows the other players; `nearest()` picks the closest. No menu, no mouse handling beyond the egui launcher. `PLO_STAFFGUILDS` (47) and `PLO_PROFILE` (75) are not handled; `send_pm` exists.

## Steps for Claude
1. Add mouse input to the framebuffer loop (minifb gives `get_mouse_pos`, `get_mouse_down`). Right-click inside the F7 list selects a row and opens a small menu drawn with `ui.rs` primitives, in the 2.05 order: Message (default, bold), History (hide until it exists), Buddy, Ignore, Profile. Support multi-select for Message; set the Buddy and Ignore check marks as above and keep them mutually exclusive. Double-click or Enter opens the PM compose box.
2. Message: open the existing chat input in PM mode with the target prefilled.
3. Profile: send `PLI_PROFILEGET` (80) and render the reply when PLO 75 arrives (implement the 10-field parser from `chat-pm-rc.md`; drop field 0).
4. Ignore: keep a set of account names, saved to `ignoredaccounts.txt` next to the settings (one account per line). Filter chat/PM/toall/bubbles for them and tint the row.
5. Buddy: see 14.
6. Store 47 and draw a "Staff" section label for players whose guild matches.
7. Do not add a menu for a world click: 2.05 has none.

## How to test
- Headless unit tests on the menu model (selection, ignore filter). Visual check under Xvfb on display :9 only.
- Lab: with a lab account PLI 80 reaches GServer, which sends nothing back (expected); profile display needs a listserver reply, so test with a recorded 10-field PLO 75 frame in `lab_replay`.

## NEEDS
Filled by the 2026-10-24 2.05 decompile: item order, check-mark rules, PM recipient encoding, what `TPersonAction` is, and that no world right-click exists (all above).

Still open (none blocks a menu):
- The 1.39 popup items (its menu strings are built character by character and were not re-read).
- Where the "Your messages are ignored." auto-reply is sent from.
- What the History window shows (not traced).
- Enable/disable (greyed) rules beyond the check marks, if any.
