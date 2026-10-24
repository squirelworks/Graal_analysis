# 12 Server MOTD and rules

Snapshots read: Graal_analysis `8da6800`, Seihai `06aacfd`, GServer-v2 (`TPlayerLogin.cpp` `sendLoginClient`, `TServer.cpp` message load, `CWordFilter.cpp`, `TPlayerProps.cpp`), the lab server config.
Folded here from the public-server report: **PLO_STARTMESSAGE 41, PLO_RPGWINDOW 179**, and the empty `PLO_SERVERTEXT 82`.

## Packets (server to client, at the end of login) **[srv]**
| Id | Name | Payload | Versions |
|---:|---|---|---|
| 41 | STARTMESSAGE | the server message as one text string | 1.x-2.x; 2.05 has it (client form `TServerMessage`); newer 5/6 clients ignore it |
| 179 | RPGWINDOW | quoted, comma-separated lines: `"Welcome to <server name>.","<vendor> <app> programmed by <credits>."` | 2.1+ (in the 2.17/2.22 sets) |
| 82 | SERVERTEXT | empty at login; the server sends it "to allow serverwarp and some other things". Later it carries replies to `PLI_REQUESTTEXT`/`SENDTEXT` as `weapon,type,option,data` tokens | 2.1+ |
| 171 / 172 | BIGMAP / MINIMAP | see 06 | 2.1+ |
`sendLoginClient` order: level data (warp), bigmap, minimap, RPG window, start message, empty server text, flush.

### The message text (`TServer`) **[srv]**
Loaded from `config/servermessage.html`, then every `\r` is removed and every `\n` replaced by a space, so it is **one long line of HTML**. The lab file is the default HTML sample (head, style, a `div` with a welcome and a changelog block). The client is expected to render HTML or at least strip tags.

### "Rules" in GServer
`config/rules.txt` is the **word filter**, not a player-facing rules text. Syntax: optional `WARNMESSAGE`, `SHOWWORDSTORC`, then `RULE` ... `RULEEND` blocks with `CHECK` (pm, chat, nick, toall), `MATCH` (`?` wildcard), `PRECISION` (number or percent), `WORDPOSITION` (full, start, part), `ACTION` (log, tellrc, replace, warn, jail, ban) and an optional per-rule `WARNMESSAGE`. `CWordFilter::apply` runs on chat (prop 12), PM (`msgPLI_PRIVATEMESSAGE`), toall, and nickname changes. `replace` swaps matched letters for `*`; `warn` replaces the whole message with the warn text; `log`/`tellrc` go to server log and RC; **`jail` and `ban` are stubs and do nothing**. For chat, if the text was changed the server echoes the new CURCHAT to the sender so the client's own bubble shows the censored text.
Real "rules" a player sees come from the server message, the RPG window and NPCs.

## Seihai today
- 41, 179 and 82 are counted as unhandled. Chat text arrives and displays; a censored echo from the server is just another prop update.

## Steps for Claude
1. Handle PLO 41: store the raw text in `SessionState.start_message`.
2. Small HTML reducer: drop `<style>`, `<script>` and comments blocks, convert `<br>`/`</p>`/`</div>` to newlines, strip other tags, decode a few entities, and wrap to the chat width. Show it in the existing panel (`ui::draw_panel`) once after login, dismissed with Enter/Esc. Unit test with the lab `servermessage.html`.
3. Handle PLO 179: parse the quoted list and print the lines to the chat log.
4. Handle 82 with empty payload as a no-op marker (`server_text_ready = true`); log non-empty payloads for later use (14).
5. Offer a `--no-motd` flag for scripts and tests.
6. No filter logic is needed in the client.

## How to test
- Lab: edit a **copy** of `servermessage.html`, restart the lab gserver, log in with Seihai, and assert `start_message` equals the file with newlines folded. Add a rule in `rules.txt` (`RULE` with `CHECK chat`, `MATCH`, `ACTION replace`), send a chat line, and check the CURCHAT echo contains `*`.
- Replay frames from the public report only as structure checks; the report notes all four public servers sent 41 and 179.

## NEEDS
nothing blocking. Optional: "the 2.05 start-message handler" (does it show the HTML in `TServerMessage` immediately or only on request).
