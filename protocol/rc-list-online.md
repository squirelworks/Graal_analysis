# Listing the RCs that are online (and why id 65 is not the way)

Date: 2026-11-12 (updated the same day with the 2010 Linux RC and RC3)

Question: how does a Remote Control learn which other RCs (admins) are online? gs2lib names
client → server id 65 `PLI_RC_LISTRCS`, and `seihai-rc` left "List RCs" open because the
2.22-era RC (`GSERV024`) never sends it. This note checks every staff client and every
GServer source in the materials.

Tags: **[bin]** read from a client binary (static) · **[src]** read in the 2001 GServer
sources (1.39 and New World) · **[srv]** GServer-v2 / gs2lib only · **[inf]** inferred.
No lab run was made for this note.

Field notation as in `packet-ids.md`: `c` = GCHAR (byte + 32), `s` = GSHORT (two 7-bit
groups + 32), `str` = a `c` length and then that many bytes.

## Answer

- **Id 65 was never implemented.** No RC build in the materials (1999 to RC3, 2015) sends it, and no GServer
  source answers it. There is no server → client reply id for it either. **[bin][src][srv]**
- **The online-RC list is the player list.** Since 1999 the server has put every RC into the
  RC player list with `PLO_ADDPLAYER` (55) and taken it out with `PLO_DELPLAYER` (56). An RC
  entry is a player with an **empty level**. The server also prints `New RC: <account>` and
  `RC disconnected: <account>` as `PLO_RC_CHAT` (74) lines. RC2 sorts entries with an empty
  level into an **Admins** folder at the top of its player list. **[src][bin]**
- For `seihai-rc`: build "list RCs" from the 55/56 stream (a level that is empty after
  trimming = RC; GServer-v2 sends one space). Do not send 65: the 2001 servers ignore it and
  GServer-v2 handles it as a no-op. **[src][srv]**

## Who sends 65 **[bin]**

Every RC send path was read: the constant id at each send call site. 65 (wire byte `a`) is in
none of them.

| Build | Login token | Client → server RC ids (constant) | 65 | 66 | 67 |
|---|---|---|:-:|:-:|:-:|
| GServer2 RC shipped with 1.21 | `GSERV007` | 1, 51–62 | no | no | no |
| GServer2 RC shipped with 1.25, 1.28 and the 1.3 test | `GSERV010`, `GSERV011` | 1, 51–64 | no | no | no |
| GServer2 RC 2000/8/19 | `GSERV019` | 1, 2, 6, 28, 55–58, 61–64, 67–79, 82 | no | no | **yes** |
| GServer2 RC 2001/01/27 | `GSERV021` | 1, 2, 6, 28, 55–58, 61–64, 68–74, 76–79, 82 | no | no | no |
| 2000/10/25, 2001/08/20, 2002/01/04, 2002/05/02 | `GSERV020`–`GSERV023` | see `tools/remotecontrol-lineage.md` | no | no | 2000/10/25 only |
| Graal Remote Control 2004/01/17 (Delphi), and its community mods (three rebuilds and the UPX-packed "Agret" RC) | `GSERV024` | 2, 6, 28, 51–54, 61–64, 68–76, 78, 79, 82, 84, 86, 88–92, 94, 96–98 (the same in every variant) | no | no | no |
| Remote Control 2006/12/20 (RC2 2.05, MSVC + GTK) | `GSERV025` | 1, 2, 3, 6, 7, 28, 50–54, 61–64, 68–86, 88–90, 92–94, 96–98, 103–119, 150–152, 154–156, 160 | no | no | no |
| Remote Control 2010/03/29, Linux x86-64 (GCC, stripped) | `GSERV025` | 2, 3, 7, 28, 51–54, 62, 63, 68–71, 75, 76, 78, 79, 81, 82, 84, 88–90, 92, 93, 97, 103, 105–108, 115, 117–119, 150–152, 154–156 (partial, see below) | no | no | no |
| RC3 (MinGW, file date 2015, symbols kept) | `GSERV025` | 2, 3, 6, 50, 61–64, 69–72, 74–85, 88, 90, 92–94, 96–98, 103, 107, 110–112, 114, 116–119, 151, 152, 154–156, 160 | no | no | no |

The 2001/01/27 row was read again for this note and includes 69, which
`remotecontrol-lineage.md` leaves out. The RC2 row mixes the RC and NC sockets (one virtual send); 103–119 and 150/151 are the NC
ids. 87 (`PLI_RC_PLAYERBANGET`) has no constant site in RC2 and may be sent with a computed
id; it was not traced.

The 2010 Linux build is stripped, so its row lists the constant ids found at the two send
shapes the compiler used; ids built at run time are missing from it. RC3 keeps its C++ symbols,
so every `sendData` call site was read by name; there too some ids (51–54, 68, 73, 86, 87, 89,
91, 95) are not constants at a call site. In both builds the only 65 constants near a
send are the player prop 33 inside a `PLI_PLAYERPROPS` (2), as in RC2.

**Not checked:** a Linux i386 RC from January 2005, packed with UPX 1.90 with a damaged header
(`upx -d` refuses it). It sits between the 2004 Delphi RC and RC2 2.05 in time. **[inf]**

## What the 2001 servers do **[src]**

The GServer 1.39 and New World sources name the ids `LISTRCS` (65), `DISCONNECTRC` (66) and
`APPLYREASON` (67), next to the account and player ids. In the message switch:

- 65 and 66 have **no case**. The message is dropped without a reply.
- 67 has a case: if the sender is an RC with admin level 3 or more, the server writes
  `Reason for the follwing account modification:` and the text to its log. Nothing is sent back.
- On the server → client side, ids 60 and 62–69 are empty slots in the same sources. There is no
  "RC list" reply id.

GServer-v2 keeps the gs2lib names and handles 65, 66 and 67 as no-ops marked "Deprecated". **[srv]**

## How the server announces RCs

### 2001 servers **[src]**

When an RC logs in, the server:

1. Sets the RC's own player fields: nickname `<account> - away`, head `head25.gif`, **level
   empty**. (It also disconnects any other RC from the same IP with "Another RC logged in from
   the same IP.")
2. Sends the new RC one `PLO_ADDPLAYER` (55) for every logged-in player **and RC**:
   `s id`, `str account`, then property pairs `c 20` + `str level`, `c 0` + `str nickname`,
   `c 11` + `str head`.
3. For each RC already online, sends the new RC `PLO_RC_CHAT` (74) `New RC: <that account>`,
   and sends the other RC a 55 for the new one plus `New RC: <new account>`.

When anyone leaves, every RC gets `PLO_DELPLAYER` (56) `s id`; if the leaver was an RC, also
74 `RC disconnected: <account>`.

So the full list of online RCs is: the entries of the 55/56 stream whose level is empty. The
"New RC" lines name the RCs online at login, but only as text.

### GServer-v2 **[srv]**

Same idea, more properties: 55 carries `s id`, `str account`, then level (20), player-list
status, nickname (0) and community name. An RC's level is **one space**, not empty. After
login the RC also gets one 74 line `Currently online: <a>, <b>, …` listing every RC, and every
RC gets `New RC: <account>`. `seihai-rc` already reads a level that is empty after trimming as
an RC.

## How RC2 2.05 shows them **[bin]**

RC2's player list has two folders, **Admins** (sorted first) and **Players**. An entry goes into
Admins when either:

- its nickname has a guild tag in parentheses that is in the staff-guild list from
  `PLO_STAFFGUILDS` (47), or
- its id is above 0, its level (prop 20) is empty, and bit 0 of prop 81 (player-list category)
  is clear.

Everything else goes into Players. Prop 81 bit 0 set (an external entry, for example a
server or channel) keeps an entry out of Admins; bits 1 and 2 move it to separate lists.

So RC2 needs nothing beyond 55, 56 and 47 to show who is staff and who is an RC.

RC3 uses the same rule, with the same untrimmed length test, unchanged from RC2. **[bin]**

The level test is on the length, with no trim. Against GServer-v2, whose RCs have a level of
one space, RC2 2.05 would most likely list the other RCs under Players, not Admins. **[inf]**
A server that wants RC2's Admins folder should send RCs an empty level.

## RC2 2.05: server → client ids **[bin]**

The RC socket's receive switch (previously "not located" in `unknown-ids-2026-11-06.md`)
handles: 8, 13, 16, 30, 35, 37, 47, 55, 56, 58, 59, 61–70, 72–77, 79, 82, 100, 102, 103, 180,
190. That is exactly the set of the 2010 Linux RC. 8, 56, 58 and 59 share one entry that reads
`s id` first. 65 on this socket is `PLO_RC_FILEBROWSER_DIRLIST`, unrelated to `PLI_RC_LISTRCS`.

## Open

- [x] Read the send paths of the 2010 Linux RC and RC3 (neither sends 65 or 66).
- [ ] Unpack the 2005 Linux i386 RC (damaged UPX header) and read its send path.
- [ ] A lab run with RC2 2.05 and two RC logins against the GServer-v2 fork, to confirm the
      Admins folder on the wire and whether the one-space level puts RCs under Players.
