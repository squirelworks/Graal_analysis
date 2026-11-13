# Graal 1.25 and 1.27 (Aug and Oct–Nov 1999): the first binaries of the two missing GSERV builds

Date: 2026-11-13. Static read of two owner-held InstallShield 3 installers that no earlier note covers. Evidence ID
`CLIENT-HUNT-20261113` ([evidence index](../docs/evidence-index.tsv)). No build was run and no lab login has been done.
Every finding is **[bin]** (read from the executables) unless it is tagged **[doc]** (the release notes shipped in the same
package) or **[inf]**.

Until now 1.25 and 1.27 were "L only" in the [token catalogue](version-token-catalogue.md): their tokens came from a
server-side table, with no client executable in any collection.

## How the executables were taken out

Both installers are a self-extracting zip that holds an InstallShield 3 disk set (`SETUP.EXE`, `_SETUP.LIB`, `_SETUP.1`,
`SETUP.INS`). The game files are inside the `_SETUP.1` archive, compressed with the PKWARE Data Compression Library.
They were unpacked statically with [`tools/is3-extract`](../tools/is3-extract/README.md); no installer was run.
Every file came out at the size its directory entry records. As a check, the same tool unpacks the 1.21 installer to a
`Graal.exe`, `GServer.exe` and `remotecontrol.exe` with the MD5s that [`build-catalogue.md`](build-catalogue.md) gives for
1.21, which were taken from an installed copy.

| | 1.25 | 1.27 |
|---|---|---|
| Installer title | "Graal v1.2.5 - The adventure" | "Graal - The adventure (V. 1.2.7)" |
| Disk set built | 1999-08-07 | 1999-11-27 |
| Files in `_SETUP.1` | 290 in 12 groups | 582 in 12 groups |
| `Graal.exe` size | 999,936 | 1,065,472 |
| `Graal.exe` stored date | not usable (the 1.21 and 1.25 packages store 1997 dates) | 1999-10-23 |
| Also ships | `GServer.exe`, `remotecontrol.exe` | `GServer.exe`, `remotecontrol.exe`, Graal Character Designer and Graal Clock (two community tools, Nov 1999) |

The PE link stamps are Delphi's fixed value and say nothing. Like 1.21, neither exe has a VERSIONINFO resource.
Both packages also ship a sample `accounts.txt` for the bundled server; it was not read further and is not reproduced.

## Identity

| | 1.21 (known) | 1.25 | 1.27 | 1.28 beta 2 (known) |
|---|---|---|---|---|
| Login token | `GSERV007` | **`GSERV009`** | **`GSERV011`** | `GSERV013` |
| Default server | `<list-host-classic>`:14804 | same | same | same |
| GS1 commands (`table` scan) | 71 | **80** | **84** | 84 |
| Server messages handled | 0–29, 31–34, 100 (35) | **0–38, 100 (40)** | **0–38, 100 (40)** | 0–38, 100 (40) |
| Receive dispatcher bound | `0x64` | `0x64` | `0x64` | `0x64` |
| Save magics | reads Graalsav9/Graalsv10/Graalsv11, writes Graalsv11 | same strings, same arrangement | same | same |
| `nodecompressionerror` config key | no | no | **yes** | yes |
| UDP (`bind`/`sendto`/`recvfrom` imported) | no | no | **no** | yes |
| Delphi 4 RTL (`TMultiReadExclusiveWriteSynchronizer`) | no | no | **no** | yes |

The token was read as a string literal next to the default port, the same place 1.21 and 1.28 beta 2 keep it. The
command count is from [`tools/gs1-table-scan`](../tools/gs1-table-scan/README.md) in `table` mode, and the handled-message
list is the method of [`plo-handled-ids-by-build.tsv`](../version-profiles/plo-handled-ids-by-build.tsv). Both methods
reproduce the 1.21 and 1.28 beta 2 rows exactly, so the two new rows are comparable with them.

## What the two builds settle

1. **`GSERV009` and `GSERV011` are now [bin].** The gs2lib list's 1.25 → `GSERV009` and 1.27 → `GSERV011` both hold. The
   client token went 007 (1.21), 009 (1.25), 011 (1.27), 013 (1.28 beta 2). Of the numbers in between, 010 is the 1.25
   RemoteControl (see 3). 008 and 012 have no binary yet; the 1.22–1.24 and 1.26 releases are the likely owners **[inf]**.
2. **The 13 GS1 commands credited to 1.28 beta 2 are older.** The [GS1 note](../npc-library/gs1-commands-by-version.md) could
   only say "new in 1.28 beta 2". They split across the two new builds, and the release notes agree **[bin][doc]**:

   | First seen in | Commands | Release notes |
   |---|---|---|
   | 1.25 (Aug 1999) | `sleep`, `while`, `hideplayer`, `timereverywhere`, `setminimap`, `setmap`, `showcharacter`, `setplayerprop`, `setcharprop` | `setmap`/`setminimap` in 1.23; `showcharacter`/`setcharprop` in 1.25 |
   | 1.27 (Oct 1999) | `showfile`, `setstring`, `setbackpal`, `setletters` | `showfile` in 1.26 rev 2; the other three in 1.27 |

   1.27's command table is identical to 1.28 beta 2's, entry for entry. 1.27 is also the first build whose table has the
   entry `hurt ` with a trailing space (taking an argument) in place of `hurt`. The scan normalises both to `hurt`.
3. **"RemoteControl 1.28" is the 1.27 RemoteControl.** The `remotecontrol.exe` in the 1.27 package is byte-identical to
   the `RemoteControl1.28.exe` shipped with 1.28 beta 2 (dated 1999-10-20, token `GSERV011`). The 1.25 package's
   RemoteControl is a different build that sends **`GSERV010`**, which confirms the 1.25 row of
   [`rc-list-online.md`](../protocol/rc-list-online.md). So 1.27 is the first release where the client and the RemoteControl
   share a token.
4. **The 1999-10-20 GServer is the 1.27 server.** The 1.27 package's `GServer.exe` is byte-identical to the standalone
   "GServer with RC, 1999-10-20" found in the same hunt, so that build needs no separate identification.
5. **Server messages 35–38 arrived by 1.25.** 1.21 handles 0–34 except 30; 1.25 already handles 0–38 and 100, the same set
   as 1.27 and 1.28 beta 2. The new range is still unnamed (see [`gserv-1999.md`](../protocol/gserv-1999.md#open-questions)).
6. **Two features move earlier or later.**
   - `nodecompressionerror=` (hide the inflate error) first appears in 1.27, not 1.28 beta 2. The 1.27 notes list it as the
     new "don't show decompression errors" option in Graal → F1 → More **[bin][doc]**.
   - UDP "direct data packages" are still absent in 1.27, so 1.28 beta 2 stays the first UDP build.
7. **The compiler change narrows to Oct–Nov 1999.** 1.25 and 1.27 use the older Delphi RTL layout, like 1.21, so the
   switch to Delphi 4 happened between 1.27 (1999-10-23) and 1.28 beta 2 (1999-11-23).
8. **Graal Clock is an offline launcher, not a network tool.** The 1.27 package's Graal Clock (version 1.0, Delphi, by the
   Graal Character Designer's author) imports no socket library. It shows the time, keeps its settings in `GraalClock.ini`,
   finds the client in a few common install folders (or asks for it), and has buttons to start `Graal.exe`, open the
   readme and the Character Designer, and load or save `.chr`/`.chi` character files to the client's character list. Its
   only outside link is a browser opened over DDE **[bin]**.

## The bundled GServers

| Package | Tokens on the server's list | Refusal text for an older client |
|---|---|---|
| 1.21 (known) | `GSERV007` | "You need Graal version 1.2 rev1 to play on this server." |
| 1.25 | `GSERV007`–`GSERV010` | "You need Graal version 1.2 rev1 to play on this server." |
| 1.27 | `GSERV007`–`GSERV011` | "You need at least Graal version 1.27 to play on this server." |
| 1.28 beta 2 (known) | `GSERV007`–`GSERV013` | "You need at least Graal version 1.28beta2 to play on this server." |

The login checks were read from both servers' code **[bin]**:

- **1.25** has no version number on the connection yet. A player is let in only if its token is exactly `GSERV007`,
  `GSERV008` or `GSERV009`, so 1.21 clients still get in and anything else gets the 1.21 refusal text as message 16. A
  RemoteControl must send `GSERV009` or `GSERV010`. Any other token closes the RemoteControl login without a message.
- **1.27** turns `GSERV007`–`GSERV011` into the numbers 7–11 and stores it on the connection, as 1.28 beta 2 does.
  Players need 11 (`GSERV011`, the 1.27 client), and anything lower gets the 1.27 refusal text. RemoteControl needs 9 or
  more, so the 1.25 RemoteControl (`GSERV010`) can still log in to the 1.27 server. The RemoteControl path also tests two
  account fields before letting it in. One is most likely the 1.26 "blocked" account option **[inf]**. Both carry the "GServer2 (C) Stefan
Knorr" banner and the "execution file is corrupted" self-check that the 1.28 server has.

## Release notes in the packages **[doc]**

The 1.25 readme covers 1.2 beta 7 to 1.25. The 1.27 readme covers 1.26, 1.26 rev 2 and 1.27. Points that bear on behaviour
or protocol:

- **1.23:** accounts shown as a tree, a "no rights" account level, the F7 player list, and the server only pushes a hit
  player instead of setting its x/y.
- **1.24:** message codes in `message` and the new `strequals(str1,str2)` flag; `seturllevel` disabled online; `isleader`
  works offline.
- **1.25:** player-looking NPC characters (`showcharacter`, `dir`, `sprite`, `setcharprop`); message codes usable in most
  commands; the guild system (a `(guild)` suffix on the nickname, checked by the server against `guild<name>.txt`).
- **1.26 / 1.26 rev 2:** a "blocked" account option; actionflags and chests saved by the server; death costs 1000 rupees;
  lava tiles (a half heart every 5 seconds) and snow tiles; `showfile`; the "npc animator" timeout rule (timeouts of a level's
  NPCs stay with the first player on the level).
- **1.27:** English and German language files; `onwall` sees NPC characters; guild members do not hurt each other with
  swords or NPC weapons; `setstring`, `strcontains`, `#s(var)`, `strtofloat`; a `created` flag; `setbackpal`, `setletters`;
  `save[0]`–`save[9]` NPC variables that are sent to the server and other players; `hurtdx`/`hurtdy` from `hitplayer` on
  character NPCs; jailed players cannot send toall or private messages.

## Open

- [ ] Player, NPC and baddy prop ranges for 1.25 and 1.27 (the [`gserv-1999.md`](../protocol/gserv-1999.md#props-by-build)
  table has 1.21 and 1.28 beta 2 only). 1.27's `save[0]`–`save[9]` NPC variables should show up as new NPC props.
- [ ] Names for server messages 35–38.
- [x] The minimum token the 1.25 and 1.27 servers accept for players (see [The bundled GServers](#the-bundled-gservers)).
- [ ] A lab login of both clients on a loopback GServer.
