# Static reads for Appendix E (2026-11-19)

Date: 2026-11-19. Evidence: **[bin]** (a disassembler read of the real client executables on the
Mirae lab, with no client run). Only behaviour is given here. Covers App. E#306, E#608, E#620,
E#328, E#307, E#10 and E#323. The probe-offset table that several of these lean on is in
[link-probe-offsets-205-222-2026-11-19.md](../protocol/link-probe-offsets-205-222-2026-11-19.md).

Builds read: 2.05 rev 2 `Graal.exe` (2.0.5.2), Windows 2.22 (`Graal_222.exe`), 1.41 rev 1, 1.39,
the 2.1.0.0 to 2.1.0.4 images and 2.17.1.

## Pull sound (E#306, 2.05)

- The choice between `lift.wav` and `lift2.wav` reads a byte of the object being lifted or pulled,
  not a player flag.
- A non-zero byte plays `lift.wav`, and zero plays `lift2.wav`.
- So the sound belongs to the object. The earlier note's "player flag" was wrong about the owner.
  What the byte means for each object kind was not traced.

## `arrays.dat` lists in the old-mode walk test (E#608, 2.05)

- The loader reads 25 lists.
- The old-mode passability test checks the tile against list 0 and, if that misses, against
  list 1. No other list is used by this test.
- This confirms Claim B (lists 0 and 1). Claim A (list 0 only) dropped the second list.

## Program check (E#620, 1.41 rev 1)

- The handler belongs to a stock Delphi self-integrity component, TProgramCheck 1.1.
- On a failed check it shows "This program has been modified either by a virus or by a transfer
  problem. It will terminate now." and a "The Graal execution file is corrupted" message, then
  ends the client.
- The component's own warning text says a check that is active but "was not processed by
  stamp.exe" has nothing to compare against. The copy whose event goes straight to its final
  return is consistent with a build that was not stamped, so its check does nothing.

## Tick source (E#328, 2.22)

- 2.22 imports no multimedia-timer functions (no `timeSetEvent` or `timeKillEvent`).
- It does import the window-timer call (`SetTimer`, which drives `WM_TIMER`) and the clock reads
  `timeGetTime`, `QueryPerformanceCounter` and `GetTickCount`.
- So the 50 ms step is not a multimedia timer. It runs either from a window timer or from the idle
  handler behind a clock gate. This pass did not decide which, and a lookup by name at run time
  was not ruled out.

## 1.39 movement (E#307)

1.39 holds the same 64-byte per-facing probe-offset block as 2.05 and 2.22, byte for byte. Its
six-probe and nudge step tables were not extracted separately.

## Gmap code in the 2.1 builds (E#10)

The gmap machinery, including `loadgmaps.txt`, is absent from the 2.1.0.0 to 2.1.0.4 images and
present in 2.17.1. So the `maps` download rule arrived after 2.1.0.4 and by 2.17.1, along with the
gmap work. 2.12 to 2.16 are still missing, so the exact build cannot be named.

## 2.22 level-object code (E#323)

- The 2.22 movement probe table is byte-identical to 2.05's.
- The 2.22 carry, throw and take-player-carry logic sits in one large script action dispatcher.
- The individual throw, cut-lift and drop routines were not compared one by one.
