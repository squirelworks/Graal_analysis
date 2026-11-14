# Small Graal utilities (gap 9 of the tool coverage)

Date: 2026-11-14. Static reads of the copies we hold. apcalc and Guild Manager were packed; they were unpacked in an offline Windows lab VM (UPX for Guild Manager, a memory copy of the running process for apcalc). This
closes gap 9 of `tools-coverage-2026-11-14.md`. Only Graal Messenger has
anything a Seihai tool needs; the rest are recorded so they need no second look.

| Tool | What it is | Port |
|---|---|---|
| Graal Messenger (2012) | Stand-alone buddy list, PM and server browser for the 6.x login | Optional, low: a `seihai-rc` mode |
| Graal Sound Fix (2010) | Java one-button toggle of one client option | Not needed; one line in the launcher |
| Default characters and theme icon DLLs (1999) | Icon libraries | Not needed |
| apcalc | VB6 AP calculator (minutes to 100 AP and to healing) | Not needed |
| Guild Manager 1.4 (2003) | VB6 offline guild member-list editor | Not needed |
| guildcode / Guild Maker | The 1999 `.code` writer, already in `server-tools-2001.md` | Small: a `.code` reader and writer in seihai-core |
| START-HUB | A GS1 level, not a program | Not needed; a GS1 test fixture |

## Graal Messenger

`messenger.exe` (1,110,528 bytes, 2012-05-30) is a MinGW C++ program built
with GTK, boost 1.35 asio, zlib and bzip2. Class names: `Graal::list_client`,
`Graal::network::framework`, `Graal::messenger::{login, client, window,
buddy_list, server_list, server_browser, chat_dialog}`. It is a fan-made
client, so its packets show what the servers accepted, not what the official
client sends.

It opens two connections:

1. **Server list**: the public listserver on port 14922. Login packet 0
   carries the type byte 7, a key byte, then the version `G3D30123rc2`;
   packet 1 carries the account and password as length-prefixed strings. It
   shows the server list ("Server list recieved", a timeout message if none
   comes).
2. **Login server**: a hard-coded IPv4 address on port 14900. Login packet 0
   carries the type byte 5, a key byte and the version `G3D14097`, then the
   account and password, then an identity line
   `win,<a>,<b>,<c>,"Hi There!"` built from a fixed 48-character filler cut
   into three 16-character pieces. On connect it sends:
   - `GraalEngine,lister,options,globalpms=true,buddytracking=true,showbuddies=true`
   - `GraalEngine,lister,verifybuddies,1,-1`
   - `GraalEngine,pmservers,""`

   and from the buddy list `GraalEngine,lister,addbuddy,"<account>"` and
   `GraalEngine,lister,deletebuddy,"<account>"`, plus
   `GraalEngine,pmserverplayers,"<server>"` for the browser. Status lines:
   "requesting buddylist", "Buddy list recieved", "went online", "went
   offline", "You cannot send messages if the player is offline."

Settings are a plain `key = value` file (`nickname`, `password`,
`color_nickname`, `buddy_…`).

Why it matters: `client-internals/feature-specs/14-friends-ignore.md` still
lists the `addbuddy`/`deletebuddy` token layout as unseen. This client quotes
the account and sends `verifybuddies,1,-1` where 4.x sends a CRC; the
`options` line (`globalpms`, `buddytracking`, `showbuddies`) is new. These are
third-party evidence ([bin], fan client), not a capture of the official
client.

## Graal Sound Fix

`GraalSoundFix.jar` with its `Main.java` source (2010). It looks for
`game_config.txt` in `C:\Graal`, the two Program Files folders and four
folders under the user's home, then flips one line,
`tryloadsoundson64bit=true|false` (adding `=true` if absent). The button reads
"Change to 32-bit sound" or "Change to 64-bit sound". The key is a 5.x/6.x
Windows client option; if `seihai-launcher` ever edits a real client's
`game_config.txt`, this is the whole of it.

## Icon DLLs

`Graal Defaults Caracters Icons.dll` (95,232 bytes) and `GraalOnline Theme
Icons.dll` (14,592 bytes), both 1999-07-31 by Fuitad. 16-bit NE resource
libraries built with Borland tools: 29 icons (the 28 default characters, named
in a string table, plus the Graal icon) and 5 theme icons (signs, chests, the
"Graal - The Adventure" icon). No code.

## apcalc

`apcalc.exe` (17,408 bytes): a native-code VB6 program ("Project1", internal
name `apcalc`), packed with PECompact. It was unpacked by running it in an
offline lab VM and copying its image out of memory. It is an AP (alignment
point) calculator: type the current AP, press Enter, and it shows the minutes
until 100 AP and until the player may heal.

The rates it assumes, in seconds per AP point, by band:

| AP | Seconds per point | Range it prints |
|---|---|---|
| 0–19 | 30 | +/- 30 seconds |
| 20–39 | 90 | +/- 90 seconds |
| 40–59 | 300 | +/- 5 minutes |
| 60–79 | 600 | +/- 10 minutes |
| 80–99 | 1200 | +/- 20 minutes |

Time to 100 is `(band top − AP) × rate` plus the full bands above, so the
whole climb from 0 is 43,800 s. Healing needs 40 AP: below 40 it prints the
minutes to reach 40, from 40 up "Able to heal". It also has the messages
"Getting closer to saint status" and "Saint Status" for the top band and
"Please enter correct AP" for input it rejects (it compares against 0 and
100).

These are the same `aptime0..4` defaults (30/90/300/600/1200 s) as
`client-internals/feature-specs/04-death-respawn.md`, here from a player tool
of the time rather than a server. Nothing to port; the gserver owns AP.

## Guild Manager

`Guild Manager.exe` 1.4.0.4 (32,256 bytes; 548,864 unpacked with UPX in the lab
VM), native-code VB6, 2003, by its author. It edits a guild member list
offline: add (account name and nickname), remove, remove doubles, a member
count ("There are currently N member(s) in your guild."), open and save the
list as a `.txt` file, a default guild loaded on start, text colour, skins and
a tray icon. Settings go to `settings.ini` with `[Guild Settings]`
`GuildLoc`, `[Skin Settings]` `SkinLoc` and `[Color Settings]` `LabelColor`.
"LiveUpdate" downloads `guildmanager.zip` from the author's old GeoCities page
as `Update.zip` and asks the user to unzip it. The only separator constant is
`:`, used where account and nickname are joined, which fits the
`account:nickname` lines of a GServer guild file; that join was not traced
instruction by instruction. It does not talk to a server. Nothing to port.

## guildcode and Guild Maker

The guildcode set holds `Guildmaker1.1.exe` (1999-04), `Guildmaker.exe`
(1999-05) and four 48-byte `.code` samples. The Guild Maker set holds the same
`guildmaker.exe` (one header byte differs) with a fan readme. The format (two
DES-variant halves keyed `AXBORG15` and `VERGRAAL`) and the sample contents are
already in `server-tools-2001.md`. A Rust reader and writer would let Seihai
read the 1.x `guildname.code` and `reg.code`.

## START-HUB

A `GLEVNW01` level (2019) with 21 NPCs and 12 signs, plus the PNG and GIF
images they use. Each NPC gives a weapon or sets the player's look (`toweapons`,
`setplayerprop`, `sethead`, `setbody`); the signs explain them. It is an
offline starting room, not a launcher. It is useful as a GS1 sample for
`gs1-lint` and for the Seihai GS1 engine, nothing more.
