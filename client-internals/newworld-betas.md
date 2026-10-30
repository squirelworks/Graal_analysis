# NewWorld beta clients (graalnwb1, graalnwb2)

Date: 2026-10-21

The two NewWorld betas are forks of mainline client builds:

| Build | Linked | Code base | Compared against |
|---|---|---|---|
| graalnwb1 (`Graal-NW.exe`, MD5 88d1f84c…) | 2001-08-06 | 2.05 | 2.05 rev2 |
| graalnwb2 (`Graal-NW.exe`, MD5 af2d2106…) | 2001-10-03 | 2.1 test | 2.1 test 3 |

Both betas went through the same Ghidra pipeline as `build-diff-204-205.md` (Delphi compiler spec, RTTI names, switch-table recovery, feature export, `tools/build-diff/fdiff.py`).
Each beta was compared with its own base, so what's left over is the NewWorld delta. Every change below appears in **both** betas unless the text says otherwise.
This note is cleaned: it has no addresses and no decompiler output.

| Pair | Functions (old / new) | Identical | Changed | Only old | Only new |
|---|---|---|---|---|---|
| 2.05 rev2 → nwb1 | 6647 / 6494 | 5917 | 423 | 307 | 154 |
| 2.1 test 3 → nwb2 | 6703 / 6579 | 6051 | 354 | 298 | 174 |
| nwb1 → nwb2 | 6494 / 6579 | 5715 | 611 | 168 | 253 |

The nwb1 → nwb2 row is mostly the 2.05 → 2.1 base change. The NewWorld-specific code is the same in both betas.

## Classes

**Added (both betas):** `TLevelHeights`, `TAdventureBacktileArea`, `TDrawText`. Each is a plain `TObject` with no published methods.

**Removed (both betas):** `TComputer`, `TEditBaddy` (baddies), `TAdventureHorse` (horses), `TEditorChest`, `TChestEdit` (chests), `TAdventureCarry`, `TAdventureBall`, `TPos`, `TWebClient`.
This matches `readmenw.txt`: "horses are npcs now", "there are no built-in horses, carry object, freezeplayer etc. anymore, see the control-npc script for it". Baddies and chests are scripted too.

All other class differences between the two betas (`TEditNPC`, `TEditVariable`, `TEditorDefNPC`, `TSmilie` and others) come from the 2.05 → 2.1 base change and are not NewWorld code.

**Instance sizes:**

| Class | 2.05 rev2 | nwb1 | 2.1 test 3 | nwb2 |
|---|---|---|---|---|
| `TAdventureLevel` | 184 | **33968** | 184 | **33968** |
| `TGraalMap` | 76 | 96 | 256 (now a `TAdventureLevel` subclass) | 34060 |
| `TServerPlayer` | 336 | 320 | 364 | 348 |
| `TPlayer` | 800 | 760 | 836 | 792 |

## The 33968-byte level: a 65 × 65 height grid

`TAdventureLevel` in the betas is a 168-byte header followed by a **65 × 65 grid of doubles** (65 × 65 × 8 = 33800; 168 + 33800 = 33968).
The grid holds one height per tile corner of the 64 × 64 board, row-major with a stride of 65.

The 168-byte header has five fewer object lists than 2.05's (most likely the lists for the removed baddy, chest, horse and carry objects) and one new list, the backtile areas (see below). The other fields move to fill the gap.
The board is still a separate `TBoard` (4096 tiles), as in 2.05.

In nwb2 the 2.1 base had already made `TGraalMap` a subclass of `TAdventureLevel`, so the gmap inherits the 33968-byte level part and adds its own 92 bytes.

### Where the heights come from

Heights apply only when the current level is part of a gmap that has a height file, and only in one game mode (internal value 5; which mode that is wasn't confirmed). Otherwise every height reads as 0.

1. **Map corners.** When a gmap loads, the client looks for a sibling file named `<gmap base>_heights<ext>`, so `world.gmap` gives `world_heights.gmap`.
   (The shipped samples are named `..._heights.txt` next to a `.txt` map, for example `levels/test3d/test3dmap_heights.txt`.)
   The file is a CSV grid of (width + 1) × (height + 1) quoted entries, one per level corner:
   ```
   "100:36646","50:29374","100:97473","100"
   "50:4646","-30:342","-50:12393","-50"
   ```
   Each entry is `height` or `height:seed`. The seed in the entry at (x, y) belongs to the level whose top-left corner that is. The entry at the bottom-right corner (width, height) holds the map-wide seed.
2. **Level edges.** Each edge between two corners is filled by 1-D midpoint displacement out to 64 steps.
   The midpoint gets the average of the two ends plus `(random − 0.5) × 2 × amplitude`. The amplitude starts at 4.0 and is multiplied by 0.6 at each level of subdivision.
   The RTL random seed is set to the map-wide seed first. Neighbouring levels share their edges, so seams match.
3. **Level interior.** When a level is entered, its four 65-sample edges are copied from the map. The RTL random seed is set to that level's seed, and the interior is filled by recursive subdivision.
   Each step displaces the centre column and centre row, then recurses into the four quadrants. The amplitude starts at 4.0 × 0.6 and also shrinks by 0.6 per step.
   The terrain is deterministic: the same file always gives the same heights.
4. **Per-level control grid (`TLevelHeights`).** The gmap holds one `TLevelHeights` per level: an enabled flag and a 9 × 9 grid of doubles (one point every 8 tiles; 4 + 4 + 81 × 8 = 656 bytes).
   When the flag is set, each 8 × 8 cell gets a bilinear correction, so the generated surface passes exactly through the 81 control points.
   - nwb1 creates these objects but nothing in it sets the flag, so the control grid is inert there.
   - nwb2 fills them from a `HEIGHTS` … `HEIGHTSEND` block in the gmap parser (the generator form in `formats/grmap001.txt`). That block sets the flag.

### Using and changing the heights

- Drawing players and other level objects looks up the heights of the four corners of the tile under the object.
- **`setz x,y,w,h,z1,z2,z3,z4`** writes heights into the grid itself. Every grid point in [x, x+w] × [y, y+h] gets a bilinear blend of the four corner values. A zero width or height averages the corners instead.
  Points outside 0..64 are skipped.
- **`updateterrain`** re-clamps the view and redraws the terrain surface. The `readmenw.txt` workflow is "change `waterheight` / `groundheights[]`, then call `updateterrain`". Those two variables are in nwb2 and the 2.1 base, not in nwb1.

In 2.05 itself `setz`, `updateterrain` and `setbacktile2` are parsed but have no executor case (see `build-diff-204-205.md`). The betas are the builds where they do something.

## Backtile areas (`TAdventureBacktileArea`)

`setbacktile tile` sets one level-wide "back tile", the tile drawn behind trees and other foreground tiles.
**`setbacktile2 tile,x,y,w,h`** adds a 24-byte area record (tile, x, y, width, height) to the level's area list and redraws the board.
To find the back tile for (x, y), the client scans the areas in the order they were added and uses the first one whose rectangle contains the point. If none does, it uses the level-wide back tile.
Both commands work on the current level in play and on the editor's level.

## Deferred text (`TDrawText`)

While a frame is drawn, the client keeps a temporary list. Any nickname or chat text drawn during the scene pass is not drawn right away. It is queued as a 28-byte `TDrawText` holding the text, x and y as doubles (offset by the level's position in the gmap), and the colour.
After the scene (terrain, objects, overlays) is finished, the queue is drawn in one final pass and freed. Outside a frame, text is drawn immediately as in 2.05.
The likely purpose is to keep raised terrain and neighbouring levels from covering names. It matches the beta changelog line "Nicknames/Chat texts are displayed in the correct level."

## GS1 changes

The command table keeps the 2.05 layout: 12-byte records (name, a flags word, an argument-signature string).
It has **161 commands in 2.05 and nwb1** (`say` … `hide`) and **165 in nwb2**.
After it come a 4-name direction list (`up`, `left`, `down`, `right`), then, in both betas only, an **8-name NW time-variable list**:

| Variable | Range (from `readmenw.txt`) |
|---|---|
| `nwday` | 1…28 |
| `nwweek` | 1…40 |
| `nwyear` | 1000… |
| `nwweekday` | 1…7 |
| `nwmonth` | 1…10 |
| `nwtime` | 0…1439 (minutes) |
| `nwhour` | 0…23 |
| `nwmin` | 0…59 |

These are script variables (also usable as `#v(name)` message codes), **not commands**. The calendar has 28-day months, 10 months and 40 weeks. The server sends the time (packet 42), and "2000/5/1 realtime was 1000/1/1 graal time".

**String-list commands (nwb2 only):** `addstring`, `insertstring`, `removestring` and `deletestring` are inserted after `loadmap`, with the signatures shown here:

| Command | Arguments |
|---|---|
| `addstring list,text` | string, string |
| `insertstring list,index,text` | string, number, string |
| `removestring list,text` | string, string |
| `deletestring list,index` | string, number |

They go with `sarraylen(list)`, `lindexof(list,text)` and `#I(list,i)`, which are also only in nwb2. Lists are stored as normal string flags in comma form (`numbers="12 34",567,"8,9"`).
nwb1 has none of this. Its `readmenw.txt` doesn't mention string arrays either; the section appears only in nwb2's copy.

**Executor cases.** These counts compare the betas with their bases. They are the same for both pairs, apart from nwb2's four string commands.

- Live in the betas, ignored in the base: `setfocus`, `resetfocus`, `setbacktile`, `drawovertrees`, `setbacktile2`, `setz`, `updateterrain`.
- Parsed but ignored in the betas, live in the base: `removecompus`, `putcomp`, `putnewcomp`, `hitcompu` (baddies);
  `puthorse`, `takehorse`, `takeplayerhorse`, `removehorse` (horses); `carryobject`, `throwcarry`, `takeplayercarry`;
  `setsword`, `hidesword`, `setbow`; `freezeplayer`; `enabledefmovement`, `disabledefmovement`; `toinventory`; `followplayer`.
  The control NPC script (`controlnpc.txt`) takes over movement, swords, carrying and horses.

## Packets

### Server → client (TCP)

The receive switch covers 0…168 in 2.05 and 0…169 in 2.1. Compared with its base, each beta **drops six receivers**:

| Id | 2.05 meaning | Why it goes |
|---|---|---|
| 2 | BADDYPROPS | no built-in baddies |
| 4 | LEVELCHEST | no built-in chests |
| 17 | HORSEADD | horses are NPCs |
| 18 | HORSEDEL | horses are NPCs |
| 154 | FREEZE | no built-in freeze; `freezeplayer` is gone too |
| 155 | UNFREEZE | as above |

Everything else in the base's receive set is still there. nwb2 also has ids 49 and 169, but they come from the 2.1 base.

### Client → server (TCP)

Several 2.05 senders have no matching function in nwb1: HORSEADD (7), BADDYPROPS (15), BADDYHURT (16) and OPENCHEST (20).
The bomb, arrow, item-add and item-take senders match 2.05 exactly.
"No match" is an upper bound (see the matching caveat in `build-diff-204-205.md`), but it agrees with the removed classes.

### Peer-to-peer UDP

The UDP receive switch covers 0…26 in 2.05 and 0…27 in 2.1. Both betas drop **16 and 17**, the horse add/remove pair that mirrors TCP 7/8 (see `protocol/udp-p2p.md`).
They keep 0 and 10–15 and 18 up to the end of the range. nwb2 keeps the 2.1 addition, 27.

## List server

Both betas hide the list-server host with the same DES string as 2.05 (`www.graalonline.com`; see `des-and-hidden-strings.md`). They build the port and list name one character at a time, as 2.05 does:

| Build | Port | List name sent with id 0 |
|---|---|---|
| 2.05 rev2 | 14921 | `newmain` |
| nwb1 | 14921 | `newworld` |
| 2.1 test 2/3 | 14922 | `newmain` |
| nwb2 | 14922 | `newworld` |

So the port comes from the code base (14921 in the 2.05 line, 14922 from the 2.1 tests on), and the list name is the only NewWorld change.
The betas log in to game servers with the token `G2N15041` instead of the mainline `GNW03081` (see `build-catalogue.md`).

## Live lab runs (2026-10-30)

Both betas were run under Wine (32-bit prefix, virtual X display) in a network namespace whose hosts file points the GraalOnline names at a local stub. The stub answers as list server (14921 to 14923) and as game server, and logs every packet. The 2.1 test 3 build was run the same way for comparison. The per-version results are in `version-profiles/141-217.toml` (`vnwb1`, `vnwb2`).

### List server

| Build | Port | What it sends |
|---|---|---|
| nwb1 | 14921 | id 0 `newworld` only |
| nwb2 | 14922 | id 0 `newworld`, then id 1 with account and password (two GSTRINGs) |
| 2.1 test 3 | 14922 | id 0 `newmain`, then id 1 with account and password |

So sending the account to the list server begins with the 2.1 tests (September 2001), not 2.17. nwb1, on the 2.05 code, does not do it. nwb2's start window is GraalOnline-themed with Account and Password fields. In one run it sent 23 characters of a 28-character password; the cut-off was not pinned down.

### Game server login

Both betas send client type 0, the key byte, `G2N15041`, the account and the password, then LANGUAGE (37) `English`. Their first props are the same six as 2.05: NICK (0), HEADGIF (11), COLORS (13), STATUS (18), UDPPORT (31) and ADDITFLAGS (33).

- **COLORS has seven bytes**, the same in every run, where 2.05 has five. Both betas' prop parsers read eight colour bytes. A server must take the length from the prop and must not echo seven bytes to a client that reads a different count.
- HEADGIF comes without an extension (`headalgo000`).
- STATUS has a new bit, 0x20.
- The first login sometimes stalled with the level drawn but no HUD or player and no props sent. Logging in again fixed it every time.

### After joining

- **Files.** nwb1 asks WANTFILE `shield1.png` and UPDATEFILE `bodynw.png` and `timenums.png`. nwb2 also asks for `idle.gani` and `headalgo000`. Neither asks for the sword, bomb and bow images 2.05 asks for.
- **Movement.** GANI (10) goes out as a string. While idle the client re-sends `idle` about every 100 ms, because the control NPC calls `setani` each tick (2.05 sends it only now and then). Walking sends X and Y in half tiles plus SPRITE, and nwb2 re-sends `walk` on each step.
- **Keys.** S does nothing online, so a server has to give the sword as an NPC weapon. A plays the grab animation. The control NPC comes from the local `controlnpc.txt` as the weapon `Control-NPC`, added when the player is created.
- **Time (packet 42).** The payload is a GINT4: minutes since 1000/01/01 00:00 on the NW calendar (28-day months, 10 months, 280-day year). A value of 162310450 showed as 1402/06/16 14:10 on the HUD clock.
- **Offline Training** in nwb1 runs without a server (HUD 150/150, clock 1000/01/01).

### Client → server set

A scan of the send sites (same method as `version-profiles/README.md`) shows both betas drop seven ids that their bases send: 7, 8, 11, 15, 16, 17 and 20 (horse add/delete, throw carried, baddy props/hurt/add, open chest). That widens the four listed under Packets above. The prop parsers and writer otherwise match each base, and there is no baddy-props parser.

## Corrections to other notes

- `build-catalogue.md` credited "string arrays" to nwb1. They are nwb2-only. nwb1's distinctive features are the terrain heights, backtile areas, deferred text and NW time variables.
- The 2.05 GS1 table has 161 commands. A count of 163 reads two entries past the end (`up` and `right` from the direction list that follows).
