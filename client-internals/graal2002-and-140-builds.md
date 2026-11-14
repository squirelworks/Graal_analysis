# Graal 2002 world builds (2.1.0.x, Oct–Dec 2001) and the 1.40 builds

Date: 2026-11-13. Static read of owner-held client builds that no earlier note covers. Evidence ID `CLIENT-HUNT-20261113`
([evidence index](../docs/evidence-index.tsv)). No build was run, and no lab login has been done yet. Every finding here is
**[bin]**: read from the executable files, never seen on the wire.

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

- [ ] Capture a login frame from ver10 or v22 on a loopback lab server, to take `GNW31101` from B to W. Do the same for 1.40's `GNW23090`.
- [ ] Lab check of ids 2, 4, 17, 18, 154 and 155 on ver7–ver13. Send a baddy, a chest and a horse, and see whether the client draws them.
- [ ] Read the client-to-server ids each 2.1.0.x build can send, for manual §2.4's 2.1x rows.
- [ ] Add the six builds to `tools/gs1-table-scan/builds.tsv` and regenerate the matrix TSV.
