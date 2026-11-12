# Gmap neighbours on 2.x: which level a board lands on

Date: 2026-11-12. Clients read: 2.17.1, 2.22 and 2.31 (Windows), with the 2.05 rev 2 receive path for comparison. Server read: GServer-v2 `beta4` as merged into `seihai-gserver-v2` (`PlayerClient`, `PlayerClientOriginal`, `PlayerLogin`, `msgPLI_ADJACENTLEVEL`). Tags: **[bin]** read from the client binaries · **[srv]** server source · **[cap]** lab capture · **[inf]** inferred.

## The question

A server sends the `.gmap` file before the warp so a 2.x client stops hanging on the loading screen. The client then sends `PLI_ADJACENTLEVEL` (35) for each neighbour, as it should. But each neighbour's tiles also overwrite the tiles of the level the player is standing in.

## Short answer

The client does not read the level from the board message. Level data (the board in `RAWDATA` + `BOARDPACKET`, `LEVELBOARD`, links, signs, chests, `LEVELMODTIME`, `BOARDMODIFY`) always goes to the level named by the **last `PLO_LEVELNAME` (6)**. Neither the board nor the reply to 35 carries a level name or a gmap position. The client finds the cell from its own 3x3 grid. **[bin]**

So a reply to 35 must start with `PLO_LEVELNAME <neighbour name>` before the board. If it does not, the board goes to whatever level was named last. After a warp that is the player's own level, which gives exactly the overwrite.

GServer-v2 gets this wrong for clients that log in with the **classic login type 0**, which includes 2.17 and the 2.1 test builds. These get `PlayerClientOriginal`. Its level send writes `PLO_LEVELNAME` only once per session, so the replies to 35 come with no name at all. Clients with the gen-5 login (2.22, 2.3, 2.31) get `PlayerClient`, which frames every reply with the name. **[srv]** Neither ordering nor a missing gmap-membership packet causes it: the neighbour's name is simply never sent.

## How the client picks the target level **[bin]**

The builds keep two level pointers, as 2.05 does (`packet-layouts.md`): the *named level* and the object level that NPC packets use. The `LEVELNAME` rule below was read in all three builds. The board, link, sign, chest, modtime, warp and 3x3-grid rules were read in 2.22, which uses the same `LEVELNAME` logic as 2.17.1.

- **`PLO_LEVELNAME` (6)** sets the named level by looking the name up in the client's list of level objects. The lookup drops any path before the last `/` or `\` and ignores ASCII case. It never creates a level: an unknown name gives "no named level", and the level data that follows is dropped.
- The name ending in `.gmap` is a special case:
  - 2.17.1 and 2.22: if the named level already is the player's own level, nothing changes. Otherwise the client looks up the gmap name like any other level name. That finds nothing, so the named level is cleared. **[bin][inf]** (The gmap is kept in a separate list. Nothing in the level list carries a `.gmap` name.)
  - 2.31: if the name is the player's current gmap, the named level is set to the player's own level. Any other `.gmap` name is ignored.
- **`BOARDPACKET` (101 after `RAWDATA`)** first empties the named level's links and signs. It then copies the 64x64 tiles into the named level and redraws that level's cell, if it has one in the 3x3 grid. With no named level, the board is dropped.
  - The one exception is a warp still waiting for its level. When the named level is the player's level, or the last `LEVELNAME` text equals the warp's level name, the board finishes the warp and goes to the player's level.
- **`LEVELBOARD` (0)** follows the same rule: it finishes a waiting warp, and otherwise applies its board runs to the named level.
- **`LEVELLINK` (1), `LEVELCHEST` (4), `LEVELSIGN` (5), `BOARDMODIFY` (7) and `LEVELMODTIME` (39)** all act on the named level and do nothing when there is none.

## What the client does before it sends 35 **[bin]**

The client keeps a 3x3 grid of level objects around the player. Each time it rebuilds the grid, it finds the player's current level name in the gmap's `LEVELNAMES`, which gives the cell. Then it takes the eight neighbour names from the same table. The centre slot is the player's own level.

For every neighbour slot it has no level object for, an online client:
1. creates an empty level object under the `LEVELNAMES` name,
2. adds it to the level list that `PLO_LEVELNAME` searches,
3. sends `PLI_ADJACENTLEVEL` (35): the level's cached modtime (5 bytes) followed by that name, without any path and in lower case.

The level object therefore exists before the reply arrives. `PLO_LEVELNAME` with the name the client sent (or the same name in any case, or with a path) finds it.

## The warp and the `.gmap` file **[bin]**

- `PLO_PLAYERWARP2` (49) with a `.gmap` name: if the gmap's `LEVELNAMES` is loaded, the client clamps the cell bytes to the grid and swaps the gmap name for that cell's level name. It then **finishes the warp at once, without waiting for a board**: the player's level becomes that level object, created if needed. It also clears the named level and sets the last `LEVELNAME` text to the gmap name.
- If the `.gmap` is not on the client's disk when 49 arrives, the gmap loads with no `LEVELNAMES`. The handler stops there and leaves the warp waiting under the gmap name. That is the loading-screen hang. Having the file on disk before the warp avoids it.
- `PLO_PLAYERWARP` (14) with a `.gmap` name takes the same path in 2.22 but has no cell bytes. The client always picks the **first** entry of `LEVELNAMES`, the top-left cell. 2.17.1, 2.22 and 2.31 all handle 49 (and so do the 2.1 test builds, `../client-internals/decomp-findings-2026-10-24-c/06-handler-changes-by-build.md`). A server should send 49, not 14, whenever the target is a gmap.

## What GServer-v2 sends **[srv]**

- **Gen-5 login (2.22, 2.3, 2.31) → `PlayerClient`.** Every level send, including the reply to 35, is: `LEVELNAME <sub-level>`, then a blank `LEVELBOARD` on the first load, the board, links, signs, chests (or an empty `LEVELBOARD` when the board is skipped), `LEVELMODTIME`, and `LEVELNAME <the player's level name>`, which is the gmap name while on a gmap. A gmap warp uses 49. A real 2.22 handled this sequence in the lab: the neighbour boards went to the neighbours (`../client-internals/feature-specs/06-gmap-overworld.md`, capture of 2026-10-24). **[cap]**
- **Classic login type 0 (2.17 and older, including the 2.1 test builds) → `PlayerClientOriginal`.**
  - A warp always uses 14, so on a gmap the client lands in the top-left cell whatever the server thinks.
  - The level send writes `LEVELNAME` **only for the first level of the session**. The reply to 35 comes with the same shape, so it is: board, links, signs, `LEVELMODTIME`, chests. It has no name before it and none after it.
  - The client has no other way to know where these belong, so they land on the last named level. After the first level that is the player's own level. Each neighbour's board replaces the current tiles, and its links are added to the current level, so a player can be warped by a neighbour's link. Its modtime is stored as the current level's.
- The trailing `LEVELNAME <gmap>` that `PlayerClient` sends after a neighbour is right for 2.31. On 2.17.1 and 2.22 it leaves no named level (see above). Level data that later arrives without its own `LEVELNAME` is then dropped until the next one. **[bin][inf]** Sending the player's current **cell level** name instead puts the named level back on the player's level on all three builds.

## The sequence that works on 2.17.1, 2.22 and 2.31

For each `PLI_ADJACENTLEVEL` (35):

```
PLO_LEVELNAME     <neighbour level name, as the client sent it>
[PLO_RAWDATA + BOARDPACKET, PLO_LEVELLINK..., PLO_LEVELSIGN...]   when the client's copy is stale
[PLO_LEVELBOARD (empty)]                                           when it is not
PLO_LEVELCHEST..., PLO_LEVELMODTIME
PLO_LEVELNAME     <the player's current cell level name>
```

On entering the gmap: send the `.gmap` before 49 (or be ready for the client to ask for it and warp again), use 49 for every client that handles it, then send the player's level framed the same way.

For GServer-v2 the fix is in `PlayerClientOriginal`. It needs to put `PLO_LEVELNAME <level>` before the board on every send, not just the first one, and end a neighbour reply with the player's level name. The other choice is for `msgPLI_ADJACENTLEVEL` to add the two names itself for type-0 clients. It also needs to pick 49 by client version rather than by login type.

## Limits

- Static read of the three binaries plus the GServer-v2 source. The overwrite was not reproduced in a lab, and no 2.17 session on a GServer-v2 gmap has been captured.
- To confirm: in a loopback lab, run a 2x2 gmap with a 2.17.1 client, one capture with stock `PlayerClientOriginal` (expect the overwrite) and one with the framing above (expect correct neighbours). Do the same with a 2.22 client to check that the trailing cell name keeps `BOARDMODIFY` and chest updates for the current level working.
- 2.05 rev 2 reads `LEVELNAME` and `LEVELBOARD` the same way (`packet-layouts.md`). It sends 35 for its `bigmap.txt` neighbours, not for gmaps, and was not checked further here.
