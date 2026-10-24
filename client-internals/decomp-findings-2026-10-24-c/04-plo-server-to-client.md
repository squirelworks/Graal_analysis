# 04 Server-to-client ids (PLO) per build

Tables: `plo_handled_ids_by_build.tsv` (sets), `id_changes_between_builds.tsv` (adds/removes), `plo_decode_signatures.tsv` (field layouts, heuristic). Names are gs2lib's.

## Set growth
| step | added | removed |
|---|---|---|
| 2.00 | 53 ids: 0-45, 75, 100, 150, 151, 153, 154, 155 | |
| 2.00 rev1-3 | none | none |
| 2.01 | 46 HITOBJECTS, 156 SETACTIVELEVEL | |
| 2.01 rev1 | none | |
| 2.02 | 47 STAFFGUILDS | |
| 2.02 rev1, rev2 | none | |
| 2.03 | 48 TRIGGERACTION, 165 MOVE | |
| 2.04 | 166 SHOWIMGNPC | 26 NPCACTION |
| 2.05, rev1, rev2 | 168 (UNKNOWN168) | |
| 2.1 test2 | 49 PLAYERWARP2, 169 UPGRADEURL | |
| 2.1 test3 | none | |

- Dispatcher bound (last index): 0x9b (2.00-2.00r3), 0x9c (2.01-2.02), 0xa5 (2.03), 0xa6 (2.04), 0xa8 (2.05), 0xa9 (2.1 test). It always grows with the highest handled id.
- Correction to batch b note 04: 2.04 drops 26 only. 25 (SIGNATURE) stays in every build. The earlier wording "swaps 26 for 25" was wrong.
- Id 26 (NPCACTION, absent from the repo's 2.05 table) exists in 2.00-2.03. It reads GINT3 npc id and the rest, and only acts when the player's level is the active one. It has no handler in 2.04 and later, which agrees with the repo's "no jump-table entry for 26 in 2.05".
- Id 168 has an almost empty body (client-side reset only). In the 2.00-2.05 family it is first handled in 2.05 (all three 2.05 builds), consistent with batch b's 2.05 note that the login server sends it.
- 156 SETACTIVELEVEL is handled from 2.01 on. It stores the active-level reference by looking up the raw level name. The handler was reworked (much shorter) in 2.03.

## Active-level gating
- Only id 26 is gated on "player's level == active level" in the 2.0x builds, by my scan. For later ids (46-48, 165, 166) the batch-b 2.17+ analysis already lists the gating; I did not re-derive it per 2.0x build.
- Because 156 only appeared in 2.01, a 2.00 client has no active-level concept. Level-addressed packets in 2.00 act on the current level only.

## Layouts that are stable and verified by structure
(GINT/GCHAR counts; field meanings come from gs2lib. "len>N" means a minimum payload length guard.)
- 3 NPCPROPS, 24 NPCMOVED, 29 NPCDEL, 150 NPCDEL2, 165 MOVE, 166 SHOWIMGNPC: GINT3 npc id first.
- 8 OTHERPLPROPS, 11 BOMBADD, 19 ARROWADD, 20 FIRESPY, 21 THROWCARRIED, 32 SHOWIMGPLAYER, 36 EXPLOSION, 37 PRIVATEMESSAGE, 40 HURTPLAYER, 46 HITOBJECTS, 48 TRIGGERACTION: GINT2 player id first, then the rest.
- 42 NEWWORLDTIME: GCHAR + GINT3 (length guard >3); present since 2.00 and in every build, including NewMain.
- 13 TOALL: GINT2 sender + GCHAR + string. The 2.00 and 2.01 decodes looked different only because the scan was incomplete for the long handler.

## Handler behaviour changes
See `06-handler-changes-by-build.md` and `handler_shape_changes.tsv`.

## Missing in NewWorld and NewMain
See `08`.
