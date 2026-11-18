# Preagonal Hubserver v0.3.7 and two Delteria backups, 2026-11-18

Static reads only. Nothing was run. Tags: **[bin]** for the Hubserver bundle,
**[file]** for the Delteria backups. Evidence IDs are in
[`docs/evidence-index.tsv`](../docs/evidence-index.tsv); file inventories with
full digests stay owner-held.

## Hubserver v0.3.7 against v0.3.6

Evidence: `HUBSERVER-037-20261118`, `HUBSERVER-036-20261113`.

Same six platform builds as v0.3.6 (Linux, macOS and Windows on x64 and arm64).
Each zip holds one .NET single-file host, its symbols file, two settings files
and the native SQLite library. The comparison below is the Linux x64 build;
the other builds have the same files, except that Windows adds an IIS module and `web.config`, and macOS ships the SQLite library as a `.dylib`.

| Item | v0.3.6 | v0.3.7 |
|---|---|---|
| Server program code | baseline | **identical**: every one of 1,663 method bodies has the same IL, with the same types, fields and string literals. Only the compiler-generated type names that embed a source-file hash changed. **[bin]** |
| Default settings file | baseline | identical **[bin]** |
| Preagonal common and GS2 libraries bundled in the host (common, AST, grammar, compiler, VM) | baseline | identical bytes **[bin]** |
| Entity Framework Core and its SQLite provider | 10.0.15 | 11.0.0 **[bin]** |
| MySQL provider / connector | 10.0.14 / 2.6.2 | 11.0.0 / 3.0.0 **[bin]** |

So v0.3.7 is a dependency refresh. It adds no protocol, packet, version-token
or database-schema change over v0.3.6. **[bin]**

### What the Hubserver shows (unchanged from v0.3.6)

v0.3.6 was fetched on 2026-11-13 but not read then, so these are first notes.
They describe the Preagonal hub, not the official listserver.

- **Three listening sockets.** Game servers on 14900, new-protocol clients on
  14922, old-protocol clients on 14923. Game servers have one interface setting, and the two client ports share another.
  Every setting can come from environment variables instead of the file. **[bin]**
- **Two client protocol generations.** An enum with `Version1`, `Version2`, and
  `Unknown`. A connection classed as new protocol is logged as "forwarding
  client". Old-protocol players are logged as "Legacy Player". **[bin]**
- **Allowed-version table.** The hub carries its own version-token table from
  1.25 to 6.037 (Linux 6.037 split out), the iPhone 1.1, 1.5, 1.11 and Belote
  1.5 clients, and the NPC-server token. All tokens are already in
  [`VERSION-TOKENS.md`](../VERSION-TOKENS.md); none is new. The string `allowedversions`
  sits beside the game-server settings handling. **[bin][inf]**
- **Server list replies.** Recognises `lister`, `simplelist` and
  `simpleserverlist` requests; the list carries `players=-1` as a value; a full hub answers "No available server! Try again later". **[bin]**
- **Server registration.** Server name uniqueness is enforced ("Servername is
  already in use!"), with a duplicate cap (default 3) and a server cap (default
  100). A registered-server password check returns `Valid`, `NotActivated`,
  `InvalidPassword` or `Unregistered`. **[bin]**
- **Accounts.** Account status `Normal`, `NotActivated`, `Banned`,
  `InvalidPassword`, `NotFound`; admin levels None, Moderator, Admin, SuperAdmin.
  Device ids are a platform plus an HDD hash, a NIC hash and an Android id, kept
  per account. Buddies, guilds (with nickname and rank per member), IP bans and
  profiles (age, sex, country, ICQ, e-mail, URL, hangout, quote) are stored in
  `graal_*` tables (names like the classic PHP listserver's **[inf]**). A web API with JWT
  bearer login sits beside the sockets. **[bin]**
- **IRC-style relay.** Channel joins and parts, private and mass messages, and a
  `#hubserver` channel bridged to Discord. Player status words are Online, Away,
  Hiding and DND. **[bin]**
- **GS2 inside the hub.** The hub links Preagonal's GS2 compiler and VM and
  has strings for a `dbnpc`, an `onCreated` entry and a script compile error, so it compiles database NPCs itself **[inf]**. That is their
  MPL-2.0 code; see
  [`docs/preagonal-gs2-clean-room-2026-11-07.md`](../docs/preagonal-gs2-clean-room-2026-11-07.md)
  for why none of it moves into Seihai. **[bin]**

## Delteria backups

Evidence: `DELTERIA-2002-BACKUP-20261118`, `DELTERIA-2019-BACKUP-20261118`.

### Both were already held

| Backup | Files | Distinct contents | Against what we held |
|---|---|---|---|
| 2002 (dated 2002-12-08, newest file 2002-12-07) | 2,740 | 2,699 | The archive is byte-identical to the copy already in the combed archive. Its contents also match the older December 2002 archive file for file. **[file]** |
| 2019 (dated 2019-09-07, files 2005–2019, most 2016) | 785 | 724 | A different container (zip, not rar) from the held 2019 archive, but every file is identical. **[file]** |

So neither download adds new level or script data. The two backups differ
from each other completely. They share no level names, and they come from
different engine eras.

### Level formats: no `GR-V1.05` sample

| Backup | `GR-V1.03` `.graal` | `GLEVNW01` `.nw` | `GR-V1.05` |
|---|---|---|---|
| 2002 | 1,697 | 916 | **0** |
| 2019 | 0 | 692 (one has no extension) | **0** |

Every file was checked by its first eight bytes, not its extension. The 2002
set predates 5.00r7, where [`GR-V1.05`](../formats/gr-v105-500r7.md) first
appears, so a negative there is expected. The 2019 set holds only text levels.
The open item "decode one real on-disk `GR-V1.05` sample" in
[`gr-v105-empty-tiles-2026-11-16.md`](../formats/gr-v105-empty-tiles-2026-11-16.md)
stays open. **[file]**

The 2019 set does have **three real multi-layer `GLEVNW01` levels**: `BOARD`
rows on layers 1 and 2, 141 rows in total. Every other `.nw` file in either
backup uses layer 0 only. Those three are the nearest real input for the
multi-layer writer and for the "live serve of a multi-layer file to 5.12 /
6.03r7" lab: convert one to `GR-V1.05` with the 5.x writer rule, then serve
it. **[file][inf]**

### Script dialects

| Backup | Script body | Shape |
|---|---|---|
| 2002 | Level NPCs, plus 119 loose NPC and weapon text files | GS1 only. 861 files use `if (created)`-style event tests, and 433 use `#s`/`#v`-style message codes. There is no `function onX()`, `join`, `trigger*` or `scheduleevent`. **[file]** |
| 2019 levels | 691 `.nw` level NPCs | **Mixed.** 190 files have `function onX()` handlers and 158 call `join("class")` (108 distinct classes). 122 still use GS1 `if (created)`, and 100 files mix both styles. **[file]** |
| 2019 server backup | 40 originals (25 classes, 6 weapons, 1 npc script, 7 comments, server options) plus 5 edited copies | Full GS2. Only 11 of the 108 classes that the levels join are in this backup. **[file]** |

### GS2 features worth a test

Counts are over the 2019 server backup (45 files). Each item is a feature that
appears in real 2016–2019 server code. The raw scripts stay private. Only
these counts are published.

- `public function` (61 in 15 files) and `function onX()` events (140).
- `new Gui…Ctrl(…) { … }` object blocks (97 in 3 files) and `new TStaticVar`.
- `for (temp.x : list)` iteration (74 in 16 files) and `in |a, b|` ranges (22).
- `switch`/`case` (29 / 169), the ternary operator (68), and `with (obj)` (45).
- `temp.` locals (2,500 uses), and `clientr.`, `client.` and `serverr.` variables.
- `triggerserver`/`triggerclient` pairs (102 / 49), `scheduleevent` (24),
  `waitfor` (6), `sleep` (39) and `trigger` (7).
- String and list methods: `.starts` (39), `.substring` (37), `.size()` (52),
  `.add` (31), `.pos`, `.tokenize`, `.insert`, `.index`, `.delete`,
  `.subarray`, `.length()`, `format()`, `@` joins, and `SPC`/`NL`/`TAB`.
- `findplayer`, `findlevel`, `findnpc`, `putnpc2`, `setlevel2`, `savelog`,
  `loadlines`/`savelines`, `loadvars`/`getstringkeys`, `requesttext`, and
  gmap names (88).

For **seihai-core**, the parser on `main` already names most of these
(`public`, `with`, `switch`, `in`, `new` blocks, `waitfor`). The 2019 levels
are the useful new case: a single level NPC can hold GS1 `if (event)` blocks
next to GS2 `function onX()` handlers and `join` calls. 100 real files do
this. A mixed-dialect compile test, written from synthetic text in that shape,
would cover them. **[inf]**

For **graal-client-repro**, the 2019 set is a 6.x-era (2016 and later) server.
The levels lean on `join`, `drawunderplayer` (2,770), `setshape` (799) and
clientside `this.` state. Weapons use `triggerserver` with GUI controls. The
three multi-layer levels test tile-layer drawing. **[inf]**
