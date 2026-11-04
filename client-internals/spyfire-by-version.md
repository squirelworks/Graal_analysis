# When `spyfire` started working

Date: 2026-11-04

Question: the GS1 command `spyfire` is in the 1.41 command table, but scripts that call it do nothing. In which client build does it start to work, and was the 1.41 entry a NewWorld placeholder?

## Result

| Build | Table size | `spyfire` in the table | Executor case for `spyfire` |
|---|---|---|---|
| 1.39 | 111 | no | n/a |
| 1.41 rev1 | 126 | yes, index 115 | **none** (parses, does nothing) |
| NewMain 1.42 (NM24) | 134 | yes, index 115 | **none** |
| NewMain 1.42 (NM26) | 134 | yes, index 115 | **none** |
| 2.0 | 142 | yes, index 115 | **yes**, first build |
| 2.01, 2.02 rev2, 2.03, 2.04, 2.05, 2.05 rev2 | 144 to 161 | yes, index 115 | yes |

`spyfire` first does something in **2.0** (file date 2001-02-01). From 1.41 rev1 (token date 13 Nov 2000) through both NewMain 1.42 builds (January 2001), the command parses but is ignored. **[bin]**

In 2.0 the case reads its two arguments, places a fire spy just in front of the player (player position plus their facing direction, the same as 2.05 in `npc-library/gs1-command-reference-205.md`), and sends it online. The 2.05 case adds a guard that skips everything when there is no local player object. **[bin]**

## How it was read

- **Index.** The command table is the 12-byte record table described in `cross-version-timeline.md`. In every build from 1.41 rev1 to 2.05 rev2, `spyfire` is record 115 (op 715 in the 2.05 numbering), with `callweapon` at 114 and `function` at 116. The table sizes match the GS1 commands table in `cross-version-timeline.md`. **[bin]**
- **Executor.** The script executor dispatches on the record index through one jump table. Commands without a case share one target that skips to the end of the switch. In 1.41 rev1 and both NewMain builds, slot 115 goes to that shared target. From 2.0 on it has its own case. **[bin]**
- **Cross-check.** The same shared target holds the commands that earlier notes already list as no-ops: `canwarp` (1.41), `canwarp2` (from NewMain 1.42), `drawovertrees` and `function` (handled by the parser, not the executor). So the method agrees with what was known. **[bin]**

## Was it a NewWorld placeholder?

There is no sign of that. **[bin][inf]**

- The fire spy itself is much older than the command. Every client from 1.33 handles the server packet for a relayed fire spy (PLO 20, see the packet table in `cross-version-timeline.md`), and the 1.41 readme lists "spy fire" as the item-button action when riding a horse. In 1.41 rev1 the routine that creates the fire spy (and plays `fire.wav`) is called from two places outside the script executor, a packet handler and the player update. **[bin][doc]** Which call is the horse action is **[inf]**.
- So in 1.41 the script command was a new table entry for an existing game effect, added before its executor case was written. Several other 1.41 additions were also table-only at first (`canwarp`, `drawovertrees`).
- The NewWorld clients are later. The NewWorld betas date from after 2.05 (`newworld-betas.md`), and the `GNW` prefix of the 1.41 token is the token format, not a NewWorld marker (`build-catalogue.md`).

## Side finding: `callweapon`

`callweapon` (record 114, also new in 1.41 rev1) follows the same pattern one step later. It has no executor case in 1.41 rev1, NewMain 1.42 or 2.0, and gets one in **2.01**. **[bin]**

## Builds

The builds are the ones listed by MD5 in `build-catalogue.md`: 1.41 rev1 (the patched copy, the only one available), NewMain 24 and 26, 2.0, 2.01, 2.02 rev2, 2.03, 2.04, 2.05 and 2.05 rev2. No lab run; static reads only.
