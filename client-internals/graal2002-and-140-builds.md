# Graal 2002 world builds (2.1.0.x, Oct–Dec 2001) and the 1.40 builds

Date: 2026-11-13. Static read of owner-held client builds that no earlier note covers. Evidence ID `CLIENT-HUNT-20261113`
([evidence index](../docs/evidence-index.tsv)). The original batch and the separately dated ver10 addition below are
**[bin]**: behavior read from the executable files, not established by a traffic capture.

## The builds

Six Windows Delphi clients for the Graal 2002 world, and four clients from the 1.39 to 1.41 line. The dates are the
modification times of the files shipped with each build. The PE link stamps are Delphi's fixed value and say nothing.

| Build | FileVersion | Shipped | Size (bytes) | Token [bin] | GS1 commands | Server messages handled (bound) |
|---|---|---|---|---|---|---|
| 2.1 test 3 (already catalogued, for reference) | 2.1.0.0 | 2001-09 | 1,753,600 | `GNW03081` | 161 | 61 (`0xa9`) |
| Graal 2002 ver7 | 2.1.0.0 | 2001-10-09 | 1,665,536 | `GNW03081` | 167 | 55 (`0xa9`) |
| Graal 2002 ver8 | 2.1.0.0 | 2001-10-19 | 1,670,656 | `GNW03081` | 167 | 56 (`0xaa`) |
| Graal 2002 ver9 | 2.1.0.0 | 2001-10-30 | 1,673,216 | `GNW03081` | 168 | 56 (`0xaa`) |
| Graal 2002 ver10 | 2.1.0.2 | 2001-11-15 | 1,676,288 | `GNW31101` | 169 | 60 (`0xae`) |
| Graal 2002 ver13 | 2.1.0.4 | 2001-11-27 | 1,676,800 | `GNW31101` | 169 | 60 (`0xae`) |
| Graal 2002 v22 | 2.1.0.4 | 2001-12-31 | 1,805,824 | `GNW31101` | 174 | 69 (`0xb1`) |
| 2.17.1 (already catalogued, for reference) | — | 2002-12 | 2,180,096 | `GNW22122` | 198 | 79 (`0xb9`) |

| Build | FileVersion | Size (bytes) | Token [bin] | GS1 commands | Server messages handled |
|---|---|---|---|---|---|
| 1.39 (already catalogued) | 1.3.8.0 | 1,448,960 | `GNW07080` | 111 | 45 (`0x64`) |
| 1.39 "duplicate" build | 1.3.9.1 | 1,450,496 | `GNW07080` | 111 | — |
| 1.40 | 1.3.9.1 | 1,488,384 | `GNW23090` | 125 | 45 (`0x64`) |
| 1.40 rev 1 | 1.4.0.1 | 1,488,384 | `GNW23090` | 125 | 45 (`0x64`) |
| 1.41 rev 1, two more copies | 1.4.1.1 | 1,506,816 | `GNW13110` | 126 | 45 (`0x64`) |

How each column was read:

- **Token:** with the character-immediate scanner described in the
  [token catalogue](version-token-catalogue.md#evidence-grades).
- **GS1 commands:** with [`tools/gs1-table-scan`](../tools/gs1-table-scan/README.md) in `table` mode.
- **Server messages handled:** each build's receive dispatcher has a range check, an index table and a destination table.
  The count is the number of logical ids whose destination differs from the default route, the same method as
  [`plo-handled-ids-by-build.tsv`](../version-profiles/plo-handled-ids-by-build.tsv). The method reproduces that table's
  rows for 2.05, 2.1 test 3, 2.17.1, 1.39 and 1.41r1 exactly.

The two extra 1.41r1 copies have the same size and version as the catalogued 1.41r1, but different bytes. Their token, command
list and dispatcher match it. They are not separate releases.

A later [focused callback comparison](early-windows-callback-variants.md) identifies a
program-check error binding that enters a handler in one copy and the same handler's
final return in another and the baseline. It does not establish the event trigger,
helper effects or modification history. **[bin]**

A later read of the same 22 code-section bytes shows what the other 21 are. They are
character constants that spell the list host and the list port, and the two copies do
not spell the same endpoint. The login token, the 45-id receive set and the GS1 command
list do not change. The host and the port are not written out, and spelling a different
endpoint does not by itself show that the copy reaches it. **[bin]**

## What the Graal 2002 builds settle

1. **`GNW31101` is now [bin].** The token-catalogue row "2.1.0.0–2.1.0.3, `GNW31101`, L" now has three executables
   (ver10, ver13 and v22) that carry it. Its DDMMY stamp reads 31 Oct 2001, which falls between ver9 (shipped 30 Oct, still
   `GNW03081`) and ver10 (15 Nov). The first three Graal 2002 builds kept 2.05's token, as the 2.1 tests did. FileVersion 2.1.0.4
   also sends `GNW31101`, so the public list's "2.1.0.0–2.1.0.3" range understates it. The grade stays B until a login frame is
   captured.
2. **The 2.1x GS1 additions now have dates.** The [GS1 note](../npc-library/gs1-commands-by-version.md) could date the 33
   commands that 2.17.1 adds only to "after 2.1 test 3, by 2.17.1". Nine of them now date more closely:

   | First seen in | Commands |
   |---|---|
   | ver7 (2001-10-09) | `play2`, `shoot` |
   | ver9 (2001-10-30) | `replacestring` |
   | ver10 (2001-11-15) | `savelog` |
   | v22 (2001-12-31) | `setcursor`, `setcursor2`, `setshootparams`, `wraptext`, `wraptext2` |

   The other 24 first appear in 2.17.1. ver7 also brings `addstring`, `deletestring`, `insertstring` and `removestring` into
   the main client line. NewWorld beta 2 already had all four. `setbacktile` and `seteffect` differ between v22 and 2.17.1 only
   in the scanner's trailing-space marker. The two scan modes (`table` for v22, `init` for 2.17.1) write it differently, so
   neither command counts as new.
3. **Server-message ids 170 to 177 are new in 2.1.0.x.** ver8 and ver9 add id 170, ver10 and ver13 add 171 to 174, and v22
   adds 175 to 177. 2.17.1 then has 168 to 185, plus 68 and 69. This splits the "2.1 set plus …" rows of manual §2.4 by build.
4. **ver7 to ver13 route six ids to the default branch.** Ids 2, 4, 17, 18, 154 and 155 have their own branch in 2.05, in the
   2.1 tests, in v22 and in 2.17.1, but not in ver7 to ver13. In the classic numbering, 2, 4, 17 and 18 are baddy props, the
   level chest and the two horse messages. That fits a world build that shipped without baddies, chests or horses and got
   them back by the end of December 2001. This is a static reading of dispatch only; whether these ids were really ignored
   needs a lab run.
5. **The Graal 2002 world files.** Each build ships the world's gmaps (main, forest, dustari, pirates, samurai and zormite;
   v22 adds caverns, start and mines), plus a `loadgmaps.txt`. They are the earliest gmap-based world clients in the set.
   Shipping that file is not the same as the executable opening it. The preload loop was traced only in v22
   ([Local gmap preload and controlnpc](#local-gmap-preload-and-controlnpc)).

## Receive layouts of ids 170 to 177

The binding counts above say which ids have a non-default receive destination. They do not say what the handler reads. The table is the body-read receipt for two images. The public 2.1.0.0 image was read for ids 170 to 174. Graal 2002 v22 was read for ids 175 to 177. Each row is the payload width read in that handler body and the condition under which the handler applies it. Nothing was run. These are server-to-client receives. No client send of ids 170 to 177 was read. ver8, ver9, ver10 and ver13 bind some of these ids. Their handler bodies were not compared with the public image, so the widths are not claimed for them. **[bin]**

A Graal character (`c`) is the wire byte minus 32. A Graal short (`s`) is two Graal characters, high byte first. **[bin]**

| Id | Image | Direction | Width and encoding | When it is applied |
|---:|---|---|---|---|
| 170 | public 2.1.0.0 | receive | one `c` flag; ghost mode is on when that value is above 0. A payload shorter than one byte is not applied | when the server sends 170 |
| 171 | public 2.1.0.0 | receive | comma-separated text. At least two fields are required. Field 0 is the map text name and field 1 is the image name. When at least four fields are present, fields 2 and 3 are decimal floats (a default head position). 171 and 172 enter one shared parser. After that parse, an id-dependent branch calls a distinct callee for each id | when the server sends 171. Which display role that callee implements remains unestablished |
| 172 | public 2.1.0.0 | receive | the same shared comma parser as 171, then that id-dependent branch to 172's own callee | when the server sends 172. Which display role that callee implements remains unestablished |
| 173 | public 2.1.0.0 | receive | the whole payload, with no length prefix, is stored as the ghost-mode text | when the server sends 173 |
| 174 | public 2.1.0.0 | receive | one `c` flag, the same test as 170; the result is the ghost-icon flag | when the server sends 174 |
| 175 | v22 | receive | at least two bytes. The player id is an `s`. The bytes after those two are the shot payload and are passed to that player's shoot handler | only when the player's current level is the active level. A shorter payload is not applied |
| 176 | v22 | receive | no payload bytes are read. The handler stores the constant 1 in the Kingdoms-mode flag and returns | when the server sends 176. A further form change past that store was not traced in v22 |
| 177 | v22 | receive | no payload bytes are read. The handler stores the constant 1 in the New-World-mode flag and returns | when the server sends 177. A further form change past that store was not traced in v22 |

The 2.17 to 2.31 layouts in [`plo-layouts-217-231.tsv`](../version-profiles/plo-layouts-217-231.tsv) already describe the same widths, and they go further on 171 versus 172 (one routine, split by id, 172 to the minimap) and on 176 and 177 (the main form switches mode). This read shows those widths are already present in the public 2.1.0.0 image and in v22. On the public image it also shows an id-dependent branch to distinct callees after the shared parse of 171 and 172. Which display role each callee implements remains unestablished. It does not re-prove the later images, and it does not prove the mid-ladder bodies. ver8, ver9, ver10 and ver13 handler bodies stay uncompared. **[bin]**

## Local gmap preload and controlnpc

### GRMAP001 in the public image, and loadgmaps.txt in v22

The public 2.1.0.0 gmap reader's body was walked. It accepts `GRMAP001` and the keys `WIDTH`, `HEIGHT`, `GENERATED`, `LEVELNAMES` through `LEVELNAMESEND`, `GENSEED`, `GENBASE`, `GENEVENBORDERS`, `GENHEIGHT`, `GENCHAOS`, `LEVHEIGHT`, `LEVCHAOS`, `MAPIMG`, `HEIGHTMAP` through `HEIGHTMAPEND`, `RANDOMSEEDS` through `RANDOMSEEDSEND` and `HEIGHTS` through `HEIGHTSEND`. After a successful read it records the status text `Loaded gmap`. The 2.05 reader note does not list `LEVELNAMES`. This pass did not find `MINIMAPIMG`, `NOAUTOMAPPING`, `LOADFULLMAP` or `LOADATSTART` in that reader. **[bin]**

The literal `LEVELNAMES` has one code reference from ver9 onward in this set (ver9, the public image, ver10, ver13 and v22) and is absent from ver7 and ver8. The status text `Loaded gmap` has one code reference in the public image, ver10, ver13 and v22, and is absent earlier in the set. That count is presence. Only the public reader's body was walked. **[bin]**

v22's preload body was walked. It joins its base path with `loadgmaps.txt`. When that file exists, each line is passed to the gmap loader. That is a preload list. The literal `loadgmaps.txt` is in the v22 image and is absent from ver7, ver8, ver9, the public image, ver10 and ver13. A world package can still ship the file beside an earlier executable; this read does not show those executables opening it. **[bin]**

### controlnpc.txt on ver10

On ver10, the loader body runs only when a global gate byte is clear (zero) and the resolved path for `controlnpc.txt` is nonempty. The predicate is that nonempty resolved path. A nonempty file-content check is a different test, and this branch does not use it. The client then loads the file. The helper that follows trims each line-feed-terminated piece and removes a preceding carriage return, appends the section-sign separator, then appends a remaining nonempty unterminated tail unchanged. That helper is the text attached to the weapon. It does not compile GS1 and it does not execute GS1. The client creates a weapon named `Control-NPC`, attaches the joined text, and appends the weapon to the player's weapon list. The option or config key that writes the gate byte is still unidentified. Which built-in weapons the text replaces stays unestablished. Whether the joined text later runs or causes a packet stays unestablished. **[bin]**

The literal `controlnpc.txt` has one code reference in ver7, ver8, ver9, ver10 and ver13, and is absent from the public 2.1.0.0 image and from v22. Only ver10's loader body was walked. The NewWorld beta note that installs `Control-NPC` when the player is created is a different client and is not evidence for this ladder. **[bin]**

## Ver10 initial player-properties update (2026-11-15)

This addition is an exact-build static trace of the Graal 2002 ver10 client, FileVersion 2.1.0.2. Evidence ID `WIN-VER10-INITIAL-PROPS-20261115` ([evidence index](../docs/evidence-index.tsv)). It does not transfer to the public 2.1.0.0 build, ver13 or v22 merely because they share `GNW31101`. **[bin]**

### Ordered first-update construction

The guarded first-update path, when its cached player state is absent, walks a six-entry property table in order. For each entry it appends the property id followed by the selected serializer output, then passes the resulting stream to the player-properties message sender (id 2). This establishes a construction order, not an observed first packet on the wire. **[bin]**

| Order | Property | Selected encoding observed in ver10 |
|---:|---|---|
| 1 | 0 NICKNAME | counted text, limited to 200 bytes by this serializer |
| 2 | 11 HEADGIF | a recognised numbered head below 100 uses one `c` index; the custom-name branch limits its prepared name to 100 bytes and emits `c(100 + length)` followed by those bytes |
| 3 | 13 COLORS | five `c` values |
| 4 | 18 STATUS | one `c` value |
| 5 | 31 UDPPORT | three encoded 7-bit groups from the connection’s saved socket-bound port |
| 6 | 33 ADDITFLAGS | one `c` value |

The encoding notation is defined in [player properties](../protocol/player-props.md). The order and selected branches above were read in ver10 itself; they are not inferred from the older six-property list. The UDP initializer is the direct helper called after login/language setup: it is not the player-properties serializer. **[bin]**

### Necessary receive-side gate

The connection constructor sets a gate that the outgoing update path tests. The receive dispatcher’s self player-properties message (id 9) calls the self-property parser and clears this gate after the parser returns normally. The parser’s ordinary loop runs only while more than one payload byte remains; an empty or one-byte body skips that loop and reaches its normal return path. This is bounded control-flow evidence, not a claim about arbitrary malformed input. **[bin]**

The outgoing path also tests the network object and separate player/update state, including its cached-state branch. The id-9 gate is therefore necessary on this traced path, not proof that any id-9 reply immediately produces an update or that a complete login/world entry succeeds. Which complete startup conditions reach the first emitted update remains unmeasured. **[bin]**

### Method and remaining limits

The trace joins the mapped receive tables and gate write to the update guard, ordered data table, selected serializer branches and message wrapper. Some valid Delphi virtual entries were not defined as procedures by default analysis; mapped-byte observations and independent bounded instruction decoding were used rather than attributing them to a guessed neighbouring function. Decompiler types and exception-handler coverage remain limited. **[bin]**

No native traffic capture establishes this first update. These findings do not complete the outgoing message-id inventory, the whole player-property codec, helper semantics for other properties, or any whole-build teardown. A discriminating capture must start before the first server reply and compare no reply, an unrelated well-formed reply, and self-properties replies in fresh sessions, preserving other startup conditions and no-emission results. **[bin]**

## Ver10 list entry and connection boundary

This exact-build static follow-up uses evidence ID `WIN-VER10-LIST-ENTRY-STATIC-20261115` ([evidence index](../docs/evidence-index.tsv)). Retained analysis observations were checked with bounded independent instruction decoding, selected data-table reads and import-thunk mapping. It does not establish a complete login or first player-properties emission. **[bin]**

The reviewed list-loading path constructs an encoded fixed host, appends a suffix and supplies a fixed list port. Its generic connection initializer checks a host cache, tries numeric-address parsing and then hostname resolution, creates a TCP socket, parses the supplied port and connects before switching to nonblocking mode. The loader sends its list token and subsequent login strings after that initializer returns. Host identity is intentionally omitted; no arbitrary endpoint configuration follows from this trace. **[bin]**

The list-reply reader decodes biased row counts, per-row field counts and per-field lengths, then copies the stated bytes. The selected-row join requires at least eight fields and takes the game host and port from zero-based fields 6 and 7. These are selected list-row fields, not the list connection's fixed endpoint and not player-property ids. This observation does not establish complete validation of malformed lists. **[bin]**

The inspected cache starts empty. Its sole direct writer call found in executable bytes follows address resolution. No ordinary file-input route was found in the inspected loader or cache routines. Direct-call/immediate-reference searches do not exclude aliases, indirect calls or other unreviewed entry paths; this is not a whole-program proof that local entry is unavailable. **[bin]**

### Two bounded local-entry attempts

On 2026-11-15, the unchanged exact ver10 executable was used in a Windows lab guest with virtual NICs disabled and guest-only input. Supporting data was mixed: an adjacent 2.1 data table and ten root resources from 2.22; no executable, DLL or configuration was overwritten. The peer was a self-authored Node list fixture, not a GServer checkout, so no server commit or full server-protocol coverage is claimed. Evidence ID `WIN-VER10-LIST-ENTRY-LAB-20261115` binds the owner-held run report, event logs and screenshots; no original art or raw artifact identity is reproduced. **[lab][cap]**

Each attempt began at a clean visible welcome without resource errors, with its listener already active. Online immediately showed connection failure: one attempt tested a local-file list candidate, the other the unchanged existing guest mapping at the statically identified list port. Neither listener recorded an accept or client bytes during its 30-second window. Independent review checked that the reported Online action fell inside each logged listening window and that both screenshots showed the failure. The existing mapping differed from the independently decoded fixed host, so the second attempt is not a test of that exact host mapping. **[lab][cap]**

Separate synthetic clients connected to both listener configurations and received the expected eight-field row. Those controls validate the fixture/loopback transport only; they do not show original-client protocol acceptance. After the original attempts no local row had been obtained, and owned client/fixture processes were cleaned up. Two negative entry hypotheses do not establish that all local routes are unsupported. None of the four original-client reply arms was reached, and no first player-properties emission was observed. **[lab][cap]**

### Native ver10 list/game entry and first wire frame

A later isolated Windows run on 2026-11-15 reached an owned loopback list and
then a selected game socket using the unchanged original ver10 executable,
FileVersion 2.1.0.2, through the normal no-argument client. Supporting DATA was
mixed, so this is not a pristine-install compatibility claim. The server was
a bounded synthetic list/game fixture, not a game-server release or commit.
Before this run, normal local entry had not been established by the two
attempts above; afterward, three fresh sessions supplied complete first game
frames. Evidence ID `WIN-VER10-GATE03-WIRE-20261115` in the
[evidence index](../docs/evidence-index.tsv) binds the reviewed structure-only
receipt and redacted log aliases `arm-A02.events`, `arm-B.events` and
`arm-C.events`. **[lab][cap]**

Each captured first frame was 66 wire bytes: a two-byte big-endian length
field declared 64 compressed bytes, which expanded to 56 bytes. The login
line identified client type 0 and token `GNW31101`. The three subsequent
client messages decoded as ids 37, 39 and 23 after generation-3 insertion
removal; all nine expected insertion-byte checks across the three frames
passed. None was player-properties id 2. Only decoded structure is published;
raw login fields and capture contents are excluded. **[cap]**

The listener lifetime was 30 seconds, approximately 29 seconds after accept,
with replies sent 500 ms after the complete first frame. The world-time and
empty-self-properties reply sessions recorded no later client chunks within
that bound. The no-reply session had a wrong-timer warning and is confounded.
The first player-properties update was not observed, and the remaining
reply-arm discriminator is unresolved. These observations do not prove that
clearing the static gate is sufficient, nor that the client never sends an
update. **[lab][cap]**

The wire observation upgrades only the exact ver10 game-login association.
The public 2.1.0.0 image, ver13 and v22 retain their own static grades despite
sharing the token. No complete client-send table, successful level entry or
whole-program behavior follows from this bounded first frame. **[inf]**

## Form resources

The resource directory names the Delphi forms compiled into each image. A name here is a window the executable carries. It does not say which of those windows the player can open. **[bin]**

ver7, ver8 and ver9 share one name set. It includes `TEDITNPC` and the 1.41 server-list forms (`TSERVERLISTFRAME`, `TSERVERMESSAGE`, `TSHORTMESSAGE`, `TWAABOUT`). It does not include `TCHESTEDIT`, `TEDITBADDY` or `TLOGFRAME`. ver8 and ver9 add no form name to ver7. ver13 matches ver10. The public 2.1.0.0 image and v22 match each other.

| Image | FileVersion | Size (bytes) | Form names added to the ver7 set |
|---|---|---|---|
| ver7, ver8, ver9 | 2.1.0.0 | 1,665,536 / 1,670,656 / 1,673,216 | none |
| public 2.1.0.0 | 2.1.0.0 | 1,771,008 | `TLOGFRAME`, `TCHESTEDIT`, `TEDITBADDY` |
| ver10 | 2.1.0.2 | 1,676,288 | `TLOGFRAME` |
| ver13 | 2.1.0.4 | 1,676,800 | `TLOGFRAME` |
| v22 | 2.1.0.4 | 1,805,824 | `TLOGFRAME`, `TCHESTEDIT`, `TEDITBADDY` |

The chest and baddy editor forms follow the dispatch split in the section above: absent on ver7–ver13, present on v22 and on the public 2.1.0.0, which is the image whose receive table keeps ids 2, 4, 17, 18, 154 and 155. `TLOGFRAME` is already in ver10 (15 Nov 2001), ver13, the public image and v22. The form matrix still lists `TABOUTDLG`, `TRPGFRAME` and `TTILESARRAYFRAME` as 2.17.1 additions; none of those three names is in this set. **[bin]**

## What the 1.40 builds settle

1. **New token `GNW23090`** (DDMMY 23 Sep 2000) in two executables labelled 1.40 (FileVersion 1.3.9.1 and 1.4.0.1). It sits
   between 1.39's `GNW07080` (7 Aug 2000) and 1.41r1's `GNW13110` (13 Nov 2000). It is on no public version list.
2. **1.391's listed token `GNW12080` is still unseen.** Both FileVersion 1.3.9.1 executables send something else: the
   "duplicate" build sends 1.39's `GNW07080`, and the 1.40 build sends `GNW23090`. 1.391 stays at grade L.
3. **1.40 adds 14 GS1 commands that 1.41r1 already has.** They are `function`, `return`, `break`, `continue`, `callnpc`,
   `callweapon`, `say2`, `canwarp`, `changeimgvis`, `drawovertrees`, `putexplosion2`, `setimg`, `setimgpart` and `spyfire`. In
   the scanner's form, `putexplosion` also changes to `putexplosion ` (it gains an argument). The [GS1 note](../npc-library/gs1-commands-by-version.md)
   dated these to "1.39 → 1.41r1". They now date to 1.40, Sept 2000. 1.41r1 adds only `showstats` on top.
4. The receive dispatcher is unchanged from 1.39 to 1.41r1: 45 ids, 0–41, 43, 75 and 100.

## Other builds in the same batch

- **Graal3D, later beta.** It sends `GR3DV003`, the next protocol revision after the Feb 2000 build's `GR3DV002` (on the wire). The full comparison is in [graal3d/beta3-genesis.md](../graal3d/beta3-genesis.md): the beta moves to Genesis3D and keeps the protocol.
  New strings show DirectInput with force feedback, camera distance and player-centre settings, and a deathmatch start. It needs
  its own lab run against the Graal3D server, to see whether that server accepts `V003`.
- **2.22, two more copies (FileVersion 2.2.2.0).** Both have 2.22's token `GNW03014` (and the listserver `GNW30123`), its 198
  commands and its 80-id receive table. They are the same build line as the catalogued 2.22. One is a modified copy that differs
  from the other in 4 bytes (a patched self-check). Neither is a new release.
- **Already covered, despite new copies:** the 3.04 Linux client (same executable as the one the 3.04 notes read) and GraalX
  2.0.0.3 (same archive as the one catalogued).

## Open points

- [x] ~~Capture the exact ver10 login token on an isolated loopback fixture.~~ [Native wire observation](#native-ver10-listgame-entry-and-first-wire-frame); sibling grades stay separate.
- [ ] Capture v22 and checked 1.40 login frames independently; no shared-token grade inheritance.
- [ ] Lab check of ids 2, 4, 17, 18, 154 and 155 on ver7–ver13. Send a baddy, a chest and a horse, and see whether the client draws them.
- [ ] Read the client-to-server ids each 2.1.0.x build can send, for manual §2.4's 2.1x rows.
- [x] ~~Read the receive bodies of ids 170 to 174 in the public 2.1.0.0 image and of 175 to 177 in v22.~~ [Receive layouts of ids 170 to 177](#receive-layouts-of-ids-170-to-177). ver8 to ver13 bodies were not compared. Client-to-server sends of these ids stay open.
- [x] ~~Form-resource names for the seven 2.1.0.x images.~~ [Form resources](#form-resources): the log form is in ver10 and later in this set; the chest and baddy forms return on the public 2.1.0.0 and on v22.
- [x] ~~Add the six builds to the scanner inventory and regenerate the matrix.~~ [67-build matrix](../npc-library/gs1-commands-by-version.md): six exact-input scans added; existing membership cells preserved.
