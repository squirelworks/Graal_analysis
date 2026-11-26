# The 5.12-class client never loads a local `.mis` — the 3D mission comes only over the wire (T3D-010, Linux 4.20r6)

Date: 2026-11-26. Single-client lab on native Linux 4.20r6 (5.12-class, protocol 24, g3d420 route), software GL; file-open trace of a full 3D session. Observation only. Board row: [T3D-010](3d-capability-board.tsv). Confirms the static finding (5.12 has no `.mis` literal and no compiler) with a live run.

## Headline

**The 5.12-class (4.20r6) client does not read a local `.mis`.** The mission arrives **entirely over the wire** as the protocol's phased download. A marker `.mis` pre-placed in every candidate folder was **never opened**, and no `.mis` of any name was opened during a full session.

## Method **[lab]**

Marker `.mis` files were pre-placed in every plausible mission/level location — the client root, `levels/`, `missions/`, the user-home `levels/`, and `levels3d/` — then a full 3D session was run (login → sky+shape scene → idle → quit) with **all file opens traced**.

## Result

- The client opened **zero** `.mis` files. The pre-placed marker was never touched, and no `.mis` of any name was opened.
- The mission came in as the protocol's phased download instead — console shows `Phase 1: Download Ghost Objects` … (the proto-24 handshake), never a local `.mis` read.
- 4.04r2 (protocol 19) likewise takes its mission over the wire (`Download Datablocks` → `Download Ghost Objects`), with no local `.mis` load — consistent, though not separately marker-traced this run.

This matches the static read: the 5.12-class engine carries no `.mis` string literal or compiler, so there is no code path to load one from disk.

## For a server

A 3D mission **must be delivered over the wire**. Dropping a `.mis` next to the client does nothing — no build after 4.04r2 reads a local `.mis`. The mission reaches the client only through the phased ghost/datablock download of the session protocol.

## Method caveat

Single client, our own loopback server, software GL. The negative ("no `.mis` opened") rests on a full file-open trace of one representative session covering every candidate folder; a `.mis` loaded only by some content type the lab server did not emit cannot be excluded, but no `.mis` load path exists in the engine statically.
