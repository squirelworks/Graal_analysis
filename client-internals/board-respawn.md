# Bush, pot and stone respawn: who restores the board, when, and who drops items

Date: 2026-10-30

How cut bushes and grass, lifted bushes, signs, pots (vases) and stones, and other board changes come back, and where the rupees and hearts they drop come from. Covers the 1999 GServer13 (shipped with 1.3 test), the 1.3 test client, the 2.05 rev 2 client, and the GServer-v2 lab server.

Tags: **[bin]** read from the binary · **[live]** measured with the real program under Wine (`tools/respawn-lab/`) · **[cap]** earlier lab capture (`protocol/packet-layouts.md`) · **[src]** GServer-v2 source · **[doc]** the official `newfeatures*.txt` / `readme.txt` · **[inf]** inferred.

## Summary

| | 1.3 era (GServer13 + 1.3 client) | 2.00 to 2.05 (client) | GServer-v2 lab server |
|---|---|---|---|
| Who restores a cut or lifted object | Server only | Server only | Server only |
| Clients regrow anything on their own | No | No, offline nothing ever comes back **[live]** | n/a |
| Which changes respawn | Any change that is exactly **2 × 2** **[bin][live]** | n/a | A change whose top-left tile was one of 11 listed ids **[src]** |
| Timer | `trunc(R·rand·0.5 + 0.75·R)` one-second ticks, R = `respawntime`, default **10**, so 6 to 12 s **[bin][live]** | n/a | Exactly `respawntime`, default **15** **[src][cap]** |
| Restore packet | `PLO_BOARDMODIFY` (7) with the old tiles, to everyone in the level | handled as any board modify | same |
| Sender gets its own change echoed | No **[bin][live]** | n/a | Yes, to the whole level **[cap]** |
| Item drops from bushes and pots | **Client**, local random roll, sent peer to peer **[bin]** | **Server** ("bush rupees and pot hearts are server-side", v2.00 **[doc]**). The 2.05 cut and lift code spawns no item **[bin]** | Server, 50 % of 6 items for bushes, a heart for a vase **[src]** |

## The objects

The tables are `arrays.dat` lists. They are the same in 1.21, 1.3 test and the 2.22 install (2.05 runs from that folder) **[bin]** (`tools/respawn-lab/arrays_dump.py`). In 1.21 they sit one index lower because 1.21 has 24 arrays, not 25.

**Cut with the sword:**

| # | Object | Tiles (2 × 2, top row then bottom row) | Leaves |
|---|---|---|---|
| 0 | bush | 2 3 / 18 19 | 677 678 / 693 694 |
| 1 | tall grass | 420 421 / 436 437 | 679 680 / 695 696 |

**Lift with A**, in glove order (name table in the 2.05 exe: `bush sign vase stone blackstone`):

| # | Object | Tiles | Leaves |
|---|---|---|---|
| 0 | bush | 2 3 / 18 19 | 677 678 / 693 694 |
| 1 | sign | 512 513 / 528 529 | 1802 1803 / 1818 1819 |
| 2 | pot (`vase`) | 684 685 / 700 701 | 1770 1771 / 1786 1787 |
| 3 | stone | 34 35 / 50 51 | 1834 1835 / 1850 1851 |
| 4 | black stone | 990 991 / 1006 1007 | 1834 1835 / 1850 1851 |

Glove power g allows the first g + 2 lift entries (`decomp-findings-2026-10-25-l/03-cut-lift-chest.md`). Players start at glove 1, so the pot lifts with no glove item.

A thrown object does not touch the board when it lands. It breaks into leaves (`TAdventureLeap`, `crush.wav`, or `water.wav` for entry 5). The board change happens once, at the lift. Respawn therefore puts the object back where it was lifted, not where it landed.

"Swamp" is not a destructible object. It is tile type 6 (and 7, lava swamp) in the tile-type list (`newfeatures2001.txt`, `setshape2`). GServer-v2's comment "Bushes, grass, swamp" refers to its own tile list, not to a third cut type.

Push and pull blocks are different again. The 2.05 client sends the 4 × 4 area around the old spot (`ledges-push-pull.md`). GServer13 never respawns that (see below).

## Clients

### No client-side respawn

**2.05 rev 2, offline, live.** Level `resp1.nw` (made with `tools/respawn-lab/mklevel.py`) was played with the real client under Wine, and both 64 × 64 boards in its memory were polled every 10 ms for 10.5 minutes (`boardwatch.py`).

- Sword on a bush: tiles 2 3 18 19 became 677 678 693 694 at once.
- A on a pot: 684 685 700 701 became 1770 1771 1786 1787.
- A second bush was cut later.
- No tile changed back in the whole run, 633 s after the pot was lifted.

The client has a `TBoardModify` class, but it is only a record built to send one change (`x, y, w, h`, tile array). It has no timer **[bin]**. The 1.3 client is the same: its `TBoardModify` users are the cut and lift sender, the push and pull code, and one other board-write path, and none of them keeps a timer **[bin]**.

So a cut bush stays cut until the level is loaded again. Whether 2.05 offline reloads the level from disk on re-entry was not tested here.

### Sending the change

- **2.05:** cut and lift both call one routine. It writes the leftover tiles to the board, then, only when online, sends `PLI_BOARDMODIFY` (1) with `c x, c y, c w, c h` + w × h GSHORT tiles. It sends nothing if the tiles were already equal. Cut then adds the leaves effect **[bin]**.
- **2.04+ (2.05 checked):** the whole 2 × 2 has to match a table entry before anything happens. 1.3 matched the single tile under the sword tip and wrote the leftover block at the derived corner **[bin]**. This is the 2.04 change "check for correct tiles when lifting/eating/slaying bushes" **[doc]**.
- **2.05:** "bombs don't destroy half bushes" **[doc]**.

### Item drops in 1.3 (client-side)

Drops are rolled by the client that cut or lifted the object **[bin]**:

| When | Drop |
|---|---|
| Bush cut, bush lifted, or bush destroyed by a blast routine that walks both tables (probably bombs **[inf]**) (entry 0 only, not tall grass) | `Random(100)`: 0–24 green rupee (25 %), 25–26 blue rupee (2 %), 27–31 heart (5 %), 32–36 bombs (5 %), 37–99 nothing (63 %) |
| Pot lifted, or destroyed by that blast routine (lift entry 2) | A heart, every time |

- **Timing:** the drop happens at the lift, not when the thrown pot breaks.
- **Item flags:** items are created with flag value 164 and the "announce" flag set.
- **When online:** the client sends the new item straight to the other players over UDP (`sendto` each peer), as id 19, with `chr(x·2+32) chr(y·2+32) chr(item+32)`. Only item kinds marked in a per-item table are sent. The GServer does not take part. The board change itself still goes to the server over TCP (id 1).

### Item drops from 2.00 on (server-side)

- **2.00:** "bush rupees and pot hearts are server-side" **[doc]**.
- **2.05 binary:**
  - The cut routine creates only `TAdventureLeap`.
  - The lift routine creates only the carried object.
  - The only `TAdventureExtra` constructor is reached from the chest code, a weapon-drop path, one network handler (most likely `PLO_ITEMADD` **[inf]**) and the GS1 executor. None of these is the cut or lift code.
  - So **an offline 2.05 bush or pot gives nothing**, and online every drop is a `PLO_ITEMADD` (22) from the server **[bin]**. The capture in `packet-layouts.md` shows the same thing: no client sent `PLI_ITEMADD` and the server sent the drops **[cap]**.
- **Not covered:** a 2.x-era official GServer binary is not in the archive. The real 2.x drop rates are unknown, and only GServer-v2's rates are written down.

## GServer13 (November 1999, GSERV014)

### Options

`serverconfig.txt` keys and the start dialog (screenshot-checked, defaults filled in):

| Key | Dialog label | Default |
|---|---|---|
| `respawntime` | Respawn time (bushes etc.) in sec | 10 |
| `horselifetime` | Horse lifetime in sec | 10 |
| `apincrementtime` | Alignment increment time in sec | 1200 |
| `baddyrespawntime` | Baddies respawn time in sec | 60 |

GServer 1.28 beta 2 (`GServerv.exe`) has the same four keys.

### `PLI_BOARDMODIFY` (1) handling **[bin]**

1. Needs at least 4 bytes and a current level, and `len ≥ 4 + 2·w·h`.
2. Writes the new tiles into the server's 64 × 64 board and builds the old-tile string from what was there.
3. If any tile changed:
   - Relays `PLO_BOARDMODIFY` (7) with the client's bytes to every other player in the level. **The sender is skipped.**
   - Makes a change record: new tiles, old tiles, a countdown and a reference count.
   - **If w = 2 and h = 2:** countdown = `Trunc(Random · R/2 + 3R/4)` with R = `respawntime`, and the record joins the level's respawn list.
   - **Any other size:** countdown −1, so it never respawns. This covers 1 × 1, 2 × 1, 3 × 3 and the 4 × 4 push/pull block.
   - The record is also added to the "changed since you left" list of every player who has left this level since loading it. Any earlier record with the same `x, y, w, h` header is replaced.
4. **No tile check.** Any 2 × 2 change respawns, whatever the tiles. A client can blank a 2 × 2 of floor and it comes back.

### Respawn tick **[bin]**

- `Timer1` (TTimer default interval, 1000 ms) walks every loaded level, empty or not, and decrements each countdown.
- At < 1, the server:
  - removes the record;
  - sends `PLO_BOARDMODIFY` (7) with the **old** tiles to everyone in the level, the original sender included;
  - writes the old tiles back into its board;
  - updates every "changed since you left" list. If the list still holds the original change, it is dropped, because that player never saw it. If not, the restore is queued instead.
- **Timing:** the countdown starts at an integer n in 7..12 for R = 10, and the first tick comes 0 to 1 s after the change. The restore therefore lands n − 1 to n seconds later.
- **Weights:** n = 7 and n = 12 are half as likely as 8 to 11, because of the truncation of [7.5, 12.5).

### Measured **[live]**

GServer13.exe ran under Wine in a loopback-only namespace with one load-only account. Two scripted clients (`g2cli.py`) were used: A sends changes and B watches.

| Test | Result |
|---|---|
| 2 × 2, 60 positions, one every 0.37 s | All 60 respawned. Delays 6.21 to 11.98 s, mean 9.21 s. ceil(delay) 7/8/9/10/11/12: 4, 9, 16, 11, 12, 8 (expected 6, 12, 12, 12, 12, 6). |
| 1 × 1, 2 × 1, 1 × 2, 3 × 3, 4 × 4 | Relayed to B at once, never respawned (watched 20 s past the 2 × 2 respawns) |
| Echo | A never received its own change. A and B both received every respawn. |
| Restored tiles | The level's original tiles (632 for `house1.graal` floor), not a fixed "bush" id |

Raw rows: `version-profiles/lab-gs13-respawn.tsv`.

### Level re-entry **[bin]**

- **On leave:** the server starts a per-player change list for that level.
- **On re-entry:**
  - If there is no list, the client gets the level as on a first visit.
  - Otherwise only the queued changes go out (as id 0), and the list is dropped. **[bin]**, the branch is hard to read, so treat the exact packet as **[inf]**.
- **Effect:** a player who leaves while bushes are cut and comes back after they regrew is sent nothing for them.
- **Disconnect:** the player's lists are freed.

## GServer-v2 (lab server) **[src]**

This is the open reimplementation used for the 2.05 and 2.22 captures. It is not an original server.

- **Respawn condition:**
  - The top-left tile *before* the change must be one of `0x1ff 0x3ff 0x2ac 0x002 0x200 0x022 0x3de 0x1a4 0x14a 0x674 0x72a`. Those are bush (2), tall grass (420), pot (684), sign (512), stone (34), black stone (990), and five others.
  - Then the change respawns after exactly `respawntime` (default 15).
  - Otherwise it is kept with no timeout.
- **Size:** any size can respawn.
- **Overlap:** a new change deletes stored changes it fully covers.
- **Echo:** relays `PLO_BOARDMODIFY` to the whole level, sender included.
- **Restore:** swaps old and new tiles. It keeps the record, so late joiners get the restored state.
- **Drops:** only for clients at the 2.1 version slot or above.
  - **Bush, grass or swamp tiles** (2, 0x1a4, 0x1ff, 0x3ff) with `bushitems`: `tiledroprate` % (default 50) of the time, item `rand() % 6`.
  - **Pot** (0x2ac) with `vasesdrop`: a heart.
  - **Why 2.05 got drops in the lab:** the lab maps `GNW03081` (2.05) into the 2.1 slot (`tools/lab-setup.md`), which is why the earlier capture shows server drops for 2.05.
- **Push-pull blocks:** a 4 × 4 change made of a red or blue push-pull stone is refused and the board is sent back when `clientsidepushpull` is on.

## What a Seihai version profile should do

| Profile | Respawn | Drops |
|---|---|---|
| 1.x online (GServer13-style) | Server, any 2 × 2, `trunc(rand·R/2 + 3R/4)` s on a 1 s tick, R = 10 | Client rolls the 1.3 table (above) on cut/lift/blast of a bush, a heart for every pot. Announce to peers, not the server. |
| 1.x offline | None | Same client table |
| 2.00–2.05 online | Server pushes `PLO_BOARDMODIFY`. Client never regrows. | Only `PLO_ITEMADD` from the server |
| 2.00–2.05 offline | None | None |
| Seihai's own server | Pick per profile: GServer13 (random 0.75–1.25 × R, 2 × 2 only, no echo) or GServer-v2 (fixed R, tile whitelist, echo) | |

## Open

- The real 2.x GServer's timer, tile whitelist and drop rates. No binary of a 2000–2002 official server has been found.
- Whether 2.05 offline reloads a level from disk on re-entry, which would make a cut bush come back.
- Drop tables in 1.21 and 1.39 to 1.41: same routine shape expected, not read.
- Later clients (2.2+ `updateboard2` / `PLO_BOARDMODIFY2` on gmaps, v4+). Not covered here.

## Lab notes

- **2.05 offline:** `tools/respawn-lab/mklevel.py` writes a level with every object in a row. `boardscan.py` finds the board copies in client memory. `boardwatch.py` logs every tile change with a timestamp. Keys: `xdotool keydown Up`, `s` for sword, `a` for lift. The Wine screen often stops repainting tiles after a few actions, so trust the memory log.
- **GServer13:**
  1. Extract `graal13b.7z` and start `GServer13.exe` under Wine inside the namespace.
  2. Press OK on the options dialog.
  3. Edit accounts, then Guest Accounts, then Add: name `guest`, password `guest`, load only, level `house1.graal`.
  4. Run `gs13_respawn.py out.jsonl 60` inside the namespace.
