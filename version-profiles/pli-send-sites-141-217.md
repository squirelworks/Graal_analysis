# Client-to-server send sites, 1.41r1 to 2.17.1: are the lists complete?

Date: 2026-11-13. Static read of 21 Windows Delphi clients. No build was run. Every finding here is **[bin]**.

Manual §2.4.2 lists the ids each build can send, but marked the 1.41r1 to 2.17.1 rows `unmeasured` in the *Complete?*
column. The earlier scans counted only sends whose id is a constant. A send that passes the id in a register, or a send
from outside the network unit, would not have been counted. This note checks both.

## Method

- In every build of this family the network unit holds the server, the listserver client, the game client
  (`TAdventureClient`) and a web client. The game client's send routine is slot 1 of its virtual method table. It takes the id
  in the second argument register and the payload string in the third, adds the id byte and the newline, and applies the
  insertion cipher.
- **Inside the unit:** every call through a virtual slot 1, and every direct call to the send routine, was listed. For each,
  the instruction that last set the id register was read. Calls to other classes' slot 1 in the same unit were kept too; a
  call that does not pass a constant would show up either way.
- **Outside the unit:** the game client stores itself in a few globals when it is created. Every slot-1 call elsewhere in
  the program was checked for an object loaded from those globals, or from the pointer cells that point at them.
- Calibration: on 2.05 rev2 the method gives 0–24, 26–30, 32–38, 80 and 81, the set `protocol/player-props.md` and
  `protocol/packet-ids.md` already give for 2.05.

## Result

**Every game-client send passes a constant id.** In all 21 builds there is no call inside the unit that passes the id in
a register, and no call from outside the unit sends through the game client. The one outside call that loads the client
global reads a stream (a buffer and a length), not a send. Ids 0, 30 and 33 have two send sites each (2.17.1 has one
for 30); every other id has one.

| Build | Ids sent | Same as manual §2.4.2? |
| --- | --- | --- |
| 1.41 rev1 | 0–24, 26–30, 32, 33, 80, 81 | yes |
| NewMain 24, NewMain 26, 2.00, 2.00 rev1–rev3 | 0–24, 26–30, 32–34, 80, 81 | yes |
| 2.01, 2.01 rev1, 2.02, 2.02 rev1 | 0–24, 26–30, 32–36, 80, 81 | yes |
| 2.02 rev2 | 0–24, 26–30, 32–37, 80, 81 | yes |
| 2.03, 2.04, 2.05, 2.05 rev1, 2.05 rev2, 2.1 test 2, 2.1 test 3 | 0–24, 26–30, 32–38, 80, 81 | yes |
| NewWorld beta 1, beta 2 | 0–6, 9, 10, 12–14, 18, 19, 21–24, 26–30, 32–38, 80, 81 | yes (Claim A of App. E#11) |
| 2.17.1 | 0–24, 26–30, 32–41, 43–45, 80, 81 | yes |

So the lists in §2.4.2 for these builds are complete, not floors. The sends to the listserver (through the listserver client
class) are not part of these lists.

## NewWorld betas: ids 8 and 20 (App. E#11)

The two NewWorld betas send neither 8 (`PLI_HORSEDEL`) nor 20 (`PLI_OPENCHEST`):

- No send site in the network unit passes 8 or 20, and there is no register send that could.
- A raw byte search of the whole executable finds no `mov` of 7, 8, 11, 15, 16, 17 or 20 into the id register followed by
  a slot-1 call. The same search on 2.1 test 3 finds one site for each of those seven ids.

This sides with Claim A (the 2.1 test set without 7, 8, 11, 15, 16, 17 and 20, so 32 ids). Claim B's 34 ids is wrong. It
fits the receive side: the betas also have no handler for the server's chest (4) and horse (17, 18) messages
(`client-internals/decomp-findings-2026-10-24-c/08-test-builds-newworld-newmain.md`).

## Limits

- Static only. A lab run would show which of these ids a client really sends in play, not whether others exist.
- The 1.39 and older builds (§2.4.2 rows marked *floor* or "a few register sends uncounted") were not re-read here.
- 6.01r1 is a C++ build with a different send path. Its row stays open.
