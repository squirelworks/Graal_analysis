# 1st Graal (Sept 1998 Delphi beta): protocol summary (derived)

Checked against `relay-1998.md` and `early-clients.md`.

## Connection and login
- Default relay host the loopback address, port **14801**, through the event-driven socket component (matches the existing notes).
- No login token, no account, no password, no compression, no cipher. Lines are text ending in a newline; first character is the command.
- Join line: `N<game>#def`. The client always sends the name `def` and sends the real nickname later in a `D` payload.

## Game (room) name: new detail
- The constant `Zelda2` is only used in one branch. In the other branch (selected by an argument given when the network client object is created) the client builds the room name from the current level file's base name: `Z` + base + `2`, for example a level `level1.zelda` would give a room `Zlevel12`. Right after that it runs a follow-up routine (not traced).
- Which branch is used for normal play was not traced. The two-client local mode (two client objects exist) is a likely user of the difference.
- The existing note says every 1st/2nd Graal join uses the constant `Zelda2`. That is true for one branch only.

## D payload types received
The receive handler has cases for A B C D E F G H L M N O P R S T W (17 letters). That agrees with the existing note, which lists 16 sent types plus a receivable `D`. No other types.

## Other confirmed facts
- Save files start with the marker `Graalsav1`.
- Level files use `.zelda` heavily and `.graal` in a few places; some built-in level names are tested by hard-coded comparisons (cave, house, village, level numbers).
- Web levels: the client has an HTTP check for "http" in a level path.

## Not covered
Lobby line handling beyond I / + / - / D (P and C were not re-read), and feature behaviour (combat, items).
