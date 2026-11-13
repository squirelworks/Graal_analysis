# A live Login session, observed (6.03r7 Windows, community Login server)

Date: 2026-11-13. Evidence: `LOGIN-CAPTURE-247-20261113` in `docs/evidence-index.tsv`. The pcap, the decoded frame log, the screenshots, the account, the host names and the verbatim script text are owner-held and not in this repo. Approved by the owner in writing for GitHub issue #247 (one run, read-only, with an account the owner typed in by hand).

**Scope.** This shows how a live community Login server behaves with an unmodified Windows 6.03r7 client. It does not show what the official Login server sends. Matrix unknown #3 stays open for the official look. **[cap]**

## Setup

- **Client:** the original packed Windows 6.03r7 `Graal.exe`, unmodified. A fresh folder with no `updatepackages/`. The Wine memory dump of the same build crashes at start on Windows and was not used.
- **Machine:** a throwaway clone of the Windows 10 lab VM with a new virtual NIC. The guest clock was held at a date just after the build's link date; the client faults at start with the clock set before its link date.
- **Server:** a community-run GS2Emu (OpenGraal) game server named `Login`, on `<login-host>`. The client's compiled-in Login names were pointed at it with the guest's hosts file. On port 14900 that host closes the connection right after the client's login packet, without sending anything; the `Login` entry on its server list uses a different port, and a plain TCP relay inside the guest bridged 14900 to it. Nothing rewrote the traffic.
- **Capture:** a host-side trace of the VM's NIC, decoded offline with the gen-5 cipher. The client's own `game_console.log`. Screenshots.

## Login packet (Câ†’S, before any frame)

- Type 5 (gen 5), then the key byte, then the 8-byte token. **The Windows 6.03r7 sends `G3D0311C`**, not the `G3D0511C` of the Linux 6.03r7. **[cap]**
- Account and password as length-prefixed strings. The client sends a login packet the moment it starts, before the login screen exists: its account field then holds a placeholder default. The second login, after the user fills in the screen, carries the real account. **[cap]**
- After the password: `win`, an empty quoted string, two 32-hex-digit machine hashes, and the quoted OS version (`"6.2 9200 "` on Windows 10 under compatibility reporting). **[cap]** The hash values are owner-held.

## Order of the session

1. **First connection (no account typed yet).** The client asks for `basepackage.gupd` (Câ†’S 23, sent twice) and its language (Câ†’S 37 `en`). The server answers with 28 (`serverr.server=login`), weapon adds (33/197), 179 with two welcome lines, then the package and file traffic (100/102, 105/106, 30 for missing files), 19 script weapons as Sâ†’C 140 bytecode, and the level packets. **[cap]**
2. **The login screen is a scripted GUI** served by that session. Fields: nickname (prefilled `unknown`), account (a drop-down), password with a "save password" box, and language. Buttons: Options, Guest, Start, and "Become a Member". The backdrop is a full-window image with the server's logo; it is not a level. **[cap]**
3. **Pressing Start closes the connection and opens a new one** with a new login packet carrying the typed account and password. The cached Login packages are then checked with Câ†’S 47 (not 23), and the server answers 45 for up-to-date files. **[cap]**
4. **The server list.** The server-list weapon asks the server through script messages (Câ†’S 152/154, answered by Sâ†’C 82): `subscriptions`, `getlockcomputer`, `simplelist`, `serverinfo`, `upgradeinfo`, and `packageinfo` for `login.gupd`. The list reply is one comma line, one entry per server: name, a quoted type-prefixed display name, and a player count. The client then asks for one icon per server (`login_icon_<name with spaces as underscores>.png`); missing icons get Sâ†’C 30. A `login_servermap_.png` is also requested. **[cap]**
5. **Picking a server.** Selecting a server sends three script queries for that server's info and events, then **Câ†’S 41 with the server name**. The server answers **Sâ†’C 178**: `"<name>","<type-prefixed name>",<host>,<port>`. The client closes the Login session and logs in to that host. This matches the 178 layout in `login-session-known.md`. **[cap]**

Sâ†’C 190 arrives once in each session **with an empty body**. **[cap]**

## What the Login server sends besides the GUI

- **Backdrop level `black.nw`:** every tile is the same tile, with no chests and no NPCs of its own. Its level packets include, in this order, 14 (`black.nw` with its prefix), 6, 101 (the 8192-byte board), 39, 0, 10, 156 and 3. **[cap]**
- **Sâ†’C 41** carries a small HTML welcome page, **Sâ†’C 47** the staff rank names, and **Sâ†’C 180** the status list (`Online, Away, DND, Eating, Hiding, No PMs, RPing, Sparring, PKing`). **[cap]**
- The NPC-server player is announced with Sâ†’C 8. **[cap]**
- The script weapons cover the login screen, a shared function pack, an IRC-style chat bridge, a loading screen for the 3D login steps, patch scripts for the server list and an "Adventure" offline-mode hook. Two weapons call functions that this 6.03r7 engine lacks (`destroyObject` in a shared helper, `drawimage` on a GUI icon) and log a script error. The login screen still works. **[cap]**

## Packages

- `basepackage.gupd`: `GRPKG001`, `NAME Login Packages`, `VERSION 3.00`, `PLATFORM any`, one `SUBPACKAGE login.gupd`, `USECHECKSUM false`, `PROTECTOVERWRITE true`, `FLAG popupforoptionalpackages=true`. It lists no `FILE` lines. **[cap]**
- `login.gupd` (`Graal Assets`, 3.01) has a download-menu description and five subpackages: `levels.gupd`, `sounds.gupd`, `videocompression.gupd`, `fonts.gupd`, `images.gupd`. **[cap]**
- `videocompression.gupd` is `PLATFORM win` and lists the three FFmpeg DLLs. `fonts.gupd` (`MODE required`, `USECHECKSUM true`) lists `arial.ttf`, `tempsitcbd.ttf` and `open sans.ttf`. `levels.gupd` ("Levels and Graphics", 1.16) is 241 lines: ganis, heads, bodies, sprites, emoticons and a `main.gmap`. **[cap]**
- On the first run the client downloads the whole asset set (about 300 files, including a 2.5 MB sound bank and a 2.4 MB backdrop image) before the login screen is usable, with a "Download Progress" window on top. **[cap]**

## Not covered

- The official Login server's bytes, script and look (matrix unknown #3).
- Account screens beyond the login form: the run stopped when the client warped to a game server.
- The 6.11 connector path.
