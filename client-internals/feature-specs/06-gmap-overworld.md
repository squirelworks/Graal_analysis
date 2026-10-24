# 06 GMAP overworld and map links

Snapshots read: Graal_analysis `8da6800` (`formats/gmap.md`), Seihai `06aacfd`, GServer-v2 (`TMap.cpp`, `TPlayer.cpp` `setLevel`/`sendLevel`/`msgPLI_ADJACENTLEVEL`, `TPlayerProps.cpp`, `TLevelLink.cpp`, `TPlayerLogin.cpp`).
Folded here from the public-server report: **PLO_BIGMAP 171, PLO_MINIMAP 172, PLO_SETACTIVELEVEL 156, PLO_LEVELMODTIME 39**.

## Three different "maps" (do not mix)
1. **Level links** (`PLO_LEVELLINK` 1): `dest x y w h newx newy` text per link. Walking into the rectangle makes the client send `PLI_LEVELWARP` (0) / `PLI_LEVELWARPMOD` (30). `newx`/`newy` may be `playerx`/`playery`. `TLevelLink::parseLinkStr` accepts level names with spaces. Seihai parses PLO 1 and has `send_levelwarp`.
2. **bigmap-style server maps** (`maps =` option, `bigmap.txt` text grid, `MapType::BIGMAP`): server only. It lets the server know which levels are adjacent so players are visible and can chat across edges. The client does nothing special. Level-to-cell data comes from `TMap::loadMapLevels`.
3. **GMAP** (`gmaps =` option, `GRMAP001` file, `MapType::GMAP`): the client walks continuously across level borders.
Separate again: `bigmap =` / `minimap =` options (4 comma fields `text,image,x,y`) make the server send `PLO_BIGMAP` (171) and `PLO_MINIMAP` (172) at login (2.1+, in `sendLoginClient`). These are overlay settings for the client's map screen and minimap: file names to fetch plus a default x,y for heads of players off the map. Harmless to skip. The notes warn that setting `bigmap` breaks gmaps.

## GMAP wire behaviour **[srv]**
- File keys (`formats/gmap.md`): WIDTH, HEIGHT, LEVELNAMES block (quoted CSV rows), MAPIMG, MINIMAPIMG, NOAUTOMAPPING, LOADFULLMAP, LOADATSTART.
- Entering a gmap level (2.1+ clients): `PLO_PLAYERWARP2` (49): `c x*2, c y*2, c z+50, c gmapX, c gmapY` + gmap file name. 2.05 has no handler for 49 and gets plain `PLAYERWARP` (14).
- In `sendLevel`: after the level's board, links, chests, horses, baddies, the server sends `PLO_LEVELNAME` (6) with the **gmap name** (not the level) and, when this is the first level, `PLO_SETACTIVELEVEL` (156) with the gmap name before the NPC props, then `PLO_GHOSTICON` 0.
- Neighbours: the client sends `PLI_ADJACENTLEVEL` (35) `i5 modtime + level`; the server replies with that level's data (`sendLevel(..., fromAdjacent)`), then restores `LEVELNAME` to the gmap. The 3x3 neighbourhood is preloaded this way.
- Crossing a border is **client-driven**: the client updates `PLPROP_GMAPLEVELX` (43) / `GMAPLEVELY` (44) and X/Y in gmap coordinates. For each of those props the server looks up the new level name in the map (`TMap::getLevelAt`), leaves the old level and enters the new one with an unknown mod time.
- Props: `PLPROP_CURLEVEL` carries the gmap name while on a gmap; X/Y inside a gmap level are level-local plus the cell; newer clients (2.30+) also send X2/Y2/Z2 pixel props (78-80).
- UDP id 24 ("entered level") goes to peers in the 3x3 neighbourhood (see 07).
- `PLO_LEVELMODTIME` (39): `i5 modtime` after each full level; keep it per level so that the next entry can use `LEVELWARPMOD` (30) or `ADJACENTLEVEL` with a cached board.

## Lab capture of a real 2.22 client crossing gmap edges, 2026-10-24 **[cap]**
Setup: a 2x2 gmap of open-grass levels; the client walked east, south, west and north across all four edges.
- **Login.** The server sends `PLO_PLAYERWARP2` (49) with x*2, y*2, z+50, gmap cell x, gmap cell y, then the **gmap name** (not a level name). Then `PLO_LEVELNAME` (6) with the level, a second `6` with the gmap file name, 174, 10, and `156 SETACTIVELEVEL` = the gmap name. The `.gmap` file arrives as a file transfer (rawdata + file) because the client asks for it. The first big server frame also carries the neighbour levels' boards. The client sends `PLI_ADJACENTLEVEL` (35, `i5 modtime` + name) at login for the three neighbour levels (modtime 0 on a cold cache).
- **A crossing uses only normal props; there is no level-warp packet.**
  - The client sets the flags `gr.x` / `gr.y` (`PLI 18`, flag set) on every half-tile step. They carry the **global** position: local + 64 * cell, so they run past 63.5. (Earlier notes in `version-profiles/2.22-2.31.md` say these flag sets come from the server's movement NPC rather than from client code; both fit if the server-sent movement weapon runs inside the client and the client sends the resulting flag sets. The capture cannot tell which.)
  - East: in the frame where global x reaches 64.0 the client sends `PLI 39` (the tampercheck constant, see 08), `gr.x=64`, and a props message with local X = 0 and `GMAPLEVELX` (prop 43) = 1.
  - South: the frame at global y 64.0 carries `PLI 39` and the flag only; the props message with local Y = 0.5 and `GMAPLEVELY` (prop 44) = 1 follows in the next half-step frame, because position props go out only on whole-tile steps.
  - West: `PLI 39` goes out at global x 63.5; the next props message has X = 63.0 and prop 43 = 0. North is the same with Y = 63.0 and prop 44 = 0.
  - Rule: local = global - 64 * cell; the cell prop changes in the same props message as the wrapped coordinate; position props use whole-tile steps; **2.22 re-sends `PLI 39` on each crossing**.
- **Server answer to each crossing** (one frame): `6` new level name, `39` (server to client level mod time, only when the client does not have the level cached), `0` (an empty board packet), `6` gmap name, `174`, `10`, `156` gmap name. A second visit to a level omits the server's `39`.
- The merged Seihai, connected to this lab, treated the gmap name in `PLO_PLAYERWARP2` as a level name and requested `<gmap>.nw`, which does not exist. Gmap support (this spec) is still not implemented; the above is the data it needs.

## Seihai today
- Profile flag `levels.gmap` exists (set per version profile in `profile.rs`; check which ones before relying on it); the `LEVELNAMES` text is not parsed. PLO 49, 171, 172, 156, 39, 6 (LEVELNAME) is handled; PLI 35 is never sent. The rest are not implemented. 156/39/171/172 are counted as unhandled in the public-server report.
- `draw_minimap` draws a 64x64 level minimap (not the gmap).
- Single-level warps (`PLAYERWARP` 14, `send_levelwarp`) work.

## Steps for Claude
1. Add `formats::gmap` parser: `GRMAP001`, WIDTH, HEIGHT, LEVELNAMES rows (quoted CSV, lower-cased lookup), MAPIMG/MINIMAPIMG, flags. Test with a hand-written 2x2 file.
2. Handle PLO 49 (decode the layout above) to enter a gmap; store `gmap_name`, `cell_x`, `cell_y`. Handle PLO 6 on a gmap as "the map name". Store 156 and 39 (modtime per level).
3. Fetch the `.gmap` with WANTFILE if absent, then the levels of the 3x3 neighbourhood: send `ADJACENTLEVEL` (35) for each neighbour.
4. Render neighbour levels offset by 64 tiles; compose collision across seams. Position in world = cell*64 + local.
5. On crossing an edge, send `PLPROP_GMAPLEVELX/Y` (43/44) plus the wrapped X/Y in one prop message. Let the server answer with the new level data; keep the old level data for one tick to avoid flashing.
6. Parse 171/172 into settings (file names + default x,y); fetch images only if a map screen exists. Otherwise ignore.
7. Gate everything on `profile.levels.gmap` so 2.05 keeps working.

## How to test
- Lab: copy a 2x2 set of lab levels, write `lab2x2.gmap`, set `gmaps = lab2x2.gmap` in a **copy** of the lab `serveroptions.txt`, restart the lab gserver, log in with a 2.22 client (Seihai `--version 2.22`), warp into one of the levels and walk across an edge. Confirm PLO 49, 6, 156 and the neighbour level packets in the decoded frames. Display :9 only.
- Unit tests for the parser and for the cell/world coordinate maths.

## NEEDS
~~a lab capture of a real 2.22 client crossing a gmap edge~~ Done 2026-10-24 (see above; 2.22 has no X2/Y2 props). Still open: a 2.31 crossing (it has X2/Y2/Z2), and how the 2.17+ client lays out the gmap overview on the map screen.
