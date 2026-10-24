# 13 Ban and kick handling

Snapshots read: Graal_analysis `8da6800` (`protocol/gserv-1999.md`, `packet-ids.md`), Seihai `06aacfd` (`protocol/dispatch.rs`, `net/mod.rs`), GServer-v2 (`TPlayer.cpp` login and cleanup, `TPlayerLogin.cpp` `sendLogin`, `TPlayerRC.cpp`, `TServer.cpp` `isIpBanned`, `TServerList.cpp`).

## What it is
Every refusal, kick and ban reaches the client as **`PLO_DISCMESSAGE` (16)**: rest = text, `\r` = line break. The server then closes the socket (or the client does). Seihai already parses 16 into `disconnect_reason`.

## Exact server behaviour (messages, in the order they can happen) **[srv]**
`TPlayer::msgPLI_LOGIN` (steps 1-4), then listserver verification (`TServerList`), then `TPlayer::sendLogin` (steps 5-8):
1. Player limit (`maxplayers`): "This server has reached its player limit."
2. IP ban (`TServer::isIpBanned`, wildcard match against `config/ipbans.txt`, skipped for staff with the modify-staff right): "You have been banned from this server."
3. Client version not in `allowedversions.txt` (ranges `a:b` allowed): "Your client version is not allowed on this server." plus a line with the allowed list.
4. Listserver down: "The login server is offline.  Try again later." Listserver rejected the login: the listserver's own text (for example wrong password), then disconnect.
5. Account banned (`BANNED 1` in the account file, not for staff): "You have been banned.  Reason: <BANREASON>" (newlines become `\r`).
6. `onlystaff`: "This server is currently restricted to staff only." IP not in the account's `IPRANGE`: "Your IP doesn't match one of the allowed IPs for this account."
7. Account already online: if the old session was idle for 30 s or more, the old one gets "Someone else has logged into your account." and is dropped; otherwise the new login gets "Account is already in use." (the check is case-insensitive).
8. No start level: "No level available."
While connected:
- Idle: `disconnectifnotmoved` with `maxnomovement` seconds: "You have been disconnected due to inactivity."
- More than 5 unknown packet ids (`msgPLI_NULL`), or garbled props: "Disconnected for sending invalid packets."
- RC kick (`msgPLI_RC_DISCONNECTPLAYER`): "One of the server administrators, <name>, has disconnected you" plus " for the following reason: <reason>" if given.
- RC ban by account (`msgPLI_RC_ACCOUNTSET` and `msgPLI_RC_PLAYERBANSET`): "<name> has banned you.  Reason: <reason>" and the account's `BANNED`, `BANREASON` are saved.
- RC account reset: "Your account was reset by <name>".
- `PLO_UPGRADEURL` (169) can accompany a disconnect to turn Reconnect into an Upgrade button (2.14+).
The word filter's `ban` action is not implemented (12).

## Seihai today
- `SessionState.disconnect_reason` is filled; the CLI prints it. No classification, no UI, no retry policy. The public-server run saw clean logins only, so no refusal text has been captured from a public server.

## Steps for Claude
1. Add `enum DisconnectKind { PlayerLimit, IpBanned, VersionNotAllowed, LoginServerOffline, ListserverRejected(String), AccountBanned(String), StaffOnly, IpMismatch, InUse, KickedByStaff, Inactivity, InvalidPackets, Other }` and `classify(&str) -> DisconnectKind` (match on the phrase starts above, case-insensitive; keep the raw text).
2. Show the reason in the launcher/GUI on exit with the raw text and a hint per kind (for example VersionNotAllowed shows the allowed list; InUse says wait 30 s).
3. Retry policy: never auto-reconnect after a ban, version, staff-only, IP mismatch or invalid packets; allow a manual retry for InUse, player limit, offline login server.
4. Keep the invalid-packet guard from 02/08: assert in tests that no frame Seihai sends has an id outside the profile's `pli` set.
5. Record the reason in the exit code of the CLI (nonzero, distinct per kind) for lab scripts.

## How to test
- Lab (private display :9): set `maxplayers = 1` on a **copy** of the lab options and log in twice; put the placeholder account's `BANNED 1` and `BANREASON test` into a copy of the account file; add the loopback address to `config/ipbans.txt` copy; use an unlisted version string; log in the same account from two sessions; stop the listserver stub. Check the exact text and `classify`.
- Unit tests feeding each phrase to `classify`.
- No public server contact.

## NEEDS
nothing. (The text of refusals from the real listserver for a banned or unknown account is not in the captures; capture it only if the user approves a public login.)
