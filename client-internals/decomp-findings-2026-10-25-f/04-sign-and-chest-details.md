# Signs and chests in the corpus

- 2381 signs in 808 levels; 684 sit at (0, 0) (dialogue text kept by index, as `level-binary-client.md` guessed).
- 498 `#K(n)` escapes with n not 13, the commonest n values being 95 (`_`), 164, 61 (`=`), 42 (`*`), 36 (`$`), 64 (`@`), 94 (`^`), 124 (`|`), 134, 233, 169, 43 (`+`). Characters missing from the 97-entry table are written this way, as `sign-text.md` says.
- 375 chests in 88 levels. Item indexes seen: 0 to 11, 16, 17, 19, 24, and one 78 (outside the 25-name table). 343 of the chests have sign index -1 (byte `0x1F`), which is "no sign".
- The old Seihai decoder (`char + 89`) lost punctuation and line breaks; it is replaced by the alphabet decoder.
