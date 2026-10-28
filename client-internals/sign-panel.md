# The sign panel and NPC drawing (2.05)

How the 2.05 client draws a sign while the player reads it, the keys that turn its pages, and what it draws for an NPC whose image is missing. Read from the 2.05 program and checked against the `letters.png` sheets of 1.39 and 2.22. Seihai follows this in `documentation/signs.md`.

## The sheet

`letters.png` is 256×224: 16 glyphs a row, each 16 wide and 32 tall, so glyph `g` is at (`g % 16 × 16`, `g / 16 × 32`). It carries the font, the button pictures and the pieces of the scroll frame. The client loads it once, at start.

Glyph order: a character's glyph is its place in

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!?-.,#>()#####"####':/~&### <####;
```

(then a newline). The `#` places are glyphs with no plain character. Each glyph has its own advance, the client's table of half widths doubled (I is 6 pixels, space 8, most letters 12).

| glyphs | use |
|---|---|
| 96, 97, 98, 99 | frame corners: top-left, top-right, bottom-left, bottom-right |
| 100, 101 | top and bottom edge |
| 102, 103 | left and right edge (32 pixels tall) |
| 91 to 94 | the A, B, X and Y buttons |
| 77 to 80 | the up, down, left and right pictures |
| 71 to 75, 87, 88, 67 | the other button pictures |

The pixels at (252..255, 223) are colours, not art. The client fills the inside of the frame with (254, 223) and, 8 pixels further in, (255, 223), and skips a fill whose colour is the sheet's transparent one. On the 2.22 sheet both are the same cream; on 1.39 the inner one is white.

## The panel

- 24 cells wide and 9 tall (16-pixel cells), centred across the view.
- On a 640-wide view it sits at y 256, or at y 128 when the player is more than 14 tiles down the view. At 800: 18 tiles, y 320 or 160. At 1024: 22 tiles, y 448 or 192. Which two values the client compares is inferred from the code's shape (the player's row against the view's top); the thresholds and positions are as read.
- The frame: the top and bottom edges every 16 pixels, the sides every 32 pixels, the corners over them, then the two fills from (x + 16, y + 24) to the right and bottom pieces.
- Text: three lines a page, from (x + 16, y + 16), 32 pixels apart. The sign's text is split at newlines.
- In a line, `#` and a letter draws button pictures: `#A`, `#B`, `#X`, `#Y`, `#u`, `#d`, `#l`, `#r`, `#h`, `#x`, `#y`, `#z`, `#4`, `#.`. `#` and any other letter draws glyph 86 and moves 16 pixels. `#i` and a character puts up an image from the level's list.
- A character outside the glyph order is drawn by the client in its system font, in the colour at (253, 223).

## Keys while reading

- The action key turns to the next three lines, unless the page on show is not full (the sign has fewer lines than the page's first line plus three); then reading ends. A sign of exactly three lines therefore shows an empty second page before it closes, as in the client.
- The first direction key (Up) turns back three lines, when not on the first page.
- Another key ends reading at once.
- The client plays a sound when the page turns and runs `playerendsreading` when reading ends.

## NPCs with no image

- In game, an NPC with no image loaded draws nothing of its own, only its text if it has any.
- An NPC with a GANI draws the GANI, and a character NPC is drawn the way players are.
- The client's placeholder picture for an NPC with no image appears only in the level editor's view.

## Confirmed, inferred, not tested

- Confirmed from the program: the glyph grid, glyph order and advances, the frame pieces and fill colours, the panel size and line layout, the `#` codes, the paging rule, and the NPC draw rules above.
- Inferred: which two values the panel's height test compares, and that key 0 is Up.
- Not tested against a real client screenshot.
