# Offline save games after 1.41r1: none

Date: 2026-11-13. Static read of the Windows clients. No build was run. Every finding here is **[bin]**.

Manual §1 lists which save-game magics each build reads and writes. Up to 1.41 rev1 the clients read `Graalsav9`,
`Graalsv10` and `Graalsv11` and write `Graalsv11` (`client-internals/build-catalogue.md`, `formats/graalsav.md`). The rows
for NewMain, 2.00 to 2.04 and 2.05 on were unmeasured.

## Method

Each executable was searched for the three magics (the full `Graalsav` and the shortened `Graalsv` spelling), for the
`Load game (F2)` menu caption and for the open-dialog filter `Graal save games (*.gsave, *.save)`.

## Result

| Build | Save magics | Load-game menu | Save-game dialog filter |
| --- | --- | --- | --- |
| 1.41 rev1 | `Graalsav9`, `Graalsv10`, `Graalsv11` | yes | yes |
| NewMain 24, NewMain 26 | none | no | yes |
| 2.00 | none | no | yes |
| 2.00 rev3, 2.01, 2.02, 2.02 rev2, 2.03, 2.04 | none | no | no |
| 2.05, 2.05 rev2, 2.1 test 3, NewWorld beta 1 and 2, 2.17.1 | none | no | no |

No build after 1.41 rev1 can read or write a save game. NewMain and 2.00 keep only the dialog's filter string, a leftover in
the form resource with no menu entry to open it; it is gone by 2.00 rev3. Offline save games end with the 1.4x line.

## Limits

- GraalX was not read; its row stays open.
- A string search cannot rule out a magic built from single characters, but every earlier build stores it as a string, and
  the menu entry is gone too.
