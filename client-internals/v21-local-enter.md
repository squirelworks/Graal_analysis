# Local-enter arguments on the public 2.1.0.0 image and on v22

Date: 2026-11-15. Static read of the local-level enter path in the public 2.1.0.0 image and in Graal 2002 v22. Nothing was run. No packet was read. ver7's enter body was not this read. The literal `Player enters local level ` is absent from ver7's string table.

## Two values of 31

When the level name is `level1.graal`, `YoshiClanR2.zelda` or `YoshiClanFields.zelda`, both images call a helper with the level and two floating-point values, each 31. What the helper changes was not read. **[bin]**

2.05 runs an extra step for the same three names, and that step is still unread (→ the open row in `manual/app-e-open-questions.md`). This read does not say that 2.05 passes 31.

## v22 shifts a 3 by 3 table by 64

The public enter body has no 3 by 3 walk.

v22, after the level is swapped, walks a 3 by 3 table of earlier level pointers when an integer field equals 2 and further object tests pass. Rows and columns are 0, 1 and 2. A matching slot adds `(row - 1) * 64` and `(column - 1) * 64` to coordinate pairs, so the shifts are -64, 0 and +64. A table with no match clears the coordinate list those shifts would have updated. The integer field was not identified. What writes it was not read. **[bin]**

## Widths beside that call

A header that is not one of `Z3-V1.03`, `Z3-V1.04`, `GR-V1.00`, `GR-V1.01`, `GR-V1.02`, `GR-V1.03` or `GLEVNW01` stores a flag byte and the integer 40, and does not swap the level. Linux 3.04 already stores 40 for that rejection (`torque/304-adventure.md`). On these two images the enter line is logged before the test. No send of 40 was read. **[bin]**

On v22, when the name is not already resident, a second lookup is empty, and the same integer field equals 2, the client writes a stream of exactly eight bytes, `GLEVNW01`, and enters with that stream. Another value of the field does not write the stream. This path sends no packet. **[bin]**

## Open

- [ ] Read the helper that receives the two 31 values, on these images and on 2.05.
- [ ] Find what writes v22's integer field.
- [ ] Read ver7's enter body. The log literal is absent; that does not show the body.
