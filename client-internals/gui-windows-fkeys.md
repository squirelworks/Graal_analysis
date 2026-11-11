# Function-key windows and the server message window (1st Graal to 2.31)

## Scope and evidence

This note covers every window a Windows Graal client opens from F1 to F12, and the window that shows the server message (`PLO_STARTMESSAGE`, 41). It replaces the scattered key lists in the per-version notes, which were copied from one build to the next and missed several changes.

`[bin]` The static read covers 33 Windows builds: 1st to 15th Graal, 1.1 and 1.1.9, 1.28 beta 2, 1.3 beta, 1.31 to 1.39, 1.41 rev1, NewMain 24 and 26, 2.0 to 2.05 rev2 (all revisions), the 2.1 test2 and test3 builds, NewWorld beta 1 and 2, 2.17, 2.22 and 2.31. For each build the forms were decoded from the executable's form resources, the key handler of the main game form was read, and the windows it opens were matched to their forms through the class table. Graal3D was read for comparison only.

`[lab]` Evidence ID `FKEY-WINDOWS-139-20261111`. 1.39 was run offline in a Windows 10 guest against the lab gserver (`seihai-gserver-v2` 4.0.0-seihai.1, commit `576c9543`), world `classic` on the loopback address, port 14803. Keys were sent to the guest console; 37 screenshots and a key log were kept by the owner. 2.05 rev2 and 2.22 could not be run in that guest; see [Open](#open).

Key names below are the Windows virtual keys. "Online" means connected to a game server.

## The key handler by family

`[bin]` Every build handles function keys in the main game form's key-down handler. F11 and F12 have no handler in any build, and F9 is handled only by the NewWorld betas. Esc and Alt+Enter (fullscreen) are in every build.

### 1st to 5th Graal (1998)

| Key | Window or action |
| --- | --- |
| F1 | Options window (caption "Options"). A "Save games" group with Load game (F2) and Save game (F3), and a "Level editing" group with the current level name, Edit level (F4) and Load level (F5). 5th Graal adds a More button. |
| F2 | load a save game through a file dialog (1st Graal: `Graalsav1` header) |
| F3 | save the game (1st Graal: `.save` file) |
| F4 | open the built-in level editor |
| F5 | the Load level window |
| Esc | quits at once, no prompt |

### 6th Graal to 1.1.9

`[bin]` The same five keys, but the handler is a jump table that maps F6 to F10 onto F1 to F5, so F6 also opens Options and F10 also opens Load level.

- 9th Graal (not the 9th alpha) adds the Esc prompt "Do you really want to quit Graal?".
- 15th Graal and 1.1 add More options and Controls buttons to F1.
- 1.1.9 ignores F4 and F5 while the editor is open or the reconnect window is showing.
- The string "When you load a level you will be disconnected" is present from 9th Graal on; its online-editor counterpart arrives in 1.28 beta 2.

### 1.28 beta 2 to 1.39

`[bin]` The aliases are gone and F6 and F7 arrive.

| Key | Window or action |
| --- | --- |
| F1 | Options, same groups as before, now with `&` accelerators |
| F2 | load a save game (file dialog) |
| F3 | save the game; offline only (1.34 writes `.gsave`) |
| F4 | the editor; online it shows "You cannot open the editor in the online mode." |
| F5 | Load level; online it asks first, because loading a level disconnects |
| F6 | the script debugger (`TDebuggerFrame`). From 1.32 it opens only offline, or when the server address is the loopback address; 1.28 beta 2, 1.3 beta and 1.31 have no check. |
| F7 | the player list. In fullscreen it is docked to the top right (x = 640 minus its width). |
| Alt+1 to Alt+9 | screenshot, minimap, bytes counter and the other Alt functions (→ [versions-133-139.md](versions-133-139.md)) |

F4 and F5 are ignored while the reconnect window is showing.

`[lab]` 1.39 online against the lab server, windowed:

| Key | Seen |
| --- | --- |
| F1 | window titled "Options": Load game (F2), Save game (F3), Edit level (F4), Load level (F5), More options, Controls, Close |
| F2 | a "Load save game" file dialog |
| F3 | "You cannot save in online mode…" |
| F4 | "You cannot open the editor in the online mode." |
| F5 | OK/Cancel "When you load a level you will be disconnected from the server. Continue?"; Cancel stays online |
| F6 | the server was the loopback address, so the debugger check passed; the client closed within a second each time (three times), with no dialog, and the server logged a disconnect |
| F7 | the "Playerlist" window at the top left, showing `--- 0 online ---` |
| F8, F9, F10, F11, F12 | nothing |
| Esc | "Do you really want to quit Graal?" |

`[inf]` The F6 exit is not explained yet. The debugger is meant for offline play, and the online path may not expect it.

### 1.41 rev1

`[bin]` The F1 window's caption becomes "Help". It keeps the save-game buttons and adds Debugger (F6), Playerlist (F7), General options and Controls. F8 arrives: it opens the server list (below).

### NewMain 24 and 26, 2.0 to 2.05 rev2

`[bin]` Save games are gone; the client holds the string "Save games are not supported anymore", and F2 and F3 do nothing.

| Key | Window or action |
| --- | --- |
| F1 | "Help": current level, Edit level (F4), Load level (F5), Debugger (F6), Playerlist (F7), ServerList (F8), General options (opens `TMoreOptions`, "More Options"), Controls (opens `TControlsFrame`, "Change Controls"), Close |
| F4 | the editor; online the same warning as 1.39 |
| F5 | Load level (`TLoadLevel`); online it asks first |
| F6 | the debugger; offline or loopback server only |
| F7 | the player list; top right in fullscreen |
| F8 | the server list window (`TServerListFrame`, below) |
| F10 | from 2.02 (not 2.0 or 2.01): toggles the window border between sizeable and none |
| Esc | asks to quit, except while certain modal states are active |

### 2.1 test2 and test3

`[bin]` The F1 window is redesigned. A "Game windows" group holds Edit Level, Load Level, Debugger, Player List, Server List and General Options, under the text "With the function keys F4 - F8 you can open several windows…", which points to `readme.txt`. The keys themselves are as in 2.05, and F10 is still there.

### NewWorld beta 1 and 2

`[bin]` As 2.02, plus F9, which works offline only. Each press moves the game clock on one hour: hour 0 to 23, then day 0 to 27, month 0 to 9, then the year. The new hour is shown as the player's own chat text for 60 ticks.

### 2.17, 2.22 and 2.31

`[bin]` The key-down handler keeps only Esc and F10. Every other function key goes to a separate dispatcher.

| Key | Window or action | 2.17 | 2.22 | 2.31 |
| --- | --- | :---: | :---: | :---: |
| F1 | Options/Help window | yes | yes | yes |
| F2 | shows the RPG window (`TRPGFrame`), if the server has created it with `PLO_RPGWINDOW` (179) | yes | yes | yes |
| F4 | the editor | yes | yes | no |
| F5 | Load level, with the current level and position filled in | yes | yes | yes |
| F6 | the debugger | yes | yes | no |
| F7 | the player list | yes | yes | yes |
| F8 | online only: raises a flag that the server-list thread polls; when it sees the flag it clears it and shows the server list window. The F1 window's Server list button and the reconnect window's hide handler raise the same flag. | yes | yes | yes |
| F10 | window border toggle | yes | yes | yes |

`[bin][cap]` In 2.31 the F1 window's form still has Edit level and Debugger, but they are hidden at run time (→ [2.22-2.31.md](../version-profiles/2.22-2.31.md)).

### Graal3D

`[bin]` For comparison only: F1 opens the hardware options and F2 the player look window.

## The server list window (F8, 1.41 to 2.05)

`[bin]` F8 shows `TServerListFrame`. Its caption names the list host followed by "Server List"; the host is written here as `<listserver-host>`. The account and password fields default to `guest`.

If no list connection exists yet, F8 creates one. The host name is decoded at run time from a hidden string, and the port is 14921. The client sends its version token with id 0. While it waits, the short-message window (`TShortMessage`) shows "Graal Server List" with "Connecting to server ..." and then "Getting server list ...".

## The server message window

### What sends it

`[srv]` GServer-v2 sends `PLO_STARTMESSAGE` (41) at the end of login, after the RPG window (179). The text is `config/servermessage.html` folded onto one line (→ [12-motd-rules.md](feature-specs/12-motd-rules.md)).

### 1.32 to 1.39: `TRTFMessage`

`[bin]` The form is `TRTFMessage`, captioned "Server message". It is a stay-on-top window with a rich-edit box and a Close button (1.32 uses a dialog border). 1.39 adds Save, which offers RTF and TXT.

- 1.32 and 1.33: the handler trims the text, loads it into the rich-edit box as rich text, and always shows the window. HTML is not RTF, so it shows as raw text.
- 1.39: the handler first compares the text with `servermessage.rtf` in the game folder. If they are the same, nothing is shown. Otherwise it saves the new text to that file, sets the caption, loads the text and shows the window.

`[lab]` 1.39 against the lab server:

| Case | Seen |
| --- | --- |
| HTML message | a window titled "Server Message" with the raw HTML text, Save and Close; `servermessage.rtf` written next to the executable |
| Save | a "Save text" dialog offering RTF (`*.rtf`), Text (`*.txt`) and All files |
| Close or Esc | closes the window |
| same message at the next login | no window, and the file is not rewritten |
| one character changed | the window opens again |
| RTF message (`{\rtf1 …}`) | drawn as rich text (bold, italic, line break); `servermessage.rtf` holds the RTF |
| the game behind it | shows its Continue/End menu whenever the message window opens |

`[bin]` 1.39 reuses the same form as the private-message History window. Lines from the player are prefixed "You:" in purple, lines from the other player "Opposite:" in red, and the caption comes from the "&History" menu text.

### 1.41 rev1 to 2.31: `TServerMessage`

`[bin]` From 1.41 rev1 the form is `TServerMessage`. Its form resource holds Close, Save, five flat speed buttons and a label. When the form is created it builds a read-only rich-edit box at run time (436 × 362, filling the window). The logic is the same in 1.41 rev1, NewMain 24, every 2.0x build, the 2.1 test3, 2.17, 2.22 and 2.31.

When 41 arrives:

1. The text is trimmed. If it starts with `{\rtf1` it is RTF; otherwise it is treated as HTML.
2. The file is `servermessage.rtf` or `servermessage.html` in the game folder. If that file exists and holds exactly the same text, nothing is shown and nothing is written. Otherwise the text is written to it.
3. RTF: loaded into the rich-edit box and shown. Save offers RTF and TXT.
4. HTML: the rich-edit box is hidden, and an embedded web browser control is created on first use. The form is shown, the browser goes to `about:blank`, the client waits until the page is ready, and then it writes the message lines into the document. Save offers HTML.

The speed buttons drive the browser:

| Button | Action | At start |
| --- | --- | --- |
| 1 | Back | disabled |
| 2 | Forward | disabled |
| 3 | Stop | disabled |
| 4 | Refresh | enabled |
| 5 | go to a stored address | enabled |

The browser's command-state events turn Back and Forward on and off as history allows. Its download-begin and download-complete events turn Stop on and off. When the page title changes, the window caption follows it, unless the page is `about:blank`. `[bin]` No handler opens links in an outside browser, so a clicked link loads inside the window.

`[bin]` Esc or Close hides the window. The caption and Close text come from the language file, keys `RTFMessage` and `RTFMessage-CloseButton`.

`[bin]` Nothing else opens the server message: the 41 handler is the only caller of the routines that show it, and there is no menu item or key for it. Because of step 2, a player sees a server's message once per change.

### The same form as the PM History window (2.05, 2.1 tests)

`[bin]` The player list's History item and the message editor's History button both open `TServerMessage` in rich-text mode. The client reads the stored conversation with that player and writes it out in pairs of lines: a header line, then the message. A header starting "You:" is drawn in purple with the player's own name; one starting "Opposite:" is drawn in red with the other player's name; anything else is drawn in red as "unknown:". Message lines are indented. The caption is the History menu text without its `&`, followed by the other player's name.

## Open

- [ ] 2.05 rev2 and 2.22 live: both need their list host to resolve to the loopback address inside the Windows guest, which takes an administrator edit of the guest's hosts file. The clients are staged in the guest.
- [ ] Why 1.39 closes on F6 when the server is the loopback address.
- [ ] Whether the 2.17 to 2.31 F2 does anything before the server has sent 179.
