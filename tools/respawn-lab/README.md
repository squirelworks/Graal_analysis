# Respawn lab scripts

Used for `client-internals/board-respawn.md`. Everything runs in the Wine lab from `tools/lab-setup.md` (loopback-only namespace, Xvfb :9).

| Script | Use |
|---|---|
| `mklevel.py out.nw` | Writes a grass level with bush, sign, pot, stone, black stone and tall grass in a row at y 26, and six bushes at y 33. |
| `boardscan.py <pid>` | Finds the 64×64 i16 boards in a running client by the y-26 row pattern. The board base is the hit minus `(26*64+20)*2`. |
| `boardwatch.py <pid> <secs> out.jsonl <base>...` | Logs every tile change with a timestamp (10 ms poll). |
| `pos.py <pid>` | Prints the 2.05 rev 2 player x, y. |
| `g2cli.py` | Minimal gen-2 (`GSERV014`) client: `u16be` + zlib frames, `chr(id+32)` lines. |
| `gs13_respawn.py out.jsonl N` | Two `g2cli` sessions against GServer13: shape tests, then N 2×2 changes, and logs every `PLO_BOARDMODIFY` both sessions get. |
| `arrays_dump.py arrays.dat` | Prints the cut, lift and push/pull tables. |

The GServer13 account is a load-only `guest`/`guest` made in the server's own account editor. No real account is involved.
