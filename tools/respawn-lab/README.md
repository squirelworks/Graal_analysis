# Respawn lab scripts

Used for `client-internals/board-respawn.md`. Everything runs in the Wine lab from `tools/lab-setup.md` (loopback-only namespace, Xvfb :9).

| Script | Use |
|---|---|
| `mklevel.py out.nw` | Writes a grass level with bush, sign, pot, stone, black stone and tall grass in a row at y 26, and six bushes at y 33. |
| `boardscan.py <pid>` | Finds the 64×64 i16 boards in a running client by the y-26 row pattern. The board base is the hit minus `(26*64+20)*2`. |
| `boardwatch.py <pid> <secs> out.jsonl <base>...` | Logs every tile change with a timestamp (10 ms poll). |
| `pos.py <pid> <player-global-hex>` | Prints the 2.05 rev 2 player x, y. The player global is found on a live client (addresses are not kept in the repo). |
| `g2cli.py` | Minimal gen-2 (`GSERV014`) client: `u16be` + zlib frames, `chr(id+32)` lines. |
| `gs13_respawn.py out.jsonl N` | Two `g2cli` sessions against GServer13: shape tests, then N 2×2 changes, and logs every `PLO_BOARDMODIFY` both sessions get. |
| `arrays_dump.py arrays.dat` | Prints the cut, lift and push/pull tables. |

The GServer13 account is a load-only `guest`/`guest` made in the server's own account editor. No real account is involved.

## Finding the addresses

`pos.py` needs the static global that points at the player object. Addresses are not kept in the repo, so find it again on your own client (2.05 rev 2 for `pos.py`; 2.22 works the same way, see `live-runs/2gta-222-2026-10-30/README.md`). The two scanners are in `live-runs/2gta-222-2026-10-30/tools/`. They only read memory (ReadProcessMemory, no debugger), so run them with a Windows Python, under Wine in the lab.

1. Start the client in the lab, join a level and stand still on a spot whose tile x, y you know.
2. Snapshot every plausible position value: `mem.py snap <pid> s0.pkl`. It keeps every double between 0 and 4096 that is a multiple of 1/32.
3. Narrow it down by moving. Step left and stop, then run `mem.py filter <pid> s0.pkl s1.pkl dec`. Step right, then `filter … s1.pkl s2.pkl inc`. Stand still, then `filter … s2.pkl s3.pkl same`. Repeat until a few addresses are left, and check them with `mem.py show <pid> s3.pkl`. x moves 0.5 tile per 50 ms tick, and y is the next double, 8 bytes on.
4. The player object starts 4 bytes before x, with its VMT pointer first. Run `findptr.py <pid> <x-address> 8`. It lists the dwords in the exe image that point just below x. The hits reported with x at +4 are the static player globals: 2.22 has two, so use the first.
5. Confirm with `pos.py <pid> <global>` (`pos.py` reads `/proc/<pid>/mem`, so run it from the Linux side on the Wine process). Walk and check that x changes. Then restart the client: the global stays the same, because it is in the exe image, but the heap object it points at moves.
