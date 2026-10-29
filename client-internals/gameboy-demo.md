# Graal Game Boy Color demo (1999)

Date: 2026-10-29

This note covers the full disassembly of `Graal V1.1 Adventure Demo (PD) [C].gbc` (262,144 bytes, MD5 2b2fef91…, the same bytes as `graal.gb` in `graalgb.rar`).
The first look at this ROM is in `precursors-and-fan-builds.md`.

The disassembly itself is in the project's shared folder under `graal-decompile/gameboy-demo/`, not in this repo. That folder holds RGBDS-syntax sources for all 16 banks, the graphics as `.2bpp` files, PNG renders of every room, the scripts that produce them, and a README.
The sources reassemble to a byte-identical ROM. That was checked with a small assembler written for this job; RGBDS itself was not run.
This note is cleaned: it has no code and no code addresses. ROM locations are given only where they describe a data format.
Nothing was run in an emulator, so the behaviour below comes from reading the code.

## What it is built with

- **GBDK 2.x and its LCC C compiler.** The start-up code is GBDK's crt0: interrupt handler chains, the `.mode` table, `add_VBL` and the rest. The game code has LCC's fingerprints: arguments on the stack, `switch` statements as jump tables, and `int` constants read from a per-bank constant pool.
  Of 161 functions, 41 are GBDK library or crt0 routines (`set_bkg_data`, `set_win_tiles`, `set_sprite_palette`, `joypad`, `memcpy`, `arand`, the multiply and divide helpers and so on). The other 120 are the game.
- **Everything runs in the VBlank interrupt.** `main` sets up the screen, loads room 0, installs one VBlank handler with `add_VBL`, turns on sound, switches the CGB to double speed and returns. From then on crt0 just idles. The handler does one game tick: OAM DMA, scrolling, the window slide and music on every VBlank, and the game logic on every second one (about 30 Hz).
- **Banking.** One helper writes the MBC1 bank register and remembers the bank. Code in banks 1 and 3 is reached through small bank-0 wrappers that switch, call and switch back.

## Header and bank map

The cartridge type is `$02` (MBC1+RAM), but the RAM size byte is 0. The CGB flag is `$80`, so the ROM runs on both models. Only banks 0 to 5 hold anything. Banks 6 to 15 are all `$FF`.

| Bank | Contents |
|---|---|
| 0 | crt0, the GBDK library, and the core game: room loader, input, text box, Select menu, collision, the VBlank tick |
| 1 | Entity update and AI, entity drawing, lifting and throwing, camera, the music player and its note table |
| 2 | Graphics: two tilesets of 256 tiles, the 82-tile font, walk bitmaps, five BG palette sets, animated tiles, 172 sprite tiles |
| 3 | Objects (lifted and thrown things), sound effects, entity set-up, sprite sorting, two AI routines, the character table with heads, palettes and names |
| 4 | Room pointer table and rooms 0 to 4 |
| 5 | Rooms 5 and 6 |

## Screen and coordinates

- A room is exactly one 32×32-tile BG map, which is 256×256 pixels. Nothing is streamed: the loader writes the whole map to VRAM, and the camera scrolls over it.
- Positions are 16-bit values in half pixels. A map tile is 16 units (8 pixels).
- Directions are numbered 0 up, 1 left, 2 down, 3 right. That is the same order as the PC client.
- The window layer holds the text box and the Select menu, and slides up from the bottom of the screen.
- Sprites are 8×16. The game builds them in a WRAM buffer, sorts them by Y, and copies them to the DMA page every tick.

## Room format

Bank 4 starts with a table of seven 16-bit header pointers. Rooms 0 to 4 are in bank 4 and rooms 5 and 6 in bank 5; the loader picks the bank as room / 5 + 4.

**Header (13 bytes):**

| Offset | Size | Field |
|---|---|---|
| 0 | 2 | map pointer |
| 2 | 1 | tileset (0 outdoor, 1 indoor) |
| 3 | 1 | BG palette set (0 to 4) |
| 4 | 1 + 2 | link count, link list pointer |
| 7 | 1 + 2 | text count, text list pointer |
| 10 | 1 + 2 | NPC count, NPC list pointer |

- **Map:** 1,024 tile ids, then 1,024 CGB attribute bytes (palette, VRAM bank, flips), both 32×32. The loader keeps two WRAM copies of the tile ids: one as loaded and one that changes when things are lifted. Collision reads the second one.
- **Link (8 bytes):** x, y, width, height, new x, new y, then the target room as a 16-bit number. A new x or y of −1 keeps the player's coordinate. This is the PC client's link record (`file x y w h newx newy`), with a room number in place of the file name. The player's tile is tested against the rectangle on every step.
- **Text (4 bytes):** x, y and a pointer to a zero-terminated string. A text at (0, 0) is never read from the map; NPCs and events show it by index. Signs are read only while the player faces up and the tile above is solid.
- **NPC (16 bytes):** x and y in tiles, direction, character type, two unknown bytes, a text index (−1 for none), five movement bytes (a mode, then patrol bounds), a 16-bit flag word whose eleven low bits are copied into separate entity fields, and a 16-bit event number.
  Flag bit 0 makes the NPC turn to face the player and chase once lined up. The other flags are still unknown.
- **Event 1** is the only event in the demo, on the captive in room 4. It is a timed script that counts down a timer in the entity. The captive walks a few steps, stops, lifts the stone in front of it, turns and throws it, and then text 1 opens ("Now press Select…"). While it runs, the player is held in the lower part of the room.
- **Walk bits:** each tileset has a 256-bit walkable bitmap in bank 2, plus a second 256-bit set that the object code reads when something is put down. What that second set means is not settled.

## The seven rooms

The six outdoor rooms form a 2×3 grid. Room 1 is the inside of the house in room 6.

```
 room 4 (captive)   room 6 (house, "That's your house!")
       |                    |
 room 3 (two chasers) room 5 ("Hello!")
       |                    |
 room 0 (start) ---- room 2
```

| Room | Tileset | Links to | NPCs (character type) | Texts |
|---|---|---|---|---|
| 0 | outdoor | 2 (east), 3 (north) | – | a sign: "Welcome to Graal! Demo version by Stefan Knorr" |
| 1 | indoor | 6 (the door) | – | – |
| 2 | outdoor | 0 (west), 5 (north) | Ryu | – |
| 3 | outdoor | 4 (north), 0 (south) | Pach Soldier, Squall | – |
| 4 | outdoor | 3 (south) | Fung Si Yun (the captive), event 1 | the captive's two texts |
| 5 | outdoor | 2 (south), 6 (north) | Mandi, Lunar, Mandi | "Hello!" (all three NPCs) |
| 6 | outdoor | 5 (south), 1 (the house door) | Vincent, Squall | a sign: "That's your house!" |

The "Welcome to Graal" text is an ordinary sign in the first room, not a title screen. There is no title screen: `main` goes straight to room 0.

Room 4's texts, as the 18-character lines lay them out:

> Thanks for freeing me! I will follow you and help you completing your task. But first let me show how to lift stones! Press A to lift, A again to throw!
>
> Now press "Select" and switch to "Fung Si Yun"

PNG renders of all seven rooms with their real palettes, and of the whole grid, are in the shared folder under `png/`.

## Text

- The text box is three lines of 18 characters at the bottom of the screen. The strings are padded with spaces so that words break at the right places.
- A new press on the d-pad while the box is open shows the next three lines. After the last page the box closes.
- Character codes: `0x20` space, `0x21`–`0x3A` A–Z, `0x3B`–`0x54` a–z, `0x55`–`0x5E` 0–9, then punctuation (`0x5F` "!", `0x62` ".", `0x63` ",", `0x67` used both as an apostrophe and as a quotation mark). The tile drawn is the code minus `0x20`; the font sits at tile 0 of CGB VRAM bank 1.

## Characters

Bank 3 holds a table of 31 character types. Each type has a name, three CGB OBJ palettes and a 16×16 head with two frames. Several types reuse another type's head with new colours.

| # | Name | # | Name | # | Name | # | Name |
|---|---|---|---|---|---|---|---|
| 0 | Fung Si Yun | 8 | Zoraas | 16 | Oldman | 24 | Green Pach |
| 1 | Pach Soldier | 9 | Mad Max | 17 | Gold Soldier | 25 | Blue Lizard |
| 2 | Ninji | 10 | Pachukite | 18 | Gold Squall | 26 | Fire |
| 3 | Lunar | 11 | Matt | 19 | Gold Zoraas | 27 | Silver |
| 4 | Squall | 12 | Brandon | 20 | Gold Max | 28 | Theif (sic) |
| 5 | Vincent | 13 | Bob | 21 | Gold Matt | 29 | Red Squall |
| 6 | Mandi | 14 | Athena | 22 | Gold Silver | 30 | Water Athena |
| 7 | Ryu | 15 | Lizardon | 23 | Red Max | | |

Recoloured heads: Gold Soldier and Green Pach use Pach Soldier's head; Gold Squall and Red Squall use Squall's; Gold Zoraas uses Zoraas's; Gold Max and Red Max use Mad Max's; Gold Matt uses Matt's; Blue Lizard uses Lizardon's; Water Athena uses Athena's; Gold Silver uses Silver's.

These names are the character types of the demo, not only baddies. NPCs in rooms pick one by number, and so does the player.

- The player starts as type 0. Fung Si Yun, the captive in room 4, is type 0 too.
- **Select** opens a carousel in the window that shows three heads and the name of the middle one. Left and right turn it, and each step changes the player's own character type by one, wrapping through all 31.
  So the Select menu, as coded, is a free character picker over every type. It is not limited to the companion that the room 4 text mentions.

## Entities

- There are at most eight entities. Entity 0 is the player and the rest come from the room's NPC list. Each one is 50 bytes.
- Fields that are understood: position, character type, direction, text index, event number, state, animation frame, OBJ palette, movement mode and bounds, a timer, a knock-back velocity, and the id of a carried object (−1 for none).
- States: 0 idle, 1 walking, 2 reading a text, 3 swinging the sword, 4 knocked back, 5 chasing the player, 8 carrying, 9 lifting.
  The update routine dispatches on the state. Movement mode 1 is a random walk; modes 2 to 4 patrol inside bounds kept in the record, and their exact rules were not worked out.

## Player controls

| Button | Effect |
|---|---|
| D-pad | Walk; turn the page in a text box; turn the Select carousel |
| A | Lift the bush or stone in front, or throw what you carry |
| B | Sword, unless carrying |
| Select | Open or close the character carousel |
| Start | Toggle music |

Lifting works on 2×2 map objects. The game looks two tiles ahead and compares the object's top two tile ids with a list of four liftable kinds: three kinds of bush and stone, and a dropped object.
For the first three it writes that kind's "lifted" 2×2 tiles into the map; for a dropped object it puts back the room's original tiles. The player goes into the lifting state, then carries the object as a sprite.
A thrown object is tracked as an object of its own. Where it comes down, it seems to be drawn back into the map as a dropped object, which can be lifted again.

## Sound

- There are eight one-shot sound effects on the two pulse channels and the noise channel. They are skipped while music plays.
- A music player is in bank 1, with a 72-entry table of note periods. **Start** turns it on and off.
- The player enables cartridge RAM before it reads, and its one song pointer is `$A000`, the start of cartridge RAM. The header declares no RAM, and nothing in the ROM writes to that area. So the demo carries no song of its own, and what Start plays depends on whatever answers at `$A000`.
  This is a static reading. It may be a leftover from a development cartridge that had a song loaded into its RAM.

## Compared with the PC client

- The same link record: a rectangle plus a new x and y, with −1 to keep a coordinate.
- The same direction numbers, and the same lift, carry and throw of 2×2 bushes and stones with A. Here the liftable objects are a fixed list of tile pairs.
- Rooms are fixed 32×32-tile maps, not 64×64 levels. Positions are in half pixels, and there is no NPC scripting: NPC behaviour is a few built-in movement modes, flags and event numbers.
- The text alphabet is a straight ASCII-like run, not the PC sign alphabet.

## Open

- The music data format, since no song is in the ROM.
- Several entity fields and most NPC flag bits.
- The patrol rules of movement modes 2 to 4.
- Whether the Select carousel was meant to stay a free picker in a later version.
