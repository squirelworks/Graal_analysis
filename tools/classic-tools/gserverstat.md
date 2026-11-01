# gserverstat and gserverstat2

Date: 2026-11-01

Two ELFs from the 1999 gserver tree, plus the `statmaker` shell script that runs them. They print an HTML leaderboard on standard output. Neither image imports a socket call. **[bin]**

`account13.py` reads and writes the account blob and builds a page row. The row has no password.

## What the operator runs

`statmaker` loops forever. Each step runs one ELF with one mode name and moves the HTML into a `stats/` tree (admin modes under `stats/admin/`). It sleeps 10 seconds between pages and 600 seconds at the end of the loop. **[file]**

| Program | Modes the script asks for | Page |
| --- | --- | --- |
| `gserverstat` | kills, deaths, rupees, highap, lowap, onlinetime | `stats/<mode>.html` |
| `gserverstat2` | swordpower, maxpower, glovepower, bombpower, shieldpower, highap | `stats/admin/<mode>.html` |

Both images contain the same 14 mode names, matched without regard to case. With no argument the mode is kills. **[bin]**

| Index | Name | Field, highest first unless noted |
| --- | --- | --- |
| 0 | Maxpower | max hearts |
| 1 | Power | current hearts |
| 2 | Rupees | rupees |
| 3 | Arrows | arrows |
| 4 | Bombs | bombs |
| 5 | Glovepower | glove |
| 6 | Bombpower | bomb power |
| 7 | Swordpower | sword |
| 8 | Shieldpower | shield |
| 9 | Kills | kills |
| 10 | Deaths | deaths |
| 11 | Onlinetime | online seconds |
| 12 | Highap | alignment, highest first; a tie keeps fewer kills first |
| 13 | Lowap | alignment, lowest first; a tie keeps more kills first |

## What it reads

The working directory is the server directory. The loader shared with that era's gserver reads `weapons.txt`, `accountslist.txt`, and, if present, `accounts.txt` (that file is removed after import). Each account file is `accounts/acc` plus the file number from the list. **[src][bin]**

`accountslist.txt` is one account per line: length-prefixed name, length-prefixed password, a flag byte, and a three-byte file number. The flag byte is bit 0 only-load, bits 1–3 admin level, bit 4 blocked. **[src]**

`accounts/accN.txt` is the blob `account13.py` parses: name, password, property list, the same flag byte, two unused zero counts, weapons, action flags, opened chests. The property list is a sequence of `id + 32` and a value. The leaderboard ids used here are nickname (0), max hearts (1), rupees (3, three 7-bit bytes), kills (27), deaths (28), online seconds (29) and alignment (32). **[src]**

## What it shows

A green page (`#009933`, background `image/fond2b.gif`) and a table 410 pixels wide. The header cells are Place, Name, and the mode title. Each data row is the place in red, the nickname, and the value in black. An empty nickname is left blank. At most 50 rows. **[bin]**

Skipped before ranking: an account with the only-load flag set, and the account whose name is exactly `super`. **[bin]**

## What it never sends

No socket, so no login and no list request. The HTML does not include the password or the account file number. The script only redirects standard output into those HTML files. **[bin][file]**
