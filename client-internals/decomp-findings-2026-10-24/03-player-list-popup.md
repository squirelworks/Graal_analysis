# 2.05 rev2: F7 player list, right-click popup, person action (derived)

## Player list window
- Stay-on-top form with a multi-select list view. A panel caption reads "--- N online ---". Buttons: Profile, Options.
- Popup menu items in order: **Message** (default item), **History**, **Buddy**, **Ignore**, **Profile**.
- Right-click selects the row under the cursor, then sets the Ignore and Buddy check marks to "checked if all selected players are in that list".
- Double-click or Enter: opens the read-PM window if a PM from that player is pending, otherwise the compose window.

## Actions
| Item | Behaviour |
|---|---|
| Message | Builds the recipient list from all selected rows and reuses an existing PM window for the same set. Recipient encoding: a count as two bytes, then two bytes per player id, at most 50 (0x32) recipients. |
| History | Opens the message history window (not traced further). |
| Ignore | Toggles each selected account in the ignore list and saves `ignoredaccounts.txt` and the buddy list. |
| Buddy | Toggles the buddy list (`buddyaccounts.txt`). Ignore and Buddy are mutually exclusive. |
| Profile | Uses only the first selected player. If online, sends PLI_PROFILEGET (80). |

- Messages from ignored players get the auto reply string "Your messages are ignored." (the string exists; the send condition was not traced).
- PM window titles: "Send Message" and "Read Message".
- Options window: 5 check boxes. Profile edit window: 10 fields.

## "Person action" is not a player menu
`TPersonAction` is the "Set Npc's Action" script editor used by the level editor. It has nothing to do with right-clicking a player. There is no per-player action form (trade, duel and so on) in the 2.05 client.

## Not found
- No right-click handler on a player sprite in the game world was found in 2.05.
