# Status

Source image: Mac PowerPC `Graal`, Ghidra project `MacGraal_v304`. Notes are under `teardown/`. The client is `python/client.py`. It uses the standard library.

## What it can do today

- Build the game login line from `login.md`: id 5, `G3D28015`, two length-prefixed strings, newline, and the first-record extra byte.
- Build the id-37 follow-up, the lister hello `G3D30123newmain`, the lister id-1 line, and a file-ask id `0x17` that refuses `.gft`.
- Parse an inbound player buffer the way a client routine does for ids 0–10, and stop on any other id.
- Load a local `GLEVNW01` file, read `BOARD` runs with the 62-character alphabet, and store `(index1 << 6) + index2` on a 64×64 grid.
- Step `up` `down` `left` `right` and refuse a coordinate outside 0..63.
- Stay off the network unless `--stub` or `--host` is set. `--stub` is a localhost thread that reads one line and answers with inbound id 0.

Checked with `python/examples/tiny.nw`, four steps, and `--stub`.

## What is still a stub

- The two login strings and the id-37 payload have no recovered names. The flags default to `guest` and empty.
- Id 4’s optional image string is parsed as one byte, same as ids 0–3 and 5–7.
- The outer flush (big-endian length, mode byte, LCG, and the two unrecovered transforms) is described in `teardown/framing.md` and is not applied on the socket.
- File packets `0x22`, `0x5D`, `0x9B`, and `0x9C` are documented and not sent.
- NPC, baddy, chest, sign, link, and heights sections are recorded by name and not interpreted.
- Sword, shield, and head encoders from a client routine are not called.

## What would make a level play offline

A step function that this image does not contain: which tile values block, how far one `moveUp` moves, and how `walk` / `walkslow` choose a frame. The 64-bound and the `BOARD` grid are already loaded. Gani playback (`SCRIPTEND` and the verb list) and the `Gui*` draw path are names only.

## What would make a level play online

The LCG words at connection `+0x08`, `+0x10`, and `+0x0B`, plus whatever a client routine and a client routine do, so the flush matches a client routine. Also the real contents of login strings A, B, and the id-37 buffer, and a server reply the client treats as success. No such reply opcode was recovered. Inbound ids stop at 10.
