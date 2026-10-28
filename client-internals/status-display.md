# Status display (HUD)

Date: 2026-10-28

* **Code:** read from the 2.05 rev 2 client's status routine, with two
  constants checked in its executable: the heart-row table and the
  small-heart stagger. **[2.05]**
* **Sheets and picture:** the shipped sheets, and a 2.22 lab screenshot.
  **[cap]**
* **What these notes leave out:** addresses, routine names and decompiler
  text.

## Sheets

* Every build from 1.41 on ships a 224×145 `state.png`.
* The 2.22 sheet matches the 2.05 rev 2 and 2.1 test 3 sheets pixel for
  pixel, except for one 27×14 patch at (190, 60), which the status routine
  does not use.
* 1.41's sheet has three blank buttons side by side at x 158, 180 and 202.
* The 2.0-era NewMain sheets have one button at x 202, which the routine
  draws in all three slots.

## Layout

All positions are measured from the top-left of the game view. The routine
uses a base point of (15, 15).

| Part | `showstats` bit | Sheet rect (x, y, w, h) | Screen position |
|---|---|---|---|
| Rupee, bomb and arrow icons | 0x02 | (80, 33, 120, 16), one strip | (274, 30) |
| Rupee count | 0x04 | digit d = (14d, 81, 14, 16) | 1–7 digits, no leading zeros, 12 px apart, centred on x 280, y 48 |
| Bomb count | 0x08 | same digits | two digits at x 326 and 338, y 48 |
| Arrow count | 0x10 | same digits | two digits at x 374 and 386, y 48 |
| Hearts | 0x20 | big (40·half, 0, 40, 44); small (80 + 31·half, 0, 31, 33) | see below |
| Buttons | 0x01 | (202, 0, 22, 33) | x 15, 80 and 145, y 30 |
| Key names | 0x01 | text | on each button: 26 pt Helvetica, white, with a black copy at +1, +1; smaller sizes for two-letter and longer key names. Key 9 (item list) is drawn small at (147, 27) |
| Glove icon | 0x01 | sprite 145 for power 2; sprite 325 drawn on top for power 3 | (40, 29); power printed at (60, 31) when it is 2 or more |
| Sword icon | 0x01 | sprite 17, taken from the player's sword image | (105, 31); sword power printed at (125, 31) |
| Selected weapon | 0x01 | the weapon's whole image | x 170, vertically centred on y 45 |
| Alignment bar | 0x40 | frame (0, 97, 130, 22); fill (0, 119, AP, 10) | (15, 65); fill at +22, +6 |
| Magic bar | 0x80 | frame (0, 49, 130, 22); fill (0, 71, MP, 10) | (15, 90); drawn only with weapons on and MP > 0 |

Bits 0x100 and 0x200 belong to the player icons and to the stacked weapon
image list, which are drawn by the same routine but are not part of the
status display.

* **Sprite rects.** Sprites 17, 145 and 325 come from the sprite table in
  `arrays.dat` (array 24). The 2.22 file gives:
  * 17: (94, 36, 28, 28), from the sword image
  * 145: (28, 212, 28, 32), from `sprites.png`
  * 325: (0, 212, 28, 32), from `sprites.png`
* **Weapons flag.** The same flag gates the S and D keys. With it off, only
  the first button, its key name and the alignment bar are drawn.

### Hearts

* **Drawing.** One heart is drawn per container while power remains; empty
  containers are not drawn. Power is a value in hearts: heart *i* is full
  when `power − 1 ≥ i` and half when `i < power`.
* **Big hearts.** Used while power is 4 hearts or less. They start at
  (W − 198, 24), 45 px apart, where W is the view width.
* **Small hearts.** Used above 4 hearts, 35 px apart. New rows start at
  hearts 5, 11, 16, 22 and 27. Row *k + 1* is 20(k + 1) px lower and
  shifted `round(17.5(k + 1)) − 35` px sideways. The whole block moves 10 px
  down while power is below 6 hearts.

## Not read

* The 2.22 and 2.31 status routines. Their sheets and the 2.22 picture match
  2.05.
* The routine of any build before 2.05, including how 1.41 uses its three
  button cells.
* The text drawing that prints the glove and sword power: its font, colour
  and anchor.
