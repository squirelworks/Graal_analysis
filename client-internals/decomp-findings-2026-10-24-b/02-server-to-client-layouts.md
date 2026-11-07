# Server -> client payloads above id 48 (and 25, 39, 41, 44, 47, 156, 168-189): 2.17.1, 2.22, 2.31

Source: the receive dispatchers of the 2.17.1, 2.22 and 2.31 clients, read from the disassembly. Full table: `version-profiles/plo-layouts-217-231.tsv`. Handled-id set per build: `version-profiles/plo-handled-ids-by-build.tsv`.

## Dispatcher shape (all builds)
- id = first byte - 0x20; bound check; byte-index table; dword jump table; every unhandled id shares one default arm that does nothing.
- Dispatch bounds: 2.17.1 up to id 185 (bound 0xb9); 2.22 up to 186 (0xba); 2.31 up to 189 (0xbd).
- Number encodings read by the handlers: GCHAR = byte-0x20; GSHORT = 7-bit shifts (b0<<7 + b1); GINT3 shifts 14,7,0; GINT4 21,14,7,0; GINT5 28,21,14,7,0. Text payloads are the rest of the line. Several "comma text" ids go through the TStrings comma-text parser (double quotes allowed).

## Handled ids above 48
- 2.17.1: 49, 68, 69, 75, 100, 150, 151, 153-156, 165, 166, 168-185. (79 handled ids in total.)
- 2.22: same + 186. (80 total.) Id 7 is a three-instruction stub forwarding to a helper (in 2.17.1 the body is inline); wire format of 7 unchanged as far as the diff shows.
- 2.31: the 2.22 set + 84 + 189, minus 44. (81 total.)
- Ids 50-67, 70-74, 76-83, 85-99, 101-149, 152, 157-164, 167 are unhandled in all three (default arm). 152 and 167 are NOT handled in any of them.

## Layouts, short
(see `version-profiles/plo-layouts-217-231.tsv` for the full text and version gates; "dec" = decoded from the binary)
- 25 SIGNATURE: GCHAR v. v=1 quits; v=0 quits unless host is the loopback address; other values ignored.
- 39 LEVELMODTIME: raw rest passed to active gmap/level object (needs an active level).
- 41 STARTMESSAGE: raw RTF/HTML text, cached as servermessage.rtf/.html, shown in viewer.
- 44 HASNPCSERVER: no payload, 2.17/2.22 only, gone in 2.31.
- 47 STAFFGUILDS: comma list.
- 49 PLAYERWARP2: GCHAR x2, GCHAR y2, GCHAR z (unused here), GCHAR gmapX, GCHAR gmapY, level name. x,y halve (value/2.0). gmapX/Y only used for .gmap levels, clamped to the grid.
- 68/69 LARGEFILESTART/END: raw name; 84 LARGEFILESIZE (2.31 only): GINT5.
- 75 PROFILE: repeated GCHAR n + n chars; first field = account, rest = lines.
- 100 RAWDATA: GINT3 length.
- 150 NPCDEL2: GCHAR n, n-char level name, GINT3 npc id. 151 HIDENPCS: none (removes NPCs 1..999 of active level).
- 153 SAY2: text. 154/155 FREEZE/UNFREEZE: none. 156 SETACTIVELEVEL: name, .gmap handled specially; 2.31 adds a follow-up step.
- 165 MOVE: GINT3 id + rest. 166 SHOWIMGNPC: GINT3 id + props. 189 MOVE2 (2.31): same shape as 165, extra flag.
- 168: payload ignored (local reset). 169: URL text. 170 GCHAR flag. 171/172: comma text txt,png,x,y (needs >=4 fields). 173 text. 174 GCHAR flag.
- 175 SHOOT: GSHORT player id + rest, only when in the active level.
- 176/177: mode switches, no payload. 178 SERVERWARP: comma text with >=4 fields, field 0 unused, 1 = name, 2 = host, 3 = port (lab-confirmed on 2.31, `08-lab-findings-levelchange-24-178.md`).
- 179 RPGWINDOW: text. 180 STATUSLIST: text. 181: GSHORT id + GCHAR toggle.
- 182 LISTPROCESSES: no payload; client replies PLI 44 with its process list. 183 HASPROCESSRUNNING: names; client replies PLI 45 = GCHAR 0/1 (whether the server's string occurs in its own process list). (These are PLI ids sent BY the client; the server-side PLO 44 is something else.)
- 184 TAKESCREENSHOT: file name, only ".png" accepted, saved under a screenshots folder.
- 185 BOARDHEIGHTS: GCHAR mapX, mapY, blockX, blockY, w-1, h-1 then w*h cells of two raw bytes, value = (b0-0x20-50) + (b1-0x20)/128.0.
- 186 BOARDMODIFY2 (2.22+): GCHAR mapX, mapY, x, y, w, h then w*h GSHORT tiles row-major (bytes after the tiles are ignored padding: lab-tested with injected frames, see `07-lab-findings-46-186-200.md`).

## Differences 2.17.1 -> 2.22 -> 2.31 that change behaviour or ids
- 2.17.1 -> 2.22: new id 186; id 7 refactored into a helper; every other handler's wire format identical after diffing 37, 42, 49, 75, 150, 151 (only local-variable/offset noise). Tamper check re-sent on level change (new). Login token changes GNW22122 -> GNW03014.
- 2.22 -> 2.31: id 44 no longer handled; new ids 84 and 189; id 6 (level name) now also compares with the current level name; 68 clears the stored file size; 156 gets an extra step; object offsets shift by 0x40 in the player/level classes (irrelevant on the wire). Timer-driven PLI 39/24 and PLI 46 added (see 03).
