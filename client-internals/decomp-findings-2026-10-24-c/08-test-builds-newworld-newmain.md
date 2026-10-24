# 08 The 2.1 test builds, NewWorld betas, NewMain

## 2.1 test2 and test3
- Same login token as 2.05 (GNW03081), same login shape, same PLI set as 2.05 (39 ids, 0-24, 26-30, 32-38, 80-81). No new client-to-server id.
- Two new server-to-client ids: 49 PLAYERWARP2 and 169 UPGRADEURL (61 ids handled, bound 0xa9). Same two ids appear in NewWorld beta2 and are in the 2.17-2.31 layouts documented in batch b, so these builds are where they started.
- test2 to test3: same id sets. Differences are the "skip reloading the already-loaded level" checks in LEVELBOARD, LEVELNAME and PLAYERWARP, plus one extra call in SAY2. Vendor changelog adds snapshot-level lighting fixes and smilies in PMs (`levels/smilies/smiliesdef.txt`, lines `code,filename`). Those are client-only.
- The exe is about 140 KB smaller than 2.05 rev2 despite more functions, because of the rewritten image engine (the changelog says the image handling no longer uses Windows GDI).
- Editor classes changed: the person/NPC/show-code windows were merged into a tabbed editor (class list in `classes_by_build.tsv`).
- Script additions (strings): `ascii`, `defnpc` (predefined npcs from `defnpc*.txt`), `playeronline`, `startinfullscreen`, `tiles` (test2); `groundheights`, `waterheight`, `playerhp`, `playermaxhp`, `smiliesdef.txt` (test3). Also see `script_vocab_deltas.tsv`.

## NewWorld beta1 / beta2
- Token G2N15041. Branch point: the 2.02 code line (token digits, class list with the old person-editor windows, same PLO bound as 2.05 for beta1).
- Beta1 server-to-client set: 53 ids. Compared with 2.05 rev2 it lacks 2 (BADDYPROPS), 4 (LEVELCHEST), 17/18 (HORSEADD/DEL), 154/155 (freeze/unfreeze), 49 and 169, and (like 2.04+) 26; it still has 156, 165, 166, 168.
- Beta2 adds 49 and 169 (55 ids) and switches to the 2.1 editor classes. In other words beta2 follows the 2.1 test branch; beta1 follows 2.05.
- Client-to-server: 34 ids. Same as 2.1 test but without 7 (HORSEADD), 11 (THROWCARRIED), 15 (BADDYPROPS), 16 (BADDYHURT), 17 (BADDYADD).
- Script vocabulary: new `nw*` time variables (nwyear, nwmonth, nwweek, nwweekday, nwday, nwhour, nwmin, nwtime), `layer`, `arraysnw.dat`, `bodycolors.txt`, `bodynw.png`, `controlnpc.txt`, `selectedsword`, `playerhearts`, `playerfullhearts`, plus string-list helpers (addstring, insertstring, deletestring, removestring, sarraylen, lindexof) in beta2. Dropped: the Graal classic baddy/animal names (blue soldier, gray soldier, dragon, frog, ...) and `arrays.dat`.
- Confirms that the NewWorld "world" is a different content stack (new body images, own array file) on top of the unchanged 2.0x protocol, with the NEWWORLDTIME packet (42) already present in 2.00.

## NewMain 24 / 26
- Token GNW08011. PLO set: 51 ids, 0-45, 75, 100, 150, 151, 153 only. That is the 2.00 set without 154, 155. PLI set: 35 ids, the 2.00 set.
- NewMain 24 and 26 have identical handler shapes and an identical login. They differ only in resources and a few VCL calls.
- NewMain pulls in the Delphi DDE classes (TDdeMgr etc.) and keeps the person/NPC/chest/baddy editor windows, consistent with an older, pre-2.00 code line.
- Handler shapes differ from 2.00 more than any 2.0x revision does (many ids below 0.7 similarity), so NewMain is a separate branch, not a rev of 2.00.
