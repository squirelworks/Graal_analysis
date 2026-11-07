# Classic server-side tools

Date: 2026-11-01

Plain behaviour of the tools whose earlier summaries stopped at a purpose line.
Static reads only: strings, import tables, and named functions. No image was
executed. Tags: **[bin]** the image, **[src]** the 1999 account writer that the
stat tools link, **[file]** a sample file in the tool's own archive, **[doc]**
that archive's readme.

| Note | Tool | What was new |
| --- | --- | --- |
| `serverlist3.md` | Classic listserver ELF | Config keys, the zlib frame, what a client sends, what a game server sends, what is never sent. |
| `gserverstat.md` | `gserverstat` and `gserverstat2` | The 14 page modes, the top-50 rules, the account file, the HTML columns. |
| `character-designer.md` | GCD 1.2.7 and GChar 1.0 | The `CHR:1.00` line, CHI versus CHR, and that neither tool opens a socket. |
| `graal-level-gen.md` | GraalLevelGen (December 2000) | Image rules, colour table, output names, merge-on-second-run. |
| `text-convert.md` | TextConvert | Folder walk, GR-V1 in, GLEVNW01 out, no socket. |

In-process references, with tests in `test_classic_tools.py`:

| Module | Recovers |
| --- | --- |
| `listframe.py` | The listserver frame and the client and game-server login lines. |
| `account13.py` | The `accounts/accN.txt` blob and a leaderboard row with no password. |
| `chrfile.py` | A `CHR:1.00` character line. |

## Skipped

- Win32 `ListServer.exe`. Already described in `../server-tools-2001.md`, including the saved-login hand-off. Not reimplemented.
- Trainers. Another branch owns those notes.
- `GServer Stats.zip` on Drive. Blocked as an abusive download. The stat notes come from the small gserver source archive's `gserverstat`, `gserverstat2` and `statmaker` instead.
- GraalLevelGenNW. The December 2000 generator's own HTML now covers the operator contract, and the NW summary already says that build is offline and writes a `levels` tree.
- Remote control, NPC control, Guildmaker, the later C# listserver. Existing notes already answer what they send.
